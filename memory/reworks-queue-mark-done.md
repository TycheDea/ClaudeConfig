---
name: reworks-queue-mark-done
description: "After a rework's plan steps are all committed, always update the reworks file's cross-type queue note to mark it done"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8246bce-3b07-4b7a-986c-d3e802f2dca4
---

When the last step of a rework's plan is committed, immediately update the reworks report's cross-type queue note (e.g. `docs/reviews/reworks-networking.md` "## Findings (implementation order)") to strike the rework out and record the plan filename. Don't offer — just do it, then include it in the same commit or the response.

**Why:** User said "yes always update" when I offered to mark reworks 8 and 10 done; the queue note is the single source of truth for what remains.

**How to apply:** Strike the number in the queue line (`~~8~~`) and append a "done (plan-file, N steps)" line under it. Related: [[finding-review-alignment-only]].

**A strike inherits its subject's pending gate:** never strike an item Done — or record "premise re-checked and survives" — while the mechanism its premise lives on has a settling measurement pending in the same queue. If a queued measurement can still eliminate the mechanism, record the item as **blocked on that gate**, named explicitly, and strike only after the gate settles; "Done" launders the provisionality out of the queue note. Items independent of the mechanism's survival, and instrumentation the gate itself needs, are exempt (they may land, just not be struck Done early).
