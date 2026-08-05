---
name: numeric-outcome-weights
description: "Fires whenever options are presented to the user (AskUserQuestion, plan forks, decided-while-unsure lists): outcome/confidence weights must be numbers and context-agnostic"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a38eccbe-e253-4073-8a05-baa0bd7d9b10
  modified: 2026-08-05T11:07:00.553Z
---

Every option presented to the user carries its weights as **numbers, readable without domain knowledge**: outcome /10, confidence /10, cost in concrete units (wall-clock, GPU minutes, tokens). A prose description that requires understanding the topic to compare ("kills the sliver strips, cuts every box to 12 tris") is not an outcome qualification — it is supporting detail that may follow the numbers, never replace them.

**Why:** the user is not the one coding; they ruled twice on 2026-08-05 — "outcome should be a number not a description that requires knowledge about the topic" and "make sure future outcome qualifications are numbered and context agnostic" — after a kit-bevel fork was offered with descriptive-only weights.

**How to apply:** extends CLAUDE.md §6's three-independent-weights rule; the three weights stay independent and unmerged, and each is stated numerically first, with at most one plain-language sentence of support. Applies to AskUserQuestion options, plan-file forks left to the user, and checkpoint "decided while unsure" items.
