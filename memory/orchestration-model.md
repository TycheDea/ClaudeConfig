---
name: orchestration-model
description: "Durable role-based orchestration: the main session coordinates but never implements; findings and changes use separate dispatches; explicit quality-first model seats, upward substitution, serial work, and independent artifact verification apply across harnesses"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a38eccbe-e253-4073-8a05-baa0bd7d9b10
  modified: 2026-08-06
---

# Orchestration model — durable rationale

The taxonomy names responsibilities, not vendors. Planning errors multiply into
every downstream edit, while routine implementation and mechanical execution
do not need the same reasoning budget. Preserve the role boundary when models,
providers, or harness commands change; re-measure which model can fill a role.
Any capability claim tied to a model generation expires with that generation
([[model-rules-expire-with-the-model]]).

## Roles

- **Orchestrator:** the main/parent session. It receives goals, sequences work,
  reviews findings, verifies artifacts, manages queue/commits, and resolves
  surprises. It never implements or conducts an unbounded investigation.
- **Analysis worker:** produces plans, audits, root causes, comparisons, maps,
  or decision-bearing enumeration. Analysis receives the strongest reasoning
  seat because a cheap wrong finding is expensive downstream.
- **Visual judge:** independently evaluates supplied images and reports only
  pass/fail, severity, axes, and frame-cited defects. It does not produce the
  frames or recommend fixes; planning returns to the orchestrator
  ([[visual-verification]]).
- **Hard implement worker:** applies a settled but difficult or sensitive change
  under exact scope, deliverable, and stop boundaries. Strength does not grant
  design latitude.
- **Default implement worker:** applies ordinary bounded code, tests,
  documentation, gates, or content changes from settled requirements.
- **Mechanical worker:** performs exact commands, moves, downloads, transforms,
  probes, or metric runs whose output requires no judgment.

Current semantic seats are Sol for orchestrator/analysis/judge/hard implement,
Terra for default implementation, and Luna for mechanical execution. In pi,
select available runtime IDs matching those seats. Claude compatibility uses
the strongest reasoning/vision model for Sol roles, Sonnet-class workers for
Terra, and Haiku-class workers for Luna. These mappings are compatibility
layers, not the rationale itself.

## Why the main session does not implement

The main session must retain enough clean context to compare a worker's output
with the user's goal and current gates. If it also authors the change, maker
and checker collapse into one perspective, exploration consumes integration
context, and “one quick fix” bypasses routing. Investigation therefore counts
as work: source tracing, web research, audits, and probes get bounded finding
contracts. Narrow exceptions are verification reads, bookkeeping, one lookup
to choose a worker, and committing a verified worker change.

## Why findings and changes are separate

“Investigate and fix” lets tentative assumptions become code without review.
A dispatch must produce either a **finding** or a **change**. The orchestrator
reviews evidence between them and freezes the implementation boundary. A
finding worker does not edit; a change worker does not redesign. On an
unexpected condition, one bounded check may establish measured reality, after
which the worker implements within the contract or stops and reports tension.

Every dispatch explicitly names six fields: model seat, deliverable, scope,
do-not-touch/do-not-decide boundary, orchestrator verification, and finding or
change type. Inherited model selection is not evidence of intentional routing.

## Quality, escalation, and execution order

Use the least expensive seat that reliably meets the bar, but never route
analysis or visual ship judgment downward to save tokens. Substitute upward
when a seat is unavailable and after two verification failures
(Luna → Terra → Sol); name a downgrade if no upward path exists. Quality
outranks time and change cost, while licensing remains a hard gate.

Optimize the weekly token budget rather than wall time. Serial dispatch is the
default because later tasks often depend on earlier answers and gates. Parallel
work is justified only when answers are independent. Do not launch work that an
in-flight gate may invalidate; refresh plan evidence at dispatch and stage
exact paths ([[dispatch-discipline]]).

Before an approved campaign phase, a strong planning worker decomposes it into
single-worker tasks tagged with role and verification. The orchestrator reviews
dependency order, dispatches serially, verifies diffs/tests/frames/files rather
than prose, and commits only green steps. Every campaign plan records this in
an “Execution model” section.

## Recalibration trigger

When a harness or model generation changes, smoke-test one analysis task and
one bounded implementation task. Re-run the visual bake-off when vision changes.
Update only the compatibility mapping proven by those results; do not weaken
the role separation or silently preserve generation-specific folklore.
