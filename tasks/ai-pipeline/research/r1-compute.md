# R1 — Compute options for the AI asset pipeline

Research date: 2026-07-20. Every number below is cited to a live source fetched/searched on this date. Where a primary source could not be extracted (JS-rendered pages that blocked content extraction), that is stated explicitly and the figure is marked as secondary-sourced or unverified.

Context: solo dev, Spain/EU. Local GPU RTX 3080 Ti, 12 GB VRAM, 32 GB system RAM (Ampere architecture — relevant below, no native FP8 tensor cores). Project shape: unattended, scripted, batch image/3D generation — not interactive demos.

---

## 1. NVIDIA Developer Program — and why it is mostly NOT compute

**What free membership concretely grants**, per the program page itself ([developer.nvidia.com/developer-program](https://developer.nvidia.com/developer-program)):
- **(a) SDK/toolkit access**: CUDA Toolkit, Nsight tools, NGC catalog access, source from NVIDIA's GitHub. This is tooling, not compute.
- **(b) DLI training credit**: one complimentary self-paced Deep Learning Institute course "worth up to $90" (some promo codes are $30-value). This is a training-course voucher, not compute — confirmed nowhere does it convert to GPU time. [developer.nvidia.com/join-nvidia-developer-program](https://developer.nvidia.com/join-nvidia-developer-program), [nvidia.com/en-gb/events/supercomputing/free-dli-codes](https://www.nvidia.com/en-gb/events/supercomputing/free-dli-codes/)
- **(c) Actual hosted inference credits (build.nvidia.com / NIM API catalog)**: this is the one part that is real compute, and it does exist, but it is narrower than it sounds:
  - Signing up for a build.nvidia.com API key grants **1,000 inference credits**, extendable via an in-portal "Request More" button to **5,000 total**, capped at **40 requests/minute per model** — confirmed by NVIDIA's own developer forum threads, which is the closest thing to a primary source since NVIDIA doesn't publish this in a single spec page: [forums.developer.nvidia.com/t/credit-rate-limit-increase-request-1-000-5-000-credits-40-200-rpm/376601](https://forums.developer.nvidia.com/t/credit-rate-limit-increase-request-1-000-5-000-credits-40-200-rpm/376601), [forums.developer.nvidia.com/t/api-credits-for-build-nvidia-com/306633](https://forums.developer.nvidia.com/t/api-credits-for-build-nvidia-com/306633)
  - The catalog **does include relevant image/3D models as hosted API endpoints**, not just self-host containers: FLUX.1-dev, FLUX.2-klein, Qwen-Image, and others appear on [build.nvidia.com/models](https://build.nvidia.com/models) with playground + API access. Example: [build.nvidia.com/black-forest-labs/flux_1-dev/modelcard](https://build.nvidia.com/black-forest-labs/flux_1-dev/modelcard), [build.nvidia.com/qwen/qwen-image](https://build.nvidia.com/qwen/qwen-image).
  - **Critical catch — the trial ToS forbids production use.** The governing document, [NVIDIA API Trial Terms of Service](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf), states you may only use the trial API "for internal testing and evaluation purposes, not in production," and defines production use as "any use... other than development, testing, research or evaluation... including activity serving real end-users." **This means the free build.nvidia.com credits are explicitly licensed for trying a model, not for generating shippable game assets.** A paid subscription would be required to lift that restriction, and no self-serve subscription price is published (enterprise sales contact).
  - What is separately confirmed **not** compute: the **self-hosted NIM containers** for visual generative AI (FLUX, Qwen-Image, Hunyuan3D) are Docker/Podman images you download and run on **your own GPU** — the official docs explicitly walk through obtaining an NGC key and running the container locally, with no managed/cloud-run option mentioned: [docs.nvidia.com/nim/visual-genai/latest/getting-started.html](https://docs.nvidia.com/nim/visual-genai/latest/getting-started.html). This is packaging/tooling, not additional compute — it still needs your 3080 Ti (or bigger) underneath.
- **(d) NVIDIA Inception** (separate program, startup-focused): see below.

**Verdict: mostly not compute, exactly as suspected.** The one real compute grant (1,000-5,000 API credits) is capped, rate-limited, per-model-cost-variable (no published credit-cost table for image-gen calls — could not confirm), and contractually restricted to evaluation, not production asset generation. **Trial only.**

### 1d. NVIDIA Inception (separate from Developer Program)

Per [nvidia.com/en-us/startups](https://www.nvidia.com/en-us/startups/) and secondary summaries of its FAQ ([klymentiev.com/blog/nvidia-inception-program](https://klymentiev.com/blog/nvidia-inception-program), [thundercompute.com/blog/nvidia-inception-program-guide](https://www.thundercompute.com/blog/nvidia-inception-program-guide)):

- **Eligibility**: must be "officially incorporated," employ at least one developer, maintain a working website, and be less than 10 years old. No revenue requirement, no funding-stage requirement, no application fee.
- **Solo-dev fit**: Inception explicitly says "whether you're a solo researcher or a Series A startup" it will accept you — but the incorporation requirement is the actual gate. **UNVERIFIED**: whether a Spanish *autónomo* (self-employed registration, not a formal company like an SL) satisfies "officially incorporated" — none of the sources address this directly; it would need a direct application or forum question to NVIDIA to resolve. If it requires a formal corporate entity (SL equivalent of an LLC), that's an added cost/step before applying.
- **Credits granted if accepted**: up to **$100,000 in DGX Cloud credits** for dedicated H100 capacity, plus up to **$100,000 in AWS credits** (separate pool), preferred GPU pricing, and free technical training — per the same secondary sources; NVIDIA's own page does not publish exact dollar figures, only "access free cloud credits from NVIDIA and partners."
- **Verdict**: if you can clear the incorporation bar, this is genuinely large real compute — **sustainable production use**, potentially overkill. If incorporation is a blocker, this whole path is closed. This needs a direct eligibility check before counting on it.

---

## 2. Kaggle Notebooks

Kaggle's own docs page and forum posts (content behind JS rendering that repeatedly failed clean extraction — figures below are corroborated across multiple independent secondary sources, not a single clean primary fetch):

- **GPU types**: one **NVIDIA P100 (16 GB)**, or two **T4 (16 GB each, 32 GB combined)** — [kaggle.com/docs/efficient-gpu-usage](https://www.kaggle.com/docs/efficient-gpu-usage)
- **Weekly quota**: historically ~30 GPU-hours/week, but Kaggle switched to an unpublished **"floating" quota** system in a 2024+ product update ([kaggle.com/product-feedback/173129](https://www.kaggle.com/product-feedback/173129)) — the exact number is not published and fluctuates with platform demand. Community estimates cluster around 15–30 hours/week. **Treat as approximate.**
- **Per-session limit**: up to 12 hours of continuous execution (9–12h cited across sources).
- **Persistent storage/model caching**: `/kaggle/working` persists only within a session; cross-session caching requires saving to a Kaggle Dataset and re-attaching it — there is no free-form persistent disk like a normal VM.
- **Commercial use / ToS**: **UNVERIFIED — could not confirm.** WebFetch repeatedly returned only page titles for both [kaggle.com/aup](https://www.kaggle.com/aup) and [kaggle.com/terms](https://www.kaggle.com/terms) (JS-rendered content not visible to the fetch tool). Secondary search snippets suggest competition **data** carries non-commercial restrictions, but nothing conclusive was found about the notebook **compute environment itself** being restricted from producing commercial outputs. This needs a direct read of the ToS page in a browser before relying on Kaggle for shippable assets.

**Verdict: occasional burst / prototyping only.** Free, decent VRAM (P100 16GB > local 12GB), but session limits, unpredictable weekly quota, no durable storage, and an unconfirmed commercial-use posture make it unsuitable as a dependable pipeline stage. Fine for testing a script before committing to paid compute.

---

## 3. Google Colab

Primary pricing pages ([cloud.google.com/colab/pricing](https://cloud.google.com/colab/pricing), [colab.research.google.com/signup](https://colab.research.google.com/signup)) returned truncated/no content to the fetch tool; figures below are from secondary aggregators corroborating each other, **not independently confirmed against the primary page text**:

- **Free tier**: GPU type varies by availability (typically T4-class), sessions capped at up to 12 hours, subject to dynamic throttling based on usage patterns — confirmed directly from Colab's own FAQ: "notebooks can run for at most 12 hours, depending on availability and your usage patterns," and GPU/TPU types "vary over time... necessary for Colab to provide access... free of charge" ([research.google.com/colaboratory/faq.html](https://research.google.com/colaboratory/faq.html), primary, successfully fetched).
- **Colab Pro**: ~$9.99/month (one EU-region aggregator quoted $11.99, likely VAT-inclusive pricing — **unverified which is correct for a Spain billing address**).
- **Colab Pro+**: ~$49.99/month, adds background execution and priority access to premium GPUs (A100-class), up to 24h continuous execution if compute units allow.
- **Compute-unit model**: pay-as-you-go is $9.99 per 100 compute units; a T4 burns ~1.76 CU/hr (≈57 hrs per 100 CU ≈ $0.18/GPU-hr equivalent); an A100 burns ~15 CU/hr (≈7 hrs per 100 CU ≈ $1.43/GPU-hr equivalent).

**Verdict: occasional burst.** Pro/Pro+ compute-unit pricing is actually competitive per GPU-hour vs. raw rental once you're paying, but access is throttled by "availability and usage patterns" language that Google deliberately keeps vague — there's no SLA. Not something to build an unattended pipeline around without a fallback.

---

## 4. Hugging Face Spaces / ZeroGPU

Primary source, cleanly fetched: [huggingface.co/docs/hub/en/spaces-zerogpu](https://huggingface.co/docs/hub/en/spaces-zerogpu), [huggingface.co/pricing](https://huggingface.co/pricing).

- **Hardware**: ZeroGPU dynamically allocates slices of an **NVIDIA RTX Pro 6000 Blackwell**. `large` (default) = half card = **48 GB VRAM**, `xlarge` = full card = **96 GB VRAM** (2× quota cost).
- **Free tier daily quota**: unauthenticated 2 min/day, free account **5 min/day**, resets 24h after first use.
- **PRO tier ($9/month, confirmed on pricing page)**: **40 min/day** GPU quota (extensible), highest queue priority, up to 10 ZeroGPU Spaces, overage billed at **$1 per 10 minutes** once quota is exhausted.
- **Hard technical constraints that matter for a batch pipeline**: ZeroGPU is **Gradio-SDK-only** — it is not a general compute backend, it's a decorator (`@spaces.GPU`) inside a Gradio app that grabs a GPU slice for the duration of one function call (default 60s max, extendable via `duration=`). PyTorch 2.8+ required; `torch.compile` unsupported (AOT compilation is the workaround). Models must be moved to `cuda` at module load time under an emulation layer, then real CUDA only exists inside the decorated function.

**Verdict: trial only for our purposes.** This is architecturally a demo-hosting product — a scripted, unattended batch job is exactly what it is *not* designed for (daily-reset minute quotas, per-call duration caps, Gradio-only). The 48–96 GB VRAM is tempting on paper but functionally inaccessible for headless batch scripting. Even PRO's 40 min/day would only cover a handful of generations if each takes more than a few seconds.

---

## 5. Credit-based serverless GPU (Modal, Lightning AI, Baseten, Replicate, fal.ai)

These are the most promising category for **scripted, unattended batch generation** since they expose a plain API/SDK you call from your own pipeline code, no notebook or Gradio UI involved.

| Provider | Free credit | A100 80GB | H100 | L40S/L4 class | Notes |
|---|---|---|---|---|---|
| **Modal** ([modal.com/pricing](https://modal.com/pricing), primary) | $30/mo on Starter plan, ongoing (not one-time) | $0.000694/sec ≈ **$2.50/hr** | $0.001097/sec ≈ **$3.95/hr** | L40S $0.000542/sec ≈ **$1.95/hr** | Per-second billing, no idle charge, no platform fee, Python-native SDK — good scripting fit |
| **Replicate** ([replicate.com/pricing](https://replicate.com/pricing), primary) | No published signup credit found; $10 one-time referral bonus (12mo expiry) | $0.0014/sec ≈ **$5.04/hr** | $0.001525/sec ≈ **$5.49/hr** | T4 $0.000225/sec ≈ **$0.81/hr** | Also has flat **per-model** pricing: FLUX 1.1 Pro $0.04/image, FLUX Dev $0.025/image, FLUX Schnell **$0.003/image** (cheapest found across all providers) |
| **fal.ai** ([fal.ai/pricing](https://fal.ai/pricing), primary) | No free tier confirmed; modest starter credits only | not itemized on pricing page | not itemized | not itemized | Purely per-model flat pricing: Qwen-Image $0.02/megapixel, Seedream V4 $0.03/image, FLUX Schnell **$0.025/image** — note this is **8× more expensive than the same FLUX Schnell model on Replicate** ($0.003 vs $0.025), so price-shop per model, don't assume providers are interchangeable |
| **Baseten** (secondary: [costbench.com](https://costbench.com/software/ai-gpu-cloud/baseten/), primary pricing page: [baseten.co/pricing](https://www.baseten.co/pricing/)) | $30 free credits on signup | not directly itemized | B200 $9.98/hr (top of range) | T4 from **$0.63/hr** | Startup program (separate application) offers up to $25k for dedicated deployments |
| **Lightning AI** (secondary: [saasworthy.com](https://www.saasworthy.com/product/lightning-ai/pricing), [gputracker.dev](https://gputracker.dev/provider/lightningai)) | Free plan: 15 monthly credits + 1 Studio (4h auto-restart) | not found in 24GB-class searches | not found | T4 $0.68/hr, L4 $0.70/hr, A10G $1.80/hr | Pro is $50/mo (annual) or $600/mo (monthly) — oriented around persistent "Studios" (dev environments), less naturally scriptable-batch than Modal/Replicate |

**Verdict, ranked for THIS project's scripted-batch shape:**
1. **Modal — sustainable production use.** Cheapest per-hour A100/H100/L40S of this group, ongoing $30/mo free credit effectively subsidizes light usage indefinitely, and it's built for exactly this (Python functions you deploy and call, per-second billing, no idle cost).
2. **Replicate — sustainable production use for known models.** If the pipeline uses FLUX or another model already packaged on Replicate, the flat per-image pricing (as low as $0.003/image for Schnell) is the cheapest path to a given image with zero infra management. Worse deal if you need a custom/uncommon model (falls back to raw per-second GPU pricing, which is pricier than Modal).
3. **fal.ai — occasional burst**, same category as Replicate but consistently pricier per test above; worth checking per-model if a specific model is cheaper there.
4. **Baseten — occasional burst.** Reasonable T4 pricing, small free credit, viable but not distinctly better than Modal for our shape.
5. **Lightning AI — not a great fit.** Studio/IDE-oriented product; usable but fighting the grain for headless batch scripting.

---

## 6. Raw GPU rental (RunPod, Vast.ai, Lambda)

### RunPod — primary, [runpod.io/pricing](https://www.runpod.io/pricing), cleanly fetched

| GPU | Community Cloud | Secure Cloud |
|---|---|---|
| RTX 4090 (24GB) | $0.34/hr | $0.69/hr |
| L40S (48GB) | $0.79/hr | $0.99/hr |
| A100 PCIe 80GB | $1.19/hr | $1.39/hr |
| A100 SXM 80GB | $1.39/hr | $1.49/hr |
| H100 PCIe 80GB | $1.99/hr | $2.89/hr |
| H100 SXM 80GB | $2.69/hr | $2.99/hr |

Billed per second. No true spot/interruptible tier — "Community Cloud" is the budget option (lower reliability guarantee, not officially preemptible). No signup credit found.

### Vast.ai — marketplace, primary page had no live numbers extractable; figures from secondary aggregators cross-checked against each other ([vast.ai/pricing/gpu/RTX-4090](https://vast.ai/pricing/gpu/RTX-4090), [thundercompute.com/blog/vast-ai-vs-thunder-compute](https://www.thundercompute.com/blog/vast-ai-vs-thunder-compute), [synpixcloud.com](https://www.synpixcloud.com/blog/vast-ai-vs-runpod-rtx-4090-pricing))

- RTX 4090 (24GB): roughly **$0.29–0.59/hr** depending on host and on-demand vs. interruptible
- A100 80GB: from **~$1.09/hr**
- H100 80GB: from **~$1.89/hr**, sweet-spot verified-host range **$1.50–1.87/hr**
- **Interruptible instances are 30–50%+ cheaper** than on-demand from the same host, billed per second. Being a peer marketplace, prices are inherently more volatile/host-dependent than RunPod's fixed catalog.

### Lambda — primary, [lambda.ai/pricing](https://lambda.ai/pricing), cleanly fetched

- H100 SXM: $4.29/GPU/hr (1×) down to $3.99/GPU/hr (8×)
- A100 SXM 80GB: $3.99/GPU/hr (only an 8× cluster rate was shown; no confirmed cheap single-GPU A100 tier)
- 24–48GB class (single GPU): Quadro RTX 6000 (24GB) $0.69/hr, A10 (24GB) $1.29/hr, A6000 (48GB) $1.09/hr
- **No spot/preemptible pricing at all** — on-demand only. No free trial credit found on the pricing page.

**Verdict**: Lambda is priced and structured for multi-GPU training clusters, not single-card inference bursts — its H100/A100 rates are the most expensive of the three for a lone GPU-hour. **RunPod and Vast.ai are both practical** for this project: RunPod for predictable fixed pricing and a clean API/CLI to script against; Vast.ai for the cheapest possible $/hr if you're willing to tolerate marketplace variability and preemption on interruptible instances. Both: **sustainable production use** for burst/batch jobs, scripted via their APIs.

---

## 7. The local-vs-cloud tradeoff on 12 GB (RTX 3080 Ti, Ampere)

Techniques that extend what fits in 12 GB, and their real costs:

- **FP8 quantization**: halves storage vs. fp16/bf16. **Important Ampere-specific catch, confirmed via NVIDIA's own developer forums and independent GPU-architecture references**: FP8 tensor-core acceleration was introduced in **Ada Lovelace (RTX 40-series) and Hopper**; **Ampere (RTX 30-series, including the 3080 Ti) has no native FP8 tensor cores** ([forums.developer.nvidia.com/t/4090-doesnt-have-fp8-compute/232256](https://forums.developer.nvidia.com/t/4090-doesnt-have-fp8-compute/232256), [bestgpusforai.com/faq](https://www.bestgpusforai.com/faq)). On a 3080 Ti, FP8 weights still save VRAM (smaller storage footprint) but get **no speed benefit** — compute has to upcast to fp16/bf16 under the hood. Community projects like ["Backporting FP8 to the RTX 3090"](https://amohan.dev/blog/2026/fp8-as-storage-imma-ampere/) exist specifically because this isn't native. Treat FP8 on this card as a VRAM optimization only, not a speed one.
- **INT4 / GGUF quantization** (e.g., Q4_K_M via the ComfyUI-GGUF node by city96): ~4× smaller than fp16, works on any CUDA GPU including Ampere, larger quality loss than FP8 (more visible artifacting, especially at Q2–Q3). This is the technique that actually makes big models fit: Qwen-Image (20B) at Q4_K_M quantization needs roughly **12–13 GB** for the diffusion transformer component alone at native 1328×1328 resolution.
- **Sequential CPU offload**: keeps only the currently-executing layer/block on GPU, streaming the rest from system RAM (32 GB available here comfortably covers most current models). Enables extreme VRAM floors — DiffSynth-Studio's layer-by-layer offload for Qwen-Image claims inference within **~4 GB VRAM** — but at a severe speed cost, since GPU↔CPU transfer becomes the bottleneck every step.
- **Block swap** (used for video/large diffusion transformers, e.g. kijai's ComfyUI-WanVideoWrapper): swaps whole transformer blocks between CPU and GPU per denoising step rather than per-layer; a documented example swapping 20 blocks of a 14B model saves roughly **12 GB** of VRAM ([deepwiki.com/kijai/ComfyUI-WanVideoWrapper](https://deepwiki.com/kijai/ComfyUI-WanVideoWrapper/6.2-runtime-memory-management)). Same speed tradeoff as sequential offload, somewhat less severe since whole blocks move at once.
- **Tiled VAE**: decodes the final image in overlapping tiles instead of all at once, enabling e.g. 4K output on 8 GB cards. Costs some wall-time and introduces **tile-seam/tone-variation artifacts** at tile boundaries that need overlap/denoise tuning to hide.

**Can a ~20B-parameter image model run in 12 GB, concretely?** Yes, with caveats. Using Qwen-Image (20B) as the concrete example: GGUF Q4_K_M gets the diffusion transformer to ~12–13 GB by itself; the text encoder (Qwen2.5-VL) is reported at **~17 GB in bf16** and the VAE at **~0.3 GB** ([lilting.ch VAE-memory article](https://lilting.ch/en/articles/vae-memory-optimization-qwen-hunyuan), [garystafford.medium.com quantization article](https://garystafford.medium.com/runtime-quantization-options-for-qwen-image-edit-2511-on-eks-47150e3ece6d)) — meaning the **full pipeline does not fit in 12 GB simultaneously** even with the DiT quantized; the text encoder must also be quantized or run-then-offloaded to system RAM before the DiT stage runs. This is exactly what community ComfyUI-GGUF workflows do in practice, and it is reported to work on 12 GB cards (RTX 3080/4070 class) at native resolution.

**Speed cost, best evidence found** (community-reported, not lab-controlled — flagged as loosely sourced):
- FLUX.1-dev (12B, comparable class) at full fp16 on a 24GB card (RTX 3090): **10–18 sec/image** at 20 steps, no offload needed.
- FLUX.1-dev with GGUF Q4 on an 8GB card plus `--lowvram` offloading: **over 60 sec/image**.
- FLUX.1-dev with sequential CPU offload on a 12GB RTX 3060 (weaker than the 3080 Ti): **38–41 sec/image** after the first (slower) run.
- Qwen-Image community guides cite a rough **30–60 sec/image** range on 12 GB-class cards with GGUF quantization; no controlled RTX 3080 Ti benchmark was found — **treat as approximate**.

**Bottom line for the local-vs-cloud tradeoff**: yes, it runs, but expect roughly **10–20× slower per image** than an unquantized run on a 24GB+ card, plus a real (if hard-to-quantify) quality hit from Q4-class quantization on the transformer. For a handful of hero assets this is tolerable; for a large batch run it is not — that's exactly the case where renting an A100/L40S/H100 by the hour (Section 5/6) becomes cheaper in wall-clock time even before counting your own electricity.

---

## Ranked recommendation for this project's shape (mostly-batch, unattended, scripted)

1. **Modal** for anything needing arbitrary/custom models or full pipeline control (ComfyUI workflows, custom 3D-gen scripts) — cheapest per-GPU-hour of the serverless tier, ongoing free credit, built for scripted deployment.
2. **Replicate**, model-by-model, whenever the specific model you need is already hosted there — check its flat per-image price against Modal's raw GPU-hour cost for your expected throughput; for FLUX Schnell-class cheap generation, Replicate's flat pricing wins outright.
3. **RunPod (Secure Cloud)** as the fallback for anything that doesn't fit Modal's execution model (e.g., needs a long-lived stateful container, ComfyUI server, or a non-serverless workflow) — predictable published pricing, easy scripting via API/CLI.
4. **Vast.ai interruptible** only if you can make your batch jobs checkpoint/resume-tolerant — cheapest raw $/hr but with preemption risk.
5. **Local 3080 Ti with GGUF Q4 quantization** for iteration/testing and for models that genuinely fit — free, but 10-20x slower per image than a rented 24GB+ card, so reserve it for prototyping the pipeline logic, not for the production batch run itself.
6. **NVIDIA Developer Program build.nvidia.com credits** — useful only to *evaluate* a model's output quality before committing (its own ToS forbids production use); do not build any pipeline stage that depends on it staying available or being license-clean for shipped assets.
7. **Kaggle / Colab free tiers** — fine for one-off experiments or teaching yourself a new model's behavior; too quota-constrained and ToS-ambiguous to be a dependable pipeline stage.
8. **HF Spaces ZeroGPU** — skip for this project; it solves a different problem (hosting a public interactive demo), not scripted batch generation.
9. **NVIDIA Inception** — worth a direct eligibility inquiry given the scale of credits ($100k DGX Cloud) if incorporation isn't a blocker, but don't plan around it until eligibility is confirmed.

---

## What this research could not determine

- **Kaggle's exact ToS/AUP clause on commercial content generation.** Both `kaggle.com/aup` and `kaggle.com/terms` are JS-rendered and repeatedly returned only page titles to the fetch tool, not policy text. Needs a manual browser read before trusting Kaggle for anything beyond throwaway experiments.
- **Whether a Spanish autónomo registration satisfies NVIDIA Inception's "officially incorporated" requirement**, or whether a formal company (SL) is needed. No source addressed this directly.
- **Exact credit cost per image-generation call on build.nvidia.com** (i.e., how many of the 1,000-5,000 free credits one FLUX or Qwen-Image call consumes) — no published per-model credit table was found, only the aggregate pool size and RPM cap.
- **Controlled, apples-to-apples benchmark numbers for our actual target models (Hunyuan3D 2.1, TRELLIS, Qwen-Image) on an RTX 3080 Ti specifically.** Available community benchmarks cluster around RTX 3060/3090/4070, not the 3080 Ti; the 30-60s/image figures for quantized 20B-class models are best-effort estimates from adjacent hardware, not measurements on this card.
- **Exact regional/VAT-inclusive pricing for Colab Pro/Pro+ from a Spain billing address** — the $9.99/$49.99 figures are US-quoted; one EU aggregator suggested a higher VAT-inclusive number ($11.99) without a clean primary-source confirmation either way.
- **Whether build.nvidia.com / NVIDIA API catalog access has any EU-specific availability restriction.** Nothing found suggesting it's geo-blocked, but this wasn't explicitly confirmed either.

## Corners that may have been missed

- **Model output licensing is a completely separate gate from compute cost, and this research did not cover it.** FLUX.1 [dev] specifically carries a non-commercial license from Black Forest Labs (only FLUX.1 [schnell] and the paid FLUX Pro API grant commercial rights, per general knowledge of BFL's licensing — **not independently re-verified in this research pass**). Before committing to any specific model in the pipeline, its output-usage license needs its own check, independent of where/how cheaply you can run it.
- **Adjacent free/cheap compute programs not investigated**: AWS Activate, Google Cloud's startup/free-trial credit ($300-class), Azure for Startups, plus alternative GPU marketplaces like Salad.com, TensorDock, Genesis Cloud, CoreWeave, and Paperspace — any of these could beat the providers covered here on price or terms and weren't checked.
- **Scaleway showed up as an NVIDIA Inception partner in search results** ([scaleway.com/en/nvidia-inception](https://www.scaleway.com/en/nvidia-inception/)) — as an EU-based (French) cloud provider, it may offer better data-residency/latency for a Spain-based dev than US clouds, and possibly GPU discounts tied to Inception membership even at smaller scale. Not investigated further.
- **Electricity cost of local generation in Spain** was out of scope for this research pass but is a real input to the local-vs-cloud comparison (Spain has had some of the more volatile electricity pricing in the EU) — not researched here.
- **GDPR/data-residency implications of routing generation requests through US-based APIs** (Modal, Replicate, fal.ai, Baseten) were not considered — likely a non-issue since game asset generation involves no personal data, but not explicitly verified.
- Several pricing pages (Colab, Kaggle AUP/Terms, Vast.ai's live table, NVIDIA's Inception credit page) render pricing/policy text client-side via JavaScript, which defeated the fetch tool repeatedly. All such figures above were triangulated from secondary aggregator sites that were themselves cross-checked against each other rather than a single primary source — this is a real risk of staleness or error that a manual browser visit would resolve.

---

## Verification pass (orchestrator, 2026-07-20)

**CONFIRMED — the NVIDIA production restriction.** The PDF resisted extraction, but the
clause was recovered verbatim through search of the same document:

> "Unless you purchase a Subscription from NVIDIA or a Service Provider, you may only use
> the API Service for internal testing and evaluation purposes, **not in production**."

and separately: "You must have a separate service subscription from NVIDIA or a third-party
service provider to use the API Service in production or after you have used your available
Credits." The finding stands as reported — build.nvidia.com free credits **cannot** legally
produce shipped game assets. Source: NVIDIA API Trial Terms of Service.

**NEW FINDING — FLUX.1 is a generation behind.** BFL's live licensing tiers enumerate
**FLUX.2 [dev]** and **FLUX.2 [klein] Base 9B** as the current open-weights models
(bfl.ai/licensing). FLUX.1 [dev] — the model the user named — is superseded. R2 must
evaluate FLUX.2, not FLUX.1.

**BFL commercial pricing is NOT public.** Verified across three BFL pages
(`bfl.ai/licensing`, `bfl.ai/pricing/licensing`, the self-serve help article): tiers and
limits are published, **prices are not**. Confirmed tier shape:

| Tier | Volume | Scope | Self-serve? |
|---|---|---|---|
| **Builder** | 10K images/month | single domain, fine-tuning + LoRA rights, 10 licensed users | yes — `dashboard.bfl.ai/licensing`, account required |
| Platform | 100K images/month | FLUX.2 klein 9B + FLUX.2 dev | contact sales |
| Professional | 100K images/month | up to 3 client domains | contact sales |
| Enterprise | custom | all models, permissive commercial use | contact sales |

**Builder is the relevant tier** (a solo dev, single game, well under 10K images/month).
Its price requires a logged-in dashboard visit — **user action**, not resolvable by research.

## Gap-check pass (orchestrator)

One analytical gap in the report's own conclusion, beyond the gaps it self-flagged:

**The report under-rates the local 3080 Ti by judging it on wall-time.** It concludes a
10–20× local slowdown makes batch runs "not tolerable" — but that is only true for
*interactive* work. This pipeline is unattended, scripted, and overnight-tolerant: a batch
that takes 9 hours instead of 30 minutes costs nothing but electricity if it runs while
nobody is waiting. Wall-time is close to free here; **quality and license cleanliness are
the binding constraints, not speed.** Cloud rental earns its cost when a model *cannot fit
in 12 GB at acceptable quality* — not merely when it would run faster elsewhere. R2 should
therefore treat "fits in 12 GB at Q4+ without visible degradation" as a first-class
selection criterion rather than assuming rental papers over it.

Corollary: the Q4-quantization **quality** hit (real, per the report) matters far more to
this decision than the Q4 **speed** hit (irrelevant). No source found measures that quality
delta on our target models — flagged for R2.
