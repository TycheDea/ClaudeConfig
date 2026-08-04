# chapel_arch fix (subplan)

> **STATUS 2026-07-25 — F0/F1/F2 done, F3 FAILED at a design wall, session
> ended by user.** Execution log lives in `tasks/todo.md`. The short version:
> the plan's remedy for cause (1) is exhausted — MaterialAnything's bump head is
> blank (std 4–6/255), and the albedo high-pass fallback moved `normal_lap_std`
> 0.188 → 0.382 without moving a single visible pixel. Underneath both sits a
> ceiling this plan never priced: **2048² over 136.68 m² at 42.3% utilization is
> 8.9 mm/texel, and limestone grain is 1–3 mm**, so no atlas-space method can
> carry it at any amplitude. F4/F5/F6 remain valid as seam and facet work but
> are **not** a path to the AA bar on their own. The user has since ruled that
> quality outranks cost and that replacing tools or technologies is in scope —
> so the next plan is a stack question, not a parameter question.

Source: fix phase of the prop-quality campaign, planned 2026-07-24 against the
Phase 0 instrument (`asset_inspect`, `prop_audit.py`) and the on-disk baseline
`target/fix-phase/before/`. Subject is **chapel_arch only** (user directive:
one model, iterate until no human eye calls it AI slop). No other prop is
touched; `content/zones/zones.ron` is not touched.

**Every number below was re-derived from the shipped asset, not carried over.**
Two Phase-0 claims are corrected here and one is overturned — see Findings.

**GPU: ~1 min nominal, ≤17 min ceiling.** Every generation run is named in the
budget table. Everything else is CPU and §8-exempt. This is the plan's central
result: the visible gap is not a generation problem, it is an *authoring* gap
— the pipeline never authored surface micro-relief, never authored AO, and
authored roughness from a lit render. Regeneration is explicitly rejected with
evidence (Finding 5).

---

## Findings (measured, this session)

Measurements are **island-masked** (TEXCOORD_0 triangles rasterized into the
2048² atlas) unless stated. Island covers **42.3%** of the atlas; unmasked
statistics conflate surface with empty atlas and are why the Phase-0 numbers
misled.

**F-1 — the high-to-low normal bake is NOT a no-op. It is nearly
information-free.** Overturns the leading hypothesis.
- In-island mean normal tilt is **16.8°** (p50 12.5°, p90 38.7°). A no-op bake
  is 0° everywhere. The bake fired and wrote real data.
- Ray budget is adequate: with `cage_extrusion=0.01` / `max_ray_distance=0.03`,
  **97.0%** of the clean surface falls inside the ray window. Signed
  clean→hires deviation along the normal is p05 −8.7 mm / p50 0.0 mm /
  p95 +8.3 mm on a 5.5 m prop. Ray distance is not the bug.
- The bake has almost nothing to carry: `clean_hires.glb` has **773,704 tris,
  mean edge 18.9 mm, surface area 137.66 m²** against the decimated mesh's
  **136.68 m²** — the 773k-face cage adds **+0.7% area**. A surface with real
  stone relief (amplitude ≈ λ/10) would add ~5%. Hi3DGen produced a smooth
  surface finely tessellated, not a detailed one.
- The 25.4% in-island dead-flat texels are therefore *correct output*: where
  the hires equals the clean, the tangent-space normal is exactly (128,128,255).
- The manifest's `normal_bake_s: 1.1` is consistent with a real bake over a
  3 cm ray window; it is not evidence of failure.

**F-2 — `prop_audit.py`'s normal/albedo/roughness stats cannot detect the
failure they were read as detecting.** They run over the whole atlas.
chapel_arch: whole-atlas `normal_flat_frac` 0.264 vs in-island **0.254** vs
off-island 0.271 (bake margin dilation carries island values outward). The
reference `rock_face_01` has a near-fully-utilized atlas, so the 1.2% vs 26.3%
comparison was never like-for-like. See `tasks/lessons/2026-07-21-metric-must-detect-failure.md`.

**F-3 — MaterialAnything already predicts a bump map and the pipeline throws it
away.** `prop_pbr.py:83`:
```python
albedo, rm, _bump = pipe(...)
# bump discarded: the texture stage bakes a real high-to-low normal map
```
The estimator is a triple-head UNet: albedo, roughness/metallic, **bump**. The
bump head is the only stage in the whole chain that produces sub-centimetre
surface relief, it is already paid for on every run, and its justification for
being discarded is exactly the claim F-1 refutes. This is the missing
micro-detail source, and it is *image-derived*, so it is correlated with the
albedo the way real stone is.

**F-4 — the shipped material, re-read from the glb.** Node has no scale; mesh
is 5.461 × 5.497 × 1.425 m, 14,999 tris / 13,982 verts, mean tri edge 13.5 cm.
Attributes `POSITION, NORMAL, TEXCOORD_0` — no TANGENT, so
`gltf_import.rs:189` generates tangents from UVs (Lengyel + Gram-Schmidt,
`smirk/engine-renderer/src/tangent.rs`). That is a different basis from
Blender's mikktspace bake basis; on a smooth-shaded chart atlas the divergence
is small and second-order to everything else here — **not** a ranked cause,
recorded so nobody re-derives it.
In-island: roughness mean **0.572** std 0.102 p1 0.455; albedo luma p1 **0.395**
p50 0.596 p99 **0.989**; no `roughnessFactor`/`metallicFactor` (both default
1.0, so 0.572 ships uncorrected); no `occlusionTexture`.

**F-5 — regeneration is the wrong lever, and this is measurable.** The hires
cage adds +0.7% area and deviates ±8 mm from the 15k decimation (F-1). Raising
`slat_sampler` 6→12 changes shape convergence, not the resolution of the
flexicube surface SLat decodes to — it cannot manufacture millimetre grain. A
re-candidate also discards a silhouette the user already accepted at B3.4. GPU
spent on regeneration buys nothing that F1–F3 below do not buy for free.

**F-6 — coverage is a placement problem the existing predictor already priced.**
`blend_coverage 0.5504`, `hole_texels 1,202,912`. The greedy next-best-view
search over 36 azimuths × 4 elevations found exactly **one** candidate clearing
`MV_EXTRA_MIN_GAIN = 0.03` (front-from-below, +5.29%). The residue is therefore
*scattered*, not one big unseen soffit — no single extra view buys ≥3%. Buying
it means lowering the gain floor and paying for more canvases, i.e. GPU, for a
diminishing return. Ranked last, staged last, conditional.

**F-7 — atlas utilization is 0.409** (UV triangle area / atlas). xatlas packs at
`UV_ATLAS_RESOLUTION = 1024` while the bake ran at 2048. Repacking could
plausibly reach ~0.5, i.e. 112 → ~124 px/m. Modest, and D2 already established
density is not what makes the control read correctly. Optional inside F4, not a
stage of its own.

**F-8 — baseline defect.** `target/fix-phase/before/*/macro_01.png` frames empty
ground; the subject is out of frame at angle 01, macro distance. The judge must
not score angle 01 at macro on either side of the before/after.

---

## Ranked causes of the visible gap

| # | Cause | Share | Evidence |
|---|---|---|---|
| 1 | **No surface micro-relief exists anywhere in the asset.** No stage authors sub-centimetre relief; the one stage that predicts it (MaterialAnything's bump head) discards it. | ~45% | F-1 (+0.7% cage area, ±8 mm deviation), F-3, `studio_normal/macro_00.png` broad pastel gradients vs `ref_macro_00.png` dense perturbation |
| 2 | **Roughness 0.572 on limestone** — a semigloss, shipped with no corrective factor. Reads as wet clay / unfired ceramic. | ~25% | F-4 (in-island 0.572/0.102, p1 0.455); S7-F1 candelabra at declared 0.8 reads correct; control 0.882; `studio_beauty/gameplay_02.png` translucent sheen |
| 3 | **No crevice darkness at any layer.** Albedo p1 0.395 (darkest 1% is mid-grey) on a "soot-darkened carvings" prompt, AND no `occlusionTexture` while `mesh_shader.wgsl:91` samples one and `store.rs:125` binds 1×1 white. | ~20% | F-4; D3; control albedo p1 0.053 |
| 4 | **Naked facets.** 15k tris, mean edge 13.5 cm on a 5.5 m arch, smooth-shaded, with no normal detail to break up the interpolation. Partly a *consequence* of #1. | ~10% | `raking_beauty/macro_00.png`; `studio_normal/macro_00.png` hard straight boundaries between smooth sweeps |
| 5 | **Inpaint smear + chart seams.** 45% of island texels are Telea filler; chart-boundary discontinuities read as hard lines. | *labelled a guess for share* | F-6; visible vertical seam and rectangular patch edges in `studio_beauty/gameplay_02.png` |

Shares 1–4 are apportioned by judgement over the measurements, not measured
directly — treat the ordering as evidence-backed and the percentages as
estimates. Cause 5's share cannot be separated from cause 3 until 1–3 are
fixed; that is exactly why it is staged last.

**Texture-only or mesh?** Texture-and-material, with one conditional mesh item.
The mesh's *shape* is accepted (F-5). Its *density* is a real but secondary
contributor (cause 4) and gets a conditional stage after the material work, so
we learn whether relief alone hides the facets before spending a re-unwrap.

---

## GPU budget (CLAUDE.md §8 — approving this plan is the go-ahead for exactly these runs)

| ID | Run | Expected wall-time | Anchor |
|---|---|---|---|
| G1 | F3: `prop_pbr.py` re-run over the 5 existing views to emit `bump.png` | **~1 min** | manifest `pbr_estimator.elapsed_s = 44.6` for these exact 5 views @ 50 steps |
| G2 | F5 (conditional): 2 extra multiview canvases (2 Z-Image passes @1536×3072) + estimator on 4 new views | **~4 min, ceiling 6 min** | b3.md fact 11(b): full multiview retexture ~1.5–2.5 min for 3 canvases + 5 estimator views |
| G3 | F7 (contingency, only on a judge stop after F1–F5): one full re-candidate, Hi3DGen `slat_sampler` 12 + multiview | **ceiling 10 min** | b3.md fact 11(a)+(b) ~6 min/candidate, +50% for doubled slat steps |

**Nominal ~1 min. Ceiling ≤17 min.** Everything else is CPU: every ComfyUI
canvas, every `gen.png`/`albedo.png` and every depth/normal render already
exists under `target/prop-batch/b3/arch/cand_0/multiview/`, and both
`generate_views` and `estimate_materials` resume from disk — so a full
`prop_texture.py` re-run costs **0 GPU**. Per-stage CPU: F0 ~10 min, F1 ~12 min,
F2 ~8 min, F3 ~12 min, F4 ~18 min, F6 ~15 min + one workspace nextest.

---

## Judge loop (executed by the orchestrator between every stage)

```
cargo run -p vordar-client --release --features offscreen --bin asset_inspect -- \
  content/models/props/chapel_arch/chapel_arch.glb \
  --out target/fix-phase/<stage> --size 1024x1024 \
  --lighting studio,raking --channel beauty,normal,rough,albedo \
  --angles 4 --distance gameplay,macro --reference
python scripts/ai-pipeline/prop_audit.py --asset chapel_arch
```
Per-frame PNGs are the evidence; sheets are only an index. Compare each frame
against the same filename under `target/fix-phase/before/`. **Skip
`*/macro_01.png` on both sides (F-8).**

---

## Tasks

- [ ] **F0 — island-mask the audit, correct the record** `[sonnet]` **(CPU ~10 min, 0 GPU)**
  - `prop_audit.py`: rasterize the glb's TEXCOORD_0 triangles into an
    atlas-resolution mask once per prop; compute `normal_flat_frac`,
    `normal_lap_std`, `albedo_luma_*`, `albedo_blown_frac` and the ARM stats
    over island texels only. Report a new `island_frac` column.
    **Swap rule: the unmasked variants are deleted, not kept alongside.**
  - Same file, two unifications that the deletions in F1/F2 force:
    when no `metallic_roughness` slot exists, `roughness_mean`/`metallic_mean`
    take the glTF `roughnessFactor`/`metallicFactor` and `roughness_std` is 0
    (this also makes candelabra's old scalar path comparable for the first
    time); `ao_mean` reads the **occlusion slot** — the ARM-red reading is
    deleted, it was never a rendered channel (D3).
  - **No threshold, no gate, no non-zero exit.** That constraint is unchanged.
  - Rewrite `tasks/todo.md`'s "Fix phase — hypotheses" block with F-1…F-8;
    delete the overturned "26.3% dead-flat normals" and "bake is a no-op" text.
  - **Verify:** `python scripts/ai-pipeline/prop_audit.py --asset chapel_arch`
    prints `island_frac 0.423±0.005`, in-island `normal_flat_frac 0.254±0.005`,
    `normal_lap_std 0.183±0.005`, `albedo_luma_p1 0.395±0.005`,
    `roughness_mean 0.572±0.002`, `ao_bound false`. All ten props still print;
    runtime under 90 s. `git diff` touches only `prop_audit.py` and `todo.md`.

- [ ] **F1 — roughness: delete the estimated MR path** `[sonnet]` **(CPU ~12 min, 0 GPU)**
  Cause 2. Cheapest and most certain, so it goes first — and it changes how
  causes 1 and 3 are judged.
  - `prop_texture.py`: the multiview path stops producing a
    metallicRoughness texture. Roughness/metallic ride the glTF scalar factors
    on **both** strategies (the `mr_stats` branch collapses to one path).
    Ship `--roughness 0.85 --metallic 0.0` for this prop.
  - **Deletes** (swap rule, code + tests + docs): the `rm.png` `blend_views`
    call; `mr_img`/`prop_mr` construction and every branch on it; the
    `ShaderNodeSeparateColor` MR wiring and its `metallicFactor/roughnessFactor
    = 1.0` comment; `--dielectric` and the `dielectric` parameter through
    `pbr_multiview`; the `metal_fraction` stat; the "MR, multiview strategy:
    per-texel …" header paragraph. In `prop_pbr.py`: the `rm.png` save, its
    resume-set entry, `rm_sha256` in `pbr_meta`, and the header line describing
    it. In `gen_prop.py`: `--dielectric` and its pass-through. In
    `scripts/ai-pipeline/README.md`: every `--dielectric` / per-texel-MR /
    `metal_fraction` mention. `tasks/ai-pipeline/research/a6-1-mr-contract.md`
    is a research record and stays (history), but no live doc may still assert
    the per-texel MR contract.
  - Re-run the texture stage on the existing work dir; reinstall to
    `content/models/props/chapel_arch/`.
  - **Verify (machine):** shipped glb material has `roughnessFactor 0.85`,
    `metallicFactor 0.0`, **no** `metallicRoughnessTexture`;
    `chapel_arch.textures/` no longer contains the mr image; `prop_audit`
    `roughness_mean 0.850 / roughness_std 0.000`; `placed_px_per_m` still 112.0.
  - **Verify (eye):** `studio_rough/gameplay_00..03` read a uniform bright grey
    (≈217) where before they read ≈141. `studio_beauty/gameplay_02.png` loses
    the translucent waxy sheen down the column face.
  - **Judge gate:** if the surface still reads plasticky at uniform 0.85, the
    problem is not the level and F3 is where it lives — say so and continue,
    do not retune the scalar.

- [ ] **F2 — author AO and bind it** `[sonnet]` **(CPU ~8 min, 0 GPU)**
  Cause 3, the half of it that belongs at render time rather than in the albedo.
  - `prop_texture.py`: Cycles AO bake from the hires cage onto the clean mesh's
    atlas (same selected-to-active rig as the normal bake, samples raised so it
    is not 1-sample noise), written as the glTF `occlusionTexture`. The shader
    already samples it (`mesh_shader.wgsl:91`) and the importer already reads it
    (`gltf_import.rs:329`) — nothing renderer-side changes.
  - Confirm `preprocess_prop.mjs` and `bake_textures.mjs` carry a 4th image
    (both are slot-generic; verify, do not assume). Size budget: the enforced
    lint is `MAX_MODEL_BYTES = 16 MB` (`content_lint.rs:17`, VQ-B2) plus the
    1 GB total texture budget (VQ-C5) — **not** the 8 MB figure an earlier draft
    of this plan cited, which is only `preprocess_prop.mjs --max-bytes`'s default
    and has no referent in the project's rules. 8 MB is also unreachable
    alongside the 2048 atlas this same gate requires for 112 px/m. Pass
    `--max-dim 2048 --max-bytes 16777216`; the mr texture deleted in F1 pays for
    the AO texture, so the total should fall from F1's 10.14 MB.
  - **Verify (machine):** `prop_audit` `ao_bound true`, `ao_mean` in 0.70–0.90;
    `.textures/manifest.json` lists an `occlusion` slot; final glb < 16 MB.
  - **Verify (eye):** in `studio_beauty/macro_00.png` the recessed carvings and
    the inner corners darken; the flat cream fill that reads as unfired ceramic
    gains depth. `studio_beauty/gameplay_02.png` gains form-shadow at the drum
    joints.

- [ ] **F3 — micro-relief from the estimator's bump head** `[fable]` **(GPU ~1 min = G1; CPU ~12 min)**
  Cause 1, the largest share. Highest design risk, so it runs after the two
  certain stages.
  - `prop_pbr.py`: stop discarding `_bump`; save `view_<i>/bump.png` at the gen
    resolution, add it to the resume set and to `pbr_meta`. Delete the stale
    `# bump discarded: …` comment (§5: it asserts something the pipeline no
    longer does, and its premise is refuted by F-1).
  - **G1:** re-run `prop_pbr.py` over the 5 existing views to emit bump.
    **~1 min GPU.** No other stage re-touches the GPU.
  - `prop_texture.py`: blend `bump.png` into the atlas through the *existing*
    `blend_views` machinery (Non-Color, same facing weights, same occlusion
    test — reuse, do not write a second blender), giving a height field over
    the island. Convert to tangent-space normal by Sobel in atlas UV, with the
    gradient scaled through the per-texel UV→world ratio so the grain has a
    **physical size** independent of atlas resolution and prop scale. Composite
    over the geometric high-to-low bake (UDN/whiteout — the geometric map keeps
    its low frequencies, the bump adds highs). One new amplitude constant, named
    and commented with the world-space scale it encodes.
  - **Pre-authorized alternative** (take it without stopping if the bump comes
    back as mush — under-amplitude or blobby at 768²): derive the detail normal
    from a high-pass of the **blended albedo atlas** instead. Same compositing
    code, different height source; the estimator's bump save still lands and
    still gets recorded. Say in the task report which source shipped and why.
  - **Verify (machine):** in-island `normal_flat_frac` ≤ 0.05 (from 0.254);
    in-island `normal_lap_std` ≥ 0.25 (from 0.183; control 0.270). If lap_std
    lands between 0.20 and 0.25, that is a judge call on the frames, not a
    retune loop.
  - **Verify (eye), the deciding frames:**
    - `studio_normal/macro_00.png` — high-frequency perturbation covering the
      *faces*, not only the facet boundaries; comparable in **density** (not
      necessarily amplitude) to `studio_normal/ref_macro_00.png`.
    - `raking_beauty/macro_00.png` — the key light picks out grain across the
      faces. Before, the only thing raking light finds is facet edges.
    - `studio_beauty/macro_00.png` — mineral texture where before there are
      smooth cream sweeps and blurry stains.
  - **Judge gate:** if the relief reads as sprayed-on uniform noise rather than
    stone, stop and surface — that is Q1 territory, not a constant to tune.

- [ ] **F4 — mesh density (CONDITIONAL on the F3 judge)** `[sonnet]` **(CPU ~18 min, 0 GPU; ≤2 min GPU only if the extra-view pick moves)**
  Runs **only** if facets still read as the dominant edge at
  `raking_beauty/macro_00` after F3. Cause 4.
  - `prop_cleanup.py --tri-budget 45000` for this prop (the 15000 default is
    untouched for everything else — it is a per-run argument, not a constant).
    Optionally repack the atlas at `UV_ATLAS_RESOLUTION 2048` / padding 8
    (F-7: 112 → ~124 px/m, modest; take it only because the re-unwrap is
    already being paid for).
  - **Cost trap to handle before spending anything:** a new clean mesh changes
    the depth renders, and `pick_extra_views` is deterministic *given the
    geometry* — a re-decimated mesh can pick a **different** extra view, which
    would demand a new ComfyUI canvas. Pin the extra views to the five recorded
    in the manifest for this re-run so the stage stays CPU-only. If the worker
    cannot pin them cleanly, that is ≤2 min GPU inside the G2 ceiling — say so
    in the report.
  - **Verify:** `prop_audit` shows tris ≈45k and `atlas_px_per_m` ≥ 112.0;
    `raking_beauty/macro_00` and `gameplay_00..03` show no straight facet
    boundary reading as a crease; silhouette against the before frames is
    unchanged in shape (this is a density change, not a shape change).

- [ ] **F5 — view coverage (CONDITIONAL on the F3/F4 judge)** `[fable]` **(GPU ~4 min, ceiling 6 min = G2; CPU ~12 min)**
  Runs **only** if the judge still names inpaint smears or chart seams as a
  slop tell after F1–F4. Cause 5. Last because it is the only stage whose
  return F-6 shows to be diminishing.
  - Lower `MV_EXTRA_MIN_GAIN` 0.03 → 0.01 and raise `MV_EXTRA_MAX` 2 → 4;
    add a soffit-directed candidate set (elevations that see *through* the
    archway opening, which the current ±15/−35/+55/+75 grid under-samples for
    an object with a large interior span).
  - **G2:** up to 2 new canvases + estimator on the new views. **~4 min GPU,
    ceiling 6 min.**
  - **Verify (machine):** `blend_coverage` ≥ 0.70 (from 0.5504); `hole_texels`
    below 700k (from 1,202,912).
  - **Verify (eye):** `studio_beauty/gameplay_02.png` — the vertical chart seam
    and the rectangular patch discontinuities no longer read as hard lines at
    gameplay distance; the interior soffit of the arch carries the same stone
    material as the outer faces rather than a smear.

- [ ] **F6 — install, gate, record** `[sonnet]` **(CPU ~15 min + one workspace nextest)**
  - Install the winning build to `content/models/props/chapel_arch/` (glb +
    `.textures` + regenerated `generation_manifest.json`). `zones.ron` untouched.
  - Full judge sweep into `target/fix-phase/after/` at the F6 framings; keep the
    artifacts (`tasks/lessons/2026-07-21-keep-verification-artifacts.md`).
  - `tasks/todo.md` struck + review section; a `tasks/lessons/` note for any
    correction taken during the phase, indexed in `lessons.md`.
  - **Verify:** `cargo test -p vordar-game --test content_lint` green; **ONE**
    `cargo nextest run --workspace` (§7); `git diff HEAD --name-only` touches
    only the prop directory, the four pipeline scripts, the README, and the
    tasks files.

- [ ] **F7 — full re-candidate. NOT PROPOSED.** Reserved contingency only, and
  only if F1–F5 all land and the judge still calls it slop. In that case the
  residual failure is the **silhouette**, not the material, and that is a
  different plan — stop and surface rather than spending G3. Budget line exists
  so the ceiling is honest, not because the plan expects to use it.

---

## Gate

CLOSED when every non-conditional box is struck and:

**Machine** (all from `prop_audit.py --asset chapel_arch`, island-masked):
- `normal_flat_frac` ≤ 0.05 · was 0.254
- `normal_lap_std` ≥ 0.25 · was 0.183 · control 0.270
- `roughness_mean` 0.850 / `roughness_std` 0.000 · was 0.572 / 0.102
- `ao_bound` true, `ao_mean` 0.70–0.90 · was false
- `placed_px_per_m` ≥ 112.0 (no accidental density regression)
- final glb < 16 MB (`MAX_MODEL_BYTES`, VQ-B2); `content_lint` green; one
  workspace nextest green

**Eye** (each named frame, after vs `target/fix-phase/before/`, angle 01 at
macro excluded per F-8):
1. `studio_beauty/macro_00` — mineral grain visible at 1024²; no waxy
   translucency; facet boundaries are not the dominant edge.
2. `raking_beauty/macro_00` — the key light finds surface, not just facets.
3. `studio_normal/macro_00` — high-frequency perturbation across the faces,
   density comparable to `ref_macro_00`.
4. `studio_beauty/gameplay_02` — no chart seam, no rectangular patch edges.
5. `studio_rough/*` — uniformly bright, not mid-grey.
6. **The blind test.** The orchestrator views `studio_beauty/gameplay_00..03`
   beside `ref_gameplay_00..03` and cannot pick which is the photoscan on
   material grounds alone. This is the user's actual criterion; 1–5 are its
   decomposition. If 1–5 pass and 6 fails, 6 wins and the phase is not done.

**Constraint restated:** `prop_audit.py` gains no threshold and gates nothing
in this phase. Every pass/fail above lives in this document and in the judge.
