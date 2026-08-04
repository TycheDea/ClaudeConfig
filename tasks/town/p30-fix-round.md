# P3.0 chapel gate — fix round

Answers `docs/reviews/town/p30-chapel-legibility-2026-08-01.md` (FAIL).
Evidence re-rendered to `target/zone-review/p30-chapel/` (28 PNG).

## R0 — checks that graded meshes the renderer never draws

| check | mesh it read | mesh the renderer draws | verdict |
|---|---|---|---|
| C1 footprint | build-time `dims` over every built object | same | sound |
| C2 collapse | `limestone_dressed` verts, wall band | same | sound mesh, **blind to a level datum** |
| C3 signature | espadaña / bell / cross / portal bboxes | same | sound |
| C4 `slope_uv_seam` | the deck cluster (largest up-sloped plane) | the deck is buried under 25 barrel tiles + 26 ridge caps | **wrong mesh — deleted** |
| C5 `ridge_bare` | `*_ridge_*` terracotta above the deck | same | sound; its scope simply never covered UVs |
| C6 `_quoin_flush` | shipped `_quoin_` bboxes vs encalado planes | same | **sound mesh, wrong defect** |

Root cause behind gate fixes 2 and 3: `materials.project_uv` used
`bpy.ops.uv.cube_project`, whose origin is the **object's own median**, so every
congruent object landed on an identical UV set — 25 roof tiles, 26 ridge caps,
18 vault voussoirs, the crown blocks and the rubble boxes each stamping one
patch N times. Replaced with a world-anchored per-face box projection;
`vordar_uv_offset` (the per-quoin random offset that worked around the same
defect) is subsumed and deleted.

- [x] R0 world-anchored box projection
- [x] C4 replaced by `uv_patch_repeat` — compares the whole per-object UV
      multiset (a bounding rect is dominated by a barrel tile's buried flanks
      and over-fires), across every type. **32 faults on the shipped models,
      0 after.**
- [x] C2 gains `collapse_crown_datum` — longest horizontal masonry line in the
      collapsed bay / bay length. **1.00 shipped, 0.20 after**, threshold 0.30.
      Flat for any ground floor 0.2–4.0 m and any quantum ≤ 0.02.
- [x] C6 gains `quoin_course_void`. **139 voids of exactly 0.030 m shipped, 0 after.**
- [x] `barrel_shell` wedges get a cylindrical UV (arc length × radius ×
      extrusion) — a voussoir ring box-projected as flat wall inherits the
      tile's horizontal courses and reads as the wall it is cut into.

## The ten fixes

- [x] 1 crown datum destroyed (blocker) — span B rebuilt as broken masonry columns
- [x] 2 roof tile UVs (via R0)
- [x] 3 ridge cap UVs (via R0)
- [x] 4 quoins — **DIVERGENCE**: the gate's mechanism is spec §0's *pre-fix*
      code. Shipped quoins are already flush + 0.02. The real defect is the
      0.03 m air void `gap` left between courses. Bonded instead; proud 0.02 → 0.05.
- [x] 5 oculus dressed: full 16-wedge ring, r_in 0.50 / r_out 0.85
- [x] 6 east wall face recessed 0.20 m inside the 0.60 m thickness; rings and
      espadaña keep x = 8.600 so the footprint does not move
- [x] 7 interior rubble: 17 pieces, rotated + tilted, bedded, spread x 0.75–7.60,
      6 in the voussoir size family
- [ ] 8 exterior rubble — **NOT DONE, blocked.** See below.
- [x] 9 bell profile (flared mouth + crown) and yoke clear of the arch head
- [x] 10 coplanar hatch: `chapel_floor` top sat at local z = 0 → world −0.5,
      exactly `client::ground::GROUND_TOP_Y`. Paving raised to +0.05.
- [x] watch item: `chapel_skyline` frame added — espadaña against sky, east
      approach, standing height

### Fix 8 is geometrically blocked

The chapel's XZ AABB is x [−11.629, 8.600], z [±4.100] and `footprints.ron`
records it verbatim with 0.02 m of D5 margin. There is no slack on any axis, so
the chapel model cannot emit a single vertex outside its own walls. Exterior
rubble therefore has to be a separately placed prop, and the two routes both
fail on their own terms:

- `kind: "kit"` — D5 then demands a `footprints.ron` entry, a chapter03
  collision prefab and an axis-aligned yaw. A collision box on ankle-height
  debris is wrong, and axis-aligned yaw kills the scatter that makes rubble read.
- any other kind — `prop_material_matches_surface_class` requires an occlusion
  map and forbids a metallic-roughness map, i.e. the generated-prop bake, which
  a townkit export does not produce.

R2 (layout) remains the right owner. Reported, not worked around.

## Observations, not fixed

- `iron_wrought` is metallic 1.0 with a near-black albedo, so its f0 is ~0.03
  and the IBL specular term is all it has: the bell still renders very dark.
  The new profile carries the read as a silhouette, which is what the tronera
  framing gives it. Changing the family's metallic would touch every reja and
  the crucero — a ratified materials decision, escalated rather than taken.
- ~~A faint regular vertical striping is visible on limestone at ~2 m
  (`close_chapel.png`). It comes from the renderer's world-space triplanar
  detail overlay (`sample_detail(in.world_pos, …)`), not from any UV, so it is
  independent of this round.~~ **Wrong, and asserted from code-reading rather
  than a probe.** Measured in the re-gate round below: the striping is this
  round's own span-B masonry columns.

---

# RE-GATE round — the four non-blocking fixes

Answers the re-gate section of
`docs/reviews/town/p30-chapel-legibility-2026-08-01.md` (PASS with fixes).
Chapel only; no other kit model's bytes move.

## 1 — striping attribution: **the kit's own geometry, introduced by `3feb4a7`**

Probe: the chapel's north wall re-rendered at zone_review's own close-up
distance, crossing camera azimuth (the shipped grazing 45° vs head-on) with
the shared detail tile bound vs the renderer's neutral 1×1 default
(`DETAIL_*_STRENGTH = 0` without touching the shader).

- The lines survive with the detail tile unbound, pixel for pixel — not the
  overlay, not the tile's wrap.
- Their world positions match the span-B column boundaries measured from the
  shipped glTF to within 1 cm (7 of 14 detected dark lines; the rest are the
  albedo's own ashlar joints).
- They are absent from `3feb4a7^`'s chapel at the identical framing, so they
  do not predate the commit.

Cause: each broken-masonry column carried `bevel=0.02` and overlapped its
neighbour by 1 cm, so every junction was a chamfer pair plus a coplanar
sliver, running the wall's full height. Columns now abut on an exact shared
plane with no chamfer; the world-anchored UV runs on through the junction.

- [x] 1 striping — 0 of the remaining dark lines fall on a column boundary
- [x] 2 oculus opened — shuttered in `oak_dark` at the back of the reveal
- [x] 3 rubble — bedded from the piece's own rotated low point, 17 → 23
      pieces, weighted to mid-bay. **Divergence, see below.**
- [x] 4 crown stair rhythm — surviving piers rise against the funnel

### Fix 3's stated diagnosis does not reproduce

The record says the scatter "clusters where the roof survives". Every piece,
before and after, lies in x ∈ [0.75, 7.60] — the collapsed bay — and none is
under the vault. Inverting `mid_graveyard.png`'s camera onto the floor plane
shows why: that frame's floor is chapel-local x −7.6 … +2, i.e. the *roofed*
half seen through the fracture; the east wall hides the breach floor from
that camera entirely. The defect the crop actually shows is that the pieces
did not read as mass — `bed` was a fraction of the box's *unrotated* half
height, so a tilted metre-long voussoir sat up to 60 % underground. Bedding
now measures the rotated low point. Judged from `interior_door.png`, where
the bay floor is genuinely visible.
