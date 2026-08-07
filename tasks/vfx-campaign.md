# VFX Register Exploration Campaign (2026-08-07 →) — ACTIVE

Plan: `~/.claude/plans/shiny-hopping-bengio.md` (approved 2026-08-07). Particle
system v2 (production), AI sprite pipeline (Z-Image Turbo only on shipping path),
`vfx_review` offscreen harness, 5 showcase style packs (pyro / wisp / sigil /
censer / shard — technique varies, VQ-A4 color law holds), blind Sol judge verdict
→ `.claude/docs/vfx-register-verdict.md`.

Approved GPU runs (one at a time): sprite gen ~20–30 min · re-roll ~10 min ·
vfx_review --all capture ~10–15 min.

Execution model: orchestrator dispatches per plan's phase table (seats Sol
hard-implement / Terra / Luna); serial verify of each diff; commit only
workspace-green batches. NOTE: another session owns models/textures work —
stage exact pathspecs only, never sweep.

## Phase 1 — Engine v2

- [x] 1.1 Sol: ParticleInstance repack (cell, cell_next, rotation, frame_mix),
      shader rotation + flipbook crossfade, grid via FxParams. VERIFIED:
      diff inspected (4 files +85/−34, surgical); `cargo test -p engine-renderer`
      126 lib + 33 offscreen green incl. new offset asserts + naga shader
      validation test (red-proofed by worker). FxParams binding widened to
      VERTEX_FRAGMENT (vertex reads grid — forced, correct). Uncommitted:
      batches with 1.3+1.4 for workspace-green commit.
- [x] 1.3 Sol: EffectDef/EmitterDef/curves/shapes in game vfx.rs; BurstDef
      deleted; recursive load_dir; 5 ability RONs + 3 prefab trails migrated;
      core atlas.ron authored. VERIFIED: diff exact (+587/−55 in-bounds),
      `cargo test -p vordar-game` 75 lib + 22/22 content_lint green.
      RULING absorbed: content_lint parsed prefabs via lossy `ron::Value`
      (drops enum variant names) — approved 2-line fix to `RawValue` (engine's
      own mechanism); worker red-proofed the lint empirically (impact removed →
      panics at :213; restored byte-identical). Uncommitted, batches with 1.4.
- [x] 1.4 Sol: client sim v2 + trigger sites (absorbed 1.5's site migration).
      VERIFIED: 69 lib + integration green; footprint 4 client files
      (+837/−244). Approved deviation: no follow-position field (no caller —
      dead code). Shape semantics documented on sample_shape; trail runtimes
      cached per entity; unknown sprite = fail-soft log+skip (lint owns hard).
- [x] 1.5 Orchestrator: `cargo test --workspace` ALL GREEN (0 failures across
      every suite). Committed 9eba159 (engine v2 batch, 18 files) +
      b5e6a7a (sprite tooling, 4 files), exact pathspecs.
- [x] 1.2 Terra: atlas-as-asset DONE (facade set_particle_atlas, PNG via
      existing image path, white-placeholder default, resize preserves grid;
      atlas_pixels/ATLAS_GRID + 2 tests deleted; core atlas.png 2×2 256²
      verified per-pixel vs atlas_pixels before generator deletion; offscreen
      harness gained the particle pass with live-frame-identical compose
      split; rotated-streak analytic test red-proofed both directions).
      Approved boundary crossing: game vfx.rs:606 grid assert 4→2 (forced by
      grid change). Stale atlas_pixels citations in vfx_post repointed
      (orchestrator, comment-only). VERIFIED 296 tests 0 fail across 3 crates.
      Committed 941c30e.
- [x] 1.6 Luna: hot-reload watcher DONE (vfx_reload.rs; pre-validates all
      RONs then whole-library swap, else keeps old; VfxGeneration bump clears
      trail cache — defense-in-depth, honestly documented as not-currently-
      coupled; caught+regression-tested a drain bug in the copied engine.ron
      precedent: any() short-circuits the batch). VERIFIED 81 tests green.
      Committed e649f99.

## Phase 2 — Sprite tooling (after 1.3 locks atlas.ron shape)

RULING (2026-08-07, orchestrator, evidence
`docs/vfx/ruling-sheet-flipbook-retired.png` + smoke run): sheet-based flipbook
generation retired — text-to-image has no temporal notion across grid cells
(4 near-identical frames + white gutters on the smoke sheet). Flipbooks are now
SEPARATE per-frame images: seed variants (churn/flicker) or staged keyframe
prompts (evolution), smoothed by the engine's cell_next crossfade; a crossfaded
wrap is seamless by construction, so the loop gate is deleted too, not fixed.
Single-sprite quality confirmed high (photoreal incense wisp on first try).

- [x] 2.1 Terra: vfx_sprite.json + gen_vfx_sprite.py (Z-Image Turbo,
      provenance, --stages ordered-prompt frames, candidate seeds shared across
      stages, owns ComfyUI lifecycle). Ratified: --prompt deleted (one-stage
      spec covers it). Re-smoke clean (2 frames, centered, no gutters); stale
      smoke_puff evidence deleted. Committed b5e6a7a.
- [x] 2.2 Terra: vfx_post.py + 9 pytest green (Rec.709 mask, black-point p0.5
      whole-image, clip gate pre-centering + border gate post-centering, both
      on quantized bytes, integer-pixel centroid centering, RGBA8 [b,b,b,b]
      linear, fail=no PNG+exit 1; red-proofs incl. no-wrap). Committed b5e6a7a.
      RULING: no img2img continuation path — staged prompts don't bind
      silhouette (spark burst vs flame plume at shared seed); packs use
      variant-crossfade churn + runtime curves instead (sigil reveal = static
      glyph + curves). Revisit only if pack authoring hits the wall.
- [ ] 2.3-deferred: install_asset.py `vfx-atlas` kind — BLOCKED: file dirty
      from the models/textures session; dispatch after it commits.
- [x] 2.3a Luna: vfx_atlas_pack.py + 7 pytest green (pixel-exact placement,
      row-boundary flipbook contiguity, >64-cell refusal red-proof,
      determinism, duplicate-name refusal); bake_textures.mjs `mask` mode
      BC4_UNORM linear, verified via DDS DX10 header dxgiFormat=80 + texconv
      stdout. VERIFIED + committed de190d4. (install_asset.py part split off
      to 2.3-deferred below.)
- [x] 2.4 Luna: content_lint — vfx_atlas_sidecars_are_fresh (VQ-C5;
      {source?, images} manifest convention; missing manifest OK for core,
      stale hash red) + vfx_sprites_resolve_in_atlas (VQ-E3; via real
      load_dir; showcase defs → showcase atlas else counted skip; prefab
      trails + impacts via RawValue pattern). Both red-proofed. One
      correction round: worker minted colliding VQ tags blind (visual-quality
      law lives in .claude/, outside its Glob) — relabeled to VQ-C5.
      VERIFIED 24/24 green. Committed a3edc0e.
- [x] pre-4.0 Terra: set_particle_atlas DDS routing DONE (one
      load_color_texture helper, both facade + offscreen callers; BC4_UNorm
      DXGI mapping added to parse_dds; BC4 fixture test; worker e2e-verified
      real BC4 atlas renders on adapter). Found while reconciling packer
      manifest vs lint: staging keeps packer manifest as
      generation_manifest.json; install writes {source, images} content
      manifest. VERIFIED 127 tests green. Committed bb84c26.

## Phase 3 — Harness (after 1.4)

- [x] 3.1 Terra: bin/vfx_review.rs DONE after one correct STOP (offscreen had
      no mesh+particles entry point — ruled entry-point gap; render_scene
      delegate authorized). Approved deviations: VfxLibrary::keys() sorted,
      hand-beat lateral offset (spawn inside capsule was invisible), zone
      lighting from zones.ron (exposure 0.576 — bloom unjudgeable at wrong
      exposure), MovingEmitter accumulator (ActiveEmitter pins pos).
      --vfx-dir + fixtures make all 3 staging branches red-able; 2 checks
      red-proofed by breakage. VERIFIED: 6 gated tests + live bolt run
      reproduced stats byte-identically + frame eyeballed (capsule, shadow,
      bloomed sparks). NOTE: gated tests need explicit
      `cargo test -p vordar-client --features offscreen --bin vfx_review`.
      Committed 4f3a75d.

## Phase 4 — Style packs (after 1.5 + sprites installed)

- [~] 4.0 Terra: IN FLIGHT (GPU run 2, ~20–30 min) — 40 cells / 8×8 / 2048²:
      pyro_{ember,flash,smoke×8}, wisp_{soft,streak,flame×8},
      sigil_{glyph_a,b,c,spark}, censer_{haze,mote,smoke×8},
      shard_{sliver,flare,twinkle×4}. 3 candidates/frame, vfx_post triage,
      pack→BC4 bake→install with {source,images} manifest. Sigil constraint:
      abstract ornamental geometry only, no script/real symbols. Authorized:
      --cell-size Lanczos in packer if load_cell only validates.
- [ ] 4.1–4.5 Terra: author pyro/wisp/sigil/censer/shard packs,
      content/vfx/showcase/<style>/{cast,projectile,aoe}.ron.

## Phase 5 — Judgment

- [ ] 5.1 Orchestrator: vfx_review --all (GPU run 3) + anonymize to pack-a..e.
- [ ] 5.2 Sol judge: blind rank (art-law fit, combat legibility, craft ceiling,
      perf headroom). Defects + severity only.
- [ ] 5.3 Orchestrator: verdict doc + ability-migration note.

## Review

(fill at close)
