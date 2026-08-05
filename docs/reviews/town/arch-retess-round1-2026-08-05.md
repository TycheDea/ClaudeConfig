# chapel_arch retessellation — round 1 verdict and adjudication (2026-08-05)

Executes `decimation-attribution-2026-08-01.md` §8(b). Status: **code
shipped (`466edb7`), first asset install FAILED judge and was reverted** —
the arch ships at 15k until round 2 passes. This record carries the two
adjudications that redirect round 2.

## The budget re-anchor (decided while unsure)

The §8 prescription derived ~171k tris from `2·136.7/0.04²`. The fresh
chain derived **103,068** — because the interior-face strip
(`1f32bbe`/`323c55c`) postdates every arch build and removes 38% of the
raw mesh's area: real post-strip area **82.455 m²**; the study's 136.7 m²
was measured on the stale pre-strip shipped bytes. Adjudicated: the 40 mm
footprint is the goal, not the 171k intermediate — spending tris on
stripped interior faces is waste. Cross-checks: an independent area script
reproduces both figures; decimation conserves area to 99.94%; installed
candidate measures 47.86 mm mean edge (in the 30–65 band); the S2 GPU gate
tested 171k, strictly above what ships. `verify_glb.py` re-anchored to
103068±5% and re-red-proofed (FAILs both checks on the shipped 15k arch:
`target/arch-retess/red_proof_shipped_v2.log`).

## Round-1 judge (fresh Opus, matched macro frames, old 15k vs new 103k)

Scores 5/9/3/5 — **FAIL**. Two independent grounds:

1. **Texture ghost (the real blocker, 3/10).** The fresh albedo roll baked
   surface-locked shading and a painted arcade silhouette from a foreign
   viewpoint: studio dark fraction 11.9% vs old 1.9%; cross-rig dark-mask
   IoU 0.398 vs old 0.036 (light-dependent darkness moves between rigs;
   this doesn't); atlas p95/p5 **7.55×** vs 3.42× for the photoscan
   reference — second-darkest albedo of all 19 shipped props.
2. **Relief band (5/10 against an over-strict gate — see adjudication).**
   Measured band contrast new/old: 4–8 mm 1.70× median but inconsistent
   (2 of 5 crops worse); 8–17 mm 2.36×; 17–40 mm 2.62×; 40–100 mm 2.13×.
   Silhouette clean (IoU 0.9985, 9/10).

Side-finding: `prop_audit.py --asset chapel_arch` errors on the retess
UVs — the cached coverage artifact `target/prop-coverage/
holes_chapel_arch.png` predates the new layout; regen at next install.

## Adjudication of criterion 1: the gate was stricter than the mechanism

The dispatch asked the judge to "rule the melted-carving defect dead" at
4–17 mm. The study itself priced that band: 20 mm footprint ≈ 683k tris
("essentially shipping the hires mesh") and chose 40 mm deliberately. A
40 mm mesh can never geometry-carry 4–17 mm; that band belongs to the
normal map — which provenance tracing confirms is already a true hires
bake (Cycles selected-to-active from the 773k mesh,
`scripts/ai-pipeline/proptex/export.py:49-71`), in both old and new
builds. The judge's own numbers show the prescription delivered where
physics allows: the 1–5 cm carving band (10–50 mm) improved 2.4–2.6×.
**Geometry is settled at 103k; round 2 re-judges texture, not tessellation.**

## Ghost mechanism and round-2 fix path

The multi-view albedo blend (`proptex/albedo.py:113-128`,
`proptex/atlas.py`) has facing-weight² and per-texel visibility masking,
but **no color-consistency or outlier rejection — disagreeing views
average instead of compete**. Roll variance decides the damage; the old
arch's albedo from the same pipeline is clean (crop p95/p5 1.3–1.4×).
Round 2: re-roll the texture stage on the SAME accepted 103k geometry
with new seeds, pre-screen each roll's atlas directly (p95/p5 and
dark-texel fraction against the old-arch/photoscan anchors) before
spending bake+judge, then a fresh judge with the re-anchored gate:
ghost dead (light-dependence test), 8–40 mm band ≥ old, silhouette held,
studio read ≥ old.
