# A5 — Comparative: does the model actually look good, and what happens when real people use it

Research date: 2026-07-20. Every score, rank, and quote below is sourced from a live WebSearch/
WebFetch on this date. This report deliberately does **not** re-verify licenses (done in A1/A3/A4)
and does not re-litigate VRAM/training-cost numbers (done in A3) — it answers a narrower question
those passes could not: **is the output actually good, specifically for dark, painterly,
Spanish-religious concept art, and what breaks when people use these models for real work.**

**Recency discipline, stated up front because it is the load-bearing finding of this whole
report**: the single most concrete, comparable number in this space — the Artificial Analysis
Elo leaderboard — is extremely volatile *by rank* even when a model's *score* barely moves,
because dozens of new competitor models enter the arena every month and dilute everyone's
relative position. Two models in this report demonstrate this directly:

- **Z-Image Turbo** launched at rank 8 overall / **"#1 open-weight model"** per Artificial
  Analysis's own announcement (late Nov 2025). Today, 2026-07-20, it sits at **rank 66** (Elo
  1100) — not because the model changed, but because ~58 new entries (mostly closed models)
  were added above it. [x.com/ArtificialAnlys, Nov 2025](https://x.com/ArtificialAnlys/status/2002839525609865575)
- **HiDream-O1-Image** was reported at **rank 8, "the highest-ranked open-weight entry on the
  board"** as of 2026-05-05. Today it sits at **rank 59** (Elo 1111) — the same pattern, ~2.5
  months later. [WaveSpeed, 2026-05-05](https://wavespeed.ai/blog/posts/hidream-o1-image-dev-pixel-unified-transformer/)

Any comparison article, benchmark citation, or "X is #1 open-weight" claim below is therefore
reported with its **Elo score** (comparable across time) separately from its **rank** (not
comparable across time — a snapshot of a specific, shifting field). Anything older than ~4
months is flagged **provisional**; nothing found in this pass is younger than ~2.5 months.

---

## Bottom line

**Ranked recommendation for vordar's specific need** — dark, painterly, Spanish-religious
dark-fantasy concept art, depth-ControlNet-driven, needing a durable house-style LoRA — **stated
with honest, medium confidence**, because the one thing that would settle this (a direct
painterly/dark-fantasy side-by-side) does not exist anywhere in the literature found (§ "Where
the evidence is thin").

1. **Z-Image (Base for training / Turbo for inference)** — best-evidenced fine-tuning story of
   any model in this report (real GitHub/Civitai training write-ups, not just vendor docs), beats
   the full 20.4B Qwen-Image on blind-preference Elo despite being 6B, and has a genuine depth
   ControlNet (A4). **The real risk, and it is a real one**: every quality signal found for
   Z-Image is about photorealistic portraits and skin texture — its one documented weak spot,
   repeated independently on Hacker News, is "how little it can do" outside photographic subject
   matter. That is close to the opposite of what this project needs. Recommend as the lead
   bake-off candidate, but do not assume its Elo score transfers to painterly work.
2. **Qwen-Image (20.4B, the listed candidate)** — most literal/instruction-following of the
   group, genuinely strong depth ControlNet already in ComfyUI core (A4), and the LoRA-training
   *process* is reported as smooth. But it carries the report's single most repeated, most
   cross-sourced complaint (**"plastic skin"** — independently reported across HF discussion
   threads and multiple YouTube "fix" tutorials, not one loud post) and a documented low-seed-
   variance problem that **a trained LoRA did not fix** in one direct practitioner account. Both
   are aesthetic-fidelity risks for a project chasing painterly texture and material grime, not
   glossy uniformity.
3. **FLUX.2 klein 4B (Apache, the only fully commercially-clean FLUX.2 tier per A3)** — the
   weakest raw-quality standing of the four Apache-clean bases on the one dated blind-preference
   number available (tied with Qwen-Image's full 20.4B at 1058 Elo, ~40-90 points behind Z-Image
   and FLUX.2 dev), and it structurally runs at CFG=1 in its distilled form, narrowing prompt-
   adherence tuning. It remains relevant only because of BFL's own vendor-grade LoRA tooling (A3)
   — a tooling advantage, not a quality one.
4. **SDXL (incumbent baseline)** — decisively behind on raw quality now: **873 Elo**, roughly
   190-280 points below every other candidate in this report, the largest gap in the whole table.
   It survives only as the "safe fallback with 1,900-5,000+ Civitai resources behind it," not as
   a quality target. Its presence in this report is to calibrate how far the field has moved, not
   as a live recommendation.
5. **FLUX.2 dev** — the best raw open-weight quality of anything in this report (1152 Elo, clear
   leader among the candidates) and reportedly punches above HiDream/Cosmos-tier competitors — but
   A3 already ruled it non-commercial-licensed and un-trainable on this project's hardware; listed
   here only for the quality ceiling it establishes.
6. **HiDream-I1/O1 (mentioned per the brief's instruction, not a primary candidate)** — genuinely
   strong on benchmarks (HiDream-O1-Image at 1111 Elo, ahead of Z-Image and Qwen-Image 2.0; one
   source claims it "beat" a much larger FLUX.2 on several published metrics) but A3/A4 already
   flagged the Llama-3.1 text-encoder licensing wrinkle and the missing dedicated depth
   ControlNet — this report adds no reason to revisit either finding.

---

## The dated leaderboard — Artificial Analysis, live fetch 2026-07-20

[artificialanalysis.ai/image/leaderboard/text-to-image](https://artificialanalysis.ai/image/leaderboard/text-to-image),
cross-checked against [artificialanalysis.ai/image/models](https://artificialanalysis.ai/image/models).
Blind-preference Elo from human votes comparing two images from the same prompt. **Same caveat
R2 already raised, restated because it applies with full force here**: Elo-from-blind-votes
rewards "which image do untrained raters click as prettier" — punchy contrast and photographic
realism — not painterly/dark/atmospheric fidelity, depth-controllability, or style-lock. Treat
rank as one input, never the verdict.

| Rank | Model | Elo | Params | License posture | Released | Open-weight? |
|---|---|---|---|---|---|---|
| 1 | GPT Image 2 (high) | 1339 | — | closed | — | No |
| 35 | **FLUX.2 [dev]** | 1152 | 32B | non-commercial (A3) | Nov 2025 | Yes, gated non-comm |
| 33 | Qwen Image Max 2512 | 1155 | — | closed hosted tier | Dec 2025 | No (not a candidate) |
| 55 | FLUX.2 [klein] 9B | 1118 | 9B | non-commercial (A3) | Jan 2026 | Yes, gated non-comm |
| 59 | HiDream-O1-Image | 1111 | 8B | MIT transformer + Llama wrinkle (A3) | May 2026 | Yes |
| 66 | **Z-Image Turbo** | 1100 | 6B | Apache 2.0 | Nov/Dec 2025 | **Yes** |
| 67 | Qwen Image 2.0 | 1099 | 7B | Apache 2.0 (per prior reporting) | Mar 2026 | Yes — **different model from the 20.4B candidate, see note below** |
| 75 | HiDream-O1-Image-Dev | 1086 | 8B | MIT transformer + Llama wrinkle | May 2026 | Yes |
| 77 | FLUX.2 [klein] Base 9B | 1082 | 9B | non-commercial | Jan 2026 | Yes, gated non-comm |
| 90 | HiDream-I1-Dev | 1062 | 17B | MIT transformer + Llama wrinkle | Apr 2025 | Yes |
| **91/92** | **FLUX.2 [klein] 4B** / **Qwen-Image (20.4B)** | **1058 / 1058** | 4B / 20.4B | **both Apache 2.0** | Jan 2026 / Aug 2025 | **Yes — both listed candidates, tied** |
| 93 | HiDream-I1-Fast | 1057 | 17B | MIT + Llama wrinkle | Apr 2025 | Yes |
| 99 | Z-Image Base | 1032 | 6B | Apache 2.0 | Jan 2026 | Yes (trainable checkpoint) |
| 119 | FLUX.2 [klein] Base 4B | 965 | 4B | Apache 2.0 | Jan 2026 | Yes (trainable checkpoint, low raw Elo by design — see A3's "train on base, infer on distilled") |
| 132 | **SDXL 1.0** | **873** | 3.5B | permissive | Jul 2023 | Yes |

**Read carefully, this is the report's central number**: the 6B **Z-Image Turbo (1100)** outranks
the full 20.4B **Qwen-Image (1058)** by 42 Elo points, and both the 20.4B Qwen-Image and the
4B **FLUX.2 klein** land in an exact tie at 1058 — a fifth-the-size Apache model matching a
20B Apache model on blind human preference. **SDXL trails everything by 85-280+ points.** This
table is the single cleanest, most-recent, most-comparable answer to Q1 and Q5 found in this
pass — everything else below is qualitative texture around these numbers.

**Important correction to how the candidate list maps onto this table**: comparisons found in
this pass are overwhelmingly about **Qwen Image 2.0 (7B, Mar 2026)**, not the **20.4B Qwen-Image**
that A1/A3 verified and that the brief lists as the candidate. These are different models —
2.0 is a much lighter, separately-trained architecture, not a size variant of the 20.4B base.
Confusingly, 2.0 (7B) *outranks* the original 20.4B on this same leaderboard (1099 vs 1058),
which is the same "small model beats big model" pattern Q5 asks about for Z-Image, just inside
Qwen's own model family. **If the project is willing to revisit A1/A3's base-model identity
(20.4B → 2.0/7B), that substitution is worth its own dedicated check** — it was out of scope
here since the brief named the 20.4B specifically, but the community's actual 2026 attention is
on 2.0, not the 20.4B.

---

## Z-Image / Z-Image-Turbo (Tongyi-MAI, 6B, Apache 2.0)

**Quality evidence**: 1100 Elo (rank 66, 2026-07-20), down from rank 8 / "#1 open-weight" at
launch (Nov 2025) — score is the comparable number, not rank (see recency note above). A
head-to-head against FLUX.2 Dev (302.AI, 2026-12-09 — **note: this is likely a typo for
2025-12-09 in the source's own byline, treated as ~7.5 months old, provisional**) scored Z-Image
5/5 on portrait realism and visual aesthetics across two portrait test cases, versus FLUX.2 Dev's
3-4/5 — but FLUX.2 Dev won decisively (5/5) on product-accuracy/branding fidelity, and neither
model reproduced a specific album cover correctly (Nano Banana Pro won that category). A
structured 5-prompt bake-off against Qwen-Image-2512 (dev.to, Garyvov, 2026-01-05) found Z-Image
applied "aesthetic smoothing" versus Qwen's literal grit, legible but less precise text, and
**declined to declare an overall winner** — the most methodologically careful of the comparison
articles found, and it still would not pick a winner.

**What practitioners praise**: speed (sub-second on datacenter GPUs, 8-step inference), skin/
portrait realism repeatedly described as beating FLUX.1, Qwen-Image, HiDream, and FLUX.2 Dev on
this specific axis; "HDR-like" contrast in wet/rain/skin detail scenes; genuine 12 GB-VRAM local
LoRA training success stories exist with real numbers, not just vendor claims — a GitHub issue
thread ([ostris/ai-toolkit #550](https://github.com/ostris/ai-toolkit/issues/550)) documents a
"Sharing Experience" 12 GB VRAM training run, and a Civitai practitioner article documents
**100+ trained ZIT LoRAs** (mostly anime) with concrete settings: 6-30 images, 2000 steps,
0.0001-0.0002 LR, ~12-18 minutes for a first pass on a mid-range GPU, 1-2 epochs recommended
before background memorization sets in past 3 epochs. This is the single most concrete,
first-person fine-tuning practitioner evidence found for *any* model in this report.
[Civitai ZIT anime LoRA training experience](https://civitai.com/articles/24472/z-image-turbo-zit-anime-lora-training-experience)

**What practitioners complain about**: a Hacker News thread on the model's release ([HN
46654814](https://news.ycombinator.com/item?id=46654814)) is the one place genuine dissent
surfaced rather than marketing-adjacent blog copy — one commenter stated Z-Image **"performs
worse than FLUX 2 and Qwen-Image across most metrics"** outside photography, and that it
**"quickly shows just how little it can do"** on non-photographic subjects; the same thread notes
weak NSFW-content training data causing anatomical inaccuracy in that specific use case. Separate
sources document hand/finger artifacts as a known, common issue, LoRA "overcooking" (oversaturated
artifacts) at weight 1.0, and weaker text rendering than Qwen-Image. **This directly contradicts
the marketing-flavored "punches above its weight" framing found elsewhere** — see Q5 below for
the full reconciliation.

**Fine-tuning verdict**: strong and well-evidenced, the best of the group by concreteness of
practitioner reports — but note a genuine tension in adoption-rate sourcing: one aggregator
(localaimaster.com, undated but recent) rates Z-Image's LoRA ecosystem 1/5 ("tiny"), while A3/R2
characterized it as "unusually fast" ecosystem uptake. Neither is simply wrong: **Civitai's
`z-image` tag carries 213 resources today**, accumulated in ~8 months since launch — a genuinely
respectable per-month rate, but a small absolute number next to Civitai's `flux` tag (2,072,
across FLUX.1+FLUX.2's longer combined lifespan) or `sdxl` (1,949, across 3 years). "Fast for its
age, small in absolute terms" is the honest read, not either extreme.

**Fitness for dark painterly game art**: **no direct evidence either way.** Every quality signal
found is photorealistic-portrait-specific. The one style-transfer test found (Art Nouveau/Mucha
illustration category in the Jan 2026 5-prompt benchmark) did not report a clear winner for that
specific category. Given the HN complaint that non-photographic subjects are its weak point, this
is a real, not merely theoretical, risk for painterly concept art — flagged prominently, not
buried.

---

## Qwen-Image (20.4B, Apache 2.0) — and the separate Qwen-Image 2.0 (7B)

**Quality evidence**: original 20.4B at 1058 Elo (rank 92) — tied with the much smaller FLUX.2
klein 4B. The separate, newer **Qwen-Image 2.0 (7B, Mar 2026)** scores higher, 1099 Elo (rank 67)
— Atlas Cloud's framing ("beating the giants") is about **this 7B model**, not the 20.4B
candidate A1/A3 verified — see the correction note in the leaderboard section above.

**What practitioners praise**: "exceptional prompt comprehension," most literal/instruction-
following of the group (a repeated, independently-corroborated finding: "cracks like dry earth"
followed strictly in the Jan 2026 benchmark; "remarkable fidelity to user instructions... without
deviation" per a dedicated strengths/weaknesses writeup); real dedicated depth ControlNets exist
and are usable today (InstantX genuine ControlNet, Image Union LoRA-based, DiffSynth model-
patching — three separate implementations, confirming A4's finding of a real depth path); LoRA
training process itself is reported smooth (AI-Toolkit, 400-image dataset, RTX 3090, 3,000 steps,
~4 hours, produced a working style LoRA).

**What practitioners complain about**: **"plastic skin"** is this report's most repeated,
independently cross-sourced complaint for any single model — two separate Hugging Face discussion
threads on a popular Qwen-Image-Edit checkpoint
([#270](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/discussions/270),
[#188](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/discussions/188)), plus two
independent YouTube "fix the plastic skin" tutorials, plus a direct quote that Reddit users call
it **"way too plastic most of the time."** This is community consensus, not one loud post. Second:
**low seed-to-seed variance** — "highly similar images across different random seeds," and
critically, **a trained LoRA did not fix this** in one direct practitioner account ("captured
style effectively but couldn't overcome the base model's poor seed variation"). Third: **tag
bleed** — in Danbooru-tag fine-tuning experiments, unwanted tags ("twintails," "maid outfit")
persisted in output even when absent from the prompt, attributed to Qwen's text encoder not
natively mapping niche vocabulary — an architectural issue, not a data-volume one. Fourth,
ControlNet-specific: a hands-on practitioner (Diffusion Doodles, **2025-09-16, ~10 months
old, provisional, predates Qwen-Image-2.0**) found the ecosystem "confusing" — not every published
"ControlNet" is architecturally a true ControlNet — and specifically flagged canny/edge control as
weak, overriding prompt instructions (e.g., carrying forward original lighting when the prompt
asked for a sunset). Depth control was the most reliable of the modes tested, which is the
specific mode this project needs.

**Fine-tuning verdict**: process is smooth per available reports, but the base model's own
aesthetic tendencies (plastic-skin uniformity, low seed variance) are reported to **survive**
LoRA training rather than being trainable away — a structural risk for a project whose whole
premise is breaking out of a generic "AI look" into a specific painterly register. 319 Civitai
resources in ~11 months (a slower per-month rate than Z-Image's).

**Fitness for dark painterly game art**: mixed signal. Its literalism/instruction-following is
a genuine asset for depth-reprojection accuracy (Q7). Its plastic-skin tendency is a genuine
liability for grimy, worn, candlelit material realism — "plastic" is close to the opposite of
"worn metal, cloth, stone." No painterly-specific test found either way.

---

## FLUX.2 [klein] 4B (Apache 2.0) and FLUX.2 [dev] (non-commercial, quality reference)

**Quality evidence**: FLUX.2 dev leads the whole open-weight candidate set at 1152 Elo (rank 35).
FLUX.2 klein sits well below it — one aggregator (ImageGPT Learn, undated) cites an internal
comparison putting **Dev at ~1143 and Klein 4B (distilled) at ~1070, a 73-point gap**, roughly
matching the AA leaderboard's own 1152-vs-1058 spread for the same pair. **This is a consistent,
independently-converging number across two different sources** — one of the few places in this
report where two sources actually agree on a specific magnitude.

**What practitioners praise**: klein 9B (non-commercial, not the shippable tier) is reported
"more consistent than Z-Image Turbo, provided you do not push it too far" on prompt adherence in
photorealistic contexts (Diffusion Doodles, 2026-01-22); klein's image-editing capability is
called out as a unique advantage for style-conversion tasks; the whole klein line is explicitly
positioned for rapid iteration/prototyping over maximum fidelity.

**What practitioners complain about**: the same Diffusion Doodles review states klein
"underperforms compared to larger models like Flux.1 Krea" specifically on artistic styles — a
direct, if single-sourced, signal against this project's painterly use case. Structurally, **the
distilled klein variants must run at CFG=1** — classifier-free guidance is disabled — which
removes a standard prompt-adherence tuning knob available on non-distilled models. FLUX.2 dev
itself carries a surprising, single-sourced complaint: "photorealism surprisingly weak... 'soft
and blurred' faces despite sharp, clean overall aesthetic" (Diffusion Doodles Model Rundown,
2026-01-06) — worth treating cautiously since it is one author's characterization and cuts against
dev's leaderboard-leading Elo, but flagged because it is specific and detailed, not vague.

**Fine-tuning verdict**: unchanged from A3 — klein 4B has the most vendor-mature, best-documented
official training pathway (BFL's own blog, ai-toolkit's recommended trainer) of any base in this
report, but that is a tooling-maturity finding, not a quality one; this pass found no new
practitioner LoRA-training write-ups for klein 4B specifically beyond what A3 already covered.

**Fitness for dark painterly game art**: klein 4B's raw quality is the weakest of the three
Apache-clean 2026-generation bases on the one comparable number (1058 Elo, tied with the full
20.4B Qwen-Image despite being 5x smaller — read positively as parameter-efficiency, or
negatively as "the ceiling is lower than the other options"). The one specific artistic-quality
complaint found (underperforming FLUX.1 Krea on artistic styles) points away from painterly
fitness, though it is single-sourced.

---

## SDXL 1.0 (incumbent baseline)

**Quality evidence**: 873 Elo (rank 132) — this pass found no new comparative testing beyond
confirming the existing leaderboard gap. It is not close: SDXL trails the next-weakest candidate
(FLUX.2 klein Base 4B, 965) by 92 points and trails the strongest open candidate (FLUX.2 dev,
1152) by 279 points — by a wide margin the largest quality gap in this entire report.

**What practitioners praise**: ecosystem depth, full stop. "The undisputed king of style breadth"
and "the workhorse ecosystem none of the newcomers can match" are recurring, consistent
characterizations across multiple sources (localaimaster, botmonster, thundercompute) — genuine,
repeated consensus, not a single opinion. Civitai's `sdxl` tag shows **1,949 resources** today
(one secondary source claimed "5,000+ LoRAs," not independently confirmed by direct tag-count in
this pass — treat 1,949 as the more reliable, directly-fetched number, and the 5,000+ figure as
possibly counting differently or as dated/inflated).

**What practitioners complain about**: lower prompt adherence than every 2025-2026-generation
model, weak native text rendering — neither of these is new information relative to A1/R2.

**Fine-tuning verdict**: unmatched maturity, zero quality ceiling — the project already knows
this trade-off from R2/A3; this pass adds nothing new except confirming the *magnitude* of the
quality gap is now larger than it may have appeared when SDXL was still a live frontier model.

**Fitness for dark painterly game art**: SDXL-era anime/illustration checkpoints and LoRAs are
genuinely abundant and painterly-capable — this is the one place where "ecosystem maturity"
plausibly compensates for base-model quality, since so much of SDXL's community output already
targets stylized/painterly registers rather than photorealism. Not independently re-tested here,
carried forward as a real (if secondhand) consideration.

---

## HiDream-I1 / HiDream-O1-Image (mentioned per brief instruction — comparisons name it repeatedly)

HiDream came up unprompted often enough in this pass to warrant inclusion, consistent with the
brief's instruction. **Quality evidence**: HiDream-O1-Image at 1111 Elo (rank 59) — ahead of both
Z-Image Turbo (1100) and Qwen-Image 2.0 (1099) on this snapshot, and one source
([WaveSpeed](https://wavespeed.ai/blog/posts/hidream-o1-image-dev-pixel-unified-transformer/))
claims it "wins every reported benchmark while being 7x smaller than FLUX.2 Dev" — this specific
"7x smaller" framing appears to conflate FLUX.2 dev's 32B with a possibly-inflated denominator
(the source text says "56B FLUX.2," which does not match FLUX.2 dev's confirmed 32B size from A3
— **treated as an unverified/likely-erroneous figure in the source**, not repeated as fact here).
Its rank-8-to-rank-59 fall over 2.5 months is the report's second demonstration of leaderboard
volatility (see top of report).

**What practitioners praise**: pixel-native architecture is credited with strong text rendering,
avoiding "historical failure modes where latent-space models collapse" on text; parity with or
superiority over the much larger 27B(sic)/20.4B Qwen-Image on several published metrics.

**What this pass adds beyond A3/A4**: nothing new on the licensing wrinkle (Llama-3.1 text
encoder) or the missing depth ControlNet — both already correctly flagged as open problems.

---

## Q6 — known failure modes and complaints, consolidated

| Model | Most-repeated complaint | Sourcing strength |
|---|---|---|
| Z-Image Turbo | Weak outside photographic/portrait subjects ("quickly shows how little it can do") | Single strong source (HN), echoed loosely elsewhere |
| Z-Image Turbo | Hand/finger anatomy artifacts | Multiple how-to/troubleshooting guides, consistent |
| Qwen-Image | "Plastic skin" | **Strongest cross-sourced complaint in this report** — 2 HF threads + 2 YouTube fixes + Reddit mentions |
| Qwen-Image | Low seed-to-seed variance, survives LoRA training | 2 independent practitioner sources |
| Qwen-Image | Tag bleed on niche/anime vocabulary | 1 detailed source, plausible mechanism given |
| Qwen-Image | Confusing/inconsistent ControlNet ecosystem, canny overrides prompt | 1 hands-on source, ~10 months old |
| FLUX.2 dev | "Soft and blurred" faces despite sharp overall aesthetic | 1 source, surprising given leaderboard rank — flagged as needing a second opinion |
| FLUX.2 klein | CFG=1 constraint on distilled variants limits prompt-adherence tuning | Structural/documented, not just opinion |
| FLUX.2 klein | Underperforms larger models (FLUX.1 Krea) on artistic styles | 1 source |
| SDXL | Weak prompt adherence, weak text rendering vs 2025-2026 models | Well-established, not new to this pass |

---

## Q7 — prompt adherence and control fidelity, direct answer

**Qwen-Image is the most consistently praised for literal instruction-following** across
independent sources ("exceptional prompt comprehension," strict adherence to specific descriptive
detail). Its ControlNet-depth path is real and used, though the wider ControlNet ecosystem around
it is inconsistent by implementation (some are LoRA-based patches, not true ControlNets) and canny
mode specifically has been reported to override prompt intent. **Z-Image's ControlNet-fidelity
claim (94% retained vs. 12-block models, 58% less VRAM) comes from a vendor/product page
(RunComfy), not an independent test — flagged as unverified marketing copy, not a measured
result.** FLUX.2 klein's CFG=1 constraint in distilled form is the one structural (not just
anecdotal) limitation found on prompt-adherence tunability. No source directly pitted all three
against each other on depth-ControlNet fidelity specifically using the same prompt/reference set —
this is a real gap (restated below).

---

## Where the evidence is thin

- **No painterly/illustrative/moody/dark-fantasy/concept-art-register comparison exists anywhere
  found in this pass, for any model.** Every comparison test set found targets photorealistic
  portraits, product photography, text/typography rendering, or general scene complexity. This is
  the single largest gap relative to what this project actually needs, and it is a blunt,
  plainly-stated absence, not a soft one. The one near-miss (an Art Nouveau/Mucha-style category
  in a 5-prompt benchmark) did not produce a clear verdict.
- **No material-specific test (worn metal, stone, cloth, candlelit interiors) exists.** What
  little material commentary was found is a byproduct of portrait/character reviews (skin,
  clothing incidentally mentioned), not a dedicated material-realism test.
- **Nothing genuinely current was found.** The freshest hands-on practitioner comparison located
  is dated 2026-01-05/06 (~6.5 months old); the bulk of useful qualitative content clusters
  Nov 2025-Jan 2026, around each model's launch window — predating Qwen-Image-2.0 (Mar 2026) and
  every recent leaderboard reshuffle. No comparison article published in the last ~3 months
  surfaced in repeated, varied searches.
- **FLUX.2 klein 4B specifically (the only Apache-clean, locally-trainable FLUX.2 tier per A3) is
  thinly covered on its own.** Most "klein" commentary treats the 4B/9B pair together or focuses
  on the 9B (which is non-commercially licensed and therefore not actually usable per A3) because
  9B scores higher and is what most reviewers reach for.
- **No same-dataset, same-steps, blind-judged LoRA training bake-off exists across bases.** Every
  fine-tuning report found is single-model; none compares training difficulty head-to-head under
  controlled conditions.
- **ControlNet-depth fidelity was never directly compared across models with the same reference
  image and prompt.** Each model's ControlNet assessment above comes from a different, independent
  hands-on account, not a shared test.
- **The candidate-list mismatch** (community attention is on Qwen-Image-2.0/7B, not the 20.4B
  A1/A3 verified) means a meaningful fraction of the "Qwen beats X" commentary found in this pass
  is technically about a different model than the one under evaluation — corrected for above, but
  worth restating as a standing gap if the project later swaps candidates.

## Sentiment vs. measurement

**Measured, with a number attached**: the AA Elo table (all rows); the FLUX.2 dev-vs-klein ~73-93
point gap (two independently-converging sources); Civitai resource-tag counts (213 z-image / 319
qwen / 1,949 sdxl / 2,072 flux, all directly fetched, not estimated); HF download counts for
Z-Image-Turbo-FP8 (91,114, one variant only).

**Pure sentiment, no number attached, and should be weighted accordingly**: "punches above its
weight" (Z-Image, echoed across several SEO-flavored blog posts using near-identical phrasing —
this reads like a marketing narrative that propagated across content-mill sites, not independently
arrived-at practitioner consensus); "aesthetic smoothing" vs. "literal and gritty" (Z-Image vs
Qwen, one benchmark author's own framing); "battle-worn aesthetic" material claims (FLUX.2 klein
9B, a single arena-compare tool's copy, likely partly auto-generated/promotional); "94% control
fidelity" (Z-Image ControlNet, a vendor product page, not an independent measurement).

**A specific, worth-flagging pattern**: one author, Chris Green ("Diffusion Doodles"), produced
several of this report's most detailed, most hands-on-sounding practitioner writeups (the Model
Rundown, the Qwen-Image ControlNets deep-dive, the FLUX.2 klein assessment). His work reads as
genuinely first-person and technically careful — but it is **one recurring voice, not independent
corroboration**, every time it appears alone across these sections. Treated accordingly above:
cited by name, not folded into "community consensus" language.

---

## Sources

- [Artificial Analysis — Text to Image Leaderboard, live fetch 2026-07-20](https://artificialanalysis.ai/image/leaderboard/text-to-image)
- [Artificial Analysis — Image Model Comparisons page, live fetch 2026-07-20](https://artificialanalysis.ai/image/models)
- [x.com/ArtificialAnlys — Z-Image Turbo #1 open-weight announcement, Nov 2025](https://x.com/ArtificialAnlys/status/2002839525609865575)
- [WaveSpeed — HiDream-O1-Image-Dev pixel-unified transformer, 2026-05-05](https://wavespeed.ai/blog/posts/hidream-o1-image-dev-pixel-unified-transformer/)
- [Hacker News — Z-Image discussion thread, item 46654814](https://news.ycombinator.com/item?id=46654814)
- [Medium/Diffusion Doodles (Chris Green) — Model Rundown: Z-Image Turbo, Qwen Image-2512, FLUX.2 Dev, 2026-01-06](https://medium.com/diffusion-doodles/model-rundown-z-image-turbo-qwen-image-2512-edit-2511-flux-2-dev-fc787f5e87ad)
- [Diffusion Doodles Substack — Qwen Image ControlNets, 2025-09-16 (provisional/dated)](https://diffusiondoodles.substack.com/p/qwen-image-controlnets)
- [Diffusion Doodles Substack — FLUX.2 Klein: Shrinking FLUX.2 Dev, 2026-01-22](https://diffusiondoodles.substack.com/p/flux2-klein-shrinking-flux2-dev)
- [Medium/302.AI — Z-Image Turbo vs FLUX.2 Dev, dated 2025-12-09](https://medium.com/@302.AI/z-image-turbo-vs-flux-2-dev-heres-what-we-found-e7a31327be40)
- [dev.to (Garyvov) — Qwen-Image-2512 vs Z-Image Turbo 5-Prompt Benchmark, 2026-01-05](https://dev.to/gary_yan_86eb77d35e0070f5/qwen-image-2512-vs-z-image-turbo-5-prompt-benchmark-which-model-is-better-5ni)
- [Medium (Koin AI) — Exploring Qwen-Image: Strengths, Weaknesses, and LoRA Limitations, 2025-08-22 (provisional/dated, pre-Qwen-Image-2.0)](https://medium.com/@koin7302/exploring-qwen-image-strengths-weaknesses-and-lora-limitations-332dac6a3500)
- [Civitai — Z-Image Turbo (ZIT) Anime LoRA Training Experience](https://civitai.com/articles/24472/z-image-turbo-zit-anime-lora-training-experience)
- [Civitai — Z-IMAGE as a Catalyst: Supercharging SD-1.5/SDXL, 2025-11-30](https://civitai.com/articles/23125/z-image-as-a-catalyst-a-new-way-to-supercharge-sd-15-and-sdxl)
- [GitHub — ostris/ai-toolkit issue #550, Z-Image LoRA on 12GB VRAM](https://github.com/ostris/ai-toolkit/issues/550)
- [Hugging Face — Qwen-Image-Edit-Rapid-AIO discussion #270, plastic skin](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/discussions/270)
- [Hugging Face — Qwen-Image-Edit-Rapid-AIO discussion #188, plastic skin](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/discussions/188)
- [Atlas Cloud — Qwen Image 2.0 vs FLUX.2, undated (2026)](https://www.atlascloud.ai/blog/guides/qwen-image-2-0-vs-flux-2-why-this-7b-model-is-beating-the-giants-in-ai-arena)
- [fal.ai — FLUX vs Qwen Image: What's the Difference?](https://fal.ai/learn/tools/flux-vs-qwen-image)
- [localaimaster.com — Best Local AI Image Models 2026: FLUX vs SDXL vs Qwen](https://localaimaster.com/blog/best-local-image-models-compared)
- [RunComfy — Z Image Turbo ControlNet product page (vendor-sourced fidelity claim)](https://www.runcomfy.com/models/tongyi-mai/z-image/turbo/controlnet/lora)
- [ImageGPT Learn — FLUX.2 Dev vs FLUX.2 Klein 4B Distilled comparison (Elo figures)](https://imagegpt.cloud/learn/compare/flux-2-dev-vs-flux-2-klein-4b-distilled)
- [Civitai tag: z-image (213 resources), live fetch 2026-07-20](https://civitai.com/tag/z-image)
- [Civitai tag: qwen (319 resources), live fetch 2026-07-20](https://civitai.com/tag/qwen)
- [Civitai tag: flux (2,072 resources), live fetch 2026-07-20](https://civitai.com/tag/flux)
- [Civitai tag: sdxl (1,949 resources), live fetch 2026-07-20](https://civitai.com/tag/sdxl)
- [z-image.ai — GLM-Image vs Flux vs Qwen comparison, 2026](https://z-image.ai/blog/glm-image-vs-flux-comparison-2026)
- [botmonster.com — Local Image Models 2026: Qwen vs FLUX vs SDXL on VRAM](https://botmonster.com/ai/best-local-image-generation-models-2026/)

---

## Unresolved / could not verify

- Whether the "5,000+ SDXL LoRAs on Civitai" figure (found in one aggregator source) reflects a
  different counting method than this pass's direct `sdxl` tag fetch (1,949) — not reconciled.
- The exact publish date of the 302.AI Z-Image-vs-FLUX.2-Dev Medium piece shows "2025-12-09" in
  one place in the fetched content but the source URL/byline context suggested possible
  inconsistency — treated as ~7.5 months old either way, not load-bearing to any conclusion.
- HiDream-O1's "7x smaller than FLUX.2" framing traces to a source figure of "56B FLUX.2," which
  does not match FLUX.2 dev's A3-confirmed 32B — likely a source error (possibly conflating with
  a different, un-identified comparison point), not resolved, not repeated as fact in this report.
- No source directly confirmed whether Qwen-Image-2.0 (7B) is genuinely open-weight/self-hostable
  versus a hosted-only "Pro"/"Max" tier naming overlap — treated as open per prior reporting
  (R2) but not independently re-confirmed with a license-file check in this pass (that
  verification, if wanted, belongs to a future A1/A3-style licensing pass, not this one).

---

# Verification pass (orchestrator, 2026-07-20)

## Corrected — Qwen-Image-2.0 is real, and unusable

The report flags "Qwen-Image-2.0 (7B, March 2026)" as the model current community buzz is
actually about, and suggests it may deserve its own pass. Checked directly:

- **No such repo exists on Hugging Face.** Enumerated the `Qwen` org: the only image models are
  `Qwen-Image`, `Qwen-Image-2512`, `Qwen-Image-Edit`, `-Edit-2509`, `-Edit-2511`.
- **`Qwen/Qwen-Image-2512` is not it.** Created 2025-12-30, and `safetensors.total` =
  **20,430,401,088** — byte-identical parameter count to the original `Qwen/Qwen-Image`. It is a
  December 2025 refresh of the same 20.4B architecture, not a 7B model. (Both Apache 2.0,
  both ungated — that much is unchanged.)
- **The 7B model does exist, but its weights are closed.** Released **2026-02-10** (not March),
  7B, currently #1 on AI Arena for both text-to-image and editing. Availability: **API-only,
  invitation testing on Alibaba Cloud BaiLian. The weights have not been open-sourced** — there
  is an open prediction market on whether they ever will be.

So Qwen-Image-2.0 is **disqualified outright**, and not on a close call: no weights means no
local LoRA training, no ControlNet, no self-hosted pipeline. It cannot be a base for a house
style under any budget. It should be recorded as blocked, not as a pending research item.

The agent's underlying observation was still valuable and correct in substance — the buzz it
was reading genuinely is about a different model than our candidate. It just landed on the
wrong conclusion about what that means for us.

## Could not verify

The **Artificial Analysis Elo figures** (Z-Image Turbo 1100, Qwen-Image 1058, FLUX.2 klein 4B
1058, SDXL trailing by 190–280) are the report's only hard numbers and I could not independently
confirm them — the leaderboard renders client-side and returns no scores to a plain fetch. They
are single-source, agent-fetched, and should be treated as indicative rather than established.
The report's discipline of quoting **score separately from rank** is right and worth keeping:
Z-Image's fall from rank 8 to rank 66 came from the field growing beneath it, not the model
changing.

---

# Gap-check pass

## The measurements we have are aimed at the wrong target

The report's blunt Q2 answer — *nothing anywhere tests painterly, illustrative, dark-fantasy, or
concept-art output; every comparison tests photorealistic portraits, product shots, and text
rendering* — is the most important line in it, and it undercuts its own quantitative section.
Arena Elo is a blind human preference aggregate, and that population overwhelmingly prompts for
photoreal people, products, and legible text. A model can win that population decisively and
still be mediocre at candlelit worn metal and Zurbarán-register chiaroscuro.

So the Elo table is not weak evidence because the numbers are shaky. It is weak evidence
because **it measures a different thing than this project needs**, and no amount of further
searching fixes that. Three passes' worth of quality research converge on the same wall.

## The one dissent points the wrong way, which raises the stakes

The single independent dissenting source on Z-Image (Hacker News) reports it as weak
**specifically outside photographic and portrait subjects**. If that holds, it is close to the
inverse of this project's requirement — and it sits directly against the leaderboard result that
makes Z-Image attractive. One post is not a finding, but the disagreement is precisely on the
axis we care about and cannot resolve by reading.

## Qwen-Image's most-cross-sourced complaint is a texture complaint

"Plastic skin" is the report's most independently corroborated practitioner claim (two HF
threads, two video fixes, Reddit), and one practitioner reports a trained LoRA **did not** fix
it. This matters more here than the phrase suggests: a base with a smoothing, waxy surface prior
is a bad foundation for a pipeline whose entire output is worn, grimy, tactile material. That is
a mechanism-level concern about a 20.4B model that also happens to be the one that does not fit
in 24 GB.

## Net position — and why this is the end of the research road

Consolidating A3, A4 and this pass, each base fails on a different axis:

| Base | Blocks on |
|---|---|
| FLUX.2 klein 4B | No depth control (A4) — hard blocker regardless of quality |
| Qwen-Image 20.4B | 40.9 GB; needs aggressive quant to train on 24 GB; waxy-surface prior |
| Qwen-Image-2.0 7B | Weights closed — disqualified |
| HiDream-I1 | No control tooling at all (A4) |
| Z-Image 6B | Best-shaped on every measured axis; quality on our register untested, one dissent |
| SDXL | Tooling unbeatable; ruled out on quality, and Elo now corroborates that |

**No further reading changes this table.** The remaining question is quality on dark painterly
material, the one thing nobody has benchmarked, and it is answerable in an afternoon with
hardware already on the desk. A5 as a *research* bullet is closed; A5 as a *generation* bullet
is the next action and needs a go-ahead.
