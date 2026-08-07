---
name: claude-seat-mapping
description: Fires whenever dispatching Sol/Terra/Luna seats from a Claude Code session — which Claude model each seat maps to
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 63c2f974-ab1f-426c-b675-702b9fbe1405
  modified: 2026-08-07T10:35:10.166Z
---

User ruling (2026-08-07): in Claude Code sessions the seat ladder shifts up one class now that Fable tops it — **Sol → Fable, Terra → Opus, Luna → Sonnet**. Haiku is off the ladder.

**Why:** the old mapping (Sonnet=Terra, Haiku=Luna) predates the Claude 5 family; per [[model-rules-expire-with-the-model]] tier-capability rules die on upgrade.

**How to apply:** Agent tool `model` param — Sol seats `fable` (or inherit), Terra `opus`, Luna `sonnet`. Roles and gates unchanged ([[orchestration-model]]).
