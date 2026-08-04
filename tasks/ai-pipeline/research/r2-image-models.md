# R2 — Image generation models for the AI art pipeline

Research date: 2026-07-20. Every model name, score, price, and license claim below is sourced
from a live WebSearch/WebFetch on this date; no figure comes from training-data memory. Where a
claim could not be independently verified it is marked **UNVERIFIED**. This report continues
[r1-compute.md](./r1-compute.md), which established the compute/hosting landscape (RTX 3080 Ti,
12 GB VRAM, 32 GB RAM local; Modal/Replicate/RunPod/Vast.ai as the practical cloud options) and
one load-bearing correction that carries forward into this report: **this pipeline is unattended
and batch/overnight-tolerant, so local wall-time is nearly free — the binding local-vs-cloud
question is whether a quantized model visibly degrades output quality, not how many
seconds/image it takes.**

Judging criterion throughout, per the brief: **quality first.** Cost is reported, never a filter.
"Runs on 12 GB" is a reported attribute per option, not an exclusion test.

---

## Snapshot: the current quality ranking

[Artificial Analysis](https://artificialanalysis.ai/image/leaderboard/text-to-image) runs the
most-cited blind-preference (Elo) leaderboard for text-to-image; scores below are from a live
fetch on 2026-07-20. This is **one benchmark among several** (see caveats after the table) but is
the best single cross-model reference point found.

| Rank | Model | Provider | Elo | Open weights? |
|---|---|---|---|---|
| 1 | GPT Image 2 (high) | OpenAI | 1339 | No |
| 2 | MAI-Image-2.5 | Microsoft AI | 1266 | No |
| 3 | HiDream-O1-Image-1.5 | HiDream | 1265 | No (proprietary variant) |
| 4 | GPT Image 1.5 (high) | OpenAI | 1258 | No |
| 5 | Nano Banana 2 Lite (Gemini 3.1 Flash-Lite Image) | Google | 1258 | No |
| 6 | Nano Banana 2 (Gemini 3.1 Flash Image Preview) | Google | 1254 | No |
| 7 | Reve 2.0 | Reve | 1246 | No |
| 8 | Nano Banana Pro (Gemini 3 Pro Image) | Google | 1218 | No |
| 9 | Cosmos3-Super-Text2Image (agentic) | NVIDIA | 1217 | **Yes** (OpenMDW-1.1) |
| 10 | Recraft V4.1 Utility Pro | Recraft | 1208 | No |
| 14 | Krea 2 Medium | Krea | 1196 | Yes, variant-dependent (see §1) |
| 15 | FLUX.2 [max] | Black Forest Labs | 1192 | No (API-only tier) |
| 16 | Seedream 4.0 | ByteDance Seed | 1189 | No |
| 18 | HiDream-O1-Image-Dev-2604 | HiDream | 1186 | **Yes** (MIT) |
| 19 | FLUX.2 [pro] | Black Forest Labs | 1185 | No |
| 21 | FLUX.2 [flex] | Black Forest Labs | 1178 | No |
| 23 | Qwen Image 2.0 Pro (2026-04-22) | Alibaba | 1171 | No (hosted Pro tier) |
| 24 | Luma UNI 1 Max | Luma Labs | 1171 | No |
| 26 | Ideogram 4.0 Quality | Ideogram | 1169 | Partial — see §2 |
| 29 | ERNIE Image | Baidu | 1163 | **Yes** (Apache 2.0) |

Notably absent from this table's visible open-weight tier: **FLUX.2 [dev]** itself (the base
open-weight checkpoint, distinct from the hosted [pro]/[max]/[flex] API tiers) — it clusters
lower, in the 1150-1185 range per the same source's category summary, behind HiDream and
Cosmos3. **Caveat on this whole table**: Elo-from-blind-votes rewards "which image do untrained
raters click as prettier," which correlates with punchy contrast/saturation and photographic
realism — not with the things this pipeline actually needs (depth-map controllability, multi-view
coherence, style-lock fidelity). Treat rank as one input, not the verdict. [Artificial Analysis
leaderboard](https://artificialanalysis.ai/image/leaderboard/text-to-image)

---

## 1. Local open-weights models

The field has moved completely since FLUX.1 (which the brief named and which is now confirmed
superseded, per R1). The current open-weight generation is FLUX.2, Qwen-Image / Qwen-Image-2.0,
HiDream-I1 / HiDream-O1-Image, Chroma1-HD, Z-Image, plus two more that turned up in this pass
that were not in the original list: **ERNIE Image** (Baidu) and **Cosmos3-Super-Text2Image**
(NVIDIA).

### FLUX.2 [dev] (32B) and [klein] (4B / 9B) — Black Forest Labs

- **Description**: BFL's current flagship line. FLUX.2 [dev] is the 32B flow-matching
  transformer, released 2025-11-25, delivering the highest visual fidelity among openly-licensed
  BFL checkpoints. FLUX.2 [klein] (4B and 9B) is a fast/small distilled family released
  2026-01-15, built for real-time and consumer-hardware use. [BFL FLUX.2
  blog](https://bfl.ai/blog/flux-2), [MarkTechPost on
  klein](https://www.marktechpost.com/2026/01/16/black-forest-labs-releases-flux-2-klein-compact-flow-models-for-interactive-visual-intelligence/)
- **Technology**: Flow-matching diffusion transformer (MMDiT lineage), same family as FLUX.1 but
  scaled and retrained.
- **License / commercial IP terms**: **Split by variant.** FLUX.2 [dev] and FLUX.2 [klein] 9B are
  under the **"FLUX Non-Commercial License"** (renamed from the old FLUX.1-dev license, no
  material change) — not shippable in a commercial game without a paid license. **FLUX.2 [klein]
  4B is Apache 2.0** — full commercial use, no royalties, derivatives allowed. Commercial rights
  to the larger models come via BFL's **Builder tier**: 10,000 images/month, single domain,
  includes fine-tuning + LoRA rights, self-serve via `dashboard.bfl.ai/licensing` — **price not
  published**, requires a logged-in account to see (confirmed dead-end in R1, re-confirmed here).
  [bfl.ai/licensing](https://bfl.ai/licensing)
- **Cost**: Builder-tier price UNVERIFIED (account-gated). Hosted API tiers ([pro]/[max]/[flex])
  are pay-per-image through third parties (fal.ai, Replicate, etc.) at roughly $0.02-0.08/image
  depending on tier — not independently re-priced in this pass, see R1 for the general cloud-API
  cost landscape.
- **VRAM / local-12GB fit**:
  - FLUX.2 [dev] (32B): bf16 ~64 GB, fp8 ~32 GB, GGUF Q4 ~19 GB. **Does not fit 12 GB at any
    quantization level with published evidence** — even Q4 needs ~19 GB.
    [willitrunai.com](https://willitrunai.com/blog/flux-2-klein-9b-vram-requirements)
  - FLUX.2 [klein] 4B: reported ~13 GB at the precision level community guides recommend for a
    24 GB card, which is tight but plausibly fits 12 GB at a lower quant — **not independently
    confirmed at a specific GGUF level for a 12 GB card**, flagged as a gap below.
  - FLUX.2 [klein] 9B: intermediate, no clean 12 GB figure found.
- **Wall-time**: klein family is explicitly built for sub-second-class inference; dev is slower
  (standard 20-50 step diffusion transformer at 32B scale).
- **ControlNet/LoRA ecosystem**: FLUX offers ControlNets for canny, depth, and a union model —
  present and used. Ecosystem is "leaner" than SDXL's but "accelerating quickly." LoRA training
  tooling is strong: **kohya_ss (sd-scripts)** has had "rock solid" FLUX.2 support since late
  2025; **ai-toolkit** (Ostris) is BFL's own recommended trainer, supporting both dev and klein.
  [thundercompute.com](https://www.thundercompute.com/blog/best-open-source-image-generation-models)
- **Pros**: Highest visual fidelity among the openly-distributed BFL checkpoints; the LoRA/style
  fine-tuning path is the most mature and best-documented of any 2026-generation open model
  (official BFL blog post walks through klein LoRA training end to end); FLUX Redux gives an
  actual style/image-prompt adapter (BFL's IP-Adapter equivalent).
- **Cons**: FLUX.2 [dev] itself is non-commercial and does not fit 12 GB; the commercially-clean
  path (klein 4B Apache-2.0, or a paid Builder license for dev) is a real narrowing of options;
  BFL pricing opacity makes budgeting hard without creating an account.
- **Where it falls short of a human concept artist**: struggles with genuinely novel structural
  invention (architectural logic of a cathedral ruin that must actually stand up, consistent
  wrought-iron joinery across a turnaround) — it excels at surface/material fidelity, less at
  invented-but-coherent 3D structure, which is exactly the multi-view consistency weakness the
  brief flags as disqualifying if unaddressed.
- **Comparable shipped-game art quality**: no verified public disclosure found of a shipped title
  built on FLUX.2 output directly. Qualitatively, FLUX.2 [dev]'s best single-image output is in
  the range of strong AA marketing key art, not the sustained, art-directed consistency of
  Diablo 4 / PoE2 — this is my own qualitative assessment, not a sourced claim.
- **Maturity**: dev is production-proven (widely deployed since Nov 2025); klein is newer
  (Jan 2026) but built directly on the same lineage — moderate-to-high confidence either way.

### Qwen-Image (20B) and Qwen-Image-2.0 (7B) — Alibaba

- **Description**: Qwen-Image (20B MMDiT) launched first; **Qwen-Image-2.0** (7B) followed
  2026-02-10 with a much lighter architecture that scores *higher* on benchmarks than its bigger
  predecessor — DPG-Bench 88.32 vs. FLUX.1's 83.84 — and holds #1 on the AI Arena blind-eval
  platform in both generation and editing. [qwenimages.com
  blog](https://qwenimages.com/blog/qwen-image-2-release)
- **Technology**: Diffusion transformer with strong native text-rendering (bilingual CN/EN),
  unified generation+editing in the 2.0 line.
- **License / IP terms**: **Apache 2.0**, full commercial use, no revenue cap, no attribution
  requirement beyond the license text. [GitHub
  LICENSE](https://github.com/QwenLM/Qwen-Image/blob/main/LICENSE) — this is the cleanest
  commercial license of any model in this report.
- **Cost**: free to self-host; Alibaba Cloud Model Studio hosts a Pro API tier (Qwen Image 2.0 Pro
  ranks #23 on the AA leaderboard) at unconfirmed per-image pricing.
- **VRAM / local-12GB fit**: for the 20B line, bf16 needs 24GB+, NF4 16-20GB, GGUF Q4 gets the
  diffusion-transformer component to roughly 12-13 GB — but R1 already established the **text
  encoder (Qwen2.5-VL) alone needs ~17 GB in bf16**, so the full 20B pipeline does not
  simultaneously fit 12 GB without also quantizing/offloading the text encoder. **Qwen-Image-2.0
  at 7B is a much better 12 GB fit** — no specific VRAM figure was found for it in this pass
  (gap, flagged below), but scaling from the 20B numbers, a 7B DiT should comfortably clear 12 GB
  even at fp8.
- **Wall-time**: not independently benchmarked on a 3080 Ti-class card in this pass; R1 cites
  30-60 sec/image as a rough community figure for 12 GB-class cards with the 20B model under GGUF
  quantization.
- **ControlNet/LoRA ecosystem**: ControlNets exist for depth, pose, lineart, softedge — a
  dedicated **Qwen-Image-Blockwise-ControlNet-Depth** model is published on Hugging Face, directly
  relevant to this pipeline's depth-reprojection texture step. [HF
  model](https://huggingface.co/SahilCarterr/Qwen-Image-Blockwise-ControlNet-Depth). LoRA training
  is supported by **OneTrainer**, **Musubi Tuner**, and **Civitai's** training orchestration; one
  practitioner write-up describes hands-on OneTrainer Qwen-Image LoRA training. Ecosystem is
  described as "smaller" than FLUX/SDXL but actively growing.
- **Pros**: cleanest commercial license in this report bar none; genuinely dedicated depth
  ControlNet already exists (directly matches the pipeline's stated need); strong benchmark
  standing, especially the 2.0/7B line for local fit.
- **Cons**: the 20B variant's full pipeline (DiT + text encoder) does not comfortably fit 12 GB
  simultaneously; LoRA/ControlNet ecosystem, while growing, is behind FLUX's in raw tooling
  volume and community checkpoint count.
- **Where it falls short**: strong text rendering and instruction-following, but community
  consensus (echoed across several of this pass's sources) places its raw painterly/atmospheric
  quality a step behind FLUX.2/HiDream-tier models for moody, painterly dark-fantasy work
  specifically — it is comparatively strongest at structured/graphic content (posters, UI,
  infographics) per its own release notes, which is a strike for atmospheric concept art but an
  asset for UI/icon generation if that's ever needed.
- **Comparable shipped-game art quality**: no disclosed case found. Own assessment: 7B/2.0 output
  quality sits around solid mobile/mid-tier PC game key-art, not AAA dark-fantasy tier without
  heavy style LoRA work (see §3).
- **Maturity**: production-proven at API scale (Alibaba Cloud hosts it commercially); local
  tooling is community-maintained and improving monthly.

### HiDream-I1 (17B) and HiDream-O1-Image (8B) — HiDream-ai

- **Description**: HiDream-I1 (17B, MIT, released 2025-04-07) was the prior-generation strong
  open model. **HiDream-O1-Image** (8B, MIT, released 2026-05-08) is the newer "reasons before it
  draws" model — smaller than FLUX.2 [dev] by 4x yet **matches or beats it on five published
  benchmarks**, including GenEval 0.90. [WaveSpeed
  writeup](https://wavespeed.ai/blog/posts/hidream-o1-image-dev-pixel-unified-transformer/) A
  proprietary hosted variant, **HiDream-O1-Image-1.5**, ranks **#3 overall** on the Artificial
  Analysis leaderboard (1265 Elo) — ahead of GPT Image 1.5 and every FLUX.2 tier — while the
  open-weight **HiDream-O1-Image-Dev-2604** checkpoint ranks #18 overall / effectively #2
  open-weight (1186 Elo), a real gap under Cosmos3 but ahead of every FLUX.2 open tier.
- **Technology**: pixel-native transformer ("no VAE" per one summary) — an architectural
  departure from the latent-diffusion norm most other models on this list share.
- **License / IP terms**: **MIT** — for both I1 and O1-Image. This is as permissive as it gets:
  personal, research, and commercial use, no revenue cap, no field-of-use restriction found.
  [HiDream-I1 model
  card](https://huggingface.co/HiDream-ai/HiDream-I1-Full) confirms MIT for commercial use.
- **Cost**: free to self-host (MIT); no confirmed hosted API pricing found for the open checkpoint
  in this pass (the #3-ranked -1.5 variant is the closed hosted version, price UNVERIFIED).
- **VRAM / local-12GB fit — the standout local candidate**: HiDream-I1 fp8 needs ~16 GB, GGUF Q4
  ~12 GB, Q2 ~8 GB. **HiDream-O1-Image at fp8 fits ~10 GB** and is explicitly reported tested on
  12 GB cards (RTX 3080/4070/4080 named directly) at 2048×2048 resolution — this is the single
  most concrete "yes, this fits your card" data point found across every model researched.
  [GitHub HiDream-I1-FP8](https://github.com/envy-ai/HiDream-I1-FP8),
  [drbaph/HiDream-O1-Image-FP8](https://huggingface.co/drbaph/HiDream-O1-Image-FP8)
- **Wall-time**: not independently benchmarked here for a 3080 Ti; the fp8 8B-class size suggests
  meaningfully faster than the 20B/32B competitors at equivalent quant depth.
- **ControlNet/LoRA ecosystem**: thinner than FLUX/SDXL — this pass found quantized-checkpoint
  tooling (nf4, GGUF, fp8 variants proliferate fast on Hugging Face/Civitai) but did **not** find
  a dedicated depth-ControlNet for HiDream specifically, which is a real strike against it for
  this pipeline's stated depth-reprojection requirement. Flagged as a gap.
- **Pros**: best quality-per-GB of any open-weight model researched; MIT license removes all
  commercial-use anxiety; concretely confirmed to run and generate at reasonable resolution on
  exactly this GPU class.
- **Cons**: no confirmed depth ControlNet — a real gap against this pipeline's core texturing
  requirement; pixel-native architecture is a genuine departure that community LoRA/ControlNet
  tooling (built mostly around latent-diffusion conventions) may take longer to catch up to; newer
  than FLUX/SD, so tooling volume and battle-testing are both thinner.
- **Where it falls short**: strong on raw single-image benchmarks; multi-view/pose-turnaround
  consistency and depth-guided control were not evidenced in this pass the way they were for
  Qwen-Image or FLUX — an open question rather than a confirmed weakness.
- **Comparable shipped-game art quality**: no disclosed case found; own assessment based on
  benchmark standing: single hero-shot output plausibly approaches upper-mid-tier AA key art;
  unverified whether that holds under the multi-view/depth-control demands this pipeline needs.
- **Maturity**: HiDream-I1 is production-proven (14+ months in the wild); HiDream-O1-Image is
  **cutting-edge/barely-used** (released 2.5 months before this report) — genuinely the newest
  model in this report's local-model section with real benchmark traction, but with the least
  battle-testing.

### Chroma1-HD (8.9B) — lodestones (independent/community)

- **Description**: An Apache-2.0 base model built on the FLUX.1-schnell architecture, explicitly
  positioned as a **true base model without aesthetic fine-tuning** — designed to be a clean
  starting point for further fine-tuning rather than a polished out-of-the-box product.
  [HF model card](https://huggingface.co/lodestones/Chroma1-HD)
- **Technology**: FLUX.1-schnell-derived diffusion transformer, 8.9B.
- **License / IP terms**: **Apache 2.0** — full commercial rights, no restrictions found.
- **Cost**: free, self-hosted only; no hosted API presence found in this pass.
- **VRAM / local-12GB fit**: ~22 GB at fp16 for 1024×1024; fp8 best-download size ~8.9 GB, which
  should fit 12 GB comfortably; GGUF variants exist. Community guidance flags Chroma as
  "needs more than 8GB" — 12 GB is plausible but not confirmed at a specific quant/resolution
  combination in this pass.
- **ControlNet/LoRA ecosystem**: FLUX.1-schnell-derived, so it can plausibly reuse some of that
  ecosystem's tooling, though this was not directly confirmed; Chroma-specific LoRA training via
  kohya-style tooling is documented (networkDim 16, adamw8bit defaults cited in a training
  recipe).
- **Pros**: deliberately unaesthetic-by-default base is exactly the kind of clean canvas that
  favors a strong style LoRA taking full control rather than fighting a baked-in "AI look" —
  directly relevant to the brief's uniqueness requirement.
- **Cons**: smaller community, no commercial hosted option, "no aesthetic tuning" means
  out-of-the-box output likely needs more prompt/LoRA work to look finished than FLUX.2 or
  HiDream.
- **Where it falls short**: as an unrefined base, raw single-shot quality trails the frontier
  models in this list; the entire value proposition is what you build on top of it, not its
  default output.
- **Comparable shipped-game art quality**: not assessable out-of-the-box; depends entirely on
  fine-tuning investment.
- **Maturity**: **cutting-edge/community-maintained**, not a lab-backed release — genuinely
  useful niche (fine-tuning substrate) rather than a general answer.

### Z-Image / Z-Image-Turbo (6B) — Tongyi-MAI (Alibaba, separate team from Qwen)

- **Description**: Released 2026-01-27 (Turbo variant), a distilled 6B model that ranked **8th
  overall** on the Artificial Analysis leaderboard at launch — the **#1 open-weight model at that
  time**, later reportedly surpassing FLUX.2 [dev], HunyuanImage 3.0, and Qwen-Image per
  Artificial Analysis's own announcement. [x.com/ArtificialAnlys
  post](https://x.com/ArtificialAnlys/status/2002839525609865575)
- **Technology**: distilled flow-matching diffusion transformer, 8 NFEs (very few sampling
  steps) for near-instant inference; a non-distilled **Z-Image Base** checkpoint was released
  alongside it specifically to give the community a fine-tunable foundation.
- **License / IP terms**: **Apache 2.0**, confirmed via the repo's own LICENSE file — full
  commercial use, no restrictions. [GitHub
  LICENSE](https://github.com/Tongyi-MAI/Z-Image/blob/main/LICENSE)
- **Cost**: free, self-hosted; Alibaba Cloud Model Studio also exposes a hosted API.
  [Alibaba Cloud Z-Image API docs](https://www.alibabacloud.com/help/en/model-studio/z-image-api-reference)
- **VRAM / local-12GB fit**: explicitly reported to fit "comfortably within 16 GB consumer
  devices" for Turbo; at 6B this is the smallest model in the entire report and should clear
  12 GB with real margin even before aggressive quantization — the best-fitting model researched
  after HiDream-O1-Image.
- **ControlNet/LoRA ecosystem**: genuinely active — **Musubi Tuner confirmed Z-Image Base
  LoRA/fine-tuning support** in a 2026-01-29 update (two days after release, unusually fast
  ecosystem uptake); **kohya_ss (Musubi Tuner)** has official presets; workflows already combine
  Z-Image with **ControlNet (depth/pose)** and inpainting per community write-ups. A
  "de-distillation" adapter exists specifically to make the distilled Turbo checkpoint more
  LoRA-trainable, since distilled models are normally harder to fine-tune well.
  [lilting.ch de-distill writeup](https://lilting.ch/en/articles/z-image-turbo-lora-dedistill-adapter)
- **Pros**: best combination of small footprint + genuinely fast-moving, already-active LoRA/
  ControlNet ecosystem found in this report; Apache 2.0; near-instant inference means iteration
  speed is exceptional even locally.
- **Cons**: as a distillation, the base Turbo checkpoint is intrinsically harder to fine-tune well
  without the de-distill workaround (documented above, but adds a step); very new (6 months old
  at most), so long-run production reliability is unproven; being 6B, raw single-image ceiling
  quality is a plausible step below the 17-32B models on painterly/atmospheric fidelity, though
  no controlled side-by-side against HiDream/FLUX was found.
- **Where it falls short**: no direct evidence found on multi-view consistency or fine detail at
  the level this pipeline's texture-projection step demands; distillation-related quality
  ceilings are a known general risk category for turbo/distilled models regardless of vendor.
- **Comparable shipped-game art quality**: not assessable from available evidence.
- **Maturity**: **cutting-edge**, released within the report's 6-month window; unusually fast
  ecosystem adoption is a positive signal but this is still an early-days model.

### Other local open-weight models surveyed (lighter treatment)

| Model | Params | License | 12GB fit | Notes |
|---|---|---|---|---|
| **SD3.5** (Large/Medium) | 8B / 2.5B | Stability AI Community License (free <$1M revenue) | Yes, comfortably | Not frontier quality anymore (superseded by FLUX.2 per its own analysis), but **the most mature ControlNet/LoRA ecosystem of any model in this report** — "the workhorse... through 2026" per community consensus. Still worth considering purely for tooling maturity if quality parity can be recovered via a strong style LoRA. [stability.ai](https://stability.ai/news-updates/introducing-stable-diffusion-3-5) |
| **Lumina-Image 2.0** | 2.6B | Apache 2.0 | Yes, easily | ICCV 2025 paper, Feb 2025 release — now a full generation behind the frontier; useful mainly as a very cheap-to-run baseline, not a quality target. [GitHub](https://github.com/Alpha-VLLM/Lumina-Image-2.0) |
| **ERNIE Image** (+ Turbo) | 8B | Apache 2.0 | Plausibly yes (8B DiT) | Baidu, released 2026-04-15, ranks in the 1160s Elo range (#29-30 on AA leaderboard) — genuinely commercial-clean and small, but not top-tier quality. Strong bilingual text rendering, per its own technical report. [ERNIE-Image technical report](https://arxiv.org/html/2605.25347v1) |
| **Cosmos3-Super-Text2Image** | **64B** | OpenMDW-1.1 (permits commercial use + derivatives) | **No** — needs H200 (141GB) or B200 (192GB)-class hardware | Tops the open-weight leaderboard at 1217 Elo (rank 9 overall, ahead of Recraft and every FLUX.2 tier) — but this is only meaningfully "open weights" if you can rent multi-hundred-GB hardware; irrelevant to a 12 GB local card and a poor cloud-rental fit too (this is enterprise-cluster scale, well past the RunPod/Vast.ai single-GPU tier covered in R1). Listed for completeness since it is the literal open-weight quality leader, but practically excluded by scale alone. [HF model card](https://huggingface.co/nvidia/Cosmos3-Super-Text2Image) |
| **Ovis-Image**, **LongCat-Image** | 7B / 6B | UNVERIFIED for Ovis-Image; LongCat ecosystem generally MIT | Likely yes at their size | Both surfaced only in listicle-style coverage in this pass; too thinly documented to assess with confidence — flagged in "corners possibly missed." |

### The quantization-degradation question — what evidence actually exists

This is the question the brief calls out as the key unknown. Findings, by source quality:

- **Q8 vs fp16/bf16**: strong, repeated community consensus across multiple independent sources
  that **Q8_0 GGUF is visually indistinguishable from full precision** — "no quality degrade,"
  "almost the same images." This is the safest quantization tier if VRAM allows it.
- **Q5 vs Q8**: also reported as "barely noticeable" loss; one direct blind test claim found —
  "users genuinely could not tell which was which on most prompts" comparing Q5 FLUX to full
  precision.
- **Q4**: consistently described as the tier where degradation becomes *visible but usable* —
  "noticeable drops in detail," "moderate quality tradeoffs," "slightly higher perplexity."
  Community sentiment splits between "Q4 is fine for most tasks" and "Q8 is the real sweet spot,
  anything lower trades quality for VRAM."
- **Q2-Q3**: degradation described as clearly visible in every source that mentions it; treated as
  a last-resort tier.
- **Model-specific evidence for our actual candidates is thin.** The clearest, most concrete
  quantization-fit claim found in this entire pass is HiDream-O1-Image at fp8 fitting ~10 GB and
  being *directly reported tested* on RTX 3080/4070/4080-class cards. For FLUX.2 and Qwen-Image,
  the evidence is either about FLUX.1 (a different, superseded model) or about LLM quantization
  (Qwen 3.6 language model, not Qwen-Image) rather than the image models themselves — **this is a
  real gap**, restated below in "could not determine."
- **No controlled, rigorous, blind A/B study was found for any of the specific 2026-generation
  image models at Q4 vs. full precision.** Every source is community forum/blog-post-level
  evidence, not a lab benchmark. This matches the honesty standard the brief asks for: real
  evidence exists and points toward "Q8 safe, Q4 usable-but-visible, Q2-3 risky" as a general
  rule, but nothing rigorous ties that specifically to FLUX.2, Qwen-Image, or HiDream-O1-Image at
  our target resolution and content type (painterly dark-fantasy concept art, not photoreal
  portraits — most quantization comparisons found were photoreal-subject tests, which may not
  transfer to painterly/stylized output where subtle degradation is easier or harder to spot,
  untested either way).

---

## 2. Commercial / hosted APIs

### GPT Image 2 — OpenAI

- **Description**: OpenAI's current flagship image model (same underlying model as the
  "ChatGPT Images 2.0" consumer product — confirmed as the same model, different product
  surfaces). Currently **#1 on the Artificial Analysis leaderboard** at 1339 Elo, a real margin
  over #2.
- **Technology**: proprietary, architecture undisclosed.
- **License / IP terms for shipped game assets**: users "own the output... OpenAI assigns all
  right, title, and interest in the output to users." **Critical gap**: OpenAI does **not**
  indemnify against third-party IP infringement claims for standard usage — "studios bear 100% of
  the infringement risk themselves" per legal-analysis coverage — unlike Adobe Firefly, which does
  offer indemnification to paid subscribers. Enterprise customers get a narrower indemnity that
  excludes trademark claims arising from commercial use and excludes modified/combined outputs.
  [terms.law 2026 AI platform comparison](https://terms.law/FAQ/ai-tools/ai-platform-terms-comparison-faq.html)
- **Cost**: token-based, not flat per-image: $8/million image input tokens, $30/million image
  output tokens, $5/million text input tokens; real-world per-image estimates cluster
  $0.005-$0.211 depending on resolution/complexity, and iterative "generate then edit" workflows
  push real cost to 2-3x the naive per-image estimate. [wavespeed.ai
  pricing analysis](https://wavespeed.ai/blog/posts/gpt-image-2-pricing-2026/)
- **VRAM/compute**: N/A, API-only.
- **Wall-time**: not independently benchmarked in this pass; generally seconds-scale for API image
  generation at this tier.
- **ControlNet/LoRA ecosystem**: **none** — closed API, no fine-tuning, no ControlNet-equivalent
  structural control beyond prompting and (per other models in this class) reference-image
  conditioning. This is the single biggest strike against it for this pipeline's core
  requirement.
- **Pros**: highest raw quality on the most-cited leaderboard; excellent text rendering (~99%
  character accuracy per comparative reviews); strong instruction-following.
- **Cons**: no commercial IP indemnification exposes the studio to infringement risk with no
  vendor backstop; zero fine-tuning/ControlNet path — cannot be steered into a proprietary house
  style beyond prompt engineering and image-to-image reference; no way to guarantee cross-view
  consistency for texture-projection work.
- **Where it falls short of a human concept artist**: cannot be locked into a consistent house
  style across hundreds of assets without either a lot of manual prompt-engineering discipline or
  accepting "generically OpenAI-flavored" output — directly the failure mode the brief calls out.
- **Comparable shipped-game art quality**: reviews describe it as "structurally sound... more
  neutral color accuracy" but lacking "the tactile realism and dynamic lighting that makes a
  render feel like a real photograph" compared to Nano Banana 2 — own assessment: best single
  images plausibly approach upper-tier marketing key art; sustained house-style consistency across
  a full asset catalog is unproven and structurally hard given the lack of fine-tuning.
- **Maturity**: production-proven at massive scale (OpenAI's consumer product), but the
  *image-specific* API is comparatively new.

### Google Nano Banana 2 / Nano Banana Pro (Gemini 3.1 Flash Image / Gemini 3 Pro Image)

- **Description**: Google's current image line inside Gemini. Three tiers found: **Nano Banana 2
  Lite** (fastest/cheapest, rank 5 at 1258 Elo — genuinely outscoring the non-Lite Nano Banana 2
  on this leaderboard snapshot), **Nano Banana 2** (rank 6, 1254), and **Nano Banana Pro** (rank
  8, 1218, but with the deepest editing feature set — up to 14 reference images blended, up to 5
  people's likeness maintained).
- **Technology**: proprietary, part of the Gemini multimodal family.
- **License / IP terms**: output is user/customer-owned; Google "does not assert ownership... in
  Generated Output." Commercial use explicitly permitted, no royalties. API/Vertex AI data is
  **not** used for training (opt-out default differs for free consumer tier).
  [terms.law Gemini rights guide](https://terms.law/ai-output-rights/gemini/)
- **Cost**: $0.50/million input tokens, $3/million output tokens for the standard tier ($0.25 /
  $1.50 for Lite); real per-image cost ~$0.067/image at 1K resolution standard API, ~$0.034/image
  via the Batch API (50% discount). [openrouter.ai pricing pages, multiple, cross-checked]
- **VRAM/compute**: N/A, API-only.
- **ControlNet/LoRA ecosystem**: none in the traditional sense, but **multi-turn, multi-image
  conditioning is a first-class, well-developed feature** — this is architecturally the closest
  thing among the proprietary APIs to what this pipeline needs for cross-view consistency: it
  maintains "accurate details across edits" and same-subject consistency through iterative,
  stateful conversation turns, explicitly including swapping backgrounds/outfits/props while
  keeping the subject recognizable. This is a genuinely different mechanism than ControlNet
  (conversational iterative editing vs. explicit structural conditioning) and its applicability to
  strict depth-map-driven multi-view texture projection is **unproven, not confirmed working for
  that specific workflow**.
- **Pros**: best-in-class photorealism per comparative reviews; strong multi-image/multi-turn
  consistency feature set; clean, permissive commercial terms; competitive price.
- **Cons**: no fine-tuning or LoRA path at all — house style is achievable only through prompting
  and reference images, session to session, with no persistent trained style; multi-turn
  consistency ≠ depth-ControlNet-grade geometric control, which is what the texture-reprojection
  step specifically needs.
- **Where it falls short**: same structural gap as GPT Image 2 — no durable, trainable style lock;
  reviews describe it as leaning "cartoonier" than GPT Image 2 for concept-art use specifically,
  which cuts against a gritty dark-fantasy direction without heavy prompt compensation.
- **Comparable shipped-game art quality**: "wins on photorealism, multi-turn editing, 4K batch
  cost" per comparative reviews — own assessment: best fit among proprietary APIs for
  photoreal texture/material reference plates, less proven for the painterly concept-art side.
- **Maturity**: production-proven, backed by Google's infrastructure; Nano Banana 2/Pro line
  itself is a 2026 release, so the *specific* model generation is fairly new even if the product
  family is established.

### Midjourney (v7 / v8.1)

- **Description**: The long-standing leader for concept-art *aesthetic* quality — one comparative
  review states "Midjourney V8.1 is the winner for game and film concept art, whose default
  aesthetic is unmatched for ideation," even though it does not appear on the Artificial Analysis
  Elo table used above (Midjourney isn't part of that leaderboard's tested set in the fetch
  obtained).
- **Technology**: proprietary, architecture undisclosed, Discord/web-first product.
- **License / IP terms**: paid tiers (Basic $10/mo, Standard $30/mo) grant full commercial rights;
  free tier has **zero** commercial rights. Companies with >$1M annual gross revenue must be on
  Pro ($60/mo) or Mega ($120/mo) — applies to the entire corporate entity, not per-seat. Important
  copyright nuance: a subscriber gets a broad **use license** but courts (per Thaler v.
  Perlmutter) hold that purely AI-generated portions aren't independently copyrightable absent
  human authorship — selective composition/editing/prompt-engineering contributions may be.
  [terms.law 2026 Midjourney guide](https://terms.law/2026/01/15/midjourney-commercial-use-rights-complete-2026-guide/)
- **Cost**: subscription-based as above, not metered per-image within plan limits.
- **VRAM/compute**: N/A.
- **ControlNet/LoRA/automation**: **the single biggest practical strike against Midjourney for
  this project** — the official API is **enterprise-dashboard-gated** (apply for developer
  access), and prior to/outside that, there is **no public API**, meaning "character consistency
  workflows cannot be automated... every generation requires manual interaction." For a scripted,
  unattended batch pipeline (the shape this whole project is built around, per R1), this is a hard
  structural mismatch unless Enterprise API access is secured. `--cref` (character reference) and
  `--sref` (style reference) are genuinely strong, purpose-built consistency tools when used
  interactively — `--cref` targets "who" (facial/physical features), `--sref` targets "how it
  looks" (palette/aesthetic), and they can be combined — but this power is locked behind manual or
  Enterprise-only automation.
- **Pros**: widely regarded as having the best default aesthetic sense for fantasy/game concept
  art of any model surveyed; --cref/--sref is a purpose-built, mature consistency toolset.
- **Cons**: no accessible API for a solo dev's automated pipeline (Enterprise-only); no
  fine-tuning/LoRA path at all — "house style" is achieved entirely through sref image references
  and prompt discipline, which drifts over hundreds of generations without a trained anchor; the
  copyright-authorship nuance adds legal texture worth being aware of even though the use-license
  itself is broad.
- **Where it falls short**: same core problem as the other proprietary APIs — no durable trained
  style; additionally, the automation gate makes it structurally awkward for exactly this
  pipeline's batch/scripted shape regardless of quality.
- **Comparable shipped-game art quality**: widely used across the games industry for *concept
  ideation* (per multiple sources) — this is the API where "used at a shipped studio" is most
  plausible, though no specific shipped-title confirmation was found in this pass.
- **Maturity**: production-proven, the longest-established of the proprietary APIs surveyed.

### Ideogram 4.0

- **Description**: 9.3B-parameter model, leads on typography/layout among open-weight-adjacent
  models; ranks #26 on the AA leaderboard (1169 Elo, "Quality" tier).
- **License / IP terms — genuinely three-tier and worth reading carefully**: (1) the
  **downloadable Hugging Face weights are Non-Commercial only**, no revenue threshold, no
  small-business exemption — any monetized self-hosted use requires (2) a **self-serve commercial
  license** covering 10K-100K images/month for self-hosted quantized weights, or (3) full
  **Enterprise** licensing for >100K images/month, full precision, or API-like third-party access.
  Using the hosted `ideogram.ai` subscription or developer API sidesteps all of this and is
  commercially clean out of the box. [ideogram.ai/licensing](https://ideogram.ai/licensing/)
- **Cost**: API $0.03 (Turbo) - $0.10 (Quality) per image; subscriptions from $15/mo (Plus) to
  $42/mo (Pro).
- **ControlNet/LoRA**: not found for the hosted product; the open-weight variant's fine-tuning
  story was not clearly evidenced in this pass — flagged as a gap.
- **Pros**: best-in-class text/typography rendering; a real (if gated) self-hosting path exists,
  unlike most other proprietary-leaning APIs on this list.
- **Cons**: the license structure is a trap for an unwary solo dev — grabbing the "open weights"
  from Hugging Face and shipping a commercial game with them directly violates the Non-Commercial
  Model Agreement; the correct path (self-serve commercial license or the hosted API) must be
  deliberately chosen.
- **Comparable shipped-game art quality**: not assessed; typography strength is not directly
  relevant to this pipeline's concept-art/texture use case.
- **Maturity**: production-proven, actively iterated (4.0 was a mid-2026 release).

### Recraft V4.1

- **Description**: Ranks well on the leaderboard (#10 at 1208 Elo for Utility Pro), but its real
  differentiator is **design-system/brand-consistency tooling** — native SVG vector output,
  editable layers, and a "brand style system" that locks a color palette/illustration
  style/aesthetic direction across a whole generated set.
- **License / IP terms**: "you keep full ownership and commercial rights to those images even
  after cancellation" for paid API usage.
- **Cost**: ~$0.035-0.04/image standard, $0.21/image for the Pro tier (Vercel AI Gateway pricing).
- **ControlNet/LoRA**: proprietary, closed — the "brand style" feature is Recraft's own
  style-lock mechanism, not an open fine-tuning path; cannot be exported or reused outside
  Recraft's product.
- **Pros**: closest thing among the proprietary APIs to a built-in "house style" feature — a real,
  purpose-built answer to part of the uniqueness requirement, if you're willing to be locked into
  Recraft's ecosystem for it; native vector output is directly useful for UI/icon work adjacent to
  this pipeline.
- **Cons**: raster photoreal/painterly quality is not the leaderboard leader; the "brand style"
  lock-in is Recraft-proprietary — you cannot take that trained style elsewhere the way you could
  a portable LoRA file.
- **Comparable shipped-game art quality**: strongest for stylized/vector or UI-adjacent work,
  weaker fit for painterly dark-fantasy concept art specifically.
- **Maturity**: production-proven, actively used for brand/marketing design work industry-wide.

### Seedream 4.5 (ByteDance Seed)

- **Description**: ranks #28 (1165 Elo); optimized for 4K output, multi-image consistency, and
  text accuracy.
- **License / IP terms**: "all paid plans include a commercial license... marketing, advertising,
  products, and resale" — broadly clean for shipped commercial use.
- **Cost**: ~$0.03-0.045/image depending on provider (EvoLink, PoYo, ByteDance direct all quoted
  slightly different numbers in this pass — treat as approximate).
- **ControlNet/LoRA**: proprietary, closed; no self-hosting path found (unlike Ideogram).
- **Pros**: cheap per-image; strong multi-image consistency claims relevant to this pipeline's
  cross-view requirement, though not independently verified against a depth-ControlNet-equivalent
  standard.
- **Cons**: no fine-tuning/style-lock path at all; being China-hosted (ByteDance), data-residency
  and long-term platform-stability considerations for an EU-based commercial project were not
  evaluated in this pass.
- **Comparable shipped-game art quality**: not assessed; general commercial creative use (e-comm,
  advertising) is its documented use case, not games specifically.
- **Maturity**: production-proven within its home market; less established in Western game-dev
  workflows specifically.

### Krea 2 (Raw / Turbo / Medium / Large)

- **Description**: genuinely notable — a **from-scratch 12.9B single-stream DiT** (not a FLUX or
  SD derivative) built explicitly for aesthetic/style control, with Krea 2 Raw and Turbo released
  as **open weights**. Ranks #14 (Medium, 1196 Elo).
- **Technology**: single-stream multimodal DiT, grouped-query attention, learned output gate,
  per-head QK norm, 3-axis RoPE; text conditioning via **Qwen3-VL-4B-Instruct** tapped at 12
  layers; VAE is the **Qwen-Image autoencoder** — an interesting cross-pollination with the Qwen
  ecosystem that may mean some tooling crossover, unconfirmed. [Krea 2 technical
  report](https://www.krea.ai/blog/krea-2-technical-report)
- **License / IP terms**: hosted platform commercial use requires at least the $9/mo Basic plan
  (free tier has no commercial license); the **open-weight Raw/Turbo variants are under a Krea 2
  Community License** — free commercial use under $1M annual revenue and 50 seats, custom
  Enterprise license required above that. Krea explicitly states it "does not claim copyright or
  other IP rights over content generated by users."
- **Cost**: API $0.015 (Turbo) - $0.06 (Large) per image; platform plans $9-$70/mo.
- **VRAM / local-12GB fit**: 12.9B parameters — in the same size class as FLUX.1-dev; no direct
  quantized-VRAM figure was found in this pass (gap), but by parameter-count analogy to FLUX.1-dev
  (fp8 ~12GB, GGUF Q4 ~7GB) this should plausibly fit 12 GB at fp8 or better — **unconfirmed,
  flagged below**.
- **ControlNet/LoRA ecosystem**: too new for a mature ecosystem assessment; being open-weight and
  built with a Qwen-Image-compatible VAE, there's a plausible-but-unconfirmed path for
  cross-compatible tooling. This is worth a direct hands-on check given how recently (2026) it
  shipped.
- **Pros**: explicitly built "aesthetic-first" with real style control as a design goal (not
  bolted on); open weights with a genuinely usable community license; strong leaderboard standing
  for an open model; built from scratch rather than another FLUX/SD fine-tune, which is itself
  interesting for the uniqueness angle — its default aesthetic is not "the same base model
  everyone else is using."
- **Cons**: youngest architecture in this report with the least tooling maturity; VRAM-at-quant
  figures unconfirmed for our specific card.
- **Comparable shipped-game art quality**: not assessed; too new.
- **Maturity**: **cutting-edge**, released mid-2026 — the single most interesting "watch this
  closely" entry in the whole report given its explicit aesthetic-control design goal, but
  genuinely unproven in production.

### Reve 2.0, Luma Photon — brief treatment

- **Reve 2.0**: ranks #7 (1246 Elo), a real jump from Reve's prior standing. API price ~$0.0067/
  image (cheapest frontier-tier API found in this pass). Commercial use rights specifically gated
  to the **Enterprise 2.0** subscription tier — lower tiers do not include commercial rights per
  the pricing page structure found. Layout-first, native 4K, code-like layout control per one
  review. No ControlNet/LoRA path found; proprietary.
- **Luma Photon** (+ Photon Flash): extremely cheap — $0.015/image (Photon), $0.002/image (Photon
  Flash) at 1080p, claimed 10x faster than competitors. Commercial licensing language is
  plan-specific and was **not fully resolved** in this pass — "check the plan-specific licensing
  language before using output in client or paid work" was the most concrete guidance found,
  which is itself a signal to verify directly before relying on it. Ranks well down the
  leaderboard relative to price (Luma UNI 1 Max, a different/newer Luma model, is the one that
  appears at rank 24; Photon itself wasn't directly on the fetched leaderboard slice). No
  ControlNet/LoRA path found.

---

## 3. Style uniqueness — how to get a proprietary house style

This is the section the brief flags as potentially the most important, and the research bears
that out: **every model surveyed above, used at default settings, produces recognizably "that
model's" output** — Nano Banana leans cartoonish-photoreal, GPT Image 2 leans neutral/structural,
Midjourney leans painterly-dramatic, FLUX leans photoreal-crisp. None of them, out of the box,
produces the Castilian-gothic-baroque penitent/cathedral-ruin aesthetic the project needs. The
brief's "house style you cannot find in any existing asset ecosystem" requirement is only solvable
by **fine-tuning or a strong style-reference pipeline on top of a base model**, not by prompting
alone.

### Fine-tuning (LoRA) — the durable, portable answer

**What it takes, by tool:**

- **kohya_ss (sd-scripts)**: the most widely used LoRA trainer; **FLUX.2 support landed late 2025
  and is described as "rock solid."** Also underlies "Musubi Tuner," which has official Z-Image
  and other-model presets.
- **ai-toolkit (Ostris)**: BFL's own recommended trainer for FLUX.2, web-UI based, supports both
  dev (32B) and klein (4B/9B).
- **SimpleTuner**: general-purpose, geared toward image/video/audio diffusion fine-tuning broadly,
  used for FLUX.1-era style/concept LoRAs historically.
- **OneTrainer**: broadest per-model coverage found — explicitly supports **Z-Image, Qwen-Image,
  FLUX.1, FLUX.2 dev and klein** in one tool, trades UI simplicity for exposed low-level control
  (optimizer choice, quantization settings) that ai-toolkit hides. A practitioner write-up
  specifically documents training a Qwen-Image LoRA in OneTrainer.
  [Civitai OneTrainer/Qwen-Image writeup](https://civitai.com/articles/31712/training-lora-for-qwen-image-as-example-in-onetrainer-my-experience)

**Cost and wall-time — concrete, sourced numbers:**

- A FLUX.2 [klein] 4B LoRA: **fits in 24 GB VRAM**, takes **about an hour on an RTX 4090**, costs
  **roughly $0.50** on a rented 4090. BFL's own blog walks through this end to end.
  [HF blog: fine-tune klein under 60 minutes](https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora)
- **Dataset size**: **15-40 images that share one look** for a style LoRA (BFL's own guidance);
  a separate community guide cites 15-30 or 20-60+ images with 1000-3000 training steps depending
  on target model. Edit-style LoRAs (learning a transformation rather than a look) want more:
  50-200 paired images.
- **Budgeting for iteration**: 2-3 training passes to dial in rank/learning-rate/dataset
  composition puts a fully-tuned FLUX.2-klein-class LoRA at **$5-15 total** on a single rented
  consumer GPU (RunPod RTX 4090 $0.34-0.69/hr, Vast.ai $0.29-0.59/hr, both confirmed live in R1).
- **Larger models cost more to train**: one source states **FLUX.2 [dev] (32B) training needs
  ~80 GB VRAM** — i.e., an A100/H100-class rental, not a 4090, and definitely not the local 3080
  Ti. This is a real, sourced constraint: **training a style LoRA for FLUX.2 [dev] itself cannot
  happen on the local 12 GB card at all** — klein is the locally-trainable tier; dev-tier training
  is a cloud-only exercise. Similarly, **Qwen-Image (20B) training wants ~32 GB**, also beyond the
  local card. [Spheron cost
  analysis](https://www.spheron.network/blog/fine-tune-flux2-wan-lora-cost-gpu-cloud-2026/)
- **A local-12GB LoRA training run is realistic on**: Z-Image (6B — explicitly the smallest,
  fastest-training model surveyed, with Musubi Tuner support days after release), HiDream-O1-Image
  (8B, already confirmed to run inference in ~10 GB fp8, training would need somewhat more but is
  plausibly local-feasible — not directly confirmed for training specifically, flagged as a gap),
  and FLUX.2 [klein] 4B (though the one concrete training benchmark found used a 24 GB card, not
  12 GB — **unverified whether klein 4B LoRA training specifically fits 12 GB**, a real gap).

**Which base models actually have a good LoRA ecosystem today — the brief's explicit ask:**

| Model | LoRA ecosystem verdict |
|---|---|
| FLUX.2 (dev + klein) | **Strong.** Official BFL tooling + docs, kohya_ss "rock solid," ai-toolkit is BFL's own recommended path. Best-documented of the frontier-tier models. |
| SD3.5 | **Strongest of all**, but on an aging base — "the ecosystem none of the newcomers can match," per community consensus, though the base model quality itself trails the 2026 frontier. |
| Qwen-Image | **Growing, real.** OneTrainer + Musubi Tuner support confirmed; a dedicated depth ControlNet already exists (rare and directly useful). Behind FLUX in raw community-checkpoint volume. |
| Z-Image | **Surprisingly strong for its age.** Musubi Tuner support landed 2 days after release; active community LoRA sharing within months. The de-distillation workaround needed for the Turbo checkpoint is a genuine extra step, but Z-Image Base exists specifically to sidestep it. |
| Chroma1-HD | **Present but niche.** Explicitly designed as a fine-tuning substrate (unaesthetic-by-default base), documented training recipes exist, but a much smaller community than FLUX/SD. |
| HiDream-I1 / O1-Image | **Weak-to-unclear.** Quantized-checkpoint tooling (nf4/GGUF/fp8) proliferates fast, but this pass found **no confirmed dedicated ControlNet and no clearly documented LoRA-training success story** for O1-Image specifically — this is the report's clearest example of the brief's warning that "some newer architectures have weak or no LoRA ecosystem," despite HiDream-O1-Image being one of the strongest models on raw quality/VRAM-fit grounds. **This is a real tension**: best local-fit model, weakest confirmed fine-tuning story. |
| Krea 2 | **Unclear/too new.** No LoRA training reports found in this pass at all — flagged as an open question given how recently it shipped. |
| Cosmos3-Super | **Not applicable locally** — scale alone excludes fine-tuning on any hardware this project has access to. |
| Proprietary APIs (GPT Image 2, Nano Banana, Midjourney, Seedream) | **None.** No fine-tuning path exists for any proprietary API surveyed. Style consistency on these is achieved only through reference images (IP-Adapter-style conditioning, Midjourney's --sref, Nano Banana's multi-image conditioning) re-supplied every session — this is fundamentally less durable/portable than a trained LoRA file, and does not compound the way a LoRA does (a LoRA gets better/more precise the more curated data you feed it once; a reference-image workflow re-derives style-adherence from scratch, or close to it, on each generation). |

### Style-reference features (no training required)

- **FLUX Redux**: BFL's own IP-Adapter equivalent — takes an image as a style/content prompt,
  supports "Advanced" mode with separate text/image-prompt weight control. Genuinely useful for
  fast style exploration before committing to a LoRA.
- **IP-Adapter / PuLID / InstantID** (community, model-agnostic-ish): community consensus places
  reference-image-only consistency at roughly **70-85%** subject fidelity vs. **85-95%** for a
  properly trained LoRA — a meaningful, quantified (if informally sourced) gap. PuLID Flux II is
  specifically cited for multi-angle character turnarounds.
- **Midjourney --cref/--sref**: strong, purpose-built, but manual/non-automatable per the API
  gating discussed in §2.
- **Nano Banana's multi-turn conditioning**: a genuinely different mechanism (conversational,
  stateful editing) rather than a static reference adapter — strong for iterative refinement,
  unproven for the specific batch multi-view generation this pipeline needs.

**Bottom line on style uniqueness**: the durable, portable, pipeline-automatable answer is a
**trained style LoRA on an open-weight base with a real training ecosystem** — FLUX.2 [klein] 4B
or Qwen-Image are the strongest-evidenced choices for that (mature tooling + confirmed
local/cheap-cloud training path), Z-Image is a fast-moving dark horse worth testing given its
tiny footprint and surprisingly early tooling support, and HiDream-O1-Image is a quality-tempting
but fine-tuning-unproven wildcard. A curated reference set of **15-40 images** establishing the
Castilian-gothic-baroque look (concept sketches, photobashes, even real-world reference photos of
Andalusian churches/wrought iron, licensed appropriately) is the realistic starting dataset size,
achievable by a solo dev. Total cost for a first style-LoRA pass: **roughly $5-15 in cloud GPU
time** if not training locally, a few hours of wall-time, with 2-3 iterations to dial in.

---

## 4. Control and consistency tooling

- **ControlNet-depth maturity by base model**: **SDXL has by far the deepest ControlNet library**
  (5+ types including a union multi-control model) — the most mature option if raw model quality
  can be recovered via a strong style LoRA. **Qwen-Image has a dedicated, named depth ControlNet**
  already published (`Qwen-Image-Blockwise-ControlNet-Depth`) — directly relevant and the
  strongest concrete match to this pipeline's stated depth-reprojection requirement among the
  frontier-tier models. **FLUX (including FLUX.2)** has canny/depth/union ControlNets, ecosystem
  "leaner... but accelerating quickly." **HiDream**: no dedicated depth ControlNet was found in
  this pass — a real gap for a model otherwise strong on quality/VRAM-fit.
- **Multi-view-consistent generation for texture projection — this is an active 2025-2026
  research area, not a solved/shipped commodity tool.** Relevant recent papers found: **MVPainter**
  (ControlNet-based geometric conditioning specifically for multi-view texture generation, using
  normal+depth priors), **Hitem3D 2.0** (renders multi-view depth/normal control signals, then
  diffuses per-view textures, then reprojects/bakes via UV inpainting — architecturally very close
  to what this pipeline's texture stage needs to build), **MV2UV** (CVPR 2026 — treats multi-view
  generations as semantic prompts, uses pixel-aligned 3D-coordinate cross-attention positional
  encoding specifically to resolve multi-view inconsistency and fill occlusions, fine-tunes SDXL
  for UV-space output directly), and **FlexPainter** (multi-view generation with explicit geometry
  constraints for texture baking). **None of these are turnkey open-source tools with a pip-install
  and a model checkpoint ready to drop into a pipeline** — they are published research
  papers/methods, several with code releases, that would need real integration engineering. This
  is squarely a "corner possibly missed" territory the brief anticipated: **this pipeline's
  specific need (multi-view-consistent depth-guided texture generation) is closer to active
  research than to a mature commodity tool**, and the game-texture-gen commercial products (Meshy,
  Tripo, Rodin, Hunyuan3D Studio, 3D AI Studio) that already ship this exact capability as a
  product (image→3D with automatic PBR texture generation, described as reaching 4K tileable
  material-ball quality) may be a more practical near-term answer than assembling
  ControlNet-depth-plus-reprojection from research papers by hand — worth evaluating directly
  against the "build it ourselves on FLUX/Qwen" path.
- **Tileable PBR material generation**: a mature-enough commercial category exists specifically
  for this — **3D AI Studio**, **Polycam's AI material generator**, and the free/open **ArmorLab**
  (local, no cloud upload) were named as current tools producing seamless, tileable Base
  Color/Metallic/Roughness/Normal sets from text prompts in 10-60 seconds. This is worth treating
  as a separate, already-solved sub-problem rather than something to build from a base
  text-to-image model directly.
- **IP-Adapter / character consistency, general state**: PuLID/InstantID/IP-Adapter chained with a
  trained character LoRA plus pose control and face-detailing is described as "the most
  challenging and most technical route, but ideal for unlimited local generation with zero drift"
  — i.e., the highest-consistency path requires combining multiple tools, not any single one.
- **Regional prompting**: mature in ComfyUI for both grid/coordinate-based regions and
  attention-mask-based regions; Flux-specific regional-conditioning nodes exist (`Create Flux
  Regional Cond`); one compatibility gotcha found — Flash Attention and regional prompting are
  mutually exclusive in current ComfyUI, a real gotcha to know before optimizing for speed.
- **Inpainting/refinement quality**: not separately benchmarked in this pass across models — flagged
  as a gap.

---

## Ranked recommendation for this use case

Quality first, cost stated but never filtering:

1. **Build the pipeline on FLUX.2, specifically training a style LoRA on FLUX.2 [klein] 4B
   (Apache 2.0, locally-trainable-adjacent) for iteration and day-to-day generation, with FLUX.2
   [dev] under a BFL Builder license (cloud-rented for training/inference, ~80GB-class GPU) as the
   quality ceiling for hero/key assets.** Reasoning: FLUX has the single best-documented,
   most mature LoRA training path of any model in this report (official BFL tooling, kohya_ss and
   ai-toolkit both first-class), a real ControlNet-depth model, and the klein 4B tier is both
   commercially clean (Apache 2.0) and cheap to train ($0.50-15 per style LoRA). This directly
   answers the brief's uniqueness requirement — a trained style LoRA is the most portable, durable,
   pipeline-automatable answer found — while still leaving a path to FLUX.2 [dev]'s higher ceiling
   for hero assets where the Builder-tier cost is worth paying.
2. **Qwen-Image (20B, Apache 2.0) as the primary alternative/complement, specifically for the
   texture/depth-reprojection stage**, given it is the only frontier-tier open model researched
   with an already-published, purpose-built depth ControlNet — directly matching the pipeline's
   stated core requirement rather than requiring it to be assembled from research papers. Its
   cleaner license (no non-commercial tier to navigate, unlike FLUX.2 dev) is a real operational
   simplification.
3. **HiDream-O1-Image (8B, MIT) as a closely-watched wildcard, not yet a primary pick.** It has
   the single best confirmed 12 GB local-hardware fit and benchmark standing of any open model in
   this report, and the most permissive license (MIT). It is held back from a top recommendation
   only by an unconfirmed/thin fine-tuning and ControlNet story — worth a direct hands-on
   evaluation before the pipeline commits, since if its LoRA/ControlNet ecosystem catches up (it
   is only 2.5 months old), it could become the strongest all-around local choice.
4. **For hero/marketing-grade single images where automation isn't required**, Nano Banana Pro or
   GPT Image 2 via API are worth using opportunistically for their raw quality ceiling and cheap
   per-image cost — but not as the pipeline's backbone, since neither offers a fine-tuning path,
   which the brief treats as close to disqualifying given the uniqueness requirement.
5. **Midjourney for early ideation/mood-boarding only** (manual, not pipeline-integrated) — its
   aesthetic strength for fantasy concept art is real and well-regarded, but the lack of
   accessible API access makes it unsuitable as an automated pipeline stage without pursuing
   Enterprise access specifically.
6. **Krea 2 deserves a direct hands-on evaluation before the pipeline is finalized** — it is the
   only model in this report explicitly designed from scratch for aesthetic/style control (its
   stated design goal maps unusually well onto the brief's uniqueness requirement), is open-weight
   with a workable license, and is plausibly local-fit by parameter-count analogy — but it is too
   new for this research pass to confirm any of that with real evidence. Test it before ruling it
   in or out.
7. **Do not build around**: Cosmos3-Super (tops the open-weight leaderboard but requires
   H200/B200-class hardware, entirely impractical at any accessible price point for this project);
   Seedream/Reve/Luma for the pipeline backbone (no fine-tuning path, and in Seedream's case,
   unresolved EU data-residency considerations); Ideogram's downloaded weights without explicitly
   purchasing the correct commercial-license tier (an easy, sourced trap).
8. **For tileable PBR materials specifically**, use a dedicated commercial tool (3D AI Studio,
   Polycam, or the local/free ArmorLab) rather than prompting a general text-to-image model for
   this — it is a solved, purpose-built product category separate from the concept-art/texture
   question above.

---

## Could not determine

- **No controlled, rigorous, model-specific Q4-vs-full-precision quality comparison exists for
  FLUX.2, Qwen-Image, or HiDream-O1-Image at painterly/stylized (non-photoreal) content.** This
  was the brief's explicitly named key unknown; the evidence found is general community consensus
  about GGUF quantization tiers (Q8 safe, Q4 visible-but-usable, Q2-3 risky) plus one strong
  concrete data point (HiDream-O1-Image fp8 confirmed tested on 12GB-class cards), but nothing
  rigorous ties a specific quant level to a specific quality delta on our actual candidate models
  and our actual content style.
- **FLUX.2 [klein] 4B LoRA training's exact VRAM floor on a 12 GB card specifically.** The one
  concrete benchmark found (BFL's own blog) used a 24 GB RTX 4090; whether 12 GB works with
  reduced batch size/resolution/gradient-checkpointing was not confirmed either way.
- **BFL's actual Builder-tier price.** Confirmed to exist, confirmed to be the right tier for a
  solo dev under 10K images/month, but the number itself sits behind a login wall
  (`dashboard.bfl.ai/licensing`) that neither this pass nor R1 could get past.
- **Krea 2's VRAM-at-quantization figures and its LoRA/ControlNet ecosystem maturity** — the
  model is too new (mid-2026) for either to have been documented in searchable sources yet.
- **Whether any shipped commercial game at anything close to Diablo 4/PoE2 art-direction quality
  has used any of these specific models in production.** Two disclosed, verifiable AI-art case
  studies were found (Lost Lore/Bearverse using Midjourney for concept exploration; Little Buffalo
  Studios using Kaedim for image-to-3D) but both are indie/small-scale, not AAA-tier. All
  "comparable shipped-game quality" judgments in this report above that point are my own
  qualitative visual assessment against known non-AI art bars, explicitly labeled as such, not
  sourced claims of pipeline usage.
- **Seedream/ByteDance data-residency and long-term platform-stability implications for an
  EU-based commercial project** — not evaluated.
- **Ovis-Image and LongCat-Image's exact license terms and ecosystem maturity** — both surfaced
  only in aggregator/listicle coverage in this pass, too thinly sourced to include as a real
  recommendation candidate.
- **A rigorous, apples-to-apples comparison of inpainting/refinement quality across the models in
  this report** — not separately researched.

## Corners possibly missed

- **This pipeline's actual core technical need — depth-guided, multi-view-consistent texture
  generation for UV reprojection — is closer to an active 2025-2026 research problem than a
  mature commodity tool.** MVPainter, Hitem3D 2.0, MV2UV, and FlexPainter (all found in this pass)
  are recent papers, several with released code, that solve pieces of exactly this problem, but
  none is a turnkey pip-installable tool. **The commercial image-to-3D products (Meshy, Tripo,
  Rodin, Hunyuan3D Studio, 3D AI Studio) already ship this capability as a finished product** and
  deserve direct evaluation against the DIY ControlNet-depth-plus-reprojection path — this whole
  category (texturing-as-a-service on top of your own geometry) was outside this report's
  per-image-model schema but may be a more practical near-term answer than the base
  text-to-image-model comparison this report focused on.
- **Film/VFX-adjacent techniques not covered**: production VFX pipelines have long used
  projection-painting and multi-camera-consistent texture workflows (Mari, Substance 3D Painter's
  own AI features, NVIDIA's own texture-synthesis research) that this pass did not investigate —
  these fields solved "paint once, project consistently across views" for photoreal film assets
  years before game-dev AI pipelines existed, and specifically Substance 3D Painter's newer
  AI-assisted texturing features were not researched here despite being a very plausible adjacent
  answer.
- **Adobe Firefly** was not evaluated in this report despite being explicitly named in one source
  as the only major AI image platform offering real IP indemnification to paid subscribers — given
  the brief's emphasis on shipped-commercial-game IP risk, this is a real gap; Firefly's raw
  aesthetic quality for dark-fantasy concept art is a separate open question.
- **Grok Imagine** (xAI) appears on the leaderboard (`grok-imagine-image-quality`, rank 12,
  1201 Elo) but was not researched for license/cost/ecosystem in this pass — a real gap given its
  competitive ranking.
- **Meta's Muse Image**, Meta Superintelligence Labs' first image model, launched **2026-07-07 —
  thirteen days before this report** — genuinely too new to assess: no benchmark standing, no
  confirmed developer/API access terms (rollout is "coming weeks" per Meta's own announcement at
  time of research), proprietary, Meta-ecosystem-integrated. Flagged rather than scored, exactly
  the "too new to be indexed" case the brief anticipated.
- **The EU AI Act's Article 50 disclosure obligation** (entering into force 2026-08-02, per one
  legal-analysis source touched on in this pass) and **Steam's AI-content disclosure requirement**
  (referenced in passing by one game-dev-focused source) are both compliance considerations for a
  Spain/EU-based commercial game shipping AI-generated assets that sit adjacent to, but outside,
  this report's model-quality scope — worth a dedicated compliance check before shipping, not
  covered here.
- **LoKr and other parameter-efficient fine-tuning variants beyond standard LoRA** (mentioned in
  passing re: ai-toolkit) were not investigated in depth — may offer a better
  parameter-efficiency/quality tradeoff than standard LoRA for the style-lock use case and
  deserves a closer look during actual implementation.
- **No pricing/quality check was done on running any of these models through the NVIDIA
  build.nvidia.com NIM catalog** for image generation specifically (R1 flagged the catalog
  includes FLUX.1-dev, FLUX.2-klein, and Qwen-Image as hosted endpoints) — R1 already established
  the trial-ToS production restriction, but a paid subscription tier's pricing for this specific
  use was not chased down in either pass.

---

## Verification pass (orchestrator, 2026-07-20)

Licenses re-checked against primary sources, since these become CREDITS ledger rows and
HF tags have misreported before (`sdxl_360`: MIT claimed in README, empty API field).

| Model | Claimed | **Verified** | Source |
|---|---|---|---|
| FLUX.2 [klein] 4B | Apache 2.0 | **CONFIRMED Apache 2.0**, released 2026-01-15, 4B distilled from a 9B flow model + 8B Qwen3 text embedder, 4 inference steps | HF repo + BFL blog |
| Qwen-Image | Apache 2.0 | **CONFIRMED `apache-2.0`**, 20.4B params (20,430,401,088 BF16), **ungated** | HF API `cardData` |
| HiDream-I1-Full | MIT | **CONFIRMED `mit`**, 17.1B params, **ungated** | HF API `cardData` |

FLUX.2-klein's HF API returns **401 — the repo is gated**. Not blocked, but terms must be
accepted before download. Apache 2.0 governs the weights once obtained.

Minor discrepancy: the report cites "HiDream-O1-Image 8B"; the repo verified here is
`HiDream-I1-Full` at 17.1B. Both MIT. The 8B variant was not independently confirmed —
resolve before relying on the smaller size.

**Three genuinely permissive, current, high-quality backbones exist** — this is a materially
better position than the 2026-07-18 ledger pass found, and it was reachable only by asking
"what is best?" instead of "is this one cleared?"

## Gap-check pass (orchestrator)

**The 12 GB ceiling is now the binding constraint, and it binds on all three finalists.**

| Model | Native size | Fits 12 GB unquantized? |
|---|---|---|
| FLUX.2 [klein] 4B | ~13 GB VRAM (BFL's own figure, RTX 3090/4070 class) | **No — just over** |
| Qwen-Image | 20.4B | No |
| HiDream-I1-Full | 17.1B | No |

Every top candidate requires quantization on this card, and the Q4 *quality* delta on
painterly dark-fantasy content is precisely what no source measures. The pipeline's whole
quality thesis would rest on an unmeasured degradation.

**Missed corner — nobody costed a GPU upgrade.** Both R1 and R2 treated 12 GB as immovable
and reasoned about renting around it. Given the user's ruling that cost is acceptable where
quality justifies it, this deserves pricing: a **24 GB RTX 3090** (used, ~€600–700) or a
**32 GB RTX 5090** removes the constraint *permanently*, runs all three finalists
unquantized at full quality, eliminates recurring cloud spend, and keeps generation local,
private and unmetered. For a project generating hundreds of assets over months, the
one-time cost plausibly beats sustained rental — and it deletes the quantization-quality
unknown entirely rather than managing it. **Recommend costing this before committing to a
cloud-dependent architecture.**

Carried to R3/R5: the report's finding that multi-view-consistent depth-guided texturing is
still research-grade (MVPainter, Hitem3D 2.0, FlexPainter) while commercial image→3D
products (Meshy, Tripo, Rodin) already ship it as a product.
