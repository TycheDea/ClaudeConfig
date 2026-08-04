---
name: implement-finding
description: Implements one numbered finding via the finding-worker subagent. Use when asked to implement, execute, or fix an audit finding, e.g. "/implement-finding 2" or "implement finding 3 of the networking audit". Args: <finding-number> [report-path]
---

You are the orchestrator; the finding-worker subagent does ALL implementation
work. You do not read the report, extract finding text, edit files, or run
fixes yourself.

The arguments give a finding number N and optionally a report path REPORT.
Reports live in per-domain folders: `docs/reviews/<domain>/`. When no path is
given, list `docs/reviews/*/audit-*.md` (do not open the files): if the
matches all sit in one domain folder, use the newest by filename date; if
more than one domain folder matches, stop and ask the user which report they
mean. REPORT may also be a plan file produced by /plan-rework
(`docs/reviews/<domain>/plan-*.md`) — its "Findings (execution order)"
section uses the same finding format.

Before spawning, read ONLY finding N's section in REPORT (its `### N.` title
through the end of its Path bullet) — to route it to a model AND to paste it
verbatim into the spawn task below (the worker never opens the report; you
form no implementation opinions from it). Route on how much thinking the step
needs, taking the cheapest tier that actually has it, and pass it as `model`
in the Agent call:

- `haiku` — implementor with no thinking: docs-only steps ("(docs-only)"
  titles, diagrams, tables, queue notes); purely mechanical edits whose Path
  enumerates exactly what to change with nothing to diagnose; and /plan-rework
  steps whose Path dictates signatures/order (planned extraction steps,
  verbatim statement sequencing).
- `sonnet` — implementor with minimum thinking, the default: bounded code
  fixes with a test, mechanical refactors with clear gates, anything a
  faithful executor lands from the Path alone.
- `opus` — thinking implementor, for the hard steps: a diagnosis the Path
  names (a failing timing test to debug, a race to find, calibration against
  behavior that must be measured before acting), a subtle or wide-blast-radius
  change, a step whose design the plan left partly open, or a step a previous
  worker already failed.

`fable` is the planning tier and is never a finding-worker — a step that needs
design work needs a planner, not a deeper implementor.

Tell the user in one line which model you chose and why.

Also before spawning, take the last known full-suite result already in this
session — the previous finding's final gate output, or this loop's own
baseline check — as `N/N` passing. Do not run a fresh baseline yourself; if
no such result is in context yet (this is the loop's first finding), say so
in the spawn task instead of inventing a count.

After file structure moves, treat cargo as the only oracle. IDE diagnostics
become unreliable (phantom unresolved-module and duplicate-definition errors)
until an `ide_sync_files` call or a natural index refresh. Optionally call
`ide_sync_files` after move-heavy commits, or simply disregard phantom errors
until the next verification round. Do not re-run gates solely to clear phantom
diagnostics — they are ambient noise while the index updates.

## Loop behavior

Loops of pre-planned findings run under fable like everything else, and fall back to opus only when fable is out of tokens; audits and plan reviews stay on fable either way.

If a finding-worker spawn dies to a 5xx pre-edit on the second consecutive
attempt, do not retry yet: probe with a 1-turn haiku task (no tools, "Reply
with the single word: ok") to isolate the tier. Probe green ⇒ that tier is
overloaded: respawn on the tier ABOVE it (haiku→sonnet, sonnet→opus,
opus→fable) and tell the user which model implemented it. Substitute upward,
never downward — an outage must not quietly cost a step its thinking depth,
and only when no tier remains above does a downgrade become the option, named
as such. Probe red ⇒ back off long and tell the user the API path is down.

A finding-worker spawn that dies **after** it has already edited files needs
different handling: the diff must be preserved, not discarded outright, but
the workspace still has to come back to green before anything else runs. On
the first such death for an item: run `git status --short` in the workspace
root, and separately `git -C .claude status --short` — `.claude/` is
gitignored and is its own nested git repository, so a workspace-root `git
stash` never touches it, and a dead spawn's diff may land in either repo, or
both. Stash whichever repo(s) came back dirty: `git stash push -u -m
"dead-spawn <item>"` in the workspace root, `git -C .claude stash push -u -m
"dead-spawn <item>"` in the nested repo. The stash itself returns each repo
to its last green commit (HEAD, since a dead spawn never got far enough to
commit) — no separate reset is needed. Respawn the same item immediately; do
not contact the user, this is routine recovery, not an incident. Stash refs
are named per item, so a partial diff can be recovered and salvaged later if
it turns out to matter — nothing is destroyed. Only if the SAME item dies
post-edit a second time in one loop, stop and tell the user: two deaths on
one item is a pattern, not noise, and a third respawn would burn tokens
against a cause that hasn't changed.

When launching a loop of multiple findings, scan the entire queue first for
any findings tagged "(user-decides)" in their titles. If any exist, batch all
their questions to the user at launch, before spawning any finding-worker
agents. Collect the user's decisions in order and attach them to each tagged
finding's spawn task, so workers implement without stalls. This prevents
mid-loop defaults and focuses user attention at the natural decision point
(loop start), not scattered throughout implementation.

### Micro findings — no spawn at all

A finding tagged "(micro)" in its title (see audit-base's Finding tags) is
applied by YOU inline, skipping the ~35–38k worker boot entirely: it must be
strictly enumerated, single-file, and need no new test. Make the edit, run
the gate its file class requires (`cargo check --workspace --all-targets`
for source; `bash scripts/lint-comments.sh` when a comment changed; nothing
for gitignored config), and show the diff. If while applying it you discover
it is NOT actually micro (needs a second file, a test, or any diagnosis),
stop, revert your partial edit, and spawn a worker normally — never stretch
the inline path. Untagged findings always spawn a worker, however small they
look.

### Spawning

Spawn ONE finding-worker subagent (Agent tool, subagent_type
"finding-worker") with exactly this task, substituting N, REPORT, the green
count, and the finding's verbatim section text:

"Implement finding N of REPORT. HEAD is green at N/N — do not re-establish a
baseline. Your finding's complete section (title through Path) is pasted
below — it is the full text; do NOT open any file under `docs/reviews/`,
except when appending rework-scale findings (tail-only, ~40 lines from end).
Explore the codebase through the section's Evidence file:line pointers, and
execute its Path steps faithfully. You may edit any file in the workspace
the fix or its test requires. Declining or reporting 'not done' without code
edits is not an option.

Your output ceiling is ~100k tokens (the planner's pass-boundary band). If
you overrun it, stop and report as exhausted — do not push on, and do not
commit a half-landed change.

<the finding's section, pasted verbatim>"

### Corrections

When a worker's result needs a follow-up fix you can state in ≤5
self-contained lines with no dependence on the worker's transcript (delete
this leftover file, rename that test, run this gate), spawn a FRESH
finding-worker with that brief — haiku unless the fix itself is subtle. Do
NOT resume the original agent for mechanical corrections: a resume replays
its whole transcript (~60–80k tokens measured) to do a 3-tool job. Resume
only when the correction genuinely depends on what the original worker
knows.

When it returns:
1. Show the user the worker's final report verbatim.
2. Run `git status --short` and `git diff --stat` and show both — the status
   catches new untracked files that the diff stat alone misses.

Never re-run a gate the worker reported green — its pasted output is the
record; a duplicate run buys nothing and costs a turn.

A modified or new `docs/reviews/reworks-*.md` in that status is legitimate:
workers move rework-scale remainders of their finding there (their agent rules
require it). Point it out so the user knows a rework was queued.

Nothing else: no edits, no commits, no fixes of your own, no review beyond
the two commands above unless the user asks.
