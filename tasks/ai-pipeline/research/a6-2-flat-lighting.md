# A6.2 — Replace the flat-lighting control

**Result: no replacement is needed. The premise was false.**

## The premise

`prop_multiview.json` runs SDXL at cfg 7 with the negative prompt
`"scenery, landscape, multiple objects, dramatic lighting, strong shadows, cropped"`.
At cfg 1 a distilled base has no negative prompt, and negation in a positive
prompt is ignored — so A5b recorded flat albedo as having "no mechanism" on
Z-Image, and A6.2 was opened to build one.

That assumed the negative prompt was doing the work. It was never tested.

## Measuring the right thing

Mean luma and R−B were both used as flatness proxies during A5b and both are
confounded: a dark palette reads as "lit", a warm albedo reads as "warm light".

Baked lighting is luminance that **tracks surface orientation**. So: recover
normals from the depth map each view was conditioned on, then find the single
directional light whose `max(N·L, 0)` best explains the generated luma. The
explained variance is the baked-lighting fraction. A uniformly dark object with
flat albedo scores ~0. (`scripts/ai-pipeline/bakeoff/metrics.py`)

**The scores are meaningless without a positive control**, so
`lit_control.py` renders the same rig with a hard sun and a flat white
material — pure shading on the real geometry. It also re-renders depth, which
doubles as a mesh-identity check (silhouette IoU 0.955 against the bake-off's
own depth; normals align).

## Result

| Config | baked fraction | mean luma |
|---|---|---|
| **Positive control — sun-lit white mesh** | **0.330** | — |
| SDXL, negative prompt @ cfg 7 | 0.011 | 0.336 |
| Z-Image, flat-lighting clause in positive | 0.014 | 0.211 |
| Z-Image, **clause removed** | **0.014** | 0.219 |
| Z-Image, **asked FOR dramatic chiaroscuro** | **0.018** | 0.207 |

The control tops out at 0.33, not 1.0, because a real render carries shadow,
occlusion and interreflection rather than pure Lambert. Generated views sit
18–55× below it.

**Removing the flat-lighting clause changes nothing** (0.014 → 0.014). And the
base cannot be made to bake directional lighting *even when explicitly asked
for it* (0.018).

The adversarial config is what makes the null meaningful, and the prompt
demonstrably took effect: `dramatic` differs from `short` by 0.076 mean
absolute pixel difference — 3× the `nolight` difference — and raises on-object
luma std from 0.207 to 0.238. The model responds to the prompt. It just cannot
impose a lighting *gradient*, because the depth ControlNet at strength 1.0 pins
the low-frequency structure and 8-step distilled sampling has no headroom to
fight it.

## Conclusion

Flat albedo on this stage is a property of **depth-conditioned multiview
generation**, not of the prompt. The negative prompt was inert insurance on
SDXL too — SDXL scores 0.011 with it, Z-Image 0.014 without.

So A6.2 closes with a deletion rather than a mechanism: when A6.4 rewrites
`prop_multiview.json` for Z-Image, the negative prompt simply does not carry
over, and nothing replaces it. The positive prompt keeps its
`"flat even neutral studio lighting"` clause — it costs nothing and it is a
description rather than a negation — but it is documented as **not
load-bearing**, so nobody re-derives it as a constraint later.

**Watch item for A6.3:** this result holds *because* the depth signal dominates.
Anything that weakens depth conditioning to improve material separation may
reintroduce baked lighting. Re-run `metrics.py` against `lit_control.py` after
any such change rather than assuming flatness survives.

## Cleanup

The A5b prompt-tuning variants (`zimage_mat`, `zimage_s14`) and the A6.2
ablation variants (`zimage_nolight`, `zimage_dramatic`) are deleted along with
their outputs — their findings are recorded here and in `a5b-bakeoff-results.md`,
and each is one prompt clause away from `wf_zimage_short.json` if ever needed
again. The harness keeps `sdxl`, `zimage`, `qwen` and `zimage_short`.
