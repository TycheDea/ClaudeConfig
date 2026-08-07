# Hi3DGen Fork Reworks — 2026-07-28

Companion to `audit-hi3dgen-2026-07-28.md` (same anchor conventions: `fork:` =
`C:/tools/Hi3DGen/Hi3DGen`, `hub:` = the StableNormal torch-hub snapshot,
unprefixed = vordar-repo relative).

## Ideal end state

The fork produces solid, single-shell, floater-free meshes conditioned on
multiple views, exposed through a clean installable headless API, with every
extraction and guidance knob measured rather than inherited. The vordar-side
script is CLI + gates + manifest; all upstream-shaped knowledge lives in the
fork we own.

## Findings (implementation order)

Queue (single cross-file sequence, mirrored from the fixes file):

> **~~finding 1~~ → ~~finding 2~~ → ~~finding 3~~ → ~~finding 4~~ → ~~finding 5~~ →
> ~~finding 6~~ → ~~finding 7~~ → ~~finding 8~~ → ~~finding 9~~ → ~~finding 10~~ →
> ~~finding 11~~ → ~~finding 12~~ → ~~finding 13~~ → ~~finding 14~~ →
> ~~finding 17~~ → ~~finding 15~~ → ~~finding 16~~ → ~~rework 1~~ →
> ~~finding 18~~ → ~~finding 19~~ → ~~finding 20~~ → ~~finding 21~~ →
> ~~finding 22~~ → ~~finding 23~~ → ~~finding 24~~ →
> ~~rework 2~~ → ~~rework 3~~ → ~~rework 4~~ → ~~rework 18~~.**

Rework 2 closed 2026-07-29, negative verdict, no code change beyond what
step 2 already landed: `docs/reviews/hi3dgen/ab-multiview-2026-07-29.md`.
Multi-view conditioning is not adopted; `--view`/`--mv-mode` stay plumbed,
opt-in, and dormant, not wired into `gen_prop.py`/`gen_character.py`
defaults.

This file's findings 24 and 25 (orientation-robust fidelity metric;
same-subject back/side noise floor) are **parked 2026-07-30, user ruling**:
no pending A/B consumes them since multi-view was rejected, so they wait for
the next orientation-sensitive experiment rather than entering this queue.
Campaign closed 2026-07-30 — aggregate regenerated at `1532b9d`, lesson-mining
pass done (2 lessons accepted: `tasks/lessons/2026-07-30-*`).

The findings numbered in *this* file (10–17, 19) are discoveries from rework
execution and sit outside that mirrored queue; they are struck here. Where the
two numberings collide, this file's own are written "this file's finding N".

Parked: rework 5 (gate: finding 24's measurement shows extraction is a
dominant wall-clock share).

cypress is the one regression — its boundary edges per face rise 40% — and it is
the prop whose deleted share is smallest (10.5% of raw). Not chased; recorded.
olive_stump's deleted count jumps 52%, the largest move on the board: a gnarled
stump has deep bark crevices no orthographic view can reach, and the strip's own
premise is that what the baker cannot reach is not worth carrying. That premise
is now load-bearing on a prop where it was not before, and is worth a look when
olive_stump is next reviewed in engine.

Implementation notes worth carrying: the worker found the facing condition in
this note's own framing (`n·(−d) > 0`) sign-ambiguous against
`atlas.view_weight`, and resolved it by reusing `view_weight`'s literal
expression on `mv_camera_rig`'s own `v["f"]` rather than re-deriving the formula
— the right call, and the reason the two stages cannot drift. `prop_cleanup.py`
gains a **required `--asset`**; `gen_prop.py` and `gen_character.py` thread it
through, and a `kind="downloaded"` asset is refused outright since it declares no
azimuths.

*Step 8's gate is not writable, and the reason is not missing data.* The gate was
specified to catch "a hollow-shell regression". Lead (1) established that the
hollow shell is architectural and permanent — every prop is one, always — so
there is no regression for it to catch. The fallback of gating raw watertightness
fails on its own measurement: the raw main island is closed on only 2 of 7 props
(0, 0, 4, 12, 42, 68, 366 boundary edges), and its face fraction runs 0.658
(candelabra_shrine, whose arms are genuinely separate bodies) to 1.0. Calibrating
a fail-loud threshold across that spread from seven passing samples and zero
failures is the guessed band `~/.claude/CLAUDE.md:14` forbids. **No threshold is
installed.** What would make one writable is a corpus of failed generations to
put a floor under; until that exists the corrected stats are the deliverable and
they gate nothing.

Post-weld-deletion baseline, all seven props
(`target/prop-solid-validation/r1s78/`):

| prop | raw main boundary edges | raw main face fraction | components | boundary edges / main face |
|---|---|---|---|---|
| broken_column | 0 | 0.9908 | 7 | 0.0784 |
| candelabra_shrine | 0 | 0.6581 | 6 | 0.0395 |
| chapel_arch | 4 | 0.9996 | 109 | 0.1471 |
| crucero | 12 | 0.9995 | 8 | 0.0135 |
| cypress | 366 | 0.9114 | 3 | 0.2839 |
| gravestone | 68 | 1.0 | 12 | 0.0249 |
| olive_stump | 42 | 0.9951 | 38 | 0.2079 |

*Step 7 found a live defect and changed the constant's shape.* Clean→hires
deviation, measured at 20k/80k/320k surface samples per prop (p99 stable to 3e-4
across that refinement, so the sample count is not deciding the answer):
`BAKE_MAX_RAY_DISTANCE_M = 0.03` **clips on cypress**, which needs 0.0454 at p99
and 0.0582 at p99.9 — roughly 1% of its normal-bake texels have been falling back
to flat. candelabra_shrine needs 0.0111. A flat bound raised to cover cypress
hands the smallest prop five times the reach it needs, and the spread is not
noise: deviation tracks prop size because the triangle budget does not — every
prop decimates to the same 15,000. Replaced by `BAKE_RAY_DIAG_FRACTION = 0.006`
of the prop's own bbox diagonal, added to the cage extrusion at the call site;
every prop clears its own p99.9 by ≥1.6×. Overshoot is safe by construction —
Cycles takes the first hit, so extra ray length can only turn a miss into a hit,
never corrupt one.

| prop | bbox diag | p99 | p99.9 | needed (p99.9 + cage) | supplied |
|---|---|---|---|---|---|
| candelabra_shrine | 1.853 | 0.00068 | 0.00105 | 0.0111 | 0.0211 |
| gravestone | 1.906 | 0.00184 | 0.00264 | 0.0126 | 0.0214 |
| olive_stump | 2.047 | 0.00400 | 0.00553 | 0.0155 | 0.0223 |
| broken_column | 2.317 | 0.00211 | 0.00324 | 0.0132 | 0.0239 |
| crucero | 4.247 | 0.00431 | 0.00629 | 0.0163 | 0.0355 |
| chapel_arch | 7.877 | 0.01188 | 0.01884 | 0.0288 | 0.0573 |
| cypress | 13.414 | 0.03541 | 0.04822 | 0.0582 | 0.0905 |

**Decided autonomously under the standing "best outcome" instruction, and worth
the user's eye:** the approved plan's step 7 said to keep a single metre constant
and scale it by 1.5 if the measurement demanded it. Measurement made that *form*
indefensible, not just that value, so the constant became size-relative — the
idiom `prop_cleanup.py` already uses for its own tolerances. Reversible; neither
scope nor licensing.

The deviation spread is itself a symptom: the flat `--tri-budget 15000` is what
makes a 12 m cypress and a 1.2 m stump deviate by 52×. The per-asset triangle
budget already queued as a quality finding is the root fix, and this constant
should be re-derived once it lands. Deriving it now was still correct — cypress
is clipping today.

Artifacts: `target/prop-solid-validation/r1s78/` (per-prop `cleanup.json`,
`bake_ray_derivation.json`) and `r1s78-noweld/` (the A/B arm).

Done 2026-07-29 (finding 24, fork `c7389f5`, vordar `1d5c681`). A `perf_counter`
around the extractor call, surfaced as `SparseFeatures2Mesh.last_extract_s` and
recorded as `elapsed_s.extraction` in the per-candidate manifest — a
**sub-interval** of `elapsed_s.geometry`, not a sibling, so the two must never be
summed. Confirmed populated on a CPU replay; the number that decides rework 5's
gate is the extraction share under the normal GPU path, which the next routine
candidate run reports. Rework 5 stays parked until then.

### 5. GPU iso-surface extraction — PARKED
- **Gate:** activate only if audit finding 24's measurement shows CPU marching cubes is a dominant share of per-candidate wall time under batch mode (where it can otherwise overlap the next candidate's GPU work).
- **Evidence:** `fork:hi3dgen/representations/mesh/cube2mesh.py:136-147` — 68 MB GPU→CPU round trip, single-threaded skimage over 17 M voxels, GPU idle meanwhile. This is the fork's license-driven replacement for FlexiCubes; any GPU alternative must be permissively licensed — nvdiffrast/kaolin/FlexiCubes remain banned by the standing ruling.
- **Ideal:** Extraction is not a meaningful share of candidate wall time.
- **Gap:** Unmeasured; parked without a queue position until the gate is evaluated.
- **Suggestion:** If activated: evaluate permissively-licensed GPU marching cubes implementations; otherwise rely on batch-mode overlap and strike this rework.
- **Outcome:** `7/10`
- **Cost:** `7/10`
- **Path:** gate first (audit finding 24) → strike or plan.

### 7. `--normal-resolution` never reaches the denoiser: both normal pipelines process at 768 internally
- **Evidence:** Measured while running audit finding 13's A/B. `hub:hubconf.py`'s `Predictor.__call__` resizes the input with `resize_image(img, resolution)` and then calls `self.model(img, match_input_resolution=…, **kwargs)`, where `kwargs` carries `num_inference_steps` only — `processing_resolution` is never passed. Both pipelines fall back to their own `default_processing_resolution`, which is `768` in the constructor signature of `hub:stablenormal/pipeline_yoso_normal.py:159` and `hub:stablenormal/pipeline_stablenormal.py:246`, and is not overridden by either checkpoint's `model_index.json`. So at `--normal-resolution 1024` the conditioning image is resized to 1024, downsampled by the pipeline to 768, denoised at 768, and upsampled back — the denoiser never sees more than 768 px in either arm. Corroborating measurement: with one instrument over all cells, the r768 arm carries *more* top-octave energy than r1024 (candelabra 0.0306 vs 0.0060, crucero 0.0112 vs 0.0019), the opposite of `ab-conditioning-2026-07-28.md`'s ordering — consistent with LANCZOS upsample ringing rather than with resolved detail.
- **Ideal:** `--normal-resolution` sets the resolution the normal is actually denoised at, so the knob the queue adopted a default for is the knob it measured.
- **Gap:** Finding 12's adopted `--normal-resolution 1024` default currently buys only a different resample chain, not a higher-resolution prediction. The genuine 1024 prediction has never been run, so the knob's real quality ceiling is unmeasured; the 768 cap is also a candidate cause of the full predictor's speckle at higher step counts (`ab-normal-model-2026-07-28.md`).
- **Suggestion:** Pass `processing_resolution` through from `prop_hi3dgen.py` — either by calling the pipeline directly instead of via `Predictor.__call__`, or by carrying the fix in the fork/hub snapshot. Then re-run the 768-vs-1024 A/B, since its adopted conclusion rests on cells that never differed in denoising resolution. Check VRAM: 1024 denoising is ~1.8x the pixels at the stage that already peaks the process.
- **Outcome:** `7/10` — a quality knob the queue believes it has already tuned, and does not have.
- **Cost:** `4/10` — small plumbing change, plus a re-run of finding 12's A/B under §8.
- **Path:** plumb `processing_resolution` → confirm the manifest resolution matches the denoiser's actual working size → re-run the 768/1024 grid on the same two subjects.
- **Status (2026-07-28):** CONFIRMED — `--normal-resolution` never reaches the
  denoiser; both arms of every past grid denoised at 768. Still open: the Path
  above (plumb `processing_resolution` through, then re-run the 768/1024 grid
  with the angular instrument and ≥2 repeats per cell). The instrument dispute
  raised alongside this finding is settled: the radial-spectrum top-octave
  reading in `ab-conditioning-2026-07-28.md` was measuring resample artifact,
  not denoised detail, and is corrected there; the angular-domain suite
  (mean/p95 angular difference, detail-pixel angular gradient, speckle
  fraction) is the instrument for future normal-map comparisons. The default
  stays `--normal-resolution 1024` meanwhile — it is the strictly cleaner
  resample chain around the same 768 denoise, independent of this finding's
  outcome — and is not a defense against the re-run above.

### 9. `prop_audit.py` can't measure 6 of 7 generated props: coverage-sweep data is stale against current UV islands
- **Evidence:** Measured while implementing audit finding 20 (`height_m`). Running `python scripts/ai-pipeline/prop_audit.py` (unmodified, no code involved from finding 20) aborts immediately: `holes_broken_column.png island misses 8.8% of the rasterized UV island (must be >= 98% contained)`. Per-asset re-runs show the same failure for `candelabra_shrine` (22.0%), `crucero` (30.8%), `cypress` (34.3%), `gravestone` (19.5%), `olive_stump` (7.6%) — every generated prop except `chapel_arch`, which passes clean. `covered_mask`'s containment check (`prop_audit.py`) compares the glb's current, freshly-rasterized UV island against `target/prop-coverage/holes_<name>.png`, a Blender-baked coverage map from an earlier `prop_coverage_sweep.py` run. `prop_cleanup.py` gained an interior-face strip at `1f32bbe` (before finding 20's changes), which removes faces and therefore reflows the xatlas unwrap; the six affected props' `holes_*.png` predate that topology change, `chapel_arch`'s manifest post-dates it.
- **Ideal:** `target/prop-coverage/` reflects the UV layout of the props currently on disk, so `prop_audit.py` can measure every shipped prop, not just whichever one happens to have a fresh coverage bake.
- **Gap:** Six of seven generated props are unmeasurable until `prop_coverage_sweep.py` re-runs against current geometry. Finding 20's per-metre density re-baseline could only be demonstrated on `chapel_arch` (and the downloaded `rock_face_01` reference) as a result.
- **Suggestion:** Re-run `prop_coverage_sweep.py --asset <name>` for the six stale props (or all seven, for a clean baseline) so `target/prop-coverage/coverage.json` and `holes_*.png` match current geometry, then re-run `prop_audit.py` for the full density re-baseline finding 20's Path calls for.
- **Outcome:** `6/10` — unblocks measuring 6/7 generated props; no other consumer of `target/prop-coverage/` is affected.
- **Cost:** `3/10` — `prop_coverage_sweep.py` is a Blender multiview render pass (§8 go-ahead), ~7 props.
- **Path:** go-ahead for the render pass → `prop_coverage_sweep.py` per stale asset → `prop_audit.py` full sweep → compare against the pre-fix, fictional-height density numbers already on record from finding 20.

### ~~18. Per-asset triangle budget (user-decides): the flat 15,000 over-serves small props and starves large ones~~
- **Evidence:** `scripts/ai-pipeline/prop_cleanup.py`'s `--tri-budget` defaults to a flat 15,000 for every prop, and `gen_prop.py` never overrides it. Measured through the pipeline itself on all seven props at 5k/15k/30k/60k/120k (35 runs, `target/prop-solid-validation/tribudget/`, p99 clean→hires deviation at 80k surface samples per run): at the shipped 15,000 the deviation normalized by bbox diagonal spans **0.000369 (candelabra_shrine) to 0.002633 (cypress), a 7.1× range**. The same measurement is what forced `BAKE_RAY_DIAG_FRACTION` to become size-relative — this is that defect's root cause rather than its symptom.
- **Ideal:** Every prop is decimated to the budget its own geometry needs to hold a chosen deviation, so the triangle budget buys the same visual fidelity everywhere instead of an accident of prop size.
- **Gap:** The budget is uniform and the quality is not. candelabra_shrine currently gets 4× more fidelity than it needs while cypress gets less than half; nobody chose that split.
- **Suggestion:** Per-asset `tri_budget` in `content/models/assets.json` (alongside `height_m`, same `_GENERATED_FIELDS` treatment audit finding 20 describes), threaded through `gen_prop.py`. **Do not derive it from a formula.** Measured budget needed for a uniform deviation, against prop size:

| prop | bbox diag | hires area | needed @0.0015 | tris/m² implied |
|---|---|---|---|---|
| candelabra_shrine | 1.85 m | 2.3 m² | 4,993 | 2,140 |
| gravestone | 1.91 m | 5.0 m² | 7,837 | 1,577 |
| olive_stump | 2.04 m | 6.5 m² | 18,383 | 2,832 |
| broken_column | 2.32 m | 7.1 m² | 11,170 | 1,574 |
| crucero | 4.25 m | 15.5 m² | 9,531 | 615 |
| chapel_arch | 7.88 m | 82.5 m² | 13,756 | 167 |
| cypress | 13.44 m | 202.9 m² | 24,182 | 1,467 |

  Neither diagonal nor surface area predicts it: olive_stump at 2.04 m needs
  nearly twice crucero at 4.25 m, and the implied triangle density spans 17×.
  The driver is geometric complexity — gnarled bark against a smooth cross —
  which no size formula carries. The budget is therefore a per-asset
  measurement, not a computed field.
- **THE USER'S DECISION — the deviation target.** It is a free parameter and a visual one, so it is not the implementer's to pick. Totals across the seven props, against today's 105,000:

| target p99/diag | total tris | vs today | what changes |
|---|---|---|---|
| 0.0020 | 66,322 | −37% | cypress and olive_stump improve; candelabra_shrine drops 15,000 → 4,051 |
| 0.0015 | 89,852 | −14% | every prop at or better than today's worst; candelabra_shrine → 4,993 |
| 0.0010 | 138,350 | +32% | every prop at or better than today's best except candelabra_shrine |
| 0.0005 | 292,235 | +178% | diminishing — candelabra_shrine already measures 0.000014 at 120k |

  Recommendation: **0.0015**. It is the only row that is both cheaper than today
  in total and no worse than today on any prop, because the flat budget's waste
  on the small props pays for the large ones. The reason it still needs the
  user's eye is that it cuts candelabra_shrine to a third of its triangles on the
  strength of a distance metric, and whether that reads at gameplay framing is
  not a headless judgement.
- **Outcome:** `6/10` — uniform fidelity per triangle spent, and it removes the size dependence that `BAKE_RAY_DIAG_FRACTION` now works around.
- **Cost:** `2/10` — the measurement is already done and kept; the change is a registry field plus threading. Re-deriving `BAKE_RAY_DIAG_FRACTION` afterwards is part of it.
- **Path:** user picks the target → write the per-asset budgets from the measured curve (never a formula) → thread `tri_budget` through `gen_prop.py` → re-run the seven props → re-derive `BAKE_RAY_DIAG_FRACTION` against the new deviation spread → in-engine look at candelabra_shrine and olive_stump before the budgets are considered settled.

### 21. `mv_ab_metrics.py`'s planned single `cv2.fillPoly` call over all faces cancels a closed mesh's silhouette instead of union-filling it
- **Evidence:** `plan-rework2-multiview-conditioning-2026-07-28.md` finding 3's Suggestion specified rasterizing every face with one `cv2.fillPoly(canvas, polys, 255)` call. Implementing it exactly and running the finding's own analytic test (`trimesh.creation.box(extents=[1, 2, 3])` at az=0, el=0) gave a fill fraction of 0.035 inside the bbox, not the expected ≥0.999. Isolated repro in the Hi3DGen venv (`cv2` 4.11.0): a single triangle alone fills its bbox correctly (25806 px for a 130x390 half-box rectangle); two *exactly* overlapping triangles passed to one `cv2.fillPoly` call together fill only 909 px, regardless of matching or opposite vertex winding. `cv2.fillPoly`'s multi-contour fill is an edge-parity (even-odd-style) algorithm, not a union: overlapping contours in the same call cancel. For any closed/watertight manifold, a straight line through the interior along the view axis crosses the surface an even number of times (front face + back face, at minimum) at every interior silhouette point, so this cancellation is not specific to the axis-aligned test box — it is the generic case for any closed mesh rasterized this way, at any azimuth (confirmed off-axis: az=5/el=0 and az=1/el=1 on the same box both still returned only ~3000-3700 px instead of a filled silhouette).
- **Ideal:** The instrument's rasterizer computes the true union of all face projections regardless of how many surfaces overlap at a pixel, so it works for both closed test primitives and open/hollow raw Hi3DGen output.
- **Gap:** No single-call `cv2.fillPoly` invocation over a full face list has union semantics; the finding's Suggestion assumed one did.
- **Suggestion:** Already applied in the landed `scripts/ai-pipeline/mv_ab_metrics.py`: paint each face with its own `cv2.fillConvexPoly` call in a loop, so every face independently ORs 255 into the canvas (idempotent, order-independent, no cancellation). Benchmarked at ~3.8s per 512x512 view on the 768,804-face `chapel_arch_e2e/cand_0/raw.glb` fixture — acceptable for this instrument's occasional-use A/B role, but worth revisiting (e.g. bounding-box-limited rasterization, or a vectorized scan-conversion) if it is ever driven at a tighter loop cadence (a per-candidate sweep across many props, or a finer azimuth scan step).
- **Outcome:** `8/10` — without this fix the instrument silently reports near-zero silhouette coverage for any closed mesh (including its own analytic self-test), which would have made every later multi-view A/B reading on this yardstick meaningless.
- **Cost:** `0/10` — already implemented and tested as part of landing finding 3; nothing further required unless the per-view runtime becomes a bottleneck for a future sweep.
- **Path:** none outstanding — recorded for provenance; revisit only if a later step's call volume makes the per-face-loop runtime a bottleneck.

### 22. `mv_ab_metrics.py` measured silhouettes in the wrong frame: `trimesh.load` keeps glTF Y-up, but `view_axes` assumes Blender's Z-up
- **Evidence:** `view_axes` mirrors `proptex/views.py`'s `mv_view`, which runs inside Blender and is correct there because Blender's glTF importer converts glTF Y-up to Blender Z-up on load. `mv_ab_metrics.py` instead loads the `.glb` with `trimesh.load`, which keeps the raw glTF Y-up frame, so the mirrored camera math treated the mesh's Z axis (depth) as "up" and looked down its real height axis. Measured on `target/mv-ab/det-nf1/cand_0/raw.glb` against `target/prop-solid-validation/chapel_arch_e2e/cand_0/concept_rgba.png` (extents X 0.9997 / Y 1.0008 / Z 0.2551 — Z is wall thickness, Y is the arch's real height): as-is `fitted_yaw=0, best_iou=0.3076` (a squat wide slab); converting vertices `(x, y, z) -> (x, -z, y)` before rendering gave `fitted_yaw=155, best_iou=0.8807`, matching the concept's pointed gothic arch. The existing analytic test (`trimesh.creation.box(extents=[1,2,3])`, rendered directly with `render_mask` in the same call) is structurally blind to this class: it never crosses the glTF/Blender frame boundary `trimesh.load` introduces, so it validates the camera math against its own convention regardless of which "up" axis is right.
- **Ideal:** `mv_ab_metrics.py`'s silhouettes are computed in the same frame `proptex/views.py`'s Blender-side renders use, so the module's own claim of apples-to-apples comparison with the ControlNet-depth stage is actually true.
- **Gap:** No frame conversion existed between `trimesh.load` and `view_axes`; the module docstring and `view_axes`'s docstring asserted convention parity with `proptex/views.py` that only holds inside Blender.
- **Suggestion:** Already applied. A single `load_mesh(path)` owns the conversion — `trimesh.load` plus `(x, y, z) -> (x, -z, y)`, returning a mesh already in the frame `view_axes` assumes — and is the only load path in the module; `main()` and the tests all go through it, so the string `-v[:, 2]` occurs exactly once in the workspace. No flag is threaded through the render path and no as-is code path is kept. Both docstrings (module header, `view_axes`) state the Z-up assumption and the glTF-Y-up-vs-Blender-Z-up fact. Added `test_gltf_y_up_box_renders_tall_not_wide` to `scripts/ai-pipeline/test_mv_ab_metrics.py`: builds a box tall in glTF Y (`extents=[1, 3, 1]`), exports it to `.glb`, and drives the CLI as a subprocess so the assertion runs against the shipped entry point rather than an in-process helper call, asserting the rendered silhouette's height/width aspect exceeds 2. Reverting the conversion was verified to fail this test (measured aspect 1.02) and to fail the pre-existing `test_yaw_fit_recovers_grid_azimuth` the other direction; restoring it passes all three. Putting the conversion inline in `main()` was the first fix attempted and was rejected: it forced the same two lines into the test's own load site, which is how a convention silently acquires a second copy.
- **Outcome:** `9/10` — every prior `mv_ab_metrics.py` reading (including `target/mv-ab/noise_floor.json`'s `iou_front` floor, now recomputed to 0.8806-0.8807 at `fitted_yaw_deg=155`) was measuring the wrong silhouette; any future multi-view A/B on this instrument would have compared a real render against a spuriously bad geometric baseline.
- **Cost:** `0/10` — already implemented, tested, and the noise floor recomputed; nothing further required.
- **Path:** none outstanding.

### 24. Silhouette IoU cannot resolve front from back — an orientation-robust fidelity metric is needed
- **Evidence:** `docs/reviews/hi3dgen/ab-multiview-2026-07-29.md` (rework 2 step 8). `fit_yaw`'s argmax is degenerate: across the 18-candidate multi-view A/B, the gap between IoU at the fitted argmax and IoU at (argmax + 180 deg) runs 0.0014-0.1053, with 7 of 18 candidates below 0.01 — the same order as the cross-arm effects being claimed (0.0037-0.0081). All three `pilgrim_monk` `sv` candidates fit ~180 deg off (confirmed visually: the "front" render shows the monk's back), which inverted step 7's reported "MV beats sv on iou_front" into a front-vs-back comparison. This is the third instrument in this domain to fail on a front/back or panel-viewpoint distinction that turns out to be semantic rather than geometric (finding 23, `panel_matte_ab.py`, made the same discovery for concept-sheet panels: no silhouette or pixel statistic separates "the back of this object" from "the front of this object again").
- **Ideal:** A fidelity metric for a multi-view A/B (or any future orientation-sensitive comparison) resolves which side of a near-symmetric silhouette it is looking at, so cross-arm deltas are not confoundable with which of two tied peaks the yaw fit happened to pick.
- **Gap:** No orientation-robust instrument exists in this pipeline. Silhouette IoU is blind to it by construction — a standing figure's front and back silhouettes are near-identical by anatomy, and an arch or a stump reads similarly from opposite sides too.
- **Suggestion:** Correlate rendered camera-space normals against Hi3DGen's own predicted `normal.png` (already written to every candidate directory) to break the 180-degree tie. The silhouette fit already localizes the peak pair (argmax and argmax+180), so only those two candidates need normal correlation, not a full azimuth sweep — 2 renders per candidate, not a re-run of the whole scan.
- **Outcome:** `6/10` — unblocks any future orientation-sensitive A/B in this pipeline (multi-view conditioning, concept-sheet turnaround checks) that silhouette IoU cannot currently adjudicate.
- **Cost:** `3/10` — two camera-space normal renders per candidate through the existing `proptex.views`/`mv_camera_rig` machinery, plus a correlation function; no new GPU generation.
- **Path:** implement normal-map correlation in `mv_ab_metrics.py` at the argmax and argmax+180 candidates → validate on the 7 already-ambiguous candidates from this A/B (known ground truth: `pilgrim_monk` sv is back-fitted, MV arms are front-fitted) → only then would a re-run of the multi-view A/B be worth the GPU time.

### 25. Same-subject noise floor covering `iou_back` / `iou_side`
- **Evidence:** `docs/reviews/hi3dgen/ab-multiview-2026-07-29.md` (rework 2 step 8). `target/mv-ab/noise_floor.json`'s determinism probe only ran `--front`, so `iou_back` and `iou_side` have no measured noise floor at all — every value for those two metrics in both `ab.json` files was reported raw, with no claim rule applicable. Back/side fidelity is the rework's actual question and was never adjudicable by metric as a result; the verdict rests entirely on visual review instead (finding 24's front/back degeneracy separately voided `iou_front` too).
- **Ideal:** A same-subject noise floor exists for `iou_back` and `iou_side`, so a future A/B can claim a back- or side-fidelity effect the way this one claimed `vertex_count`.
- **Gap:** No repeat-candidate data has ever been collected with `--back`/`--side` mattes supplied to `mv_ab_metrics.py`.
- **Suggestion:** 3 same-seed repeat candidates per subject (mirroring `noise_floor.json`'s existing 3-repeat design), run through `mv_ab_metrics.py --front --back --side` so `max_pairwise_abs_diff` is computed for all three IoU axes, not just front. Do on at least one prop and one character subject, since `pilgrim_monk`'s floor is currently borrowed cross-subject from chapel_arch.
- **Outcome:** `5/10` — without it, no back/side metric claim is possible for any future multi-view (or other orientation-sensitive) A/B in this pipeline.
- **Cost:** `2/10` — ~2 min GPU per repeat candidate, 6 candidates total (3 per subject) if both subjects are covered; reuses the existing `noise_floor.json` harness with `--back`/`--side` added to the metrics call.
- **Path:** run 3 same-seed repeats per subject → `mv_ab_metrics.py --front --back --side` per candidate → record `max_pairwise_abs_diff` for `iou_back`/`iou_side` alongside the existing `iou_front` floor → update `noise-floor-2026-07-29.md`'s pre-registered thresholds if the two new axes need their own adjudication bar.
