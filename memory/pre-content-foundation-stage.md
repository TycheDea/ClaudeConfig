---
name: pre-content-foundation-stage
description: Vordar is pre-content (no real enemies/NPCs yet) — benchmarks exist to harden foundations BEFORE gameplay code accumulates on them
metadata: 
  node_type: memory
  type: project
  originSessionId: c769a8ca-05d9-4352-a6f0-44cee00a7a34
---

The game has no real enemies or NPCs — only test/synthetic
entities. The benchmark suite (benchmarks/, docs/benchmarks/BASELINE.md) was
built to expose structural weak points so they can be fixed while little code
sits on top of them, not to validate current load.

**Why:** The user explicitly said: "the game is not finished... I only wanted
to know what are the weakpoints so I work with them before having a lot of
code on top of them."

**How to apply:** The ranked weak-points list is committed at
`docs/benchmarks/WEAKPOINTS.md` (5 items: world.get-in-loops idiom, O(E·P)
enemy targeting, snapshot fan-out on the sim thread, reliable-stream
snapshots, dense-cell broadphase) plus a "gaps to close" section (prefab-spawn
RON parse at combat rate — suspected foul; client netcode benches; packet-loss
check; long-run growth soak) — start there when the user resumes foundation
work. Frame performance findings as fix-now-vs-defer based on how
much future code will build on the pattern, not on whether current load fits
the budget. Structural items (per-mechanism costs, access patterns like
world.get-in-loops, sim-thread/snapshot coupling, targeting model) matter now;
load-dependent tuning can wait for real content. See [[serious-project-not-learning]]
and [[dev-singleplayer-pack]].
