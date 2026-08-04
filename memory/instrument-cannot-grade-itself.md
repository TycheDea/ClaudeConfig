---
name: instrument-cannot-grade-itself
description: The measurement that justifies building X must never come from X; any criterion with a free parameter is unvalidated until swept to a plateau
metadata:
  type: feedback
---

Fires when reporting a count that decides whether to build something, a fresh detector's violation total, a premise measured with the mechanism's own criterion, any criterion carrying a direction/sample/ray/resolution/tolerance parameter, or any shipped constant denominated in the data's own units.

**Why:** a linter justified itself with "806 stale anchors" (independent recount: 29, all in closed reports); a 26-direction hidden-cell probe justified an interior-fill mechanism whose count collapsed 690,882 → 7 when swept to 1330 directions — the probe was the mechanism grading its own entrance exam; a weld epsilon sat unswept for a campaign and the sweep deleted the stage outright.

**How to apply:**
- Build-or-drop counts come from an instrument that is not the candidate (a one-off grep, a hand count).
- A violation total is not evidence until ~10 hits are confirmed genuine; report the distribution, not the total — hits concentrated in a closed corpus mean the class is extinct.
- Sweep every free parameter toward its limit and report the curve; a result that moves under refinement was set by the parameter, not the data. A curve still falling at the last sample has not converged. The question for any constant: would refining it change the output?
- Comparisons across a stage boundary need one subject definition, fixed in the pipeline's own terms, measured through every stage.
- Does not apply to instruments predating the decision, or to distrusting a *failing* gate. Dual: [[checks-must-fail-when-broken]].
