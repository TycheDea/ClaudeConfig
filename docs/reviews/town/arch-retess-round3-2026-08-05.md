# chapel_arch retess round 3 — judge verdict: FAIL, axis 5 only (2026-08-05)

Fresh-Opus judge over `target/arch-retess/renders_old/` (shipped 15k) vs
`renders_round3/` (103k geometry + shipped-albedo transfer, post seam fix),
studio + raking rigs, 8 frames each. Gate pre-registered per the
priced-mechanism rule: (1) relief 8–40 mm ≥ old, (2) ghost dead by light
dependence, (3) studio read ≥ old incl. resample sharpness, (4) silhouette
held, (5) no transfer artifacts.

## Frame inventory finding

macro_01 and macro_03 are EMPTY in both rigs and both sets — the 0.6 m macro
aim point lands in the arch's void at those yaws (max |old−new| 1–2/255,
0.0% chromatic). Real evidence = 4 informative frames per set. (Process
note for any future macro rig work: aim-point validity is not checked.)

Scale: fovy 45°, MACRO_DISTANCE 0.6 m → 0.485 mm/px.

## Axis verdicts

1. **Relief 8–40 mm — 8/10 PASS.** Shading-isolated instrument
   (log(raking/studio), cancels albedo): every band ≥ old on both
   informative frames (m00 ×1.14–1.29, m02 ×1.07–1.15); raw raking band
   contrast m00 ×1.55–1.83. Round 1's 2.36–2.62× does NOT reproduce — that
   number rode a ghosted albedo's baked shading and was never a geometry
   measure. 4–8 mm (normal-map band) also up; studio-rig bands flat as
   expected (frontal light is not the relief instrument).
2. **Ghost dead — 9/10 PASS.** New tracks light better than old
   (corr(studio,raking) 0.405→0.294 m00, 0.551→0.496 m02); studio-locked
   dark fraction down on both frames. Light-independence sweep returns only
   deepened real grooves (dark in both rigs by construction).
3. **Studio read — 9/10 PASS.** Value ±1.4%, chroma/hue within 1%,
   high-frequency energy UP (+13.9% m00, +1.5% m02) — no resample softness.
4. **Silhouette — 9/10 PASS.** IoU 0.99545/0.99682, XOR confined to thin
   contour strips, max lateral shift ~12 mm; profile bumpier (real stone
   contour), no shape change. Interior observations (non-blocking, mesh
   properties not transfer defects): m00 slot y55–100 x200–330 renders as
   hard alternating bright/black triangles; m00 through-aperture y615–810
   x440–630 blows out pale under raking (light-dependent, ratio 2.10).
5. **Transfer artifacts — 3/10 FAIL (blocking).**
   - **Undocumented patch** (the blocker): macro_02 rows 3–59 × cols
     101–192, 2449–3241 px = 0.26–0.34% of object. Weber vs 41 px annulus:
     studio +0.547 (old +0.028), raking +1.375 (old +0.062), at HALF the
     surround's chroma (0.097 vs 0.200) — same sign both rigs ⇒
     surface-locked chalky albedo paint, not highlight, not hole (reads
     0.104 under raking's black sky, a hole would be black). Absent in old.
     Plainly visible at 1:1; the judge flagged it on first read before
     measuring.
   - **Documented residual re-ruled:** rows 828–842 × cols 285–366. The
     manifest's "NOT visible in raking" is FALSE — relative contrast is
     twice as high under raking (+0.338 vs studio +0.160).
   - **Same family:** three more bright dashes on the m02 course line
     (y510–517 x653–708, y515–525 x786–843, y505–510 x714–776).
   - Total light-independent bright artifact: 4647 px = 0.497% of object in
     macro_02. The manifest's 37-texel/two-cluster accounting covers only
     the groove dash; the loudest artifact was never in it.

## Instrument lesson

The pre-screen stayed green (1.6078× / 0.40%) across a defect a human sees
at 1:1: an island-percentile gate is blind to a localized 0.3% patch, and
the worker's residual count was derived from its own fix's diagnostic
region, so artifacts of any other origin were invisible to it. Full-atlas
independent accounting + an orchestrator eyeball of the frames precede any
future judge dispatch.

## Disposition

Axes 1–4 stand for round 4 wherever geometry is bit-identical (axis 1/4 are
geometry-driven); axes 2/3/5 re-judge on fresh renders after the albedo
fix, since the fix touches the albedo channel they measure. Fix round
dispatched: root-cause the top-edge patch + course-line dash family at bake
input (no output painting, no frame-space masking), honest manifest
correction, full-atlas residual accounting.
