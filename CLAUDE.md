# CLAUDE.md
## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Comment Policy

**A comment states a constraint or a why the code itself cannot show — never history, never narration.**

Allowed, and only these:
- **Constraint the code cannot show** — an invariant, guarantee, or ordering requirement enforced by convention rather than the type system. Exemplar: `server/vordar-server/src/db.rs:218-221` (the `Drop` impl's comment states that dropping the sender closes the channel before the worker drains pending saves, so shutdown is safe).
- **Why not derivable from the code** — a fact about the world the reader cannot get from the next line alone. Exemplars: `client/vordar-client/src/weapons.rs:204-206` (the socket matrix bakes a cm→m scale, so only rotation+translation carry over to weapon transforms); `game/vordar-game/src/motion/movement.rs:9-15` (why `PLAY_RADIUS` is set where it is, relative to the client's ground mesh).
- **Module header** — intent plus scheduling/ownership contracts at the top of a file. Exemplar: `smirk/engine-app/src/scheduler.rs:1-11`.
- **Spec-clause reference** — a pointer into a living spec doc that anchors a stated constraint: `DESIGN.md §N`, `docs/visual-quality.md` clause ids (`VQ-B2` in a lint assert, "HDR emissive (VQ-C3)"). The reference must ride a constraint; a bare tag with no constraint, or a tag explaining when/why code was written, is provenance and forbidden.

Forbidden:
- Narration of the next line — a comment that just restates the code below it.
- PR/change-log talk — finding/rework/audit citations, "used to be", "now we", roadmap tags (`VQ-*`, `Phase N`) used as provenance. Provenance belongs to git history and `docs/reviews/`, not to source.
- Restated function/struct signatures.
- Stale claims — a comment asserting something the code no longer does.
- TEMP scaffolding that outlives its stated removal condition.

## 6. Uncertain Decisions Escalate

**Not clearly forced by the plan, the code, or a verified fact → escalate. Up the model ladder first, to the user last.**

- **An agent's doubt goes up a tier, never into a guess.** What an agent cannot settle from the code or a verified fact it hands to a deeper-thinking model; that model may route it further up instead of answering. Only a doubt no tier can settle reaches the user.
- **Think twice before asking.** Quality outranks time, tokens and change cost, so a clearly best outcome is not a question — take it and say you took it. Anything with a **reasonable** alternative: AskUserQuestion, don't decide — and reasonable means *close on outcome*, because an option that ends worse is not an alternative, it is a worse plan, however much cheaper it is. The call is the user's by right regardless of the weights when it is theirs to make: scope, licensing, branch/base, anything irreversible.
- **Every option carries three independent weights** in its description: **outcome** (how good the end result is), **confidence** (how sure you are of that outcome, and on what evidence), and **cost** (resources/difficulty). Outcome is scored as if the work were free — cost never discounts it, and the three never merge into one number. Confidence rates the *evidence*, not the appeal: an option that looks best but rests on a code read alone is high-outcome and low-confidence, and must say so. Where confidence is low, name the cheap probe that would raise it — that probe is often the better thing to do first.
- If autonomy forces an in-flight call (mid-rebase, blocked pipeline), keep a running list and present every "decided while unsure" item at the next checkpoint, unprompted.
- Forced or reversible-and-conventional calls proceed without asking — log them if any doubt remains.

## 7. Batched Test Cadence

**Test suites are expensive (time + tokens). Never run them per small change.**

- Cadence: finish a batch of tasks → run the suite ONCE for the batch → fix every failure → run ONCE more to confirm. Two suite runs per batch, not one per change.
- Per-task checks stay cheap and local: script exit codes, output-file existence, compiling the touched crate.
- Applies to subagents too: workers don't run `cargo test --workspace` unless their task IS the batch check.

## 8. Heavy Compute Needs a Go-Ahead

**Ask the user before launching expensive CPU/GPU workloads.**

- Applies to generation runs: textures, HDRIs, meshes, seed sweeps, inference batches — name the expected wall-time when asking.
- Does NOT apply to test suites or compiles. Seconds-scale smoke checks (one small preview, a 2-step verify) are exempt.
- A user-approved plan that explicitly lists its generation runs counts as the go-ahead for exactly those runs; bundle asks into existing checkpoints rather than interrupting per run.

## 9. Compact at Phase Gates

**Never carry a spent context into the next phase.**

- At every phase gate: persist all state to files (subplan struck, todo.md updated, "decided while unsure" delivered), then end the turn telling the user to `/compact` before the next phase starts — or `/clear` instead when the next task is unrelated to the finished one (nothing in the conversation is worth carrying).
- Mid-phase, when context reaches ~150k tokens, do the same at the next clean checkpoint — unless the task in flight genuinely needs the accumulated context to finish.
- A compact point must be self-sufficient: everything needed to resume lives in tasks/ files and commits, never only in conversation.

## 10. Exclude `reference/` from Searches

`reference/` contains downloaded external projects for study only — exclude it from all searches and sweeps (including raw shell recursion like `Get-ChildItem -Recurse` / `find`) unless the task is explicitly analyzing those projects.

---

IMPORTANT: When applicable, prefer using rustrover-index MCP tools for code navigation and refactoring.