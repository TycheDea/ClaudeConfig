---
name: run-queue
description: Runs a report's findings queue end to end — fixes loop automatically, each rework is planned and gated on one go/stop, green steps commit, queue notes strike, tokens report per loop. Use when asked to run a whole queue or campaign, e.g. "/run-queue" or "run the rendering queue". Args: [report-path]
---

You are the orchestrator running an entire findings queue. This skill only
chains procedures that live elsewhere: /plan-rework and /implement-finding
do all per-item work, and every convention they carry — model routing, the
micro inline path, user-decides batching, probe-and-override API-failure
recovery, spawn templates, the corrections path — applies here by INVOKING
those skills (Skill tool; a skill already loaded this session is followed
from its loaded text), never by restating them. If an instruction here
seems to conflict with one of theirs, theirs wins for the step it governs.

Your launch is the user's standing request for the whole run: the commits,
queue-note strikes, and token reports below are user-asked, which is what
implement-finding's closing "unless the user asks" requires.

**Session tier.** Queue runs happen under a fable session — fable is the
orchestration tier. Opus is the backup seat and only that: take it when
fable is out of tokens, never as a preference, since opus is otherwise
better spent as a subagent on visual gates and hard analysis. If the
session is on neither at launch, ask the user to switch (`/model fable`,
or `/model opus` if fable is exhausted) and wait. Plan depth is safe
either way: the rework-planner agent is pinned to fable in its own
definition.

**Locate the queue.** Resolve REPORT the way /implement-finding does when
no path is given (list `docs/reviews/*/audit-*.md` without opening them;
newest if all matches share one domain folder; ask the user if several
domains match). Read ONLY the cross-type queue note — the blockquote under
"## Findings (implementation order)" — never the finding bodies (those are
read per item by the procedures you chain). The queue note is the
campaign's durable state: your position is the first unstruck entry;
entries listed as parked (gate stated, no position) are skipped and named
at launch. After any compaction, re-read the queue note before the next
spawn instead of trusting memory.

**Launch checkpoint (once per campaign).** Show the user: the remaining
queue, any parked entries you will skip, and ALL "(user-decides)"
questions from fixes findings anywhere in the remaining queue, batched
per implement-finding's convention. Do NOT ask rework-level user-decides
here — a rework's real questions do not exist until its plan is written,
and they surface at that rework's own pause. Collect the decisions, then
run.

**Walk the queue in order.**

- **`finding N`** (fixes file): run the /implement-finding procedure —
  route the model, apply inline if "(micro)", spawn otherwise, review its
  status/diff. When green, commit it (short descriptive message, no
  attribution trailers). Consecutive fixes findings are one loop: carry
  the last full-suite count as the next spawn's baseline, and name the
  loop's final finding as loop-final in its spawn task so it runs the
  full gate. When a contiguous fixes segment completes, strike those
  entries in the queue note in BOTH report files (fixes and reworks —
  the note is mirrored) with a one-line done-note, commit the strike,
  then advance. If a batch's diffs touched the replication path
  (`smirk/engine-net/`, `server/vordar-server/src/net/`, or
  `game/vordar-protocol/`), refresh the bench baseline with `cargo bench -p
  vordar-benches --bench snapshot -- --save-baseline main` on a quiet box
  (no background CPU load).

- **`rework N`** (reworks file):
  1. Run the /plan-rework procedure. Its API-failure recovery — probe
     and override — lives there; follow it there.
  2. Commit the plan file (short descriptive message, no attribution
     trailers) as its own commit, before the pause below — the go/stop
     the user gives next must be pinned to the exact plan text at a
     named SHA, not to an uncommitted file that could still change.
  3. Show the planner's final report verbatim plus the previous loop's
     token report, and surface any user question the plan's Design
     decisions raise. **Pause: wait for one go/stop from the user.** This
     checkpoint always happens — it is the behavior, not a mode.
  4. On go: loop the /implement-finding procedure over the plan's steps
     in order (`/implement-finding <k> <plan-path>`), committing each
     green step; name the last step loop-final in its spawn task. On
     stop: end the run and report position.
  5. After the last step's commit: strike `rework N` in the queue note
     in BOTH report files and append "done YYYY-MM-DD (<plan-file>, K
     steps, loop-final gate X/X[, premise-falsified: <item>[, <item>]])"
     per the mark-done convention; commit the strike. The optional
     `premise-falsified:` clause is appended when a step's execution
     contradicted a premise the plan or the finding stated, naming the
     item. It is the loop's only record of that class. (Skip whatever the
     plan's own close-out step already struck.)
  6. Report the loop's tokens by running `python3 scripts/campaign_report.py
     <report-path>`. The vector's `output_max` and `output_max_spawn` fields
     name the outlier the clause asks for. Then advance.

**Stopping.** Any user message during the run is honored at the next
commit boundary: finish the in-flight worker, commit if green, report
position (the struck queue note plus the in-flight item). Stop the queue
yourself — never push on — on any of these terminal states: **blocked**
(the probe says the API path is down, or a plan raises a question the
user has not answered), **stalled** (a worker failure survives one
fresh-spawn correction round, or a gate stays red after one rerun), or
**exhausted** (a worker spawn overruns its declared output ceiling before
landing a green commit — it must halt-and-report, never push on, never
commit). On every such self-initiated stop, append one stop line under
the queue note in BOTH report files (the note is mirrored, per
audit-base.md's queue-note contract): `**STOP** <item> · <tier> · <category> · <attempted> · <gate>`,
where `<category>` is exactly one of `blocked`, `stalled`, or `exhausted`.
A later "run the queue" resume re-verifies the named gate before honoring
the line, and clears the line once that gate is green — so a stale line
(the user fixed the blocker by hand without clearing it) never causes a
skip or misroute on its own; the gate check catches it. Every stop leaves
the workspace green and the queue note accurate, so a later "run the queue"
resumes from the files alone.

**End of queue.** Strike anything completed but still unstruck, then run
`python3 scripts/campaign_report.py <report-path>` and show the emitted
`docs/campaigns/<domain>-<date>.md`, committing it as part of the
campaign's close-out.

**Lesson-mining pass.** After the aggregate report, spawn one analysis-tier
agent (`model: "fable"`, or `"opus"` when fable is unavailable) to read the
campaign's commits, reverts, struck queue notes, and per-step gate results —
including the clean ones — and propose memory entries (candidate description +
rule) for the user to accept, never write them itself. Give it: the queue
note's struck entries and stop lines for this campaign, `git log` for the
campaign's commit range, and the memory index `.claude/memory/MEMORY.md` (the
existing index, so it can dedupe). Its output contract: **at most 3 proposed
memory entries, and zero is a valid and expected result**; each citing its
artifact (a SHA, a gate record, or the struck note line — no artifact, no
entry) and naming a near-duplicate among the existing entries or explicitly
stating there is none; plus a suppression line naming the areas whose gates
were clean, where the pass is forbidden to propose; plus a strike list of
entries whose class did not recur and which a named harness `file:line` now
enforces. Show the user its proposals verbatim — the user accepts, edits, or discards each;
none is written to `.claude/memory/` without that.
