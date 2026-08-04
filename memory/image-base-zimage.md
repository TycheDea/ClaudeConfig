---
name: image-base-zimage
description: Z-Image is the ruled image-generation base; Qwen-Image retained on disk as the fallback
metadata:
  node_type: memory
  type: project
  originSessionId: 6b88d90b-2f02-4356-8a95-5d50bfe5c020
  modified: 2026-07-24T13:56:41.119Z
---

**Z-Image** (`Tongyi-MAI/Z-Image-Turbo`, 6B, Apache 2.0) is the image-generation base for the
asset pipeline, ruled after a measured bake-off. SDXL was eliminated on measurement.
**Qwen-Image weights stay on disk (~32 GB) as the documented fallback.**
`workflows/prop_multiview.json` carries the Z-Image graph as of A6.4 (cfg 1, 8 steps,
Fun ControlNet-depth model patch). `prop_concept.json` is also Z-Image as of `1451bfb`
(t2i graph — A/B on the crucero ruled it over SDXL, single-object framing
3/3 vs 1/3; SDXL concept path deleted per swap rule). SDXL still runs the HDRI and
material stages.

**Why:** a trained house-style LoRA is the only durable route to a proprietary look, and Z-Image
is the only candidate that trains comfortably in 24 GB (Qwen needs 3-bit quantization). The user
ruled trainability above today's texture quality, explicitly keeping Qwen for a possible revisit.

**How to apply — the A6 phase settled what actually constrains this base (V1-verified):**
1. **Name a strong, unambiguous colour for every material in the subject string.** At cfg 1 it
   does not infer colour from a material name, and weak colour words are not seed-robust: "cream
   wax" flips to black under 3 of 4 seeds, "deep crimson red wax" binds 4/4 views. Views are
   independent generations, so a weakly-bound colour resolves differently per view and survives
   the blend. Shape-ambiguous props (candle-vs-cup) are the risk class; per-view separation stays
   a per-asset turntable-review gate, not a solved property.
2. **Keep prompts short.** Verbosity trades against geometric fidelity; raising ControlNet
   strength makes it worse, not better. Name colours, add no clauses.
   Live confirmation (candelabra seed 4): plain "white wax candles" flipped to
   black iron in the back view when the frame material ("wrought iron") dominated;
   "bright pure white wax candles" bound 4/4. Intensity+hue compounds are the robust form.
3. **Planar props need oblique side azimuths** (`prop_texture.py --azimuths 0,60,180,300`).
   An exact side view of a planar prop degenerates to a sliver depth map and the base
   hallucinates an unrelated object into it, which the blend then smears over thin members.
4. **Flat albedo needs no mechanism.** Measured (A6.2, reconfirmed at n=28 in V1): it holds
   because the depth signal dominates, not because of any prompt. Anything that weakens depth
   conditioning could change this — re-measure with `bakeoff/metrics.py` + `lit_control.py`,
   do not assume.

**Per-texel MR exists (`a4d25e5`):** `prop_texture.py --mr-mask "<white metal /
black dielectric prompt>"` runs a second depth-conditioned multiview pass as a material-ID
render and bakes a real `metallicRoughnessTexture` (smoothstepped luma → metallic; roughness
lerps `--metal-roughness` 0.65 / `--roughness` 0.8). Use it for mixed-material props; the
scalar declaration remains the default for single-material ones.

The material-separation risk the ruling accepted is **causal-and-mitigable, not resolved**
(V1, `.claude/tasks/ai-pipeline/research/v1-execution-verification.md`): colour naming provably works
and generalizes to other meshes, but is necessary, not sufficient per-seed. Z-Image's cross-view
drift is also seed-variable (0.019–0.060; Qwen's 0.0128 beats every observed seed) — the Qwen
revisit trigger is seam quality on regenerated props. Whether the style LoRA stabilizes material
binding is the next real test.

**Watch item — Z-Image Omni (C1 gap-check).** ComfyUI core already ships the
multi-reference in-context path for our family: `ZImagePixelSpace(Lumina2)` in `comfy/model_base.py`
consumes `reference_latents`, and `comfy_extras/nodes_zimage.py::TextEncodeZImageOmni` takes 3
reference images. That is the DiT-native cross-view mechanism, and it would close the
independent-per-view gap in latent space. **Omni is unpublished** — HF search returns 0; ModelScope
returns `record not found` (Turbo returns a real tree); ComfyUI landed the node ahead of
the model. Re-check availability before building any pixel-space substitute for it.

Related: [[research-needs-comparisons]], [[aa-art-direction]].
