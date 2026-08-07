# Code Hygiene Audit — 2026-08-07

Third run. The entire 2026-07-15 queue (findings 1–20 plus reworks 1–2) landed
between the runs — every prior finding re-verified resolved against current code;
see "Resolved since last report". This run swept the workspace fresh: every crate's
module tree read, the largest and newest files read (renderer SSAO/culling/camera,
the five review bins, the decomposed server `net/` family, engine-net's post-rework
shape, chapter crates, content tree). `bash scripts/lint-comments.sh` ran clean —
**0 hits** — so the provenance-tag class that dominated the last two audits is
extinct; what remains is a new, smaller defect class created by the docs→ClaudeConfig
repo move, plus duplication that grew with the new code.

Gate note: the dispatch brief stated `scripts/lint-findings.sh` no longer exists; it
does exist (alongside `lint-comments.sh`) and was run on both report files before
superseding — see the close-out note at the end.

## Ideal end state

Every comment states a constraint or a why the code cannot show, and every pointer in
a comment resolves — including pointers into the `.claude` docs repo, which must
survive doc moves or be replaced by their constraint core. No algorithm exists twice
in one file; no plumbing helper exists five times across sibling bins when a shared
module already exists for exactly that. Every file's name predicts its contents, and
the System/naming conventions hold in tests and harness code exactly as in src.

## Findings (implementation order)

Cross-type queue (mirrored in `reworks-hygiene-2026-08-07.md`):

> **finding 1 → finding 2 → finding 3 → finding 4 → finding 5 → finding 6 →
> finding 7.**
>
> Findings 1–2 (comment-only) go first so later diffs land in files whose comments
> are already honest. Findings 3–7 have no dependencies between them and are ordered
> by impact: the two hot-path dedups (server cast dispatch, transport token bucket)
> before the tooling-bin dedup, naming, and the scaffolding decision.

### 1. Dead doc pointers: the docs→ClaudeConfig move broke six source citations

- **Evidence:** the game repo's `docs/` and `tasks/` trees moved to the `.claude`
  repo (game-repo commit `5e251c0` "Remove docs folder (moved to ClaudeConfig)";
  game-repo `docs/` now holds only `observability/`). Six comment citations still
  use the old paths:
  - `client/vordar-client/src/bin/asset_inspect.rs:6` and
    `client/vordar-client/src/bin/zone_review.rs:9` cite
    `tasks/lessons/2026-07-23-review-in-engine-at-gameplay-framing.md` — this file
    no longer exists anywhere (checked both repos; `.claude/tasks/` has no
    `lessons/` directory).
  - `client/vordar-client/src/bin/zone_review.rs:372` cites
    `docs/reviews/town/p24-layout-review-2026-07-31.md` §3 as the source of a
    framing threshold — exists only at `.claude/docs/reviews/town/`.
  - `game/vordar-game/tests/content_lint.rs:2` cites `docs/visual-quality.md` —
    the living spec every VQ assert in that file anchors to — exists only at
    `.claude/docs/visual-quality.md`.
  - `game/vordar-game/tests/content_lint.rs:898` cites `tasks/town/p24-layout.md`
    §5 — exists only at `.claude/tasks/town/`.
  - `server/vordar-server/tests/soak.rs:227` cites `docs/benchmarks/BASELINE.md` —
    exists only at `.claude/docs/benchmarks/`.
- **Ideal:** every pointer resolves from where a reader stands. Living-spec
  citations (visual-quality.md, BASELINE.md, the layout spec) carry their real
  current location; citations to artifacts that no longer exist are replaced by the
  constraint they carried.
- **Gap:** four citations misdirect to paths that are empty in the repo the reader
  is in; two point at a file that is gone entirely, so the lesson they defer to is
  unrecoverable from the comment.
- **Suggestion:** prefix the four moved-doc citations with `.claude/` (the standing
  convention already treats `.claude/DESIGN.md` as "DESIGN.md", so alternatively
  adopt and document one citation convention for cross-repo docs — but pick one).
  For the two `tasks/lessons/` citations, inline the lesson's constraint core in
  place of the pointer: review renders must be in-engine at gameplay framing because
  turntable framing cleared five props that then failed in-game.
- **Outcome:** `7/10` — comment navigation stops lying; the review-tool rationale
  survives its dead source.
- **Confidence:** `9/10` — every path's existence/absence was checked on disk in
  both repos this run.
- **Cost:** `1/10` — six comment edits.
- **Path:** (1) edit the six sites; (2) green gate: `cargo check --workspace` zero
  warnings — comments only; re-run `bash scripts/lint-comments.sh` (stays 0).

### 2. Stale claim and history framing: culling's "no draw-path changes yet", vfx's "legacy", a test's "previously reported"

- **Evidence:**
  - `smirk/engine-renderer/src/culling.rs:3-5` — header ends "This step only adds
    the math and captures mesh bounds at upload — no draw-path behavior changes
    yet." The tree contradicts it: `smirk/engine-renderer/src/mesh/sync.rs:340` and
    `:349` call `classify` to skip invisible instances — culling IS live draw-path
    behavior. The header is roadmap-step narration frozen at the module's birth.
  - `client/vordar-client/src/vfx.rs:105` ("The legacy tuned look — hot core-glow
    sparks.") and `:256-257` ("falls back to the legacy tinted spark burst") — the
    burst is not legacy, it is the live default for unauthored abilities; "legacy"
    frames a current contract as history.
  - `client/vordar-client/src/net/e2e.rs:54-58` — "instead of the single
    `max_recv_jump` float those tests previously reported" — before/after
    narration; the constraint is just that the ring attributes a failure without a
    rerun.
- **Ideal:** the culling header states what the module owns now (pure math +
  `classify`, consumed by mesh sync's visibility pass); vfx names the burst by its
  role (default fallback look); the trace doc states the invariant without the
  history.
- **Gap:** one header actively false, three sites framing live behavior as leftover.
- **Suggestion:** delete the "This step… yet" sentence; replace "legacy" with the
  role ("default fallback look for unauthored abilities" / "the tuned core-glow
  default"); drop the "instead of…" clause.
- **Outcome:** `6/10` — the one lying header is in a module every renderer reader
  meets early.
- **Confidence:** `9/10` — the contradicting `classify` call sites were read
  directly this run.
- **Cost:** `1/10` — four comment edits in three files.
- **Path:** (1) edit the four sites; (2) green gate: `cargo check --workspace` zero
  warnings — comments only.

### 3. dispatch_cast: Scheduled and Leap duplicate the mechanic-scheduling block

- **Evidence:** `server/vordar-server/src/net/receive.rs:330-366` (Scheduled arm)
  and `:391-434` (Leap arm) share a near-verbatim ~30-line block: range gate,
  cooldown insert, `next_mechanic_id` bump, `world.spawn((Transform, Mechanic))`,
  `encode(&ServerMsg::MechanicScheduled { … })`, AOI broadcast loop, and the log
  line. Leap's own comment at `:406-408` admits the identity: "Same scheduling as
  Scheduled — the arrival hit test IS a Mechanic". The only Leap-specific additions
  are the `LeapImpulse` insert (`:420-423`) and the log wording.
- **Ideal:** one `schedule_mechanic(world, state, …) -> id` (or similar) that both
  arms call; a new scheduled-style effect variant adds one call, not a third copy
  of the spawn/encode/broadcast contract.
- **Gap:** the server's cast-handling hot path — where every new ability effect
  lands — must keep two copies of the wire contract in sync; drift here desyncs
  clients.
- **Suggestion:** extract the shared block into a free function beside
  `dispatch_cast` (the file's established shape: `handle_login`,
  `complete_db_load`, `respawn_dead` are already free functions), parameters being
  the fields both arms destructure; Leap keeps its `LeapImpulse` insert after the
  call.
- **Outcome:** `7/10` — the MechanicScheduled wire contract exists once.
- **Confidence:** `8/10` — code read; the e2e_combat suite pins both arms'
  behavior, so an extraction regression is detectable, but no measurement beyond
  the read backs the "near-verbatim" claim being fully mechanical.
- **Cost:** `3/10` — one extraction in one file; borrow scopes already proven by
  the current inline code.
- **Path:** (1) extract; (2) green gate: `cargo nextest run -p vordar-server` green
  (e2e_combat pins Scheduled and Leap), `cargo check --workspace` zero warnings.

### 4. handle_connection: the token bucket is implemented twice in one function

- **Evidence:** `smirk/engine-net/src/server.rs` — inside `handle_connection`
  (`:554-703`), the datagram task carries `dgram_tokens` with inline
  refill/drain/reject math (`:615`, `:633-641`) and the stream reader loop carries
  `msg_tokens` with the identical math (`:656`, `:673-686`): same
  `MSG_BUCKET_CAPACITY` cap, same `MSG_REFILL_PER_SEC` refill, same
  `record_reject` on empty. The file already models the right pattern for exactly
  this kind of per-connection state: `RttEstimator`/`RttHandle` (`:57-113`) are
  named types with unit tests.
- **Ideal:** one `TokenBucket` type (`new(capacity, refill_per_sec)`,
  `try_take(now) -> bool`) owned per lane; the rate-limit policy is written once
  and unit-testable the way `RttEstimator` already is.
- **Gap:** the flood-control invariant — the thing `tests/flood_control.rs` exists
  to pin — lives as two hand-expanded copies in the workspace's largest non-test
  source file (702 non-test lines); a tuning change must find both.
- **Suggestion:** extract `TokenBucket` beside `RttEstimator`, use it in both
  loops. Optionally, in the same pass, name the three per-connection stages
  (writer task `:589-600`, datagram task `:601-650`, reader loop `:660-697`) as
  functions — the stages are currently comment-labeled blocks, the shape the
  2026-07-15 rework 1 noted and consciously left to a later pass.
- **Outcome:** `7/10` — one rate-limit policy, testable in isolation, in the file
  most likely to be edited under pressure.
- **Confidence:** `8/10` — both copies read side by side this run;
  flood_control/datagram tests pin the behavior, but the stage-extraction part is
  judged from the read alone.
- **Cost:** `3/10` for the bucket alone; `4/10` with the stage naming (async
  captures need care).
- **Path:** (1) `TokenBucket` + swap both loops; (2) optional stage extraction;
  (3) green gate: `cargo nextest run -p engine-net` green (flood_control,
  impairment, datagram-lane tests), `cargo nextest run --workspace` green.

### 5. Review-bin plumbing duplicated five ways beside the module built to share it

- **Evidence:** `smirk/engine-renderer/src/review.rs:1-3` exists precisely because
  "a bin cannot reach a sibling bin" — yet the bins still each carry their own
  copies of the same plumbing:
  - `parse_size` — byte-identical in five bins:
    `client/vordar-client/src/bin/zone_review.rs:115`,
    `client/vordar-client/src/bin/asset_inspect.rs:168`,
    `client/vordar-client/src/bin/gear_render.rs:44`,
    `client/vordar-client/src/bin/render_material.rs:46`,
    `smirk/engine-renderer/src/bin/turntable.rs:53`.
  - `die` — identical modulo the bin-name prefix in four:
    `zone_review.rs:110`, `asset_inspect.rs:163`, `gear_render.rs:39`,
    `turntable.rs:48`.
  - `save` (PNG write + parent-dir create) — `zone_review.rs:521`,
    `asset_inspect.rs:416`, and a variant at `chapel_probe.rs:148`.
  - `orbit_eye` (spherical-eye math mirroring `Camera::recompute_eye`) —
    `zone_review.rs:55` and `chapel_probe.rs:45`.
- **Ideal:** review.rs (already the shared home, already imports `image`) owns
  `parse_size`, `save`, `orbit_eye`, and a `die`/fail helper taking the bin name
  (`env!("CARGO_BIN_NAME")` at the call site); each bin keeps only its own
  argument schema and scene logic.
- **Gap:** five copies of `parse_size` is exactly the drift the review.rs header
  promises to prevent; `orbit_eye` duplicating `Camera::recompute_eye`'s
  parametrization in two bins doubles the places a camera-convention change must
  visit.
- **Suggestion:** hoist the four helpers into `engine_renderer::review`; the
  client bins already depend on the crate with the `offscreen` feature, and
  turntable lives in the same crate.
- **Outcome:** `6/10` — tooling-only, but the review-bin population is still
  growing (chapel_probe is the fifth) and each new bin currently starts by copying
  plumbing.
- **Confidence:** `8/10` — the `parse_size`/`die` copies were diffed by eye this
  run and are identical; `save`/`orbit_eye` compared by signature and shape.
- **Cost:** `2/10` — mechanical hoist, bins compile or they don't.
- **Path:** (1) move helpers into review.rs; (2) delete the copies, update the
  five bins; (3) green gate:
  `cargo check --workspace --all-targets --features offscreen`-equivalent (the
  gated bins compile: `cargo check -p vordar-client --features offscreen
  --bins -p engine-renderer --features offscreen`), `cargo nextest run --workspace`
  green.

### 6. Naming consistency: three System impls without the suffix, one file that under-predicts

- **Evidence:**
  - `server/vordar-server/tests/mechanic_pipeline.rs:29` `struct Spawn` and `:60`
    `struct Observe` implement `System` without the `…System` suffix; the same
    convention was already enforced test-side by the 2026-07-15 audit (finding 12:
    `PanicOnceSystem`, `server/vordar-server/tests/watchdog.rs:23`, carries it today).
  - `testing/test-support/src/server.rs:83` `pub struct MetricMirror` implements
    `System` (`:88`) — harness src, same convention, no suffix.
  - `server/vordar-server/src/net/login.rs` — the name promises login handling,
    but the file holds only the `LoginFailures` per-IP failure ledger (`:16`);
    actual login handling is `handle_login` in
    `server/vordar-server/src/net/receive.rs:169`. A reader
    hunting login logic lands on the rate limiter.
- **Ideal:** every `System` impl carries the suffix wherever it lives; `login.rs`
  is named for the one thing it owns.
- **Gap:** three suffix deviations (all in test/harness code, where the last audit
  showed conventions erode first) and one first-guess miss.
- **Suggestion:** rename to `SpawnSystem`/`ObserveSystem` (or behavior-named
  equivalents) and `MetricMirrorSystem`; rename `login.rs` →
  `login_limiter.rs` (or fold `LoginFailures` into receive.rs beside its only
  consumer — but the file split is fine, only the name misses).
- **Outcome:** `5/10` — convention integrity; cheap to keep, expensive to
  re-establish once deviations become precedent.
- **Confidence:** `9/10` — the full `impl System for` population was enumerated by
  grep this run; these are the only three deviations.
- **Cost:** `1/10` — renames; none of the three names appears in
  `.config/nextest.toml` filters or BASELINE.md (verify at implementation time per
  the standing rename-sweep rule).
- **Path:** (1) rename the three structs + the file (module path updates in
  `server/vordar-server/src/net/mod.rs:40`); (2) green gate:
  `cargo nextest run --workspace` green at
  unchanged count.

### 7. chapel_probe: a self-described throwaway probe with no expiry condition (user-decides)

- **Evidence:** `client/vordar-client/src/bin/chapel_probe.rs:1-8` — "Headless
  interior evidence for the chapel's broken-vault-vs-enclosed-volume design
  question… Not a ship-gate tool (zone_review is); throwaway probe logic (the roof
  ablation filter, the containment sweep) lives here". 291 lines with hard-coded
  scene constants (`NAVE_CENTER`, `HDRI`, fog at `:35-50`) serving one design
  question. The comment policy forbids open-ended temporary scaffolding: the probe
  names no condition under which it dies.
- **Ideal:** probes either state their expiry ("delete when X ships") or are
  deleted when their question closes; ship-gate tooling (zone_review) is the only
  standing render tool per zone.
- **Gap:** if the vault question is settled (chapel_arch and retablo installs
  suggest chapel work has progressed), this is expired scaffolding kept compiled;
  if it is still open, the bin merely lacks its expiry note. The audit cannot
  decide which from code alone.
- **Suggestion:** user decides: (a) the question is settled → delete the bin (its
  reusable part already lives in `vordar_client::chapter_geometry` per its own
  header, so nothing else is lost); (b) still open → add the expiry condition to
  the header.
- **Outcome:** `5/10` — either one dead bin removed or the scaffolding rule kept
  honest.
- **Confidence:** `7/10` — the bin and its header were read; whether the design
  question is closed is not decidable from the tree, which is why this is
  user-decides.
- **Cost:** `1/10` — a deletion or a one-line comment.
- **Path:** (1) user answers settled/open; (2) delete (also drop the `[[bin]]`
  entry at `client/vordar-client/Cargo.toml:49-52`) or annotate; (3) green gate:
  `cargo check --workspace --all-targets` zero warnings.

## Carried forward from previous report

None — all twenty 2026-07-15 findings and both reworks re-verified resolved this
run (see below).

## Resolved since last report

All twenty 2026-07-15 findings and both reworks, each re-verified against current
code this run:

1. **Stale claims and dead pointers** — all nine sites fixed: `resolve.rs:1-4` now
   states the stub contract, `menu.rs` pointer gone (no `apply_pending_menu_actions`
   anywhere), `vfx.rs:28` points at `hit_react.rs`, `locomotion.rs` `net.rs` pointer
   gone, `presentation.rs:1-4` scoped to what the file holds, `behavior.rs:1-12`
   describes the real registry mechanism, `instance_sync.rs:1-3` doc matches both
   systems, telegraph's invariant stated once (`telegraph.rs:2`), both `///`
   headers now `//`.
2. **test-support provenance purge** — lint-comments 0 hits; `bot.rs` docs are
   constraint-only.
3. **smirk test/bench/WGSL provenance purge** — lint-comments 0 hits workspace-wide.
4. **Server-crate provenance purge** — lint-comments 0 hits.
5. **Game/client provenance purge** — lint-comments 0 hits.
6. **Expired mesh probe + glTF diagnostics** — no `mesh_probe` reference and no
   DIAGNOSTIC block remains anywhere.
7. **Root strays** — `example` and `req.md` deleted.
8. **content/ naming follow-ups** — statue is `content/models/statue_vroid.glb`;
   `content/source/` root holds only `CREDITS.md`, `characters/`, `test/`; the
   `vroid/` directory (with its empty `clips/`) is gone entirely.
9. **Dead `Time.server_offset_micros`** — field and write both gone.
10. **Bot constructor ladder** — one private `Bot::new` (`bot.rs:204`); the ladder
    delegates.
11. **Re-export retirement** — `locomotion.rs` imports `crate::net::NetMotion`
    (`:22`), `class.rs` has no race re-export. `SnapshotBroadcastSystem`/
    `MechanicResolveSystem` remain `pub`, which is required: the feature-gated
    bench seam re-exports them (`server/vordar-server/src/net/bench.rs:6-7`), and a `pub use` cannot widen a
    `pub(crate)` item — resolved as designed.
12. **Test naming** — `PanicOnceSystem` (`watchdog.rs:23`); `PhaseMeter` and
    `fn end_to_end` gone. (Three new deviations elsewhere are finding 6 of this
    report.)
13. **chapter.rs split** — `world/chapter_registry.rs` exists beside `chapter.rs`.
14. **gltf_import split** — `mesh/anim_import.rs` exists.
15. **Engine small placements** — `PhysicsStatsSystem` in `engine-physics/src/stats.rs`;
    `cube_view_of` gone; one Quit path (`menu_actions.rs:82` is the only
    `process::exit` in the renderer); video-mode fitting exists once
    (`app_loop.rs:162` is the only refresh-rate site).
16. **offscreen feature gate** — `lib.rs:18-19` gates the module on
    `feature = "offscreen"`; consumers wire the feature (self dev-dependency,
    client bins' `required-features`).
17. **frame.rs/state.rs seams** — `RenderSystem::run` reads as a frame graph
    (`record_shadow_pass`/`record_depth_prepass`/`record_ssao`/`record_main_pass`/
    `record_particle_pass`/`record_egui_overlay_pass`, `frame.rs:305-351`);
    `state.rs` init delegates to `create_*` per-subsystem constructors
    (`state.rs:286-588`).
18. **test-support crate shape** — `util.rs` split into `fs.rs`/`stats.rs`/
    `threads.rs`/`rng.rs`; the flat namespace is documented as the harness
    convention (`lib.rs:1-7`).
19. **Third-pass residue** — manifests, watchdog/shutdown narration, client
    headers all clean (lint-comments 0 hits; client Cargo.toml comments read).
20. **Fourth-pass residue** — no WEAKPOINTS reference anywhere in the workspace.
- **Rework 1 (engine-net decomposition)** — landed: `clock.rs` and a unified
  `impair.rs` exist; `client.rs` is down to 373 lines of transport. Its
  consciously-descoped second-order seam (`handle_connection` staging) resurfaces
  only as the bounded finding 4 of this report.
- **Rework 2 (receive.rs seam promotion)** — landed: `NetReceiveSystem::run` is a
  short dispatcher over `handle_login`/`dispatch_cast`/`complete_db_load`/
  `respawn_dead`/`drain_intents` (`receive.rs:63-660`).

Close-out gate: `bash scripts/lint-findings.sh` run on both new reports (this file
and `reworks-hygiene-2026-08-07.md`) — the dispatch brief believed the script was
deleted, but it exists and passed.
