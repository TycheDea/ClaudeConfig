---
name: incumbent-tools-not-gates
description: No current pipeline tool (e.g. Mixamo) is a hard requirement when evaluating alternatives — judge toolchains on end-to-end outcome
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 03a50bbf-9098-4b68-a967-a2e05f9f1745
  modified: 2026-07-23T14:35:02.398Z
---

Ruled during the repo-study A1 (UniRig) evaluation: do NOT discard a
candidate tool because it is incompatible with an incumbent (the trigger was
rejecting on "no Mixamo-compatible skeleton"). No tool currently in the pipeline is
a must; if another path with other tools gives a better end-to-end outcome, we
switch paths.

**Why:** the pipeline is pre-content and every stage is replaceable; gating on the
incumbent silently locks in today's choices.

**How to apply:** in adopt/reject evaluations, treat incumbent-compatibility as a
*cost to price in* (e.g. "adopting X also means re-solving animation sourcing"),
never as a disqualifier. Verdicts compare whole toolchains by outcome. See
[[strict-nc-tooling-ruling]] for the one true gate (licensing).
