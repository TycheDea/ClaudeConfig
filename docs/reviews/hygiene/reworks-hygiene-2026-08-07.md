# Code Hygiene Audit (Reworks) — 2026-08-07

Rework-scale companion to `audit-hygiene-2026-08-07.md`. This run produced **no
rework-scale findings**: the two large-module hotspots the last report designated
for design passes (engine-net's client transport, the server's receive system) both
landed their reworks, and no new file or module in the sweep needs a design pass
before code can change — every 2026-08-07 finding is a bounded fix in the fixes
file.

## Ideal end state

Every source file in the workspace has one responsibility its name predicts, with
seams promoted to named modules and functions — a state the tree now substantially
holds after the 2026-07-14/15 rework cycles; keeping it requires only the fix-scale
vigilance recorded in the fixes file.

## Findings (implementation order)

None this run.

Cross-type queue (mirrored verbatim from `audit-hygiene-2026-08-07.md`):

> **finding 1 → finding 2 → finding 3 → finding 4 → finding 5 → finding 6 →
> finding 7.**
>
> Findings 1–2 (comment-only) go first so later diffs land in files whose comments
> are already honest. Findings 3–7 have no dependencies between them and are ordered
> by impact: the two hot-path dedups (server cast dispatch, transport token bucket)
> before the tooling-bin dedup, naming, and the scaffolding decision.

## Carried forward from previous report

None.

## Resolved since last report

- **Rework 1 (2026-07-15): engine-net decomposition** — landed
  (`plan-hygiene-rework-1-2026-07-15.md`, now superseded): `smirk/engine-net/src/`
  holds `clock.rs` (the sync filter) and a unified `impair.rs`; `client.rs` is 373
  lines of transport and task graph. The plan's consciously-descoped
  `handle_connection` staging note is re-anchored as bounded fixes finding 4 in the
  new fixes file (token-bucket dedup + optional stage naming), not a rework.
- **Rework 2 (2026-07-15): receive.rs seam promotion** — landed
  (`plan-hygiene-rework-2-2026-07-15.md`, now superseded): `NetReceiveSystem::run`
  dispatches to `handle_login`, `dispatch_cast`, `complete_db_load`,
  `respawn_dead`, and `drain_intents` as free functions
  (`server/vordar-server/src/net/receive.rs:63-660`), the exact target shape the
  rework specified.
