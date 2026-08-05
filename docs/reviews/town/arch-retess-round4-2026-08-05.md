# chapel_arch retess round 4 — judge verdict: OVERALL PASS (2026-08-05)

Fresh-Opus judge, axes 2/3/5 on `renders_old` vs `renders_round4` (axes 1
relief and 4 silhouette stand from round 3 — geometry bit-identical).
Calibration: the judge's instruments reproduce the round-3 record's numbers
on the round-3 set (corr 0.298/0.495 vs 0.294/0.496; HF +14.3% vs +13.9%),
so all three rounds sit on one scale. Scratch: `target/arch-retess/
judge_round4/`. Fix under judgment: cage 15 mm / ray 30 mm transfer bake +
2 px rim source cleaning (`arch-transfer-diagnosis-2026-08-05.md`
prescription, implemented per `transfer_manifest.json`).

## Axis 2 — ghost dead: 9/10 PASS
Cross-rig luma correlation old → r4: macro_00 0.4053 → 0.3035, macro_02
0.5511 → 0.5080; stable under mask erosion 0/2/6 px and below old at every
HF sigma tested. r4 marginally above r3 (+0.005/+0.013) — expected: the
restored bright content is genuine light-independent albedo. Instrument
caveat recorded: round 3's "studio-locked dark fraction down" does NOT
reproduce at any threshold for r3 or r4 (deltas ≤0.6 pp, both directions);
that instrument is ruled inconclusive and the axis rests on correlation.

## Axis 3 — studio read: 9/10 PASS
CIELAB vs old: ΔL* +0.64/−0.74%, ΔC* +0.62/+1.01%, Δh* ±0.13°, ΔE76 of
means 0.40/0.43 — inside round-3 tolerances and tighter than r3 on every
term. HF band energy ×1.03–1.13 of old in every band (no softness).
Per-pixel distance to old shrank vs r3 (m02 mean|ΔRGB| 7.13 → 5.44).

## Axis 5 — transfer artifacts: 8/10 PASS
Round-3 FAIL regions: chalky patch +0.331/+0.770 → **+0.009/−0.011**,
chroma ratio 1.00 — dead. Dashes A/B dead (back to old / dark at half
old's depth); documented-residual box now a deepened groove (relief
channel, axis 1's territory). Full-frame bright sweep: macro_02
chalky-signature area old 433 px → r3 1529 → **r4 515** (old's level);
round 3's blocking 4647 px does not reproduce anywhere. The 24 restored
bright atlas clusters: zero object pixels ≥225 luma in either rig; the
brighter-than-r3 differential concentrates on chart rims at column corner
edges and is strongly light-dependent = lit relief, not paint.
Honest residuals (reported, non-blocking): dash C at 66–69% reduced
magnitude, chroma ratio 0.97, reads as a normal course seam at 2×; m00
top-right corner facet (423 px, 0.045%, improved ~39% vs r3) reads as
plausible pale stone, slightly gray.

## Non-scored geometry carryovers (bit-identical to r3, for the ledger)
The mesh-family items round 3 flagged remain: the macro_00 raking
through-aperture (y615–810 x440–630) renders a pale blown backface with
hard black polygonal cutouts — light-dependent (surface-locked test
correctly excludes it) but at 1:1 the loudest feature in any frame; the
m00 slot triangles; the m02 capital-corner sliver notch (69 px). These are
properties of the accepted 103k mesh (accepted round 1 on silhouette +
relief), not of the transfer. Carried as a known cosmetic item for the
user; any rework is a new, separately-scoped decision.

## Disposition
PASS clears the install gate recorded in the ledger: build the honest
`transfer` stage in proptex/, produce the content-addressed chain, install
with shipped-bytes-equal-judged-bytes asserted, lint, commit.
