---
name: quality-over-cost-ruling
description: Quality outranks time/coding/change cost; replacing tools or whole technologies is in scope
metadata: 
  node_type: memory
  type: project
  originSessionId: 5a202ec3-bb7c-40b2-b00e-426ccfd983ce
  modified: 2026-07-24T22:25:34.673Z
---

Ruled during the chapel_arch fix phase, verbatim: *"we want quality
at any cost (of time, coding or changes) so go for the best outcome solution, if
we need to check for tools and replace technologies we go for it, we need the
quality."*

**Why:** the fix phase established that the current asset stack (Hi3DGen meshes +
multiview-diffusion texturing) produces smooth shapes with blurry painted albedo,
and that no post-processing manufactures surface detail the source never had. The
ruling was given in direct response to that finding, so it is aimed at exactly
this class of decision.

**How to apply:** when a plan's options split into "incremental fix within the
current stack" vs "replace the tool/technology", do not default to the
incremental one on cost grounds, and do not pre-filter the expensive option out
of a choice presented to the user. Price both honestly and recommend by outcome
quality. The [[strict-nc-tooling-ruling]] licensing gate still binds — quality
does not override licensing. See also [[incumbent-tools-not-gates]] and
[[aa-art-direction]].
