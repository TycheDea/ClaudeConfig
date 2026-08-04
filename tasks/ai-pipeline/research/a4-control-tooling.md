# A4 — Control + consistency tooling (depth ControlNet composability, per base model)

Research date: 2026-07-20. This bullet is `BACKLOG.md`'s **A4** ("Control + consistency
tooling"), promoted from optional to **blocker** by `a3-style-lora.md`'s own gap-check: the
pipeline does not generate free-floating images — `prop_texture.py --strategy multiview`
renders orthographic depth maps from real Blender geometry and drives **xinsir
ControlNet-depth on SDXL** through headless ComfyUI, then reprojects the four generated views
into a UV atlas via facing-weighted, occlusion-tested blending (`prop_texture.py:483-521`). A3
concluded the house-style LoRA target is `FLUX.2-klein-base-4B` (Apache 2.0, ungated, trains at
24 GB, infers at ~13 GB) — but that conclusion is void if klein 4B cannot be depth-controlled
with the precision this reprojection math needs. It cannot, not at the incumbent's proof level.
That is this report's headline finding.

**Sourcing discipline**: every model-card/license/gating claim below was fetched as raw JSON or
raw Markdown bytes — `huggingface.co/api/models/...` and `raw.githubusercontent.com/...` via
`curl`, not through a summarizing proxy. `WebFetch`/`WebSearch` were used only for two
prose-only items (a Medium article, a GitHub code-search), both labeled where used. No figure
in this report is a summarizer paraphrase of a primary document unless explicitly flagged.

**Bottom line up front**: **Qwen-Image is the only one of the three A3 candidates with a
production-grade, natively-ComfyUI-loadable depth ControlNet today** —
`InstantX/Qwen-Image-ControlNet-Union`, Apache 2.0, trained from scratch on 10M images, and
ComfyUI's own `comfy/controlnet.py` has a first-class loader for its exact checkpoint format
(`load_controlnet_qwen_instantx`) — zero custom nodes required. **FLUX.2 klein 4B has no
ControlNet at all**; the only structural-control options found are a community LoRA
(`thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora`, Apache 2.0, 701 downloads) that
fuses a *reference image* with a depth map rather than conditioning on depth alone, and a
DiffSynth-Studio "Template" (Apache 2.0, real weights, 24-40 GB VRAM) that is not a ComfyUI node
at all — it runs through DiffSynth-Studio's own Python pipeline. Neither is proven at anything
close to xinsir's precision or adoption level. **HiDream-I1-Full has nothing** — the one
"controlnet" repo found on HF is its own trainer's admitted 2-step, 29-image sanity test, not a
usable model. **SDXL (the incumbent) remains the only base with a battle-tested, ComfyUI-native,
precision-proven depth path** — which reframes A3's conclusion into a real fork, not a
formality: either accept FLUX.2 klein's depth-control gap as a hard blocker and stay on
SDXL+xinsir (abandoning the style-LoRA plan's chosen base), or treat this as evidence to
re-open the base decision toward Qwen-Image.

---

## 1. Depth control per base — the crux

### SDXL (incumbent) — `xinsir/controlnet-depth-sdxl-1.0`

- **Extended description**: the exact model `prop_texture.py --strategy multiview` already
  calls today (`MV_WORKFLOW` → `prop_multiview.json` → `ControlNetLoader` /
  `ControlNetApplyAdvanced`). Standard SDXL ControlNet architecture (a trainable copy of the
  UNet's encoder blocks), trained on paired depth maps.
- **Technology**: classic ControlNet (Zhang et al. 2023 architecture) on SDXL's UNet.
- **License + IP terms**: **Apache 2.0**, confirmed via `huggingface.co/api/models/xinsir/
  controlnet-depth-sdxl-1.0` (`"license":"apache-2.0"`), ungated (`"gated":false`).
- **HF repo/gating**: `xinsir/controlnet-depth-sdxl-1.0`, ungated, 1.25B params (F16),
  16,119 downloads, 96 likes, last modified 2024-07-09 — stable/complete, not actively updated,
  but a finished ControlNet checkpoint has no reason to churn.
- **VRAM**: fits the 3080 Ti's 12 GB today — this is the pipeline's own proven, running
  configuration (SDXL base + this ControlNet + the multiview reprojection pass all execute on
  this exact box per `a4.md`'s A4.6/A4.9 log: "82 s GPU" / "~3 min/candidate").
- **Wall-time per iteration**: **measured, in-repo**: ~3 min/candidate for 4 ControlNet-depth
  views + CPU reprojection (`a4.md` A4.9 batch log; `a3-style-lora.md` budget table).
- **Maturity**: **production-proven** — this is literally what ships today.
- **Pros**: already integrated, already proven at the precision this pipeline's occlusion/
  facing-weight reprojection math depends on (the whole `blend_views()` function in
  `prop_texture.py` implicitly assumes the generated silhouette tracks the depth map tightly).
- **Cons**: SDXL is the weakest base of the four on raw image quality/style headroom (the entire
  reason A1-A3 went looking for a replacement).

### Qwen-Image — two real, Apache-2.0, from-scratch-trained ControlNets

**`InstantX/Qwen-Image-ControlNet-Union`** (recommended)
- **Extended description**: a *union* ControlNet — one checkpoint, four selectable control
  modes (canny, soft edge, **depth**, pose) via a `controlnet_conditioning_scale` /
  mode-selection mechanism, not one model per condition type.
- **Technology**: "5 double blocks copied from the pretrained transformer layers," trained
  *from scratch* for 50K steps on 10M high-quality images at 1328×1328, BF16, batch 64, lr 4e-5
  (numbers straight from the model card, not a summary). Ships as `QwenImageControlNetModel` /
  `QwenImageControlNetPipeline`, merged into upstream `diffusers` (PR #12215 referenced directly
  in the README).
- **License + IP terms**: **Apache 2.0**, confirmed via HF API (`"license":"apache-2.0"`).
- **HF repo/gating**: `InstantX/Qwen-Image-ControlNet-Union`, ungated, 1.77B params (BF16),
  4,037 downloads, 120 likes, last modified 2025-08-26. InstantX is a repeat, reputable
  ControlNet/IP-Adapter publisher (SD3, FLUX.1-dev, InstantID) — not a one-off community upload.
- **VRAM**: Qwen-Image's own base footprint is already large —  verified
  arithmetic puts BF16 weights at **40.9 GB**, before the text encoder (Qwen2.5-VL, ~17 GB per
  R2) or this ControlNet's own +1.77B params (~3.5 GB BF16). **Does not fit 12 GB or 24 GB
  unquantized**; needs the same GGUF/quantization strategy already established as necessary for
  Qwen-Image generally (Q8 near-lossless per §"Corrected arithmetic"). No
  source found benchmarking the ControlNet-attached pipeline specifically at any quant level —
  flagged as a gap below.
- **Wall-time per iteration**: not benchmarked in this pass or any source found; Qwen-Image's
  20.4B size and known slower per-step cost (R2: "30-60 sec/image... rough community figure")
  suggests noticeably slower than SDXL's ~3 min/4-view number, but no ControlNet-specific figure
  exists — **unresolved**.
- **Maturity**: **production-usable today** — real training run, real dataset, merged into
  upstream diffusers, natively loadable in ComfyUI core (§7).
- **Pros**: dedicated depth mode in a maintained, well-adopted checkpoint; matches Qwen-Image's
  own Apache-2.0 cleanliness; zero custom ComfyUI nodes needed (§7).
- **Cons**: adds real VRAM/compute on top of an already-heavy base; Union-mode precision on
  *depth specifically* (vs. a depth-dedicated model) is not independently benchmarked against
  xinsir's here.

**`DiffSynth-Studio/Qwen-Image-Blockwise-ControlNet-Depth`** (dedicated depth alternative)
- **Extended description**: a depth-only (not union) ControlNet, "Blockwise" architecture,
  trained via the DiffSynth-Studio (ModelScope/Alibaba) framework on the BLIP3o-60k dataset.
  (The earlier R2 report cited a reupload of this exact model at
  `SahilCarterr/Qwen-Image-Blockwise-ControlNet-Depth`, which — checked here — carries **no
  license tag at all**; the authoritative repo is this one, DiffSynth-Studio's own.)
- **License + IP terms**: **Apache 2.0**, confirmed via HF API.
- **HF repo/gating**: `DiffSynth-Studio/Qwen-Image-Blockwise-ControlNet-Depth`, ungated, last
  modified 2025-09-28, **0 downloads / 0 likes** on this exact repo (the SahilCarterr mirror has
  the visible community traction, 6 likes, but no license) — thin adoption despite being a real,
  purpose-built model.
- **VRAM / wall-time**: not separately characterized; runs through DiffSynth-Studio's own
  `QwenImagePipeline`, same base-model VRAM floor as above.
- **ComfyUI support**: **not verified** — ComfyUI's native Qwen ControlNet loader
  (`load_controlnet_qwen_instantx`, §7) is named for InstantX's checkpoint format specifically;
  whether it also accepts this Blockwise checkpoint's tensor layout was not confirmed either way
  in this pass. **Flagged as unresolved**, not assumed compatible.
- **Maturity**: real, Apache-2.0, but low-adoption and ComfyUI-compatibility unconfirmed — treat
  InstantX's Union model as the primary recommendation, this as a depth-precision fallback worth
  a direct A/B if InstantX's union-mode depth underperforms.

**`alibaba-pai/Qwen-Image-2512-Fun-Controlnet-Union`** (third option, noted not evaluated
in depth) — Apache 2.0 confirmed via HF API search; part of Alibaba PAI's "VideoX-Fun" project
line (the same publisher whose FLUX.2-**dev** equivalent is non-commercial, see below — but
this Qwen-Image variant is Apache 2.0, unlike that one). ComfyUI's `comfy/controlnet.py` has a
distinct native loader for this exact "Fun" checkpoint family (`load_controlnet_qwen_fun`,
separate code path from `load_controlnet_qwen_instantx`) — so this is *also* natively
ComfyUI-loadable. Not otherwise characterized (VRAM, dataset, maturity) in this pass.

### FLUX.2 [klein] 4B — no ControlNet exists; two substitutes, neither proven

**What does NOT exist, checked directly against the `black-forest-labs` HF org** (35 repos
enumerated via `huggingface.co/api/models?author=black-forest-labs`): there is **no**
`FLUX.2-Depth-dev`, `FLUX.2-Canny-dev`, or `FLUX.2-Redux` repo. BFL's "Tools" suite
(`FLUX.1-Depth-dev`, `FLUX.1-Canny-dev`, `FLUX.1-Redux-dev`) exists **only for FLUX.1**, and is
gated (`"gated":"auto"`) under the **FLUX.1 [dev] Non-Commercial License** (confirmed by fetching
`LICENSE.md` from `FLUX.1-Depth-dev` directly) — not usable in a shipped commercial game and not
architecturally FLUX.2 regardless. This closes off the "just use BFL's own official depth tool"
path entirely for the commercially-clean klein 4B.

A third-party ControlNet-Union for the **FLUX.2-dev (32B)** line does exist
(`alibaba-pai/FLUX.2-dev-Fun-Controlnet-Union`, supports Canny/HED/**Depth**/Pose/MLSD/Scribble)
— but it is (a) licensed `flux-dev-non-commercial-license` (inherits FLUX.2-dev's own
non-commercial terms, confirmed via its README frontmatter), and (b) trained against
FLUX.2-**dev**'s transformer block structure specifically ("added on 4 double blocks" of the
32B model), not klein 4B's differently-sized transformer — a ControlNet's copied/injected blocks
are shaped to match the specific transformer they were trained against, so this is very likely
architecturally incompatible with klein 4B even setting the license aside. **Not independently
load-tested; flagged as inferred-incompatible, not confirmed.**

**`DiffSynth-Studio/Template-KleinBase4B-ControlNet`** (structural-control, real weights)
- **Extended description**: a "Diffusion Templates" structural-control model, explicitly built
  against `black-forest-labs/FLUX.2-klein-base-4B` (the exact LoRA training target from A3).
  Conditions on an input image (the shown example is a depth map) to control "spatial
  structure, object outlines, and perspective."
- **Technology**: per the file listing, the control weights are **3,875,544,576 params** —
  identical to klein 4B's own flow-transformer parameter count (`a3-style-lora.md`'s verified
  arithmetic: "Flow transformer 3,875,544,576"). This is a full-size parallel control branch,
  not a lightweight adapter — architecturally heavier than a classic ControlNet's
  partial-block-copy design. Backed by a named technical report, arXiv:2604.24351.
- **License + IP terms**: **Apache 2.0**, confirmed via HF API.
- **HF repo/gating**: `DiffSynth-Studio/Template-KleinBase4B-ControlNet`, ungated, 0
  downloads/likes on HF (traction, if any, is on ModelScope, not measured here).
- **VRAM**: **stated directly in its own README**: "Direct inference (requires 40GB GPU
  memory)"; a lazy-loading/offload config is offered "requires 24G GPU memory." **Does not fit
  12 GB under any configuration documented**; 24 GB is the documented floor.
- **Wall-time**: not benchmarked; 50-step inference is the shown default (`num_inference_steps`
  50 in the sample code), no wall-clock figure given.
- **Precision concern (the task's explicit ask)**: the shown examples condition on a depth image
  but the README's own framing is generic "structural control" (spatial structure/outlines/
  perspective) rather than a claim of pixel-tight depth correspondence, and the showcased
  outputs visibly restyle the subject (a photorealistic crystal ball → "3D Pixar style" scene)
  while loosely preserving composition — this reads as **looser, more interpretive structural
  guidance than xinsir's SDXL depth ControlNet**, which this pipeline's reprojection math
  depends on tracking closely. Not independently benchmarked for geometric fidelity; flagged as
  a real open risk, not dismissed.
- **ComfyUI support**: **none found**. A GitHub code search for `ComfyUI DiffSynth` custom node
  packs returned zero results. DiffSynth-Studio ships its own Python inference pipeline
  (`diffsynth.pipelines.flux2_image.Flux2ImagePipeline` + `diffsynth.diffusion.template.
  TemplatePipeline`) — using it from this project's headless-ComfyUI-JSON pipeline would mean
  writing a new custom ComfyUI node from scratch, not dropping in an existing one.
- **Maturity**: real, funded, documented training+inference code, Apache 2.0 — but essentially
  zero independent adoption evidence and no ComfyUI path today.

**`thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora`** (LoRA, reference + depth fusion)
- **Extended description**: **not a depth ControlNet** — a LoRA that fuses **two inputs**, a
  reference image (identity/style donor) and a depth map (pose/structure), producing an output
  that keeps the reference's identity while adopting the depth map's composition. Trigger word
  `refcontrol`.
- **Technology**: standard LoRA (diffusers `library_name: diffusers`) on
  `black-forest-labs/FLUX.2-klein-base-4B` — the exact same base A3 targets for the style LoRA.
- **License + IP terms**: **Apache 2.0**, confirmed via HF API.
- **HF repo/gating**: `thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora`, ungated, 701
  downloads, 9 likes, created 2026-05-28 (~7 weeks old at research time) — real but young; its
  9B-parameter sibling (`refcontrol-FLUX.2-klein-9B-...`) has more traction (7,243 downloads),
  suggesting the 4B variant is the less-used of the pair.
- **VRAM**: base klein 4B alone is ~13 GB (BFL's own inference figure); a LoRA adds negligible
  VRAM (tens–hundreds of MB of extra weights) — **plausibly fits 24 GB comfortably, tight/marginal
  on the 3080 Ti's 12 GB** (klein 4B inference is already "just short" of 12 GB per the
  established A3/G2 figures, before any LoRA overhead).
- **Wall-time**: not benchmarked; klein 4B's own generation is fast (sub-second to
  few-second class per BFL's marketing), no figure specific to this LoRA's added cost found.
- **Precision concern**: this mechanism explicitly trades off identity preservation against
  depth fidelity ("recommended weight 0.8-1.0... how strongly you want to preserve identity" —
  i.e., turning the depth signal *down* relative to identity is a documented, expected knob).
  That is a fundamentally different contract than a classic ControlNet, which has no competing
  identity signal to trade against. For this pipeline's actual need — four independent camera
  views of one object, each needing to match its OWN depth render precisely so the reprojection
  math's occlusion/facing tests hold — a mechanism that intentionally softens depth adherence to
  protect identity is a plausible but **unproven fit**, not a drop-in ControlNet replacement.
  One structurally interesting angle worth testing, not assumed: feeding the *front concept
  image* as the "reference" and each side/back depth render as the "depth" input per view could
  map naturally onto this pipeline's existing concept-then-multiview structure — but this is
  this report's own extrapolation, not a documented use case, and reference-input class here was
  trained "primarily on humans... also works with objects" (mixed evidence for prop classes).
- **ComfyUI support**: **yes, directly** — ships an actual ComfyUI workflow JSON
  (`image_flux2_klein_image_edit_4b_refcontrol_depth.json`) alongside the weights. Needs
  `Fannovel16/comfyui_controlnet_aux` (Apache 2.0, confirmed via GitHub API) installed for
  depth-map *extraction from photos* — this pipeline doesn't need that specific piece, since it
  already renders exact geometric depth in Blender rather than estimating it from an image.
- **Maturity**: young (< 2 months old), real weights, real ComfyUI workflow, low but nonzero
  adoption. The most concretely *usable-today-in-ComfyUI* FLUX.2 klein option found — but its
  design goal (identity-from-reference) is adjacent to, not identical with, this pipeline's need
  (identity-from-text-prompt, precision-from-geometry).

### HiDream-I1-Full — nothing production-usable found

- **What exists**: exactly one HF repo surfaced by any depth/controlnet search —
  `ControlNetLoRA/hidream-i1` (mirrored as `bghira/hidream-controlnet-lora-test` — the repo name
  itself says "test"). Its own model card, read directly: **0 training epochs, 2 training
  steps, LoRA rank 1, a 29-image dataset at 256×256 resolution, `"not-for-all-audiences"`
  tagged**. This is its own maintainer's (bghira, SimpleTuner's author) admitted sanity check of
  ControlNet-LoRA plumbing on HiDream, not a usable depth model by any reading. License is
  `"other"` (unspecified/restrictive), not even permissive.
- **Verdict, stated plainly**: **no depth ControlNet, dedicated or otherwise, exists for
  HiDream-I1-Full as of this research date.** This directly confirms R2's earlier finding
  ("no dedicated depth-ControlNet for HiDream specifically... a real gap") rather than
  contradicting it — re-checked independently here with a fresh, targeted search and it still
  holds.
- **Consequence for this pipeline**: HiDream-I1-Full is **eliminated** as a texture-stage base
  regardless of its MIT license or quality standing (already flagged elsewhere as the base with
  the Llama-3.1 text-encoder licensing wrinkle) — it simply cannot run this pipeline's core
  depth-reprojection step today.

---

## 2. Composability: style LoRA + depth control simultaneously

This is the question that decides whether A3's plan actually works, and it is the thinnest
evidence base in this whole report — stated honestly, not papered over.

- **SDXL**: mechanically trivial in ComfyUI — a `LoraLoader` node and the existing
  `ControlNetLoader`/`ControlNetApplyAdvanced` nodes both apply to the same frozen UNet
  independently; nothing in `prop_multiview.json` today loads a LoRA (checked directly — no
  `LoraLoader` class_type in the committed workflow), so this specific combination is
  **not yet exercised in this repo**, only mechanically unremarkable. One practitioner guide
  found (Medium, **[secondary]**, fetched via WebFetch) shows a working combined example at
  `controlnet_conditioning_scale = 0.8` but gives no systematic degradation data either way.
  General ML-community consensus (via WebSearch, **[secondary, aggregated]**): "naive
  combination strategies can hurt generation quality" in some configurations, but "LoRA and
  ControlNet can technically be combined... with careful design... composability can be
  achieved effectively" — i.e., it works but is not automatically artifact-free; strength
  tuning (starting low on the LoRA and/or the ControlNet scale, verifying by eye) is the
  practical mitigation cited everywhere, not a documented fixed recipe.
- **Qwen-Image**: InstantX's ControlNet-Union copies/trains additional blocks on top of a frozen
  Qwen-Image base; a LoRA trains low-rank deltas on the base's own weights. No architectural
  collision between the two mechanisms is evident from either model's design, but **no source
  found tests this specific combination** (style LoRA + Qwen ControlNet-Union) — flagged as
  untested, not as verified-safe.
- **FLUX.2 klein 4B**: this is the hardest case, precisely because neither depth-control option
  is a clean ControlNet. `DiffSynth-Studio/Template-KleinBase4B-ControlNet`'s control weights
  are a **frozen copy of the base transformer taken at training time** — if a style LoRA is
  applied on top of the *base* model used for generation, the Template's own copied blocks stay
  un-style-tuned (they were trained once, against the plain klein-4B-base checkpoint), so the
  two influences would not be jointly optimized and could plausibly pull against each other in
  ways no source addresses. `thedeoxen/refcontrol`'s mechanism **is itself a LoRA** — stacking a
  second (style) LoRA on the same transformer means running two LoRAs simultaneously, which
  diffusers/ComfyUI support mechanically (chained `LoraLoader` nodes) but which is exactly the
  "naive stacking may degrade quality" scenario flagged above, now doubled (a control LoRA and a
  style LoRA competing for the same low-rank update budget on the same base weights). **No
  source tests two stacked FLUX.2 klein LoRAs of this kind.** This is a real, unresolved risk
  that a hands-on test would need to settle before committing to klein 4B for this pipeline.
- **HiDream**: moot — there is nothing to compose with.

---

## 3. Multi-view / cross-view consistency tooling

- **`huanngzh/MV-Adapter`** (recommended reference point): Apache 2.0 (confirmed via GitHub
  API), ICCV 2025-accepted, 1,273 stars, **actively maintained** (core repo pushed 2026-06-26,
  API-touched as recently as 2026-07-18 — two days before this research). Purpose-built for
  exactly this pipeline's problem class: it ships **geometry-conditioned multi-view generation**
  and dedicated **Text2Texture / Image2Texture** demo pipelines (image→3D texture generation
  with cross-view coherence enforced by the adapter's own attention design) — closer to a
  turnkey answer to this pipeline's actual job than anything found in R2's prior pass. **Base
  model support is SDXL and SD2.1 only** — confirmed by reading the full README's model table
  and usage sections; **no FLUX.2, Qwen-Image, or HiDream variant exists**. It explicitly
  supports stacking community LoRAs and ControlNets (its own scribble-to-multiview example uses
  `xinsir/controlnet-scribble-sdxl-1.0`) — i.e., MV-Adapter is itself evidence that SDXL's
  ecosystem already solves LoRA+ControlNet+multi-view composition together, which is a point in
  the incumbent's favor that the other three bases cannot currently match.
- **ComfyUI wrapper** (`huanngzh/ComfyUI-MVAdapter`, Apache 2.0 confirmed): exists, but **stale**
  — last pushed 2025-06-26, over a year before this research date, while the core MV-Adapter
  repo itself has commits as recent as two days ago. A real maintenance-lag flag if this were
  adopted today.
- **This pipeline's own answer already exists and is not MV-Adapter**: `prop_texture.py`'s
  `blend_views()` (facing-weighted, occlusion-tested, silhouette-aware reprojection of
  independently-generated per-view images onto a shared UV atlas) is itself a from-scratch,
  already-shipped substitute for this whole tooling category — it does not rely on any
  attention-sharing or cross-view-consistency model at generation time; consistency is enforced
  *after* generation, geometrically, at the reprojection stage. This is worth stating plainly:
  the pipeline is not actually missing multi-view tooling for SDXL, it built its own. The open
  question this category actually raises is whether that same reprojection-based strategy
  survives a base swap (it should, in principle — it operates on the generated images
  post-hoc, agnostic to which model produced them) rather than whether a cross-view-attention
  tool needs to be bolted on.
- **Research-only methods** (MVPainter, Hitem3D 2.0, MV2UV, FlexPainter) — carried forward from
  R2 without re-verification in this pass (out of this bullet's scope to re-check); R2's own
  characterization ("published research... none is a turnkey pip-installable tool") stands.

---

## 4. Reference/identity conditioning (IP-Adapter equivalent)

- **SDXL**: `h94/IP-Adapter`, **Apache 2.0** (confirmed via HF API), ungated, 1,383 likes — the
  long-standing, production-proven incumbent option.
- **FLUX.2 klein 4B**: **native, built into the base checkpoint** — the model card states
  directly: "FLUX.2 [klein] 4B Base is a 4 billion parameter rectified flow transformer capable
  of generating images from text descriptions and **supports multi-reference editing
  capabilities**." No separate adapter model is needed; this capability ships under the same
  Apache 2.0 license as the base weights. This is architecturally distinct from — and should not
  be confused with — BFL's **FLUX.1 Redux** (`black-forest-labs/FLUX.1-Redux-dev`), which is
  FLUX.1-only and non-commercial-gated; klein's multi-reference editing is a first-class,
  commercially-clean capability of the 4B checkpoint itself.
- **Qwen-Image**: no dedicated IP-Adapter repo found (targeted HF search returned zero results;
  InstantX, despite publishing IP-Adapters for SD3.5 and FLUX.1-dev, has published no Qwen-Image
  equivalent). R2's earlier note on Qwen-Image-Edit's "multi-turn conditioning" being a
  genuinely different, unproven-for-this-use mechanism stands uncontradicted — carried forward,
  not re-verified in this pass.
- **HiDream**: no dedicated IP-Adapter repo found; targeted search returned zero results.

---

## 5. Inpainting / refinement

- **SDXL**: mature, dedicated inpainting checkpoints and native ComfyUI support
  (`VAEEncodeForInpaint`, `SetLatentNoiseMask`, `ControlNetInpaintingAliMamaApply` all confirmed
  present in ComfyUI core `nodes.py`/`comfy_extras/nodes_controlnet.py`) — this is bedrock,
  multi-year SD-ecosystem territory, not independently re-benchmarked in this pass.
- **Qwen-Image**: `InstantX/Qwen-Image-ControlNet-Inpainting`, **Apache 2.0** (confirmed via HF
  API), ungated, 1,854 downloads, 116 likes, same publisher/quality tier as the depth
  ControlNet above — a real, dedicated option.
- **FLUX.2 klein 4B**: **no production option found.** BFL's own `FLUX.1-Fill-dev` exists but is
  FLUX.1 (non-commercial-gated, wrong generation). One community repo,
  `dreMaz/flux2-klein-inpaint`, surfaced in search — checked directly: **no license tag at all**,
  0 downloads, 1 like, 31 MB total (too small to plausibly be a full inpainting-tuned model;
  more likely a small prompt-embedding or LoRA-scale artifact) — **too thin to count as a real
  option**, flagged as a gap rather than a finding.
- **HiDream**: no inpainting-specific repo found at all.

---

## 6. Regional / spatial prompting

**Solved at the ComfyUI-core level, for all four bases simultaneously** — this is the one
category in this report that is *not* base-model-gated. Confirmed directly by reading
`Comfy-Org/ComfyUI`'s `nodes.py`: `ConditioningSetArea`, `ConditioningSetAreaPercentage`,
`ConditioningSetAreaStrength`, `ConditioningCombine`, and `ConditioningSetMask` all exist in
ComfyUI core and operate purely on conditioning tensors before sampling — they have no
base-architecture dependency, so they work identically whether the underlying checkpoint is
SDXL, Qwen-Image, FLUX.2 klein, or (hypothetically) HiDream. Nothing further to resolve per base;
carried forward as a settled point rather than re-litigated per model below.

---

## 7. ComfyUI support — native core vs. custom-node vs. nonexistent

Checked directly against `Comfy-Org/ComfyUI`'s source tree (the project moved from
`comfyanonymous/ComfyUI`, redirect confirmed, actively pushed as of 2026-07-19 — one day before
this research, i.e. genuinely live upstream, not a stale fork).

| Base | Depth-control loading | Where it lives |
|---|---|---|
| SDXL (xinsir) | **Native core** — generic `ControlNetLoader`/`ControlNetApplyAdvanced`, already proven in this exact pipeline. | `comfy_extras/nodes_controlnet.py` |
| Qwen-Image (InstantX Union) | **Native core** — `load_controlnet_qwen_instantx(sd, ...)` recognizes the checkpoint format directly; loads via `comfy.ldm.qwen_image.controlnet.QwenImageControlNetModel`. Zero custom nodes. | `comfy/controlnet.py:664-680` |
| Qwen-Image (Alibaba PAI "Fun" line) | **Native core**, separate loader — `load_controlnet_qwen_fun`. | `comfy/controlnet.py:681-713` |
| Qwen-Image (DiffSynth Blockwise-Depth) | **Unconfirmed** — not verified whether the InstantX-named loader also accepts this checkpoint's tensor layout. | n/a |
| FLUX.2 klein (`thedeoxen` refcontrol LoRA) | **Works, but not via the ControlNet system at all** — loads as an ordinary LoRA (`LoraLoader`) plus klein's own native multi-reference/edit conditioning; ships its own ComfyUI workflow JSON. Needs `Fannovel16/comfyui_controlnet_aux` (Apache 2.0) only for depth *estimation from photos*, which this pipeline doesn't need (it already has ground-truth geometric depth). | Community workflow, no core involvement |
| FLUX.2 klein (DiffSynth Template) | **No ComfyUI path found at all** — GitHub code search for a ComfyUI/DiffSynth wrapper returned zero results; runs only through DiffSynth-Studio's own Python `diffsynth` pipeline. Would require writing a new custom ComfyUI node to integrate. | Not integrated |
| FLUX.2 (any variant) generic ControlNet loader | **None** — `comfy/controlnet.py` has loader functions matching `flux` (XLabs/Mistoline, InstantX — all FLUX.1) and `qwen`, but no `flux2`/`klein`-pattern loader exists anywhere in the file (grepped directly, zero matches). | n/a |
| HiDream (any) | **None** — no ControlNet-shaped checkpoint exists to load in the first place. | n/a |
| Regional prompting (§6) | **Native core, all bases.** | `nodes.py` |
| Reference conditioning: FLUX.2 klein native multi-reference | **Native core** — `EmptyFlux2LatentImage`, `Flux2Scheduler`, and the underlying `Flux2KleinPipeline`-equivalent nodes are present in `comfy_extras/nodes_flux.py` / `comfy/ldm/flux/`. | `comfy_extras/nodes_flux.py` |
| Reference conditioning: FLUX Redux | **Native core** (`comfy/ldm/flux/redux.py`) — but FLUX.1-only, non-commercial base. | `comfy/ldm/flux/redux.py` |
| IP-Adapter (SDXL, h94) | Standard third-party custom node pack territory (ComfyUI_IPAdapter_plus and similar) — not re-verified in this pass, bedrock-established. | Custom node (well-known) |

---

## Verdict per base

| Base | Depth control (§1) | LoRA + control composability (§2) | Multi-view tooling (§3) | ComfyUI support (§7) | **Viable for this pipeline today?** |
|---|---|---|---|---|---|
| **SDXL (incumbent)** | Production-proven, precision-proven, already shipping. | Mechanically trivial; not yet exercised with a style LoRA in this repo but the ecosystem (MV-Adapter's own LoRA-stacking examples) treats it as routine. | Purpose-built option exists (MV-Adapter) though this pipeline uses its own reprojection instead. | Native, proven. | **Yes — the only base with zero open risk on this axis.** |
| **Qwen-Image** | Real, Apache-2.0, from-scratch-trained, natively ComfyUI-loadable (InstantX Union). Second dedicated-depth option exists (DiffSynth Blockwise) with unconfirmed ComfyUI compatibility. | Untested combination, no architectural red flag. | No dedicated multi-view tool; this pipeline's own reprojection approach is base-agnostic and should carry over. | Native core loader, zero custom nodes. | **Yes, with real but bounded unknowns** — the strongest alternative to SDXL found in this report, and the only one of the two non-incumbent bases with a genuinely production-grade depth path. |
| **FLUX.2 klein 4B** | **No ControlNet exists.** Best available: a young community LoRA (reference+depth fusion, not pure depth) or a heavyweight (24-40 GB) non-ComfyUI structural-control model from DiffSynth-Studio. Neither proven at xinsir's precision/adoption level. | **Highest risk in this report** — the depth-control option is itself often a LoRA, so adding A3's style LoRA means stacking two LoRAs with no source testing that combination, or pairing a style LoRA with a frozen, un-style-tuned parallel control branch (DiffSynth Template) whose weights would go stale relative to a style-tuned base. | None found for this base at all. | The LoRA option has a working ComfyUI workflow; the Template option has none. | **Not viable as researched today** — A3's chosen base has no proven depth-control path; this is the report's central, load-bearing finding and directly contradicts the working assumption A3 handed off. |
| **HiDream-I1-Full** | **Nothing.** The only "controlnet" repo found is its own trainer's 2-step sanity test. | Moot. | None found. | None. | **No — eliminated**, consistent with (and now more firmly confirmed than) R2's prior finding. |

---

## Unresolved / could not verify

- **Qwen-Image ControlNet + LoRA + full pipeline VRAM at any specific quantization level** — no
  source benchmarks the InstantX Union ControlNet attached to a quantized Qwen-Image base on a
  24 GB card; only the unquantized BF16 floor (~44 GB combined) is arithmetically derived here,
  not independently measured.
- **Whether `DiffSynth-Studio/Qwen-Image-Blockwise-ControlNet-Depth` loads through ComfyUI's
  existing `load_controlnet_qwen_instantx` path or needs its own loader** — not confirmed either
  way; would need a direct load attempt to settle.
- **Whether `alibaba-pai/FLUX.2-dev-Fun-Controlnet-Union`'s weights are architecturally
  compatible with FLUX.2-klein-4B** — inferred incompatible from differing model sizes and the
  README's "4 double blocks" language being specific to the 32B dev transformer, but not
  independently load-tested.
- **thedeoxen refcontrol LoRA's actual geometric precision** — no independent benchmark against
  xinsir's depth-map-fidelity behavior; the "reference image = front concept, depth = other
  views" application to this pipeline is this report's own untested extrapolation, not a
  documented use case of the LoRA's author.
- **DiffSynth Template-KleinBase4B-ControlNet's real-world depth fidelity** — the showcased
  examples visually restyle their subjects, suggesting looser structural adherence than a
  classic depth ControlNet, but this is a qualitative read of four showcase images, not a
  measurement.
- **No wall-time-per-iteration figure exists for any Qwen-Image or FLUX.2-klein depth-control
  path specifically** — only the SDXL incumbent has an in-repo measured number (~3 min/candidate,
  4 views).
- **LoRA+ControlNet composability generally** rests on one secondary Medium walkthrough and one
  aggregated WebSearch summary of unnamed sources — no primary vendor or paper-level study was
  found quantifying the degradation risk for any of the three target bases specifically.

---

## Sources

Primary (fetched as raw bytes — HF API JSON or `raw.githubusercontent.com`):
- [huggingface.co/api/models/xinsir/controlnet-depth-sdxl-1.0](https://huggingface.co/api/models/xinsir/controlnet-depth-sdxl-1.0)
- [huggingface.co/api/models/InstantX/Qwen-Image-ControlNet-Union](https://huggingface.co/api/models/InstantX/Qwen-Image-ControlNet-Union)
- [huggingface.co/InstantX/Qwen-Image-ControlNet-Union/raw/main/README.md](https://huggingface.co/InstantX/Qwen-Image-ControlNet-Union/raw/main/README.md)
- [huggingface.co/api/models/InstantX/Qwen-Image-ControlNet-Inpainting](https://huggingface.co/api/models/InstantX/Qwen-Image-ControlNet-Inpainting)
- [huggingface.co/api/models?author=InstantX](https://huggingface.co/api/models?author=InstantX&limit=100)
- [huggingface.co/api/models/SahilCarterr/Qwen-Image-Blockwise-ControlNet-Depth](https://huggingface.co/api/models/SahilCarterr/Qwen-Image-Blockwise-ControlNet-Depth)
- [huggingface.co/SahilCarterr/Qwen-Image-Blockwise-ControlNet-Depth/raw/main/README.md](https://huggingface.co/SahilCarterr/Qwen-Image-Blockwise-ControlNet-Depth/raw/main/README.md)
- [huggingface.co/api/models/DiffSynth-Studio/Qwen-Image-Blockwise-ControlNet-Depth](https://huggingface.co/api/models/DiffSynth-Studio/Qwen-Image-Blockwise-ControlNet-Depth)
- [huggingface.co/api/models?search=alibaba-pai%20qwen%20controlnet](https://huggingface.co/api/models?search=alibaba-pai+qwen+controlnet)
- [huggingface.co/api/models?author=black-forest-labs](https://huggingface.co/api/models?author=black-forest-labs&limit=200)
- [huggingface.co/api/models/black-forest-labs/FLUX.1-Depth-dev](https://huggingface.co/api/models/black-forest-labs/FLUX.1-Depth-dev)
- [raw.githubusercontent.com/black-forest-labs/flux/main/model_licenses/LICENSE-FLUX1-dev](https://raw.githubusercontent.com/black-forest-labs/flux/main/model_licenses/LICENSE-FLUX1-dev)
- [huggingface.co/black-forest-labs/FLUX.2-klein-base-4B/raw/main/README.md](https://huggingface.co/black-forest-labs/FLUX.2-klein-base-4B/raw/main/README.md)
- [huggingface.co/alibaba-pai/FLUX.2-dev-Fun-Controlnet-Union/raw/main/README.md](https://huggingface.co/alibaba-pai/FLUX.2-dev-Fun-Controlnet-Union/raw/main/README.md)
- [huggingface.co/api/models?search=klein%20depth](https://huggingface.co/api/models?search=klein+depth)
- [huggingface.co/api/models?search=klein%20controlnet](https://huggingface.co/api/models?search=klein+controlnet)
- [huggingface.co/thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora/raw/main/README.md](https://huggingface.co/thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora/raw/main/README.md)
- [huggingface.co/api/models/thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora](https://huggingface.co/api/models/thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora)
- [huggingface.co/DiffSynth-Studio/Template-KleinBase4B-ControlNet/raw/main/README.md](https://huggingface.co/DiffSynth-Studio/Template-KleinBase4B-ControlNet/raw/main/README.md)
- [huggingface.co/api/models/DiffSynth-Studio/Template-KleinBase4B-ControlNet](https://huggingface.co/api/models/DiffSynth-Studio/Template-KleinBase4B-ControlNet)
- [huggingface.co/api/models/dreMaz/flux2-klein-inpaint](https://huggingface.co/api/models/dreMaz/flux2-klein-inpaint)
- [huggingface.co/api/models?search=HiDream%20controlnet](https://huggingface.co/api/models?search=HiDream+controlnet)
- [huggingface.co/ControlNetLoRA/hidream-i1/raw/main/README.md](https://huggingface.co/ControlNetLoRA/hidream-i1/raw/main/README.md)
- [huggingface.co/api/models/h94/IP-Adapter](https://huggingface.co/api/models/h94/IP-Adapter)
- [api.github.com/repos/modelscope/DiffSynth-Studio](https://api.github.com/repos/modelscope/DiffSynth-Studio) (license: Apache 2.0, confirmed via raw `LICENSE` fetch too)
- [raw.githubusercontent.com/modelscope/DiffSynth-Studio/main/LICENSE](https://raw.githubusercontent.com/modelscope/DiffSynth-Studio/main/LICENSE)
- [api.github.com/repos/Fannovel16/comfyui_controlnet_aux](https://api.github.com/repos/Fannovel16/comfyui_controlnet_aux)
- [api.github.com/repos/huanngzh/MV-Adapter](https://api.github.com/repos/huanngzh/MV-Adapter)
- [raw.githubusercontent.com/huanngzh/MV-Adapter/main/README.md](https://raw.githubusercontent.com/huanngzh/MV-Adapter/main/README.md)
- [api.github.com/repos/huanngzh/ComfyUI-MVAdapter](https://api.github.com/repos/huanngzh/ComfyUI-MVAdapter)
- [api.github.com/repos/comfyanonymous/ComfyUI](https://api.github.com/repos/comfyanonymous/ComfyUI) (redirects to Comfy-Org/ComfyUI)
- [raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy/controlnet.py](https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy/controlnet.py)
- [raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_controlnet.py](https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_controlnet.py)
- [raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_flux.py](https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_flux.py)
- [raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_qwen.py](https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/comfy_extras/nodes_qwen.py)
- [raw.githubusercontent.com/Comfy-Org/ComfyUI/master/nodes.py](https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/nodes.py)
- [api.github.com/repos/Comfy-Org/ComfyUI/contents/comfy/ldm](https://api.github.com/repos/Comfy-Org/ComfyUI/contents/comfy/ldm) (native module list: `flux`, `qwen_image`, `hidream`, `hidream_o1`, `depth_anything_3`, no `flux2`/`klein` directory)
- In-repo: `scripts/ai-pipeline/prop_texture.py`, `scripts/ai-pipeline/workflows/prop_multiview.json`, `tasks/ai-pipeline/a4.md` (A4.6/A4.9 measured wall-times), `tasks/ai-pipeline/research/a3-style-lora.md`, `tasks/ai-pipeline/research/r2-image-models.md`

Secondary (flagged inline where used, not used for any load-bearing license/gating/architecture
claim):
- [Medium — Combining ControlNet and LoRA with Stable Diffusion XL](https://medium.com/@mehmetttozlu/combining-controlnet-and-lora-with-stable-diffusion-xl-dd1732b10892) **[secondary]**
- WebSearch aggregate summary on LoRA+ControlNet composability (query: "LoRA ControlNet applied
  together same time diffusion model degrade quality composability") — sources included
  arXiv:2508.03373 and kevinlu.ai/loras-as-programs, neither fetched directly in this pass,
  relayed only via the search tool's own summary **[secondary, aggregated, not independently
  re-verified]**

---

# Verification pass (orchestrator, 2026-07-20)

All checks below are raw `curl` against `huggingface.co/api/...`, `raw.githubusercontent.com`,
and the GitHub API — plain bytes, no summarizing proxy.

## Confirmed — the central finding stands

- **No FLUX.2 ControlNet loader exists in ComfyUI core.** Read `comfy/controlnet.py` end to end.
  The dispatch chain has `load_controlnet_flux_xlabs_mistoline`, `load_controlnet_flux_instantx`
  (both FLUX.**1**), `load_controlnet_qwen_instantx`, `load_controlnet_qwen_fun`,
  `load_controlnet_sd35`, `load_controlnet_mmdit`. No `flux2`/`klein` branch anywhere.
- **BFL never published FLUX.2 control tools.** Enumerated the `black-forest-labs` org: the only
  control repos are `FLUX.1-Depth-dev`, `FLUX.1-Depth-dev-lora`, `FLUX.1-Canny-dev`,
  `FLUX.1-Canny-dev-onnx`, `FLUX.1-Redux-dev`. All FLUX.1, all `-dev`, all non-commercial.
- **`InstantX/Qwen-Image-ControlNet-Union`** — `license: apache-2.0`, `"gated": false`,
  1,768,003,584 params (~3.5 GB BF16), 4,037 downloads. ComfyUI core support confirmed at
  `comfy/controlnet.py:664` (`load_controlnet_qwen_instantx`), dispatched at line 801 on the
  `transformer_blocks.0.img_mlp.net.0.proj.weight` key. Zero custom nodes. **The agent's
  strongest claim is accurate.**
- **`thedeoxen/refcontrol-FLUX.2-klein-4B-reference-depth-lora`** — Apache 2.0, ungated, but
  **701 downloads, 9 likes, last modified 2026-05-28**. Thin, as reported.

## Corrected — one inference in the Unresolved list is wrong

The report guessed `alibaba-pai/FLUX.2-dev-Fun-Controlnet-Union` was "architecturally
incompatible with klein-4B... inferred from differing model sizes." That inference is not what
blocks it. The real situation is cleaner and worse:

VideoX-Fun ships a working `LoadFlux2ControlNetInPipeline` ComfyUI node whose default checkpoint
is literally `FLUX.2-dev-Fun-Controlnet-Union-2602.safetensors`. **The code path exists.** What
does not exist is a klein-4B-trained checkpoint for it — the only published weights target
FLUX.2-**dev**, which is `flux-non-commercial-license`. So klein is blocked by *missing weights
under a usable license*, not by architecture. Same verdict, different and more precise reason —
and it means a klein control checkpoint could appear at any time without an architecture change.

---

# Gap-check pass

## The big miss: a fourth base nobody has evaluated — Z-Image

The report scoped itself to the three bases A1/R2 handed it and never asked whether a base
outside that list solves the problem. One does, and it was hiding in the same `alibaba-pai` org
the report was already reading (`Z-Image-Turbo-Fun-Controlnet-Union` sits directly above
`FLUX.2-dev-Fun-Controlnet-Union` in that org's repo listing).

**`Tongyi-MAI/Z-Image-Turbo`** — all verified directly:

| Property | Verified value |
|---|---|
| License | `apache-2.0`, `"gated": false` |
| Size | 6,154,908,736 params (~12.3 GB BF16) |
| Model card | "6B parameters… fits comfortably within **16G VRAM** consumer devices", 8 NFEs |
| Adoption | **1,044,803** downloads; `Comfy-Org/z_image_turbo` has **4,613,500** |
| Architecture | Scalable Single-Stream DiT (S3-DiT) |

And every gate this bullet exists to test:

- **Depth control**: `alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union` — Apache 2.0, ungated,
  **53,338 downloads**. README: "supports multiple control conditions—including Canny, HED,
  **Depth**, Pose and MLSD… can be used like a standard ControlNet."
- **ComfyUI**: `class ZImage(Lumina2)` is in ComfyUI core `supported_models.py:1171`, and
  `Comfy-Org` publishes an official repackaging. The *ControlNet* loads through
  **VideoX-Fun's own ComfyUI node pack** (`aigc-apps/VideoX-Fun`, **Apache-2.0**, 2,175 stars,
  pushed 2026-07-16 — four days before this research), which ships `comfyui/z_image/nodes.py`.
- **Composability — the question A3 hinged on**: that same file defines **`LoadZImageLora`
  (line 678) and `LoadZImageControlNetInPipeline` (line 704) in one pipeline.** A LoRA and a
  depth ControlNet applied together is a first-class, shipped code path, not an untested stack.
- **LoRA training**: ai-toolkit's README lists `Z-Image`, `Z-Image-Turbo`, **and
  `ostris/Z-Image-De-Turbo`** — a de-distilled variant published specifically as a training
  target, structurally the same base-vs-distilled split BFL recommends for klein.

At 6B / ~12.3 GB, this is the only candidate that plausibly runs **and trains** without the
24 GB upgrade being strictly required — and it is the only one of the four where depth control,
LoRA training, and LoRA+ControlNet composition are all Apache 2.0 and all already implemented.

**Honest limits — this is a lead, not a conclusion:**
- **Image quality is entirely unassessed.** R2 never evaluated Z-Image; nothing here says it
  reaches the dark-painterly register. That is the whole point of the base choice and it is
  untested.
- **Not ComfyUI core.** ControlNet runs through a third-party pack (Apache, active, but a
  dependency the pipeline does not have today).
- **Depth precision unverified** against xinsir's behavior on ortho depth maps from real
  geometry — the same gap the report correctly flagged for every non-SDXL option.
- Turbo is distilled at 8 steps; whether that constrains style-LoRA expressiveness is exactly
  what `Z-Image-De-Turbo` exists to address, but that is unverified.

## Second gap: nothing was tested, only catalogued

Every non-SDXL verdict rests on repo metadata. The decisive experiment is small and already
scriptable with what is in the repo: take one existing ortho depth render from
`prop_texture.py`, run it through the incumbent SDXL/xinsir path and through the Qwen-Image and
Z-Image paths, and compare reprojection fidelity by eye. That is a bounded GPU check, not a
research question — and it would settle in an afternoon what no amount of further reading can.

## Third gap: the incumbent got graded on a curve

SDXL is the only base scored "zero open risk" — but it is the base the user ruled out on
**quality**, which is the one axis this bullet never scored. A4 measures control maturity, and
control maturity is exactly where an older ecosystem wins by construction. Worth stating plainly
so the table is not misread as "keep SDXL": it says SDXL has the best *tooling*, which was never
in dispute.

## Net position

The agent's central finding holds: **FLUX.2 klein 4B has no usable depth-control path today, so
A3's base selection cannot stand as-is.** But the conclusion "fall back to Qwen-Image" is
premature — Qwen-Image is 40.9 GB BF16 and needs aggressive quantization to train on 24 GB,
whereas **Z-Image (6B, Apache, depth ControlNet + LoRA composition already shipped in one Apache
node pack) is the better-shaped candidate on every axis this bullet measures.** Its quality is
unknown, and that gap is closed by generating images, not by more research.

---

# Correction from A5b setup (orchestrator, 2026-07-20)

**My gap-check claim that Z-Image's depth control "runs through VideoX-Fun's own ComfyUI node
pack" is wrong.** Found while building the bake-off harness.

Z-Image's Fun ControlNet loads through **ComfyUI core nodes**, in an **official
Comfy-Org workflow template** — `templates/image_z_image_turbo_fun_union_controlnet.json` in
`Comfy-Org/workflow_templates`. Its graph:

```
ModelPatchLoader(Z-Image-Turbo-Fun-Controlnet-Union.safetensors) -> MODEL_PATCH
QwenImageDiffsynthControlnet(model, model_patch, vae, image, strength) -> MODEL
```

Both are core (`comfy_extras/nodes_model_patch.py:227` and `:515`). No custom node pack, no
VideoX-Fun install.

**Why both the agent and I missed it:** we each grepped `comfy/controlnet.py` for a `z_image`
loader and found nothing, then concluded no core support existed. But this is not a ControlNet
in ComfyUI's sense at all — it is a **model patch**, applied to the MODEL rather than to
conditioning, so it never touches the ControlNet subsystem. Absence from `controlnet.py` was
evidence of a different architecture, not of missing support. Confusingly, the core node is
named `QwenImage...` and is reused for Z-Image because both are DiffSynth-lineage patches.

**Revised A4 verdict for Z-Image:** depth control is Apache 2.0, core-node, officially
templated. Its ComfyUI story is now *better* than the report's, and roughly level with
Qwen-Image's InstantX path rather than a tier below it.

## Second correction: negative prompts do not transfer

Both Z-Image and Qwen-Image's official templates run at **cfg 1.0** (Z-Image zeroes the negative
via `ConditioningZeroOut`). At cfg 1 a negative prompt has no effect.

This matters because `prop_multiview.json` enforces flat lighting **through its negative
prompt** — `"dramatic lighting, strong shadows"`. That control silently disappears on a cfg-1
base, and flat albedo is a hard requirement of the texturing stage, not a preference. Any base
swap to a distilled cfg-1 model must move that constraint into the positive prompt. The
bake-off's `wf_zimage.json` does exactly that, and whether it holds as well is one of the
things the run measures.
