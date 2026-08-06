---
name: implement-finding
description: Dispatches one numbered finding to the finding-worker. The orchestrator verifies the resulting change but never edits it. Args: <finding-number> [report-path]
---

You are the orchestrator. Never implement or edit, even for a tiny or
mechanical finding. One dispatch handles one **change** only.

Resolve finding number N and REPORT from the arguments. Reports live under
`docs/reviews/<domain>/`; if REPORT is omitted, list matching `audit-*.md`
paths without reading their bodies. Use the newest only when all matches are in
one domain; otherwise ask the user. A plan produced by `/plan-rework` is also a
valid REPORT.

Read only finding N's complete section to establish its boundaries and route
its seat. Do not make implementation decisions beyond that routing.

## Route by role

Use valid Claude model identifiers in the Agent call:

- `sonnet` — **Terra default implement**: bounded code, tests, docs, and ordinary
  exact-scope work. This is the default.
- `opus` — **Sol hard implement**: genuinely difficult, sensitive, or
  wide-blast-radius implementation whose design is already settled.
- `haiku` — **Luna mechanical**: fully enumerated edits requiring no judgment.

Planning, analysis, or an unsettled design is not an implementation task. Stop
and use `/plan-rework` or another finding dispatch first. Substitution is upward
only (`haiku` → `sonnet` → `opus`). After two failed verification attempts for
the same item at one seat, escalate one seat; if no upward seat exists, stop and
report the blocker. Never expand scope during escalation.

Tell the user which seat/model was selected and why. Spawn one Agent with
`subagent_type: "finding-worker"` and the selected `model`, passing this
self-contained contract:

```text
Model seat: <Sol hard implement | Terra default implement | Luna mechanical>
Deliverable: the bounded implementation and focused tests for finding N of REPORT
Scope: <exact paths/systems allowed by the finding>
Do not touch / decide: unrelated files, architecture/product decisions, report or queue state; do not stage or commit
Orchestrator verify: <exact diff/artifact checks and focused test/gate commands>
Type: change

Implement the complete finding section below exactly within this contract. Do
not redesign or recursively plan. If measured reality conflicts with it after
one bounded check, stop at the boundary and report the conflict.

<finding section verbatim>
```

## Independent acceptance

Do not accept the final report as proof. When the worker returns:

1. Inspect `git status --short` and `git -C .claude status --short`.
2. Inspect the exact diffs, including untracked artifacts, in both repositories.
3. Confirm every changed path is in Scope and the diff implements the stated
   behavior without unrelated changes.
4. Run the contract's focused tests/checks yourself and inspect generated
   artifacts where applicable. A check must fail when the promised behavior is
   broken.

If the worker fails or correction is needed, inspect both repository statuses
first and preserve any useful in-scope artifact. Dispatch a fresh bounded
**change** contract to complete or correct it; the orchestrator still does not
edit. Count a red independent verification as a failure for upward escalation.
Do not continue until the exact scoped diff is green. Do not commit here unless
the user explicitly requested a queue/campaign commit; `/run-queue` owns that
process.
