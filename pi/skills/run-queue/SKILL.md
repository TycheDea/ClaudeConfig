---
name: run-queue
description: Runs a findings or rework queue serially with separate planning and implementation, independent gates, exact-path commits, and seat escalation. Use for /skill:run-queue [report].
---

# Run Queue

Remain an edit-free orchestrator. Run one item and one subagent at a time; never use parallel or chain mode.

## Start or resume

- Resolve the queue note and re-read its durable state before every dispatch. List remaining and parked items; collect all currently known user decisions before work begins.
- Check both repositories independently: workspace root and nested `.claude`. Record each clean baseline and current HEAD. Stop if unrelated dirt makes ownership ambiguous.
- Recheck each item's evidence, prerequisite gate, user approval, and current applicability immediately before dispatch. Do not launch work an in-flight or failed gate could moot.

## Per item

- Rework: load and follow `plan-rework`; planning is one Sol finding and no implementation. Present the plan and wait for the required go/stop decision before any change dispatch.
- Approved plan step or ordinary finding: load and follow `implement-finding`; dispatch exactly one change to the explicit project agent selected by role and complexity.
- Independently inspect artifacts in both repositories and run the item's verification. Worker claims are not gate evidence.
- Keep execution serial. Do not start the next item until the current artifact is verified, committed, and its queue state is accurate.

## Failure and escalation

A verification failure gets one fresh, bounded correction at the same seat when appropriate. After two verification failures for the same item, stop retrying there and escalate exactly one seat: `luna-mechanical` to `terra-implement`, or `terra-implement` to `sol-hard-implement`. Sol failure stops the queue for user review. Never downgrade silently or merge planning with correction.

## Commits and stopping

- Determine which repository owns every changed path. Stage explicit paths only with `git add -- <paths>` or `git -C .claude add -- <paths>`; never stage all files.
- Before each commit, compare staged paths to the item's allowed scope. Never commit unrelated paths or mix root and nested-repository changes in one commit command. Use short messages without attribution trailers.
- Re-run the required gate before clearing a stale stop, striking a queue entry, or resuming after interruption.
- Stop at the next commit boundary on user request. Stop immediately on blocked prerequisites, persistent red gates, scope breaches, or exhausted Sol escalation; report the exact queue position, repo states, and gate output.
