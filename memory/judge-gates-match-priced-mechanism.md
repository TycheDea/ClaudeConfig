---
name: judge-gates-match-priced-mechanism
description: "Fires when pre-registering a judge/gate criterion for a fix or rebuild — the criterion must be what the chosen, priced mechanism can deliver, not the defect's headline description."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a38eccbe-e253-4073-8a05-baa0bd7d9b10
  modified: 2026-08-05T12:53:25.527Z
---

A gate criterion phrased as "defect X dead" fails honest fixes when the
approved mechanism was never priced to kill all of X. Anchor the gate to
the mechanism's deliverable (with the physics bound stated), and list the
out-of-band remainder as a separate check on its own channel.

**Why:** chapel_arch retess round 1 (artifact:
`docs/reviews/town/arch-retess-round1-2026-08-05.md`, ClaudeConfig; gate
FAIL 5/9/3/5): the dispatch asked "rule the melted-carving defect dead at
4–17 mm", but the study (§8, `decimation-attribution-2026-08-01.md`) had
priced 20 mm footprint at ~683k tris and deliberately chosen 40 mm — a
mesh that can never geometry-carry 4–17 mm (that band is normal-map
territory). The judge's own data showed the mechanism delivered exactly
what was priced (1–5 cm band up 2.4–2.6×); the criterion, not the fix,
produced half the FAIL. The other half (texture ghost) was the real
blocker.

**How to apply:** before dispatching a judge on a fix, re-read the
prescription's own cost/coverage pricing; write the gate as "mechanism
delivered its priced band" + "no regression elsewhere". A Nyquist/physics
bound (e.g. geometry floor ≈ 2× footprint) is a two-line check — do it at
gate-writing time, not after the FAIL. Related: [[a-number-is-not-the-thing]],
[[checks-must-fail-when-broken]].
