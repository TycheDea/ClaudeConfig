# Albedo ghost attribution — mesh vs pipeline era (2026-08-05)

Follow-up to `../town/arch-retess-round1-2026-08-05.md`: after all three
round-2 re-roll seeds failed the atlas pre-screen (6.23–8.32× island
p95/p5, 14–16% dark-frac, vs gate ≤4.0×/≤6.5%), this probe attributes the
ghost before any blend fix is designed. Metric throughout: island-masked
albedo luma p95/p5 and fraction of texels below 45% of median
(`target/arch-retess/pre_screen.py`).

## Measurement 1 — shipped-set map (July-era pipeline)

| prop | p95/p5 | dark-frac |
|---|---|---|
| chapel_arch | 1.78× | 0.23% |
| broken_column | 2.03× | 1.33% |
| gravestone | 2.76× | 4.23% |
| crucero | 2.89× | 4.62% |
| olive_stump | **7.34×** | **11.08%** |
| candelabra_shrine | **8.62×** | **11.71%** |
| rock_07 / rock_09 / rock_face_01 (photoscan truth) | 2.88 / 2.44 / 3.10× | 0.27 / 0.08 / 4.23% |

(cypress skipped — procedural, no generated atlas.)

## Measurement 2 — today's pipeline, July's 15k arch geometry, seed 7

Geometry bit-identical to the shipped arch build (clean.glb sha match;
concept/geometry/cleanup all logged `skip (exists)`; xatlas recompute
under today's code reproduces the exact shipped UV footprint,
island_texels 1,774,817). Result: **4.52× / 7.24%** — between July's
shipped 1.78× (seed 0, same mesh) and the 103k rolls' floor (6.23×).

## Findings

1. **The ghost mechanism is campaign-wide and predates the retess.** Two
   shipped July props (olive_stump, candelabra_shrine) already sit at
   ghost-class ratios, matching the blind tests' "shading painted into
   albedo" tell. Photoscan truth is ≤3.1×.
2. **Severity is a function of geometry and roll, not a new-pipeline
   regression alone.** Same mesh, July seed-0 vs today seed-7: 1.78 vs
   4.52 (single samples each — seed and era are confounded at n=1). The
   103k mesh's four rolls (6.2–10.9×) are consistently worse than the
   15k mesh's one today-roll (4.5×).
   [CORRECTED 2026-08-05, `era-attribution-2026-08-05.md`: the 1.78-vs-
   4.52 pair is delit-vs-direct plus seed, not era evidence — July's
   1.78× went through the MaterialAnything delighting removed for cause
   in `d037686`; the July direct-path arch variant scores 3.61×/5.27%.
   Era is exonerated at hash level.]
3. **Root mechanism (from round-1 provenance trace):** `blend_views`
   averages every visible view per texel with facing-weight² and
   visibility masking only — no color-consistency or outlier rejection
   (`proptex/albedo.py:113-128`). Disagreeing views blend into
   surface-locked ghosts instead of competing.
4. **S5 H chains stay held** until a blend fix lands and re-judges: five
   new props through the unfixed stage would risk five ghosted albedos;
   two of six shipped generated props already carry the defect.

Prior art to consult before designing the fix: the prop-texture-redesign
campaign's `wta`/`hwta` blend variants outscored shipped averaging in
blind test #2 (hwta 4, wta 3, shipped 2.5, photoscan 8) and did not ship —
history recovery in flight; no fix is designed in this record.
