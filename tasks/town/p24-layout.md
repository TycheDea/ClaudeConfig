# P2.4 — Rocalba full layout: kit visuals as zones.ron props + mirrored chapter03 collision

Subplan for `tasks/todo.md` P2.4 (branch ai-pipeline). Premise: `docs/town-premise.md`.
No camps in v1 (chapter.ron already spawns nothing living — stays that way).

---

## 1. Facts (verified 2026-07-31, file:line)

**zones.ron prop schema** — `game/vordar-game/src/world/zones.rs:105-115`:
`PropDef { model: String, pos: Vec3, scale: f32 (default 1.0), yaw: f32 deg }`.
Props are client-only (`ZoneVisuals` "server parses but never reads it", zones.rs:24).
Client spawns each placement as `RenderMesh { asset: model-path }`
(`client/vordar-client/src/presentation.rs:150-161`) — no AOI, always rendered.
Existing props sit at y = −0.5 (ground plane), e.g. `content/zones/zones.ron:45-73`.

**Renderer asset handling** — `smirk/engine-renderer/src/mesh/store.rs`:
- `MeshStore` dedups whole models by asset path (store.rs:282-298): N placements of
  one glb = one `GpuMesh`. Cross-instance duplication is NOT the problem.
- `upload_mesh` creates 5 fresh GPU textures **per primitive** (store.rs:123-127,
  183) — no sharing across the 138 primitives of casa_corner even though the glb
  embeds only ~18 unique images (6 material families × ~3 maps; 86.1 MB glb,
  `target/town-kit/build_report.json`). Measured: ~7.0 GB decoded RGBA8 for ONE
  loaded casa_corner; the G2 street scene OOMed a 3080 Ti even with 2048 BC
  sidecars (todo.md "RENDERER DEBT").
- **Consequence: the shipped client cannot load even one kit casa.** The full
  layout is NOT renderable in-game as-is; P2.4's own render evidence
  (zone_review uses the same store) is equally blocked. See §2 — this is the
  plan's gating prerequisite.

**Content lints that fire on kit props** — `game/vordar-game/tests/content_lint.rs`:
- `zone_visual_refs_load` (:224): every prop glTF must parse.
- `total_texture_memory_within_budget` (:376): 1 GB cap, counted **per placement,
  per primitive slot** (:439-455) — mirrors today's runtime; goes red by an order
  of magnitude on the town until the dedup fix lands and the count moves to
  unique images.
- `prop_placements_are_registered` (:613): assets.json entry keyed by the model's
  parent dir name (path-agnostic).
- `prop_material_matches_surface_class` (:635): asserts ONE surface class across
  all primitives of a model — cannot fit a 5-material building (limestone carries
  `detail: true`, others false; build_report `detail_extras`). Needs a kit-aware
  branch.
- `material_textures_have_fresh_sidecars` (:472): every placed model needs a
  `<asset>.textures/manifest.json` sidecar bake (`bake_textures.mjs`).
- `prop_models_within_byte_budget` (:732): every `.glb` under
  `content/models/props/` ≤ 32 MB (VQ-B5). casa_corner.glb is 86 MB embedded —
  resolved by exporting glTF-separate with shared textures (§2), not by a dir dodge.

**chapter03 state** — `game/chapter-03/src/lib.rs`,
`content/chapters/chapter03/chapter.ron`: 7 graybox prefabs, 12 spawns
(chapel_wall_side ×2, chapel_wall_apse, chapel_door_jamb ×2, chapel_lintel,
chapel_roof, casa_long ×2, casa_block ×3). Prefabs carry `ShapeGroup` visuals +
`Hitbox` + `Solid` + `Anchored`; hitbox is one **axis-aligned** Aabb centered on
the spawn point (`smirk/engine-core/src/components.rs:96-99` — Aabb | Sphere
only, no rotation). Graybox chapel interior x∈[−30,−14], z∈[−16.5,−9.5]
(pulled east for AOI — see §3).

**AOI mechanism** — `server/vordar-server/src/net/mod.rs:52`
`AOI_RADIUS: f32 = 40.0`; per-player exact center-distance test on the entity's
Transform (`net/broadcast.rs:126-143`). Client movement prediction collides
against **replicated** `Solid + Anchored` statics only
(`client/vordar-client/src/net/prediction.rs:126-131`). Largest town hitbox
half-extent is 8.8 m (chapel side wall) ≪ 40, so a static always replicates long
before a player can touch its surface — AOI popping of *invisible* collision is
gameplay-safe. What is NOT safe today: prefab `ShapeGroup` visuals ride
replication, so anything beyond 40 m of the player is invisible — that is why
P0.4 pulled the chapel. Replication test
`server/vordar-server/tests/zones.rs:161-171` asserts all 12 shells replicate to
a bot standing at spawn — breaks the moment any spawn exceeds r=40.

**Camera / P-C street data** — `smirk/engine-renderer/src/camera.rs:42-57`:
default orbit radius 34 m, pitch 0.8 rad (≈46°); zoom clamp
`CameraConfig { min_radius: 4.0, max_radius: 100.0 }`
(`client/vordar-client/src/ui/mod.rs:21`). At default zoom the eye sits
34·sin(0.8) ≈ **24.4 m above** the target and 23.7 m back — above every kit
ridge (max 8.1 m), so streets never need to contain the default orbit. P0.5
measured (todo.md P0.5, frames in `target/town-probe/`): 34 m never contained in
the 7 m nave; contained at zoom ≤ 5 m at nave center; min-zoom 4 m still clips
within ~0.5 m of a wall. **Derived street rule: ≥ 7 m clear width guarantees a
containable zoom (5 m) on the street centerline; plaza/street here is 19 m
facade-to-facade — comfortable.** The 3.2 m gate opening and the 2.4 m chapel
door clip at min zoom exactly as P-C's door finding — accepted transient.

**Kit footprints** — `scripts/asset-pipeline/townkit/buildings.py` (local frame:
X=width, Y=depth, Z=up, door facade = +Y; glbs in `target/town-kit/`):

| type | footprint w×d (m) | wall h | ridge/top | notes |
|---|---|---|---|---|
| casa_small_a | 6.0 × 8.0 | 4.0 | ≈5.60 | door+window front (:175) |
| casa_small_b | 5.6 × 7.4 | 3.8 | ≈5.42 | (:185) |
| casa_two_story | 7.0 × 10.0 | 6.4 | ≈8.11 | (:199-203) |
| casa_corner | main 6×6 + wing 4.5×4.0 at local offset (4.8, 1.0) | 4.0/3.8 | 5.60/5.00 | build_report dims; wing rotated 90° |
| wall_segment | 4.0 × 0.6 | — | 2.6 (+rubble) | (:344) |
| gate_arch | 6.4 × 0.9 | — | wall_top ≈ 5.6; opening 3.2 w × 3.6 springline | (:361-401) |
| well_basin | r = 1.25 round | — | basin 0.9, posts to 2.7 | (:404-424) |
| chapel | nave 16 × 7 interior, walls 0.6, apse fan west ~+2.5 | springline 7.5 | vault ≈10.5 | door east 2.4 × 3.2 (:440-449) |
| reja_set | 3 loose grilles | — | ≤1.5 | **not placed v1** — rejas are built into casa/window geometry already |

**Chapel door inconsistency** (todo P2.2 note): premise §6 says WEST doors;
graybox and kit both build the door EAST. East is correct for the layout (door
faces the town approach); premise §6 needs a one-line amendment — checkpoint §7.

**Hardcoded graybox coords elsewhere**:
`client/vordar-client/src/bin/zone_review.rs:87` `NAVE_TARGET (−22, eye, −13)`;
`chapel_probe.rs` (throwaway, dies Phase 4 — leave it).

---

## 2. Gating prerequisite P2.4.0 — texture dedup (renderer debt, pulled forward)

Without it: one casa OOMs the client, zone_review can't render P2.4 evidence,
and VQ-C5 lint is red → no green Phase 2 gate exists. Options (§6 weights):

- **A (recommended): dedup textures by source identity + kit ships shared
  textures.**
  Renderer: cache `ColorTexture` per unique image (content hash of encoded
  bytes, or per glTF image index within a model at minimum) in
  `smirk/engine-renderer/src/mesh/store.rs` / `mesh/gltf_import.rs`; primitives
  share bind-group textures. Kit: `build_town_kit.py` exports glTF-separate
  (.gltf + .bin + shared texture files), the precedent of the downloaded
  rock_*.gltf props — VQ-B5 stays honest, repo carries one tile set instead of
  9 embedded copies. Lint: `total_texture_memory_within_budget` counts unique
  images (matching the new runtime — the lint's own stated contract, :372-374).
  Outcome 9/10: constraint removed permanently; whole town ≈ one 6-family tile
  set resident (~0.15–0.6 GB depending on BC vs RGBA — estimate, see probe).
  Confidence: mechanism HIGH (per-prim creation verified store.rs:123-127;
  path dedup verified :282; OOM measured). Sizes MEDIUM until measured — probe:
  after the fix, load all 9 types through MeshStore and read
  `texture_memory_bytes()` (existing instrument, store.rs:347) — minutes.
  Cost: MEDIUM — renderer cache + export change + 9-type rebake + lint rewrite;
  golden risk low (identical pixels, shared bindings).
- **B: dedup by content hash only, keep 86 MB embedded glbs, install outside
  `content/models/props/` to skip VQ-B5.** Outcome 6/10 (runtime fixed; repo
  +~700 MB duplicate embedded textures; budget-dir split is a dodge).
  Confidence HIGH. Cost slightly below A. Not recommended — near-equal cost,
  strictly worse artifact.
- **C: no renderer work; 1024² DDS everywhere + raise the budget.** Outcome
  3/10 (lossy at street distance, still likely over budget, OOM margin thin).
  Rejected.

A is clearly best and has no outcome-close alternative → proceed on A; flagged
in §7 only because it pulls the queued renderer-debt item into Phase 2.

---

## 3. AOI reconcile — AOI_RADIUS 40 vs precinct (−30,−30)

- **Option 1 (recommended): keep AOI_RADIUS 40; strip `ShapeGroup` from all
  chapter03 prefabs (collision-only, invisible); site the chapel at the premise
  precinct.** Visuals live in always-rendered props, so AOI in/out popping has
  nothing to show; prediction still sees every wall before contact (facts §1:
  max half-extent 8.8 ≪ 40). Server/bench constants untouched.
  Outcome 9/10 · confidence HIGH (all three mechanisms read from source, plus
  the prediction path has e2e coverage) · cost LOW (prefab edits + replication
  test update). The P0.4 pull existed only because visuals rode replication —
  that reason dissolves with D5.
- **Option 2: raise AOI_RADIUS to ~55.** Outcome 6/10 — works, but pays
  snapshot fan-out for every zone forever, invalidates bench framing
  (`benchmarks/benches/snapshot.rs:32` comment-contract, e2e comments), and
  doesn't scale to larger towns. Confidence HIGH. Cost MEDIUM. Not needed.
- **Option 3: keep the chapel pulled to door-front x=−13.2.** Outcome 3/10 —
  violates premise §4, crowds the plaza SW, leaves the ruin cluster orphaned.
  Rejected.

Decision: Option 1, taken (no outcome-close alternative), logged here.

---

## 4. The layout

Axes +X east, +Z north. Props at y = −0.5; collision spawns at y = 0
(graybox convention). **All yaws ∈ {0, 90, 180, 270}** — collision is
axis-aligned Aabb (facts §1). "front→S" means the door facade faces −Z.
Kit local front is +Y; the numeric yaw per facing is confirmed once in step 6
(one render), then applied to the whole table.

### Zone props (content/zones/zones.ron, start zone — new "Rocalba town" block)

Model paths `content/models/props/<type>/<type>.gltf` (post-P2.4.0 install).

| # | type | pos (x, −0.5, z) | facing | role |
|---|---|---|---|---|
| T1 | casa_small_b | (−12.2, ·, 13.2) | front→S | north row W end; widow's candle window toward plaza |
| T2 | casa_small_a | (−6.4, ·, 13.5) | front→S | north row |
| T3 | casa_two_story | (0.1, ·, 14.5) | front→S | north row center — merchant house |
| T4 | casa_corner | (6.6, ·, 12.5) | front→S, wing toward road (E) | north row E end at the road mouth |
| T5 | casa_small_a | (−12.0, ·, −13.5) | front→N | south row W end |
| T6 | casa_corner | (−6.0, ·, −12.5) | front→N, wing W | south row — baker's corner |
| T7 | casa_two_story | (0.5, ·, −14.5) | front→N | south row |
| T8 | casa_small_b | (6.8, ·, −13.2) | front→N | south row E end |
| T9 | chapel | (−30.0, ·, −29.0) | door→E | precinct anchor; nave interior x∈[−38,−22], z∈[−32.5,−25.5] |
| T10 | gate_arch | (15.0, ·, 0.0) | opening along X (yaw 90) | east gate astride the road |
| T11 | well_basin | (0.0, ·, −4.6) | any | plaza well |
| T12 | wall_segment | (15.0, ·, 9.0) | run along Z | wall fragment N of gate |
| T13 | wall_segment | (15.0, ·, 13.5) | run along Z | fragment, staggered gap |
| T14 | wall_segment | (15.0, ·, −5.5) | run along Z | fragment S of gate |
| T15 | wall_segment | (15.0, ·, −10.0) | run along Z | fragment |

Row fronts sit on facade lines z = ±9.5; party walls touch (adjacent x-extents
meet: north row x −15.0/−9.4/−3.4/3.6/9.6). Backs are sealed shells (G2), fine
to see from above. Fragment gap z∈[3.2, 7.0] at the gate is deliberate: the
crucero shrine stands in the unfinished breach.

### Existing dressing edits (same file)

- Crucero **stays** (15.0, −0.5, 6.0) — now the gate shrine in the wall gap.
- Gravestones move out of the chapel volume to the graveyard patch N of it:
  (−31,−27)→(−31.0, −0.5, −22.5); (−28.5,−24.5)→(−27.5, −0.5, −22.0);
  (−33.5,−29.5)→(−35.0, −0.5, −22.5).
- broken_column (−20,−29) blocks the chapel door → (−19.5, −0.5, −34.0).
- chapel_arch ruin moved to (−26,−36.5): yaw 40 swings its 5.46 m span into
  z, so the (−26,−34) placement's west pillar crossed the chapel south wall
  (z=−33.1) and stood on the nave floor — the check that cleared it by 0.9 m
  used the model's nominal depth, not the yawed footprint. At (−26,−36.5) the
  north extent is −34.2, clearing the wall by 1.1 m.
- Everything else (rocks, cypresses, olive stumps, candelabra_shrine, far
  landmarks) untouched.

### Clearances (checked by step 8 script, then P2.5 lint)

- Spawn ring r=3: nearest solid = well edge at 3.35 m (well moved to z=−4.6,
  F8). ✓
- Portal corridor z∈[−3,3], x∈[0,22]: casa fronts at z=±9.5; gate jambs start
  |z|≥1.6; well north edge z=−3.35. Arrival (16,0,0) is 0.55 m east of the gate
  plane, inside the 3.2 m opening, no solid within 1.1 m. ✓
- Street rule §1: plaza/street 19 m facade-to-facade ≥ 7 m. ✓
- Extent: farthest solid = chapel apse corner ≈ (−41, −33), r ≈ 52.7 < 55;
  play clamp 65 (`game/vordar-game/src/motion/movement.rs:23`). ✓

---

## 5. Collision mirror (chapter03) + D5 cross-check hand-off

**Prefab set** (all: `Transform + Hitbox(Aabb) + Solid + Anchored`, **no
ShapeGroup** per §3; one file each under `content/chapters/chapter03/prefabs/`):

- NEW `casa_small_a.ron` (3.0, 2.8, 4.0)·, `casa_small_b.ron` (2.8, 2.7, 3.7),
  `casa_two_story.ron` (3.5, 4.0, 5.0), `casa_corner_main.ron` (3.0, 2.8, 3.0),
  `casa_corner_wing.ron` (2.25, 2.5, 2.0 — pre-rotation w×d 4.5×4.0 as placed),
  `wall_segment.ron` (2.0, 1.5, 0.3), `gate_jamb.ron` (0.8, 1.8, 0.45),
  `gate_head.ron` (1.6, 1.0, 0.45; spawned at y≈4.6 over the opening),
  `well_basin.ron` (1.15, 1.4, 1.15 — square vs round, faces −0.10/corners
  +0.31 m; accepted approximation, noted for the P2.5 tolerance).
  ·(half_extents x,y,z at yaw 0; swap x/z at 90/270 by using the swapped
  literal in chapter.ron-facing prefab variants is NOT done — instead each
  spawn's prefab is authored per placed orientation only where needed; the two
  rows share orientation per row, so one prefab per type + per-90° variant only
  where a type appears in both orientations: here every casa appears only
  front→S or front→N (both z-facing, same AABB), gate/wall run along Z (one
  orientation) — **no variants needed in v1**.)
- UPDATED chapel prefabs (kit dims replace graybox near-match):
  `chapel_wall_side.ron` half (8.3, 5.5, 0.3); `chapel_wall_apse.ron` unchanged
  shape; `chapel_door_jamb.ron`, `chapel_lintel.ron`, `chapel_roof.ron`
  unchanged shapes — positions do the work.
- DELETED: `casa_long.ron`, `casa_block.ron` (swap rule — graybox visuals+shells
  fully replaced).

**chapter.ron initial_spawns** — every town prop T# gets spawns at the SAME XZ
(hitbox y-centering per graybox convention):

- T1..T8 → one spawn per casa at the prop XZ; casa_corner additionally spawns
  `casa_corner_wing` at prop XZ + world wing offset (derived from local
  (4.8, 1.0) under the confirmed yaw map, step 6).
- T9 chapel → 7 spawns, graybox pattern translated to center (−30, −29):
  side walls (−30, 0, −25.2) & (−30, 0, −32.8); apse (−38.4, 0, −29);
  jambs (−21.6, 0, −31.35) & (−21.6, 0, −26.65); lintel (−21.6, 7.1, −29);
  roof — west half only — (−34.4, 11.3, −29).
- T10 gate → `gate_jamb` at (15, 0, −2.4) & (15, 0, 2.4), `gate_head`
  at (15, 4.6, 0).
- T11 → `well_basin` (0, 0, −4.6). T12–T15 → `wall_segment` at each prop XZ.

Total ≈ 21 spawns / 14 prefab files.

**D5 cross-check contract for P2.5** (designed here, implemented there, in
`game/vordar-game/tests/content_lint.rs`): commit a per-type footprint manifest
`content/chapters/chapter03/footprints.ron` (numbers from §1's kit table —
constants from buildings.py, verified once against glb AABBs in step 3). Lint
asserts: (a) every start-zone prop whose model dir is a kit type has ≥1
chapter03 spawn at identical XZ (±0.01; composite types via the manifest's
member-offset list), and every chapter03 spawn maps back to exactly one prop —
bijection, no orphans; (b) each spawn's Aabb half-extents match the manifest
footprint within a stated per-type tolerance (well/apse carry theirs
explicitly); (c) prop yaw ∈ {0,90,180,270}; (d) no solid Aabb intersects the
spawn ring r=3 or the corridor rectangle; (e) all solids inside r=55.
P2.5 also re-aims the replication test: bot at spawn sees exactly the
within-r40 subset; bot walked to the chapel door sees all 7 chapel pieces.

---

## 6. Steps (worker-executable; cheap checks only — the workspace suite runs
once at the Phase 2 gate, not here)

- [x] **0. P2.4.0 texture dedup (option A, §2).** Files:
  `smirk/engine-renderer/src/mesh/store.rs`, `mesh/gltf_import.rs`,
  `game/vordar-game/tests/content_lint.rs` (VQ-C5 unique-image counting).
  Verify: `cargo test -p engine-renderer` green (goldens included);
  new unit test: two primitives sharing one glTF image yield one cached
  texture; `texture_memory_bytes()` for casa_corner drops from per-prim
  duplication to ~18-image cost — record the measured number in this file.
  **Measured (casa_corner.glb, 139 prims, BC sidecars bound): before
  2,332,045,256 B (2224 MB) → after 83,887,592 B (80 MB), 27.8×.** Dedup is
  content-hash keyed (`SharedImage.key` + srgb) in a MeshStore-wide cache, so
  identical images also share across models; images decode once per glTF
  image index (CPU-side dedup rides the same `Arc`). Lint now counts unique
  (content key, srgb) images across models, one load per model path —
  current content: 128.3 MB.
- [x] **1. Kit export switch + rebake.** (Shipped in `133662f`.) `scripts/asset-pipeline/build_town_kit.py`
  (+ `townkit/` as needed): glTF-separate export, shared texture files; rebuild
  all 9 types; run `townkit/verify.py` (green, incl. open-face + roof checks).
  Verify: 9 exports exist; per-file size ≤ a few MB; texture file set is shared
  (one copy on disk). GPU-light (Blender headless, no ComfyUI) — minutes.
- [x] **2. Install under `content/models/props/<type>/`** (9 dirs), run
  `node scripts/asset-pipeline/bake_textures.mjs gltf <asset>` per model;
  add 9 entries to `content/models/assets.json` (new `kind: "kit"`), extend
  `content/models/surface_classes.json` + the kit-aware branch in
  `prop_material_matches_surface_class` (per-material-name family table —
  the single-class assert cannot fit multi-material buildings, facts §1).
  Verify: `cargo test -p vordar-game --test content_lint` green pre-placement.
  **Done.** Shared textures installed ONCE at `content/models/townkit_textures/`
  (18 files); model URIs rewritten `textures/…` → `../../townkit_textures/…`
  at install (outside props/ so check_registry's dir↔assets bijection holds).
  Six kit families added to surface_classes.json (roughness 1.0 — the map
  multiplies; iron_wrought metallic 1.0); check_registry.py knows `kit`.
  Sidecars: 84 DDS (448 MB working tree) but only 18 unique blobs — texconv
  output is byte-identical across models, so git stores ~96 MB and the
  runtime content-hash cache residents each image once.
- [x] **3. Footprint manifest.** Write
  `content/chapters/chapter03/footprints.ron` from §1's table; one-off scratch
  check (scratchpad python, gltf parse) that each installed model's XZ AABB
  matches its manifest footprint ±0.1 m (catches export-frame surprises).
  **Done — with measured corrections the later steps must consume:**
  - §1's table lists wall-CENTERLINE footprints; built walls extend +0.6 m
    (one wall thickness) per axis. Manifest records outer extents:
    casa_small_a 6.6×8.6, casa_small_b 6.2×8.0, casa_two_story 7.6×10.6,
    casa_corner main 6.6×6.6 + wing 5.1×4.6 at offset (4.8, −1.0) (model
    frame: local Blender (4.8, 1.0) maps to glTF/world (4.8, −1.0)).
    ⇒ §5's prefab half-extents are stale (casa_small_a is (3.3, ·, 4.3),
    not (3.0, 2.8, 4.0)); step 4 authors from footprints.ron, and step 8
    re-checks §4's clearances (party walls now overlap 0.6, casa fronts sit
    0.3 closer to the street — still ≥ 7 m rule-clear).
  - Chapel nave runs along X in the model frame (door end +8.6, apse fan to
    −11.63; fan is +3.03 beyond the nave rectangle vs §1's ~2.5). Door→E =
    yaw 0. Footprint 20.23×8.2, tolerance 3.05 (fan uncollided past the flat
    apse wall).
  - well_basin 2.5×2.5 exact (tol 0.31), gate_arch 6.4×0.9 exact,
    wall_segment 4.0×0.6 (coping to 4.1×0.8). reja_set omitted (unplaced).
  Scratch check green: per type, size ≤ whole-model XZ AABB ≤ size + 2·tol.
- [x] **4. Collision prefabs.** Author/update/delete prefab files per §5
  (ShapeGroup stripped everywhere). Files: the 14 under
  `content/chapters/chapter03/prefabs/` + delete `casa_long.ron`,
  `casa_block.ron`. Verify: `cargo build -p chapter-03` + prefab RON parse via
  the replication test compile (run deferred to step 7).
  **Done — half-extents from footprints.ron outer sizes (not §5's stale
  centerline list); y = measured structure top / 2 (per-model glTF AABB):**
  casa_small_a (3.3, 3.13, 4.3), casa_small_b (3.1, 3.03, 4.0),
  casa_two_story (3.8, 4.49, 5.3), casa_corner_main (3.3, 2.87, 3.3),
  casa_corner_wing (2.55, 2.57, 2.3), wall_segment (0.3, 1.54, 2.0) and
  gate_jamb (0.45, 1.8, 0.8) / gate_head (0.45, 1.0, 1.6) authored in placed
  orientation (run along Z), well_basin (1.25, 1.43, 1.25),
  chapel_wall_side (8.3, 3.75, 0.3) — built walls are 16.6 long and top at
  the 7.5 springline, the vault is the roof slab's job —
  chapel_wall_apse (0.3, 3.75, 3.8), chapel_door_jamb (0.3, 3.75, 1.3),
  chapel_lintel (0.3, 2.15, 1.2), chapel_roof (4.0, 0.3, 3.5).
  No lib.rs dereg needed: prefabs load via `add_prefab_dir`.
- [x] **5. chapter.ron spawns** per §5 table. Verify: RON parses
  (`cargo test -p vordar-game --test content_lint` still compiles/loads).
  **Done — 25 spawns / 14 prefabs (§5's ≈21 undercounted). Yaw map verified
  once from `presentation.rs:154` `Quat::from_rotation_y(yaw.to_radians())`
  with kit door facade = −Z: yaw 0 → door S, 90 → W, 180 → N, 270 → E;
  chapel door end +X, so door→E = yaw 0. Member offsets rotate the same way
  (yaw 180 maps (4.8, −1.0) → (−4.8, 1.0)): wings at (11.4, 11.5) / (−10.8,
  −11.5). Chapel spawns adjusted to measured kit geometry (0.6 walls,
  per-node glTF AABBs): jambs (−21.7, 0, −26.5)/(−21.7, 0, −31.5) — built
  east-wall pieces are 2.6 wide centred z=±2.5, not §5's ±2.35; lintel
  (−21.7, 5.35, −29) spanning door head 3.2 → wall top 7.5, not graybox 7.1;
  apse (−38.3, 0, −29); roof (−34.0, 10.2, −29) — vault covers local
  x∈[−8,0], crown 10.5; side walls (−30, 0, −25.2)/(−30, 0, −32.8) as §5.**
- [x] **6. zones.ron props + dressing edits** per §4, after confirming the
  yaw→facing convention with ONE zone_review render of T2 (door must face the
  plaza); then fill every yaw in the table. Also update
  `client/vordar-client/src/bin/zone_review.rs:87` NAVE_TARGET →
  (−30.0, EYE_HEIGHT, −29.0). Verify: `zone_visual_refs_load` +
  `total_texture_memory_within_budget` green.
  **Done — yaw map confirmed visually (probe renders: casa_small_a yaw 0
  shows blank N/E backs, casa_small_b yaw 180 shows its door on the north
  face, casa_two_story yaw 270 shows its door on the east face — the 270
  probe also pins the rotation chirality): yaw 0→S, 90→W, 180→N, 270→E as
  established. Walls/gate placed at yaw 90 (local width axis → world Z,
  matching the collision prefabs' placed orientation).**
  **Layout fix the table needs: §4's T6 wing (yaw 180 locks the wing to −X)
  interpenetrated T5 by 4.6 m. South-row slots swapped — casa_corner takes
  the row's WEST end (−12.0, ·, −12.5), wing outward at (−16.8, ·, −11.5),
  casa_small_a takes (−6.0, ·, −13.5); mirrored in chapter.ron. Both types
  are 6.6 m outer width, so every party-wall line is unchanged; this mirrors
  the north row (corner at the row end, wing outward).**
  **zone_review reworked to match the prop-visual world: interior shots draw
  the placed props (chapter prefabs are collision-only, so the old
  chapter-geometry path rendered nothing — dead merge in render_wide
  removed); NAVE_YAW_APSE/DOOR were inverted vs their comments and are now
  apse = eye east (az 0), door = eye west (az π), verified from the frames.
  Lints 15/15 green.**
- [x] **7. Replication test update.** `server/vordar-server/tests/zones.rs:161-171`:
  assert the spawn-visible subset (all spawns with r ≤ 40 from origin — every
  town spawn except the 7 chapel pieces at r ≈ 41–43 and wall fragments as
  computed) replicates at spawn; leave the walk-to-chapel extension to P2.5.
  Verify: `cargo test -p vordar-server --test zones` (this one test) green.
  **Done — the bot is the server's first connection (ConnId starts at 1,
  `engine-net/src/server.rs:369`), so it spawns at (2.12, 0, 2.12) on the
  r=3 ring, not the origin; AOI distance is 3D (`broadcast.rs:136`).
  Within-r40 subset: 20 of 25 spawns — everything except chapel_wall_side ×2
  (42.2 / 47.5), chapel_wall_apse (51.0), the south chapel_door_jamb (41.2)
  and chapel_roof (48.8); the north jamb (37.2) and lintel (39.6) are in.
  Test asserts exact per-prefab counts, including 0 for the beyond-r40
  pieces. `cargo test -p vordar-server --test zones` green (6/6).**
- [x] **8. Geometry self-check + evidence.** Scratchpad script asserts §4's
  clearance list (AABB vs spawn ring / corridor / pairwise overlaps / r≤55).
  zone_review full pass on start (wide + mid + both interiors) — renderable
  now that step 0 landed; frames to `target/town-layout/p24/` for the Phase 2
  gate judge. Verify: script exit 0; frames non-black; interior shots show the
  relocated nave.
  **Done — script (25 solids from chapter.ron × prefab half-extents) exit 0:
  spawn-ring nearest ground solid = well_basin at 4.25 m (> 3); portal
  corridor clear of ground solids except the two gate jambs whose faces sit
  exactly at |z| = 1.6 (the 3.2 m opening); 12 intersecting pairs, all
  expected — 6 party walls at 0.60 m, 2 wing↔main at 1.05 m (kit-structural:
  the wing tucks into the main block), 4 chapel joints at 0.30 m; farthest
  corner chapel_wall_apse r = 50.65 ≤ 55. Frames: wide, mid_00-02 (mid_02 =
  plaza with south-row doors + well), interior_apse, interior_door (relocated
  nave looking east through the open door, vault-collapse rubble on the
  floor), 18 closes, contact_sheet. Wide is fog-heavy at the ~130 m turntable
  fit — authored zone fog, not a defect (gameplay orbit is 34 m). Replication
  test re-run green after the south-row spawn moves (all three stay within
  r40, counts unchanged).**
- [x] **9. Erasure sweep.** Confirm deleted: casa_long/casa_block refs,
  graybox ShapeGroups, any stale graybox coordinates in comments
  (chapter.ron header layout note rewritten to the new numbers). Update
  `tasks/todo.md` P2.4 entry; strike this subplan's boxes.
  **Done — zero casa_long/casa_block references repo-wide; graybox mentions
  survive only in chapel_probe.rs (left alone per §1) and its helper
  chapter_geometry.rs (now chapel_probe's sole consumer — dies with it in
  Phase 4); the old graybox NAVE_TARGET and zone_review's chapter-geometry
  drawing are gone.**

Steps 0–1 are the only ones ahead of content edits; 2–6 are sequential file
work; 7–8 close the loop. Suite-wide run: Phase 2 gate only.

---

## 7. Open questions / user checkpoints

1. **P2.4.0 scope pull** (§2): renderer texture-dedup debt executes now, inside
   P2.4, as option A. Recommended·proceed — no outcome-close alternative
   exists (weights in §2). Flagged because it re-orders the queued renderer
   debt, which is scheduling the user may want to own.
2. **Chapel door east vs premise §6 "west doors"** (facts §1): recommend keep
   the built east door (faces the town approach; graybox + kit + G2 evidence
   all east) and amend `docs/town-premise.md` §6 one line. Outcome 8/10 vs
   rebuilding the kit door west 4/10 (cost MEDIUM, zero visible gain — the
   yaw can point the door anywhere; "west" only mattered liturgically).
   Confidence HIGH. User owns the binding premise doc → bundled ask, not taken.
3. **reja_set unplaced in v1** (§1 table): grilles already exist on casa
   windows; a standalone placement has no premise slot. Recommend: keep the
   glb in the kit, place none. Outcome-neutral; flag only so the kit piece
   isn't read as forgotten.
4. **AOI Option 1** (§3): decided (no reasonable alternative), logged — listed
   here per the decided-while-unsure protocol, not as an ask.
