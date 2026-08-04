---
name: synthetic-cannot-validate-real
description: Synthetic input cannot validate a premise about real input — test the premise on a real artifact already on disk, as step 1, before building
metadata:
  type: feedback
---

Fires when a fix rests on a structural property of the input data (enclosed, sealed, connected, monotone) tested only against inputs built by the same reasoning; at plan time when ordering steps; when citing a prior commit's "measured validation"; when a self-test's fixture could have been authored by the code under test.

**Why:** two full rounds and a GPU regeneration were built on "the interior is an enclosed region" — a ten-case analytic-SDF battery passed exactly, and the shipped mesh (one fused component carrying both walls, three minutes of CPU to check, on disk the whole time) falsified the premise outright; a metrics camera baked a Z-up assumption, passed exact self-tests on self-authored boxes, and rendered a gothic arch as a squat slab — "camera math is a property of the code" was a claim about which frame real glTF bytes arrive in, which is data.

**How to apply:**
- Name the premise as a testable proposition about real data; find the cheapest test on an artifact already on disk; run it before the fix. Position, not cost, is the criterion — a premise check scheduled after implementation steps is the failure itself.
- Synthetic green proves the code does what it says, never that what it says is what the data needs. Report those as two different states.
- Self-test fixtures come from the real producer (an artifact off the pipeline), or they verify internal consistency only — a fixture the consumer could have written shares its conventions and cannot catch a frame/unit/channel/winding mismatch.
- A fix that fails safe is indistinguishable from one that never ran; verify execution and effect independently.
- General form — any fact guessed rather than fetched — is enforced by the global CLAUDE.md "get the fact before planning around it" rule.
