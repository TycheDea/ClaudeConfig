---
name: checks-must-fail-when-broken
description: A check is worthless until shown red on the broken input — assert the shipped artifact's property, never an exit code, a proxy artifact, or a tautology
metadata:
  type: feedback
---

Fires when writing or trusting any check that stands in for a property of a shipped artifact.

**Why:** three recurrences of the same shape — an undecoded "swizzle probe succeeded" shipped an all-zero roughness channel; green geometry checks graded a roof deck the camera never sees; two audit findings shipped asserts that were already green before the fix existed.

**How to apply:**
- Decode the artifact and assert the property; never trust a tool's exit code or a wrapper's claim.
- Name which bytes the check reads and which bytes the consumer gets — they must be the same artifact, not an intermediate, a source object, or an occluded surface.
- Ask: what value would make this assert fail, and can the broken code produce it? If none exists, it is a tautology wearing a test's clothes.
- Every check is shown red on the broken input before its green counts, and the red proof comes from an instrument sharing no code with the check.
- Partly enforced for finding workers by `.claude/agents/finding-worker.md` rule 4 (reports must carry the fail-first proof or its absence); everywhere else apply manually. Render deliverables additionally get [[visual-verification]]. Dual: [[instrument-cannot-grade-itself]] (a check that fires when nothing is wrong).
