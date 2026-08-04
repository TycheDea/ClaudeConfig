# Repos to learn from — GitHub survey short-list (2026-07-22)

Follow-up to `tasks/openmmo-comparison.md`. All entries verified on GitHub; licenses
checked because they decide adopt-vs-study-only (strict-NC ruling applies).

## Tier 1 — highest value, clean licenses

### Asset pipeline (our biggest problem)
1. **Stable-X/Stable3DGen** — MIT, 1.3k★. Same lineage as our Hi3DGen, rebuilt
   specifically to strip nvdiffrast/kaolin/flexicube (the exact NVIDIA NC deps behind
   our TRELLIS eval-only ruling). Natural upgrade/diff target for our geometry stage.
2. **VAST-AI-Research/UniRig** — MIT (code + weights), 1.7k★, SIGGRAPH 2025.
   Learned auto-rigging: autoregressive skeleton-tree prediction + cross-attention
   skinning weights; generalizes beyond humanoids. The real Mixamo alternative for our
   rigging stage.
3. **OpenTexture/Paint3D** — Apache-2.0, 804★, CVPR 2024. Depth-aware ControlNet
   multiview texturing + UV-inpaint refine, outputs *delit* (lighting-free) textures.
   Closest published analog to our depth-conditioned multiview + bakeoff design.
4. **huxingyi/autoremesher** — MIT, 3.0k★, active. Production quad-remesh
   (Geogram/libigl). Candidate retopo step after Hi3DGen, before UV unwrap.
5. **jpcy/xatlas** — MIT, 2.5k★. Industry-standard UV unwrap/atlas packing (used by
   Blender/Unity/Filament). Candidate automated-UV step ahead of texture baking.
6. **MrForExample/ComfyUI-3D-Pack** — MIT, 3.8k★. Wraps ~15 image-to-3D backends in
   one ComfyUI graph; reference architecture for multi-model bakeoffs.
   Also: **Stable-X/ComfyUI-Hi3DGen** (MIT) — official ComfyUI wrapper for our own
   geometry model; worth diffing against our integration.

### MMO architecture
7. **levy-street/world-of-claudecraft** — code MIT, 1.9k★, very active. WoW-Classic-
   style browser MMO vibe-coded with Claude. One deterministic sim drives offline
   browser world, authoritative multiplayer server, AND a headless RL env behind an
   `IWorld` interface. Solves our identical asset problem the opposite way: **zero
   AI-generated 3D art** — procedural world + curated CC0 (KayKit/Quaternius/Kenney/
   Poly Haven) with disciplined CREDITS.md licensing. Standout candidate for a
   dedicated OpenMMO-style close read.
8. **cBournhonesque/lightyear** — MIT/Apache dual, 1.1k★. Best Rust netcode
   reference: client prediction + rollback, snapshot interpolation, rooms-based
   interest management. Bevy-flavored but concepts port to our stack.
   Second opinion on minimal replication machinery: **projectharmonia/bevy_replicon**
   (MIT/Apache, 631★).

## Tier 2 — study-only or narrower

- **ubisoft/ComfyUI-Chord** — **Research-Only Copyleft, NC-BANNED from shipping
  path.** CHORD: full PBR set (basecolor/normal/height/roughness/metal) decomposed
  from a single generated texture — exactly our missing PBR-maps problem. Study the
  architecture; reimplement clean or find a permissive equivalent.
- **daveredrum/Text2Tex** — **CC BY-NC-SA, NC-BANNED.** Textbook precedent for
  progressive multiview texture synthesis with next-best-view selection. Read the
  algorithm only.
- **Tencent-Hunyuan/Hunyuan3D-2.1** — **Tencent Community License: excludes EU/UK/
  Korea territory + MAU cap.** Physics-grounded material simulation in its texture
  stage is worth reading; not adoptable.
- **clockworklabs/SpacetimeDB** — **BSL 1.1** (→AGPL later), 24.8k★. Powers BitCraft;
  state-sync-on-subscription model worth understanding, license blocks reuse.
- **space-wizards/RobustToolbox** (Space Station 14) — GPL/MIT mix, C#. 7 years of
  live-service ECS + netcode + engine/content split at real player scale.
- **matrix-org/thirdroom** — Apache-2.0. glTF-canonical asset pipeline; threaded ECS
  via SharedArrayBuffers.
- **SeloSlav/2d-multiplayer-survival-mmorpg** — Apache-2.0 with IP carve-outs. Second
  solo-AI-assisted-MMO case study after OpenMMO (SpacetimeDB-based).
- **Pumpkin-MC/Pumpkin** (GPL-3) / **ferrumc-rs/ferrumc** (MIT) — from-scratch Rust
  Minecraft servers; chunk storage + protocol codec patterns (prefer FerrumC's MIT if
  borrowing shape, not just reading).
- **AmbientRun/Ambient** — MIT/Apache, **abandoned**. A funded team's attempt at
  exactly our engine category; read the architecture as a design-space map.
- **astra-vision/MaterialPalette** — code MIT but depends on OpenRAIL-M weights;
  texture-from-swatch fallback idea.

## Action plan — adopt/reject evaluations, in priority order (2026-07-22)

Goal of every action: end with an explicit **adopt / reject / defer** verdict recorded
here. Ordering principle: actions that can unblock stalled work rank first; within a
track, cheap desk-work gates expensive GPU runs. Standing ruling: ClaudeCraft-style
procedural generation WILL eventually be adopted, but scoped to **dungeons**, not the
global world — A6 evaluates *how*, not *whether*.

### A1. UniRig — rigging-stage evaluation  → **VERDICT: REJECT** (2026-07-22)
Desk read done (clone at `reference/UniRig`); GPU smoke skipped as unnecessary.
Ruling (2026-07-22): **Mixamo compatibility is NOT a gate** — no incumbent tool is a
must; a different toolchain with a better end-to-end outcome wins. Judged that way:
- **Decisive: superseded + immature release.** The README itself announces SkinTokens
  as the successor (claimed ~2× skinning accuracy); the released checkpoint is not
  the paper's headline one; no humanoid example ships; README recommends manual
  skeleton refinement before skinning (human-in-the-loop expected). No reason to
  invest in the older model when its own authors point elsewhere.
- Cost factor (not a gate): output is per-mesh bone topology with generic names
  (`bone_0`, …; the `mixamo` class token is untrained scaffolding), so adopting any
  UniRig-family tool means also solving animation *sourcing/retargeting* for
  non-standard skeletons — that full path must be priced into A1b's verdict.
- License note: code+weights MIT as advertised, but the vendored Michelangelo shape
  encoder is GPL-3.0 inside both models, and `bpy` (Blender, GPL) is load-bearing for
  all mesh I/O. GPL ≠ NC — an offline GPL tool doesn't encumber the assets it outputs,
  so this alone wouldn't have blocked it, but it's recorded for the file.
- Otherwise technically plausible (8 GB VRAM, seeded, auto-normalizing input) — the
  research direction stays interesting; SkinTokens audit promoted to A1b.

### A1b. SkinTokens — successor audit  → **DESK VERDICT: ADOPT-CANDIDATE** (2026-07-22)
UniRig's official successor (github.com/VAST-AI-Research/SkinTokens, clone at
`reference/SkinTokens`): skeleton + skinning unified in one autoregressive sequence.
Desk audit passed; hands-on validation pending go-ahead.
- **Licensing: clean.** Code MIT, weights MIT on HF (confirmed live, ~1.6 GB, and the
  recommended ckpt IS the paper's GRPO-refined headline model). No NC anywhere;
  copyleft recorded-but-acceptable: bpy (GPL, sole mesh I/O, runs as a separate
  subprocess server) + vendored GPL-3 Michelangelo encoder (same pattern as UniRig).
- **Skeleton story better than UniRig's**: real `mixamo.yaml`/`vroid.yaml` named-bone
  templates wired into a *trained* cls-token embedding — but the shipped demo
  hardcodes generic "articulation" conditioning. Whether `cls="mixamo"` is a live
  trained class is checkable with one ckpt-load smoke via the library API
  (`TokenRig.generate(cls="mixamo")`). If live: Mixamo-name output nearly free. If
  not: budget a one-time hierarchy-based (name-agnostic) retarget mapper. Either way
  boundable, not a blocker.
- **Costs/risks**: flash-attn is HARDCODED (main LLM + skin-VAE paths, no config
  escape) → from-source Windows build required, the main integration cost. No
  spconv/torch_scatter (good). ≥14 GB VRAM stated (beam search 10). Not natively
  seedable — no --seed flag; external torch.manual_seed wrap needed (trivial).
  `--use_transfer` maps rig back onto the original textured mesh (the production
  path). GLB-first export (FBX deprecated in bpy 4.2). Inference-only release; arXiv
  preprint (2026-02), not peer-reviewed; benchmarks self-reported.
- **Hands-on validation done (2026-07-22)**, env at `C:\tools\SkinTokens`
  (venv py3.11 + torch 2.7.0+cu128 + prebuilt flash-attn 2.8.3 wheel — no source
  build needed; scipy was missing from their requirements). Results on RTX 3080 Ti:
  - Runs fine on 12 GB: **3.7 GiB peak VRAM** (14 GB claim very conservative),
    42 s full rig, ~18 s skin-only, valid skinned GLB out.
  - `cls="mixamo"` is NOT in the trained vocabulary (`{rignet, vroid,
    articulation}` per checkpoint hyper_parameters) — Mixamo-named output
    unreachable. `cls="vroid"` conditions correctly (decoded back from the
    sequence) but the model emitted no body/hand part tokens on our mesh, so
    names fall back to generic `bone_0…` and topology is per-mesh (57 joints vs
    the 52-bone template). Full-generation mode ⇒ name-agnostic retargeting, always.
  - **The adoption shape is skin-only mode**: `--use_skeleton --use_transfer` took
    our rigged human.glb, kept our skeleton as input, predicted new skin weights,
    transferred onto the original textured mesh. Caveat: the skeleton round-trips
    through their tokenizer — 28 joints in → 22 out (leaf/end bones dropped),
    names re-emitted generic. Since WE supply the skeleton, names are recoverable
    with a deterministic nearest-joint rename against our canonical rig; the
    mapper must handle dropped non-deforming leaves.
- **Verdict: ADOPT as a learned auto-skinning stage** over our canonical
  Mixamo-standard skeleton (kills the manual Mixamo upload for skinning; skeleton
  and animation library stay ours). User feel-check passed (2026-07-22): skin-only
  output vs Mixamo auto-rig "very similar" quality, and the user *prefers* the
  round-tripped skeleton (ours minus the 6 non-deforming leaf/end bones).
  **Integration shipped (2026-07-22)**: `gen_character.py`'s rig stage is now
  `char_rig.py fit` → `char_skin.py` (SkinTokens venv, external seed) →
  `char_rig.py finish`; bone-heat deleted. The reference-check on the 6 dropped
  leaves cut the trim to 3: the socket bones (`handslot.r/l`, `head`) are
  runtime-referenced (weapons.rs/vfx.rs/content_lint guardrail) and are re-added
  post-skinning as before; only the Mixamo end bones are trimmed, weights folded
  into parents (the round-trip VARIABLY keeps and weights them — 22 vs 25 of 28
  joints observed across meshes). The rename mapper is hierarchy-descent with
  min-total-distance sibling assignment, not nearest-position — quantization
  error (~5 cm) exceeds neck/shoulder spacing and chain tips absorb their
  dropped leaf. Full findings: `tasks/ai-pipeline/a4.md` amendment.

### A2. Stable3DGen — geometry-stage diff vs Hi3DGen  → **VERDICT: ALREADY ON IT** (2026-07-22)
Desk-diff done (clone at `reference/Stable3DGen`): **the same repository** — GitHub
renamed Stable-X/Hi3DGen → Stable-X/Stable3DGen; our production checkout at
`C:\tools\Hi3DGen\Hi3DGen` is the identical commit (`c29f668`, byte-identical tree,
still the live main HEAD). The survey entry describing it as a separate rebuild was
wrong. Confirmed bonuses from the diff:
- Our checkout already carries the de-NC'ing (no nvdiffrast/kaolin/flexicubes
  anywhere; mesh extraction is scikit-image marching cubes) — we hold no hidden NC
  deps.
- All three weight repos are permissive (trellis-normal-v0-1 MIT, yoso-normal
  Apache-2.0, BiRefNet MIT); code MIT.
- No GPU A/B warranted — nothing distinct to compare. Follow-up only if
  Stable-X/Stable3DGen ever moves past `c29f668` ("[WIP] modular framework" per repo
  description): re-run the desk-diff against the new HEAD.

### A3. autoremesher + xatlas — retopo/UV gate  → **SPLIT VERDICT** (2026-07-22)
Prototyped on candelabra cand_4 `raw.glb` (335k tris) + `clean.glb` (14.5k tris);
artifacts in scratchpad a3/.
- **autoremesher: REJECT for unattended pipeline use.** Has a real headless CLI
  (contrary to expectation), but: non-deterministic (identical command → 1 crash +
  3 different outputs in 4 runs; geogram quad_cover assertion at ~25%), target-quads
  undershot 2–3× every run, 8–21% non-quad residue, and at bbox-preserving settings
  it shattered 11 components into 227 (vs clean.glb's 9). Not gate material as-is.
- **xatlas: ADOPTED, shipped (2026-07-22).** `prop_cleanup.py` unwraps the decimated
  mesh (single 1024-target atlas, padding 4 px, `uv_charts`/`uv_utilization` in the
  stats line); `prop_texture.py` consumes the incoming layer and hard-fails on a
  UV-less mesh (smart_project deleted) — so the atlas is stable across texture
  re-runs, which the deferred Paint3D UV-inpaint bundle needs. Wheels live in
  Blender's per-user modules dir (Blender ignores the Python user site; install
  line in `scripts/ai-pipeline/README.md`). Verified on candelabra cand_4:
  utilization 0.778, geometry stats identical, blend_coverage 0.584 vs 0.609.

### A4. Paint3D — texture-stage technique extraction  → **PER-TECHNIQUE VERDICT** (2026-07-22)
Desk read done (clone at `reference/Paint3D`, Apache-2.0 confirmed). No wholesale swap;
per-technique adopt list vs our `prop_texture.py` + bakeoff:
- **ADOPT — all three shipped (2026-07-22)** in `prop_texture.py`:
  - *Multi-view single-canvas generation* — opposite views tiled side by side into
    one 2048×1024 conditioning canvas per sampling pass (`view_pairs` +
    `generate_views` rework; decoded canvas split back into per-view crops, blend
    machinery untouched; MR-mask pass inherits it via the shared path).
  - *Depth-outline dilation* — 5 px grow on the conditioning PNG only
    (`MV_DEPTH_DILATE_PX`); the float EXR keeps the true silhouette for occlusion
    and the pad mask. `pad_edges` KEPT alongside it (user ruling 2026-07-22:
    prevention + repair compose; deletion would bet on model compliance).
  - *Telea atlas hole-fill* — `cv2.inpaint` over island texels no view covered
    (`hole_texels` in stats; ~40% of island texels on the candelabra — these were
    flat mean grey before); off-island gutter keeps the mean fill.
- **DEFER (both hinge on an inpaint-capable model; bundle, revisit after A3 xatlas
  lands):**
  - *UV-space inpaint refinement* — the one genuinely missing stage. Their trick: a
    per-texel world-position map lets a 2D inpaint model respect 3D adjacency across
    UV-island seams; we already bake that exact position+normal atlas
    (`bake_geometry_atlas`) but only use it for reprojection. Prototype plain
    inpaint-in-UV first; their trained UV-pos ControlNet is SD1.5-only (would mean a
    ~10 GB second model family in ComfyUI) — only if seams stay bad.
  - *Progressive inpaint view scheduling* — later views inpaint against renders of
    the already-textured mesh instead of generating blind; Z-Image Turbo inpainting
    in ComfyUI unproven.
- **SKIP:** standalone "delit" — it's prompt phrasing + their trained UV model, not a
  post-process; we already do the reachable prompt half and *measure* baked lighting.
- Licenses all pass strict-NC: their UV-pos ControlNet Apache-2.0, SD1.5 +
  lllyasviel ControlNets OpenRAIL-M (use-restricted, not NC). One trap: their UVHD
  base model (`realisticVisionV13` HF re-upload) has dubious provenance — never use.

### A5. CHORD + Text2Tex — PBR-maps design study  → **VERDICT: ADOPT-PERMISSIVE-ALTERNATIVE** (2026-07-22)
Design note written: `tasks/pbr-maps-design-note.md` (clones at `reference/ComfyUI-Chord`,
`reference/Text2Tex` — both NC, read-only). Key outcomes:
- Ground truth corrected: our stage is not strictly albedo-only — it already bakes a
  real high→low normal map and scalar/two-tone MR. The true gaps: lighting baked into
  the multiview basecolor, no per-texel roughness, binary metallic — exactly what
  single-image PBR decomposition fixes.
- **MaterialAnything adoption — SHIPPED (2026-07-22)** (`8feb605` + `2dfb79d`):
  estimator (MIT code, Apache-2.0 weights, pinned `be3d6b3`, own venv at
  `C:\tools\MaterialAnything`) decomposes each multiview `gen.png` into delit
  albedo + per-texel rough/metal (`prop_pbr.py`), conditioned on a camera-space
  normal render; both channel sets blend through the unchanged facing-weight
  machinery. `--mr-mask` pass and its flags DELETED. Candelabra verify: delit
  albedo confirmed visually, metal_fraction 0.269, resume run 18 s with no GPU
  respend, geometry stats exactly reproducible across fresh dirs (generated
  pixels are not — GPU kernel nondeterminism, provenance shas are per-run).
  Clean-room CHORD rebuild rejected (weeks + training budget for what a
  permissive model already does); accept-albedo-only rejected (fix was cheap).
- **OpenRAIL-M ruled NOT a gate**: commercial use permitted, restrictions purely
  behavioral — resolves the MaterialPalette flag (consistent with the A4 finding on
  SD1.5/ControlNet weights).
- Text2Tex's sequential inpaint core is a poor trade for us; the clean-room
  coverage-driven extra-view pick — **SHIPPED (2026-07-22)** in `prop_texture.py`:
  coverage is purely geometric, so up to 2 extra views are greedily picked from an
  az/el candidate grid BEFORE generation (deterministic, resume-safe; MR pass
  inherits the picks). Elevations (-35, 15, 55) + 75 top — measured on the
  candelabra, DOWN-facing texels dominate the holes (45%), so the below view
  gains ~2x the best above view; coverage 0.584 → 0.653 with one -35 pick.
- CHORD architecture understood (single-step SD2.1 translator, rendering-equation-
  ordered channel prediction with analytic intermediates); nothing to lift, NC stands.

### A6. world-of-claudecraft — clone + deep-dive  → **VERDICT: PATTERNS EXTRACTED** (2026-07-22)
Comparison doc written: `tasks/claudecraft-comparison.md` (clone at
`reference/world-of-claudecraft`, MIT, HEAD 8950e61). Eight adopt patterns recorded
there for the eventual dungeon-gen design; the load-bearing ones:
- **Composition, never geometry synthesis**: a dungeon run is a seeded shuffle of
  *authored* room modules + fixed finale (~15 lines of picker); the real cost is
  authoring modules. Strong evidence for curation-first dungeon gen.
- **One layout struct feeds both collision and render** — kills renderer/collider
  hand-mirroring; the central design decision to copy.
- **One dungeon seed, purpose-keyed sub-streams** (their delve code migrated to this
  after a shared-RNG stream made draw order load-bearing — validates our existing
  stateless-hash idiom). Teleport-stitched modules with per-module confinement delete
  corridor-routing entirely (per-instance hecs World for us). Semantic dressing
  anchors (`{kind,x,z}` → renderer maps kind→asset) pair with our prop pipeline.
  Affix pool + seeded golden layout-hash tests round it out.
- **CREDITS.md as operative license record — SHIPPED (2026-07-22)**: `content/source/
  CREDITS.md` restructured (default-closed preamble, Redistribution enum, recolumned
  asset table, ledger kept as the input-side record). Deviations: no fork section
  (no root LICENSE to explain) and manifest-path provenance, not content hashes.
- Two corrections to the survey entry: their "vibe-coded" reputation is wrong
  (1,244 test files, mechanically-enforced invariants); and `IWorld` is the
  *presentation* seam, not the host seam — server and RL env drive `Sim` directly,
  so our shared `vordar-game` crate already has the equivalent property and should
  NOT grow an IWorld double-implementation. No real worldgen to study (towns
  hand-placed) — OpenMMO and this repo are complementary, not overlapping.

### A7. lightyear + bevy_replicon — parked skim  [defer]
Netcode is not a current pain point. Revisit when replication/interest-management
work resumes; no action now.

### No action (decided): Hunyuan3D-2.1 (territory-excluding license), SpacetimeDB
(BSL), thirdroom, SS14/RobustToolbox, Pumpkin/FerrumC, Ambient, Broth & Bullets —
already-read survey notes above are the full takeaway; ComfyUI-3D-Pack only becomes
relevant if the bakeoff ever expands to multiple geometry backends.
