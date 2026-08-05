# Texture-Native, 3D-Consistent Texturing for an Existing Mesh — Licensing & Capability Brief

Commissioned 2026-08-05 after the blend-estimator probe
(`blend-estimator-probe-2026-08-05.md`) proved the baked-lighting ghost
enters at generation (view-consistent), closing the blend-side fix class.
Research worker output, verbatim below. **No adoption decision is made
here — every licensing call is the user's.**

---

**Scope:** candidates that texture an *existing* mesh (mesh + concept image → albedo/PBR), evaluated against the measured defect (generator paints shading into albedo consistently across views).

**Hard rules applied:** NC-licensed components never touch the shipping asset path (eval-only at best). Licensing is the only gate; tool incompatibility is not a rejection reason.

## 0. Three findings that reframe the whole landscape

**(a) The real NC gate is the rasterizer, not the weights.** `nvdiffrast` (and `nvdiffrec`) are under the **NVIDIA Source Code License (1-Way Commercial)**: *"The Work and any derivative works thereof only may be used or intended for use non-commercially… research or evaluation purposes only and not for any direct or indirect monetary gain."* Almost every academic texturing pipeline bakes UV through nvdiffrast. This taints the *pipeline*, not the model weights, and is removable by swapping the rasterizer.
License: https://github.com/NVlabs/nvdiffrast/blob/main/LICENSE.txt

**(b) The standing "TRELLIS = NC/eval-only" ruling does not match the license text, and our own mesh stage already contradicts it.** `microsoft/TRELLIS` and `microsoft/TRELLIS.2` state MIT for **both code and weights**; the HF card `microsoft/TRELLIS.2-4B` is tagged `mit`. Meanwhile **Hi3DGen/Stable3DGen — our current mesh generator — is itself a TRELLIS derivative under MIT**, and its README states the NVIDIA deps (kaolin, nvdiffrast, flexicubes) were *removed specifically so the adapted version can be used commercially*. So the NC concern was always finding (a), and Stable3DGen already solved it once for TRELLIS v1. **This needs the user's re-read** — it may unblock the strongest candidate.
https://github.com/microsoft/TRELLIS.2 · https://huggingface.co/microsoft/TRELLIS.2-4B · https://github.com/Stable-X/Stable3DGen

**(c) Tencent's territory clause is a hard EU blocker, verbatim in both 2.0 and 2.1.** The grant covers *"the worldwide territory, **excluding the territory of the European Union, United Kingdom and South Korea**."* The user is in the EU, so the licensee arguably receives **no grant at all** — not a restriction on outputs, an absence of licence. Plus a 1M-MAU commercial trigger and a no-training-other-models clause. Output ownership is clean (*"Tencent claims no rights in Outputs You generate"*). **This is the flagged legal read.** It knocks out the current published quality leader.
https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE · https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE

## 1. Ranked comparison

Rank = (usable on an EU shipping path) × (architecturally delit) × (textures *our* mesh) × (fits 12 GB).

| # | Candidate | License (code / weights) | EU-shipping-path OK? | Output | Consistency model | Mesh+image in? | 12 GB fit |
|---|---|---|---|---|---|---|---|
| 1 | **TRELLIS.2** (MS, Dec 2025) | MIT / MIT | ⚠️ **weights yes; pipeline needs nvdiffrast swap** | BaseColor+Rough+Metal+Opacity | **Native 3D (O-Voxel)** | ✅ `example_texturing.py` | ⚠️ 24 GB official; GGUF/fp8 community forks 6–12 GB |
| 2 | **Material Anything** (CVPR'25 Highlight) | MIT / released | ✅ (no nvdiffrast; bpy) | Albedo+Rough+Metal+Bump, UV-refined | Per-view + UV refiner | ✅ (mesh; handles *already-lit* textures) | ✅ SD2.1-class |
| 3 | **MVPainter** (AMAP, May 2025) | Apache-2.0 / **Apache-2.0** | ✅ likely (deps unverified) | RGB MV → PBR via IDArb (MIT) | MV diffusion + ControlNet geo | ✅ GLB + ref image | ⚠️ 3B, unstated |
| 4 | **Paint3D** (CVPR'24) | Apache-2.0 / released | ✅ | **Lighting-less** 2K UV albedo | **UV-space native** | ✅ (mesh + image/text) | ✅ SD1.5/2-class |
| 5 | **FlashTex** (Roblox, ECCV'24) | Apache-2.0 / released | ✅ | Albedo + rough/metal/normal | LightControlNet, per-mesh optim | ⚠️ mesh + **text** | ✅ |
| 6 | **MV-Adapter** | Apache-2.0 / **Apache-2.0** | ✅ | **Shaded RGB only** | Geometry-conditioned MV | ✅ | ✅ 10–16 GB |
| 7 | **Step1X-3D** texture module | Apache-2.0 / Apache-2.0 | ✅ | RGB (texture-only class) | SDXL MV, geo-conditioned | ✅ | ✅ |
| 8 | **SyncMVD** | MIT / n/a (SD-based) | ✅ | **Shaded RGB**, text-driven | Synchronized MV diffusion | ⚠️ mesh + text | ✅ |
| — | **Hunyuan3D-2.1 Paint** (+2.0, RomanTex, MaterialMVP) | Tencent Community Licence | 🚫 **EU excluded from grant** | Albedo+MetalRough+Normal | MV diffusion, illum-invariant | ✅ mesh+image | ⚠️ 21 GB @6×512 |
| — | **UniTEX** (CVPR'26) | Apache-2.0 code / **FLUX.1-dev LoRA = NC** | 🚫 NC | Diffuse (illumination-free) | 3D Texture Functions, UV-free | ✅ | ⚠️ |
| — | **LumiTex** (ICLR'26) | Apache-2.0 code / **FLUX + Hunyuan deps, repo self-declares NC** | 🚫 NC | Albedo+Metal+Rough, delit by design | MV + lighting-aware attention | ✅ mesh+image | ⚠️ |
| — | **MatLat** (CVPR'26 Highlight) | code ? / **CC BY-NC 4.0 weights** | 🚫 NC | PBR maps | Material latent space (SD3.5) | ⚠️ mesh + **text** | ? |
| — | **TEXGen** (SIGGRAPH Asia'24) | **NO LICENSE FILE** (`license: null`) | 🚫 all-rights-reserved | UV albedo | **UV-space native** | ✅ | ✅ 24 GB test |
| — | **NaTex** (CVPR'26, Tencent) | — | 🚫 **no code/weights released** | Albedo (native 3D color) | Color point-cloud VAE + DiT | ✅ | — |
| — | **Meta AssetGen 2.0** | — | 🚫 **no weights, ever** | — | — | — | — |
| — | **Meshy / Tripo API** | Contractual (paid = full commercial) | ✅ by contract | Albedo w/ explicit delight toggle | proprietary | ✅ upload own mesh | n/a (cloud) |

## 2. Per-candidate detail

### TRELLIS.2 — the only permissive, natively-3D, PBR, mesh-conditioned option
Microsoft Research + Tsinghua, released Dec 2025 (arXiv 2512.14692), 4B params. Its O-Voxel latent encodes geometry *and* surface attributes jointly, so it predicts **Base Color / Roughness / Metallic / Opacity as material channels** rather than painting RGB and hoping — this is the architectural answer to a baked-lighting ghost, since the training target is PBR ground truth from Objaverse-XL (Sketchfab subset), and 3D-FUTURE was *excluded from training precisely because it lacks PBR materials*. Crucially there is a **separate texturing-only entry point** (`example_texturing.py`, `app_texturing.py`) that takes **an existing mesh + an image** and conditions on the provided shape — exactly our integration surface, and it slots behind Hi3DGen without touching geometry.

*Two caveats, both real.* First, **licence**: MIT on model and code, but the repo notes nvdiffrast/nvdiffrec are "under separate license terms", and issue [#22](https://github.com/microsoft/TRELLIS.2/issues/22) is an unresolved open request for clarification on commercial use; the community ask is to swap in PyTorch3D or another MIT/Apache rasterizer, which Microsoft has not done. Stable3DGen already performed this exact surgery on TRELLIS v1, so precedent and a worked example both exist. Second, **evidence**: TRELLIS v1 has a documented baked-shadow complaint ([microsoft/TRELLIS#199](https://github.com/microsoft/TRELLIS/issues/199) — "shadows baked into the texture that remain even after lighting the mesh"), and **no published head-to-head measures TRELLIS.2 albedo delighting against Hunyuan3D-2.1**. The delit claim rests on architecture and training-data reading, not on a measurement. That is the single cheapest probe available and it should precede adoption.

Hardware: 24 GB official (verified on A100/H100). Community `ComfyUI-Trellis2` (visualbruno, **MIT**) exposes `Trellis2MeshTexturing` and `Trellis2MeshTexturingMultiView` nodes for existing meshes, and has shipped **fp8 (Feb 2026) and GGUF Q4–Q8** paths reported to run the 4B model at 6–12 GB with 2–3× slower generation. Reference timings on H100: 512³ ≈ 3 s, 1024³ ≈ 17 s, 1536³ ≈ 60 s. Note the low-VRAM reports come largely from SEO-ish tutorial blogs (trellis2.app, dailytopai) — treat as directionally true, not measured.

### Material Anything — the surgical fix that keeps the current pipeline
CVPR 2025 Highlight (3DTopia/Shanghai AI Lab), **MIT**, weights released (`material_estimator`, `material_refiner`). Uniquely among all candidates it explicitly enumerates **"generated objects… their textures may exhibit unrealistic lighting effects"** as a supported input class, alongside texture-less, albedo-only, and scanned. It runs a triple-head SD2.1 U-Net (albedo / roughness-metallic / bump) per view, driven by a **confidence mask that encodes illuminance uncertainty**, then unwraps to UV and refines. Dependency list is clean — trimesh, diffusers, bpy — **no nvdiffrast, no kaolin, no pytorch3d**. Blender/bpy is GPL but is used as a rendering tool, which does not encumber output assets.

The honest limitation: it does not *remove* baked lighting so much as **decide how much to trust it** per region, then re-derive materials semantically. Whether that clears our specific consistent-across-views ghost is unmeasured. Its Table 1 (1,200 images / 20 objects) reports FID 100.63 vs NvDiffRec 103.81, DreamMat 113.34, Text2Tex 116.41; CLIP 31.06. Baselines are all 2023–24 — **it has never been benchmarked against Hunyuan3D-Paint, MVPainter, or TRELLIS.2**, so its ranking against the modern field is unknown. Its appeal is that it is additive: keep the Qwen-Image per-view generator, bolt this on as a delighting/PBR stage.

### MVPainter — the only bake-off that used *our* geometry
AMAP (Alibaba), May 2025. Code **Apache-2.0** (LICENSE verified verbatim: *"no non-commercial, territory, or field-of-use restrictions"*) and weights **Apache-2.0** on HF (`shaomq/MVPainter`, 3B). Provenance is clean: the paper states the MV model was trained on ~1.2M Objaverse-derived models with **no mention of initialising from a pretrained base**, and the PBR extractor is **initialised from IDArb, which is MIT** (`Lizb6626/IDArb`). So unlike most Apache-labelled academic repos, this one does not appear to launder Tencent or FLUX weights — though the requirements file could not be fetched to confirm the rasterizer, leaving the nvdiffrast question open.

Its evidence is the most directly transferable in this brief: an Elo bake-off across four geometry backbones — and **Hi3DGen is one of them**. On Hi3DGen meshes MVPainter scores 1125 / 1148 / 1156 (reference-texture alignment / geometry-texture consistency / local texture quality) vs Hunyuan3D-2.0 at 865 / 859 / 837 and MV-Adapter at 1010 / 993 / 1008 — its largest margin of the four backbones. A 5-participant human study on TripoSG geometry confirmed the ordering. Caveats: the baseline is Hunyuan **2.0**, not the much stronger 2.1 PBR model; the Elo judge is a VLM; n=5 for the human check. And PBR here is a *post-hoc extraction* from shaded RGB views via IDArb — architecturally the same shape as our current problem, just with a better estimator, so it is a weaker structural answer than TRELLIS.2 or Material Anything.

### Hunyuan3D-2.1 Paint — best measured quality, wrong jurisdiction
The published leader. `hy3dpaint` is a standalone stage: **mesh.glb + image.png → albedo, metallic-roughness, normal, position, textured_mesh.glb**, powered by RomanTex (3D-aware RoPE multi-attention, ICCV'25) and MaterialMVP (illumination-invariant multi-view PBR diffusion, whose entire thesis is consistency across *lighting* as well as viewpoint — i.e. it targets our exact defect). VRAM: **≥21 GB at 6 views / 512** per the official README — above our card; ComfyUI has shipped low-VRAM fixes but at reduced view count/resolution.

**It is nevertheless the one candidate not to touch without the user's explicit legal ruling**, and the ruling looks unfavourable: the licence grant is territorially defined to *exclude* the EU. This is stronger than a use restriction — there is no grant to rely on. It also propagates: **MaterialMVP's repo carries no explicit licence** and its "professional" weights *are* Hunyuan3D-Paint; RomanTex likewise. Anything whose weights descend from Hunyuan inherits this.

For reference on what we would be giving up: LumiTex's Table 1 (133 held-out objects) puts Hunyuan3D-2.1 at texture FID 196.6 / relight FID 103.7, and a 23-professional-modeller study rates it 3.69/5 overall. NaTex's table has RomanTex/MaterialMVP as the strongest open baselines at cFID 24.78, CMMD 2.191, LPIPS 0.121 (albedo-only comparison).

### The NC tier — capable, and firmly out of the shipping path
**UniTEX** (CVPR'26, HKUST) is technically the most interesting of these: it abandons UV entirely for continuous **Texture Functions** mapping any 3D point to colour by surface proximity, topology-independent, and its output is described as *illumination-free albedo-like diffuse colour*. Table 1 on generative meshes: CMMD 0.826, FID_CLIP 16.03, CLIP 0.808, LPIPS 0.090, 65.9% user preference, beating Hunyuan3D-Paint, Paint3D, TexPainter, TexGaussians. But the shipped checkpoints are **FLUX.1-dev LoRAs**, and FLUX.1-dev is the **FLUX [dev] Non-Commercial License** — Apache-2.0 on the wrapper code does not launder that. **Eval-only at best.**

**LumiTex** (ICLR'26) is the paper that most precisely names our defect — *"existing methods often produce diffuse maps with baked-in lighting"* — and it beats Hunyuan3D-2.1 on every metric (texture FID 160.8 vs 196.6; relight FID 99.6 vs 103.7; 4.48 vs 3.69 in the 23-modeller study) via lighting-aware material attention over shared illumination priors. Its own repo is admirably honest: *"This project also uses third-party components with non-commercial license: FLUX model, Tencent Hunyuan3D-2.1 rendering code."* **Double-tainted: NC and territory. Eval-only.** It is, however, the best available reference implementation of *how* to do delit generation, and the best source of a benchmark protocol.

**MatLat** (CVPR'26 Highlight, KAIST) ships checkpoints under **CC BY-NC 4.0** — explicitly NC — and is text+geometry conditioned rather than image-conditioned, so it would not carry our concept image anyway.

**TEXGen** is a different failure: SIGGRAPH Asia 2024 Best Paper Honourable Mention, 700M params diffusing albedo **directly in UV space** (architecturally the cleanest answer to cross-view consistency), 24 GB inference — but the GitHub API reports **`license: null`**. No licence file means all rights reserved, which is *more* restrictive than NC. Unmaintained since 2024-12-18. **Unusable.**

**NaTex** (CVPR'26, Tencent Hunyuan + CUHK) is the current research frontier — texture as a dense colour point cloud, geometry-aware VAE at >80× compression plus a multi-control DiT, trained from scratch on 3D data, **albedo-only output** with an illumination-invariant loss, beating RomanTex/MaterialMVP (cFID 21.96 vs 24.78, CMMD 2.055 vs 2.191, LPIPS 0.102 vs 0.121). **No code or weights released.** Being Tencent Hunyuan, expect the same territory clause if they ever ship. Watch item only.

**Meta AssetGen 2.0** — TextureGen exists and is deployed inside Meta Horizon; **no weights released**, no path to local use. Dead end.

### The permissive-but-doesn't-fix-the-defect tier
**MV-Adapter** is genuinely clean — Apache-2.0 code *and* Apache-2.0 weights, six variants including text-geometry-to-MV and image-geometry-to-MV on SDXL, 10–16 GB — and it is the best-licensed geometry-conditioned MV generator available. But it emits **shaded RGB**, i.e. it is architecturally the same class as our current Qwen-Image stage. Swapping to it would improve view consistency and change nothing about the baked-lighting ghost. **Step1X-3D**'s texture module (Apache-2.0, SDXL-based, geometry-conditioned) is in the same bucket — LumiTex classifies it under "texture-only", not PBR. **SyncMVD** (MIT) is text-prompt-driven shaded RGB from 2023, wants <40k faces and clean non-overlapping UVs; superseded.

**Paint3D** deserves a second look despite its age. CVPR 2024, **Apache-2.0**, and it is the one older method whose *entire design goal* is our defect: a two-stage UV-space diffusion that produces **"high-quality, lighting-less, and diverse 2K UV texture maps"**, with a UVHD refinement model trained specifically to strip illumination artefacts. UV-space native means no blend seam and no cross-view inconsistency by construction. It is weaker than the 2025–26 field on raw fidelity (it loses to UniTEX and Hunyuan-Paint in every table it appears in) and has been unmaintained since April 2024. As a *reference* for the UV-space delit approach, and as a zero-licence-risk fallback, it is worth keeping on the list.

**FlashTex** (Roblox, ECCV'24 Oral, **Apache-2.0**, weights on HF as `kangled/lightcontrolnet`) disentangles lighting from reflectance via a LightControlNet that takes desired lighting as a conditioning image, outputting `texture_kd.png` plus roughness/metallic/normal. Clean licence, correct goal — but it is **text-prompt driven**, not image-conditioned, so it cannot carry our concept image, and it is per-mesh optimisation rather than feed-forward. The *LightControlNet idea* (condition on lighting explicitly so the model stops guessing it) is the transferable part.

### Commercial APIs — clean by contract, if local inference is negotiable
**Meshy** supports uploading your own mesh, offers an explicit **"Remove Lighting" delighting toggle** at 2K/4K and applies it automatically at 8K, and paid plans grant full commercial rights (free tier is CC BY 4.0, attribution required). **Tripo**'s OpenAPI prices texture and mesh-editing tasks separately at ~$1/100 credits with commercial use included. No VRAM problem, no licence archaeology, per-asset cost and no reproducibility. Listed for completeness — this is a scope decision, not a technical one.

## 3. Shortlist

**Before any of this: one cheap probe should run first.** Every "is it delit?" claim above rests on architecture reading, not measurement. Take one prop already in the pipeline, texture it with the top two candidates, render the albedo under two opposed environment lights, and difference them. If the ghost survives, the candidate is wrong regardless of its FID. That probe costs an afternoon and is the instrument that should decide, not this brief.

**1 — TRELLIS.2 texturing pipeline** (with nvdiffrast swapped out)
- **Outcome 8/10.** The only permissive candidate that is natively 3D-consistent *and* material-space by construction; predicts BaseColor as a PBR channel rather than painting RGB. Correct integration surface — mesh + image, geometry untouched.
- **Confidence 5/10.** Evidence is MIT licence text (verified on repo and HF card), a documented texturing entry point, and training-data reasoning. **No published delighting benchmark, and v1 had a real baked-shadow complaint (issue #199).** Low-VRAM claims come from SEO tutorial blogs, not measurement. Raise it with the two-light albedo probe above.
- **Cost.** Setup: high — nvdiffrast must be replaced before anything ships (Stable3DGen is the worked precedent, and it is already in our tree). VRAM: 24 GB official; needs the GGUF/fp8 ComfyUI path or equivalent for a 3080 Ti. Runtime: seconds on H100, unmeasured on 12 GB — expect low minutes per prop.

**2 — Material Anything as a delighting/PBR stage on the current pipeline**
- **Outcome 6/10.** Doesn't beat a native-3D generator on fidelity, but it is *additive* — keeps Qwen-Image and the atlas blend, attacks only the defect. Lowest-disruption option by a wide margin.
- **Confidence 6/10.** Evidence: MIT licence, weights released, dependency list verified clean of nvdiffrast/kaolin, and the paper explicitly names "generated objects with unrealistic lighting" as a target class with a confidence-mask mechanism for it. Against that: baselines are all 2023–24, never benchmarked vs the modern field, and it *reweights* trusted lighting rather than provably removing it.
- **Cost.** Setup: low-moderate (SD2.1-class + Blender 3.2.2 pin). VRAM: comfortable in 12 GB. Runtime: unstated, per-view + UV refine — expect ~1–3 min/prop.

**3 — MVPainter**
- **Outcome 6/10.** Strong texture quality with clean Apache-2.0 on both code and weights, and no evident upstream taint. But PBR is post-hoc extraction from shaded views — structurally the same bet we are already losing, with a better estimator.
- **Confidence 6/10.** Best-targeted evidence in the brief: an Elo bake-off run **on Hi3DGen geometry specifically**, where it beats Hunyuan3D-2.0 by ~290 Elo and MV-Adapter by ~120–155, corroborated by a human study. Discounted for VLM-judge methodology, n=5 humans, and a Hunyuan **2.0** baseline. Rasterizer dependency unverified.
- **Cost.** Setup: moderate (3B MV model + IDArb extractor, two stages). VRAM: unstated for 3B — likely tight but feasible at reduced views. Runtime: unmeasured.

**Deliberately not shortlisted:** Hunyuan3D-2.1 Paint / RomanTex / MaterialMVP (EU outside the grant), UniTEX, LumiTex, MatLat (NC), TEXGen (no licence at all), NaTex and Meta AssetGen (no weights). Several of these are the quality leaders — that is exactly why the licence questions below matter.

## 4. Flagged for the user's legal read

1. **Tencent Hunyuan territory clause (2.0 and 2.1).** The grant excludes the EU, UK and South Korea *from the territory itself*. Does an EU-domiciled licensee hold any licence? This gates the current quality leader and everything derived from it (RomanTex, MaterialMVP, LumiTex's Hunyuan rendering code, and any future NaTex release).
2. **Whether the standing "TRELLIS = NC/eval-only" ruling should be narrowed to "nvdiffrast = NC".** The weights are MIT on both repo and model card, and Hi3DGen — already in our shipping path — is a TRELLIS derivative that removed the NVIDIA deps for exactly this reason. If the ruling stands as written, our own mesh stage is implicated; if it narrows, TRELLIS.2 unblocks.
3. **nvdiffrast contamination sweep.** NVIDIA Source Code License (1-Way Commercial) is non-commercial for everyone but NVIDIA. It is the default UV-baking rasterizer across this entire field. Any candidate adopted needs its rasterizer audited, not just its model card — verified clean only for Material Anything so far; **unverified for MVPainter**.
4. **Apache-2.0 wrappers over NC weights.** UniTEX (Apache code, FLUX.1-dev LoRA) and LumiTex (Apache code, self-declared NC deps) show the pattern: the repo badge is not the licence that governs. Assume weights need separate verification for every candidate.
5. **TEXGen has no licence file.** `license: null` on the GitHub API — all rights reserved, stricter than NC.
6. **Commercial API route (Meshy/Tripo)** is a scope decision, not a technical one — clean commercial rights by contract on paid tiers, free tiers CC BY 4.0 with attribution.

**Evidence hygiene note:** the `trellis2.app` / `trellis3d.net` / `hunyuan3d.cc` / `3daistudio.com` family are affiliate/SEO sites, not practitioner reports; they are the *only* source for the 6–12 GB low-VRAM claims and for "TRELLIS 2 has room to improve on texturing", and are weighted accordingly. All licence facts above come from raw LICENSE files, GitHub API, or HF model cards; all benchmark numbers come from the papers' own tables — which means each is reported by a party with an interest in winning it.
