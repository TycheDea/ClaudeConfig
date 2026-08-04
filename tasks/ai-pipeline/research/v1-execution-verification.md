# V1 — Execution verification round (2026-07-21)

Purpose: the A5b/A6 rulings were made on measurements; wrong execution would mean
wrong rulings (the F1 drape test already caught one metric blind to its failure
mode). This round re-derives every decision-bearing number independently and
re-checks every qualitative claim against the images, before the toolchain is
declared settled.

## Reproduced clean

| Claim | Doc | Re-check | Verdict |
|---|---|---|---|
| A6.2 baked fractions (sdxl / nolight / short / dramatic) | 0.011 / 0.014 / 0.014 / 0.018 | identical, `metrics.py` re-run | exact |
| A6.2 positive control | 0.330 | 0.330 (re-rendered `lit_control.py`) | exact |
| A6.2 mesh-identity IoU | 0.955 | 0.955 | exact |
| A5b cross-view drift (sdxl/zimage/qwen/short) | .0367/.0254/.0128/.0231 | .0367/.0254/.0127/.0231, independent reimplementation | exact |
| A5b warm cast / luma range / mean luma | — | match to 2–3 decimals | pass |
| A6.1 Otsu threshold + separability, all 4 bases | e.g. 0.490/0.751 | identical to 3 decimals | exact |
| A6.1 metal %, p10/p50/p90 | 57.9–81.4% | within 1–2 pts (per-view vs pooled averaging) | pass |
| Z-Image collapse / Qwen consistency / `zimage_short` half-fix / `zimage_mat` geometry loss | prose | confirmed by eye on the contact sheets | pass |
| A6.3 colour-naming fix | "resolved" | both full-stage runs recovered from ComfyUI's retained outputs: generic prompt → black candles in all views; "pale cream-white wax" → cream in all four | real |

Adversarial variant: scoring the positive control against the *bake-off's* depth
normals instead of its own drops it 0.330 → 0.156 — still 8–14× above every
generated view, so A6.2's null survives even a misaligned-normals assumption.

## Corrections to the record

- **SDXL's "good material separation" (A5b) was generous.** Its view 2 has black
  candles too — the same per-view flip Z-Image was faulted for, milder. The shipped
  SDXL asset won its separation partly through blend luck. No ruling changes (SDXL
  lost on drift and baked lighting), but colour-naming in subjects is best treated
  as a base-agnostic authoring rule, not a Z-Image accommodation.
- **"Grey stone base" in the A6.3 fix run is not confirmed.** The base reads dark
  bronze in every view; wax-vs-iron separates, the third material does not clearly.
- A6.4's `blend_coverage 0.674` could not be re-verified: no artifact survives.

## Process findings

1. **Verification artifacts were not preserved.** The A6.3/A6.4 full-stage runs
   left no GLB, no blend output, no stage dirs; the raw views were recoverable only
   because ComfyUI's own output folder retains copies. A verification run whose
   evidence is deleted is prose, not verification — keep the outputs of any run a
   ruling cites, or point the doc at the retained ComfyUI copies.
2. **Decision-bearing metrics were ad-hoc, uncommitted scripts.** The drift/luma
   numbers that eliminated SDXL were unreproducible from committed code. Fixed:
   `metrics.py` now prints drift and luma-range columns alongside baked fraction,
   and reproduces the recorded baseline exactly. (A6.1's zoning/Otsu forensics are
   deliberately *not* committed — the mechanism they measured is retired.)
3. **Every ruling rested on n=1** (one seed, one subject). The docs say so, but two
   authoring *rules* were generalized from that sample: "name material colours" and
   "prompt verbosity trades against geometry". Closed by the robustness batch below.

## Robustness batch (run 2026-07-21, `target/robustness/`)

`run.py` gained `--seed`, `--subject`, `--materials` (the colour cue moved from
`wf_zimage_short.json` into a `{materials}` placeholder; the default reproduces the
recorded prompt byte-identically). Six configs, 4 views each, Z-Image only.

| Config | baked | drift | separation (by eye) |
|---|---|---|---|
| cand seed 2 (baseline) | 0.014 | 0.0231 | mixed within/between views |
| cand seed 7 | 0.007 | 0.0188 | **fails** views 1, 3 (black candles) |
| cand seed 13 | 0.005 | 0.0341 | mixed within views |
| cand seed 42 | 0.019 | 0.0220 | **fails** most views |
| cand "deep crimson red wax" | 0.036 | 0.0197 | **4/4 clean** — crimson everywhere |
| trunk seed 2 | 0.009 | 0.0281 | wood/bark consistent; boundary height wanders |
| trunk seed 7 | 0.016 | 0.0599 | wood/bark consistent; boundary wanders more |

### What this settles

1. **Colour-naming is causal, and it generalizes.** "Deep crimson red wax" binds in
   all four views; on a second mesh, "pale sun-bleached grey wood, dark brown bark"
   assigns both materials consistently at both seeds. The A6.3 rule survives its
   intervention test.
2. **But weak colour words are not seed-robust.** "Cream" flips to black under 3 of
   4 seeds — A6.3's clean full-stage run (which used the stronger "pale cream-white
   wax candles") sits on a phrasing/seed combination this batch shows is not
   guaranteed. The rule refines to: **name a strong, unambiguous colour per
   material**, and treat per-view separation as a reviewed gate per asset, not a
   solved property.
3. **The failure mode is geometric ambiguity.** Candle-vs-iron-cup is a genuine
   two-reading shape; the trunk offers no such ambiguity and never flips. Props
   whose silhouette affords two material readings are the risk class.
4. **Flat albedo is fully confirmed** — 24 new views, max 0.036 vs the 0.330
   control. A6.2's null holds at n=28.
5. **Z-Image's drift advantage is seed-variable** (0.019–0.034 on the candelabra;
   0.060 on the trunk via boundary wander). Qwen's recorded 0.0128 beats every
   Z-Image seed observed. This does not touch the trainability ruling, but the
   Qwen-revisit trigger should watch seam quality on regenerated props, not assume
   the bake-off's seed-2 drift number.

### Standing of the rulings after this round

- **A5b (Z-Image base)** — stands. Evidence base reproduced; the ruling's known
  risk is now quantified rather than anecdotal, and the style-LoRA phase is itself
  the next test of whether training stabilizes material binding.
- **A6.1 (zoning retired)** — stands; forensics reproduced exactly.
- **A6.2 (no flat-lighting mechanism needed)** — strengthened (n=4 → n=28).
- **A6.3 (colour naming)** — refined as above; "resolved" was too strong, "causal
  and necessary, not sufficient per-seed" is accurate.
- **A6.4 remainder** — proceed, with strong colour words in each re-authored
  subject and per-asset turntable review as the separation gate.
