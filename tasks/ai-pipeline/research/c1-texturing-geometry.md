# C1 — Texturing existing geometry: incumbent vs. named candidates vs. 2026 SOTA

Research date: 2026-07-21. Every license clause, dependency, star count, and timing number
below is sourced from a live WebSearch/WebFetch on this date against primary sources (raw
`LICENSE` files, `requirements.txt`, GitHub's own repo-metadata API, HF model-card API, arXiv
abstracts/HTML) wherever a primary source exists; anywhere a secondary source (a blog, an
aggregator, a WebSearch summary) is the only thing found, it is labeled **[secondary]** inline
and never used as the sole basis for a Blocked/Clear licensing call.

**Verification pass (2026-07-21, orchestrator).** Every Blocked ruling was re-checked against raw
bytes with a plain HTTP client rather than a summarizing fetch: nvdiffrast's NC clause,
FlexPainter's `requirements.txt` pin, Hunyuan3D-2's territory clauses, and `license: null` on
MVPaint/TEXGen all confirmed as written. Two gaps the research pass left open were closed, and
**one of them reversed a ruling — MVPainter is Blocked, not eval-only** (§ MVPainter). Everything
below reflects the post-verification state.

**Gap-check pass (2026-07-21, orchestrator).** The passes above only ever asked "does candidate X
support *our* base?" They never asked whether a cross-view mechanism exists for **any** DiT. It
does, it is already wired into our own architecture family inside ComfyUI core, and the one
checkpoint that can drive it is unreleased — see § Gap-check.

**Framing, stated up front**: this bullet was scoped as "multiview depth-reprojection vs.
MVPainter/FlexPainter/MV2UV/SyncMVD/Paint3D/TEXTure/MV-Adapter." Having read all seven, the
honest shape of the answer is not "which one do we swap in" — it is **"the incumbent's actual,
measured problem (A6.3's independent-per-view generation) is a narrow mechanism gap, and none of
the seven named tools is adoptable as a drop-in fix for it."** Two of the seven are outright
Blocked on licensing or a dependency chain (**FlexPainter** and **MVPainter** — the latter
confirmed in the verification pass, see below), as are the two closest 2026-generation relatives
this pass surfaced (Hunyuan3D-Paint, MVPaint). Three more are clean
but architecturally frozen to SD1.5/SDXL-era UNets (SyncMVD, Paint3D, TEXTure) and cannot be
grafted onto our Z-Image, cfg-1, ControlNet-Union stack without a from-scratch reimplementation.
MV2UV doesn't exist as code yet. Only **MV-Adapter** is both clean and closely relevant — and
even it requires retraining its adapter against Z-Image's DiT architecture rather than loading
as-is, because it ships trained only for SDXL/SD2.1 UNets.

---

## Verdict up front

**Do not adopt any of the seven named tools, or the bonus 2026 candidates this pass added
(Hunyuan3D-Paint, MVPaint, TEXGen), as an all-or-nothing pipeline replacement. Close A6.3's measured gap (independent per-view generation)
with a same-day mechanism change inside `prop_texture.py` itself, borrowing the *idea* — not the
code — of TEXTure's/Paint3D's sequential, already-painted-conditioned generation.**

Concretely: `generate_views()` (`scripts/ai-pipeline/prop_texture.py:348-398`) currently fires
four fully independent ComfyUI jobs (`seed * 100 + i`, no shared state) — this is the entire root
cause A6.3 diagnosed. The cheapest fix that is provably compatible with our exact stack (Z-Image
Turbo, cfg 1, `Z-Image-Turbo-Fun-Controlnet-Union`) is **sequential img2img conditioning**: render
view 0 as today, then for views 1-3, reproject the growing texture back onto that view's depth
render (the same `blend_views()` math already does this reprojection, just at the end instead of
between views) and feed it into the ComfyUI graph as a low-denoise img2img source alongside the
depth ControlNet, so each new view starts from what the previous views already agreed on instead
of hallucinating independently. This is TEXTure's and Paint3D's core idea (§ "TEXTure",
§ "Paint3D" below) — sequential inpainting conditioned on the already-textured render — but
implemented with nodes ComfyUI already ships (`VAEEncodeForInpaint`/img2img, already confirmed
present in ComfyUI core per `a4-control-tooling.md` §5), not by adopting either repo. It requires
no new model, no new license exposure, and no VRAM increase (one view generates at a time, same
as today) — it is a change to workflow wiring and to `blend_views()`'s call order, estimated at
**a day, not a research project.**

**MV-Adapter is the correct second step, not the first.** Its whole architectural point — a
frozen base UNet plus a duplicated-attention adapter that generates all views in one joint pass —
is a general, principled solution to exactly A6.3's problem, is Apache 2.0 clean, is actively
maintained (pushed 2026-06-26, [github.com/huanngzh/MV-Adapter](https://github.com/huanngzh/MV-Adapter)),
and already ships dedicated Text2Texture/Image2Texture pipelines. But the released weights are
trained only against SDXL's and SD2.1's UNet attention layout — there is no Z-Image (DiT/S3-DiT)
variant, and porting the adapter's training recipe to Z-Image is a multi-week research project
(new adapter architecture, new training run, new dataset), not an integration task. Until that
research happens (or someone else publishes it), MV-Adapter is a pointer for a future pass, not
something to adopt this quarter.

**What would falsify this**: (1) the sequential img2img experiment, run on the same candelabra
mesh A6.3 used, fails to fix the black/cream candle flip — meaning the failure isn't actually
"independent generation" but something else the earlier report misdiagnosed; (2) MV-Adapter's
SD2.1 variant, tried head-to-head on our own dark-painterly register (a same-day GPU check, no
retraining needed — the SD2.1 weights already exist), turns out to beat Z-Image on quality and
consistency by enough margin that reverting the texture stage specifically to SD2.1 (keeping
Z-Image elsewhere) is worth the quality trade A5b already measured against SDXL-family bases.

**The bigger caveat, stated because this bullet is explicitly judged against F1**: every
candidate in this report — including the incumbent, including MV-Adapter — solves at best
**cross-view** consistency within one generation. None of them solve **cross-variant**
consistency across the ~150 armor variants this plan needs. A joint-attention adapter guarantees
that a single candelabra's four views agree with each other; it guarantees nothing about whether
variant #47 and variant #112 of the same garment shell read as the same art book. That is a
property of the prompt/LoRA/seed discipline layered on top (A3/A5b/A6.3's own findings), not of
any texturing *mechanism* surveyed here — and it is the one axis where F1's deterministic node
graphs win by construction, not by tuning. If F1 turns out competitive on quality per shell, this
report's honest read is that it wins the 150-variant question outright, and generative texturing
survives only for the smaller subset of hero/unique props where per-item hand-tuning is
affordable.

---

## Options table

| Option | License (own repo) | Hard dependency risk | VRAM (native fit on 12 GB?) | Wall-time/iter | Maturity | Verdict |
|---|---|---|---|---|---|---|
| **Incumbent** (multiview depth-reprojection, Z-Image) | Apache 2.0 (Z-Image + ControlNet) | none new | Yes, proven | ~3 min / 4 views | Production, shipping today | Baseline |
| TEXTure | MIT | none (Kaolin Apache-2.0, SD2-depth RAIL++-M) | Yes (2023-era, tiny by 2026 standards) | 90 s | Stale (2023), historically foundational | Clean, but superseded, needs adapting to Z-Image |
| Paint3D | Apache 2.0 | none | Yes | 60 s | Aging (2024), Apache-clean | Clean, superseded, SD1.x/ControlNet only |
| SyncMVD | MIT | none (PyTorch3D BSD, xatlas MIT) | Yes | 50 s | Aging (2023/24) | Clean, superseded, oversmooths detail |
| MV-Adapter | Apache 2.0 | none | Yes (SD2.1 variant, <10 GB) / marginal (SDXL variant) | 18-33 s | Active, ICCV 2025, best-shaped of the group | Clean, best mechanism, wrong base architecture |
| MVPainter (MV-Painter) | Claims Apache 2.0 — **verified to redistribute Tencent's NC, EU-excluded code with the license header stripped** | **Vendored Hunyuan3D-2 modules (`rasterizer.cpp` byte-identical)** + 40 GB VRAM floor | **No** — needs 40 GB, rented-compute only | Not benchmarked | Young (Apr-Jul 2025), real weights | **Blocked — NC + EU-excluded upstream, mis-relicensed** |
| FlexPainter | MIT (own repo) | **Direct pip dependency on `NVlabs/nvdiffrast`** (NVIDIA Source Code License, non-commercial) **+** base model is **FLUX.1-dev** (BFL non-commercial license) | Not documented | Not documented | Young (2025), 44 stars | **Blocked — doubly** |
| MV2UV | Unknown — **no code released** | n/a | n/a | n/a | Too new (CVPR 2026, preprint Mar 2026) | Cannot be adopted; nothing to evaluate yet |
| Hunyuan3D-Paint (Hunyuan3D-2/2.1) | Tencent Hunyuan 3D Community License (custom, restrictive) | none beyond the license itself | ~12-16 GB w/ offload | Not independently benchmarked | Production-grade, most cited 2025-2026 turnkey option | **Blocked — EU/UK/South Korea excluded territory** |
| MVPaint (3DTopia) | **No license file — GitHub API confirms `license: null`** | inherits MVDream/SyncMVD/Paint3D tooling | Not documented | Not documented | Real, CVPR 2025, "preliminary" release | **Blocked by default copyright** until a license is added |
| TEXGen | **No license file — `license: null`** | n/a (feed-forward, no multiview stage) | Not documented (700M-param model) | Not documented | SIGGRAPH Asia 2024, stale since Dec 2024 | **Blocked by default copyright**; also architecturally unlike the rest (native UV-space diffusion) |

---

## The incumbent, for reference (not re-derived — see the brief's baseline)

`prop_texture.py --strategy multiview`: 4 independent ControlNet-depth generations (Z-Image
Turbo 6B, Apache 2.0, cfg 1, 8 steps) at azimuth 0/90/180/270°, elevation 15°, 1024², reprojected
into a Smart-UV atlas with facing-weighted (`MV_WEIGHT_EXPONENT = 2.0`), occlusion-tested
blending (`prop_texture.py:480-518`). Measured `blend_coverage ≈ 0.674` on the candelabra
reference asset. Normal map is a real Cycles high-to-low bake; MR is two declared scalar
constants. The measured, load-bearing weakness this whole bullet responds to: the four views are
`seed * 100 + i`, no shared latent or conditioning state, and per-view material disagreement
survives the facing-weighted blend intact (`a6-3-material-separation.md`) — this is precisely the
"cross-view consistency" axis every candidate below is graded on.

---

## Per-option assessments

### TEXTure — Text-Guided Texturing of 3D Shapes

**Extended description**: the foundational paper in this whole space (Feb 2023, Technion/Tel Aviv
University). Iteratively paints a mesh from a sequence of camera viewpoints using a depth-to-image
diffusion model, classifying each rendered pixel into a "trimap" of generate/refine/keep zones so
later views respect what earlier views already painted.
[arXiv:2302.01721](https://arxiv.org/abs/2302.01721) ·
[github.com/TEXTurePaper/TEXTurePaper](https://github.com/TEXTurePaper/TEXTurePaper).

**Underlying technique — the mechanism this report cares about most**: **sequential inpainting
conditioned on the already-textured render.** View *i*'s generation is seeded from the actual
rendered pixels of views *0..i-1* reprojected onto view *i*'s camera, with a trimap mask telling
the diffusion sampler which regions must be kept, which may be refined, and which are genuinely
new. This is architecturally the simplest mechanism of any candidate in this report, and the one
most directly transplantable into our own reprojection code (see Verdict).

**License + IP terms**: **MIT**, confirmed via raw fetch of
[github.com/TEXTurePaper/TEXTurePaper/blob/main/LICENSE](https://github.com/TEXTurePaper/TEXTurePaper/blob/main/LICENSE).
Dependencies: `kaolin==0.11.0` (NVIDIA Kaolin, **Apache 2.0**, confirmed via
[api.github.com/repos/NVIDIAGameWorks/kaolin](https://api.github.com/repos/NVIDIAGameWorks/kaolin)
— permissive, not the nvdiffrast trap), base model `stabilityai/stable-diffusion-2-depth` under
**CreativeML Open RAIL++-M**, which permits commercial use subject to content-based (not
revenue-based) use restrictions — the same license family SDXL itself ships under, already
accepted for this pipeline. **Clean for commercial shipping**, nothing blocked.

**Real cost**: free, local, no rented compute needed — 2023-era SD1.x/2.x-class compute
requirements are trivial against a 12 GB card by 2026 standards.

**VRAM/compute**: fits 12 GB comfortably (not independently re-benchmarked here; SD2-depth alone
is a fraction of Z-Image's footprint).

**Wall-time per iteration**: **90 s**, per MV-Adapter's own comparison table, Table 3, RTX 4090
([arXiv:2412.03632](https://arxiv.org/abs/2412.03632)) — a secondary source's number for this
specific model, not independently re-timed in this pass, but a primary paper's own reported
figure rather than a blog estimate.

**Pros**: cleanest license stack in this report; the one mechanism most directly reusable inside
our existing Blender/ComfyUI harness without adopting the repo; historically the reference every
later method (Paint3D, SyncMVD, MVPaint) is benchmarked against.

**Cons**: worst quality of the group on the same benchmark table (FID 56.44, KID 61.16×10⁻⁴,
both worst-or-second-worst — only Text2Tex is worse); "the stochastic nature of the generation
process can cause many inconsistencies when texturing an entire 3D object" per the paper's own
framing; no PBR (albedo-only, same limitation our own MR-as-constant approach already accepts);
built entirely around a real-CFG SD2.x UNet — the repo's code is not directly runnable against
Z-Image without a rewrite.

**How much worse than a human artist, and where**: worse specifically at maintaining one
material's identity across an object's parts (exactly A6.3's candle problem) and at any
asymmetric or head-bearing subject — general community consensus (echoed across TEXTure's
successor papers, not independently re-verified against our own meshes in this pass) is that it
suffers the "Janus problem" (front/back conflation) more severely than any later method here.

**1-2 shipped games at comparable quality**: none found. TEXTure predates the current wave of
commercial AI-3D tools (Meshy launched 2023, Tripo/Rodin later) and none of the search results
in this pass name it as a component of any specific shipped title. The honest comparator is
"pre-2024 hobbyist ComfyUI texture experiments" — a hand quality tier below even today's
budget-tier commercial APIs, not a shipped-game reference point.

**Maturity**: production-proven **as a research artifact** (799 stars, real usage as a baseline
in every later paper) but **stale** — last pushed December 2023, no maintenance since
([api.github.com/repos/TEXTurePaper/TEXTurePaper](https://api.github.com/repos/TEXTurePaper/TEXTurePaper)).

---

### Paint3D — Paint Anything 3D with Lighting-Less Texture Diffusion Models

**Extended description**: CVPR 2024, Tencent-affiliated (Zeng et al.). Coarse-to-fine: a
depth+UV-position ControlNet generates view-conditional images, then two dedicated diffusion
models (UV Inpainting, UVHD) refine directly **in UV space** to remove baked illumination and
fill unseen regions. [arXiv:2312.13913](https://arxiv.org/abs/2312.13913) ·
[github.com/OpenTexture/Paint3D](https://github.com/OpenTexture/Paint3D).

**Underlying technique**: hybrid — view-space generation first (similar category to the
incumbent), then a genuine **UV-space diffusion** pass for refinement/inpainting. This is the one
named-candidate-adjacent method that demonstrates the "UV-space diffusion" mechanism the brief
asks about directly, as a second stage rather than the whole pipeline.

**License + IP terms**: **Apache 2.0**, confirmed via raw fetch of the LICENSE file (full text
quoted, standard Apache 2.0 boilerplate, nothing appended) —
[raw.githubusercontent.com/OpenTexture/Paint3D/main/LICENSE](https://raw.githubusercontent.com/OpenTexture/Paint3D/main/LICENSE).
Dependencies (`environment.yaml`): SD1.x-era stack, `xatlas==0.0.7` for UV unwrapping — **no
nvdiffrast, kaolin, or pytorch3d at all**, the lightest dependency footprint of any candidate in
this report.

**Real cost**: free, local.

**VRAM/compute**: fits 12 GB trivially (SD1.x-era footprint, PyTorch 1.12/CUDA 11.3 stack).

**Wall-time per iteration**: **60 s**, per the same MV-Adapter Table 3
([arXiv:2412.03632](https://arxiv.org/abs/2412.03632)).

**Pros**: clean Apache license end to end, lightest dependency chain of any candidate, and the
only one of the older methods with an explicit, working UV-space refinement stage — directly
relevant if the sequential-img2img fix (Verdict) needs a second pass to clean up seams.

**Cons**: **"performance is highly related to UV wrapping or texture complexity"** — practitioner
comparisons find it produces "decent results" on simple prompts (copper cup, black boots) but
"artifacts and seams" on complex ones (Santa, eagle) **[secondary, aggregated WebSearch summary,
not independently re-run against our meshes]**; on the same FID/KID table it beats TEXTure/
Text2Tex but trails SyncMVD (FID 44.38 vs SyncMVD's 36.13); stale since November 2024.

**How much worse than a human artist, and where**: specifically worse on complex, multi-material
subjects — the exact shape of our armor-variant problem (a garment shell with several distinct
material zones: leather, metal trim, cloth) is closer to "Santa"/"eagle" complexity than "copper
cup" in the practitioner reports found.

**1-2 shipped games at comparable quality**: none found by name. Its lineage (Tencent-affiliated
authors) sits adjacent to Tencent's own Hunyuan3D-Paint line, which is production-grade and does
have real commercial deployment claims (see below) — Paint3D itself is not documented as directly
shipped in any title.

**Maturity**: real, peer-reviewed, 804 stars, but aging —
[api.github.com/repos/OpenTexture/Paint3D](https://api.github.com/repos/OpenTexture/Paint3D)
confirms last push 2024-11-05, no activity since.

---

### SyncMVD — Text-Guided Texturing by Synchronized Multi-View Diffusion

**Extended description**: Nov 2023 (Liu, Yuxin et al). Shares denoised latent content across all
views *at every denoising step* rather than generating each view independently or sequentially.
[arXiv:2311.12891](https://arxiv.org/abs/2311.12891) ·
[github.com/LIU-Yuxin/SyncMVD](https://github.com/LIU-Yuxin/SyncMVD).

**Underlying technique — direct answer to "by what mechanism"**: **synchronized/joint
denoising.** At each diffusion step, all views are projected onto a shared texture-space
buffer, aggregated, and re-projected back into each view's latent before the next step — the
views are never independent generations at any point in the sampling process, which is the
strongest possible answer to A6.3's exact failure mode (four generations that never talk to each
other). This is architecturally the ancestor of MV-Adapter's joint approach, implemented as a
sampling-time trick on a frozen SD1.5 rather than as a trained adapter.

**License + IP terms**: **MIT**, confirmed via raw fetch
([github.com/LIU-Yuxin/SyncMVD/blob/main/LICENSE](https://github.com/LIU-Yuxin/SyncMVD)).
Dependencies: **PyTorch3D** (BSD-3-Clause, permissive) for UV-space rendering, **xatlas**
(MIT, optional auto-unwrap), base model `runwayml/stable-diffusion-v1-5` (CreativeML Open
RAIL-M, commercially permitted) + depth/normal ControlNets. **No nvdiffrast, no restrictive
dependency anywhere in the chain.**

**Real cost**: free, local.

**VRAM/compute**: fits 12 GB trivially (SD1.5-era footprint).

**Wall-time per iteration**: **50 s**, per MV-Adapter's Table 3 — the fastest of the three
2023/2024-era baselines on that same benchmark.

**Pros**: cleanest mechanism-to-problem match of any older candidate (literally built to solve
cross-view disagreement); best FID/KID of the three pre-2025 baselines (36.13/42.28 vs Paint3D's
44.38/47.06 and TEXTure's 56.44/61.16); simple, well-documented dependency chain.

**Cons**: **"tends to produce textures that are excessively smooth, resulting in a loss of
intricate detail"** and **"severe Janus problems on generating objects with heads"**
**[secondary, aggregated WebSearch summary of practitioner/paper comparisons, not independently
re-run here]** — the best-FID number and the "oversmoothing" complaint are in real tension, and
this report did not resolve which one dominates for our specific dark-painterly, grimy-material
register. Explicit, documented mesh constraints: **avoid flipped face normals and overlapping
UVs, keep triangle count under ~40,000** — worth checking against Hi3DGen output topology before
any hands-on test (flagged as a GPU-run item, not resolvable by reading). `.glb` input is
explicitly called "unstable/experimental."

**How much worse than a human artist, and where**: the oversmoothing complaint is the specific,
concrete risk for this project — worn/grimy/weathered material detail (rust, wax drips, fabric
wear) is exactly the kind of high-frequency surface information a synchronized-denoising blur
would erase first.

**1-2 shipped games at comparable quality**: none found. Same category as the other pre-2025
methods — a research baseline other papers benchmark against, not a documented shipped-game
component.

**Maturity**: real, 181 stars, last pushed 2025-03-18
([api.github.com/repos/LIU-Yuxin/SyncMVD](https://api.github.com/repos/LIU-Yuxin/SyncMVD)) — the
freshest-maintained of the three pre-2025 baselines, though still architecturally frozen to SD1.5.

---

### MV-Adapter — Multi-view Consistent Image Generation Made Easy

**Extended description**: ICCV 2025 (huanngzh et al). The first **adapter-based** (not
full-fine-tune) solution for multi-view generation: a plug-in module with duplicated self-attention
and a parallel-attention architecture, layered onto a **frozen** pretrained T2I UNet, trained on
far fewer parameters than a full fine-tune (127M trainable params for the SD2.1 variant, vs.
Era3D's 993M). [arXiv:2412.03632](https://arxiv.org/abs/2412.03632) ·
[github.com/huanngzh/MV-Adapter](https://github.com/huanngzh/MV-Adapter).

**Underlying technique**: **cross-view attention sharing via a trained adapter**, generating all
views in a single joint forward pass rather than independently or sequentially — architecturally
the most "native multiview" of any candidate here that still fits on a UNet backbone. Ships
dedicated **Text2Texture** and **Image2Texture** pipelines that condition on geometry (camera +
depth/normal) directly, plus a "Genesis Camera" arbitrary-view extension.

**License + IP terms**: **Apache 2.0**, confirmed in `a4-control-tooling.md`'s prior verification
pass and re-confirmed here via
[api.github.com/repos/huanngzh/MV-Adapter](https://api.github.com/repos/huanngzh/MV-Adapter) and
its `requirements.txt` — **no nvdiffrast**, uses `xatlas` for UV unwrapping. Base models are
SDXL and SD2.1, both permissively licensed. **Clean for commercial shipping.**

**Real cost**: free, local.

**VRAM/compute**: **SD2.1 variant fits 12 GB comfortably (<10 GB)**; the SDXL variant needs
**>12 GB** for its joint multi-view batch (all N views held in memory simultaneously for the
shared-attention pass — a real architectural cost difference from our incumbent's strictly
sequential, one-view-at-a-time generation, which is why the incumbent's per-view VRAM footprint
stays low even on a 12 GB card while a joint-attention method's footprint scales with view count).
**[secondary, WebSearch-aggregated figure, not independently re-benchmarked on our own box in
this pass]**

**Wall-time per iteration**: **18-19 s (SD2.1) / 32-33 s (SDXL)** for text- and image-conditioned
texture generation respectively, per the paper's own Table 3, RTX 4090 — by a wide margin the
fastest of every method in this report, incumbent included (our incumbent's ~3 min/4-view number
is not directly comparable, since it includes the ComfyUI server startup + reprojection bake,
not just sampling, but even accounting for that gap MV-Adapter's joint pass is genuinely fast).

**Pros**: best FID/KID of any method on the shared benchmark table (SDXL-Image: FID 27.28, KID
29.47×10⁻⁴ — clear best); fastest; cleanest license; actively maintained (pushed 2026-06-26 per
`a4-control-tooling.md`'s verification); purpose-built Text2Texture/Image2Texture pipelines,
closer to turnkey than any other named candidate; explicitly demonstrated stacking with community
ControlNets and LoRAs on SDXL (its own scribble example uses `xinsir/controlnet-scribble-sdxl-1.0`
— the same publisher as our incumbent's own xinsir depth ControlNet), evidence the SDXL ecosystem
already solves LoRA+ControlNet+multi-view composition together.

**Cons — the one that matters most**: **no Z-Image variant exists.** The adapter's attention
layers are trained against SDXL's/SD2.1's specific UNet block structure; Z-Image is a DiT
(S3-DiT/Lumina2-family) architecture with a fundamentally different attention layout, so the
released weights cannot be loaded against our base at all — this is not a config change, it is a
different-architecture retraining problem. Whether the *method* (duplicated attention, frozen
base) is CFG-agnostic (compatible with our cfg-1 distilled base) was not addressed in any source
found — SDXL/SD2.1 both use real CFG in MV-Adapter's own demos, and no test at cfg=1 was found.
**Flagged as unresolved, not assumed either way.**

**How much worse than a human artist, and where**: best-measured of the group on the shared
metric, but that metric (FID/KID against a photoreal/product-shot-style eval set, inferred from
the paper's own benchmark framing) is not a painterly/dark-fantasy-register test — same caveat
`a5-comparative.md` raised about the base-model Elo table applies here: winning FID does not mean
winning "Zurbarán-register worn iron and cream wax."

**1-2 shipped games at comparable quality**: none found by name, but the closest real production
signal of any candidate in this report: **VAST (the company behind Tripo AI) hosts an official
MV-Adapter Image2Texture demo Space on Hugging Face**
([huggingface.co/spaces/VAST-AI/MV-Adapter-Img2Texture](https://huggingface.co/spaces/VAST-AI/MV-Adapter-Img2Texture))
— a commercial 3D-generation company (Tripo3D) publishing and hosting this exact method is a real,
if indirect, signal that the technique category is production-relevant, not merely academic.
Tripo itself (VAST's product) is used in real, if not necessarily AAA-tier, shipped game
pipelines per general industry commentary **[secondary]** — but that is evidence for the
*category*, not a claim that MV-Adapter's exact weights ship in a specific title.

**Maturity**: **the most production-adjacent of any named candidate** — real adoption signal
(VAST/Tripo hosting), active maintenance, ICCV 2025 peer review, 1,273 stars
(`a4-control-tooling.md`'s prior verification).

---

### MVPainter (MV-Painter) — Accurate and Detailed 3D Texture Generation via Multi-View Diffusion with Geometric Control

**Extended description**: amap-cvlab (Alibaba/Amap), May 2025. Explicitly builds on Hunyuan3D,
IDArb, and MaterialAnything — adds data filtering/augmentation and ControlNet-based geometric
conditioning, and extracts full PBR attributes (not just albedo) from the generated multiview
images. [arXiv:2505.12635](https://arxiv.org/abs/2505.12635) ·
[github.com/amap-cvlab/MV-Painter](https://github.com/amap-cvlab/MV-Painter) ·
[amap-cvlab.github.io/MV-Painter](https://amap-cvlab.github.io/MV-Painter/).

**Underlying technique**: geometry-conditioned (ControlNet-style ) multi-view diffusion, plus a
dedicated PBR-decomposition stage derived from IDArb — this is the only named candidate that
attempts full material-channel (not just albedo) extraction directly from generated views, which
would in principle also solve our declared-constant MR problem (A6.1) rather than just the
albedo cross-view problem (A6.3) — untested here.

**License + IP terms — Blocked. Resolved in the verification pass; this is the most serious
finding in the report.**

The research pass left two questions open (why GitHub's API reports `NOASSERTION` against a
LICENSE that reads as Apache 2.0, and whether the `custom_rasterizer`/`differentiable_renderer`
modules are an independent reimplementation or a copy of Tencent's EU-restricted code). Both were
settled by byte-level fetch and diff.

**1. The `NOASSERTION` discrepancy is benign in itself.** A normalized diff of the raw LICENSE
against canonical Apache 2.0 (`apache.org/licenses/LICENSE-2.0.txt`) shows the body is verbatim
Apache 2.0, with **a 6-line NOTICE header prepended** — which is why GitHub's detector cannot
match it. The header reads: *"Unless otherwise specified, all files in this repository are
licensed under the Apache License, Version 2.0... Files or directories explicitly marked with a
different license are subject to the terms of that specified license."*

**2. That header is what makes the provenance question decisive**, because a full tree listing
([git/trees/main?recursive=1](https://api.github.com/repos/amap-cvlab/MV-Painter/git/trees/main?recursive=1),
188 paths) confirms **`LICENSE` is the only license file in the entire repository** — nothing is
"explicitly marked with a different license." So the repo asserts blanket Apache 2.0 over the
vendored modules. That assertion does not survive a diff:

- `custom_rasterizer/lib/custom_rasterizer_kernel/rasterizer.cpp` is **byte-identical** to
  Hunyuan3D-2's (`sha256:4dc12207b90ad660…`, 6789 bytes, both).
- `differentiable_renderer/mesh_processor.py` is identical **except that MV-Painter has removed
  the 14-line license header**, which in Tencent's original reads: *"Hunyuan 3D is licensed under
  the TENCENT HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT…"*
- `grep -i "tencent\|hunyuan"` finds **no attribution anywhere** in MV-Painter's copies.

This is not an independent reimplementation. It is a verbatim redistribution of Tencent code with
the license notice stripped, relicensed as Apache 2.0 — which the upstream license does not permit
Amap to do. **A downstream user inherits Tencent's restrictions regardless of what MV-Painter's
own LICENSE says**, and those restrictions are (a) **non-commercial** per the stripped header and
(b) **EU-excluded** per the Community License (§ Hunyuan3D-Paint below). Both are dispositive
here, and the standing 2026-07-19 NC ruling applies directly.

Worth stating plainly for the ledger: this is the inverse of the usual trap. The project's
"read the license text, not the tag" discipline assumes the text is authoritative — here the text
is *clean and wrong*, and only a source-level diff exposed it. **A permissive LICENSE file is not
evidence that the code in the repo is the author's to license.**

**Real cost**: local, if the VRAM floor below can be met; otherwise rented compute (a cost line,
per the brief's own framing, not researched further here since VRAM alone likely rules this out).

**VRAM/compute**: **the repo's own INSTALL.md states "at least 40GB GPU memory"** — does not fit
12 GB, does not fit a 24 GB upgrade either. This alone would rule the tool out for local use on
this project's hardware regardless of the license question above.

**Wall-time per iteration**: not documented in any source found in this pass.

**Pros**: full PBR extraction (not just albedo) is architecturally the most complete answer to
this project's texture-channel needs of any candidate; real training code, real released weights,
246 stars.

**Cons**: **Blocked** — redistributes non-commercial, EU-excluded Tencent code under an Apache
claim upstream does not permit (verified by diff, above). Independently, a 40 GB VRAM floor rules
out local use even on a 24 GB upgrade. Not independently quality-benchmarked against any other
candidate in any source found.

**How much worse than a human artist, and where**: not assessable — no hands-on practitioner
account or independent benchmark was found for this specific tool.

**1-2 shipped games at comparable quality**: none found.

**Maturity**: young (first release April 2025, most recent push July 2025 —
[api.github.com/repos/amap-cvlab/MV-Painter](https://api.github.com/repos/amap-cvlab/MV-Painter)),
real weights, low-to-moderate adoption (246 stars), essentially bleeding-edge/barely-used outside
its own publication.

---

### FlexPainter — Flexible and Multi-View Consistent Texture Generation

**Extended description**: June 2025 (StarRealMan et al). Builds a shared conditional embedding
space across text/image/reference-image inputs, generates all views jointly via a grid
representation, and adds a "view synchronization and adaptive weighting module" during sampling
plus a separate 3D-aware texture-completion + enhancement model for final seamless output.
[arXiv:2506.02620](https://arxiv.org/abs/2506.02620) ·
[github.com/StarRealMan/FlexPainter](https://github.com/StarRealMan/FlexPainter).

**Underlying technique**: hybrid of "native multiview base" (grid-generated joint views) and
"synchronized sampling" (an explicit consistency module during diffusion) — mechanistically the
most sophisticated named candidate, on paper.

**License + IP terms — Blocked, on two independent grounds**:
1. The repo's own `requirements.txt`
   ([raw.githubusercontent.com/StarRealMan/FlexPainter/main/requirements.txt](https://raw.githubusercontent.com/StarRealMan/FlexPainter/main/requirements.txt))
   pins `git+https://github.com/NVlabs/nvdiffrast` as a **direct pip dependency**. nvdiffrast's
   own license, confirmed by raw fetch of
   [raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt](https://raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt),
   states plainly: **"The Work and any derivative works thereof only may be used or intended for
   use non-commercially,"** with "non-commercially" defined as "for research or evaluation
   purposes only and not for any direct or indirect monetary gain." This is the exact precedent
   the standing NC ruling (2026-07-19) already named. FlexPainter's own MIT license on its own
   code does not launder this — the tool cannot run its own core texturing step (which needs
   nvdiffrast for rasterization/baking) without pulling in an NC-only dependency, so per the
   standing ruling this is Blocked from the shipping asset path regardless of FlexPainter's own
   license file.
2. **Independently**, FlexPainter's base diffusion model is **FLUX.1-dev**, confirmed via its own
   README acknowledgments. FLUX.1-dev ships under BFL's **FLUX.1 [dev] Non-Commercial License**
   (confirmed in the prior `a4-control-tooling.md` pass by fetching
   `raw.githubusercontent.com/black-forest-labs/flux/main/model_licenses/LICENSE-FLUX1-dev`
   directly). A tool whose generative base is itself non-commercial cannot produce commercially
   shippable output at all, independent of any rasterizer question.

Either finding alone is sufficient; both hold simultaneously.

**Real cost / VRAM / wall-time**: not evaluated further — Blocked, per constraint #2, before
these numbers would matter.

**Pros**: architecturally interesting (the shared-embedding, image-based-CFG decomposition idea
for reference-stylization is a real, novel contribution per its abstract) — worth revisiting only
if the authors (or a fork) ever retarget it to an Apache-licensed base and rasterizer.

**Cons**: doubly non-commercial, thin adoption (44 stars).

**How much worse than a human artist**: not assessable — Blocked before this question is
reachable.

**1-2 shipped games**: none, and none possible under current licensing.

**Maturity**: young (June 2025-Dec 2025 pushes), real weights on HF
(`StarYDY/FlexPainter`), low adoption. Bleeding-edge, not production-usable here regardless of
maturity.

---

### MV2UV — Generating High-quality UV Texture Maps with Multiview Prompts

**Extended description**: CVPR 2026 (accepted; presented June 2026), Huawei HiSilicon Linx Lab +
HKUST. Treats already-generated multiview images as semantic *prompts* (not final pixels) for a
dedicated UV-space generative model that simultaneously inpaints unseen regions and resolves
multiview inconsistency directly in UV space.
[arXiv:2603.15436](https://arxiv.org/abs/2603.15436) ·
[CVPR 2026 poster](https://cvpr.thecvf.com/virtual/2026/poster/37737).

**Underlying technique**: **native UV-space diffusion, conditioned on multiview outputs as a
semantic prior rather than as ground truth to be blended** — this is a meaningfully different
mechanism from every other candidate in this report (including Paint3D's UV-refinement stage,
which corrects illumination/gaps but does not treat the multiview images as merely a soft prompt
for a UV-native generator to reconcile). If it holds up, this is architecturally the most direct
answer to "resolve multiview disagreement" of anything surveyed — closer to a principled fix for
A6.3 than sequential conditioning or joint attention.

**License + IP terms**: **cannot be assessed — no code repository was found for this paper in
any search performed in this pass.** One paper-notes aggregator explicitly logged "code
availability: not mentioned"
([github.com/zhaoyang97/Paper-Notes-en](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/CVPR2026/3d_vision/mv2uv_generating_high-quality_uv_texture_maps_with_multiview_prompts.md)).

**Real cost / VRAM / wall-time / pros / cons**: none of these are assessable without released
code or weights.

**How much worse than a human artist**: not assessable.

**1-2 shipped games**: none, and cannot be — no artifact exists to run.

**Maturity**: **too new to have real usage, flagged plainly per the brief's own recency
instruction.** Preprint March 2026, conference presentation June 2026, four months old at
research time and zero adoption signal of any kind. This is a "watch" item for a future research
pass, not an evaluable candidate today.

---

### Hunyuan3D-Paint (Hunyuan3D-2 / 2.1) — the 2026 turnkey SOTA not on the backlog list

**Extended description**: Tencent's texture-synthesis component within the Hunyuan3D-2/2.1/2.5
family — a large-scale multiview texture diffusion model (Hunyuan3D-Paint), with 2.1 adding a
dedicated PBR-material estimation stage on top ("production-ready PBR material" per its own
framing). Widely cited as the current highest-quality open-weight *turnkey* texture-generation
option; on a self-reported CMMD comparison (Hunyuan3D 2.5's own paper) it beats Paint3D (2.400)
and SyncMVD (2.584) with a score of 2.064 (lower better) **[secondary, self-reported by the
authors, not independently reproduced in this pass — treat as an authors'-own-benchmark number,
same caution `a5-comparative.md` applied to every vendor-reported figure]**.
[github.com/Tencent-Hunyuan/Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) ·
[huggingface.co/tencent/Hunyuan3D-2](https://huggingface.co/tencent/Hunyuan3D-2).

**Underlying technique**: multiview diffusion + custom in-house rasterizer/differentiable
renderer for UV baking (its own `custom_rasterizer`/`differentiable_renderer` modules — not
confirmed either way whether these vendor NVlabs/nvdiffrast source internally; no license header
or attribution was found inside those specific subdirectories in this pass, and this was not
resolved).

**License + IP terms — Blocked outright, independent of the rasterizer question**: the repository's
own `LICENSE` file, fetched raw
([raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE)),
is the **Tencent Hunyuan 3D 2.0 Community License Agreement**, which states plainly: **"This
LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA."** This
alone is a hard blocker for a Spain/EU commercial shipping target — constraint #1 in this bullet's
brief. The verification pass confirmed this is stronger than a mere absence of grant: §1(l)
defines "Territory" as worldwide *excluding* the EU/UK/South Korea, and **§3(c) states "You must
not use, reproduce, modify, distribute, or display the … Works, Output or results … outside the
Territory. Any such use outside the Territory is unlicensed and unauthorized."** Use from Spain
is affirmatively prohibited, not merely unlicensed — and the prohibition explicitly reaches
**Output**, so generated textures are covered even if the model ran elsewhere. Separately, the license imposes a 1-million-MAU commercial-request threshold and a clause
prohibiting use of outputs "to improve any other AI model (other than Tencent Hunyuan 3D 2.0 or
Model Derivatives thereof)." One secondary source claimed the project is "fully open source under
Apache 2.0" **[secondary, contradicted by the primary LICENSE file fetched directly above — this
is precisely the "read the text, not the tag/claim" trap the standing ruling exists to catch]**;
a GitHub issue titled "Suggestion: Consider Adopting an Open License"
([github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/50](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/50))
independently corroborates that the community itself does not consider this permissively
licensed today.

**Real cost / VRAM**: full shape+texture pipeline reported at ~12 GB with sequential offloading,
texture stage alone reportedly runnable under 6-16 GB depending on offload configuration
**[secondary, aggregated]** — moot given the license finding.

**Wall-time**: not independently benchmarked in this pass.

**Pros**: by community consensus the current highest-quality open-weight turnkey option in this
category, genuine PBR extraction, actively developed through multiple version bumps (2.0 → 2.1 →
2.5) into 2026.

**Cons**: **EU-excluded license is a hard, dispositive blocker** for this project's stated
commercial-shipping territory. No amount of quality justifies working around this.

**How much worse than a human artist**: moot — Blocked before this question is reachable for our
use case.

**1-2 shipped games at comparable quality**: cited widely as the quality bar other 2025-2026
methods measure themselves against (this report's own comparison table above uses its CMMD score
as the reference point), but no specific shipped commercial game was found naming it directly —
and it could not be shipped by this project regardless.

**Maturity**: **production-proven and the most mature 2025-2026 candidate in this entire report**
— exactly the kind of finding that makes the license blocker sting the most. Worth revisiting only
if Tencent ever changes the EU exclusion, or if this project's shipping territory changes.

---

### MVPaint (3DTopia) — closely related, separately named, separately blocked

**Extended description**: CVPR 2025, explicitly built by combining MVDream + SyncMVD + Paint3D
into one framework: synchronized multi-view generation, spatial-aware 3D inpainting for unseen
regions, and a UV-space refinement/super-resolution stage.
[arXiv:2411.02336](https://arxiv.org/abs/2411.02336) ·
[github.com/3DTopia/MVPaint](https://github.com/3DTopia/MVPaint) ·
[mvpaint.github.io](https://mvpaint.github.io/). Named here because it is easily confused with
"MVPainter" (the actual backlog item) and because it is a closer architectural descendant of
SyncMVD/Paint3D than MVPainter is — worth a dedicated paragraph rather than a schema entry given
the finding below.

**License + IP terms — Blocked by default copyright, not by any explicit restrictive clause**:
GitHub's own repository-metadata API reports the license field as **`null`**
([api.github.com/repos/3DTopia/MVPaint](https://api.github.com/repos/3DTopia/MVPaint)), and a
direct fetch of `LICENSE` at the repo root returned a 404 — **no license file exists at all.**
Under default copyright law, code with no license grant is "all rights reserved" — nobody outside
the authors has any right to use, modify, or redistribute it, commercially or otherwise, until
they add one. This is a starker version of the exact risk pattern constraint #4 warns about (a
tag with no LICENSE file is a risk finding, not clearance) — here there is not even a tag.

**Status otherwise**: real, working, weights available via Dropbox per its README, "preliminary
version for testing" released July 2025, 258 stars, pushed as recently as August 2025. Genuinely
one of the more credible 2025-generation methods on paper (three established prior methods'
strengths combined) — but **legally unusable for a commercially shipped asset today, full stop**,
until the authors publish a license.

**Maturity**: real and recent, but licensing-blocked, not quality-blocked.

---

### TEXGen — a Generative Diffusion Model for Mesh Textures (brief, for completeness)

**Extended description**: SIGGRAPH Asia 2024, Best Paper Honorable Mention (CVMI-Lab / VAST
co-authorship). A 700M-parameter **feed-forward** model — no multiview intermediate stage at
all, generates the UV texture map directly, end-to-end, by interleaving UV-space convolutions
with point-cloud attention. [arXiv:2411.14740](https://arxiv.org/abs/2411.14740) ·
[github.com/CVMI-Lab/TEXGen](https://github.com/CVMI-Lab/TEXGen).

**Why it's here despite not being on the named list**: it is the cleanest example of "native
UV-space diffusion" as a *primary* mechanism rather than a refinement afterthought (Paint3D) or a
future promise (MV2UV) — genuinely the most architecturally distinct mechanism in this whole
report, closing the multiview-consistency question by never having multiple independent views to
disagree in the first place.

**License + IP terms**: **`null`** — GitHub's repository-metadata API confirms no license field
([api.github.com/repos/CVMI-Lab/TEXGen](https://api.github.com/repos/CVMI-Lab/TEXGen)). Same
default-all-rights-reserved status as MVPaint. **Blocked by default copyright** until the authors
add one.

**Status otherwise**: 335 stars, but stale — last pushed December 2024, no activity since, and
now nearly two years old relative to research date without a license ever being added, which
reads as a low-probability-of-ever-being-licensed signal rather than an oversight likely to be
fixed soon.

**Maturity**: real, peer-reviewed, architecturally interesting, but both stale and unlicensed —
not adoptable regardless of quality.

---

## Closing the incumbent's independent-generation gap — mechanisms ranked by cost-to-adopt

This section answers directly: **which candidate mechanisms actually close A6.3's measured gap,
and at what cost to adopt each.**

| Rank | Mechanism | Source | Cost to adopt | Compatible with cfg-1 Z-Image + ControlNet-Union? |
|---|---|---|---|---|
| 1 | **Sequential inpainting conditioned on the already-textured render** | TEXTure / Paint3D's core idea | **~1 day.** Implementable directly in `prop_texture.py`'s `generate_views()`/`blend_views()` using ComfyUI-core img2img/inpaint nodes already confirmed present (`a4-control-tooling.md` §5). No new model, no new license, no VRAM increase (still one view at a time). | **Yes, by construction** — it operates on pixels/masks, not on the base model's attention internals, so it is architecture-agnostic and CFG-agnostic. This is precisely why it is the recommended first move. |
| 2 | **Synchronized/joint denoising (shared latent state across views at every step)** | SyncMVD | **A multi-day-to-multi-week reimplementation.** The *idea* (aggregate-and-redistribute a shared texture buffer mid-sampling) is portable in principle, but SyncMVD's actual code is wired to `diffusers`' SD1.5 sampling loop internals — porting the same trick to Z-Image's DiT sampler in ComfyUI means writing a custom step-callback against a different model family, not swapping a checkpoint. | **Unclear.** The mechanism doesn't obviously require CFG>1 (it manipulates latents between steps, not the CFG combination itself), but no source tests this on a distilled cfg-1 DiT — flagged unresolved, would need a hands-on trial. |
| 3 | **Cross-view attention sharing via a trained adapter** | MV-Adapter | **A genuine research project**, not integration — requires training a new adapter against Z-Image's DiT attention layout from scratch; the released weights are SDXL/SD2.1-only and cannot be loaded against our base. Best mechanism on paper, worst-shaped for "adopt this quarter." | **Unknown** — no test at cfg=1 found anywhere; SDXL/SD2.1 (both real-CFG) are the only demonstrated bases. |
| 4 | **UV-space generative reconciliation of multiview outputs** | MV2UV (no code) / TEXGen (unlicensed) / Paint3D's refinement stage (licensed, real, but a secondary pass, not primary) | Paint3D's specific refinement stage could be studied and reimplemented (same day-to-days cost as #1, since it's "just" a second diffusion pass over the atlas) but no source in this pass characterized how well it holds up as a *standalone* addable stage separate from Paint3D's own coarse generation. MV2UV/TEXGen are not adoptable at all (no code / no license). | Architecture-agnostic in principle (operates on the finished UV atlas), most likely of all four rows to compose cleanly with our existing Blender-side atlas pipeline. |
| 5 | **Full PBR-channel extraction from multiview outputs** | MVPainter's IDArb-derived stage | Not adoptable independent of the whole 40 GB-VRAM, provenance-uncertain MVPainter pipeline — the idea is attractive (would also address A6.1's declared-constant MR gap) but nothing in this pass isolated it as a separable component. | Not assessed — would need its own research pass if pursued. |

**Read plainly**: rank 1 is a this-week fix using tools already in the repo. Everything below it
either needs weeks of ML engineering (ranks 2-3) or isn't adoptable at all today (ranks 4-5's
best instances). The Verdict section above already commits to rank 1 as the next action.

---

## Blocked / eval-only list

| Candidate | Reason | Primary source |
|---|---|---|
| **FlexPainter** | Direct pip dependency on `NVlabs/nvdiffrast` (NVIDIA Source Code License — non-commercial-only, the same precedent as the standing 2026-07-19 ruling) **and** its base model FLUX.1-dev is itself non-commercially licensed. Doubly blocked. | [requirements.txt](https://raw.githubusercontent.com/StarRealMan/FlexPainter/main/requirements.txt), [nvdiffrast LICENSE.txt](https://raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt), [FLUX.1-dev LICENSE](https://raw.githubusercontent.com/black-forest-labs/flux/main/model_licenses/LICENSE-FLUX1-dev) |
| **Hunyuan3D-Paint (Hunyuan3D-2/2.1)** | License text explicitly excludes the EU, UK, and South Korea from the grant. Hard blocker for a Spain-based commercial shipping target, independent of quality (which is otherwise the best in this report). | [raw LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE) |
| **MVPaint (3DTopia)** | No license file exists anywhere in the repository (`license: null` per GitHub's own API; 404 on a direct `LICENSE` fetch). Default copyright applies — nobody has usage rights until the authors publish a license. | [api.github.com/repos/3DTopia/MVPaint](https://api.github.com/repos/3DTopia/MVPaint) |
| **TEXGen** | Same as MVPaint — `license: null`, no LICENSE file found, default all-rights-reserved. | [api.github.com/repos/CVMI-Lab/TEXGen](https://api.github.com/repos/CVMI-Lab/TEXGen) |
| **MVPainter (MV-Painter)** | **Blocked (verification pass).** Its LICENSE is verbatim Apache 2.0 under a NOTICE header, and it is the repo's *only* license file — yet `custom_rasterizer/…/rasterizer.cpp` is **byte-identical** to Hunyuan3D-2's, and `differentiable_renderer/mesh_processor.py` is identical except that the 14-line **"TENCENT HUNYUAN NON-COMMERCIAL LICENSE"** header has been removed, with no Tencent attribution anywhere. Downstream users inherit the NC restriction and the EU exclusion regardless of MVPainter's own LICENSE. Separately 40 GB VRAM. | [raw LICENSE](https://raw.githubusercontent.com/amap-cvlab/MV-Painter/main/LICENSE), [repo tree](https://api.github.com/repos/amap-cvlab/MV-Painter/git/trees/main?recursive=1), [MVPainter `rasterizer.cpp`](https://raw.githubusercontent.com/amap-cvlab/MV-Painter/main/MVPainter/mvpainter/custom_rasterizer/lib/custom_rasterizer_kernel/rasterizer.cpp) vs [Hunyuan3D-2 `rasterizer.cpp`](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/hy3dgen/texgen/custom_rasterizer/lib/custom_rasterizer_kernel/rasterizer.cpp) |
| **MV2UV** | Not blocked — simply doesn't exist as a usable artifact. No code repository found anywhere. | [Paper-Notes-en tracker](https://github.com/zhaoyang97/Paper-Notes-en/blob/main/docs/CVPR2026/3d_vision/mv2uv_generating_high-quality_uv_texture_maps_with_multiview_prompts.md) |

**Clear for adoption on licensing grounds** (none of these are blocked; adoption is gated on other
factors as discussed per-option above): TEXTure, Paint3D, SyncMVD, MV-Adapter.

---

## Gaps and unknowns

- **No painterly/dark-fantasy-register quality test exists for any candidate**, exactly the same
  structural gap `a5-comparative.md` found for base image models. Every FID/KID/CMMD number in
  this report (MV-Adapter's Table 3, Hunyuan3D 2.5's CMMD comparison) is a general-purpose
  photoreal/product-style benchmark, not a worn-material/candlelit-register test. This is not
  fixable by more reading — it needs a hands-on run on our own meshes.
- ~~MVPainter's license-detector discrepancy~~ — **closed in the verification pass.** A
  normalized diff against canonical Apache 2.0 shows a verbatim body under a prepended 6-line
  NOTICE header; that header is precisely why GitHub's detector reports `NOASSERTION`.
- ~~MVPainter/Hunyuan3D-2 code-provenance question~~ — **closed in the verification pass, and it
  reversed the ruling.** `rasterizer.cpp` is byte-identical to Tencent's; `mesh_processor.py` is
  identical minus a stripped NC license header. MVPainter moved from eval-only to **Blocked**.
  **Generalizable lesson for the ledger:** a clean LICENSE file is not evidence that the code in
  a repo is the author's to license. Where a repo says it "builds upon" a restrictively-licensed
  project, diff the vendored modules — the license text alone cannot catch this class of defect.
- **Whether Hunyuan3D-2's own `custom_rasterizer` internally vendors NVlabs/nvdiffrast source**
  was not confirmed either way — no license header was found inside the relevant subdirectories
  via the GitHub web UI in this pass, but this was not exhaustively checked file-by-file. Moot
  for this project given the EU-exclusion blocker already disqualifies Hunyuan3D-Paint outright,
  but worth resolving if the EU restriction is ever lifted or waived.
- **No practitioner account was found for MVPainter or FlexPainter specifically** — both are
  young enough (2025) that no independent hands-on report (Reddit/Discord/blog) surfaced in any
  search performed. Everything reported about them comes from their own paper/README.
- **SyncMVD's documented mesh constraints (avoid flipped normals/overlapping UVs, <40k
  triangles)** were not checked against actual Hi3DGen output topology in this pass — this is
  exactly the kind of thing a GPU run settles in minutes and reading cannot: run
  `prop_cleanup.py`'s output mesh through a manifold/normal-consistency check before assuming any
  of the SD1.x-era tools' documented constraints are met.
- **MV-Adapter's CFG-agnosticism (whether its joint-attention mechanism works at cfg=1) is
  untested anywhere found.** This is the single most load-bearing unknown for whether MV-Adapter
  could ever be retargeted to our exact stack — a real experiment (train or find a toy cfg-1
  adapter variant), not a reading question.
- **The rank-1 "sequential img2img" fix recommended in the Verdict has not been tried.** It is
  this report's own extrapolation from TEXTure's/Paint3D's published mechanism, adapted to our
  existing code — a plausible, cheap experiment, not a verified result. The correct next step per
  this project's own compute-gating discipline is a go-ahead for a bounded GPU smoke test (re-run
  the candelabra case with sequential conditioning, check whether the candle-color flip
  disappears), not more research.
- **Wall-time and VRAM numbers for MVPainter, FlexPainter, and MV2UV are entirely absent** from
  every source found — none of the three has a single independently- or self-reported timing
  figure anywhere in this pass's search results.

---

## Gap-check pass — is there a DiT-native cross-view mechanism?

The research and verification passes shared a blind spot: both asked "does candidate X ship
weights for Z-Image?" Neither asked the portable version of the question — **does a cross-view
consistency mechanism exist for any DiT base at all?** Z-Image is Lumina2-family, so a mechanism
built for another DiT is far closer to reach than one written against an SDXL UNet, and the
answer changes what "retargeting is a research project" is worth.

**Answer: the mechanism exists, is DiT-native, and is already implemented in ComfyUI core for our
own model family — but the checkpoint that drives it has not been released.**

### What the mechanism is on a DiT

MV-Adapter's approach — bolt a duplicated-attention module onto a frozen UNet — has no DiT port
and never will need one. On a DiT the equivalent is **in-context token concatenation**: reference
images are VAE-encoded and appended as extra tokens, and the transformer's *own* native
self-attention performs the cross-image interaction. Alibaba's In-Context LoRA paper
([arXiv:2410.23775](https://arxiv.org/html/2410.23775v1)) states this requires no architecture
modification at all — only training data. That is why no "MV-Adapter for DiT" exists: on this
architecture the adapter is the wrong shape of solution.

### It is already in ComfyUI core, for Lumina2/Z-Image specifically

Verified by reading the source, not by search summary:

- `comfy/ldm/lumina/` (`model.py`, `controlnet.py`) and `comfy/text_encoders/lumina2.py` — our
  architecture family is first-class in core.
- `comfy/model_base.py`: class `Lumina2` consumes `reference_latents` as a `CONDList` plus
  `reference_latents_text_embeds` as `ref_contexts`; **`class ZImagePixelSpace(Lumina2)`**
  inherits it and declares `memory_usage_factor_conds = ("ref_latents",)`.
- `comfy_extras/nodes_zimage.py`: **`TextEncodeZImageOmni`** accepts `image1/image2/image3`,
  VAE-encodes each, and appends them to conditioning as `reference_latents`.

So multi-reference in-context conditioning is plumbed end-to-end for Z-Image today, in the
runtime we already run, with **three** reference slots — which happens to fit a 4-view stage
exactly (view 4 can see views 1–3).

### Why it is not actionable yet

`TextEncodeZImageOmni` targets **Z-Image Omni**, not the `Z-Image-Turbo` checkpoint we run. Turbo
is T2I-only and was not trained to attend to reference tokens. Omni is not published:

- ComfyUI commit *"Support zimage omni base model"* (#11979) landed **2026-01-20** — the code
  anticipates the model.
- HF search for `z-image-omni` returns **0 results**; `Tongyi-MAI` publishes only `Z-Image` and
  `Z-Image-Turbo`.
- ModelScope `api/v1/models/Tongyi-MAI/Z-Image-Omni/repo/files` returns
  `record not found`, while the same call for `Z-Image-Turbo` returns a real file tree.
  (Bare model *pages* 200 for anything, including a deliberately fake path — control-tested, so
  page status is not evidence either way.)

**Watch item, not an adoption.** If Omni ships under Tongyi's usual Apache terms, the incumbent's
independent-view gap closes natively in latent space rather than via the pixel-space workaround.

### Correction to a finding that did not survive verification

A DiT-native in-context framework built on Lumina-Image-2.0 by its own authors —
**Lumina-Accessory** — initially looked like the shortest possible port, and its HF page carries
an `apache-2.0` card tag. **It is not clean.** The GitHub repo
[Alpha-VLLM/Lumina-Accessory](https://github.com/Alpha-VLLM/Lumina-Accessory) reports
`"license": null` from the repo API and has **no LICENSE file at any ref** (`main` and `master`
both 404 on raw fetch; a recursive tree listing contains no file matching `licen*`). The card tag
covers the weights repo; the *framework code* — the part that would have been built inside — is
undeclared, and by this project's own standing rule an undeclared license is Blocked, not
permissive. Repo last pushed 2025-04-25.

This is the same trap as MVPainter, in its milder form: **an HF card tag is not a code license.**
Both must be checked, and they are separate artifacts.

### Negative space — searched, not found

- **MV-Adapter is dead upstream.** Zero commits since 2025-06-26; no issue or PR requesting
  FLUX/SD3/DiT/Lumina support; no fork implementing it. Its own paper
  ([arXiv:2412.03632](https://arxiv.org/abs/2412.03632)) lists DiT support as future work, never
  delivered.
- No multiview/cross-view adapter of any kind for **SD3/SD3.5, PixArt-Sigma, Sana, HunyuanDiT,
  CogView4, or Chroma**.
- No pretrained multiview checkpoint for **Lumina-Image-2.0, Lumina-Next, or Z-Image**.
- Nobody has applied the in-context multiview recipe to a fully-permissive DiT **for texturing**.
  The recipe exists on FLUX.1-dev (NC-tainted: UniTEX, `fourviews-incontext-lora`) and on
  Qwen-Image for single-view camera-angle editing only.
- A June 2026 survey of neural 3D mesh texturing
  ([arXiv:2606.00137](https://arxiv.org/html/2606.00137)) does not treat DiT backbones as a
  category at all — corroboration that this is genuinely unpopulated, not merely unfound.

### Effect on the verdict

**The rank-1 recommendation stands, and its status improves.** Sequential img2img conditioning is
no longer a crude stand-in for something unreachable — it is the pixel-space form of the exact
mechanism this architecture family will expose natively. Implement it plainly, with no
abstraction for the hypothetical Omni path; if Omni ships, the conditioning channel is swapped
then, on evidence.

---

## Sources

Primary (raw LICENSE/requirements/API fetches, arXiv abstracts/HTML, HF model-card API):
- [TEXTurePaper/TEXTurePaper — LICENSE (MIT)](https://github.com/TEXTurePaper/TEXTurePaper/blob/main/LICENSE), [repo API](https://api.github.com/repos/TEXTurePaper/TEXTurePaper), [arXiv:2302.01721](https://arxiv.org/abs/2302.01721)
- [NVIDIAGameWorks/kaolin — repo API (Apache-2.0)](https://api.github.com/repos/NVIDIAGameWorks/kaolin)
- [OpenTexture/Paint3D — LICENSE (Apache 2.0)](https://raw.githubusercontent.com/OpenTexture/Paint3D/main/LICENSE), [environment.yaml](https://raw.githubusercontent.com/OpenTexture/Paint3D/main/environment.yaml), [repo API](https://api.github.com/repos/OpenTexture/Paint3D), [arXiv:2312.13913](https://arxiv.org/abs/2312.13913)
- [LIU-Yuxin/SyncMVD — LICENSE (MIT)](https://github.com/LIU-Yuxin/SyncMVD/blob/main/LICENSE), [requirements.txt](https://raw.githubusercontent.com/LIU-Yuxin/SyncMVD/main/requirements.txt), [repo API](https://api.github.com/repos/LIU-Yuxin/SyncMVD), [arXiv:2311.12891](https://arxiv.org/abs/2311.12891)
- [huanngzh/MV-Adapter — requirements.txt](https://raw.githubusercontent.com/huanngzh/MV-Adapter/main/requirements.txt), [repo API](https://api.github.com/repos/huanngzh/MV-Adapter), [arXiv:2412.03632 (incl. Table 3)](https://arxiv.org/abs/2412.03632), [VAST-AI Img2Texture Space](https://huggingface.co/spaces/VAST-AI/MV-Adapter-Img2Texture)
- [amap-cvlab/MV-Painter — LICENSE (raw)](https://raw.githubusercontent.com/amap-cvlab/MV-Painter/main/LICENSE), [repo API (NOASSERTION)](https://api.github.com/repos/amap-cvlab/MV-Painter), [MVPainter/INSTALL.md](https://raw.githubusercontent.com/amap-cvlab/MV-Painter/main/MVPainter/INSTALL.md), [arXiv:2505.12635](https://arxiv.org/abs/2505.12635)
- [StarRealMan/FlexPainter — requirements.txt](https://raw.githubusercontent.com/StarRealMan/FlexPainter/main/requirements.txt), [repo API](https://api.github.com/repos/StarRealMan/FlexPainter), [arXiv:2506.02620](https://arxiv.org/abs/2506.02620)
- [NVlabs/nvdiffrast — LICENSE.txt](https://raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt)
- [Tencent-Hunyuan/Hunyuan3D-2 — LICENSE (raw)](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE), [requirements.txt](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/requirements.txt), [HF README](https://huggingface.co/tencent/Hunyuan3D-2/raw/main/README.md), [Issue #50 open-license request](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/50)
- [3DTopia/MVPaint — repo API (license: null)](https://api.github.com/repos/3DTopia/MVPaint), [arXiv:2411.02336](https://arxiv.org/abs/2411.02336)
- [CVMI-Lab/TEXGen — repo API (license: null)](https://api.github.com/repos/CVMI-Lab/TEXGen), [arXiv:2411.14740](https://arxiv.org/abs/2411.14740)
- [MV2UV — arXiv:2603.15436](https://arxiv.org/abs/2603.15436), [CVPR 2026 poster](https://cvpr.thecvf.com/virtual/2026/poster/37737)
- In-repo: `scripts/ai-pipeline/prop_texture.py`, `tasks/ai-pipeline/research/a4-control-tooling.md`, `tasks/ai-pipeline/research/a5-comparative.md`, `tasks/ai-pipeline/research/a6-3-material-separation.md`

Secondary (flagged inline where used, not used for any load-bearing license/architecture claim):
- WebSearch-aggregated practitioner/comparison summaries for SyncMVD/Paint3D oversmoothing and
  Janus-problem complaints, MV-Adapter VRAM figures, Hunyuan3D VRAM/offload figures, "gameslop"
  Steam-disclosure context, Meshy-vs-Tripo blind-test figure — none independently re-verified
  against a primary document in this pass.
