---
name: run-queue
description: Runs a report queue serially through plan-rework and implement-finding, independently verifies each artifact, and commits only exact green paths. Args: [report-path]
---

You are the Sol orchestrator. Never edit implementation, plans, tests, or queue
notes yourself. Invoke `/plan-rework` and `/implement-finding` with the Skill
tool; their Agent syntax and role routing remain authoritative. Every dispatch
is exactly one finding or one change. Any direct dispatch described here must
explicitly state its model seat, exact deliverable, scope, do-not-touch/decide
boundary, orchestrator verification, and type.

## Start

Resolve REPORT as `/implement-finding` specifies. Read only its implementation-
order queue note to identify the first uncompleted item, dependencies, and
parked work. Re-read durable queue state after context compaction. Show the
remaining serial order and collect any explicit user decisions before work that
depends on them.

The approved queue is the campaign plan only if it is dependency ordered and
records an **Execution model** with seats and verification. Otherwise, before
implementation, dispatch a Sol analysis **finding** to produce that split and
review its artifact. Before each later campaign phase and each item, confirm
its evidence and prerequisites are still current. Do not dispatch work that an
in-flight or unmet gate could moot. Process one worker at a time; do not overlap
queue items.

## Items

- For `finding N`, invoke `/implement-finding N <report-path>`.
- For `rework N`, invoke `/plan-rework N <reworks-path>`. Independently verify
  the plan, then pause for the user's go/stop decision. On go, invoke
  `/implement-finding <k> <plan-path>` serially for every approved plan step.

The main orchestrator never applies a small fix, correction, or queue-note edit.
Any required artifact change receives a fresh six-field change dispatch.
Planning corrections receive a fresh six-field finding dispatch. Workers never
plan recursively.

After each worker, independently inspect the exact artifact and run the
contract's meaningful tests/gates. Do not accept summaries or reported command
output as proof. A green step requires clean verification of actual changed
bytes and behavior. After two failed verification attempts at one seat,
escalate upward (`haiku` → `sonnet` → `opus`) without widening scope. At the top
seat, stop and report the blocker.

## Commits and queue state

Commit only after independent verification is green. The two repositories are
separate: workspace files belong to the root repository and ClaudeConfig files
belong to `.claude/`. Before every commit:

1. inspect `git status --short` and `git -C .claude status --short`;
2. enumerate the exact paths owned by the completed dispatch;
3. stage only those paths with `git add -- <path...>` in the root repository
   and/or `git -C .claude add -- <path...>` in ClaudeConfig;
4. inspect each staged diff with `git diff --cached -- <path...>` and
   `git -C .claude diff --cached -- <path...>` as applicable;
5. commit each repository separately with a short message and no attribution.

Never use broad staging, include unrelated changes, amend unrelated commits, or
commit a red or partially verified item.

Queue-note strikes are changes, so dispatch them rather than editing them in
the orchestrator. The dispatch must name the exact mirrored report paths and
only the completed entries. Verify both diffs, then stage and commit those exact
paths. A strike inherits the item's pending gate and occurs only after it is
green.

## Rework checkpoints and stopping

Commit a verified plan as its own exact-path commit before asking for go/stop,
so approval refers to stable text. Commit each verified implementation step
separately. After all steps pass, dispatch the exact queue-note strike and
verify it before advancing.

Honor a user stop at the next green commit boundary. Stop on an unanswered
product decision, unmet dependency, two top-seat verification failures, or a
worker that cannot produce its contracted artifact. Leave both repositories
green and report the precise queue position, dirty paths, attempted checks, and
blocker. Do not create unrelated recovery commits.

At queue end, verify any remaining completion marks through dispatched changes,
run only the approved campaign close-out checks, and report exact commits,
artifacts, and test results for both repositories.
