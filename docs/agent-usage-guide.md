# Agent usage guide

Operational reference for running Vordar sessions in Claude Code or pi. Shared
rules live only in `../CLAUDE.md`; this guide shows the workflow. Harness setup
is `../AI-SETUP.md`, and migration status is `harness-migration-plan.md`.

## Start and choose the session goal

Start either harness from the game-repository root. State the desired outcome
and relevant constraints rather than prescribing an implementation. The main
session stays in the orchestrator role.

Use a fresh session for an unrelated goal and compact a continuing session when
context becomes expensive. Neither action is a gate. At startup, do not open
the live queue or broad design/memory material unless the request is resuming
that work or directly requires it.

Default flow:

```text
user goal
  → orchestrator identifies the next bounded deliverable
  → finding worker when analysis is needed
  → orchestrator reviews the finding
  → change worker implements settled scope
  → orchestrator inspects diff/artifacts and runs verification
  → independent visual judge when shipping depends on images
  → update queue state and commit exact paths
```

## Dispatch contract

Copy this shape for every worker:

```text
MODEL SEAT: <Sol analysis | Sol judge | Sol hard-implement | Terra | Luna>
TYPE: <finding | change>
DELIVERABLE: <exact path or artifact shape>
SCOPE: <files, systems, and accepted inputs>
DO NOT TOUCH / DECIDE: <explicit boundary>
VERIFY: <command or artifact check the orchestrator will run>
CONTEXT: <only the files this worker must read>
```

`CONTEXT` is useful operational detail; it does not replace any of the six
required contract fields.

### Root-cause then fix

```text
MODEL SEAT: Sol analysis
TYPE: finding
DELIVERABLE: Root-cause note with file/line evidence and a reproducible test
SCOPE: server reconnect path and its focused tests
DO NOT TOUCH / DECIDE: No edits; no redesign outside reconnect behavior
VERIFY: Orchestrator reproduces the failure and checks cited source
CONTEXT: Relevant protocol and server modules only
```

After review, dispatch the change separately:

```text
MODEL SEAT: Terra
TYPE: change
DELIVERABLE: Focused regression test and minimal fix
SCOPE: Files named in the accepted root-cause note
DO NOT TOUCH / DECIDE: No protocol redesign or adjacent cleanup
VERIFY: cargo test -p vordar-server <focused-test>
CONTEXT: Accepted finding plus named source/test files
```

### Visual gate

Frame capture and judgment are separate jobs. The judge contract adds:

```text
MODEL SEAT: Sol judge
TYPE: finding
DELIVERABLE: Pass/fail and frame-cited defects by supplied axes
DO NOT TOUCH / DECIDE: Do not recommend fixes, tools, prompts, or next steps
VERIFY: Orchestrator checks every cited frame and required axis is present
```

### Sensitive implementation

Use Sol hard-implement only with frozen requirements and a narrow boundary:

```text
MODEL SEAT: Sol hard-implement
TYPE: change
DELIVERABLE: Minimal diff and focused tests
DO NOT TOUCH / DECIDE: Outside listed files/contract, stop and report
VERIFY: <targeted diagnostics/test command>
```

## Model-seat operation

| Need | Seat |
|---|---|
| Plan, audit, comparison, root cause | Sol analysis |
| Ship decision based on images | Sol judge with images |
| Difficult/sensitive bounded edit | Sol hard-implement |
| Ordinary bounded implementation/docs | Terra |
| Exact no-judgment operation | Luna |

In pi, select the currently available runtime model corresponding to the named
seat; if no per-call selector is exposed, substitute upward and state it in the
brief. In Claude Code, use the strongest reasoning/vision worker for Sol,
Sonnet-class implementation for Terra, and Haiku-class execution for Luna.
Never change the main session into an implementation seat to save a spawn.

If a worker fails verification twice, redispatch the same settled contract one
seat upward. If the failure disproves the finding, stop implementation and
return to a new analysis dispatch instead of stacking fixes.

## Campaigns and queues

For a multi-step approved phase:

1. dispatch a Sol planner for dependency-ordered tasks tagged `seat + verify`;
2. review the split against current artifacts and gates;
3. dispatch one task at a time;
4. verify outputs on disk and commit green exact paths;
5. update `../tasks/todo.md` or the campaign task file at the checkpoint.

Do not start a task that a pending gate may invalidate. Parallel dispatch is
reserved for work whose answers cannot affect one another.

For an existing findings queue, read the queue and selected finding, not the
whole campaign archive. One queue item produces one implementation dispatch.
Large findings first receive a separate planning dispatch. Strike or mark an
item complete only after its inherited verification gate passes.

Available skills/agents may automate audit, `implement-finding`, `plan-rework`,
or `run-queue` flows. Treat them as wrappers around the same contracts; inspect
their emitted artifacts and do not assume their names prove compliance.

## Resume and handoff

To resume, open `../tasks/todo.md`, then only the task/campaign files it points
to. Confirm repository status and whether recorded gates still match artifacts
before dispatching. A useful checkpoint records:

- completed and pending items;
- evidence paths and exact verification results;
- unresolved user decisions or uncertain in-flight decisions;
- separate game/ClaudeConfig repository state;
- the next bounded dispatch and its seat.

“Save the state” means write that checkpoint and stop. Detailed durable rulings
belong in `../memory/` only after a real correction; add a concise index entry
without copying the ruling into the index.

## Repository closeout

Because `.claude/` is a separate repository, inspect both status lists. Stage
exact paths, keep unrelated work untouched, and commit each repository
separately. Before reporting success, run the task's targeted checks plus
`git diff --check` in each repository that changed.
