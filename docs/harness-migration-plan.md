# Harness migration status

## Current status — 2026-08-06

| Area | Status |
|---|---|
| Claude Code | Retained as a supported interactive harness |
| pi + OpenAI/Codex | Available on this machine |
| Shared project law | Canonical body is `.claude/CLAUDE.md` for Claude and pi |
| pi project adapter | Established and verified for startup and project resource discovery through root `AGENTS.md` and the local `.pi` junction to `.claude/pi` |
| Claude project memory | Uses the junction documented in `../AI-SETUP.md` |
| Prime Agent | Not verified; not an assumed production path |
| Sol visual-judge replacement | Bake-off not recorded; unsupervised ship calls remain gated |

This is a compatibility migration, not a retirement of Claude. Both supported
interactive harnesses use the same role taxonomy and shared law. Setup details
belong in `../AI-SETUP.md`; daily operation belongs in
`agent-usage-guide.md`.

## Established target

Minimal startup context is:

- Claude: `.claude/CLAUDE.md` plus `memory/MEMORY.md`
- pi: root `AGENTS.md` pointer, then the same canonical law and memory index

Design, queue/task files, migration material, and individual memory bodies are
opened only when relevant. The game repository and ClaudeConfig remain separate
repositories with separate commits.

Model routing is role-based rather than tied to a product snapshot: Sol for the
orchestrator, analysis, visual judgment, and hard sensitive implementation;
Terra for default bounded implementation; Luna for no-judgment mechanical
work. Claude uses capability-equivalent workers as documented in the canonical
law. Model IDs are runtime facts, not policy.

Verified in this session:

- the local `.pi` junction exists and targets `.claude/pi`;
- noninteractive `pi.cmd --mode json --no-session --approve --print ...`
  exited 0 with provider `openai-codex` and model `gpt-5.6-sol`;
- automatic context was exactly `AGENTS.md`, `.claude/CLAUDE.md`, and
  `.claude/memory/MEMORY.md`, with no other automatic bodies;
- project skills `implement-finding`, `plan-rework`, and `run-queue` were
  available;
- a real `subagent` call with `agentScope: project` discovered and ran
  `sol-analysis`; checked agent frontmatter remains the source for seat pinning;
- extension tests passed 6/6, including rejected post-write enforcement.

## Remaining gates

### 1. Full pi engineering orchestration smoke

Basic startup/resource discovery and a real project-scoped agent dispatch are
recorded above. As a separate end-to-end gate, run and record one ordinary
finding-to-change engineering task with:

1. main session remaining orchestrator-only;
2. explicit Sol finding dispatch when diagnosis is needed;
3. separate Terra (or upward substitute) change dispatch;
4. artifact/test verification by the main session;
5. no production implementation authored by the main session.

### 2. Visual-judge bake-off

Before any unsupervised visual shipping decision, compare Sol judgment against
3–5 historical packages with known written outcomes. Use identical frames and
axes, blind where practical, and require defects-only output.

Pass requires at least 4/5 agreement on ship-critical pass/fail, overlap on the
decisive defects, and no metrics-based rationalization of a visual failure.
Record frames, briefs, verdicts, and score in a task or review artifact. Until
that record exists, a user spot-check remains required for ship calls and Prime
must not run an autonomous visual gate.

Re-run the bake-off when the visual model/API materially changes.

### 3. Prime evaluation

Prime is optional and remains unverified. If long/detachable factory work still
justifies it after pi is stable:

1. verify install, OpenAI login, model selection, and repository access;
2. prove a parent orchestrator can dispatch explicit role-bound children;
3. run one bounded factory packet: generation/metrics/frames, then the baked-off
   independent judge, then install only after a pass;
4. verify gates against worker artifacts and confirm the parent authored no
   implementation diff;
5. constrain automated refinement to process details such as GPU order,
   metric order, timeouts, and manifests—never design, art law, premise,
   licensing, or ship criteria.

Windows/WSL behavior, retained-worker reliability, and long GPU job handling
must be measured rather than assumed.

### 4. Workflow parity

Adapter configuration, project resource availability, and post-write
enforcement are verified. During ordinary use, validate the workflows still
used: focused audits, `implement-finding`, `plan-rework`, and queue execution.
Each must preserve the six-part contract, finding/change split, model-seat
selection, exact-path verification, and serial gate order.

## Stable constraints during migration

Migration does not authorize edits to CREDITS/license verdicts, the NC-tooling
rule, secrets, DESIGN, visual-quality law, town premise, or user-global config.
It also does not weaken in-engine visual evidence, documented asset installs,
GPU serialization, or independent verification. Those constraints remain in
the canonical law and their on-demand source documents.

## Completion criteria

The pi adapter configuration is established for minimal startup context,
project resource discovery, project-scoped dispatch, and extension enforcement.
Full ordinary engineering readiness additionally requires the separate
finding-to-change orchestration smoke. Prime readiness and visual autonomy are
separate gates; neither blocks retaining Claude or using pi for non-visual
interactive work.
