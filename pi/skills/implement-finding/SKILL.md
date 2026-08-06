---
name: implement-finding
description: Implements one audit or plan finding through an explicit project implementation agent while the main orchestrator stays edit-free. Use for /skill:implement-finding <finding> [report].
---

# Implement Finding

The main session orchestrates and never modifies files. Execute exactly one change.

1. Resolve the numbered finding and gather only the text and evidence needed for a self-contained contract.
2. Choose one explicit project agent:
   - `luna-mechanical`: fully enumerated deterministic operations with no judgment.
   - `terra-implement`: default bounded code, test, or documentation work.
   - `sol-hard-implement`: sensitive, subtle, wide-blast-radius, or previously failed work under exact scope.
3. Tell the user the selected seat and reason. Call `subagent` once with that agent, `agentScope: "project"`, and `confirmProjectAgents: false`.
4. The task must explicitly contain all six fields: `MODEL SEAT: <selected role>`, `DELIVERABLE`, `SCOPE`, `DO NOT TOUCH / DECIDE`, `VERIFY`, and `TYPE: change`. The model seat is mandatory and must not be inferred from the chosen agent. Include available evidence; forbid other changes and commits.
5. After return, independently inspect both `git status --short` and `git -C .claude status --short`, inspect the actual diff and untracked artifacts, and run the stated targeted check. Do not treat worker prose as evidence.
6. Report artifacts and exact check output. If scope or verification fails, leave the diff visible and stop for a fresh bounded correction dispatch; never repair it in the orchestrator.

Do not combine findings, dispatch planning, commit, or modify files yourself.
