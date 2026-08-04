---
name: dispatch-discipline
description: Work gated on an in-flight verdict waits; plan evidence is a snapshot re-checked at dispatch; stage exact paths while agents hold the tree
metadata:
  type: feedback
---

Fires when dispatching work whose usefulness depends on a measurement still in flight; when dispatching a step from a plan authored in parallel with another plan; when running `git add` with a directory/`-A` scope or `git commit -a` while any agent or session holds files under it.

**Why:** a research fleet went out on a hypothesis whose gating study returned REFUTED an hour later — and the fleet's conclusion was relayed to the user for approval before the gate returned; three reworks planned in parallel each cited lines a sibling plan had deleted or moved; `git add -A` swept another agent's half-written edit into an unrelated commit.

**How to apply:**
- Before dispatching, ask what the in-flight gate could return that would make the work moot — if any answer would, wait. Cheapness is the rationalization this error always wears, never a reason. Parallelism is for work independent of the *answer*, not merely the files; premise dependency serializes tasks that touch no common file.
- Never relay a gated option to the user for approval while its gate runs — a gate jumped in dispatch becomes a gate jumped in conversation.
- A plan's Evidence is a snapshot and approval does not refresh it: before dispatching a step, check whether an executed step moved what it cites (one grep, orchestrator's job), and state the drift explicitly in the brief. Sequence concurrent plans largest-blast-radius first. Pre-registered numbers go stale the same way and get argued with instead of failing loudly.
- While anything else holds the tree: stage exact paths and commit with the pathspec form (`git commit -- <paths>`), account for every `git status --short` line first. Sweep-committed foreign work is backed out with `reset --soft` + `restore --staged`, never by touching the worktree.
