# License-free texture plan — killing the baked-shading ghost with what we own (2026-08-05)

Deliverable of the user directive's third branch (legal read →
tool research → this). Everything below uses only components already
license-cleared for the shipping path: Qwen-Image lightning (Apache),
Hi3DGen (MIT), Blender bake, xatlas, our own blend/audit code, and the
Z-Image trainability ruling. No new external weights required; the two
conditional external tracks are explicitly optional and gated.

## Why this can work at all (the asymmetry the tools ignore)

Generic delighting is hard because the geometry under the photo is
unknown. Ours never is: we generate views OF A MESH WE OWN. Every
shading component the generator paints — contact shadow, AO pooling,
directional falloff — is predictable from that mesh under a hypothesized
light. That turns "remove unknown lighting" into "regress out a known
basis", which is deterministic math, not a licensed model.

The measured defect (cart/votive attribution, both probes): painted
contact shadows at junctions + view-baked sheen, consistent enough
across views to survive facing-weighted averaging. Three independent,
composable attacks:

## P0 — the premise probe (pre-registered; ~1–2 h GPU, one prop)

Question (unmeasured, decides P2's shape): does Qwen-Image obey lighting
direction in the prompt? Render the votive's views twice — "flat even
diffuse studio light, shadowless" vs strong single-direction raking
prompts (opposed pair) — same seeds otherwise. Measure per-texel: (a)
correlation of generated-view luma with rendered AO/irradiance of the
mesh under the prompted light; (b) how much of the dark-tail
(open_dark's flagged texels) moves with the prompted light direction.
- If shading FOLLOWS the prompt → P2 (paired-light solving) is live.
- If shading is prompt-invariant → P2 dies, P1 carries the whole load
  (the shading is then a fixed geometry-correlated bias — exactly what
  P1 removes).
Either answer is useful; the probe cannot fail to inform. Artifacts +
correlation numbers go in a review record; v2 open_dark is the
before/after instrument.

## P1 — geometry-conditioned delight + robust blend (the core, no ML)

Two changes to the existing texture stage, both in our own code:

**P1a — AO-basis regression per view.** For each generated view, render
the mesh's irradiance proxies under the same camera: AO term +
N·L for a small light basis. Solve per-texel (log-space, multiplicative
shading model) for the reflectance that best explains the generated view
minus the basis; clamp the correction to the shading subspace so albedo
detail (spec'd soot, paint) is untouched — spec'd content is
geometry-UNcorrelated, shading is geometry-correlated. This directly
deletes the two attributed signatures: contact shadows (AO-correlated)
and directional shading (N·L-correlated).

**P1b — outlier-rejecting blend.** Replace facing-weight² averaging with
the hwta/wta family that beat shipped averaging in blind test #2 (our
code, on disk in history): per-texel robust vote across views so a
shadow painted in a minority of views loses instead of averaging in.
View-baked sheen is view-dependent by nature → it disagrees across
views → robust estimators kill it where averaging smears it.

Gate (pre-registered): the three blocked artifacts on disk — cart s6/7/8,
votive s4/5/6 (re-blended from their cached views, zero new GPU) — must
move materially toward the v2 line, and at least one must PASS or
ESCALATE; then one fresh iron roll passes v2 and a G3-style judge at
1:1. Costs: P1 is CPU + minutes-scale re-blends; implementation is the
main spend.

## P2 — paired-light generation (only if P0 says prompts steer light)

Generate each view under the opposed-light pair; per-texel log-space
combination cancels first-order shading before P1 even runs; P1 then
mops residuals. Doubles texture-stage GPU per prop (4.5 → ~9 min) — a
price only paid by props that need it (dark/recess-dense classes).

## P3 — metal response (the "great metallic" half)

Ghost-free albedo is necessary, not sufficient: metal needs
roughness/metalness the renderer can shine. `painted_metal` ships flat
factors today. Procedural MR authoring from the mesh we own: curvature →
edge wear (lower roughness, exposed metal), AO/recess → soot and rust
masks keyed to the surface-class contract, luma-keyed metallic for gilt
vs oak on mixed props. Deterministic, art-directable, zero license.
Gate: opus judge on in-engine gameplay frames — sheen must move with the
light, not live in the albedo (the exact inverse of today's defect).

## P1c — emissive discipline (from the G3 limestone FAIL, same day)

The shrine judge found the third ghost variant: painted LIGHT — phantom
candle flames and glow washes in albedo, invited by a registry subject
that specs "warm candle-gold flame". Emissive content is the engine's
job (HDR emissive, VQ-C3), never a generated albedo's. Rule: texture-
stage conditioning (subject string + concept crop) describes the UNLIT
surfaces; flames/glow are authored as engine emissive + light at
install. Registry subjects for texture generation lose their lighting
adjectives; the concept stage may keep them (concepts are judged as
art). Also note: this ghost variant is view-CONSISTENT (surface-locked
across 8 angles, per the judge) — the blend stage cannot remove it, so
P1b does not cover it; P1c prevention + P2/P4 are its owners. And v2's
open_dark is blind to bright ghosting by construction — the judge layer
is the standing catch until a bright-ghost discriminator is added
(open_bright: bright-tail texels uncorrelated with spec'd content —
design at P1 gate time).

## P4 — optional LoRA (if P1+P2 leave a residual)

Z-Image/Qwen LoRA trained on OUR renders: PBR-textured meshes (CC0
material libraries) rendered lit vs their known albedo → teaches the
generator albedo-space output natively. Training data fully owned;
trainability is what Z-Image was ruled on. This is the escalation path,
not the plan's spine.

## Optional external tracks (not required by this plan)

- **TRELLIS.2 surgery**: swap the one `dr.rasterize` UV-bake for our
  Blender/xatlas baker (Stable3DGen precedent), prove 12 GB, then run
  the P0-style two-light probe on its output before any adoption.
- **Material Anything retest**: eval-only A/B against P1 output —
  license-clean but deleted for cause once ("monochrome cream",
  `d037686`); it must beat P1 on the same gate to earn a second look.

## Order and gates

P0 (probe) → P1 (implement, gate on re-blended blocked artifacts) →
P2 if P0 said yes and P1's gate shows residual → P3 (metal response)
→ P4 only on measured residual. Every stage gates on v2 open_dark +
judge frames; no stage adopts anything unmeasured.
