# AA Visual Prototype — Semi-Realistic Dark Fantasy (Player + Environment)

## Context

The game currently reads as a minigame: low-poly KayKit characters, flat Lambert shading, no shadows/post/HDR, untextured particle discs, and a bare ground slab. The user wants an **AA look prototype** that sets the game's theme — **semi-realistic dark fantasy** (Diablo IV / Lost Ark vibe) — focused on the **player character and the environment**. Enemies are explicitly out of scope (they stay as placeholder ShapeGroup blobs until real enemy design happens later). KayKit's low-poly style is rejected ("looks cheap/mobile").

Exploration found the plumbing is solid and reusable: skinned glTF pipeline with skeletal animation (crossfades, one-shots, bone sockets), glTF import, CPU particle sim, orbit camera, good network smoothing, and a GPU-free testable core (`anim.rs`, `load_gltf_data`). What must be built for a semi-realistic AA look: **full PBR shading (normal maps, tangents, metallic-roughness), image-based lighting from HDRIs, shadow mapping, HDR + tonemap + bloom + MSAA + mipmaps, textured VFX, and a real environment** — plus a new character asset pipeline replacing KayKit.

**Asset strategy (all license-safe):**
- **Characters + animations: Mixamo** (free Adobe, royalty-free in games). ⚠️ The one manual step: Mixamo has no API — the **user downloads** the FBX files per a shopping list I provide (can happen in parallel with renderer work). Conversion FBX→glTF is automated headlessly via **Blender CLI** (Blender 5.2, installed, driving the pipeline since Phase A0).
- **Environment: Poly Haven** (CC0; has a public API for scripted downloads) — PBR texture sets, HDRIs (sky + IBL source), rock/tree/prop models — plus **ambientCG** (CC0 PBR textures) as backup.
- **Renderer test assets: Khronos glTF sample models** (DamagedHelmet etc., CC0) so PBR/IBL work is verifiable before any game asset lands.
- **VFX: Kenney particle pack** (CC0 grayscale glows/smoke — style-agnostic) tinted at runtime.
- Provenance tracked in `content/source/CREDITS.md`.

Deliverables: (1) `docs/visual-quality.md` quality-bar rules; (2) phased implementation, one commit series per phase; headless verification only — the user does manual feel-checks in the sandbox at phase boundaries.

---

## Part 1 — Quality bar document (`docs/visual-quality.md`)

Rules have IDs (`VQ-xx`); **machine-checked** rules name their enforcing test, **eyeball** rules get a written check procedure. Enemy-specific rules are written now, marked *deferred until enemies land*.

**A. Art direction (eyeball)**
- VQ-A1: Semi-realistic dark fantasy: realistic proportions, PBR materials, moody desaturated palette with warm accent light (fire/ember/magic). No flat-shaded or low-poly-stylized assets; no toon outlines.
- VQ-A2: Every surface is PBR-textured (albedo + normal + roughness at minimum). Untextured flat color is placeholder-only, never shipped.
- VQ-A3: New asset packs require a side-by-side cohesion screenshot in the sandbox before adoption (texel density and realism level must match).
- VQ-A4: Reserved color language: player VFX cool/arcane hues, threat/telegraph red-orange, ambient world desaturated. Documented as HSV ranges.
- VQ-A5: Lighting sells the theme: low sun/dusk HDRIs, fog depth, emissive accents (portals, magic) — bright noon-neutral scenes are off-theme.

**B. Characters (machine-checked; enemy clauses deferred)**
- VQ-B1: Every combat-relevant entity renders as a rigged glTF mesh with min clip set idle/walk/run/attack/hit/death. *(Players: enforced now; enemies: deferred.)* SDF ShapeGroup is dev-fallback only.
- VQ-B2: Rigged assets: ≤ 64 joints (engine palette cap), height-normalized feet-on-ground, `forward_offset` documented, ≤ 16 MB on disk (realistic textures are heavier than low-poly; budget revised from 3.5 MB).
- VQ-B3: Character rigs expose sockets (right/left hand, head) via the per-race socket-bone mapping; every socket named in RON exists in the glb.
- VQ-B4: Every clip named in a `.ron` exists in the referenced `.glb` (content-lint via `load_gltf_data`).

**C. Materials & textures (machine-checked)**
- VQ-C1: Every filtered texture has a full mip chain; samplers use anisotropic filtering (≥ 8x) for surfaces.
- VQ-C2: sRGB correctness: albedo/emissive sRGB; normal/metallic-roughness/AO linear.
- VQ-C3: Anything "magical" uses HDR emissive (> 1.0) so bloom picks it up — no fake glow via bright albedo.
- VQ-C4: Normal maps present on all environment surfaces and characters; tangents present or generated at import.
- VQ-C5: Texture budgets: ≤ 2k per character map, ≤ 4k per tiling environment set; total texture memory ≤ 1 GB.

**D. Lighting & framebuffer (machine-checked where possible)**
- VQ-D1: Scene renders HDR (Rgba16Float), tonemapped (ACES/AgX) before UI composite.
- VQ-D2: Image-based lighting from the zone HDRI (diffuse irradiance + specular prefilter + BRDF LUT); the same HDRI is the visible sky.
- VQ-D3: Directional sun with real shadows (PCF); every grounded entity casts and receives.
- VQ-D4: MSAA 4x on the scene pass (documented fallback if unsupported).
- VQ-D5: Day/night flows through sun + IBL exposure via the existing `DayNightSystem` seam, never per-material hacks.

**E. VFX & feel (machine-checked count, eyeball quality)**
- VQ-E1: Every ability has three VFX beats: cast (at hand socket), travel (trail/beam), impact (scaled by outcome). Content-lint checks `classes/*.ron` abilities against the VFX registry.
- VQ-E2: Every death has an effect; every hit has flinch + impact particles.
- VQ-E3: Particles are textured (atlas), soft (depth-fade), support additive and alpha blend.
- VQ-E4: Telegraphs legible: contrast vs ground, ≥ 0.4 s lead time.

**F. Performance budgets (machine-checked via benchmarks)**
- VQ-F1: 60 fps @ 1080p in a stress scene (40 skinned characters, 2k particles) on the dev GPU.
- VQ-F2: ≤ 256 skinned instances (engine cap) until raised deliberately; ≤ 4096 live particles.
- VQ-F3: Frame never allocates unbounded per-entity GPU resources.

**G. Verification policy**
- VQ-G1: Every renderer feature lands with a headless test — pure-CPU unit test (pattern: `anim.rs`, `load_gltf_data`) or offscreen-render readback with **analytic** assertions (darker-than, coverage %, monotonic — never exact pixels). GUI checks are manual-only, listed in a feel-checklist appendix.

---

## Part 2 — Phases (ordered; each shippable; one commit series each)

### Phase 0 — Hygiene + headless harness + quality doc
1. **Commit the current working tree as-is** (everything is uncommitted on `main`, 3 commits total) so all renderer surgery is bisectable.
2. Write `docs/visual-quality.md` (Part 1) and `content/source/CREDITS.md`.
3. **Offscreen render harness**: extract the Main Pass target in `smirk/engine-renderer/src/lib.rs` so it can render to an offscreen texture (pre-stages the HDR retarget). New `smirk/engine-renderer/tests/offscreen.rs`: render → buffer readback → analytic assertions; skips cleanly with no adapter; uses RGBA8 assets (fallback adapters lack BC7).
4. Content-lint test (`game/vordar-game/tests/content_lint.rs`) starting with VQ-B4 for races.
5. Fetch Khronos PBR sample models (DamagedHelmet, MetalRoughSpheres — CC0) into `content/source/test/` as renderer test fixtures.
6. **Hand the user the Mixamo shopping list** (see Phase 5) so downloads happen in parallel.

Verify: `cargo test --workspace` headless; content-lint green on current assets.

### Phase 1 — Full PBR materials (foundation; changes every surface)
- Extend `mesh.rs` import to read the whole glTF material: normal, metallic-roughness, emissive, occlusion textures + factors (currently parsed-past; only base_color is read).
- Add **tangents** to `Vertex`/`SkinnedVertex` (read from glTF; generate via mikktspace-style algorithm when absent — pure CPU, unit-testable).
- Material bind group grows to albedo/normal/MR/emissive/AO + sampler (1×1 neutral defaults per slot so untextured content keeps working).
- **Cook-Torrance GGX BRDF** in `mesh_shader.wgsl` / `skinned_mesh_shader.wgsl` (primitive `shader.wgsl` gets the same lighting math with uniform material params).
- **Mipmaps + anisotropic filtering**: render-pass blit chain (`mipgen.rs` + `mipgen.wgsl`) for RGBA8 textures at load in `texture.rs`; DDS loader reads all baked levels instead of forcing `mip_level_count: 1`; sampler anisotropy 8x. (Mipgen blit infra is reused by IBL prefilter and bloom.)

Files: `smirk/engine-renderer/src/{mesh.rs, texture.rs, pipeline.rs, mesh_pipeline.rs, skinned_pipeline.rs}`, all three geometry WGSL; new `mipgen.rs`, `mipgen.wgsl`, tangent-gen module.
Verify (headless): tangent-gen unit tests (orthonormality, handedness on known quads); mip-chain unit test (checkerboard mip1 averages mid-gray); offscreen render of MetalRoughSpheres — roughness-0 sphere has tighter/brighter specular peak than roughness-1 (analytic region compare).

### Phase 2 — HDR + tonemap + MSAA + IBL sky (the theme-setter)
- **HDR**: Main Pass → `Rgba16Float` offscreen (swap of Phase 0 target), fullscreen **ACES/AgX tonemap** pass with exposure uniform → swapchain → egui unchanged. Clear color and `DayNightSystem` tints move to linear HDR.
- **MSAA 4x**: multisampled HDR target + resolve; all pipelines `sample_count: 4` (query support, fall back to 1). Same phase as HDR to touch descriptors once.
- **IBL**: load a Poly Haven `.hdr` (Radiance format — via `image` crate), equirect→cubemap, **diffuse irradiance convolution + specular prefilter mips + BRDF LUT** (compute once at zone load with render passes reusing the blit infra). Ambient term in the PBR shaders switches from flat ambient to IBL. **Skybox pass** renders the same HDRI cubemap behind the scene — the slab world instantly has a dark-fantasy sky and correct ambient mood.

Files: `lib.rs`, `camera.rs` (light/exposure uniforms), new `post.rs`, `tonemap.wgsl`, `ibl.rs`, `ibl.wgsl`, `sky.wgsl`; `texture.rs` (.hdr float textures); `Cargo.toml` (+`image` crate, hdr feature); PBR shaders gain IBL ambient.
Verify (headless): readback — emissive 8.0 tonemaps < 1.0 and > a 1.0 emitter (monotonic, no clip); MSAA diagonal-edge pixel intermediate; IBL — white-furnace-style sanity (uniform white HDRI ⇒ sphere shading ≈ flat within tolerance) and sky pixels non-black where no geometry.

### Phase 3 — Shadow mapping (grounds everything)
Single fitted orthographic cascade (camera is a bounded orbit radius 16–55 over compact zones; CSM deferred): 2048² depth map fitted to the visible AABB, PCF 3×3, slope-scaled bias, texel-snapped light origin (no orbit shimmer). Depth-only pre-pass with depth-only variants of the three geometry pipelines (skinned variant re-binds the existing joint storage buffer). Particles don't cast.

Files: new `shadow.rs`, `shadow.wgsl`, `shadow_skinned.wgsl`; edits to `lib.rs`, `camera.rs` (`light_view_proj`), the three pipeline files + their shaders.
Verify (headless): offscreen — cube above ground, sun 45°: band under cube darker than open ground; lit face unchanged vs shadows-off render.

### Phase 4 — Bloom + emissive
Dual-filter Kawase bloom: soft-knee prefilter from the HDR resolve, 5–6 downsample/upsample levels on the blit infra, composited in the tonemap pass. Route emissive content through it: glTF emissive (now imported), portal monuments, projectiles, telegraph accents in HDR emissive; night scenes get payoff.

Files: `post.rs`, `tonemap.wgsl`, new `bloom.wgsl`, `client/vordar-client/src/presentation.rs`, content `.ron`s.
Verify (headless): readback — small HDR-bright quad on black: energy present beyond quad rect with bloom on, absent with it off.

### Phase 5 — Character pipeline: Mixamo replaces KayKit (player becomes AA)

**SUPERSEDED (2026-07-23):** the AI character pipeline replaced this Blender-merge approach — machinery: `tasks/ai-pipeline/a4.md`; production character swap: Phase B4 of `zesty-bubbling-acorn.md`. The Mixamo *clip library* remains the durable asset (on disk, in use); the build steps fenced below are historical and do not execute.

> - **User's manual step (parallelizable from Phase 0):** download from mixamo.com per my shopping list — per race archetype: 1 character FBX (with skin, T-pose) + clips idle/walk/run/3 attacks/hit/death (FBX, without skin, 30 fps, in-place) into `content/source/characters/mixamo/<race>/`. I pick the specific characters/clips (dark-fantasy appropriate) and write the list in Phase 0.
> - **Install Blender via winget** (headless CLI use only). New `scripts/asset-pipeline/build_character.py` (Blender `-b -P`): import character FBX, import each animation FBX and merge onto the rig as named actions (rename Mixamo clip names → our clip names), normalize height/feet-on-ground, export `.glb` with tangents. Then a gltf-transform post-step (evolves `scripts/preprocess-characters/preprocess.mjs`): prune, dedup, resize textures to ≤ 2k, verify (clips present, ≤ 64 joints, ≤ 16 MB).
> - **Socket remap**: Mixamo bones are `mixamorig:RightHand` etc. — make socket bone names data-driven per race (extend `RaceModel` in `game/vordar-game/src/player/class.rs` with a socket map; `SocketConfig` consumes it) instead of hardcoded `handslot.r/l/head`.
> - Update `content/races/*.ron` (4 races → new models + clip names + speeds + forward_offset), retire class `outfit`/`tint` SDF-era fields for mesh races (keep schema, neutral values), delete nothing — KayKit sources stay until the user confirms the look.
> - Locomotion/react/vfx systems work unchanged (they key off `LocomotionClips`/`AnimController`).
>
> Files: `scripts/asset-pipeline/` (new), `content/races/*.ron`, `game/vordar-game/src/player/class.rs`, `smirk/engine-renderer/src/mesh.rs` (socket config plumbing), `content/models/`.
> Verify (headless): content-lint VQ-B1–B4 on the new glbs via `load_gltf_data` (clips, joints ≤ 64, sockets exist, size); existing `body.rs`/locomotion tests updated to the new assets.
> **Block-resilience:** if Mixamo downloads aren't available when I reach this phase, I proceed to Phase 6 and return.

### Phase 6 — Environment set dressing (zones stop being slabs)
- **Ground**: replace the procedural slab pattern with a real mesh — gentle heightmap-displaced grid + tiling Poly Haven PBR set (albedo/normal/roughness, e.g. rocky forest floor), UV-tiled with the Phase 1 material path; per-zone texture set + fog color/density in zone RON.
- **Props**: Poly Haven CC0 models (rocks, dead trees, ruins-adjacent props) fetched via its API by a `scripts/asset-pipeline/fetch_polyhaven.mjs`; static-prop preprocessing (normalize scale/origin, prune, dedup, ≤ 2k textures); placed via `props: [...]` list in `content/zones/zones.ron`, rendered through the existing static mesh pipeline (the `mesh_probe` path proves the seam).
- **Theme pass on the start zone**: dusk HDRI, fog, emissive portal monuments, scattered silhouetted props — this is the "starting point to base the theme of the game."
- Distance fog already added in shaders (Phase 2 exposure/IBL work); tune per zone here.

Files: `client/vordar-client/src/presentation.rs`, `content/zones/zones.ron` + zone schema loader, `scripts/asset-pipeline/`, `content/models/props/`, `content/textures/`.
Verify (headless): content-lint — every zone prop/texture ref loads; offscreen zone render — ground texel variance > threshold (non-flat), sky non-black.

### Phase 7 — Player VFX quality pass (textured particles)
- Particle **texture atlas** (Kenney CC0 glows/sparks/smoke, runtime-tinted) + sampler in `particle_pipeline.rs`; per-particle atlas cell + blend flag (additive vs premultiplied-alpha variants); **soft particles** (depth-fade using the scene depth buffer — available since the HDR pass owns its depth); **stretched billboards** for projectile trails (velocity-aligned, replaces mote spam).
- Data seam: `content/vfx/*.ron` effect defs (emitter shape, atlas cell, color/size-over-life, caps) referenced by ability id — `vfx.rs` stops hardcoding bursts; VQ-E1 becomes checkable.
- Rebuild the player's cast/travel/impact effects (bolt, leap, telegraph) to theme standard (cool arcane player hues per VQ-A4).

Files: `particle_pipeline.rs`, `particle_shader.wgsl`, `client/vordar-client/src/vfx.rs`, new `content/vfx/` + loader, `content/classes/*.ron`, atlas in `content/textures/`.
Verify (headless): content-lint VQ-E1 + atlas-cell ranges; `ParticleSim` CPU unit tests (counts, lifetimes, caps).

### Phase 8 — Perf guardrails (light — no enemy crowds yet)
GPU timestamp timing in the dev overlay; warnings at > 80% of `MAX_SKINNED_INSTANCES`/`MAX_PARTICLES`; benchmark CPU joint-palette and PBR-material bind costs in `benchmarks/` as the baseline for the future enemy influx. Frustum culling / instance-cap raises deferred until enemies exist.

---

## Out of scope (deliberate)
- **Enemies/NPCs** — stay as ShapeGroup blobs; no enemy meshes or creature pipeline. Quality rules written but deferred.
- CSM, SSAO, TAA, GPU particles, LOD, frustum culling, KTX2/Basis — listed in the doc as future work.
- SDF fallback path in `body.rs` is **kept** (dev prototyping value; VQ-B1 bans it from shipped prefabs via content-lint, not code deletion).

## Risks
- **Mixamo is manual**: no API; user must download FBX files (Adobe login). Mitigated: shopping list delivered in Phase 0, character phase ordered after renderer phases, and I skip ahead if blocked.
- **FBX→glTF fidelity**: Blender CLI conversion of Mixamo rigs is well-trodden but clip merging/naming needs the pipeline's verify step (content-lint) to catch drift. Blender 5.2 is installed and has driven the pipeline since Phase A0.
- **wgpu 29 MSAA/pass coherence**: every pipeline in the pass must agree on `sample_count`; BC7 is a device feature fallback adapters lack → harness uses RGBA8 assets.
- **Texture memory growth**: realistic PBR sets are heavy — budgets in VQ-C5, resize step in the pipeline.
- **Headless CI variance**: analytic assertions with tolerances only; skip cleanly when no adapter.
- **Uncommitted tree**: Phase 0 step 1 fixes bisectability before surgery.

## Verification (end-to-end)
- `cargo test --workspace` headless after every phase (offscreen readback + content-lint + CPU unit tests); `cargo build` of both client binaries.
- User feel-checks in the sandbox at phase boundaries (I never launch the GUI). Expected big visual jumps: after Phase 2 (HDR+IBL sky), Phase 3 (shadows), Phase 5 (Mixamo player), Phase 6 (dressed zone).
