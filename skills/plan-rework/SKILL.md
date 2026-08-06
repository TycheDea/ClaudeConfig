---
name: plan-rework
description: Dispatches one rework-scale finding to the rework-planner and independently verifies the plan artifact. Args: <rework-number> [reworks-path]
---

You are the orchestrator. Never design or implement the rework yourself. One
dispatch produces one **finding** only.

Resolve rework number N and REPORT from the arguments. Reports live under
`docs/reviews/<domain>/`. If REPORT is omitted, list matching `reworks-*.md`
paths without reading their bodies. Use the newest only when all matches are in
one domain; otherwise ask the user.

Determine the exact plan path from REPORT, N, and today's date. Spawn one Agent
with `subagent_type: "rework-planner"` and `model: "opus"` using this contract:

```text
Model seat: Sol analysis (Opus-class)
Deliverable: docs/reviews/<domain>/plan-<domain>-rework-N-YYYY-MM-DD.md
Scope: rework finding N of REPORT and the code seams needed to plan it
Do not touch / decide: no production, test, queue, memory, or configuration edits; do not implement, stage, commit, or silently decide product questions
Orchestrator verify: inspect the exact plan diff, both repository statuses, required sections, step contracts, dependency order, and cited code evidence
Type: finding

Read the finding's complete section first. Study the bounded codebase seams and
write only the plan Deliverable described by your agent instructions.
```

Planning and analysis use Opus-class capability. If the dispatch or independent
verification fails twice, stop and report the blocker; there is no higher
Claude compatibility seat to substitute without an explicit user decision.

When the planner returns, verify independently:

1. Run `git status --short` and `git -C .claude status --short`.
2. Inspect the plan's exact diff and confirm it is the only new artifact.
3. Check that the plan is finding-only, cites inspected evidence, records an
   Execution model, and splits work into serial, self-contained change steps.
4. Confirm every step contains model seat, deliverable, scope, do-not-touch,
   orchestrator verification, and type, with behavioral tests where practical.

Show the verified plan path, decisions, ordered steps, and unresolved user
questions. Do not edit defects in the plan yourself; issue a fresh bounded
finding dispatch for correction. Execute approved steps later with
`/implement-finding <k> <plan-path>`.
