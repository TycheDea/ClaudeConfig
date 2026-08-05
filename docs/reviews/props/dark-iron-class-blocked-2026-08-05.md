# H7 votive BLOCKED; brazier withheld — spec'd-dark class closed to per-view generation (2026-08-05)

Companion to `cart-blocked-2026-08-05.md`; same protocol, same attribution
discipline.

## H7 votive stand (asset `candelabra_shrine`, concept C6/seed_4)

| seed | p95/p5 | dark_frac | dark_open_frac | open_dark | verdict |
|---|---|---|---|---|---|
| 4 | 17.32 | 16.8% | 0.531 | 8.89% | FAIL |
| 5 | 23.35 | 20.6% | 0.485 | 9.98% | FAIL |
| 6 | 25.13 | 18.1% | 0.609 | 11.00% | FAIL |

3/3 FAIL = BLOCKED. Chains clean, artifacts + per-roll `pre_screen_v2.txt`
under `target/prop-batch/h7-votive/`.

**Attribution (pre-registered for this prop because its body is spec'd
matte-black iron):** probe on cand_4 (`dark_flag_cand_4.png`, script =
`target/prop-batch/h6-cart/dark_probe/cart_dark_probe.py`): the generated
body is charcoal (median 0.219, deciles 0.07–0.33) and sits ABOVE the dark
threshold 0.099 — the gate is not counting the spec'd body. The flagged
near-black (p50 0.068) is a patchy tail at member edges, junctions, and
the tray around the candle holes, with 49–61% on open surfaces; the atlas
additionally shows baked specular sheen on the post members — view-baked
shading in the albedo of matte iron. Calibration point: the shipped
candelabra ghost (same material family) scores 3.47%; these rolls are
2.5–3× a known ghost. Gate vindicated; genuine ghosting.

## Brazier (gate_brazier, C8/seed_407) — WITHHELD, not rolled

Decided-while-unsure, on attribution: the brazier is the extreme member of
the class both blocks just closed — matte black wrought iron, deep round
openwork basket (maximal recess density). Cart 7.1–9.3%, votive 8.9–11.0%,
mechanism confirmed by probe on both; a third 3/3 block at ~20 min GPU + 3
texture rolls buys no new information. Precedent: ~75 min withheld at
era-attribution. The user can order the roll anyway; concept
`concept-c1b/C8/seed_407` and the registry-entry text (in
`tasks/todo.md` item 20 and `p31-c1-concepts.md:522`) stand ready.

## Registry unwound (nothing from this class ships now)

- `candelabra_shrine.subject` reverted to the shipped five-candle string
  (the C6 votive subject is preserved verbatim in this record's companion
  concept manifest and todo item 20; re-apply on unblock).
- `gate_brazier` entry removed (re-add verbatim from todo item 20 /
  spec line 522 on unblock).
- Apse + chapel placements keep the shipped candelabra_shrine glb —
  status quo, the known fix-class-4 backlog item.

## S5 queue — final disposition

| chain | state |
|---|---|
| H3 retablo | cand_1 + cand_3 v2 PASS → G3 (cand_2 ESCALATE, judge-only) |
| H4 shrine | s203 + s501 v2 PASS → G3 |
| H6 cart | BLOCKED (3/3, attributed) |
| H7 votive | BLOCKED (3/3, attributed) |
| brazier | WITHHELD on attribution |

The pattern across both blocks: spec'd-dark + recess-dense props are
structurally hostile to per-view generation — every junction/contact gets
its shading painted into albedo, and dark bodies give the blender no
contrast headroom to reject it. Fix class 4 (texture-native generation) is
the unlock; licensing decision is the user's. Until then, dark
recess-dense subjects should not enter the S5 queue.
