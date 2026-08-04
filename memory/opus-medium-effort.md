---
name: opus-medium-effort
description: Opus agents may run up to high effort — never xhigh or max
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5a202ec3-bb7c-40b2-b00e-426ccfd983ce
  modified: 2026-07-25T08:41:41.165Z
---

Opus may run at **medium or high** effort, never xhigh/max. Original medium-only
cap set after the user stopped an Opus planning agent mid-run; later raised to
allow high.

**Why:** Opus still overthinks at the top tiers, but the user's judgement is that
high is within the useful range — only xhigh/max degrade the output.

**How to apply:** let Opus agents inherit the session effort; raising to high is
fine when the task needs the depth, but never go above it. This is about Opus
specifically; it does not change routing for other tiers.
See [[orchestration-model]].
