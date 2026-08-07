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
- [ ] 1.2 Terra: atlas-as-asset (facade load + VfxAtlasMeta); export fallback
      `content/textures/vfx/core/` atlas; DELETE atlas_pixels/create_particle_atlas/
      ATLAS_GRID + 2 atlas tests; headless rotated-particle analytic test.
- [ ] 1.6 Luna: hot-reload watcher for content/vfx (notify, debounced,
      parse-error keeps old library).

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
- [ ] 2.3 Luna: vfx_atlas_pack.py + pytest; install_asset.py `vfx-atlas` kind;
      bake_textures.mjs BC4 class.
- [ ] 2.4 Luna: content_lint — atlas sidecars + sprite-name resolution.

## Phase 3 — Harness (after 1.4)

- [ ] 3.1 Terra: bin/vfx_review.rs (per-frame PNGs, stats.json, seeded,
      skip-clean w/o GPU) + smoke test.

## Phase 4 — Style packs (after 1.5 + sprites installed)

- [ ] 4.0 Terra: generate + gate + install showcase sprites (GPU run 2) →
      content/textures/vfx/showcase/.
- [ ] 4.1–4.5 Terra: author pyro/wisp/sigil/censer/shard packs,
      content/vfx/showcase/<style>/{cast,projectile,aoe}.ron.

## Phase 5 — Judgment

- [ ] 5.1 Orchestrator: vfx_review --all (GPU run 3) + anonymize to pack-a..e.
- [ ] 5.2 Sol judge: blind rank (art-law fit, combat legibility, craft ceiling,
      perf headroom). Defects + severity only.
- [ ] 5.3 Orchestrator: verdict doc + ability-migration note.

## Review

(fill at close)
