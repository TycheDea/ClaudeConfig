# A3 — Fine-tuning a proprietary house visual style (Spanish-religious dark fantasy, DIV/PoE2 register)

Research date: 2026-07-20. Every claim below is sourced from a live WebSearch/WebFetch on this
date. WebFetch in this environment routes page content through a small summarizing model before
returning it to me — I could not read raw HTML/PDF bytes directly. Where a figure is important I
cross-checked it against a second, independent source; single-sourced figures are marked
**[single-source]**. Aggregator/blog figures (not the vendor's own docs/repo) are marked
**[secondary]**. This report reads as a continuation of `r1-compute.md` and `r2-image-models.md` —
it does not re-litigate base-model selection, only whether/how those three bases can be
style-tuned.

**Bottom line up front:** the working assumption survives, with one important correction. LoRA
(specifically DoRA-flavored LoRA, or plain LoRA — not full fine-tune, not textual inversion) is
the right method, and it is production-proven technology, not a research bet. But **trainer
support across the three target bases is uneven right now**, and this is the load-bearing
finding: **kohya_ss/sd-scripts — the tool R2 assumed had "rock solid" FLUX.2 support — has no
FLUX.2, Qwen-Image, or HiDream support at all** as of its current main branch (confirmed by direct
repo fetch, checked below). The tool that actually supports all three bases today is
**ai-toolkit (ostris)**, MIT-licensed. That single fact should be treated as correcting R2's
tooling claim, not just adding to it.

The harder, non-tooling finding is about **FLUX.2 [klein] 4B specifically fitting the 3080 Ti today**:
Black Forest Labs' own training docs state the 4B model trains on 12 GB VRAM. That is the one
base of the three where the *existing* GPU, not the hoped-for 3090 upgrade, is enough to start
today. Qwen-Image and HiDream both need the 24 GB upgrade at minimum, and HiDream needs
aggressive quantization even then.

---

## 1. Method comparison

### LoRA (Low-Rank Adaptation)
- **Extended description**: freezes the base model, injects small rank-decomposed update
  matrices into attention/MLP projection layers, trains only those (typically <1% of parameters).
  The de facto standard for diffusion style/subject adaptation since 2023; every tool in §2
  supports it as the baseline mode.
- **Technology**: rank-r matrix pair (A, B) added to each targeted weight, `W' = W + BA·scale`.
- **License**: the technique itself is unencumbered (Microsoft's original LoRA paper/code is
  MIT); license exposure comes from the *trainer* and *base model*, not the LoRA method.
- **Captures style vs. subject**: yes for style, well-documented — Black Forest Labs' own klein
  LoRA guide is a style-LoRA walkthrough end to end (captioning rule: describe *content*, never
  name the style; use a nonsense trigger token). [BFL/HF blog: "Fine-tune FLUX.2 [klein] with a
  LoRA under 60 minutes"](https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora)
- **Pros**: cheap, fast, small artifact (tens–hundreds of MB), swappable/combinable, the entire
  tooling ecosystem in §2 is built around it.
- **Cons**: rank ceiling limits how much a single adapter can absorb before quality degrades;
  standard LoRA (unlike DoRA) can under-fit large stylistic departures from the base model's
  native look at low rank.
- **Maturity**: production-proven, the industry default.

### DoRA (Weight-Decomposed LoRA)
- **Extended description**: decomposes the pretrained weight into magnitude and direction, learns
  a plain LoRA update for direction and a separate learnable magnitude vector. Published Feb 2024
  (arXiv:2402.09353), so over two years mature by the time of this report.
- **Technology**: `network_type: "dora"` — natively supported in ai-toolkit (§2). Cannot be merged
  back into base weights (must stay a separate adapter at inference) — a real operational
  constraint if the pipeline expects a single merged checkpoint.
  [arXiv:2402.09353](https://arxiv.org/abs/2402.09353)
- **License**: paper/method unencumbered; same base/tool license exposure as LoRA.
- **Captures style vs. subject**: DoRA "consistently outperforms LoRA" in the original paper's
  benchmarks (LLaMA/LLaVA/VL-BART tasks — the paper is not diffusion/style-specific, this is an
  extrapolation the ML community made, not a diffusion-style-transfer-specific claim from the
  paper itself). In practice DoRA is reported to learn stronger, more faithful adaptations at the
  same rank, which is exactly the property a "wholly novel style" push needs, at a training-time
  cost (slightly slower per step, one extra buffer to store).
- **Pros**: stronger fidelity per rank than plain LoRA; drop-in in ai-toolkit.
- **Cons**: cannot merge to base; not diffusion-style-transfer benchmarked directly, only inferred
  from language/VLM results; slightly higher VRAM/step time than plain LoRA.
- **Maturity**: production-proven as a technique (2+ years old, shipped in a major trainer); its
  specific advantage for *diffusion style transfer* is inferred, not directly measured in the
  source paper — flagged as inference, not sourced fact.

### LoKr / LyCORIS (and LoHa, (IA)³, DyLoRA)
- **Extended description**: a family of alternatives to plain LoRA from the LyCORIS project
  (Kohaku-BlueLeaf), published at ICLR 2024. LoKr uses a Kronecker-product decomposition instead
  of a plain low-rank one; the project's own guidance: "if space is more a concern than quality,
  use LoRA; if your model doesn't learn well enough, try LoKr with low factors; if it 'learns too
  well' [overfits], try LoHa or LoKr with large factors." [LyCORIS
  Guidelines.md](https://github.com/KohakuBlueleaf/LyCORIS/blob/main/docs/Guidelines.md)
- **Technology**: Kronecker-product / Hadamard-product weight updates; supported in ai-toolkit
  (`network_type: "lokr"`, with `lokr_full_rank`/`lokr_factor` params) and in OneTrainer/SimpleTuner.
- **License**: **Apache 2.0**. [KohakuBlueleaf/LyCORIS
  LICENSE.md](https://github.com/KohakuBlueleaf/LyCORIS/blob/main/LICENSE.md)
- **Captures style vs. subject**: this is the tool Kohaku-BlueLeaf used for his own Kohaku-XL
  Epsilon/Delta style models — real production precedent for exactly this use case (a from-scratch
  distinct visual style trained onto an open base). [kblueleaf.net Kohaku-XL
  posts](https://kblueleaf.net/posts/kohaku-xl-epsilon/)
- **Pros**: better fit than plain LoRA when a style is a large departure from the base's native
  distribution (the vordar case exactly — "no stock model produces this"); tunable
  learn-more/learn-less knob via factor size.
- **Cons**: more hyperparameters to tune correctly than plain LoRA/DoRA; slightly less
  battle-tested outside the SD1.5/SDXL/anime-model community it grew up in.
- **Maturity**: production-proven within its community (2+ years, peer-reviewed), but has less
  documented history specifically on FLUX.2/Qwen-Image/HiDream than plain LoRA/DoRA do.

### Full fine-tune / DreamBooth (all-weights)
- **Extended description**: updates every parameter, not a small adapter. DreamBooth specifically
  is the diffusion-model full/near-full fine-tune recipe (rare prior-preservation regularization
  images + a small set of target images).
- **Technology**: standard gradient descent on the full model (or a large fraction of it).
- **License**: no special exposure beyond the base model's own license.
- **Captures style vs. subject**: yes, more completely than LoRA when you have enough data — one
  cited academic full-SDXL-finetune run used **32× A100 GPUs, fp16, batch 192, 10K curated
  images, 40K steps, ~3 hours** [secondary, research-paper training-run description found via
  search, not independently re-verified against the paper itself] — that is a different order of
  magnitude of both dataset and compute from what a from-scratch style bootstrap can supply (§4).
- **Pros**: highest achievable fidelity/consistency ceiling; produces a standalone checkpoint, no
  adapter-stacking behavior at inference.
- **Cons**: **disproportionate to a house-style LoRA problem** — needs 10-40× the data and compute
  of a LoRA run to actually outperform it; full checkpoint is multi-GB per variant vs. tens of MB;
  the "no style dataset exists yet" bootstrapping problem (§4) makes assembling a full-finetune-scale
  clean dataset (thousands of style-consistent images) the real blocker, not compute.
- **Maturity**: production-proven technique in general, but wrong-sized for this specific problem
  — nobody in the trainer ecosystem researched here recommends full fine-tune as the first move
  for a style LoRA use case; it is the fallback if LoRA/DoRA/LoKr genuinely cannot hold the style
  after real attempts.

### Textual inversion
- **Extended description**: freezes the whole model, learns only a new text-embedding token.
  Artifact size is a few KB.
- **Captures style vs. subject**: **no** for this use case. "Textual inversions can capture rough
  concepts; LoRAs can capture detailed visual information... For faces, products, or detailed
  styles, LoRA is significantly better." A dark-fantasy painterly register with specific palette,
  brushwork, and iconography is exactly the "detailed style" case textual inversion is
  documented to be too weak for.
- **Maturity**: production-proven but **ruled out for this task** — included only because the
  brief asked for the comparison. Not carried forward into the tooling/cost sections below.

### Training-free / reference-guided style transfer (2026 papers — a different category, not a fine-tune)
- **Extended description**: a distinct, newer research direction that does **not** bake style into
  model weights at all — instead it injects style from one or a few reference images at inference
  time via attention manipulation (AttenST, arXiv:2503.07307), semantic correspondence (CoCoDiff,
  arXiv:2602.14464, ICLR 2026), or a single trained style-adapter combined with training-free
  structural guidance from the content image (AnyStyle, arXiv:2607.04677, submitted July 2026).
- **Relevance to vordar**: **not a substitute** for a baked-in house style LoRA — these methods
  need a reference image per generation and are pitched at interactive/creative tools, not a
  reproducible catalog pipeline. But AnyStyle's approach (style-adapter + reference image, rather
  than fully retraining per asset) is a plausible **consistency aid layered on top of** a trained
  style LoRA: once a house-style LoRA exists, using its own best outputs as inference-time style
  references for a training-free layer could tighten cross-asset-class consistency (armor vs.
  environment vs. character) without retraining. This is my own extrapolation from the papers, not
  a claim made by any of them — flagged as a hypothesis, not sourced fact.
- **Maturity**: **bleeding-edge / research-only.** No production trainer or pipeline integration
  found for any of these three papers. Not recommended as the primary route; worth a later
  experiment once the core style LoRA exists.

**Method verdict**: LoRA or DoRA in ai-toolkit, with LoKr as the documented fallback if either
under- or over-fits the target style. Full fine-tune is the correct move only if the bootstrapped
dataset (§4) grows into the thousands of images and LoRA/DoRA/LoKr all measurably plateau below
usable quality — not a first move. Textual inversion is ruled out.

---

## 2. Tooling — which trainer supports which base, today

| Tool | License | FLUX.2 [klein] 4B | Qwen-Image 20.4B | HiDream-I1-Full 17.1B |
|---|---|---|---|---|
| **ai-toolkit** (ostris) | MIT | **Yes** | **Yes** | **Yes** |
| **kohya_ss / sd-scripts** | Apache 2.0 | **No** | **No** | **No** |
| **SimpleTuner** (bghira) | AGPL-3.0-or-later | **Yes** | **Yes** | **Yes** (untested <16 GB per its own docs) |
| **OneTrainer** (Nerogar) | AGPL-3.0 | **Yes** (dev + klein) | **Yes** | **No** — open feature request #788 since April 2025, still unresolved |
| **diffusion-pipe** (tdrussell) | GPLv3 | **Yes** | **Yes** (+ Qwen-Image-Edit) | **Yes** — best documented low-VRAM (24 GB, single-3090) recipe of any tool for HiDream |

This table is the single most important correction this report makes to the project's prior
assumptions: **the tool most people reach for by reputation (kohya_ss/sd-scripts) supports none
of the three target bases.** I fetched its GitHub README directly (not a summarizer/blog): as of
its current main branch (v0.11.1, June 2026) it lists SD1.x/2.x, SDXL, SD3/3.5, **FLUX.1**,
Lumina, HunyuanImage-2.1, and Anima. FLUX.2, Qwen-Image, and HiDream are not mentioned anywhere in
that list. [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts) — this directly
contradicts a secondary-source claim surfaced in R2 ("kohya_ss has had 'rock solid' FLUX.2 support
since late 2025," sourced there to thundercompute.com, a blog, not the repo itself). **R2's
tooling claim on this point should be treated as superseded by this direct repo check.**

### ai-toolkit (ostris) — recommended primary trainer
- **License**: MIT. [github.com/ostris/ai-toolkit](https://github.com/ostris/ai-toolkit)
- **Base support**: FLUX.1, FLUX.2-dev, FLUX.2-klein-base-4B, FLUX.2-klein-base-9B, Qwen-Image,
  Qwen-Image-2512, HiDream-I1-Full, HiDream-O1-Image, HiDream-E1-1, Z-Image, SDXL, SD1.5,
  Wan 2.1/2.2, LTX 2/2.3, Ace Step.
- **Method support**: LoRA, DoRA (`network_type: "dora"`), LoKr (`network_type: "lokr"`).
- **Official vendor endorsement**: Black Forest Labs' own klein LoRA blog post uses ai-toolkit as
  the walkthrough tool and calls it "a popular community trainer with a no-code web UI," offering
  both a RunPod template and local deployment.
- **VRAM (see §5 for full numbers)**: FLUX.2 klein 4B fits 12 GB per BFL's own docs; Qwen-Image
  needs ~24 GB with 3-bit quantization; HiDream's default ai-toolkit config
  (`train_lora_hidream_48.yaml`) targets **48 GB**, and community reports say it does not yet fit
  a single 24 GB card in ai-toolkit specifically (unlike diffusion-pipe, which does — see below).
- **Maturity**: production-proven for FLUX.1/FLUX.2/Qwen-Image; HiDream support exists but is the
  toolkit's weakest-fitting corner (48 GB target config).

### kohya_ss / sd-scripts
- **License**: Apache 2.0. [kohya-ss/sd-scripts
  LICENSE.md](https://github.com/kohya-ss/sd-scripts) (fetched directly).
- **Base support**: none of the three target bases (see table above). Historically the
  highest-trust FLUX.1/SDXL trainer; that reputation does not currently extend to this project's
  target bases.
- **Verdict**: not usable for this task today. Worth re-checking in a few months — the project is
  active — but do not plan around it now.

### SimpleTuner (bghira)
- **License**: AGPL-3.0-or-later. [pyproject.toml
  license field](https://github.com/bghira/SimpleTuner/blob/main/pyproject.toml)
- **Base support**: has dedicated quickstart docs for both FLUX2 and Qwen-Image
  ([FLUX2.md](https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/FLUX2.md),
  [QWEN_IMAGE.md](https://github.com/apppidev/SimpleTuner/blob/main/documentation/quickstart/QWEN_IMAGE.md)),
  and lists HiDream as a supported model family with MoE gate-loss handling — but its own docs say
  "HiDream has not been tested on 16G cards... even 24G is pushing limits," an honest maturity
  admission from the maintainer, not a hedge I'm adding.
- **AGPL caveat**: AGPL's copyleft attaches to the *software* (if you modify and network-deploy
  SimpleTuner itself, you'd owe source). It does not, under current legal consensus (untested in
  court for ML specifically), extend to the *output weights* of a training run — a LoRA file is
  not treated as a derivative work of the training script that produced it, the same way a
  DreamBooth checkpoint from an Apache-2.0 trainer isn't. This is community consensus, not a
  settled legal ruling — flagged as a real but low-probability risk, not a blocker.

### OneTrainer (Nerogar)
- **License**: AGPL-3.0. [github.com/Nerogar/OneTrainer](https://github.com/Nerogar/OneTrainer)
  (same AGPL caveat as SimpleTuner above).
- **Base support**: Qwen-Image and FLUX.2 (dev + klein) both supported. **HiDream is not** — a
  feature request (#788) has been open since April 2025 with no resolution as of this search.
- **Verdict**: fine as a secondary GUI-based option for FLUX.2/Qwen-Image, not usable for HiDream.

### diffusion-pipe (tdrussell)
- **License**: GPLv3. [github.com/tdrussell/diffusion-pipe](https://github.com/tdrussell/diffusion-pipe)
  (same non-viral-to-output caveat as the AGPL tools above, GPL rather than AGPL).
- **Base support**: broadest list found of any tool — SDXL, Flux (1 and 2, dev and klein),
  LTX-Video, HunyuanVideo, Cosmos, Lumina 2.0, Wan 2.1/2.2, Chroma, **HiDream**, SD3,
  Cosmos-Predict2, OmniGen2, Flux Kontext, Qwen-Image, Qwen-Image-Edit, HunyuanImage-2.1, and more.
- **Standout finding**: this is the only tool with a **documented, working single-3090 (24 GB)
  HiDream LoRA recipe** — a maintainer/community issue thread with concrete settings: nf4
  quantization (fp8 quantization was reported to fail), `blocks_to_swap=24`,
  `micro_batch_size_per_gpu=1`, `activation_checkpointing=true`, rank-64 LoRA, 111-image dataset,
  1024px, ~8.8 sec/step, ~65 min/epoch. [tdrussell/diffusion-pipe issue
  #268](https://github.com/tdrussell/diffusion-pipe/issues/268)
- **Verdict**: the right tool specifically **if HiDream is the chosen base** and the 24 GB
  upgrade is in hand; pipeline-parallel design also means it's the one built to scale beyond a
  single GPU if the project ever rents multi-GPU.

**Tooling verdict**: standardize on **ai-toolkit (MIT)** as the primary trainer for FLUX.2 klein 4B
and Qwen-Image. If HiDream specifically is chosen as the base (its 17.1B size and MIT-labeled
license make it tempting — but see §3's licensing wrinkle), use **diffusion-pipe (GPLv3)** instead
of ai-toolkit for that one base, since it has the only proven 24 GB recipe.

---

## 3. A licensing wrinkle the brief's "(MIT)" label doesn't capture

HiDream-I1-Full's **transformer** is MIT-licensed, confirmed directly from the model card. But the
model's text encoder stack is **two** components, not one:
`google/t5-v1_1-xxl` (Apache 2.0, clean) **and** `meta-llama/Meta-Llama-3.1-8B-Instruct`
— which is under the **Llama 3.1 Community License Agreement**, not MIT and not OSI-approved.
[HiDream-ai/HiDream-I1-Full README](https://huggingface.co/HiDream-ai/HiDream-I1-Full),
[Llama 3.1 Community License](https://www.llama.com/llama3_1/license/)

That license is commercial-use-permissive for a game studio of vordar's scale (the one hard cap is
>700M MAU, which triggers a mandatory separate license from Meta — not a near-term concern), **but
it is not license-free the way MIT is**: it carries a "Built with Llama" attribution requirement
and a Notice-file requirement if the Llama Materials themselves are distributed or made available
as part of a product/service. Because the pipeline here would use Llama-3.1-8B-Instruct purely as
a frozen internal text encoder — never redistributing the Llama weights themselves to players, only
shipping the *resulting texture/concept-art images* — this most likely does **not** trigger the
attribution/naming clauses (those are written for people distributing the model itself or a
Llama-branded derivative). I could not find a primary source addressing this exact "frozen
internal component, only image outputs ship" scenario directly — flagged as **[unresolved,
low-confidence-but-probably-fine]** rather than a clean verified answer. If the studio wants
zero doubt on this point, Qwen-Image (pure Apache 2.0, no Llama dependency) or FLUX.2 klein 4B
(pure Apache 2.0) are the cleaner choices; HiDream is the one base of the three that isn't a
single, uniform permissive license end to end.

---

## 4. Dataset — bootstrapping a style that does not exist yet

### Size and captioning (from the trainer vendors' own guidance, not aggregator blogs)
- **BFL's own klein LoRA guide**: 15–40 images "that share one look," 1024px+, trained to 1800
  steps with checkpoints every 250, watching sample outputs rather than loss — "for most style
  LoRAs the visual peak is around step 750–1500, not the final step" (i.e., overfitting past that
  point is expected and must be caught by eye, not by the loss curve).
  [HF blog](https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora)
- **Captioning rule, stated explicitly by BFL**: describe *what is in the image*; say **nothing**
  about the style itself. No style adjectives ("painterly," "dark fantasy") in captions — a
  unique, non-dictionary trigger token (their example: `SPR1TE8`) carries the style instead. This
  is the opposite instinct from subject/character LoRA captioning and is easy to get backwards.
- **Broader community range**: 10–50 images is the recurring number across independent guides;
  quality/diversity of the set matters more than raw count, and a documented failure mode is that
  "your model will find it harder to generate images that were not represented in your dataset" —
  e.g., no landscapes in the training set means the style will not reliably transfer to
  environment art later. This is directly relevant to §6 (catalog breadth).

### The hard problem: where does the seed set come from?

| Source | Description | IP/legal risk | Verdict |
|---|---|---|---|
| **Public-domain Spanish/Golden-Age religious painting** (Zurbarán d.1664, Ribera d.1652, Goya d.1828) via Wikimedia Commons | Free, high-resolution, thematically exact match for "Spanish-religious dark fantasy." | **Low**, with a specific EU nuance below. | **Primary recommended seed.** |
| **Museo del Prado's own Image Bank** | The Prado's *own* website (imagebankmuseodelprado.com) sells reproduction rights and explicitly states images are "for Humanities projects... may not be made available to commercial organizations" and charges €65+VAT/image for high-res files, non-commercial use only. [imagebankmuseodelprado.com](https://www.imagebankmuseodelprado.com/en/license-agreement) | **Do not use this specific channel** — contractually barred from commercial use even though the underlying paintings are public domain. | Avoid; use Wikimedia Commons instead (see below). |
| **Hand-picked closed-model generations** (e.g., curating hundreds of Midjourney/GPT-Image outputs toward a target look, then training on the curated set) | Fast, cheap, infinitely steerable during curation. | **Unchecked in this pass** — most closed-model ToS restrict using their outputs to train competing/redistributable models; this needs a dedicated ToS check per vendor before use and is flagged as **unresolved** below. | Conditional — verify per-vendor ToS first. |
| **Commissioned original art** (small paid batch from human artists specifically to seed the style) | Cleanest possible legal position — you own or license it outright. | **None**, if contracted properly. | Best legal footing, slowest/priciest per-image; realistic as a *small* seed supplement, not the bulk. |
| **Photography reference** | Legal, useful for material/lighting ground-truth. | None. | Useful supplement, not a style-transfer substitute — photography doesn't carry painterly brushwork/palette. |

**The EU public-domain nuance** (this is the finding that makes the Wikimedia Commons route
actually clean, not just "probably fine"): **Article 14 of the EU Copyright in the Digital Single
Market Directive (2019/790)** states explicitly that *"when the term of protection of a work of
visual art has expired, any material resulting from an act of reproduction of that work is not
subject to copyright or related rights, unless the material resulting from that act of
reproduction is original."* The Directive's own recitals cite exactly the practice this clause was
written to stop: *"Spanish museums claiming copyright over paintings by Dutch masters"* and German
museums suing over hosted reproductions. [EUR-Lex Directive
2019/790](https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng), [Kluwer Copyright
Blog](https://legalblogs.wolterskluwer.com/copyright-blog/the-new-copyright-directive-article-14-or-when-the-public-domain-enters-the-new-copyright-directive/)

In practice: the Prado's own contractual fee applies only to files obtained *from the Prado under
its contract*. A faithful photographic reproduction of a Zurbarán obtained from Wikimedia Commons
(uploaded under the long-standing "PD-Art" reasoning, reinforced by Article 14 specifically for EU
use) carries **no new copyright** for a shipped EU commercial product. This is a meaningfully
different, cleaner position than the German pre-2019 case law (BGH's Reiss-Engelhorn ruling,
Case No. I ZR 104/17, Dec 2018) which had found German related-rights protection for museum
photos of PD art *before* Article 14 was transposed — Article 14 was written specifically to
override that outcome EU-wide going forward.

**Copyrighted contemporary concept art as a data source** (e.g., scraping ArtStation portfolios or
published artbooks for register-matching, not direct copying): the **EU TDM exception (Article 4,
same Directive)** permits text-and-data-mining, including for commercial purposes, on lawfully
accessed copyrighted works **by default**, unless the rightsholder has opted out via a
machine-readable reservation. Two German courts have already confirmed Article 4 covers AI
training specifically (Munich Regional Court, Nov 2025), with the caveat that if the trained model
*memorizes and reproduces* specific training images, that output falls outside the exception's
protection. [technollama.co.uk](https://www.technollama.co.uk/we-need-to-talk-about-the-eu-tdm-exception-and-ai-training),
[jiplp Oxford Academic](https://academic.oup.com/jiplp/article/19/5/453/7614898). This is
**legally permissive but reputationally live** — ArtStation and similar platforms have pushed
opt-out mechanisms, and "did a AAA-adjacent studio train on scraped living artists' portfolios" is
exactly the kind of story that generates real backlash regardless of the legal floor. Recommend
treating public-domain historical painting as the **primary** seed and any contemporary reference
as **mood-board-only, never training data**, to keep the legal and reputational pictures both
clean.

---

## 5. Cost and wall-time per training run

| Base | 12 GB local (3080 Ti, today) | 24 GB local (3090, if bought) | Rented |
|---|---|---|---|
| **FLUX.2 klein 4B** | **Fits.** BFL's own docs list 12 GB VRAM (RTX 3060 12GB / RTX 4060 Ti 16GB) as the minimum for LoRA training. Community reports of Q4-GGUF-level 12 GB training exist but call it "several hours per attempt" [secondary]. | Comfortable — BFL calls the RTX 4090 the "sweet spot," ~1 hr for an 1800-step run. | RunPod RTX 4090 secure $0.69/hr, community $0.34/hr, RTX 3090 community $0.22/hr — a full 1–3 hr run costs roughly **$0.25–$2**. |
| **Qwen-Image 20.4B** | **Does not fit** at anything beyond an unverified edge case (Ostris's own tweet on the *Edit* variant reports 8–9 GB is reachable only with 3-bit ARA quantization + layer offloading + 60GB+ system RAM — not independently confirmed for the base model, not practical). | Fits with quantization — Ostris (ai-toolkit's own maintainer) states 24 GB VRAM with 3-bit ARA quantization is the real minimum. | RunPod A100 80GB $1.19–1.49/hr; multi-hour run (no clean total-hours figure found for Qwen-Image specifically) — **[gap, flagged below]**. |
| **HiDream-I1-Full 17.1B** | **Does not fit at all** — the model needs ~27 GB of VRAM just for *inference* at usable precision, confirmed via a direct HF model-card discussion thread. | Fits only via diffusion-pipe's specific nf4-quantization recipe (§2): ~65 min/epoch, 8.8 sec/step, on a 111-image/444-step-per-epoch dataset; the recipe author trained 10+ epochs and resumed repeatedly to catch overfitting, so realistic wall-time to a checked, non-overfit result is several hours, not one epoch. ai-toolkit's own default HiDream config targets 48 GB, not 24 GB. | RunPod RTX 3090 community $0.22/hr / secure $0.46/hr for the diffusion-pipe recipe; a full multi-hour (5–10 hr) run costs roughly **$1–$5**. |

**Iterations to converge on a usable, shippable style**: no primary source directly quantifies
"how many training *runs*" (as opposed to steps within one run) a from-scratch novel style needs.
My own reasoned estimate, stated as inference not fact: converging on ONE clean style-LoRA training
run, given a well-curated 15–40 image seed set, takes the BFL-documented ~1 hour/$1-2 (FLUX.2
klein) — but getting from "no style exists" to "shippable, catalog-wide house style" is an
iterative *dataset* loop, not a training-hyperparameter loop: curate seed → train → generate a test
batch across asset classes → identify where it drifts (see §6) → add counter-examples/recaption →
retrain. Budget **3–8 training-run iterations**, each an hour and a few dollars on FLUX.2 klein 4B,
before the style is stable enough to trust at catalog scale. Total compute cost to a shippable LoRA
is therefore trivial (likely under $20 all-in on rented RTX 4090/3090 spot pricing); the actual
cost driver is **human curation time** across those iterations, not GPU-hours.

**Renting vs. NVIDIA free credits**: NVIDIA's own API Trial Terms of Service and LaunchPad Terms
of Use both restrict free/trial credits to "internal testing and evaluation," explicitly **not
production** use without a paid subscription. [NVIDIA API Trial
ToS](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)
— confirms the project's existing assumption; do not route shipped-asset training through NVIDIA
free-credit programs.

---

## 6. Consistency at scale across ~1,100 catalog items, multiple asset classes

Documented failure modes, from the trainer ecosystem and one directly relevant 2026 paper:

- **Style drift on out-of-distribution content**: "your model will find it harder to generate
  images that were not represented in your dataset" — if the seed set is character-heavy and
  thin on environments/props, style fidelity measurably degrades on those under-represented
  classes. **Actionable**: the seed dataset (§4) must deliberately span armor, props,
  environments, *and* characters, not just "good-looking art" — breadth is a training-data
  requirement, not a nice-to-have.
- **Overfitting / memorization**: "common overfitting occurs when a LoRA has memorized training
  images rather than learning underlying traits, manifesting as generations that look identical
  to source images, often with artifacts. Too many epochs cause content memorization" — this is
  exactly why BFL's own guide says to watch sample outputs, not the loss curve, and expects the
  visual peak mid-run (step 750–1500 of 1800), not at the end.
- **Content/style bleed and subject bleed**: "stylistic bleed refers to whether a LoRA imposes
  unwanted styles or artifacts from training data onto new generations" — a homogeneous seed set
  (e.g., all half-body devotional portraits) risks the trigger token absorbing incidental
  *subject* matter (pose, composition, cropping) along with the intended *style*, producing
  unwanted sameness across unrelated catalog items. Mitigation cited in the literature: prompt
  dropout during training, and explicitly varying composition/subject within the style-consistent
  seed set.
- **ConsisLoRA's three named failure modes** (arXiv:2503.10614, a 2026-relevant paper addressing
  exactly this): "content inconsistency, style misalignment, and content leakage" in vanilla
  LoRA-based style transfer. Its fix (predicting the denoised image rather than noise, plus a
  two-step content/style-separated training strategy) is a real, more-robust alternative training
  objective if vanilla LoRA/DoRA measurably struggles with cross-class consistency in testing —
  but it is a research technique, not shipped in any of the five trainers in §2. Flagged as a
  fallback to investigate, not a day-one plan.

**Practical read**: a single style LoRA can plausibly hold across ~1,100 items *if* the seed
dataset is deliberately built to span every asset class up front, epochs are kept conservative
(watching samples, stopping near the documented 750–1500-step peak rather than training to
convergence-by-loss), and the studio budgets for an iterative curation loop (§5) rather than a
one-shot training run. No source found guarantees this at 1,100-item scale specifically — this is
extrapolated from documented failure modes and the vendor's own overfitting warnings, not a
verified claim that any team has actually run a style LoRA across a catalog this size.

---

## 7. The honest comparison: how much worse than a human concept artist, and where

**Comparable shipped games and their real pipelines:**

- **Diablo IV** (Blizzard) — the closest register match found: art director John Mueller has
  stated the team's explicit references were academic/classical painting — neoclassicism,
  pre-Raphaelites, Géricault's *Raft of the Medusa*, Bulwer-Lytton-era history painting — the same
  "museum painting applied to dark fantasy" register vordar is targeting, even though the specific
  reference painters differ (French Romanticism/British academic painting vs. Spanish Golden Age).
  Diablo IV's pipeline was **not** small: it combined a large in-house concept team with an
  external outsourcing studio, **Room 8 Group**, which delivered character skins, armor sets,
  weapons, mounts, and cosmetics under named division leads (a Principal Character Concept Lead, a
  2D Division Art Director, a 3D Characters Team Lead, and a dedicated Art Producer coordinating
  the engagement). [Room 8 Studio case
  study](https://room8studio.com/news/room-8-groups-artwork-for-diablo-iv-a-closer-look/),
  [gameshub.com Diablo IV art director
  interview](https://www.gameshub.com/news/features/diablo-4-art-director-interview-classical-art-for-a-new-generation-2623172/) [secondary/blog, WebFetch was blocked by a 403 on direct fetch — relayed via search summary, not independently re-verified against the original article text]
- **Path of Exile 2** (Grinding Gear Games) — fully in-house, human-illustrated. Concept artist
  Shaun Brown's public role covers "Monsters, Weapons, Bosses, Portals, MTX, Uniques, Characters,
  Pets, Symbols, and Graphical illustrations" — i.e., one specialist illustrator's remit already
  spans most of what vordar's catalog needs, illustrating how much per-artist range a AAA-adjacent
  studio expects from skilled humans. [Steam News developer
  interview](https://store.steampowered.com/news/app/238960/view/2925613388070970013) No public
  disclosure of GGG using AI tooling in their pipeline was found.

**Cost framing**: freelance concept art rates cluster around **$63–68/hr average**, or per-piece
flat rates in the range of **$300 (character sketch) to $800 (fully rendered character)**
[secondary/aggregator sources, not a single authoritative rate card — figures recur consistently
across multiple pricing-guide sites but none is a primary industry survey]. At a blended
conservative $150/item across ~1,100 catalog items spanning simple props through full character
pieces, human concept art alone would run **roughly $150,000+** before any 3D production — and
that reflects exactly the team-scale reality Diablo IV's own pipeline shows (in-house team +
outsourcing vendor), not a boutique/solo effort.

**Where the LoRA route is worse, specifically**:
- **No architectural/mechanical reasoning**: a human artist designing a cathedral ruin or a piece
  of armor reasons about how it would actually be built/worn; a diffusion model renders surface
  plausibility without underlying structural logic — this is the single most consistently reported
  qualitative gap in the broader research (echoed in R2's own note on FLUX.2's "genuinely novel
  structural invention" weakness).
- **No directed revision**: a human artist takes art-direction notes ("move the pauldron in,"
  "make the cross more Visigothic-specific") and iterates with intent; a LoRA-driven pipeline
  iterates by reprompting/regenerating and hoping, which is slower to converge on a *specific*
  brief even though it's faster to produce *volume*.
- **Requires a human curation pass regardless**: every cited trainer guide assumes someone is
  looking at sample grids and rejecting bad output by eye (this is explicitly how BFL says to find
  the "peak" checkpoint) — the LoRA route does not remove the human art-director role, it changes
  it from "draw everything" to "curate and steer everything," and understates the effort if that
  curation loop is not budgeted for.
- **Where it's NOT worse**: raw per-item marginal cost and turnaround for volume/breadth (armor
  variant #47 of a catalog of 200) — this is exactly the case where a converged, well-curated
  style LoRA plausibly matches or beats a human pipeline on cost, and where AAA studios
  historically threw outsourcing-studio headcount at the problem instead.

---

## 8. Maturity summary

| Option | Maturity |
|---|---|
| LoRA (any base) | Production-proven |
| DoRA | Production-proven as a technique; diffusion-style-specific advantage is inferred, not directly benchmarked |
| LoKr/LyCORIS | Production-proven within its community; less history specifically on the three target bases |
| Full fine-tune/DreamBooth | Production-proven technique, wrong-sized for this problem's realistic dataset scale |
| Textual inversion | Production-proven, ruled out as too weak for detailed style |
| Training-free/reference-guided (AttenST/CoCoDiff/AnyStyle) | Bleeding-edge, research-only, no production tooling found |
| ai-toolkit on FLUX.2 klein 4B | Production-proven, vendor-endorsed (BFL's own blog) |
| ai-toolkit on Qwen-Image | Production-proven, community-standard |
| ai-toolkit on HiDream | Works, but its own default config wants 48 GB — the toolkit's weakest-fitting corner |
| diffusion-pipe on HiDream (24 GB) | Bleeding-edge-but-working — one documented community recipe, not an official vendor guide |
| kohya_ss/sd-scripts on any of the three target bases | **Not supported at all** — not a maturity gap, a support gap |

---

## Unresolved / could not verify

- **Exact GGUF-quant level and step-by-step numbers for FLUX.2 klein 4B training specifically on a
  3080 Ti (12 GB)** — BFL's docs confirm the 4B model's minimum is 12 GB, but no source gave a
  concrete wall-time/step figure at that exact VRAM ceiling on that exact card; the "several hours
  per attempt" figure found is for Q4 GGUF generically, not benchmarked on a 3080 Ti.
- **Total wall-time-to-convergence for a Qwen-Image style LoRA** — VRAM minimums are well-sourced
  (24 GB via 3-bit ARA), but no source gave a total-hours or steps-to-peak figure comparable to
  BFL's own 750–1500-step guidance for klein.
- **Closed-model-output ToS restrictions on using generations as LoRA training data** — flagged in
  §4 as a real open question (Midjourney/GPT-Image/etc. ToS on this were not checked in this pass)
  and should be resolved per-vendor before that sourcing route is used.
- **Whether shipping a game whose internal art pipeline used HiDream's frozen Llama-3.1-8B-Instruct
  text encoder, without redistributing the Llama weights, triggers the Llama 3.1 Community
  License's "Built with Llama" attribution clause** — no primary source addressing this specific
  "frozen internal component, only image outputs ship" scenario was found; treated as
  probably-fine but unverified in §3.
- **Whether AGPL/GPL training-tool licenses (SimpleTuner, OneTrainer, diffusion-pipe) create any
  copyleft obligation on the LoRA weights those tools produce** — general ML-community consensus
  says no (weights aren't a derivative work of the training script), but this is untested in court
  for machine-learning specifically; flagged as low-probability risk, not verified absence of risk.
- **Gameshub.com's Diablo IV art-director interview** was relayed via WebSearch's summary only — a
  direct WebFetch returned HTTP 403. The quotes attributed to it above should be treated as
  secondary/paraphrased, not a verbatim primary-source quote.
- **A concrete per-run dollar/hour total for a full 3–8-iteration bootstrap loop** (§5's "under
  $20 all-in" figure) is my own arithmetic from sourced per-hour rates and a reasoned iteration
  count, not itself a sourced figure — flagged as an estimate, not a verified cost.

---

## Sources

- [black-forest-labs/FLUX.2-klein-4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B)
- [BFL/HF blog — Fine-tune FLUX.2 [klein] with a LoRA under 60 minutes](https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora)
- [docs.bfl.ml — FLUX.2 klein training docs](https://docs.bfl.ml/flux_2/flux2_klein_training)
- [Qwen/Qwen-Image model card](https://huggingface.co/Qwen/Qwen-Image)
- [Qwen/Qwen-Image LICENSE](https://huggingface.co/Qwen/Qwen-Image/blob/main/LICENSE)
- [HiDream-ai/HiDream-I1-Full model card](https://huggingface.co/HiDream-ai/HiDream-I1-Full)
- [HiDream-ai/HiDream-I1-Full VRAM discussion #13](https://huggingface.co/HiDream-ai/HiDream-I1-Full/discussions/13)
- [Llama 3.1 Community License Agreement](https://www.llama.com/llama3_1/license/)
- [ostris/ai-toolkit GitHub repo](https://github.com/ostris/ai-toolkit)
- [ostris/ai-toolkit HiDream 48GB example config](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_hidream_48.yaml)
- [Ostris (X/Twitter) — Qwen-Image LoRA on 24GB with 3-bit ARA quantization](https://x.com/ostrisai/status/1955464335616327810)
- [kohya-ss/sd-scripts GitHub repo](https://github.com/kohya-ss/sd-scripts)
- [kohya-ss/sd-scripts LICENSE.md](https://github.com/kohya-ss/sd-scripts/blob/main/LICENSE.md)
- [bghira/SimpleTuner GitHub repo](https://github.com/bghira/SimpleTuner)
- [bghira/SimpleTuner pyproject.toml (license)](https://github.com/bghira/SimpleTuner/blob/main/pyproject.toml)
- [bghira/SimpleTuner FLUX2 quickstart](https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/FLUX2.md)
- [SimpleTuner Qwen-Image quickstart (mirror)](https://github.com/apppidev/SimpleTuner/blob/main/documentation/quickstart/QWEN_IMAGE.md)
- [Nerogar/OneTrainer GitHub repo](https://github.com/Nerogar/OneTrainer)
- [Nerogar/OneTrainer HiDream feature request #788](https://github.com/Nerogar/OneTrainer/issues/788)
- [tdrussell/diffusion-pipe GitHub repo](https://github.com/tdrussell/diffusion-pipe)
- [tdrussell/diffusion-pipe LICENSE](https://github.com/tdrussell/diffusion-pipe/blob/main/LICENSE)
- [tdrussell/diffusion-pipe HiDream single-3090 notes, issue #268](https://github.com/tdrussell/diffusion-pipe/issues/268)
- [DoRA: Weight-Decomposed Low-Rank Adaptation, arXiv:2402.09353](https://arxiv.org/abs/2402.09353)
- [KohakuBlueleaf/LyCORIS GitHub repo](https://github.com/KohakuBlueleaf/LyCORIS)
- [LyCORIS Guidelines.md](https://github.com/KohakuBlueleaf/LyCORIS/blob/main/docs/Guidelines.md)
- [Kohaku-XL Epsilon (Kohaku BlueLeaf)](https://kblueleaf.net/posts/kohaku-xl-epsilon/)
- [ConsisLoRA, arXiv:2503.10614](https://arxiv.org/abs/2503.10614)
- [AnyStyle, arXiv:2607.04677](https://arxiv.org/abs/2607.04677)
- [CoCoDiff, arXiv:2602.14464](https://arxiv.org/pdf/2602.14464)
- [AttenST, arXiv:2503.07307](https://arxiv.org/pdf/2503.07307)
- [RunPod pricing page](https://www.runpod.io/pricing)
- [NVIDIA API Trial Terms of Service (PDF)](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)
- [EUR-Lex — Directive (EU) 2019/790 (DSM Directive), Article 14 and Article 4](https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng)
- [Kluwer Copyright Blog — Article 14 and the public domain](https://legalblogs.wolterskluwer.com/copyright-blog/the-new-copyright-directive-article-14-or-when-the-public-domain-enters-the-new-copyright-directive/)
- [Museo del Prado Image Bank license agreement](https://www.imagebankmuseodelprado.com/en/license-agreement)
- [Wikimedia Commons — Category:Paintings by Francisco de Goya](https://commons.wikimedia.org/wiki/Category:Paintings_by_Francisco_de_Goya)
- [Wikimedia Commons — Category:Paintings by José de Ribera](https://commons.wikimedia.org/wiki/Category:Paintings_by_Jos%C3%A9_de_Ribera)
- [TechnoLlama — EU TDM exception and AI training](https://www.technollama.co.uk/we-need-to-talk-about-the-eu-tdm-exception-and-ai-training)
- [JIPLP (Oxford Academic) — Article 4(3) CDSMD opt-out analysis](https://academic.oup.com/jiplp/article/19/5/453/7614898)
- [Room 8 Studio — Diablo IV artwork case study](https://room8studio.com/news/room-8-groups-artwork-for-diablo-iv-a-closer-look/)
- [gameshub.com — Diablo 4 art director interview (relayed via search, direct fetch 403'd)](https://www.gameshub.com/news/features/diablo-4-art-director-interview-classical-art-for-a-new-generation-2623172/)
- [Path of Exile Steam News — Developer Interview, Concept Artist QingYi Li / Shaun Brown](https://store.steampowered.com/news/app/238960/view/2925613388070970013)
- [BGH Reiss-Engelhorn ruling summary, Lexology](https://www.lexology.com/library/detail.aspx?g=a3fbc691-11fa-4bfe-805c-c07ab323f01d)

---

# Verification pass (orchestrator, 2026-07-20)

Re-checked every load-bearing claim against raw primary sources — `raw.githubusercontent.com`
files and the HF API, fetched as plain bytes via curl, not through a summarizing proxy.

## Confirmed

- **kohya_ss/sd-scripts supports none of the three bases.** Direct README fetch, current main:
  supported list is SDXL · SD3/SD3.5 · **FLUX.1** · LUMINA · HunyuanImage-2.1 · Anima. No FLUX.2,
  no Qwen-Image, no HiDream. (The one Qwen-Image mention in its changelog is a *VAE* PR consumed by
  Anima training, not Qwen-Image model support.) **R2's "kohya_ss has rock-solid FLUX.2 support"
  claim is superseded and should be struck.**
- **ai-toolkit is MIT** (`Copyright (c) 2024 Ostris, LLC`) and its README lists FLUX.2-dev,
  FLUX.2-klein-base-4B, FLUX.2-klein-base-9B, Qwen-Image, HiDream-I1-Full, HiDream-O1/E1. All three
  bases confirmed.
- **HiDream's Llama dependency is real.** `model_index.json` declares four text encoders:
  two `CLIPTextModelWithProjection`, one `T5EncoderModel`, and `text_encoder_4` =
  **`LlamaForCausalLM`**. The MIT tag covers the transformer only. The wrinkle stands.

## Corrected — the agent's headline "good news" is wrong

The report's bottom-line claim that *"BFL's own training docs state the 4B model trains on 12 GB
VRAM"* is **not supported**. BFL's own LoRA guide says the opposite, verbatim:

> "a LoRA run lands under 24 GB, so a 4090 or an L4 is enough" · "An RTX 4090 (24 GB) is the sweet
> spot" · "you have a 24 GB+ NVIDIA GPU"

The 12–13 GB figure is the **inference** number, not training. The model card: *"The FLUX.2 [klein]
4B Base model fits in ~13GB VRAM and is accessible on NVIDIA RTX 3090/4070 and above."*
The agent conflated the two. So:

| | VRAM | 3080 Ti (12 GB) | 3090 (24 GB) |
|---|---|---|---|
| klein 4B inference | ~13 GB BF16 | just short — needs offload or Q8 | comfortable |
| klein 4B LoRA training | <24 GB | **no** | **yes, exactly at spec** |

**This converges with G2 rather than undermining it.** BFL names the RTX 3090 as the entry card for
inference and 24 GB as the training requirement. The G2 recommendation is unchanged and now has a
second independent justification: 24 GB is the stated minimum to train a house style at all.

## Corrected — R2's FLUX.2 klein facts were wrong in two ways

R2 recorded "FLUX.2 [klein] 4B, Apache 2.0, HF repo **gated (401)**" and "4B distilled from 9B flow
+ **8B Qwen3 text embedder**". Both wrong:

1. **Not gated.** `FLUX.2-klein-4B` and `FLUX.2-klein-base-4B` are both `"gated": false`,
   `license: apache-2.0`, with Apache text in `LICENSE.md`. R2's 401 came from querying a repo name
   that does not exist (`FLUX.2-klein`, no size suffix). **Both are downloadable right now.**
2. **The text encoder is Qwen3-4B, not 8B.** `text_encoder/config.json`: `Qwen3ForCausalLM`,
   hidden 2560, 36 layers; index metadata `total_parameters: 4,022,468,096`,
   `total_size: 8,044,936,192` bytes.

Corrected arithmetic for klein 4B:

| Component | Params | BF16 |
|---|---|---|
| Flow transformer | 3,875,544,576 | 7.75 GB |
| Qwen3 text encoder | 4,022,468,096 | 8.04 GB |
| **Total** | **~7.9B** | **~15.8 GB** (BFL quotes ~13 GB with offload) |

**My G2 table listed klein 4B at "4B flow + 8B text embedder, ~24 GB."** That 8B belongs to the
9B klein / FLUX.2-dev line, not the 4B. G2's klein row is overstated by ~8 GB. The G2 *conclusion*
survives — the buy case never rested on klein, it rested on Qwen-Image (40.9 GB) and HiDream
(34.2 GB), both re-verified and unchanged — but the klein row itself should be read as ~15.8 GB.

## New finding: the 9B klein is not usable

`FLUX.2-klein-9B` and `-base-9B` are `"gated": "auto"` under **`flux-non-commercial-license`**.
BFL's model card states the split deliberately: *"we approved the release of the open-weight
FLUX.2 [klein] 4B models under an Apache 2.0 license and the release of the FLUX.2 [klein] 9B
models under a non-commercial license."* Only the **4B** is commercially shippable. Any future
note that says "FLUX.2 klein is Apache" without the size qualifier is wrong and will mislead.

Also verified from the model card, and worth recording because it is the exact permission this
project needs: *"Outputs can be used for commercial purposes, as described in the Apache 2.0
license."*

## New finding: train on base, infer on distilled

klein ships each size as a **distilled (4-step)** and a **base (50-step)** variant. BFL: *"For LoRA
training the relevant one is base... you train against the base checkpoint and the adapter still
loads on the distilled model afterward."* And: *"Applying the LoRA on the distilled model typically
gives better results than the base model, and it's faster — so distilled is the one to run."*
Both variants are Apache 2.0. So the pipeline is: train `FLUX.2-klein-base-4B` → ship inference on
`FLUX.2-klein-4B` at 4 steps. The agent's report never distinguished the two.

---

# Gap-check pass

Four things this research did not cover, one of which could invalidate the whole approach.

## 1. Control tooling for FLUX.2 klein was never checked — this is the real risk

The armor plan does not generate free-floating images. `prop_texture.py --strategy multiview`
drives **xinsir ControlNet-depth on SDXL** from ortho depth renders. A house-style LoRA is worth
nothing to this pipeline unless the base it trains on also has a mature depth-control path, and
**a style LoRA and a ControlNet must compose at inference without either degrading the other.**
Neither question was asked. Assigned to **A4**, which is now a hard blocker on the base decision
rather than an "as it becomes relevant" item — the ordering in BACKLOG.md should change.

## 2. Dataset breadth vs. dataset size is an unresolved contradiction

§4 takes BFL's **15–40 images** at face value; §6 then requires the seed set to deliberately span
armor, props, environments **and** characters or the style silently degrades on whatever class is
under-represented. Those pull against each other — 15–40 images across four asset classes is ~8
per class, which is below any cited threshold for reliable coverage. Three ways out, none
researched: a larger single set (100–200, into LoKr territory), **one LoRA per asset class sharing
a seed aesthetic**, or a small style LoRA plus per-class prompt scaffolding. Unresolved, and it
determines dataset labor — the report's own stated real cost driver.

## 3. The bootstrap loop is described but never specified

"Where does the dataset come from" gets a good sourcing table but no mechanism. The concrete loop
is: prompt a stock base hard, using public-domain Zurbarán/Ribera/Goya plates as img2img or style
reference → curate the ~30 that land nearest the target → train → regenerate → recurate. The
implication nobody stated: **iteration 1's dataset is necessarily off-target**, so the first LoRA
is a stepping stone, not a deliverable. The "3–8 iterations" estimate is doing a lot of unexamined
work — it is the single largest unknown in the plan, and it is a labor estimate, not a compute one.

## 4. Assumption worth naming: one style LoRA for the whole catalog

Every section assumes a single adapter. Nothing verified says that is right, and §6's own cited
failure modes (content leakage, style misalignment) are exactly what surfaces when one adapter is
stretched across dissimilar content. Cheap to test once a first LoRA exists; expensive to discover
late.

## Not a gap — correctly out of scope

The report properly refused to guess on closed-model-output ToS (A2's job) and correctly flagged
the AGPL-output question as community consensus rather than settled law. Both stay open, neither
blocks.

## Net position

The working assumption survives verification: **LoRA/DoRA on FLUX.2-klein-base-4B via ai-toolkit
(MIT) is a fully permissive, commercially-shippable, vendor-documented path to a house style**, at
trivial compute cost, gated on 24 GB of VRAM and on A4 confirming depth-control composability.
The real cost is human curation across an unknown number of dataset iterations, not GPU time.
