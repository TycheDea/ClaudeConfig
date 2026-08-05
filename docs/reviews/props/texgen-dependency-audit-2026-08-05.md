# Texgen dependency audit + legal rulings (2026-08-05)

Follow-up to `texgen-licensing-brief-2026-08-05.md`, executed under the
user's directive: legal read → research for a viable tool → license-free
plan if none. Research-worker findings condensed; all quotes fetched from
raw LICENSE files / repo source / HF cards this day.

## Legal rulings (orchestrator, license texts fetched and quoted)

**Ruling A — Hunyuan is a hard out for an EU developer.** Hunyuan3D-2.1
Community License, verbatim: "THIS LICENSE AGREEMENT DOES NOT APPLY IN
THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA AND IS EXPRESSLY
LIMITED TO THE TERRITORY"; "'Territory' shall mean the worldwide
territory, excluding the territory of the European Union, United Kingdom
and South Korea"; "You must not use, reproduce, modify, distribute, or
display the … Works, Output or results … outside the Territory." An
EU-domiciled licensee holds no grant, and even outputs are barred. Taints
all weight/code descendants: RomanTex, MaterialMVP, LumiTex's Hunyuan
components, any future NaTex release under like terms. (Not legal
advice; the clause admits one reading.)

**Ruling B — standing "TRELLIS = NC" NARROWED to "nvdiffrast/nvdiffrec =
NC".** nvdiffrast license verbatim: "The Work and any derivative works
thereof only may be used or intended for use non-commercially";
"'non-commercially' means for research or evaluation purposes only".
TRELLIS.2 code and weights are MIT (repo + HF card `mit`). The strict-NC
principle is unchanged — those two libraries never touch the shipping
path; MIT weights are not contaminated by a swappable dependency
(Hi3DGen, our shipping mesh stage, is the worked precedent: a TRELLIS
derivative that stripped the NVIDIA deps for commercial use).

## Dependency audit verdicts

**MVPainter — TAINTED, out.** Repo badge Apache-2.0, but:
`mvpainter/differentiable_renderer/mesh_render.py` carries "Copyright (C)
2024 THL A29 Limited, a Tencent company … licensed under the TENCENT
HUNYUAN NON-COMMERCIAL LICENSE AGREEMENT" and IS the texture baker
(vendored Hunyuan `custom_rasterizer` + back-projection);
`src/utils/mesh_util.py` carries the NVIDIA proprietary header and
`import nvdiffrast.torch`. GitHub issue #2 raised commercial use;
closed without maintainer reply. 12 GB fit unverified (only a 24 GB
practitioner report). IDArb (its PBR init) is MIT code but its weights
carry no license tag; lineage SD2.1/OpenRAIL++.

**TRELLIS.2 — TAINTED for texturing as shipped.**
`trellis2/pipelines/trellis2_texturing.py` top-level `import
nvdiffrast.torch as dr` and calls `dr.rasterize(...)` for the UV bake —
the texturing entry point is unreachable without the NC dep. Issue #22
(commercial clarification) open, no reply. No nvdiffrast-free fork
exists (Stable-X has no TRELLIS.2 project). ComfyUI wrapper ships
nvdiffrast wheels. GGUF weight repos: `ilintar/trellis2-gguf` license
tag `other` with an erroneous source link; `Aero-Ex/Trellis2-GGUF` no
card/tag. 12 GB texturing unbenchmarked (a GGUF shape-stage fix reports
~4.6 GB peaks; texturing unmeasured). Adoption requires our own
Stable3DGen-style surgery on the bake step + a VRAM proof.

**Material Anything — license-CLEAN, quality-burned.** MIT repo; weights
`xanderhuang/material_estimator`/`material_refiner` tagged `apache-2.0`;
inference deps clean of nvdiffrast/nvdiffrec/kaolin (bpy-based); base
SD2.1 (OpenRAIL++ lineage — use-restricted, commercial-ok; tag-vs-lineage
tension noted, not NC). BUT: our own pipeline adopted its delighting once
and deleted it for cause — "monochrome cream" albedos (commit `d037686`),
and its issue #13 reports the same white-albedo failure with no
maintainer reply; issue #16 reports non-reproducibility. License-clean,
evidence-negative on OUR defect class.

**Landscape delta since June 2026: no clean new hit.** StableGen
(Blender plugin, June 2026) is GPL-3.0 and pulls nvdiffrast in its
TRELLIS.2 mode; nothing else verifiable.

## Net position

No license-clean tool is PROVEN for our defect today. Two conditional
paths (Material Anything retest as eval; TRELLIS.2 after self-performed
bake surgery + VRAM proof) and one unconditional path: the license-free
in-house plan (`tasks/texgen-license-free-plan.md`), which the user's
directive names as the deliverable when no tool is found.
