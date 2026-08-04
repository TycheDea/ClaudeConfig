---
name: strict-nc-tooling-ruling
description: "User ruling — non-commercial-licensed tools may never touch the production asset path, even as build tools"
metadata: 
  node_type: memory
  type: project
  originSessionId: c22c49b4-e784-4a42-8b1b-ce1396b5adec
  modified: 2026-07-23T09:49:14.564Z
---

Non-commercial-licensed software (e.g. nvdiffrast) must NOT be used anywhere in the pipeline that produces shipping assets — the "tools don't taint outputs" reading is rejected. Eval-only/research use of NC tools is allowed, but their outputs never ship.

**Why:** user ruled "Strict: no nvdiffrast" when TRELLIS's glb texture bake was found to hard-import nvdiffrast (NC) — consistent with the earlier TRELLIS.2 block for the same dependency. Zero license risk outranks pipeline convenience.

**How to apply:** production image→3D backbone is Hi3DGen (MIT, nvdiffrast stripped) with a bespoke texturing step; TRELLIS 1 demoted to eval-only in the `content/source/CREDITS.md` ledger. Any new tool entering the pipeline gets the same test: NC dependency in the shipping path = blocked.

**A clean LICENSE file is not proof the code is the author's to license** (learned C1). MVPainter ships verbatim Apache 2.0 yet was found redistributing Tencent's `custom_rasterizer` byte-identically with the "TENCENT HUNYUAN NON-COMMERCIAL LICENSE" header stripped. So when a repo says it "builds upon" a restrictively-licensed project, **diff the vendored modules against upstream** — license text alone cannot catch this. Two other traps worth reusing: check licenses for **territory** clauses, not just commercial/NC ones (Hunyuan3D-2 excludes the EU outright, and its §3(c) reaches generated *Output*, not just the code); and fetch license bytes with a plain HTTP client, since a summarizing fetch hides prepended NOTICE headers and stripped attribution.

**An HF card tag is not a code license** (learned C1 gap-check). Lumina-Accessory's HF
page tags `apache-2.0`, but that covers the weights repo; its GitHub repo reports `license: null`
with no LICENSE file at any ref — so the framework code is undeclared and blocked. Weights and
code are separate artifacts with separate licenses; check both, and check the code one from the
GitHub repo API plus a raw LICENSE fetch, never from the model card.
