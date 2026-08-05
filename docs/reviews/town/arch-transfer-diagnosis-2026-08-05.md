# chapel_arch transfer-defect diagnosis — two mechanisms confirmed (2026-08-05)

Fable-tier root-cause finding for the round-3 judge FAIL
(`arch-retess-round3-2026-08-05.md`, axis 5). Diagnosis only; no pipeline
file, bake output, or render modified. Evidence scripts + masks:
`target/arch-retess/cand_transfer/diag/` (s1–s9). Atlas is 2048² (the
round-3 record's 4096² figure was wrong); atlas coords PIL row-0-top.

## Corrections to prior accounting

- The manifest's `known_residual` cluster (1103,782) is NOT visible in
  macro_02 at all — the judge's "documented residual" at y828–842 is a
  different, undocumented artifact (wrong-surface class, below).
- The killed worker's "wrong-surface hits, not margin filler" note was
  half right: true for the chalky patch + y828 groove, false for the
  y505–525 dashes (which ARE filler — the seam fix's own refill).
- Inherited `frame_to_atlas.py` map verified correct by independent
  Möller–Trumbore ray casts (10/10 exact).

## Mechanism C — cage/ray geometry accepts the surface behind

The bake used cage_extrusion 10 mm and max_ray_distance = 10 mm + 0.4% ×
mesh diagonal (7.881 m) = 41.5 mm — a heuristic copied from
proptex.export's hires→lowres bakes, where deviations are sub-mm. Here
local 15k-vs-103k deviation at the defect spots is 10.5–15.3 mm > cage,
so the inward ray starts PAST the correct source surface, flies 33–42 mm,
and lands on the pale far side of a 23–32 mm wall gap — inside the 41.5 mm
budget. Exact reproduction: at cage 10 mm every probed defect texel
reproduces the bake's wrong pixel; at cage 15 mm every one snaps correct
at 0.5–4.2 mm travel (`diag/s7_ray_repro.py`, `s7b_cage_probe.py`).
Produces the macro_02 chalky patch (atlas 1198–1213 × 1385–1405, samples
chart 444 pale stone luma 181–199 into a 117–127 surround) and the
y828–842 groove dash. Full atlas: 7,833 texels / 1,185 clusters at the
physically-derived >20 mm threshold (legit deviation p99 = 15.5 mm; wall
gaps ≥23 mm). Mesh deviation field: p50 4.7 / p95 10.6 / p99 15.5 /
p99.9 22.4 / max 39.8 mm.

## Mechanism A — margin cleaning falsified real content

`clean_source_margin.py`'s 8 px erosion marks 54% of the source island
untrusted (island 0.423 → trusted 0.193 over 1,264 charts). Thin strip
charts (grooves, course lines) keep only a skeleton — chart 358 retains
0.6% of its window — and get flood-refilled monochrome; the bake's 3D
correspondence there is CORRECT, the input was falsified. Produces the
three y505–525 dashes. Full atlas: 186k texels / 8,079 clusters (>15
luma rewrite). Also present: 6,050 OUT texels (source UV degeneracies,
1–2 px speckle) and 27,089 NOHIT texels (1.9% of island, margin-filled).

Both detectors are correspondence-based (independent of frame renders and
of the parameters they gate) and red-proofed: they fire on every judged
defect box on the current output.

## Prescription (implemented separately)

1. Cage/ray from the MEASURED deviation field, not the export heuristic:
   cage must exceed the deviation the transfer bridges (p99.9 22.4 mm ⇒
   cage ≈ 20–25 mm); max_ray ≈ cage + 15 mm, staying below cage + the
   smallest cross-wall gap (23 mm). Sweep cage ∈ {15, 20, 25}, gate on
   the s8 class-C detector, pick the plateau.
2. Rewrite the source cleaning to KEEP every island pixel's original
   content; regenerate only outside-island plus at most a 1–2 px boundary
   rim (where the 1296-era margin junk actually lived: median +1 px
   inside the boundary), per-chart-capped.
3. Rerun bake → s8 full-atlas accounting as the gate → correct the
   manifest (incl. the known_residual misattribution) → fresh renders →
   judge axes 2/3/5 (axes 1/4 stand, geometry unchanged).

Honest remainder after the fix: texels whose deviation exceeds the chosen
cage (~0.2% of island at 20 mm, groove interiors) become margin-filled
no-hits — locally plausible smear, sub-visible at 0.485 mm/px; the OUT
speckle and any junk ≥3 px inside source charts are outside this
pipeline's reach and are re-measured after the rerun. The 37-texel
sliver-UV residual is real but macro_02-invisible and untouched.

Forbidden to the implementor: painting any output, frame-space masks,
per-defect/per-chart special cases, keeping the 8 px erosion, or carrying
forward the manifest's residual misattribution.
