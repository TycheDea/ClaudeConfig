# Era attribution — no pipeline regression; gate mis-anchored (2026-08-05)

Fable-tier finding on the question raised by S5's 0/11 failing rolls vs
July's 4/6 shipped passes. Verdict: **code, config, and weights are
exonerated at hash level. Today's 0/11 is (a) a prop batch drawn entirely
from the subject class that already failed in July, (b) a pre-screen
anchored on an artifact of a stage July deleted for cause, and (c)
unselected seeds compared against a winner-selected July baseline.**
Evidence scripts: `target/era-probe/`. Zero GPU probe runs needed.

## Axis findings

1. **Code/config**: `git diff 4c46519..HEAD` on the texture-stage closure
   is inert (env-var plumbing with defaults preserved; procedural-kind
   registry addition; the export.py factor fix). `albedo.py`, `views.py`,
   `atlas.py`, `coverage.py`, `scene.py`, `comfy_run.py` byte-identical;
   `workflows/prop_multiview.json` sha identical July→today. Cache-key
   divergence localizes exactly to the inert edits (exploited as the
   CPU discriminator — no GPU needed). The one real delta predates the
   ship: `d037686` (07-26) removed MaterialAnything per-view delighting
   for cause (tonal diagnostic: delight lifts luma p1 36×, destroys 66%
   of std, "monochrome cream"; direct matched photoscan p1 with 17×
   lower baked-lighting fraction). Only chapel_arch (07-25) shipped
   through delit; the other five July props are already direct.
2. **Weights**: image model / CLIP / ae shas, comfy commit, torch,
   Blender — all byte-identical July→today.
3. **Prop identity — the dominant predictor.** The July direct-path arch
   A/B variant (`target/delight-ab/chapel_arch_variant.glb`, seed 0,
   5 views) scores **3.61×/5.27% — the 1.78× anchor is a delit artifact,
   unreproducible by the current pipeline by design.** July direct props
   split by subject: pale plain limestone 2.03–2.89 pass; dark/complex
   7.34/8.62 fail. Every today-prop is spec'd-dark or recess-dense
   (arch "soot-darkened carvings"; retablo "deep near-black brown" body —
   island median luma 0.18–0.20, 72–79% below 0.25, so p95/p5 explodes
   by construction against spec'd gilt; shrine spec'd recess soot).
4. **Seed**: same-cell spread 1.75× (103k s0–s3); July-views re-blend of
   seed-7 vs July seed-0 differs 1.59× with every hashed input identical.
   July's ships were winner-selected from sweeps (crucero cand_21) —
   "4/6 clean" carries survivorship bias vs today's unselected first-k
   rolls. A uniform era shift ≤~1.5× cannot be excluded at these n;
   nothing larger survives subject control. 13 views IMPROVED seed 7
   (5.73→4.52) — view count is not a failure driver.

## The discriminator that measures the defect, not the spec

**Open-dark fraction** = dark_frac × dark_open_frac (fraction of dark
texels on open faces of the mesh's own occlusion distribution;
`target/era-probe/dark_geography.py`). Ghost-class props (blind-flagged):
3.5–7.6% open-dark, dark_open_frac 0.30–0.47. Pass-class AND shrine:
≤2.9% (shrine 0.3–0.4% — its dark is 95–97% occluded = spec'd soot
geography). Clean separation at ~3% on all 9 props with data.
A global dark-frac ≤6.5% can never pass a prop whose spec paints >6.5%
of the island in soot; p95/p5 ≤4.0 can never pass a dark-bodied material
with spec'd bright accents.

## Corrections to prior records

- `albedo-ghost-attribution-2026-08-05.md` finding 2's 1.78-vs-4.52 pair
  is delit-vs-direct PLUS seed, not era evidence (annotated in place).
- The shipped chapel_arch albedo is delit-era: visually judge-accepted,
  but its tonal statistics are artifacts of a stage removed for cause.
  The round-3 transfer preserves that accepted look by construction
  (old-vs-new judging); the G(λ) material-response probe (deferred
  phase) is where its delit flatness would be revisited.
- The S5 re-hold's "possible era regression" premise is struck; the
  re-hold itself remains correct in hindsight (it bought the gate
  correction before three more mis-gated runs).

## Prescription (design; implementation dispatched separately)

1. No era fix exists to hunt. Strike the regression premise.
2. Pre-screen v2, committed as a standing pipeline instrument:
   open-dark ≤3% primary (threshold mid-gap; any prop landing in the
   2.9–3.5% ambiguity band escalates to a judge instead of auto-verdict);
   p95/p5 ≤4.0 retained ONLY for pale-bodied surface classes (photoscan
   ≤3.10 + July direct passes ≤2.89 are the honest anchors — the 1.78×
   delit anchor is dropped); dark-bodied classes report ratio without
   gating on it. Red-proof: the packaged v2 must reproduce the 9-prop
   separation (ghost props fail, pass props + shrine pass).
3. Re-verdict all existing S5/arch candidates under v2 (CPU-only);
   resume the S5 queue under v2. Structural remainder unchanged:
   recess-dense geometry + spec'd-dark subjects stay hostile to per-view
   lit generation (fix class 4, texture-native generator,
   licensing-gated on the user).
