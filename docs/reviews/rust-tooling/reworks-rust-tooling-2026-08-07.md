# Rust & Tooling Audit (reworks) — 2026-08-07

## Ideal end state

Same as `audit-rust-tooling-2026-08-07.md`: a lint-gated workspace whose
per-crate clippy scopes are green, whose lockfile and majors are current or
pinned with living reasons, and whose bench gate log and baseline describe
the tree they claim to.

## Findings (implementation order)

**No rework-scale findings this audit.** Everything found is a bounded diff a
worker can land surgically. The sweep re-checked the rework-scale suspects
the 07-17 audit cleared and they remain clear:

- **Workspace architecture:** the engine→game dependency direction still
  holds across all 15 manifests, including the two members added since
  (chapter-03, test-support); test-support's dev-cycle back into
  vordar-server remains the documented intentional exception
  (`server/vordar-server/Cargo.toml:44-46`). engine-audio is still the empty
  stub (`smirk/engine-audio/src/lib.rs:1`) with a clean two-line manifest —
  no dead dep, no structure problem.
- **Feature architecture:** the offscreen/bench-internals private-internals
  pattern is consistent across engine-renderer, vordar-client, and
  vordar-server; its one defect (ungated offscreen-only items) is fixes
  finding 2, an attribute-level diff.
- **Error handling:** production resource lookups run through
  `Resources::expect`/`expect_mut` (`smirk/engine-core/src/traits.rs:42-49`);
  the surviving `.unwrap()` density outside `#[cfg(test)]` is a handful of
  mutex/invariant sites (e.g. 2 in `server/vordar-server/src/db.rs`, 0 in
  vordar-game's world modules) — no redesign warranted.
- **Lint posture:** pedantic wholesale stays rejected per the 07-17
  measurement (1,429 hits, near-all style noise); the default-set gate is
  green workspace-wide.

Cross-type queue (mirrored verbatim from `audit-rust-tooling-2026-08-07.md`):

> **finding 1 → finding 2 → finding 3 → finding 4 → finding 5 → finding 6 →
> finding 7.**
>
> Finding 1 goes first because it repairs the bench gate's durable log before
> any later step runs that gate. Finding 2 makes scoped clippy usable as the
> per-crate verification every later diff cites. 3 precedes 4 so the lock
> refresh resolves through single declarations. 4 precedes 5–6 so the
> compatible-refresh diff is isolated from the semver-major diffs. 7 is last
> because 4, 5, and 6 each move codegen and would stale a fresh baseline.

## Carried forward from previous report

- **Finding 14 (reworks-rust-tooling-2026-07-17)** — carried into the new
  fixes file as `audit-rust-tooling-2026-08-07.md` finding 2, re-verified
  red 2026-08-07 and root-caused to ungated offscreen-only items; it is
  fix-scale, so it leaves this reworks file.

## Resolved since last report

- **Finding 13 (reworks-rust-tooling-2026-07-17)** — resolved:
  `cargo clippy -p vordar-client --all-targets -- -D warnings` exits 0 on
  rustc 1.97.1 (run 2026-08-07); the `float_literal_f32_fallback` sites are
  gone.
