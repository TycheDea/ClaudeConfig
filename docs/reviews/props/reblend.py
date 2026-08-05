"""CPU-only, Blender-free reimplementation of proptex/albedo.py's
blend_views (the shipped weighted-mean albedo estimator), plus two
alternative per-texel estimators explored in a prior campaign
(tasks/prop-texture-redesign.md rows 43-45): harmonized WTA (hwta) and a
median variant (med-hwta). Everything is read from the pipeline's on-disk
content-addressed cache (target/prop-cache/{atlas,depth,generate,blend}/
<stage-key>/...); nothing here calls Blender, ComfyUI, or any GPU stage.

VALIDATION FIRST: the "mean" variant must reproduce the candidate's cached
base.png (MAD <= 0.5/255 on covered island texels) before the other variants
are trusted. See run_candidate() / main().

Row-orientation note: pos.npy/nrm.npy/island.npy were saved by
proptex/atlas.py directly from Blender's row-0-is-bottom pixel buffer, so
they need no flip. depth.exr and the generate:*/gen_*.png view images are
read here through non-Blender decoders (row 0 = top, the normal file
convention), so each is flipped vertically once on load to match the
pos/nrm/island convention; the final composite is flipped back before
writing to PNG (see save_png_bottomup).
"""
import json
import struct
import sys
import zlib
from math import cos, radians, sin
from pathlib import Path

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "target" / "prop-cache"
OUT_DIR = REPO / "target" / "blend-probe"

sys.path.insert(0, str(REPO / "scripts" / "ai-pipeline"))
from prop_audit import iter_prims, island_mask, load_gltf  # noqa: E402

sys.path.insert(0, str(REPO / "target" / "arch-retess"))
from pre_screen import measure as pre_screen_measure  # noqa: E402

# ---- constants ported from proptex/atlas.py, proptex/coverage.py ----------
MV_WEIGHT_EXPONENT = 2.0
MV_OCCLUSION_EPS = 0.02
MV_EDGE_PAD_PX = 8
MV_COVERAGE_EPS = 1e-4

# ---- frequency-band cutoffs (mm); see report for the exact formulas below -
HWTA_SPLIT_MM = 14.0
HWTA_HARMONIZE_MM = 28.0
BAND_MM = 7.2
GAIN_CLIP = (0.5, 2.0)  # per-texel harmonization gain clamp (mine; stated in report)


# ============================================================================
# Minimal scanline-EXR reader (this env's cv2 build has no OpenEXR codec;
# depth.exr is a single-part, increasing-Y, ZIP-compressed float32 EXR, as
# written by Blender's OPEN_EXR/32 exporter -- proptex/views.py:depth_setup).
# ============================================================================

def read_exr_channel(path, channel="R"):
    data = Path(path).read_bytes()
    magic, _version = struct.unpack_from("<iI", data, 0)
    if magic != 0x01312f76:
        raise ValueError(f"{path}: not an EXR file")
    off = 8
    attrs = {}
    while True:
        end = data.index(b"\x00", off)
        name = data[off:end].decode()
        off = end + 1
        if name == "":
            break
        end2 = data.index(b"\x00", off)
        typ = data[off:end2].decode()
        off = end2 + 1
        size = struct.unpack_from("<i", data, off)[0]
        off += 4
        attrs[name] = (typ, data[off:off + size])
        off += size
    header_end = off

    compression = attrs["compression"][1][0]
    xmin, ymin, xmax, ymax = struct.unpack("<4i", attrs["dataWindow"][1])
    width, height = xmax - xmin + 1, ymax - ymin + 1
    if attrs["lineOrder"][1][0] != 0:
        raise ValueError(f"{path}: unsupported lineOrder (need INCREASING_Y)")

    chdata = attrs["channels"][1]
    channels = []
    o = 0
    while o < len(chdata) and chdata[o] != 0:
        end = chdata.index(b"\x00", o)
        cname = chdata[o:end].decode()
        o = end + 1
        pixel_type = struct.unpack_from("<i", chdata, o)[0]
        o += 4 + 1 + 3 + 4 + 4
        if pixel_type != 2:
            raise ValueError(f"{path}: channel {cname} is not FLOAT")
        channels.append(cname)
    channels_sorted = sorted(channels)
    ch_idx = channels_sorted.index(channel)
    n_ch = len(channels_sorted)

    rows_per_block = {0: 1, 1: 1, 2: 1, 3: 16}[compression]
    if compression not in (0, 3):
        raise ValueError(f"{path}: unsupported compression code {compression}")
    n_blocks = (height + rows_per_block - 1) // rows_per_block
    off = header_end + n_blocks * 8  # skip the chunk offset table

    out = np.empty((height, width), dtype=np.float32)
    row = 0
    for _ in range(n_blocks):
        off += 4  # chunk's leading scanline-y (int32); not needed, blocks are sequential
        comp_size = struct.unpack_from("<i", data, off)[0]
        off += 4
        chunk = data[off:off + comp_size]
        off += comp_size
        n_rows = min(rows_per_block, height - row)
        raw_size = n_rows * width * 4 * n_ch

        if compression == 0:
            raw = chunk
        else:
            decompressed = zlib.decompress(chunk)
            if len(decompressed) != raw_size:
                raise ValueError(f"{path}: block size mismatch")
            t = np.frombuffer(decompressed, dtype=np.uint8).astype(np.int64)
            t[1:] -= 128
            t = (np.cumsum(t) & 0xff).astype(np.uint8)
            half = (raw_size + 1) // 2
            deint = np.empty(raw_size, dtype=np.uint8)
            deint[0::2] = t[:half]
            deint[1::2] = t[half:]
            raw = deint.tobytes()

        pos = 0
        for r in range(n_rows):
            for ci in range(n_ch):
                if ci == ch_idx:
                    out[row + r] = np.frombuffer(raw, dtype="<f4", count=width, offset=pos)
                pos += width * 4
        row += n_rows
    return out


# ============================================================================
# Camera rig (proptex/views.py) reimplemented from the glb's own vertex data
# via prop_audit.py's pure-struct glTF reader (no pygltflib/trimesh/bpy).
# ============================================================================

def mesh_bounds(glb_path):
    """clean.glb is Blender's own glTF export, which (like its importer)
    converts between glTF's Y-up axis convention and Blender's internal
    Z-up: on disk (gltf_X, gltf_Y, gltf_Z) = Blender's (X, -Z, Y). The
    atlas's pos.npy/nrm.npy (baked from Blender's own Position node) are in
    Blender's Z-up frame, so the rig built here -- which pos/nrm get
    reprojected against via view_weight -- must convert back to it
    (verified against pos.npy's own min/max over the island)."""
    gltf, buffers = load_gltf(Path(glb_path))
    pts = np.concatenate([(pos * scale).astype(np.float64)
                           for pos, _uv, _tris, scale in iter_prims(gltf, buffers)])
    pts = pts[:, [0, 2, 1]] * np.array([1.0, -1.0, 1.0])
    return pts.min(axis=0), pts.max(axis=0)


def build_rig(glb_path):
    lo, hi = mesh_bounds(glb_path)
    radius = float(np.linalg.norm(hi - lo) / 2) * 1.05
    return {"lo": lo, "hi": hi, "half": radius}


def mv_view(az_deg, el_deg, rig):
    az, el = radians(az_deg), radians(el_deg)
    d = np.array([sin(az) * cos(el), -cos(az) * cos(el), sin(el)])
    f = -d
    s = np.cross(f, [0.0, 0.0, 1.0])
    s /= np.linalg.norm(s)
    u = np.cross(s, f)
    dist = 2.0 * rig["half"]
    near, far = rig["half"], 3.0 * rig["half"]
    return {"cam": (rig["lo"] + rig["hi"]) / 2 + d * dist, "f": f, "s": s, "u": u,
            "near": near, "far": far}


# ---- proptex/atlas.py, ported unchanged --------------------------------

def bilinear(arr, px, py):
    h, w = arr.shape[:2]
    x = np.clip(px, 0.0, w - 1.0)
    y = np.clip(py, 0.0, h - 1.0)
    x0 = np.clip(np.floor(x).astype(np.int64), 0, w - 2)
    y0 = np.clip(np.floor(y).astype(np.int64), 0, h - 2)
    fx, fy = x - x0, y - y0
    if arr.ndim == 3:
        fx, fy = fx[:, None], fy[:, None]
    a = arr[y0, x0] * (1 - fx) + arr[y0, x0 + 1] * fx
    b = arr[y0 + 1, x0] * (1 - fx) + arr[y0 + 1, x0 + 1] * fx
    return a * (1 - fy) + b * fy


def pad_edges(colors, mask, iterations):
    for _ in range(iterations):
        grown = mask.copy()
        for src, dst in (((slice(1, None),), (slice(None, -1),)),
                         ((slice(None, -1),), (slice(1, None),)),
                         ((slice(None), slice(1, None)), (slice(None), slice(None, -1))),
                         ((slice(None), slice(None, -1)), (slice(None), slice(1, None)))):
            fill = mask[src] & ~grown[dst]
            colors[dst][fill] = colors[src][fill]
            grown[dst] |= mask[src]
        mask = grown
    return colors


def view_weight(v, depth, rig, pos, nrm):
    depth = depth.astype(np.float64)
    h, w = depth.shape
    rel = pos - v["cam"]
    px = ((rel @ v["s"]) / rig["half"] * 0.5 + 0.5) * w - 0.5
    py = ((rel @ v["u"]) / rig["half"] * 0.5 + 0.5) * h - 0.5
    zc = rel @ v["f"]
    inside = (px >= 0) & (px <= w - 1) & (py >= 0) & (py <= h - 1)
    z_rend = v["far"] - bilinear(depth, px, py) * (v["far"] - v["near"])
    visible = zc <= z_rend + MV_OCCLUSION_EPS
    weight = np.maximum(0.0, nrm @ -v["f"]) ** MV_WEIGHT_EXPONENT
    weight *= (inside & visible).astype(np.float64)
    return weight, px, py


def covered_mask(wsum, island):
    return island & (wsum > MV_COVERAGE_EPS)


def atlas_size(texels):
    from math import isqrt
    return isqrt(texels.shape[0])


# ============================================================================
# Candidate cache-key config -- collected by reading each candidate's
# generation_manifest.json / texture_stats.json (target/arch-retess/,
# target/arch-ghost-attr/) and cross-checked against target/prop-cache/*/*/
# directory names, which are keyed by each stage's own cache key (not by an
# output's content hash -- verified: prop-cache/blend/<blend-key>/base.png
# etc.).
# ============================================================================

def _views5(az_el15_key, az_el_neg35_key):
    return [
        {"az": 0, "el": 15, "depth_key": "27b5d5158a3a93440b935f8710bf44a5c5c3d2bda8261cf38ebcf6bbcd7d145d"},
        {"az": 90, "el": 15, "depth_key": "99b6668a02396ef22d3b00a396f31d93dabc3d8a968d06488659e511dd8ed48c"},
        {"az": 180, "el": 15, "depth_key": "83c0cbaa0282fdd349a65be61173996af5a70f75d36205382844e2afa4ec472f"},
        {"az": 270, "el": 15, "depth_key": "0daa80575a8b211dcd31f4d71ade8f6c491baad8b67639629a4ff661f808badf"},
        {"az": 0, "el": -35, "depth_key": "cd9252a8953f5d81c7fcee4f29cb20fccffd16c19cc1dae7495b2de15315e79b"},
    ]


CANDIDATES = {
    "chapel_arch_103k_s0": {
        "clean_glb": REPO / "target/arch-retess/cand_fresh/cand_0/clean.glb",
        "atlas_key": "637f9005c6f09e9ebf0c6a1e0b76136554c824c4abc96de44b4510689979b05a",
        "views": _views5(None, None),
        "canvases": {
            "canvas_0": {"key": "b6cb03f9ec81ede3411b8f23581951adf0d6ba20c114084155aa5bee4420f98c",
                         "views": [(0, 15), (180, 15)]},
            "canvas_1": {"key": "5c3a56e128a7bf644653f999ff7115e1d1f558d0ba3fd52a89fc1f020e84707d",
                         "views": [(90, 15), (270, 15)]},
            "canvas_2": {"key": "93aaba8f2b41dba9a181a95afa983afd3f3ef247df3d10c2f6dd7c0209256f74",
                         "views": [(0, -35)]},
        },
        "blend_key": "cc47f340b5540430a2216715101ef69fff14df093d8f9ef50cb8f860949ce485",
    },
    "chapel_arch_103k_s1": {
        "clean_glb": REPO / "target/arch-retess/cand_reroll_s1/cand_1/clean.glb",
        "atlas_key": "637f9005c6f09e9ebf0c6a1e0b76136554c824c4abc96de44b4510689979b05a",
        "views": _views5(None, None),
        "canvases": {
            "canvas_0": {"key": "ae8881b7bd05856e6119da9ab409e4d3ace583215b773f5fdc1cc3f350073202",
                         "views": [(0, 15), (180, 15)]},
            "canvas_1": {"key": "9807b5cb9703127de36bcfcaab5d3d8feccce1ce45d2f96a3e8892fb399683e2",
                         "views": [(90, 15), (270, 15)]},
            "canvas_2": {"key": "42352175ae0ef8781ffaa039a2a637d7a46efeb475df1e293ddc9c5ce8d36b9c",
                         "views": [(0, -35)]},
        },
        "blend_key": "dd3bb82dfa562fdaed0803b4fbcbe1e737c9edb63e0a8aac238d0754a6fff7bf",
    },
    "chapel_arch_103k_s2": {
        "clean_glb": REPO / "target/arch-retess/cand_reroll_s2/cand_2/clean.glb",
        "atlas_key": "637f9005c6f09e9ebf0c6a1e0b76136554c824c4abc96de44b4510689979b05a",
        "views": _views5(None, None),
        "canvases": {
            "canvas_0": {"key": "971ed67bd59d4987259f9fb4fc56ab16838ef4c495fddee576660bd8d47e5f33",
                         "views": [(0, 15), (180, 15)]},
            "canvas_1": {"key": "2ff66e8413f6a1a15e59a32726711ae71e63969633a8f86dce2cc9c31ac897e6",
                         "views": [(90, 15), (270, 15)]},
            "canvas_2": {"key": "b3b55712ead43da4572296257c8c1f86b1c9178121d49bc985205657c4f3276f",
                         "views": [(0, -35)]},
        },
        "blend_key": "39dd5b72f21da85385973c0dbe376a958d7bf6f90af5aa4f070f2f4e3806cb82",
    },
    "chapel_arch_103k_s3": {
        "clean_glb": REPO / "target/arch-retess/cand_reroll_s3/cand_3/clean.glb",
        "atlas_key": "637f9005c6f09e9ebf0c6a1e0b76136554c824c4abc96de44b4510689979b05a",
        "views": _views5(None, None),
        "canvases": {
            "canvas_0": {"key": "8ad54bc5abd493c42bb871ed0ddde4cc4d1d003b863596d8127425a7ecc533ea",
                         "views": [(0, 15), (180, 15)]},
            "canvas_1": {"key": "b9590b10a0c8ea8e52a298d7b0a90850bd1117dfd568879fc46e5bb23310e0a1",
                         "views": [(90, 15), (270, 15)]},
            "canvas_2": {"key": "b176033a9f104a78020316517c3737b90f14cf884ed765f9c14935805861ccb7",
                         "views": [(0, -35)]},
        },
        "blend_key": "0d4b42fe017036ac097a7517b22eb1a785015a7baf6f86bf7e54f9b978791732",
    },
    "chapel_arch_15k_s7": {
        "clean_glb": REPO / "target/arch-ghost-attr/cand_7/clean.glb",
        "atlas_key": "f08c344991d3266a2d844e5c06b98ce2e7b89e677e017bea2209fefa04e63cba",
        "views": [
            {"az": 0, "el": 15, "depth_key": "25bc289cb67660746c75d9649aacf79c98dee4276d720b54b5f249a508de1f80"},
            {"az": 90, "el": 15, "depth_key": "5bbd55c5d874076b404a9e9d9e63d5c7410aca05363592171350c2eca22796e1"},
            {"az": 180, "el": 15, "depth_key": "62943beb771c36ac8e2a89c2fa05839b4d238b7ff53644414a2ddce93a1e1f8e"},
            {"az": 270, "el": 15, "depth_key": "dc320b86f7133081b98ccd2403df45995299d7465da65e41a81a9fe33b8470ca"},
            {"az": 0, "el": -35, "depth_key": "b2be6c39dce469e6647c36f81adbea80c193e0b2ae56ebc8ef0f60b2108488ee"},
            {"az": 210, "el": -35, "depth_key": "c43a107b11f8a391825ea213d4511d78c3af1a4188dc25b740c851b2dfd5cadd"},
            {"az": 180, "el": 55, "depth_key": "64f3e95617158b8773b12af91fc5e79b5842bf775d009d58797da2015ae16925"},
            {"az": 270, "el": 55, "depth_key": "720bc350834fd8583da7328dffefa2f5e477bec026a00f1eb5a23acb458201d0"},
            {"az": 300, "el": 15, "depth_key": "39b7e94ad9da9c1afacfddd3b38ce6d4f59e225e2a774b2c5e9f4029a823419b"},
            {"az": 210, "el": 15, "depth_key": "80f161183d064f45c510cb6bf55ab55edddc4b2fb11ffc7c6786d9a999c1feb4"},
            {"az": 30, "el": -35, "depth_key": "6165e5b166600241479605867a889c3aa33a80876faf4c814b5f3eaf52fca081"},
            {"az": 270, "el": -35, "depth_key": "95b376efdcff35516a1c3e16a5905b6b6301a407d380ed125badc53fce44d8e4"},
            {"az": 300, "el": -35, "depth_key": "793cd819d709b89d44765027c6c36cfac1b4cb6f5400dbc31e32b1a8fb15c357"},
        ],
        "canvases": {
            "canvas_0": {"key": "82582cc68de346896fbc95ad68b84105d8f65a094657b03f7177ed8e617a378d",
                         "views": [(0, 15), (180, 15)]},
            "canvas_1": {"key": "cf6af64469ceaa6c1c2c5b3558ea0bcaf31b909372935513886e9e7dfd9e4826",
                         "views": [(90, 15), (270, 15)]},
            "canvas_2": {"key": "a4ebe2c5f899249417749d28b7ce6e322f35ada177bd534f1535e20bdbd14dc5",
                         "views": [(0, -35), (210, -35)]},
            "canvas_3": {"key": "7ceee1d8205dc025d4a0d682e15f109101f4cf39f2e026a8879d6aa0a160eac0",
                         "views": [(180, 55), (270, 55)]},
            "canvas_4": {"key": "da08cd45a8426c238cceef0e8ab3139bab6fa347d9ca6b337f69cab8ee7f21fe",
                         "views": [(300, 15), (210, 15)]},
            "canvas_5": {"key": "0911c178e44fcbc3a128d9617b5858ba7c3d12583c1dc6025b83ca4444620dd4",
                         "views": [(30, -35), (270, -35)]},
            "canvas_6": {"key": "52c119c33b2fdad580719cf7dfc26c23c88dbbb3bd3f2030f2e9886b3ab5d348",
                         "views": [(300, -35)]},
        },
        "blend_key": "6496ecd79938c10b5ac32537b4ec2b2b42d6774255f8a80dd67850d17f7d4e8e",
    },
}

ANCHORS = {
    "old_shipped_arch": {"p95_over_p5": 1.78, "below_45pct": 0.0023},
    "photoscan_ref_max": {"p95_over_p5": 3.10, "below_45pct": 0.0423},
    "pre_screen_gate": {"p95_over_p5_max": 4.0, "below_45pct_max": 0.065},
}


# ============================================================================
# Image IO helpers
# ============================================================================

def load_gen_png(path, expect_hw):
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float64) / 255.0
    img = np.flipud(img)  # file is row0=top; flip to Blender's row0=bottom
    if img.shape[:2] != expect_hw:
        raise ValueError(f"{path}: shape {img.shape[:2]} != depth shape {expect_hw}")
    return img


def save_png_bottomup(out_rgb01, path):
    """out_rgb01 is (size,size,3) float in [0,1], row0=bottom (Blender
    convention) -- flip once to the on-disk row0=top convention, matching
    what Blender's own save_png does on write."""
    img8 = (np.clip(out_rgb01, 0.0, 1.0) * 255.0).round().astype(np.uint8)
    img8 = np.flipud(img8)
    cv2.imwrite(str(path), cv2.cvtColor(img8, cv2.COLOR_RGB2BGR))


# ============================================================================
# Per-candidate view loading (geometry + reprojected raw view colors)
# ============================================================================

class ViewData:
    __slots__ = ("az", "el", "weight", "color")


def load_candidate(cfg):
    atlas_dir = CACHE / "atlas" / cfg["atlas_key"]
    pos = np.load(atlas_dir / "pos.npy")
    nrm = np.load(atlas_dir / "nrm.npy")
    island = np.load(atlas_dir / "island.npy")
    rig = build_rig(cfg["clean_glb"])

    # az/el -> gen png path, via the canvas map
    gen_path_of = {}
    for cv_name, cv_cfg in cfg["canvases"].items():
        gen_dir = CACHE / "generate" / cv_cfg["key"]
        for i, (az, el) in enumerate(cv_cfg["views"]):
            gen_path_of[(az, el)] = gen_dir / f"gen_{i}.png"

    views = []
    for vspec in cfg["views"]:
        az, el = vspec["az"], vspec["el"]
        depth_dir = CACHE / "depth" / vspec["depth_key"]
        depth = read_exr_channel(depth_dir / "depth.exr", "R")
        depth = np.flipud(depth)  # file row0=top -> Blender row0=bottom
        v = mv_view(az, el, rig)
        weight, px, py = view_weight(v, depth, rig, pos, nrm)
        gen = load_gen_png(gen_path_of[(az, el)], depth.shape)
        gen = pad_edges(gen, depth > 0.01, MV_EDGE_PAD_PX)
        color = bilinear(gen, px, py)
        vd = ViewData()
        vd.az, vd.el, vd.weight, vd.color = az, el, weight, color
        views.append(vd)

    return pos, nrm, island, views


def texel_density_mm(pos, island):
    """Median world-space distance between horizontally/vertically adjacent
    in-island atlas texels, in mm -- an actual measurement of this
    candidate's texel density (not a reused nominal number), used to convert
    the campaign's mm-denominated cutoffs (7.2/14/28mm) to texels."""
    size = atlas_size(island)
    pos2 = pos.reshape(size, size, 3)
    isl2 = island.reshape(size, size)
    dx = np.linalg.norm(pos2[:, 1:] - pos2[:, :-1], axis=-1)
    mdx = isl2[:, 1:] & isl2[:, :-1]
    dy = np.linalg.norm(pos2[1:, :] - pos2[:-1, :], axis=-1)
    mdy = isl2[1:, :] & isl2[:-1, :]
    samples = np.concatenate([dx[mdx], dy[mdy]])
    return float(np.median(samples)) * 1000.0


# ============================================================================
# Estimators
# ============================================================================

def mean_estimate(views, pos, island):
    size = atlas_size(island)
    accum = np.zeros((pos.shape[0], 3))
    wsum = np.zeros(pos.shape[0])
    for vd in views:
        accum += vd.color * vd.weight[:, None]
        wsum += vd.weight
    covered = covered_mask(wsum, island)
    out = np.full((pos.shape[0], 3), 0.5)
    blended = accum[covered] / wsum[covered, None]
    out[covered] = blended
    fill = blended.mean(axis=0) if covered.any() else np.full(3, 0.5)
    out[~covered] = fill
    out = inpaint_holes(out, covered, island, size)
    return out, wsum, covered


def inpaint_holes(out, covered, island, size):
    holes = island & ~covered
    if not holes.any():
        return out
    img8 = (np.clip(out, 0.0, 1.0) * 255.0).round().astype(np.uint8).reshape(size, size, 3)
    mask8 = holes.reshape(size, size).astype(np.uint8)
    filled = cv2.inpaint(img8, mask8, 3, cv2.INPAINT_TELEA)
    out = out.copy()
    out[holes] = filled.reshape(-1, 3)[holes] / 255.0
    return out


def normalized_gaussian_blur(field2d, mask2d, sigma_px):
    """Mask-aware ("normalized convolution") Gaussian blur: holes/outside-
    mask texels do not bleed into the blurred estimate at their
    neighbours."""
    m = mask2d.astype(np.float32)
    filled = (field2d * m[..., None]).astype(np.float32)
    num = cv2.GaussianBlur(filled, (0, 0), sigma_px)
    den = cv2.GaussianBlur(m, (0, 0), sigma_px)
    if num.ndim == 2:
        num = num[..., None]
    return num / np.maximum(den[..., None], 1e-6)


def weighted_median_across_views(vals, weights):
    """vals: (n_views, n_texels, 3) float, weights: (n_views, n_texels) ->
    (n_texels, 3) per-texel per-channel weighted median. Zero-weight
    entries (a view that does not cover that texel) contribute 0 to the
    cumulative weight and so cannot become the median."""
    n_texels = vals.shape[1]
    out = np.empty((n_texels, 3), dtype=np.float32)
    for c in range(3):
        order = np.argsort(vals[:, :, c], axis=0)
        sv = np.take_along_axis(vals[:, :, c], order, axis=0)
        sw = np.take_along_axis(weights, order, axis=0)
        cumw = np.cumsum(sw, axis=0)
        total = cumw[-1]
        target = total / 2.0
        idx = np.argmax(cumw >= target[None, :], axis=0)
        out[:, c] = np.take_along_axis(sv, idx[None, :], axis=0)[0]
    return out


def hwta_estimate(views, pos, island, mm_per_texel, mean_raw, wsum, covered, use_median):
    """Harmonized WTA: 28mm per-view gain-ratio harmonization (mine --
    see report for the exact formula) + 14mm consensus-LF/winner-HF split.
    use_median=False reproduces the campaign's "harmonized WTA"; True is
    the "med-hwta" variant (weighted-median LF combine instead of
    weighted-mean)."""
    size = atlas_size(island)
    sigma28 = (HWTA_HARMONIZE_MM / mm_per_texel) / 3.0  # see report: sigma = cutoff/3
    sigma14 = (HWTA_SPLIT_MM / mm_per_texel) / 3.0

    covered2 = covered.reshape(size, size)
    mean_raw2 = mean_raw.reshape(size, size, 3)
    lf28_mean = normalized_gaussian_blur(mean_raw2, covered2, sigma28)

    n = len(views)
    weight_stack = np.stack([vd.weight for vd in views]).astype(np.float32)  # (n, n_texels)
    color_stack = np.stack([vd.color for vd in views]).astype(np.float32)  # (n, n_texels, 3)

    lf14_stack = np.empty_like(color_stack)
    for i, vd in enumerate(views):
        cov_i2 = (vd.weight > 0).reshape(size, size)
        color_i2 = vd.color.reshape(size, size, 3).astype(np.float32)
        lf28_i = normalized_gaussian_blur(color_i2, cov_i2, sigma28)
        gain = np.clip(lf28_mean / np.maximum(lf28_i, 1.0 / 255.0), *GAIN_CLIP)
        corrected2 = color_i2 * gain
        corrected = corrected2.reshape(-1, 3)
        color_stack[i] = corrected
        lf14_i2 = normalized_gaussian_blur(corrected2, cov_i2, sigma14)
        lf14_stack[i] = lf14_i2.reshape(-1, 3)
    hf14_stack = color_stack - lf14_stack

    if use_median:
        lf_final = weighted_median_across_views(lf14_stack, weight_stack)
    else:
        wsum3 = weight_stack.sum(axis=0)
        lf_final = (lf14_stack * weight_stack[:, :, None]).sum(axis=0) / np.maximum(wsum3[:, None], 1e-9)

    winner = np.argmax(weight_stack, axis=0)  # (n_texels,)
    hf_final = np.take_along_axis(hf14_stack, winner[None, :, None], axis=0)[0]

    out = np.full((pos.shape[0], 3), 0.5, dtype=np.float64)
    combo = (lf_final + hf_final).astype(np.float64)
    out[covered] = combo[covered]
    out = inpaint_holes(out, covered, island, size)
    return out, winner


# ============================================================================
# Metrics
# ============================================================================

def luma(rgb01):
    return 0.2126 * rgb01[..., 0] + 0.7152 * rgb01[..., 1] + 0.0722 * rgb01[..., 2]


def seam_excess(out_rgb01, winner2d, island2d, covered2d):
    """Mean luma-gradient magnitude on winner-boundary texels divided by
    the mean on island-interior (non-boundary) texels. The boundary set is
    computed from the view-weight argmax field alone (winner2d), so it is
    identical across variants for a given candidate -- the mean control's
    floor and a variant's number are measured over the same locations."""
    l01 = luma(out_rgb01).astype(np.float32)
    gx = cv2.Sobel(l01, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(l01, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.sqrt(gx * gx + gy * gy)

    w = np.where(covered2d, winner2d, -1)
    boundary = covered2d.copy()
    boundary &= (
        (np.roll(w, 1, axis=0) != w) | (np.roll(w, -1, axis=0) != w) |
        (np.roll(w, 1, axis=1) != w) | (np.roll(w, -1, axis=1) != w)
    )
    boundary &= island2d
    interior = island2d & covered2d & ~boundary
    if not boundary.any() or not interior.any():
        return float("nan")
    return float(mag[boundary].mean() / mag[interior].mean())


def band_std_7p2mm(out_rgb01, island2d, mm_per_texel):
    """DoG band centred at BAND_MM: blur(sigma/1.6) - blur(sigma*1.6),
    std over island texels of the luma DoG response. Higher = more
    retained mid-frequency detail. Definition is mine (not recovered from
    the campaign log); see report."""
    center = BAND_MM / mm_per_texel
    s1, s2 = center / 1.6, center * 1.6
    l01 = luma(out_rgb01).astype(np.float32)
    lo = cv2.GaussianBlur(l01, (0, 0), s1)
    hi = cv2.GaussianBlur(l01, (0, 0), s2)
    dog = (lo - hi) * 255.0
    return float(dog[island2d].std())


# ============================================================================
# Driver
# ============================================================================

def run_candidate(name, cfg, report):
    print(f"\n=== {name} ===")
    out_dir = OUT_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    pos, nrm, island, views = load_candidate(cfg)
    size = atlas_size(island)
    mm_per_texel = texel_density_mm(pos, island)
    print(f"texel density: {mm_per_texel:.3f} mm/texel ({size}x{size})")

    mean_out, wsum, covered = mean_estimate(views, pos, island)
    save_png_bottomup(mean_out.reshape(size, size, 3), out_dir / "mean.png")

    # ---- validation: mean_out vs the pipeline's actual cached base.png ----
    ref_path = CACHE / "blend" / cfg["blend_key"] / "base.png"
    ref = cv2.imread(str(ref_path), cv2.IMREAD_COLOR)
    ref = cv2.cvtColor(ref, cv2.COLOR_BGR2RGB).astype(np.float64) / 255.0
    mine8 = np.flipud((np.clip(mean_out.reshape(size, size, 3), 0, 1) * 255.0).round()) / 255.0
    covered2d = covered.reshape(size, size)
    covered2d_topdown = np.flipud(covered2d)
    mad = float(np.abs(mine8 - ref)[covered2d_topdown].mean()) * 255.0
    print(f"validation MAD (covered island texels): {mad:.4f} /255")
    report["candidates"][name] = {"mm_per_texel": mm_per_texel, "validation_mad_255": mad, "variants": {}}
    if mad > 0.5:
        print(f"!!! VALIDATION FAILED for {name}: MAD {mad:.4f} > 0.5/255 -- STOPPING before variants")
        report["candidates"][name]["validation_failed"] = True
        return

    # recompute the raw (pre-inpaint) mean for use as the harmonization
    # target inside hwta/med-hwta (mean_estimate() already inpainted; redo
    # the raw covered-only blend here since hwta needs the un-inpainted
    # values so inpaint fill doesn't get treated as real low-frequency
    # signal)
    accum = np.zeros((pos.shape[0], 3))
    wsum2 = np.zeros(pos.shape[0])
    for vd in views:
        accum += vd.color * vd.weight[:, None]
        wsum2 += vd.weight
    mean_raw = np.full((pos.shape[0], 3), 0.5)
    mean_raw[covered] = accum[covered] / wsum2[covered, None]

    hwta_out, winner = hwta_estimate(views, pos, island, mm_per_texel, mean_raw, wsum, covered, use_median=False)
    save_png_bottomup(hwta_out.reshape(size, size, 3), out_dir / "hwta.png")

    med_out, _ = hwta_estimate(views, pos, island, mm_per_texel, mean_raw, wsum, covered, use_median=True)
    save_png_bottomup(med_out.reshape(size, size, 3), out_dir / "med_hwta.png")

    island2d = island.reshape(size, size)
    winner2d = winner.reshape(size, size)

    for variant_name, out_flat, glb_img_path in (
        ("mean", mean_out, out_dir / "mean.png"),
        ("hwta", hwta_out, out_dir / "hwta.png"),
        ("med_hwta", med_out, out_dir / "med_hwta.png"),
    ):
        out2d = out_flat.reshape(size, size, 3)
        pre = pre_screen_measure(cfg["clean_glb"], glb_img_path)
        se = seam_excess(out2d, winner2d, island2d, covered2d)
        band = band_std_7p2mm(out2d, island2d, mm_per_texel)
        gate_ok = pre["p95_over_p5"] <= ANCHORS["pre_screen_gate"]["p95_over_p5_max"] and \
            pre["below_45pct_median_frac"] <= ANCHORS["pre_screen_gate"]["below_45pct_max"]
        report["candidates"][name]["variants"][variant_name] = {
            **pre, "seam_excess": se, "band_std_7p2mm": band, "pre_screen_gate_pass": gate_ok,
        }
        print(f"  [{variant_name}] p5={pre['luma_p5']:.4f} p50={pre['luma_p50']:.4f} "
              f"p95={pre['luma_p95']:.4f} p95/p5={pre['p95_over_p5']:.3f} "
              f"below45%={pre['below_45pct_median_frac']:.4f} seam_excess={se:.3f} "
              f"band7.2mm_std={band:.3f} gate={'PASS' if gate_ok else 'fail'}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {"anchors": ANCHORS, "candidates": {}}
    for name, cfg in CANDIDATES.items():
        try:
            run_candidate(name, cfg, report)
        except FileNotFoundError as e:
            print(f"\n=== {name}: SKIPPED (cached input not found: {e}) ===")
            report["candidates"][name] = {"skipped": True, "reason": str(e)}
    (OUT_DIR / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_DIR / 'report.json'}")


if __name__ == "__main__":
    main()
