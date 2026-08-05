# Blend-estimator probe — verdict: estimator refuted as the ghost lever (2026-08-05)

Executes the probe registered in `albedo-ghost-attribution-2026-08-05.md`.
Offline, CPU-only re-blend of cached generate-stage view canvases
(`target/prop-cache/`) for 5 candidates — chapel_arch 103k seeds 0–3
(`target/arch-retess/cand_fresh/cand_0`, `cand_reroll_s{1,2,3}`) and 15k
seed 7 (`target/arch-ghost-attr/cand_7`) — under three per-texel
estimators: **mean** (shipped control), **hwta** (mean-LF@14 mm + 28 mm
gain-ratio harmonization + winner-take-all HF), **med-hwta**
(weighted-median LF instead of mean-LF).

Harness: `reblend.py` (committed alongside; live copy + per-variant PNGs
+ `report.json` at `target/blend-probe/`). Validation gate: reproduce the
shipped estimator to MAD ≤ 0.5/255 on covered island texels — achieved
3.0–3.8 × 10⁻⁵/255 on all five candidates (essentially exact). One rig
bug fixed en route: `clean.glb` accessors are glTF Y-up while the atlas
`pos.npy`/`nrm.npy` are Blender Z-up — the third Y-up/Z-up trap this
campaign; any tool mixing glb accessors with atlas arrays must permute.

## Result — no variant clears the pre-screen gate on any candidate

Gate ≤4.0× island p95/p5 AND ≤6.5% dark-frac; anchors: old shipped arch
1.78×/0.23%, photoscan truth ≤3.10×/≤4.23%. Full tables in
`report.json`; summary (p95/p5 | dark-frac):

| candidate | mean | hwta | med-hwta |
|---|---|---|---|
| 103k s0 | 10.88 / 20.3% | 11.00 / 21.2% | 12.26 / 22.4% |
| 103k s1 | 8.32 / 14.5% | 8.45 / 15.1% | 9.03 / 15.7% |
| 103k s2 | 7.76 / 15.8% | 7.91 / 16.7% | 8.41 / 17.1% |
| 103k s3 | 6.23 / 14.0% | 6.33 / 14.7% | 6.73 / 15.2% |
| 15k s7 | 4.52 / 7.2% | 4.73 / 8.6% | 4.83 / 9.0% |

Estimator choice moves the ghost metric <10% — and slightly the wrong
way. Secondary metrics behaved: seam excess stays at the mean control's
floor (±5–8%; the old whole-image-WTA seam blow-up, 3.28 vs 1.45 on
broken_column, does not reproduce for HF-only WTA), and 7.2 mm band std
rises mean → hwta → med-hwta on every candidate (both variants retain
more mid-frequency detail — consistent with hwta's old blind-test win on
stone read, a different charge).

## Interpretation — the ghost is view-consistent; it enters at generation

A weighted **median** across views removes any minority-view outlier. It
removed nothing. Therefore at ghost texels the majority of generated
views agree on the painted shading: the ghost is not created by the
blend averaging disagreeing views — it arrives baked into the view
canvases themselves. This **refutes finding 3 of the attribution record
as the operative lever** (the blend's lack of outlier rejection is real
but immaterial here) and closes the blend-side fix class: mean, hwta,
med-hwta all measured and rejected for this charge; plain wta already a
rejected comparator. Fix class 4 — a texture-native, 3D-consistent
generator producing delit albedo instead of per-view images of a shaded
object — is confirmed as the root-cause successor (licensing-gated;
research dispatched).

## Consequences (decided while unsure, under the standing autonomy grant)

1. **chapel_arch round 3 redirected: transfer the shipped, judge-clean
   albedo (1.78×) onto the accepted 103k geometry** instead of burning
   more generation rolls (4 consecutive failures, floor 6.23×). The §8
   prescription was geometry-only; the fresh texture roll was pipeline
   coupling (new UVs), not intent. Transfer = resample shipped maps into
   the new UV layout (normal map stays the candidate's own hires bake).
   Judge round 3 gate: 8–40 mm band ≥ old, studio read ≥ old, silhouette
   held, no transfer artifacts (seams/softness); ghost dead by
   construction. Honest provenance in the manifest or STOP.
2. **S5 H chains UNHELD under a per-roll pre-screen protocol**: every
   texture roll is pre-screened (`pre_screen.py`, gate ≤4.0×/≤6.5×%)
   before bake/judge spend; up to 3 seeds per prop; a prop with 3
   failing rolls is reported blocked, never shipped. Rationale: the
   hold's premise ("texture stage unconditionally bad") is refined by
   the shipped-set map — 4 of 6 July props rolled clean; the defect is
   roll-dependent and detectable pre-spend. S5's GPU spend was
   user-approved in-plan; worst-case re-roll overhead ≈ +45 min.
3. **Licensing research dispatched** on 3D-consistent texture
   generators (Hunyuan3D-Paint class) per the strict-NC ruling —
   licensing is the only gate.
