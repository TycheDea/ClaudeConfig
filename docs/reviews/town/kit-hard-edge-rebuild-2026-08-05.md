# Town kit hard-edge rebuild — probe, fork, regression verdict (2026-08-05)

Closes the "FORK FOR THE USER" left in the bevel root-cause note (todo.md,
kit bevel item). Fork taken under the user's standing autonomy grant of this
date; logged as a decided-while-unsure item. Shipped in main repo commit
`45bab1d` — bevel path deleted from `scripts/asset-pipeline/townkit/
{geo,buildings}.py`, all 9 kit pieces rebuilt and installed.

## Probe (target/kit-bevel-probe/)

The prior root-cause note ("unwelded per-face quads") was refuted a second
time: `bmesh.ops.create_cube` is welded (`remove_doubles` is a no-op). The
real degeneracy: `bmesh.ops.bevel` with the kit's `segments=2` +
`clamp_overlap=True` at offset 0.02 on kit-scale boxes collapses to a flat
0-non-axis border loop lying on the face — no arris is cut. `segments=1`
(and 3) cut a real chamfer. Face/tri/normal stats per variant in
`target/kit-bevel-probe/stats.json`:

- current (segments=2): 30 faces / 60 tris / 6 normals, 0 non-axis
- real_chamfer (segments=1): 26 / 44 / 26, 20 non-axis
- hard_edge (no bevel): 6 / 12 / 6, 0 non-axis

Isolated judge scores: current 3/10 (13–15% luma trough on every arris),
real_chamfer 9/10, hard_edge 9/10 — chamfer indistinguishable from hard
edge at gameplay framing (2 cm ≈ 1.5 px). Hard edge chosen: visual tie,
12 tris vs 44 per box, and it deletes the degenerate path entirely
(swap rule) instead of re-parameterizing it.

## Rebuild

`bevel`/`bevel_segments` removed from `make_box`, `wall_with_openings`,
and every call site in `buildings.py`. The reja curve-profile bevel
(`curve_data.bevel_depth` in `curve_bars_to_mesh`) is a distinct Blender
mechanism and is untouched — reja_set is byte-stable at 576 tris.
Post-rebuild grep of `townkit/` shows no box-bevel remnant.

Triangle counts (full table with methodology:
`kit-hard-edge-tri-table-2026-08-05.md` alongside this record; supersedes
the P3.0 §4.1 / G2 record counts, which are historical):
casa_small_a 4066→2578, casa_small_b 4092→2700, casa_two_story 5768→3608,
casa_corner 7166→4382, wall_segment 420→84, gate_arch 388→244,
chapel 3413→2437, well_basin 244→100, reja_set 576→576.

## Regression judge (fresh Opus, full-scene zone_review, 31 frames/set)

Old set: `target/ground-cobble-install/renders/` (chamfered kit, same
cameras, captured pre-rebuild). New set: `target/kit-rebuild/renders/`.
14 frames bit-identical (all non-kit close-ups + interior_apse).

1. **Edge/arris — 9/10.** Old chamfer measured as a true defect at
   `close_wall_segment`: a 9 px band 5.7% BELOW the darker adjoining face,
   followed by a 3 px spike +39% ABOVE it; plus floating translucent
   slivers (a −18.4% streak 133 px long across flat sunlit stucco on
   casa_small_b). New: clean monotone 1 px step everywhere. Not 10 only
   because a correctly built chamfer remains the theoretical ideal.
2. **Regression sweep — 8/10.** Diff confined to kit arrises in every
   frame; no UV break, no moved geometry, no z-fighting. Embedded window
   grilles |d| = 0.00000. Two sub-visible observations: a ~0.4–1% UV
   rescale on wall_segment/gate_arch faces (texture stats preserved,
   below perceptual threshold) and sub-visible shading re-noise on those
   two frames only (p50 |d| 0.0087, invisible at 1:1).
3. **Silhouette/faceting at gameplay framing — 10/10.** The chamfer was
   already invisible at mid range in both sets (peak |d| 0.0073); no CG
   faceting — texture/normal detail carries the corner.
4. **Interiors — 10/10.** interior_apse bit-identical; door reveals and
   iron posts |d| ≤ 0.00001.

**VERDICT: PASS — hard-edge kit ships.** Prediction confirmed and
exceeded: the hard edge removes three measured artifacts of the old
chamfer rather than merely matching it.

Lint: content_lint 22/22 green at install. Judge diff crops/heatmaps were
scratchpad-local (session-lifetime); the numbers above are the record.
