---
name: plan-rework
description: Dispatches one Sol planning task for a rework and returns an evidence-backed implementation plan without implementing it. Use for /skill:plan-rework <finding> [report].
---

# Plan Rework

Remain the orchestrator; do not design or implement.

1. Resolve the requested rework and read only enough source material to form the dispatch contract.
2. Call `subagent` once with `agent: "sol-analysis"`, `agentScope: "project"`, and `confirmProjectAgents: false`.
3. The task must explicitly contain all six fields: `MODEL SEAT: Sol analysis`, `DELIVERABLE` (the requested plan), `SCOPE` (exact files/systems), `DO NOT TOUCH / DECIDE`, `VERIFY` (the eventual implementation checks), and `TYPE: finding`. Include the evidence to inspect.
4. Require acceptance criteria, ordered change steps, exact paths, test-first RED/GREEN steps where practical, risks, and an execution model that assigns each step to `luna-mechanical`, `terra-implement`, or `sol-hard-implement`.
5. Return the planner's plan and independently confirm that repository status contains no planner edits. Flag any changed path as a contract breach.

Do not dispatch implementation, modify files, or turn unresolved assumptions into design decisions.
