# PBR maps for prop textures — design note (repo-study A5, 2026-07-22)

Desk study only. NC repos cloned read-only under `reference/` (gitignored); no code
lifted, no weights proposed. Grounding: `scripts/ai-pipeline/prop_texture.py`.

## Where we actually stand

The "albedo-only" framing understates our stage. Today it already produces:
- **basecolor** — projection bake or 4-view ControlNet-depth multiview blend
  (facing-weighted, occlusion/silhouette-tested), but with **lighting baked in**:
  the generated views are lit renders blended verbatim.
- **normal** — real high-to-low Cycles bake from the hires mesh (not AI).
- **metallic/roughness** — declared scalar factors, with an opt-in `--mr-mask`
  second multiview pass producing a two-tone metal/dielectric mask.

The real gaps: (1) baked-in shading polluting basecolor, (2) no per-texel
roughness variation, (3) metallic is binary. All three are exactly what
single-image PBR decomposition solves. Ground materials are separate and already
PBR-complete via StableMaterials (`gen_material.py`).

## Technique 1 — CHORD (Ubisoft, SIGGRAPH Asia 2025) — NC, study only

License: Ubisoft ML License (Research-Only, Copyleft) on code AND weights. Never
touches the shipping path. Concepts (from paper + read of `reference/ComfyUI-Chord`):

- Input is a single **lit texture render**; output is basecolor, normal,
  roughness, metallic (+height via FFT Poisson integration of the normal map).
- Backbone: SD 2.1 UNet used as a **single-step, deterministic image-to-image
  translator** (x0-prediction, fixed per-map text prompt a la RGB↔X). "LEGO
  conditioning": per-map swap-in conv_in/conv_out plus cloned first-down/last-up
  blocks around a shared UNet core; multiple conditioning latents are summed.
- **Chain of Rendering Decomposition** — predict channels in rendering-equation
  order, feeding analytic intermediates back in:
  1. basecolor ← render;
  2. approx irradiance = render / basecolor (analytic quotient);
  3. normal ← render + approx irradiance;
  4. approx rough/metal ← per-pixel grid search inverting a Cook-Torrance GGX
     forward render under a light direction estimated from the blurred
     irradiance (bisection on hemisphere radiance asymmetry);
  5. rough+metal ← render + that analytic guess, refined by the network.
- Trained on MatSynth + proprietary materials (28,344 after augmentation),
  rendered under directional corner lights. Claims 11x speedup over RGB↔X at
  better PSNR/LPIPS.

Verdict: the *technique class* (diffusion-prior intrinsic decomposition of one
lit image) is well represented outside NC land — see landscape. The chained
analytic intermediates are CHORD's edge but demand CHORD-scale training data.

## Technique 2 — Text2Tex (CC BY-NC-SA 3.0) — NC, study only

Progressive depth2img inpainting over a view sequence (from read of
`reference/Text2Tex`): render current partial texture from a candidate view,
classify each pixel **new / update / old** (never textured / textured from a
more oblique view / good), inpaint only new+update, back-project to UV.
Per-view "similarity" (normal·view cosine) is cached in texture space; the
**next-best-view criterion** is a greedy argmax of "view heat" = weighted pixel
fractions (new=1.0, update=0.5, old=0.1) over a 36-view candidate sphere, with a
x0.01 punishment on already-picked views. Output is albedo only, lighting baked.

Relevance to our fixed-azimuth scheme: the sequential-inpainting core would
replace our whole blend machinery (PyTorch3D renderer, per-view latency) — poor
trade. But the **coverage-driven extra view** idea maps cleanly onto what we
already compute: `blend_views` knows exactly which island texels got zero
weight, and the camera/visibility code can score a candidate azimuth by how much
uncovered area it sees. A greedy "add the azimuth that sees the most uncovered
texels" pass is a ~1-day clean-room addition and directly attacks low
`blend_coverage` props. Worth doing independent of PBR.

## Permissive-alternatives landscape (checked 2026-07-22)

| Candidate | What it is | Code | Weights | Verdict |
|---|---|---|---|---|
| **MaterialAnything** (3DTopia, CVPR'25) | mesh (+optional albedo) → albedo/rough/metal/bump UV maps; per-view SD2-scale triple-head estimator + progressive views + UV refiner; trained on Material3D (80K objects) | MIT | Apache-2.0 (HF `xanderhuang/material_estimator`, `material_refiner`, ~0.9B) | **Clean. Primary candidate.** |
| **Marigold-IID-Appearance** (prs-eth) | single image → albedo + rough/metal; SD2 fine-tune, trained on InteriorVerse (interiors, not props) | Apache-2.0 | CreativeML OpenRAIL++-M | License OK; domain mismatch risk |
| **MaterialPalette** (astra-vision, CVPR'24) | photo region → tileable SVBRDF swatch | MIT | OpenRAIL-M | License OK (see below); wrong shape for mesh texturing — swatch source only |
| **StableMaterials** | text/image → tileable PBR set | — | OpenRAIL | Already shipping in `gen_material.py`; ground mats only |
| Hunyuan3D-2.1 Paint | mesh → multiview PBR (albedo+MR) | Tencent community license | same | Conditional: MAU cap, EU/UK/KR territory exclusion, attribution. Backstop, not first pick |
| RGB↔X (Adobe) | image ↔ intrinsic channels | Adobe Research License (non-commercial) | same | NC — out |
| IntrinsiX (NeurIPS'25) | text → PBR image set | CC BY-NC-SA 4.0 | same | NC — out |

**OpenRAIL-M ruling (prior flag resolved):** OpenRAIL-M/RAIL++-M explicitly
permits commercial use and downstream output ownership; its Attachment-A use
restrictions are behavioral (no illegal use, disinformation, harassment, medical
advice, etc.). Generating game-asset textures triggers none of them. **Not a
gate** — consistent with StableMaterials already being in the shipping path.

## Recommendation: adopt-permissive-alternative (MaterialAnything estimator)
### → SHIPPED 2026-07-22 (`8feb605` runner + `2dfb79d` prop_texture swap); step 1
### below is live, `--mr-mask` deleted. One correction from implementation: the
### estimator's "confidence mask" is a RePaint keep-mask (1 = pin to init
### materials, 0 = estimate), and it conditions on a camera-space normal render
### — both reproduced from our own Blender renders.

Build-clean-room is rejected: reproducing CHORD means a 28K-material dataset
pipeline plus multi-day diffusion training — weeks of work and GPU budget to
approximate what a MIT+Apache model already does. Accept-albedo-only is also
rejected: the gap is real (lit basecolor, binary metal) and the permissive fix
is cheap.

Plan sketch, in cost order:
1. **Per-view decomposition slot-in (~3-5 days).** Run MaterialAnything's
   material estimator (Apache-2.0, diffusers, own venv like StableMaterials) on
   each multiview `gen.png` → per-view albedo/roughness/metallic. Blend each
   channel through the existing facing-weight machinery (it is channel-agnostic)
   and pack rough/metal exactly as `--mr-mask` already does. Delit albedo,
   per-texel roughness, continuous metallic — and the two-tone `--mr-mask` pass
   plus its second generation run become deletable. Eval on 2-3 props first
   (generation runs → needs the standing heavy-compute go-ahead).
2. **Coverage-driven extra view (~1 day, clean-room, independent).** Greedy
   Text2Tex-style pick of one extra azimuth maximizing visible uncovered texels
   when `blend_coverage` is low.
3. **Fallback** if per-view estimates blend inconsistently: MaterialAnything's
   full progressive pipeline (confidence masks + UV refiner), at the price of a
   PyTorch3D/Blender-3.2 environment (~1-2 weeks) — or Hunyuan3D-2.1 Paint as a
   conditional-license backstop.

Projection-strategy props keep declared scalar MR; decomposition applies to the
multiview path where the lit-render problem lives.
