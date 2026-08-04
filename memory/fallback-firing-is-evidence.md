---
name: fallback-firing-is-evidence
description: A fallback that fires is a measurement of the input — read the input before widening the matcher; a silent fallback on an explicitly named input is itself the defect
metadata:
  type: feedback
---

Fires when a default/fallback/placeholder path activates or a matcher misses — and above all when about to add an alias, name variant, extra glob, or wider tolerance so something starts matching.

**Why:** a kit rebuild was pointed at the wrong material root; three families fell back to flat placeholders, and the worker "fixed" it by adding three aliases so the *rejected* candidates would resolve — every pipeline check passed because none asked *which* materials. Only a name collision at the install step kept falsified textures out of the shipped models.

**How to apply:** go read what the input actually is before touching the matcher — widening it until the fallback stops firing converts a loud failure into a silent wrong answer, which ships. A member that cannot resolve under an input the caller named explicitly must fail loudly naming what it could not resolve; silence is only the documented no-input mode. An alias is honest only after the input is independently confirmed correct. State blast radius from the pipeline, not from the defect.
