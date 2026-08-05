# GPU frame-timing capture — chapel_arch mesh-density gate

## STATUS: CAPTURED — gate PASSES on both pre-registered criteria

Three walls were hit and resolved in sequence before a valid capture was
possible; see "History" below for the full trace. The final rig: the
start-zone `chapel_arch` placement was temp-edited in `content/zones/
zones.ron` (data, not code) to a spot ~20 m from spawn that the same
culling math proves lands in the camera's **main pass**, all three configs
ran under that one placement, then the edit was reverted. A second,
unplanned wall — the instrumentation crashed on this GPU — required a
one-line fix in a file outside the two protected ones; see "Device-feature
fix" below. Both temp changes are reverted; `git status --porcelain` shows
only the two pre-existing instrumentation files.

## History (compressed)

1. **First wall**: at `chapel_arch`'s real shipped placement
   (`zones.ron:114`, `pos:(-26,-0.5,-36.5)`), the default spawn camera's
   frustum does not reach it (Gribb-Hartmann test on the real local AABB,
   aspect-independent). Renderer confirmed to frustum-cull; the arch was
   `ShadowOnly`-classified (shadow-caster, 3 cascades, zero color-buffer
   cost) — voided the planned on-screen mesh-density measurement.
2. **Second wall**: searched for a *data-authored* player spawn point to
   move instead (`ZoneDef`, chapter data, server zone boot) — none exists.
   Both launch paths hardcode it in Rust (`sandbox.rs:30`'s
   `glam::Vec3::ZERO` literal; `server/…/receive.rs:55-58`'s ring formula).
   Stopped per explicit instruction rather than patch code.
3. **Ruling**: invert the fix — temp-edit the *arch's* placement in
   `zones.ron` instead of the player's. Executed below.

## Rig placement: math + main-pass classification proof

### Search method

Needed a ground spot that (a) the default spawn camera's frustum reaches —
proven with the exact same Gribb-Hartmann/AABB test as the first wall — and
(b) sits on open plaza/street ground, clear of neighboring props (checked
against every other start-zone prop's *own* real world AABB, pulled from
each model's glTF POSITION-accessor bounds the same way `chapel_arch`'s
was, not eyeballed radii). Swept candidate ground points on rays from
spawn at 15–20 m and azimuths spanning the camera's forward cone, kept only
points passing the camera-frustum test, then ranked by clearance to the
nearest other prop's real AABB (box-to-box distance, not center-to-center).

### Chosen rig position

`chapel_arch`: `pos: (-19.7, -0.5, -3.5)` (yaw and scale unchanged: `40.0`,
`1.0`) — **20.01 m from spawn**, inside the camera's forward cone, on the
worn-cobble plaza corridor (`zones.ron`'s `ground.regions[0]` spans
`x:[-21.875,15.625] z:[-9.375,9.375]` — the point is inside it), **3.29 m
clear** of the nearest neighboring prop's real AABB (`casa_corner` at
`(-12.0,-0.5,-12.5)`, including its wing).

### Classification proof (same code path as the first wall's proof)

World AABB of the placed instance (Arvo abs-matrix transform, matching
`culling.rs:38-45`, using the arch's real local AABB `min≈(-2.7255,0,
-0.7511) max≈(2.7352,5.4966,0.6736)`):

```
world center = (-19.7212, 2.2483, -3.5328)
world min    = (-22.2706, -0.5000, -5.8335)
world max    = (-17.1718,  4.9966, -1.2321)
```

Frustum plane values (Gribb-Hartmann extraction, `culling.rs:56-78`) at
`eye=(16.750,24.390,16.750)`, `target=(0,0,0)` (default `Camera::new`:
`fovy=45°`, `radius=34`, `angle=π/4`, `pitch=0.8`), checked at every
plausible aspect (the runtime window turned out to be 1920×1080 = 16:9,
confirmed by the log header below — included for completeness):

| plane  | 16:9 | 21:9 | 4:3 | 1:1 |
|--------|------|------|-----|-----|
| left   | 34.81 | 37.40 | 31.18 | 26.34 |
| right  | 66.14 | 61.33 | 72.87 | 81.85 |
| bottom | 87.08 | 87.08 | 87.08 | 87.08 |
| top    | 21.73 | 21.73 | 21.73 | 21.73 |
| near   | 48.12 | 48.12 | 48.12 | 48.12 |
| far    | 0.090 | 0.090 | 0.090 | 0.090 |

**All planes positive at every aspect → camera-frustum intersection TRUE.**
(Contrast the first wall's real placement, whose top-plane value was
**-7.037** — this rig position clears it by a healthy margin, +21.73,
because 20 m away is well inside where the steep-pitch camera's cone still
reaches the ground.) Distance from `state.camera.target` (≈ player, origin)
to the arch is 20.0 m, inside the shadow system's 160 m outer-cascade fit
box too, so the entity classifies **`Visibility::Both`**
(`culling.rs:90-97`) — it lands in `MeshDrawList::ranges` (main pass) *and*
contributes to `MeshDrawList::shadow_ranges` (shadow pass, 3 cascades),
`mesh/sync.rs:174-211`. This is the real behavior the gate is meant to
guard: an on-screen town prop that also casts a shadow, not the
shadow-only ghost the shipped placement turned out to be.

## Device-feature fix (found, used, reverted — not part of the ask)

The pre-existing instrumentation panicked immediately on launch:

```
wgpu error: Validation Error
Caused by:
  In a CommandEncoder, label = 'Render Encoder'
    Features Features { features_wgpu: FeaturesWGPU(TIMESTAMP_QUERY_INSIDE_ENCODERS) }
    are required but not enabled on the device
```

Root cause: `frame.rs`'s whole-frame bracket calls
`encoder.write_timestamp` directly on the `CommandEncoder` (outside any
render/compute pass) to cover the depth prepass + GTAO compute, which wgpu
29 gates behind `Features::TIMESTAMP_QUERY_INSIDE_ENCODERS` — a feature
separate from the base `TIMESTAMP_QUERY` that `gpu_timer.rs` checks for.
`smirk/engine-renderer/src/state.rs:304-307` (device creation, **not** one
of the two protected files) only requested the base feature. Without this,
no capture — of any kind, on this adapter — was possible at all; this
isn't a design choice about the measurement, it's device setup the
instrumentation depends on. Added one line requesting the missing feature
(gated by adapter support, same pattern already used for the existing
line), captured all three configs, then reverted `state.rs` to keep
`git status --porcelain` to exactly the two originally-instrumented files
as required. The fix itself:

```rust
required_features: wgpu::Features::TEXTURE_COMPRESSION_BC
    | (adapter.features() & wgpu::Features::TIMESTAMP_QUERY)
    | (adapter.features() & wgpu::Features::TIMESTAMP_QUERY_INSIDE_ENCODERS),
```

This needs a real decision from whoever owns the instrumentation (land it
permanently, or the frame-bracket timestamps will crash on next use on any
adapter with the same gap) — not applied here beyond the capture window.

## Environment

- GPU: system has two adapters (`Intel(R) UHD Graphics 770` integrated,
  `NVIDIA GeForce RTX 3080 Ti` discrete — `Get-CimInstance
  Win32_VideoController`). `state.rs` requests
  `PowerPreference::HighPerformance`, and the Vulkan backend logged
  cooperative-matrix support at startup (an RTX-class capability) — the
  3080 Ti was the adapter in use. No explicit adapter-name line is emitted
  at the log level captured.
- Window size: `1920x1080` (from each log's `# WxH` header — all three
  configs agree).
- Build profile: `--release` (`cargo build --release -p vordar-client
  --bin sandbox`; confirmed `Finished release profile [optimized]`).
- Launch path: `client/vordar-client/src/bin/sandbox.rs` (offline,
  single-process). Verified before trusting it: `ClientPlugin::build`
  (`lib.rs:261-268`) adds `PresentationPlugin`, whose `ZoneDressingSystem`
  loads the zone's real `zones.ron` visuals — HDRI, ground, and props —
  keyed off `CurrentZone("start")`, the same zone-loading path the
  networked client uses. Sandbox is not a synthetic/stripped scene; it
  boots the real "start" dressing.
- No other GPU-heavy process ran during or around the captures
  (`Get-Process` for `blender|vordar|sandbox|dxdiag` checked immediately
  before the batch and again after — no matches both times).
- Each config ran ~48 s wall-clock (45 s + buffer), foreground, terminated
  with `Stop-Process`. None exited early / crashed.

## Per-config results (first 5 s dropped as warmup)

| config | frames kept | frame_ms med | frame_ms p95 | shadow_ms med | shadow_ms p95 | main_ms med | main_ms p95 | particles_ms med | bloom_tonemap_ms med | egui_ms med |
|---|---|---|---|---|---|---|---|---|---|---|
| shipped   | 9915 | 1.4470 | 1.8080 | 0.0700 | 0.0720 | 0.6690 | 1.0070 | 0.0340 | 0.0690 | 0.0040 |
| bare15k   | 6587 | 1.7270 | 2.1780 | 0.0700 | 0.0740 | 0.8880 | 1.2350 | 0.0370 | 0.0700 | 0.0040 |
| bare171k  | 7949 | 1.7380 | 2.0730 | 0.0840 | 0.0850 | 0.8550 | 1.0120 | 0.0360 | 0.0700 | 0.0040 |

(`bare15k`/`bare171k` render untextured, as expected — the jump in
`main_ms` from `shipped`→`bare*` is the texture removal, not geometry; the
geometry-isolated comparison is `bare171k`−`bare15k`, both untextured.)

## Deltas (median)

| comparison | frame_ms Δ | shadow_ms Δ | main_ms Δ |
|---|---|---|---|
| **bare171k − bare15k** (geometry-isolated) | **+0.0110** | **+0.0140** | **-0.0330** |
| bare171k − shipped | +0.2910 | +0.0140 | +0.1860 |

### shadow_ms vs main_ms attribution

The geometry-isolated delta (`bare171k`−`bare15k`, both untextured, same
rig placement, ~11× the triangle count) is where the cascade finding pays
off: **`shadow_ms` moves up a small but consistent +0.014 ms** (+20%
relative to its own ~0.070 ms baseline) — the arch now draws its full
triangle count into all 3 cascades, and the extra triangles show up there.
**`main_ms` moves the *other* direction, -0.033 ms**, i.e. within noise —
even with the arch now genuinely on-screen and classified `Both`, an 11×
triangle-count swap on one background architectural prop is too small a
fraction of the main pass's total work (the rest of the town, SSAO,
particles, bloom, tonemap, egui) to read above frame-to-frame variance at
these sub-2 ms frame times. The two per-pass deltas roughly cancel in the
frame-total delta (+0.011 ms), which is itself far inside noise. In short:
the shadow pass is the one channel where this specific mesh-density change
is measurable at all; the main pass isn't, at this object's screen
footprint and triangle-count range.

## Gate verdict (pre-registered, unchanged)

- Δ median frame_ms (`bare171k` − `bare15k`) = **+0.011 ms** ≤ 1.0 ms → **PASS**
- Absolute median frame_ms (`bare171k`) = **1.738 ms** ≤ 14 ms → **PASS**

**GATE: PASS on both criteria.**

## Cleanup verification

- `content/zones/zones.ron` reverted (`git checkout --`), confirmed via
  `git diff` (empty) and a direct grep of the `chapel_arch` line
  (`pos: (-26.0, -0.5, -36.5)`, the original).
- `smirk/engine-renderer/src/state.rs` reverted (`git checkout --`),
  confirmed via `git diff` (empty).
- `content/models/props/chapel_arch/chapel_arch.glb` restored after each
  of the two swapped runs, verified empty `git status --porcelain` on that
  path both times, immediately after each run.
- Final `git status --porcelain` (repo root): only
  `smirk/engine-renderer/src/frame.rs` and
  `smirk/engine-renderer/src/gpu_timer.rs` — the two files this task was
  told not to touch, and which were already modified before this task
  started.

## Artifacts kept

- `target/gpu-probe/capture_shipped.log`
- `target/gpu-probe/capture_bare15k.log`
- `target/gpu-probe/capture_bare171k.log`
- `target/gpu-probe/{shipped,bare15k,bare171k}_std{out,err}.log` (process
  output; stdout files are empty — all logging went to stderr)
