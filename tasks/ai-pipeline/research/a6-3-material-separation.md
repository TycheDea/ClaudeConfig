# A6.3 — Material separation

**Result: resolved. No Qwen trigger. The failure was a prompt confound.**

## What the view-stage failure actually was

Z-Image renders the candelabra's candle cylinders as **black iron cups** in the
front/back views and **cream wax candles** in the side views. The model is
resolving a genuine ambiguity — a cylinder on a candelabra is either a candle
or a candle cup — and resolving it differently per view, because the four views
are four fully independent generations (`seed * 100 + i`, no shared state).

## Two hypotheses, both wrong

**"The blend will wash it out."** The pipeline reprojects with facing weights
(`MV_WEIGHT_EXPONENT = 2.0`), so each texel is dominated by the view that sees
it most face-on, and view-space disagreement on grazing texels is discarded.
SDXL had the *worst* measured cross-view drift of any config (0.0367 vs
Z-Image's 0.0231) yet ships a clean asset, which made this plausible.

It is false. Running the full stage with Z-Image produced an asset whose
candles are **black** — the per-view failure survives the blend intact.

**"Z-Image's material separation has failed; revisit Qwen."** Also false, and
this is the one that nearly cost a base swap. That run used the generic
pipeline prompt, where the subject says `"melted wax candles"` — no colour.
The bake-off config that produced cream candles said `"**cream** wax candles"`.

Re-running with `"pale cream-white wax candles"` in the subject produces
correct, consistent material separation in the final asset: cream wax candles,
dark weathered iron, stone base. Comparable to the shipped SDXL asset — SDXL
carries slightly more melt-drip character, Z-Image slightly crisper ornament.

## The actual finding

**Z-Image requires material colours named explicitly in the subject string.**
SDXL at cfg 7 infers "wax ⇒ cream"; the cfg-1 distilled base does not. This is
an asset-authoring requirement, not a pipeline mechanism — the subject string
is the asset's own description, and naming the colour is legitimate authoring
rather than a workaround.

It composes with A5b's constraint (keep prompts short): name the *colour* of
each material, do not add clauses. `"pale cream-white wax candles,
near-black weathered dark iron, stone base"` is the shape that works.

## Correction to A6.1

The `candelabra-review` turntable renders show the shipped prop as bright
chrome, which looked like a visible `--mr zoned` failure. **It is not.** That
review renders under a bright neutral studio environment; under the game's
own HDRI (`evening_road_01_puresky_2k.hdr`) the shipped zoned MR, a uniform
`metallic 1`, and a uniform `dielectric` are all but indistinguishable — dark
weathered iron either way, because dark albedo at roughness 0.65–0.8 under a
dim dusk sky reads much the same whatever the metallic value.

A6.1's ruling stands on its real merits — it deletes four fragile constants,
an enum, a flag and a 1.4 MB texture — but its **visual** stakes were
overstated in that document, and the `metallic 1` choice for the candelabra is
visually near-neutral rather than a correction of something broken.

## Two regressions the swap exposed

Both were silent, and both are fixed:

1. `generate_views` recorded `manifest["seed"].get("8")` — a hardcoded sampler
   node id from the SDXL graph. Z-Image's sampler is node `11`, so **seed
   provenance silently became `null`**. Now records every node's resolved seed
   (`"seeds"`), which is workflow-agnostic.
2. `stats["strategy"]` was the literal `"sdxl_multiview_controlnet_depth"`,
   which the swap made a lie. Now `"multiview_controlnet_depth"`.

Stale SDXL references in the multiview path's comments and README were
corrected too. SDXL references elsewhere (concept, HDRI, materials) are
accurate and untouched — those stages still use it.

## A6.4 status

The swap itself is **done** — `workflows/prop_multiview.json` now carries the
Z-Image graph (UNETLoader + Fun ControlNet model patch + `ConditioningZeroOut`
for the inert negative, 8 steps, cfg 1), with the generic pipeline prompt
rather than the bake-off's candelabra-specific one. Verified end-to-end on the
candelabra: 4 views, `blend_coverage 0.674` (shipped SDXL: 0.6801).

Remaining under A6.4: regenerate the shipped props, and re-author their subject
strings to name material colours per the finding above.
