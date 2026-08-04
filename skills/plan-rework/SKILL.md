---
name: plan-rework
description: Plans one rework-scale finding via the rework-planner subagent. Use when asked to plan, design, or break down a rework or big feature, e.g. "/plan-rework 1" or "plan rework 2 of the networking reworks". Args: <rework-number> [reworks-path]
---

You are the orchestrator; the rework-planner subagent does ALL design work.
You do not read the reworks report, extract finding text, or design anything
yourself.

The arguments give a rework finding number N and optionally a reworks report
path REPORT. Reports live in per-domain folders: `docs/reviews/<domain>/`.
When no path is given, list `docs/reviews/*/reworks-*.md` (do not open the
files): if the matches all sit in one domain folder, use the newest by
filename date; if more than one domain folder matches, stop and ask the user
which report they mean.

Spawn ONE rework-planner subagent (Agent tool, subagent_type "rework-planner")
with exactly this task, substituting N and REPORT:

"Design the implementation plan for rework finding N of REPORT. Read the
finding's full section from that file first, study every part of the codebase
the design touches, and write the plan document as your agent instructions
specify. You write no code. Reporting 'not done' without a written plan file
is not an option."

When it returns:
1. Show the user the planner's final report verbatim.
2. Run `git status --short` and show it — the plan file should be the ONLY
   new artifact; anything else is out of bounds and must be flagged.

The plan file's "Findings (execution order)" section uses the audit fix
format, so each step is executed afterwards with
`/implement-finding <k> <plan-file-path>`.

### API failure recovery — probe and override

If a spawn dies to a 5xx (Overloaded, Service Unavailable) pre-edit:
on the SECOND consecutive pre-edit 5xx death of the same spawn, do not retry
yet. Launch a 1-turn haiku probe (model: "haiku", no tools, no context) with
the task "Reply with the single word: ok". If the probe succeeds, the model
tier is overloaded — respawn the planner with `model: "opus"` (the documented
fallback) and tell the user which model produced the plan (this is a
downgrade from the ideal fable depth; always name it). If the probe fails,
back off long (the API path is down) and tell the user to wait.

Nothing else: no edits, no design opinions of your own, no review beyond the
command above unless the user asks.
