# Session resume — 2026-08-01

Standalone because the session ended mid-flight. Everything needed to resume is
here; nothing lives only in the conversation.

## Settled this session (do not re-litigate)

- **Decimation REFUTED as the campaign's stone-read cause.**
  `docs/reviews/town/decimation-attribution-2026-08-01.md` (uncommitted).
  In the 60–124 mm residual band decimation loses ≤0.4% of relief on every prop
  (chapel_arch 0.0038, broken_column 0.0000). Rank correlation vs decimation
  damage = **−0.80**. The blind test's winner, `rock_face_01`, is the *coarsest*
  mesh in the study (243 mm mean edge, 100% of its surface incapable of carrying
  62 mm relief). The hypothesis predicts the inverse of the observed ranking.
  Survives only as: chapel_arch's carving genuinely IS destroyed, at **4–17 mm**,
  and it alone merits retessellation (~171k tris, 12× current) as a legibility
  defect for a 5.5 m hero prop — NOT as the campaign's answer.

- **`content/models/assets.json` per-asset `tri_budget` has NEVER shipped.**
  All seven props sit at 14,997–15,000. `9e92cab` (07-29, added budgets) is not
  an ancestor of `4c46519` (07-28, generated props). Applying that file as-is
  would make **four of seven props coarser** than they ship today. The earlier
  "~110k → ~305k across six props" plan is DEAD — do not execute it.
  Also: those budgets targeted p99 deviation normalized by bbox diagonal, i.e.
  scale-*invariant*, so density falls as objects grow (chapel_arch 167 tri/m²
  vs olive_stump 2,832). Scaled by the wrong metric, not unscaled.

- **RUN-H chains UNBLOCKED.** They were held on the premise that props would ship
  with destroyed fine geometry. Dead for six of seven props. Held chains:
  H3 retablo (C3 seed 1), H4 shrine (C4 seed 203), H6 cart
  (`concept-c1/C5/seed_6`), H7 votive stand (C6 seed 4), brazier (C8 seed 407).
  ~3.1 h GPU. **Needs a go-ahead before running.**

- **Hunyuan3D-Omni: BLOCKED, permanently.** Its own `License.txt`, read
  independently rather than inherited, repeats the EU/UK/South Korea Territory
  exclusion verbatim. CREDITS row added (uncommitted). Beyond license: Omni's raw
  output is marching cubes at `octree_resolution=512` with no retopology — same
  triangle-soup regime, same decimator, no help. Bbox conditioning is 8 points
  through a shallow MLP into cross-attention: soft guidance, no hard constraint,
  no control-strength knob. The flat-back ruling in
  `tasks/town/p30-chapel-legibility.md` §6 is UNTOUCHED.

- **Hunyuan3D-2.1 + AirLLM: moot.** 2.1 carries the same exclusion (re-verified).
  AirLLM re-streams every layer per forward pass — a 30–50 step denoiser pays
  30–50 full sweeps per mesh — and its code is hard-wired to
  `AutoModelForCausalLM` with no DiT path. VRAM was never the binding constraint.

- **Orphaned grunt spawns removed.** Commit `32c4394`, verified on disk.
  `blood_moon` deleted whole (both its `spawns` and `waves` referenced only
  `grunt`, which lives in chapter01, which no shipped zone installs). Was
  emitting ~18 errors per 120 s per zone with zero players connected. The test
  `shipped_events_ron_parses_with_a_wave` was pinning the broken content green;
  renamed and re-asserted. Three flags recorded and NOT fixed — see the
  "Debt notes — orphaned grunt spawns cleanup" section in `tasks/todo.md`.

## In flight when the session ended (results lost — re-dispatch if wanted)

- **Albedo band table** → `docs/reviews/town/albedo-band-table-2026-08-01.md`.
  10 assets × an octave ladder 4–500 mm, albedo AND beauty separately,
  mm-denominated, controls measured identically, instrument self-validated, every
  free parameter swept. **This is the probe that replaces the refuted
  hypothesis** — the deficit is present in the albedo render, which contains no
  geometry at all, and blind test #2 moved 2.5 → 4 on albedo alone.
  `results.json` carries a macro band figure for only TWO assets, which is why
  60–124 mm cannot be regressed against anything.
  Includes a roughness column to **price, not assume**, this candidate: every
  generated prop ships flat scalar roughness with no `metallicRoughnessTexture`
  while all three controls ship spatially varying ARM maps. Against it:
  `rock_face_01`'s roughness std is only 7.97/255.

- **GPU perf probe** — still the right question, far lower stakes now (one prop,
  not seven). No GPU measurement of this renderer exists anywhere: the criterion
  benches are pure CPU, `render_cpu.rs` never creates a device, VQ-F1's 60 fps is
  checked by eye and never recorded. `gpu_timer.rs` already measures pass times
  and prints to F3; nothing writes them to a file. The hires 773,704-tri GLBs are
  on disk. Architecture argues the props are free: the start zone is 547,424 tris
  in ~3,540 draw calls (**41 tri/draw**), and the seven generated props are 1
  primitive each — raising their density adds ZERO draw calls. The renderer is
  submission-bound.

- **Simplifier research fleet (4 agents) — MOOT, discard.** Dispatched against
  the refuted set-wide premise. Salvage only what bears on a single-prop
  chapel_arch retessellation. Already extracted: meshoptimizer is MIT and won the
  only rigorous 2026 study at 57.6% preference; Blender's collapse is
  position-only QEM with the UV-seam guard commented out and a
  `USE_TOPOLOGY_FALLBACK` that activates exactly where this relief lives, and
  Blender's own devs are replacing it with meshoptimizer (PR #158508). Normal
  maps cannot fix a 14.5 cm silhouette. Virtual geometry is two orders below its
  crossover. Simplygon / InstaLOD / RapidPipeline / Exoside-Indie all
  licence-gated out.

## Uncommitted on disk

- Ground regions, 10 files (+263/−64) — mechanism validated (0.488 px RMS
  straight-line fit), material wrong. **Do not commit** until the cobble is
  chosen and the plaza apron is clipped.
- `content/source/CREDITS.md` — the Hunyuan3D-Omni row.
- Four `docs/reviews/town/*.md` reports.

## Next actions, in order

1. **Clip the plaza region in z.** It leaks 3.3 m past the z = ±9.2 facade line
   as an apron in open field. **This gates the cobble install, not the reverse:**
   the shipped cobble was value-matched to the earth (ΔV ≈ 0.01) so the apron read
   as a hue difference; every candidate lands ΔV 0.14–0.25 and turns it into a
   dark rectangle in open field.

2. **Choose the cobble** — deliverables in
   `target/town-materials-cc0/ground_cobble/`. Three CC0 candidates, all clearing
   §2 outright, blue cast gone in all three. The choice is between three
   compromises, none clean:
   - **cand_1** PavingStones150, 0.18 m — the only one inside the 10–25 cm band,
     correct dark earth joints, but **has moss**, which §3 forbids.
   - **cand_2** cobblestone_floor_09, 0.29 m — uniform dark earth-brown under a
     heavy dirt film, V 0.230 = darkest surface in Rocalba. Fails §3's "mixed
     cool greys pale to slate".
   - **cand_3** cobblestone_pavement, 0.40 m — best colour match (S 0.140,
     genuine pale-to-slate), but squared setts in regular courses read as
     machine-cut, and 0.40 m sits at the top of the gate's own ceiling.

   Whole-set risk none escapes: all render V 0.23–0.34 against cracked earth 0.48
   and dressed limestone 0.444. Warming the albedo to fix hue cost value — the
   street stops being the bluest thing in frame and becomes the darkest. A value
   lift may be needed. **Judge on re-renders after the apron clip, not on
   swatches.**

   The agent's instrument note is worth trusting: stone size was counted against a
   metric ruler drawn on the assembled tile
   (`review/ground_cobble_scale_ruler.png`) after discarding three scalar
   estimators — autocorrelation read the shipped cobble at 0.27 m when the gate
   measured 2.17 m, and two estimators misread joint polarity on real assets.
   Both paths validated against the gate's own numbers first.

3. **Re-render and re-judge the ground, then commit the ground work.**

4. **chapel_arch retessellation alone** (~171k tris), gated on the GPU probe.
   Re-decimate from the on-disk `raw.glb`, retexture that ONE prop, look at it.
   Note: xatlas unwraps AFTER decimation and the hires has no UVs, so any
   tri-count change invalidates atlas → normal/AO bake → albedo for that prop.

5. **Re-dispatch the albedo band table** if its result was lost.

## Still open, carried

- Build-wrong defects from the premise reconciliation: zero candle-gold emissive
  anywhere (§1 calls it the signature; §5's porter's brazier unplaced);
  m5 `plaster_smoked` re-source/re-grade; exterior rubble (blocked by
  content-lint rules); `wall_segment` coplanar-sliver striping (KIT DEBT → G4).
- `gen_material.py` fate — still needs the fact about shared code / env-var hooks
  with the Phase 3 prop-texture chain before a delete-vs-keep ruling.
- Whether a three-quarter concept costs anything downstream (`prop_hi3dgen.py`
  reconstructs in the image's camera frame while retexture calls view 0 "front").
- C4's spec fix U1 ("no cast-shadow floor" → "no floor geometry continuous with
  the object").
- **Stale item to strike in `tasks/todo.md`** (~line 384): the no-texture-dedup
  debt was fixed by `cac3c94` (07-31) — `TextureCache` now keys on a content
  hash; the townkit is 15 shared images ≈84 MB, down from ~4.8 GB per casa
  instance.

## Lesson added

`tasks/lessons/2026-08-01-gated-work-waits-for-its-gate.md`, indexed persistent.
Two artifacts: the 8 moot C1 re-rolls, and the simplifier fleet dispatched while
the study that refuted its premise was still running. The sharp half is that the
error reached the user — "~305k across six props" was presented and approved
before the gate returned, so the retraction had to travel back through an
approval that should never have been requested yet.
