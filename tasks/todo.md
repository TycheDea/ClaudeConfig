# Start-Town Campaign (2026-07-30 →) — ACTIVE

Plan: `~/.claude/plans/zippy-wibbling-pancake.md` (approved 2026-07-30). Real start
zone: themed Castilian town ("Rocalba") + one enterable landmark (chapel, broken
vault), de-orange the dusk lighting (4 candidate looks, Opus picks), lighting becomes
zone-authorable. **Process change, user ruling 2026-07-30: user feel-checks STOPPED —
Opus is the visual gate** (supersedes every open "owed feel-check" item below,
including B4's gate final box and the occupancy-sheet visual call). Plan approval =
§8 go-ahead for exactly the runs in its GPU table (~8 h total, +1 h contingency).

Ratified decisions: D1 hybrid buildings (Blender-procedural shells + gen_material
tiling sets; Hi3DGen only for ≤5.5 m heroes) · D2 broken-vault chapel · D3 look
chosen by Opus at G1 · D4 Qwen texture A/B decides · D5 visuals-as-props + mirrored
collision prefabs + lint cross-check · D6 east keeps dressing, relight only ·
D7 one glb per building type.

Constraints in force: GPU runs serialized (one 12 GiB card; ComfyUI never up during
geometry); headless verification only (no GUI runs — P-C probe via offscreen renders,
not sandbox walking); foreground shells only; one workspace suite per phase gate.

## Phase 0 — Premise + probes (~40 min GPU)

- [x] P0.1 `docs/town-premise.md` (spec in plan §Phase 0.1 — Rocalba, vespers
      premise, closed material vocabulary, layout inside r≈55) — 7 sections;
      chapel precinct ~(-30,-30) absorbing the ruin cluster; gate arch ~(15,0)
- [x] P0.2 RUN-P1: measured **6.07 mm/texel** vs 6.4 arch reference (~5% gain
      for 27% smaller size — size² scaling absent); chain produced a whole
      hip-roofed building when asked for a wall slab (75.9 m² world area).
      Artifacts: target/prop-batch/town-probe-wall/cand_0/. Opus verdict:
      **FAIL, not borderline** — invented carved-swirl detail on flat
      whitewash, no per-face albedo identity (white from 2/8 angles), hard
      edges lost to decimation (boundary edges 20→704), chain silently
      substituted a whole hip-roofed shed for the requested slab; atlas spent
      on roof the camera never sees → effective wall density worse than 6.07.
      **D1 CONFIRMED** (hybrid path; Hi3DGen heroes ≤5.5 m only)
- [x] P0.3 RUN-P2: **D4 = Qwen-Image wins on metric.** Object-masked, same
      instrument both arms: concept R−B 16.1 / a* 1.51; A (Z-Image-Turbo)
      31.8 / 2.81 atlas; B (Qwen) 22.9 / **1.45** atlas — perceptual warm cast
      eliminated, R−B residual +6.8. Artifacts: arch-rebuild/cand_0_qwen/.
      COST: Qwen texture pass ~15.3 min vs turbo ~4 (no lightning LoRA staged;
      base model 20 steps, CPU-offload on 12 GiB) → Phase 3's 30-candidate
      hero budget (~5.5 h) becomes ~10 h. USER RULED (2026-07-30): try the
      Qwen lightning LoRA first — license-check, download, ONE ~15-min A/B
      re-verify at 8 steps; if color degrades, fall back to funding the
      overrun question again. Do this as Phase 3 prep, not now.
      Keep: generate.py env-var hooks + prop_multiview_qwen.json (Phase 3
      needs the swap mechanism; A-arm defaults byte-identical).
- [x] P0.4 Graybox chapter03: new `game/chapter-03` crate + 7 prefabs (5 chapel
      pieces + 2 casas), `chapter: Some("chapter03")` on start; replication test
      + content_lint green. Chapel interior x∈[−30,−14] z∈[−16.5,−9.5], vault
      y=11, door east face gap z∈[−14.2,−11.8] open→y3.2; roof west half only.
      NOTE: chapel pulled to door-front x=−13.2 to stay inside AOI_RADIUS 40
      from spawn ring — premise doc says precinct ~(−30,−30); reconcile at
      Phase 2 layout (AOI is a layout constraint the plan didn't list).
- [x] P0.5 Probe P-C: frames+data in target/town-probe/. (1) Containment: default
      zoom 34 m NEVER contained — camera views interior from above through the
      broken vault; zoom ≤5 m contained at nave center; min-zoom 4 m still clips
      near door. Broken vault = camera window, not containment. (2) IBL leak is
      renderer-level: ambient = unoccluded env lookup (pbr_common.wgsl:97) —
      roof ablation bit-identical; covered≈open (lum 0.309 vs 0.336). The
      plan's interior-volume ambient/fog fallback is FORCED → Phase 4.
      (3) Candle PointLight at portal.ron values reads clearly (+32% G pool).
      → D2: broken vault confirmed as viewing mechanism + fallback feature
      scheduled; no camera engine work v1 (zoom-in gives true interior).
- [x] P0.6 Probe P-D: wide shot useless for building-scale content (framing tuned
      for <2 m props — extreme close crop on wall corners); no shot type sees
      inside chapel. → G4 needs an interior preset; wide framing fix needed for
      G2 too. Fold both into Phase 1's zone_review pass. Permanent wiring added:
      client chapter_geometry.rs + zone_review draws chapter prims. One-off
      chapel_probe.rs bin kept until Phase 4 interior re-verify, then delete.
- [x] Phase 0 gate (2026-07-30): D1/D2/D4 recorded above with evidence;
      content_lint 15/15 + zones 6/6 green on the combined tree; committed
      `c6cf379` (premise+graybox+offscreen wiring) + `e0bc9b7` (Qwen swap
      hooks). Open user decision carried into Phase 1: Phase 3 texture-speed
      question (see P0.3). Phase 1 additions from probes: zone_review interior
      preset + building-scale wide framing (P-D); interior-volume ambient/fog
      feature scheduled for Phase 4 (P-C).

## Phase 1 — Lighting redesign (~25 min GPU) — IN PROGRESS 2026-07-30

User ruling 2026-07-30 (before leaving for a few hours): do NOT stop at compact
points — continue autonomously; if all planned work ends, orchestrator plans and
executes the next move.

- [x] P1.1 Plumbing DONE (`5933c31`): 6 optional ZoneVisuals fields; defaults
      keep the old literals verbatim (DEFAULT_SUN_DIR moved not recomputed —
      trig would perturb low bits); 1.5× folded into default sun_color
      (1.5,1.38,1.2); resolve_sun_dir/resolve_sun_color in zones.rs;
      set_exposure wired at zone apply. Byte-identity PROVEN: all mid/close
      frames byte-identical before/after; only wide (reframed) + new interior
      frames differ. turntable.rs had no sun constants to retire (generic
      engine-renderer bin, can't see vordar crates) — chapel_probe.rs was the
      real third duplicator, fixed.
- [x] P1.2 zone_review DONE (same commit): --visuals-override (partial
      LightingOverride RON — layers onto lighting fields only, zone keeps
      ground/props), bounding-sphere wide framing, interior_apse +
      interior_door shots (1600×900, non-black). Override smoke: mid mean
      RGB (205,153,117)→(202,174,169) under a cool test override.
      Override extension DONE (`13740f0`): fog_color + env_hdr (reuses
      ZoneVisuals.env; image::open takes target/ paths directly). Worker
      caught an azimuth-convention mismatch: hdr_post manifests use image-
      column azimuth, engine uses world-vector (world = image + 180°);
      verified bit-exact against DEFAULT_SUN_DIR (83.1° reproduces it) —
      RONs use 83.1 not 263.1. hdr_post --sun-tint folded into this commit.
- [x] P1.4 renders: baseline + L1-L4 under target/lighting-looks/review/
      (identical framing; wide mean RGB — baseline (245,218,172) vs
      L1 (137,126,181) / L2 (159,166,180) / L3 (140,142,150) /
      L4 (158,163,182)). override_L{1..4}.ron carry full-precision constants.
- [x] P1.5 Opus G1 VERDICT: **WINNER L3 overcast** (scores 8/9/9/7/8 on
      theme/true-color/A4-headroom/depth/mood) — neutral limestone read,
      zero-chroma field = max candle-gold canvas, dread w/o crush; RUNNER-UP
      L2 late_afternoon (4/9/4/8/3 — best material truth + shadows, off-theme,
      would swallow candles; two-frame re-check owed at G4). L1 rejected
      (magenta cast replacing amber — same failure class), L4 rejected
      (defective: blown ground + black-crush + interior/exterior exposure
      inconsistency). All but L4 clearly beat baseline. Shared defects
      carried: interior horizon seam (clause-9 class), wide-shot fog density
      too high at altitude in ALL looks → Phase 4 watch items.
- [x] P1.6 SHIPPED (`9f7958e`): castilian_plateau_overcast_2k.hdr installed,
      dusk hdr DELETED (git rm; zero file deps remained); start+east author
      full G1 visuals identically (D6); VQ-A5 rewritten (+ stale appendix
      "Theme read" item fixed); G1 record at
      docs/reviews/town/g1-lighting-2026-07-30.md; rework-1 evidence note
      corrected; warm-band test lighting_look.rs (R/B ∈ [0.65,1.05], R−B<0.05;
      falsified red at R/B 1.9378 on restored amber look); golden_helmet_ibl
      rebaked (only golden that moved, sanity non-black). Worker judgment
      accepted: asset_inspect Lighting::Dusk → Lighting::Ship (reads actual
      start-zone visuals dynamically so the review tool cannot drift).
      chapel_probe.rs left on amber constants (throwaway, dies Phase 4).
- [x] P1.3 RUN-L1..L4: ALL FOUR looks green (~13 min GPU); constants +
      previews under target/lighting-looks/, table in looks_summary.json.
      Shipped-HDRI reference measured: horizon band 13.6×/9.0×/4.0× brighter
      than upper sky per R/G/B — confirms horizon sampling as the amber-fog
      root cause. L2 late_afternoon failed hdr_post seam gate twice (seed 7
      0.0401, seed 13 0.0264 vs 0.02; L**6 top-end amplifies 8-bit seams on
      near-white sky) then passed at seed 8 + softer-haze prompt (0.0107);
      gate untouched. Worker added --sun-tint arg to hdr_post.py (default =
      old constant, shipped behavior unchanged) — needed for per-look sun
      colors; uncommitted, fold into the Phase 1 commit.
- [x] Phase 1 gate (2026-07-30): workspace suite ONCE — 425/425 green
      (+1 = lighting_look); content_lint 15/15; commits `5933c31` `13740f0`
      `9f7958e`. Decided while unsure (logged, zero live effect): zones.rs
      numeric ZoneVisuals defaults being aligned to the overcast constants
      post-gate — fallback env is overcast but numeric defaults still
      reproduced the deleted dusk look; dead transition weight, both live
      zones author explicitly.

## Phase 2 — Materials, kit, layout (~1.5 h GPU) — IN PROGRESS 2026-07-30

- [x] P2.0 post-gate cleanup DONE (`9ea6333`): zones.rs numeric defaults =
      overcast constants; DEFAULT_SUN_DIR literal deleted for
      DEFAULT_SUN_AZIMUTH/ELEVATION_DEG through sun_dir_from_angles (one
      source of angle math). No test asserted dusk numbers; vordar-game
      63+15 green; lighting_look green (defaults inert — both zones author
      explicitly). camera.rs LightUniform::default_sun untouched (unrelated
      engine fallback, fog_density 0).
- [x] P2.1 RUN-M1..M6 DONE (~70 min GPU, 16/16 pass, 3 first-retry gate
      fails resolved): target/town-materials/{m1..m6}/cand_N/ +
      materials_summary.json. Stone/whitewash all |a*| < 1.3 — no warm
      drift. M6 wrought-iron cand_2 flagged (a* 10.19, rust-brown dominant
      vs §3 "never bright orange") — needs visual check at selection.
      Notes: gen_material.py emits diff/nor_gl/rough ONLY (no AO path —
      kit loader matches); CLIP 77-token limit forced citation prefixes out
      of model-facing prompts (citations tracked in report only).
- [x] P2.2 build_town_kit.py: v1 committed (script + townkit/ package;
      Blender 5.2 headless; all 9 types export, dimension asserts green,
      vordar_detail extra round-trip proven, UV scale 13.107 m/2048² tile =
      6.4 mm/texel matching VQ-A3). Orchestrator preview screen found 8
      geometry defects; FIX ROUND DONE (`25e7c5b`): gables closed, eave
      overhang, casa_corner true valley join, chapel apse + 0.6 m exposed
      wall tops, gate_arch rebuilt — root cause was NOT flipped normals but
      0.2494 m joint gaps between box-approximated voussoirs rendering
      black; rebuilt as true radial wedges; verify.py _wedge_joint_gaps
      proven red on old math + scoped radial-normal check (0 faults) —
      well shaft opened. Re-screen: gables/eaves/arch/apse good.
      ACCEPTED RISK (logged): roof slopes remain flat planes + ridge row;
      barrel-tile course structure to come from photoscan normal relief;
      G2 arbitrates — if cohesion fails on roofs, add scalloped eave strip
      + geometric rows. Minor watch for G2/G4 frames: chapel rim corner
      specks + vault-wall junction seam, gate arch intrados hairline. NOTE for P2.4: premise §6 says
      chapel doors WEST but graybox+kit build them EAST — pre-existing doc
      inconsistency, reconcile at layout. Kit has no "worn cobble" slot —
      cobble is ground/streets, not building material.
- [x] P2.3 Material selection + Opus G2 kit pilot: swatch renders DONE
      (render_material extended `aa6f9d2` — now reads start-zone authored
      lighting incl. exposure 0.576 instead of stale generic defaults, +
      --distance flag; 32 frames + 6 family sheets under
      target/town-materials/review/, no black/clipped frames; ~0.7-0.8×
      darkening = expected ACES+exposure, verified not a wiring bug).
      Opus selection VERDICT: **ALL SIX FAMILIES FAIL — no candidate ships.**
      Systemic causes verified from assets: (1) gen_material.py native res is
      512² upscaled to 2048 (manifests: native_generation_size 512, upscale
      hops 1024/2048) — all 1 m detail is mush; (2) structured families came
      back unstructured — square slabs for barrel tile, boulders/crackle for
      ashlar, black MARBLE (§3-excluded) for oak planks, smooth copper/nickel
      dowels for forged iron; (3) m6 cand_2 orange sits in §2's reserved
      threat band 350°-25° — hard color-law violation; (4) 15/16 prompts
      dropped the §7.1 premise citation. tiling_check passed everything —
      tiles wrap, they just depict the wrong materials.
      **DECIDED WHILE UNSURE (wall → re-derive, plan D1 partially amended):
      town material source swaps from gen_material.py to CC0 photoscan
      tiles** (ambientCG/PolyHaven) — the proven path (Rock060 detail tile,
      user-ratified CC0 ruling 2026-07-25); real photoscans carry the
      oriented structure diffusion failed to produce; licensing (CC0) is the
      only gate and passes; selection instrument unchanged (in-engine
      swatches under ship light + Opus). RUN-M1..M6's 70 min stands as an
      honest falsification probe. OPEN for user checkpoint: gen_material.py
      fate (falsified for structured families; possibly still fit for
      unstructured ground?); m5 note: soot-as-height-gradient cannot live in
      a tiling texture — v1 ships uniform smoked tone, gradient belongs to
      Phase 4 interior treatment if at all.
      ROUND 2 sourcing DONE: 18 CC0 photoscans from ambientCG (2K-PNG), 3
      spec-matching candidates per family at
      target/town-materials-cc0/<family>/cand_N/, sources.json +
      sanity_stats.json + swatch sheets under review/ (ship lighting, 1 m +
      4 m). Two 2048×1024 sources tiled 2× to square (proportions preserved,
      noted in sources.json). Flags: m6 Metal046A luminance 92.3 +
      Metal046A/B near-flat normals; m2 Bricks089 is "Bricks"-category but
      claimed coursed ashlar — judge decides from pixels.
      ROUND 2 VERDICT (Opus, on-disk naming cand_1..3): 4 WINNERS —
      m1 cand_2 Plaster003 (8/9/8/8; watch: diagonal band + plaque patch
      upper-left 1 m tile will repeat on long facades), m4 cand_1
      WoodSiding003 (7/7/9/8; sat ≈0.38 just over the ≤0.35 ambient
      ceiling, hue 27° permitted), m5 cand_2 Concrete035 (7/8/7/8; floor-
      scan substrate, busy at 1 m), m6 cand_3 Metal046B (8/9/6/8; near-flat
      normal — patina-carried, tolerable on rejas). Runner-ups: Plaster001,
      Planks023A, Concrete036, Metal027 (Metal027 collapses black under the
      key, 4 m featureless). m6 threat-band: whole family clean.
      2 FAMILIES REJECT ALL — m2 (all three were ground/paving scans:
      lichen cobbles / literal fired brick / machine-chamfered precast; none
      vertical wall ashlar) and m3 (all flat northern-format tiles, zero
      barrel geometry; PLUS rendered sat 0.57-0.65 vs premise §2 ceiling
      S≤0.35 for terracotta). COHESION notes for G2: m4 (44) vs m6 (40)
      only 5 levels apart at 4 m — doors and rejas risk merging at street
      distance; with m2 out nothing occupies the 100-160 mid band; the two
      rejected families carry the silhouette (all roofs + all dressed-stone
      landmarks), so no palette verdict until they fill.
      ROUND 2b re-sourcing DONE: m2 cand_4-6 = Poly Haven wall-category
      coursed ashlar (stone_tile_wall Lab 67.9/1.0/3.1;
      white_sandstone_blocks_02 67.8/2.2/12.5; sandstone_blocks_05
      64.9/3.5/14.9 — warmth left for the judge), m3 cand_4-6 = genuine
      barrel teja (ceramic_roof_01, roof_3, clay_roof_tiles_02), albedo
      sat graded 0.43/0.51/0.70 → 0.298 (uniform HSV S-scale, raws kept as
      diff_2048_raw.png, grades in sources.json). ambientCG's whole
      RoofingTiles line confirmed flat-format — none qualify. Worker bug
      fixed en route: PIL convert("L") flattens 16-bit roughness to 255;
      3 candidates re-converted with explicit uint16 scaling + re-rendered.
      Round-2 sheets: review/{m2-dressed-limestone,m3-terracotta-tile}
      _sheet_round2.png.
      ROUND 2b VERDICT: **PALETTE COMPLETE — six winners.** m2 = cand_6
      sandstone_blocks_05 (8/7/9/8; only truly dressed candidate, strongest
      normal relief of the whole set; rendered 4 m S 0.217 hue 30° = legal
      warm-stone band; demerits: travertine-porous left-edge block will
      repeat on quoin runs). m3 = cand_6 clay_roof_tiles_02 (9/5/9/7; only
      genuine teja; rendered S sits AT ceiling at 4 m (0.309, 21% px over)
      and OVER at 1 m (0.345, 47% over) — the 0.298 grade record measured
      the albedo map, not the render; hue 16-18° in the reserved window but
      at less than half the threat saturation floor). cand_4s disqualified
      (blue porcelain slab grid / mossy northern flat tile).
      COHESION: **COHERES WITH RISKS.** Ladder 165/124/95/88/44/40 — the
      100-160 gap is CLOSED by m2 at 124. Named risks for G2: (1) m4/m6
      44-vs-40 merge persists — separation rests on warm/cool hue +
      silhouette only; (2) m2/m3 hue proximity 30° vs 16° — value alone
      separates chapel stone from roof; (3) m3 saturation at/over ceiling
      as rendered; (4) premise §2's V≤0.6 ceiling broken by m1 on 89% px,
      m2 on 32% — the clause as written outlaws the whitewash the premise
      itself mandates. DECIDED WHILE UNSURE (doc contradiction, for user
      checkpoint): treat §2's ambient S/V ceilings as binding CHROMATIC
      surfaces (threat-telegraph prevention), not near-achromatic whitewash
      — premise text amendment deferred until the user rules; judges told
      the observed values meanwhile. Also flagged: m5 reads mineral-stained
      stone rather than smoked m1 — weakest set member, G2/G4 watch.
      PILOT DONE: casa_corner rebuilt with the six winners (chosen for its
      roof valley junction — the one real roof-to-roof seam in the kit;
      all casa types bind the same 5 slots, plaster_smoked is chapel-only).
      Winners-only dir at target/town-kit-materials/ (flat family layout
      REQUIRED: _resolve_family_dir falls back to highest cand_* — pointing
      at town-materials-cc0/ would silently swap 3 of 6 winners). verify.py
      green, 5317 tris. Evidence: 336-frame inspect matrix (4 lightings ×
      7 ch × 3 dist × 4 angles) + 20 street frames (casa beside the
      chapel-ruin cluster; mid_00/wide/close_town-kit), zones.ron temp
      entry reverted, tree clean. Under target/town-kit/g2-pilot/.
      INFRA FOUND: background shells killed at ~68 min (twice, same spot)
      → split per lighting group; memory updated. ~~KIT DEBT (flag, don't
      fix now): build_town_kit.py overwrites build_report.json wholesale
      on partial --types runs (worker backed up + merged by hand).~~ FIXED
      2026-08-02: partial runs now merge by type over the existing report and
      re-emit it in ALL_TYPES order. The live evidence for the bug was still
      on disk — `target/town-kit/build_report.json` holds exactly one entry,
      `chapel`, a nine-type kit reported as one. That file is stale until the
      next build; nothing reads it but a human.
      G2 VERDICT: **FAIL** (Q1 3/10, Q2 2/10, Q3 5/10, Q4 2/10) — but the
      roof accepted-risk is VINDICATED, not refuted: relief reads as 3D
      barrel courses where mapped right (ridge strips, raking_beauty);
      the MAPPING is broken. Failing evidence: (1) roof slope UVs — front
      slope rotated 90°, rear slopes ~4× too fine, ≥3 tile scales on one
      asset (46.0 vs 16.4 px same plane/depth), valley junction = hard
      scale+orientation cut with black gaps; (2) wing long face has NO
      WALL — open void + orphaned quoin ladder, verify.py green misses it;
      (3) quoins read as excluded brick — warm tan hue 33°, identical
      30 cm courses, one-block repeat corr 0.308; (4) eave sawtooth fringe
      + stray debris specks. DISCHARGED with numbers: R3 terracotta can't
      telegraph (S 0.28/V 0.38 vs threat gate S≥0.7/V≥0.8); R4 whitewash
      never clips (0 px > V 0.90, p95 0.753) — user's "blinding" report
      does not reproduce under L3 in-zone (likely furnace rig frames).
      R1 oak/iron CONFIRMED WORSE (Δlum 0.010 at the reja — silhouette
      only separates); untestable at street in this frame set. Judge also
      ruled the street framing inadequate evidence (casa corner-cropped).
      WATCH (fail doesn't rest on them): D9 encalado macro mip-blur
      (detail-layer candidate), D10 ghost blocks under whitewash, encalado
      repeat untested at party-wall length, in-zone encalado V 0.597 = at
      §2 ceiling exactly.
      PRIORITY FOR NEXT SESSION (user ruling 2026-07-31, verbatim intent):
      the SSAO bias fix `8e00aa3` only improved the in-game look ~10% —
      "ssao shadows look really bad idk if its the technology or what it
      is but we should solve it asap. but not today." → First item
      tomorrow: root-cause SSAO quality pass. Known weak point from the
      investigation: ssao.wgsl reconstructs normals via dpdx/dpdy (noisy
      on flat walls) and the investigator's multi-tap reconstruction
      attempt traded one artifact for banding. Scope per the
      quality-over-cost ruling includes replacing the technique (proper
      per-pixel normals into the AO pass, or a better AO algorithm
      entirely — GTAO/HBAO-class); licensing is the only gate. Judge =
      Opus over offscreen A/B frames incl. the user's screenshot framings
      (C:\Users\egm_8\Desktop\tmp). Then the held Opus G2 re-gate.
      SESSION CUT (user, 2026-07-31 00:30): fix worker STOPPED mid-
      evidence, render killed, zones.ron temp edit reverted (tree clean),
      kit fix round COMMITTED `241f23a` (F1-F5 + verify open-face check;
      casa_corner.glb already rebuilt with fixes + graded ashlar, verify
      green). Evidence state at target/town-kit/g2-regate/: ship group
      COMPLETE through ship_clay (7 channels); raking group NOT rendered;
      3-casa street set NOT rendered; manifest NOT written. RESUME:
      rebuild nothing — render raking group, then street set (3-casa
      party-wall row via temp zones.ron edit, frames must show roof/eave/
      opening and door+reja per the judge's named gaps, revert after),
      write manifest, then Opus re-gate. Do the SSAO pass FIRST, then
      re-render the ship group with the post-SSAO binary so the judge
      sees one consistent binary (current ship frames are pre-fix).
      USER BUG REPORT (in-game, fixed `8e00aa3`): "dirt filter" on
      building walls = SSAO self-occlusion acne — dpdx/dpdy normal
      reconstruction noise on large flat near/grazing walls vs a 0.02 m
      bias; raised SSAO_BIAS to 0.2 (ssao.rs:29). Proven by SSAO on/off
      A/B + raw-normal visualization; shadows and textures exonerated
      (walls were graybox). 122/122 renderer tests green, goldens
      untouched. Evidence: target/dirt-investigation/ + user screenshots
      C:\Users\egm_8\Desktop\tmp. Residual: faint trace at an
      unreachable-in-gameplay near-90° grazing minimum-zoom framing only.
      NOTE for the re-gate judge: the g2-regate frames render with the
      PRE-FIX binary — faint flat-wall speckle in those frames is this
      fixed artifact, not a material defect.
      SSAO PASS DONE (2026-07-31): root-cause note
      tasks/ssao-quality-2026-07-31.md (RC1-RC6; hemisphere SSAO class-
      limited). DECIDED (clearly best, quality-over-cost): Option A — XeGTAO
      port via Bevy WGSL reference (MIT/Apache), hemisphere path deleted
      wholesale. Landed `60ddbbe`: first compute passes (prefilter_depth
      5-mip R32Float chain / gtao 3×3 slices 0.73 m / edge-aware denoise),
      full-res AO, depth-derived normals (stage 1), set_ssao kept; 123
      crate tests green; golden_sdf_composite rebaked (only SSAO-on golden;
      SSAO-off goldens untouched). Opus verdict: **PASS ship as-is**
      (acne 9/10 — 43-50× blotch reduction vs user frames, at/below AO-off
      floor; contact 9/10 — 2× deeper corner occlusion, ±60 px falloff vs
      old ±300; no banding/halos/bleed; strictly better on all shared
      framings). Evidence: target/ssao-gtao/ (7 framings × on/off/ao).
      PROBES CLOSED (Opus, 2026-07-31): D3 curvature CLEAN — crucero +
      broken_column _ao buffers show groove-exact occlusion, correct
      convex polarity (on/off ratio maxes at exactly 1.000, zero pixels
      brightened), no faceting/false creases → NO normal prepass, stage 2
      dead. D1 crawl ACCEPTABLE — diff energy entirely silhouette/
      disocclusion edges; interior noise spatially uncorrelated (does not
      survive r=6 blur, converged at r=12) → no temporal accumulation.
      PASS FINAL, binary stable. Watch (non-blocking): D2 ~5.8 px
      periodic structure; grazing far-floor noise = first suspect if
      in-motion crawl is ever reported. Probe artifacts:
      target/ssao-gtao/probes/.
      RE-GATE EVIDENCE round 1 (2026-07-31): full set rendered
      (ship+raking 7ch×12 + street row/door/window sets, manifest at
      target/town-kit/g2-regate/manifest.json) but INSTRUMENT DEFECT
      found: OffscreenRenderer defaults ssao_enabled=false and
      asset_inspect/zone_review never enable it → AO invisible in ALL
      review evidence ever produced by those bins (re-rendered ship
      frames pixel-identical to pre-fix). Fix + full AO-on re-render in
      flight (set_ssao(true) in the two review bins only; offscreen
      default untouched — tests/goldens depend on it). Street-set
      notes: casa door has no reja by construction (rejas are
      window-only — gap c covered as door close + window-reja close);
      3-casa row renders carry 1024² DDS sidecars (OOM workaround,
      flagged in manifest — judge repeat/geometry there, texel quality
      from inspect + closes).
      ~~RENDERER DEBT (queued, not now): no texture dedup — store.rs
      binds textures per primitive (casa = 139 prims → ~7.0 GB decoded
      RGBA8 per instance; 3-instance street scene OOMs a 3080 Ti even
      with 2048 BC sidecars). A dedup fix removes the street-scene
      constraint entirely.~~ SUPERSEDED, verified 2026-08-02: the dedup
      landed the same day this was written, `cac3c94` "Dedup material
      textures: one GPU texture per unique image, shared across primitives
      and models". Both levels exist now — a file's primitives alias one
      `Arc<SharedImage>` so decode runs once per image, and the store-level
      cache keys on a content hash so identical images dedup across
      separately loaded models. **The OOM is therefore unattributed again,
      not fixed**: whoever next hits it must re-measure rather than assume
      this note's cause. One live suspect is that a content hash cannot be
      taken before the decode it would have avoided, so peak CPU memory is
      unchanged by dedup.
      AO-on evidence DONE (`897c40c`: set_ssao(true) in asset_inspect +
      zone_review, offscreen default untouched; clay-channel diff proves
      AO visible). G2 RE-GATE VERDICT (Opus, 2026-07-31): **FAIL, one
      blocker** — record at docs/reviews/town/g2-kit-regate-2026-07-31.md
      (original G2 was never written to docs; judge recovered it from
      transcript and carried Q1-Q4/D-ids into the record). Blocker is a
      NEW regression: 2 of 4 roof slopes render as plaster, no tile
      (proven in normal+clay+albedo channels; g2-pilot had all 4 tiled
      → arrived with `241f23a` and/or the DDS sidecar bake, evidence
      can't separate). Scores Q1 3 Q2 3 Q3 6 Q4 4 (was 3/2/5/2).
      Healed: wing wall sealed, quoins fixed (corr 0.205, S 0.049),
      eave sawtooth gone, ashlar grade in band (L* mean 68.7, b* at
      ceiling), valley continuous, encalado 30 m repeat risk DISCHARGED
      (only periodicity is the 3×-same-glb building module). Residuals:
      wing slope UVs still 90° rotated (louvre read); tile blob past
      wing eave (watch). Watch: D9 mip-blur persists, D10 ghost blocks
      now dominate whitewash read, m4/m6 merge confirmed worse (Δlum
      0.006), m5 unbound on casa → G4, m2/m3 hue resolved, m3 sat
      unchanged non-telegraphing. FIX WORKER (a77c68bb9980f493e): killed
      mid-run by API session limit 2026-07-31 ~13:47, resumed from
      transcript after disk-state verification. Verified done: root
      cause = Blender boolean UNION material-slot fallback (fix in
      buildings.py: pre-append slots + single multi-operand EXACT
      union), geo.py +sign slope rotation (tiles were buried under
      deck), wing transform baked into mesh data (UV louvre fix),
      verify.py _roof_slope_faults check; casa_corner.glb rebuilt
      13:46, roof_faults []. Worker completed the rest: open_wall_faces
      red root-caused to 241f23a's chained pairwise unions (160
      non-manifold edges) — replaced by the single multi-operand union,
      detector T-junction pairing fixed with a midpoint-coverage test,
      the 4 residual flags proven seams against pre-export ground
      truth; red-proof artifact target/town-kit/g2-regate/probe/
      verify_red_casa_corner_street.json; full green, all committed
      `6d665d6`; evidence fully re-rendered (AO on), manifest updated,
      zones.ron reverted.
      G2 FINAL VERDICT (fresh Opus judge, same day): **PASS**. Blocker
      cleared in all channels (4 slopes tiled, identical pan gauge
      across the ridge; street 30 m roof band 19.4% terracotta; value
      hierarchy corrected — roof 0.344/0.366 vs wall 0.532). Wing UV
      louvre read gone (single 16 px along-ridge autocorr peak). Union
      rework regressed nothing (facade column-step p99 2.96-4.25/255 ≈
      FAIL round's 3.1; corner weld + valley clean; D10 ghost-plaque
      structure identical pre/post → texture-layer, not UV seams).
      Scores Q1 7 Q2 8 Q3 7 Q4 7. NEW WATCH N3: roof albedo
      mirror-wraps down the fall line (corr 0.763, dark mid-slope band
      legible at 30 m) — texture-layer, D9/D10 family; also noted: no
      ridge cap (caballete), bare arris. Carried watch: D9 mip-blur,
      D10 ghost blocks, m4/m6 Δlum 0.006, m5 unbound → G4, N2 tile
      blob. Record: docs/reviews/town/g2-kit-regate-2026-07-31.md
      (re-check section appended, supersession pointer added).
- [x] P2.4 Full layout: visuals as zones.ron props + mirrored collision in
      chapter03; RECONCILE AOI_RADIUS 40 vs premise precinct (−30,−30);
      spawn + portal corridor clear; street widths from P-C; no camps v1
      DONE (2026-07-31, all steps 0-9 of tasks/town/p24-layout.md; step 1
      folded into 0/2): 15 kit props live in zones.ron start (2 casa rows,
      chapel at premise (−30,−29) door east, gate + 4 wall fragments,
      well) mirrored by 25 collision-only spawns / 14 prefabs in
      chapter03; yaw map render-confirmed (0→S, 90→W, 180→N, 270→E);
      one plan defect fixed in flight — §4's mid-row south casa_corner
      wing interpenetrated its west neighbor by 4.6 m, south row slots
      swapped so the corner holds the west end, wing outward at
      (−16.8, −11.5). Clearances script-verified: ring 4.25 m, gate
      opening exactly 3.2 m on the corridor, only party-wall (0.60) /
      wing-main (1.05) / chapel-joint (0.30) overlaps, extent r=50.65.
      content_lint 15/15 + server zones 6/6 green; evidence frames in
      target/town-layout/p24/ (plaza mid, both nave interiors).
      USER CHECKPOINTS (bundled, not taken): (1) P2.4.0 scope pull =
      scheduling ack; (2) chapel door east vs premise §6 "west" —
      recommend amend premise one line, doc is user-owned, NOT edited;
      (3) reja_set stays unplaced v1 (rejas built into casa windows).
- [x] P2.4b Opus layout review: PASS with fixes, 3 required + 4 minor.
      Record: docs/reviews/town/p24-layout-review-2026-07-31.md (premise
      fidelity 7, composition 8, readability 6, interiors 5, defects 6).
      Skeleton right: facade lines exact (north row z=+9.1, south z=−9.1,
      18.2 m street), party walls read as a terrace with no z-fight, both
      corner wings turn outward, gate+breach frames the east approach, no
      floating/sunken/bad-yaw, ring+corridor clear against visual AABBs.
      Fixes APPLIED (uncommitted, verified on disk, zones 6/6 green):
      F1 chapel_arch (−26,−34)→(−26,−36.5) — yaw 40 swung its 5.46 m span
      into the nave, a pillar stood on the chapel floor; §4's "clears by
      0.9 m" was false, doc corrected to 1.1 m. F2 cypresses ×5 (1.8 m
      shrubs → 8.6–10 m silhouettes). F3 candelabra_shrine off the plaza
      → two votive stands flanking the apse (−38,−27.6)/(−38,−30.4).
      F4 olive_stump →(−17,19) off casa_small_b's corner. F5 rocks
      rescaled to 0.65–0.85 m (worker corrected a swapped height→type
      label in the fix spec by measuring the glTF accessors — rock_09
      base 0.0329 m/unit, rock_07 0.1437). F6 gravestone z jittered.
      F8 well z −5.5→−4.6 in BOTH zones.ron and chapter.ron.
      WATCH for the F7 judge: rock_09 at scale 24.3 is a ~3.2×4.0×0.8 m
      flat slab — plausible as a field outcrop, unconfirmed on a frame.
      NOT DONE, user-owned: premise §6 needs a TWO-line amendment, not
      one — doors east AND collapse over the entry (east) bays, apse
      intact. The built chapel already does this; only the doc lags.
- [x] P2.5 D5 guard DONE (`3c0dbe1`): 4 new lints in content_lint.rs —
      bijection+coverage, axis-aligned yaw, clearances, play radius;
      19/19 green. Kit-vs-dressing split keys on assets.json kind=="kit"
      (no name list). CORRECTED MID-TASK: the worker's first footprints.ron
      pass gave every composite member a `size` copied from the prefab
      under test — check (b) would have been green by construction. Member
      sizes deleted; composites now union their spawned hitboxes and
      compare to the glTF-MEASURED top-level footprint, which is an
      independent witness. Chapel union falls 3.03 m short vs the 3.05 m
      tolerance authored earlier for the uncollided apse fan — 0.02 m
      margin, two numbers that never saw each other. Red-proof on BOTH
      axes: chapter.ron spawn +0.5 → RED; footprints.ron member offset
      +0.5 → RED incl. the coverage check firing independently.
      Two worker corrections worth keeping: buildings ARE server-side
      solid (its walk route clipped the south row), and clearance now
      excludes solids outside a [0,2.0] player band because
      SeparationSystem's narrowphase ignores Y while the broadphase gate
      does not — an aloft lintel never collides with a ground player.
      Replication walk extended: bot threads x≈−20 to the chapel door and
      sees all 7 chapel pieces; zones 6/6.
- [x] P2.4-F7 evidence gap CLOSED: zone_review's single-linkage clustering
      (CLUSTER_RADIUS 20) merged all 30 town props into one cluster and
      spent the only mid shot on the plaza — criteria 1–3 were scored on
      a partly unmeasured town. Four targeted frames required before the
      gate record closes: east gate + crucero breach, chapel exterior
      from the plaza side, chapel precinct/graveyard, north row facade.
      DONE: NamedShot/ROCALBA_SHOTS/render_named in zone_review.rs, four
      hand-aimed shots gated on chapter=="chapter03" (clustering path kept
      only for zones with no authored list; east re-run as regression,
      unaffected). Frames in target/town-layout/p24-f7/ — worker read
      every PNG and re-aimed twice.
- [x] P2.4c Opus re-judge on F7 evidence: PASS with fixes, 1 required.
      Scores 7/8/7/6/7 (readability +1 — missing-evidence penalty gone and
      3 of 4 beats read; interiors +1 — F1 removed the worst fault;
      defects +1 — 4 of 6 round-one defects closed. 1 and 2 hold: gains
      were already priced in, new measured losses cancel them).
      F1/F4/F5/F6 landed. F8 UNVERIFIED — no frame in the set covers the
      plaza. rock_09 @24.3 RULED KEEP: reads as an angular field boulder
      with grounded contact shadow, not pavement, not stretch — the flat
      aspect is the model and the footprint carries the read.
      F2 landed at distance with a named cost: cypresses are now the only
      silhouettes surviving the fog, but ×5 gives 0.6 m foliage plates and
      no trunk — a 9 m wall of dark shards up close, all five inside the
      play radius. Keep the scale; a multiplier cannot buy both reads.
      Needs a real cypress model → carried to asset work.
      REQUIRED F9 (queued, not yet applied — P2.5 holds zones.ron):
      both candelabra x −38.0 → −37.0. The apse end wall is a full-height
      panel at exactly x = −38.00 and each stand has ±0.59 m depth, so
      half of each was inside the masonry. NOTE: −38.0 came from the
      round-one judge — third instance today of a placement claim made
      without checking the actual extent against the surface it clears.
      Also queued: R1 crucero scale 1.0→1.5 (at 1.8 m its gameplay
      silhouette is identical to a gravestone's); R2 two or three rock
      props outside the chapel's collapsed east half (coords + door-axis
      exclusion in the review doc). Both dressing-only, no collision.
      ALL THREE APPLIED (`44be52d`). The mandatory extent check earned
      itself immediately: the review's prescribed R2 coordinates did NOT
      clear — they overlapped chapel_arch's true world AABB — so the
      worker computed its own, placing 2 rock_07 at (−25.5,−24.1) yaw 90
      and (−21.6,−34.3) yaw 0, clearances 0.32–1.43 m, both inside the
      collapsed east half. It dropped the third rather than force a bad
      placement (the only remaining pocket sat under the intact roof).
- [x] Phase 2 gate: cargo test --workspace GREEN on the first run, no
      fixes needed. 63 game + 19 content_lint + 12 protocol + 38 server
      + 10 e2e + 3 combat + 5 persistence + 3 security + 5 wireformat
      + 2 shutdown + 1 watchdog + 6 zones; loss/soak ignored
      (release-only). Committed `44be52d` + `3c0dbe1`.
- [ ] KIT FINDING, escalated — the chapel does not read as a chapel.
      mid_chapel.png: no bell gable, no cross, no window, no portal
      surround — a rectangular ashlar box with half a vault; and the
      collapse reads as NEVER ROOFED (level coped wall tops, a clean
      voussoired cut edge, zero rubble outside). G2 gated the kit's
      materials and geometry, never whether the building reads as a
      church, so this was never measured. Not a Phase 2 layout blocker
      (judge passed the layout); belongs to kit work. R2 is the cheap
      layout-side half. Second kit-side item from the same frames: quoin
      chains strand as loose blocks on the flush facades at every party
      junction — caused by the placement decision but no overlap value
      fixes it. Third: the roof mirror-band (G2 watch N3) is WORSE at
      28 m than at wide framing — re-price from watch item to
      gameplay-framing artifact.
PHASE 2 CLOSED 2026-07-31 at `3c0dbe1`. Next: Phase 3 (heroes).

## Phase 3 — Hero + dressing generation (~5.5 h GPU) — IN PROGRESS 2026-08-01

REORDERED vs the plan, and the reorder is forced, not preference: the plan's
first chain run is RUN-H1 "chapel portal / arch re-roll", but the escalated kit
finding says the chapel has no portal surround, no bell gable, no cross, no
window. D1 rules shells are Blender-procedural and Hi3DGen is heroes ≤5.5 m
only — so whether the portal is kit geometry or a hero decides what C1's
concepts depict. The chapel shell pass therefore gates C1, and it is zero-GPU,
so it costs nothing from the §8-approved budget.

DISPATCH CONSTRAINT 2026-08-01: **Fable 5 tier limit reached** — the P3.0 spec
worker died on it (disk verified clean first, zero artifacts, re-dispatched on
opus). Analysis dispatches route UP to opus for the rest of the campaign, never
down to sonnet; sonnet still implements. Capacity event, not a reasoning fault
— no lesson (and none is admissible: it left no artifact).

- [ ] P3.0 Chapel church-legibility kit pass (zero GPU). Closes the escalated
      KIT FINDING above plus its two riders (quoin stranding at party
      junctions; roof mirror-band N3 re-priced to a gameplay-framing artifact,
      no ridge cap). Spec first (fable → `tasks/town/p30-chapel-legibility.md`),
      then implement, then Opus judges offscreen renders. Spec must rule
      per-feature what is kit vs hero — that ruling is what unblocks C1 — and
      must price the D5 coverage-lint impact (an espadaña moves the chapel's
      measured glTF footprint against a 0.02 m tolerance margin).
      SPEC DONE: `tasks/town/p30-chapel-legibility.md` (790 lines, opus).
      F1 espadaña + F2 bell/cross + F3 flush portal + F4 oculus/saeteras +
      F5 collapse read (ragged crowns, fracture lip 14→18 wedges jitter→0,
      new `extrude_ends` cantilever) + F6 ridge cap on all four casas;
      riders: quoin flush (measured protrusion swings −0.015 to **+0.146 m**)
      and N3 root-caused as MEASURED not inferred — `_roof_deck_panel` uses
      the cube's *signed* local coords, so the wrap seam lands exactly at
      mid-slope. 6 new verify checks C1-C6, each red-proofed.
      **H1 RULING (gates the GPU run): chapel-portal half CANCELLED, every
      chapel feature is kit.** Three sufficient reasons — no flat-back/
      dimension guarantee for mating against a 0.6 m wall; a hero atlas =
      different limestone at different texel density, which IS the G2 Q1
      3/10 failure; and nothing to generate (a poor village portal is a
      plain voussoir ring). H1 keeps ONLY the `chapel_arch` re-roll
      (5.497 m, freestanding, no mating contract) — all ×4 candidates now
      on one subject instead of split. C1's concept list must depict no
      portal, bell gable, cross or oculus.
      **D5 impact ZERO by design** — the espadaña is made coplanar with the
      east wall, so the XZ AABB stays 20.229×8.200; union 17.20×8.20,
      shortfall 3.03 vs tolerance 3.05, margin 0.02, all unchanged. Only
      height moves (10.534→13.16) and no lint reads height. No new collision
      member: espadaña base sits at world y 7.0, five metres above the
      clearance lint's 2.0 m band. Check C1 turns that invisible coupling
      into a build failure.
      OPEN-1 and OPEN-3 RESOLVED by the orchestrator, no user needed:
      OPEN-1 moot (the H2-H7 chain list is in the approved plan file outside
      the repo; retablo is already H3). OPEN-3 closed by ratified D2
      "broken-vault chapel" — the vault IS the roof, and the spec's own
      arithmetic makes tiles over it geometrically impossible, so the chapel
      carries no terracotta. OPEN-2 (premise §6 wording) stays user-owned.
      CORRECTION absorbed: casa_corner is **6576** tris, not the 5317 this
      file recorded; chapel 1037 → ~2025, casa_corner → ~7226. No lint caps
      triangles.
      QUEUED, found while measuring, NOT fixed (out of P3.0 scope):
      (a) ~~**the D5 union check is circular for single-piece types**~~ CLOSED
      2026-08-02 by a new check (b'),
      `town_footprint_sizes_match_installed_gltf`: `footprints.ron`'s `size` is
      re-measured off the installed glTF over the same 2 m player band the
      clearance lint uses (that constant is now shared, not duplicated), so
      every type — single-piece included — is graded against something no one
      authored. Red-proved in both directions.
      It caught real drift on its first run, and the drift was exactly the
      `nominal-dimensions-are-not-placed-extents` failure: four casa `size`
      rows were the plan's wall-centerline number plus one wall thickness — an
      ARITHMETIC — sitting ~5 cm wide of the built mesh, under a header comment
      claiming they were "measured from the installed glTFs". Chapel was 0.20 m
      wide for a different reason: its `size` was the full-height extent, not
      the ground-band one. All five corrected to the reading; check (b) stays
      green with margin (chapel shortfall 3.03→2.83 against tol 3.05).
      Tolerances untouched — the only slack added is 1 cm of the manifest's own
      centimetre quantization. (b) ~~`chapel_wall_side.ron`'s comment is stale (spans to
      3.75 m, not 7.5)~~ — fixed 2026-08-02; the shell is spawn-centred at
      y=0, so its top is 3.75 m and the 7.5 m springline is the visual's. (c) ~~`gate_arch`'s intrados is 1.94 m over a 3.2 m
      opening — the same extrados/intrados confusion F3 was written to avoid.~~
      FIXED 2026-08-02 `8c90f41`, exactly the spec's one-line fix (§5.6 item 3):
      extrados sized one band out, clear span 3.2 m, arch peak 5.20→5.83, wall
      top 5.60→6.23, `gate_head`'s shell and its chapter.ron spawn y follow.
      A build-time assert on the *returned* radius now guards it — red-proved
      by reverting the line, which printed the predicted "spans 1.940 over a
      3.2 opening". Verified on `mid_gate.png` (target/gate-arch-fix/): the
      ring springs off the jamb faces and the opening reads full width.
      content_lint 20/20, footprint unchanged at 6.4×0.9.
      SEEN IN THAT FRAME SET, for the ground task not this one, and stated at
      its real size rather than as an alarm: the street rectangle's east edge
      (x = 15.625) is only 0.6 m past the gate at x = 15, so the hard line is
      the threshold, not an apron in open country. What does read oddly is its
      z extent there — full width ±9.375 at an x where the casa rows have
      already ended, so the corner between the last house and the gate is paved
      empty ground. Defensible for a town gate approach; decide it together
      with the material, not before. The blue-slab cobble against warm cracked
      earth is louder at gameplay framing than the gate record measured.
      IMPLEMENTED (uncommitted, tree verified): F1-F6 + both riders + checks
      C1-C6, each red-proofed. Measured off the rebuilt glTFs — chapel
      1037→2009 tris, XZ AABB 20.229x8.200 UNCHANGED, y-max 13.160; casas
      4006/4092/5768/7226 (exact match to spec §4.1). content_lint 19/19
      with all five D5 tests green and NO edit to footprints.ron or
      chapter.ron — the coplanarity constraint held. Workspace suite green
      twice.
      MATERIAL-ROOT REGRESSION, caught and fixed before the gate: the first
      rebuild resolved materials from `target/town-materials/` — the
      gen_material candidates P2.3 REJECTED wholesale — instead of
      `target/town-kit-materials/` (the six CC0 winners). Three families had
      no dir under the wrong root and fell back to placeholder; the worker
      read that as a naming gap and ADDED ALIASES so the wrong root would
      resolve, converting a loud failure into a silent swap. Caught by
      diffing materials.py because P2.3 had flagged that resolution path as
      fragile — no automated check saw it. Fix: aliases reverted; root cause
      closed — `build_materials` now HARD-FAILS when `--materials-dir` was
      given and a family cannot resolve (placeholder kept only for the
      genuine no-arg mode; proven to fire against a bogus dir). Rebuilt
      against the correct root, all six families `baked:town-kit-materials`,
      zero placeholder. **Blast radius zero** — the install step rewrites
      URIs to the committed, correct, complete shared
      `content/models/townkit_textures/`, so nothing falsified reached a
      shipped model or a frame. That is a name collision doing a guard's
      job, not a guard: had the shared dir lacked `iron_wrought` (the one
      family this pass adds), the rejected m6 rust-brown would have shipped
      as the bell and cross. Lesson:
      `tasks/lessons/2026-08-01-a-fallback-that-fires-is-evidence-about-the-input.md`.
      GATE ROUND 1: **FAIL** (5/4/8/2/3), record
      `docs/reviews/town/p30-chapel-legibility-2026-08-01.md`. Blocker: the
      "ragged" crown was a BATTLEMENT — ten blocks sharing a bottom face at
      y=6.58 over a 6.9 m run, reading as merlons; the pass lowered the level
      coped top 0.92 m instead of destroying it. Bigger finding: **three of
      the six new checks were green while the defects they name were still in
      the pixels** — C4/C5 graded `geo._roof_deck_panel` (real, called, really
      fixed) while the visible terracotta is separate tile meshes that never
      route through it; C6 read the right mesh, wrong property. Every
      red-proof was honest; the drafts genuinely moved. Widened γ of
      `tasks/lessons/2026-07-21-probe-must-fail-when-broken.md` (the
      false-negative direction is its home — a duplicate clause added to
      `the-instrument-cannot-grade-itself` was removed so the two don't drift).
      FIX ROUND: root cause under all the UV symptoms was ONE line —
      `bpy.ops.uv.cube_project` origins each projection on the object's own
      median, so every congruent object (25 tiles/slope, 26 ridge caps, 18
      voussoirs, crown blocks, rubble) stamped one identical patch. Replaced
      by a world-anchored per-face projection; `vordar_uv_offset` (a per-quoin
      random offset workaround for the same defect) DELETED as subsumed.
      `slope_uv_seam` deleted not fixed — it graded the deck, buried under a
      full course of tiles, on a premise ("no integer crossing") that is false
      for a REPEAT-tiled texture. Two divergences from the gate's fix list,
      both accepted on merit at re-gate: the quoin fix targeted an inter-course
      air void because the record's prescription described PRE-FIX code (the
      nominal-dimensions lesson firing on a reviewer again), and barrel_shell
      wedges gained a cylindrical UV because a world box projection is blind to
      depth. Fix 8 (exterior rubble) NOT DONE, geometrically blocked and
      reported: chapel AABB has 0.02 m D5 margin on every axis so the model
      cannot emit a vertex outside its walls, and a separate prop hits
      contradictory content-lint rules (`kind:"kit"` demands a collision box +
      axis-aligned yaw, both wrong for debris; any other kind demands an
      occlusion map a townkit export doesn't produce).
      GATE ROUND 2: **PASS with fixes** (8/7/8/8/7). Blocker dead — crown
      descends as broken courses, no shared datum, no merlon rhythm at three
      angles. Riders verified on the VISIBLE terracotta independently of round
      one's broken metric: along-ridge autocorrelation peaks only at the
      24.4 px tile pitch, and **no peak above 0.35 at any lag down the fall
      line**. COMMITTED `3feb4a7`.
- [x] P3.0b Re-gate's 4 non-blocking fixes. **Fix 1 runs first and may
      invalidate the rest**: the limestone striping (hard 1-2 px full-height
      seams, most legible thing on the wall at 2 m) is confirmed real but
      UNATTRIBUTED — the shipped detail tile IS non-seamless (wrap-edge |Δ|
      4.50 vs 3.47 interior), yet a wrap artifact should seam in both axes and
      the measurement is 2.16× more vertical than horizontal. A grazing camera
      explains that; so does this round's UV change. If the latter, `3feb4a7`
      shipped a regression. Probe: head-on re-render + detail strengths at 0.
      Then: (2) open the oculus bore, currently a filled disc with bright bars;
      (3) move interior rubble weight into the collapsed bay — it clusters
      where the roof survives; (4) break the crown's five near-equal stair
      steps.
      CARRIED TO G4: `iron_wrought` is metallic 1.0 with near-black albedo, so
      f0 ≈ 0.03 and IBL specular is all it has — the bell reads very dark and
      the fix touches every reja and the crucero. Campaign-level materials
      finding, not taken locally. Also: the content-lint rule forbidding
      ankle-height debris props is what should be fixed to unblock fix 8.
      DONE, ADJUDICATED **ACCEPTED WITH RESIDUALS** (PASS stands), committed
      `5646f61`. Fix 1 was the payoff: the striping is a REGRESSION FROM
      `3feb4a7`, not the renderer's. Probe = detail strengths at 0 + head-on +
      a parent-commit render at identical framing — striping identical with
      the overlay bound and unbound (14 lines, min hp −34.86 vs −34.84),
      present head-on, ABSENT on the parent. Cause: span-B columns carried
      `bevel=0.02` and overlapped 1 cm → every junction a chamfer pair plus a
      full-height coplanar sliver; 7 of 14 lines within 1 cm of predicted
      `chapel_side_-1_B_wall*` boundaries. After: grazing 14→0 by the judge's
      count, head-on 6→0 (better than the worker's claimed 8→4).
      Round one's "it's the renderer's triplanar overlay, independent of this
      round" was a CODE READ used to route the defect out of scope — γ of
      `tasks/lessons/2026-07-26-a-visible-mechanism-is-not-an-attributed-one.md`
      widened for it (disowning a defect on an unmeasured cause is the same
      error as fixing on one, and gets less scrutiny because it is cheaper).
      Ironically the layer blamed is that note's own second occurrence.
      Fixes 2/3 both DIVERGED and both accepted: (2) deepening the oculus bore
      was tried and MEASURED INERT — 1.15 m occludes 17% of the aperture at an
      8° off-axis camera — real cause is the bore facing a vault soffit lit
      from above by the missing roof, so shuttered in `oak_dark` instead;
      (3) the judge's "rubble clusters where the roof survives" DID NOT
      REPRODUCE — vault occupies local x [−8.000, 0.000], all pieces lie in
      x [1.176, 6.981], and `mid_graveyard`'s eye (23.1 m up, 20.9 m out) is
      shadowed by the east wall from x 2.2-7.6 so the frame shows the nave
      down the vault tunnel. Judge confirmed this independently and accepted
      the artifact finding. Real defect underneath: `bed` used the UNROTATED
      half-height, burying tilted voussoirs up to 60%.
- [ ] KIT DEBT — the coplanar-sliver signature still ships on `wall_segment`
      (`close_wall_segment.png` corner pier: 3 px band at x 260-262, +30 luma
      over the wall face, 92% of wall height, crossing every course and the
      coping — four bands where a chamfered arris has three). NOT this
      campaign's regression: its POSITION accessors are byte-identical across
      `3feb4a7`, only UVs moved. Same root cause as the chapel's span-B fix
      (`5646f61`) and the same known fix; owner is the kit box builder, and
      the blast radius is every kit box, which is why it was not tacked onto
      P3.0. Judge ruled non-blocking → G4.
      **ROOT CAUSE MEASURED 2026-08-02, and it is not what this note says.**
      `make_box`'s `bevel=` produces NO CHAMFER. Isolated probe, one box,
      current code: `geo.make_box(..., bevel=0.02)` returns 30 polys / 32 verts
      but only **6 distinct face normals, every one axis-aligned** — the call
      `bmesh.ops.bevel(bm, geom=bm.edges[:], affect="EDGES")` splits each face
      into a 2 cm border loop lying FLAT on the face instead of cutting an
      arris. `project_uv` is innocent: polys/verts/normals are identical before
      and after it. So what ships at every kit arris is a full-height coplanar
      2 cm strip — the "four bands where a chamfered arris has three" was the
      right observation and the wrong explanation, and the docstring
      ("exposed edges chamfered by `bevel`") describes geometry no asset has.
      Cost carried meanwhile: every kit box is 60 tris where 12 would do.
      Two other stated causes are REFUTED for `wall_segment` by direct
      measurement of the shipped glTF (all 420 tris): UV/world density is
      **uniform at 0.005821** — no texel-density seam anywhere — and there are
      **0 duplicate triangles** — no coplanar duplicate. Rebuilding the asset
      reproduces both figures exactly, so the installed file is not stale.
      Retro-note on `5646f61`: its "every junction a chamfer pair plus a sliver"
      narrative was half wrong — no chamfer existed — but the fix it actually
      made (removing the 1 cm column overlap) is untouched by this, and its
      14→0 measurement stands.
      **FORK FOR THE USER, not taken — both need a kit-wide rebuild and a
      re-gate, and neither should start on the last of a credit budget:**
      (A) make the bevel real (pass verts as well as edges) — the kit gains the
      chamfered arris the code always claimed, silhouettes change slightly,
      tri counts rise again; (B) delete the `bevel` parameter outright — pure
      erasure, kills the sliver strips, cuts every box from 60 tris to 12, and
      the arris reads as the hard 90° edge it already effectively is. B is
      cheaper and cannot introduce new geometry; A is the only one that keeps
      the softened-arris intent. Either way P3.0's §4.1 tri table and the G2
      records' counts go stale and must be re-measured.
      **FORK TAKEN 2026-08-05 (self-approved under user autonomy grant): B,
      hard edge — decided-while-unsure item for the user.** Probe re-run
      refuted this note's root cause a second time: `create_cube` is welded
      (remove_doubles a no-op); the degeneracy is `segments=2` +
      `clamp_overlap=True` at offset 0.02 on kit-scale boxes — segments=1/3
      cut a real chamfer. Three pixel-distinct variants rendered; judge
      scored current 3/10 (13–15% luma trough on every arris),
      real_chamfer 9/10, hard_edge 9/10 — indistinguishable at gameplay
      framing (2 cm ≈ 1.5 px), and hard edge is 12 tris vs 44 and deletes
      the degenerate path (swap rule). Probe artifacts:
      `target/kit-bevel-probe/`. KIT-WIDE REBUILD DONE (uncommitted):
      bevel params deleted from geo.py/buildings.py (curve-bar
      `bevel_depth` for reja is a distinct mechanism, untouched), all 9
      pieces rebuilt+installed, lint 22/22, tri table
      `target/kit-rebuild/tri_table.md` (e.g. wall_segment 420→84,
      casa_small_a 4066→2578; reja_set 576 unchanged). Regression judge
      **PASS** (9/8/10/10): hard edge removes three measured OLD artifacts
      (−5.7% sub-shadow trough, +39% ghost spike, floating slivers);
      chamfer already invisible at mid range. SHIPPED in `45bab1d`.
      Record + new tri table (supersedes P3.0 §4.1 / G2 counts):
      `docs/reviews/town/kit-hard-edge-rebuild-2026-08-05.md`. CLOSED.
      PROCESS NOTE from the adjudication, worth keeping: **byte-identity
      licenses skipping a REGRESSION check, not a fresh look.** The worker
      skipped 14 close-ups on byte-identity grounds and was right about
      regression; the residual above was reachable only by opening the very
      frame fix 1 had named.
      GATE G-P3.0 **FAILED** (`docs/reviews/town/p30-chapel-legibility-2026-08-01.md`):
      blocker = the ragged crown was a battlement, plus 10 numbered fixes.
      FIX ROUND DONE (uncommitted) — plan/record `tasks/town/p30-fix-round.md`.
      Root cause under gate fixes 2+3 and the reason three checks were green
      on shipped defects: `project_uv` used `cube_project`, whose origin is the
      OBJECT'S OWN MEDIAN, so every congruent object got an identical UV set
      (25 roof tiles, 26 ridge caps, 18 vault voussoirs, crown blocks, rubble).
      Replaced by a world-anchored box projection; `vordar_uv_offset` deleted as
      subsumed. C4's `slope_uv_seam` graded the deck — a surface buried under a
      full course of barrel tiles — and was replaced by `uv_patch_repeat`
      (per-object UV multiset, every type): 32 red on shipped, 0 after. C2 gains
      `collapse_crown_datum` (1.00 -> 0.20, threshold 0.30, stable across its
      free parameters); C6 gains `quoin_course_void` (139 voids of 0.030 m -> 0).
      DIVERGENCE from the gate on fix 4: its prescribed mechanism is spec §0's
      PRE-fix code; shipped quoins were already flush, the real defect was the
      0.03 m inter-course air gap. Fix 10's coplanar pair was `chapel_floor`'s
      top at world -0.5 = `GROUND_TOP_Y`. Fix 8 (exterior rubble) NOT DONE and
      reported blocked: the frozen footprint forbids kit-side geometry outside
      the walls, and both prop-registration routes are wrong for scattered
      debris — stays with R2. Chapel 3733 tris, XZ AABB 20.229x8.200 unchanged,
      content_lint 19/19, two green workspace suites, 28 frames re-rendered
      including the new `mid_chapel_skyline` (espadana against sky).
USER RULING 2026-08-01 — **every open user checkpoint is closed by delegation.**
Verbatim intent: the premise doc was withheld deliberately, "this task was asked to
do independently without my help to test your capacity to do quality assets and a
good looking zone that makes sense and can end in a real production environment, so
makes no sense me babysiting you. Do whatever you think is the best to reach our
goal." Consequences, binding for the rest of the campaign:
  - `docs/town-premise.md` is NO LONGER user-owned. It is mine to amend. The
    standing "recommend, do not edit" rule on it is DEAD — strike it wherever it
    appears above; those entries are all superseded.
  - Nothing further goes to a user checkpoint. Rulings that were bundled and
    waiting are taken by the orchestrator and recorded here with their argument.
  - The bar is production-shippable, not plan-compliant. A divergence that makes
    the zone better is the point of the exercise, not a deviation to apologise for.
  Checkpoints closed immediately, no work required: P2.4.0 scope pull was a
  scheduling ack only. `reja_set` stays unplaced in v1 — rejas are built into the
  casa window geometry, so a separate placeable set has no subject; it is not
  deleted because Phase 4 interiors may bind it.
  Delegated (in flight): premise §2/§6 reconciliation (doors east, collapse over
  the east bays, the P3.0 chapel features, the S/V-ceiling contradiction, m5 soot).
  Still open, needs a fact before a ruling: `gen_material.py`'s fate — falsified
  for structured families at P2.3 and superseded by the CC0 photoscan path, but
  its relationship to the Phase 3 prop-texture chain (shared code? shared env-var
  hooks? `prop_multiview_qwen.json`?) decides delete-vs-keep. Do not guess it.

- [x] PREMISE RECONCILED (uncommitted, diff verified on disk: +44/−17, one file).
      Eleven divergences ruled; the doc lagged on nine of them. Beyond the six
      known: §1 said decay rises with distance from the CHAPEL while §4 puts the
      most decayed quarter beside it (→ "from the plaza"); §3 promised terracotta
      on "every roof" when the chapel's vault IS its roof (OPEN-3's arithmetic,
      now in the doc); §3 bound worn cobble to the chapel floor while
      `buildings.py:761` binds lime slabs; the "six materials" list did not match
      the kit's six slots (smoked plaster folded into the encalado entry, cobble
      named as ground — vocabulary still closed at six, none added); and the one
      that would have cost real work: **§6 placed the retablo at the EAST end,
      and the door is east** — uncorrected, the doc specified the altarpiece
      behind the open door. Retablo → apse, which is where F3/F9 already put the
      votive stands.
      §2's per-pixel S/V gate is DELETED, not softened: replaced by a threat
      reservation stated as a conjunction (hue 350°–25° ∧ S≥0.7 ∧ V≥0.8) with a
      hard S 0.35 sub-ceiling inside the reserved window, so terracotta passes by
      MARGIN and m6's rust-orange still fails — no exemption list. The ambient
      ceiling now reads on the rendered mean under ship lighting and binds
      chromatic surfaces; near-achromatic whitewash is bound in saturation only.
      §7's premise-citation clause: the prefix mechanism dies (CLIP's 77-token
      limit binds the concept and multiview stages too, so it was unfollowable at
      exactly the stages it targeted); citation moves to the run manifest, which
      is where traceability was actually wanted.
      Spec number corrected: p30 §5.6's "~12.6 m above the plaza" is the espadaña
      apex's world y; `GROUND_TOP_Y = −0.5` makes the height above the plaza
      13.16 m.
- [ ] BUILD-WRONG defects found while reconciling — the doc was NOT edited to
      absolve any of these. Ordered by how much zone quality they buy:
      (1) **Zero candle-gold emissive anywhere in the town.** §1 calls it "the
      town's signature and its wrongness" and §6 stages the whole lighting intent
      as cool shafts vs warm candle-gold; half of that is unbuilt. §5's lit
      porter's brazier at the east gate is also unplaced. This is the largest gap
      between the premise and the built zone, and it is Phase 4 interior/lighting
      work, not a materials fix.
      (2) **Plaza and streets are `cracked_earth`; §3 mandates worn cobble.**
      INVESTIGATED — my "cheap zones.ron change" premise was WRONG, and the
      worker correctly refused to implement rather than force it. The ground is
      **one material per zone, full stop**: `GroundDef { texture_dir, tile, size }`
      (`zones.rs:93-103`) is three scalars with nothing spatial, and
      `generate_ground` (`ground.rs:62-116`) emits ONE primitive with UVs a pure
      linear function of world XZ. East's `worn_cobble` (`zones.ron:150`) is not a
      bounded-region precedent — it is the same all-or-nothing switch thrown the
      other way, and east gets away with it because east IS a cobbled square.
      Doing it in `start` cobbles the countryside to 200 m. Confirmed ABSENT, not
      merely unfound: no splat (`MeshVertex` is a fixed 48-byte layout, no color
      or weight channel, `mesh_pipeline.rs:20-25`), no decals (zero hits repo-wide).
      SMALLEST HONEST FIX, and the renderer already supports it — `MeshData
      .primitives` is a Vec, each `PrimitiveData` carries its own material, and
      `frame.rs` already binds per primitive. **Zero engine or shader change.**
      `GroundDef` gains an ordered `regions: Vec<GroundRegion { texture_dir, tile,
      min, max }>`; `generate_ground` emits one primitive per region. Blast radius
      is 4 content_lint sites, 3 mechanical. No server/collision/gameplay impact —
      ground is client-visual only and walkability is the flat `GROUND_TOP_Y`
      plane regardless of material.
      DESIGN DECISION RULED (it is the reason this is not a small diff): the grid
      step is 400/129 = 3.125 m, so a per-quad region test staircases the cobble
      edge in ~3 m steps against an 18.2 m street. **Ruling: rectangular regions
      with bounds snapped OUTWARD to the grid.** A grid-aligned rectangle has no
      staircase at all — quantization only bites diagonal and curved bounds — so
      the defect disappears by construction instead of being mitigated. Cost is
      that the plaza becomes a rectangle rather than the premise's r≈12 circle,
      and the street edge lands at z ±9.375 instead of ±9.1, i.e. 0.275 m under
      the facades where it is never seen. Rejected: raising RESOLUTION (pays
      vertices across the whole 400 m mesh to fix a 40 m problem) and exact
      boundary-quad splitting (generator complexity for an edge hidden under a
      wall). Rejected outright: a coplanar cobble slab authored as a dressing prop
      — it passes the lints, and it is a second ground path that z-fights.
      LATENT BUG this change would surface, pre-existing and currently harmless:
      `content_lint.rs:427` does NOT dedup ground dirs across zones (unlike `:534`
      which does), so a `worn_cobble` referenced by both zones double-counts
      against the 1 GB texture budget.
      DOC ERROR CAUGHT, do not inherit it: the layout review
      (`p24-layout-review-2026-07-31.md:251`) claims §3 specifies cobble for
      "plaza, streets and chapel floor". It does not, and never did — §3 scopes
      cobble to plaza and streets, and §6 gives the chapel dressed limestone
      slabs. Independently confirms the premise reconciliation's item I.
      (3) **m5 `plaster_smoked` does not depict smoked encalado** — Concrete035
      reads green-grey mineral-stained concrete at a detail frequency an order
      below the ashlar beside it, and it is the largest low-information surface
      visible through the breach. §3 now gives it an acceptance criterion it
      lacked. Re-source or re-grade before G4.
      (4) **m4 `oak_dark` MEASURED — PASSES, no re-grade.** The recorded S≈0.38
      violation was an albedo-space number and does NOT transfer: the map reads
      S 0.418 while render-space runs 0.17–0.37. Same pattern as m3, same
      direction. V passes by a mile (max 0.22 vs a 0.6 ceiling). S passes on
      every surface as a whole: casa door 0.32 at 2.3 m and 0.21 at 12 m, chapel
      leaves 0.17–0.19, shutter 0.338–0.346. Instrument is sound — two
      independent masks agree to 0.001 on the same region, V-cutoff and
      downsample sweeps move S by ≤0.011.
      **TWO CORRECTIONS TO MY OWN BRIEF, both mine, neither the worker's:**
      (a) I asserted oak sits outside the reserved threat window at hue 27°. It
      does not — rendered hue is 19°–27°, so MOST oak surfaces render INSIDE
      350°–25° (chroma-weighted means match unweighted to 0.4°, so this is not
      low-V hue noise). Verdict unchanged, because the band is a conjunction
      needing S≥0.7 ∧ V≥0.8 and the in-window sub-ceiling is the same S 0.35 just
      measured — but the premise must never cite oak's hue as 27°.
      (b) The real defect was in the clause I had just committed: **"rendered
      mean" never said mean of WHAT.** The shutter reads 0.338 as a whole
      surface, 0.340 across its rows, and 0.355–0.367 on one clean pane — pass or
      fail purely by choice of crop. That is the subject-definition free parameter
      from `the-instrument-cannot-grade-itself`, shipped by me into a spec clause.
      Fixed at `144a2c9`: the subject is one whole bound surface (one material,
      one authored face group) at the 2.3 m walk-up range, never a crop, never a
      pane, never an albedo map. Saturation falls with distance, so the walk-up
      range binds and anything passing there passes down the street.
      **RE-GRADE REJECTED, and the reason is a real tradeoff, not thrift.**
      Buying margin would need render-space S down ≈0.03 on the shutter (≈9%
      chroma, albedo 0.418→0.38). But the standing m4/m6 finding is that oak and
      wrought iron already MERGE at street distance (Δlum 0.006, confirmed worse
      at the G2 re-gate), and their separation now "rests on warm/cool hue +
      silhouette only". Desaturating oak attacks precisely the chroma carrying
      that separation. Trading a confirmed silhouette-legibility defect for
      margin against a ceiling the surface already meets is a bad trade.
      2.3 m is the closest oak that exists on disk; no macro frame lands on oak.
      The trend implies a 0.6 m read sits higher, but macro is a texel-reading
      tool, not a gameplay framing, so it does not bind.
      (5) exterior rubble (P3.0 fix 8) and (6) `wall_segment` striping are already
      logged above as blocked/KIT DEBT.
- [x] P3.1 CONCEPT LIST AUTHORED: `tasks/town/p31-c1-concepts.md` (opus).
      Slots: C1 ruined arch (H1) · C2/C3 retablo silhouettes A/B (H3) ·
      C4 wayside shrine PILLAR, re-scoped (H4) · C5 ox cart, solid disc wheels
      (H6) · C6/C7 votive stand tall-pricket vs low-tiered rack (H7) ·
      C8 gate brazier, lit (replaces H5).
      **THREE CHAINS CANCELLED, all three the P3.0 ruling firing again.**
      H2 fountain: there is no fountain in Rocalba — §4/§5 give a well basin,
      already kit and shipped; "fountain" is plan-era wording that predates the
      premise. H5 gate doors: planks + ledges + straps is the plain-repeated-form
      case, it must mate to the kit `gate_arch` jamb, and §5 rules the gates OPEN
      so both leaves are seen edge-on; slot re-spent on the porter's brazier,
      which the premise names twice and nothing implements. H6 barrel/crate: a
      barrel is a lathe of revolution placed in multiples (generation gives one
      lumpy instance instanced N times) and a crate is six boards AND an
      anachronism for 1490s Castile; the cart survives.
      Budget: 22 chain candidates ≈ 3.1 h vs the approved 30 / 5.5 h —
      **~2.4 h released.** RULED: bank it. Spending a reserve before G3 says
      which class is weakest is strictly worse than spending it after.
      TWO PIPELINE FINDINGS, both material:
      (i) **There is no negative-prompt channel** — node 5 is a
      `ConditioningZeroOut` of the positive and sampling is at cfg 1.0. Every
      exclusion must be carried by affirmative wording plus the screening
      criterion. Sharpest on C8: a lit brazier is the one subject a model will
      render straight into the reserved threat band.
      (ii) **The 77-token limit does NOT bind these prompts.** That was
      `gen_material.py`'s SDXL path (`todo.md:163`); the concept and multiview
      workflows encode with Qwen3-4B and have no cap. I had already committed a
      premise §7 rewrite citing that limit as its rationale — FALSIFIED and fixed
      at `f245f34`. The clause's conclusion survives on a better reason (a prompt
      carries only what reaches the image); the reason it shipped with was a fact
      inherited from the campaign log and never checked. Instance of
      `get-the-fact-before-planning-around-it`, on me, not a worker.
      (iii) Do NOT dispatch C1 through `gen_prop.py` — `stage_concept` opens a
      fresh ComfyUI server per seed (64 cold loads blows the budget alone) and
      `--asset` refuses the five unregistered subjects. One resident server, 64
      `comfy_run.run_workflow` submits.
      Open, ruled by orchestrator: votive-stand form stays TWO slots (C6 screens
      thin-iron feasibility, which decides whether H7 runs at all — that is not a
      taste question); C4-vs-crucero/gravestone crowding is a layout call, taken
      at screening; period dressing to replace the crate (sacks/panniers) is not
      slotted, but C5's cart carries a sack load so the screen shows it free.
- [x] P3.1 RUN-C1 EXECUTED — 64/64 images on disk, verified by directory count
      not by exit code (8 per slot C1-C8, sizes 833 KB–1.47 MB, no degenerate
      frames). **~11 min wall, not 35** — the plan's 8.5 min/candidate figure is
      the full Hi3DGen chain, not a concept image; Turbo sampling at 8 steps is
      far cheaper. ~24 min of the approved budget unspent on top of the ~2.4 h
      released by the chain cancellations.
      Dispatch worked as specified: ONE resident ComfyUI server across four
      foreground chunks of 16 submits (server backgrounded as a service, submits
      foreground under the 10-min shell ceiling, reachability checked per chunk).
      Operating point untouched — steps 8, cfg 1.0, res_multistep/simple, shift
      3.0, 1024², `ConditioningZeroOut` on positive; only the subject string and
      seed varied. All 8 prompts verbatim from the spec, none altered, zero
      failures. Premise citation in the manifest, not the prompt (§7 clause 1).
      Output `target/concept-c1/<slot>/seed_<n>/concept.png` + aggregate manifest.
- [x] P3.1b OPUS SCREEN DONE — record
      `docs/reviews/town/c1-concept-screen-2026-08-01.md`, all 64 opened, colour
      claims measured over background-masked objects.
      C1 FAIL (prompt-fixable) · C2 FAIL (structural) · **C3 PASS** seed 1 ·
      C4 PASS-WITH-PROMPT-FIX · C5 FAIL (prompt-fixable, low confidence) ·
      **C6 PASS** seed 4 · C7 FAIL (structural) · **C8 PASS** seed 8.
      THE THREE ANSWERS IT EXISTED TO PRODUCE:
      (1) **The C8 threat-band hazard did not fire.** Flame median hue 33.5–38.7°,
      p95 42–54°, S 0.34–0.37, V 0.97 — candle-gold. Full threat-band pixels 0–49
      out of ~650 k; iron body mean S 0.045–0.067. The brazier ships LIT. Its real
      defect is the basket: solid bowl in 7/8, true openwork only in seed 8.
      (2) **Thin iron is FEASIBLE** — C6's slender post is one crisp continuous
      member in 8/8, tripod legs three distinct bars in 8/8, no melt or blob.
      H7 RUNS, on silhouette A. C7 inverted its own hypothesis (members thinner
      than C6's post in 8/8, under the 3 cm floor) → cancelled.
      (3) **Retablo: C3 outright.** C2 returned a modern picture frame with a
      naive landscape triptych in 8/8, including a 20th-century car in seed 4.
      C3 returned a true three-bay oak retablo with a deep empty niche in 8/8.
      **THE FINDING THAT CHANGES A GPU SPEND: C1's melted carving did NOT
      reproduce** — U6 passes 8/8. The campaign believed the shipped arch's melt
      originated in the concept stage, and RUN-H1's 34 min is budgeted on that
      belief. If the melt is downstream, a concept re-roll cannot fix it.
      ATTRIBUTION PROBE DISPATCHED before spending H1 — rule from artifacts on
      disk, not from the campaign log's prose about itself, since the log is what
      is in doubt. C1's actual failure is marble (`dressed`/`ashlar`/`voussoirs`
      is the attractor) plus moulded plinths instead of broken stumps.
      C5 lost on one adjective — 8/8 spoked wheels against an explicit "solid
      disc". RULED: re-roll once with stronger wording, and **if it fails again,
      ACCEPT spoked wheels.** The reason the spec mandated solid discs was thin-
      geometry risk, and C6 just falsified that risk outright; spoked wheels are
      period-plausible for 1490s Castile. A constraint whose justification has
      been measured away is not a constraint.
      COLOUR LAW: no threat-band clusters anywhere (max 85 px = 0.012%). Real
      finding is sub-region over-cap — C4's candle-lit recess interior hue 23–25°
      at S 0.60–0.65, non-emissive stone over the in-window S 0.35; same pattern
      in C8 rust and C5 timber. Whole-surface means pass everywhere.
      TWO RUBRIC DEFECTS the judge raised against ITSELF, both real:
      (i) U1 as written ("no cast-shadow floor") fails ~40 of 64 on studio
      lighting and goes vacuous — must read *no floor geometry continuous with
      the object*. Fix in the spec.
      (ii) §2's S ≤ 0.35 is defined on a whole surface under ship lighting at the
      walk-up range, which **a concept PNG cannot supply** — so the colour law
      does not bind concepts at all, by construction of the clause committed at
      `144a2c9`. The judge reported both whole-object and sub-region numbers
      rather than silently picking one, which was right. Concepts are screened for
      material identity and form; compliance is measured on shipped surfaces.
      Do not re-apply the ceiling to concept images.
- [x] **RUN-H1 CANCELLED — its premise is REFUTED BY ARTIFACT.** The shipped
      arch's melted carving does NOT come from the concept stage. Probe verdict
      (b) downstream, full hash-linked chain recovered on disk, shipped GLB proven
      byte-identical to `clean.glb`.
      Concept is CRISP: high-pass RMS 0.0494, exactly the median of the fresh C1
      grid (0.0443–0.0532). Concept→yoso normal preserves everything. Hi3DGen
      reconstruction preserves everything. **Decimation 773,704 → 14,999 tri is
      where it dies**, and the signature is precise: orthographic depth band-pass
      residuals show **amplitude unchanged at every scale while structure below
      ~3 cm goes uncorrelated** — Pearson 0.343 at σ≈8 mm, 0.585 at 17 mm, 0.764
      at 34 mm, 0.940 at 135 mm. The carving is not attenuated, it is REPLACED by
      equal-amplitude faceting noise. That is what "melted stone" is. Ranking and
      scale-dependence stable under a 1024→2048 refinement, no crossing.
      ROOT CAUSE: `assets.json` hand-sets `tri_budget` per asset with **no scaling
      by size**. chapel_arch gets 14,000 tri at 5.50 m = 110 tri/m² over 136.7 m²,
      a **14.5 cm mean triangle edge** against 1–5 cm relief — by far the lowest
      triangle density of the seven generated props, while `olive_stump` gets
      20,500 at 1.2 m and `broken_column` 12,000 at 1.4 m.
      Releases H1's 34 GPU-min. The fix needs NO concept and NO Hi3DGen run —
      `raw.glb` and `clean_hires.glb` are both on disk, so it is a CPU re-run of
      `prop_cleanup.py` at a size-appropriate budget plus a retexture (the only
      GPU cost). Second fix: derive `tri_budget` from surface area, because this
      recurs on every large prop.
      Caveat recorded by the probe against its own grid: the new C1 concepts pass
      the crispness criterion partly because they contain almost NO carving —
      plain marble panels, no ornament. U6 is a weak test on that grid either way.
- [x] **DECIMATION-AS-ROOT-CAUSE STUDY DONE — REFUTED as the campaign's
      stone-read deficit.** Record: docs/reviews/town/
      decimation-attribution-2026-08-01.md. Decimation loses <=0.4% of the
      60-124 mm band on every prop; the blind-test winner is the coarsest
      mesh in the study; rank correlation runs the wrong way (-0.80 vs
      direct damage). Survives only as chapel_arch's 4-17 mm melted-carving
      defect (retess ~171k tris prescribed, GPU-perf-probe gated). Follow-up
      probe docs/reviews/town/albedo-band-table-2026-08-01.md then killed
      the 60-124 mm figure itself (mislabelled denominator, 14-26x off on
      the control); best surviving predictor is beauty/albedo gain G
      (rho -0.90) - a material-response lead, not geometry. NOTE record
      integrity: that band-table file is incomplete on disk (s6 is a
      literal SWEEP_TABLE placeholder, s7 cuts mid-sentence; verdict s1-s5
      complete; sweep JSONs lost with the session scratchpad - flagged,
      not re-run). Next phase plan: ~/.claude/plans/
      glittery-chasing-rossum.md (approved 2026-08-05: cobble choice, GPU
      probe, retess + surface-area tri_budget, H chains approved in-phase,
      kit-bevel probe-then-decide).
      Original hypothesis text, kept for the record: this
      is not one prop but the campaign's central unresolved defect. The blind test
      that beat the whole texture-detail campaign left a **residual deficit at
      60–124 mm**, two orders above the millimetre grain band the texel arithmetic
      had named, and never explained. **A 14.5 cm mean triangle edge lands inside
      that band.** If it holds, "generated props don't read as stone" is
      substantially GEOMETRIC under-tessellation, not texture — and `blend_views`
      1/√N attenuation is another real-faithful-irrelevant mechanism, which is
      exactly the failure `a-visible-mechanism-is-not-an-attributed-one` records.
      Agent is told to try to REFUTE it: per-prop mean triangle edge must predict
      per-prop perceptual deficit across the set, the statistic must be able to
      come out zero, and the photoscan control's own tessellation must be checked
      — if the control is also coarse and still wins, the hypothesis dies.
- [x] S2 GPU PERF PROBE DONE — GATE PASS 2026-08-05. Record: docs/reviews/
      rendering/gpu-frame-baseline-2026-08-05.md (+ logs zip alongside).
      First GPU timing record of this renderer: RTX 3080 Ti, 1920x1080,
      release sandbox, ~45 s x3 configs. Geometry-isolated delta
      (bare171k - bare15k, same rig placement): frame_ms +0.011 (gate
      <=1.0), absolute median 1.738 ms (gate <=14) - PASS both. Attribution:
      the 11x tri swap reads only in shadow_ms (+0.014, 3 cascades);
      main_ms within noise. Rig: chapel_arch temp-placed 20 m from spawn
      (frustum-proved Visibility::Both), zones.ron + glb swaps reverted,
      verified clean. Instrumentation (frame bracket + VORDAR_GPU_LOG, plus
      TIMESTAMP_QUERY_INSIDE_ENCODERS device request found necessary
      mid-capture) landing as its own commit. UNBLOCKS S3 retess chain.
- [ ] S3 RETESS — CODE SHIPPED `466edb7`, FIRST INSTALL FAILED JUDGE,
      ARCH REVERTED TO 15k, ITERATION OPEN. 2026-08-05 chain of findings:
      (1) Formula derives 103,068 tris at 40 mm (not the pre-registered
      ~171k) because the interior-face strip (`1f32bbe`/`323c55c`,
      post-dates every arch build) removes 38% of raw area: real
      post-strip area 82.455 m² vs the study's 136.7 m² (measured on
      stale pre-strip shipped bytes). Adjudicated: 40 mm footprint is the
      goal, 103k accepted (decided-while-unsure). Decimation conserves
      area 99.94%; mean edge 47.86 mm in-band. Also shipped in `466edb7`:
      `--max-tris` clamp + gen_character passes 30000 (silent-fallback
      fix; character budget was file-size/joint-capped, not footprint).
      (2) Fresh chain ran (cand at `target/arch-retess/cand_fresh/
      cand_0/`), installed, judged old-vs-new on matched macro frames —
      **FAIL** (5/9/3/5): (a) texture roll ghosted — surface-locked baked
      shading + painted arcade silhouette in albedo, atlas p95/p5 7.55×
      vs 3.42× photoscan ref (old arch albedo clean at 1.3–1.4×, so a
      clean roll is achievable → seed re-roll is the fix path);
      (b) judge's "defect dead at 4–17 mm" criterion was over-strict —
      study §8 itself priced 20 mm at ~683k and chose 40 mm; measured
      band gains 8–17 mm 2.36×, 17–40 mm 2.62× = the prescribed 1–5 cm
      carving band improved as designed; 4–8 mm is normal-map territory
      at any sane budget. Install REVERTED (arch back at shipped 15k).
      (3) Judge side-finding: `prop_audit.py --asset chapel_arch` errors
      on the retess UVs (stale cached coverage artifact
      `target/prop-coverage/holes_chapel_arch.png`) — regen needed at
      next install. (4) Normal-map provenance SETTLED: the shipped
      normal IS a true hires Cycles bake (`proptex/export.py:49-71`) in
      both builds — geometry accepted at 103k, round 2 is texture-only.
      (5) ROUND-2 RE-ROLL FAILED PRE-SCREEN, all 3 seeds (island-masked
      albedo p95/p5: old shipped arch **1.78× / 0.23%** dark-frac;
      new-mesh seeds 0/1/2/3 = 10.88/8.32/7.76/6.23× with 14–20%
      dark-frac; gate ≤4.0× & ≤6.5%). Four consecutive ghosted rolls =
      mechanism defect (blend has no color-consistency/outlier
      rejection — `proptex/albedo.py:113-128`: disagreeing views
      average, never compete), not seed luck. Nothing installed. Metric
      script: `target/arch-retess/pre_screen.py`; rolls at
      `target/arch-retess/cand_reroll_s{1,2,3}/`.
      (6) S5 H CHAINS: held 2026-08-05 am on the ghost risk; **UNHELD
      same day by the estimator-probe verdict** under a per-roll
      pre-screen protocol — every texture roll pre-screened
      (pre_screen.py, ≤4.0×/≤6.5%) before bake/judge spend, ≤3 seeds
      per prop, 3 failures = prop reported blocked, never shipped
      (decided-while-unsure; worst-case overhead ≈ +45 min GPU).
      (7) ATTRIBUTION DONE (record: `docs/reviews/props/
      albedo-ghost-attribution-2026-08-05.md` + pre_screen.py alongside):
      ghost is campaign-wide, mechanism not seed/mesh — shipped set maps
      olive_stump 7.34×/11.1%, candelabra_shrine 8.62×/11.7% (ghost-
      class) vs photoscan truth ≤3.10×; today's pipeline on July's 15k
      arch = 4.52×/7.2% (between eras, seed-confounded n=1).
      (8) HISTORY RECOVERED (prop-texture-redesign.md rows 43-45):
      hwta (consensus-LF@14mm + 28mm gain-ratio + winner-HF) judged
      "confirmed as an improvement and refuted as a solution" (2.5→4,
      worth building, never built, scratch code lost); plain wta
      REJECTED (seam excess 3.28 vs 1.45 floor) — rejected comparator,
      successors must not match it. Ghost charge ≠ the stone-read charge
      hwta failed on: ghost lives largely in LF, where hwta's mean-
      consensus would keep averaging it in → median-LF variant added to
      the probe. Constraints honored: coverage gate untouchable
      (quality-over-cost), CoverageFailure must keep refusing to build,
      no-regression rule vs incumbent on every prop.
      (9) ESTIMATOR PROBE DONE — **no variant clears on any candidate;
      blend-side fix class CLOSED** (record + reblend.py + report.json:
      `docs/reviews/props/blend-estimator-probe-2026-08-05.md`; live
      outputs `target/blend-probe/`). Harness reproduced the shipped
      estimator to MAD 3e-5/255 on all 5 candidates, then mean/hwta/
      med-hwta moved the ghost metric <10% (slightly worse). A weighted
      MEDIAN removing nothing ⇒ the views AGREE on the painted shading
      ⇒ ghost enters at GENERATION, not blend — attribution finding 3
      refuted as the lever. Fix class 4 (texture-native 3D-consistent
      generator, licensing-gated) confirmed as root-cause successor;
      licensing research dispatched.
      (10) ROUND 3 REDIRECTED: transfer the shipped judge-clean albedo
      (1.78×) onto the accepted 103k geometry via UV resample (normal
      stays the candidate's hires bake; honest manifest or STOP), then
      pre-screen → renders → fresh Opus judge (8–40 mm band ≥ old,
      studio read ≥ old, silhouette held, no transfer artifacts) →
      install+commit on PASS. No more generation rolls for the arch
      (4 consecutive failures, floor 6.23×).
      (11) TRANSFER EXECUTED (Cycles CPU EMIT selected-to-active bake,
      15k shipped clean.glb → 103k atlas UVs, params from export.py's
      own constants): pre-screen **1.61× / 0.34%** — clears the gate,
      tighter than the shipped anchor. Deliverables at
      `target/arch-retess/cand_transfer/` (textured.glb,
      transfer_manifest.json, transfer_albedo.py, bake log); renders at
      `renders_round3/`. Shipped maps enumerated: albedo+normal+AO;
      roughness/metallic are glTF SCALAR factors from surface_classes
      limestone (no map to re-derive). Two walls surfaced honestly:
      (a) cand_0 top-level normal.png is STALE (dir-reuse leftover, 87%
      off the manifest's bake) — correct files taken from
      prop-cache/bake_{normal,ao} and verified byte-identical to
      textured.glb's embedded images (instrument caveat: NEVER trust
      top-level cand files over manifest-hashed cache entries);
      (b) install_asset.py requires a content-addressed texture.stages
      chain — no `transfer` stage type exists, so the manifest is
      deliberately NOT install-compatible (no forged records); a real
      `transfer` stage in proptex/ is the honest path, to be built
      only after judge PASS. SEAM FIXED AT ROOT (bake input, not
      output): 76% of bright texels sampled the SHIPPED bake's own
      8px margin-dilation band as if it were content —
      `clean_source_margin.py` erodes each shipped chart to trusted
      interior (depth-capped so thin charts keep pixels) and refills
      before the transfer bake reads it. Ray-miss/wrong-hit ruled out
      by experiment (0% position error). Bright texels 1296→37
      (residual = sliver-triangle UV artifact in the 103k unwrap's
      own charts, genuine content repeated, faint in studio macro_02
      only); pre-screen 1.608×/0.40%. All 8 frames re-rendered.
      JUDGE ROUND 3 DISPATCHED (fresh Opus, renders_old vs
      renders_round3, re-anchored gate: 8–40 mm band ≥ old /
      light-dependence / studio read / silhouette / artifact
      visibility ruling on the 37-texel residual).
      ROUND 3 VERDICT: FAIL, AXIS 5 ONLY — record
      `docs/reviews/town/arch-retess-round3-2026-08-05.md`. Axes 1–4
      PASS (relief ≥ old every band on the shading-isolated
      instrument; ghost dead; studio read matched, HF energy UP;
      silhouette IoU 0.995+). Blocker: undocumented ~2500–3200 px
      chalky desaturated albedo patch, macro_02 top edge (Weber
      +0.55 studio / +1.38 raking, half surround chroma,
      surface-locked) — NOT in the worker's 37-texel accounting;
      manifest's "not visible in raking" claim on the documented
      residual REFUTED (+0.34 raking). Also: macro_01/03 are EMPTY
      frames (macro aim point in the arch void at those yaws) — 4
      informative frames per set, note for any macro-rig work.
      Instrument lesson recorded in memory (percentile gate blind to
      localized patch; fix's own diagnostic can't do the residual
      accounting). ROUND 4, corrected flow after USER CORRECTION
      (2026-08-05): my first dispatch bundled diagnose+implement in
      one opus agent — killed. Rule recorded in orchestration-model
      memory: thinking (investigation/plan/audit/root-cause) and
      implementation NEVER share a dispatch; all thinking runs on
      the fable tier except visual judging (opus); implementation
      model scales with difficulty. Killed worker left only diag
      scripts (frame_to_atlas.py, diag_hit_uv.py, uv_raster.py,
      diag/) + unverified note "wrong-surface hits, not margin
      filler". DIAGNOSIS DELIVERED (fable tier) — record
      `docs/reviews/town/arch-transfer-diagnosis-2026-08-05.md`.
      TWO mechanisms, both reproduced: CLASS C (chalky patch + y828
      groove) = wrong-surface ray hits — max_ray heuristic 0.4%·diag
      = 41.5mm exceeds 23–32mm wall gaps while cage 10mm < local
      deviation 10.5–15.3mm; cage 15mm snaps all probed texels
      correct; 7,833 texels/1,185 clusters full-atlas. CLASS A
      (y505–525 dashes) = the seam fix's OWN 8px erosion falsified
      54% of source island; thin charts flood-refilled flat; 186k
      texels rewritten. Manifest known_residual MISATTRIBUTED (its
      cluster invisible in macro_02; the y828 artifact was class C).
      Prior worker's note half right. IMPLEMENTATION DISPATCHED
      SEPARATELY (opus, constrained to the prescription): keep-island
      source cleaning (≤2px rim only), cage sweep {15,20,25} gated on
      the diag/s8 detector (red-proofed, correspondence-based,
      independent of the tuned parameter), max_ray = cage+15mm, final
      bake, honest manifest rewrite, renders_round4. Then round-4
      judge: axes 2/3/5; axes 1/4 stand (geometry sha unchanged).
      (12) LICENSING BRIEF DELIVERED: `docs/reviews/props/
      texgen-licensing-brief-2026-08-05.md`. Headlines FOR THE USER:
      Tencent Hunyuan licenses EXCLUDE THE EU from the grant territory
      (2.0+2.1 verbatim) — quality leader unusable here; the standing
      "TRELLIS = NC" ruling may actually be "nvdiffrast = NC" (TRELLIS
      weights are MIT; Hi3DGen itself is a TRELLIS derivative that
      stripped the NVIDIA deps) — needs user re-read, would unblock
      TRELLIS.2 (top shortlist, outcome 8/10 conf 5/10); permissive
      shortlist TRELLIS.2 / Material Anything / MVPainter; named cheap
      probe before any adoption: two-opposed-light albedo differencing
      on one prop. NO adoption decided — licensing is the user's call.
      (13) S5 EXECUTION STARTED under the (6) protocol: H3 retablo
      chain dispatched (C3 seed 1, derived budget, per-roll
      pre-screen ≤3 seeds). H4/H6/H7/brazier queue behind it.
      (14) H3 RETABLO BLOCKED per protocol — 3/3 seeds fail pre-screen
      (p95/p5 | dark-frac vs gate ≤4.0× AND ≤6.5%): seed 1 6.63×/6.92%,
      seed 2 5.95×/7.95%, seed 3 4.93×/6.17% (ratio-only fail). Trend
      monotonic toward the gate but not through it. Derived budget
      60,879 tris (48.70 m² @ 40 mm). Candidates kept at
      `target/prop-batch/h3-retablo/cand_{1,2,3}`; blend atlases in
      `target/prop-cache/blend/{40ce92d2,e0cadb4c,d7dcbc25}…`.
      USER DECISION QUEUED: concept-level re-roll for retablo, or
      accept blocked until the texgen successor lands (the ghost enters
      at generation — more seeds of the same class are unlikely to be
      the lever; trend says close, mechanism says no).
      DECIDED WHILE UNSURE (m): reverted the uncommitted retablo
      assets.json entry — blocked prop, keeps the tree clean for the
      arch install commit. Recreate verbatim when unblocked:
      `"retablo": { "kind": "generated", "subject": "small poor parish
      altarpiece, three-bay dark oak frame, shallow empty central niche
      flanked by flat painted panels, plain low pediment above, thin
      gilt beading catching warm candle-gold, dark oak, deep near-black
      brown, silvered light-grey weathering on raised grain, modest
      village work", "height_m": 3.0, "surface_class": "oak_dark",
      "texture_size": 2048, "view_res": 1536 }` (alphabetical, between
      reja_set and rock_07; no tri_budget — derived).
      (15) LATENT EXPORT BUG exposed by H3 (blocks H6 cart identically):
      `proptex/export.py:_validate_export` reads absent MR factor keys
      as None instead of the glTF 2.0 spec default (Blender's exporter
      omits factors equal to 1.0; oak_dark roughness=1.0 is the first
      generated-path class to hit it). FIXED + COMMITTED `21ebf7a`
      (spec-default fallback, 3-case red-proof: absent+default PASS,
      absent+nondefault FAIL, present-mismatch FAIL).
      (16) H4 SHRINE_PILLAR BLOCKED per protocol — 3/3 rolls fail
      (p95/p5 | dark-frac): s203 3.58×/8.67%, s501 3.59×/8.60% (both
      dark-frac ONLY), s777 5.04×/12.95%. Derived budget 6,269 tris
      (5.02 m² @ 40 mm). Cands `target/prop-batch/h4-shrine/
      cand_{203,501,777}`; blend keys 8b33c8c2/0e572917/ceed2f6e.
      Concept sha dab771fc…. shrine_pillar assets.json entry
      REVERTED (same rationale as retablo); recreate verbatim:
      `"shrine_pillar": { "kind": "generated", "subject":
      "freestanding wayside shrine pillar, plain square stone post
      with a deep hooded recess near the top, flat slab hood, one lit
      white wax candle standing inside the recess, warm candle-gold
      flame, pale grey dressed limestone ashlar, cool light grey with
      faint sandy flecks, matte, thin dark-grey soot in the recess,
      undecorated", "height_m": 2.0, "surface_class": "limestone",
      "texture_size": 2048, "view_res": 1536 }` (between rock_face_01
      and wall_segment). OPEN QUESTION flagged: this subject SPECS
      dark content (soot in recess) — a dark-frac gate may never pass
      it; era-probe agent assesses.
      (17) S5 QUEUE RE-HELD (decided while unsure, n): the unhold
      premise ("defect is roll-dependent; July rolled 4/6 clean")
      is refuted by S5's own data — today's rolls are 0/11 (arch
      s0-s3 + s7, retablo ×3, shrine ×3) vs July's 4/6 props.
      H6 cart / H7 votive / brazier NOT dispatched (~75 min GPU
      withheld; would likely reconfirm the pattern, not break it).
      ERA-ATTRIBUTION INVESTIGATION DISPATCHED (fable tier,
      findings-only): separate code/config era vs model weights vs
      prop identity vs seed luck; git log of scripts/ai-pipeline
      since July ship; shipped-manifest param/cache-key diff (CPU
      discriminator); authorized ≤2 bounded GPU probe runs, canonical
      = today's pipeline on July's exact arch inputs at seed 0,
      texel-diffed against shipped base. Queue resumes (or reroutes)
      on its finding.
      Renders: `target/arch-retess/renders_{old,new}/`. Red-proof v2 log:
      `target/arch-retess/red_proof_shipped_v2.log`.
- [x] S4 BATCH GATE PASS 2026-08-05: `cargo test --workspace` 457 passed /
      0 failed / 5 ignored (51 binaries) in one run over the committed
      batch `abb9619`+`f154d2e`+`45bab1d`+`466edb7`; no fixes needed, so
      the confirm run was not required.
- [x] P3.1c RE-ROLL EXECUTED — 32/32 on disk at `target/concept-c1b/`, ~10 min,
      seeds 101-108/201-208/301-308/401-408 (distinct from run 1, so this is a
      genuine re-roll and not a re-render), all prompts verbatim from the screen
      record §4, operating point untouched, `target/concept-c1/` preserved intact
      as the evidence behind a written review. Screen of C4/C5/C8 in flight.
      **ORCHESTRATION ERROR, mine: I dispatched this re-roll in parallel with the
      attribution probe that was explicitly gating H1.** C1's 8 images are moot —
      the arch's fix is re-decimating geometry already on disk, not a new concept,
      and no concept re-roll could have changed that. ~2.5 GPU-min wasted. The
      probe was dispatched *because* a spend hung on its answer; work depending on
      that answer had to sit behind it, and parallelism being cheap is not a
      reason to run a gated task alongside its own gate. → lessons at the gate.
- [x] RE-ROLL SCREEN DONE (record §7-§12 appended, §1-§6 byte-preserved).
      **C4 PASS, improved — winner seed 203.** Crop fixed 8/8 (original bottom
      margin was 2 px in ALL eight; re-roll 18-41 px). The recess colour finding
      resolved BY HUE not by saturation: 23-25° → 30-38°, so it left the reserved
      window and the in-window S cap stopped binding; zero threat-band pixels in
      all 8, against up to 85 before. Recess Weber contrast 0.17-0.44, flat across
      a 4× resolution sweep, reads at 2 m and 28 m. Residual: 203 is the ONLY
      limestone read in either grid — 6/8 speckled conglomerate, 204/208 marble-
      adjacent crystalline white (a §3 exclusion), 202/205 grew pagoda eaves.
      **C8 PASS, improved — winner seed 407** (alt 406, zero threat px). Genuine
      openwork 7/8 against 1/8; describing the lattice as construction worked.
      Flame colour re-confirmed on the new grid: hue 34.1-41.6°, S 0.31-0.44,
      threat px ≤0.10%. Ornament gone entirely.
      **C5 FAIL — a REGRESSION, and the revised prompt caused it.** Spoked 8/8
      again (informational under the standing ruling), but the new wording turned
      the timber into charred glossy shou-sugi-ban pine, the draught pole into a
      machined steel tube in 5/8, and seed 308 has **pneumatic tread tyres**. Net
      read: 20th-century farm trailer. **REVERT to `concept-c1/C5/seed_6`** (alt
      3) — under the spoked-wheel ruling the ORIGINAL grid already passes on cart
      quality, so H6 proceeds with no third run.
      Worth keeping: the C5 failure was **invisible to the rubric** — timber hue
      24-29°, S 0.40-0.45, zero threat px, statistically identical between grids.
      A colour-clean concept can still be off-period. Rubrics that measure only
      what is easy to measure will pass a farm trailer.
      **INDEPENDENT CORROBORATION OF THE DECIMATION FINDING:** the judge measured
      C8's openwork bars at **16-25 mm** at the stated 1.0 m height, then scaled
      the arch probe's own figure (14.5 cm mean edge at 14,999 tri on 5.5 m, edge
      ∝ L/√N) to **~3.9 cm mean edge at 1.0 m / 7,000 tri — wider than the bars.**
      The brazier's cage would melt exactly as the arch's carving did. That is a
      PREDICTION made from the decimation model by an agent that was not testing
      it, on a different prop, before any chain ran.
      → **RUN-H CHAINS ARE NOW BLOCKED ON THE TRI_BUDGET FIX.** Running them
      first would spend ~3.1 h producing props whose fine geometry is destroyed on
      the way out, and C8 is the proof it would happen. Correct order: settle the
      decimation study, derive tri_budget from surface area, re-decimate
      chapel_arch from the on-disk `raw.glb` and verify the fix visually, THEN run
      chains at correct budgets.
      UNSETTLED, carried: whether a three-quarter concept costs anything
      downstream — `prop_hi3dgen.py` reconstructs in the image's own camera frame
      while retexture calls view 0 "front". Every carried concept this campaign is
      3/4-ish so it is not specific to C4 203, but it is unverified; seed 201 is
      the frontal fallback.
- [ ] (superseded) P3.1c Concept re-rolls: C1 (marble attractor +
      broken stumps), C4 (all 8 cropped by the frame edge — a cropped concept
      extracts a cropped prop), C5 (solid disc, one attempt), C8 (openwork
      basket). Revised prompts in the screen record §4. HOLD until the ground
      worker's evidence render frees the card.
- [ ] (superseded) Opus screen of the 8×8 grid → record at
      `docs/reviews/town/c1-concept-screen-2026-08-01.md`. Judge told to open all
      64, to separate **prompt-fixable drift from structurally hopeless subjects**
      (there is no negative channel, so forbidden things WILL appear and that is
      generator behaviour, not proof a subject is dead), and to measure the C8
      brazier against the reserved threat band rather than eyeball it. C6 carries
      the thin-iron feasibility answer that decides whether H7 runs at all.
- [x] GROUND REGIONS IMPLEMENTED (uncommitted, diff verified on disk: 10 files,
      +263/−64). No wall hit — the ruled design held exactly, and the
      investigation's "zero engine or shader change" premise was correct.
      `GroundDef.regions: Vec<GroundRegion>`; `generate_ground` assigns quads by
      centre to grid-snapped rectangles, last match wins; **empty regions falls
      through to the untouched single-primitive path**, so every no-region zone is
      byte-identical to before. Region bounds were DERIVED, not invented: facade
      z came from `footprints.ron`'s measured casa depths against each row's
      placed centre-z, and all four house types independently give z = ±9.2 →
      snapped to ±9.375; X from casa_corner's composite AABB rotated per yaw,
      spans [−19.35, 13.95] → snapped to [−21.875, 15.625]. Plaza (±12.5, ±12.5),
      listed after the street so it wins the overlap.
      Latent bug FIXED as scoped: `total_texture_memory_within_budget` now dedups
      ground dirs across zones via a HashSet, so `worn_cobble` shared by `east`
      and `start` counts once against the 1 GB budget.
      Two new `ROCALBA_SHOTS` — `plaza` and `street` — because no existing named
      shot showed the ground being changed. content_lint 19/19, server zones 6/6,
      client ground 6/6. Opus visual gate IN FLIGHT; the load-bearing claim it
      must falsify or confirm is that a grid-snapped rectangle produces NO
      staircase at the boundary.
- [x] GROUND GATE: **PASS WITH FIXES** (boundary 4/5, extent 2/5, material 2/5,
      improvement 3/5). Record `docs/reviews/town/ground-regions-2026-08-01.md`.
      **THE RULING SURVIVED CONTACT.** Grid-snapped rectangles produce NO
      staircase: the plaza west edge fits a straight line at **0.488 px RMS** over
      81 sampled rows, and every apparent step is the single plaza/street union
      corner — two straight runs meeting at 90°. UV continuity holds in pixels as
      well as in code, no phase or scale jump at any seam. The 0.275 m
      under-facade claim is true; cobble meets the wall base cleanly along the
      whole north row. No regressions: 13 of 28 named shots byte-identical, only
      frames standing on the new regions moved.
      **THE MECHANISM IS RIGHT AND THE MATERIAL IS WRONG** — three measured
      failures, none fixable by tuning `tile`:
      (1) stones render **2.17 m across** (107 px joint spacing against a 345 px =
      7.0 m tile period) where the asset's own prompt asked "fist-sized"; the
      texture holds only ~3×3 stones, so scaling down shrinks the motif and
      worsens repeat. (2) **joints are INVERTED** — brightest, most neutral part
      of the surface (V 0.537, S 0.016) where §3 mandates "dark earth-brown
      packed"; confirmed in the source albedo, so it is the asset. (3) renders at
      **hue 223°, S 0.10** — as chromatic as the dressed limestone, so §2's warm
      20°–50° bias binds and it sits ~200° outside; near-neutral albedo (S 0.013)
      takes the cool sky straight while cracked_earth's warm albedo resists.
      Repeat also worsened, autocorrelation 0.400 → 0.585 in the far band.
      Root cause is provenance: `worn_cobble` was sourced for the EAST zone, a
      paved square where large slabs are defensible. A village street is not that.
      §2's numeric ceiling passes comfortably at the binding 2.3 m range
      (S 0.082, V 0.462) — this is a spec-identity failure, not a colour-law one.
      HONEST IMPROVEMENT ANSWER: yes structurally — the street finally has a floor
      and the row stops reading as a film set in a desert — but the new floor is
      blue under terracotta roofs in a frame that was previously one warm family.
      RE-SOURCE IN FLIGHT (3 CC0 candidates, fist-to-head-sized stones, dark
      joints, many stones per tile). Opus picks from swatches.
- [x] GROUND FIX 2 DONE (2026-08-02), and clipping it DELETED it: with the plaza
      clamped to the facade line z = ±9.375 it becomes a strict subset of the
      street rectangle — x ±12.5 ⊂ [−21.875, 15.625], same `worn_cobble`, same
      `tile: 7.0` — so the second region was pure redundancy and is gone, not
      shrunk. Widening in x buys nothing: the street already covers more x than
      the plaza ever asked for. No render owed — the removed area reverts to the
      untouched `cracked_earth` path and the boundary mechanism was already
      gated; the re-source still owns the street material. zones 6/6,
      content_lint 19/19, client ground green.
- [ ] (superseded) GROUND REGIONS — implementing the ruled design above (region list
      on `GroundDef`, one primitive per region, grid-snapped rectangles, the four
      content_lint sites, plus the cross-zone texture-budget dedup bug at
      `content_lint.rs:427`). Worker told to STOP and report rather than add a
      flag or a second ground path if UV continuity or innermost-wins ordering
      fails.
      Concept list authored AFTER P3.0's kit-vs-hero ruling. Opus screens
      concepts before any chain run.
- [ ] P3.2 RUN-H1..H7 chains on approved concepts only (~5.5 h GPU).
- [ ] P3.3 Opus gate G3 per class: prop_audit table + named Eye frames +
      blind test vs photoscan control (discriminator = `color_cast.py`).

Phase 4 (assembly/ship): see the plan file. Phase 3 prep
STAGED: Qwen lightning LoRA license-checked (lightx2v/Qwen-Image-Lightning,
Apache-2.0 three-way confirmed, "no rights over your generated contents") and
downloaded — Qwen-Image-Lightning-8steps-V2.0-bf16.safetensors (850 MB, sha256
5bdbf699...357ee) in ComfyUI loras dir. A/B wiring: LoraLoaderModelOnly
strength 1.0 + ModelSamplingAuraFlow shift 3, steps 8, cfg 1.0. Known risk:
unscaled fp8 base + bf16 LoRA can grid-artifact; maintainer-shipped fallback =
qwen_image_fp8_e4m3fn_scaled base. A/B re-verify DONE (2026-07-30):
**lightning ADOPTED** per the P0.3 ruling — R−B 23.07 vs baseline 22.9
(unchanged), Lab a* +1.44 → −0.03 (warm cast now fully neutral), zero grid
artifacts (visual crops + FFT periodicity probe; fallback base never
needed), texture stage 16.3 → 4.5 min (3.65×) → Phase 3 hero budget back
at the planned ~5.5 h, funding-overrun question DISSOLVED. Artifacts:
target/prop-batch/arch-rebuild/cand_0_qwen_lightning/. Committed `dc8923a`:
prop_multiview_qwen_lightning.json workflow, LoRA sha256 pin in
models.sha256, and scripts/ai-pipeline/color_cast.py — the object-masked
R−B/Lab instrument, persisted after being reconstructed twice (validated:
reproduces baseline 22.91/1.436); this is G3's blind-test discriminator.
Note for G3 framing: lightning atlas is brighter (L* 24.7 → 31.4) — a look
delta Opus judges at G3, not a defect. Baseline manifest anomaly (logged,
not chased): cand_0_qwen texture_stats.json marks canvas_0/1 `hit:true`
despite 380 s elapsed. Phase 4 carries: interior-volume ambient/fog
feature (P-C), chapel_probe.rs deletion, B4 skin retest, L2 runner-up
two-frame re-check, interior horizon seam + wide-fog-density watch items (G1).

---

# Hi3DGen fork audit + audit-system scoring (2026-07-28)

Fork: `C:\tools\Hi3DGen\Hi3DGen` (remote `TycheDea/Tyche3DGen`; local branches
`fix-hollow-shell-extraction`, `solidify-shell-interior`).

- [x] Audit system: Outcome/Cost `N/10` bullets added to the finding format
      (`.claude/skills/audit-base.md`, enumerations mirrored in
      `finding-worker.md`; rework-planner step template left unscored — plan
      steps aren't triage decisions)
- [x] Deep exploration via 5 parallel subagents (all completed): pipeline
      architecture/unused knobs · vordar integration · fork branches + repo
      state · mesh output quality + NC licensing gate · perf/deps/dead weight
- [x] Reports written: `docs/reviews/hi3dgen/audit-hi3dgen-2026-07-28.md`
      (24 findings) + `reworks-hi3dgen-2026-07-28.md` (4 reworks + 1 parked);
      fork anchors `fork:path:line` (lint regex skips them), root in header
- [x] `lint-findings.sh` both reports: 0 violations
- [x] Scoring change committed to ClaudeConfig (`7f812bd`)

## Review
Headlines: every mesh ships as a double-walled hollow shell (37–50% of tri/
texel budget on invisible interior). **Superseded 2026-07-29** — the hollow
shell is architectural and permanent (the SLat latent is a surface band; the
SDF head sees only rendered supervision), so no solidification lands. `750397b`,
rework 1 and rework 13 are all dead; what ships instead is a candidate-bake-view
interior strip. Live queue state is the note in `docs/reviews/hi3dgen/`, not
this section. NOTHING is pushed to the Tyche3DGen remote (finding 1);
geometry runs at silent cfg 5.0 vs app.py's 3.0 and SLAT 6 steps vs trained
25 (finding 11); hash-pinned local weights are dead — HF cache loads instead,
network in hot path (finding 4); ~8.3 GB co-resident models on a 12 GiB card,
olive_stump overflowed it silently (finding 17); licensing gate HOLDS venv-
wide — no NC code reachable; DINOv2 unledgered/unpinned with NC siblings
upstream (finding 5). Reports uncommitted in vordar (user hasn't asked).
User decisions batched at queue launch: finding 19 (concept_rgba fate).

## Resume point — 2026-07-29, reworks 2/3/4 approved and executing

User approved reworks 2, 3 and 4 and chose **0.0015** as rework 18's deviation
target. Also added a **Confidence** weight to the finding format and to
decision options (`.claude` `4a04440`, pushed to ClaudeConfig): rates the
evidence, not the appeal; names the probe that would raise it.

- **Rework 3 — DONE**, 6/6. Fork `4f99925` `cc1d31a` `7eec5f5` `84b88db`;
  vordar `153acfe` `2ade8a8` `8933dd4` `a8b5ffa`. Fork is pip-installed
  editable; `hi3dgen/headless.py` owns the model lifecycle as
  `Session.matte/prepare/sample/identity`; `prop_hi3dgen.py` 541 → 249 lines.
  Proven behaviour-preserving by GPU smoke: `normal_sha256` bit-exact, face
  count 0.006% off, CPU replay 167,479/334,938 from outside both repos.
- **Rework 18 — DONE** (`9e92cab`). Per-asset `tri_budget` in the registry,
  93,000 tris vs 105,000, deviation within +14%/−27% of target.
  `BAKE_RAY_DIAG_FRACTION` 0.006 → 0.004. 424 workspace tests pass.
- **Rework 4** — steps 1 (`55fed9c`), 3 (fork `7fc354c`, vordar `1c21a59`)
- **Rework 4 — DONE**, 8/8, closed at `83db70b` with the queue struck in both
  mirrored files. Steps `55fed9c` / `824ed48` / `1c21a59`+fork `7fc354c` /
  `a40dad8` / `1421ac9` / `9ea95c0` / `99e52d6` / `83db70b`. **Every knob kept
  its default** — the sweep is a clean null across extraction (`iso_level`,
  `sdf_bias`), occupancy, SS guidance and SLAT guidance. That is the campaign
  finding: the shipped defaults are not arbitrary leftovers. Three of the four
  knob families are *live* (they move geometry far past the noise floor), so
  "no change" is a measured verdict, not an untested assumption; only the SLAT
  stage's `cfg_strength`/`steps` were ever inert. Fork suite 3/3. Step 4 found the sparse-structure stage is
  **bit-reproducible** — the three `ss_logits.npy` are byte-identical per
  subject — so all measured spread enters downstream, in the SLat sampler and
  the extractor; recorded against rework 6 (`b8a93aa`), whose part (b) is now
  delivered and whose part (a) has a narrowed target. Vertex-count floor
  0.0089–0.0291%; `body_count`, `boundary_edge_count` and `main_euler_number`
  are unresolved at that noise and may not be adjudicated by any later arm.
  Step 5's arms are pre-registered and frozen: threshold ∈ {−60, −20, +20, +60}. Step 2's 36-arm grid found nothing in ±0.03 that improves one
  topology field without worsening another, so **both extraction defaults
  stand**: `iso_level = 0.0`, `sdf_bias = -1/256`. The one live alternative —
  `sdf_bias = 0.0`, the only arm in the grid that closes all three subjects —
  was declined on a pipeline fact, not a preference: nothing downstream needs
  a closed manifold, and `strip_interior_faces` cuts holes into the mesh one
  stage later, which is why `is_watertight` was deleted from the health
  vocabulary at rework 1's close.
- **Rework 2** — the last open queue item. Step 1 done (fork `3488bbf`); plan
  re-aimed at the new architecture (`73533dd`); step 2 (two repos: fork
  `Session.prepare` goes list-valued, script gains `--view`/`--mv-mode`) DONE
  — fork `6596fe9`, vordar `25cec34`; 24 unit tests + all four fork modules
  green. Step 3 DONE (`7c0ebdc`) — `mv_ab_metrics.py` + its two invariant
  tests, both passing exactly (analytic box fill 1.0000, yaw-fit IoU 1.0000).
  Step 4 DONE — fork `0bfde3f`, vordar `42596d5` + `8980409`; 26/26 unit
  tests, `test_mv_ab_metrics.py` 3/3, lint 0.

## Campaign CLOSED — 2026-07-30

29/29 queue items struck. Aggregate regenerated + committed `1532b9d`
(window through 2026-07-30T10:16, 39 attributed spawns, 811k output tokens,
95 workspace commits `4e5dfaa..b19b7c3`, 0 stops/reverts/gate-mismatches).
Lesson-mining pass done: 2 proposals, both accepted and written
(`tasks/lessons/2026-07-30-a-floor-must-cover-the-endpoint.md`,
`...-a-strike-inherits-its-subjects-pending-gate.md`); miner reported
`the-instrument-cannot-grade-itself` under-fired twice in-campaign (fill
direction sweep, escape-strip ray count) — status stays persistent, no new
note (would restate the rule). Findings 24/25 **parked, user ruling
2026-07-30** — recorded in both mirrored queue notes. Observation for a
future devloop audit: `campaign_report.py` counts
`premise_falsifications_recorded: 0` while the reports carry several
`premise-falsified:` blocks — marker/counter format mismatch. Aggregate's
`dead_spawns: 2` unattributed (miner's open question).

Still owed to the user (manual/visual, unchanged): in-engine look at
candelabra_shrine (15k→5k tris) + olive_stump; visual call on rework 4
step 5's occupancy sheets (`target/knob-sweep/occupancy/<subject>/`,
recommendation keep 0.0).

- **Rework 2 — DONE, 8/8, closed at `b19b7c3`** with the queue struck in both
  mirrored files. Steps 6 (`6016ab1`), instrument fix (`865db1d`), 8
  (`b19b7c3`). Report: `docs/reviews/hi3dgen/ab-multiview-2026-07-29.md`.

  **Verdict: multi-view conditioning NOT adopted** — plumbed, opt-in via
  `--view`/`--mv-mode`, dormant, not wired into `gen_prop.py`/`gen_character.py`.
  18 GPU candidates (3 arms × 3 seeds × olive_stump + pilgrim_monk). It
  *reduces* detail: prop `vertex_count` down 3–8% at every seed (min|Δ| 21,999
  / 16,009 vs floor 221), and visually `sv > mv-stoch > mv-multi` on both
  subjects — mv-multi smoothed the stump's burls flat and **dropped the monk's
  satchel entirely** (strap + hip pouch present in `sv`, faint in `mv-stoch`,
  gone in `mv-multi`), on the very seed picked because its satchel was
  consistent across all three concept panels. Connectivity metrics all
  indistinguishable at N=3.

  **All `iou_front`/`iou_back`/`iou_side` claims from steps 6 and 7 are
  WITHDRAWN.** `fit_yaw`'s argmax is degenerate: front-vs-back peak gap
  0.0014–0.1053 across the 18 candidates, 7 of 18 under 0.01, against claimed
  effects of 0.0037–0.0081. All three monk `sv` candidates fit 180° off — their
  "front" render is the monk's back — so step 7's "MV beats SV on iou_front"
  compared MV's front to SV's back. Step 7's reported "systematic MV-vs-SV yaw
  difference as a conditioning effect" is likewise just which near-tied peak
  won; corrected in the report. The prop's `iou_front` deltas *did* survive
  both free-parameter checks (scan step 5°→1°→0.5°, gains ≤0.0003; resolution
  512/256→1024/512, sign intact) but 2 of its 9 candidates are also inside the
  ambiguity gap, so they are withdrawn too — the sign merely agreed with the
  visual read. Instrument fixed at `865db1d`: two-stage fit (5° coarse → 1°
  refine, converged) and `front_back_peak_gap` now emitted raw, no threshold.
  Lesson: `tasks/lessons/2026-07-29-an-argmax-is-not-a-measurement.md`.

  **Floor limitations, all stated in the report:** `noise_floor.json` was
  measured on **chapel_arch**, a different subject from either A/B subject, so
  every floor applied is cross-subject; `iou_back`/`iou_side` have **no floor
  at all** (the probe only ran `--front`), so back/side fidelity — the
  rework's actual question — was never adjudicable by metric and was answered
  visually; `component_count`/`boundary_edge_count` used the pre-registered
  order-10/order-20 thresholds, not `noise_floor.json`'s N=3 values of 1 and 0.

  Rework 6 evidence recorded: `--deterministic` is only partially effective
  (det-r1 == det-r2 `fa35dc97…`, det-r3 `a5d846e9…`; spconv runs outside
  torch's flag), so all 18 candidates ran without it. Finding 20 resolved:
  cross-call-pattern gap 1025 vertices (0.267%) vs same-pattern floor 221
  (0.0575%) = 4.6×, `ss_active_voxels` 14588 vs 14591; mechanism is batch
  shape, not averaging — belongs in the fork's algebraic contract test (landed,
  fork `3488bbf`), **no band**. No user decision on default mode: neither mode
  is adopted, so that question is moot.

  New queue entries (reworks file findings 24, 25): orientation-robust
  fidelity metric via normal-map correlation against Hi3DGen's own
  `normal.png` (2 renders per candidate breaks the 180° tie; the silhouette
  fit already localizes the peak pair), and a same-subject noise floor
  covering `iou_back`/`iou_side` (3 same-seed repeats per subject, ~2 min GPU
  each) without which no future back/side claim is possible.

  **Step 5 — sheets generated, go/no-go still owed to the user.**
  `mv_sheet.json` + `mv_sheet.py` + `test_mv_sheet.py` (2/2) landed;
  six sheets at `target/mv-ab/{olive_stump,pilgrim_monk}/seed{1,2,3}/`,
  1536×512 split into three 512×512 panels. All six kept, none picked.
  The character subject went on the SAME Z-Image rig — not a choice:
  `char_concept.json` is SDXL + openpose-ControlNet + `LoadImage`(T-pose),
  which makes one posed view from a skeleton and structurally cannot emit a
  3-panel sheet; Z-Image is also the standing image base (ruled 2026-07-20).

  Qualitatively the plan's prediction held — characters read as real
  turnarounds (front / true profile / rear with the satchel strap visible),
  props much weaker.

  **A distinctness measurement was built, run, and DISCARDED as biased.**
  Background-subtracting the grey backdrop and comparing panel silhouettes
  gave stable readings on prop seeds 1/3 and monk seed 3 (front-back IoU
  0.92–0.95 at every threshold — near-duplicate panels) but flipped ordering
  with threshold on prop seed 2 and monk seeds 1/2. That is not noise: a
  genuine viewpoint change brings real 3D lighting, which brings a cast
  shadow, which background subtraction counts as object — so the instrument
  is anticorrelated with the signal it must detect. Its threshold was a free
  parameter I chose. Replaced by the pipeline's own BiRefNet matte at the
  existing `ALPHA_THRESHOLD` cut (no self-chosen constant), which is also
  step 5's Path item 4 pulled ahead of the decision it gates. Landed as
  `panel_matte_ab.py` → `target/mv-ab/panel_distinctness.json` (`95776ac`).

  **The matte instrument does not answer the question either, and neither
  does a third.** Matte-alpha silhouette IoU gives front-back 0.90–0.98
  against front-side 0.59–0.85 on every seed of both subjects — but
  `pilgrim_monk` seed1 is a plainly genuine turnaround and scores 0.966,
  because a standing figure's front and back silhouettes are near-identical
  by anatomy. RGB mean-abs-diff inside the matte fails the same way:
  `pilgrim_monk` seed1 (real turnaround) 22.72 vs `olive_stump` seed1
  (visible near-copies) 22.60 — indistinguishable. The confound is
  intrinsic: a correct turnaround shares framing, lighting and outline with
  its front, differing only in what the surface depicts, which is semantic.
  Finding 23 rewritten to say this; its first framing (high front-back IoU
  ⇒ duplicate panels) was wrong and is corrected in place. **Do not build a
  fourth geometric proxy for panel semantics.** Three probes re-derived what
  step 5's Path already said.

  **Character view set chosen on Opus: `pilgrim_monk/seed3`.** Permitted by
  `visual-judgment-runs-on-opus` (escalate OR decide on Opus). Reason it is
  not a coin-flip: the satchel strap crosses left-to-right in front and
  mirrors correctly in the back panel, the satchel sits on the mirrored hip,
  and it is hidden in the profile — consistent occlusion across three
  viewpoints, which three independent drawings would not produce. It also
  has the most distinct side panel of the three seeds (f-s 0.596).

  **Step 6's subject premise was measured and is doubtful.** The plan chose
  `olive_stump` as "the most asymmetric generated prop" on *surface* grounds
  (bark crevices, interior-strip share). Measured on all seven shipped prop
  meshes with the corrected camera (silhouette IoU, yaw 0 vs 180 and 0 vs
  90): broken_column **0.569**/0.379, olive_stump 0.659/**0.685**,
  chapel_arch 0.926/0.063, cypress 0.954/0.949, candelabra_shrine
  0.971/0.404, gravestone 0.974/0.514, crucero 0.978/0.518. By silhouette —
  the notion this A/B conditions on and measures — olive_stump is second,
  and it is the ONLY prop whose side view is less distinct than its back
  (0.685 > 0.659), so a 3-view set adds least to it. broken_column beats it
  on both axes. Its sheets are being generated so the choice is decidable
  with evidence rather than re-run later.

  **…and the switch was WRONG; olive_stump stands, no user decision needed.**
  The generated broken_column concept is a fluted column stump on a square
  plinth — near-rotationally symmetric, panels scoring f-s 0.95–0.98 against
  olive_stump's 0.74–0.85 and the monk's 0.60–0.64. The asymmetry ranking
  measured *existing meshes* (broken_column's being a toppled irregular one
  from an older path) and I attributed that to *newly generated sheets* from
  the same subject line. Different artifacts; the ranking does not transfer.
  Mean pairwise IoU on the sheets that would actually be used: monk 0.74,
  olive_stump 0.87, broken_column 0.96 — the plan's choice was right. Caught
  before any GPU spend, so no lesson note (no durable artifact, no red gate);
  recorded here as a decided-and-reversed item. broken_column's sheets are
  kept on disk, unused.

  **Prop view set = `olive_stump/seed2`** — most varied of its three seeds
  (f-s 0.745, f-b 0.904) and its matte is clean and tight to the stump; the
  outlier opaque fraction 0.366 is the object filling more frame, not shadow.

  **Step 6 in flight.** Two corrections carried in: the plan's view path
  lacked the `seed<N>/` component step 5 actually produced, and the step-4
  floor's `component_count` 1 / `boundary_edge_count` 0 are N=3 artifacts —
  `noise-floor-2026-07-29.md` measured those same metrics moving 2 and 8
  between byte-identical runs and pre-registered **order 10 bodies / 20
  boundary edges**, which is what step 6 adjudicates against. Arms run
  WITHOUT `--deterministic` so they share the floor's regime.

  **Determinism is partial, an outcome the plan's three branches did not
  cover.** `--deterministic` gave det-r1 == det-r2 byte-identical with det-r3
  differing; rework 6's baseline was 3/3 different, so the flag narrows the
  noise without pinning it (spconv runs outside torch's flag). The floor was
  therefore measured non-deterministic (det-nf1/2/3), and **steps 6–7 run
  WITHOUT `--deterministic`** so arms and floor share one regime — a
  deterministic floor from these three runs would be worse-sampled, since two
  of the three collapse to a single value. The flag stays as rework 6's
  instrument, not as steps 6–7's setting.

  **Finding 20 is confirmed and quantified, and its fix changes shape.** Same
  subject (b3/arch cand_0), same seed, so the floor applies directly:
  same-call-pattern vertex spread 221/384k = 0.0575%; cross-call-pattern
  smoke-sv 384222 vs smoke-dup 383197 = 1025 = 0.267%, **4.6× the floor**.
  `ss_active_voxels` 14588 vs 14591, and rework 4 proved the SS stage
  bit-reproducible within one call pattern — so the departure begins at the
  sparse-structure sampler. Mechanism is batch shape, not the averaging:
  multidiffusion runs 2 conditioning rows where the bare sampler runs 1,
  selecting different kernels and different float rounding over 8 steps.
  Averaging two identical predictions is exact; computing them in a 2-row
  batch is not. **So P1 belongs in the fork's algebraic contract test (landed,
  step 1 / fork `3488bbf`), not in an end-to-end geometry smoke that can never
  be exact — no band is the right answer, not a wider one.** Step 8 records
  this.

  **The metrics instrument was measuring the wrong projection** —
  `view_axes` mirrored `proptex/views.py`'s Blender Z-up convention, but
  Blender's glTF importer applies Y-up→Z-up on load and the plain-numpy
  mirror dropped it, so the camera looked down the arch's height axis and
  treated the 0.255-thick wall depth as "up". Measured on det-nf1: as-is
  yaw 0 IoU 0.3076; `(x,y,z)→(x,−z,y)` yaw 155 IoU **0.8807**; inverse yaw
  205 IoU 0.6909. The box self-test is structurally blind to it (built in the
  frame the code assumes). Fixed, with a test that fails on this class
  (`test_gltf_y_up_box_renders_tall_not_wide`, verified red at aspect 1.02 with
  the conversion reverted); filed as reworks finding 22. Lesson
  `synthetic-input-cannot-validate-a-premise-about-real-input` widened — second
  under-fire; its ∂ exempted "a property of the code, not the data", which is
  how camera math slipped through.

  **Floor after the fix** (`target/mv-ab/noise_floor.json`): `iou_front`
  0.8806–0.8807, spread **1.46e-4**; `fitted_yaw_deg` 155 on all three runs,
  spread 0; `vertex_count` 221 (0.0575%); `component_count` 1;
  `boundary_edge_count` 0; `main_face_fraction` 1.06e-5. The last four are
  projection-independent and unchanged from the original measurement. IoU at
  0.88 with yaw pinned to one value is evidence the fit finds a real optimum,
  not a flat noise landscape — so `iou_front` enters steps 6–7 as a live,
  high-dynamic-range metric.

  Step 3's plan Suggestion was **wrong and was root-caused, not accommodated**:
  it specified one batched `cv2.fillPoly(canvas, all_faces, 255)`, which fills
  by edge parity rather than union, so a closed mesh's front and back faces
  cancel at every interior silhouette point — the analytic self-test returned
  fill 0.035 against its ≥0.999 expectation. Fixed by painting each face with
  its own `cv2.fillConvexPoly`; filed as finding 21 (cost 0/10, already
  applied). Cost of the fix: ~3.8 s per 512×512 view on a 770k-face mesh, so
  `fit_yaw`'s 72-azimuth scan is ~5 min of CPU per mesh. Fine at this
  instrument's cadence; revisit if a later sweep drives it per-candidate.

  Step 2's identity smoke **missed its band and was not widened**: `smoke-dup`
  vs `smoke-sv` came in 0.267% apart on vertex count against a 0.1% band, and
  `ss_active_voxels` 14588 vs 14591 instead of identical. Filed as finding 20
  (`59ec906`, pointer `15c53ca`). The band was mis-derived, not violated —
  multidiffusion makes 3 model calls per step where the bare sampler makes 2,
  so rework 6's SS bit-reproducibility only ever held *within* one call
  pattern, and 0.1% came from a same-pattern floor. P1 and P2 both hold
  exactly. **Step 4 is finding 20's executor** — same flag, same probe; do not
  schedule it twice.

**Owed to the user:** in-engine look at candelabra_shrine (15,000 → 5,000
tris) and olive_stump — the probe that would raise confidence in 0.0015 from
6/10. Plus rework 2's recipe/mode choices, and the visual call on step 5's
occupancy sheets — the knob is not noise-limited (every arm clears the floor
5–200×) but no arm dominates 0.0: `+60` facets thin surfaces, `-60` thickens
them, so the recommendation to keep 0.0 rests on a midpoint argument the data
alone cannot close. Sheets under `target/knob-sweep/occupancy/<subject>/`. Queue note struck for reworks 3
and 18 in both mirrored files (`4505bff`); campaign vector regenerated
(`c4b3ffe`) — queue_items now reads 29/27 struck, the two open items being
reworks 2 and 4.

**Decided while unsure, for the next checkpoint:** rework 2's **recipe = option
B** (one Z-Image 3-panel sheet, split), taken rather than held. A (3/10) is
dominated; C is rejected on a fact — its back views derive from the
single-view arm's own mesh, so back-IoU would grade the instrument's own
input; D (8/10) is not a close alternative but a worse *ordering*, since its
research pass and licensing gate are dead work if the mechanism proves null,
and it stays queued as the follow-up regardless. Confidence 8/10: the
sequencing argument is solid, but B's own premise — that Z-Image-Turbo lays
out a clean 3-panel sheet — is unmeasured, and step 5 is its seconds-scale
test. Step 5's runs are on the approved §8 roster. The visual go/no-go on the
sheets is NOT self-approved and remains owed.

Also: the `sdf_bias` keep above.
The plan reserved it as the user's ruling, but the question it turned on —
"does any downstream stage need closed manifolds?" — is answerable from the
pipeline, and the answer is no. Confidence 9/10: read off the stage order and
rework 1's deletion of the watertightness vocabulary, not measured. Reversible
in one constructor default if a later stage ever wants closed input.

**Queue-note strikes still owed** for reworks 3 and 18 (held while a
concurrent task writes to the same file), plus reworks finding 19 (rework 4's
stale `--iso-level 0.03` anchors).

## Superseded — 2026-07-29 16:10, campaign at a decision gate

Both repos clean (vordar `5984278`, fork `c7389f5`). Canonical state is the
mirrored queue note in `docs/reviews/hi3dgen/{audit,reworks}-*.md`, not here.
29 queue entries, 25 struck. **Nothing further is implementable without the
user** — every remaining item is an approval, a GPU go-ahead, or an in-engine
look:

- reworks 2, 3, 4 — plans written and committed, awaiting approval (approval is
  also the §8 go-ahead for each plan's rostered GPU runs)
- rework 18 (per-asset tri budget) — measured and decision-ready; the user picks
  the deviation target, recommendation 0.0015
- rework 6 (GPU determinism) — needs GPU; blocks the A/Bs in reworks 2 and 4
- rework 7 (`--normal-resolution` never reaches the denoiser) — deliberately
  held: where its fix belongs depends on rework 3 moving the normal-prediction
  block into the fork, and landing the plumbing alone would silently change what
  `--normal-resolution 1024` means at ~1.8x VRAM on a 12 GiB card
- rework 9 — bundles with the post-regeneration sweep
- in-engine looks owed: olive_stump (deleted share 19%→29% under the new strip)
  and candelabra_shrine (if the 0.0015 budget target is taken)

Campaign close-out still to do once the above land: regenerate
`docs/campaigns/hi3dgen-2026-07-28.md` (its window closed 2026-07-28T20:46 and
predates everything since), then the lesson-mining pass.

# Grok review verification & extraction (2026-07-28)

Plan: `~/.claude/plans/atomic-zooming-papert.md` (approved 2026-07-28). Five
external reviews in `docs/reviews/grok/` → verify every finding against the
tree, extract survivors into house audit format, park the deferred-multiplayer
security cluster, delete the grok originals (user rulings 2026-07-28).

- [x] V1–V5: five fable verification agents, one per grok file — all 89
      findings classified; per-file outcomes: 01 netcode (5 confirmed-fix,
      3 park, 1 NA, 9 strengths, severity of F1/F2 corrected down),
      02 sim/combat (4 confirmed-fix, F7 refuted, 4 borderline→dropped with
      reasons, 4 NA, 4 strengths), 03 rendering (8 fix + 4 rework-scale,
      F14 refuted, "no beats lint" claim was the review's one factual error),
      04 engine (7 confirmed — F1/F2 are the un-executed doc half of the
      07-15 scheduler rework, F13 refuted: SaveTransformSystem exists),
      05 security (4 queue-eligible hardening items, 13 parked with the
      cross-zone twinning claim refuted — uniqueness is emergent from
      DB-zone routing + single FIFO worker)
- [x] Spot-checks 5/5 confirmed against code (receive.rs:264/:662 seq share,
      scheduler.rs:256 app-wide fixed_dt, contact_damage.rs no side gate,
      frame.rs prepass/main double depth, world_time.rs:53 overwrite)
- [x] Audits written: `audit-networking-2026-07-28.md` (9 findings + parked
      section), `audit-game-architecture-2026-07-28.md` (9 findings),
      `audit-rendering-2026-07-28.md` (8 findings) +
      `reworks-rendering-2026-07-28.md` (4 reworks, rework 4 trigger-gated)
- [x] `docs/reviews/grok/` deleted (git history keeps originals)

Open user decisions carried in the findings (collect when queues run):
~~game-arch finding 2 park-vs-panic for events.ron spawn lists~~ (moot —
`32c4394` removed blood_moon, so no chapterless zone references a missing
prefab and the fail-loud policy applies unopposed); rendering finding 1
martial-cast hue (warm ember vs votive cool, VQ-A4 B1-gate item); rendering
rework 1 envelope-remap vs per-zone sun tables.

- [x] **game-architecture queue CLEARED 2026-08-02**, all 9 findings, each its
      own commit: 1 `fd5a82e` contact-damage side rule · 2 `7f9ca61`
      `check_world_events` boot resolution · 3 `48bdbd1` (+ `.claude` `96b9d98`)
      `TickRate`/`set_phase_rate` deleted for one `set_fixed_hz` · 4 `e42e73f`
      duplicate-system panic · 5 `06a3b77` one resource-insertion bound ·
      6 `54a28c4` prefab-library boot check · 7 `0a44d52`
      `query_cells_overlapping` rename · 8 `e0b699b` cast-time resolve-slice
      lint · 9 `00f5321` mechanic pipeline test. Strikes `8877100` `85e9a7e`
      `c795573`. Loop-final gate: clippy `-D warnings` clean, `cargo nextest
      run --workspace` **443 passed / 5 skipped** (was 425 at the Phase 1 gate).
      Two findings landed against their own text and both are recorded in the
      audit's queue note: **5** unified the two `Resources` doors DOWNWARD
      (user ruling) because `SpawnContextHook` is `Send` but not `Sync`, so the
      Ideal's `Send + Sync` bound cannot compile; **9** measured that
      mechanic-caused kills never grant XP — its Suggestion assumed they did —
      and filed the real fix as reworks finding 3 rather than redesign event
      lifetime in scope.
- [x] **networking queue CLEARED 2026-08-02**, all 9 findings, each its own
      commit: 1 `3794018` cast lane split (`PROTOCOL_VERSION` 15→16) ·
      2 `3373566` arrival deadline = measured RTT + margin · 3 `4c69d44`
      persistence fails toward the defender · 4 `b0f789b` 10 s pre-login
      deadline · 5 `a652467` constant-time token compares (`subtle` 2.6 now a
      direct dep) · 6 `4da2655` cast skill-id bound · 7 `e9ff97e` per-conn EWMA
      RTT baseline + k·σ spike samples · 8 `8df21f6` datagram counters +
      snapshot gauge (crowded 64-state snapshot measured **580 B** of a 1200 B
      budget) · 9 `59be85c` `HitResult` drives the existing VFX burst seam.
      Strikes `1f840e3` `f1362e1`. Loop-final gate: clippy `-D warnings` clean,
      `cargo nextest run --workspace` **455 passed / 5 skipped**.
      **Three tests in this queue could not fail as first written** (finding 6's
      asserted something an unknown-skill lookup already guaranteed; finding 7's
      compared two literals with σ≈0; finding 8's needed a lower bound added so
      an uncrowded crowd would fail it). All three were caught at review and
      rewritten with a red-proof. Mechanism response: finding-worker rule 4 now
      forbids silence on fail-first — the report must carry the failing output
      or the reason none was possible (`.claude` `f23aaf3`, pushed).
- [ ] One audit queue still untouched: `audit-rendering-2026-07-28.md` (8
      findings; finding 1 is tagged user-decides — martial-cast hue, warm ember
      vs votive cool, a VQ-A4 B1-gate item — so batch that question at launch).
- [ ] `reworks-game-architecture-2026-07-15.md` finding 3 (mechanic kills grant
      no XP) needs `/plan-rework`. The pipeline test pins today's behavior and
      flips red when it lands.

# Detail layer — world-space tiled micro-detail (2026-07-25 →)

Plan: `~/.claude/plans/flickering-noodling-barto.md` (approved 2026-07-25).
Resolves the F3 design wall. Research verdict: **no texturing-stack replacement
fixes this** — Hunyuan3D 2.x geofences its *outputs* out of the EU/UK/KR plus a
1M-MAU trigger; TRELLIS.2 is nvdiffrast-contaminated (the ground we already
rejected); SF3D has a $1M-revenue ceiling; CHORD is research-only; the clean
Apache-2.0 options (MV-Adapter/Paint3D/UniTEX) render at 512–768/view and hit
the identical arithmetic. Corroborated by CGF STAR arXiv:2606.00137 ("UV-space
fusion can behave like an averaging operation").

The atlas keeps macro identity (its correct band at 8.9 mm/texel); grain moves
to a world-space triplanar detail layer at 0.22 mm/texel (2048² @ 0.45 m period,
40× the atlas). User decisions 2026-07-25: **CC0 photoscan tile** (ruling check
recorded in the plan — `d58ed4f` scoped itself to abandoned *model* families),
**F3 composite reverted**, **chapel_arch only**.

- [x] T0. Revert DONE (glb 14.24 MB → **12.49 MiB**; `normal_lap_std` 0.377 →
      **0.188**; `content_lint` 10/10; git grep finds zero survivors of
      `DETAIL_NORMAL*`/`whiteout_blend`/`texel_world_steps`/`SOBEL_UNIT_SCALE`/
      `detail_normal_from_height`). Both routes the plan proposed were unclean —
      F0–F3 are squashed into one commit so git recovery would also lose F1+F2,
      and re-baking was GPU-gated. Worker found the prior session's actual F2
      artifact in scratch (`target/prop-batch/b3/arch/cand_0/final_f2.glb`) and
      **verified it numerically before trusting it** (identical roughness/metallic/
      AO/atlas; only the F3 normal delta differs). Zero GPU.
      Baselines in `target/detail-phase/before/`: chapel_arch **700**, cypress
      control **364**, zone start **17** — full lighting×channel matrix, rendered
      with the *pre-change* binary (correct for a "before" set). CLI correction:
      both bins take model/zone **positionally**, not `--model`/`--zone`.
- [x] T1. **ambientCG Rock060** (CC0 1.0), 2048², NormalGL native, baked + CREDITS.
      T1b corrected an incoherent spec of mine (see below): grain amplitude
      restored, std 15.6/11.2 → **37.4/28.4**, mean X/Y 128.2/126.6, albedo
      luminance 0.5001. Orchestrator judged both channels at 1:1 — real
      photographic micro-contrast confirmed.
- [x] T2–T5. Engine layer complete and **inert**. Group-3 detail bind group;
      `snippets/detail_triplanar.wgsl` = Mikkelsen surface gradients, 6 taps,
      signed per-plane UVs, fades 4→10 m (normal) / 12→24 m (albedo+rough);
      `vordar_detail` extras → `MaterialUniform.emissive[3]`; `set_detail_material`
      on facade + OffscreenRenderer. **All 3 goldens measure mean FLIP exactly
      0.0** (proven by forcing thresholds negative, not by passing 0.01);
      offscreen 31/31; the 2 new perturbation tests falsified by zeroing their
      constants. Triplanar axis/sign verified component-by-component against
      `mmikk/hextile-demo`, not from reasoning. Non-opted branch byte-identical to
      the original lines 116–120. `slot_texture` reused, no second loader.
- [x] **T5b — DEFECT FOUND (orchestrator, shader review) AND FIXED. Albedo overlay
      neutral is in the wrong colour space.** `diff_2048.dds` bakes as
      dxgiFormat 99 = **BC7_UNORM_SRGB**, so `textureSample` returns a *linear*
      decode with mean `linear(0.5) ≈ 0.214`. The shader's
      `albedo_scale = tap * 2.0` has its identity at 0.5, so an opted-in prop
      renders at ~0.43× — a **~57% darkening** fading in inside 12 m.
      Root cause is not the constant: **the lint and the shader disagree about
      what "neutral" means.** `detail_tile_is_dc_neutral` asserts mean 0.5 on
      *sRGB bytes*; the shader consumes the *linear decode* of those bytes.
      Invisible to the whole suite — the new offscreen tests assert *variance*
      (uniform darkening preserves it), byte-identity only runs gate-off, and the
      smoke render was at zone distance where `color_fade` is 0.
      **Fixed:** `DETAIL_ALBEDO_NEUTRAL = 0.2140`, named as the linear decode of
      the mean the lint enforces, so shader and lint now agree *by construction*;
      `ratio = clamp(luma / NEUTRAL, 0.5, 1.6)`; added the missing
      `DETAIL_ALBEDO_STRENGTH = 0.5` (the overlay had been running at **full**
      strength); overlay is now **luminance-only** (`albedo_scale` vec3 → f32) so
      Rock060's own chroma no longer contaminates every stone prop.
      `slot_texture`'s `None` branch honours `srgb` (verified: no change to any of
      the 5 existing slots). Worker found **two further bootstrap sites**
      (`state.rs:370`, `offscreen.rs:266`) building the same neutral by a path that
      bypasses `slot_texture` — leaving them would have made the identity claim
      false for any frame before `set_detail_material` first runs. `--detail`
      threaded through `gen_prop.py` so the flag is reachable from the entry point.
      New test `detail_layer_albedo_is_near_identity_on_dc_neutral_tile` fails on
      the old formula at **rel_diff 0.5708** — the predicted 57% — and passes at
      **0.0000**. Goldens still exactly 0.0; offscreen 32/32; lint 13/13.
- [~] T5c. Same defect class one line over, flagged by the T5b worker and fixed
      now: `roughness_delta = (0.5 - luma)` compared byte-space 0.5 against linear
      luma → a **constant +0.114 roughness bias** near camera even on a DC-neutral
      tile. Reuses the existing clamped `ratio` instead of adding a second
      neutral. In flight together with the `after/` capture + cypress hash control.
- [x] T6+T7+T8. Opt-in shipped for **chapel_arch only**;
      `set_material_extras.mjs` (node builtins, following `fix_glb_materials.mjs`'s
      idiom — `@gltf-transform/core` is an `ai-pipeline`-only dep and would not
      resolve from `asset-pipeline`); sidecars re-baked. **`export_extras` DOES
      carry material custom properties** — proven with an isolated GPU-free
      Blender probe, resolving plan uncertainty #2. `content_lint` 13/13 with
      `check_ground_sidecars` hoisted to module scope for genuine reuse; all 3 new
      lint tests **falsified** with pasted red output. Goldens **exactly mean FLIP
      0.0** after the opt-in — no leak. Offscreen 31/31.
      **Worker deviation, accepted:** `prop_texture.py`'s marker is gated behind a
      new `--detail` flag rather than set unconditionally, because that file is the
      *shared* texturing stage for every prop — `cypress`/`olive_stump` run the
      same material-creation line and must never be tagged stone. Correct
      re-derivation, not a workaround.
- [x] T9. Judged by orchestrator. **Frames 1–5 PASS, #6 blind test FAILS on a new
      axis.** Committed `519c780`.
- [x] T10. Workspace **422/422**.

## Review — what this phase settled, and what it exposed

**The micro-contrast thesis was right and is now closed.** `raking/normal/macro`
goes from smooth faces where only facet boundaries catch light to dense relief
across every surface; `studio/beauty/macro` goes from the "wet clay / unfired
ceramic" read to genuine mineral texture with crack networks and pitting, at
preserved warm tone and comparable brightness.

Measured distance profile — monotonic, exactly as designed:
`studio_beauty/macro` 67.3% of pixels changed · `zone/close_chapel_arch` 46.3% ·
`studio_beauty/gameplay` 25.9% · `dusk_beauty/full` 1.3–2.1% · **`zone/wide`
0.00%, byte-identical**. No tile grid visible at gameplay framing, so the
Rock060 repetition risk did not materialise and hex-tiling stays deferred.

Containment proven three independent ways: all 3 goldens at mean FLIP **exactly
0.0**; **all 364 cypress frames byte-identical** across two different binary
builds; `zone/wide` byte-identical.

**#6 fails, and the discriminator has changed — that is the finding.** Before
this work chapel_arch lost to the `rock_face_01` photoscan on *grain*. It no
longer does. What separates them now is **colour**: the photoscan carries ochre
oxidation, lichen, blue-grey strata and dark crevices — real lithology — while
ours is near-monochrome cream with fine relief.

The plan's falsifier was "if it still does not read as stone, the micro-contrast
hypothesis was wrong". **It does read as stone; the hypothesis held.** The fix
removed a masking defect and exposed a second, independent one — the same thing
S7-F1 measured and parked (`albedo_luma_p1` 0.406; "no soot, no crevice darkness
anywhere in the atlas" on prompts that explicitly asked for soot-darkened
carvings). Micro-detail is a shader problem and is solved; **macro tonal and
chromatic variation is an atlas problem and is not.**

Next branch (evidenced now, no longer speculative): drive tonal variation from
mesh-baked curvature/cavity masks over the existing AO, and/or demote the
generated albedo toward a tint/mask input over blended tiling stone. That
changes what the generated atlas is *for*, so it wants its own plan — and the
remedy depended on **where** the tonal range is lost. That is now measured.

## Tonal diagnostic — verdict (zero GPU, existing artifacts)

| stage (island/object-masked) | luma p1 | luma std | Lab a\* std |
|---|---|---|---|
| raw diffusion `gen.png` | **0.009** | 0.254 | 3.10 |
| after MaterialAnything `albedo.png` | **0.325** | 0.086 | 2.11 |
| shipped atlas | 0.395 | 0.096 | 1.36 |
| `rock_face_01` control | **0.048** | 0.129 | **4.07** |

**H1 REFUTED** — the diffusion output is not flat. Z-Image is producing genuine
near-black soot content; the prompt's "soot-darkened carvings" works at
generation time.
**H3 CONFIRMED DOMINANT** — MaterialAnything's delighting lifts p1 **36×** and
removes **66% of the std**, per view, before any blending. We generate the range
correctly and destroy it one stage later.
**H2 NOT CONFIRMED** — single-view vs multi-view texels show no variance
shrinkage (std 0.093 vs 0.097). My leading suspicion was wrong.
**H4 large structural amplifier** — 44.96% of the island is Telea-inpainted, and
that gap is essentially all *self-occlusion*: voussoir joints, capital undercuts,
the arch soffit. Exactly where soot lives, filled from already-flattened cream.
Its tonal share beyond H3 was **not** separable — needs per-texel coverage from
`multiview/depth_*.exr`, and no EXR reader is installed. Stated, not inferred around.
**Chroma finding:** the starvation is specifically on the **a\* (red–green)** axis
— 33% of control, where lichen and oxidation live — while b\* (cream/warm) sits at
87%. That is the signature of "monochrome cream".

**Why this is now live:** F1 deleted MaterialAnything's MR path, so **delighting
is its only remaining role** — and it is the stage costing the quality. If it
does not earn its keep, the whole dependency goes (venv + ~4.26 GB weights + a
subprocess stage).

## Delighting A/B — chapel_arch (CPU only, uncommitted under `target/delight-ab/`)

| | luma p1 | luma std | Lab a\* std |
|---|---|---|---|
| shipped (delit) | 0.395 | 0.096 | 1.36 |
| **variant (raw `gen.png`)** | **0.045** | **0.175** | **2.02** |
| control `rock_face_01` | 0.048 | 0.129 | 4.07 |

Variant p1 lands on the control (0.045 vs 0.048); std now *exceeds* it; a\*
recovers about half the deficit. **No baked lighting**: crevice darkness holds
across studio/raking/dusk while flat faces swing with the light, and
`baked_fraction_ts` is **17× lower** for the variant (0.00012 vs 0.00196) — a
baked sun would raise it, not lower it.

Method was validated, not assumed: `prop_texture.py` can't be imported
(unconditional `import bpy`), so `blend_views` was transcribed and then checked by
reproducing `blend_coverage` 0.5236 against the recorded 0.5504, after fixing two
real bugs (glTF Y-up vs Blender Z-up; a pixel-row order flip) that had it off by
27 points.

**Correction:** that same axis bug was present in the diagnostic's coverage-proxy
maths, so the earlier "H2 not confirmed" test was **invalid**. H2 is nonetheless
refuted by stronger evidence — the variant recovers p1 to control level *through
the identical blend*, so the blend cannot be what destroys range.

Promoted `scripts/ai-pipeline/prop_tonal_audit.py` (committed) — decision-bearing
metrics belong in the repo.

**NOT shipped, and deliberately so.** Installing this means deleting
MaterialAnything outright (swap rule: code, venv, ~4.26 GB weights,
`models.sha256`, `check_models.py`, CREDITS), and the variant glb was built by
transcribed code, so the real path is changing `prop_texture.py` and re-running
its texture stage. A dependency deletion resting on one prop has a reasonable
alternative — validate wider — so it is a **user decision** (§6).

## Generalisation check — VERDICT: per-material, NOT deletion

6 of 7 props provenance-verified (5/5 or 6/6 per-view `gen_png_sha256` matches;
the `multiview_1024` decoy dirs correctly *failed*, proving the check can fail).
`candelabra_shrine` **disqualified — no cached `albedo.png`**, so metal is still
completely untested.

| prop | material | p1 lift | luma std drop | Lab a\* under delighting |
|---|---|---|---|---|
| chapel_arch | stone | 36.3× | 66.2% | 3.10 → 2.11 (down) |
| broken_column | stone | 4.4× | 64.8% | 1.94 → 1.73 (down) |
| gravestone | stone | 3.7× | 44.9% | 2.42 → 2.49 (flat) |
| crucero | stone | 4.4× | 53.7% | 2.07 → 2.05 (flat) |
| olive_stump | wood | 192× | 52.2% | 1.15 → 1.26 (flat) |
| **cypress** | **foliage** | **16.6×** | **6.4%** | **3.02 → 5.13 (UP)** |

**Stone + wood: the chapel_arch result is systematic, not a fluke.**
**Cypress breaks the pattern in kind** — std drop an order of magnitude weaker,
and chroma moves the *opposite* direction (atlas: shipped 2.87 vs variant 2.33,
i.e. the delit version is richer).

Physically sensible, which is why it is trustworthy rather than noise: on stone
the diffusion's dark pixels are mostly **real material** (soot, crevice stain), so
delighting destroys signal; on dense canopy they are mostly **inter-leaf
self-shadowing**, which is exactly what an albedo must not carry. Delighting is
doing its job on foliage and harm on stone.

**Consequence: do NOT delete MaterialAnything.** Deleting it on the stone
evidence would have broken the foliage path. The stone-family fix (bypass
delighting, blend from `gen.png`) looks safe to generalise; foliage rests on a
single cypress run and metal on none.

**OPEN — user decision.** How to express per-material delighting: a per-prop
pipeline flag mirroring the existing `--metallic`/`--roughness`/`--detail` idiom,
or something else. Then the stone props need their atlases rebuilt through the
real `prop_texture.py` (the A/B variants were built by transcribed code and must
not ship). Also unresolved: metal is untested, and the H4 inpaint share (45% of
the island, concentrated in exactly the occluded crevice geometry where soot
lives) is a separate contributor that bypassing delighting does not address.

## Rollout — `7999a60`

`broken_column`, `gravestone`, `crucero` opt in; subjects verified from each
`generation_manifest.json` before enabling (all three genuinely stone, all on the
dielectric-estimator path). **`candelabra_shrine` excluded on material grounds** —
its subject is dark grey weathered iron, and the shipped tile is limestone; an
opt-in that encodes what a surface *is* must not be handed the wrong material.
It would want a metal tile, which is a separate asset and a separate decision.
`stone_props_declare_detail` now asserts the full six-prop true/false split, so
the intent is encoded rather than sampled.

Goldens still exactly 0.0; offscreen 32/32; content_lint 13/13; workspace
422/422. `zone/wide` **byte-identical** even with three more props enabled — at
wide framing the fade has already retired the layer. No visible tiling grid on
any of the three: gravestone's and crucero's shafts are narrower than one 0.45 m
tile period, so a repeat never completes across the face.

Note: `tasks/` is gitignored (0 tracked files) — these notes are local working
state by design, not part of either commit.

**`prop_audit.py` is the wrong instrument for this phase** — it measures the
atlas, which this work does not modify. The instrument is the rendered normal
channel.

**Tile chosen: ambientCG Rock060** (CC0 1.0), 2048², NormalGL native. Rock063 was
rejected on inspection at 1:1 (moss/leaf-litter cliff face, non-square) and
Rock058 on hue (blue-grey slate). Albedo high-passed to mean luminance 0.5001;
normal at full native amplitude, std 37.4/28.4, mean X/Y 128.2/126.6.

**T9 watch item (orchestrator, from judging the tile at 1:1):** Rock060 is
natively a *cliff face*. At a 0.45 m period its fine speckle lands sub-mm — which
is what we want — but its strong vertical strata and major crack channels land at
~10–20 cm, i.e. ~6–7 visible repeats across a 3 m arch. The albedo high-pass
stripped low frequencies from colour; the **normal still carries that macro
structure**. If judge frame #2 shows a tiling grid, the ladder is: shorten the
period → high-pass the normal's low frequencies → hex-tiling (its named trigger).
Do not pre-emptively apply any of these.

## Rollout — broken_column, gravestone, crucero (2026-07-25, committed `7999a60`)

Plan named four follow-ups (`broken_column`, `gravestone`, `crucero`,
`candelabra_shrine`); only the first three enabled. **`candelabra_shrine`
excluded** — its subject is dark grey weathered iron (S7-F1), a material
mismatch with the shipped limestone tile; stays a separate future decision.

Subjects verified from each `generation_manifest.json` before opt-in, all
confirmed stone on the dielectric-estimator path (not the old scalar-roughness
path S7-F1 flagged): `broken_column` "broken stone column... weathered fluted
limestone" (metal_fraction 0.0441); `gravestone` "weathered stone wayside
cross... sun-bleached granite" (metal_fraction 0.0047); `crucero` "weathered
stone wayside cross, pale sun-bleached limestone" (metal_fraction 0.0241).

`set_material_extras.mjs vordar_detail` + `bake_textures.mjs gltf` re-run on
all three glbs. DDS pixel content is byte-identical (the extra is glb JSON
metadata only) — `git status` confirms only the 3 glbs + their
`manifest.json` sha stamps changed. `stone_props_declare_detail` extended to
assert the full split: chapel_arch + the 3 new props `true`;
candelabra_shrine/cypress/olive_stump `false`.

Verified: `content_lint` 13/13; all 3 goldens **exactly mean FLIP 0** (forced
thresholds negative to read the real number, reverted — `git diff` on
`golden.rs` empty — `UPDATE_GOLDENS` never set); offscreen 32/32; workspace
nextest 422/422.

Eyeballed via `asset_inspect` (studio+raking × beauty/normal/rough,
gameplay+macro) + `zone_review start`: all three show dense relief/pitting at
macro that reads as real mineral grain, not flat surfaces. No visible tiling
grid at gameplay framing on any of the three, despite gravestone/crucero being
narrower than chapel_arch (their shaft width sits under one 0.45 m tile
period, so the period's own repeat never completes across the visible face).
Rock060's vertical-strata macro structure (T9 watch item) is visible in the
narrow shafts' normal channel at macro distance as regularly-spaced vertical
crack channels, same character as chapel_arch's already-accepted read — not a
new defect, and it recedes into ordinary weathered-stone striation at gameplay
distance and in the dusk zone shots. `zone/wide` byte-identical to
`target/detail-phase/after/zone/wide.png` (mean abs delta 0.0, all 3 channels)
— these props sit in the start zone but at wide framing the fade already
retires the layer, same as chapel_arch's control.

---

# Phase 0 — inspection instrument (2026-07-24 →)

Plan: `~/.claude/plans/linear-swimming-nest.md` (approved 2026-07-24). User
directive: build better eyes BEFORE any texture fix. Three instrument defects
found while planning: D1 offscreen PNGs lack the sRGB transfer encode (live
swapchain is sRGB, offscreen target is `Rgba8Unorm`) — every review image ever
judged is ~2.2-gamma dark; D2 `rock_face_01` is placed at scale 4.0/3.2 so its
in-world density is ~38 px/m, a third of chapel_arch's — it is a *material*
control, not a density one; D3 no prop declares an `occlusionTexture`, so the
shader's AO input is white for every asset including the control.
Iteration subject for the later fix phase: **chapel_arch** (112 px/m, 1.20 M
inpainted texels, 136.68 m², every failure mode at once).

- [x] S1–S4. DONE. `debug_mode`@60 in LightUniform (offsets unchanged);
      `snippets/debug_channel.wgsl` included by both geometry shaders;
      tonemap `passthrough`/`encode` (encode = `!output_format.is_srgb()`,
      set once in `TonemapPass::new` → live path untouched);
      `set_debug_channel` + `DebugChannel`; bloom encode gated off for debug.
      **Identity proven: roughness 0.6 → G byte 153 exactly.** Goldens red by
      design (FLIP 0.409/0.477/0.477 vs 0.01), `actual.png` = clean uniform
      brightening, `UPDATE_GOLDENS` never set. [sonnet]
- [x] S4b. DONE. 4 non-golden offscreen tests also broke —
      `blend_material`, `bloom_threshold`, `sky_fog`, `point_light`. All
      assert **ratios or near-black byte thresholds**; sRGB expands near-black
      ~7× and compresses bright ratios. Fixed by decoding to linear at the
      assertion sites via a new `linear()` EOTF helper + linear variants of
      `channel_mean`/`mean_luminance`. **No constant changed value** — the
      proof it was a space fix, not a retune. 28/28 green. Correction to the
      orchestrator's diagnosis: the monotonic falloff assertion did NOT
      survive in byte space (h2=31.07 < h6=37.49, order reversed) — sRGB is
      monotonic pointwise but these compare *means over pixels*, and the mean
      of encoded ≠ encoded of the mean. Plan's claim that only goldens would
      break was wrong. [sonnet]
- [x] S4c. DONE (folded into S5). Hit the anticipated wall: `debug_channel()`
      needs `light.debug_mode` and `tonemap.wgsl`'s bind group has no `light`
      uniform. Took the pre-authorized alternative — `srgb_oetf` became its
      own snippet included by both. `tonemap.wgsl` now preprocessed (7th) and
      naga-parsed by `generated_shader_tests`; `wgsl_hook.mjs`'s STANDALONE
      set updated to match its new category.
- [x] S5. DONE. `engine-renderer/src/review.rs` holds the 4 helpers; 5 copies
      deleted (4 bins + `golden.rs`). All 4 reconciliations held: `aabb` takes
      the slice form, `ground_quad` takes `extent` (40.0 / 100.0 NOT unified),
      `skin_to_pose` tolerant early-return, `contact_sheet` resamples only on
      size mismatch. **−217 lines net.** turntable CLI + output filenames
      unchanged (smoke run: 4 frames + sheet); zone_review still runs;
      offscreen 28/28. `golden.rs` dedup sequenced last and proven inert —
      FLIP identical to 8 decimals (0.40897626 / 0.47708878 / 0.47746462
      before AND after). [sonnet]
- [x] S6. DONE. `asset_inspect` bin. Verification sweep on chapel_arch:
      **28 sheets, 336 frames**, none missing/flat/blank. Measured, not
      assumed: `studio/rough` 129–155 per frame (mean 141.6 ≈ atlas 0.572×255
      minus mip-filtered partial-visibility), `studio/ao` **255 everywhere**
      (D3 confirmed), `studio/metal` 0 everywhere, ground swatch roughness
      **229** (f32 0.9 → 229.4999 rounds down, not 230). Plan self-contradiction
      caught by worker: its Channels table said the albedo swatch reads 128, but
      its own JC-2 sRGB-encodes albedo in-shader → **188**. JC-2 is what shipped.
      `full` distance has 0% alpha coverage (GROUND_EXTENT=40 fills frame) — the
      alpha geometry-mask only pays at gameplay/macro. [sonnet]
- [x] S7. DONE. `scripts/ai-pipeline/prop_audit.py` — all 10 props, ~24 s,
      no thresholds/no gate. Reproduced every pinned value independently
      (crucero flat_frac 0.298 vs 0.299 = the only delta, inside ±0.01);
      `placed_px_per_m` 38.4 for rock_face_01 (D2 confirmed); `ao_bound`
      false on every row (D3 confirmed). Two NEW findings below. [sonnet]

  **S7-F1 — the waxy roughness is the MaterialAnything estimator.**
  `candelabra_shrine` measures roughness 0.824 (control 0.882) because its
  manifest shows the OLD scalar path: `roughness: 0.8`, `metal_roughness:
  0.9`, `mr_mask_bake_s` (the deleted `--mr-mask` pass), no `dielectric`,
  no `metal_fraction`. chapel_arch/crucero/broken_column all carry
  `dielectric: True` + `metal_fraction` — i.e. `prop_pbr.py`'s per-texel
  estimate — and land at 0.543–0.658. The prop that reads correctly was
  *told* 0.8, never estimated. Clean existence proof for the **roughness**
  axis; the estimator is the named regression.

  NOT evidence for the albedo axis — candelabra's subject is "dark grey
  weathered iron" while the failing three are "sun-bleached limestone", so
  the albedo comparison is confounded by subject. The albedo defect stands
  on its own terms instead: `albedo_luma_p1` 0.406 means the *darkest 1%*
  of texels is mid-grey, on prompts that explicitly specify "soot-darkened
  carvings" over crevice-heavy geometry. No soot, no crevice darkness
  anywhere in the atlas — measured against the prop's own brief.

  **S7-F2 — `broken_column` is the worst atlas, not chapel_arch.**
  hole_frac **0.466** (47% inpainted) and albedo_luma_p1 **0.510**, both
  worst in the set; atlas_px_per_m 107.3, lowest. But it is still a 1024
  atlas, so it has an untried lever (→2048) that chapel_arch has already
  spent. Iteration subject stays **chapel_arch**: 2048 already and still
  112 px/m over 136.68 m² (3.3× the column's area), worst normal flatness
  0.263, albedo p99 0.989 (near-clipped), and it needs architectural
  precision. Fixing it requires solving the problem, not pulling a lever.

  Also recorded for the fix phase: `rock_07`/`rock_09` carry real AO data
  (ao_mean 0.806/0.771) that the renderer never reads (ao_bound false), and
  sit at 836/1676 placed px/m — pebble atlases stretched onto boulders.
- [x] S8. DONE. README subsections for `asset_inspect` + `prop_audit.py`.
- [x] Gate CLOSED 2026-07-24. Workspace run: **exactly 1 target failed,
      `golden.rs` (3/3), by design** — all else green (offscreen 28, client 53,
      game 63, server 38, protocol 12, e2e/persistence/security/wireformat/
      shutdown/watchdog/zones, content_lint, ui_snapshots). User regenerated the
      goldens (`$env:UPDATE_GOLDENS = "1"; ...; Remove-Item Env:\UPDATE_GOLDENS`)
      and confirmed 3/3 pass on a clean re-run. No second workspace run: the only
      delta was those 3 PNGs, so no other target could have moved — see
      `tasks/lessons/2026-07-24-never-double-run-a-suite.md`.
      **Tree is UNCOMMITTED** — 21 modified + 5 new files, nothing committed
      (user hasn't asked). New: `review.rs`, `snippets/debug_channel.wgsl`,
      `snippets/srgb_oetf.wgsl`, `bin/asset_inspect.rs`, `prop_audit.py`.

## Instrument validated (orchestrator vision pass, chapel_arch @ studio/macro)

The rig immediately showed what 512² amber turntables could not:
- **Zero micro-relief.** Smooth cream sweeps, no grain/pitting/mineral
  variation. Reads as wet clay or unfired ceramic, not limestone.
- **Faceted low-poly geometry with nothing hiding it** — raking light makes
  the facet boundaries and hard edges unmissable.
- **All apparent "detail" is blurry stains painted into the albedo** (the
  inpaint filler); the normal map contributes nothing visible, which is what
  26.3% dead-flat normal texels looks like from outside.
- Control `rock_face_01` at the same framing: mineral banding, lichen, ochre
  oxidation, crumbled strata — and visibly stretched at its placed scale 4.0,
  confirming D2 in the image as well as the number.

## Fix phase — findings (do NOT start before /compact)

Full record: `tasks/ai-pipeline/chapel-arch-fix.md`. Re-derived this session,
island-masked (F-2); two Phase-0 hypotheses corrected, one overturned.

F-1 — the normal bake is NOT a no-op; it fired correctly, but the hires cage
carries almost no relief (773k tris add only +0.7% area over the decimated
mesh). Overturns "26.3% dead-flat normals" / "bake is a no-op": in-island
25.4% dead-flat is correct output where the hires surface equals the clean
one, not the bake failing.
F-2 — `prop_audit.py`'s normal/albedo/roughness stats ran over the whole
atlas (island covers only 42.3%), which is why chapel_arch vs rock_face_01
was never like-for-like. Fixed in F0 (island masking).
F-3 — MaterialAnything's bump head is estimated and discarded every run
(`prop_pbr.py:83`); it is the only stage that predicts sub-cm relief.
F-4 — shipped material: in-island roughness mean 0.572/std 0.102, no
roughnessFactor correction (ships at estimator-raw 0.572); albedo p1 0.395;
no occlusionTexture.
F-5 — regeneration is the wrong lever (hires cage +0.7% area, ±8 mm
deviation from the 15k decimation); GPU spent there buys nothing F1–F3 don't
buy for free.
F-6 — coverage (blend_coverage 0.5504) is scattered residue, not one big
unseen soffit; the greedy extra-view search already found the one view
worth adding (+5.29%).
F-7 — atlas utilization 0.409 (xatlas packed at 1024 while the bake ran at
2048); repacking could reach ~124 px/m, modest.
F-8 — `target/fix-phase/before/*/macro_01.png` frames empty ground (subject
out of frame at angle 01, macro); exclude angle 01 at macro from before/after
judging on either side.

Ranked causes: (1) ~45% no micro-relief anywhere in the asset, (2) ~25%
roughness 0.572 on limestone reads as wet clay, (3) ~20% no crevice darkness
/ no AO, (4) ~10% naked facets (15k tris, 13.5 cm mean edge), (5) inpaint
smear + chart seams (share not separable from (3) yet).
Subject: chapel_arch only, per the user's "one model" directive.

## Fix phase — execution log (2026-07-24/25). SESSION ENDED BY USER.

- [x] **F0 — island-masked audit.** `prop_audit.py` stats now island-only
      (unmasked variants deleted); `ao_mean` reads the occlusion slot, ARM-red
      reading deleted; `island_frac` column added. Verified: island_frac 0.423,
      normal_flat_frac 0.253, normal_lap_std 0.188, albedo_luma_p1 0.395,
      roughness_mean 0.572, ao_bound false. All 10 props print, 25.5 s.
      Worker hit a UV V-axis convention mismatch (glTF V-down vs bake V-up) and
      fixed the bug rather than tuning toward the target number.
- [x] **F1 — estimated MR path deleted, scalar roughness shipped.** 0 GPU.
      `roughnessFactor 0.85` / `metallicFactor 0.0`, no metallicRoughnessTexture,
      mr atlas image deleted. `--dielectric`, `metal_fraction`, the rm.png blend
      and the MR material wiring removed from `prop_texture.py`/`prop_pbr.py`/
      `gen_prop.py`/README. **Judge: waxy translucency gone, surface still reads
      as smooth ceramic** — the plan's own F1 gate ("the problem is not the
      level, F3 is where it lives"), so no retune.
- [x] **F2 — AO authored and bound.** 0 GPU. Cycles AO bake from the hires cage,
      128 samples, `AO_DISTANCE_M = 0.15` (voussoir-joint scale, set once on
      physical grounds). Two real bugs found: Blender's glTF exporter has no
      BSDF occlusion input (needs a `glTF Material Output` group), and
      `prop_audit.py` looked up slot `"occlusion"` while `bake_textures.mjs` has
      always emitted `"ao"` — so **`ao_bound`/`ao_mean` had never computed for
      any prop**. `ao_mean` 0.538, outside the planner's 0.70–0.90 band; NOT
      tuned. Judge confirmed why: at gameplay distance AO is near-white across
      faces with fine dark lines in the masonry joints and undercuts; the
      near-zero third of island texels lives on interior/back faces that never
      render. Glb 12.49 MiB.
- [~] **F3 — micro-relief. FAILED. This is a design wall, not a tuning gap.**
      GPU 49.4 s (G1, matching the 44.6 s anchor); ComfyUI canvases stayed
      resumed at 0 GPU.
      - **MaterialAnything's bump head is blank** — island-masked mean
        (129,127,255), std 4–6/255. It is not under-used; it predicts nothing.
        The plan's whole premise for cause (1) was that this output existed.
      - Fallback (albedo high-pass → Sobel → UDN composite) shipped instead.
        **`normal_lap_std` 0.188 → 0.382, clearing its ≥0.25 target and beating
        the control's 0.270 — with no visible change in any rendered frame.**
        `normal_flat_frac` 0.251 vs a 0.05 target; 98.4% of dead-flat texels
        stayed flat. Where it does fire it sources contrast from the inpaint
        smears, i.e. it embosses an artifact into relief.
      - **Resolution ceiling (orchestrator, decisive):** 2048² over 136.68 m² at
        42.3% utilization = **8.9 mm per texel**. Limestone grain is 1–3 mm.
        Carrying it would need ~18,000² (80× the texels). **No atlas-space
        approach can ever hold this detail** — not the bake, not the bump head,
        not any height source or amplitude constant.
      - **Correction to the Phase-0 read:** `rock_face_01` reads as stone mainly
        because its *albedo* carries photographic micro-contrast — it wins at
        38 px/m, a third of chapel_arch's density. The gap was never primarily
        normal-map relief. Our albedo is diffusion-generated: smooth, blurry,
        stain-like.
      - **F4 and F5 cannot address cause (1)** — denser mesh removes faceting,
        better view coverage removes seams; neither puts grain on a surface.

**Asset state:** F3's composite is STILL SHIPPED (glb 14.24 MB). The user was
asked whether to revert it and chose to leave it pending ("maybe keep both...
enough changes today"). **Decide before F4/F5/F6.**

**User ruling 2026-07-25, standing:** *"we want quality at any cost (of time,
coding or changes) so go for the best outcome solution, if we need to check for
tools and replace technologies we go for it, we need the quality."* This lifts
the incremental-fix framing — replacing Hi3DGen, the multiview texturing stack,
or both is now on the table.

**Resume point (next session, after `/clear`):** the ceiling argument says the
fix is either (a) a world-space tiled detail normal + detail albedo, sampled at
its own frequency independent of atlas density, or (b) a texturing stack that
produces albedo with real micro-contrast — or a technology replacement that
delivers both. That question is unresolved and is the first thing to plan.
`tasks/ai-pipeline/chapel-arch-fix.md` F4/F5/F6 are NOT invalidated as
seam/facet work, but they are no longer a path to the AA bar on their own.

**Judge artifacts kept:** `target/fix-phase/{before,f1,f2,f3}/` — 1024² frames,
studio+raking × beauty/normal/rough/albedo/ao, gameplay+macro, 4 angles, with
`ref_` photoscan control. Exclude `*/macro_01.png` (F-8).

# Unsupervised GPU block (2026-07-24, user away; plan approved = §8 go-ahead)

Plan: `~/.claude/plans/reflective-stirring-blossom.md` (approved 2026-07-24).
Decisions locked with user: concept-base A/B on the crucero (loser deleted per
swap rule); B4 runs in full to the feel-check boundary (KayKit/old-glb deletion
stays user-gated). GPU ≤60 min ceiling (~35 nominal). Facts corrected during
planning: multiview is ALREADY Z-Image (`c675a23`, 2026-07-20 — the B3 "SDXL
multiview" note was stale; only the concept stage runs SDXL); branch is level
with origin (the "~70 unpushed" note below is stale).

**STOPPED early — Fable 5 tier hit its usage limit mid-P2 (crucero placement
worker died on the limit). User asked to save state + report. Session paused
here, NOT completed. Remaining work below is unstarted or parked.**

- [x] P1. Z-Image t2i concept graph + crucero A/B + swap-rule erasure — DONE,
      committed 1451bfb. A/B ruled Z-Image (single-object framing 3/3 vs SDXL
      1/3); prop_concept.json now the Z-Image t2i graph, SDXL concept path
      deleted per swap rule; models.sha256 + check_models.py gained 4 Z-Image
      + 4 Qwen-fallback hashes (check_models exit 0); stale SDXL comment/help
      strings reworded base-agnostic; README inventory fixed.
- [~] P2. Q6 crucero — MOSTLY DONE. 3 candidates through full chain @2048/1536;
      winner cand_21 (flared-arm cross, clean 8 angles, dielectric) installed
      at content/models/props/crucero/ with DDS bake + CREDITS + manifest,
      committed acc19a8. **Placement into zones.ron NOT done** — the fable
      worker dispatched for it died on the Fable limit. Crucero is installed
      but unplaced (zones.ron unchanged). ← resume point.
- [x] P3. B3 batch gate machine side — DONE (2026-07-24). Fresh zone_review
      both zones (crucero now in-scene); orchestrator re-reviewed vs the 3
      complaints — all clear (matte stone/no gloss, close-ups crisp, crucero
      monument scale correct). nextest 414/414 + doc tests green. b3.md gate
      stays CLOSED-except-user-walk; crucero folded into that open re-walk box.
      Player-mannequin skin still bright = the carried B4 overexposure flag.
- [~] P4. Bench baseline quiet-box re-save — DEFERRED + LEDGERED (2026-07-24).
      RustRover is open (2.3 GB) with cargo indexers live; my file edits trigger
      re-index bursts. BASELINE.md warns background CPU pushes criterion noise to
      ±25%, swamping the 10% gate — a baseline re-saved under that taint silently
      corrupts the regression gate. Reversible path: park it; the current `main`
      baseline stays valid. NEEDS a confirmed-idle box (close RustRover or pause
      indexing), then: `cargo bench -p vordar-benches --bench snapshot --
      --save-baseline main` + one `scripts/bench-gate.ps1 -Bench snapshot
      -Threshold 0.10` smoke + BASELINE.md caveat/date bump. User-side condition.
- [ ] P5. Phase B4 subplan (fable → tasks/ai-pipeline/b4.md) then execution
      to the feel-check boundary (CPU-only; monk swap + 3 themed races +
      outfit/tint + overexposure fix); ONE nextest at B4 gate.
      **b4.md subplan was WRITTEN this session (9 tasks + 1 deferred + gate);
      execution NOT started.**
- [ ] P6. Wrap-up: ledger, todo/memory GC, push green commits, user report +
      feel-check checklist — NOT STARTED. NOTE: user constraint this session
      was **do NOT push** — the 2 landed commits (1451bfb, acc19a8) stay local.

# AI-setup upgrades — 7 research items + reference/ exclusion (2026-07-23 →)

Plan: `~/.claude/plans/wondrous-moseying-brooks.md` (approved 2026-07-23).
Source research: AI-setup report, session 8c040e2d. Decisions locked: D1 tracked
settings.json; D2 3 golden scenes, zone deferred; D3 Task Scheduler + committed
reports; D4 global ccusage; D5 push ClaudeConfig per commit; reference/ excluded.
Orchestrator dispatches per task (tier in brackets), verifies by re-running the
verify command, commits on green. ONE workspace nextest run at the phase gate.

- [x] T0. reference/ exclusion: .obsidian/app.json + .gitignore + CLAUDE.md line [haiku]
      (vordar 395c8c0; ClaudeConfig 3fda7aa pushed; finding-worker.md dirt untouched)
- [x] T1. settings.local.json allowlist prune 123 → 11 [haiku] (second pass also
      collapsed shadowed Read(...) set + bare Bash/PowerShell dupes; gitignored, no commit)
- [x] T2. hook scripts (comment_lint / wgsl / deny_dangerous) + naga-cli [sonnet]
      (48882d5; naga 30.0.0 installed; full stdin matrix green. Ledger: hooks
      degrade to exit 0 on stdin-encoding mismatch — UTF-16 pipe test proved the
      degrade path; T5 fresh-session smoke is the authoritative live proof)
- [x] T3. tracked .claude/settings.json hooks config [haiku] (ClaudeConfig 8df13b6)
- [x] T4. WGSL parse test += sky.wgsl [haiku] (3b053cb; test + comment renamed
      preprocessed_shaders — sky isn't geometry, name had gone stale)
- [~] T5. finding-worker erasure + nested commits DONE (edd09aa: clippy gate in,
      lint-comments prose out; pushed) — fresh-session live-fire smoke PENDING
      at the phase gate (hooks load at session start)
- [x] T6. golden.rs harness + 3 scenes + initial goldens (nv-flip 0.1.2) [sonnet]
      (bb8b4c7; all 3 scenes shipped incl. skinned human; goldens eyeballed OK.
      Ledger: worker's "pre-existing workspace check failure" was a stale
      incremental build — cargo clean -p engine-renderer fixed it, canonical
      gate green; the 2026-07-05 lesson applied, not feature unification)
- [x] T7. threshold calibration + negative control [sonnet] (noise floor ZERO —
      bit-identical across 5 independent renders; thresholds 0.01 floor; 2° sun
      nudge fails at 0.055; committed)
- [x] T8. golden gate wired into finding-worker.md [haiku] (ClaudeConfig 102979f;
      insertion point fixed inline — worker split the paste-real-output sentence pair)
- [x] T9. ccusage statusline (user settings merge) [haiku] (ccusage 20.0.18
      global; statusLine merged into user settings.json, all keys preserved;
      renders cost/burn/context — visible from the next session)
- [x] T10. egui_kittest 0.34.1: 2 UI snapshots, trial [sonnet] (03004a7; zero
      src changes needed; snapshots eyeballed — real minimap/action-bar content;
      kill criterion in module header: >2 spurious regenerations = trial failed)
- [x] T11. bench-gate.ps1 + snapshot baseline, trial [sonnet] (committed; clean
      run max-delta 4.7% exit 0, negative control +66% exit 1. Ledger: worker
      caught PS5.1 scalar-collapse bug that made the gate always-pass; box was
      running Palworld → ±25% noise, quiet-box caveat added to BASELINE.md,
      baseline needs a quiet re-save before the gate is trusted)
- [x] T12. bench gate wired + baseline-refresh rule [haiku] (ClaudeConfig
      e2c0769; gate in finding-worker step 5, refresh rule in run-queue only)
- [x] T13. token-report.ps1 + weekly Task Scheduler job [sonnet] (5108e17;
      VordarTokenReport Sundays 09:00, next 26/07; first report committed —
      week-to-date $476.87 / 410M tokens, cache hit 97.5%. Ledger: dropped
      ErrorActionPreference=Stop — PS 5.1 turns native stderr into exceptions)
- [~] Phase gate 2026-07-23: verifies re-run per task ✓; ONE nextest run
      413/413 green (incl. 3 golden + 2 ui-snapshot tests) ✓; erasure sweep
      clean ✓; ledger delivered ✓. PENDING (user, fresh session): hooks
      live-fire smoke (T5), statusline visible, Obsidian reference/ gone;
      quiet-box bench baseline re-save before first real gate use.

# MaterialAnything per-view PBR decomposition (2026-07-22 →)

Plan: `~/.claude/plans/snazzy-scribbling-alpaca.md` (approved 2026-07-22).
Branch: `ai-pipeline`. Goal: delit albedo + per-texel roughness/metallic via
MaterialAnything's estimator on each multiview view; `--mr-mask` pass deleted.

- [x] 0a. Install (2026-07-22): clone @ `be3d6b3` → `C:\tools\MaterialAnything`;
      venv py3.11.9 (torch 2.7.1+cu128, diffusers==0.28.2, transformers 4.42.4,
      huggingface_hub 0.25.2 + accelerate 0.31.0 — both pins REQUIRED, newer
      hub removed `cached_download`); weights 4.26 GB; import smokes pass
- [x] 0b. Conventions pinned from clone (full report in session): normal =
      camera-space OpenGL encoding (+X right/+Y up/+Z toward cam, n*0.5+0.5,
      WHITE bg); RGB cond = white-bg composite, exactly 768² (pipeline never
      resizes); masks = RePaint KEEP-mask (1=pin to init, 0=estimate);
      init_materials = all-white (1,768,768,3) ×3; 13ch = 4 noisy + 4 RGB
      VAE + 4 normal VAE + 1 raw mask; outputs [albedo, rm(G=rough,B=metal),
      bump]; upstream seeds Generator(0), cfg 1.0, 50 steps
- [x] 1. `prop_pbr.py` written (runner, resume gate, pbr_meta.json, seeded
      seed*1000+i)
- [x] 2. `prop_texture.py`: `_ortho_camera`/`_render_exr` factor,
      `_normal_setup` + `render_normal_views` (normal_<i>.png + mask_<i>.png),
      `estimate_materials` subprocess (stdout captured — protects the
      '{'-stats-line contract), `blend_views(filename, srgb)`,
      `pbr_multiview` (albedo → basecolor, rm → MR atlas, metal_fraction)
- [x] 3. Deletions done: `mr_multiview`, `--mr-mask`, `--metal-roughness`,
      `MR_MASK_SMOOTHSTEP_EDGES`, `DEFAULT_METAL_ROUGHNESS`, MR block in
      main, gen_prop plumbing; repo grep clean (only historical
      generation_manifest.json records remain, deliberately kept)
- [x] 4. Docs: README multiview section + MaterialAnything venv install;
      CREDITS ledger row added
- [x] 5. Verify batch DONE (sonnet worker, all substantive asserts PASS):
      fresh run 2m20s exit 0 — textured.glb embeds basecolor+normal+packed
      MR (3 images), albedo visually delit vs gen.png, rm two-tone with real
      structure, metal_fraction 0.2687, extra view az0/el-35 picked, no
      scalar-MR keys in stats; resume 18.3 s, no ComfyUI start, shas
      identical; gen_prop --through texture end-to-end exit 0 (skips
      concept/geometry/cleanup, texture_stats has pbr_estimator, no mr keys);
      deletion sweep zero matches. Two apparent failures resolved as
      non-bugs: (a) coverage 0.6589 vs "baseline" 0.6526 — the baseline run
      used oblique --azimuths 0,60,180,300 (verified in stats1.json), batch
      ran default 0/90/180/270; geometry reproduced EXACTLY across the two
      fresh dirs in-batch; (b) generated/estimated pixels differ across
      fresh dirs at same seed (GPU kernel nondeterminism) — same-dir resume
      is exactly deterministic, which is the pipeline's actual guarantee;
      per-run provenance shas already model this
- [x] 6. Commits: `8feb605` (prop_pbr runner), `2dfb79d` (prop_texture swap
      + gen_prop + README + CREDITS ledger row); shortlist + design note
      struck. PENDING: user feel-check of SP\pbrtest\textured.glb

Decided while unsure (deliver at phase gate):
- Mask A/B DISSOLVED (not run): the plan's A/B assumed the mask meant
  "trust the lighting"; the clone's code shows it is a RePaint keep-mask
  (1 = pin latents to the white init materials, 0 = estimate). Only one
  sensible standalone construction exists — estimate over the object,
  keep the white background — which is exactly upstream's first-view call.
- Per-view estimator seeds use our deterministic seed*1000+i instead of
  upstream's hardcoded Generator(0) — provenance-tied and per-view unique;
  any fixed seed is equally valid to the model.
- Estimator rm R channel dropped when packing the MR atlas (glTF ignores
  R in metallicRoughnessTexture; upstream also discards it).
- Estimator bump output discarded — the stage's real high→low normal bake
  is geometric ground truth (in-plan, restating).

---

# AI asset pipeline + Spanish-religious pivot (campaign, 2026-07-18 →)

Plan: `~/.claude/plans/zesty-bubbling-acorn.md` (approved twice: initial + license-verification revision).
Subplans: `tasks/ai-pipeline/a0.md`–`a3.md` — all struck green.
Branch: `ai-pipeline` (rebased onto docs/mastery-skills — 299 commits of finished
pipeline work lived there, not on stale main; pushed to origin).

- [x] Phase A0 — infra + governance: ComfyUI 0.28.0 headless + 38.6 GB models,
      TRELLIS 1 native install (stable-projectorz fork), turntable render tool,
      comfy_run.py (provenance manifests), check_models.py, fetch_polyhaven
      hdris/textures, 26-row license ledger in CREDITS.md (EU-safe verdicts)
- [x] Phase A1 — materials: gen_material.py (StableMaterials 512-native +
      chained SDXL img2img hops, cpu_offload mandatory, seam gate),
      render_material bin, cracked_earth 2k fixture (vision-approved).
      Lesson: only 512-native previews predict structure; 2048 ≈ 4.5 min/set
- [x] Phase A2 — HDRIs: 3-way pano bake-off → circular-x SDXL wins (gen_pano_
      sdxl.py, license-unconditional); hdr_post.py (LDR→HDR + sun injection,
      f16-safe); castilian_plateau_dusk_2k.hdr fixture (vision-approved);
      Diffusion360 kept as alternate; sdxl_360 blocked at seam gate
- [x] Phase A3 — props (2026-07-19). STRICT NC RULING: nvdiffrast never in
      the production path → backbone switched to Hi3DGen (MIT, geometry-only)
      + Blender projection-bake texturing; TRELLIS demoted eval-only (its
      xformers blocker fixed for the E1 baseline). Chain: prop_hi3dgen →
      prop_cleanup → prop_texture → preprocess_prop → gen_prop (resumable).
      candelabra_shrine fixture committed (winner of 4 candidates, 3 review
      passes, 2 real defect fixes: alpha-matte handoff + MR sRGB double-
      encode). ~18 min GPU. Post-gate (2026-07-19, user-funded): Strategy 2
      multiview ControlNet-depth retexture shipped (~1.5 min GPU, T rows) —
      near-black iron, roughness 0.65 (`c58bc7d` + `028ca57`); multiview is
      now a documented prop_texture strategy for register-critical props
- [x] Phase A4 — characters (2026-07-19 → 2026-07-23): rig = canonical-
      skeleton transplant (never generated); AI chain (Hi3DGen + SkinTokens
      skinning) built and green but its candidates fell below the bar at the
      A4.11 gate → MPFB2 hybrid rung won: parametric CC0 monk with authored
      weights (`char_mpfb.py`, `gen_character.py --mpfb`), user-accepted
      2026-07-23. Fixture at `content/models/characters/human_gen/`, lint
      10/10, held for B4's swap. Phase gate CLOSED — a4.md all boxes; ~28
      min GPU vs 36 nominal. Iteration backlog: elbow-flexion shrink, robe
      texture budget (a4.md step-4 block)
- [x] Phase A5 — VFX atlases — SKIPPED (user ruling 2026-07-23): B5 covers
      VFX in the new register; atlas tooling gets built if/when B5 wants
      bespoke shapes
- [x] Phase B1 — direction lock (2026-07-23): visual-quality.md rewritten
      (`8487584`), RON lore reskinned (`03ebef8`), character-direction-notes +
      AA-plan Phase 5 superseded; gate closed — user text review PASSED, VQ-A4
      HSV table approved as-is (now the locked generation targets). Subplan:
      `tasks/ai-pipeline/b1.md`
- [x] Phase B2 — environment swap (2026-07-23): start zone → cracked_earth
      ground + castilian dusk HDRI, fog/palette retuned to the HDRI horizon,
      directional key aligned to the baked sun (az 263.1° el 8.0°). User
      ruled regenerate-fixtures at the go-ahead; both incumbents won the
      side-by-side selection (HDRI seed 7, cracked_earth seed 1 kept).
      worn_cobble set generated + committed unreferenced, held for B3;
      mud_leaves/evening_road deleted (d58ed4f ruling). ~15 min GPU vs ≤26
      approved. Commits `6741ff5`→`0c1cb1a`; subplan `tasks/ai-pipeline/
      b2.md`. Gate closed except user sandbox feel-check (big-visual-jump
      boundary — fog/palette tunable there, VQ-A4 targets not)
- [x] Phase B3 — props + zone dressing (2026-07-23, one session): 5 props
      generated through the full chain (12 candidates, zero geometry
      reseeds, 1 retexture) and installed — chapel_arch, broken_column,
      stone_cross, cypress, olive_stump; start zone re-dressed (14
      placements, dead_quiver roles taken over); east zone resurrected
      with worn_cobble + portal pair + tilt-derived fog; dead_quiver_trunk
      deleted; portal re-themed candle-gold with the lint hue assertion
      flipped in the same commit. ~58.8 min GPU vs ≤112 approved. Commits
      `3958522`→`6ded883`; subplan `tasks/ai-pipeline/b3.md` (Decision
      log + 11-item ledger). Gate closed except user feel-check
- [ ] Phase B4–B5 — characters (human_gen monk swap, held from A4), VFX

## Standing rules established this campaign (also in .claude/CLAUDE.md §6–9 + memory)

- Model routing by thinking depth: high/medium=fable (opus dropped), low=sonnet,
  none=haiku. Subplanning is always fable.
- Batched tests: one workspace run per phase gate, cheap local checks per task.
- Heavy GPU generation needs user go-ahead; approved subplan budget = the go-ahead.
- Uncertain decisions → ask; "decided while unsure" list at every phase gate.
- Workers: foreground commands only (background shells die silently — 3×).
- Compact at every phase gate (and at ~150k context mid-phase, unless the task
  needs it): persist state to files, then prompt the user to /compact.

# B3 prop-quality fix batch (2026-07-23 →, user-approved incl. ~10–15 min GPU)

User's B3 feel-check FAILED on the props (metallic gloss / far-LOD
close-ups / stone_cross oversized). Measured causes in b3.md gate note;
lesson: tasks/lessons/2026-07-23-review-in-engine-at-gameplay-framing.md.

- [x] Q1. Roughness bug FIXED (`2e58874` + `a2205b3`): root cause was
      NOT in the blend — Blender stamps sRGB chunks on Non-Color PNG
      exports and texconv honors the chunk over the requested format,
      sRGB-decoding linear MR AND NORMAL data at DDS bake. Fix:
      --ignore-srgb on mr/ao/normal slots; --dielectric opt-in flag
      added. column/cross/stump rebaked+reinstalled: roughness within
      0.03 of estimator, metal 0, normals ~0.5. Exact roundtrip probe
      + lint 10/10; verified. [sonnet]
- [x] Q7. Corruption sweep DONE (`427cacc`): mechanism is WIDER than the
      fix commit's message — texconv/WIC assumes sRGB for ANY source
      that can't declare otherwise (JPEG has no chunk mechanism), so the
      Poly Haven rocks were affected too (rock_07 roughness shipped
      0.071!). Affected+rebaked to source-exact: candelabra, rock_07/
      09/face_01 (normals+MR). Clean (measured): human_gen, human,
      statue_vroid, both ground sets (PIL/gltf-transform PNGs, no
      chunk). Committed fix covers the wider mechanism unchanged.
      Pre-existing out-of-scope note: rocks' AO channel unwired.
- [x] Q2. zone_review bin DONE (`13298f8`): both zones render (wide/mid/
      close + player for scale, real zone lighting); its evidence
      independently reproduced all three user complaints. Small library
      seams: Camera::look_at + set_camera_lookat, SUN_DIR/SUN_COLOR pub.
      New flag for B4: player skin overexposes under the dusk key
      (reproduced vs gear_render's neutral light).
- [x] Q3. arch + cypress at 2048 DONE (`e30d3ce` + `96890ff`): px/m
      372.6/293.2 (was 186/147; candelabra 629.5), roughness/normals
      source-true, metal 0, heights unchanged, 10.1 min GPU. Worker
      surfaced two real walls instead of patching: atlas lever is
      prop_texture TEXTURE_SIZE (orchestrator authorized --texture-size,
      forced by verified CLI facts), and preprocess --max-dim 1024 was
      silently undoing the 2048 (threading pre-existing flags; byte cap
      16 MB per character-chain precedent — mislabeled VQ-B2 comment
      flagged). DDS dims re-verified by orchestrator. [sonnet]
- [x] Q4. gravestone rename DONE (`7fd04a3`): clean git renames (glb sha
      matches manifest — DDS byte-identical), CREDITS renamed with the
      rename note, START gets a 3-stone graveyard cluster by the chapel
      (effective 1.54–1.65 m), field-edge + east placements deleted with
      their comments. Lint 10/10; verify re-run green.
- [~] Q6. Crucero STOPPED BY USER 2026-07-23 mid-concepts (both first
      draws failed single-object framing; re-rolls not run). No repo
      changes — zones currently ship NO wayside cross (gravestone
      placements were removed by Q4; nothing dangling, lint green).
      BEFORE resuming: resolve the image-base question below — the
      crucero should be the first prop generated per the current ruling.
- [ ] OPEN (user flagged at session end): B3/Q6 ran SDXL concepts +
      SDXL ControlNet-depth multiview despite the 2026-07-20 Z-Image
      image-base ruling (trainability; Qwen fallback; 3 recorded
      constraints — see memory image-base-zimage.md). Next session:
      check the multiview/ControlNet stage against those constraints,
      decide swap vs documented divergence; concept stage likely swaps.
      Lesson: tasks/lessons/2026-07-23-recheck-standing-rulings-on-reuse.md
- [ ] Batch gate (Q1–Q4, Q7, Q3 all committed; PENDING): fresh
      zone_review renders of both zones + orchestrator re-review against
      the three user complaints; ONE workspace nextest run; user re-walk.
      Held until the Q6/image-base decision so the gate runs once.

# Feel-check fix batch (2026-07-23 →)

B2 feel-check PASSED (environment approved, no retunes) but reported three
defects, all pre-B2 subsystems. One workspace test run at batch end (§7);
orientation fixes verified by eyeballed offscreen renders, never the GUI.

- [x] F1+F2. Gear orientation [sonnet] (`1613704`): root cause was NOT the
      presumed KayKit bake (that path is gone — VRoid human since 6cc1ace);
      sword/shield are runtime attachments in weapons.rs whose grip-local
      was Mat4::IDENTITY, and both handslot bones carry near-vertical local
      Z. Fix: named grip-correction rotations (sword 90° roll about blade
      length; shield cyclic axis permutation) composed at spawn. New
      offscreen gear_render review bin (mirrors turntable.rs pattern).
      Before/after renders eyeballed by worker AND orchestrator: blade edge
      vertical, shield upright facing outward. Goldens untouched (golden
      renders human.glb without gear).
- [x] F3. Camera below ground [sonnet]: eye height floored at MIN_EYE_Y=0
      inside `recompute_eye()` (single funnel for orbit+zoom; ground top is
      −0.5 so 0.5 m margin, engine stays free of client constants); sweep
      test over 4 radii × full pitch walk, every step asserted. Verify
      re-run by orchestrator: engine-renderer camera:: 3/3 green.
      Committed `cf5fe85`.
- [x] Batch gate CLOSED 2026-07-23: ONE nextest run 414/414 green (413 +
      the new camera sweep test); no golden regen needed; commits
      `cf5fe85` (camera) + `1613704` (gear). Pending user re-feel-check of
      grip/shield/camera next time they run the sandbox — bundled into
      B3's gate walk, no separate stop.

## Next session (session ended 2026-07-23 by user; tree CLEAN, all
## fix-batch commits in; branch ai-pipeline ~70 commits ahead of origin,
## UNPUSHED — push when the user says so)

Resume order:
1. **Image-base decision** (user-flagged): SDXL vs the 2026-07-20
   Z-Image ruling for the prop chain — see the OPEN item in the fix
   batch above. Decide before generating anything new.
2. **Q6 crucero** (stopped by user mid-concepts): regenerate under
   whatever base 1 decides; then batch gate — fresh zone_review renders
   both zones, orchestrator re-review vs the three complaints (metallic
   gloss / far-LOD close-ups / scale), ONE workspace nextest, then the
   user re-walk. b3.md's feel-check gate box stays open until that walk.
3. **B4** — characters through the pivot (human_gen monk swap; subplan
   reads b3.md Decision log + a4.md from disk). Carry the zone_review
   flag: player skin overexposes under the dusk key (B4 material work).
Still open (user): candelabra_shrine + human_gen monk renders
(`target/human-gen-review/`), AI-setup fresh-session checks (hooks smoke,
statusline, quiet-box bench baseline re-save).

---

# AA visual upgrade — executed 2026-07-08 (8 of 9 phases)

Plan: tasks/aa-visual-upgrade-plan.md. One commit per phase, headless-verified.

- [x] Phase 0 — quality bar doc, offscreen harness, content lint (`0bad4c7`)
- [x] Phase 1 — full PBR materials (`f2ad4c7`)
- [x] Phase 2 — HDR + ACES tonemap + MSAA 4x + IBL sky (`e55b2ec`)
- [x] Phase 3 — shadow mapping (`d37caef`)
- [x] Phase 4 — bloom + emissive routing (`cbeac41`)
- [ ] Phase 5 — Mixamo character pipeline — **BLOCKED on manual downloads**
      (shopping list: content/source/characters/mixamo/SHOPPING_LIST.md)
- [x] Phase 6 — environment set dressing (`4c2e4ee`)
- [x] Phase 7 — textured particle VFX (`a289b9d`)
- [x] Phase 8 — perf guardrails (`f23ca6c`)

## Review

- Renderer went from flat Lambert/no-shadow/LDR to: full glTF PBR (normal/MR/
  emissive/AO + generated tangents), Cook-Torrance GGX everywhere, HDR
  Rgba16Float scene with ACES tonemap + exposure, MSAA 4x, IBL from the zone
  HDRI (irradiance + GGX prefilter + BRDF LUT) with the same HDRI as visible
  sky, PCF shadow mapping (fitted texel-snapped cascade), dual-filter bloom
  fed by HDR emissive (SDF colors > 1.0 emit), exponential distance fog.
- Zones: per-zone visuals in zones.ron (env/fog/ground/props); procedural
  heightmap ground (flat play area, hills at horizon) with Poly Haven PBR set;
  CC0 rock/tree props via scripts/asset-pipeline/fetch_polyhaven.mjs.
- VFX: atlas-textured particles (procedural grayscale atlas — deviation from
  the planned Kenney pack: no stable download URL, procedural is equivalent
  for glows/streaks/smoke and unit-testable), additive + premultiplied-alpha
  variants, soft depth-fade in a dedicated particle pass, velocity-stretched
  streaks; content/vfx/<ability>.ron cast beats, travel/impact on projectile
  prefab VfxTrail, telegraph-resolve impact; VQ-E1 content-lint.
- Guardrails: cap meters + 80% warnings, GPU frame time in dev overlay
  (timestamp queries), criterion baseline "pre-enemies" for joint palette
  (~110 µs @ 40×64 joints) and particle fill (~15 µs @ 4096).
- Verification: `cargo test --workspace` green after every phase (offscreen
  analytic readback tests + content lint + CPU unit tests); both binaries build.

## Next

1. User: sandbox feel-check (big jumps landed in Phases 2/3/6/7).
2. User: Mixamo downloads per SHOPPING_LIST.md → then Phase 5 (Blender CLI
   pipeline, socket remap, races switch, KayKit retirement pending sign-off).
3. Exposure/fog/bloom tuning knobs all exist if the feel-check wants shifts.

---

# Character animation fixes + live skill bar (2026-07-05)

Feel-check on the Phase-C characters surfaced: no facing, no walk anim, no attack
anim; user also wanted a working skill bar. Investigation added two headless
tests proving the animation math + FacingSystem + locomotion state machine are
correct, so the bugs were narrow:
- [x] Facing: KayKit rigs face +Z; `forward_offset` was 0 (assumes −Z) → moonwalk.
  Fixed: `forward_offset: 3.14159` in the 4 race files. Likely also fixes the
  "no walk" perception (a backward-facing run cycle reads as broken).
- [x] Attack: sandbox player (ravager) has only server-resolved (Scheduled/Leap)
  abilities; offline `SandboxCastSystem` only fired Projectile. Generalized it —
  LMB/Q/E now fire the cooldown + `trigger_attack` (attack clip) for any slot;
  Projectile abilities still spawn their bolt. Full damage resolution stays
  online (MechanicResolveSystem is server-side; no enemies in the sandbox).
- [x] Skill bar: already existed + wired; enabled its slots offline so the bar is
  live with cooldown sweeps (was dimmed because the ravager's slots are needs_server).
- [x] TEMP diagnostic: ~1 Hz `log::info!` of the skinned player's clip/time in
  MeshRenderSyncSystem (logger defaults to Info, shows without RUST_LOG). Confirms
  the live pose advances; REMOVE once the character animates on screen.

Verify: cargo test --workspace green (incl. the 2 new motion/facing tests).
Pending user feel-check: faces travel, legs animate, attack on LMB/Q/E, skill bar
visible. If legs still frozen, the `skinned anim:` log isolates GPU vs data.

---

# Real models & textures: glTF mesh pipeline (multi-session)

User verdict: primitive-shape visuals read as programmer art. Direction chosen
(AskUserQuestion): full mesh pipeline — glTF models + textures + skeletal
animation, assets from CC0 packs (Kenney/Quaternius/Mixamo-class). The engine
today draws exactly one thing: an instanced unit cube (SdfInstance pool, one
pipeline, one global texture bind). "Sphere/Capsule" never had geometry.

## Phase A — static textured meshes (DONE 2026-07-05)

- [x] A1. `RenderMesh { asset, tint }` component in engine-core + prefab registry entry
- [x] A2. engine-renderer `mesh.rs`: CPU stage `load_gltf_data(path) -> MeshData`
      (gltf 1.4 `import`, node transforms baked into vertices, per-primitive
      vertices/indices/baseColor) — pure, unit-tested with a hand-built GLB
- [x] A3. GPU stage: `MeshStore` (path → GpuMesh; failed loads cached as None,
      log once), per-primitive buffers + sRGB baseColor texture bind group;
      untextured primitives get a 1×1 of baseColorFactor
- [x] A4. `mesh_shader.wgsl` + second pipeline (mesh_pipeline.rs): same
      camera/light group 0, texture group 1, 80-byte MeshInstance
      (model + tint), u32 indices, same Lambert/depth as the primitive pass
- [x] A5. `MeshRenderSyncSystem` (RenderSync): lerp vs PreviousTransform,
      load-on-demand, group by mesh into MeshDrawList; RenderSystem draws the
      ranges in the same render pass after the cube draw. Draw list rebuilt
      per frame — no slot bookkeeping, despawn free. MeshStore/DrawList are
      taken out of Resources during the frame and restored on every exit path
      (incl. surface-lost early returns) so loaded meshes survive
- [x] A6. content/models/avocado.glb (Khronos sample, CC0, textured) +
      content/prefabs/mesh_probe.ron + sandbox spawn at (4, -0.5, 0);
      real-asset load test (skips if asset absent) proves PNG decode path
- [x] A7. cargo test --workspace green from full clean (the stale-incremental
      E0432 ghost reappeared under `check --workspace --benches`; cargo clean
      fixed it, same as the weakpoints session). User manual check pending:
      run sandbox, textured avocado beside spawn.

## Phase B — skeletal animation (DONE 2026-07-05)

Plan: `~/.claude/plans/floofy-coalescing-gosling.md`. Built "like a professional
animator": crossfade blending + speed-driven state machine + eased turning, not
hard-cut clip swaps. Dev probe = CC0 Khronos Fox (Survey/Walk/Run, 24 joints).

- [x] B1. glTF skin + animation extraction (engine-renderer `anim.rs` pure math +
      `mesh.rs` extraction). Skinned vertex (JOINTS_0/WEIGHTS_0), Skeleton
      (nearest-joint-ancestor parenting, inverse binds), AnimationClip (per-joint
      T/R/S tracks, LINEAR/STEP, CUBICSPLINE→linear). **Bake branch**: skinned
      primitives stay mesh-local (joint palette places them); static ones bake as
      before. Hand-built 2-joint animated GLB test proves it GPU-free.
- [x] B2. Skinned GPU pipeline (`skinned_pipeline.rs` + `skinned_mesh_shader.wgsl`):
      SkinnedVertex, per-instance joint_base, joint-palette storage buffer (group 2),
      linear-blend skinning. Coexists with the static Phase-A pipeline (mesh skinned
      iff glTF has a skin). GpuMesh carries CpuSkin (skeleton+clips) for CPU sampling.
- [x] B3. Runtime: `AnimationPlayer` component (engine-core, `transition_to`
      crossfade API), `pose_player` (advance+sample+blend→joint matrices),
      SkinnedDrawList, MeshRenderSyncSystem routes static→MeshDrawList /
      skinned→SkinnedDrawList, RenderSystem uploads joints + draws skinned ranges.
      Engine lazily attaches a default AnimationPlayer to skinned entities.
- [x] B4. Facing (client `locomotion.rs` `FacingSystem`): eased yaw slerp toward
      movement heading, per-asset `forward_offset`. Pure `heading_yaw`/`turn_toward_yaw`
      unit-tested. Client-owned cosmetic — sim ignores rotation (net.rs is position-only).
- [x] B5. Controller (`LocomotionSystem`): speed→idle/walk/run via LocomotionClips,
      attack one-shot (`trigger_attack`, wired into both cast paths alongside
      trigger_swing) + death latch (AnimController). Pure `desired_state` tested.
- [x] B6. Fox probe: `content/models/fox.glb` (CC0) + `fox_probe.ron` + sandbox
      `FoxProbeDriver` (orbits the player with ramping speed → shows idle/walk/run
      blend + continuous turning). Real-asset skip-if-absent test. **Verified: 34
      suites green from full `cargo clean`; check --workspace --benches green (no
      ghost this time). Avocado static probe unregressed.** User feel-check pending:
      run sandbox — Fox should circle the player, blending idle→walk→run and turning
      to face its path. If it moonwalks, flip fox_probe forward_offset to π.

Note: Fox has no attack/death clips, so those layers are proven by code/tests, not
the probe — they animate on Phase-C humanoid characters that ship those clips.

## Phase C — content integration + real assets (DONE 2026-07-05)

- [x] Races reference a skinned model + clip names — `RaceModel` in
  `game/vordar-game/src/player/class.rs`; race RON is now `(body: [...],
  model: Some((asset, idle/walk/run/attack/death, walk_speed, run_speed,
  forward_offset)))`. `body` kept as an SDF fallback.
- [x] Class → mesh tint (`ClassDef.tint`); glTF races ship pre-dressed so the
  SDF outfit is dropped for them. Wayfarer = cool steel, ravager = ember red.
- [x] `BodyComposeSystem` (`client/.../body.rs`) branches: race with a model →
  `RenderMesh` + `LocomotionClips` + `AnimController`, no ShapeGroup/PoseRig;
  else the unchanged SDF path. Enemies/NPCs author ShapeGroup directly + carry
  no Race, so they never enter here → stay SDF by construction.
- [x] Assets: CC0 KayKit Adventurers (Knight/Barbarian/Rogue/Mage → human/
  dwarf/elf/valkyrie), preprocessed with gltf-transform: pruned to the skinned
  body meshes (weapon/hat/cape props dropped — sockets are a later feature),
  trimmed to the 5 used clips, scale + ground offset baked onto the armature.
- [x] Engine: renderer now honours the skeleton's root-ancestor transform
  (`Skeleton::root` in anim.rs) — folds an armature's baked scale/offset into
  the joint palette (was a latent bug: armature transforms were ignored). This
  is what grounds the characters' feet to the floor.
- [x] Retired the Fox probe (sandbox + prefab); the WASD-driven player is now
  the real skinned human. Kept the avocado (static-path guard) + fox.glb (test).

Verify: `cargo test --workspace` all green (renderer 14 incl. root-offset math +
real human.glb load; game 46 incl. race-model/tint parse; client 12 incl. mesh
vs SDF branch). `cargo check --workspace --benches` clean.

Deferred (need supporting systems, not warranted yet): per-class weapon meshes
(joint sockets), death animation wiring (needs a corpse-hold/despawn-delay),
class-specific attack clips. Only `human` is live-spawned; elf/dwarf/valkyrie
ship content-ready but unspawned (no class picker).

User feel-check (I don't run the GUI): run the sandbox — the player should be a
rigged humanoid that idles, runs when moving, turns to face its heading, and
swings on a cast. If it moonwalks, set the race's `forward_offset` to 3.14159;
if the size/height is off, re-bake (adjust TARGET_H in the preprocess step).

---

# Ravager class + races/outfits + Emberwood Rest (first content pass)

Plan: `~/.claude/plans/jiggly-chasing-lovelace.md` (revised mid-pass: damage
triangle made mechanically real; visuals became race-base + class-outfit
composition per user direction).

## Todo

- [x] 1. CombatStats + compute_damage (power/defense/crit, splitmix64 deterministic crit roll — no rand) wired into all 3 damage sites; no-stats = byte-identical passthrough. Deviation from plan text, kept deliberately: no max_health on CombatStats / no Health injection — Health stays its own authored component.
- [x] 2. Damage triangle real: DamageType (Physical>Life>Runes>Physical ×1.3/×0.75, Divine↔Corrupt mutual ×1.3, Elemental neutral, True skips defense+multipliers), affinity on CombatStats, damage_type carried by ContactDamage/Projectile/Mechanic/AbilityEffect (serde defaults keep old content Physical). 6 unit tests per edge.
- [x] 3. Data-driven classes: ClassLibrary (RON per class), AbilityDef/AbilityEffect replace the SKILLS const, ClassId on prefabs, server CastIntent resolves class→ability (per-ability cooldowns already keyed by id). Client generalized to slots (0=LMB hold-repeat, 1=Q, 2=E), action bar fed from the library. human.ron migrated byte-identical.
- [x] 4. Ravager kit: rend (fast small Scheduled), cleave (heavy Scheduled, shares blast's e2e choreography numbers), onslaught (new AbilityEffect::Leap — LeapImpulse velocity override between PlayerMovement/Movement, arrival Mechanic, client prediction mirror + optimistic dash). Default spawn flipped to "ravager" (PLAYER_PREFAB const + sandbox); e2e: phase4→cleave, phase6-health range assert, phase7_5 reworked to kiting rend fight (face-tanking at 0 defense loses — verified 4 stable runs), new onslaught dash+resolve e2e.
- [x] 5. Passives: Finishing Blow (+40% under 30% HP, integer-exact boundary) + Rage (BuffStack: +2 power/stack, cap 5, 4 s refresh-on-hit decay) via new DamageDealt event from all 3 damage sites; RavagerRageSystem (server PostUpdate after MechanicResolve), BuffDecaySystem (shared PreUpdate). No general aura/dispel framework. Unit + second-hit-lands-harder integration tests.
- [x] 6. Races + outfits: RaceLibrary (4 base bodies: human/valkyrie/dwarf/elf, convention 0=torso 1=head), class RON gained outfit shapes + pose params, client BodyComposeSystem assembles ShapeGroup = base + outfit and inserts PoseRig; prefabs author Race/Class instead of ShapeGroups. NPCs = race body, no class, no gear.
- [x] 7. Pose animation: SubShape.rotation (serde default, renderer honors it), PoseAnimationSystem (client RenderSync) — idle torso bob + out-and-back weapon swing on cast (trigger_swing from both cast paths, own player only). Pure-math + integration tests.
- [x] 8. Town (chapter-02 "Emberwood Rest", east zone): buildings/villagers via initial_spawns (town_hall, cottages, human villager + dwarf elder — no Health = damage-immune by construction), grunt/brigand/mossback camps outside aggro-clear of walls, new Anchored marker (separation pushes only the other side — walls/NPCs never shoved). zones.ron east→chapter02, palette retint, all 3 binaries register chapter_02. e2e: town replicates, villager unhittable by cleave centered on it.
- [x] 9. Final verification: cargo test --workspace + check --workspace --benches green after full clean rebuild (a cargo clean -p mid-build corrupted incremental state — full clean fixed it). 44 game unit tests, 13 e2e, 6 zones, 7 client.

## Review

- The one genuinely new engine mechanic is the leap (velocity override +
  scheduled arrival hit); everything else composes existing seams (Mechanic,
  CampDef, initial_spawns, PrefabLibrary-style load_dir).
- Deliberate scope holds: no aura/debuff framework, no class-picker UI, no
  navmesh (camps placed aggro-clear of walls instead), no remote-player swing
  replication (needs a caster id on MechanicScheduled — protocol bump, later).
- Known manual-check items for the user (run skill): Ravager reads as
  dual-wield/dark, races read distinctly, idle bob + cast swing feel, leap
  responsiveness (watch for rare misprediction snaps), town reads as a town.
- Criterion baseline note: separation query widened (Satisfies<&Anchored>) and
  damage paths gained mods — re-baseline `main` before the next perf pass.

---

# Fix structural weak points (WEAKPOINTS.md #1–#4 + gaps A/B/C)

Plan: `~/.claude/plans/jiggly-chasing-lovelace.md` — fix-now items #1–#4 plus bench gaps A/B; gap C gates the #4 datagram decision. Out of scope: #5, gap D.

## Todo

- [x] 1. Benches for gaps A/B (prefab_spawn, client_netcode + vordar-client bench-internals seam) → verified: seam absent from normal builds, 31 suites green, baselines saved. Numbers: bolt spawn 4.0 µs (RON parse), churn n32 126 µs, client enters_64 264 µs (dominated by prefab spawns), states_a200 10.9 µs, reconcile 240 = 847 ns (no fix needed)
- [x] 2. #1 view idiom: narrowphase, separation, enemy Provoked → verified vs main baseline, tests green. Numbers: narrowphase cluster −90% (12.97 ms → 1.32 ms @500, ~104 → ~11 ns/pair), separation −72% (~202 → ~57 ns/pair), chain cluster-200 −70% (3.22 ms → 961 µs), full_tick e1000_p200 −39% (2.97 → 1.81 ms). enemy_ai mixed: big wins at low P (Provoked get gone), +14–25% on idle at high P (Option<&Provoked> widens the fetch) — moot, Phase 3 replaces the idle scan entirely
- [x] 3. #2 grid-based enemy targeting → verified vs main, 23 vordar-game tests + workspace green. Three-way split: grid radius query (nearest by dist², entity-id tie-break) / global scan when provoked, aggro > 50, or < 64 players (below that the O(P) scan beats the ~400 ns grid walk — first cut regressed p1 cases +1650% before the threshold). Numbers: idle e1000_p200 −67% (1.18 ms → 380 µs), idle e1000_p1 −80% (3.9 µs), engaged e1000_p200 −23% (1.20 ms); new enemy_ai/aggro group baselined (e1000_p200 830 µs). O(E·P) eliminated: idle cost now ~E × 0.4 µs regardless of P
- [x] 4. Gap A fix: compiled prefab spawn plans → verified vs main, workspace green. ComponentLoader parses RON once → CompiledComponent (clone-to-apply closure); PrefabEntry.plan is OnceLock-lazy under the shared Resources borrow; parse errors returned, not cached; Clone derives on 8 core + 4 game components, register_component bound += Clone. Numbers: prefab/spawn/bolt −83% (4.0 µs → 646 ns), churn n32 −81% (126 → 23.6 µs)
- [x] 5. Gap B fix: client apply_snapshot (mem::take + (&mut NetLerp, &Transform) view, own-player state extracted before the view for reconcile) → verified vs main, workspace green incl. QUIC e2e. Numbers: states_a200 −76% (10.9 → 2.76 µs), states_a64 −74%, enters_64 −79% (264 → 54 µs, mostly item 4's compiled spawns), reconcile −21% for free
- [x] 6. #3 snapshot stagger + cheap gather → GATE PASSED: soak 400 bots input p99 51 ms → 19.05 ms (< 25 budget), input/post both 60.0 Hz, bots at exactly 10 snap/s + ~11 KB/s. PostUpdate now Fixed(60); Mechanic/Transfer self-gate to 10 Hz via tick counters; broadcast serves conn % 6 == tick % 6; gather uses query_radius_into + reused scratch + one (&Transform,&PrefabId) view; known set mem::swap'd. Bench: full round c200 −36% (7.1 → 4.56 ms), per-tick spike now 870 µs (was the whole 7.1 ms on one tick); new snapshot/broadcast_slice group baselined. Workspace green.
- [x] 7. Gap C: engine-net hygiene (read_frame reads tag byte separately — O(len) buf.remove(0) gone; broadcast payloads as Arc<Vec<u8>> — one encode, refcount bump per conn) + LossySocket in impair.rs (drops received datagrams below QUIC via AsyncUdpSocket wrapper, deterministic LCG; NetClient::connect_impaired) + loss probe tests/loss.rs (#[ignore]). Workspace green incl. QUIC e2e. Probe (50 ms RTT, 30 s/rate): 0% p50/p99/max = 100/113/118 ms; 1% 100/149/163; 3% 100/157/161; 5% 99/163/164.
- [x] 8. #4 datagram snapshots → NOT BUILT: the step-7 gate (p99 gap > 250 ms or max > 500 ms at 1–5% loss) was not met — worst case 164 ms ≈ one QUIC retransmit cycle, absorbed by the 100 ms snapshot cadence. Reliable-stream snapshots stay; re-probe if RTTs or loss assumptions change.
- [x] 9. Re-baseline + docs → fresh `--save-baseline main` on the final tree (mixed-vintage baseline problem resolved), soak 200/400 re-run, BASELINE.md and WEAKPOINTS.md rewritten with post-fix numbers. See review below.

## Review

Full pass (2026-07-03 → 2026-07-04): all four fix-now items (#1–#4) plus gaps A/B/C
done; #5 and gap D confirmed still open and out of scope.

- **#1 view idiom**: narrowphase 104 → 12 ns/pair, separation ~205 → ~40 ns/pair.
- **#2 grid targeting**: enemy AI idle/aggro paths no longer scale with player
  count; O(E·P) confined to the provoked-only fallback, which is bounded by active
  provocations, not crowd size.
- **#3 snapshot stagger**: the headline gate — soak 400-bot input p99 51.25 ms →
  18.73 ms (budget 25 ms). PostUpdate now 60 Hz, self-gated systems preserve their
  original cadence.
- **#4 datagram snapshots**: evaluated via gap C's below-QUIC loss probe, gate not
  met (164 ms worst gap vs 250/500 ms threshold) — correctly **not built**.
  Reliable-stream snapshots stay; the decision and its evidence are recorded in
  BASELINE.md/WEAKPOINTS.md so it doesn't get silently re-litigated.
- **Gap A** (prefab spawn): 4.0 µs → 677 ns per bolt via compiled spawn plans.
- **Gap B** (client netcode): apply_snapshot 10.9 µs → 2.84 µs at A=200.
- **Gap C** (packet loss): real below-QUIC loss simulation built and probed;
  also fixed two engine-net hygiene issues (`read_frame` O(len) memmove,
  per-connection broadcast payload clone) that existed independent of the #4
  decision.
- Whole sim tick at 1000e+200p: 2.97 ms → 478 µs (17.8% → 2.9% of the 60 Hz budget).
- Workspace tests green throughout every phase; every fix verified against the
  criterion `main` baseline before landing.
- Remaining open items are explicitly out of scope for this pass: #5 (dense-cell
  broadphase all-pairs degeneration, still ~7.3 ms at a 500-entity pile) and gap D
  (long-run growth soak). Both are documented in WEAKPOINTS.md for whenever
  they become load-bearing.

---

# Benchmark the parts that can limit the game

Plan: `~/.claude/plans/reactive-puzzling-lark.md` — criterion suite in `benchmarks/` + parameterized soak + `docs/benchmarks/BASELINE.md`. Measurement only, headless.

## Todo

- [x] 1. Root Cargo.toml + `benchmarks/` skeleton (Cargo.toml, src/lib.rs builders) → verified: `cargo check -p vordar-benches` clean
- [x] 2. Seam-free benches: spatial_grid, physics_pipeline, enemy_ai, separation, protocol → compile clean; smoke in progress
- [x] 3. `App::run_ticks` seam + full_tick bench → compile clean
- [x] 4. `bench-internals` seam in vordar-server + snapshot bench → `cargo check -p vordar-server` (no feature) clean — seam absent from normal builds
- [x] 5. Soak `VORDAR_SOAK_BOTS` env var + summary line → `cargo test --workspace`: 31 suites green
- [x] 6. Full release bench run (`--save-baseline main`) + soak 200/400 → `docs/benchmarks/BASELINE.md` written with numbers + analysis

## Review

- Phase 1–5 (2026-07-03): suite + seams landed. Notes:
  - criterion pulled in at workspace level (`default-features = false` + `cargo_bench_support` — no plotters, headless).
  - `[lib] bench = false` required in vordar-benches — criterion CLI flags would hit the lib's libtest harness otherwise.
  - Seam verification: `cargo check -p vordar-server` (no feature) clean; `cargo test --workspace` 31 suites green.
  - Systems that mutate their scenario (Separation pushes entities apart, MechanicResolve despawns the mechanic) are benched with `iter_custom` + untimed reset so measurements stay stationary.
- Phase 6 (2026-07-03): baseline captured (criterion `main` + docs/benchmarks/BASELINE.md). Headline findings:
  - Whole sim tick at 1000 enemies + 200 players: 2.97 ms = 18 % of the 16.67 ms budget — plenty of headroom at design load.
  - The one cliff: dense single-cell piles — 500 entities in one cell = broadphase 9.8 ms + narrowphase 13 ms (all-pairs degeneration).
  - Soak: 200 bots pass all budgets; 400 bots hold 60 Hz *average* but input p99 hits 51 ms (>25 budget) — snapshot fan-out jitter on the sim thread is the clients-per-zone limiter (~200–300 mutually visible).
  - parry3d removal is a dep-weight win only; narrowphase cost is world.get fetches (~104 ns/pair), not the AABB math.
  - Soak stats now print before assertions so over-budget scaling probes still report.

---

# Phase D: geared models, full animation wiring, real particles

Plan: `~/.claude/plans/zippy-wiggling-coral.md` — superseded the minimal weapons+SDF-sparks plan
with the best-outcome version: rigid-skinned gear, per-ability clips + hit/death reactions,
an additive billboard particle pipeline, and protocol v8 (hp + EntityDied).

## Todo

- [x] 0. Reproducible asset pipeline: KayKit sources committed (`content/source/characters/`),
       `scripts/preprocess-characters/preprocess.mjs` (10-clip keep set, gear rigid-bound to
       handslot.r/.l/head with in-script asserts), all 4 `content/models/*.glb` regenerated
       → renderer test asserts 10 clips + all primitives skinned
- [x] 1. Bone sockets: `Joint.name` kept, `anim::global_transforms`, `SocketConfig`/`SocketTransforms`
       published per frame by MeshRenderSyncSystem → real-asset test: handslot.r moves during the chop
- [x] 2. Particle pipeline: `CameraUniform` gains right/up basis; `particle_pipeline.rs` +
       `particle_shader.wgsl` (camera-facing quads, procedural soft disc, One+One additive,
       depth read-only) drawn after the skinned pass; `ParticleDrawList` resource
- [x] 3. Client sim: `vfx.rs` (ParticleSim resource — plain Vec, no entities; xorshift; burst/trail),
       shared `VfxTrail` component registered in GameComponentsPlugin, authored on bolt/ember/shard
       prefabs; VfxSystem in both plugins
- [x] 4. Per-ability animations: `AbilityDef.anim/anim_secs` (ravager: chop/slice/spin; wayfarer:
       spellcasts), `RaceModel.hit` = Hit_A, `trigger_attack_clip`, cast bursts at the hand socket
       in both cast paths (SlotMeta in net.rs)
- [x] 5. Networked locomotion gap: FacingSystem/LocomotionSystem registered in NetClientPlugin;
       `NetMotion` from snapshot deltas animates remote players
- [x] 6. Reactions: `react.rs` — HealthWatch/HitReactSystem (flinch + impact burst, never cancels
       attacks), CorpseOnDeathSystem (DespawnFlush First; corpse holds Death_A), CorpseTtlSystem
- [x] 7. Protocol v8: hp on EntityState/EntityPos, `ServerMsg::EntityDied`; server broadcasts
       deaths pre-flush; client applies hp (hit reacts live online) + corpse on EntityDied

## Review

- 2026-07-07: all 7 phases landed, `cargo test --workspace` green after each (final run: all
  suites incl. e2e 13/13 — rend-kill test now also asserts replicated hp decreases and the
  EntityDied broadcast). `cargo check --workspace --benches` clean.
- Verified during planning: KayKit clips are all LINEAR (the CUBICSPLINE downsample at
  mesh.rs:259 is a non-issue); snapshots carried no health/rotation pre-v8; DeathSystem
  despawns same-tick → death anim must be a client-side cosmetic corpse.
- Kept the TEMP anim diagnostic logs (mesh.rs / body.rs) — on-screen animation still awaits a
  user feel-check.
- Feel-check items for the user (GUI): gear seating in the hand, per-ability swings, cast/impact/
  death particles, projectile trails, remote-player run animation, corpse hold. Tuning knobs:
  burst constants at the top of `client/vordar-client/src/vfx.rs`; gear offsets in
  `scripts/preprocess-characters/preprocess.mjs`.

---

# Devloop: pass two + convert the research doc into a runnable queue (2026-07-25)

Plan: `~/.claude/plans/warm-purring-kettle.md`.
Source: `docs/reviews/devloop/research-agentic-loop-techniques-2026-07-25.md` (pass one, breadth).

Decisions taken at planning: pass two runs before any conversion; the 2026-07-17 report pair
is kept (divergence from `audit-base.md:97-108` recorded in the new report header) because
the research doc and the new findings cite it by line ~15 times.

## Phase 1 — pass two: six dedicated per-paper reads

- [x] 1. HORIZON (arXiv:2604.11978) — seven-category definitions + judge protocol behind k=0.84
- [x] 2. DeepVerifier (id to recover from doc 3.2) — is the reject-as-LLM / trial-as-script split right
- [x] 3. ACE (arXiv:2510.04618) — token/latency claims unverified; where (if anywhere) it lands
- [x] 4. Scaling TTC for Agentic Coding (arXiv:2604.16529) — G=2/V=8/T=2 came from an aggregator
- [x] 5. SENTINEL (arXiv:2606.12908) — confirm taxonomy-rejected / sourcing-adopted holds
- [x] 6. EvoAgentBench (arXiv:2607.05202) — an adopt riding on one headline number
- [x] 7. Append `## Pass two` to the research doc; revise the decision queue, affected cluster
       entries and the source-quality ledger in place; DELETE `## Shortlist for pass two`

## Phase 2 — convert into the live report pair

- [x] 8. `docs/reviews/devloop/audit-devloop-2026-07-25.md` — findings 1-8 (adopts) + 9-11 (trials)
- [x] 9. `docs/reviews/devloop/reworks-devloop-2026-07-25.md` — rework 1 (per-campaign outcome
       vector), rework 2 (cross-audit map) PARKED with its gate
- [x] 10. Cross-type queue note, mirrored verbatim in both files
- [x] 11. Verify: structure, resolving `file:line` anchors, Tradeoffs bullet per finding, Path
       naming a measurable, 07-17 untouched

Not in this plan: running the queue (separate go, opus session); editing any `.claude/` file
(every harness edit is a finding for the queue to land).

## Review

- 2026-07-25 phase 1: six pass-two per-paper reads done. **Routed to opus, not fable** —
  fable hit its usage limit mid-launch; ruling 3 names opus as the fallback and opus is the
  cheaper tier, so this was a downgrade, not an escalation.
- Pass two changed reasoning under three adopts, corrected one venue attribution, corrected
  one cost estimate upward 4-5x, and removed one field from an adopted schema. No verdict
  flipped adopt<->reject. Every correction to a *rejected* technique ran toward more
  expensive, so the fan-out table got stronger, not weaker.
- The research doc was revised in place (stale numbers corrected in their own cluster
  entries), gained a `## Pass two` section, and lost `## Shortlist for pass two` — a resolved
  shortlist is not a record.
- Phase 2: report pair written. Verified: queue note byte-identical across both files (18
  lines), 77 line-range anchors in range, all referenced paths exist, all 13 findings carry
  Evidence/Ideal/Gap/Tradeoffs/Suggestion/Path plus a measurable.
- **Not committed** — the three files under docs/reviews/devloop/ are staged for the user's
  call. `.claude/` was not touched: every harness edit is a finding for the queue to land.
- Next: `/run-queue docs/reviews/devloop/audit-devloop-2026-07-25.md` in an opus session,
  after a `/compact`. Two (user-decides) questions batch at launch (findings 4 and 6); rework
  1 has a third at its own pause.

## Campaign: devloop 2026-07-25 — /run-queue in progress

Launched 2026-07-25. Queue note (struck state) lives in both report files; this
section records only what the note cannot: progress *inside* rework 1.

- [x] finding 1 — stop lines (`.claude` `c3884c5`)
- [x] finding 2 (micro, inline) — routing stays flat (`.claude` `db5d005`)
- [x] finding 3 — terminal states + worker output ceiling (`.claude` `39d9cf2`)
- [x] finding 4 — post-edit death policy + plan SHA (`.claude` `945351f`)
- [x] finding 5 — lessons batch. **No commit: all targets unversioned.**
      Measured 24→22 notes, index −30%, 2 absorbed strikes, 2 merges.
      Pre-edit snapshot: `<scratchpad>/pre-finding5/` (only rollback that exists)
- [x] finding 6 — widened lesson sourcing (`.claude` `afa8ca3`)
- [x] finding 7 — failure vocabulary, residual inverted (`.claude` `5931f22`)
- [x] finding 8 (micro, inline) — planner reads error register (`.claude` `8eee577`)
- [x] strike findings 1–8 in both report files (`f97e535`)
- [x] rework 1 planned (`b187b47`), decided **inform-only** (`5402b69`)
- [x] rework 1 step 1/8 — `scripts/campaign_report.py` cost block (`a238589`)
- [ ] rework 1 steps 2–8 (step 9 NOT built — inform-only)
- [ ] finding 9 (trial) — gate zero is free, take it first
- [ ] finding 10 (trial), finding 11 (micro, trial)
- [ ] strike rework 1 and findings 9–11; campaign aggregate; lesson-mining pass

### Decisions taken at launch (recorded in the findings themselves)
- Finding 4: post-edit spawn death stashes per item in whichever repo is dirty,
  then discards and respawns silently. Stop only on a *second* death of one item.
- Finding 6: lesson-mining pass adopted in full (steps 2–4).
- Rework 1: quality vector is **inform-only**; it never gates.

### Carry to the next devloop audit (not patched here)
- The ~100k output ceiling finding 3 added lands only in the finding-worker spawn
  template. The rework-planner has no ceiling and ran to **155.6k** this campaign.
- The loop has no representation for "rework N is k/K steps done" — the queue note
  strikes only on completion, so mid-rework progress lives in git log alone.
- (moved 2026-07-29 to `lessons/2026-07-29-stage-explicitly-while-agents-hold-the-tree.md`
  after it recurred — recording it here gave it no trigger to fire on.)

## In-engine prop review (2026-07-29, user)

Verdict from the user's own in-engine pass — the gold reference the campaign's
metrics were all proxies for. `candelabra_shrine` and `olive_stump` pass ("barely
artifacts that make you see it's AI"); the stump's texture is the weakest part of
a passing asset. `chapel_arch` and `cypress` fail ("AI slop at its finest,
especially the tree").

### chapel_arch — stale, not defective
- Sole prop still on the OLD `multiview_controlnet_depth` texture path
  (manifest 07-25, `turntable: null`); every other prop was rebuilt 07-28 on the
  current atlas→depth→nbv→generate→blend→bake path.
- Installed `chapel_arch.glb` (13092440 B) matches `final_f2.glb` from 07-24
  23:45 — an intermediate fix attempt, not even the newest local variant.
- Geometry is **sound**: `multiview/canvas_0/depth.png` shows the pointed arch,
  archivolt mouldings, four columns, plinths. Only carved panel detail is soft.
- Generation is **sound**: `multiview/canvas_0/vordar_mv_00103_.png` is pale grey
  sun-bleached limestone with crisp capitals — production quality.
- Shipped asset is orange terracotta. So the hue is destroyed somewhere between
  generate and install. Do NOT theorize which stage: rebuild on the current path
  and look. Grey ⇒ it was staleness. Orange ⇒ a live bake defect that the other
  subjects' warm/grey albedo happens to mask.
- Geometry needs no regen (`clean.glb`, `clean_hires.glb` exist), so this is a
  texture rerun + reinstall.

### cypress — architectural, out of class
- Concept (`concept.png`) is excellent: fine needle sprays, dark desaturated
  olive-green, fluted trunk, correct columnar proportion.
- Texture generation is excellent: `multiview/canvas_0/vordar_mv_00106_.png` is
  correct dark olive-green, matte, per the prompt's "muted dark tones".
- Geometry is the failure: `multiview/canvas_0/depth.png` is a **solid opaque
  lumpy cone** — a cauliflower on a stick. No sprays, no gaps, no branch
  structure.
- Root cause: Hi3DGen extracts a surface, and cypress foliage has no surface.
  Same family as the permanent hollow-shell result — a representational limit,
  not a knob. Painting a photoreal tree onto a blob cannot fix the silhouette,
  and the painted needle detail dies in atlas reprojection.
- No seed, sampler, guidance or multi-view setting addresses this. Foliage needs
  alpha-cutout cards, i.e. a different production path.

### Open
- [ ] chapel_arch texture rerun + reinstall (pending user go-ahead, §8)
- [ ] foliage production path decision (user's call — scope, maybe licensing)
- [ ] olive_stump texture crispness — weakest part of a passing asset, unscoped

### Foliage path — decided, and its real first step is renderer work

User ruled (2026-07-29): living vegetation comes from a **Blender procedural
generator**, not Hi3DGen. Facts gathered before planning, two of which reorder
the plan:

1. **Blender 5.2 bundles no tree generator.** `addon_utils.modules()` returns 14
   add-ons; the only name matching tree/plant/curve is `io_curve_svg`. Sapling
   Tree Gen is gone from the bundle. So the generator is either a vendored GPL
   add-on or authored in-house (geometry nodes / pure-Python), not "enable the
   built-in one".
2. **The main pass already does alpha cutout properly** —
   `smirk/engine-renderer/src/mesh_shader.wgsl:96-110` implements glTF MASK with
   alpha-to-coverage edge AA, and `mesh/store.rs:129-133` carries the cutoff from
   `AlphaMode::Mask(c)`. glTF import round-trips it
   (`mesh/gltf_import.rs:323-326`, tested at `:385` and `:492`).
3. **The shadow pass has no fragment stage at all.**
   `smirk/engine-renderer/src/shadow.wgsl:1-4` says so outright: three vertex
   entries, depth-only. A foliage card therefore casts the shadow of its **full
   quad**. Under the dusk HDRI's long shadows a card-built cypress would cast a
   stack of solid rectangles — worse than today's blob. **This blocks alpha
   foliage.**
4. **The depth prepass draws MASK geometry as opaque.** `frame.rs:515` and `:531`
   skip a primitive only `if prim.blend`; `AlphaMode::Mask` sets `blend = false`
   (`mesh/store.rs:131`). So foliage quads write full-quad depth into the SSAO
   prepass and SSAO shades the tree as a solid box. Not absent — wrong.

Both 3 and 4 need the same fix shape: a fragment stage sampling albedo alpha
against the material cutoff and discarding, which means those two pipelines need
the material bind group they currently don't take.

**Fork in the plan, for the user at the plan gate:**
- **Alpha cards** — needs fixes 3 and 4 first. Correct dappled shadows, cheap
  triangles, works for any species later.
- **Solid micro-geometry foliage** — needle clusters as real tris. Needs no
  renderer change and shadows work today; costs triangles, and a cypress's
  tightly-packed scale foliage suits it where a broad-leaf tree would not.

### chapel_arch rebuild — hypothesis REFUTED, live defect found

Rebuild ran clean (exit 0, 237.4 s texture, 46 stages, 384160 verts) into
`target/prop-batch/arch-rebuild/cand_0/`. **The result is still orange.**
Marginally less saturated than the shipped asset, nowhere near the concept's
pale grey. So "chapel_arch is merely stale" is **wrong** — the current path
reproduces the defect on a fresh run. Staleness was a real difference but not
the cause.

Where the hue dies, measured on this run's own artifacts (R−B on subject texels
only; the concept read against its own alpha matte, the canvas with its flat
background colour dropped — an earlier luma>70 cut let the concept's neutral
grey backdrop in and understated the concept at +9.0):

| stage | R−B | Δ |
|---|---|---|
| `concept_rgba.png` (approved look) | **+16.1** | — |
| generated crops, pipeline's own silhouette mask | **+32.6** | +16.5 |
| blended atlas islands (`prop-cache/blend/…/base.png`) | **+31.1** | −1.0 |

**The whole drift is at generate; the blend slightly cools.** An earlier reading
of this table put the generated canvas at +25.8 and charged the blend +5.3 —
that was a masking artifact, now deleted. The +25.8 came from a modal-background
rejection over the raw canvas, while the blend consumes those same crops through
`depths[i] > 0.01`. Same pixels, two different subject definitions across a
stage boundary; on the pipeline's own mask the blend's input is +32.6, above its
output. Every operation inside `blend_views` is measured and innocent:
colourspace round-trip **0.00** (most texels are dominated by a single
best-facing view, so there is barely any average to skew), `pad_edges` **+0.03**,
facing-weight exponent **+0.71**. Validated bit-exact — the re-run's `base.png`
sha256 matches the cached file.

Per-canvas spread of the generated crops, the substantive finding:

| canvas | views | R−B | seed |
|---|---|---|---|
| canvas_0 | az0 front / az180 back | +30.6 / +23.0 | 0 |
| canvas_1 | az90 / az270 sides | +43.4 / +50.1 | 1 |
| canvas_2 | az0 el−35 | +34.8 | 2 |

Not a uniform warm bias — within-canvas spread ~7 against an across-canvas range
~20, so sampling-pass identity dominates without being exclusive. **Seed is
fully confounded with depth conditioning**: every canvas differs in both. Until
that is separated it is unknown whether the spread is sample lottery (an
anchored init fixes it) or the model free-associating where depth constrains it
least (only a propagating anchor fixes it) — and those imply different-sized
reworks. Cheap probe: re-run two cached depth pairs with their seeds swapped.

The dusk HDRI
(`castilian_plateau_dusk`) then multiplies an already-warm albedo at
roughness 0.85 — which is why it reads as terracotta in engine rather than
merely creamy.

**Root cause:** nothing at any stage binds the output albedo to the concept's
albedo. `prop_texture.py:8-11` states it outright — basecolor is a ControlNet
**depth**-conditioned *text*-to-image pass. Geometry is conditioned on the
concept; colour is re-invented from the prompt string. Z-Image renders
"sun-bleached limestone" warm-cream, so a concept whose whole point is a cool
grey cannot survive.

Explains the entire observed pattern: `olive_stump` (grey-brown) and
`candelabra_shrine` (dark iron) have warm-tolerant albedo so the drift is
invisible — and it is exactly the "stump texture could be better" the user
noticed. `chapel_arch`'s cool grey makes it maximally visible. `cypress` is
unaffected by this (its generated panel was correctly dark olive-green); its
failure is purely geometric.

Ruled out along the way: **atlas gutter bleed.** The gutter fill equals the
island mean by construction ([87,105,119] vs island [87.5,104.8,118.6]), and a
simulated mip chain drifts R−B by only **+0.3** across 7 levels. Not the cause.

- [ ] Rebuild NOT installed — it is no better than the shipped asset, so
      installing it would spend a write for nothing. Left in
      `target/prop-batch/arch-rebuild/`.
- [ ] Needs a rework entry: bind texture albedo to the concept (concept as an
      img2img/IP-Adapter reference, or match the blended atlas's albedo
      statistics to the concept's) — fix direction unvalidated, do not plan
      around a guessed mechanism.

### Albedo binding — fact-find before the plan (2026-07-30)

User chose this track over foliage. The plan's shape turned on facts that were
not on disk, so they were gathered first.

**Conditioning routes that exist at all.** The generate graph
(`workflows/prop_multiview.json`) is pure text-to-image: `EmptySD3LatentImage`
-> `KSampler` at denoise 1.0, cfg 1.0, 8 steps, `res_multistep`, shift 3.0;
depth enters as a *model patch* (`QwenImageDiffsynthControlnet` +
`Z-Image-Turbo-Fun-Controlnet-Union.safetensors`, strength 1.0), never as a
latent. ComfyUI is vanilla — zero custom nodes, no `models/ipadapter`.
**There is no IP-Adapter for Z-Image and `z-image-edit` is unreleased**, so that
route is dead, not merely unbuilt. Union CN supports canny/hed/depth/pose/mlsd,
plus *gray* in the 2602 variant and a *tile* model in the 2.1 release; only the
base union model is installed. Live routes reduce to **img2img** (one node:
`VAEEncode` + denoise<1, model-agnostic) or the **tile CN** (2.1 download).
Both need the same missing ingredient: a per-view colour reference aligned to
that view's ortho depth render.

**The pipeline cannot express a sequential paint loop.** Every canvas is
generated independently from depth alone (`prop_texture.py:182-218`,
`generate.py:77-118`); generated pixels first meet the atlas at one terminal
`blend_views` (`albedo.py:102-155`). `nbv` feeds view *selection* only — its
`extras.json`/`reachable.npy` reach `prop_texture.py:172-179` and the coverage
gate, nothing image- or colour-related. A Text2Tex-style loop would reuse
existing helpers rather than add math: `emission_graph` + `ortho_camera` /
`render_exr` to render the partial atlas into the next view, `view_weight` /
`bilinear` / `pad_edges` to project back. Cost is structural, not arithmetic:
it serialises the currently-independent `generate` units and re-keys their
cache. `generate.py` imports no bpy by design, so the interleaving must be
driven from `prop_texture.py`, which already holds both sides; Cycles here is
CPU, so reprojection renders do not contend with the open ComfyUI server.

**Az 0 is the concept's camera — verified visually, not enforced in code.**
Hi3DGen exports in its fixed voxel frame under a constant image-independent
axis permutation (`cube2mesh.py:91-102`); nothing rotates the mesh to face the
input, so front-facing is a *learned* property of the model. Downstream
preserves yaw exactly (`prop_cleanup.py` joins/scales/translates, no rotation;
`export_yup` round-trips). Checked `chapel_arch` and `crucero` concept against
their az-0 depth: both match feature for feature (arch — column positions,
panels between them, stepped octagonal bases, ogive springing; crucero — cusped
arm terminals, crossing lobes, shaft taper). Two props is a tendency, not a
guarantee, and nothing in the pipeline would detect a flip.

Two offsets that any reprojection design must handle: depth renders sit at
**elevation 15 looking down** while concepts are eye-level, and depth is
**orthographic** against perspective concepts. Tolerable for a hue probe (the
depth patch owns structure); not tolerable for a paint loop assuming pixel
correspondence.

Ruled out as an answer: the silhouette yaw fit. It exists only in
`mv_ab_metrics.py` (an A/B tool), cannot resolve front from back, and
`fitted_yaw_deg` is untrustworthy until `front_back_peak_gap` clears the noise
floor. "Just fit it" is not available.

Rejected on principle, recorded so it is not re-proposed: histogram / albedo-
statistic matching of the atlas to the concept. It corrects the statistic, not
the painting.

**Criterion note.** R−B alone cannot grade these probes — denoise -> 0 returns
the concept unchanged, scoring a perfect +16.1 with no surface synthesised. The
number is paired with a visual verdict on whether a panel actually painted
stone.

- [ ] Route A (img2img) + Route B (tile CN 2.1) probe in flight, user-approved.
      Route B gated on the 2.1 license clearing the shipping-asset-path rule —
      NC or ambiguous means Route A alone. Contact sheet lands at
      `target/probe-albedo-binding/contact_sheet.png`.
- [x] Blend stage cleared — the +5.3 did not exist. It was a mask-convention
      mismatch across the stage boundary, not a defect; blend cools by ~1.0.
      Workstream deleted, not deferred. Numbers in the rebuild section above.
- [ ] Separate seed from depth conditioning in the ~20-point across-canvas
      spread: re-run two cached depth pairs with seeds swapped, 2 passes,
      ~1-2 min GPU. Gates how large the generate-stage fix has to be.
- [ ] Sequential-paint rework NOT priced yet — deliberately deferred until both
      probes report. Do not plan it around a guessed mechanism.

### Both colour-conditioning routes REFUTED (2026-07-30, user-approved GPU probe)

Contact sheet `target/probe-albedo-binding/contact_sheet.png`, 24 panels.
Anchor for the whole sweep, one convention throughout (pipeline's own
`depths[i] > 0.01` silhouette): concept **+16.10**, reference canvas **+26.14**.

**Route A — img2img init latent: no usable window.** denoise 0.05..0.85 return
the init essentially untouched (R−B 15.1 -> 18.7, panels visibly the pasted
concept, no synthesized surface); at 0.9 output snaps to **exactly 26.14**, the
text-only baseline, and holds through 1.0. Mechanical cause: ComfyUI computes
`total_steps = int(8/denoise)`, so an 8-step distilled model exposes only 8
effective levels and the transition is a cliff. 0.75/0.8 -> 10 steps (identical
R−B), 0.85/0.875 -> 9, 0.9/0.95/1.0 -> 8. **Once the model genuinely paints, the
init latent contributes nothing.**

**Route B — tile ControlNet 2.1 (Apache-2.0, licence gate cleared): hue-inert.**
24.6-28.9 across strength 0.05..1.0, never approaching +16.1; above 0.6 the
output collapses into colour-noise/tearing, so those numbers measure noise not
albedo.

**Therefore:** Z-Image Turbo cannot be colour-conditioned by any available
means — no IP-Adapter exists for it, distillation removes the img2img window,
tile-CN ignores hue. This is a property of the model, not of our graph.

**Correction to the sequential-paint premise.** That loop's mechanism is *masked*
generation — painted texels held fixed, new regions generated at denoise 1.0 —
which this probe did NOT test. The loop is not refuted, but it can no longer
lean on partial denoise for hue carry-over; its remaining hope is the model
matching hue across a mask boundary at full denoise. Untested.

Cost note: estimated ~5 min, actual **32 min** (A 20.3, B 12.1). The estimate
was passed on unchecked.

- [x] Tile-CN 2.1 weights deleted 2026-08-02 (see the STATE AT STOP list below).
- [ ] Two candidate mechanisms remain, both unmeasured: masked inpainting on
      Z-Image, and swapping the texture pass to a non-distilled model.
      `Qwen-Image-InstantX-ControlNet-Union.safetensors` is already installed
      and Qwen was kept as the fallback base by the 2026-07-20 ruling.
- [ ] Seed-vs-depth-conditioning confound still unseparated (2 passes, ~2 min).

### Qwen-Image is already staged — swap costs no download (2026-07-30)

All four files present, sha256 recomputed on disk and matching
`scripts/ai-pipeline/models.sha256`, all **Apache 2.0** (verified via HF API
license field, not inferred):

| role | file | size |
|---|---|---|
| diffusion | `diffusion_models/qwen_image_fp8_e4m3fn.safetensors` | 19.03 GiB |
| text encoder | `text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors` | 8.74 GiB |
| VAE | `vae/qwen_image_vae.safetensors` | 242 MiB |
| depth CN | `controlnet/Qwen-Image-InstantX-ControlNet-Union.safetensors` | 3.29 GiB |

`check_models.py`'s `EXPECTED` already lists all four. Confirms
`qwen_3_4b_fp8_mixed.safetensors` is Z-Image's text encoder (CLIP type
`lumina2`), NOT Qwen-Image's — Qwen needs the separate 2.5-VL-7B encoder, also
already present. My earlier cost weighting of the Qwen option as "possible
multi-GB download" was wrong; staging cost is zero.

**Counter-signal against the swap, recorded so it is not lost:** the 2026-07-20
a5b bake-off (`tasks/ai-pipeline/research/a5b-bakeoff-results.md`, 12
generations, this machine) measured silhouette *spill* with both depth
ControlNets active — Qwen 0.018 mean vs Z-Image short-prompt 0.0081. Z-Image was
**tighter**. That proxy is not depth-adherence measured directly, and it says
nothing about an img2img/inpaint pass on painted textures, but the early evidence
leans against Qwen on conditioning tightness and must be weighed, not skipped.

- [x] DONE 2026-08-02: three Cleared rows added to `content/source/CREDITS.md`
      (Qwen-Image + its VAE, Qwen2.5-VL-7B encoder, InstantX ControlNet-Union),
      each re-verified `apache-2.0` against the HF API rather than inherited from
      this note. The a5b spill counter-signal rides the ControlNet row so it
      cannot be lost.
- [ ] Qwen probe NOT launched yet, deliberately: GPU busy, and if masked
      inpainting works on Z-Image the swap may be unnecessary. Cheap test first.
      When it runs, start from the a5b bake-off rather than re-deriving it.

### STATE AT STOP — 2026-07-30

Working tree clean, HEAD `f36c79e`. Nothing committed this session: everything
written lives under `tasks/` (gitignored) and `target/` (gitignored). No tracked
file was modified by me or by any agent.

**Resume here.** The albedo-binding track is mid-fact-find. Three of four facts
are in; the plan is deliberately unwritten because the fourth decides its size.

Settled:
1. The whole drift is at the generate stage. Blend is innocent (cools ~1.0) —
   the +5.3 I once charged it was a mask-convention artifact.
2. Z-Image Turbo cannot be colour-conditioned: no IP-Adapter exists, global
   img2img has no usable window (`int(8/denoise)` step quantisation makes it a
   cliff), tile-CN is hue-inert.
3. Qwen-Image is fully staged at zero download cost, Apache 2.0 — but scored
   *looser* on silhouette spill than Z-Image in the a5b bake-off.

Open, in the order that matters:
- [x] **Masked-inpaint probe landed** (3 passes, 247s). Mechanism works:
      `SetLatentNoiseMask` holds slot 0 within ~0.4 of its anchor in all runs.
      Slot 1 genuinely painted stone (visually confirmed, not degenerate) and
      painted cool. Artifacts `target/probe-masked-inpaint/`.

      Read against the right anchor — the **unmasked baseline for that same
      view**, az180 at +22.97, same depth/seed/prompt — the result decomposes
      instead of being ambiguous:

      | change | slot1 R−B | delta |
      |---|---|---|
      | unmasked baseline (warm generated front beside it) | +22.97 | — |
      | masked, warm slot0 held | +18.49 | −4.5 |
      | masked, concept (cool) slot0 held | +16.10 | −2.4 |

      So hue **does** cross the mask boundary, but weakly: ~2.4 points of
      pass-through from a 14.6-point slot0 difference, ≈16%. The larger −4.5 is
      slot 1's neutral grey init bleeding through (a zero mask forces the latent
      back to the noised init each step) — that is a background colour we paste,
      a knob rather than a binding, and must not be built on. Together they land
      on the concept's +16.10, which is coincidence, not a mechanism.

      **Two design confounds — a rerun must fix both.** The arch silhouette does
      not reach the canvas midline: ~520px of background separates the slots and
      the mask boundary lies entirely in background. So (a) feathering was never
      exercised on painted stone — the seam question is untouched, and (b)
      in-canvas adjacency was far weaker than the design assumed. Masking **half
      of a single object** would test propagation sharply instead.
      Nothing here speaks to back-side *structure*; slot 1 had no reference.

- [ ] Qwen texture-pass probe — hold until the above lands; if masked inpainting
      works, the swap may be unnecessary. Start from the a5b bake-off, do not
      re-derive it.
- [x] `content/source/CREDITS.md` — Cleared rows added 2026-08-02 (see above).
- [x] Seed/depth swap probe RAN 2026-08-02, and it did NOT separate the
      confound — the answer is that the question was underpowered as designed.
      Artifacts `target/probe-seed-depth/` (calibration.json, swap_results.json,
      both swapped canvases + depth masks).
      CALIBRATION PASSED FIRST, and caught an instrument bug: Blender's
      `read_depth` (`proptex/views.py:178-180`) returns row 0 = image BOTTOM
      while `cv2.imread` on the `gen_*.png` crops reads row 0 = top. Unflipped,
      the mask misaligns and the same canvases measure ~18-26 instead of ~23-31.
      After the flip all four originals reproduced to within 0.1
      (+30.61/+22.97/+43.35/+50.10). This is the third mask-convention error in
      this track; the pipeline's own convention is only "the same" if the row
      order is too.
      SWAPPED RESULTS: canvas_0's depth at seed 1 → +39.42/+35.79 (avg 37.6, was
      26.8); canvas_1's depth at seed 0 → +20.99/+45.81 (avg 33.4, was 46.7).
      Both moved TOWARD the new seed's level and neither reached it. That kills
      "pure depth free-association" outright.
      **What blocks the verdict is a missing floor, not a missing pass.**
      canvas_1-depth/seed0 split its two views 20.99 vs 45.81 — a 24.8-point
      WITHIN-pair spread, over 3x the ~7-8 the original canvases showed, and
      comparable to the whole ~20-point across-canvas range this track is trying
      to explain. Every number in the original table is a single sample and no
      per-condition variance floor was ever measured, so "across-canvas range
      ~20" may not exceed the noise. Instance of
      `tasks/lessons/2026-07-30-a-floor-must-cover-the-endpoint.md`.
- [ ] NEXT, and it must precede any generate-stage rework pricing: measure the
      seed-lottery floor — N≥4 seeds on ONE fixed depth condition, same operating
      point (~4-6 passes, few min GPU, needs a §8 go-ahead). If the floor spans
      ~20 points the across-canvas finding dissolves and there is nothing at the
      generate stage to rework. Do not price the sequential-paint rework until
      this reports.
- [x] DONE 2026-08-02: `Z-Image-Turbo-Fun-Controlnet-Tile-2.1-8steps.safetensors`
      deleted (6.71 GB reclaimed). `check_models.py`'s `EXPECTED["model_patches"]`
      never listed it — only the Union CN, which stays — so no script or manifest
      needed touching and nothing can now fail on its absence. Revisiting Route B
      means a re-download.
- [ ] Foliage track untouched, user-approved (Blender procedural generator).
      First step is renderer work: `shadow.wgsl` and `depth_prepass.wgsl` have no
      fragment stage, so glTF MASK geometry casts solid-quad shadows and writes
      full-quad depth into SSAO. Then the alpha-cards vs solid-needles fork,
      which is the user's call.
      PRICED 2026-08-02, and the note's "latent" is WRONG — the bug is **live**:
      shipped `content/models/human.glb`, the player body, is 8/8 `alphaMode:
      MASK` cutoff 0.5 with real cutout alpha in four textures (img5/6/10/11,
      238k-522k texels under 128). Severity today is modest — the cutouts are
      small face-overlay quads coplanar with the head — but they write full-quad
      depth into SSAO every frame. Verified: both shaders vertex-only, descriptors
      `fragment: None` (`shadow.rs:218-231`, `ssao.rs:59-70`), position-only vertex
      layouts. Alpha mode survives import and the cutoff already sits in
      `MaterialUniform.mr.z`, but MASK-ness is not kept as a CPU flag
      (`GpuPrimitive` has only `blend`) and neither pass binds the material group.
      Fix reuses the existing Material BGL — no new uniform, binding or sort
      change; ~230-250 lines over 6 files. No test covers masked shadow or masked
      prepass, so one new analytic test is part of the fix.
      FIXED 2026-08-02, UNCOMMITTED (tree verified, worker did not commit).
      ~600 lines over 8 files, exactly the priced design — no new uniform,
      binding or sort change; masked `mesh_vtx`/`skinned_vtx` variants carry UV
      at location 1, `*_frag_masked` discards on
      `albedo.a * base_color.a < mr.z`, material bound at group 1 static /
      group 2 skinned, and both passes draw opaque-then-masked so each takes one
      extra pipeline switch. New test
      `masked_shadow_cutout_lets_light_through` (offscreen.rs): one frame, three
      regions — lit reference, the cutout's shadow-landing zone, and the opaque
      half's real shadow as an in-frame control; the 45° shadow offset is derived
      analytically, not tuned to the output.
      RED-PROOF, both directions, on the routing flag alone: red
      `lit 185.00 / cutout 1.10 / shadowed 0.84` (cutout as dark as real shadow);
      green `185.00 / 185.00 / 0.84`. The control is byte-unchanged across the
      two, so the fix moves cutout pixels and nothing else.
      Suite 125/125 first run, no fix round. `golden_skinned_human` PASSED under
      its 0.01 mean-FLIP threshold — the predicted shift did not materialise, and
      the reason is geometric: human.glb's cutouts are face overlays coplanar
      with the head, so the light they now pass lands on the head itself. **No
      golden rebake needed.** Worth knowing that the live-severity claim above
      and this null both follow from the same coplanarity — the bug was real but
      its shipped blast radius is genuinely small; the value of the fix is that
      it unblocks foliage.
      Note also validated: `cargo check` never parses WGSL (runtime string), so
      the worker ran both shaders through `naga` 29 directly. Pipeline-layout
      compatibility against the Rust BGL is still only checked by running.

**Decided while unsure:** let the in-flight GPU probe run to completion rather
than killing it — its artifacts land on disk and are self-describing, so the
spend is not wasted, but nothing in this note depends on its outcome.

Lessons touched this session: `orchestrate-never-implement` un-struck and its γ
widened to cover discovery (reading source, probing, researching), not just
editing; `the-instrument-cannot-grade-itself` γ widened to cover any quantity
compared across a stage boundary, since each stage offers a different convenient
subject definition and the delta then belongs to the conventions.

# Cypress alpha-card rebuild (2026-08-04 →) — ACTIVE

Plan: `~/.claude/plans/peaceful-cuddling-kurzweil.md` (approved 2026-08-04).
User chose alpha cards over solid micro-geometry at the session checkpoint.
Prereq landed: `12c7e4b` (masked shadow/prepass/SSAO). Zero ML GPU; the only
contingency is a ~10-min Z-Image fallback if the CC0 atlas fails T0, listed in
the approved plan (= its §8 go-ahead). Texture source: Pawel Olas CC0 scans
(treesdesigner.com/materials-library, license verified in-session).

- [x] T0 DONE: CC0 confirmed VERBATIM from the author's own site comments
      ("Yes. All cc0." / "the textures are released under cc0 license."),
      page HTML + quotes + sha256s in target/cypress-build/source/
      LICENSE_EVIDENCE.md. Only leaf12 is conifer (Thuja/Chamaecyparis-habit
      scale fronds; leaf09/11 404, rest broadleaf). One 2048² continuous
      frond scan (basecolor/normal/normalB/opacity/rough/height EXRs);
      5 usable crops, alpha coverage 0.20–0.63, all in band. Scan is bright
      green (mean ~0.33/0.55/0.15) → regrade to concept olive is load-bearing.
      No dry-brown scan (synthesize in T1) and NO BARK in the pack (T1
      sources a CC0 bark tile from ambientCG + records license evidence).
- [x] T1 DONE (uncommitted): cypressgen/atlas.py (pure numpy, no bpy) +
      build_cypress_atlas.py driver + NEW scripts/ai-pipeline/color_math.py
      (srgb_to_lab extracted — color_cast.py's PIL import breaks under
      Blender's Python; color_cast now imports it, behavior unchanged).
      Atlas at target/cypress-build/atlas/ (base RGBA/normal/ao 2048² + 11
      islands: 7 spray, 2 dry, 1 bark, 1 core). Bark = ambientCG Bark012
      (oak — no CC0 cypress bark exists; closest ridge profile), evidence in
      source/bark/BARK_SOURCE.md. Numbers: ΔE 3.54 to concept, S 0.309,
      hue 52°, normal mean 127.9/128.1 (chose `normal` over near-flat
      normalB), AO mean 0.919 std 0.112, mip ladder 1.03/1.06/1.13/1.24
      (coverage GROWS — thinning risk low). All 5 gates raise AtlasGateError,
      red-proven. Worker corrections, evidence-backed: Lab/RGB regrades
      produced magenta streaks → closed-form HSV regrade (0 magenta px);
      AO formula eased (spec literal measured 0.953 mean, out of band);
      mip red-proof needed a synthetic hairline pattern (erosion cannot
      fail this gate on real data — ratio stayed >1.0 at 15 px).
- [x] T2 DONE (uncommitted): check_registry procedural case (requires
      surface_class/height_m/tri_budget/texture_size, forbids
      subject/view_res/azimuths) + ProceduralContract in proptex/registry
      (GeneratedContract NOT reused — its subject/view_res are mandatory,
      reuse would misrepresent). content_lint claim VERIFIED TRUE: non-kit
      non-downloaded lands in the else-arm (occlusion required, MR forbidden,
      class values exact). 3 red-proofs fired with correct messages;
      assets.json untouched (git diff clean); registry still OK on live data.
- [x] T3 DONE (uncommitted): generator complete. Seed 7 canonical: 9664 tris
      (680 core / 8400 cards / 784 trunk), 1050 cards, h 9.0006, base 0.000,
      max radius 0.99 → h/w 4.54 (band 4.5–5.5; seeds 1/7/42 all in band).
      Blender 5.2 exporter maps CLIP → alphaMode BLEND, NEVER MASK → driver
      patches the GLB JSON chunk every run (verified, not assumed). Sky
      holes ruled out numerically (17 centerline samples below background
      luminance). WALL RESOLVED by orchestrator (forced, logged): plan's
      R=0.20·h + horizontal droop gave h/w 1.7 vs the 4–6 gate; corrected
      to R=0.10·h OUTER envelope, upswept sprays 5–20° from vertical,
      anchor = envelope − card_radial_reach (clamp to core, shorten card).
      Plan file amended. Worker's own fixes: droop trig ground-pierce,
      core/trunk island UVs, fringe reach-bounding (was overshooting to
      1.67 m), CARD_T_HI 0.96 (apex overshoot after the frame flip).
- [x] T4 DONE (uncommitted): cypressgen/verify.py — pure GLB-byte parser
      (no bpy; exporter bakes split normals + transform into accessors, so
      bytes are authoritative), wired to fail the build. Card witness is
      independent: a triangle whose 3 UVs land in one spray island IS a card
      tri (no island is shared with core/trunk). All 11 asserts green on
      seed 7; all 11 red-proofs captured (target/cypress-build/
      verify_redproof.json), geometry ones through the wired driver's real
      exit code. Assert #10 caught a REAL defect: card-quad normals used the
      anchor's radial, not the vertex's — 3 visible crown-tip vertices off
      band; 5-line root-cause fix in geo.py accepted (tri/AABB bit-identical
      pre/post). Note: Blender's UV flip and glTF's V flip cancel exactly —
      shipped V is direct py/2048 (documented in verify.py).
- [x] T5 DONE (uncommitted): content_lint `foliage_props_are_alpha_masked`
      (foliage surface_class ⇒ every primitive Mask(0 < c ≤ 0.5) +
      base_color_image). Mirrors prop_material_matches_surface_class's
      helpers, zero new ones. DELIBERATELY RED right now against the shipped
      opaque cypress ("alpha_mode Opaque is not Mask(0, 0.5]") — that is the
      red-proof; T6's promotion turns it green. Suite otherwise 21/21;
      predicate sanity-run live both directions on all six AlphaMode cases;
      lint-comments 0 hits.
- [x] T6 DONE (uncommitted): install_asset --procedural branch (refuses on
      hash mismatch / missing provenance field — both red-proved with
      captured messages; build_steps untouched). Promoted: cypress.glb now
      7.23 MB (was 16 MiB), sidecars img0-2.dds + manifest, no orphans.
      assets.json kind procedural / height_m 9.0 / subject+view_res gone;
      zones.ron five scales 0.95/1.00/0.85/1.10/0.90 by position match;
      CREDITS.md cypress row + note rewritten, leaf12 + Bark012 CC0 rows
      added with verbatim quotes + sha256s. content_lint 22/22 GREEN (incl.
      foliage MASK + fresh sidecars), check_registry OK, texture budget
      224.3/1024 MB. ENV NOTE: smirk/texconv.exe was absent on this machine
      — downloaded from microsoft/DirectXTex may2026 release (gitignored).
- [x] T7 DONE (uncommitted): asset_inspect gains Distance::Far (55 m, eye
      height, reuses aim_close) + --stats (mean H/S/V over non-background px;
      hue is a circular mean; STATS line per beauty frame). Background is the
      frame's corner pixel, NOT alpha — mesh_shader writes alpha 1.0
      everywhere so alpha cannot separate; corner is bit-exact vs the clear
      chain per offscreen's clear_only_render_is_uniform. Red-proofs:
      independent Pillow recompute agrees < 1e-4; synthetic red fixture reads
      s=0.909 with background excluded; far vs gameplay coverage 10.8% vs
      99.2% (~9× smaller). cargo check green. Bin needs --features offscreen.
- [x] T8 DONE: full evidence at target/review/cypress/ (MANIFEST.md; 31 zone
      frames incl. wide + mid_cypress_nw/se via a TEMP NamedShot addition
      (reverted, zone_review.rs verified clean) + close_cypress with player;
      288 inspect frames far/full/gameplay × ship/raking × 4 channels ×
      6 az; 72 STATS lines). Cypress means (ship): far s 0.047 v 0.774
      (fog-tinted), gameplay s 0.072 v 0.433 — clear of S 0.35 / threat
      band. No render errors. Leftover dup dir zone_pairs/ in target/
      (delete hook friction, harmless). SECURITY NOTE: worker reported two
      injected system-reminder-style messages during its run instructing it
      to hide file modifications; it refused and verified both files honest
      — relay to user.
- [~] T9 ROUND 1: **FAIL, 1 blocker** — record
      .claude/docs/reviews/town/cypress-cards-2026-08-04.md. Scores
      9/4/9/9/8/8/10/7/6. Shards-failure GONE, grounding 10/10, mip ladder
      confirmed in frames. BLOCKER B1: cards read as rectangles at all
      azimuths — spray islands carry opaque alpha to 2–4 rect borders
      (38–73% border texels > cutoff; islands are quadrant crops, fronds
      severed by construction; no border-alpha assert exists). Required:
      F1 print_stats masking (corner-pixel excludes NOTHING under ship sky —
      published stats measured the sky; judge re-derived by hand: tree
      h 66.8° S 0.099 V 0.125, passes with margin), F2 spend tri headroom
      on more smaller cards (9,664/24,000 used), F3 darken pale cream trunk
      bole. Minor: 0.26% magenta filaments, 7.65% texels in threat band
      (mean fine), profile jitter. Camera fact: full-distance turntable
      pitch 45.8° compresses h/w to 3.2 (cos 0.8 rad) — far arm is the
      honest silhouette read. Non-gating gap: mid_cypress_nw/se frames came
      from a reverted temp shot edit → make the two cypress NamedShots
      permanent (P2.4-F7 precedent). Lesson recorded in memory
      (checks-must-fail-when-broken: red-proof under deployment condition).
      FIX ROUND dispatched: worker A = atlas re-crop + border assert +
      F2/F3 + minors + rebuild/re-verify/re-promote; worker B = F1 stats
      masking (red-proof under SHIP lighting) + permanent cypress shots.
      Then re-render + fresh-judge re-gate.
      WORKER B DONE (2026-08-04): F1 fixed via background-only double
      render (non-beauty channels still draw the ground quad — diff mask
      was the only mechanism that isolates the subject). Second bug found
      during red-proof: bloom's blur pyramid is global, so occluding sky
      shifts EVERY pixel between the pair — stats render the diffed pair
      with bloom forced to 0 (judged PNG keeps normal bloom). Red-proof
      under ship lighting: mean h≈69° S≈0.10 V≈0.15 (judge hand-derived
      h≈67° S≈0.10 V≈0.13; old sky reading h≈203° V 0.43+ gone);
      independent Python mask cross-check IoU 0.96, zero false negatives;
      studio regression still sane; --reference path smoke-tested.
      cypress_nw/cypress_se now permanent in ROCALBA_SHOTS
      (zone_review.rs:392-421), reproduce from clean checkout. Evidence:
      target/review/cypress-fixB/. Scope confirmed: only asset_inspect.rs
      + zone_review.rs touched.
      WORKER A DONE (2026-08-05): B1 fixed by construction, not discovery —
      window search (summed-area table) proved the scan has NO usable
      naturally-bordered window, so islands are matted: find_crop_centers
      picks 7 separated real-density centers, organic_vignette mattes each
      to an irregular harmonic-perturbed blob hitting literal 0 alpha ~13px
      inside the crop edge. 11 islands (7 wet + 2 dry recolors + bark +
      core). New gate assert_island_border_alpha (outer 8px ring < 2%
      above cutoff) red-proofed: OLD shipped atlas fails 21.9–50.2% across
      all 9 islands; new atlas 0.0%; vignette-skipped build 48.3% rejected.
      F2: 2500 cards (was 1050), card length ×0.625, 21,264/24,000 tris;
      verify card band raised 1800–3000; sky holes 0.14% (2/1440 fine rays,
      crown apex only) via new reusable check_cypress_skyholes.py.
      F3: bark was shipping UN-regraded (H42.7° S0.43 V0.54) → H30° S0.28
      V0.20. Minors: threat band 5.56%→0.0%, magenta at natural baseline
      0.024%, profile jitter + per-card UV mirror (flip_u) replacing the
      rotated-duplicate-island trick. Chain green: atlas gates → 11 verify
      asserts → install_asset --procedural (sha match) → check_registry →
      content_lint 22/22. Worker's own preview: no straight-edge card
      boundaries at close-up, canopy closed, bole dark.
      STOPPED HERE by user instruction ("stop after current work ends").
      NEXT SESSION: T8 evidence re-render (zone_review start now includes
      permanent cypress shots; asset_inspect far/full/gameplay matrix +
      fixed --stats on re-promoted asset) → FRESH Opus judge, T9 round 2,
      same 9 criteria + explicit B1-recheck at close → if pass, T10
      (cargo test --workspace once, lint-comments.sh, check_registry,
      test_cypressgen.py — NOTE: this pytest file was in the plan's create
      list but was never created; create it at T10) → commit, no
      attribution trailers. All work UNCOMMITTED on ai-pipeline.
      SUPERSEDED 2026-08-05: the rebuild was COMMITTED `1a5bf6c` (00:45)
      by the prior session WITHOUT the round-2 gate, and the on-disk T8
      evidence predated the re-promoted glb. Chain resumed this session.
      T8 RE-RENDER DONE: target/review/cypress-r2/ (32 zone + 296 inspect
      PNGs, MANIFEST.md, stats.txt; asset confirmed the 2500-card build;
      no tracked source touched).
      T9 ROUND 2 (fresh Opus judge): **FAIL — 1 blocker, 1 required,
      2 minor.** Scores 9/8/9/9/9/4/10/6/6. Record appended to
      .claude/docs/reviews/town/cypress-cards-2026-08-04.md ("Round 2").
      B1 DEAD at source (border_alpha_gate 0.000 all sprays; zero
      straight runs at the exact R1 defect coordinates). F1/F3/M1/M2
      verified DONE from pixels; F2 PARTIAL (silhouette finer, internal
      register coarser — islands are 5-10 fat lobes, no serration).
      NEW BLOCKER B2: core spindle bare at the crown — smooth untextured
      cone above the canopy on all 5 placements from 30 m in; spindle
      runs to y=9.0 vs top spray vertex 8.878; crown card density 92/m
      vs 301/m mid-band; blade legible ~0.7 m. Regression vs R1's
      blunt-rounded crown. M3 (crown repeat) rides B2.
      REQUIRED F4 (rides B2's round): restore needle register —
      find_crop_centers picks 384 px windows at native scan res where
      single branchlets fill the window; larger windows or downsample
      first. Border-alpha gate is orthogonal, stays green.
      MINOR M4: fixed stats mask ~14% wider than hard silhouette,
      inflates V by ≈0.06.
      NEW WATCH: far-arm STATS measure the ship fog, not the asset
      (55 m silhouette repainted to h≈217°; judge REJECTED the AA/edge
      attribution with an erosion probe, S rose when eroded). Mip
      ladder RESOLVED; shot-coverage gap CLOSED. Fix round dispatched
      (worker A: B2+F4+M3 + crown-coverage verify assert red-proofed +
      rebuild/re-verify/re-promote; worker B: M4). Then re-render +
      fresh-judge round 3.
      FIX ROUND 2 DONE (both workers, 2026-08-05, UNCOMMITTED):
      M4 = BG_EPS 8→32 in asset_inspect print_stats (erosion tried and
      rejected with numbers — card-edge halos riddle the interior);
      V 0.197→0.133 vs hand-derived 0.136, IoU 0.991-0.994 (was 0.96),
      --reference + studio paths sane. B2 = three levers (CARD_T_HI
      0.96→0.97 AABB-safe over 100 seeds; +320 crown cards t∈[0.82,0.97]
      via a second generate_cards call; core_radius taper above t=0.85)
      after an offline ray-cast sim showed cards alone can't close it in
      budget; new verify assert _assert_crown_coverage (area-ratio ≥4.0,
      alpha_coverage scalar persisted in atlas_islands.json; ray-cast
      form rejected — wrong pass/fail shape, and PIL absent in Blender
      py), red-proofed on the real GLB (ratio 0.000 with crown cards
      dropped); shipped ratio 5.93. F4 = crop search on 2× downsampled
      mask, CROP_WIN 840 native px (islands now multi-branchlet
      serrated sprays, confirmed on cypress_base.png); border gate 0.0
      all islands, red-proof intact. M3 judged satisfied by B2 (escape
      clause used — flag for the round-3 judge). Build: 2820 cards,
      23824/24000 tris, h/w 4.73, skyholes 0/432. Chain 1-7 all green
      incl. content_lint 22/22 + re-promotion sha match.
      T9 ROUND 3 RE-RENDER: target/review/cypress-r3/ (same matrix;
      gameplay ship stats mean h~65.5 s~0.094 v~0.121).
      T9 ROUND 3 (fresh Opus judge): **PASS — 0 blockers, 0 required,
      2 minor.** Scores 9/9/9/9/9/9/10/7/7. Record "Round 3" appended
      at line 807 of cypress-cards-2026-08-04.md; supersession pointers
      on rounds 1+2 now point at round 3. B2 DEAD (cutout-free apex run
      0-3 px all azimuths; core radius above y=8.8 is 0.0011 m; top card
      vertex 8.9845; crown density 322/m). B1 still dead on re-cropped
      atlas (border alpha 0.0000 all sprays; longest straight run 8-16 px).
      M3 upheld — five crowns read distinct, no crown mechanism owed,
      stays open at original weight. F4 verified (+42% perimeter/area);
      M4 verified (V within 0.005 of judge's independent mask).
      Colour law clear with margin. CARRIED MINORS: M3 (profile jitter);
      M5 NEW — needle unit ~2x concept sprig, tri budget spent
      (23824/24000): further fineness must come from the atlas, not
      card count. WATCH: raking_beauty full hue 25.7-26.6 within 1.6
      of threat band (warm grazing preset, not asset — albedo hue 53);
      enclosed holes 0.94-1.28% (was 0.57-1.15). RECORD CORRECTION:
      unique alpha cutouts are 7, not 9 (both spray_dry_* byte-identical
      in alpha to spray_02/05) — still inside D7's 6-10.
- [x] T10 DONE 2026-08-05, committed `8e43a97` ("Close crown gap and
      re-crop needle atlas for the cypress alpha-card canopy", 13 files,
      +299/-44, tree clean, not pushed).
      test_cypressgen.py CREATED (scripts/asset-pipeline/cypressgen/):
      6 pytest tests, pure-math only (card count band across seeds,
      t-range, core taper monotone, card AABB under 9.1 via reproduced
      _card_quad formula, verify_export green on shipped glb +
      rejects corrupt glb). Runs via C:\Python314\python -m pytest
      (numpy 2.5.1 + pytest 9.1.1 there). Every assert red-proofed
      (temp perturb -> red -> revert, git diff clean). bpy paths
      (geo/material/atlas orchestration) left untested — no shims.
      lint-comments.sh 0 hits (scope excludes scripts/; worker
      self-reviewed comments, removed one plan-citation).
      check_registry.py OK — NOTE actual path is scripts/ai-pipeline/
      check_registry.py, not asset-pipeline. cargo test --workspace
      ONCE: 456 passed, 0 failed, 5 ignored (loss/soak, release-only).

CYPRESS ALPHA-CARD REBUILD CAMPAIGN CLOSED 2026-08-05 at `8e43a97`
(gate record: docs/reviews/town/cypress-cards-2026-08-04.md, Round 3
PASS). Open follow-ups carried as minors, NOT scheduled: M3 profile
jitter; M5 needle unit ~2x concept sprig — tri budget spent, any
further fineness must come from the atlas.

## Debt notes — orphaned grunt spawns cleanup (2026-08-01)

- ~~Wave budget counter latent bug~~ WITHDRAWN 2026-08-02, no code change: the
  conclusion does not follow from its own premise. The cap counts LIVE
  entities, so a spawn that fails contributes nothing to count *and* nothing to
  the world — there is no over-population to throttle. Within a tick the
  local `*count += 1` at `world/mod.rs:224` covers entities queued but not yet
  spawned, and `self.pulses[i][wi] = (day, due)` forfeits over-cap pulses
  unconditionally, so no catch-up burst survives to the next tick either. Same
  standard as the claim it retires: this is a code read, not a measurement, and
  it would take a resolving wave prefab to observe either way. Original note
  below, kept as the thing being answered.
  Wave budget counter latent bug: the wave budget counter in
  `game/vordar-game/src/world/mod.rs:178-181` is built by counting live
  `EventSpawned` entities. When a spawn fails, no `EventSpawned` marker is
  created, so the count stays 0 and the `*count < wave.max_alive` guard at
  `world/mod.rs:222` never throttles. Harmless while nothing spawns; the
  moment a wave prefab resolves, every pulse fires at full width, uncapped.
  Not fixed here — this change removes the failing spawns, not the guard
  defect.
- ~~`content/zones/zones.ron:147` stale "same deferral as start" comment~~ and
  ~~`server/vordar-server/tests/zones.rs:129`'s false "east = chapter02"~~ both
  corrected 2026-08-02. The second half of that note was itself wrong: the test
  overrides `test_zones()`, a synthetic fixture, not the shipped file — it never
  claimed to verify zones.ron, so there is nothing to un-overwrite. The shipped
  topology is verified separately by `shipped_topology_is_valid`.
