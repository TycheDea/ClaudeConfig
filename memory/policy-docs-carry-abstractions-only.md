---
name: policy-docs-carry-abstractions-only
description: Policy/directive docs carry only abstractions — no numbers, code identifiers, roadmap tags, or facts that merely justify a directive
metadata:
  type: feedback
---

Fires when writing or pruning a doc whose job is to orient policy — design directives, CLAUDE.md-style rules, conventions pages.

**Why:** asked to clean DESIGN.md to short directives, I removed history but kept supporting facts ("cast times dwarf network latency"), roadmap tags, and code identifiers; user corrected — erase everything that adds nothing: abstractions, not specifics.

**How to apply:** every line must be a concept being applied or to be applied. Specifics live in code and plans; justifications and history live in git and reviews. If deleting a line leaves every directive intact, delete it. Does not apply to docs whose specifics ARE the contract (protocol specs, budget tables, plans), and load-bearing structure (`§N` numbers cited from code) stays.
