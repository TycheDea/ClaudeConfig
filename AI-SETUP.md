# AI setup

How this repo is wired for Claude Code and how to get the most out of it. All
of it lives in `.claude/` — gitignored here, versioned as its own repo
(`TycheDea/ClaudeConfig`) — so the project tree carries only project files.

## The pieces

### Standing instructions

- `~/.claude/CLAUDE.md` (all projects) — how to work: intent outranks literal
  words, root-cause fixes only, no patches around walls, a memory written after
  every correction, terse chat. Consistent behavior without re-explaining it.
- `.claude/CLAUDE.md` (this repo) — how to code: surgical minimal changes,
  strict comment policy, verifiable success criteria, batched test runs,
  escalate instead of guess. Keeps diffs small and reviewable.
- `.claude/DESIGN.md` — design policies, cited from code by section number.
  Change a policy in one place; every citation follows.

Both CLAUDE.md files load automatically at session start.

### Memory (`.claude/memory/`)

Durable rulings, preferences, and the error register — every correction becomes
a memory with a firing trigger — indexed by `MEMORY.md` (loaded every session).
Decide something once — a licensing stance,
an art direction, a workflow rule — and never repeat it. Plain markdown: edit
the files directly to change what's remembered. The harness reads them through
a junction from its fixed path (`~/.claude/projects/<repo>/memory/`); recreate
the junction on a new machine or workspace.

### Working files (`.claude/tasks/`)

- `todo.md` — the live plan: checkable items, decisions with their evidence. A
  new session resumes from it, so you never re-explain where the last stopped.
- Campaign folders — per-campaign specs and research notes.

### Obsidian (`.claude/` as a vault)

A visual window into the AI workspace — above all into **what loads into
context**: the session-start set (both `CLAUDE.md` files, the `MEMORY.md`
index) sits one link away from everything that loads only on demand (memory
bodies, tasks, `DESIGN.md`), so you can see and prune what every session pays
for. Backlinks and the graph show how rulings reference each other; editing a
memory in the vault IS editing the live file — no sync, no asking. Nothing in
the pipeline depends on it; vault config lives in `.obsidian/`.

### Hooks

Hard guardrails run by the harness itself — they hold even when the model
would forget:

- Before any shell command — blocks destructive commands (force-pushes,
  recursive force-deletes outside the scratchpad).
- After any file edit — linters check exactly the file just touched (comment
  policy, shader validity, vacuous tests). Bad edits get flagged at write
  time, not at review time.

Hooks fail open: an internal hook error never blocks the session.

### Skills

- **Audits** (one skill per domain) — read-only reviews producing an
  evidence-cited findings report, ordered by implementation order, with a
  queue note. A prioritized backlog instead of vague advice.
- `/implement-finding N` — one agent implements exactly one finding,
  test-first.
- `/plan-rework N` — turns one big finding into a plan of fix-sized steps,
  writes no code.
- `/run-queue` — walks a whole findings queue: fixes land and commit
  automatically, big items pause once for your go/stop, token cost reported
  per loop. The review→fix pipeline in one command.

### Model routing

Orchestration and analysis run on the main model, implementation on a cheaper
one, visual judgment on the strongest — the expensive tier is spent only where
it pays. The orchestrator never implements.

### Tooling

An IDE-index MCP provides semantic code navigation (usages, definitions,
hierarchies) instead of text grep. `scripts/` holds the linters the hooks call
plus benchmark and token-reporting helpers.

## Driving it

### Starting a session

Say what you want; the session bootstraps itself from memory and `todo.md`.
Open a session per phase, not per day: `/clear` when the next task is
unrelated, `/compact` when it continues.

### Saying what you want

- **Be approximate on purpose.** Intent outranks literal words — say what
  "done" looks like, not the steps. Over-specifying gets a worse design
  executed faithfully.
- **Name a goal, not a task list**, for anything multi-step. It plans; you
  approve or redirect the plan.
- **For bugs, just paste it** — error text, failing test, screenshot path.
  Bug reports run autonomously through to the fix.
- **Say when you're low on credits or in a hurry** — small closable items get
  picked over campaign steps that would strand half-done.

### The pipeline

1. `audit <domain>` — produces the ordered findings queue. Costs a lot of
   reading; do it once per domain, not per question.
2. `/run-queue` — walks the queue end to end.
3. `/implement-finding N` or `/plan-rework N` — when you want one item, not
   the queue.

Ad-hoc "fix this" works, but skips the evidence and the ordering — you pay
for that later in rework.

### Questions it will put to you

- **Decisions come batched at checkpoints** — scope, licensing, anything
  irreversible, genuine forks. Options carry outcome / confidence / cost;
  read the confidence line: high-outcome low-confidence usually means "run
  the cheap probe first".
- **Approving a plan that lists heavy compute runs is the go-ahead for exactly
  those runs.** Heavy generation work otherwise waits for you with a wall-time
  estimate; compiles, tests and smoke checks never ask.
- **Correct once.** A correction becomes a memory, loaded every session. If
  you have to repeat one, say so — its trigger gets widened.

### What not to ask for

- **A GUI run** — verification is headless by ruling: offscreen renders,
  judged by the vision tier. Ask for frames, not a window.
- **A test run per change** — the cadence is one suite run per batch plus one
  to confirm.
- **A quick patch around a wall** — flags, shims and dodge-the-rule test
  rewrites are refused by standing instruction. "Blocked" is the useful
  answer.

### Housekeeping

- Say **"save the state"** to end cleanly — notes written, nothing new
  started.
- Ask for the **token report** to see where a campaign's budget went.
- After editing anything under `.claude/`, have it **commit and push** there —
  the directory is invisible to this repo, so an unpushed change exists only
  on this machine.
