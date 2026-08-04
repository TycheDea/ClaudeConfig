# World of ClaudeCraft vs vordar — comparative analysis (2026-07-22)

Source: https://github.com/levy-street/world-of-claudecraft, cloned read-only at
`reference/world-of-claudecraft` (gitignored), HEAD `8950e61` (2026-07-22).
**License: MIT for code** — lifting the shape of their code is allowed. Assets are
governed separately by their `CREDITS.md` (see §2); nothing binds us since we take
code patterns only.

What it is: a complete classic-era MMO in TypeScript — Three.js browser client,
Node/Postgres authoritative server, Electron/mobile shells, and a headless
Gymnasium RL env — all driven by one deterministic sim (`src/sim/`). Three
open-world zones, five instanced dungeons, randomized "delve" runs, arena PvP,
professions, mail, market, 22 locales. Publicly playable. Despite the
"vibe-coded" reputation of the genre, this is a rigorously engineered codebase:
1,244 test files, mechanically-enforced architecture invariants, and per-directory
CLAUDE.md maps that embed the grep command that verifies their own claims.

Standing ruling context: vordar will adopt ClaudeCraft-style procedural generation
**scoped to dungeons**, not the global world. This document evaluates *how*.

---

## 1. Dungeon-scoped procedural generation (the ruling's target)

### The headline finding: they generate *composition*, never *geometry*

Their five story dungeons are not procedural at all: each is a hand-authored
plain-number layout (`src/sim/dungeon_layout.ts` — `CRYPT_LAYOUT`,
`SANCTUM_LAYOUT`, `TEMPLE_LAYOUT`, `NYTHRAXIS_LAYOUT`, ~250 lines total). The
procedural mode is **delves** ("rebuilt from randomized chambers each run"), and
what the seed decides there is *which authored rooms, in what order, with which
spawns and affixes* — room geometry itself is always authored. Quality is
guaranteed by curation; variety comes from combinatorics. Given our AA art
direction and the pain of validating generated geometry, this is the strongest
possible evidence point for a module-library dungeon generator over a
geometry-synthesizing one.

### The room description language

`DungeonLayout` (`src/sim/dungeon_layout.ts`) is a struct of plain numbers:
rectangular shell (`zMin`/`zMax`/`wallX`), `pillars` (grid points), `tombs`
(wall-side obstacles), `stubs` (chamber-waist walls that shape a nave into
chambers), `dais` (boss platform, deliberately no collider), `doorZ`, `clutter`
scatter points, and optionally an irregular `shellPolygon` + `shellPole`. From
this ONE struct:

- `layoutColliders()` (same file) derives the interior collision set consumed by
  `src/sim/colliders.ts`;
- `src/render/dungeon.ts` (1,940 lines) derives the entire visual build — KayKit
  dungeon-kit wall/floor/pillar modules, torches, props — from the SAME data
  ("what you see is what blocks you", their words). The header comment says the
  pattern's purpose outright: "this kills the old hand-mirroring between renderer
  geometry and collider literals."

The clutter scatter even shares its placement formula between collision circles
and visual props (a sine sweep, `x = sin(i*2.4)*14, z = 12 + i*9.5`, documented
in `src/sim/delve_layout.ts`).

Irregular rooms (The Drowned Litany, `src/sim/delve_litany_layout.ts`, ~1,000
lines) extend the language rather than replacing it: a walkable **star-shaped
polygon** (validated by `geometry2d.polygonIsStarShaped` /
`polygonSelfIntersects` against an authored `pole`), plus `islands`, ellipse
`hazards` (blackwater), and **semantic dressing anchors** — `{kind:
'reed_cluster'|'plank_bridge'|'shrine_fragment'|..., x, z, rot}` authored in the
sim, with the renderer mapping `kind` → asset (`src/render/delve_marsh_dressing.ts`).
Seven shape profiles (crescent, ring, sinkhole, fan, y_split, ...) give each
module a distinct silhouette while staying inside one shared 50×110u footprint
so the KayKit wall kit fits unchanged.

### Seeded composition — the generator proper

`src/sim/delves/runs.ts` is the transferable core:

- **One run seed, drawn once** from the shared sim stream at run start
  (`run.seed = ctx.rng.int(1, 0x7fffffff)`, line 447).
- **`pickDelveModules(delve, seed, tierId)`** (line 311): Fisher-Yates shuffle
  of the delve's module pool with `new Rng(seed)`, take N (N per difficulty
  tier from `DelveDef.moduleCount`), append the fixed finale module. That's the
  whole layout algorithm — ~15 lines.
- **Purpose-keyed sub-streams**: every other seeded decision derives its own
  independent stream from the run seed — spawn-set pick per module
  (`new Rng(seed ^ (moduleIndex * 7919))`, line 819), affix roll
  (`seed ^ 0x5a11c0de`, line 1227), bountiful-chest roll (`seed ^ 0x600dc0ff`),
  the Rite finale (`seed ^ 0xd20ed71a`), the lockpick board. The module header
  names this discipline explicitly: five sub-streams kept distinct from the two
  shared-stream draws, "so it is deterministic without perturbing the global rng
  draw order that the chest loot depends on."
- **Spawn content is authored per module** as weighted spawn sets with exact
  positions and per-pack tactical intent in comments
  (`src/sim/content/delves/collapsed_reliquary.ts`); the seed only picks which
  set spawns.
- **Affixes** (`src/sim/content/delves/affixes.ts` + `rollDelveAffixes`):
  a pool of run modifiers tagged by dungeon theme (`crypt`/`mine`/`sewer`/...),
  seeded shuffle, take `tier.affixCount`. A `DELVE_IMPLEMENTED_AFFIXES` gate
  lets content defs exist ahead of code without ever rolling an inert affix.

### Module stitching: teleport, not corridors

Modules are stacked along z with a 16u gap (`delveModuleZOffset`) and
**module-to-module travel is teleport-only** through an exit object; a
confinement box clamps entities to the active module's own layout bounds
(`runs.ts` line 169-183). This deletes the classic dungeon-gen problem set —
corridor routing, connectivity validation, cross-room pathfinding — at the cost
of a loading-tunnel feel between rooms. Layouts are never sent over the wire:
both sides derive geometry from the same data + seed.

Instances live in far-off flat-ground x-bands of the single world coordinate
space (`instanceOrigin(dungeonIndex, slot)` = `x: 900 + i*600, z: -1250 +
slot*500`, `src/sim/data.ts` line 417), with all layout math in instance-local
coordinates and one world→local offset. Simple, but in Rust we'd likely prefer a
separate `hecs::World` per instance over coordinate-band partitioning.

### Transfers vs doesn't transfer

| Technique | Verdict for vordar dungeons |
|---|---|
| Module library + seeded shuffle composition (`pickDelveModules`) | **Transfers directly** — this IS the dungeon-scale pattern |
| One layout struct → collision AND render (`dungeon_layout.ts` + `layoutColliders` + `render/dungeon.ts`) | **Transfers** — the load-bearing design decision |
| Purpose-keyed RNG sub-streams (`seed ^ MAGIC`) | **Transfers**, and matches our existing stateless-hash style |
| Semantic dressing anchors (sim kind → renderer asset) | **Transfers**; pairs perfectly with our prop pipeline |
| Star-shaped-polygon shells with mechanical validation | **Transfers** when we outgrow rectangles |
| Teleport-stitched modules, per-module confinement | **Transfers** if we accept the feel; otherwise the connectivity problem returns |
| Affix pool + implemented-set gate | **Transfers** as the replayability multiplier |
| Overworld heightfield (`world.ts`: `terrainHeight` pure fn of (x,z,seed), stateless `hash2/noise2/fbm2` in `rng.ts`) | Global-world technique; the *stateless-noise-from-coordinates* idiom shrinks fine to dungeon floors/height variation, the zone-band composition (`zoneAt`) does not apply |
| Voxel density layer + hand-authored tunnel capsules (`voxel.ts`, `content/tunnels.ts`) | Doesn't transfer yet — engine-only even in their repo (tests pass, renderer never wired) |
| Settlement/biome placement | Not present here (towns are hand-placed content defs, unlike OpenMMO's habitability solver) — nothing to take |

---

## 2. CC0 curation + CREDITS.md discipline

This is the concrete template OpenMMO takeaway #2 was missing. OpenMMO told us
*what* to source (CC0 photoscan PBR for commodity surfaces); ClaudeCraft's
`CREDITS.md` shows *how to record it* so the licensing surface never rots:

1. **The file is declared "the operative licence record"** — root `LICENSE` (MIT)
   covers code only; every media asset is governed by the licence recorded in the
   tables, which "controls over the project's MIT license."
2. **Default-closed rule**: "Media assets that are not listed here are not
   licensed to you... an asset missing from it means we have not recorded its
   terms yet, not that it is free to take."
3. **One table row per pack/asset**: `Assets | Author | Source (URL) | License |
   Redistribution`. E.g. every KayKit/Quaternius/Kenney model pack, every
   ambientCG terrain texture set (by ID: Grass001, Rock051, ...), every Poly
   Haven HDRI (by name) — CC0 1.0, Redistribution `Yes`.
4. **A plain-language Redistribution enum** decoupled from license names:
   `Yes` / `Yes, attribution required` / `Yes, under SIL OFL 1.1` / `With the
   project only` / `Non-commercial only, with attribution` / `No, permission
   required` — each defined once in a legend table. Forks learn what they must
   strip in one section ("Do not redistribute these").
5. **Generated assets are first-class rows**: every AI-generated prop gets its
   own line naming the generating pipeline as provenance ("Project-generated via
   scripts/asset_pipeline (Tripo AI 3D)"), licensed `With the project only` — a
   deliberate tier letting forks ship the game while forbidding asset-pack
   extraction.
6. **Upstream notices preserved** (`third_party/licenses/kaykit-cc0.txt`); raw
   packs never committed — assets ship optimized via
   `scripts/assets/build_assets.mjs` (clip pruning, meshopt compression, texture
   resize).
7. **A "Can I still fork?" section** that answers the practical question
   directly.

For vordar: adopt the table format + Redistribution enum + default-closed rule
verbatim (our columns: Assets | Author | Source | License | Redistribution, plus
our manifest hash/provenance where the asset is pipeline-generated). Our strict
licensing policy is already stronger than theirs on inputs (they use Tripo,
which OpenMMO's own docs flagged as a licence risk — here at least it is
disclosed per-asset); what we lack is exactly this single operative record.
Note their dungeon surfaces are KayKit Dungeon Remastered + Kenney modular
dungeon kits (CC0) — the render layer proves a kit-based dungeon can look
coherent when every module obeys one shared wall/floor grammar.

## 3. One deterministic sim, three hosts — and where `IWorld` actually sits

The precise boundary matters, because the survey blurred it:

- **`Sim` (`src/sim/`) is the host-agnostic core**: no DOM, no i18n, no
  wall-clock, no `Math.random` (all mechanically banned by
  `tests/architecture.test.ts`); one fixed 20 Hz step; randomness only through
  the seeded `Rng`; output only via a `SimEvent` union; callers call `tick()` —
  the sim never self-schedules.
- **Three hosts drive `Sim` directly**: the offline browser (`src/main.ts`,
  fixed `WORLD_SEED = 20061`), the authoritative server (`server/game.ts` runs
  `sim.tick()` on an interval with catch-up ticks and profiling laps), and the
  headless RL env (`headless/env_server.ts`: NDJSON over stdio, Gymnasium
  bindings in `python/`, `frameSkip` ticks per env step, reward shaping from
  `RewardCounters` deltas over the sim's `obs.ts` surface).
- **`IWorld` (`src/world_api.ts` + 28 facet files) is NOT the host seam — it is
  the presentation seam**: "the surface the renderer + HUD need from a game
  world." It has exactly two implementations: the offline `Sim` (structurally)
  and the online `ClientWorld` (`src/net/online.ts`), which mirrors server
  snapshots and sends wire commands. `render/`, `ui/`, `game/` may only import
  `IWorld`, never a concrete world. The server and RL env sit *outside* it.

The seam is held shut by pinned gates, not convention: `IWORLD_MEMBERS` in
`tests/world_api_parity.test.ts` pins every member present and same-kind on both
`Sim` and `ClientWorld`, and that the aggregate equals the disjoint union of the
facets; command-schema and snapshot round-trip tests (W0a/W0b) pin the wire; a
purity suite bans any non-type import into the facets. Behind the sim, a
**golden-trace parity harness** (`tests/parity/`) records full entity/meta state
plus an **rng draw-order fingerprint** (rolling FNV-1a over every shared-stream
draw, in order) for seeded scenarios — any behavior change turns it red by
design, with a reviewed `UPDATE_PARITY=1` regeneration workflow.

**Against our crate split**: vordar already has the property their architecture
exists to create. `game/vordar-game` is compiled by both the client (prediction)
and the server (authority), reacts only to intent events, and touches no
renderer/window/input (`game/vordar-game/src/lib.rs` header). Their
`Sim`/`ClientWorld` duality exists because a browser client cannot run the
authoritative world online — our all-Rust client predicts with the *real* sim
crate, so we do not need an `IWorld`-style double implementation, and adopting
one would be a second channel with no consumer. What DOES transfer is the
**enforcement style**: mechanical architecture tests (banned APIs, dependency
direction) and, once dungeon gen lands, seeded golden tests.

**One contrast worth internalizing**: their single shared `mulberry32` stream
makes global draw *order* load-bearing — reordering a loop forks the world, and
they built the entire parity harness largely to police that. Their own delve
code quietly evolved away from it (the five `seed ^ MAGIC` sub-streams). vordar
already uses stateless per-event seed hashing (e.g. damage variance from entity
bits, `game/vordar-game/src/combat/projectile.rs:144`), which sidesteps
draw-order fragility entirely. For dungeon gen: keep our style — one dungeon
seed, purpose-keyed derived streams — and never introduce a shared sequential
stream that systems drain in tick order.

## 4. Other load-bearing findings (brief)

- **Testing discipline is the standout**: 1,244 test files. Architecture
  invariants (dependency direction, seam purity, determinism bans) are enforced
  as tests, not prose. A localization drift guard parses sim emit sites at test
  time and fails CI on any player-facing string the client can't translate.
  Design docs cite guard tests by name and declare "where this document and a
  committed guard test disagree, fix the disagreement in the same change."
- **Self-verifying docs**: per-directory CLAUDE.md files embed the grep that
  enumerates the live set they describe ("enumerate the live set: `grep -rl
  sim_context src/sim`; every hit must be a row here"). Docs that can be checked
  mechanically don't rot — directly applicable to our tasks/ and docs/.
- **SimContext seam** (`src/sim/sim_context.ts`): system modules own functions,
  never state; all state stays on `Sim` as live views; extraction proven
  behavior-identical by the parity gate. A tested recipe for decomposing a large
  sim without drift — relevant if any vordar crate ever grows a god-struct.
- **Netcode shape**: WebSocket + JSON-ish snapshots with distance-tiered update
  rates, per-system wire intervals, write backpressure, and a tick profiler with
  named phase laps (`server/game.ts`). Nothing ahead of our QUIC/quinn design;
  the phase-lap profiling idea is worth stealing someday.
- **Weather is render-only by contract** — biome-driven visuals that never touch
  the deterministic sim. Same shape as our client-side presentation split.
- **Content pipeline**: project props via `scripts/asset_pipeline` (Tripo cloud
  gen — weaker than our local seeded pipeline, same verdict as OpenMMO), but
  hundreds of screenshot-producing verification scripts (`scripts/*_shot.mjs`)
  amount to a visual smoke-check culture we partially have via headless checks.

## 5. Overall verdict

**They do better:** shipping breadth on one deterministic core; mechanical
enforcement of architecture (pinned seams, banned APIs, golden traces);
curation-first dungeon variety with tiny generator code; the operative
asset-licence record; self-verifying documentation.

**They do worse / not applicable:** cloud-generated prop assets (no seeds, no
local reproducibility); shared-stream RNG fragility they had to build a harness
around; TypeScript-server performance ceiling; `IWorld` double-implementation
burden our all-Rust stack doesn't need; no real worldgen to study (that was
OpenMMO's strength — the two repos are complementary).

---

## Patterns to adopt for the eventual dungeon-gen design

1. **Module library + seeded composition, not geometry synthesis.**
   *What:* a dungeon run = seeded Fisher-Yates draw of N authored room modules
   from a themed pool + a fixed finale; difficulty tier sets N.
   *Where:* `src/sim/delves/runs.ts` `pickDelveModules` (line 311),
   `DelveDef.moduleCount`/`modules` in `src/sim/content/delves/*.ts`.
   *Maps to us:* generator fn in `vordar-game`; module defs in chapter crates
   (content stays out of the sim crate, matching our existing split).
   *Effort:* S for the composition core; the real cost is authoring the module
   library, which our prop/interior pipeline feeds anyway.

2. **One layout struct as single source for collision AND render.**
   *What:* rooms described as plain numbers (shell, pillars, stubs, dais,
   clutter, door); `layoutColliders()` derives physics, the renderer derives kit
   placement from the same struct. No hand-mirroring, ever.
   *Where:* `src/sim/dungeon_layout.ts` (struct + `layoutColliders`),
   `src/render/dungeon.ts` (consumes the same data).
   *Maps to us:* layout type in `vordar-game`, colliders into engine-physics,
   visual build in `vordar-client` — both derived, neither authored twice.
   *Effort:* M — it is the central design decision of the whole feature; cheap
   in code, must be locked in before any room is authored.

3. **One dungeon seed, purpose-keyed sub-streams.**
   *What:* draw the run seed once; every decision domain (module pick, spawns,
   affixes, loot) gets `Rng(seed ^ DOMAIN_MAGIC)` so domains can't perturb each
   other and each is replayable in isolation. Never a shared sequential stream.
   *Where:* `runs.ts` lines 447/452/819/1227; the header comment names the
   discipline.
   *Maps to us:* extends our existing stateless-hash idiom
   (`combat/projectile.rs:144`); trivially expressible with a small seeded-RNG
   in `vordar-game`.
   *Effort:* XS.

4. **Teleport-stitched modules with per-module confinement.**
   *What:* modules placed with a dead gap, travel between them is a teleport
   through an exit object, entities clamped to the active module's bounds.
   Corridor routing and cross-room connectivity validation cease to exist.
   *Where:* `runs.ts` `delveModuleZOffset`/confinement (lines 151-183).
   *Maps to us:* even cleaner in Rust — a separate `hecs::World` (or reserved
   entity range) per instance instead of their coordinate-band hack
   (`data.ts` `instanceOrigin`). Decide early whether the loading-tunnel feel is
   acceptable; if not, budget for real connectivity work.
   *Effort:* S with teleport stitching; M+ if we insist on walkable corridors.

5. **Semantic dressing anchors.**
   *What:* the sim authors `{kind, x, z, rot}` prop anchors with gameplay-free
   semantic kinds; the renderer owns the kind→asset mapping. Collision circles
   and visual props share one placement formula.
   *Where:* `LitanyDressingAnchor` in `src/sim/delve_litany_layout.ts`,
   consumed by `src/render/delve_marsh_dressing.ts`; shared clutter formula in
   `src/sim/delve_layout.ts`.
   *Maps to us:* our prop pipeline outputs per-kind assets; dungeon modules
   reference kinds, so re-generating an asset never touches layout data.
   *Effort:* S.

6. **Affix pool with an implemented-set gate.**
   *What:* run modifiers as a content pool tagged by dungeon theme; seeded
   shuffle picks `tier.affixCount`; a `DELVE_IMPLEMENTED_AFFIXES` allowlist
   keeps unimplemented content defs from ever rolling.
   *Where:* `src/sim/content/delves/affixes.ts`, `rollDelveAffixes` in
   `runs.ts` (line 1227).
   *Maps to us:* the cheap replayability multiplier once modules exist; the
   gate pattern lets content land ahead of mechanics safely.
   *Effort:* M for the hook points, then XS per affix.

7. **Seeded golden tests for the generator.**
   *What:* pin generated output per seed corpus — layout hash at minimum, their
   fuller version adds state traces and an rng draw-order fingerprint — with an
   explicit reviewed-regeneration workflow (`UPDATE_PARITY=1`).
   *Where:* `tests/parity/` (harness, goldens, `trace.ts` exclusion lists with
   per-field justifications).
   *Maps to us:* a Rust test that snapshots `generate_dungeon(seed)` for a
   seed corpus into golden files; regeneration behind an env var, diffs
   reviewed. Client/server layout agreement falls out of the shared crate.
   *Effort:* S for layout goldens (we skip their draw-order machinery entirely
   thanks to pattern 3).

8. **CREDITS.md as the operative licence record** (pairs with OpenMMO
   takeaway #2).
   *What:* one file: default-closed rule for unlisted assets, per-asset rows
   (Assets | Author | Source | License | Redistribution), a plain-language
   Redistribution enum, generated assets listed with pipeline provenance,
   upstream notices kept in-tree, a fork-guidance section.
   *Where:* `CREDITS.md` (whole file), `third_party/licenses/`.
   *Maps to us:* instantiate on the first sourced CC0 pack (dungeon kit /
   Poly Haven surfaces); our generated assets add manifest-hash provenance to
   their pipeline-name column.
   *Effort:* XS — a template to copy, then discipline.
