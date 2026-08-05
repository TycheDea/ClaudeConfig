"""Moss regrade for the street_cobble albedo (cand_1, ambientCG PavingStones150).

Measures per-pixel green excess g = (G - max(R,B)) / 255 and, only on the
moss-green flecks (pixels where G > max(R,B)), rotates hue toward a dry-earth
tan (~33 deg) while holding V (max(R,G,B)) exactly fixed -- a hue-only
rotation in HSV space cannot touch overall brightness, and moving away from
green hue (120 deg) toward 33 deg mechanically drives G - max(R,B) down. The
mask is feathered both by excess magnitude (soft threshold) and spatially
(gaussian blur, wrap mode -- the source tiles) so there's no hard cutout edge.

Gate: p95 of g on the regraded albedo must be <= +0.01 (measured ~+0.0275
before, on cand_1 as delivered).

Usage: python regrade_moss.py <in_diff.png> <out_diff.png>
"""
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

TARGET_HUE_DEG = 33.0
# Sprigs are 2-3 px wide (cand_1's moss flecks) -- a wider blur dilutes the
# weight at their own center against zero-weight neighbors before the ramp
# below ever reaches 1.0, under-shifting exactly the pixels being targeted.
FEATHER_SIGMA_PX = 1.2
# Excess (0..1 scale) at which a pixel gets the FULL hue shift; below this,
# the shift scales down linearly to 0 at g=0. Set below the moss region's own
# median excess (measured 0.035 on cand_1) so most flagged pixels reach a
# full shift and only the faint fringe gets a partial one.
FULL_SHIFT_EXCESS = 0.015


def green_excess(rgb: np.ndarray) -> np.ndarray:
    """(G - max(R,B)) / 255, rgb as uint8 array (H, W, 3)."""
    r, g, b = rgb[..., 0].astype(np.float64), rgb[..., 1].astype(np.float64), rgb[..., 2].astype(np.float64)
    return (g - np.maximum(r, b)) / 255.0


def rgb_to_hsv(rgb01: np.ndarray) -> np.ndarray:
    r, g, b = rgb01[..., 0], rgb01[..., 1], rgb01[..., 2]
    maxc = np.max(rgb01, axis=-1)
    minc = np.min(rgb01, axis=-1)
    v = maxc
    delta = maxc - minc
    s = np.where(maxc > 0, delta / np.where(maxc == 0, 1, maxc), 0.0)

    rc = np.where(delta > 0, (maxc - r) / np.where(delta == 0, 1, delta), 0.0)
    gc = np.where(delta > 0, (maxc - g) / np.where(delta == 0, 1, delta), 0.0)
    bc = np.where(delta > 0, (maxc - b) / np.where(delta == 0, 1, delta), 0.0)

    h = np.zeros_like(maxc)
    is_r = (maxc == r) & (delta > 0)
    is_g = (maxc == g) & (delta > 0) & ~is_r
    is_b = (maxc == b) & (delta > 0) & ~is_r & ~is_g
    h = np.where(is_r, bc - gc, h)
    h = np.where(is_g, 2.0 + rc - bc, h)
    h = np.where(is_b, 4.0 + gc - rc, h)
    h = (h / 6.0) % 1.0
    return np.stack([h, s, v], axis=-1)


def hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = np.floor(h * 6.0).astype(np.int64)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    conds = [i == k for k in range(6)]
    r = np.select(conds, [v, q, p, p, t, v])
    g = np.select(conds, [t, v, v, q, p, p])
    b = np.select(conds, [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)


def regrade(rgb: np.ndarray) -> np.ndarray:
    rgb01 = rgb.astype(np.float64) / 255.0
    g_excess = green_excess(rgb)

    # Feather by magnitude: 0 at g<=0, ramps to 1 at g>=FULL_SHIFT_EXCESS.
    weight = np.clip(g_excess / FULL_SHIFT_EXCESS, 0.0, 1.0)
    # Spatial feather -- the source tiles, so blur wraps at the edges instead
    # of darkening/lightening the border.
    weight = gaussian_filter(weight, sigma=FEATHER_SIGMA_PX, mode="wrap")
    weight = np.clip(weight, 0.0, 1.0)

    hsv = rgb_to_hsv(rgb01)
    target_h = TARGET_HUE_DEG / 360.0
    # Shortest angular path from each pixel's hue to the target hue.
    h = hsv[..., 0]
    diff = (target_h - h + 0.5) % 1.0 - 0.5
    hsv[..., 0] = (h + diff * weight) % 1.0
    # V (hsv[...,2]) is never touched -- overall brightness ladder position
    # is untouched by construction.

    out01 = hsv_to_rgb(hsv)
    return np.clip(np.round(out01 * 255.0), 0, 255).astype(np.uint8)


def p95(g_excess: np.ndarray) -> float:
    return float(np.percentile(g_excess, 95))


def main():
    if len(sys.argv) != 3:
        print("usage: regrade_moss.py <in_diff.png> <out_diff.png>", file=sys.stderr)
        sys.exit(2)
    in_path, out_path = sys.argv[1], sys.argv[2]

    img = Image.open(in_path).convert("RGB")
    rgb = np.array(img)

    before = green_excess(rgb)
    before_p95 = p95(before)

    out_rgb = regrade(rgb)
    after = green_excess(out_rgb)
    after_p95 = p95(after)

    # Value(brightness) drift check -- max(R,G,B) per pixel, mean absolute
    # delta should be ~0 (hue-only rotation).
    v_before = rgb.astype(np.float64).max(axis=-1) / 255.0
    v_after = out_rgb.astype(np.float64).max(axis=-1) / 255.0
    v_drift = float(np.abs(v_after - v_before).mean())

    Image.fromarray(out_rgb, mode="RGB").save(out_path)

    print(f"green excess p95 before: {before_p95:+.4f}")
    print(f"green excess p95 after:  {after_p95:+.4f}")
    print(f"mean |V drift|:          {v_drift:.6f}")
    print(f"gate (p95 <= +0.01):     {'PASS' if after_p95 <= 0.01 else 'FAIL'}")


if __name__ == "__main__":
    main()
