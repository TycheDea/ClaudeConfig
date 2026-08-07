# Game Architecture Audit — 2026-08-07

Full fresh sweep: one tick traced end-to-end (winit `app_loop.rs` and
`run_headless` entry → `Scheduler::run_tick` single-clock loop → Input
(ClearEvents, net receive/casts) → PreUpdate → Update (AI, leap, camps,
world events, movement) → SpawnFlush → Collision (cell update, broadphase,
narrowphase) → CollisionResolve (separation, projectiles, contact, death,
XP) → DespawnFlush (death broadcast, XP carry, flush) → PostUpdate
(mechanics, rage, transfer, snapshots, autosave, edge drain) → RenderSync/
Render), plus every file in `smirk/engine-core`, `smirk/engine-app`,
`smirk/engine-physics`, `smirk/engine-audio` (still a 1-line stub), `game/`
(vordar-game, chapters 01–03), the simulation-relevant parts of
`client/vordar-client` and `server/vordar-server`, and the shipped content
config (`content/zones/zones.ron`, `events.ron`, chapter defs, prefabs).
`docs/architecture.mmd` (in `.claude/docs/`) matches the code at its stated
altitude; no divergence.

Gate note: the dispatch brief stated `scripts/lint-findings.sh` no longer
exists; it does exist and was run on both new reports (green). Tension
reported to the orchestrator rather than skipping the gate.

What held up under deliberate attack this pass, for the record: the
single-clock scheduler (interleaved fixed phases, duplicate-type and
unresolved-target panics, First/Last unified in the sort); the contact side
rule with pass-through tests; `step`/`predict_step`/`anchored_push` shared
verbatim by MovementSystem, reconciliation replay, and mechanic rewind
(dash-truth history included), with live-vs-predicted equivalence tests;
canonical-sorted collision events; incremental spatial-grid diffing; boot
panics on degraded prefab libraries and dangling event prefab names; the
fixed-delay playback cursor with capped extrapolation and pinned
jitter/loss/stall behavior; per-player Xp with carry-across-respawn; and the
chapter-03 collision-mirrors-props discipline, which is lint-enforced
(`town_prop_collision_matches_footprints`), not convention.

## Ideal end state

A simulation where every rule is stated once and is true everywhere it is
stated: damage rolls are independent per hit while staying deterministic;
the mutation contract in `traits.rs` matches every live spawn path; hot
per-tick loops do no work whose result is discarded (idle-enemy scans,
re-inserted components); the planar-separation design is fenced by a content
lint instead of authoring care; and no doc line describes the pre-rework
scheduler. At that point the only open architectural debt in this domain is
rework 1's cross-phase damage-attribution lifetime.

## Findings (implementation order)

Cross-type queue (mirrored verbatim in
`reworks-game-architecture-2026-08-07.md`):

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

### 1. Contact-damage crit seed is constant per attacker–target pair

- **Evidence:** `game/vordar-game/src/combat/contact_damage.rs:72` — the
  damage seed is `attacker.to_bits().get() ^
  target.to_bits().get().rotate_left(21)`, a pure function of the two
  entity ids; `compute_damage`'s crit roll is a pure function of that seed
  (`game/vordar-game/src/combat/stats.rs:69-74`, splitmix64 at `:86-92`).
  So the same pair produces the identical crit outcome on every contact for
  both entities' lifetimes. The other two damage sites already vary per
  hit: projectiles mix the per-bolt entity id
  (`game/vordar-game/src/combat/projectile.rs:144`) and mechanics the
  per-cast mechanic id (`server/vordar-server/src/net/mechanics.rs:102`).
  Latent today: a grep of `content/` shows `CombatStats` only on
  `content/prefabs/ravager.ron:16` (the player), and players carry no
  `ContactDamage` — so no live contact hit currently reaches the crit
  branch (attacker stats `None` skips it).
- **Ideal:** every hit rolls an independent, deterministic crit — seeds
  vary per hit occurrence, never per pair, with no wall clock and no local
  RNG (DESIGN.md §6).
- **Gap:** the first enemy prefab that gains `CombatStats` with
  `crit_chance > 0` will either always-crit or never-crit a given target,
  forever, through the melee path only — an invisible content trap in the
  shared damage pipeline.
- **Suggestion:** fold a monotone per-hit component into the contact seed —
  a sim-tick counter resource incremented once per fixed tick (sandbox-safe,
  unlike `WorldTime` which only the server publishes) XORed into the seed
  at the contact site. Projectile and mechanic sites need no change.
- **Outcome:** `6/10` — closes a whole class of latent per-pair
  determinism-degeneracy before any content trips it.
- **Confidence:** `8/10` — the roll being pair-constant is arithmetic read
  directly off the seed expression, not a runtime observation; the latency
  claim rests on the content grep. A fixture with `crit_chance: 0.5`
  showing differing rolls across two contacts would make it 10.
- **Cost:** `2/10`
- **Path:** (1) add the tick-counter resource (or reuse one if a suitable
  monotone already exists app-wide); (2) fold it into the contact seed;
  (3) test: same attacker/target pair, two contact events, crit outcomes
  differ across hits at `crit_chance: 0.5`; (4) game suite green.

### 2. The mid-frame mutation contract over-claims — the receive edge and AI spawn directly (user-decides)

- **Evidence:** `smirk/engine-core/src/traits.rs:78-79` states "Systems
  never mutate the world mid-frame. Push requests here instead." Live
  direct-mutation sites inside systems: `spawn_projectile`
  (`game/vordar-game/src/combat/projectile.rs:55-65`, direct
  `spawn_prefab` + `insert_one`) called from `EnemyAISystem`
  (`game/vordar-game/src/enemies/mod.rs:181-195`, Update), from
  `NetReceiveSystem` (`server/vordar-server/src/net/receive.rs:116-118`,
  Input) and from `SandboxCastSystem`
  (`client/vordar-client/src/sandbox.rs:79-83`, Input); `dispatch_cast`
  spawns `Mechanic` entities directly (`receive.rs:343-353` and
  `:406-416`) plus `insert_one(LeapImpulse)` (`:417-420`) in Input; the
  login/respawn paths spawn the player prefab directly (`receive.rs:506`,
  `:594` — these genuinely need the `Entity` synchronously for
  `PlayerConn`/Welcome). The 2026-07-15 audit's finding 7 fixed
  CampSystem/MechanicResolve precisely so "the traits.rs comment then
  states a rule with zero exceptions" — the remaining sites make it
  over-claim again.
- **Ideal:** contract text and code agree, and entity visibility never
  depends on registration order within a phase: a spawn is visible either
  to nobody until SpawnFlush or to a named, documented exception.
- **Gap:** a bolt or mechanic spawned mid-phase is visible only to
  later-registered systems of that phase (e.g. an EnemyAI bolt is seen by
  `MovementSystem` this tick only because AI registers before Update/Last);
  whether that matters is decided by silence, not by the stated rule.
- **Suggestion:** two coherent resolutions — the user picks:
  (a) route the queueable sites through `SpawnQueue` (mechanic spawns are
  semantics-free: resolve runs in PostUpdate, after the same tick's
  SpawnFlush; projectile spawns shift their first integration by one tick,
  ~0.3 units at bolt speed 18) and rewrite `traits.rs` to name the two
  sanctioned direct sites (login/respawn player spawn; `OnDeath` callbacks
  via `SpawnContext`); or (b) keep the code and rewrite the contract to the
  true rule (queues are mandatory for systems spawning during query
  iteration or without a same-phase consumer audit; borrow-safe edge code
  may spawn directly at the price of registration-order-dependent
  visibility). (a) is the cleaner end state.
- **Outcome:** `6/10` — removes a silent ordering hazard and makes the
  engine's central mutation rule true.
- **Confidence:** `7/10` — code read; the ordering-dependence mechanism is
  structural and the phase math (SpawnFlush before Collision/PostUpdate)
  was verified against the scheduler, but no misordering bug is currently
  observable, so the value is preventive.
- **Cost:** `3/10`
- **Path:** (1) user picks (a) or (b); (2) if (a): queue the mechanic
  spawn (no behavior change), queue the projectile spawn accepting the
  one-tick flight delay or offsetting the origin by one tick of velocity,
  and update any flight-distance-sensitive tests; (3) rewrite
  `traits.rs:78-79` to the chosen rule naming its exceptions; (4) game +
  server suites green.

### 3. (micro) EnemyAI's passive short-circuit is dead below 64 players

- **Evidence:** `game/vordar-game/src/enemies/mod.rs:126-148` — the branch
  order `provoked || few_players || aggro_range > GRID_AGGRO_MAX` routes
  every enemy through the O(P) global nearest-player scan whenever the zone
  has fewer than `GRID_PLAYER_MIN` (= 64, `:59`) players, so the `None` arm
  (`:146-147`, comment "passive and unprovoked — no lookup at all") is
  unreachable in any current deployment; passive sentinels/mossbacks pay a
  per-tick nearest-scan whose result the `engaged` check (`:158`) then
  discards.
- **Ideal:** passivity short-circuits before any target lookup, and the
  comment is true on every path.
- **Gap:** wasted per-idle-enemy work on the common path, and a comment
  that describes a branch the control flow can't reach below 64 players.
- **Suggestion:** hoist `if !provoked && enemy.aggro_range == 0.0 {
  velocity.linear = Vec3::ZERO; continue; }` above the target-selection
  branch.
- **Outcome:** `5/10` — idle camps become free at any player count, which
  is most of an MMO zone most of the time.
- **Confidence:** `8/10` — the control flow is unambiguous on a read;
  behavior is already pinned by `passive_enemy_ignores_nearby_player`, so
  the change is enumeration, not diagnosis.
- **Cost:** `1/10`
- **Path:** (1) hoist the guard; existing enemy AI tests green. Single
  file, covered by existing tests — micro.

### 4. Separation is XZ-planar while contact detection is 3D — overhead solids can eject walkers sideways

- **Evidence:** `game/vordar-game/src/motion/separation.rs:87-101` — the
  AABB-AABB MTV computes only `overlap_x`/`overlap_z`; the sphere-AABB arm
  (`:126-135`) is explicitly planar. Pair detection is fully 3D
  (`smirk/engine-physics/src/aabb.rs:13-17`,
  `smirk/engine-physics/src/narrowphase.rs:136-143`). Chapter 3 ships aloft
  anchored solids directly over walkable paths:
  `content/chapters/chapter03/prefabs/gate_head.ron:8` (spans y 3.6–6.23
  over the road), `chapel_lintel.ron:7` (y 3.2–7.5 over the chapel door),
  `chapel_roof.ron:7` (an 8×0.6×7 slab at y 10.2). Today's clearance over a
  player (y −0.5–0.5) is generous, but nothing checks it.
- **Ideal:** the planar-resolution design is a stated rule with a fence: an
  overhead Solid whose Y span dips into the movement band is a content-lint
  failure at authoring time, never a runtime mystery shove.
- **Gap:** an overhead box authored or resized to graze head height
  produces a 3D overlap whose Y penetration separation ignores — the MTV
  resolves horizontally, up to the slab's full horizontal overlap (meters,
  for the roof slab), shoving the walker sideways. The discipline currently
  lives only in per-prefab comments ("the passage below stays open").
- **Suggestion:** add a content-lint assert beside
  `town_prop_collision_matches_footprints`
  (`game/vordar-game/tests/content_lint.rs:997`): every chapter
  `initial_spawns` hitbox either intersects the ground band (a wall —
  expected) or clears y ∈ [ground, character top] by a stated margin. Also
  state the XZ-only resolution rule in `separation.rs`'s module header —
  today only the mixed-shape arm says it.
- **Outcome:** `5/10` — converts an authoring convention into an invariant
  before door/arch content multiplies.
- **Confidence:** `7/10` — the planar-vs-3D asymmetry is a direct read;
  today's clearances were computed from prefab RON, not reproduced at
  runtime. A unit test overlapping a walker with a low slab and observing
  the horizontal shove would raise it.
- **Cost:** `2/10`
- **Path:** (1) the lint (derive the movement band from the player prefab's
  hitbox); (2) falsify it once with a fake y=1.0 slab; (3) the header
  sentence; (4) content lint suite green.

### 5. NetMotion is re-inserted on every replicated entity every tick

- **Evidence:** `client/vordar-client/src/net/interpolate.rs:111-121` —
  each Update tick collects `(Entity, Vec3)` into a fresh `Vec` and calls
  `world.insert_one(entity, NetMotion { .. })` for every entity with a
  `NetBuffer`; AOI entry already has an insertion point where `NetBuffer`
  is attached (`client/vordar-client/src/net/apply.rs:106-119`).
- **Ideal:** steady-state playback cost is a component write through the
  query; insertion happens once, at AOI enter.
- **Gap:** per-tick per-entity `insert_one` (type-id + archetype lookup;
  in-place rewrite since the component already exists) plus a per-tick
  `Vec` allocation, scaling with AOI population at 60 Hz — work whose only
  purpose is to avoid a one-line seed at spawn.
- **Suggestion:** insert `NetMotion::default()` beside `NetBuffer` at AOI
  enter; `NetInterpolateSystem` queries `(&NetBuffer, &mut Transform, &mut
  NetMotion)` and the scratch `Vec` is deleted.
- **Outcome:** `4/10` — client hot-path hygiene; the win grows with AOI
  crowd size.
- **Confidence:** `7/10` — code read; the in-place-rewrite claim is hecs
  semantics for an already-present component, not measured. A bench delta
  on `client_netcode.rs` would confirm the magnitude.
- **Cost:** `1/10`
- **Path:** (1) seed at enter; (2) widen the query, delete the collect
  loop; (3) presentation/locomotion tests green (NetMotion consumers
  unchanged).

### 6. (docs-only) Pre-rework "per-phase / per-frame" language survives in engine-app docs

- **Evidence:** `smirk/engine-app/src/time.rs:3` — "Per-phase accumulators
  and fixed_dt live inside the Scheduler": per-phase accumulators were
  deleted by the single-clock rework (`smirk/engine-app/src/scheduler.rs:
  100-104` documents one app-wide accumulator).
  `smirk/engine-app/src/lib.rs:6` — "EventBus: typed single-frame events"
  and `:7` — "drain SpawnQueue and DespawnQueue each frame": both are per
  fixed step (`smirk/engine-app/src/events.rs:1-3` already states the
  truth; the flush systems run in fixed phases).
- **Ideal:** every doc line describes the landed single-clock design —
  stale claims are a comment-policy violation (project CLAUDE.md §6).
- **Gap:** the next reader of the crate root or `Time` learns the deleted
  architecture.
- **Suggestion:** sweep the three lines to single-clock vocabulary ("one
  app-wide accumulator", "single-fixed-step events", "each fixed step").
- **Outcome:** `3/10`
- **Confidence:** `9/10` — pure text-vs-code comparison, both read this
  pass.
- **Cost:** `1/10`
- **Path:** (1) the three lines; done. No source edits.

## Carried forward from previous report

Rework-scale: reworks finding 3 of 2026-07-15 (mechanic-kill XP
attribution) carries forward re-verified as **rework 1** in
`reworks-game-architecture-2026-08-07.md` — see that file for the fresh
evidence. No fix-scale findings carry: the 2026-07-28 queue was fully
cleared 2026-08-02.

## Resolved since last report

- `audit-game-architecture-2026-07-28.md` findings 1–9: all done
  2026-08-02 per its queue note; spot re-verified against current code this
  pass — contact side rule + pass-through tests
  (`game/vordar-game/src/combat/contact_damage.rs:44-51`, `:103-132`);
  event-prefab boot validation (`server/vordar-server/src/lib.rs:103-123`);
  single-clock API with `TickRate`/`set_phase_rate` deleted for
  `set_fixed_hz` (`smirk/engine-app/src/scheduler.rs:141-143`);
  duplicate-system-type panic (`scheduler.rs:164-168`); resource-dialect
  unification (resolved opposite to its own Ideal per user ruling — the
  `Send + Sync` bound came OFF `App::insert_resource`,
  `smirk/engine-app/src/app.rs:174-180`); prefab-library boot health
  (`server/vordar-server/src/lib.rs:87-96`,
  `smirk/engine-core/src/prefab.rs:159-193`); grid rename + honest header
  (`smirk/engine-core/src/spatial.rs:1-9`, `:58`); cast-time resolve-slice
  lint (`game/vordar-game/tests/content_lint.rs:1306-1331`); headless
  pipeline test (`server/vordar-server/tests/mechanic_pipeline.rs`).
- `reworks-game-architecture-2026-07-15.md` finding 1 (population &
  progression model): rework 1 executed 2026-07-15 per its queue note;
  per-player `Xp` component verified live
  (`game/vordar-game/src/progression.rs:23`) with respawn carry
  (`server/vordar-server/src/net/receive.rs:618-631`) and persistence
  (`server/vordar-server/src/net/mod.rs:306-315`). Its plan file
  (`plan-game-architecture-rework-1-2026-07-15.md`) is deleted with this
  supersession.
- `reworks-game-architecture-2026-07-15.md` finding 2 (PostUpdate key
  latches): rework 2 executed 2026-07-16; verified — edge sets drain once
  per fixed step at PostUpdate/Last
  (`smirk/engine-app/src/input.rs:169-176`,
  `smirk/engine-app/src/app.rs:98`), and MenuSystem/CycleCameraSystem
  consume `just_pressed` with their hand-rolled latches gone
  (`smirk/engine-renderer/src/menu.rs:281-284`,
  `smirk/engine-renderer/src/camera.rs:401`). Its plan file
  (`plan-game-architecture-rework-2-2026-07-16.md`) is deleted with this
  supersession.
