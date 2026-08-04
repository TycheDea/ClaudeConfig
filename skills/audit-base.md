# Shared audit contract

Every `audit-*` skill runs under this contract. The invoking skill supplies
the persona and these parameters: the **domain** slug (also its report folder
name under `docs/reviews/`), the **report title**, the **ordering impact
axis**, the **ideal-end-state hint**, the **sweep** instruction, plus its
Scope, its "What to hunt for" list, and any extra requirements. Extras add to
this contract, never replace it.

## Mission

Find improvements and suggestions — of any kind, at any scale — within the
skill's Scope. You implement nothing. Your sole deliverable is a written
report.

## Non-negotiables

1. **No laziness.** You read the actual code and files, not just their names. Every finding cites concrete evidence (`file:line`, a specific entry, a measured number). Generic advice that could apply to any repo is forbidden — if a finding doesn't reference something specific you saw here, delete it. Do not stop early because the sweep is long; incomplete coverage is a failed audit.
2. **The bar is the best possible final state.** Judge everything against the top of the top — the ideal end state this project could reach in the skill's domain. Never write "this is enough", "good enough for now", "sufficient for the current state", or any equivalent middle-ground framing. If something falls short of the ideal, it is a finding, no matter how many steps lie between here and there. Distance to the ideal is recorded, never used as an excuse to lower the bar.
3. **Report only. No implementations.** The only files you may create are the report files, and the only files you may delete are the superseded prior reports in your own domain folder (see "Superseded reports"). You must not modify source, configs, docs, diagrams, scripts, schemas, or assets — not even "trivial" fixes you notice along the way.
4. **Routing stays flat.** Exactly one routing level between an invoked skill and the text it acts on; never a skill whose job is to select another skill. A finding proposing a second level — a meta audit skill routing to the eight `audit-*` skills, a repo map routing to per-crate sub-skills — is struck on sight, not argued.

## Method

1. Check `docs/reviews/<domain>/` for the most recent `audit-<domain>-*.md` and `reworks-<domain>-*.md` reports. Carry forward every unresolved finding (re-verify each; drop resolved ones and say so).
2. Sweep the full Scope, the way the skill's **sweep** instruction describes. Read implementation, not tests: stop at `#[cfg(test)]` modules and `tests/` bodies unless the skill's domain is itself test quality, or a specific finding needs a test as evidence — then window into exactly that test (measured 2026-07-15: test bodies were ~37% of an audit's read volume and produced zero findings).
3. For each finding, define the ideal end state first, then measure the gap.
4. Weigh findings by the skill's **ordering impact axis** — but ORDER them in the report by implementation order: a finding goes before another when implementing it first makes the other easier, safer, or properly testable (test/tooling infrastructure and prerequisite mechanisms first, dependents after). Among findings with no dependency between them, higher impact goes first. Never order by ease of fixing. State the reason inline (e.g. "before finding 5: provides the impairment knob its test needs") whenever a dependency, not impact, decided the position.
5. Headless verification only — never launch the game. Reason from code and files; where a claim needs runtime confirmation, say exactly what test or measurement would confirm it.

## Report

Split findings into two categories and two files under `docs/reviews/<domain>/`
(create the folder if it doesn't exist; today's date):

- `docs/reviews/<domain>/audit-<domain>-YYYY-MM-DD.md` - **fixes and small changes**:
  findings a worker can land surgically in one run - a bounded diff plus a regression
  test, no new subsystem, no schema/protocol redesign, no cross-crate architecture
  shift.
- `docs/reviews/<domain>/reworks-<domain>-YYYY-MM-DD.md` - **reworks and big new
  features**: findings that need a design pass before anyone should write code (new
  subsystem, schema/protocol change, auth, architecture shift). These are consumed by
  /plan-rework, which turns one rework into a plan of fix-sized steps that
  /implement-finding can then execute one by one.

When one finding contains both (a surgical step plus rework-scale follow-ons), put the
surgical step in the fixes file and the follow-ons in the reworks file, each referencing
the other. Number findings independently within each file. The implementation-order
note is ONE cross-type sequence spanning BOTH files - dependencies cross the
fix/rework boundary (a rework can be the prerequisite of a fix and vice versa) - so
write a single ordered queue mixing `finding N` (fixes file) and `rework N` (reworks
file) entries, placed under the fixes file's "## Findings (implementation order)"
heading and mirrored verbatim in the reworks file. A rework whose own gate is unmet
(e.g. gated on a measurement not yet taken) is listed as parked with its gate stated,
not given a position. A run-queue stop line has the form
`**STOP** <item> · <tier> · <category> · <attempted> · <gate>`, where
`<category>` is one of `blocked`, `stalled`, or `exhausted`, and is part
of the note's contract: carry it forward verbatim when a fresh audit
rewrites the queue note, and only drop it once the named gate is re-verified
green. A `premise-falsified: <item>[, <item>]` clause can appear in mark-done
strikes when a step's execution contradicted a stated premise; carry this
forward verbatim as well. Both files
use this structure (the skill may add finding
bullets — e.g. a Tradeoffs bullet — but never remove these):

```
# <Report title> — YYYY-MM-DD

## Ideal end state
<2–5 sentences: what "top of the top" looks like — see the skill's ideal-end-state hint>

## Findings (implementation order)
### 1. <title>
- **Evidence:** file:line references and what you observed
- **Ideal:** what the best possible version looks like
- **Gap:** why the current state falls short
- **Suggestion:** concrete direction (no changes made — this is a recommendation)
- **Outcome:** `N/10` — how good the end state is once implemented, scored as if the work were free
- **Confidence:** `N/10` that Outcome is right, then the clause it rests on — what was measured, what comparable case it argues from, or that it is a code read alone. Confidence is about the *evidence*, never about enthusiasm: an 8/10 outcome read off a file with nothing measured is low confidence, and saying so is the point of the field. Never raise it to make a finding look stronger; instead name what would raise it. A `10/10` claims the outcome is already demonstrated, so it is only available once something has been run.
- **Cost:** `N/10` — resources/difficulty to get there (10 = hardest); never discounts Outcome, and the two never merge into one number
- **Path:** the steps from here to the ideal, however many there are

## Carried forward from previous report
<unresolved prior findings, re-verified>

## Resolved since last report
<prior findings that no longer apply>
```

Every finding must be actionable by a developer who reads only the report.
Before superseding old reports, run `bash scripts/lint-findings.sh <new report
path>` as the close-out gate for Non-negotiables item 1's anchor clause, and
fix any violation it flags.

### Finding tags

Findings may include tags in the title to mark special properties:

- **(docs-only)** — changes only documentation, diagrams, or comments; no source edits.
- **(user-decides)** — the Path contains a decision (multiple valid alternatives) that the user must make. When the orchestrator launches a loop containing tagged findings, all user-decides questions are batched and asked at launch, before any implementation begins. This prevents mid-loop stalls and defaults.
- **(micro)** — strictly enumerated, single-file, needs no new test (an existing gate covers it). The orchestrator applies these inline without spawning a worker (adopted 2026-07-15 — the ~35–38k spawn boot exceeds a micro diff ~100×). Tag ONLY when all three criteria hold; a finding that needs any diagnosis, a second file, or a new test is never micro.

### Same-day reruns

A rerun of an audit on the same date does not create a new report file — it
extends that day's existing `audit-<domain>-YYYY-MM-DD.md` with an explicitly
labeled addendum section (new findings numbered continuing the existing
sequence, same Evidence/Ideal/Gap/Suggestion/Outcome/Confidence/Cost/Path format) and extends the
queue note in place, with a one-line label saying which pass added them (e.g.
"Finding 19 was added by the same-day third-pass sweep").

## Superseded reports

After both new files are written, delete every older `audit-<domain>-*.md` and
`reworks-<domain>-*.md` in the folder. This is safe only because step 1 already
re-verified every prior finding: anything still open was carried forward into
the new report, everything else is resolved, and git history keeps the old
text. Also delete each `plan-<domain>-rework-*.md` whose rework you verified
resolved. A plan whose rework carries forward stays in place, and the
carried-forward finding must name that plan file, so the link survives the
renumbering. If you could not re-verify something (e.g. a parked rework whose
gate you can't evaluate), carry it forward as-is and still delete the old
report — the new report is always the single live one per domain.
