# Research backlog

One narrow, answerable question per item. One research pass per item — never bundled.
Each pass: research → verification (primary sources) → gap-check → report to user.

Per-option schema for every item: extended description · technology · license + IP terms
for shipped commercial assets · real cost · VRAM/compute + whether it runs on 12 GB ·
wall-time per iteration · pros · cons · **how much worse than manual, and where** ·
**1–2 shipped games at comparable quality** · maturity (production-proven vs. bleeding-edge).

Status: `[ ]` todo · `[~]` partially covered, needs a dedicated pass · `[x]` done

---

## A — Image generation (2D layer)

- [x] **A1. Local open-weights T2I models** — quality, license, VRAM, quantization cost.
      *Done in `r2-image-models.md`. Verified: FLUX.2 klein 4B (Apache, ~13 GB),
      Qwen-Image (Apache, 20.4B), HiDream-I1 (MIT, 17.1B). All exceed 12 GB natively.*
- [ ] **A2. Commercial hosted image APIs** — Midjourney, GPT Image, Nano Banana, Ideogram,
      Recraft, Seedream, Reve, Luma, Firefly. Quality, per-image price, and above all
      **the IP/commercial terms for assets shipped in a game** (some forbid it outright).
- [x] **A3. Style uniqueness — LoRA / fine-tuning.**
      *Done in `a3-style-lora.md`. LoRA/DoRA on `FLUX.2-klein-base-4B` via ai-toolkit (MIT).
      Only the klein **4B** is Apache and ungated — the 9B is non-commercial. Training needs
      24 GB (BFL's own figure); 13 GB is the inference number. kohya_ss supports none of the
      three bases. Real cost is dataset curation, not GPU time.*
- [x] **A4. Control + consistency tooling.**
      *Done in `a4-control-tooling.md`. **FLUX.2 klein 4B has no usable depth-control path** —
      no ControlNet exists, none in ComfyUI core, BFL's Depth/Canny are FLUX.1-only and
      non-commercial. A3's base pick cannot stand. HiDream eliminated. Qwen-Image has a real
      Apache depth ControlNet in ComfyUI core but is 40.9 GB. Gap-check surfaced **Z-Image**
      (6B, Apache) as a fourth base with depth ControlNet + LoRA composition already shipped —
      quality unassessed. Regional prompting is base-agnostic in ComfyUI core.*
- [x] **A5a. Comparative quality research** — *done in `a5-comparative.md`. Arena Elo puts
      Z-Image Turbo (6B) above Qwen-Image (20.4B) and FLUX.2 klein 4B; SDXL trails by 190–280.
      **Nothing anywhere benchmarks painterly/dark-fantasy output** — every comparison tests
      photoreal portraits, products, and text, so the numbers measure the wrong thing.
      Qwen-Image's cross-sourced "plastic skin" complaint is a bad sign for worn-material work.
      Qwen-Image-2.0 (7B, Feb 2026) is **disqualified — weights closed, API-only.***
- [x] **A5b. Base decision bake-off** — *done in `a5b-bakeoff-results.md`. 24 generations, 4 ortho
      views, real candelabra subject+seed. **SDXL eliminated on measurement** (worst baked lighting,
      worst cross-view drift). **Qwen-Image wins texture-fitness** — only config good on every axis,
      but 5× slower (75 s/view) and hardest to fine-tune. **Z-Image** is 5× faster, trains
      comfortably in 24 GB, best depth adherence of any run, but material separation stays
      unreliable after two prompt revisions. Awaiting user ruling.*
      Side findings: prompt verbosity trades against geometric fidelity on cfg-1 bases (raising
      ControlNet strength is the wrong lever); negation in a positive prompt is ignored, and cfg-1
      bases have no negative prompt, so the pipeline's flat-lighting control has no equivalent.*
      **RULED 2026-07-20: Z-Image**, on trainability. Qwen-Image retained on disk as the fallback;
      the bake-off harness is kept to make revisiting it cheap.

## A6 — Wiring Z-Image in (next phase, blocks C1/F1)

- [x] **A6.1. Settle the MR contract.** *Done in `a6-1-mr-contract.md`. The band does break
      (57.9% → 77.9% metal), but measurement showed it was **never valid**: it sits below the
      natural bimodal boundary even on SDXL, has exactly one consumer (`candelabra_shrine`), and
      no ground truth. A self-normalising (Otsu) threshold was tried and **rejected on
      measurement** — 82% metal on SDXL. Luma conflates albedo, shading and material, so the
      dominant split in a dark render is lit-vs-shadowed, not iron-vs-wax.
      **RULED: zoning retired.** `--mr` → declared `--metallic`/`--roughness` constants;
      four constants, the enum and the `island` return path deleted. MR now rides the glTF
      scalar factors, not a 1024² map (GLB 4.01 → 3.22 MB). Swap unblocked.*
- [x] **A6.2. Replace the flat-lighting control.** *Done in `a6-2-flat-lighting.md`.
      **No replacement needed — the premise was false.** Built a direct baked-lighting metric
      (luminance that tracks surface orientation, `bakeoff/metrics.py`) with a sun-lit positive
      control (`bakeoff/lit_control.py`) that makes the scores falsifiable. Sun-lit control 0.330;
      SDXL with its negative prompt 0.011; Z-Image without one **0.014**; Z-Image **explicitly
      asked for chiaroscuro 0.018**. Flat albedo is a property of depth-conditioned multiview
      generation, not of the prompt — the negative prompt was inert insurance on SDXL too.
      Closes with a deletion: the negative prompt does not carry over at A6.4.*
- [x] **A6.3. Material separation.** *Done in `a6-3-material-separation.md`. **No Qwen trigger.**
      The per-view candle flip is real and does **not** wash out in the facing-weighted blend —
      a full-stage Z-Image run shipped black candles. But that run used the generic prompt, whose
      subject says "melted wax candles" with no colour; the bake-off config that worked said
      "**cream** wax candles". Re-run with "pale cream-white wax candles" → correct separation,
      comparable to the shipped SDXL asset. **Finding: Z-Image needs material colours named
      explicitly in the subject** (SDXL at cfg 7 infers them; a cfg-1 base does not), composed
      with A5b's keep-prompts-short constraint. Also corrects A6.1: the "chrome" turntable render
      is a bright-studio artifact — under the game HDRI, zoned / metallic-1 / dielectric are all
      but indistinguishable, so A6.1's visual stakes were overstated.*
      **Refined by V1 (`v1-execution-verification.md`, seed/subject robustness batch):** colour
      naming is causal and generalizes, but weak colour words ("cream") flip under seed variance —
      name a **strong, unambiguous colour** per material, and gate separation per asset at
      turntable review; shape-ambiguous props (candle-vs-cup) are the risk class.
- [x] **A6.4. Swap `prop_multiview.json` to Z-Image.** *Swap done and verified end-to-end;
      fixed two regressions it exposed (null seed provenance from a hardcoded SDXL node id;
      stale `stats["strategy"]` literal). **Prop regeneration done 2026-07-21**:
      `candelabra_shrine` fully re-rolled through gen_prop (new Hi3DGen geometry, Z-Image
      multiview, subject naming strong colours per V1, blend_coverage 0.6823 vs SDXL's 0.6801).
      Review gate: cream candles hold in all 4 views — no separation flips at seed 2. Installed +
      lint-green (`1bbc106`); workspace suite 408/0. **MR declaration corrected to dielectric**
      (`0894d2f`): A6.1's metallic-1 ruling assumed a near-black asset; the bright cream candles
      at metallic 1 read as crystal, while game-HDRI side-by-side shows the dark iron identical
      either way — with one constant per prop, the declaration must favor the bright material.
      Side fix: `gen_prop.py` broke on relative `--out` in every cwd-changing stage — resolved
      once in `main()` (`26316f2`).
      **A6.1's escalation rung built 2026-07-21 (`a4d25e5`)**: `--mr-mask` runs a second
      depth-conditioned multiview pass prompting a two-tone material-ID render (white metal /
      black dielectric), blends it with the existing machinery, smoothsteps luma → per-texel
      metallic; roughness lerps `--metal-roughness`/`--roughness`. Candelabra re-rolled with it
      (metal fraction 0.30, iron reflective / wax+stone matte, `3e1a564`). The retired luma
      classifier stays dead — the mask *generates* material identity instead of inferring it.*
      **A6.2 watch item:** flat albedo holds *because* the depth signal dominates, so anything
      that weakens depth conditioning may reintroduce baked lighting — re-run `bakeoff/metrics.py`
      against `lit_control.py` rather than assuming it survives.

## B — 3D geometry

- [ ] **B1. Open-weights image→3D** — current SOTA vs our Hi3DGen incumbent. License, VRAM.
- [ ] **B2. Commercial image→3D products** — Meshy, Tripo, Rodin, 3D AI Studio, Hitem3D.
      Quality, price, IP terms. *May outclass the DIY route; must be priced honestly.*
- [ ] **B3. Text→3D and native-3D generative approaches** — anything skipping the 2D hop.
- [ ] **B4. Topology + UV automation** — quad remesh, auto-retopo, auto-UV, decimation.
      *Determines whether generated geometry is animatable or only decorative.*

## C — Texturing

- [x] **C1. Texturing existing geometry** — *done in `c1-texturing-geometry.md`. **Keep the
      incumbent; adopt no named tool.** Of the seven, four are unusable on licensing:
      **FlexPainter** (pins `NVlabs/nvdiffrast`, NC — the standing ruling's own precedent — and
      is FLUX.1-dev-based), and **MVPainter**, which claims Apache 2.0 but was verified to
      redistribute Tencent's `custom_rasterizer` **byte-identically** with the "TENCENT HUNYUAN
      NON-COMMERCIAL LICENSE" header stripped; also 40 GB VRAM. Same EU/NC block hits
      Hunyuan3D-Paint (§3(c) prohibits use *and Output* outside a Territory excluding the EU) —
      otherwise the quality leader. MVPaint and TEXGen have **no license file at all**.
      SyncMVD/Paint3D/TEXTure are clean but frozen to SD1.5/SDXL UNets; **MV-Adapter** is clean,
      fastest and best-shaped, but ships SDXL/SD2.1-only weights — retargeting to Z-Image's DiT
      is a research project. MV2UV has no code. **Recommendation: close A6.3's independent-view
      gap in-house** with sequential img2img conditioning (TEXTure's mechanism, ComfyUI-core
      nodes, ~1 day, architecture- and CFG-agnostic). **Unresolved:** nothing here fixes
      **cross-variant** consistency across 150 armor variants — the axis where F1 wins by
      construction.*
      **Gap-check:** asked the portable question the first two passes missed — does a cross-view
      mechanism exist for *any* DiT? It does, and it is **already in ComfyUI core for our own
      family**: `ZImagePixelSpace(Lumina2)` consumes `reference_latents`, and
      `TextEncodeZImageOmni` takes 3 reference images (fits a 4-view stage exactly). On a DiT the
      mechanism is in-context token concatenation, needing no architecture change — which is why
      no "MV-Adapter for DiT" exists or needs to. **But it drives Z-Image *Omni*, which is
      unpublished** (HF search 0 results; ModelScope `record not found` vs. a real tree for Turbo;
      ComfyUI shipped the node 2026-01-20 ahead of the model). Watch item, not an adoption — the
      img2img recommendation stands and is now the pixel-space form of the native mechanism.
      Also **corrected a candidate**: Lumina-Accessory's HF `apache-2.0` tag covers weights only;
      its GitHub repo is `license: null` with no LICENSE file at any ref → Blocked.
      MV-Adapter confirmed dead upstream (no commits since 2025-06-26, DiT support never shipped).*
- [ ] **C2. Commercial 3D texturing tools** — including whether B2's products expose
      texture-only modes for geometry we supply.
- [ ] **C3. Tileable PBR material generation** — StableMaterials successor + its license
      risk (`openrail` tag, no LICENSE file, dead predecessor repo).

## D — Characters

- [ ] **D1. Parametric body sources** — MPFB2 incumbent vs alternatives.
- [ ] **D2. Garment/armor authoring** — MHCLO automation from Blender, cloth sim,
      generative garment tooling. *Feeds the (b) ruling directly.*
- [ ] **D3. Auto-rigging + skinning** — UniRig incumbent vs current SOTA.
- [ ] **D4. Face/head variation** — per-race identity at scale.

## E — Animation

- [ ] **E1. Text→motion licensing re-check** — is there a non-AMASS clean corpus yet?
      *Expected answer is still no; the point is to re-test, not assume.*
- [ ] **E2. Procedural + physics-based animation** — locomotion, IK, ragdoll.
- [ ] **E3. Retargeting + animation tooling** — clip adaptation across skeletons.

## F — Non-AI automation

- [~] **F1. Procedural geometry** — *research + verification passes done in
      `f1-procedural-geometry.md`; **gap-check pass still owed**. The head-to-head closes, but
      not along the axis it was posed on: **neither Geometry Nodes nor generative AI is the
      winning unit**. Variants split into a colour/material axis (~70–90% of the matrix — an
      unsourced estimate, and the report's weakest load-bearing number) and a silhouette axis.
      The colour axis is won by **material zoning at zero marginal cost**; the silhouette axis by
      **Python-driven kitbash assembly** over a hand-modelled trim library, with GN as the
      parameterizer, not the authoring tool. **AI image-to-3D geometry is disqualified outright**
      — unstructured non-quad output satisfies neither MPFB2 `.mhclo` weight-transfer path without
      a per-variant retopo/reweight that erases the saving. So there is no crossover N; the
      crossover that exists (parts library vs. hand-modelling each piece) pays back at the
      **second variant of any shell**. Licensing is clean across the whole option space — a
      structural contrast with C1. Houdini rejected (Indie's $100K revenue cliff, plus a
      second-DCC cost Blender 5.2 no longer justifies); ArmorLab corrected — dead since 2023 and
      a texture tool, not armor geometry.*
      **Verification:** Blender 5.2 confirmed (`gen_prop.py:43`). The report's own main open risk
      resolved **against its proposed mechanism**: a whole-mesh `tint` exists plumbed end-to-end
      (`MeshInstance.tint`, both pipelines, both shaders) but is one global multiply already used
      for class identity — no `material_id` anywhere. However `MaterialUniform` is **per-primitive**,
      so four-zone armor is expressible with **zero renderer changes** by authoring four glTF
      materials and letting the variant script write four `baseColorFactor`s — the same move A6.1
      made when it put MR on glTF scalars. RGBA mask-texture work is deferred until player-facing
      dye becomes a design requirement.
      **Drape test (settled, `f1_drape_probe.py`):** the mhclo **fit** passes — novel all-quad
      shells re-fit across a 1.67 m → 2.23 m body change, standoff scaling ~1.4× against 1.34×
      growth, zero interpenetration at rest, under pose and after conform. **Weight transfer**
      passes only where a standoff cage exists: on raw `body` a pauldron inherits 25% upper-arm and
      11% head weight against 15% shoulder, swinging 48% of upper-arm length on an arm raise, and a
      shoulder cloak skins to the legs with 29 verts tearing; on `helper-skirt` the same cloak is
      inert and coherent. Of 152 basemesh groups only `body`, `helper-skirt` and `helper-tights`
      are bindable, so an uncaged part cannot declare intent. Parts therefore split three ways:
      caged loose geometry (works), rigid armor (keep the fit, discard the weights, bone-parent),
      loose geometry above the waist (no cage — author weights once per shell).
      **Four script constraints, each earned by a harness bug this test hit:** author mhclos
      **through the file** (in-memory offsets stay in MakeHuman's frame and only `Mhclo.load`
      converts them — 82–196 mm drift on an identity refit); **refit the armature** alongside the
      body, or rest positions measure correct while everything displayed is wrong; **project parts
      onto the skin** at authoring time, since MPFB preserves handed-in penetration silently and
      conform scales it up with the body (78 → 104 mm measured); and **assert with a signed
      penetration test plus a weight-distribution check** — nearest-vertex distance is blind to
      burial (it read a healthy 2.5 mm gap over 20 verts up to 78 mm inside the torso), and MPFB's
      own validation returned `all_checks_ok: True` for every failure above.
      **Negative space:** no GDC talk, postmortem or dev blog describes any AAA ARPG's *character
      armor* as kitbash/procedural at D4/PoE2 fidelity — D4 hand-sculpts armor in ZBrush and
      kitbashes only environments. The report flags this itself rather than glossing it.*
- [ ] **F2. Procedural materials** — substance-style graphs, node-based texturing.

## G — Cross-cutting

- [x] **G1. Compute envelope** — *done in `r1-compute.md`. NVIDIA free credits are ToS-barred
      from production; Modal/Replicate/RunPod are the practical rentals.*
- [ ] **G2. Hardware** — cost/benefit of a 24–32 GB GPU. All three A1 finalists exceed
      12 GB; an upgrade deletes the quantization-quality unknown instead of managing it.
- [ ] **G3. Orchestration tooling** — ComfyUI vs alternatives, pipeline frameworks,
      reproducibility, batch/queue automation.
- [ ] **G4. Quality calibration** — which shipped games sit at our target register, what
      their real pipelines were, and where each option above lands against them.
      *Runs last; synthesises the "how much worse than manual" column across all items.*

---

## Suggested order

**G2**, **A3**, **A4**, **A5**, **A6.1–A6.4** and **C1** are done; the Z-Image swap is complete
and the shipped candelabra is the first Z-Image asset (V1-verified process, `1bbc106`).

**F1's research + verification passes are done and the armor decision has flipped**: procedural
owns geometry and material zoning, AI texturing shrinks to hero/unique pieces. C1's
sequential-img2img fix stays correct but is **demoted off the critical path** — it no longer
carries the 150-variant art book's coherence, since material zoning delivers that by construction.

**The drape test is done** (`f1_drape_probe.py`, headless, CPU). The mhclo **fit** is a clean pass —
novel all-quad kitbash shells re-fit across a 1.67 m → 2.23 m body change with standoff scaling
proportionally and no penetration, which is the parts-library premise and it holds. **Weight
transfer** passes only where a standoff cage exists: bound to raw skin, a pauldron inherits 25%
upper-arm and 11% head weight against 15% shoulder and swings with the arm, and a shoulder cloak
skins to the legs and tears. Bound to `helper-skirt` the same cloak is correct. So parts split into
three rigging classes — caged loose geometry (works), rigid armor (take the fit, discard the
weights, bone-parent), and loose geometry above the waist (no cage; author weights once per shell,
a cost not a blocker). The recommendation changes shape, not direction. Four constraints on the
generation script are recorded in the F1 entry below; the sharpest is that **MPFB validates
topology and scale only** — it returned `all_checks_ok: True` for a pauldron with 20 vertices
buried in the torso, so penetration and weight distribution must both be asserted independently.

Next is **F1 gap-check**, then **C3** (materials).

Then geometry: **B1**/**B2** → **B4**. Then characters **D1–D4**, animation **E1–E3**.
**A2**, **G3** as they become relevant. **G4** last.
