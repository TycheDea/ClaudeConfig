# SSAO quality — root cause + fix options (2026-07-31)

User ruling: "ssao shadows look really bad … we should solve it asap." Scope includes replacing
the technique. Quality outranks time/cost; licensing is the only hard gate.

## Current implementation (verified)

- Forward renderer, no G-buffer. Depth-only prepass (full-res Depth32Float, `fragment: None`,
  position-only vertex layouts) feeds a **half-res** hemisphere-kernel SSAO pass, then a 3×3 box
  blur; shading multiplies the blurred AO into IBL ambient only
  (`smirk/engine-renderer/src/frame.rs:278-283,470-544`, `ssao.rs:186-247`,
  `snippets/pbr_common.wgsl:96-97`).
- Kernel: 16 fixed hemisphere points, world-space radius **3.0 m** (`ssao.rs:18`), depth bias
  **0.2 m** (`ssao.rs:29`), per-pixel white-noise rotation (`hash12` sin-fract,
  `ssao.wgsl:53-68`), binary occlusion test with `clamp(radius/diff)` range check
  (`ssao.wgsl:110-127`).
- Normals: **screen-space derivatives** of depth-reconstructed world position —
  `cross(dpdy(world_pos), dpdx(world_pos))` (`ssao.wgsl:98`).
- Depth fetch: nearest-texel `textureLoad` at `floor(uv * dims)` (`ssao.wgsl:81-85`).
- Camera: znear 0.1 / zfar 400, standard (non-reversed) perspective (`camera.rs:32-49`).
- No TAA/temporal anything in the renderer; no compute passes exist yet (grep: zero
  `ComputePipeline`/`begin_compute_pass` hits).
- AO texture R8Unorm half-res; shading upsamples with a plain linear sampler.

## Root causes

| # | Defect | Evidence | Class |
|---|--------|----------|-------|
| RC1 | **Derivative normals are noise.** `dpdx/dpdy` runs per 2×2 quad over texel-quantized reconstructed positions, at half-res (each derivative spans 2 full-res pixels). Flat walls get per-quad normal jitter; silhouette quads get garbage normals. This is the origin of the acne. | `ssao.wgsl:98`; the ssao.rs:19-29 comment itself names this noise as the reason for bias 0.2 | implementation |
| RC2 | **Nearest-texel depth fetch breaks grazing angles.** The kernel sample projects to an exact uv, but `depth_at` snaps to a texel corner — up to ~1 texel of surface slope error. On a wall near 90° grazing, one texel of slope is tens of cm of linear depth ≫ any sane bias → false occlusion. Explains the residual min-zoom grazing trace that bias 0.2 could not kill. | `ssao.wgsl:81-85,119-126` | implementation |
| RC3 | **Bias 0.2 m is a symptom patch that deletes the good part of AO.** Any crease shallower than 20 cm produces zero occlusion — exactly the crisp contact darkening AO exists for. What survives is only large blobby occlusion → the "improved ~10%" look. | `ssao.rs:29` (comment admits it exists to mask RC1 noise) | patch over RC1/RC2 |
| RC4 | **Radius 3.0 m + binary test + saturating range check = halos, undersampling, edge brightening.** 16 samples over a 3 m hemisphere is severely undersampled; `clamp(radius/diff)` is 1 for any depth gap < 3 m so mid-range geometry occludes at full strength (wide dark halos around objects vs walls/ground); near the camera the kernel spans much of the screen and offscreen samples are skipped → view-dependent brightening. The radius was inflated (comment, `ssao.rs:10-17`) to compensate for the crease band collapsing — a consequence of the falloff-free binary estimator, i.e. a tuning patch on an estimator defect. | `ssao.rs:18`, `ssao.wgsl:111-126` | patch over estimator defect |
| RC5 | **Quality-blind denoise chain.** White-noise rotation needs heavy filtering; the filter is a non-bilateral 3×3 box at half-res (≈6×6 full-res) with no depth/normal edge stopping, and shading upsamples 2× with a plain linear sampler → AO bleeds across silhouettes and reads as mush. | `ssao.wgsl:136-147`, `pbr_common.wgsl:96` | implementation |
| RC6 | **Class ceiling.** Even fully repaired, point-sample hemisphere SSAO (Crysis/LearnOpenGL 2007 lineage) is noisier and less accurate than horizon-based GTAO at equal cost; Intel's XeGTAO documents higher detail + more radiometrically correct output than HBAO+/ASSAO. | XeGTAO README | inherent to algorithm class |

Prior history confirms the causal chain: the multi-tap normal-reconstruction attempt traded RC1
acne for banding (multi-tap normals are quantized to depth texels — known failure mode), and the
bias raise (8e00aa3) traded acne for RC3 detail loss. Both were patches on the wrong layer.

## Fix options

Weights are independent per convention: **outcome** (end quality, as if free), **confidence**
(evidence quality + cheap probe), **cost** (difficulty/risk).

### Option A — Replace with GTAO: port Intel XeGTAO, using Bevy's WGSL port as reference (recommended)

Horizon-slice integration over a prefiltered depth mip chain; no per-sample binary depth compare,
so RC1–RC4 cease to exist structurally rather than being tuned away. Ships with a
purpose-built spatial denoiser (edge-aware, replaces RC5's box blur). Licensing clean:
XeGTAO is MIT (github.com/GameTechDev/XeGTAO); Bevy's WGSL port (PR #7402, `bevy_pbr` ssao) is
dual MIT/Apache-2.0.

- Pipeline: depth prefilter → 5-mip chain (compute) → GTAO main pass (compute, needs viewspace
  normals) → spatial denoise (compute) → same R8-ish AO texture consumed at `pbr_common.wgsl:96`
  unchanged.
- Normals: stage 1 uses XeGTAO's built-in edge-aware depth→normal generation (much better than
  `dpdx`: horizon-aware, edge-tested). Stage 2 (only if A/B shows curvature artifacts): add a
  normal target to the existing depth prepass — requires adding normal attributes (+skinned
  variants) and a fragment stage to `DepthPrepassPipelines` (`ssao.rs:96-125` are position-only
  today).
- Native-only concern is moot: the old WebGPU r16float storage-format limitation does not apply
  to vordar's native DX12/Vulkan wgpu.
- **Outcome: high.** Best-in-class screen-space AO; solves acne, halos, grazing angles, noise in
  one coherent design. Spatial-only denoise is the designed configuration (no TAA needed;
  matches our TAA-less renderer).
- **Confidence: high.** Battle-tested reference (Intel, shipped in Bevy 0.11+ production).
  Cheap probe: port at XeGTAO's default preset behind the existing `set_ssao` flag and A/B the
  two containment framings before touching tests/goldens.
- **Cost: high-medium.** 3 compute passes — the renderer's first compute pipelines (trivial in
  wgpu but new infrastructure), depth mip chain, hilbert-index noise, new bind groups. The
  entire hemisphere-kernel path (`ssao_frag`, `blur_frag`, KERNEL, SSAO_RADIUS/BIAS) is deleted,
  not kept beside it. Both ssao offscreen tests + goldens re-derived (expected; they encode the
  old estimator's behavior).

### Option B — Repair hemisphere SSAO in place

Keep the algorithm, fix every implementation defect: normal target in the prepass (true geometric
normals; kills RC1 and lets bias return to ~0.02), analytic receiver-plane comparison or
interpolated depth at the projected uv (RC2), radius ~0.6–1.0 m with a smooth distance-falloff
occlusion weight replacing the binary test + clamp (RC3/RC4), interleaved gradient noise
rotation, depth-aware bilateral blur + bilateral upsample (RC5).

- **Outcome: medium.** Removes acne/halos/mush, but RC6 remains: 16-point sampling stays flat
  and lacks the contact detail GTAO resolves; this is the ceiling the user is already
  dissatisfied under.
- **Confidence: medium-high.** Each individual fix is standard practitioner lore (true normals
  eliminating large-bias acne is repeatedly confirmed — mtnphil "Know your SSAO artifacts",
  gamedev.net threads). Cheap probe: prepass normals + bias 0.02 alone, A/B on
  `containment_near_door_minzoom`.
- **Cost: medium.** Prepass vertex layouts grow normals (incl. skinned), one new render target,
  shader rewrites of the estimator + blur; no compute infra.

### Option C — HBAO-class port instead of GTAO

Dominated by A: GTAO is the successor of HBAO's horizon idea (faster, higher detail, more
radiometrically correct per XeGTAO's published comparison vs HBAO+/ASSAO), needs the same inputs,
and the best open WGSL reference implements GTAO, not HBAO. No licensing advantage
(NVIDIA HBAO+ is closed). Listed only to record it was considered.

- **Outcome: medium-high. Confidence: medium** (no maintained WGSL reference → more original
  porting risk). **Cost: high-medium** (same infra as A without the reference code).

## Recommendation

**Option A**, staged: port XeGTAO (Bevy WGSL port as the working reference, MIT/Apache-2.0)
with depth-generated normals first; promote to a true normal prepass only if the A/B judge finds
curvature/normal artifacts. Delete the hemisphere path wholesale (swap rule). Option B is the
fallback only if the A probe surfaces a blocker (e.g. wgpu compute issue), which is unlikely.

## Verification contract

- A/B offscreen frames, old vs new, at the framings already used in
  `target/dirt-investigation/`: `containment_near_door_minzoom`,
  `containment_default_radius34_pitch08`, `zoom_left_wall`, `ibl_covered_lookup`, plus
  reproductions of the user's screenshot framings (`C:\Users\egm_8\Desktop\tmp\building
  closeup.png`, `building roof.png`, `other structure close up.png` — recover camera poses to
  match). Include raw-AO channel dumps alongside final frames.
- **Opus is the judge** (no-GUI rule): acne gone at grazing min-zoom, contact creases present
  and crisp (< 20 cm features visible again), no halos around props vs walls, no edge
  brightening, no silhouette bleed.
- `ssao_darkens_box_ground_contact_crease` / `ssao_darkens_final_image_crease_vs_open_ground`
  re-derived against the new AO; goldens regenerate once, then two suite runs per batch cadence.

## Sources

- [Intel XeGTAO (MIT)](https://github.com/GameTechDev/XeGTAO) and its
  [README comparison vs HBAO+/ASSAO](https://github.com/GameTechDev/XeGTAO/blob/master/README.md)
- [Bevy SSAO PR #7402 — WGSL XeGTAO port, MIT/Apache-2.0](https://github.com/bevyengine/bevy/pull/7402),
  [Bevy 0.11 notes](https://bevy.org/news/bevy-0-11/)
- [Know your SSAO artifacts — mtnphil](https://mtnphil.wordpress.com/2013/06/26/know-your-ssao-artifacts/)
- [gamedev.net: SSAO self-occlusion problems](https://gamedev.net/forums/topic/662470-ssao-self-occlusion-problems/)
- [LearnOpenGL SSAO (the current implementation's lineage)](https://learnopengl.com/Advanced-Lighting/SSAO)
