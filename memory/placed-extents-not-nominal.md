---
name: placed-extents-not-nominal
description: Clearance/fit claims derive from the object's extent under its actual transform, read from shipped geometry — never nominal dimensions, centerlines, or the authoring pass's own table
metadata:
  type: feedback
---

Fires when writing any clearance, overlap, or fit claim about an object placed under a rotation, scale, or composite offset; when prescribing a coordinate in a review (that is authoring a placement); when filing a dimension into a manifest that calls its own numbers measured.

**Why:** four rounds in one layout campaign — a yaw swung a 5.46 m span across a wall the claim said it cleared by 0.9 m; a footprint table authored as wall centerlines left every half-extent short; the reviewer's own fix prescribed coordinates that put props inside masonry; and the "measured" manifest contained the arithmetic it existed to retire, caught only when the lint re-measured `size` off the glTF.

**How to apply:** derive from the shipped geometry under the actual transform. The plan's own clearance table is never the evidence — it was computed by the pass that chose the coordinates. A reviewer prescribing a coordinate owes the same extent check as the pass being reviewed. Labels claiming "measured" are enforced by a check, not asserted. The number in the prose is the suspect; the geometry is the witness.
