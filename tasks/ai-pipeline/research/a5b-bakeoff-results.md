# A5b — Base model bake-off: measured results

Run 2026-07-20. Harness: `scripts/ai-pipeline/bakeoff/run.py` (delete once the ruling lands).

**Method.** Same mesh (`content/models/props/candelabra_shrine/candelabra_shrine.glb`), same
four ortho depth maps rendered by the pipeline's own `mv_camera_rig` + `render_depth_views`,
same subject string and seed as the shipped candelabra, ComfyUI core nodes only. The only
variable is the image model. 12 generations total on the RTX 3080 Ti (12 GB).

Scored on **texture-fitness**, per the 2026-07-20 ruling — the texturing stage emit-bakes these
images straight into basecolor (`prop_texture.py:206`, "no lighting"), so flat unlit albedo is a
requirement and baked lighting is a defect, not a style choice.

## Wall time

| Model | Params | Weights on disk | Mean s/view |
|---|---|---|---|
| SDXL + xinsir depth (incumbent) | 2.6B | 6.9 GB | **15.1** |
| Z-Image Turbo + Fun CN Union | 6B | 12.3 GB bf16 | **15.1** |
| Qwen-Image + InstantX CN Union | 20.4B | 20.0 GB fp8 | **74.9** |

Z-Image matches SDXL's speed at 2.3× the parameters. Qwen is ~5× slower — but 75 s for a 20 GB
model on a 12 GB card is far better than the constant-weight-streaming penalty I predicted.

## Measured quality

Object texels only (masked by each view's own depth silhouette, so backgrounds are excluded —
the silhouette test discards them downstream anyway).

| Metric | SDXL | Z-Image | Qwen |
|---|---|---|---|
| **Cross-view RGB drift** (σ of mean colour across the 4 views; lower is better) | 0.0367 | 0.0254 | **0.0128** |
| **Cross-view luma range** | 0.1034 | 0.0648 | **0.0330** |
| **Warm cast** (mean R−B; baked candle glow leaking into albedo) | 0.0660 | **0.0260** | 0.0375 |
| Mean luma | 0.328 | 0.190 | 0.267 |

**The incumbent is worst on both axes that govern this stage.** Cross-view drift matters most:
`blend_views()` reprojects all four views into one shared UV atlas, so per-view colour
disagreement lands directly as visible seams. SDXL drifts ~3× more than Qwen — visible in the
contact sheet as candles going white in the front view and orange in the back, and the iron
shifting grey → bluish between views.

## Qualitative, from `contact_sheet.png`

- **SDXL** — excellent depth adherence, but lit flames with real glow spill onto the wax, and the
  worst cross-view colour agreement. Good wax/iron material separation.
- **Z-Image** — depth adherence at least as tight as SDXL, the flattest lighting of the three, and
  it nails "near-black weathered dark iron" where SDXL drifts to mid-grey. **But it collapses
  material separation**: the candles render as dark metal cups rather than wax, and the base
  drifts bronze in some views and black in others.
- **Qwen** — best of the three. Cream wax with melt drips, near-black iron, and a distinct grey
  *stone* base: all three materials from the subject string correctly separated, held consistently
  across all four views, with essentially no lighting baked onto the object.

## The finding nobody would have predicted from reading

**Z-Image's mean luma is 0.190 against SDXL's 0.328.** `--mr zoned` classifies metal by darkness
(`prop_texture.py:633`, smoothstep on basecolor value, "dark = metal"). A base that renders
everything near-black pushes far more texels across the metal threshold — the same failure that
forced `--mr dielectric` for characters, where dark robes and hair were turning to iron.

So model choice and the MR contract are coupled, and the coupling runs the wrong way: the model
that best matches the art direction's "near-black weathered iron" is the model most likely to
metalize wax and stone. Neither the model card, the licence, nor the arena Elo exposes this.

## Verdict

| | Depth | Flat albedo | Material separation | Cross-view consistency | Speed | LoRA-trainable on 24 GB |
|---|---|---|---|---|---|---|
| SDXL | ✔ | ✘ worst | ✔ | ✘ worst | ✔ | ✔ (huge ecosystem) |
| Z-Image | ✔ | ✔ best | ✘ collapses | ~ | ✔ | ✔ comfortably |
| Qwen | ✔ | ✔ | ✔ best | ✔ best | ✘ 5× | ~ needs 3-bit quant |

**SDXL is eliminated on measurement, not taste** — worst baked lighting and worst cross-view
drift, the two things this stage cannot tolerate.

The remaining choice is a genuine trade, not a ranking:

- **Qwen-Image** wins the image test outright — best material separation and 2× better cross-view
  consistency than anything else. Costs 5× the time, and A3 established it needs 24 GB plus 3-bit
  quantization to train a style LoRA at all.
- **Z-Image** is 5× faster, trains comfortably in 24 GB (ai-toolkit supports it, including the
  de-distilled `ostris/Z-Image-De-Turbo` training target), and produces the flattest albedo — but
  loses material separation, which is a texturing requirement rather than a preference.

**Open question this run cannot settle:** whether Z-Image's material collapse is the model or the
prompt. The prompt was written for SDXL and carries its negative-prompt lighting control, which is
inert at cfg 1. A prompt authored for Z-Image, naming wax and stone explicitly in the positive,
might close the whole gap — that is one 15-second generation to test, and it should be tested
before the base is chosen.

## Caveats

- One seed, one prop, four views. The metrics are consistent with the visual read but this is not
  a statistical result.
- Qwen ran at fp8, Z-Image at bf16 — Qwen is the more quantized of the two, so its win is if
  anything understated.
- Warm-cast and drift metrics use the depth silhouette as the mask, which includes the background
  showing through the candelabra's open frame; that biases all three models identically.

---

# Follow-up: testing the open question, and a reversal

The report above flagged one open question — whether Z-Image's material collapse was the model or
a prompt written for SDXL. Tested it (`wf_zimage_mat.json`): same base, same seed, same depth maps,
positive prompt rewritten for cfg-1 with materials named explicitly ("pale cream wax candles with
melted wax drips, near-black weathered wrought iron frame, grey stone base") plus "unlit candles,
no flames".

## Depth adherence, measured

Object texels painted **outside** the depth silhouette, as a fraction of background — the direct
measure of whether the model obeyed the geometry. Lower is better.

| Model | per view | mean | worst |
|---|---|---|---|
| **Z-Image (original prompt)** | 0.010 / 0.004 / 0.013 / 0.000 | **0.0067** | **0.0127** |
| Qwen-Image | 0.013 / 0.001 / 0.013 / 0.047 | 0.0182 | 0.0465 |
| SDXL | 0.122 / 0.110 / 0.049 / 0.005 | 0.0716 | 0.1224 |
| **Z-Image (material prompt)** | 0.010 / **0.328** / 0.085 / 0.115 | 0.1346 | 0.3280 |

## The reversal

**The prompt rewrite fixed the material collapse and destroyed depth adherence.** Materials did
separate correctly — cream wax, dark iron, grey stone, held across views — and cross-view drift
improved to 0.0128, exactly matching Qwen, with the best luma range of any run (0.0302). Mean luma
rose from 0.190 to 0.293, clearing the `--mr zoned` metalization risk.

But view 1 spilled **33% of the background**: it generated a five-candle curved candelabra that
ignores the narrow side-view silhouette entirely (visible in `contact_sheet_mat.png`, row 2 col 2,
against rows 1 and 3 which track it correctly). The longer, more prescriptive positive prompt
overpowered the ControlNet conditioning.

So my "fix" traded a texture defect for a geometry defect, and the geometry defect is worse:
wrong-shaped output cannot be reprojected at all, whereas a metalized wax texel is a wrong constant
in the MR map. **Z-Image can currently have correct materials or correct geometry, not both, at
ControlNet strength 1.0.** That is a tuning problem — prompt length, prompt weight, or a stronger
control signal — not necessarily a model limit, but it is unresolved.

Also: **"unlit candles, no flames" was ignored** — every view still has lit flames. Negation in the
positive prompt does not work, and at cfg 1 there is no negative prompt to put it in. This is a
concrete consequence of the cfg-1 finding: the pipeline's existing lighting control has no
equivalent on a distilled base.

## Two metric confounds, stated plainly

1. **Warm cast (R−B) cannot separate warm albedo from warm light.** `zimage_mat` scores 0.0738,
   worse than SDXL's 0.066 — but that is cream-coloured wax, not baked glow. The metric is only
   meaningful between runs with comparable palettes. Do not read it as a lighting score.
2. **Spill counts a dark background vignette as object spill.** SDXL's images carry a pronounced
   vignette, so its 0.0716 is likely inflated. The `zimage_mat` view-1 failure is independently
   confirmed by eye; SDXL's is not, and should be treated as an upper bound rather than a measurement.

## Standing after the follow-up

| | Depth adherence | Flat albedo | Material separation | Cross-view drift | s/view | LoRA on 24 GB |
|---|---|---|---|---|---|---|
| SDXL | 0.072 (poor, confounded) | worst — lit glow | good | 0.0367 worst | 15.1 | yes, huge ecosystem |
| Z-Image, orig prompt | **0.007 best** | best | **fails** — collapses to metal | 0.0254 | 15.1 | yes, comfortably |
| Z-Image, mat prompt | 0.135 **worst** | good | good | **0.0128** | 15.1 | yes, comfortably |
| Qwen-Image | 0.018 | good | **best** | **0.0128** | 74.9 | needs 3-bit quant |

**Qwen-Image is the only run that is simultaneously good on every axis.** It is 5× slower and the
hardest to fine-tune, but it did not fail anything.

**Z-Image remains the higher-upside option and the only one that trains comfortably**, but it needs
a prompt-vs-control balance that this run did not find. The next experiment is cheap and specific:
the material prompt at ControlNet strength 1.2–1.5, or the material list shortened to a few tokens.
Roughly 15 seconds per attempt.

---

# Resolving the prompt-vs-control tension (final)

Two more Z-Image configurations, 4 views each, ~15 s/view.

- **`zimage_s14`** — the long material prompt at ControlNet strength **1.4**.
- **`zimage_short`** — a short material cue ("cream wax candles, black iron, stone base") at
  strength 1.0.

| Config | Spill mean | Spill worst | Drift | Luma range | Mean luma |
|---|---|---|---|---|---|
| Z-Image, original prompt | **0.0067** | **0.0127** | 0.0254 | 0.0648 | 0.191 |
| Z-Image, material prompt | 0.1346 | 0.3280 | **0.0128** | **0.0302** | 0.293 |
| Z-Image, material @ str 1.4 | 0.0649 | 0.1414 | 0.0320 | 0.0877 | 0.239 |
| **Z-Image, short cue** | **0.0081** | **0.0110** | 0.0231 | 0.0602 | 0.207 |
| Qwen-Image | 0.0182 | 0.0465 | **0.0128** | 0.0330 | 0.266 |

## What resolved it

**Prompt length, not control strength.** Raising the ControlNet to 1.4 while keeping the long
prompt only partially recovered adherence (0.135 → 0.065, still 8× worse than baseline) *and*
made cross-view drift worse (0.0128 → 0.0320). Shortening the material cue instead restored
adherence completely — 0.0081 mean, 0.011 worst, the best of any run including Qwen.

So the failure was never the control signal being too weak; it was the positive prompt being long
and prescriptive enough to compete with it. Useful and non-obvious: on a cfg-1 distilled base,
**prompt verbosity trades directly against geometric fidelity**, and cranking ControlNet strength
is the wrong lever.

## But the material problem is only half fixed

`contact_sheet_short.png` (row 1 = `zimage_short`, row 2 = `qwen`): geometry now tracks the
silhouette in all four views. Materials do not resolve cleanly — some candles render cream, others
stay black metal, varying both within a single view and between views. Mean luma rose only 0.191 →
0.207, confirming numerically that most of the object is still reading near-black.

Qwen holds cream wax with melt drips, dark iron, and a stone base consistently across all four
views, at roughly half Z-Image's cross-view drift (0.0128 vs 0.0231).

## Ruling this run supports

**Qwen-Image is the measured winner on texture-fitness.** It is the only configuration tested that
is good on every axis simultaneously: adherence 0.018 (fine), drift 0.0128 (best), consistent
three-way material separation, minimal baked lighting.

**Z-Image is the better-shaped option that does not yet clear the bar.** It is 5× faster, the only
candidate that trains a style LoRA comfortably in 24 GB, and it posts the single best depth
adherence of any run — but its material separation is unreliable in a way two prompt revisions
improved without solving.

The two are close enough, and their trade-offs orthogonal enough, that this is a judgment call
rather than a measurement: Qwen buys texture quality today at 5× the generation time and a much
harder fine-tuning path; Z-Image buys speed and trainability against an unsolved material issue.

## Files

`target/base-bakeoff/` — depth maps, per-model views, `contact_sheet.png` (3-way),
`contact_sheet_mat.png`, `contact_sheet_short.png`, `timings.json`.

---

# RULING (user, 2026-07-20)

**Z-Image is the image base.** Trainability outranks today's texture quality: A3 established that
a trained house-style LoRA is the only durable route to a proprietary look, and Z-Image is the only
candidate that trains comfortably in 24 GB. Qwen-Image's 5× generation cost and 3-bit-quantized
training path make it the wrong foundation for the thing the pipeline actually needs to do.

**Qwen-Image is retained, not deleted** — weights stay on disk
(`qwen_image_fp8_e4m3fn.safetensors`, `qwen_2.5_vl_7b_fp8_scaled.safetensors`,
`qwen_image_vae.safetensors`, `Qwen-Image-InstantX-ControlNet-Union.safetensors`, ~32 GB) as the
documented fallback if Z-Image does not work out. It measurably wins texture-fitness today; the
ruling trades that for trainability, and that trade is reversible.

`scripts/ai-pipeline/bakeoff/` is therefore **kept, not deleted** — it is the harness that makes
the revisit cheap, and the metrics in this document are its baseline.

## Consequences to carry forward

1. **Z-Image's material separation is unresolved.** Candles render cream in some views and black
   metal in others. Two prompt revisions improved it without solving it. This is the known risk the
   ruling accepts, and the thing to watch: if it does not yield, that is the trigger to revisit Qwen.
2. **`--mr zoned` is now dangerous.** Z-Image's mean luma (0.191–0.207 vs SDXL's 0.331) pushes far
   more texels past the dark-equals-metal threshold (`prop_texture.py:633`). Either the threshold is
   retuned against Z-Image output, or props move to `--mr dielectric` like characters already did.
   Do not wire Z-Image in without settling this.
3. **Keep prompts short.** Prompt verbosity trades directly against geometric fidelity on this
   cfg-1 base; the short cue scored the best depth adherence of any run (0.0081). Raising ControlNet
   strength is the wrong lever — it made drift worse.
4. **The negative prompt is gone.** `prop_multiview.json` enforces flat lighting via its negative
   prompt, which is inert at cfg 1, and negation in the positive ("no flames") is ignored. Flat
   albedo needs a different mechanism on this base — unsolved.
5. **SDXL stays wired in until Z-Image replaces it.** `prop_multiview.json` still loads
   `sd_xl_base_1.0.safetensors`, and `content_lint.rs` hard-panics on shipped assets, so nothing
   is deleted before the swap lands.

## Cleanup now unblocked (Tier 1) — NOT yet executed, needs a go-ahead

With the base ruled, these have no remaining consumer: `flux1-schnell-fp8` (17.2 GB) +
`clip_l` + `t5xxl_fp8_e4m3fn` (~5.1 GB), and `sdxl_360_diffusion` (7.1 GB). ~29 GB.
SDXL itself and all Qwen weights are explicitly retained.
