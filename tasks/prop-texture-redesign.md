# `prop_texture.py` redesign — declared contracts, content-addressed stages

Status: **plan, not approved.** Evidence: anatomy + boundary/ledger analyses,
2026-07-25. Supersedes nothing yet; `tasks/todo.md`'s open items D5/D6 (delighting)
are absorbed here.

## 1. Diagnosis

Twenty recorded defects reduce to three structural faults.

**F-I — inference where declaration belongs.** D1 (roughness estimated from a lit
render), D10/D11/D13 (metal classified from basecolor luma), D16/D17 (provenance
read from a hardcoded node id / literal strategy string), D5/D6 (albedo delit by a
model that is right for foliage and wrong for stone). The MR contract has been
rebuilt six times — zoning → sRGB fix → dielectric mode → declared constants →
mask pass → per-view estimator → scalar factors — and landed every time on
*declare it, don't estimate it*. Delighting is the same fault, still live, in the
albedo channel.

**F-II — degeneration where refusal belongs.** D12 (missing alpha matte → the
stage fitted the full frame and shipped white porcelain), D18a (mean-colour fill
past the silhouette), D7 (44.96% of chapel_arch's island is Telea filler,
*reported as a statistic*). Each produced a plausible asset from an invalid input,
so the failure surfaced as "looks like AI slop" three stages later instead of as
an exit code.

**F-III — the contract lives in the script, the defect lives in the asset.** D9:
`36f1c29` fixed the MR contract; six of seven props still ship the old one,
because installation is a manual copy with no re-bake and no lint tying an asset
to the contract that produced it. Compounded by path-keyed resume (anatomy §8):
resume keys are filenames, never input hashes, so a rerun with a changed subject,
seed, azimuth set or re-cleaned mesh reuses stale images **and attaches the
previous run's prompts and seeds as provenance**.

Every provenance number read this campaign rests on nobody having done that.

## 2. The missing concept

`--metallic 0.0 --roughness 0.85 --detail` is one fact — *this prop is limestone* —
spelled three times in argv. Delighting would be a fourth. Today that fact is
spelled in five places and stored in none: argv (lost), glb `extras`,
`roughnessFactor`, `content_lint`'s hardcoded `stone_props_declare_detail` list,
and a rollout list in `todo.md`. Characters inherit their entire material contract
by *accident* — `gen_character.py` never passes `--metallic`/`--roughness`, so
`DEFAULT_ROUGHNESS = 0.8` is the character contract, mirrored by hand a second
time at `char_mpfb.py:361`.

**Surface class** is the concept. Declared once per asset, resolved to a contract,
recorded in provenance, stamped into the glb, asserted by lint.

## 3. Architecture

### A. Declaration split: registry = intent, manifest = record

`content/models/surface_classes.json` — the class table. JSON because Python, Rust
(`content_lint`) and Node (`bake_textures.mjs`) all read it natively; `.ron` would
be Rust-only.

```
limestone      { metallic 0.0, roughness 0.85, albedo_source direct, detail true  }
wood           { metallic 0.0, roughness 0.85, albedo_source direct, detail false }
foliage        { metallic 0.0, roughness 0.70, albedo_source delit,  detail false }
painted_metal  { metallic 0.0, roughness 0.75, albedo_source direct, detail false }
character_skin { metallic 0.0, roughness 0.80, albedo_source delit,  detail false }
```

Four fields, because four are read: §3B.1 keys `export` on `metallic`,
`roughness` and `detail`, and rows 4/6 branch on `albedo_source`.

**`wood` — `0.0 / 0.85`.** Dielectric by physics, as every class here is. Its
roughness equals limestone's because nothing separates them: both are
coating-free weathered dielectrics with no polish and no coherent specular lobe,
and `olive_stump`'s subject is "gnarled dead olive tree stump … deep cracked
bark", not finished timber. The one measurement that could argue otherwise
refutes itself — the shipped MR texture puts `olive_stump` at mean roughness
0.576, inside the 0.499–0.658 band the same estimator produced across the
limestone props, so it does not separate wood from stone at all (it is D1, and
it reads ~0.3 low against `rock_face_01`'s authored, near-scalar 0.882 ± 0.031).
`wood` therefore earns its existence on `detail`, not on roughness: the overlay
tile is `content/textures/detail/limestone` (`presentation.rs:41`), and tiling
masonry over bark is the defect the flag exists to prevent.

**`foliage` — `0.0 / 0.70`.** A plant cuticle is a smooth waxy dielectric, the
only coherent specular lobe in the set, so foliage must sit below 0.85 or the
class models nothing stone does not. The floor comes from the mesh: `cypress`
ships **opaque** — a 15k-triangle solid canopy, RGB basecolor, `alphaMode
OPAQUE`, not the alpha-masked cards `--detail`'s help text assumes — so no leaf
geometry breaks a highlight up, and below ~0.6 a single coherent band crosses a
2.5 m blob and reads as plastic. **0.70 is unforced inside that 0.6–0.8 band**
and is called as such. Settling it costs seconds under §3B: `roughness` keys row
10 alone, so re-exporting `cypress` at 0.70 and 0.85 re-runs `export` and
nothing else, and the scene key is an 8°-elevation dusk sun
(`presentation.rs:34`) — grazing incidence, the one condition that shows the lobe.

**`ao_distance_m` is not a class field; no class carries it.** The bake is
unconditional (`prop_texture.py:918`, characters included), so this is not a key
read on no path — it is a key that does not partition on class. `chapel_arch`
(5.5 m) and `gravestone` (2.2 m) are both limestone and share the value, while
what would move `olive_stump`'s is its size: at 0.70 m across, a 0.15 m ray
reaches a fifth of the way over the stump and re-creates the far-leg-across-the-
opening failure the constant was bounded to avoid (`prop_texture.py:91-95`). Size
is not wood-ness. Nor does it move to `assets.json`: §3A.1 earns a place there by
*measured* per-asset variance, and this value has been exercised on exactly one
asset — `chapel_arch` is the only prop shipping an `occlusionTexture` at all. It
stays the single module constant `AO_DISTANCE_M` that §3B.1 row 9 already keys and
the manifest already keeps; five declared copies of a number measured once would
be five invented facts. Row 36's review of the rebuilt prop is the measurement
that could move it, with `olive_stump` the named candidate.

**No class carries a coverage or hole field either, and row 27 ruled it for the
same reason.** The gate derived from rows 25–26 is one number — a hole
component's *extrapolation depth* may not exceed 1.5% of atlas width — and it
does not partition on class. Row 26's bands were established across the mixed
1k/2k set and read the same on every prop in it: ≤0.4% of width undetectable on
all seven, >1.5% failing on all seven **including `cypress`**, "the most
forgiving material in the set (foliage, where hue and value match perfectly)".
So the one measurement that could separate foliage refutes the separation, and
five declared copies of a number measured once would be five invented facts —
six, counting `character_skin`, which has no asset and would carry a number
measured never. It stays the single module constant `MAX_HOLE_DEPTH_FRAC` in
`proptex/coverage.py`, §3D's home for the gate. `min_coverage` does not exist in
any spelling: §7 records why the coverage *fraction* is not the quantity a gate
can key on. Row 36's review of the first rebuilt prop is the measurement that
could move the constant.

There is no `iron` class. Paint is the surface, so painted iron is a dielectric —
`candelabra_shrine` is `painted_metal`, and its shipped `metallic 0.0` was already
right. No shipped asset is bare metal, so a metal class would be an abstraction
for a case that does not exist. It arrives with the first bare-metal asset, tested
on that asset rather than inferred now.

`content/models/assets.json` — the asset table: `name → {kind, surface_class,
subject, texture_size, view_res, azimuths?}`. This is the first enumerable list
of what exists; today props are discoverable only through `zones.ron`.

Per-asset `generation_manifest.json` stays exactly where it is and keeps its job:
what actually happened. Intent in, record out — never the same file.

**Consequence:** six CLI flags (`--metallic --roughness --detail --azimuths
--view-res --texture-size`) collapse into `--asset <name>`. The class of defect
where `--azimuths` and `--view-res` are silently accepted and discarded under
`projection` disappears with them.

### A.1 The CLI/registry contract

The registry holds every fact **fixed across a seed sweep**; the CLI carries the
one that is not. That single line settles all six questions below, because a
sweep is the only situation where the two could disagree.

```
blender --background --python prop_texture.py -- \
    <clean.glb> <hires.glb> <textured.glb> --asset <name> --seed N

python gen_prop.py --asset <name> --seed N --out <dir> \
    [--skip-concept IMG] [--symmetrize] [--symmetrize-keep +x|-x] \
    [--through STAGE] [--max-bytes N]

python gen_character.py --asset <name> --seed N --out <dir> \
    [--skip-concept IMG] [--height M]
python gen_character.py --mpfb --out <dir> [--height M]
```

**`prop_texture.py`** — positionals lose `concept_png`; flags collapse to
`--asset` plus `--seed`. Dropped: `--strategy`, `--subject`, `--metallic`,
`--roughness`, `--detail`, `--azimuths`, `--view-res`, `--texture-size`, and
with them `DEFAULT_METALLIC`/`DEFAULT_ROUGHNESS`. The key is `--asset` and not
`--surface-class` because three of the resolved facts are **measured** to be
per-asset, not per-class: the shipped set runs `texture_size` 1024 *and* 2048,
`view_res` 1024 *and* 1536, and azimuths `0,90,180,270` *and* `0,60,180,300`
(candelabra_shrine, crucero) — chapel_arch and gravestone are both limestone and
disagree on all three.

**`gen_prop.py`** — the `subject` positional is deleted, `--asset` replaces it.
Dropped flags: `--texture-strategy`, `--metallic`, `--roughness`, `--detail`,
`--azimuths`, `--view-res`, `--texture-size`, `--max-dim`. `--max-dim` goes
because it is `texture_size` spelled a second time — its own help says "raise
alongside `--texture-size`, or the preprocess stage silently downscales the bake
back down", and chapel_arch confirms the coupling (bakes at 2048, ships three
2048² images). The preprocess stage takes the resolved `texture_size` directly.
`--max-bytes` stays: it is a per-kind budget (8 MB props, 16 MB characters,
VQ-B2), not a per-asset fact.

**`gen_character.py`** — same deletion of the `subject` positional, same
`--asset`; the hardcoded `--strategy multiview` goes with the strategy itself.
This closes §2's "characters inherit their contract by accident" — `character_skin`
is declared rather than inherited from `DEFAULT_ROUGHNESS`. `--height` stays: it
is not one of the six, and moving it into the registry would leave
`mixamo_rig.py`'s `TARGET_HEIGHT` as a second unclosed copy. `--mpfb` refuses
`--asset` exactly as it already refuses `subject`/`--seed`, because the
parametric path runs no texture stage; it does resolve `character_skin` from
`surface_classes.json`, deleting the third hand-spelling of the character
contract (`char_mpfb.py:361`, `Metallic 0.0 / Roughness 0.8`) — §2's remaining
mirror. That lands with row 23, which updates the callers.

**`subject` and `seed`** — `subject` in the registry, `seed` on the CLI, neither
in both. A sweep varies exactly one thing; everything it holds fixed is the
asset's declaration. So **there is no unregistered exploratory candidate**: the
entry is written before the sweep, not at promotion. One entry serves the whole
sweep, the winner installs under that same name, and an abandoned exploration is
deleted from the registry like any other dead declaration. Putting `seed` in the
registry too would force `gen_prop.py` to override it per candidate — the same
fact on two channels, rejected. Putting `subject` on the CLI would let two
candidates of one asset carry different prompts, which is D16/D17's provenance
drift restated. A shipped asset's seed is recovered from its installed
`generation_manifest.json`; reading a record to reproduce the thing it records is
what a record is for.

**`strategy`** — deleted, from `assets.json` and from the manifest extras alike.
Once `projection` dies the field has one possible value. What identifies the
generation path is the workflow's own identity — `prop_multiview.json` name +
sha256, already in the stage key (§3B) — which changes when the graph changes,
unlike a literal. Row 21's "zero matches for `multiview_controlnet_depth`" is
satisfied by deletion, not by deriving a constant.

**`concept_png` and the D12 refusal** — the positional is deleted;
`prop_texture.py` reads no concept image on any path. The refusal moves to the
matte's producer: `prop_hi3dgen.py`, immediately after `matte_concept()` and
before `concept_rgba.png` is written. Same two conditions (opaque fraction
≥ 0.995, or no opaque pixels at all), one stage earlier, where the matte's only
surviving consumer is `preprocess_image` — a degenerate matte there reconstructs
the background as geometry, which is D12's silent degeneration in the channel
that still exists. Row 9's verify for this half: a raw RGB concept (alpha ≡ 255)
exits non-zero from `prop_hi3dgen.py` before `raw.glb` is written, and the
BiRefNet-matted one passes.

### B. Content-addressed stage cache

Every stage declares `(stage version, resolved params, input content hashes) →
outputs`. The cache key is their hash; the cache directory is keyed by it. A
stage reruns iff its key changes.

One mechanism, three defects closed: stale-image reuse under changed inputs
(anatomy §8), the nine of eleven sub-stages that recompute needlessly every run
(three atlas bakes, all depth and normal renders, up to 37 candidate ortho
renders), and provenance drift — **the key record *is* the provenance**, derived
rather than transcribed, so D16/D17 cannot recur in that form.

### B.1 The key schema, stage by stage

**Stage version is derived, not declared — and so is its source set.** A
hand-bumped integer is a transcription, and §1's whole diagnosis is that
transcriptions drift; a hand-listed *set of files* is the same transcription one
level up, which is why row 24 does not keep one. `⟨v⟩` is the sha256 over the
stage's source set, and that set is the **transitive intra-tree import closure**
of the stage's entry module: walked by `ast`, resolving only names that land
under `scripts/ai-pipeline/`, so `bpy`/`cv2`/`numpy` fall out as toolchain
identity and ride the params instead. Adding an import extends the set
automatically; nothing can drift out of it. The closure reproduces exactly what
this section would otherwise have hand-listed — `comfy_run.py` lands in
`generate`'s set because `generate.py` imports it, and `scene.py` lands in
`atlas`'s because `atlas.py` imports it, which a hand-list would have missed. A
comment edit in `atlas.py` therefore re-bakes the atlas — CPU seconds — and does
not touch `generate`, whose closure is `{generate, comfy_run}`; that
proportion is the point, and it is now a checkable property rather than a claim.
**One edge no import expresses:** `albedo.py` spawns `prop_pbr.py` as a
subprocess, so `estimate` declares that one file explicitly. It is the only
declaration, and the list does not grow.

**Params are exactly the resolved facts**, from §3A.1: the registry supplies
everything fixed across a sweep, the CLI supplies `seed`. Anything else that
changes a stage's output is an implementation constant and is represented by
`⟨v⟩`, never copied into the record. That line is what deletes
`weight_exponent`, `occlusion_eps`, `edge_pad_px`, `depth_dilate_px` and
`ao_samples` from the manifest: a value worth reading in the record is a value
worth declaring in the registry, and if it is not declared it lives in the source
that `⟨v⟩` identifies. Toolchain identity rides the params of the stages that
run it: `blender` = `bpy.app.version_string` + `bpy.app.build_hash`, `np/cv2` =
both `__version__`, `comfy`/`torch` per below.

**Cache units are not functions.** Three of them are per-view or per-canvas
rather than per-call, because that is where the key is stable:

- **`depth` is keyed by direction, not index.** Today the base set, the NBV
  candidate grid and the picked extras render through the same `_render_depth`
  into three different filename ranges, and `render_depth_views(..., start=)`
  exists only to keep the numbering from colliding. Keyed on
  `(clean.glb, azimuth, elevation, view_res)`, all three draw from one cache: a
  picked candidate's depth is already a hit, so the re-render of every extra view
  disappears, and `start=` disappears with it. **This merges two of §3B's eleven
  sub-stages into one — ten stages after the ruling, not eleven.**
- **`generate` is keyed per canvas**, since one ComfyUI pass produces one canvas
  that is split into two views. `view_pairs` numbers the base pairs before the
  extras, so adding or dropping an extra view leaves every base canvas key
  untouched.
- **`estimate` is keyed per view**, which dissolves `pbr_meta.json` — a whole-run
  aggregate whose only job was to survive a partial resume.

| # | stage (§3D home) | resolved params in the key | input content hashes | outputs | cache dir |
|---|---|---|---|---|---|
| 1 | `atlas` — geometry atlas (`atlas.py`) | `texture_size`, `blender` | `clean.glb` | `pos.npy`, `nrm.npy`, `island.npy` | `target/prop-cache/atlas/<key>/` |
| 2 | `depth` — one ortho view (`views.py`) | `azimuth_deg`, `elevation_deg`, `view_res`, `blender` | `clean.glb` | `depth.exr` (true silhouette), `depth.png` (dilated 8-bit conditioning) | `…/depth/<key>/` |
| 3 | `nbv` — next-best-view pick (`coverage.py`) | the declared azimuth set + elevation, `blender` | `clean.glb`, `atlas`'s three outputs, `depth.exr` of every base view, `depth.exr` of every surviving candidate | `extras.json` — picked specs + predicted gain per pick | `…/nbv/<key>/` |
| 4 | `normal_view` — one camera-space normal + mask (`views.py`) — **runs only when `albedo_source: delit`** | `azimuth_deg`, `elevation_deg`, `view_res`, `blender` | `clean.glb`, that view's `depth.exr` | `normal.png`, `mask.png` | `…/normal_view/<key>/` |
| 5 | `generate` — one ComfyUI canvas (`generate.py`) | `subject`, each slot's `view_hint`, `canvas_seed` = `seed*100 + k`, canvas `width`=`view_res*len(pair)` / `height`=`view_res`, `comfy` | `prop_multiview.json`, each slot's `depth.png`, **every model file named by the graph** | canvas PNG, per-slot `gen_<slot>.png`, `comfy_run`'s `manifest.json` | `…/generate/<key>/` |
| 6 | `estimate` — one view's delight (`albedo.py` → `prop_pbr.py`) — **`delit` only** | `view_seed` = `seed*1000 + i`, `torch` | that view's `gen.png`, `normal.png`, `mask.png`, the estimator's weight files | `albedo.png` | `…/estimate/<key>/` |
| 7 | `blend` — reprojection, facing-weighted blend, gated inpaint (`albedo.py` + `atlas.py`) | `albedo_source`, the ordered view specs (`azimuth_deg`/`elevation_deg` per view), `np/cv2` | `clean.glb`, `atlas`'s three outputs, every view's `depth.exr`, every view's source image — `gen.png` under `direct`, `albedo.png` under `delit` | `base.png`, `coverage.json` (`blend_coverage`, `hole_texels`, `max_hole_depth_frac`, the covered mask) | `…/blend/<key>/` |
| 8 | `bake_normal` — hires→lores tangent normal (`export.py`) | `texture_size`, `blender` | `clean.glb`, `clean_hires.glb` | `normal.png` | `…/bake_normal/<key>/` |
| 9 | `bake_ao` — hires-cage AO (`export.py`) | `texture_size`, `blender` (**not** `ao_distance_m` — see below) | `clean.glb`, `clean_hires.glb` | `occlusion.png` | `…/bake_ao/<key>/` |
| 10 | `export` — material graph + atomic write (`export.py`) | `metallic`, `roughness`, `detail`, `blender` | `clean.glb`, `base.png`, `normal.png`, `occlusion.png` | `textured.glb` | `…/export/<key>/` |

`texture_size` appears on 1, 8, 9 and nowhere else: `blend` reads its atlas
dimension from the `atlas` arrays it is handed, so the two can no longer
disagree. `clean.glb` appears in every row that touches the mesh because the
camera rig — bounds, ortho scale, near/far — is derived from it, and no
downstream artifact carries those numbers.

Row 3 caches nothing worth caching: its cost is the candidate renders, and those
are row 2 entries. It is keyed and recorded because its *decision* is provenance
— which directions were added and what gain was predicted.

**Row 9 dropped `ao_distance_m`, and the rule that deletes it is this section's
own.** "A value worth reading in the record is a value worth declaring in the
registry, and if it is not declared it lives in the source that `⟨v⟩`
identifies" is the same sentence that deletes `ao_samples`; `AO_DISTANCE_M` is a
module constant, not a registry field, so copying it into params would have
contradicted the paragraph directly above the table. Invalidation is not lost and
is proven: editing `AO_DISTANCE_M` moves `export.py`'s version and therefore the
`bake_ao` key, while leaving `depth`'s untouched. Making it *readable* in the
record is a registry-field decision, not a cache one.

**Row 7 gained no param from row 27, and the rule that keeps it out is row 9's.**
The gate's threshold is `MAX_HOLE_DEPTH_FRAC`, a `coverage.py` module constant
rather than a registry field (§3A), so copying it into `blend`'s params would
contradict the paragraph above the table exactly as `ao_distance_m` would have.
Invalidation is not lost and needs no new import edge: `albedo.py` already
imports `covered_mask`/`coverage_stats` from `proptex.coverage`, so `coverage.py`
is in `blend`'s closure and editing the constant moves `blend`'s key. Row 7's
covered **mask** is likewise not an output — 4 M booleans is not a JSON payload
and no consumer exists; row 26's uncovered-island maps come from row 25's survey,
which is where that consumer actually lives.

Row 4 has **no consumer under `albedo_source: direct`.** `normal_<i>.png` and
`mask_<i>.png` are read only by `prop_pbr.py`; deleting MaterialAnything for the
non-foliage classes (§4) therefore deletes their renders too, for 5 of 7 props.
Nothing else in the pipeline reads them.

**The stage order is fixed and the cache never moves it.** Each key depends on
the previous stage's output hashes, so no stage's key is even computable before
its inputs exist — the chain is sequential by construction, not by convention.
The cache decides *whether* a stage runs, never *when*. `generate` opens the
ComfyUI server once, inside itself, iff at least one canvas key misses; the
11.5 GiB Hi3DGen peak is never concurrent with it.

**The cache root is `target/prop-cache/`, new and empty.** `target/prop-batch/**`
is not read, not indexed and not migrated (§8) — nothing to migrate is the point.
`multiview/` under the candidate dir is deleted outright: it existed only to hold
path-keyed resume state, which is the defect. Stages address their inputs by
cache path.

#### What is not reproducible from its key

A key states which inputs produced an output. For three stages it does not
promise that rerunning would produce the same bytes, and the record must say so
rather than imply otherwise:

- **`generate`** — CUDA sampler nondeterminism. The seeds are pinned
  (`seed*100+k`) and every model file is hashed, but the ComfyUI checkout, torch,
  the driver and the GPU are not files this stage can hash; they enter the key as
  a `comfy` toolchain string (ComfyUI git rev + `torch.__version__` +
  `torch.version.cuda`), which detects a swap and still does not guarantee
  bit-identity across one.
- **`estimate`** — the same, in fp16 through the MaterialAnything venv.
- **`export`** — Blender's glTF writer is deterministic for a fixed build, but
  the build is identified by `blender`, not hashed.

**~~`comfy_run.extract_models` returning `sha256: null`~~ — closed (row 24).**
An unhashed model used to record `null` and exit 0, so a key built on it was
blind to a model swap: the anatomy §8 defect relocated into the one stage where
it costs the most. `extract_models` now raises naming the model, the node id and
input key, and the `models.sha256` path it was looked up in. There is no
on-the-fly hashing path in that file and none was added — the manifest is the
single source of truth, so the fix is a refusal, not a fallback, and no flag
bypasses it. Verified with a **negative control**: with the fix stashed, the
probe's second case fails and the first still passes, so the probe detects the
original defect rather than passing trivially.

The Blender-side stages (1–4, 7–10) are reproducible for a fixed `blender` build:
1-sample EMIT bakes are exact lookups, Cycles seeds per pixel and sample so the
128-sample AO bake repeats, and `blend` is numpy plus a deterministic Telea fill.

**Gates are never cached.** `max_hole_depth_frac` is a cached *measurement*; the
§3C refusal is recomputed from it against `MAX_HOLE_DEPTH_FRAC` on every run. So
the threshold enters no key, and tightening it cannot be dodged by a hit.

#### The key record is the provenance record

Each cache directory holds a `key.json` beside its outputs:

```json
{ "stage": "generate", "unit": "canvas_0",
  "version": "<sha256 of the declared source set>",
  "params":  { "subject": "…", "canvas_seed": 4, "width": 3072, … },
  "inputs":  { "workflow:prop_multiview.json": "<sha256>",
               "depth:depth_0.png": "<sha256>", "model:z-image.safetensors": "<sha256>", … },
  "key":     "<sha256 of the canonical JSON of stage+version+params+inputs>",
  "outputs": { "gen:view_0.png": "<sha256>", … },
  "measurements": { },
  "elapsed_s": 61.4 }
```

**`outputs` and `measurements` are separate fields, and row 21 found out why the
hard way.** `outputs` is name → sha256 and nothing else: the cache row hashes,
compares and carries it as digests, so `blend`'s `blend_coverage` float landing
there would poison it silently. `measurements` is name → number — the third
category this section already names alongside key records and output hashes.
`blend` is the only stage that carries any today (`blend_coverage`,
`hole_texels`, `max_hole_depth_frac`).

**The chain is seven stages, not six**, and the missing one was found by the
producer/consumer graph rather than by inspection: `generate` lists
`depth:depth_<i>.png` among its inputs, and nothing produced them. `prep` (rig +
`bake_geometry_atlas` + `render_depth_views` + `pick_extra_views`) is that
producer, and it also carries the next-best-view diagnostic — `predicted_gain_texels`
and `predicted_gain_frac` belong to the stage that made the pick. Without it
`elapsed_s_total` also under-priced the cold chain rows 34/37 need.

**Row 21's stopping rule, which draws its boundary with row 24:** every input that
is a file on disk at record time gets hashed; in-memory handoffs between stages
are row 24's problem, because row 24 is what forces them to become files. So
`normal_bake`/`ao_bake` hash `clean.glb` + `hires.glb` (without which changing the
hires mesh would not invalidate their cache entry), `blend` hashes its per-view
albedo sources through `albedo.source_image` so the `direct`/`delit` policy stays
spelled once, and `export` leaves `inputs` empty because its three images are
still in memory.

`key` covers `stage`, `version`, `params` and `inputs` only — a key that included
its own outputs could not be computed before running. `outputs` and `elapsed_s`
are results, written once by the run that produced them and carried out of the
cache unchanged on every later hit.

`generation_manifest.json`'s `texture` section becomes exactly the ordered list
of those records, plus `hit: true|false` per stage for *this* invocation and a
chain total. `elapsed_s` is always the producing run's time, so the total prices
a **cold** chain — which is what rows 34/37 need, and what a fully-hit run would
otherwise silently misprice. Row 35's rebuild is a full miss (§8: the cache root
is new), so its total is the real number.

Everything the section holds today that is not a key record, an output hash or a
measurement is deleted:

| deleted from the manifest | replaced by |
|---|---|
| `strategy: "multiview_controlnet_depth"` (D17) | `generate`'s `inputs.workflow:prop_multiview.json` sha256 — it changes when the graph changes, which a literal never did |
| `views[i].seeds` — a dict keyed by ComfyUI **node id** (D16's shape: graph structure copied into a record, stale the moment the graph moves) | `generate`'s `params.canvas_seed`, a resolved fact |
| `views[i].models[].node_id` / `class_type` / `input` | `generate`'s `inputs`, keyed `model:<filename>` → sha256 |
| `views[i].prompt_id` | nothing — it points into a ComfyUI history destroyed when the stage kills its own server |
| `views[i].prompts` | nothing — derivable from `workflow` sha256 + `subject` + `view_hint`, all key material |
| `front_axis` | nothing — dies with `projection` (row 9) |
| `weight_exponent`, `occlusion_eps`, `edge_pad_px`, `depth_dilate_px`, `ao_samples` | **not deleted — moved into their own stage's `params`** (row 21). Folding them into `⟨v⟩` is row 24's call; parking them in `params` keeps the information and is where a key would want them anyway. The bake constants that were hardcoded in the operator calls (`cage_extrusion`, `max_ray_distance`, `margin`, `normal_space`, `AO_DISTANCE_M`) joined them — they change the output, so a record omitting them describes a bake it cannot reproduce |
| `pbr_estimator` (and `pbr_meta.json`) | per-view `estimate` records; **absent entirely** under `albedo_source: direct` |
| `base_bake_s` / `normal_bake_s` / `ao_bake_s` | per-stage `elapsed_s` + the chain total (row 21) |
| `textured_glb` (a path) | `export`'s output hash |
| `note` (hand-written prose) | nothing — a derived record has no slot for it |
| `views[i].depth_png_sha256` / `gen_png_sha256`, duplicated per view | not deleted, deduplicated: each appears once as its stage's output and once as the consumer's input |

Kept, because each is a resolved fact or a measurement: `subject`, `seed`,
`texture_size`, `view_res` (as `params.view_res`, not `render_resolution`),
`metallic`, `roughness`, `detail`, `ao_distance_m`, the per-view azimuth/
elevation, `blend_coverage`, `hole_texels`, `max_hole_depth_frac`, and every
output sha256.

**Consequences outside `prop_texture.py`.** `gen_prop.py`'s
`if textured_glb.exists(): skip` is the same path-keyed resume one level up and
is deleted: the chain always invokes `prop_texture.py`, which costs a few file
hashes on a full hit. Its other four skips — concept, geometry, cleanup,
preprocess/turntable — are the identical defect and are **not** closed here; they
are the same mechanism applied to stages this plan does not touch, and naming
them is not fixing them.

`install_asset` (§3F) does not synthesise provenance: the `texture` section is
the key records read from the cache for the glb it is installing, and a glb with
no cache entry is a refusal. An asset installed with a fabricated or empty chain
record is D9's shape — an asset nobody can tie to the run that made it.

### C. Refusal gates (F-II)

| gate | today | after |
|---|---|---|
| concept alpha | hard-fails (fixed at D12) | **not "unchanged" — it dies with the deletion.** The gate is implemented only in `concept_stats`, whose only caller is `basecolor_projection`, so deleting `projection` (§4) silently removes D12's fix and leaves the `concept_png` positional unread. Where it lives afterwards: §3A.1 |
| geometric coverage | `blend_coverage` written to stats, 0.5504 shipped | **fails when any hole component's extrapolation depth exceeds `MAX_HOLE_DEPTH_FRAC` = 0.015 of atlas width** (15 px @1k, 31 px @2k; derived at row 27), emitting the uncovered-island map, the offending components' depths, and the view directions that would cover them — the input F5 was planned around and never had. `blend_coverage` stays a recorded measurement and gates nothing: it is hole *area*, and row 26 measured area to mis-rank severity |
| inpaint | unconditional Telea over every uncovered texel | **the same predicate at the fill site, not a second threshold.** Telea runs only on components the coverage gate passed; a component over the cap raises `CoverageFailure` instead of being filled. One constant, one definition, two call sites — so an inpaint size limit cannot drift away from the coverage gate, which is the shape of defect §1 diagnoses |
| export | non-atomic; a truncated glb is not detected | temp-then-rename, then re-read and validate the written file |

**Extrapolation depth**, once, since both rows key on it: the L2 distance from a
hole texel to the nearest *covered* texel, maximised over each 8-connected hole
component. The distance transform's source set is the covered mask **alone** —
out-of-island gutter is not a source — so a hole enclosed by texture measures
about half its width while one running off a chart edge measures its full width,
which is what makes gravestone's 35 px edge strips rank above cypress's 40 px
enclosed leaf holes. That choice is not free: sourcing from "not a hole" instead
moves the measured maximum by up to 23% (broken_column 5.44% → 4.20% of width).

`coverage.py`'s `coverage_stats` does not compute this yet, and the gate is not
finished until it does. It returns `blend_coverage`, `hole_texels` and
`largest_hole_texels`; `largest_hole_texels` is replaced (swap rule — it has no
reader anywhere in the tree, `prop_audit.py:343` taking only the first two) by
`max_hole_depth_frac`, plus the per-component depths row 28's refusal message and
row 29's fill decision both read. It is an addition to a function that already
builds the same 8-connected labelling.

The coverage gate is the one that changes outcomes, and on today's inputs it
changes all of them: it refuses all seven shipped props (§8 row 27). 44.96%
filler was never a number anyone chose; it was a number nobody was shown.

### D. Stage decomposition

`prop_texture.py` stays the Blender entry point (thin CLI); the body moves to a
`proptex/` package beside it — `SCRIPT_DIR` is already on `sys.path`.

| module | absorbs | defect it retires |
|---|---|---|
| `scene.py` | import, render-settings **context manager**, one emission-graph builder | render resolution/format/colour-depth set inside `_ortho_camera` and never restored; `cycles.samples` hand-restored unguarded; three near-identical node graphs; cameras linked and never unlinked |
| `views.py` | view specs, camera rig, **one** near/far definition | near/far encoded three times (`:328`, `:349`, `:364`) and silently required to agree for depth linearisation |
| `coverage.py` | island coverage, NBV selection, the gate | D7; the 37 uncached candidate renders |
| `generate.py` | ComfyUI canvas lifecycle | unchanged contract — the server lifecycle is a **VRAM-sequencing invariant** (11.5 GiB Hi3DGen peak), not a convenience |
| `albedo.py` | albedo source policy, blending, gated inpaint | D5/D6 — `direct` vs `delit` is now a declared class property |
| `atlas.py` | geometry atlas, projection | one row-order convention, stated once (today depth PNGs are bottom-up and normal PNGs top-down, cancelling only by luck) |
| `export.py` | material graph, atomic export, validation | `use_selection=True` + camera cleanup, so correctness stops depending on `preprocess_prop.mjs` happening to scrub the scene |
| `provenance.py` | the stats record | derived from resolved values only |

### E. Lint replaces the hardcoded lists

`prop_material_matches_surface_class` reads `assets.json` + `surface_classes.json`
and asserts the shipped material. It **deletes** `stone_props_declare_detail` and
its hardcoded seven-prop list.

Two `kind`s, split by **who authored the material**. `surface_class` says what
the surface *is*; `kind` says which clauses of that class are assertions rather
than description.

- `generated` — this pipeline authored the material, so the class is a contract
  it obeyed. The seven props.
- `downloaded` — a third party authored it, so the class describes the surface
  and only the clauses the renderer actually depends on are enforceable.
  `rock_face_01`, `rock_07`, `rock_09`: Poly Haven, two `zones.ron` placements
  each, no `generation_manifest.json`, a real `metallicRoughnessTexture`, no
  `occlusionTexture`, no `extras`. All three are `surface_class: limestone`.

| assertion | `generated` | `downloaded` |
|---|---|---|
| `metallicFactor` | == class `metallic` | == class `metallic` — a dielectric is a dielectric whoever authored it |
| `roughnessFactor` | == class `roughness` | == **1.0**: the factor multiplies the author's roughness map, and any other value silently rescales it |
| `extras.vordar_detail` | == class `detail` | **`false`** — the overlay is ours to stamp, and pinning it off forces a decision the moment anyone stamps it |
| `occlusionTexture` present | required | not asserted |
| `metallicRoughnessTexture` absent | required | **inverted: required present** — the roughness lives in that map, and losing it would read as a uniform 1.0 |

All three rocks are green on arrival under this, so row 8's red still names
exactly the six. **The `downloaded` extras row says `false`, not "absent",
because that is the distinction the renderer can see.** `MaterialData::detail`
is a `bool` defaulting to `false`, so absent and present-and-`false` are one
state on every path that consumes it; asserting literal absence would need a
second glTF reader parsing raw JSON alongside `load_gltf_data`, for a difference
no shader, no bake and no lint clause can observe. Stamping `true` on a rock
still fails, which is the whole forcing function.

The occlusion row is the only one asserting nothing, and the reason is not
convenience: the clause exists to prove the hires-cage AO bake ran (§3D
`export.py`), a step a downloaded asset never performs. Whether the rocks should
bind their ARM texture's R channel as `occlusionTexture` — Poly Haven packs AO
there and it ships unbound today, while every generated prop has AO — is a real
gap and a content fix, not a lint clause.

**Registration is one-directional.** Every `zones.ron` placement must resolve to
an `assets.json` entry, keyed by prop directory name (`prop_audit.py`'s existing
convention, `Path(model).parent.name`); a placement with no entry is a
**failure**, not a skip. An asset nobody asserts anything about is exactly how D9
happened, and skipping unregistered assets would make "add nothing to the
registry" the way to silence the lint. The converse is not an error: an entry
whose asset is not yet installed is a declaration awaiting its sweep (§3A.1) —
placed nowhere, rendering nothing.

This converts F-III from invisible to a red test — see §6.

### F. Install is a command, not a copy

D9's cause, in scope by ruling. Installing a prop today is a manual file copy;
`36f1c29` fixed the contract and six assets never received it because nothing
carried the fix from the script to the asset.

`install_asset` — one command, refusing at every step rather than proceeding:

```
resolve class from assets.json → read the chain record beside the built glb
  → verify that record against the glb and the class → copy → bake sidecars
  → write generation_manifest.json → run the lint clause
```

**The stamp step is deleted, and row 31 is where the design was re-derived.**
This section originally had install stamp `metallic`/`roughness`/
`extras.vordar_detail` onto the glb from the class. Three facts kill it. It is a
second spelling: `export.py` already writes all three from the same registry
contract, and row 30's validator re-reads the written glb and refuses if any
disagrees. It breaks provenance: rewriting the glTF JSON chunk means the
installed bytes are not the bytes the chain record's `export` entry hashed, which
is §7's staleness defect in a new form. And where it would *not* be a no-op it is
actively wrong — `export`'s cache key includes exactly those three params
(§3B.1 row 10), so a glb built under a superseded class table must force a
rebuild, not be stamped over.

What replaces it is a **verify** step reading data the record already carries:
`sha256(built.glb)` must equal the `export` entry's `outputs["export:textured.
glb"]`, and that entry's `params` for `metallic`/`roughness`/`detail` must equal
the resolved contract. That binds the asset to the run that produced it — the
guarantee a `target/prop-cache/` reverse lookup would have given, without the
reverse index, which does not exist.

So install never changes the bytes it installs, and the ordering guarantee gets
stronger rather than weaker: `final_glb_sha256` is computed last and equals both
the source glb's hash and the export stage's own recorded output hash.
`bake_textures.mjs gltf` was checked and writes only the `.textures/` sidecar
directory, never back to the glb.

`set_material_extras.mjs` is deleted (swap rule), but its job passed to
`export.py`'s native stamping (`export_prop` sets `vordar_detail` and exports
with `export_extras=True`), not to this command.

The rebuild of the six props (§6) runs through this command, so the rollout is one
repeatable invocation per prop instead of six hand copies — the same manual step
that produced D9.

## 4. What gets deleted (swap rule)

| deleted | why |
|---|---|
| **the `projection` strategy** — `basecolor_projection`, `concept_stats`, `project_uvs`, `FRONT_AXIS`, the branch | All seven shipped props are `multiview_controlnet_depth`; `gen_character.py` hardcodes multiview. Projection is `gen_prop.py`'s *default* and is used by nothing shipped, while carrying three open defects (D18 a–c) |
| `view_<i>/bump.png` and the estimator's bump head | Generated, hashed, resume-gated — **consumed by nothing**. F3 proved the head is blank (island mean `(129,127,255)`, std 4–6/255). Costs GPU per view for nothing |
| MaterialAnything **for every non-foliage class**, and with it those classes' per-view `normal_<i>.png` / `mask_<i>.png` renders | Once `albedo_source: direct` is declared for stone and wood, the estimator's last remaining role is gone for 5 of 7 props, and with it a hardcoded `C:\tools\MaterialAnything\venv` dependency on their path. `prop_pbr.py` is the **only** consumer of the normal/mask renders (§3B.1 row 4), so under `direct` they are GPU-free but wholly unread work |
| `blend_views(filename=, srgb=)` params + their docstring | Unreachable; one call site, both defaults |
| `scripts/ai-pipeline/bakeoff/` — **the whole directory**: `run.py`, `lit_control.py`, `wf_zimage.json`, `wf_qwen.json`, `wf_zimage_short.json`, `metrics.py` | D20 holds for `run.py:94` and `lit_control.py:40` (both call `pt.mv_camera_rig(clean)` against the two-arg signature at `prop_texture.py:332`), and the three `wf_*.json` are reachable only through `run.py`'s `WORKFLOWS` map. `metrics.py`'s `__main__` reads a bake-off output tree, so it dies with its only producer, and `normals_from_depth` serves only that `main()`. The three **live** functions — `baked_fraction` (with `_light_dirs`), `luma_of`, `rgb_of`, imported at `prop_audit.py:32` and the instrument behind every `baked_fraction_ts` in this campaign — move **into `prop_audit.py`**, their only caller: it is plain-Python numpy+Pillow exactly as they are, `proptex/` is Blender-side and cannot hold them, and a module with one consumer is an abstraction for single-use code. `prop_audit.py:18` and `:224` cite `bakeoff/metrics.py` and go stale with the move. The Qwen-fallback record survives where it already lives, `tasks/ai-pipeline/research/a5b-bakeoff-results.md`; `README.md:43`'s pointer at the directory repoints there |
| the six per-prop CLI flags | §3A |
| `scripts/asset-pipeline/set_material_extras.mjs` | §3F — `export.py` stamps `extras.vordar_detail` natively, so the hand-run patcher has nothing left to do |

## 5. Execution model

Per the routing rules, with this session's amendments recorded in
`tasks/lessons/`:

| tier | work |
|---|---|
| **opus** | every visual judgment (before/after sheets, blind test vs `rock_face_01`, coverage-map review) — *never* delegated below this tier, and never merged into the task that produced the render |
| **fable**, or opus while fable's quota is out | the stage-cache design, the coverage-gate threshold derivation |
| **sonnet** | module extraction, the lint clause, registry loaders — implementation only, no findings |
| **haiku** | gate re-runs, bakes, file moves |

## 6. Decisions (ruled by the user, 2026-07-25)

1. **Registry in scope** — approved with the plan. The spine stands.
2. **Lint covers all classes; the six props get rebuilt.** F-III closes fully
   rather than half. The lint is red between landing the code and finishing the
   rebuilds, which is the forcing function working. The rebuild is a **separate
   §8 go-ahead**, priced by timing the first prop. Manifests do record
   `texture.base_bake_s` / `normal_bake_s` (12.8–319.5 s), but every one was
   measured on a **resumed** run whose `gen.png`/`albedo.png` already existed, and
   nothing records end-to-end chain time — so no cold rebuild cost exists today
   and none will be guessed. Per-stage elapsed time is added to `provenance.py`
   before the first rebuild, not after.
3. **Delete the `projection` strategy** — approved with the plan (§4).
4. **No metal class.** Dissolved, not deferred: `candelabra_shrine` is painted
   iron, i.e. a dielectric, so it was never a metal reference and never needed
   one. See §3A. The real metal asset is the **sword**, which today is a blocky
   procedural placeholder (`client/vordar-client/src/weapons.rs:1`) — a new asset
   and a different pipeline (character gear, socket-attached), so it is named here
   and deliberately not scoped in.
5. **Install is in scope** — §3F.

**Ruled 2026-07-26, on row 27b's finding:**

6. **The hollow shell is fixed at its root, in Hi3DGen's extractor** — "we should
   do the cleanest job, dont do mess over mess trying to clean errors". This kills
   row 27a's options 1 and 2: no interior-face cull in `prop_cleanup`, and no
   island-mask exclusion that merely stops the gate from seeing the defect.
7. **The fix is carried as a fork of `Stable-X/Hi3DGen`, pinned by us** — not a
   patch file applied to a vanilla install, and not vendored into this repo. A
   patch adds an application step that can be skipped and a pin that goes stale;
   vendoring shadows the dependency with a second copy that can diverge. The fork
   makes the install reproducible from a ref with the fix's rationale in a commit
   message and no second spelling anywhere. The fork is
   **`https://github.com/TycheDea/Tyche3DGen`**, forked at `c29f668`, wired into
   `C:\tools\Hi3DGen\Hi3DGen` as remote `fork` beside upstream `origin`. An
   upstream PR follows from the same commit; the bug is genuinely theirs.
8. **One timed prop regeneration approved** (§8 heavy compute), `broken_column` /
   `b3/column/cand_0` — the highest interior fraction at 53.8%, so the sharpest
   test, and it needs regenerating anyway for row 26a's key-light defect. It is
   simultaneously the only way to test the fix on real SLat data, since no latent
   survives. Its `hi3dgen_manifest.json` records **seed 0** and the concept's
   sha256, so re-running from the same `concept.png` at the same seed changes
   exactly one variable: the extractor. Cost of the remaining six is priced off
   this run's measured wall-time, not estimated.

**Open, not blocking this plan:** nothing states what the churchyard zone *is*,
so asset choices accumulate rather than derive — `candelabra_shrine`, an interior
object, sits outdoors in three placements. `assets.json` makes the set enumerable
for the first time and therefore reviewable, but the premise itself is content
direction, not pipeline. Settled in its own pass; see
`tasks/lessons/2026-07-25-assets-need-a-content-premise.md`.

## 7. Carried uncertainties

- `preprocess_prop.mjs` constructs `new NodeIO()` with **no extensions
  registered** — any glTF extension present would be silently dropped on write.
  Harmless today (`extensionsUsed = null` on all seven) and outside this scope,
  but it is a live trap for any future extension use.
- `final_glb_sha256` and `bake.sha256` are stale by exactly +32 bytes on the four
  detail-opted props: `set_material_extras.mjs` rewrites the glb after the
  manifest is written. §3F removes the cause by ordering the install steps; the
  four are **rebuilt, not re-stamped**, so no migration path is needed. The
  authoritative hash meanwhile stays `<name>.textures/manifest.json:sha256`, which
  the lint already asserts byte-exactly.
- **`gen_character.py`'s preprocess stage is not wired to `texture_size`.** Row 23
  wired `gen_prop.py`'s `stage_preprocess_bake` to `contract.texture_size`, closing
  the silent-downscale coupling that `--max-dim` spelled twice. The character path
  has the same stage and still takes `preprocess_prop.mjs`'s bare 1024 default —
  but it never had a `--max-dim`/`--texture-size` flag to collapse, so there was
  nothing for row 23 to delete, and `assets.json` today holds **zero** entries with
  `kind: generated` + `surface_class: character_skin`, so the path resolves no asset
  at all. Closes when the first character asset is declared, not before; the fix is
  one parameter, and naming it here is not fixing it.
- **~~`prop_tonal_audit.py`~~ — resolved 2026-07-25 (user delegated the call):
  deleted, with its README section.** Three facts forced it over "update it to
  the record shape". Its question is answered — its own header calls it
  decision-bearing for the MaterialAnything keep/drop A/B, landed as
  `albedo_source: direct` (rows 11/19). Its subject is gone — it is hardcoded to
  `target/prop-batch/b3/arch/cand_0`, under gitignored build output, and its own
  README section said the evidence it produced lives "not in this repo". And
  decisively, its STAGE C/D is **a second channel for coverage that the file
  itself documents as wrong**: a facing+frustum proxy with no occlusion test,
  written that way only because "no EXR-capable library is available in this
  system Python". Row 17 dissolved that constraint by running the real path
  under Blender (`proptex/coverage.py`), so updating the script would have meant
  maintaining a knowingly-worse spelling of a number the pipeline now measures
  properly. Deleting orphaned nothing: all four `prop_audit` helpers it imported
  (`load_gltf`, `accessor_array`, `iter_prims`, `island_mask`) are used by
  `prop_audit.py` itself.

  **The deletion exposed the real defect it was masking.** `prop_audit.py` —
  the live, all-props instrument — read the *same* flat manifest keys, via
  `tex.get("blend_coverage")` / `tex.get("hole_texels")`. After row 35 both
  would return `None` and print as blank cells **identical to `rock_face_01`'s
  legitimately-empty ones**, i.e. a stale record rendered as "not generated".
  README §706 already described the record shape, so the docs were a stale
  claim against the code. `generation_stats` now reads the `blend` record
  (`measurements.blend_coverage` / `measurements.hole_texels`,
  `params.texture_size`) and **refuses** — stderr + exit 1 naming the prop — on
  a manifest with no `blend` stage, distinguishing "stale" from "never
  generated" instead of collapsing them. No dual-shape read: a compatibility
  path for a state that exists only between now and row 35 is exactly the
  speculative flexibility §2 forbids, and the refusal surfaces a deliberately
  un-rebuilt chapel_arch (the row-34 six-or-seven question) at the moment the
  decision is made rather than silently, later. Verified by probe against all
  three cases, the third against the **actual** shipped `chapel_arch`
  manifest: no manifest → `(None, None)`; record shape → `0.5504 / 0.2868`;
  shipped flat shape → rc 1, message names `chapel_arch`.
- **~~`min_coverage`~~ — settled at row 27, 2026-07-26: the concept is deleted,
  not re-numbered.** The retraction was that 0.80 refuses all seven props on
  arrival (measured `blend_coverage` spans **0.4879–0.7623**: broken_column
  0.4879, gravestone 0.5154, chapel_arch 0.5504, crucero 0.5743, olive_stump
  0.5851, candelabra_shrine 0.6088 shipped / 0.6477 recomputed, cypress 0.7623),
  and that foliage's 0.60 was equally underived. Row 27 found the deeper fault:
  a coverage **fraction** is hole *area* normalised, and row 26 measured hole area
  to mis-rank severity — candelabra's 43 136-texel disc reads dead while
  chapel_arch's 62 491-texel strip does not. It is not even a conservative proxy
  for the depth clause that replaced it, since it errs both ways: `cypress` is the
  best-covered prop at 0.7623 and still carries a 2.73%-of-width component, while
  an atlas at coverage 0.50 whose every component sits below 0.4% depth is
  acceptable by row 26's own band and would be refused by any threshold worth
  setting. So no number rescues it. `blend_coverage` and `hole_texels` survive as
  **measurements** — `prop_audit.py:343` reads both, and they are the unit this
  campaign's before/after is stated in — and gate nothing. The gate is
  §3C's single depth clause.

## 8. Execution plan

**Progress: rows 1–32 are done. Rows 11 and 19 stand as recorded (11
incomplete, closed by 19).** Row 26a ruled `albedo_source: direct` everywhere it
can be measured, leaving the estimator dead code the user chose to keep. Row 27
ruled one constant, `MAX_HOLE_DEPTH_FRAC = 0.015`, no registry field, and found
the blocker **row 27a** now carries: `MV_EXTRA_MAX = 2` may make that gate
unsatisfiable, so it is re-derived before row 34 prices a rebuild, not merely
before row 35. Row 31 deleted its own stamp step (§3F) and row 32 followed it.
Row 33's gate is done and the red is the intended shape. **Row 27a is done and
its answer is a refusal**: no pick cap satisfies the depth gate on any prop —
2.41% is the best reached at 41 views against a 1.5% cap — so neither constant
moved, and the blocker it found instead is the mesh, about half of every prop
being interior surface no view can reach. **Rows 34–38 wait on the user's ruling
on that**, which is what row 34 must now carry. Rows 34 and 37 remain user asks.

**Committed at this point** (branch `ai-pipeline`, unpushed): `9e6e75c` the depth
gate (rows 27–29), `ec94893` atomic export, `install_asset` and the
`set_material_extras.mjs` deletion (rows 30–32), `37a6faf` row 27a's comment
correction to `MV_EXTRA_MIN_GAIN`, `196ac50` the vectorised
`hole_component_depths`, `787cf74` the reachability-restricted coverage gate
(row 27m).

**Reproducing rows 25–26's numbers.** Per prop, over the seven installed props:

```
blender --background --python scripts/ai-pipeline/proptex/coverage.py -- \
    content/models/props/<name>/<name>.glb --asset <name> \
    --map target/prop-redesign-baseline/holes_<name>.png
```

Tonal stats read `basecolor_<name>.png` (the glb's embedded basecolor, which the
DDS sidecars cannot supply) masked to the hole map's covered texels — an
atlas-wide mean averages in the Telea filler, and the filler is brighter than the
content on all seven, so it flatters exactly the props with the most to hide.
Both loops ran from a scratch driver, not a committed script; the artifacts are in
`target/prop-redesign-baseline/` and the numbers are in the row 25/26 cells above.
**Folding both into one committed instrument is row 26a's to do**, since rows
35–38 need the same measurement again as the rebuild's before/after.

**Row 8 was skipped and this file claimed otherwise for the length of the phase**
— found 2026-07-25 at row 24's close, landed the same day. The overclaim lived in
this progress paragraph alone; row 8's own cell carried no **Done** marker, and
`content_lint.rs`'s last commit (`7999a60`) belonged to the detail-layer campaign.
A progress line is a transcription of the table it summarises, which is §1's
diagnosis applied to this file — `tasks/lessons/2026-07-25-summary-is-a-transcription.md`.

`prop_texture.py` is **911 → 349 lines**; `proptex/` is 1436 across eleven
modules (`registry`, `scene`, `views`, `atlas`, `coverage`, `albedo`, `generate`,
`export`, `cache`, `provenance`, `__init__`). Row 24 landed in three waves — the
mechanism (`cache.py`, stdlib-only), the geometry units, the generation units.

**Row 24's one open design question, settled: how `⟨v⟩`'s "declared source set"
is declared.** §3B.1 hand-lists a source set per stage, and that list is itself a
transcription — the exact failure mode §1 diagnoses. Every stage module imports
`proptex/scene.py`, so a `scene.py` edit changes their output and a hand-list
would miss it. So the set is **derived, never declared**: the transitive
intra-tree import closure of the stage's entry module, walked by `ast`, resolving
only names that land under `scripts/ai-pipeline/` (`bpy`, `cv2`, `numpy` fall out
as toolchain identity and ride the params instead). Checked against the real
import graph, the closure **reproduces §3B.1's hand-written source sets exactly**,
including the proportion claim the design rests on: `generate.py`'s closure is
`{generate, comfy_run}` and contains no `atlas.py`, so a comment edit
in `atlas.py` re-bakes the atlas and does not touch `generate`. Exactly one
irreducible declaration survives — `prop_pbr.py`, which `albedo.py` spawns as a
**subprocess**, an edge no import expresses.

Three smaller calls made along with it:
- **Output keys are derived, not declared:** a record's `outputs` keys are
  `f"{stage}:{filename}"`. The producing stage is then readable straight off the
  key, so a downstream stage declaring the same string as an input is what makes
  the producer/consumer chain mechanically walkable. This deletes row 21's ad-hoc
  prefixes (`gen:`, `depth:`), which named a producer that no longer had to be
  guessed.
- **The cache wraps at the call site in `prop_texture.py`; stage modules never
  import `cache.py`.** Otherwise `cache.py` lands in every stage's closure and
  every stage's version moves whenever the cache moves.
- **A relative import is a refusal, not a resolution.** The closure walk resolves
  absolute imports only; a `from .scene import …` would silently drop a file from
  the set and leave the version blind to edits in it. The tree uses absolute
  imports throughout, so refusing costs nothing today and cannot go quietly stale
  tomorrow — the alternative is implementing resolution for a form nobody uses.

Probed, not asserted: key stability across dict-order permutations; every input
hash and every param change moving the key; `source_version(atlas.py)` moving
when `scene.py`'s bytes change while `source_version(generate.py)` does not;
miss→hit round-trip with `produce` called exactly once and `elapsed_s` carried
from the producing run; and a failed `produce` leaving no `key.json` behind, so a
half-written stage can never be recorded as a success.

**Wave 1 (`atlas`, `depth`, `nbv`, `normal_view`) is landed, and the decisive
number is that it moved no behaviour.** chapel_arch's coverage comes back
byte-identical to the archived values — `blend_coverage` 0.5504, `hole_texels`
1202912, `largest_hole_texels` 62492, base-set 0.4975 / 1344337 / 63420, the
single pick `az 0, el −35` at gain 141425 (0.0529) — measured before and after
the change, not merely against a remembered figure.

**What keying by direction bought, measured:** the cold run renders 37 depth
entries and yields 5 views; the warm run re-renders **zero**; and the picked
extra view reuses the entry its own candidate render created, so an extra view
now costs nothing. `start=` is deleted with zero occurrences left in
`scripts/ai-pipeline/`, and with it the flat `work_dir/<name>_<i>.png`
convention for these stages — the three path-keyed consumers take explicit path
lists instead. `pick_extra_views` split into a pure candidate enumerator and a
pure-numpy picker with no `bpy`, no `work_dir` and no `view_res`.

**The subtle find, which had a control probe written for it:** an int `0` and a
float `0.0` azimuth serialise differently in canonical JSON and therefore hash
differently, so without coercing angles to float a picked extra would have
*missed* the candidate entry it was supposed to hit — the wave's entire benefit,
silently absent. The probe asserts the un-normalised form would collide-miss, so
the coercion cannot be dropped unnoticed.

**Two calls made on wave 1's findings:**
- **Every record is kept; nothing is elided.** The chain grew from one `prep`
  record to 39 for chapel_arch's geometry (1 atlas + 37 depth + 1 nbv), because
  each candidate render is a real entry with real `elapsed_s`. Eliding candidates
  would be a second manifest shape *and* would misprice the cold chain that rows
  34/37 exist to measure. Tens of KB is not a cost worth a second shape.
- **`coverage.py`'s standalone report stays deliberately uncached**, rendering
  into a temp root. It is a survey across archived meshes (row 25 runs it over
  seven), and populating the stage cache from it would turn row 35's rebuild into
  a partial hit whose total prices a warm run — destroying the one number rows
  34/37 need. Stated as a constraint in the code, since the obvious "improvement"
  is to wire it to the cache.

**The invariant wave 2 must establish, found while briefing it:** stage logic has
to live in the stage module, because `⟨v⟩` is the closure of a stage's *entry
module* and `prop_texture.py` is in no stage's closure. Anything doing real work
in the orchestrator is invisible to versioning — editing it would not invalidate
the entry and the cache would serve a stale output. Two live violations:
`estimate_materials` (which builds and launches the MaterialAnything subprocess)
must move to `albedo.py`, and the bake logic with `AO_SAMPLES`/`AO_DISTANCE_M`/
the four `BAKE_*` constants must move to `export.py` — in both cases to exactly
where §3B.1's table already says those stages live.

**Wave 2 is landed; row 24 is complete.** Both moves above were made, and
`prop_texture.py` now holds no function that touches an image or a mesh — only
params/inputs dicts, `cached` calls and chain assembly. It shrank by 52 lines and
`prop_pbr.py` by 43, against a whole-change net of **+84**: the two largest files
both got smaller while the cache layer landed.

**Wave 2 found a live violation wave 1 left behind, and it was in the one place
that would have hurt most.** `generate.py` imported `sha256_file` from
`proptex.cache`, which put `cache.py` into `generate`'s closure — so any edit to
the cache would have re-run every ComfyUI canvas in the system. Independently
verified after the fix: `cache.py` is in **no** stage's closure, and `generate`'s
is exactly `{generate.py, comfy_run.py}`.

**The output-key format changed, and the reason is the same drift this design
exists to kill.** Wave 1 keyed outputs `<stage>:<filename>`, but `nbv` consumes
37 depth entries whose files are *all* named `depth.exr`, so they collide in one
`inputs` dict — which wave 1 worked around by writing consumer-side keys
(`f"depth:{unit}.exr"`) that **no producer ever wrote**. That is a transcription,
and it would drift. Keys are now `<stage>[:<unit>]:<filename>` and consumers
merge the producer's key **verbatim** through `cache.outputs_of`. The chain walk
became pure set-inclusion with digest equality: 61 internal edges for
chapel_arch, 88 for cypress, **zero holes**, with negative controls proving the
walker catches a renamed producer key.

`cache.hits()` was added because §3B.1 requires ComfyUI to open *iff* a canvas
misses, and `cached` cannot answer that without running `produce`. It shares one
`_entry` with `cached`, so the two cannot disagree; the probe confirms the server
opens once cold and never warm.

**Measured, on real archived meshes** (only the two GPU produce bodies stubbed —
every key, inputs dict and cache decision real): chapel_arch 46 records,
cypress 58. Cold missed every stage; warm hit every stage and **recomputed
nothing**; warm carried `elapsed_s` unchanged. Bumping `texture_size` re-baked
normal+AO+export and re-rendered **no depth**. Across 119 cache entries, none
carries `hit` in its `key.json` and none carries a null `version` or `key`. Both
exported glbs still carry all three textures, the scalar factors and
`extras.vordar_detail`, so replacing `save_textures` with cache-entry PNG loads
preserved behaviour.

The sharpest single result is cypress's perturbed run: a slightly different atlas
made `nbv` pick a **different direction**, which cost one new `normal_view`, one
canvas and one estimate — and **zero depth renders**, because the newly-picked
candidate's depth was already an entry. That is wave 1's promise firing under a
real perturbation rather than a constructed one.

**Three costs accepted rather than engineered away, all recorded for the row-34
wall-time ask:**
- **`estimate` launches one `prop_pbr.py` per view**, so the 4.3 GiB estimator
  loads per view: roughly +25–40 s × N views, cold-run-only and `delit`-only, so
  cypress's six views carry +150–240 s. The symmetric fix (a stdin-driven worker
  gated by `hits()`, mirroring `comfy_run.server()`) was deliberately **not**
  built — it is machinery nobody asked for, and per-view launches satisfy the
  contract. It is a tradeoff, not an oversight, and it feeds row 34's estimate.
- **Toolchain probes cost ~10 s per run, hit or miss** (`comfy_id` imports torch
  at 4.7 s, `torch_id` 5.5 s), because they must resolve before hit/miss can be
  decided. Noise against a cold chain; the dominant cost of a fully-warm one.
  Reading `torch/version.py` instead of importing torch would derive the same
  fact ~1000× faster — a real follow-up, not a blocker.
- **`comfy_run.py` now sits in `blend`'s closure**, because `albedo.py` imports
  its `load_model_hashes` to hash the estimator weights (measured: hashing 4.3 GiB
  on the fly costs 13.4 s *every* run, including a full hit — so the manifest
  stays the single source of truth, and a missing entry is a refusal, matching the
  `extract_models` ruling). The cost is that a `comfy_run.py` edit needlessly
  re-keys `blend`. The alternatives — a second spelling of the manifest reader, or
  a module for one function — are both worse than the bounded waste.

`prop_texture.py` is **911 → 318 lines**; `proptex/` is 1075 across ten modules
(`registry`, `scene`, `views`, `atlas`, `coverage`, `albedo`, `generate`,
`export`, `provenance`, `__init__`).

**What has NOT been run, stated plainly.** No end-to-end invocation has happened,
because one needs a ComfyUI generation pass — heavy compute awaiting a go-ahead
(CLAUDE.md §8). Row 35's rebuild is the first.

**Exercised for real, against archived meshes read from each manifest's
`candidate_dir`:** the entire geometry path at full resolution (import, camera
rig, atlas bake, 37 depth renders, next-best-view pick, coverage stats), whose
numbers reproduce the archived manifest exactly; the normal and AO bakes;
`export_prop`, whose output glbs still carry all three textures, the scalar
factors and `extras.vordar_detail`; `blend_views`; and every key, `inputs` dict
and cache decision in the chain, cold and warm, at 256².

**Exactly two things are stubbed, and both are the GPU bodies themselves:** the
ComfyUI canvas render and the MaterialAnything per-view estimate. Everything
around them — their keys, their model hashes, their hit/miss decisions, the
`comfy_run.server()` lifecycle gate — ran for real. So what row 35 will exercise
for the first time is the *content* those two produce, not the machinery that
decides whether to produce it.

An AST arity check plus an orphan scan across the package confirm no signature
drift survives the refactor, and both were mutation-tested to prove they are not
vacuous. That is still not a run.

**Row 20 made `bpy.data.objects.remove(hires)` redundant and it was deleted.**
`use_selection=True` already excludes every unselected object, so the hand
removal was the second mechanism enforcing the same fact. Also cleared the last
three `tasks/` citations in committed source — `proptex/__init__.py`'s header and
two in `prop_texture.py`'s — dangling pointers into a gitignored directory, and
provenance rather than constraint besides. `grep -rn "tasks/"` over the package
and `prop_texture.py` now returns nothing.

**No plain `python` in this environment can import the pipeline's own
dependencies.** Row 18 needed a non-Blender interpreter with `cv2` to prove
`generate.py` is Blender-free; the system `python` (3.14) has no `cv2`, and
neither Blender's bundled interpreter nor ComfyUI's embedded one is plain. The
only interpreter satisfying both is `C:\tools\MaterialAnything\venv\Scripts\
python.exe`. Rows 20–21 and any later row wanting a "plain python" check must use
it, or state that no such check is possible.

**Row 17's entry point cannot be `python -m` and the plan was wrong to ask for
it.** `bpy` is not importable outside Blender, and coverage needs a Cycles EMIT
bake plus ortho depth renders. The only way to keep the literal spelling would be
a numpy reimplementation of the bake and the depth renders — a second channel that
drifts from what the pipeline actually measures, which is the defect this plan
exists to delete. So the module runs under Blender, matching `prop_texture.py`'s
existing idiom, and rows 25 and 28 carry the corrected invocation:

```
blender --background --python scripts/ai-pipeline/proptex/coverage.py -- \
    <clean.glb> --asset NAME
```

It resolves azimuths, `texture_size` and `view_res` from the registry contract
rather than defaulting them, and prints one JSON object so row 25 collects rather
than parses prose.

**Row 17's real find was a parameter that should never have existed.**
`depth_setup`/`normal_setup` took `hires` solely to `hidden(hires)` it out of the
depth render, so the standalone entry point — which loads only `clean.glb` — had
nothing to pass. The invariant those calls were reaching for is "only the clean
mesh renders", so `hidden(obj)` became `isolated(obj)`, which hides every other
scene **mesh** and restores each one's prior `hide_render`. `hires` then vanished
from five signatures and every call site: a net deletion, not the optional
parameter the wall was inviting.

**Decided while unsure (§6), one item.** Row 19 came back with `albedo.py`'s
`bpy`/`cv2`/`atlas`/`scene` imports pushed inside `blend_views`'s body, so
`source_image` stayed importable without Blender, plus a three-line comment
explaining the placement. I moved them back to module scope. Reason: the only
consumer that wanted the policy Blender-free was the probe, no later row needs it
(row 21's provenance keys `albedo_source` as a *param*, and row 31's install
stamps from the class and never resolves a view path), and a comment justifying
where imports sit is a workaround being narrated. Reversible in one commit if a
plain-Python consumer appears.

**Three verify cells in this phase have been wrong, and each was caught by the
worker refusing them rather than by review.** Row 10 demanded zero `bump` matches
(one is a required third-party input key); row 14 wrapped two of three callers
(the settings belong to the camera's lifetime, not the caller's); row 15's cell
was tautological by construction. Write verify cells that can *fail* — the
standing rule is `tasks/lessons/2026-07-21-probe-must-fail-when-broken.md`, and
the failure mode here is mine specifying them, not workers dodging them.

**The pipeline is invokable as of row 23 but still breaks on `direct` assets —
row 11 is incomplete and row 19 is the fix.** Row 11 gated `estimate_materials`
behind `needs_estimator(contract)`, but `blend_views` still loads
`view_<i>/albedo.png` unconditionally (`atlas.py:134`) — the file only the
estimator writes. So every `albedo_source: direct` asset now fails there, and that
is **9 of the 10 registry entries**; only `cypress` is `delit`. §3B.1 row 7 already
specifies the correct behaviour ("`gen.png` under `direct`, `albedo.png` under
`delit`") and row 19 implements it.

Row 11 was marked done on a **partial verify**: its cell required "a chapel_arch
run writes no `normal_<i>.png`/`mask_<i>.png` while a cypress run writes one pair
per view", which needs a run, and row 11 itself made the pipeline unrunnable by
requiring `--asset` before any caller passed it. The two static clauses passed and
the run clause was never executed. **Row 19 moves up to immediately after row 16.**

`prop_texture.py` carries zero module globals and zero occurrences of
`TEXTURE_SIZE` / `MV_RES` / `MV_VIEWS`.

**§3D's row-order claim is refuted, and §3D is wrong as written.** It says depth
PNGs are bottom-up and normal PNGs top-down, "cancelling only by luck". Traced at
row 16: every array `atlas.py` touches reaches it through Blender's image API
(`images.load` → `img_array`, `pixels.foreach_set` → `save`), which normalises
bottom-up in memory and top-down on disk in **both** directions, for every format —
a deterministic boundary, not two flips that happen to cancel. There is no latent
bug and no pixels moved. The genuine top-down tension is confined to
`views.py:210,213`, where `render_normal_views` bypasses `save()` and writes raw
arrays through `cv2.imwrite` for the PIL-side estimator; that flip is explicit and
documented already.

`proptex/registry.py` gained `resolve_class(class_name)` — the class table read
without an asset instance, for `char_mpfb.py`'s parametric character, which has no
`assets.json` entry and cannot be given a fake one without breaking
`check_registry.py`'s directory bijection. `resolve()` calls it, so
`surface_classes.json` has exactly one reader. This deletes §2's third
hand-spelling of the character contract (`char_mpfb.py:355`).

**Row 14 moved a defect boundary.** §3D assigned "cameras linked and never
unlinked" to `scene.py`, but the render settings that leaked are one fact —
*an ortho render needs this configuration* — and three call sites need it
(`render_depth_views`, `render_normal_views`, `pick_extra_views`). Detaching the
settings from `_ortho_camera` and re-spelling them per caller is the shape this
plan exists to delete, so `_ortho_camera` became the context manager instead,
built on `scene.py`'s `scene_state`. It spells the configuration once and the
camera unlink falls out of `scene_state`'s object tracking. `_depth_setup` and
`_normal_setup` are context managers over it; row 15 moves all three to
`views.py` unchanged.

**The pipeline is deliberately unrunnable until row 23.** Row 11 gave
`prop_texture.py` a `required=True --asset` so the class can gate the estimator,
and neither caller passes it until row 23 collapses their CLIs. Nothing between
here and there runs a generation, so this costs nothing — but do not read a
`prop_texture.py` invocation failure in rows 14–22 as a regression.

Two additions the rows themselves produced, kept because later rows reuse them:
`scripts/ai-pipeline/check_registry.py` (row 6's consistency check) and
`prop_placements_are_registered` in `content_lint.rs` (§3E's one-directional
registration, split from `prop_material_matches_surface_class` so the two failures
stay distinguishable — row 33 still expects exactly one failing test).

Ordered; numbering is continuous and phase headings are readability only. Every
`verify` is a literal command plus the assertion that makes it decisive — an exit
code alone never counts (`tasks/lessons/2026-07-21-probe-must-fail-when-broken.md`).

Three measured facts this split rests on:

- **chapel_arch is the only prop already on the fixed contract.** Decoding all
  seven glbs: chapel_arch carries `metallicFactor 0.0`, `roughnessFactor 0.85`, no
  `metallicRoughnessTexture`, an `occlusionTexture`, `extras.vordar_detail true`.
  The other six ship an MR texture, no occlusion, no factors. **The six to rebuild
  are `broken_column`, `candelabra_shrine`, `crucero`, `cypress`, `gravestone`,
  `olive_stump`** — enumerated from the artifacts, not from a list.
- **The recorded timings price nothing** (§6.2).
- **The archived candidate dirs are not reused.** §3B keys on content hash, not
  path, so the rebuild is a cold regeneration. The archived `clean.glb` meshes are
  still valid *measurement* input (rows 17, 25) — CPU only, not a generation run.

### 8.0 Design gaps — blocking; nothing below starts until all four land

Workers execute and do not explore (`.claude/agents/finding-worker.md` rule 2).
Each row is a decision this plan does not yet make and that would otherwise land
in a worker's lap.

| # | task | tier | verify |
|---|---|---|---|
| 1 | **Resolve the CLI/registry contract.** §3A collapses six flags into `--asset <name>`, but `assets.json` also holds `subject`/`seed` while `gen_prop.py` exists to sweep seeds for an *unregistered* subject. Write §3A.1: post-collapse argv for all three scripts; whether `subject`/`seed` stay CLI; how an unregistered exploratory candidate resolves a class; whether `strategy` survives at all once `projection` dies (a single-valued field is a dead flag); and **where the D12 concept-alpha refusal lives**, since `concept_stats` is its only implementation and `basecolor_projection` its only caller. | [fable/opus] | §3A.1 exists and rules keep/drop explicitly for each of `prop_texture.py`, `gen_prop.py`, `gen_character.py`, `subject`, `strategy`, `concept_png`. A heading missing any of the six is not done. |
| 2 | **Rule how non-generated assets sit in the registry.** `rock_face_01`, `rock_07`, `rock_09` are Poly Haven downloads placed in `zones.ron`, ship a real `metallicRoughnessTexture`, and have no `generation_manifest.json`. §3E asserts *absence* of that texture, so against them the clause is permanently red. Rule the `kind`s, which assertions apply per kind, and whether a zone-placed asset missing from `assets.json` fails or skips. | [fable/opus] | The ruling names all three downloads, names each `kind`, and states per assertion (`metallicFactor`, `roughnessFactor`, `extras.vordar_detail`, occlusion present, MR absent) whether it applies to a non-generated asset. |
| 3 | **Rule the `bakeoff/` deletion boundary** (§4). `run.py`/`lit_control.py` are dead; `metrics.py` is live via `prop_audit.py:32`. Decide which files die and where `baked_fraction`/`luma_of`/`rgb_of` live afterwards. | [fable/opus] | §4's row names the exact file list deleted and the surviving import path for all three functions. |
| 4 | **Write the stage-cache key schema (§3B.1).** Per sub-stage: exact resolved-param set, exact input-content hashes, on-disk layout, and how the key record becomes the provenance record — §3B claims the key record *is* the provenance and that mapping is unwritten. | [fable/opus] | A table with one row per sub-stage; a row with an empty input-hash cell is not done. |

### 8.1 Baseline

| # | task | tier | verify |
|---|---|---|---|
| 5 | Archive the pre-state: `prop_audit.py` table for all seven props plus the `rock_face_01` control, and one 8-angle turntable sheet per prop, into `target/prop-redesign-baseline/`. Capture only — no judgment. | [haiku] | `prop_audit.py --json` writes 10 asset rows including `rock_face_01`, each generated prop carrying non-null `blend_coverage`; 7 contact sheets exist. |

### 8.2 Registry — the spine; must precede the CLI collapse

| # | task | tier | verify |
|---|---|---|---|
| 6 | Write `content/models/surface_classes.json` (§3A's five classes) and `content/models/assets.json` (schema and `kind`s per rows 1–2). Data only, no loader. | [sonnet] | A python one-liner asserts the class set is exactly the five, every asset's `surface_class` resolves, and every prop directory has an entry; a typo'd class name must raise. |
| 7 | `proptex/registry.py`: load both, resolve `name → contract`, refuse unknown name or class. No defaults, no fallbacks. | [sonnet] | `resolve('chapel_arch')` yields `(0.0, 0.85, True)`; `resolve('nope')` **raises** rather than returning a default. |
| 8 | Rust registry loader + the `prop_material_matches_surface_class` clause, scoped per row 2. **Delete `stone_props_declare_detail` and its hardcoded list in the same diff.** | [sonnet] | **Done.** `cargo nextest run -p vordar-game --test content_lint`: 14 tests, 13 pass, one failure — `prop_material_matches_surface_class`, naming exactly `broken_column`, `candelabra_shrine`, `crucero`, `cypress`, `gravestone`, `olive_stump`, each on all four generated clauses (`metallic_factor 1`, `roughness_factor 1`, MR image present, occlusion image missing). `stone_props_declare_detail` has zero occurrences repo-wide. **chapel_arch and all three rocks pass through the same code path** — that is the positive control: a clause reading anything other than the shipped glb would have named them too. |

**Row 8 turns the suite red and it stays red through row 38.** Intended (§6.2), and
a known enumerated state: one failing test naming exactly six assets. Rows 33 and
40 assert that shape.

### 8.3 Deletions (swap rule — one row each, no compatibility path, no dead flag)

| # | task | tier | verify |
|---|---|---|---|
| 9 | Delete the `projection` strategy: `basecolor_projection`, `concept_stats`, `project_uvs`, `FRONT_AXIS`, the `front_axis` extras key, the branch, `--strategy`, and `gen_prop.py`'s `--texture-strategy`. Concept-alpha gate and `concept_png` per row 1. | [sonnet] | Zero matches for all seven identifiers across both scripts; `prop_texture.py --help` shows no `--strategy`. |
| 10 | Delete `view_<i>/bump.png` and the estimator bump head: the third output in `prop_pbr.py:82,88`, `bump_sha256`, and the `bump.png` term in the resume predicate. | [sonnet] | **Done. "Zero `bump` matches" was over-broad and is corrected here:** one match legitimately survives, `init_materials["bump"]` at `prop_pbr.py:79` — a *required input key* of MaterialAnything's `pipeline_stable_diffusion_switcher.py:577`, not our output. The head still computes inside the third-party model; what died is writing, hashing and resume-gating a file nothing read. Resume predicate now requires `albedo.png` alone and was shown to still discriminate. |
| 11 | Delete MaterialAnything for every non-foliage class — `albedo_source: direct` short-circuits `estimate_materials`. No flag, no env var; the class decides. | [sonnet] | **Incomplete — closed by row 19.** The two static clauses passed; the run clause was never executed because this same row made the pipeline unrunnable. It left `blend_views` loading the estimator's `albedo.png` on the `direct` path that no longer produces it. |
| 12 | Delete `blend_views(filename=, srgb=)` and their docstring paragraph. | [sonnet] | Zero matches; module compiles. |
| 13 | Delete the dead `bakeoff/` files per row 3, relocating whatever survives. | [sonnet] | `prop_audit.py --asset chapel_arch` still prints a numeric `baked_fraction_ts` — decisive, since a broken import fails at line 1. |

### 8.4 `proptex/` decomposition (§3D) — each row retires the defect §3D names

| # | task | tier | verify |
|---|---|---|---|
| 14 | `scene.py` — import, render-settings **context manager**, one emission-graph builder. | [sonnet] | **Done.** Probe under Blender: all seven snapshotted fields restored after exit and after a raise inside the block, camera unlinked; deleting the `finally` fails it (`AssertionError: 1024`), and fails it again through `_depth_setup` in isolation. `prop_texture.py` −160 lines. |
| 15 | `views.py` — view specs, camera rig, **one** near/far definition (today `:328`, `:349`, `:364`). The rig arrives from row 14 as a context manager (`_ortho_camera`, `_depth_setup`, `_normal_setup`) and moves unchanged. Also close `hires.hide_render = True … = False` — the same unguarded restore as row 14's `cycles.samples`, at all three render loops. | [sonnet] | **Done, and my verify cell was malformed.** "A view's near/far equals `near_far(rig)`" is **tautological once the fix lands** — `mv_view` calls `near_far`, so no mutation can fail it. The real gate is the grep: `3.0 * rig["half"]` appears exactly once, at `views.py:47`, with three callers. `hidden` folded into `depth_setup`/`normal_setup`, so all three render loops — `pick_extra_views` included — close structurally rather than by remembering. |
| 16 | `atlas.py` — atlas, reprojection, one stated row-order convention (depth PNGs are bottom-up, normal PNGs top-down, cancelling by luck today). | [sonnet] | **Done, and the premise was wrong** — see the refutation above; the convention is now stated in `atlas.py`'s header as the Blender-API boundary it actually is, and no pixels moved. The pinned-corner probe earned its keep: under an injected `flipud` the round-trip assertion **passed** and only the corner assertion failed, which is exactly why the cell demanded both. `view_weight` went to `atlas.py` (projection mechanics, not coverage policy); row 17 may re-decide. |
| 17 | `coverage.py` — island coverage, NBV selection, and a standalone entry point printing coverage, hole count, largest contiguous hole. Geometry only. | [sonnet] | **Done, and `python -m proptex.coverage` was impossible** — see the entry-point divergence below. Ran under Blender on `b3/arch/cand_0/clean.glb --asset chapel_arch`: `blend_coverage` 0.5504, `hole_texels` 1202912, `largest_hole_texels` 62492 — and the first two **reproduce the archived `generation_manifest.json` exactly**, which is the real gate on a refactor that moved the predicate. Zero views yields 0.0 through both guards (empty view set *and* empty island), not NaN. Mutating `MV_COVERAGE_EPS` to `1e9` collapses coverage to 0.0 with no extras picked; file byte-restored after. |
| 18 | `generate.py` — ComfyUI canvas lifecycle, contract unchanged (VRAM-sequencing invariant, 11.5 GiB Hi3DGen peak — not a convenience). | [sonnet] | **Done, and my cell was the fifth weak one.** "Exactly one `comfy_run.server` site" **cannot fail** — there was already exactly one, and repo-wide there are legitimately three (`gen_prop.py`, `gen_character.py`, here), each stage owning its own. The failable cell is that **`generate.py` imports no `bpy`**, which makes the VRAM invariant structural: a Cycles render cannot appear inside the server block if Blender is not importable in the file. Verified by an import-anchored grep — five `proptex` modules import `bpy`, `generate.py` is not among them — and by importing `generate_views` itself (not just `view_pairs`) under a plain non-Blender interpreter. `fail()` became `GenerateError`, per `SceneError`/`RegistryError`. `prop_texture.py` −97 lines. |
| 19 | `albedo.py` — albedo-source policy (`direct` vs `delit` from the class) plus blending. **D5/D6 close here.** **Moved up to run right after row 16** — it closes row 11's live break. | [sonnet] | **Done.** `source_image` is the only place the two literals decide anything; it refuses an unknown `albedo_source` with `RegistryError` rather than defaulting to either file. Swapping `limestone`/`foliage`'s `albedo_source` in `surface_classes.json` fails the probe (`chapel_arch: expected gen.png, got …albedo.png`); the file was byte-restored afterwards. `blend_views` moved `atlas.py` → `albedo.py`, taking `albedo_source` rather than the whole contract. |
| 20 | `export.py` — material graph and `use_selection=True`, so correctness stops depending on the scene happening to be clean. | [sonnet] | **Done, and the cell was wrong twice over — cameras were never the risk.** "A leaked camera fails it" is backwards: `use_selection=True` exists precisely so a leaked camera *cannot* fail it. And the camera premise was empty anyway — `export_scene.gltf` defaults `export_cameras=False`, so a linked camera never reaches the glb with or without the flag. The real mutation is a leaked **mesh**: with the flag, the probe's glb has exactly one node, no `cameras` key, an `occlusionTexture`, the contract's MR factors and `extras.vordar_detail`; delete the flag and node count goes 1 → 2. "Camera unlink" was also phantom — no such code existed to remove. |
| 21 | **`provenance.py` — record derived from resolved values only, and where per-stage `elapsed_s` lands (§6.2).** Plus a chain total. No hardcoded node ids, no strategy field at all (D16/D17, §3A.1). | [sonnet] | **Done, in three rounds — the cell was right but far too small for the row.** Timings round-trip and JSON-serialise; `elapsed_s_total` sums seven stage kinds; zero matches for `multiview_controlnet_depth`/`pbr_estimator`/the three `*_bake_s` (the only surviving `prompt_id` is `comfy_run.py`'s own HTTP field). The workflow's sha256 replaced the literal. Beyond the cell: the chain gained the **`prep`** stage and a **`measurements`** field (§4), and a walker now asserts every input hash has an earlier producer or is external — with a negative control proving the walker fires. A mechanical type check asserts every `outputs` value is 64-hex and every `measurements` value numeric. `normal_bake`/`ao_bake`'s bake constants became named and are spelled once across the operator call and the record. |

### 8.5 CLI collapse — **runs before 15–21**, not after

**Reordered after row 14, and the constraint is forced by the code.** `main()`
rebinds three module globals (`TEXTURE_SIZE`, `MV_RES`, `MV_VIEWS`) from
`--texture-size`, `--view-res` and `--azimuths`, and each is read from a
different §3D module's territory: `MV_RES` from views (`:192`, `:279-281`),
generate (`:362-383`) and provenance (`:656`); `TEXTURE_SIZE` from atlas
(`:428-443`, `:584-585`), export (`:747`, `:765`) and provenance (`:826`).
Moving any of those bodies into `proptex/` while the global still lives in
`prop_texture.py` and is rebound at runtime splits one value across two
modules — the extracted module reads its own frozen `1024` while the rest of
the pipeline reads the override. Silent, and exactly the "same fact on two
channels" this plan exists to delete.

Row 15 hit this first: `views.py` cannot own `MV_RES` while `--view-res`
rebinds it. Rows 16, 18, 20 and 21 each hit the same wall for the same reason.
The globals must die before the bodies move, so 22–23 run here. Rows 15–21
then extract into a package with no mutable module state, and — because row 23
restores a runnable pipeline — they can be verified against a real invocation
rather than by static reading alone.

The original §8.5 preamble ("needs rows 6–7 and 9–13 landed") is unchanged and
already satisfied.

| # | task | tier | verify |
|---|---|---|---|
| 22 | Collapse the six flags into `--asset <name>` resolving through `proptex.registry`; delete the module globals those flags rebound (`TEXTURE_SIZE`, `MV_RES`, `MV_VIEWS` mutation in `main()`). | [sonnet] | **Done.** Zero `global` statements; zero source occurrences of all three identifiers; `texture_size`/`view_res` threaded as explicit parameters. `--subject`, `DEFAULT_METALLIC` and `DEFAULT_ROUGHNESS` died with them. |
| 23 | Update both callers per row 1: `gen_prop.py` and `gen_character.py` pass `--asset`, and their own now-dead pass-through flags go with them. | [sonnet] | **Done.** Both `--help` match §3A.1 exactly — no `subject` positional, none of the eight. `gen_character.py` never passed `--strategy`, so nothing was left broken by row 9. `--max-dim` is now driven from `contract.texture_size`, closing the coupling its own help text warned about. `README.md` (11 sites) and `prop_cleanup.py:50` de-staled per the swap rule. |

### 8.6 Cache, refusal gates, install

| # | task | tier | verify |
|---|---|---|---|
| 24 | Implement the content-addressed cache per row 4. A stage reruns iff its key changes; the key record is written as the provenance record. | [sonnet → opus ×2] | **Done**, in three waves (mechanism, geometry units, generation units). Every input hash and every param moves the key; identical inputs reproduce it; a `cache.py` edit moves **no** stage version. Cold missed every stage, warm hit every stage and recomputed nothing, `elapsed_s` carried from the producing run. chapel_arch's coverage came back byte-identical (0.5504 / 1202912), so the whole conversion moved no behaviour. Chain walk: zero holes over 61/88 internal edges, with negative controls. |
| 25 | Run `blender --background --python scripts/ai-pipeline/proptex/coverage.py -- <glb> --asset NAME --map <png>` (row 17's divergence) over the seven **shipped** glbs (see the input correction below); record coverage, hole count, largest hole into `target/prop-redesign-baseline/coverage.json` and one hole map per prop beside it. CPU only, ~40 s/prop. | [haiku] | **Done.** Seven entries, each with coverage in (0,1) and a positive max hole; deterministic across two full runs. Coverage spans **0.4879 (broken_column) – 0.7623 (cypress)**; largest hole reaches **29.6% of the island** (gravestone) and **19.6%** (broken_column). Equivalence controls: chapel_arch shipped-vs-archived agree to **1 texel in 1 202 912** and broken_column agrees exactly; chapel_arch also reproduces its own `blend` stage record (0.5504 / 1202912 / 62492) byte-for-byte. |
| 26 | Review the uncovered-island maps against each shipped atlas and the `rock_face_01` control: where does Telea filler actually read as slop, and at what hole size does it stop mattering. Judgment only. | [opus] | **Done.** `target/prop-redesign-baseline/hole-review.md` — per-prop verdicts citing island regions by coordinate. Alignment re-checked on four props. Two findings below outrank the row's own question. |

**Row 26 finding 1: the hole gate must key on extrapolation depth, not area.**
Depth = per hole texel, the Euclidean distance to the nearest *covered* texel;
per component, its max. It is how far Telea had to invent, and it is shape-aware
for free — an enclosed hole's depth is about half its width, a hole running off a
chart edge's is its full width. The counterexample that decides it:
candelabra_shrine's base disc is **43 136** texels at depth 111.8 and reads dead
flat, while chapel_arch's strip is **62 491** texels at depth 48.0 and reads as a
ribbon; the 30%-smaller hole is visibly the worse one. Observed bands: ≤0.4% of
atlas width undetectable everywhere; 0.4–1.5% conditional on the filler's
*luminance match* to its host (cypress passes at 0.6–0.8%, chapel_arch fails at
the same depth at +15% luminance); >1.5% nothing passed. Row 27 derives its
threshold from depth plus a luminance-delta clause, not from `largest_hole_texels`
— **and the contrast clause must be an absolute floor, not a hole/covered ratio,
because a ratio passes `broken_column`, the worst prop, on the grounds that its
covered content is already flat.** *(The depth half stands and is what row 27
ruled on. The luminance-delta and contrast halves do not: row 27 measured the
luminance delta to collapse from +14.94% to +1.59% under `direct`, and `hf_rms`
to disagree 2.8× across this campaign's three instruments. Both are deleted
there, with the measurements — do not implement either from this paragraph.)*

**Row 26 finding 2, which outranks this row and rows 28–38: the *covered* content
is itself below the bar, so coverage is not the only red gate.** Measured
independently of the review, over covered texels only, against the photoscan
control:

*(Numbers below are row 26a's re-measurement over **surface** texels — the
covered set intersected with the rasterized UV island. Row 26 measured the raw
covered set, which includes the bake margin; the ranking is unchanged and every
prop moves by 1–3 luminance except `candelabra_shrine`, whose covered set is half
gutter and which moves 92.3 → 104.2.)*

| | covered luminance | covered saturation |
|---|---|---|
| broken_column | **172.4** | 0.213 |
| gravestone | 157.4 | 0.259 |
| crucero | 148.1 | 0.236 |
| chapel_arch | 147.5 | 0.239 |
| olive_stump | 147.4 | 0.110 |
| cypress | 133.8 | 0.184 |
| candelabra_shrine | 104.2 | 0.112 |
| `rock_face_01` control | **98.7** | **0.348** |

The five stone/wood props are **49–75% brighter** than the control and below it on
saturation; hole filler is brighter still on all seven. `candelabra_shrine` —
dark iron, correctly dark — is the control that rules out a global encoding error
and localises this to the stone albedo path.

**This row's proposed mechanism was wrong, and row 26a falsified it.** Row 26
reasoned that a basecolor taken `direct` from a diffusion render of a *lit*
object carries that lighting, which `albedo_source: delit` exists to remove. The
opposite holds: six of the seven shipped props were built **`delit`**, these
numbers *are* the delit result, and `delit` is what brightens them — it also
inverts occlusion, painting creases brighter than open faces. `candelabra_shrine`
is the closest to the control precisely because it is the one prop the estimator
never touched. The reasoning is kept here rather than deleted because row 26a's
ruling is the answer to it. `broken_column` measures flatter
*and* brighter than the flattest photoscan crop, so closing its 49% hole budget
still leaves an unusable prop. **Rebuilding the six on the current class contract
would spend rows 34–38's GPU time and still deliver too-bright stone.** Escalated
to the user before row 27 fixes any number.

**Row 25's input was specified wrong, and the survey re-derived it rather than
special-casing the exception.** The row said "the seven archived `clean.glb`
meshes, paths from each manifest's `candidate_dir`". `candelabra_shrine`'s
archived mesh **carries no UV atlas at all** — it is the one prop whose
`cleanup_stats.json` exists yet lacks `uv_charts`, so it predates `prop_cleanup`'s
unwrap step, and `coverage.py` correctly refuses it. The measurement wanted is
"the mesh and atlas the prop actually ships", and the archived intermediate was
only ever a proxy for that. So the survey reads the **shipped glb**, uniformly,
for all seven: one rule rather than an exception, the same path `zones.ron` and
`content_lint` use, and no dependence on `target/prop-batch/` — an untracked
scratch tree, which is precisely why one entry is unmeasurable there. Equivalence
was measured, not assumed (row 25's cell).

**Rows 25 and 26 had no connecting artifact, and row 26 was unstartable.** Row 26
reviews "the uncovered-island maps"; nothing produced any. `coverage.py` computed
the mask and discarded it, keeping three aggregates. Fixed in the instrument that
already had the mask in hand: `main` takes a required `--map PATH` and writes the
final hole state as three flat levels (black outside the island, `0.25` grey
covered, red uncovered) through `new_image`/`save_png` — the Blender image path
`atlas.py`'s docstring documents as row-order-normalising, so the map lands
aligned with the shipped atlas by construction rather than by a flip constant.
Confirmed on gravestone: red count equals `hole_texels` **exactly** (400224), and
the chart carrying the crisp carved cross reads grey while the chart beside it
that reads pure red is a flat featureless smear in the atlas — covered predicts
detail and hole predicts smear, chart for chart.
| 26a | **Settle albedo tonality before anything is rebuilt** (user ruling, 2026-07-26, on row 26's finding 2). Locate where the baked lighting enters the stone albedo path, then A/B **`broken_column`** — the worst prop at covered luminance 173.1, and the cheapest at 1024/1024 — `direct` vs `delit` at one fixed seed, and rule `albedo_source` for all five classes in `surface_classes.json`. | [opus] | The two atlases measured over **covered texels only** (the hole map is the mask), reporting luminance and saturation against the `rock_face_01` control at 95.4 / 0.351. The ruling names an `albedo_source` for every class with its measured delta; a class whose value is unchanged still needs the measurement that leaves it unchanged. **`candelabra_shrine` at 92.3 is the counter-control** — it is already correct, so a fix that darkens it is refused, not tuned. If `delit` does not move `broken_column` toward the control, say so: the hypothesis is then wrong and the cause is upstream of the albedo policy. |

**Row 26a — Done, 2026-07-26. Ruling: `direct` everywhere it can be measured.
Zero GPU was spent; the approved generation run was not needed.**

*The row's premise was inverted, and correcting it is the finding.* Every shipped
prop's `generation_manifest.json` was read for `texture.pbr_estimator`: it is
present with `estimated_views` on **six** props and **absent only on
`candelabra_shrine`**. So `surface_classes.json`'s `limestone`/`wood`/
`painted_metal: direct` — landed by rows 11/19 off the MaterialAnything
keep/drop A/B — is a declaration that has never been executed: the
shipped stone, wood and foliage atlases are all **delit** output, and the 173.1
baseline row 26 measured *is* the delit result. The counter-control is not a prop
that happens to be right: `candelabra_shrine` is right **because it is the one
prop that skipped the estimator.** The ruling therefore leaves it byte-identical,
which is what the row demanded of it.

That also made the run unnecessary. Matched-pair `direct` atlases — same archived
generation, same blend weights and constants read from each prop's own manifest,
only `gen.png` substituted for `albedo.png` — already existed on disk for
chapel_arch, broken_column and cypress from the 2026-07-25 `target/delight-ab/`
campaign; olive_stump's was built today with that same script. CPU only.

Measured over **surface** texels — the hole map's covered set intersected with
the rasterized UV island, so the bake margin is excluded. That intersection
matters: on `candelabra_shrine` the raw covered set is 534 683 texels against
275 398 after intersection, i.e. **half of it is gutter**, and the gutter is
dilated edge colour rather than surface.

| class | prop | delit lum | **direct lum** | Δ | delit sat | **direct sat** | delit hf | **direct hf** |
|---|---|---|---|---|---|---|---|---|
| limestone | chapel_arch | 147.5 | **107.4** | −40.1 | 0.239 | **0.333** | 6.76 | **21.81** |
| limestone | broken_column | 172.4 | **141.5** | −30.9 | 0.213 | **0.248** | 5.06 | **17.74** |
| limestone | crucero | 148.1 | — | — | 0.236 | — | 5.57 | — |
| limestone | gravestone | 157.4 | — | — | 0.259 | — | 9.35 | — |
| wood | olive_stump | 147.4 | **91.3** | −56.1 | 0.110 | **0.158** | 10.21 | **23.99** |
| foliage | cypress | 133.8 | **52.0** | −81.8 | 0.184 | **0.251** | 7.73 | **10.42** |
| painted_metal | candelabra_shrine | — | **104.2** (already direct) | — | — | 0.112 | — | 11.97 |
| **control** | `rock_face_01` | — | **98.7** | — | — | **0.348** | — | 9.95 |

**`direct` wins on luminance, saturation *and* micro-contrast in all four
matched pairs.** cypress's apparent micro-contrast regression — the one
counter-signal in the first pass — was margin contamination and does not
survive the correct mask. chapel_arch's `direct` atlas lands within 9 luminance
and 0.015 saturation of the photoscan control at twice its micro-contrast.
The variant PNGs are stored `flipud` of the shipped atlas — established by
high-frequency energy, which separates 12.5:1 under the right flip and ~1.1:1
under all three wrong ones, and re-confirmed against the AO atlas.

The counter-control's number moved with the mask (92.3 → **104.2**) but not its
role: `candelabra_shrine` remains the shipped prop closest to the control, the
only one built `direct`, and the ruling leaves it byte-identical.

**`delit` fails on the axis it exists to protect.** Against chapel_arch's
mesh-baked AO atlas over covered texels, the delit atlas correlates **−0.345**
with luminance the wrong way round: creased texels (AO < 0.85) average **0.617**
against open faces (AO > 0.98) at **0.594** — the estimator paints crevices
*brighter* than exposed surfaces. `direct` is **−0.004** (0.409 vs 0.448, correct
sign). A delighting pass that inverts occlusion is not removing baked lighting.

**What `albedo_source` cannot fix, stated rather than patched.** Fitting each
view's generation luminance against its own world normal (`prop_audit.
baked_fraction`, calibrated ~0.33 for hard sun and 0.006–0.018 for clean
generated albedo), **`broken_column` is the only prop carrying a real key
light** — R² **0.128 / 0.160** on views 0 and 2, against chapel_arch's **0.018 /
0.005**. That is why chapel_arch's `direct` atlas reaches the control and
broken_column's stops 45 points short. The defect is per-*generation*, not
per-class, so no value of `limestone.albedo_source` is right for all four
limestone props; the fix is regenerating broken_column, not a per-prop override.
(The opus dispatch also named `gravestone` as a second offender at a 3.09× ratio;
that did not reproduce on re-measurement — gravestone's delit R² comes out
*above* its gen R², so only broken_column is carried forward.)

**Found while folding the survey into `prop_audit.py`: that instrument's island
mask has always been vertically flipped.** `island_mask` rasterizes
`1.0 - uv[:, 1]`, but glTF `TEXCOORD_0` is already top-left-origin and so is the
decoded image array, so the flip is a double-correction. Two independent
measurements. **Containment:** the Blender-baked island is a *dilation* of the
true UV footprint, so a correctly oriented tight island must fall entirely
inside it — without the flip it does, at **0.0–0.1%** outside on all seven
generated props; with it, **7.7–37.9%** lands outside, which is geometrically
impossible for an aligned mask. **The flat-fill test:** off-island texels of a
generated basecolor are one constant mean-colour fill, and the hole map's island
leaves a complement at luminance std **0.26–0.34** where every rival hypothesis
leaves **13.8–23.9** — so `coverage.py`'s map is aligned with the shipped atlas
and `island_mask` is what disagrees. The comment at `prop_audit.py:152-155`
asserting the flip was "confirmed empirically" is a false claim and goes with it.

Blast radius: every island-masked statistic that instrument has ever printed —
`roughness_mean`/`std`, `metallic_mean`, `ao_mean`, `albedo_luma_*`,
`albedo_blown_frac`, `normal_lap_std`, `normal_flat_frac`, `baked_fraction_ts`.
The area metrics (`island_frac`, `atlas_px_per_m`, `placed_px_per_m`,
`world_area_m2`) are orientation-invariant and unaffected. The control moves
**95.9 → 98.7** luminance and 0.351 → 0.348 saturation, so row 26a's ruling is
untouched; the historical figures that leaned on the masked statistics are not,
and the detail-layer campaign's `normal_lap_std` and the `albedo_luma_p1`
discriminator are the two worth re-reading before either is cited again.

**Ruling, applied.** `foliage` **`delit` → `direct`** — the only file change
(`check_registry.py` green). `limestone` and `wood` keep `direct`, now
evidence-backed, and their shipped atlases are rebuild targets. `painted_metal`
keeps `direct` as a stated no-op. **`character_skin` is unruled**: it has no
asset, so the row's own standard — a class whose value is unchanged still needs
the measurement that leaves it unchanged — cannot be met, and guessing it would
be the failure the standard exists to prevent. Full report and its falsifier:
`target/prop-redesign-baseline/albedo-source-ruling.md`.

**Consequence: the estimator is now unreachable — kept anyway, ruled by the user
2026-07-26.** `needs_estimator` has exactly one call site
(`prop_texture.py:248`) and is reached only through a prop's class. Every class
a prop can hold now rules `direct`; `character_skin` is resolved by
`char_mpfb.py:355`, which reads only `metallic`/`roughness`, and MPFB characters
are built from authored MakeSkin textures that never enter the multiview path.
So `needs_estimator` returns False for every value it can currently be called
with. The swap rule would retire `prop_pbr.py`, `albedo.py`'s estimator half,
`prop_texture.py`'s `normal_units`/`estimate_units`, `views.py`'s
`render_normal_view`, the three `models.sha256` estimator hashes,
`albedo_source` across `registry.py`/`check_registry.py`/`surface_classes.json`,
and the README's MaterialAnything venv section. **The user ruled: keep it until
characters land** — `character_skin` is the one unruled class, and the branch
stays against the day a character asset needs delighting. The cost is carried
knowingly: a dead branch through the cache keys, the registry and the README,
plus the 4.3 GB venv dependency, and §7's per-view estimator launch cost
(+150–240 s on cypress cold) stays open rather than being retired here. Revisit
when the first character asset is declared — the same trigger §7 already carries
for the `character_skin` generated-path gap.

**The instrument, folded (user ruling 2026-07-26: extend `prop_audit.py`, do not
write a second survey script).** Two files. `prop_coverage_sweep.py` is the
committed loop that was previously a scratch driver: it runs the already-committed
`proptex/coverage.py` over every `kind: generated` asset's **shipped** glb and
writes `target/prop-coverage/holes_<name>.png` plus a combined `coverage.json`.
`prop_audit.py` then masks its albedo statistics — and only those; the MR,
occlusion and normal atlases are baked or constant and carry no Telea holes — to
the hole map's covered set **intersected with its own rasterized UV island**, and
gains `albedo_sat`. The mask is routed by `kind`: `generated` intersects, and
`downloaded` keeps the island unchanged, because a prop with no generation has no
holes and its island texels *are* its covered texels. One measurement, two
sources — not two measurements. A `generated` prop with no hole map **refuses**,
naming the sweep command, rather than degrading to the island mask, which is the
failure this change exists to remove. Verified by two implementations agreeing:
the audit's `albedo_sat` column reproduces the independent probe above to three
decimals on all ten props.

Two guards, both proven to fire rather than asserted to exist: a missing hole map
refuses by name, and a hole map that fails to contain ≥98% of the rasterized UV
island refuses as a suspected orientation error — checked by feeding a `flipud`-ed
map, which reports the exact 7.7% / 17.7% figures measured above. Containment, not
equality, is the relation that holds: the baked island is a *dilation* of the UV
footprint, so equality can never be satisfied and demanding it refused all seven
props on the first attempt.

**Decided while unsure (§6), logged rather than asked.** `prop_audit.
generation_stats` now reads `blend_coverage`/`hole_frac` from the sweep instead
of `generation_manifest.json`, and its pre-stage-record refusal is deleted with
no fallback. Forced: that refusal fired on every prop that exists today, so the
instrument could not produce the **before** half of the before/after it is being
built for. It is also the more honest source — `prop_audit.py` is declared
measurement-only, and a number read out of a manifest is provenance. The cost is
losing the recorded-vs-recomputed cross-check, which belongs to row 31's
byte-identity clause rather than to a measurement table. Reversible in one commit.

**That change immediately found something: `candelabra_shrine`'s registry no
longer describes the asset it shipped.** Its manifest records `extra_views: None`
— four base views, no next-best-view pick — while today's `coverage.py` picks a
fifth ("back view, seen from below") worth +4.77%. So its recomputed coverage is
**0.6477** against the shipped **0.6088**, and it is the only prop of the seven
where the two disagree; the other six match exactly, extra views included. The
practical consequence is that ~7% of what the current hole map calls covered for
this one prop was never rendered into its atlas and is really Telea filler, so its
104.2 is mildly flattered — it remains the closest prop to the control either way.
Row 25's table carried the recomputed 0.6477 while §7's retraction carried the
shipped 0.6088; both are now labelled. This is the staleness rows 31/35 exist to
end, and it is a rebuild target, not a number to reconcile.

| 27 | **Derive the coverage and inpaint thresholds** from rows 25–26, writing the numbers and their evidence into §3A and §3C. Keys on row 26's **extrapolation depth** — not `largest_hole_texels`. See §7. | [fable/opus] | **Done.** One constant, `MAX_HOLE_DEPTH_FRAC = 0.015`, derived below from re-measured row-25 hole maps and row-26 verdicts; it refuses all seven props, and every prop's number is stated. Three of the four proposed clauses are deleted with the measurement that deletes them. |

**Row 27 — Done, 2026-07-26. Ruled: one number, no class field, and three of the
four proposed clauses deleted because the measurement does not support them.**

**The gate is one clause.** No hole component's extrapolation depth may exceed
**1.5% of atlas width** — `MAX_HOLE_DEPTH_FRAC = 0.015`, 15 px @1024, 31 px
@2048 — and the inpaint gate is the same predicate at the fill site, not a second
number. Definition and instrument in §3C; the registry consequence in §3A.
Derivation, from row 26's bands: **>1.5% of width, no prop passed**, cypress's own
2.7% components being detectable at 1:1 in the most forgiving material in the set;
**≤0.4%, undetectable on all seven**. 1.5% is the only boundary in the evidence
with a measured verdict on both sides — 0.4% would be invented conservatism,
since the direct-atlas measurement below removes the one observed failure between
the two.

**Re-measured here, not restated** (numpy/cv2 over the seven hole maps in
`target/prop-coverage/` and the basecolors in `target/prop-redesign-baseline/`):

| prop | atlas | max component depth | % of width | hole/covered luminance Δ, shipped | Δ on the matched `direct` atlas |
|---|---|---|---|---|---|
| cypress | 2048 | 56.0 px | **2.73** | +5.09% | **+0.91%** |
| chapel_arch | 2048 | 59.2 px | **2.89** | +14.94% | **+1.59%** |
| olive_stump | 1024 | 39.2 px | **3.82** | +3.44% | **−0.17%** |
| broken_column | 1024 | 55.7 px | **5.44** | +5.96% | **+0.27%** |
| gravestone | 1024 | 73.1 px | **7.14** | +4.42% | — |
| crucero | 2048 | 200.9 px | **9.81** | +3.95% | — |
| candelabra_shrine | 1024 | 111.1 px | **10.85** | −1.73% | — |

The instrument agrees with both artifacts it re-derives: the luminance column
reproduces row 26's stated deltas (+15/+6/+4/+5/+4/+3/−2) to the point, the depth
column reproduces its per-component figures within 0.7 px, and the `direct`
covered luminances reproduce row 26a's table exactly (chapel_arch 107.5 vs 107.4,
broken_column 141.5, cypress 52.0, olive_stump 91.3).

**The clause refuses all seven props**, deepest first: candelabra_shrine 10.85%,
crucero 9.81%, gravestone 7.14%, broken_column 5.44%, olive_stump 3.82%,
chapel_arch 2.89%, cypress 2.73%. Expected — rows 35/38 rebuild them. **A passing
atlas is not hypothetical**: 94.7% of cypress's island already sits at depth
≤0.4% of width and 99.1% inside the cap. What fails is the deep enclosed cavity —
candelabra's ring interiors and base-disc undersides, crucero's back face.

**What the clause breaks, and it outranks the row's own question:
`MV_EXTRA_MAX = 2` becomes the binding constraint.** The cap is satisfiable by
adding views — that is exactly what row 28's refusal message exists to emit — but
`coverage.py` enumerates 37 candidate directions and is allowed to pick at most
two, and `MV_EXTRA_MIN_GAIN = 0.03` discards any pick worth less than 3% of the
island. cypress spent both picks and is still 1.2 points over the cap;
candelabra spent one and is 7× over. Neither constant is derived — the comment at
`coverage.py:43` justifies the gain floor by "a smaller residue is scattered
enough that Telea inpaint suffices", which is the assumption this row just
replaced with a measurement. **Both must be re-derived against the depth clause
before row 35 spends a rebuild**, and the measurement that settles them is a
`coverage.py` sweep at a raised cap — Blender, CPU-only, seven props at ~40 s
each. It is not folded into row 28: row 28 lands the refusal, and a refusal that
nothing can satisfy would burn rows 35/38's GPU time discovering it.

**Three clauses row 26 proposed are not ruled, each with the measurement that
deletes it.**

1. **The luminance-delta clause is a `delit` artifact and dies with `delit`.**
   Measured over the same covered mask on the four matched `direct` atlases row
   26a used, chapel_arch's **+14.94% becomes +1.59%**, broken_column's +5.96% →
   +0.27%, cypress's +5.09% → +0.91%, olive_stump's +3.44% → −0.17%. The largest
   delta anywhere in the `direct` set is 1.59%, on the very prop the clause
   existed to catch, whose `direct` atlas row 26a measures within 9 luminance of
   the photoscan control. Row 26a also supplies the mechanism: Telea propagates
   from the hole boundary, so filler tracks boundary luminance; holes are exactly
   the texels no view reached, i.e. creases and undersides; and `delit` paints
   creases *brighter* (AO correlation −0.345, creased 0.617 against open 0.594,
   versus `direct`'s −0.004). The +15% was measuring the estimator's occlusion
   inversion at the hole rim, never Telea. There is therefore no threshold to
   set — ≥8% fires on nothing a `direct` pipeline can produce, and ≤2% is
   calibrated against a good atlas. This also retires row 26's claim that
   chapel_arch "proves a size-only gate cannot work": it proved a *delit*-only
   gate cannot work.
2. **The absolute micro-contrast floor is not derivable, because `hf_rms` has
   never reproduced across instruments.** chapel_arch's covered `hf_rms` on the
   shipped atlas measures **11.7** (row 26's calibration table), **6.76** (row
   26a, surface-masked) and **18.67** (here, hole-map covered mask) — 2.8× apart —
   and the `rock_face_01` reference is itself 8.5–15.6 across row 26's four crops
   against row 26a's 9.95. A floor set on any of those numbers encodes an
   instrument, not a quality bar. It is also not this gate's clause: row 26's own
   argument for it is that broken_column's *covered* content is flat, which is row
   26 finding 2's territory — the plan already records that finding as outranking
   rows 27–38 — and a floor applied to *hole* texels instead would refuse cypress's
   canopy (direct hole `hf_rms` 5.09), the one filler row 26 calls acceptable.
   Settled by row 36, which measures the first rebuilt prop with the single
   committed instrument (`prop_audit.py`, post-26a mask fix) against the control
   row it already prints.
3. **The budget above the safe depth is deleted, and row 26's own evidence is
   why.** Its proposal — "island area above 0.4% depth, a budget in the low single
   digits" — reads cypress's 12.2% as the best in the set and only marginal. But
   cypress's verdict decomposes: "Canopy passes; the ~113k texels above depth 32
   do not", and depth 32 @2048 is 1.56%, i.e. the cap. Measured, cypress's
   above-0.4% load is 11.8% of island of which **4.4% sits above the cap** — the
   part clause 1 already refuses — leaving **7.4% of island in the 0.4–1.5% band,
   measured and judged acceptable.** A low-single-digit budget would refuse the
   one configuration row 26 found passing, which is `min_coverage 0.80`'s failure
   mode a second time. The only sub-cap failure ever observed is chapel_arch's
   white-worm field (17.7% of island in 0.4–1.5% components), and clause 1 above
   shows it failed on value, in a mode that does not survive `direct`. Zero
   measured failures, so no number.

   *Found while checking it, and it matters for anyone citing row 26:* "island
   area above 0.4% depth" is the **per-component** form — the area of components
   whose own maximum depth exceeds the threshold. Reproduced to within 3 points
   (cypress 11.8 vs 12.2, chapel_arch 40.9 vs 41.3, crucero 41.7 vs 41.7,
   gravestone 47.9 vs 47.3, broken_column 50.4 vs 49.0). The **per-texel** form of
   the same quantity is 5.3 / 20.9 / 34.3 / 42.0 / 37.0 — a factor of 2.3 apart —
   and the artifact does not say which it means.

**`delit` → `direct` transferability, answered rather than deferred.** The one
ruled number reads no generated pixel: it is a distance transform over the hole
mask, and `coverage.py`'s header already states that coverage is
"facing/frustum/occlusion against the depth renders, never the generated pixels".
`albedo_source` selects which image `blend` samples (§3B.1 row 7) and cannot move
which texels a view covers — confirmed on the artifacts, since the four `direct`
variant atlases were built from each prop's own archived blend weights and share
the shipped atlas's hole map byte-for-byte; the same file produced both luminance
columns above. So the flip cannot move the ruled constant, and the two numbers it
*would* have moved are exactly the two this row declines to rule. Nothing
provisional is carried forward.

**Registry untouched.** `surface_classes.json` keeps its four fields; no
`min_coverage`, no depth field, no per-class number. The reasoning is §3A's, and
it is `ao_distance_m`'s paragraph applied a second time — the evidence base
(limestone 4 props, wood 1, foliage 1, painted_metal 1, character_skin **0**)
cannot support five numbers, and the one prop that could have argued for a
foliage exception argues against it.
| 28 | `coverage_stats` computes `max_hole_depth_frac` and the per-component depths (§3C), replacing `largest_hole_texels`. Coverage refusal gate: any component over `MAX_HOLE_DEPTH_FRAC`, non-zero exit emitting the uncovered-island map, the offending depths and the view directions that would cover them. | [sonnet] | **Done.** `hole_component_depths` (`coverage.py:90`) reproduces row 27's table on all seven archived hole maps within **0.07 points** — candelabra 10.92 vs 10.85, crucero 9.84 vs 9.81, gravestone 7.21 vs 7.14, broken_column 5.45 vs 5.44, olive_stump 3.77 vs 3.82, chapel_arch 2.89 vs 2.89, cypress 2.75 vs 2.73 — i.e. sub-pixel agreement with an independent implementation, which is the clause that could have caught a plausible-but-wrong distance transform. chapel_arch then refuses live through the full geometry path: *"29 hole component(s) exceed MAX_HOLE_DEPTH_FRAC=0.015 (deepest 2.89%, …)"*, plus the map path and three ranked candidate directions from `rank_candidates`, which reuses the NBV scoring primitives rather than enumerating a second time. Mutated to 1.0 the same run exits 0 printing 0.0289; file restored byte-exactly. `largest_hole_texels`: zero occurrences repo-wide. |
| 29 | Gated inpaint at the fill site (`albedo.py:131`): Telea runs only on components the gate passed; a deeper one raises `CoverageFailure`. Same constant, same predicate — no second threshold. | [sonnet] | **Done.** A 60×60 hole at 1024² measures 2.93% and would raise; a single isolated texel measures 0.098% and fills. `MAX_HOLE_DEPTH_FRAC` is defined once (`coverage.py:41`) and compared at exactly two sites — `coverage.py:278` and `albedo.py:132` — both calling the shared `hole_component_depths`, so the predicate exists once and the depth computation is never duplicated. **The threshold enters no cache key:** mutating it in memory left `stage_key` byte-identical for `blend` and `nbv` while flipping the verdict on the same cached measurement. Editing the *file* does re-key both, since `coverage.py` was already in each closure — over-invalidation, never a stale pass, which is the direction §3B.1 requires. |
| 27a | **Re-derive `MV_EXTRA_MAX` and `MV_EXTRA_MIN_GAIN` against the depth clause** (row 27's finding, sequencing risk 6). Runs after row 28, which is what gives `coverage.py` the depth metric to sweep against. Sweep the seven shipped glbs at a raised pick cap and report, per prop, the cap at which `max_hole_depth_frac` falls under 0.015 — or that no cap does. Blender, CPU only, ~40 s × 7 per cap. | [fable/opus] | **Done.** No cap satisfies the clause on any of the seven — the best any prop reaches with all 37 candidate directions spent is 2.41% against a 1.5% cap. Neither constant is re-derived, because the pick cap is not what refuses the props. Escalated: ~half of every prop mesh is interior surface no view can reach. |

**Row 27a — Done, 2026-07-26. Negative result, and it is the decisive one: no
pick cap satisfies the depth clause on any of the seven props, so `MV_EXTRA_MAX`
was never the binding constraint and there is no number to derive. What refuses
the props is the mesh.**

**Method.** One `coverage.py` geometry path per prop over the **shipped** glb
(row 25's uniform input rule), rendering the four base views plus **all 37**
candidate directions, then running the greedy next-best-view pick to exhaustion
with both the cap and the gain floor lifted. Greedy picks form a prefix chain, so
a single run yields the entire curve — `max_hole_depth_frac` after every pick,
i.e. every cap from 0 to ~27 — rather than one run per cap value. A second figure,
the **ceiling**, unions all 41 directions with no separation pruning at all: the
best any view set drawn from this candidate rig can do. Blender 5.2, CPU,
uncached, rendered into the scratchpad. **Nothing was written to
`target/prop-cache/`, which does not exist.**

**The instrument is the shipped one, checked both ways.** At the shipped
configuration (`MV_EXTRA_MAX = 2`, `MV_EXTRA_MIN_GAIN = 0.03`) it reproduces §7's
`blend_coverage` for all seven props **exactly** — 0.4879, 0.5154, 0.5504, 0.5743,
0.5851, 0.6477, 0.7623 — and row 27's depth column within 0.7 px, the same
tolerance row 27 reported against row 26. The sweep regroups
`hole_component_depths` with `np.maximum.at` instead of its per-label full-atlas
comparison, and asserts the result component-for-component against the shipped
function on every prop's base state before trusting it (cypress: 18 983
components, identical).

| prop | atlas | shipped | cap 1 | cap 2 | cap 4 | cap 8 | cap 16 | **ceiling, 41 views** | components still over |
|---|---|---|---|---|---|---|---|---|---|
| candelabra_shrine | 1024 | 10.92 | 10.92 | 10.92 | 10.61 | 10.55 | 10.51 | **10.51** | 16 |
| crucero | 2048 | 9.84 | 9.84 | 9.84 | 7.67 | 6.49 | 5.86 | **5.60** | 55 |
| gravestone | 1024 | 7.21 | 7.21 | 7.04 | 7.04 | 7.04 | 7.04 | **6.04** | 15 |
| broken_column | 1024 | 5.45 | 5.45 | 5.45 | 5.45 | 5.45 | 5.16 | **4.81** | 21 |
| olive_stump | 1024 | 3.77 | 3.77 | 3.27 | 3.27 | 3.27 | 3.27 | **3.27** | 20 |
| chapel_arch | 2048 | 2.89 | 2.89 | 2.86 | 2.86 | 2.86 | 2.86 | **2.41** | 16 |
| cypress | 2048 | 2.75 | 2.80 | 2.75 | 2.75 | 2.75 | 2.75 | **2.75** | 9 |

Every figure is `max_hole_depth_frac` as a percentage of atlas width; the cap is
**1.5**. **There is no crossing point on any prop, and the curve is flat.** Six of
seven sit within 0.5 points of their cap-2 value by cap 8; cypress does not move
at all after cap 2. The best result anywhere is chapel_arch's 2.41% at 41 views —
still 1.6× the cap.

**View count, and what it prices for rows 34/35.** Raising the cap does buy
`blend_coverage` (olive_stump 0.5851 → 0.7118, cypress 0.7623 → 0.8638) and does
not buy a pass. The gate is depth, so **the answer is not to raise the view
count**: going from the shipped 5 views to 41 multiplies the ComfyUI canvases
roughly eightfold and still refuses. The rebuild's canvas budget stays where it
is.

**Neither constant is re-derived, and that is the measurement's answer rather
than a dodge.** `MV_EXTRA_MAX` keeps **2**: no tested value produces a pass on any
prop, so any other number would be invented. `MV_EXTRA_MIN_GAIN` keeps **0.03**;
what changes is its comment, which justified the floor by "a smaller residue is
scattered enough that Telea inpaint suffices" — the assumption row 27 replaced
with a depth measurement, so it was a stale claim in the sense §5 forbids.
Measured, after the first pick every prop drops to ≤2.94% gain and decays under
0.7% by the fourth, and **no pick below the floor moves any hole component's
depth on any prop**. The comment now states that constraint instead.

**What actually refuses the props, and it escalates: about half of every prop
mesh is interior surface no external view can reach.**

Measured on all seven, one ray from each face centroid along its own normal: the
fraction of surface **area** facing the model's own interior is **33.4% (cypress)
to 53.8% (broken_column)**, five of the seven above 44%. Signed volume confirms
the shape rather than restating it — gravestone encloses 0.119 m³ inside a
2.650 m³ bbox, candelabra 0.082 of 2.288, olive_stump 0.026 of 0.328 — each equal
to (outer area × wall thickness) within a few percent, which is a hollow
double-walled shell, not a solid. Every mesh is open (3 977–16 703 boundary
edges) with **zero** non-manifold edges on all seven.

At texel level the two sides separate cleanly, probed on **all seven**. A ray
along a texel's own normal escapes to open air for **72.7–96.0% of covered**
texels and hits the mesh for **98.7–100% of ceiling-uncovered** texels, crossing
the interior to the far wall (chapel_arch 0.52 m, gravestone 0.51 m,
broken_column 0.39 m, cypress 0.25 m, crucero 0.19 m, candelabra 0.09 m,
olive_stump 0.06 m). The reverse ray then hits the outer wall at **8.3–62 mm** on
six of the seven — that is the shell's wall thickness. **cypress is the
exception at 0.52 m**, and reading it as a wall would be wrong: it is a 7 m
foliage tree whose interior-facing area is the far side of fronds across open
canopy, which is also why it carries the lowest interior fraction (33.4%) and the
highest reachable coverage (0.8638). `coverage.py`'s own occlusion term agrees
independently: covered texels sit at depth-excess ≈ 0 and uncovered texels sit
**0.10–0.31 m behind** the surface the depth render saw, with **0%** of them
failing the facing test. Nothing is refused for want of a camera angle;
everything is refused for being behind the object.

The inner wall reaches the atlas because `prop_cleanup.unwrap_atlas` hands the
whole mesh to xatlas. Measured on the UV side — the share of *island* whose texels
are interior-facing — it is **27.8% (cypress) to 54.6% (broken_column)**, against
the 33.4–53.8% measured on 3D area; the two agree in magnitude but only within
6.0 points per prop (chapel_arch 44.2 vs 50.1, cypress 27.8 vs 33.4, gravestone
49.6 vs 48.9), so they are two measurements of the same thing and not a check to
the point. Either way roughly **half of each prop's texel budget and half its
triangle budget are spent on surface the player cannot see and the generator
cannot reach.**

**Deleting the inner shell would not by itself clear the gate on candelabra.** Its
deepest component (10.51%, 40 693 texels) is *exterior* — the reverse ray escapes
for 64% of it, its mean normal points straight up, and its own normal ray hits
prop geometry 9 cm away: a disc face under the stacked arms, occluded by the
prop's own structure. Its second (6.29%) is inner wall. Both mechanisms are
present and the first does not fix the second.

**Two consequences worth naming, neither fixed here.** `MV_EXTRA_MIN_GAIN *
island_total` normalises against an island that is about half unreachable, so
"3% of island" is really ~5–6% of reachable island; and on candelabra 23.5% of
the texels the pipeline calls *covered* are inner-wall texels whose colour was
sampled through a wall thinner than `MV_OCCLUSION_EPS` (20 mm). Both dissolve if
the interior stops being unwrapped.

**For the user — a content and mesh decision, not decided here.** The options as
the measurement shows them:

1. **Drop interior faces in `prop_cleanup` before the unwrap**, by the test used
   above (a face whose own normal ray hits the mesh). Frees ~half the triangle
   budget and ~half the atlas, and is the only option that also raises texel
   density.
2. **Keep the geometry and exclude it from the atlas and island mask**, so the
   gate measures only reachable surface. Cheaper; leaves the triangle budget
   spent.
3. **Obtain a watertight solid from the generator.** The shell originates upstream
   of `prop_cleanup`, which carries no solidify or shell step.

Not measured here, and it bounds all three: whether the residual **exterior**
self-occlusion clears 1.5% once the interior is removed and the mesh re-unwrapped.
The atlas repacks, so that number cannot be read off this sweep — and candelabra's
exterior disc face says at least one prop would still fail.

**Rows 35 and 38 are blocked on that ruling, not on a threshold.** A rebuild run
today reproduces the refusal exactly, at GPU cost, at any pick cap.

**Cost.** Seven sweeps, **965 s** total (63.9–224.6 s per prop, of which only
5.6–12.2 s is rendering; the remainder is numpy over 0.83–2.87 M island texels),
plus ~6 min of geometry probes. Blender CPU only; no GPU and no generation, so no
heavy-compute approval was required.

*Found while sweeping, and it costs the shipped gate:* `hole_component_depths`
loops `labels == label` over the full atlas once per component, which is
O(components × atlas). cypress has 18 983 hole components at 2048², making one
call ≈ 2 minutes — paid on every gate evaluation and twice per call site in
`coverage.py:main`. **Applied, `196ac50`:** `np.maximum.at` over the flattened
label image plus `np.bincount` for the counts, 70 s → 0.057 s on cypress (1227×).
Equivalence re-measured against the shipped loop over all seven archived hole
maps — same count, labels, texels and `depth_frac` within 1e-12 on every
component, 870 to 20 200 per prop — with a deliberately wrong variant confirming
the comparison can fail.

**Row 27b — the shell's origin, located and evidenced, 2026-07-26. It is
Hi3DGen's mesh extractor. Nothing in this repo creates it.**

*Ruled by the user before this row ran:* the fix is at the root, not a cull step
in `prop_cleanup` — "we should do the cleanest job, dont do mess over mess trying
to clean errors". Options 1 and 2 of row 27a's escalation are dead by that
ruling; this row establishes what option 3 actually is.

**Measured across every stage of the chain, all seven props, every intermediate
surviving on disk (`raw.glb` → `clean_hires.glb` → `clean.glb` → shipped).** The
interior-facing area fraction is **already 38–54% in `raw.glb`** and never jumps:
`symmetrize` (`prop_cleanup.py:160-187`, and only candelabra ever ran it) moves it
47.02 → 48.28; floater removal and collapse decimation move ≤0.4 points; `unwrap_atlas`
is UV-only and leaves geometry byte-identical. Three unrelated Hi3DGen candidates
outside the shipped set measure 31.3–36.1%: it is every run, not these seven.
Controls: a solid cube and sphere read **0.00%**, a hollow closed shell 47.96%,
the non-Hi3DGen Poly Haven rocks 0.26% and 1.39%.

**Mechanism, in vendored MIT code.** `utils_cube.py:74-80`'s `get_dense_attrs`
allocates the full dense `(res+1)³` grid and stamps every cell `+1` = *outside*,
then scatters the network's predicted SDF onto only the sparse-active vertices.
The SLat structure is a surface shell of voxels, so cells deep inside the object
keep `+1`. `cube2mesh.py:143-147` then marches the whole dense grid: the field is
negative only in the thin active band and positive on **both** sides, so marching
cubes extracts **two** isosurfaces — the true outer surface and a second wall one
band inward. `decoder_mesh.py:133` sets `res = resolution*4` = **256³**, and the
measured wall thickness across the seven props is **1–9 cells of that grid,
independent of each prop's real size**. A genuine solid measures ~512. A fixed
handful of voxels is a grid artifact, not geometry.

**Correction to row 27a's premise.** The raw meshes are **closed manifolds**
(0–366 boundary edges, 0 non-manifold, on ~1 M triangles) — closed *hollow*
shells, not open surfaces. The 3 977–16 703 boundary edges measured on shipped
files are glTF vertex splits at UV seams: candelabra's UV-less `clean.glb` is the
same geometry with **12**. Openness was never part of the defect.

**The fix, verified synthetically on CPU: flood the *positive region* from the
grid boundary.** Untouched cells are already `+1`, so the passability predicate is
literally `field > 0` — the flood walks through the network's own predicted-outside
band, and only untouched cells it cannot reach are set `-1`. Written cells are
never altered. `ndimage.label` on 257³ costs ~0.2 s.

The defect reproduces first, which is what makes the fix's result mean anything:
a true SDF sparsified the way SLat sparsifies it, run through the shipped
extraction path, yields two walls at 46.7–55.2% interior-facing with volume
0.14–0.29× true. With the fix, sphere and L-solid return to **0.00%**, torus to
3.74% against its own true 3.72%, and triangle counts land **exactly** on the
true-solid reference, closed and manifold throughout.

Three candidates were rejected by measurement, and one of them is the obvious one:
- **Flood the *untouched* cells instead** — correct on convex and simple shapes,
  but it **welds narrow-mouthed concavities shut**. A cup with an 8-cell mouth
  relabels 1.65 M cells of which 98.7% are outside the true surface, volume 4.94×.
  Right idea, wrong predicate.
- **`sdf_init=False`** — 95.5% of the grid becomes exactly the isolevel: 100%
  interior-facing, negative volume, 1 304 boundary edges. Also unreachable, the
  sole call site hardcodes `True` (`cube2mesh.py:354`).
- **`marching_cubes(mask=…)`** — skimage's mask does not mean "all 8 corners", so
  it cannot excise the band-boundary cubes: 24 843 boundary edges, still 41.9%.
- **Drop the inner shell as a component** — refuted on the real meshes; the inner
  wall is not a separate component (column 964 504 tris, largest component
  955 578; the rest are sub-3k specks).

**Foliage is not at risk.** On thin-plate synthetics at five gap widths the fix is
an exact no-op — **0 cells relabelled** — because a structure thinner than the
SLat band has no untouched interior to double-wall. *But the diagnostic does not
transfer:* a correct solid comb reads 73.7% interior-facing purely from legitimate
self-occlusion, so cypress's 37.10% may be partly or wholly legitimate. Do not
read cypress's number as shell.

**Inherent limitation, a real behaviour change.** A *fully sealed* cavity is
solidified — no boundary-connected path exists, so no grid method can distinguish
a sealed void from solid. The affected geometry is invisible from outside and its
removal lowers triangle count.

**Unverified, and only a GPU run can close it:** the fix is untested on real SLat
data. The synthetic band carries a true SDF; the network's is noisy. Specifically
open — whether a *positive* predicted band vertex can border an enclosed untouched
cell, which under a `-1` fill would spawn a spurious surface. It never happened
synthetically.

**Cost, and it restructures §8.8.** `prop_hi3dgen.py:169` calls
`hi3dgen_pipeline.run(...)`, and `hi3dgen.py:385-387` fuses
`sample_sparse_structure → sample_slat → decode_slat` in one `@torch.no_grad()`
call with `coords` and `slat` as locals returned to nobody. The script writes only
`concept_rgba.png`, `raw.glb` and the manifest; `gen_prop.py:142-160` sets the
resume boundary at `raw.glb`, i.e. *after* extraction. A disk search found **no
surviving latent** anywhere. **GPU sampling must therefore re-run per prop —
extraction cannot re-run alone**, and no per-prop sampling wall-time is recorded
in any manifest or log (they carry step counts and `peak_vram_allocated_gb` only),
so the first run is the only thing that can price the rest.

Seven props to re-run: `b3/column/cand_0`, `candelabra-z/cand_4`, `b3/arch/cand_0`,
`b3/crucero/cand_21`, `b3/cypress/cand_21`, `b3/cross/cand_1`, `b3/stump/cand_0`.

**Rows 34–38 are superseded in scope.** They priced a re-texture of existing
meshes; the work is now regenerate-then-retexture, and row 34's ask must carry the
extractor patch, not just the texture chain.

*Integrity:* nothing under `C:\tools\Hi3DGen` was modified — the three extractor
files retain their install-date mtimes and hashes; the harness re-implements the
numeric path in the scratchpad and only reads the Hi3DGen tree.

**Row 27c — the extractor fix was written, verified, run on real data, and is a
NO-OP. 2026-07-26.**

`fill_enclosed_sdf` (`750397b` on `fix-hollow-shell-extraction`, +20 lines, one
file, unpushed) floods the positive region from the grid boundary and fills the
unreachable remainder. Through Hi3DGen's **real** extraction code it took a
synthetic sphere 55.24% → 0.00% interior-facing, a torus 54.01% → 3.74% against
its own true 3.72%, landed triangle counts exactly on the dense-field reference,
relabelled zero cells wrongly on every solid case, and was bit-identical on thin
plates. Ten cases, closed and manifold throughout, controls stated.

**On `broken_column` it changed nothing.** Regenerated from the same
`concept.png` at the same seed 0 with the patched extractor —
`target/prop-batch/b4/column/cand_0`, **1389 s** wall for geometry + cleanup,
exit 0:

| | tris | interior-facing | bnd | non-manif | signed vol |
|---|---|---|---|---|---|
| shipped (`b3`) | 964 504 | **53.38% ±0.29** | 0 | 0 | 0.053727 |
| regenerated (`b4`, patched) | 963 484 | **53.65% ±0.29** | 0 | 0 | 0.053990 |

The patch did load: one call site, `.pyc` recompiled after the edit, branch
checked out at run time. It fails **safe** — which is indistinguishable from not
running, and cost the first stretch of diagnosis.

**The premise is false.** The fix requires the interior to be an *enclosed*
positive region. The shipped mesh is **one fused component of 955 830 triangles
carrying both walls** (area 5.294, volume +0.054), where a cleanly separated
double wall would be two closed surfaces — so the negative band pinches out, the
interior connects to open air, and the flood correctly reaches it and fills
nothing. Every synthetic case was built from an analytic SDF whose band sealed
perfectly; nothing ever tested Hi3DGen's real band.

**That falsifying measurement needed no GPU and no new artifact** — it is three
minutes of CPU on a `raw.glb` that had been on disk since 23 July. It was run
only after the regeneration failed. Lesson:
`tasks/lessons/2026-07-26-synthetic-input-cannot-validate-a-premise-about-real-input.md`.

**Row 27d — why no flood can work, and what replaces it. 2026-07-26, CPU only.**

The lost field's *sign* structure is recoverable from the mesh: `raw.glb` is that
field's level set, so rasterising it onto the same 257³ grid the extractor uses
(`decoder_mesh.py:133` → res 256; `utils_cube.py:84` → world = idx/256 − 0.5)
returns the negative region exactly. The probe **failed first** — marching-cubes
vertices lie *on* grid edges, so column rays double-count shared edges, 0.495
volume ratio — and after shifting the mesh off the lattice it recovers the true
sign field with **0 mismatched cells** on sphere, L-solid and hollow shell (torus
28 cells, 0.00016%). End-to-end control: rasterising the synthetic *defect* mesh
and filling holes returns **2 647 631** cells, exactly what the real patched
extractor relabelled.

**The band does not pinch out — it stops.** Minimum band thickness is **2.00
cells on all seven props** (p50 2.00–8.25, max 16.49), and only 4 band cells
touch the grid faces, so neither zero-thickness pinholes nor domain clipping
explains anything. The negative shell simply has wide rims, with openings ~10
cells across — the same order as its own thickness.

Cells the committed fix would relabel, against an interior of order 1.4 M:

| prop | tris | negative cells | **fix finds** | band p50 / min |
|---|---|---|---|---|
| crucero | 341 808 | 197 817 | **0** | 2.00 / 2.00 |
| gravestone | 680 448 | 173 191 | **0** | 2.00 / 2.00 |
| chapel_arch | 773 908 | 338 556 | **12** | 2.00 / 2.00 |
| broken_column (b4) | 963 484 | 906 777 | **569** | 4.00 / 2.00 |
| broken_column (b3) | 964 504 | 901 613 | 2 492 | 3.46 / 2.00 |
| olive_stump | 1 273 538 | 1 249 574 | 3 862 | 4.00 / 2.00 |
| cypress | 299 938 | 413 358 | 36 029 | 8.25 / 2.00 |
| candelabra | 334 970 | 261 268 | 155 622 | 2.83 / 2.00 |

b3 and b4 are structurally identical, so this is a property of Hi3DGen output and
not of one run.

**The `untouched`-cell variant dies with it.** Dilating the barrier by up to 4
cells in every direction still fails on three of seven — gravestone goes
`[0, 59, 13, 16, 5]` and cypress *decreases* monotonically. gravestone is
unambiguously double-walled (44 454 four-crossing ray columns, 49.35%
interior-facing) **and** stays connected to open air behind an 8-cell barrier. No
flood, of any predicate or any thickness, encloses these interiors.

*What cannot be determined, and why the evidence is gone:* whether real prop
concavities have mouths narrower than the band. A mouth narrower than the band
was welded shut by the extractor before any mesh existed to measure.

*Why the synthetic battery could not have caught this:* it fed the band the
**exact** SDF at every vertex of every active voxel, so every straddling voxel
necessarily had a negative corner and the negative region was necessarily a
closed shell. The real network's values are approximate and its negative region
has wide rims. No synthetic band built that way can exhibit the failure.

**The structurally correct direction, untested:** stop stamping a constant. An
untouched cell should inherit the sign of its **nearest written cell** rather than
a global `+1` — a cell just inside the surface reaches a negative band cell, deep
interior reaches the innermost band cell, also negative, and exterior reaches
positive. That assumes no enclosure and no connectivity, so the measured failure
cannot arise, and a locally missing negative band degrades to a small blemish
instead of a whole second wall.

**Row 27e — one batched GPU run, approved 2026-07-26, and it is the last one this
problem needs.** All seven props re-sampled in a single process (model load paid
once), dumping per prop:

- `slat.pt` — the SLat latent, ~1 MB. Closes the defect that made "GPU must re-run
  per prop" true: `decode_slat` is a standalone method taking exactly this tensor.
- `cubefeats.pt` — the SparseTensor entering `SparseFeatures2Mesh.__call__`, which
  is the extractor's whole input. Everything downstream of it (`get_layout`,
  `sparse_cube2verts`, `get_dense_attrs`, marching cubes) is pure math with no
  network, so with this on disk **every further extractor iteration is CPU-only
  with zero GPU**. Captured by monkeypatching `to_representation` inside the
  throwaway driver; nothing under `C:\tools\Hi3DGen` is edited.

**Cost, and this corrects a figure used to price the whole rebuild.** A prop's
*geometry* is **59.9 s** — 12.7 s sampling, 20.1 s decode, ~30 s of one-time model
loads. The 1389 s measured on the b4 run was `--through cleanup`, so **Blender's
decimation and xatlas unwrap over ~1 M triangles dominate it, not Hi3DGen**. Row
34's ask must not price sampling at 23 minutes.

The clone returns to `main` for the run so the dead fix is not a variable.

**The dump is provably sufficient.** Re-extracting on **CPU from `cubefeats.pt`
alone** reproduces the GPU run's mesh: 964 514 triangles both ways, max vertex
deviation **1.19e-07** — float32 epsilon. Every extractor question is now
decidable without a GPU. Measured artifact sizes: `slat.pt` 0.9 MB,
`cubefeats.pt` 739 MB for broken_column (`feats [1 845 120, 101]` float32); ~2.9 GB
for the batch, extrapolated per prop from negative-cell counts. Peak VRAM 14.16 GB,
above the 11.38 GB the old manifests record — it runs, but closer to the ceiling
than that figure suggests.

**First launch failed in 30.5 s, all seven, and the driver was at fault.** The
`torch.hub.load` memoisation returned a `DinoVisionTransformer` where
`prop_hi3dgen.py:167` expects the StableNormal predictor: the local-snapshot load
at line 133 failed *after* its nested dinov2 load had populated the cache entry,
and the fallback at line 142 then hit the poisoned entry. Re-entrancy plus an
exception path leaving a partial value behind. The memoisation was **deleted**, not
repaired — the entire load phase is 30.8 s, so it risked the batch to save a
fraction of that.

*The generalisable part:* sixteen interception checks confirmed every patch
**fired** and **delegated**, and none confirmed a patch **returned the right
object**. The same shape as row 27c — verifying the mechanism instead of the
claim. `--dry-run` now exercises the loads and stops at the sampling boundary
(reaching it *is* the proof that line 167 succeeded), an identity check rejects a
wrong object at the moment of production, and a `--smoke` runs one prop end to
end. Both green before relaunch.

**Launched 2026-07-26 ~17:15**, driver at `scratchpad/dump_latents.py`, log at
`scratchpad/dump_batch.log`, output to `target/prop-latents/<prop>/`. It calls
`prop_hi3dgen.main()` **verbatim** per prop and memoises the three expensive loads
(`from_pretrained`, `preload_birefnet`, `torch.hub.load`) by monkeypatch, so the
recipe is the repo's own lines rather than a second spelling. A third artifact was
added beyond the two specified — `normal.png`, the StableNormal output `main()`
never persists — because without it a change to *sampler* settings would still
need the normal predictor. The three together close every loop: `normal.png` →
redo sampling, `slat.pt` → redo decoding, `cubefeats.pt` → redo extraction.

Per-prop seeds differ and were read from each `hi3dgen_manifest.json`, every
concept sha256 re-verified against its manifest: broken_column 0, candelabra 4,
chapel_arch 0, crucero 21, cypress 21, gravestone 1, olive_stump 0.

*The interception proof caught a real flaw before any GPU was spent.* The first
dry run blocked on `run_calls_decode_slat_dynamically = False` — `run` is
`@torch.no_grad()`-decorated, so its `co_names` is the wrapper's, and the check
needed `__wrapped__`. A weaker assertion ("the class attribute is my function")
would have passed while proving nothing. Fourteen checks now run, including
delegation through the real classes with stubbed originals and a `cubefeats.pt`
round-trip, plus a guard that reports the extractor **as imported** and blocks if
a stale `.pyc` carries the dead fix.

*Deferred, and it belongs with the real fix:* `prop_hi3dgen.py` should persist the
latent permanently, moving `gen_prop.py`'s resume boundary from after extraction
to before it. Not done during this run — the driver dumps it, and bundling an
unrelated permanent change into a GPU-critical step is how a run gets lost.

**Done 2026-07-26. All seven dumped in 159.5 s, 3.07 GB**, at
`target/prop-latents/<prop>/` — `slat.pt`, `cubefeats.pt`, `normal.png`,
`raw.glb`, `concept_rgba.png`, `generation_manifest.json`, `dump_manifest.json`.
Sizes 0.16 GB (crucero) to 0.98 GB (olive_stump). Peak VRAM 15.76 GB on
olive_stump. **GPU is now out of the loop for this problem entirely.**

**Row 27f — derive the real fix against the seven real fields. CPU only, free,
unlimited iteration.** Candidate is nearest-written-cell sign inheritance. Open
question to settle by measurement, not taste: whether an untouched cell inherits
the nearest written cell's *sign* (±1, bounded) or its *value* (continuous) — the
failure to watch is a spurious surface where a −1 fill abuts a written cell
holding +0.001.

Acceptance is **not** interior-facing area alone. Primary test is the **share of
ray columns with ≥4 crossings**, which a genuine double wall produces and
legitimate self-occlusion does not: crucero 15 362, broken_column 38 135,
gravestone 44 454 must collapse. Interior-facing, signed vs bbox volume (Hi3DGen
raws fill 3.6–19.4% of bbox; photoscan rocks 38–52%), triangle and edge counts
ride alongside.

Two props will mislead a careless read. **cypress** is foliage, not a shell — a
*correct* solid comb reads 73.7% interior-facing — so it is judged on the crossing
statistic. **candelabra**'s deepest atlas hole is *exterior* self-occlusion, a
disc face under the stacked arms, which no mesh fix addresses; it may still fail
the depth gate with a perfect mesh.

Whether the coverage gate then passes cannot be predicted from this — it needs
cleanup and texturing re-run. What can be reported is triangles saved and atlas
fraction freed.

**Row 27g — result: the extractor is not the bug, and rows 27b–27f's mechanism is
wrong.** Nothing committed; clone clean at `c29f668`, `fix-hollow-shell-extraction`
still parked at `750397b` and now known dead.

Step 0 passed on all seven: re-extraction from `cubefeats.pt` reproduces each
`raw.glb` (identical triangle counts, max vertex deviation ≤ 1.2e-07; chapel_arch
compared by face centroid at 3.97e-08 because the glTF exporter dedups one
vertex). Every claim below rests on that control.

Four fills were tried — nearest-written **sign**, nearest-written **value**,
sign·(|value|+distance), and a per-axis first/last-crossing envelope. The first
three are topologically identical to each other (predicted, and confirmed) and
**all three add triangles**. Gravestone got 39% worse. cypress's ≥4-crossing share
appears to fall 80.8 → 45.1 only because the fill grew solid blobs in open space —
its occupied column count went 35 937 → 62 203 and its bbox volume nearly doubled.
Judging on the crossing statistic alone would have passed that.

Three measurements kill the whole family:

1. **Four props have no enclosed interior at all.** Flooding untouched cells from
   the grid boundary with the written mask as barrier: crucero **0** enclosed
   cells, gravestone **0** — yet those two are 52.6% and 72.2% ≥4-crossing. Any
   enclosure-respecting fill is a mathematical no-op there.
2. **The negative region sits mid-band, positive on both faces.** broken_column:
   negative cells at median depth 4.2 cells inside the written band, positive
   written cells at 2.0. Crossing inward the sign reads **+, −, +**.
3. **The crossings are between cells the network itself wrote** — 77.2% (crucero)
   to 98.9% (cypress) written↔written, the rest involving a stamped cell.

Since both marching cubes and FlexiCubes derive topology from **corner sign
changes**, (3) is decisive independently of which extractor runs: no operator swap
and no stamp policy can remove a sign change that lies between two predicted
values. The `+1` stamp is faithful — it agrees with the positive values already
there. SLat is a surface shell; the decoder's SDF is negative only in a thin core
of that shell and positive again on its inner face. The double wall is what
Hi3DGen produced, not what `get_dense_attrs` did to it.

**The envelope operator is not proposed** — it fills chapel_arch's arch opening and
drives gravestone to 59.1% bbox fill. Its only value is as a bound: it cuts
36–44% of triangles on the shell-like props, so the inner wall is that share of
the budget and is removable in principle.

**Where the fix belongs, and why this is the root and not a patch.** The extracted
mesh is closed and 2-manifold and its outer surface is correct; only the interior
was never represented. The field leaks through the band's rims — which is why
every flood over the *field* failed — but the **mesh** seals (0–68 boundary edges,
0 non-manifold). So the sealed boundary the operation needs exists in the mesh and
does not exist in the field. A voxel flood of the *exterior* using the mesh as
barrier, complement = solid, is therefore the correct operator: it fills the hollow
core while leaving chapel_arch's through-arch and gravestone's cross-shape
exterior, which is exactly where the axis-hull failed. Preferred over generalized
winding number, which on a shell whose inner wall is inward-oriented returns the
shell rather than the solid.

Not established: whether any of this improves cypress (2 361 enclosed cells, 98.9%
written↔written, envelope barely moves it — its 37% interior-facing is likely
legitimate foliage self-occlusion); candelabra's disc-face exterior occlusion is
untouched by any mesh fix; and whether the coverage gate passes needs cleanup and
texturing re-run.

**Row 27h — decision 9 (user, 2026-07-26): the solidify operator lives in the
Tyche3DGen fork**, applied right after extraction, not in `prop_cleanup`. Rationale
carried from the ask: it keeps the correction at the point of production, makes the
upstream PR to `Stable-X/Hi3DGen` coherent, and strips the inner wall's 36–44% of
triangles *before* `prop_cleanup`'s decimate and unwrap — which is where the 1389 s
measured in row 27e actually went, not in sampling (59.9 s).

Design handed to the derivation: use the **mesh** as the sealed barrier the field
lacks, but correct the **field** and re-extract. Extract normally → ray-crossing
parity occupancy on the 257³ grid from the mesh → cells inside-by-parity holding a
positive SDF are the hollow core, set to −1 → re-run marching cubes. The outer
isosurface's own values are untouched, so the outer surface should return unchanged
while the inner one vanishes.

Acceptance is three gates, all required, and **B and C are meaningless apart**:
**A** the outer surface must not move (the control the last round lacked); **B** the
≥4-crossing column share must collapse; **C** bbox fill and signed volume must not
balloon — the trap that nearly passed the `value` fill, where blobs grown in open
space read as 2-crossing and diluted the statistic being judged.

Two lesson notes were written from these two dead rounds:
`2026-07-26-synthetic-input-cannot-validate-a-premise-about-real-input.md` and
`2026-07-26-a-visible-mechanism-is-not-an-attributed-one.md`.

**Row 27i — the fork-side operator's first attempt is rejected; it is the envelope
in disguise.** Parked on `solidify-shell-interior` in the clone, unpushed, not
adopted. A three-stage heuristic (2-of-3 axis slice enclosure, morphological
closing r=2, axis-aligned veto) reproduces row 27g's rejected axis-aligned envelope
to within ~1% on every prop where both were measured:

| prop | tris env → cand | ≥4-cross | interior-facing | bbox fill |
|---|---|---|---|---|
| gravestone | 393 972 → 394 788 | 16.2 → 16.3 | 9.4 → 9.7 | **59.1 → 59.1** |
| crucero | 218 392 → 219 212 | 14.3 → 14.5 | 8.4 → 8.6 | 13.1 → 13.0 |
| broken_column | 538 978 → 544 874 | 35.0 → 35.7 | 17.3 → 17.6 | 24.5 → 24.4 |
| cypress | 264 832 → 263 828 | 78.5 → 78.3 | 34.5 → 30.7 | 21.9 → 21.5 |

The envelope was rejected on principle for filling concavities and oblique
through-holes; a longer derivation reached the same operator. gravestone's 59.1%
bbox fill is not "one number outside the photoscan band" — it is the rejected
operator's signature. **Gate A could not catch this by construction**: filling a
concavity only ever moves the surface *forward*, and forward motion is what gate A
permits.

Two negative results from that round are accepted and load-bearing:

- **Parity against the mesh is degenerate.** For a closed MC mesh, ray-crossing
  parity ≡ the sign of the field it came from; proven on all seven including a
  26-direction generalisation. This kills row 27h's briefed operator. My stated
  rationale — "the mesh seals where the field leaks" — was wrong *as stated*.
- Field-space morphological sealing at radii 1–6 seals nothing; the enclosed set
  equals the closing's own crevice additions at every radius.

**Row 27j — the untested predicate: reachability, not parity.** The two differ
exactly on **bounded components**, and a hollow core is bounded — a ray through it
crosses four surfaces so parity calls it outside, while a flood from the bounding
box cannot reach it. No round has yet flooded against the actual *triangles*
(conservatively voxelized at 512³, above the 257³ extraction grid the field floods
leaked through).

Step 1 is a premise test and the whole first deliverable: **do large bounded
components exist?** Per prop — component count, enclosed volume as % of bbox, leak
diagnosis (cypress 366 and olive_stump 42 boundary edges are genuinely open), and
resolution stability at 1024³. If the answer is no, the line ends: *no operator
computable from this data alone can recover the solid; it requires an explicit
prior about the objects.* That is a wanted answer, not a failure to route around.

**Gate D is new and permanent**: any candidate must report IoU and symmetric
difference against the axis-aligned envelope's occupancy. Agreement within a few
percent means the candidate *is* the envelope and is rejected regardless of
derivation. **Gate E**: through-holes must survive — the exterior must remain one
connected component through chapel_arch's arch and crucero's openings, verified,
not eyeballed.

**Row 27k — answer: NO. The line ends here, and this is the final word on it.**
Nothing committed; clone returned to `main` at `c29f668`. `fix-hollow-shell-extraction`
(`750397b`) and `solidify-shell-interior` (`53472a1`) both parked, both dead.

The predicate was validated before use, with a negative control: on synthetics a
solid sphere returns one bounded component matching (4/3)πr³ to 2%, a two-sphere
shell returns exactly two — and **deleting one triangle of 20 480** makes the wall
leak completely. So a negative on a real prop means *open*, not under-resolved.

At 512³ conservative voxelization, five of seven props have their entire signed
volume inside `[bounded, bounded+barrier]` — **the bounded set is the wall material
and nothing more.** Every largest component is a thin sheet spanning the whole
object (inscribed radius 1–4% of grid width), not a core. Share of
silhouette-enclosed volume reachable from the bounding box: gravestone **90.5%**,
chapel_arch 74.9%, broken_column 66.2%, crucero 64.2%, olive_stump 61.7%. The
apparent hollow core is exterior.

**The mesh is a cup, and its rim is a fold, not a hole.** broken_column proves it
with zero boundary edges: 99.1% of its triangles form one connected closed surface
enclosing +0.054022 — the thin wall alone. Inward-oriented (cavity-bounding)
components: broken_column 0.05% of bbox, chapel_arch 0.00%, crucero 0.00%,
gravestone **0.00%, zero inverted components at all**. There is no inner surface;
the "double wall" is a single folded one. A cup encloses only its wall — its inside
is outdoors. That one fact retro-explains every failure in this chapter: the field
floods, the parity degeneracy, and the absence of bounded components.

Leaks are irrelevant: capping every boundary loop with a centroid fan and
re-flooding changes the result **bit-for-bit** on chapel_arch, crucero, gravestone
and olive_stump (76.98→76.98, 65.46→65.46, 90.45→90.45, 61.79→61.79). Cypress moves
1.0 point. Resolution is not marginal either — bounded volume rises monotonically
toward signed volume as the barrier thins (broken_column 8.049→8.680 at 1024³
against 9.252 signed), with no room left for a cavity.

The single genuine sealed cavity, candelabra_shrine's flat 221×63×221-cell pocket
(2.09% of bbox), is not a way out: candelabra has the **lowest** ≥4-crossing share
of all seven (37.1%). Filling real cavities cannot address the defect.

**Consequence for row 27h's ruling.** The fork was chosen as the fix site on the
premise that this was Hi3DGen's bug and the correction was upstreamable. It is not
a bug — Hi3DGen emits what SLat's surface-shell representation supports. There is
no upstream PR to file, and the fork's rationale no longer stands on that argument.
Any operator from here is our pipeline's own content decision, carrying an explicit
prior about the objects rather than a computation on the data. **That prior is the
user's ruling to make and is asked, not assumed.**

Harnesses retained in scratchpad for whichever operator is chosen: `enclosure.py`,
`enclosure_control.py`, `core_reachable.py`, `cap_and_flood.py`, `enc_summary.py`,
with `enc512_bc.json`, `enc512_rest.json`, `enc1024.json`, `core512.json`.

**Row 27l — decision 10 (user, 2026-07-26): accept the shells.** No geometry
operator. Coarse voxel remesh and visibility-based face deletion were both offered
and both declined; the ruling is to stop fixing geometry and re-derive the atlas
coverage gate instead. The whole extractor line (rows 27a–27k) closes here with no
code adopted; `fix-hollow-shell-extraction` and `solidify-shell-interior` stay
parked in the clone and are never merged.

**The accepted cost, stated on the record.** Roughly 45% of surface area is
interior, so roughly 45% of atlas texels are spent on faces no camera sees.
Effective density on *visible* surface is therefore ~12 mm/texel, not the 8.9
mm/texel the detail-layer plan quotes. That strengthens the case for the
world-space tiling detail layer rather than weakening it: the atlas's remaining job
is macro identity — tone, stains, weathering, baked AO — which survives 12 mm; it
was never going to carry 1–3 mm limestone grain at any density we can buy. The
triangle cost is separately absorbed by `prop_cleanup`'s existing decimation.

**Why the gate must change, and the one change that is legitimate.** Interior faces
receive UV charts (`island` true) but no view reaches them (occlusion), so they are
permanent hole components with large `depth_frac` and the gate refuses every prop.
`coverage.py:313` already prints the diagnosis in the failure path: *"no candidate
direction newly covers the offending component(s)."* The gate exists to say *add
this view*; on interior texels that advice cannot be followed.

- **Forbidden:** raising `MAX_HOLE_DEPTH_FRAC` until the props pass. That is a test
  rewritten to dodge a broken rule and is rejected outright.
- **Forbidden:** shrinking `island`, or changing atlas packing — that is row 27a's
  option 2, which the user killed, and it would change the produced texture.
- **Adopted:** restrict the hole statistic to island texels that *some* view in the
  base set ∪ the 37-direction candidate set can reach. Unreachable texels stay in
  the atlas, stay inpainted, and stop being counted as a coverage failure — because
  no view set can fix them. This changes no output byte; it changes only what the
  gate calls a failure, and it makes the gate actionable by construction.

The candidate depth renders this needs are **already computed** on both paths
(`pick_extra_views` consumes them), so the restriction costs no extra render.

Required negative control: with a base view dropped so a genuinely visible region
goes uncovered, the gate must still fire. A gate that cannot fail is not a gate.

**Row 27m — the gate change landed and works; it unblocked one prop and exposed a
second cause.** In the working tree, uncommitted: `proptex/coverage.py` (`pick_extra_views`
also returns `reachable`, accumulated in the single pass over `cand_depths` it
already made, so no extra render), `proptex/albedo.py` (`blend_views` takes
`reachable`; this is the pipeline's actual gate), `prop_texture.py` (threads it
through `geometry_stages`/`basecolor_stages`, persisted as `reachable.npy` in the
existing `nbv` cache unit). `coverage_stats` untouched — its reported JSON is
byte-identical for every prop, because only the failure predicate moved.

Negative control passes: with `broken_column`'s two side base views dropped, the
gate fires harder (33 → 45 offending components).

| prop | exit | n_over after | max depth before→after | unreachable island |
|---|---|---|---|---|
| broken_column | fail | 33 | 5.45%→3.15% | 46.5% |
| candelabra_shrine | fail | 30 | 10.92%→8.71% | 28.7% |
| chapel_arch | fail | 27 | 2.89%→2.54% | 38.7% |
| crucero | fail | 36 | 9.84%→9.62% | 41.3% |
| cypress | **pass** | 0 | 2.75%→0 | 13.6% |
| gravestone | fail | 119 | 7.21%→6.25% | 46.8% |
| olive_stump | fail | 40 | 3.77%→3.77% | 28.8% |

**Row 27l's diagnosis was real but incomplete.** `wholly_unreachable` is 0 for four
of seven props: a hole region is almost always a reachable rim fused to unreachable
interior. Restricting to `island & reachable` correctly splits that blob — max depth
drops on every prop, the right direction — but the reachable rim often exceeds 1.5%
on its own, because `MV_EXTRA_MAX = 2` and `MV_EXTRA_MIN_GAIN = 0.03` cap how much
*reachable* exterior is ever covered. Rising component counts (gravestone 17→119)
are that split, not a regression.

This second cause is **actionable**, unlike the interior: the gate now names
directions that would fix it. Row 27n prices the required view budget in canvases
before any ask.

**Row 27n — `clean.glb` means different things across batches, and this is a real
provenance defect.** In `b3` it is post-unwrap and carries UVs; in `candelabra-z` it
is pre-unwrap with none, so `coverage.py:251` refuses it. Established by face count,
which is invariant under UV seam splitting: the shipped candelabra_shrine glb has
**14460 faces**, matching `candelabra-z/cand_4` exactly — the odd one out among five
candidates otherwise at ~15000 — with 7241 → 13222 verts from seam splitting.

An overwrite by one of the reverted geometry-fix rounds was hypothesised and is
**refuted**: the archived sha256 matches the manifest's recorded
`clean_glb_sha256`, which an overwrite would have broken, and all five candidates
are internally consistent. Nothing corrupted the archive. Filed as a stage-boundary
inconsistency to fix in the rebuild rows, adjacent to the known defect that
candelabra_shrine's registry no longer describes its shipped asset.

**Row 27o — the view budget, priced.** Harness re-runs `pick_extra_views`' greedy
verbatim one pick at a time with the gain floor removed; no constant edited. It
reproduces every prop's reported `n_over` and depth at one extra view exactly, so
it measures the shipped pick and not a paraphrase of it.

**`MV_EXTRA_MIN_GAIN` is the binding constraint, not `MV_EXTRA_MAX`.** All six
failing props take exactly **one** extra view; the cap of 2 is never reached.
Pick #2's gain: candelabra 0.0293, olive_stump 0.0294, chapel_arch 0.0156,
broken_column 0.0135, crucero 0.0046, gravestone 0.0039 — all under the 0.03 floor.
Admitting every prop's full passing prefix needs a floor of **0.0001**, i.e. none.

| prop | extra views to pass | extra canvases | needs min-sep relaxed? |
|---|---|---|---|
| cypress | 2 | 1 | no — passes today |
| candelabra_shrine | 6 | 3 | no |
| olive_stump | 16 | 8 | no |
| chapel_arch | 20 | 10 | yes |
| broken_column | 22 | 11 | yes |
| crucero | 24 | 12 | yes |
| gravestone | 29 | 15 | yes |
| **total** | **119** | **60** | |

60 extra canvases against 7 today — **74 total vs 21, ~3.5× the whole generation
cost.** Past roughly pick 4 on every prop, per-pick gain is 0.01–0.2% of island:
the picks stop painting surface and start chasing fragments. gravestone's 11
residual components total **24 texels** (sizes 1, 1, 1, 5, 1, 1, 1, 2…) and cost 13
canvases to erase.

**Two artifacts inflate that price, and both are genuine defects.**

1. **`MV_EXTRA_MIN_SEP_DEG = 20` makes the ±55°/75° rings self-pruning.** The
   candidate grid steps azimuth 30° at every elevation, but great-circle separation
   is Δ·cos(elevation) — 17.1° at 55°, below the filter. Picking any azimuth on
   that ring permanently kills both neighbours. Every residual component on the four
   stalling props is on the +55° ring and is *fully* covered by pruned candidates:
   broken_column 452 texels by (180°,55°)+(120°,55°), chapel_arch's 177 by
   (180°,55°) alone, crucero's 88 by two, gravestone's 24 by two. The ±15°/−35°
   rings are unaffected (24.5° and 28.9° separation).
   **Root fix is a deletion**: the greedy loop applies this angular prune *again*
   after each pick, where it is redundant with the gain criterion — a near-duplicate
   scores ~0 marginal gain against the actual remaining uncovered set, which is
   exact where the angular proxy is an approximation. Keep it in `extra_candidates`,
   where it genuinely saves renders; delete it from the pick loop.
2. **`787cf74` changed the mask without adapting the statistic to it.**
   `hole_component_depths` labels components over `island & reachable` but its
   distance transform still measures to the nearest **covered** texel, straight
   through unreachable territory. A single reachable texel stranded in a large
   interior blob reports `depth_frac` 3.71% — 38 texels of extrapolation — while
   being one texel of visible surface, and refuses the whole prop. The depth
   statistic assumed connected regions; restricting the mask fragments them into
   specks and depth-alone stops being a proxy for damage. This is a consequence of
   my own change and is named as such.

   **Correction to my first reading of this defect.** The distance transform is
   *physically right* — Telea does extrapolate that far and does not care about
   reachability — so it is not to be "fixed". And dropping component labelling to
   gate on total per-texel area, which I proposed first, is **rejected**: it loses
   contiguity, which is exactly what separates a visible smear from harmless
   speckle. The defect is that `depth_frac` alone decides failure while ignoring
   component **size**.

   The correction is a size condition riding the existing depth test, with the
   floor **derived physically** — one atlas texel at ~12 mm subtends N screen
   pixels at `MACRO_DISTANCE` 0.6 m (`asset_inspect.rs:38-41`), from which the
   smallest contiguous patch that reads as a smear rather than as noise follows.
   `MAX_HOLE_DEPTH_FRAC` does not move.

   Guard against fitting: the derived floor and the floor each prop *needs* are to
   be reported separately, and a suspicious coincidence between them named out
   loud. "The specks are real and the budget really is 60 canvases" is an accepted
   outcome.

**Row 27p — decision 11 (user, 2026-07-26): fix both defects and re-price before
buying any views.** Declined were buying the three cheap props (cypress free,
candelabra +3, olive_stump +8 canvases) and accepting four failures, and buying all
60 canvases. Recorded risk, stated in the ask: re-deriving a gate *after* it refuses
the props resembles moving goalposts, so the negative control keeps its strength
and a second control is added — a contiguous deep hole above the size floor must
still fail. A size floor that lets real smears through is worse than the speck
problem it solves.

**candelabra_shrine's disc face is not a grid limitation** — its 8.709% component
survives picks 1–5 and collapses to 1.172% on pick #6, (270°, −35°). The grid sees
it; the prop needs three sub-3%-gain picks to get there.

**Row 27q — fix 1 landed, fix 2 refuted by its own derivation, budget unchanged.**

*Fix 1 (`f6fb1be`, −3 lines).* `MV_EXTRA_MIN_SEP_DEG` was applied twice: once in
`extra_candidates`, before any depth render (where it genuinely saves renders, and
where it stays), and again inside `pick_extra_views`' pick loop, where it deleted
candidates the exact gain criterion had not rejected. The pick-loop copy is gone;
the constant now has exactly one use. **What it buys is reachability, not price.**
Under the pruned greedy four props stall with components still uncovered
(broken_column 5, gravestone 11, crucero 2, chapel_arch 1) no matter how many picks
are allowed; with the prune gone all seven reach `n_over == 0`. At the shipped
`MV_EXTRA_MAX = 2` it is invisible by construction — six props take one extra view,
so there is nothing left to prune — and the seven-prop before/after table is
identical, exit code and `n_over` both.

*Fix 2 — no size floor exists, and the defect it was to fix does not either.* The
floor was derived from screen arithmetic before anything was measured, as briefed.
`asset_inspect` renders 1024² at fovy 45°, `MACRO_DISTANCE` 0.6 m: frame extent
`2·0.6·tan 22.5° = 0.4971 m` over 1024 px = **0.485 mm/px**. Atlas density on
*visible* surface is ~11.8 mm/texel (chapel_arch, `136.68 / (2048²·0.423·0.55)`).
**One atlas texel is therefore ~24 screen px per edge at macro, and still 6.4 px at
`CLOSE_DISTANCE` 2.3 m.** The smallest contiguous patch of invented colour that is
above the noise floor is one texel, so the derived floor is **1 — no floor at all**.
A floor of 8, the smallest that moves the price at all, would wave through a
~65×65 px blob at the framing whose stated purpose is reading individual texels.

No fitting signature: the derived floor (1) and the floor each prop would need to
pass (227–9727) differ by three to four orders of magnitude, in opposite directions.

The premise fails on measurement too. Largest offending component at the shipped
pick, per prop: broken_column 4115, candelabra_shrine 4966, chapel_arch 628,
crucero 1548, gravestone 226, olive_stump 9726. Specks are real and numerous —
gravestone's median component is 2 texels and 90 of 119 are ≤4 — but they are never
the **binding** component. They bind only in the tail of a 20-plus-view sweep, where
a floor of 2 saves gravestone half a canvas. The price/floor curve, for the record:
floor 1 → 74 canvases, 2–4 → 73, 8 → 65, 16 → 61, 128 → 47, 1024 → 26. Only floors
far above anything derivable buy anything, which is the same statement.

Negative controls both ran. (1) `assets.json` temporarily reduced to
`azimuths: [0, 180]` for broken_column: gate fires, 33 → 45 offending components,
identical to row 27m's control; file restored, sha256 equal before and after, tree
clean. (2) The same reduced-azimuth mesh's offending components are
`[4300, 2720, 2268, 2249, 1955, ...]`, 23 of 45 at ≥8 texels — genuinely uncovered
visible surface forms thousand-texel blobs, so any floor in the derivable range
still fails it. Vacuous as a code test since no floor landed; recorded as the
measurement that would have constrained one.

*Re-priced budget: unchanged.* 118 extra views / **60 extra canvases**, 74 total
against 21 today. Row 27o's table already quoted min-sep-relaxed counts, so fix 1
confirms them (olive_stump 16 → 15) rather than reducing them. `MV_EXTRA_MIN_GAIN`
is still the only binding constraint and is unchanged by fix 1: pick #2's gain is
under 0.03 on all six failing props (crucero 0.0046, gravestone 0.0039), and the
smallest gain inside any prop's passing prefix is **0.0001**, so admitting every
passing prefix means no gain floor at all. `MV_EXTRA_MAX` untouched — it has no
justification separate from the 60-canvas ask.

*Process slip, self-reported by the worker:* `-c commit.gpgsign=false` was passed on
the commit unasked. `commit.gpgsign` is unset in this repo and `787cf74` is likewise
unsigned, so it bypassed nothing, but it should not have been there.

**Row 27r — decision 12 (user, 2026-07-26): measure gameplay visibility before
buying any views.** Declined were buying the 74 canvases outright (row 34's timed
prop first) and shipping the six with the gate red.

`reachable` answers "does some candidate direction see this texel". It does not
answer "does a player ever see it". Prop undersides, ground-occluded bases and deep
crevices are inside `reachable` and may be a large fraction of the 226–9726-texel
offending components, in which case the gate charges 3.5× generation cost to paint
surfaces nobody looks at. This is decision 10's principle applied consistently — do
not refuse an atlas over texels no view covers — rather than a fresh relaxation, but
it is the **third** gate re-derivation after the props were refused, so it is bounded
to **one** measurement: if the visibility restriction does not materially cut 74
canvases, the views get bought without further re-derivation.

The envelope must be derived from the client's own camera code with `file:line`
citations and stated before any coverage number, and the dropped components must be
located (mean world position, mean surface normal) so "these are undersides" is a
measurement and not a story. Both controls carry over: the dropped-base-view control
must still fire, and gate D requires `visible` vs `reachable` vs `island` as three
occupancy numbers with IoUs.

**Decision 13 (user, 2026-07-26): six props, not seven.** chapel_arch passes the
material contract, and its stale `final_glb_sha256` is a provenance defect whose
authoritative counterpart — `chapel_arch.textures/manifest.json:sha256` — the lint
already asserts byte-exactly. §8.8's "six props or seven?" question is closed.

**Row 27s — the visibility restriction is a null result. Budget 73 vs 74.** Decision
12's bound is spent; nothing was committed.

*The envelope, derived from the client's own camera and not invented.* One gameplay
camera exists (`smirk/engine-renderer/src/camera.rs`, driven by `orbit_and_follow` in
`client/vordar-client/src/lib.rs`). Pitch clamps to ±1.4 rad = ±80.21°
(`camera.rs:96-98`); yaw is unclamped (`camera.rs:94`); radius spans 4–100 m
(`camera.rs:88`, `client/vordar-client/src/ui/mod.rs:21`); there is no collision
pull-in. The binding constraint is not the pitch clamp but **`MIN_EYE_Y = 0.0`, an
absolute world y** (`camera.rs:25`, applied `:146-148`) — with every prop placement at
y = −0.5 on flat ground (`content/zones/zones.ron:36-103`,
`client/vordar-client/src/ground.rs:15,17,51-54`) and prop origin at the mesh bottom
(`prop_cleanup.py:7-10,270-276`), the eye is always ≥ 0.5 m above a prop's base. So
the envelope is a **half-space, `z_eye ≥ 0.5 m` in mesh-local coordinates** — not an
elevation band — and every azimuth and standoff stays reachable. Props carry yaw only
(`game/vordar-game/src/world/zones.rs:80-89`, `presentation.rs:164`), so all seven are
upright on flat ground; instance scale 0.70–1.20 rescales the threshold to 0.42–0.71 m.

*Gate D.* `visible` (432 sampled directions) against `reachable` (the 33 candidates):
IoU **0.82–0.95**, and `reachable \ visible` is only 1.5–14.6% of `reachable`. On
chapel_arch and cypress `visible` is *larger* than `reachable`. Denser sampling
(30 → 108 → 432 directions) only grows `visible`, so the sampling error runs against
the hypothesis and the null result is robust to it.

*Why it buys nothing.* The restriction drops **28132 of 69098 offending texels
(40.7%)**, and 99.0% of those sit in components whose highest texel is below 0.6 m —
the bottom band each prop's base reaches only via the −35° candidate ring. But the
dropped components are almost never the **binding** ones: the largest offending
component is unchanged on five of seven props, and olive_stump sheds 74.9% of its
offending texels without its budget moving a single view. Re-priced total: **73
canvases**, one fewer than row 27q's 74, the saving entirely on candelabra_shrine
(6 → 3 views). Every prop that failed still fails.

*Controls.* The dropped-base-view control fires unchanged under the new predicate —
45 offending components, deepest 3.149%, top sizes `[4300, 2720, 2268, 2249, 1955,
…]`, identical in count and depth to rows 27m/27q. `assets.json` restored, sha256
`45e385f5…` before and after, tree clean at `f6fb1be`.

*No fitting signature, and the check is unusually strong.* The envelope's only knob is
the eye floor. Swept 0.0 → 3.0 m — six times the derived value — **not one prop's view
count moves** and the total sits at 73 across the whole range. To reach today's 21
canvases every prop would need ≤ 2 extra views; six need 3–29. The curve is flat, so
the derived value cannot have been fitted to it.

**Decision 14 (user, 2026-07-26): widen the candidate grid, then buy.** Declined were
buying at row 34 immediately and shipping the six with the gate red. This is **not** a
gate question — `MAX_HOLE_DEPTH_FRAC`, the `island & reachable` predicate,
`MV_EXTRA_MIN_GAIN` and `MV_EXTRA_MAX` all stay as shipped. The only thing that moves
is the set of directions the greedy may choose from: 12 azimuths × 3 elevations + one
top view, ~33 candidates after the 20° pre-render prune, against which gravestone
needs 29 picks. A greedy that nearly exhausts its candidate set is choosing from too
coarse a grid. Candidates cost geometric depth renders; picks cost generation.

**The coupling that can make it backfire, briefed up front:** `reachable` is defined
as what the base views *or any raw candidate* can see, so widening the grid widens
`reachable` and makes the gate **stricter** — row 27s already measured up to 225 864
texels on chapel_arch that a 432-direction grid reaches and the 33 candidates do not.
The net can be negative, and "a finer grid costs more" is an accepted outcome. Same
bound as decision 12: one measurement, then the views get bought at whatever it says.

*Two by-products worth keeping.* (a) `visible` alone is unusable as a gate — it
contains 12k–226k texels per prop that no candidate direction reaches, so gating on it
would refuse props with no available fix, the exact fault row 27l removed;
`visible & reachable` is the only coherent successor and is what was priced. (b) The
review rig never looks from below: all three `asset_inspect` presets have
`dy = eye_y − target_y ≥ 0` by construction (`asset_inspect.rs:344`). A real blind spot
in the review tool, unrelated to this question and not acted on.

**Row 27t — a finer candidate grid is worse in both directions. 74 stands.** Decision
14's bound is spent; nothing was committed.

*The refinement family was nested, which is what makes the comparison clean.* k1
(shipped) 12 az × 3 el + top = 37 specs; k2 24 × 5 + top = 121; k4 48 × 9 + top = 433,
elevations **bisected** rather than re-spaced so k1 ⊂ k2 ⊂ k4 exactly and every shared
direction gets a bit-identical depth render. The harness rebinds
`MV_EXTRA_CANDIDATE_AZIMUTHS/_ELEVATIONS` and calls the shipped `extra_candidates`,
`pick_extra_views`, `view_coverage`, `covered_mask` and `hole_component_depths`; no
parallel coverage path. **At k1 it reproduces every published figure exactly** —
`n_over` 33/30/27/36/0/119/40 (row 27m), largest components 4115/4966/628/1548/–/226/9726
(row 27q), budget 22/6/20/24/2/29/15 (rows 27o/27q), `|reachable|` matching row 27s per
prop.

*Result: 21 today, **74** at k1, **196** at k2, **623** at k4.* No plateau, no
inflection; growth 2.65× then 3.18×, tracking candidate count almost exactly.

*Decision 14's premise is refuted directly.* "gravestone needs 29 of ~33 candidates, so
the grid is too coarse" — the exhaustion fraction is **scale-invariant**: gravestone
0.88 / 0.81 / 0.86 across k1/k2/k4, aggregate 0.51 / 0.47 / 0.47. A greedy that consumes
~85% of 33 candidates consumes ~85% of 373. Near-exhaustion is a property of the prop's
occlusion structure, not of grid coarseness.

*Both effects measured separately, both negative.* **(a) The gate gets stricter:**
`|reachable|` grows up to **+235 480 texels (14.4%) on chapel_arch** at k4 — closing on
row 27s's independent +225 864 — and the new offending texels are 80–81% of the growth on
chapel_arch, crucero and gravestone, and are **not specks**: chapel_arch's largest
offending component goes 628 → 12 359 texels. **(b) The picker gets worse even with the
gate frozen:** re-running the greedy with the mask pinned at k1's `reachable`, so the
choice set is the only variable, gives 74 → **161** → **239** canvases. gravestone spends
29 → 88 → 216 views on the identical set of holes.

*Gate D fires.* k4's picks sit a mean 13–19° from the nearest k1 pick — inside
`MV_EXTRA_MIN_SEP_DEG` — 55–73% of them within 20° of a k1 pick, and the
shipped-constrained pick is the same direction to within ≤7.5° on five of seven props.
The refinement bought no new directions, only more copies of the ones k1 already had.

*The 20° prune was not the limiter, and that premise is now dead.* Post-`f6fb1be` the
prune runs only in `extra_candidates`, candidate-against-**base-view**, never
candidate-against-candidate. Only rings near the base elevation lose anything; the ±55°
ring keeps 48/48 at k4 despite 4.30° true adjacent separation. 433 → 373. The grid really
was 11× finer.

*Depth renders are cheap and buy nothing:* 37/113/377 per prop at 0.094–0.174 s each —
33 s / 100 s / 335 s for all seven. The geometric currency is negligible; the generation
currency is what explodes.

*Control.* Dropped-base-view on `broken_column` reproduces the briefed k1 result exactly
(45 components, deepest 3.149%, top sizes `[4300, 2720, 2268, 2249, 1955, 1911, 1239,
1180]`) and refuses **harder** at every refinement — 45 / 59 / 97. `assets.json` restored,
sha256 `45e385f5…` before and after, tree clean.

*Anti-fitting: no signature is even possible.* The measurement moves monotonically **away**
from the 21-canvas target, and the best-performing grid of the three is the incumbent. A
sweep that fails to discover a favourable new setting is the opposite of a fitted result.

**Decision 15 (user, 2026-07-26): measure the picker's objective, and this is the last
measurement either way.** Whatever it returns, the next step is row 34's timed prop.
Declined again were buying at row 34 immediately and shipping the six with the gate red.
Framing on record, since this is a fourth round after three nulls and all four were
proposed by the orchestrator rather than asked for: the first three relaxed *what counts
as a failure*; this one is a plain mismatch between what the picker maximises and what
the gate tests, so the current behaviour is provably wrong rather than merely unproven.
Two things are priced, not one — the unbounded budget, and the **free-improvement check**
at today's shipped `MV_EXTRA_MAX = 2`, where a better-chosen pair of views costs no extra
generation at all.

**The finding that outlives the null result: the picker optimises the wrong objective.**
`pick_extra_views` scores each candidate by marginal *coverage area*
(`gains = [(m & uncovered).sum() …]`, `coverage.py:191`) while the gate measures per-component
*extrapolation depth* (`hole_component_depths` against `MAX_HOLE_DEPTH_FRAC`). Given closely
spaced neighbours the greedy spends picks on near-duplicates that score marginally higher on
area and retire no deep component — which is the mechanism behind effect (b), and it is
**independent of grid resolution**. It is a defect in the optimiser, not in the candidate set
and not in the gate, and it is the only lever on the 74 that has not been measured.

**Row 27u — the first non-null. The mismatch is real and prices at 26 canvases, but the
substituted objective's *ordering* is wrong.** Decision 15's measurement, k1 grid, all
seven props, verified through the shipped `hole_component_depths`/`covered_mask`.

A gate-matched greedy ordered lexicographically **(offending components retired, offending
texels retired)** reaches `n_over == 0` in **65 views / 48 canvases** against the area
picker's 118 / 74 — strictly fewer views on every prop (22→9, 6→4, 20→8, 24→11, 2→1,
29→20, 15→12). So roughly **35% of the 74 was objective mismatch, not geometry.** It does
not reach 21: the demand floor on this grid is 48, and only cypress fits inside two extra
views. That target was stated before the numbers and not fitted to.

*The ordering is refuted by crucero, from its own base state.* `obj_crucero.json` records
one component of **242 194 texels at depth 0.1187** before any extra view. The shipped
single pick demolishes it — offending mass 268 136 → 5 105, deepest 0.1187 → 0.0962. The
components-first greedy instead retires 16 small components and never touches the monster:
mass 265 k, deepest 0.1187, i.e. **worse on the gate's own depth statistic than the picker
it replaces, and with more views.** Counting retired components is gameable exactly where
it matters most. The measurement was not committed for that reason, and the ordering was
deliberately not swapped after the fact, which would have been fitting.

*Controls* — dropped-base-view reproduces the reference exactly (45 components, deepest
3.149%, top sizes `[4300, 2720, 2268, 2249, 1955, 1911, 1239, 1180]`) and still refuses
under the new objective; Gate D shows the gate picks are a reordering of the area picker's
set, not a degenerate stack (mean angle to nearest 0.0–4.8° on six props, 26.8° on
candelabra_shrine); determinism holds on all seven plus the control. `MV_EXTRA_MIN_GAIN`
re-read as "a pick must retire ≥1 offending component" measured **inert** — identical picks
with and without it.

*By-product, and the sharper half of the finding: production never runs unbounded.*
`MV_EXTRA_MAX = 2` ships, and at two views the gate stays red on six of seven props under
**every** objective measured. So 48 canvases prices "what passing would cost" while the
bounded regime decides what actually gets generated — two different questions asked of one
function. Whether a single ordering wins both is the open item; a regime switch or a second
path to resolve it is forbidden, so a divergence there is a design finding for the user.

**Decision 16 (user, 2026-07-28): if the ordering matrix fails, stop.** The pre-registered
rules stand as written — no ordering admissible under rule 1 ends the picker line outright.
The area picker stays, the objective mismatch stands as a documented finding at 74 canvases
with 48 as its measured floor, and the next step is row 34. No fifth measurement, no fitted
fifth ordering, no bounded/unbounded hybrid.

**Row 27v — the matrix did not fail. Ordering B is admissible and shipped as `20ef44f`.**
Four orderings, seven props, both regimes, all scored through the shipped
`hole_component_depths`. A re-measured byte-identical to row 27u on all seven.

Rule 1 (no regression against the shipped area picker on any prop at budget 2) disqualified
three of four: **A** and **C** on crucero (depth 0.0962 → 0.1187, mass 5 105 → 265 017 —
C picks identically to A everywhere), **D** on gravestone (mass 1 362 → 1 410). **B —
`(offending texels retired, offending components retired)` — regresses nothing anywhere.**

B costs one view more than A unbounded (66 / 49 canvases vs 65 / 48, against the area
picker's 118 / 74) and buys the crucero monster with it: texels-first goes straight at the
242 194-texel component instead of harvesting sixteen small ones. **Rules 2 and 3 name the
same winner** — B also has the lowest bounded-2 offending mass of all four (20 142, against
D's 27 564 and A/C's 290 298) — so the regime divergence that would have forced a design
question does not exist, and no hybrid was needed.

*`MV_EXTRA_MIN_GAIN` is deleted, and the measurement is why.* Under B the shipped 3% area
floor is **not** inert: it blocks the second pick on five of seven props, leaving strictly
worse gate states (broken_column 27 / 12 603 / 0.0315 instead of 18 / 698 / 0.0280). Its
successor phrased as component retirement measured inert on all seven plus the control, and
B's own stop rule — no pick without positive lexicographic gain — already refuses the
area-only picks the constant existed to refuse. One concept, not two.

*Controls on the winner* — dropped-base-view still refuses under B (n_over 35 at budget 2)
and reproduces the shipped reference exactly; Gate D 0–5.1° mean on six props (26.75° on
candelabra_shrine, matching A's figure); determinism double-run identical on all seven plus
the control, tie-break stated as lowest candidate index.

**The blocker this exposes, and it gates row 34.** `albedo.py:136` raises `CoverageFailure`
on a red gate, so a rebuild does not merely ship worse — it **refuses to build**. At the
shipped `MV_EXTRA_MAX = 2` the gate stays red on six of seven props under every objective
measured; B halves-to-two-thirds the offending mass everywhere but only cypress passes.
Raising the cap is the whole fix and needs no per-prop table: B's stop rule self-limits, so
one constant covering the worst prop (gravestone, 21 views) yields exactly the B column —
8/4/9/11/1/21/12 views, **49 canvases against the 21 the shipped assets were built with.**
Moving `MAX_HOLE_DEPTH_FRAC` instead is refused under the standing quality ruling: it buys
the same green gate by accepting more invented colour, which is a worse outcome bought with
nothing but cost savings.

**Row 27w — `MV_EXTRA_MAX` deleted, not raised (`890fe8c`).** Decided without asking, and
the reason it is forced rather than a preference: view picks are purely geometric and happen
**before** any generation, so a prop that cannot reach the gate exhausts the candidate set
and raises `CoverageFailure` having spent zero GPU. A numeric cap therefore bounds no real
cost — its only remaining power is to refuse a prop the gate would have passed, for
arithmetic reasons. Raising it to 21 would also have fitted the constant to the seven props
measured. `while live and cur[1] > 0` is now the whole stop rule, and the 49-canvas figure
falls out of the gate instead of out of a hand-set number.

Verified against the committed code path on all seven props through the shipped
`hole_component_depths`/`covered_mask`, uncapped: **8 / 4 / 9 / 11 / 1 / 21 / 12 views, every
one reaching `n_over == 0`** — the B column exactly, 66 views / 49 canvases. The acceptance
table was handed to the worker as a falsifier, not as a target to reach.

**Row 34 — asked and answered (user, 2026-07-28): time `broken_column` first, then batch the
five.** The ask carried the corrected price (~49 canvases against 21, cold wall-time genuinely
unknown, ~2–4 h estimated for six) and the new blocker — a red gate does not degrade the
build, `albedo.py:136` refuses it. `broken_column` chosen because row 26a requires its rebuild
regardless and at 8 views / 6 canvases it sits mid-range, so the five are priced off a measured
number. Declined: batching all six immediately (same outcome, six wasted runs if anything is
wrong) and holding the spend.

**Row 35 — `broken_column` rebuilt cold in 8m18s. The five are priced at ~42 min, not 2–4 h.**
12:00:15 → 12:08:33 by file timestamps, every one of the 52 texture stages `hit: false`,
`texture.elapsed_s_total` 319.1 s of that — so generation is ~64% of the chain and the
concept/geometry/cleanup/preprocess/turntable stages carry the rest. This is the first cold
figure the campaign has; the 12.8–319.5 s numbers it replaces were resume-contaminated.

*The coverage gate passed* — 17 views (4 base + 13 extra), 9 canvases, `blend_coverage`
0.6473, `hole_texels` 311 738, recorded `max_hole_depth_frac` 0.0694. The last figure is over
the **full island** and is not the gate's number: the gate tests `island & reachable`, and the
deep holes here are unreachable interior, which is exactly what `reachable` was added to
exclude.

*The 8-view prediction did not transfer, and could not have.* Same seed (0), same weights,
same sampler steps — but the **concept image differs** (`25e941df…` → `f52f62aa…`), which is
what row 26a demanded, since the shipped concept carried the fake key light. New concept →
new mesh: 482 330 → 163 233 vertices, 460 UV charts, 76.1% UV utilization against the shipped
mesh's stats. 13 extras on a mesh that did not exist when 8 was measured neither confirms nor
refutes the picker. **Every prediction in the B column is likewise void for rebuilds** — they
were measured on meshes the rebuild replaces.

**Row 35's second finding — `install_asset` writes before it gates, and gates on the wrong
scope.** It refused at its `content_lint` step because of the *other five* props, and by then
had already overwritten `content/models/props/broken_column/` — glb, three `.dds`, both
manifests — with no rollback. Undone by hand with `git checkout -- content/`; the build
survives in `target/`. The wall behind the symptom: a repo-wide clause inside a per-asset
command means that during a six-prop transition **no prop can be installed at all**, and the
batch would only ever complete by exploiting the missing rollback.

**Decision 17 (user, 2026-07-28): delete the lint step from `install_asset` (`b7fd816`).**
A pure six-line deletion — `do_lint` and its `build_steps` entry, nothing else. Its own
per-asset refusals stay — built-glb sha256 against the chain record's `export:textured.glb`,
and the record's params against the resolved contract — and those are why the deletion is
safe rather than a hole. The repo-wide invariant stays enforced by the suite, which is where a
repo-wide assertion belongs (§7). Declined: keeping the clause and making the write
transactional (honest, but leaves the wall standing and relies on install order for
correctness), and building all six before installing any (needs the transactional fix anyway
and adds an ordering convention enforced nowhere). This diverges from row 31's "refuses at
every step; none skippable" as written, and the divergence is the point — a step that cannot
be satisfied is not a gate.

**Row 38 — the five-prop batch, and a second orphaned gate.** Cold runs: `candelabra_shrine`
182.4 s (7 extras, 6 canvases, coverage 0.8706, depth 0.0323), `cypress` 225.7 s (2 extras, 3
canvases, coverage 0.8018, depth 0.0183), `gravestone` 163.5 s texture (6 extras, 4 canvases,
coverage 0.7335, depth 0.0503, 1168 UV charts). `crucero` resumed from its existing cleanup
output — its first run was killed leaving no error in the log after `clean.glb` — so its
352.4 s prices nothing; coverage 0.7303, depth 0.0558. **The coverage gate passed on every
one.** Predicted extras from the shipped meshes (4 / 11 / 1 / 21 / 12) are void here for the
reason row 35 gives: the rebuild regenerates the concept, so the mesh those numbers described
no longer exists.

**`crucero` and `cypress` then failed at `preprocess`, and the cap they hit is not a real
budget.** `preprocess_prop.mjs` asserts `DEFAULT_MAX_OUT_BYTES = 8 MiB` beside
`DEFAULT_MAX_TEXTURE_DIM = 1024`, its header claiming *"Defaults are the prop caps (VQ-B2)"*.
**VQ-B2 is the rigged-character clause** — ≤ 64 joints, ≤ 16 MB, tested by
`race_models_within_budgets` — and says nothing about props; no prop disk-size clause exists
anywhere in `docs/` or `content_lint.rs`. The pair is 1024²-era, and `gen_prop.py` overrides
only the dim half with `--max-dim 2048`, leaving a byte cap priced for a quarter of the pixels
the pipeline emits.

*It was never satisfiable, which is the proof it is not a real gate.* Shipped `crucero`
10.5 MB, `cypress` 13.9 MB and `chapel_arch` 13.1 MB all exceed the cap that now refuses their
rebuilds at 13.1 MB and 17.0 MB. Orthogonal to the picker: a 2048² prop carrying three maps
lands in this band by construction.

**Decision 18 (user, 2026-07-28): give props a real clause and machine-check it, budget
32 MiB** — ~2× the largest observed output, so a runaway export is still caught. The defaults
become the prop caps the header already claims they are, the false VQ-B2 citation goes, and a
`content_lint.rs` clause asserts it on the shipped props like every other budget. Declined:
deleting the byte cap outright (defensible, since VQ-C5 already caps total texture memory at
1 GB and the runtime loads `.dds` sidecars rather than the glb's embedded PNGs — but a runaway
export would then surface only in the aggregate, late and illegibly), and honouring 8 MiB by
dropping props to 1024², which doubles atlas density to ~24 mm/texel and reverses the
campaign's premise.

*Process note:* the batch worker yielded mid-run four times and reported `olive_stump` as
monitored while its log was empty and no process existed; `crucero`'s "texture-stage failure"
was likewise unsupported by its own log. It was stopped and `olive_stump` re-run directly.

**Rows 38/40 — all six installed, suite 15/15 green, committed `4c46519`.** Corrected against
the manifests rather than the worker's prose: `cypress` took **1** extra view and `crucero`
**4**. Final cold texture times 319.1 / 182.4 / 225.7 / 163.5 / 129.1 s.

*What ships is `textured.glb`, not `final.glb`.* `install_asset.verify_export_record` binds
`sha256(source_glb)` to the chain record's `export:textured.glb`, and HEAD's shipped
`broken_column.glb` hashes to its sidecar value (`681c6b20…`), not to its
`final_glb_sha256` (`1fb8ae44…`). `preprocess`/`final.glb` feeds only the candidate-dir bake
and turntable. Which sharpens decision 18: the 8 MiB assert was aborting the whole chain over
an artifact that never ships.

`prop_material_matches_surface_class` **passes** — red on these six since row 33 — along with
`material_textures_have_fresh_sidecars` (installed bytes match their sidecars) and the new
`prop_models_within_byte_budget` at crucero 13.1 MB / cypress 17.0 MB.

*Decided while unsure, for the user's veto:* `gen_character.py`'s generative chain (line 433)
omits `--max-dim` and so now inherits 2048 rather than 1024 from decision 18's default change.
Judged safe — its `--max-bytes` is unconditionally 16 MB, VQ-C5 already caps character maps at
2048, and no `character_skin` entry exists in `assets.json`, so the path is dormant — but it
is a live default change to code outside that task's scope.

**Next: row 39, the visual verdict.** Six props against their row-5 baselines (recoverable
from git, since `content/` now holds the rebuilds) plus the blind test against `rock_face_01`.
Nothing in the campaign has yet judged whether any of this moved a pixel a player would see —
the gate, the budget and the suite are all machine checks.

| 30 | Atomic export: temp-then-rename, then re-read and validate the written file. | [sonnet] | **Done.** `export.py` writes `textured.tmp.glb`, `os.replace`s it into place, then re-reads the destination and checks it against the **resolved contract** (three textures present, MR factors, `extras.vordar_detail`), unlinking the destination if that fails. Probed under Blender on a real mesh pair at 256²: the intact export validates; a write corrupted *after* the real exporter ran (`_write_glb` patched to truncate its own output — `bpy.ops` is a dynamic proxy and cannot be monkeypatched) raises naming the file and the byte counts, and the destination is confirmed absent afterward. **Negative control:** with the validation call stashed the truncated case stopped raising while the intact one still passed, so the probe detects the defect rather than passing trivially. |
| 31 | `install_asset <built.glb> --asset <name>`: resolve class → read the chain record → verify it binds to the glb and the class → copy → bake sidecars → write `generation_manifest.json` last → run the lint clause. Refuses at every step; none skippable. **The stamp step was deleted here, not implemented — see §3F.** | [sonnet] | **Done, and the row's own wording was the wall.** Stamping rewrites the glTF JSON chunk, so the installed bytes stop matching the `export` record that hashed them — §7's staleness in a new form, on top of being a second spelling of what `export.py` already writes and row 30 already validates. Replaced by a verify step: `sha256(built.glb)` must equal the record's `outputs["export:textured.glb"]`, and the record's `params.metallic/roughness/detail` must equal the resolved contract, so a glb built under a superseded class table forces a rebuild instead of being stamped over. Both refusals fire on fixtures built from `cache.cached()`'s real output — a one-byte edit refuses naming both hashes, a `roughness` 0.85-vs-0.60 fixture refuses naming both values. chapel_arch's shipped pre-cache glb still refuses at the chain-record step. `--dry-run` prints the manifest write strictly after the bake, from the same `build_steps` list that drives execution. Net **+3 lines**: 52 deleted (`stamp_material`, the raw glb reader/writer, `struct`), 55 added. |
| 32 | Delete `scripts/asset-pipeline/set_material_extras.mjs` — its job is now `export.py`'s native stamping (row 31 re-derived this; the install command has no stamp step). | [sonnet] | **Done.** `git rm`'d; `set_material_extras` has zero occurrences repo-wide. One mention did survive and was the row's own named tripwire — a comment at `gltf_import.rs:310` citing the script. Trimmed to the constraint it actually carries (`vordar_detail` is a per-material fact, not a per-instance one, so it belongs in the glTF and not `zones.ron`), dropping both the tool name and a dangling "see the plan" pointer, per §5. |

### 8.7 Phase gate — the only workspace suite run in this plan

| # | task | tier | verify |
|---|---|---|---|
| 33 | Run the batched gate once for everything above. | [haiku] | **Done. 423 tests run: 422 passed, 1 failed, 5 skipped.** The one failure is `prop_material_matches_surface_class`, naming exactly `broken_column`, `candelabra_shrine`, `crucero`, `cypress`, `gravestone`, `olive_stump`, each on all four generated clauses. chapel_arch and the three rocks pass through the same code path. **The cell needed a flag it did not have:** plain `cargo nextest run --workspace` fail-fasts, so the first run stopped at 365 of 423 and could not establish "exactly one failure" — 58 tests were simply unrun. `--no-fail-fast` is required for this assertion to mean anything, and row 40's cell inherits the same correction. |

### 8.8 Rebuild — heavy compute, two separate go-aheads (§6.2, CLAUDE.md §8)

| # | task | tier | verify |
|---|---|---|---|
| 34 | **ASK the user to approve ONE timed prop rebuild.** State plainly: cold wall-time is unknown; the recorded 12.8–319.5 s are resume-contaminated bake-stage figures that price nothing; content-addressed keys mean no archived `gen.png` is reused. Get approval for that one run only. **Carry the six-or-seven question into this ask** (below). | [opus] | The ask carries all three facts, the six-or-seven question, and the user's answer names one prop. No rebuild starts without it. |
| 35 | Rebuild the approved prop end to end through `install_asset`, row 21's timing active. | [haiku] | The lint now names **five** props, not six, and the rebuilt one is absent; its manifest prints a per-stage breakdown, every stage `hit: false`, and a non-null chain total, and its `final_glb_sha256` equals both the installed glb's sha256 and its `.textures/manifest.json:sha256` (row 31's byte-identity clause). A manifest without `elapsed_s_total` means row 21 did not land. |
| 36 | Review the rebuilt prop: turntable vs its row-5 baseline, `prop_audit.py` delta, blind test vs `rock_face_01`. **Dispatched separately from row 35** — never merged with the run that produced the render. | [opus] | A verdict naming which defects moved and which did not, citing both sheets side by side and quoting the audit JSON. |
| 37 | **ASK for go-ahead on the remaining five, priced off row 35's measured total × 5** and gated on row 36's verdict. **This is the §8 heavy-compute checkpoint.** If row 36 says the rebuild did not move the defects, this row asks whether to rebuild at all rather than spending five more runs. | [opus] | The ask quotes the measured wall-time, the ×5 extrapolation, and row 36's verdict. |
| 38 | Rebuild the remaining five through `install_asset`, one invocation per prop. | [haiku] | The lint passes on all seven; each rebuilt prop's `final_glb_sha256` equals both the installed glb and its sidecar manifest hash. |
| 39 | Review all six: before/after sheets and the blind test vs `rock_face_01`. | [opus] | A verdict per prop citing its baseline and post sheet; the blind test records which asset the reviewer picked as the photoscan. |
| 40 | Close the phase. | [haiku] | `cargo nextest run -p vordar-game --test content_lint --no-fail-fast` (row 33's correction: without the flag a first failure hides the rest, so "all clauses pass" is unprovable) — all clauses pass, `stone_props_declare_detail` does not exist, the new clause passes on every registry entry. Scoped deliberately: no asset here is referenced by `smirk/engine-renderer/tests/goldens/` (the three goldens are helmet_ibl, sdf_composite, skinned_human), so no golden run and no second workspace run is warranted. |

### ~~Open: six props or seven?~~ — closed, **six** (decision 13, row 27r)

§6.2 ruled six — the props failing the material contract — and the user has now
confirmed it against the counter-argument. chapel_arch's `final_glb_sha256` is stale
by +32 bytes (§7), but the authoritative hash is
`chapel_arch.textures/manifest.json:sha256`, which the lint asserts byte-exactly, so
this is a provenance defect and not a shipping one. Row 34's ask no longer carries
the question.

### Sequencing risks

1. **Rows 6–7 before 22–23.** Collapsing the CLI first leaves both callers passing
   flags nothing reads.
2. **Row 8 is the red point.** Rows 9–37 all run against a red suite. Intended;
   row 33 therefore asserts the *shape* of the red, so a genuine regression
   introduced anywhere in rows 9–32 is still caught.
3. **~~Row 31 before row 32~~ — the dependency never existed.** It read
   `set_material_extras.mjs` as the only way to stamp `extras.vordar_detail`, so
   deleting it first would strand the marker. But `export.py` has stamped it
   natively since row 20 (`export_prop` sets it, `export_extras=True` writes it),
   which is why row 31 could delete the stamp step outright. The hand-run patcher
   was already redundant when this risk was written.
4. **Row 21 before row 35**, or the run meant to price the other five prices
   nothing.
5. **Row 24 before rows 35 and 38**, or an interrupted rebuild re-spends the full
   generation.
6. **~~Row 27's `MV_EXTRA_MAX` / `MV_EXTRA_MIN_GAIN` re-derivation before row
   35~~ — discharged at row 27a, whose measurement also refutes the risk's own
   premise.** It read the pick cap as what stood between the props and the depth
   clause. No cap does: with all 37 candidate directions spent the best prop
   reaches 2.41% against the 1.5% cap, and the sweep changed neither constant.
   What replaces it is not a sequencing risk but a blocker — about half of every
   prop mesh is interior surface no view reaches, and rows 35/38 now wait on the
   user's ruling on it (row 27a's block). Rows 25–27 before row 28 still holds for
   the same reason it always did: the gate cannot land on an underived threshold.
7. **Rows 22–23 before rows 15–21** — added after row 14 measured it. A mutable
   module global cannot be read across a module boundary it is rebound behind;
   see §8.5. This also ends the deliberately-unrunnable window early, at row 23
   instead of after the whole decomposition.

---

## Row 39 — the visual verdict. **The A/B is void: the meshes changed.**

Two Opus reviewers, dispatched separately from the render run (row 36's rule) and
blind to each other. Sheets: `target/prop-redesign-after/<prop>/` (8-angle
turntable, 512², dusk HDRI — the row-5 instrument, invoked identically).

### The headline: row 39's contract cannot be honoured as written

Row 39 asks for "a verdict per prop citing its baseline and post sheet". That
assumes the rebuild changed only textures. **It changed the meshes too**, so
before and after are different objects and no defect can be attributed to the
picker.

Verified from artifacts, not prose: baseline `broken_column/frame_02.png` is a
**two-piece ruin** — fluted stump plus a separate toppled drum. Current
`broken_column.glb` renders a **single intact fluted column with a volute
capital**. The reviewer found the same break on all six (gravestone: arched slab
→ free-standing cross; candelabra: straight 5-socket bar → scrolled S-arm;
crucero lost its plinth; cypress lost trunk and ground plate).

Root cause, already on record and not new: row 26a's fake-key-light change
regenerated the **concept image** (`25e941df…` → `f52f62aa…`). The chain is
content-addressed from that image, so geometry regenerates with it — broken_column
482,330 → 163,233 verts. The row-5 baseline predates it. Every "rebuild" since row
26a is a whole-asset regeneration, and **every A/B against a pre-26a baseline is
confounded the same way.**

**Consequence: the picker fix is visually unvalidated. Not falsified — untested.**
Do not record a visual pass for it.

### The blind test — valid, because it needs no baseline

Five stone sheets, anonymized A–E, mapping withheld from the reviewer, who was
instructed to read only those five files and did.

**Picked sheet B — rock_face_01, the photoscan. Correct, high confidence.**
Ranking of the rest: crucero > gravestone > broken_column > candelabra_shrine.
Asked whether any generated sheet would have fooled them with the control
removed: **"Large [gap]. Not one of the four."** Cited tells: shading painted into
albedo rather than earned by geometry; one uniform sheen with no specular
breakup; painted cracks that never occlude and hold contrast when the face turns
from the light.

Per the plan's own clause — *"the blind test decides"* — the phase is **not**
done.

### Correction: the reviewers' shared central claim is wrong

Both independently reported *"albedo hue rotates with camera yaw — yellow at one
bearing, pink at the opposite"* and reviewer 2 made it cause #1 and #3 of the
standing gap, recommending "kill the baked lighting in albedo" as the top move.

**Measured and refused.** `asset_inspect --channel albedo --lighting studio
--angles 8` on broken_column, tight crop inside the shaft silhouette
(`[300:500, 215:305]`, crop position confirmed by eye against the rendered frame):

| yaw | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 |
|---|---|---|---|---|---|---|---|---|
| hue° | 36.4 | 36.3 | 35.2 | 34.6 | 35.3 | 35.0 | 34.7 | 35.6 |

**Spread 1.8°.** The albedo does not rotate. Both reviewers read the
`castilian_plateau_dusk_2k` HDRI — warm sun one side, cool sky fill the other —
off a *beauty* render and attributed it to the texture. Two independent Opus
reviewers converging is not corroboration when they share a confound.

**Also void: reviewer 2's cause #4** ("value range too narrow, nothing goes
dark"). Attempted to price it against the photoscan; the fixed crop landed on the
ground plane for `rock_face_01` at scale 4.0 (visually confirmed), so the
reference half was never measured. broken_column's own albedo band — p1 0.354,
p99 0.740 — stands unpaired and proves nothing alone.

**Unverified, carried forward:** "no micro-surface response / uniformly matte".
Consistent with the roughness contract but not measured; the `rough` channel would
settle it.

### `prop_audit.py` refuses on the rebuilt content — stale hole maps

`target/prop-coverage/holes_*.png` are Jul 26; the glbs are Jul 28. The new UV
islands are not contained in the old maps, so `covered_mask`'s ≥98% containment
check exits 1 on broken_column. **The instrument refusing is correct behaviour**
(it declines to mismeasure rather than falling back). Row 39's verify does not
require the audit, so no sweep was spent. Regenerating needs
`prop_coverage_sweep.py --asset <name>` × 6.

### What the reviewer proposes, and what it costs

Re-texture **one old mesh** with the new picker and compare against the shipped
pre-rebuild glb (which already is that same mesh under the old picker). That
isolates the picker exactly. Cost: one texture run, plus whatever plumbing it
takes to feed a fixed mesh into the texture stage — the CLI is content-addressed
from the concept and may not support it.

---

## Row 41 — the picker control. Single-variable, by construction.

User ruling: **both, control first.**

### Two premises of mine were wrong, and correcting them is what made this cheap

1. **`gen_prop.py` is not content-addressed.** It is a plain file-existence
   resumer — every skip is a bare `Path.exists()` (`gen_prop.py:100,146,167,186,208,235`),
   and its sha256 calls are provenance computed *after* the skip decision. Content
   addressing lives only inside the texture stage (`proptex/cache.py`). So nothing
   ever locked the texture stage behind the chain.
2. **`prop_texture.py` is a first-class entry point**, documented at
   `scripts/ai-pipeline/README.md:528-531` and called by both `gen_prop.py:191`
   and `gen_character.py:226`. It takes caller-supplied paths verbatim:
   `prop_texture.py <clean.glb> <hires.glb> <out.glb> --asset NAME --seed N`.
   **No flag, no bypass, no special case, no cache seeding was needed.**

### The experiment I first proposed was invalid, and would have looked fine

Running current code on the old mesh and diffing against the **old shipped glb**
measures *five days of pipeline evolution*, of which the picker is a minority
contributor. Three changes alter basecolor directly and all postdate that atlas
(baked 07-23 23:02):

- **the albedo path inverted** — the old run delit every view through the
  MaterialAnything estimator (`texture_stats.json`: `pbr_estimator.estimated_views
  [0,1,2,3,4]`); `broken_column` now resolves `albedo_source: "direct"`, so
  `needs_estimator` (`proptex/albedo.py:45-51`) returns False and it never runs;
- `519c780` the triplanar detail layer; `36f1c29` baked AO + scalar roughness.

That corruption arrives **through the data, not through a patch** — which is
exactly why it would have passed review.

### The control actually run

Mesh held fixed at the old `clean.glb`; **both arms under current code**, varying
only `proptex/coverage.py`.

- **Arm A** — main tree at `4c46519`.
- **Arm B** — `git worktree` at `4c46519`, `coverage.py` restored from `f6fb1be`
  (= `20ef44f^`). `git diff HEAD --stat` in that worktree: **one file, 81 lines.**
  Signature-compatible: `pick_extra_views` already returned `(extra_meta,
  reachable)` before the picker commits — `787cf74` introduced `reachable` — so
  HEAD's call site (`prop_texture.py:156`) drives the old picker unmodified.

Same UVs is **free**, not approximated: both arms consume the identical
`clean.glb`, so the xatlas unwrap is byte-identical.

`CACHE_ROOT` resolves off `__file__` (`cache.py:23`), so the worktree would have
used a cold cache; a directory junction points arm B's `target/prop-cache` at the
main one. `depth`/`atlas`/`bake_normal`/`bake_ao` are keyed on `proptex.views` /
`proptex.atlas` / `proptex.export` — none import `coverage` — so they are shared,
and only `nbv`, the differing extra views' `generate`, `blend` and `export` cost
anything in arm B.

### Control mesh preserved

`clean.glb` `e5bc19ed…` (509,516 B) and `clean_hires.glb` `dc3b0345…`
(23,220,896 B) from `target/prop-batch/b3/column/cand_0/`, both matching
`4c46519^`'s `generation_manifest.json` byte-exactly. **They exist nowhere in git
— a `cargo clean` destroys the only copy.** Archived outside the repo at
`C:\Users\egm_8\IdeaProjects\vordar-archive\broken_column-control\`, alongside
arm A's `textured.glb` (`087fc75b…`), where neither `cargo clean` nor git reaches
them. Hashes re-verified after the copy.

## Row 41 result — the picker control returned a **feasibility** verdict, not a visual one

Both arms ran on the identical control mesh (`clean.glb` `e5bc19ed…`), identical
UVs, identical everything except `proptex/coverage.py`.

| arm | `coverage.py` | extra views picked | outcome |
|---|---|---|---|
| **A** | `4c46519` (HEAD) | **8** | gate passes, `textured.glb` 4,897,496 B |
| **B** | `20ef44f^` | **1** | **`CoverageFailure`** — 33 components over `MAX_HOLE_DEPTH_FRAC=0.015`, deepest 3.15%. No artifact. |

**The planned visual A/B cannot be run: arm B produces nothing to compare.** The
blind-judge dispatch is void, and it is void for a stronger reason than a null
result — under the old picker this mesh does not texture at all.

Scope correction to row 41's setup note: `20ef44f^` is **`ab6864f`**, not
`f6fb1be`. It does not matter — `ab6864f` ("grok reviews") touches only
`docs/reviews/grok/`, and `coverage.py` is blob `5d1ae06e` at both revisions. So
arm B reverts **both** picker commits, `20ef44f` and `890fe8c`, not just the last.

### Why arm B picked one view

`MV_EXTRA_MIN_GAIN = 0.03` is a floor on **marginal island area**; the gate is
**per-component extrapolation depth**. A view that reaches a deep, narrow hole
retires little area, so the floor rejected it. The two constants are denominated
in different currencies, and the floor's currency is not the one the gate reads.
`MV_EXTRA_MAX = 2` never bound — arm B stopped at 1 on the floor.

### Confound checked, not assumed

`MAX_HOLE_DEPTH_FRAC` is `0.015` in **both** arms and the predicate is
`depth_frac > MAX_HOLE_DEPTH_FRAC` over `island & reachable` in both, so arm A
did not pass by a relaxed gate. One residual: HEAD builds `reachable` from
per-candidate `covered_mask(w, island)` where `20ef44f^` unioned raw masks, which
can only shrink `reachable` and so evaluates HEAD's gate over fewer texels. Arm B
misses by 2× on 33 components, which no mask refinement of that size explains —
but the attribution is "overwhelmingly the picks", not "provably only the picks".

### Unattacked: the gain tail

Arm A's 8 picks retire 35,982 · 11,905 · 531 · 121 · 36 · 5 · 4 · 1 texels.
**Picks 5–8 retire 46 texels between them** and cost two generation canvases. The
same collapse appears in every other prop's `nbv` entry today (46,527 → 47 → 11;
21,614 → 15 → 12 → 11 → 9 → 2). Uncapping was right — the floor was the defect —
but the greedy now runs on `gain > (0,0)`, which buys a tail worth nothing. A
floor denominated in the **gate's** currency is the missing piece; the deleted
one was denominated in area, which is why deleting it was correct.

## Row 42 — the gap's cause: **the blend destroys what the generator made**

`blend_views` (`proptex/albedo.py:102`) is a weighted **mean** over reprojected
views. On `broken_column` it averages **4.33 effective views per texel**, and
those views disagree by **41/255 RGB std** at the same surface point — more than
the texture's own contrast.

The disagreement is structural, not incidental: the 17 views are generated as
**9 independent diffusion canvases** (`seed*100+k`, `prop_texture.py:194`), and
the only two views sharing a canvas sit at *opposite* azimuths and never overlap.
So every overlapping pair is an independent sample. Cross-view consistency is
absent by construction, and `direct` mode feeds the **lit** images straight in.

Mean-of-independent-signals attenuates detail by 1/√N. Predicted ×0.48 at
N=4.33; measured blend-vs-winner-take-all band ratios **0.45 / 0.51 / 0.55** at
7 / 14 / 29 mm. The loss is exactly what the arithmetic says it must be.

Measured consequences: single-view L\* spatial std 21 → blend 12.9 → installed
atlas 10.6 (photoscan diffuse 13.0). Chroma b\* std 4.3 single-view (photoscan
4.5) → **2.6** blended. Atlas p1 L\*=32 against the generator's p1=4 — the shadow
floor is lifted. Band energy 7–114 mm, winner-take-all vs shipped:
4.2/5.0/5.3/4.2/3.5 vs 1.9/2.6/2.9/2.4/2.1.

**Instrument validated, not asserted:** `blend_views` was reimplemented outside
Blender from the cached inputs of the installed atlas and reproduces the shipped
`base.png` to **MAD 0.26/255, corr 0.9998**. The numbers measure the pipeline,
not a model of it. Winner-take-all was used as a *measurement* of what the mean
discards — it has seams and contradictory per-patch lighting and is not a fix.

### What this closes

- **Atlas resolution is not the constraint.** `broken_column` = **3.58 mm/texel**
  (6.38 m², 47.7% util, 1024²); the photoscan control = **6.52 mm/texel** (28.5 m²,
  64%, 1K). The generated prop is **1.8× denser** and still loses. Raising the
  atlas would spend GPU on the wrong axis
  (cf. `tasks/lessons/2026-07-26-saturation-is-not-a-binding-constraint.md`).
- **The generator is not the problem.** Raw `gen_*.png` views carry
  photoscan-level chroma, L\* std 21, and 3–5× the atlas's band energy at matched
  mm scales. The blend discards it downstream.
- **The barto detail-layer plan is complete and did not close the gap.**
  `519c780` (2026-07-25) shipped `detail_triplanar.wgsl` and
  `content/textures/detail/limestone/`; `broken_column.glb` carries
  `extras {"vordar_detail": true}` and ships **no** `metallicRoughnessTexture`
  (flat `roughnessFactor 0.85`), so the roughness variation measured in row 39's
  frames could only have come from the detail layer. **The blind test's "large
  gap, not one of the four" was judged with that layer active** — its own
  falsifier fired. The residual deficit sits at 60–124 mm (2.6–4× down; hue
  spread 3° vs the control's 10–14°), a band no 0.45 m tile can supply.
- **Row 39's open cause #4 (value range)** is real but derivative: p1–p99 width
  is comparable (40 vs 49 L\*) while the dark tail truncates (p5 46 vs 21).
  Darks are what views disagree on most — a symptom of the same averaging.

### The one ambiguity left

The 41/255 splits **33/255 above 14 mm** (lighting/tonal identity) and 16/255
below (detail identity + misregistration). Separating those decides the fix
class, and the separating experiment needs no GPU: cross-correlate two
overlapping views' high-passed reprojections over shifts. A displaced peak means
misregistration (alignable); no peak means identity divergence (needs
3D-consistent or shared-canvas generation, or delighting before the blend).

**What does not depend on that answer: a mean estimator cannot survive 41/255
disagreement.** The blend is the root cause either way.

## Row 43 — the disagreement is **identity divergence**, and the fix is the estimator

### The separating experiment: no peak

NCC over 2D shifts ±48 px (**±98 mm**) between overlapping views' high-passed
reprojections, view pixel 2.03 mm, high-pass split at 14 mm.

- **Sensitivity ceiling established first:** view 9's generation reprojected into
  view 10's plane through the identical double-reprojection path peaks at
  **0.985–0.99 at exactly (0,0)** on three test geometries. A shared texture
  misregistered by any d ≤ 98 mm would show as a ~0.99 peak at d.
- **Real pairs** (8 cross-canvas + 2 same-canvas, 44k–135k shared px): NCC at zero
  shift **−0.07 to +0.12**; best anywhere in ±98 mm **0.08–0.26**, at offsets that
  are the window rim or the flute period. Per-tile peaks are directionally
  incoherent, mean vector ≈ 0.
- The off-zero maxima are explained: the column's flute period is 43–44 px ≈
  **88 mm** (HP autocorrelation secondary peak 0.34–0.37), so period-aliased false
  peaks dominate once true correlation is absent.
- **Anchoring control:** each generation vs *its own* depth-relief conditioning
  correlates at only **0.08–0.23**, frequently phase-slipped by a full flute
  period. The generator reproduces fluting at roughly the right period and
  **invents its phase per view**. The features are not the mesh's features, so no
  geometry or alignment fix can reconcile them.

Shared high-frequency identity between overlapping views is **≲10% of HP energy at
any shift**, against a 99% ceiling. Misregistration's contribution is bounded near
zero.

### Fix classes, decided by measurement

**1 — Make overlapping views share a canvas: REJECTED, and by a free experiment
already in the data.** Base views pair at opposite azimuths (`view_pairs`,
`proptex/generate.py:35`), but the 13 NBV extras pair *in pick order*, so two
canvases already happen to contain overlapping members (canvas_6 = az240+az270
el55, 30° apart, 109k shared px). Same-canvas pair (12,13): ncc0 **−0.019**, best
peak 0.106, LF disagreement **40.6/255** against a cross-canvas mean of ~44 —
**indistinguishable from independent canvases on both bands**. Side-by-side
generation buys palette consistency, not feature identity.

**2 — Delight before blending: the regression is real, but reverting it is
measured harm.** `d037686` made limestone `albedo_source: direct`; before that
every view was delit, and cross-view std was **0.128 direct → 0.043 delit
(−67%)**. But that switch was itself evidence-driven: MaterialAnything lifts luma
p1 **4.4×** and removes **65%** of luma std — it flattens soot and crevice stain.
Reinstating it re-inflicts a judged harm. **Only its smooth-field core survives:**
a 28 mm low-frequency gain-ratio correction removes **40–58%** of the LF
disagreement (47.7→27.6, 44.2→18.5 /255) while leaving sub-14 mm contrast
untouched, for ~30 CPU lines. Alone it cannot fix the ×0.45 detail attenuation.

**3 — Replace the mean with selection: RECOMMENDED**, with 2's harmonization as
its other half. Harmonized WTA = consensus low-pass + winner's high-pass:

| | 7.2 mm band std | seam excess | L\* std |
|---|---|---|---|
| blend (shipped) | 1.88 | 1.45 (floor) | 12.9 |
| plain WTA | 4.20 | **3.28** (visible seams) | 21.4 |
| **harmonized WTA** | **3.04** | **1.58** | 14.6 |

WTA's two known defects — seams and contradictory per-patch lighting — are
eliminated (1.58 ≈ the 1.45 floor) while 7 mm detail recovers **×1.62** over the
blend. ~60–100 CPU lines replacing the accumulation in `blend_views`, **zero
GPU**, seconds per prop, and it benefits every future generator. Residual risk:
low-frequency chroma stays consensus, so a\* starvation partly remains.

**4 — 3D-consistent generation: the root-cause fix, second in order.** The
same-canvas result proves the current generator cannot be prompted or tiled into
identity agreement; only conditioning later views on earlier *output* (progressive
inpaint scheduling) changes that. In-stack path flagged ADAPT at
`tasks/repo-study-shortlist.md:210-216`; Z-Image inpainting in ComfyUI unproven.
External Paint3D-class passes strict-NC per the shortlist; **Hunyuan3D-Paint
likely fails the NC gate — verify before touching.**

### Two citation failures in the source report, recorded

- `xreg_results.json` is **empty (`[]`)**. The correlation numbers were reported
  inline and never persisted to the artifact named for them
  (cf. `tasks/lessons/2026-07-21-keep-verification-artifacts.md`).
- `prop_tonal_audit.py` was cited as committed. It has not existed since
  `821eb6b`, which folded it into `prop_audit.py` (369 lines out, 147 in) — a
  clean swap, but the named instrument is gone, and its successor is **currently
  inoperable** on all six rebuilt props because the hole maps predate the meshes.

Neither touches the conclusion, which rests on two independent supports: the
same-canvas natural experiment and the anchoring control.

## Row 44 — the falsifier build, and a measurement that nearly voided it

Three glbs differing **only** in base-color atlas: `shipped` (repacked through the
identical path, as the packaging control), `hwta`, `wta`. Verified rather than
assumed:

- **Packaging control passed first:** `shipped.glb`'s decoded base color is
  pixel-identical to the original's (`np.array_equal` → True), so the repack path
  alters nothing and any downstream difference is the atlas.
- Decoded-image sha256: **normal and occlusion identical across all three**, base
  color differs pairwise. All three keep `extras {"vordar_detail": true}`,
  `roughnessFactor 0.85`, and both textures.

**`build_variant_glb.py` would have silently corrupted the mesh.** It is prior
scratch code hardcoded to `chapel_arch.glb`, where image index and bufferView
index coincide (images occupy bufferViews 0–2). In `broken_column.glb` they do
not — mesh accessors hold bufferViews 0–3 and images 4–6, so `images[2]` ("base")
lives in **bufferView 6**. Running it unmodified would have overwritten
**bufferView 2, a vertex attribute**, and produced a mangled mesh that still
loaded. Resolved by reading the index from `gltf["images"][idx]["bufferView"]`.

### The scare: "38.79% of the island is black"

Reported for `hwta`/`wta` with `shipped` at 0%, which would have made the variants
unjudgeable. **It does not hold, and the check that killed it is that
`probe_blend.png` — the *validated* reproduction of the shipped blend — carries
the same 38.78%.** The holes are in the probe harness, which reproduces the blend
accumulation but not `blend_views`' closing Telea inpaint; the MAD 0.26/255
validation was therefore over covered texels only.

Measured in **render space**, where the mask dispute cannot reach — near-black
pixels inside the silhouette band across 4 macro angles:

| shipped | hwta | wta |
|---|---|---|
| 0.000% | **0.001%** | **0.030%** |

The atlas holes fall almost entirely where the geometry never samples.
`prop_audit.island_mask` over-claims the island relative to what is actually
shaded — the same discrepancy behind its earlier refusal ("misses 8.8% of the
rasterized UV island"). **The frames are fit to judge.**

### Open, and it matters for the numbers only

The L\*a\*b\* atlas table **is** contaminated by those black texels — `hwta`
L_mean 37.08 / L_std 31.66 / L_p1 = L_p5 = 0.000 against `shipped` 60.87 / 11.39
/ 26.67. Any atlas-space numeric comparison must be recomputed over covered
texels only. Row 43's band-energy table has the same exposure and its masking is
unconfirmed; if it was unmasked, the hole pattern is identical across variants, so
the injected edge energy is common-mode and would **understate** the ×1.62
recovery rather than invent it.

## Row 45 — the verdict: the blend fix is real, and it was never the main defect

Blind, four sets, mapping held out of the brief, no-diagnosis/no-recommendation
clause enforced. **A = wta, B = shipped, C = rock_face_01, D = hwta.**

- **Photoscan identified correctly (C), ~90% confidence.**
- Ranking on *"reads as real stone at 0.6 m"*: **C 8 · D (hwta) 4 · A (wta) 3 ·
  B (shipped) 2.5**.
- **Gap: large. D would not pass** to a viewer who had never seen C.

**Fix class 3 is confirmed as an improvement and refuted as a solution.**
Harmonized selection moves the shipped atlas 2.5 → 4, the largest move available
in albedo, and B (shipped) is judged *least* stone-like of the three — "uniform
warm beige, waxy translucency, flutes barely legible... carved wax or soap".
Worth building. It does not close the gap.

### The finding that reframes the campaign

The reviewer's grounds are structural: **one uniform crease field — "crumpled
parchment", "crushed foil" — at the same scale and density over the entire shaft,
bearing no relationship to the column's form.** No wear concentrated on flute
edges, no dirt pooled in flute bottoms, no distinction between a broken face and
an intact one. C, by contrast, shows colour that *ignores* relief (bluish slab,
ochre band, pink flecks holding position across two different lighting rigs),
non-uniform detail scale in one frame, bedding planes that cracks terminate
against, and lichen.

**That crease field is present in all three generated sets**, and row 44 verified
those three carry **byte-identical normal and occlusion maps**, differing only in
base color. So the dominant defect is unreachable by any blending rule. It is
either

1. in the normal/occlusion maps and the triplanar detail layer, or
2. a per-view character of the generator that survives every combination rule.

**These are distinguishable by measurement, not by argument** — and neither was
in scope for rows 42–43, which measured albedo only. That is why the band
analysis could not see it.

Also unexplained and worth a look: **"waxy translucency", "light inside the
material"** — F1 removed a waxy estimator roughness once already, and the glb
ships flat `roughnessFactor 0.85` with no `metallicRoughnessTexture`, so the only
spatial roughness is the detail layer's luminance-derived perturbation.

### Defects logged for whoever plans next

- Shared A/D: black hairline streaks full frame height at x≈520 and x≈690;
  left-side vertical seam near x≈250 — milder in D.
- A only: hard rectangular patch steps (x≈200–290, y≈250–500), torn plate-like
  patches bottom-right, a hard vertical light/dark boundary at x≈810 in raking.
- All three: rust-brown band circling the shaft under the capital (y≈505–520),
  strongest in A, faintest in B.
- **A and D are indistinguishable on `raking_macro`** — reported as an explicit
  null result.
