# showcase VFX pack — triage

120 candidates generated (16 slots, Z-Image Turbo, 1024², one ComfyUI session,
1175 s). **No atlas was shipped.** At vfx_post's defaults 0 of 120 candidates
pass its gates, and the one control vfx_post exposes cannot be set to a value
that is defensible across the pack. Details below; the candidates and their 120
gate reports are staged here for whatever fix lands.

## Blocker: the void floor vs. the border gate

Z-Image decodes onto a photographic void, not a mathematical one. Across all
120 candidates the outer 2 px band carries a floor of ~1.5/255 mean with
excursions to 3-10/255. `vfx_post`'s clip and border gates require < 2/255.
Framing is not the cause — it was fixed first (run 1 put ~50 % of the canvas
under the element and clipped outright; the reframed run holds elements to
2-18 % coverage, and the failures that remain are 3-8/255 edge maxima, i.e. the
floor, not content).

`vfx_post` can only subtract a **percentile** of the whole image. What that
costs depends on how much of the frame the element covers, so one percentile is
many different operations:

| black point | passes | subtracted level across candidates | slots with no passer |
|---|---|---|---|
| p0.5 (default) | 0/120 | 0.0–5.2/255 | 16 |
| p90 | 28/120 | 1.8–**245.6**/255 | 9 |
| p95 | 46/120 | 3.0–**250.8**/255 | 5 |
| p99 | 97/120 | 4.2–**252.0**/255 | 0 |

At p95 a sparse spark loses 3/255 (harmless) while a smoke puff loses 91/255 —
the puff's whole body. The pass rate climbs monotonically with the percentile
and never plateaus, because what is being bought is not a cleaner void but a
deleted element: the knob is being tuned against the gate that grades it.

The defect is that the floor is an **absolute** level and the control is a
relative one. Subtracting a fixed 8/255 instead passes 48/120 across 15 of 16
slots while keeping 88 % of mid-tone content; 10/255 passes 64/120 keeping 85 %.
`vfx_post` has no way to express that.

Reproduce both tables: `python scripts/ai-pipeline/assets/vfx/showcase/void_floor_sweep.py`
(recorded output in `void_floor_sweep.txt`).

**Decision needed** (out of this contract's scope — it changes what "passed
vfx_post" means for every pack): give `vfx_post` an absolute black level, with
the level calibrated once against the decoder's own noise floor on a control
render rather than against any candidate's border band.

## Per-slot content verdict

Content quality is independent of the blocker above and is broadly good; these
notes are for the re-roll pass.

| slot | candidates | content verdict |
|---|---|---|
| pyro_ember | 3 | good — sparkler burst, crisp rays, well contained |
| pyro_flash | 3 | good — dense incandescent burst, very bright |
| pyro_smoke | 24 | off-brief — thin curling plumes with a stem, not a rolling puff; also indistinguishable from censer_smoke |
| wisp_soft | 3 | good — soft radial orb |
| wisp_streak | 3 | good comet streaks; 2 of 3 run off the top edge |
| wisp_flame | 24 | contaminated — a candle body and wick base render with the flame; also too tall for the frame |
| sigil_glyph_a | 3 | excellent — concentric ring mandalas, abstract, crisp |
| sigil_glyph_b | 3 | **rejected** — "interlocking triangles" produced a hexagram (a real religious symbol); the other two are a plain triangle-in-circle. Re-prompt without interlocking triangles |
| sigil_glyph_c | 3 | excellent — rosette lattice, abstract, crisp |
| sigil_spark | 3 | acceptable, but near-duplicate of shard_twinkle |
| censer_haze | 3 | off-brief — a glowing orb, not a thin broad veil; duplicates wisp_soft |
| censer_mote | 3 | good — tiny mote with faint halo |
| censer_smoke | 24 | on-brief column, but the stem reaches the frame edge on most seeds |
| shard_sliver | 3 | good — faceted crystal shard, crisp specular |
| shard_flare | 3 | good — clean star flare |
| shard_twinkle | 12 | acceptable — tiny four-point glint, very plain |

Prompt fixes for the re-roll, beyond the framing clause already in place:
flame without a candle or wick; haze as a broad veil rather than an orb;
pyro_smoke as a compact puff distinct from censer_smoke's column; shorter
vertical extent on censer_smoke, wisp_streak and wisp_flame; sigil_glyph_b
re-prompted away from interlocking triangles.

## Toolchain change made

`vfx_atlas_pack.py` gained `--cell-size N`: post outputs are 1024² and showcase
cells are 256, and `load_cell` previously only validated sizes. Square inputs
are Lanczos-resampled to N; without the flag the old refusal on a size mismatch
is unchanged. Covered by two tests in `test_vfx_atlas_pack.py`, one of them
byte-exact against Pillow's Lanczos so a nearest/bilinear regression fails.
