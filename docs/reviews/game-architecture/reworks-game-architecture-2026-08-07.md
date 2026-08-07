# Game Architecture Audit (Reworks) — 2026-08-07

Rework-scale companion to `audit-game-architecture-2026-08-07.md`: findings
that need a design pass before anyone writes code. Consumed by /plan-rework.

## Ideal end state

Killer attribution is a property of the damage pipeline, not of which phase
happened to emit the fatal `DamageDealt`: an entity killed by any damage
source — contact, projectile, or PostUpdate-resolved mechanic — credits its
killer identically, and the event-lifetime rule that makes that true is
stated once and enforced by the headless pipeline test.

## Findings (implementation order)

Cross-type queue (mirrored verbatim from
`audit-game-architecture-2026-08-07.md`):

> **rework 1 → finding 1 → finding 2 → finding 3 → finding 4 → finding 5 →
> finding 6.**
>
> rework 1 first: it is the domain's only live-path defect (mechanic kills
> grant no XP) and its design pass touches the `DamageDealt` lifetime that
> finding 1's seed change and finding 2's contract rewrite sit next to —
> settling the lifetime first keeps both fixes from being re-touched.
> Findings 1–6 are mutually independent; they are ordered by impact
> (latent combat correctness, then contract truth, then hot-loop and fence
> work, then docs).

### 1. Mechanic-caused kills never grant XP — killer attribution reads an EventBus already cleared for that death

Carried forward from `reworks-game-architecture-2026-07-15.md` finding 3,
re-verified 2026-08-07 against current code. No plan file exists yet.

- **Evidence (re-verified):** the phase structure is unchanged.
  `MechanicResolveSystem` runs in `Phase::PostUpdate`
  (`server/vordar-server/src/net/mod.rs:123`) and emits `DamageDealt` there
  (`server/vordar-server/src/net/mechanics.rs:107-113`). `DeathSystem` runs
  in `Phase::CollisionResolve` (`game/vordar-game/src/plugin.rs:80`) and
  attributes kills by reading `DamageDealt` from the current tick's
  `EventBus` (`game/vordar-game/src/combat/death.rs:44-53`).
  `ClearEventsSystem` wipes the whole bus at `Phase::Input`, first thing
  every fixed step (`smirk/engine-app/src/flush.rs:12-16`, registered at
  `smirk/engine-app/src/app.rs:96`). A mechanic's `DamageDealt` emitted in
  tick T's PostUpdate is therefore gone before tick T+1's CollisionResolve
  — the first place `DeathSystem` can see the lethal `Health` — so every
  mechanic-caused death loses attribution structurally: no killer, no
  `Killed`, no XP. The headless pipeline test still pins exactly this:
  `mechanic_damage_flows_through_death_but_grants_no_xp`
  (`server/vordar-server/tests/mechanic_pipeline.rs:88-110`,
  `assert_eq!(out.killer_xp, None, ...)`) — it will flip to asserting the
  grant when this rework lands.
- **Ideal:** an entity killed by scheduled-mechanic damage grants XP to the
  caster exactly like a contact/projectile kill — killer attribution must
  not depend on which phase emitted the triggering `DamageDealt`.
- **Gap:** `DamageDealt`'s one-step EventBus lifetime silently assumes its
  consumer phase runs later in the SAME step as the emitting phase; that
  holds for `ContactDamageSystem`/`ProjectileHitSystem` (CollisionResolve,
  before `DeathSystem`) but not for `MechanicResolveSystem` (PostUpdate,
  after it).
- **Suggestion:** design (don't guess) where death detection for
  PostUpdate-phase damage sources should live — candidates worth weighing:
  give `DamageDealt` a two-step lifetime (survive one extra `ClearEvents`
  pass) so next-tick CollisionResolve still sees it; or add a
  PostUpdate-scoped death/XP pass for damage sources that land after
  CollisionResolve; or move `MechanicResolveSystem`'s health mutation
  earlier at the cost of its `SnapshotBroadcastSystem` ordering guarantee
  ("resolve before broadcasting so deaths reach the same snapshot wave",
  `server/vordar-server/src/net/mod.rs:122-123`). Validate the chosen
  design against `RavagerRageSystem`'s same-tick `DamageDealt` read
  (`server/vordar-server/src/net/mod.rs:124-126`,
  `game/vordar-game/src/combat/buff.rs:69-79`) so mechanic hits keep
  granting rage stacks.
- **Outcome:** `7/10` — the last damage source whose kills vanish from
  progression; also settles the cross-phase event-lifetime rule every
  future PostUpdate damage source will inherit.
- **Confidence:** `9/10` — the defect is demonstrated by a committed,
  currently-green pipeline test that asserts the missing grant, and the
  phase chain was re-read end-to-end this pass.
- **Cost:** `5/10` — the code delta is small but the lifetime decision
  ripples into rage attribution and the event-bus contract, hence the
  design pass.
- **Path:** design pass on the `DamageDealt`/killer-attribution lifetime
  across the CollisionResolve/PostUpdate boundary → plan document →
  /implement-finding steps, flipping
  `mechanic_damage_flows_through_death_but_grants_no_xp` to assert the
  caster IS granted XP.

## Carried forward from previous report

Finding 1 above is `reworks-game-architecture-2026-07-15.md` finding 3,
carried forward re-verified (evidence refreshed 2026-08-07; the pinning
test and all four phase registrations re-read).

## Resolved since last report

- 07-15 reworks finding 1 (multiplayer population & progression model) —
  rework 1 executed 2026-07-15 (6 steps); per-player `Xp` verified live.
  Plan file deleted with this supersession.
- 07-15 reworks finding 2 (PostUpdate key latches / edge-drain lifetime) —
  rework 2 executed 2026-07-16 (4 steps); PostUpdate/Last drain and
  converted consumers verified. Plan file deleted with this supersession.

Verification details for both are in `audit-game-architecture-2026-08-07.md`
§ "Resolved since last report".
