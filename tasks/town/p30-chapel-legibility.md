# P3.0 — Chapel church-legibility kit pass

Spec only. Zero GPU. Closes the escalated KIT FINDING (`tasks/todo.md:549`)
plus its two riders (quoin stranding; roof mirror-band N3 + missing ridge cap).

Ground truth for this spec is the shipped geometry, not any prior document.
Every dimension below was read from `content/models/props/*/*.gltf`,
`content/chapters/chapter03/{footprints,chapter}.ron`,
`content/chapters/chapter03/prefabs/*.ron` or
`game/vordar-game/tests/content_lint.rs`. Where a figure handed to this spec
disagreed with the geometry, the geometry wins and the disagreement is named.

---

## 0. Measured baseline (read, not restated)

Frames. `townkit` builds Z-up; `export_yup=True` maps Blender `(x, y, z)` to
glTF `(x, z, -y)`. All dimensions below are **Blender/local chapel frame**
unless prefixed `glTF`. The chapel is placed at world `(-30, -0.5, -29)`,
`yaw 0`, so local x → world x and local y → world −z.

**Chapel, `content/models/props/chapel/chapel.gltf`**

| quantity | measured |
|---|---|
| triangles | **1 037** (59 meshes) |
| glTF AABB x | `[-11.629, 8.600]` → **20.229 m** |
| glTF AABB z | `[-4.100, 4.100]` → **8.200 m** |
| glTF AABB y (height) | `[-0.150, 10.534]` |
| materials bound | `limestone_dressed`, `oak_dark`, `plaster_smoked` (3 of 6) |
| nave | 7.0 × 16.0 interior, wall thickness 0.6 |
| side walls | y centre ±3.8, outer faces ±4.1, top z = 7.5 (springline), length 16.6 |
| east (door) wall | x ∈ [8.0, 8.6], length 7.6 (y ∈ [−3.8, 3.8]), top z = 7.5 |
| door opening | y ∈ [−1.2, 1.2], z ∈ [0, 3.2], flat head |
| vault | `barrel_shell` x ∈ [−8.0, 0.0], 18 wedges, r_out 3.5417, crown z = 10.5 |
| collapse lip | `barrel_shell` x ∈ [0.0, 0.5], 14 wedges, radial jitter 0.05 |
| apse | 5-segment fan, extreme face at x = −11.63; `cone_cap` to z = 8.5 |
| interior rubble | 7 boxes, x ∈ [0.4, 3.5] — **inside the nave only** |
| verify | 0 loose verts/edges, 0 normal faults, 0/30 bad joint gaps, 0 open wall faces |

`footprints.ron` records `size: (20.23, 8.2)` — this is **exactly** the glTF XZ
AABB (20.229 × 8.200). For the chapel, "ground-level outer extent" and
"whole-model AABB" coincide, because nothing on the chapel overhangs.

**casa_corner, `content/models/props/casa_corner/casa_corner.gltf`**

| quantity | measured |
|---|---|
| triangles | **6 576** |
| glTF AABB | x `[-3.366, 7.457]`, y `[0, 5.733]`, z `[-3.399, 3.399]` |

> **Correction to the brief.** The task statement gives casa_corner as
> 5 317 tris. Both `target/town-kit/build_report.json` and the installed glTF
> read **6 576**. 5 317 is stale (pre-`6d665d6`, before the roof re-tile). All
> budget arithmetic in §4 uses 6 576.

**Quoin protrusion, measured below glTF y = 4.0 (roof overhang excluded):**

| casa_small_a | x | z |
|---|---|---|
| `encalado` outer wall plane | ±3.225 | ±4.225 |
| `limestone_dressed` (quoins) | −3.366 … +3.371 | −4.353 … +4.363 |
| **protrusion past the render** | **up to 0.146 m** | **up to 0.138 m** |

`_quoins` draws a per-course half-width of 0.32–0.37 m (long face) or
0.21–0.25 m (short face) against a wall half-thickness of 0.225 m, so a single
corner stack alternates between **1.5 cm recessed and 14.6 cm proud**, course by
course. That irregular jag is the measured "loose blocks" mechanism.

**Roof UVs, measured on the shipped `casa_corner.gltf` (N3):**

| deck slope family | measured UV span |
|---|---|
| main +Z slope (area 30.2 m²) | U `[-0.2518, +0.2518]`, glTF V `[0.8553, 1.1447]` |
| main −Z slope | same |
| wing slopes | U span 0.775, V span 0.615 — same straddle |

`-0.2518 = -3.3/13.1072` (half the 6.6 m ext_length) and `1.1447 = 1 + 1.897/13.1072`
(half the 3.794 m slope run, after the exporter's `v_gltf = 1 - v_blender` flip).
**Both axes straddle an integer tile boundary, and the crossing lands exactly at
the panel centre — mid-slope in V, mid-length in U.** N3's diagnosis is now
measured, not inferred (§3.2).

**D5 coverage, recomputed from the .ron files:**

Chapel members placed at prop `(-30, -29)`, yaw 0, with their authored hitboxes:

| piece | world centre | half-extents | world x span | world z span |
|---|---|---|---|---|
| `chapel_wall_side` ×2 | (−30, −25.2) / (−30, −32.8) | (8.3, 3.75, 0.3) | [−38.3, −21.7] | [−25.5,−24.9] / [−33.1,−32.5] |
| `chapel_wall_apse` | (−38.3, −29.0) | (0.3, 3.75, 3.8) | [−38.6, −38.0] | [−32.8, −25.2] |
| `chapel_door_jamb` ×2 | (−21.7, −26.5) / (−21.7, −31.5) | (0.3, 3.75, 1.3) | [−22.0, −21.4] | [−27.8,−25.2] / [−32.8,−30.2] |
| `chapel_lintel` | (−21.7, −29.0) @ y 5.35 | (0.3, 2.15, 1.2) | [−22.0, −21.4] | [−30.2, −27.8] |
| `chapel_roof` | (−34.0, −29.0) @ y 10.2 | (4.0, 0.3, 3.5) | [−38.0, −30.0] | [−32.5, −25.5] |
| **union** | | | **17.20 m** | **8.20 m** |

`size` 20.23 − union 17.20 = **3.03 m shortfall** against `tolerance: 3.05`
→ **0.02 m of margin**, all of it the deliberately-uncollided apse fan. The z
axis is exact (8.20 vs 8.20).

Farthest solid, by the play-radius lint's own formula:
`chapel_wall_apse` → `sqrt(38.6² + 32.8²)` = **50.65 m** against the 55 m cap.

---

## 1. Ruling: what lands

Six kit features. Every one is procedural Blender geometry in `townkit`; none
is a hero (§6). Every one is **inside the existing XZ AABB at every height**,
which is the constraint that makes §5's downstream impact zero — it is a design
choice, imposed deliberately, not a happy accident.

Every new chapel object inherits `matlib.project_uv` at
`TEXEL_SCALE_M = 13.1072 m` automatically: `build_chapel` never calls
`_finalize_shell`, so no chapel object carries `vordar_uv_final`, so
`build_town_kit.main`'s projection pass covers all of them. **Texel density
(VQ-A3, 6.4 mm/texel) needs no per-feature authoring** — the only thing that
must not happen is setting `vordar_uv_final` on chapel geometry.

### F1 — Espadaña (bell gable) · slot `limestone_dressed`

The Castilian village-church signature, and the single feature that decides the
30 m silhouette. **Coplanar with the east wall** — this is the load-bearing
decision: it keeps x ∈ [8.0, 8.6], which is where the east wall already is, so
the measured footprint does not move.

| part | helper | centre (x, y, z) | size (x, y, z) |
|---|---|---|---|
| `chapel_espadana_body` | `geo.make_box`, bevel 0.02 | (8.3, 0.0, 9.35) | (0.6, 3.6, 3.7) → z ∈ [7.5, 11.2] |
| tronera cut, straight | `geo.make_box` (operand) | (8.3, 0.0, 9.05) | (1.0, 1.6, 1.7) → z ∈ [8.2, 9.9] |
| tronera cut, round head | `geo.make_cylinder`, r 0.8, depth 1.0, `Matrix.Rotation(π/2, 3, "Y")` | (8.3, 0.0, 9.9) | crown z = 10.7 |
| `chapel_espadana_gable` | **`geo.gable_infill` reused verbatim** — `x=8.3, thickness=0.6, depth=3.6, eave_z=11.2, ridge_z=12.4` | — | pitch 33.7° |

Both cuts are `DIFFERENCE`/`EXACT` boolean modifiers applied in sequence to the
body — **the exact pattern `build_gate_arch` already uses** for its `_bore_tmp`
cylinder (`buildings.py:405-413`). Nothing new is invented.

Resulting masonry: 0.7 m plinth (z 7.5–8.2), 1.0 m piers either side of a
1.6 m round-headed opening, 0.5 m of head above the crown, then the gable to
z = 12.4. Width 3.6 m sits inside the east wall's own 7.6 m span, so the
espadaña bears on solid wall along its whole footprint.

### F2 — Bell + cross · slot `iron_wrought` (new 4th slot on the chapel)

Premise §3 assigns "bell" and gate fittings to wrought iron; the cross rides
the same slot so no fifth family is bound.

| part | helper | centre | size |
|---|---|---|---|
| `chapel_bell` | `geo.make_cylinder`, segments 12 | (8.3, 0.0, 9.64) | r 0.26, depth 0.52 |
| `chapel_bell_yoke` | `geo.make_box` | (8.3, 0.0, 9.95) | (0.14, 1.72, 0.12) |
| `chapel_cross_v` | `geo.make_box` | (8.3, 0.0, 12.78) | (0.09, 0.10, 0.76) → z ∈ [12.40, 13.16] |
| `chapel_cross_h` | `geo.make_box` | (8.3, 0.0, 12.92) | (0.09, 0.48, 0.10) |

The bell top (9.90) overlaps the yoke bottom (9.89) by 1 cm so it reads as
hung, not floating. The yoke embeds 0.06 m into each pier. Everything sits
inside the tronera void (|y| ≤ 0.8, z ∈ [8.2, 10.7]) or on the gable apex —
**max |y| = 0.86 ≪ 4.1, max x = 8.6.** Footprint untouched.

`iron_wrought` is already in `content/models/surface_classes.json`
(metallic 1.0, roughness 1.0, detail false) and `materials.py` already sets
Metallic 1.0 for it, so `check_kit_materials` needs no registry change. Its
maps already ship in `content/models/townkit_textures/` for the casas, and
`SharedImage::new` keys on content hash — so the VQ-C5 texture-memory total
should not move (§4).

### F3 — Portal surround at the east door · slot `limestone_dressed`

Replace the door's flat head with a real voussoired round arch, **entirely
within the 0.6 m wall thickness** — no projecting order, no impost course.

- `geo.barrel_shell(f"{name}_portal", 0.0, (8.0, 8.6), springline_z=3.2,
  half_span=1.55, rise=1.55, thickness=0.35, lime, n_wedges=11,
  sweep_axis="y")`.
- `barrel_shell`'s `r` is the **extrados** radius (`r_out = r + jitter`,
  `r_in = r_out − thickness`). Setting `half_span = rise = 1.55` gives a true
  semicircle, r_out 1.55, **r_in 1.20 — which is exactly half the 2.4 m door
  opening.** The intrados therefore matches the opening and the ring springs
  0.35 m outboard of each jamb, bearing on wall.
- Bore the receiving masonry: `geo.make_cylinder("chapel_portal_bore_tmp",
  (8.3, 0.0, 3.2), radius=1.53, depth=2.0, None, segments=24,
  rotation=Matrix.Rotation(π/2, 3, "Y"))`, `DIFFERENCE`/`EXACT` against the
  east wall's `head0` segment, then removed. Same pattern as F1 and gate_arch.
- Intrados crown 4.40, extrados crown 4.75. `dims["door_height"]` stays 3.2
  (the springing), so `assert_chapel_dims`' existing `door_height ∈ [3.1, 3.3]`
  check still passes unchanged.
- The oak leaves are unchanged (hinged flat against the inner wall face). The
  lunette above z = 3.2 stands open — light through the one open door in
  Rocalba, per premise §6.

Odd count (11) puts a keystone on the crown axis. Free correctness bonus: the
new ring is a `barrel_shell`, so `_radial_normal_faults` and
`_wedge_joint_gaps` cover it with no new code.

### F4 — Fenestration · slot `limestone_dressed`

**Oculus, east facade.** `geo.make_cylinder` radius **0.50**, depth 1.0, axis
X, centre (8.3, 0.0, 5.9) → a 1.0 m round light at z ∈ [5.4, 6.4], cut
`DIFFERENCE` from the same `head0` block as F3. It leaves 0.70 m of masonry
either side (head0 spans y ∈ [−1.2, 1.2]) and 0.65 m of masonry between the
portal extrados crown (4.75) and the oculus sill (5.40).

**Two saeteras, one per nave side wall.** These answer the "rectangular ashlar
box" half of the conviction directly: today both long elevations are blank
8 × 7.5 m ashlar. Placed over the *intact* west half.

- Opening: x = −4.0, width 0.5, height 1.6, sill 4.2 (z ∈ [4.2, 5.8]).
- Built through the existing `geo.wall_with_openings` mechanism — pass the
  opening in the `openings` list. No new helper.
- **The plaster liner must be pierced to match**, or the hole shows the liner's
  back face. `liner_hi_{sign}` is built with `z0=2.0`, so the matching opening
  is `{"offset": -4.0, "width": 0.5, "height": 1.6, "sill": 2.2}`.
  `liner_lo` (z 0–2.0) is unaffected.
- **No reja, no shutter.** A `make_reja` at this size costs ~300 tris each for
  a 0.5 m slit that is barely resolvable at gameplay distance, and an open
  saetera is correct for a roofless chapel. Premise §5's "every reja intact and
  locked" is a *casa* clause.

### F5 — Collapse legibility

The judge's three named causes, addressed one for one.

**(a) "level coped wall tops" → ragged crown over the collapsed bays.** Root
cause: each side wall is a single 16.6 m box topped at exactly z = 7.5 over
its whole length, so the crown is a perfect level line *even where the vault
tore out*. Split each side wall into three spans:

| span | x range | length | centre x | height | note |
|---|---|---|---|---|---|
| A (intact) | [−8.3, 1.0] | 9.30 | −3.65 | 7.5 | carries the F4 saetera at offset −0.35 |
| B (collapsed) | [1.0, 7.6] | 6.60 | 4.30 | **6.6** | base crown, 0.9 m below the intact line |
| C (east corner) | [7.6, 8.3] | 0.70 | 7.95 | 7.5 | corners survive; buttresses the espadaña wall |

Three `geo.wall_with_openings` calls per side instead of one. The 0.9 m step in
span A's east face is the fracture scar and is meant to be seen.

Then a run of crown blocks on span B, per side (`rng = random.Random(f"crown{sign}")`):

```
cursor = 1.0
while cursor < 7.6:
    step  = rng.uniform(0.35, 0.80)
    u     = (cursor - 1.0) / 6.6
    shape = 0.35 + 0.65 * abs(2*u - 1)          # collapse funnel: deepest mid-span
    h     = rng.uniform(0.10, 0.85) * shape
    if rng.random() > 0.20 and h > 0.06:         # 1 in 5 steps is a notch
        make_box(f"chapel_crown_{sign}_{i}",
                 (cursor + step/2, sign*3.8, 6.6 + h/2 - 0.01),
                 (step - rng.uniform(0.04,0.12), 0.6, h + 0.02),
                 lime, bevel=0.0)
    cursor += step
```

`bevel=0.0` deliberately: a bevelled box at `bevel_segments=2` is ~92 tris
against 12, and at gameplay distance the read is the fracture silhouette, not
the chamfers. The `−0.01` sink and `+0.02` height keep the block bottom inside
the wall rather than exactly coplanar with it. Max crown reach is
`6.6 + 0.85 = 7.45 < 7.5` — the collapsed crown never rises above the intact
crown, which is what makes the contrast read.

**(b) "a clean voussoired cut edge" → staggered fracture.** Root cause: the
vault is a plane cut at x = 0, and the `_lip` ring is 0.5 m long with 0.05 m
of radial jitter on a 3.54 m radius (1.4 % — invisible at 30 m). Replace it
with a lip whose *break line varies per wedge*:

- Extend `geo.barrel_shell` with one optional parameter,
  `extrude_ends: Sequence[float] | None`. When given, wedge `i` uses
  `e1 = extrude_ends[i]` instead of `extrude_range[1]`. That is the minimum
  mechanism for a ragged break and nothing else changes.
- Call: `barrel_shell(f"{name}_lip", 0.0, (0.0, 0.0), springline, half_w,
  CHAPEL_VAULT_RISE, 0.4, lime, n_wedges=18, sweep_axis="y",
  radial_jitter=0.0, seed=3, extrude_ends=ENDS)`.
- `n_wedges` goes 14 → **18** so the lip's wedge boundaries align exactly with
  the vault's 18, and `radial_jitter` goes 0.05 → **0.0** so lip and vault are
  radially identical. The break is now purely in x, which is the read; and with
  jitter gone `_wedge_joint_gaps`' tolerance falls to its 0.005 floor and the
  shared corner at x = 0 satisfies it exactly.
- `ENDS[i] = clamp((0.15 + 1.55 * abs(2*i/17 - 1)) * rng.uniform(0.70, 1.30), 0.10, 2.20)`
  — haunch ribs cantilever up to 2.20 m into the void, crown ribs die within
  ~0.17 m. The crown falls first and the haunches survive: physically right,
  and the spread (≈ 2.0 m) is what the new check in §4 asserts.
- Max reach x = 2.20 ≪ 8.60. Footprint untouched.

**(c) "zero rubble outside" → already covered by dressing, not respecced
here.** `zones.ron:99-100` places two `rock_07` at world (−25.5, −24.1)
scale 5.9 and (−21.6, −34.3) scale 5.0, both outside the collapsed east half,
committed in `44be52d`; `tasks/todo.md:556` assigns this cause to R2 explicitly
("R2 is the cheap layout-side half"). Kit-side interior rubble (7 boxes,
x ∈ [0.4, 3.5]) also stays as built. **Nothing is added for (c).**

### F6 — Ridge cap (caballete), all four casa types · slot `terracotta_tile`

Root cause: `geo.gable_roof` builds two decks meeting at a bare arris; nothing
caps the ridge (named art-level in the G2 re-check, "not charged"). Add a
cover-tile course inside `gable_roof`, after the two slopes:

```
cap_len   = 0.42
n_caps    = max(1, int(ext_length / cap_len))
for i in range(n_caps):
    tx = -ext_length/2 + (i + 0.5) * (ext_length / n_caps)
    make_halfcyl(f"{name}_ridge_{i}",
                 (cx + tx, cy, ridge_z + tile_radius*0.35),
                 tile_radius * 1.15, cap_len * 1.05, tile_material, segments=7)
```

`make_halfcyl` with `rotation=None` runs its length along world X and bulges
along +Z — which is exactly the ridge for `gable_axis="x"`, the only value any
kit type uses. No rotation argument, no new helper. Caps stay inside
`ext_length`, so **no casa AABB moves in XZ**; only the model top rises by
~0.2 m (§5).

---

## 2. Ruled out, with the arithmetic

**No terracotta roof over the chapel's intact vault.** This was the strongest
candidate for the "never roofed" read — a surviving tiled roof is the
counterfactual that makes the fallen half legible as loss, and premise §3 calls
terracotta "every roof". It does not fit, and the reason is geometric:

- The vault extrados crowns at z = **10.5** over a nave 7.0 m wide; the side
  wall tops (the only available eave line) are at z = **7.5**; half the outer
  depth is 4.1 m.
- A 28° roof (the casa gauge) from a 7.5 m eave rises `4.1 · tan 28° = 2.18`
  to a ridge at **9.68** — the vault pokes 0.82 m through it.
- Clearing 10.5 from a 7.5 m eave needs `atan(3.0/4.1)` = **36.2°** minimum,
  ~40° to clear with margin — a pitch that fights the 26–30° casa roofs the G2
  gate scored on cohesion.
- Raising the eave to 8.6 m to buy a 28° pitch means +1.1 m on every chapel
  wall, re-cut liners, and new proportions.
- Laying tiles directly on the extrados is impossible: `theta0` for this vault
  is **81.2°**, so the barrel is near-semicircular and its haunches are
  effectively vertical.

Both escapes change the building's core proportions, which premise §6 fixes
(nave ~7 × 16, vault springing to ~10–12 m, `assert_chapel_dims` enforcing
`vault_peak ∈ [10, 12]`). The premise specifies a **vault-as-roof** chapel;
the collapse read is therefore carried by F5(a)+(b)+(c), which is what the
judge actually named. Recorded here so the question is not re-opened — but it
is a premise reading, so it is escalated as **OPEN-3**.

**No projecting portal order (F3 option B).** A 0.15–0.20 m projecting
archivolt reads better in raking light but pushes the ground-level extent to
x = 8.75–8.80, moving `size` to 20.38–20.43. That is recoverable — shifting
`chapel_door_jamb`'s offset to (8.4, ±2.5) and its half-x to 0.4 grows the
union by the same 0.20, holding the 3.03 shortfall constant — but it churns
`footprints.ron`, `chapter.ron` and a prefab for a shadow line that D9/D10's
open texture-blur findings would swallow anyway. Flush wins.

**No espadaña coping, no impost course, no second tronera.** Rocalba is poor
(premise §1, §10); one bell, one opening, no mouldings.

---

## 3. The two riders

### 3.1 Quoin stranding — root cause and fix

**Root cause (measured, §0):** `_quoins` centres each block on the wall
*centreline* corner `(±w/2, ±d/2)` and sizes it independently of the wall, so
each course protrudes past the render by `bx/2 − 0.225` — a value that swings
between **−0.015 m and +0.146 m** as the long/short alternation flips. On an
exposed corner that is a chunky quoin. On a party junction — where premise §4
requires the neighbour's facade to be flush against this one — there is no
corner to anchor it, so what remains is a stack of blocks jutting irregular
amounts out of a flat wall. Real dressed quoins are *coursed into* the wall:
their outer faces are flush with the two wall planes (a couple of centimetres
proud of the lime render that stops against them), and the alternation shows as
varying face *length*, never varying projection.

**Fix.** `_quoins` takes `wall_thickness` and anchors each block's two outer
faces to the wall outer planes + 0.02 m:

```
sx, sy = math.copysign(1, corner_xy[0]), math.copysign(1, corner_xy[1])
proud  = 0.02
cx_b = corner_xy[0] + sx * (wall_thickness/2 + proud - bx/2)
cy_b = corner_xy[1] + sy * (wall_thickness/2 + proud - by/2)
```

Everything else in `_quoins` is untouched: the per-course size alternation and
the per-block `vordar_uv_offset` are what killed G2 D7/D8 and must survive.
Callers: `build_casa_shell` (has `wall_thickness`) and `build_casa_two_story`
(uses `WALL_THICKNESS`). Blocks now run inward past the wall's inner face into
a sealed, never-entered interior — correct for real quoins and invisible.

The quoin chain stays legible after flushing: G2 measured it at **S 0.049,
V 0.517** against encalado at V 0.542 — the read is chromatic/tonal, not
relief, so removing the projection costs nothing.

### 3.2 Roof albedo mirror-band (N3) — root cause and fix

**Root cause (measured, §0), not inferred.** `geo._roof_deck_panel` assigns
`loop.uv = (co.x / TEXEL_SCALE_M, co.y / TEXEL_SCALE_M)` where `co` is the
**signed** local coordinate of a cube centred on the panel. So UV `(0, 0)` —
the texture tile's own corner, where REPEAT wrapping happens — lands at the
panel's exact centre: **mid-slope in V, mid-length in U**. The shipped
`casa_corner.gltf` confirms it: deck U `[−0.2518, +0.2518]` = `±3.3/13.1072`,
glTF V `[0.8553, 1.1447]` = `1 ∓ 1.897/13.1072`. Both straddle an integer.

Everything the gate reported follows: a wrap seam across the fall line at
mid-slope, mirror-symmetric luminance about that row (corr 0.763 — the
signature of a mirror-tileable source map wrapping at V = 1), reading as a
painted dark band, legible at 30 m and worse at 28 m because the band subtends
more pixels the closer you stand.

**Fix.** Give the deck an origin-corner UV, offset clear of the boundary, and
decorrelate the two slopes so they are not identical twins:

```
u0 = length / 2.0
v0 = run / 2.0
vbias = 0.0 if slope == 'a' else 0.31
loop.uv = ((co.x + u0) / TEXEL_SCALE_M + 0.02,
           (co.y + v0) / TEXEL_SCALE_M + 0.02 + vbias)
```

Resulting Blender spans: U `[0.02, 0.02 + ext_length/13.1072]` — 0.83 max, at
`casa_two_story`'s 10.6 m; V `[0.02, 0.31]` slope a, `[0.33, 0.62]` slope b.
**No integer crossing on any kit type.** Scale divisor unchanged, so VQ-A3's
6.4 mm/texel holds exactly; only a translation is applied.

The U bias must stay 0: a U offset plus a >12.8 m roof would re-cross the
boundary. The new check in §4 enforces this rather than a comment.

---

## 4. Budget and constraint check

### 4.1 Triangle delta

| feature | tris |
|---|---|
| F1 espadaña body (bevelled box, two EXACT cuts) | ~150 |
| F1 gable (`gable_infill`) | 8 |
| F2 bell (12-segment cylinder) + yoke + cross | 80 |
| F3 portal arch, 11 wedges | 132 |
| F3/F4 `head0` re-bore (portal + oculus) | ~90 |
| F4 saeteras + liner openings (12 boxes) | 144 |
| F5(a) crown blocks, 24 × 12 (`bevel=0.0`) | 288 |
| F5(a) side-wall span split, +4 boxes | 48 |
| F5(b) lip 14 → 18 wedges | +48 |
| **chapel total** | **≈ +990** |

**Chapel 1 037 → ≈ 2 025 tris (+95 %).** Proportionate by inspection: the
chapel is the town's one landmark and its one enterable building, and it
currently carries *fewer* triangles than the 4 m `wall_segment` plus
`well_basin` plus `reja_set` combined (1 240). At 2 025 it is still **56 % of
`casa_small_a` (3 616)** and **31 % of `casa_corner` (6 576)**. The anomaly is
the current figure, not the new one.

F6 ridge caps, at 26 tris per cap (`make_halfcyl` segments 7: 7 side quads +
two 8-gon caps):

| type | ext_length(s) | caps | tris | before → after |
|---|---|---|---|---|
| casa_small_a | 6.6 | 15 | 390 | 3 616 → 4 006 |
| casa_small_b | 6.2 | 14 | 364 | 3 728 → 4 092 |
| casa_two_story | 7.6 | 18 | 468 | 5 300 → 5 768 |
| casa_corner | 6.6 + 4.6 | 25 | 650 | 6 576 → **7 226 (+9.9 %)** |

Quoin flush and the deck UV fix are zero-triangle changes.

**No lint caps triangles.** `content_lint.rs` caps model *bytes*
(`MAX_PROP_BYTES` 32 MB; casa_corner ships at 505 KB) and texture memory
(1 GB), neither of which is threatened.

### 4.2 Existing asserts and checks — all still hold

| check | status |
|---|---|
| `assert_chapel_dims` nave_width 7.0 / nave_length 16.0 | unchanged — no wall moves in plan |
| `assert_chapel_dims` vault_peak ∈ [10, 12] | unchanged — `dims["vault_peak"]` is the vault crown 10.5; F1 does not touch it |
| `assert_chapel_dims` door_width 2.4 / door_height 3.2 | unchanged — `CHAPEL_DOOR` still reports the springing |
| `_wedge_joint_gaps` | improves: lip jitter 0.05 → 0.0 drops the tolerance to its 0.005 floor and the shared x = 0 corner meets it exactly; F3's portal ring adds an 11-wedge group with jitter 0 |
| `_radial_normal_faults` | F3's portal ring carries `vordar_arc_*` extras from `barrel_shell` and is covered free; F1/F5(a) are boxes with no extras and are skipped by construction |
| `_open_wall_faces` | every new piece is a closed box, a `gable_infill` prism, or a boolean result; the two boolean cuts are `DIFFERENCE`/`EXACT` on a single solid, the pattern `gate_arch` already ships with 0 faults |
| `_roof_slope_faults` | chapel-exempt (`stem.startswith("casa")`); F6 must not break it — ridge caps are `terracotta_tile` and lie above the deck offset, so they add relief area rather than a new material |
| `check_kit_materials` | chapel binds a 4th family, `iron_wrought`, already registered in `surface_classes.json` |
| `total_texture_memory_within_budget` | `SharedImage::new` hashes image *content*, so the chapel's iron maps dedup against casa_corner's; expect **0 B delta**. The test prints the running total, so a regression is visible |
| `prop_placements_are_registered` / `prop_material_matches_surface_class` | `chapel` is already `kind: "kit"`; no `assets.json` change |
| `material_textures_have_fresh_sidecars` | **will fail until re-baked** — every rebuilt model needs `node scripts/asset-pipeline/bake_textures.mjs gltf <asset>` (§7) |

### 4.3 New checks — one per feature class

A feature with no automatic check is a feature that silently regresses. Five
additions, all CPU, all inside the existing `verify.py` / `assert_chapel_dims`
machinery.

**C1 — `assert_chapel_dims` gains a footprint guard (the important one).**
`build_chapel` returns the built objects' world XZ bounds in `dims`:

```
check("footprint_x", dims["footprint_x"], 20.21, 20.25)   # measured 20.229
check("footprint_y", dims["footprint_y"],  8.18,  8.22)   # measured  8.200
check("espadana_apex", dims["espadana_apex"], 12.30, 12.50)
check("overall_height", dims["overall_height"], 13.05, 13.25)
```

This converts §5's invisible coupling into a hard build-time failure: any
future feature that projects past the east wall or the side walls trips it, and
whoever trips it is forced to consciously update `footprints.ron` and re-check
the 3.05 tolerance. It is the check whose absence made the 0.02 m margin a
hazard in the first place.

**C2 — `_chapel_collapse_faults(mesh_objs)`**, run for `stem == "chapel"`
alongside the existing `startswith("casa")` branch:

- Sample the maximum z of `limestone_dressed` geometry in 0.25 m x-bins along
  each wall line (|y| ∈ [3.4, 4.2]).
- Over the collapsed span x ∈ [1.0, 7.6]: bin max−min must be **≥ 0.50 m**.
- Over the intact span x ∈ [−8.3, 0.0]: bin max−min must be **≤ 0.05 m**
  (the contrast is the read; a ragged intact crown is as wrong as a level
  broken one).
- Lip wedges (objects matching `chapel_lip_wedge\d+`): spread of per-wedge
  world x-max must be **≥ 1.00 m**. The spec's `ENDS` yields ≈ 2.0 m.

**C3 — `_chapel_signature_faults(mesh_objs)`**, same branch — presence checks
that cost four bounding-box reads and prevent a silent loss of the whole point
of this pass:

- `limestone_dressed` geometry exists with z ≥ 11.5 inside x ∈ [7.9, 8.7],
  |y| ≤ 2.0 (espadaña).
- `iron_wrought` is bound, its max z ≥ 12.8 (cross), and it has geometry in
  z ∈ [9.2, 10.1] (bell).
- A wedge group `chapel_portal_wedge*` exists with 11 members carrying
  `vordar_arc_axis` (portal).

**C4 — `slope_uv_seam`, folded into `_roof_slope_faults`.** That function
already clusters faces by plane and already identifies each family's `deck` (the
largest-area cluster). Gather the deck cluster's face UVs and fault when
`floor(min) != floor(max)` in U or V. Parameter-free, and it **fires on today's
geometry** — proof it is a real check and not a tautology. New fault kind
`slope_uv_seam`, new `slope` fields `u_span`, `v_span`.

**C5 — `ridge_bare`, same function.** From the `faces` list it already builds:
the highest `terracotta_tile` face must sit at least `0.075 m`
(`0.5 · tile_radius`) above the highest deck plane offset. Fires on today's
geometry (bare arris), passes after F6.

**C6 — `_quoin_flush_faults(mesh_objs, tol=0.05)`**, run for `casa*` stems.
Collect the `encalado` axis-aligned wall planes (faces whose normal is within
0.05 of ±X or ±Y, grouped by offset). For every object whose name matches
`_quoin_`, each of its four horizontal bbox faces must lie within `tol` of, or
inside, **some** encalado plane with that outward normal. Per-plane rather than
per-model-extreme, so the casa_corner re-entrant corner is covered too. Fires on
today's geometry (0.146 m protrusion vs 0.05 tol).

---

## 5. Downstream impact — stated precisely

**The headline: zero change to `footprints.ron`, zero change to
`chapter.ron`, zero change to any chapter03 prefab's XZ, and all five D5 tests
pass untouched.** This is not luck — it is F1's coplanarity constraint and
F3's flush ruling, chosen for exactly this reason, and now enforced by C1.

### 5.1 The measured footprint does not move

Every feature's extent against the two binding planes (x = 8.60, |y| = 4.10):

| feature | max x | max \|y\| | verdict |
|---|---|---|---|
| F1 espadaña body + gable | 8.60 (coplanar) | 1.80 | inside |
| F2 bell / yoke / cross | 8.60 | 0.86 | inside |
| F3 portal ring | 8.60 (extrude_range (8.0, 8.6)) | 1.55 | inside |
| F4 oculus / saeteras | cuts only — remove material | — | inside |
| F5(a) crown blocks | 7.60 | 4.10 (on the wall line) | inside |
| F5(b) lip, max `ENDS` | 2.20 | 3.94 (r_out at the springing) | inside |

Chapel glTF XZ AABB stays **20.229 × 8.200**. `footprints.ron` `size` stays
`(20.23, 8.2)`, `tolerance` stays `3.05`, the placed union stays **17.20 ×
8.20**, the shortfall stays **3.03 m**, and the margin stays **0.02 m**.

The relation the P2.5 scratch check recorded — `size ≤ model XZ AABB ≤ size +
2·tolerance` — holds unchanged (20.23 ≤ 20.229 ≤ 26.33, to rounding).

Only **height** grows: glTF y-max **10.534 → 13.16** (+2.63 m). No lint reads
model height. `town_solids_within_play_radius` is XZ-only;
`town_prop_collision_matches_footprints` is XZ-only; `town_layout_clearances`
reads *authored* hitbox y, not geometry.

### 5.2 No new collision member

The espadaña's lowest point is local z = 7.5 → **world y = 7.0** (props sit at
y = −0.5). `town_layout_clearances` skips any solid with
`pos.y − half.y ≥ PLAYER_HEIGHT (2.0)`, because `SeparationSystem`'s narrowphase
ignores Y while the broadphase gate does not — an aloft belfry can never
collide with a ground player, and giving it a hitbox would be actively wrong,
not merely redundant. Same reasoning already exempts `gate_head` (y 4.6) and
`chapel_lintel` (y 5.35) / `chapel_roof` (y 10.2).

The portal arch and the oculus **remove** masonry inside `chapel_lintel`'s
span (y 3.2–7.5, aloft, out of the player band). The saeteras remove masonry at
z 4.2–5.8, likewise aloft. The ragged crown removes masonry at z ≥ 6.6, aloft.
**Nothing is added or removed in the [0, 2.0] m player band**, so no hitbox
needs to shrink either.

Clearance lint result: unchanged. Ring (r = 3 at origin) and portal corridor
(x ∈ [0, 22], |z| < 1.5) are 25 m and 24 m from the nearest chapel piece.

### 5.3 Play radius

`town_solids_within_play_radius` worst case is `chapel_wall_apse` at
**r = 50.65** (cap 55). No chapel collision piece moves, so this is unchanged.

### 5.4 Casa side

- **XZ AABBs do not move.** The roof verge/eave overhang already sets or
  exceeds each casa's `size` on both axes, so flushing the quoins cannot lower
  a bound that matters. Derived per type: casa_small_a x becomes
  `max(roof 3.30, wall 3.225, quoin 3.245) = 3.30` → 6.60, exactly `size`;
  z becomes `max(eave tiles 4.389, wall 4.225, quoin 4.245) = 4.389` → 8.778,
  unchanged, because the tiles already governed that axis. casa_corner
  x becomes `[−3.30, 7.457]` = 10.757, inside `size 10.65 + 2·0.1`. casa_small_b
  6.20 = `size`; casa_two_story 7.60 = `size`. **All four still satisfy
  `size ≤ AABB ≤ size + 2·tolerance`. No `footprints.ron` edit, no hitbox
  edit, no D5 impact.** F6's ridge caps sit inside `ext_length` and add nothing
  in XZ.
- **One honest follow-up:** casa prefab y half-extents were authored as
  "measured structure top / 2" (`casa_small_a` 3.13 vs the measured 6.259 top).
  F6 raises each model top by ~0.2 m, so those four values drift from their
  documented convention. No test reads them (the D5 union check is XZ-only;
  the clearance band test only cares that the box overlaps [0, 2.0], which it
  still does). Re-measure and update the four prefabs in §7 step 8 to keep the
  data true — it is a data-honesty step, not a fix.

### 5.5 Observations found while measuring — named, not specced

Per CLAUDE.md §3 these are reported rather than silently changed:

1. **The D5 union check is circular for single-piece types.** For any type
   with no `members` list, "the union of placed hitboxes" *is* its own hitbox,
   and that hitbox was authored from `size` — so the check compares a number to
   itself. It has real force only for the three composites (`casa_corner`,
   `gate_arch`, `chapel`). Nothing in the test suite reads a glTF's extent at
   all; the "measured" provenance in `footprints.ron`'s header is guarded only
   by a one-off P2.5 scratch check. C1 closes this for the chapel; the casas
   remain unguarded.
2. **`chapel_wall_side.ron`'s comment is stale.** It says the shell rises "to
   the 7.5 m springline", but the hitbox is spawn-centred at y = 0 with
   `half.y = 3.75`, so it spans y ∈ [−3.75, +3.75] and tops out at 3.75 m. No
   gameplay effect (players are 2 m); it is a comment-policy "stale claim".
3. **`gate_arch`'s arch is narrower than the opening it spans.** `build_gate_arch`
   passes `half_span = opening_width/2 = 1.6`, and `barrel_shell`'s `r` is the
   *extrados*, so the intrados radius is `1.6 − 0.63 = 0.97` — a 1.94 m clear
   arch over a 3.2 m jamb gap, with the ring's springing points 0.05 m inboard
   of the jamb faces. Same family as F3, one-line fix
   (`half_span = rise = opening_width/2 + thickness`), out of this pass's scope.

### 5.6 Premise amendment recommended (do not edit `docs/town-premise.md`)

§6 describes only structure and dressing; it names no bell gable, cross,
window or portal. Recommended addition to §6, to be applied by the user
alongside the already-pending doors-east / collapse-east / apse-intact
amendment (which this spec does not duplicate and does not contradict):

> - **Espadaña** over the east facade: a single round-arched tronera with one
>   wrought-iron bell, a plain gable, and an iron cross at the apex — the
>   town's tallest thing at ~12.6 m above the plaza. A round-arched dressed
>   portal below it, an oculus between the two, and one saetera per nave side
>   wall. Nothing moulded, nothing carved: Rocalba could afford a bell and a
>   cross, and stopped there.

---

## 6. Phase 3 hero ruling — this section gates RUN-H1

**Ratified D1: Blender-procedural shells; Hi3DGen only for heroes ≤ 5.5 m.**
Per feature:

| feature | kit or hero | why |
|---|---|---|
| Espadaña | **KIT** | It is the east wall continued upward — structure, not an object. 5.6 m of wall above the springing, over D1's 5.5 m cap. A generated mesh would also have to mate exactly with a 0.6 m wall plane along a 3.6 m seam. |
| Bell + cross | **KIT** | 0.52 m and 0.76 m. Two primitives, ~80 tris. A hero chain for these is absurd; and they must bind `iron_wrought` from the shared kit set to sit in the same material family as the rejas and the crucero. |
| Portal surround | **KIT — H1's portal half is CANCELLED** | Three independent reasons, any one sufficient. (a) *Mating*: the ring must be exactly coplanar with a 0.6 m wall and exactly concentric with a 2.4 m opening; Hi3DGen extracts a surface in its own voxel frame with no flat-back or dimensional guarantee, and every mating defect (gap, z-fight, doubled surface) is a G2-class defect that `verify.py`'s open-face and joint-gap checks cannot see across a separate prop. (b) *Cohesion*: a hero ships its own baked atlas, so the portal would be a **different limestone at a different texel density** from the wall it sits in — precisely the asset-internal split that scored G2 Q1 at 3/10. (c) *Nothing to generate*: premise §1 makes Rocalba poor. A poor village chapel's portal is a plain ring of dressed voussoirs — exactly what `barrel_shell` already produces, with radial-normal and joint-gap verification for free. |
| Oculus, saeteras | **KIT** | Boolean cuts and `wall_with_openings` calls. There is no mesh to generate. |
| Ragged crown, fracture lip | **KIT** | Shell geometry; must stay welded to the walls and the vault. |
| Ridge cap | **KIT** | It is the roof. |

**What RUN-H1 should still generate:** the `chapel_arch` re-roll, and only
that. It is `kind: "generated"` at `height_m 5.497` — inside D1's cap by
3 mm — a freestanding ruin fragment at world (−26, −34.5) with **no mating
contract against any shell** and its own atlas by design. That half of H1 is
untouched by this spec and proceeds.

**Consequence for the ~5.5 h budget:** H1 shrinks to one chain. The freed slot
is best spent on the **retablo** (premise §6: dark oak frame, painted panels,
gilt catching candle-gold — "the richest surface in town"). It is the one
chapel element that genuinely needs generation: freestanding, ~3 m, carved and
painted, no mating contract, and it does not exist in `assets.json` or
`zones.ron` today. Whether it already occupies an H2–H7 slot is **OPEN-1**.

**Unblocking C1:** the concept list must depict **no chapel portal, no bell
gable, no cross, no oculus** — those are now kit geometry and a concept for
them would be dead work. C1 may proceed on `chapel_arch` and on the retablo if
OPEN-1 resolves that way.

---

## 7. Step list

1. **Espadaña + bell + cross (F1, F2).** Add to `build_chapel`; reuse
   `geo.gable_infill` for the gable and the `gate_arch` boolean pattern for
   the tronera. → *verify:* rebuild the chapel only
   (`--types chapel`); `build_report.json` shows `iron_wrought` in
   `material_names`, `bad_material_names` empty, `loose_verts/edges` 0,
   `open_wall_faces` empty; scratch-parse the glTF and confirm y-max ∈
   [13.05, 13.25] **and XZ AABB still 20.229 × 8.200 ± 0.02**.
2. **Portal arch + oculus (F3, F4a).** Extend the east wall's `head0` with two
   sequential `DIFFERENCE`/`EXACT` cuts; add the 11-wedge `barrel_shell`. →
   *verify:* `normals_faults` empty and `joint_gaps` all `ok` in the rebuilt
   report, with the group count up from 30 to 41 pairs (18 vault + 11 portal +
   ... recount from the report, not from this line); XZ AABB unchanged.
3. **Saeteras + liner openings (F4b).** Openings passed to the side-wall and
   `liner_hi` calls. → *verify:* rebuilt `mesh_count` rises by 12; a scratch
   ray/section check confirms the liner opening is coincident with the wall
   opening in x and z; `open_wall_faces` still empty.
4. **Collapse read (F5a, F5b).** Split each side wall into spans A/B/C, add
   crown blocks, add `extrude_ends` to `geo.barrel_shell` and rebuild the lip
   at 18 wedges / jitter 0. → *verify:* new check **C2** green; `joint_gaps`
   all `ok` with the lip group's tolerance now at the 0.005 floor.
5. **New chapel checks (C1, C2, C3).** Add `footprint_x/y`, `espadana_apex`,
   `overall_height` to `dims` + `assert_chapel_dims`; add
   `_chapel_collapse_faults` and `_chapel_signature_faults` to `verify.py`
   under an `elif stem == "chapel"` branch beside the existing casa branch. →
   *verify:* run the chapel build with F1–F5 reverted in a scratch copy and
   confirm **every one of C1–C3 fails**; restore and confirm all pass. A check
   that cannot fail is not a check.
6. **Quoin flush (3.1) + check C6.** `_quoins` gains `wall_thickness`; both
   callers updated. → *verify:* rebuild all four casas; scratch-measure
   `limestone_dressed` extent below glTF y = 4.0 against the `encalado` planes
   — expect ≤ +0.02 m (was +0.146); C6 green on the rebuild and red on the
   pre-fix glb.
7. **Deck UV origin (3.2) + ridge cap (F6) + checks C4, C5.** → *verify:*
   C4 and C5 both red on the shipped `casa_corner.gltf` and green on the
   rebuild; scratch-dump the rebuilt deck UVs and confirm U ∈ [0.02, 0.85] and
   V within one tile on all four types; tri counts land within 5 % of §4.1's
   table.
8. **Install + rebake + prefab honesty.** Copy the six rebuilt models into
   `content/models/props/<type>/`, rewrite image URIs to
   `../../townkit_textures/…`, run
   `node scripts/asset-pipeline/bake_textures.mjs gltf <asset>` per model, and
   re-measure the four casa glTF y-maxima to update
   `casa_{small_a,small_b,two_story,corner_{main,wing}}.ron` y half-extents to
   `top/2`. → *verify:* `cargo test -p vordar-game --test content_lint` green —
   in particular `material_textures_have_fresh_sidecars`,
   `total_texture_memory_within_budget` (record the printed MB; expect no
   change), and all five D5 tests, which should pass with **no edit to
   `footprints.ron` or `chapter.ron`**. If either file needs an edit, C1 has
   fired and step 1's constraint was broken — stop and re-derive, do not widen
   the tolerance.
9. **Batch gate.** Per CLAUDE.md §7: one `cargo test --workspace` for the whole
   batch, fix every failure, one confirming run. → *verify:* two suite runs,
   both green on the second.
10. **Offscreen evidence for the Opus judge.** Re-render the P2.4c named shots
    (`ROCALBA_SHOTS` in `zone_review.rs`), at minimum `mid_chapel.png` — the
    frame that convicted — plus a chapel-facade close and a north-row facade
    frame for the quoin and ridge-cap riders. → *verify:* frames exist and each
    named defect is legible in at least one of them; hand to the Opus gate.

---

## OPEN

**OPEN-1 — the freed H1 GPU slot.** §6 cancels H1's chapel-portal half. I
recommend spending the slot on the **retablo** (premise §6; absent from
`assets.json` and `zones.ron`; ~3 m, freestanding, no mating contract — the one
genuinely generation-shaped chapel element). I could not resolve whether it is
already scheduled: the RUN-H2…H7 chain list exists nowhere on disk —
`tasks/todo.md:592` names the range without contents, and neither
`tasks/aa-visual-upgrade-plan.md` nor `docs/` carries it. **Decision needed
before P3.1 authors the C1 concept list.**

**OPEN-2 — premise §6 amendment.** `docs/town-premise.md` is user-owned and
binding; §6 names no espadaña, cross, oculus, portal or saetera. §5.6 proposes
the amendment text. The features themselves are forced by the visual gate
(ground truth), so this is an approval of wording, not of scope — but it is the
user's document.

**OPEN-3 — does the chapel carry terracotta at all?** Premise §3 calls
terracotta "every roof", and the chapel binds none. §2 rules the barrel vault
*is* the roof and shows the arithmetic that makes a tiled roof impossible
without changing premise-fixed proportions (28° needs a 36.2° minimum;
tiles-on-extrados needs a vault that is not 81.2°-swept). My recommendation is
to keep the chapel in stone and treat §3's clause as a casa/roof clause. If the
user reads §3 as binding on the chapel, the chapel's vault geometry has to be
re-derived and this whole spec's §5 conclusion changes — so it is asked, not
assumed.
