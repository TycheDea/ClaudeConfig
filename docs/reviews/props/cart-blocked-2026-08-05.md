# H6 cart — BLOCKED at 3/3 v2 FAILs; gate vindicated by attribution (2026-08-05)

Chain: `gen_prop.py --asset cart`, concept `concept-c1/C5/seed_6` (ruled
winner; spoked wheels informational under the standing ruling). Per-roll
pre-screen v2 `--body dark` (open_dark FAIL >3.5%), albedo = blend-stage
`base.png`, persisted per cand as `pre_screen_v2.txt` under
`target/prop-batch/h6-cart/`.

| seed | p95/p5 | dark_frac | dark_open_frac | open_dark | verdict |
|---|---|---|---|---|---|
| 6 | 14.64 | 16.4% | 0.433 | 7.11% | FAIL |
| 7 | 13.78 | 18.4% | 0.412 | 7.57% | FAIL |
| 8 | 27.55 | 20.3% | 0.457 | 9.26% | FAIL |

All ~2–2.6× over the line; no ESCALATE reached. Protocol: 3 FAILs =
BLOCKED.

## Attribution before accepting the block

Hypothesis tested (a-number-is-not-the-thing: metric must not count spec'd
content as defect): the cart is spec'd two-tone (near-black wood + pale
sacks) — do the sacks dislocate the median so the whole spec'd wood body
counts as "dark"?

**Refuted** (`target/prop-batch/h6-cart/dark_probe/`): the pale mode
(sacks) holds only 12.8% of island mass (valley at luma 0.58); the median
0.282 sits inside the wood mode — the generated wood body is silvery-grey/
mid-brown, not the spec'd near-black. Flagged dark texels are a distinct
near-black tail (p50 luma 0.077 vs body 0.282) concentrated at plank
junctions, wheel hubs, under-sack contacts, and panel edges — with 41–46%
on open (AO-above-median) surfaces. That is painted contact shadow on lit
surfaces: the ghost defect itself, on the recess-densest prop in the queue.

## Disposition

- Cart BLOCKED; registry entry reverted from `assets.json` (re-add
  verbatim from the record above if unblocked). Concept + roll artifacts
  stay on disk.
- Consistent with the structural remainder recorded at v2 delivery:
  spec'd-dark + recess-dense is hostile to per-view generation → fix
  class 4 (texture-native generation), licensing decision user-owned.
  The cart re-rolls only after that fix class lands.
- The worsening trend across seeds (7.11 → 7.57 → 9.26%) is seed variance
  inside a structurally hostile prop, not instrument drift.
