# OpenMMO vs vordar — comparative analysis (2026-07-22)

Source: https://github.com/Julian-adv/OpenMMO, cloned read-only at `reference/OpenMMO`
(gitignored). **License: PolyForm Noncommercial 1.0.0** — study only; per our
strict-NC ruling no code or assets from it may enter vordar. Techniques and ideas only.

What it is: a solo-developed, AI-assisted ("vibe-coded") browser MMO, publicly playable.
Svelte + Three.js/Threlte (WebGPU) client, Rust/Tokio server, a shared Rust crate
compiled both natively and to WASM, and an agent-client so LLM NPCs connect through the
same WebSocket protocol as humans. Fully procedural 32×32 km world baked offline.

---

## 1. How they do models and textures (our biggest problem)

### Characters / monsters — cloud image-to-3D, minimal rigor
1. **Concept art**: ComfyUI (local) with `jibMixZIT` or **Z-Image Turbo** — the same
   model family we ruled on 2026-07-20 — plus Gemini/ChatGPT/Grok for some.
2. **Pose normalization**: concept is forced into T/A-pose using **Nano Banana (Gemini)
   or Qwen Image Edit** before 3D conversion. A dedicated step, documented per character.
3. **Image→3D**: **Meshy.ai (paid)** for nearly all characters; Tripo once (flagged as a
   license risk in their own docs and never used again); **create.verse8.io** for
   monsters. All cloud, all paid, none reproducible.
4. **Rigging/animation**: **Mixamo auto-rig**, one canonical 65-bone Mixamo skeleton for
   every humanoid; stock Mixamo clips retargeted via Blender scripts
   (`import_mixamo_animation.py`: quaternion retarget `target_rest⁻¹ × source_rest ×
   source_basis`, root translation never baked — in-place clips only).
5. **In-house GLB editor** (SvelteKit+three.js dev tool): fuzzy/Levenshtein bone-name
   standardization to the canonical skeleton, clip extraction into shared animation-pack
   GLBs (`locomotion/combat_melee/social/offhand`), SkeletonUtils retargeting with
   hip-scale correction.

Quality reality of their AI meshes:
- **Albedo-only** — no normal/roughness/AO maps on any AI-generated asset; the
  image-to-3D service's baked texture ships as-is.
- **No retopo/decimation discipline**: characters ship at native Meshy density
  (13–15.6 MB GLBs); exactly one was ever remeshed (to 10k tris). A saved one-off
  Blender script hardcoded to a `tripo_node_*` mesh shows raw Tripo output needed
  manual duplicate-vertex welding.
- Scale is calibrated **by eye** in Blender against the player model.

### Everything that actually looks good is NOT AI
- **Terrain/buildings/dungeon surfaces: Poly Haven CC0 photoscanned PBR sets**
  (diffuse+normal+ORM, 1K), repackaged as GLB "material carriers", blended through a
  16-slot splatmap (4 bytes/cell, corner-sampled bilinear blend, 4×4 512px atlas).
- **Buildings are not meshes at all**: parametric room composer (rects on a 1m grid,
  per-segment wall configs Solid/Door/Window/Open, procedural roofs/jetties/stairs)
  generates all geometry in TypeScript, textured with the Poly Haven carriers,
  ~4–5 draw calls per house.
- **Grass has no mesh or texture** — fully procedural blades, GPU-compute wind.
- **Props/items/weapons: Sketchfab/Fab downloads** (CC-BY mix), icons are Blender
  screenshots.

### Verdict vs our pipeline
Theirs is a **velocity pipeline**: cloud services + Mixamo got 14 characters, 6
monsters and a playable game shipped fast, at the cost of albedo-only texturing,
unbounded poly counts, unreproducible generations, and a license surface (Meshy tiers,
Tripo terms, verse8 unknowns, CC-BY attribution mix) that likely forced their NC
license. Ours is a **rigor pipeline**: local Hi3DGen + ComfyUI, seeded end-to-end,
manifest provenance, cleanup/symmetrize, depth-conditioned multiview texturing with a
scored bakeoff, strict license policy. We are slower per asset but own every step;
nothing in their character results suggests trading our rigor for their speed — their
own docs treat character visuals as the weak link vs their hand-engineered
terrain/water/lighting.

**Ideas actually worth taking:**
1. **Pose-normalization stage before image→3D.** Forcing the concept into a clean
   T/A-pose (they use Qwen Image Edit — our documented fallback model) before geometry
   is a cheap, discrete step that directly attacks rig quality. We should evaluate it in
   gen_character's concept stage.
2. **Don't AI-generate commodity surfaces.** Their best-looking pixels are CC0
   photoscans through a splatmap. For terrain/architectural materials, Poly Haven-class
   PBR + blending beats per-surface AI generation; reserve the AI texture pipeline for
   unique props/characters where no photoscan exists.
3. **Parametric architecture + material carriers** instead of AI-meshing whole
   buildings: geometry from code, realism from photoscanned PBR. If/when vordar needs
   towns, this sidesteps the hardest AI-mesh class entirely (and matches our
   semi-realistic direction better than AI building meshes would).
4. **One canonical skeleton + a bone-name normalizer** as an enforced pipeline gate.
   We already target Mixamo-standard rigs; their recurring `mixamorig` name-mismatch
   bug class shows why normalization should be an automated step, not a convention.
5. **In-engine A/B trials for material candidates** (they trialed 9 dungeon wall
   textures, kept a note file with runner-ups) — cheap, honest selection method;
   analogous to our bakeoff but for sourced materials.

---

## 2. Rendering / visual quality

| | OpenMMO | vordar |
|---|---|---|
| Engine | Three.js/Threlte, WebGPU, browser | smirk (custom wgpu, native) |
| Tonemapping/post | **None at all** — no exposure, no grading, hand-tuned intensities against Three defaults | HDR pipeline, tonemapped; visual-quality spec (VQ-*) |
| IBL | Generic Three `RoomEnvironment` probe; terrain gets **zero** IBL | Dusk HDRI environment, IBL part of art direction |
| Shadows | 2-cascade CSM (4096 high tier) + exactly **one** shadow-casting point light scene-wide | Cascaded shadow maps, recently landed + tuned |
| Sky/time | Real celestial sim: sun latitude/declination/axial tilt, **two moons** with phase-driven light; smooth twilight blending | Fixed dusk HDRI; DayNightSystem parked (VQ-D5: day/night must ride sun + IBL exposure) |
| Water | Strongest system: unified sea/river Gerstner shader, depth-buffer shoreline, Beer-Lambert absorption, offline-baked per-tile river flow fields (RFD1), dual-phase flowmaps | Not yet a focus |
| Vegetation | GPU-compute per-blade wind + player bending; procedural blades | Not yet a focus |
| LOD | None — instance caps + chunk radii only | — |

Their lighting *simulation* (celestial math) is ahead of ours; their lighting
*rendering* (no tonemapping, canned IBL) is well behind. The interesting artifact for
our parked DayNightSystem: they drive one directional light + ambient + a
static-texture environment whose intensity is time-scaled — and the result visibly
suffers from the environment map not matching time of day. That is concrete evidence
for VQ-D5's stance: day/night has to go through sun + IBL exposure together, or not
at all.

Performance engineering is disciplined and documented with before/after tables
(load 40s→15s; 60fps holds): pre-baking procedural noise to textures (their single
biggest pipeline-compile cost), alternate-frame half-res reflection/refraction,
quality tiers that gate whole subsystems, shadow-light count kept constant to avoid
WebGPU pipeline recompiles.

## 3. Architecture / netcode

- **Shared-crate-via-WASM parity** (their standout): collision/passability, A*,
  monster behavior trees, dungeon generation, and protocol types are one Rust crate
  compiled natively (server, agent-client) and to WASM (browser). Movement is
  client-predicted / server-reconciled-on-disagreement-only because both sides run
  bit-identical collision code. Dungeons regenerate deterministically from a seed on
  both sides (golden-hash tested) so layouts are never sent over the wire. We get the
  same property for free with an all-Rust stack — worth keeping deliberate as crates
  split.
- **Monster AI is client-delegated**: each client simulates the monsters it "owns" and
  reports moves; the server referees (spawn caps, token-bucket move rate, all dice/HP
  math). Scales server compute with players, not monsters — but monster paths are
  rate-limited, **not collision-verified**: a modified client can walk its monster
  through walls. A real trust hole we should not copy.
- Interest management: 43m-radius spatial hash, event fan-out via per-player mpsc
  channels; the global broadcast channel is used for exactly one message (8s time
  sync). Cylindrical world seam handled by querying the grid at ±world-width.
- No game tick; a swarm of independent interval loops (movement at 5 Hz) each
  panic-isolated. Single process, one `Arc<GameState>` of RwLock'd HashMaps — a real
  contention ceiling at their stated 5000-CCU target.
- Persistence: SQLite (rusqlite+r2d2) for characters, dirty-batched every 32s via
  spawn_blocking; flat per-house/per-region JSON for world authoring; monsters/ground
  items deliberately soft state. Similar spirit to our SQLite + background save worker.
- Protocol: MessagePack binary over WebSocket, delta-only, mandatory version handshake.
  Their noted rmp-serde positional-encoding gotcha (field skipping corrupts the wire)
  is worth remembering if we ever use MessagePack.
- LLM NPCs: deterministic behavior trees for combat (never blocked on an LLM);
  LLM only for conversation/trade, via Claude Code CLI subprocess (their MCP interface
  is aspirational — rmcp dependency unused). Server-side invariant enforcement for
  LLM trades (price band clamped server-side, wallet caps) is textbook
  treat-the-LLM-as-adversarial design.

## 4. World / content systems

- Worldgen is production-grade: two-tier resolution (8m global / 1m tile), hydraulic
  erosion port, priority-flood rivers with meander post-processing, habitability-driven
  settlement placement, MST+A* road network with auto bridges, all baked offline once
  (262k tiles) and served as static tiles. X axis is truly cylindrical (3D Perlin on a
  circle), not seam-blended.
- One `river_geom.rs` is the single source of truth for river width/taper so heightmap
  carve, splat band, bridge selection, and the water shader can never disagree — a
  good pattern name for our own cross-system constants.
- Housing: parametric rooms (above), cell-bitmask passability per floor shared verbatim
  client/server, door toggles flip one edge bit.
- In-game map editor (height/splat/road/zone/NPC/object) writing through the same REST
  tile API the generator uses — editor output is indistinguishable from bake output.
- Hand-authored content is a thin slice: 6 monsters, 23 items, 2 named NPCs,
  1 dungeon entrance (procedurally expanded to 5–20 floors). Systems >> content,
  same stage of life as us.

## 5. Overall verdict

**They do better:** shipping (publicly playable); asset velocity; procedural worldgen
breadth and rigor; water/vegetation shader engineering; celestial simulation;
WASM-parity netcode; LLM-NPC economy with server-clamped invariants; devlog +
per-asset provenance ledger discipline (license/tier/date per asset, unused entries
tagged).

**They do worse:** rendering foundation (no tonemapping/exposure/post, canned IBL,
terrain excluded from IBL); AI asset quality control (albedo-only, no retopo, by-eye
scale, unreproducible cloud generations); license hygiene of the asset mix (their NC
license is partly a consequence); monster-AI trust model; single-process lock-ceiling
server; docs drifting from shipped code (their water docs describe a superseded
pipeline).

**Directly actionable for vordar** (ranked):
1. Evaluate a pose-normalization (A/T-pose) image-edit step in gen_character's concept
   stage.
2. Commodity surfaces from CC0 photoscan PBR (Poly Haven) + splat blending; keep the
   AI texture pipeline for unique assets.
3. When towns/buildings arrive: parametric geometry + photoscan material carriers, not
   AI building meshes.
4. Automate skeleton/bone-name normalization as a pipeline gate.
5. DayNightSystem (when unparked): their static-IBL day/night confirms VQ-D5 — sun and
   IBL exposure must move together.
