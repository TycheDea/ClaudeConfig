# G3 gate record — class `limestone` (asset `shrine_pillar`), 2026-08-05

Judge: fresh Opus judge, Stage B. Visual verdict only.
Gate spec: `.claude/tasks/town/p33-g3-gate.md` §Gate criteria.
Candidates: `cand_203`, `cand_501`. Both v2 open-dark PASS (0.40% / 0.26%).

---

## 1. Blind answers (recorded before any labeled material was opened; unrevised)

Set: `target/prop-g3/blind/limestone/{A,B,C}.png` — 8-angle turntable contact
sheets, 3×3 grid, 8th cell black in all three.

### Which is the photoscan

**B.** Reasons given at the time:

- It is a rock face, not a manufactured object — the other two are the same
  hooded shrine pillar.
- Detail is multi-scale and non-repeating: bedding planes, fracture steps, and
  grain all at different frequencies in one frame.
- Colour events do not follow the geometry — lichen/moss colonies and
  iron-oxide staining sit across relief boundaries rather than tracking them.
- Scan-cut silhouette with an unshot black backface on several angles
  (rows 2–3), the classic photogrammetry crop.
- Crevice darkening is baked-in capture occlusion, present and fixed under
  rotation — expected for a photoscan, not a defect.

### Ranking, photographic surface credibility (1–10)

| sheet | score |
|-------|-------|
| B | **8** |
| A | **4** |
| C | **3** |

A and C are visibly the same mesh at the same 8 angles with different texture.
A carries a granular speckle and higher micro-contrast; C is smoother, slightly
creamier, with a low-frequency diagonal striation on the shaft faces. Neither
shows dressed-stone evidence — no tooled faces, no crisp arrises, no bedding.

### "Shading painted into texture" tells named (against A and C)

1. The candle body carries a painted warm gradient — a yellow/orange smear up
   the wax cylinder and a bloom that reads as flame-light printed into the base
   colour. Identical from all eight angles.
2. The recess back wall is a uniform warm-brown wash with a fixed top-to-bottom
   gradient, constant across angles — reads as painted "the inside is dark and
   warm", not as sooted pale limestone.
3. A fixed dark band under the hood slab that does not move with the light.
4. C additionally: a soft fibrous diagonal "grain" on the shaft that survives
   every angle and reads as brushed/blurred paint rather than stone bedding.
5. A: the granular speckle is uniform in scale everywhere, including on
   surfaces that should be sheltered.
6. In their favour: neither shows a hard painted contact shadow at the base.

Mapping file not opened — blind letters are deliberately not resolved to
candidate ids in this record.

---

## 2. Labeled evidence — what the frames show

Geometry, normal map, roughness and AO are **identical** between the two
candidates (`prop_audit_cand_*.txt`: `island_frac` 0.6327, `world_area_m2`
4.958, `normal_lap_std` 0.06594, `normal_flat_frac` 0.036, `blend_coverage`
0.9759 / `hole_texels` 71956 — same values in both). The candidates differ in
**albedo only**.

Albedo frames verified light-invariant: for both candidates, `studio_albedo`,
`raking_albedo` and `ship_albedo` at `gameplay_01` are pixel-identical
(max per-channel diff 0.0). Anything visible in an albedo frame is therefore
base colour, not a lighting response.

### The `ship_beauty/macro_00` hue outlier (cand_203, h=353.76)

`cand_203/ship_beauty/macro_00.png` is an ordinary shaft frame under the
overcast ship sky. It is near-neutral pale grey-white; `s=0.072` in the same
stats line. There is no magenta, pink, or channel corruption anywhere in the
frame. The 353.76 figure is a circular-mean artifact: at that saturation the
per-pixel hue is numerically unstable and the frame's faint residual tint
straddles the 0°/360° seam, so the mean wraps to just below 360 instead of
landing near the ~35–40 the other frames report. Statistics artifact, not a
visual one.

---

## 3. Per-axis scores

### Axis 1 — subject/material read at gameplay framing

**cand_203 — 5/10.**
Reads unambiguously as a freestanding wayside shrine pillar: square post,
hooded recess, cornice shelf, one lit candle, correct 2.0 m proportion, stable
under all three lightings (`cand_203/studio_beauty/gameplay_00.png`,
`cand_203/ship_beauty/gameplay_01.png`). Against that:

- Material reads as warm cream marble/alabaster, not "pale grey dressed
  limestone". No sandy flecks on any face
  (`cand_203/studio_albedo/macro_00.png` … `macro_03.png`).
- Colour cast a\* 1.440 (`color_cast_cand_203.txt`) sits on the July warm-cast
  baseline (1.436) against a spec calling for cool light grey.
- Under raking the surface is a vertical melted/flowstone relief, closer to
  bark or dripped wax than to a dressed ashlar post — no tooled faces, no crisp
  arrises (`cand_203/raking_beauty/macro_00.png`).
- Hood is a pitched gable with a ridge, not the spec'd flat slab
  (`cand_203/studio_beauty/gameplay_00.png`).
- `roughness_std = 0.000` — one constant 0.85 across stone, wax and recess, so
  the candle wax and the stone respond identically under raking and ship.
- The recess holds a warm-brown painted interior in place of the spec'd thin
  dark-grey soot.
- The flame emits nothing: with the external key removed the recess goes fully
  black (`cand_203/raking_beauty/gameplay_01.png` — same behaviour as 501).

**cand_501 — 5/10.**
Same subject read, same geometry. Better on two counts, worse on one:

- The front shaft face carries a cool grey ground with fine dark flecks that
  matches "cool light grey with faint sandy flecks"
  (`cand_501/studio_albedo/macro_00.png`); cast a\* 0.847 is meaningfully
  closer to neutral than 203.
- The flame reads warm gold at gameplay rather than 203's washed pale white
  (`cand_501/studio_beauty/gameplay_00.png`).
- But the flecked treatment covers only **one of four** shaft faces:
  `cand_501/studio_albedo/macro_01.png`, `macro_02.png` and `macro_03.png`
  revert to 203's cream veined marble. The post reads as two different stones
  depending on which side the player stands
  (`cand_501/ship_beauty/gameplay_01.png` shows the unflecked face).
- Identical gable hood, identical flowstone relief
  (`cand_501/raking_beauty/macro_00.png`), identical flat roughness, identical
  painted recess.

### Axis 2 — no ghost-class shading at 1:1 on albedo

**cand_203 — 2/10. cand_501 — 2/10.**

*Shaft and exterior: clean.* At 1:1 on `cand_203/studio_albedo/macro_00.png`
and `cand_501/studio_albedo/macro_00.png` the shaft albedo holds uniform
luminance edge to edge — no painted contact shadow at the base, no directional
highlight, no darkening into the corners. The pale hairline vein network is
geometry-backed: it appears as raised relief under raking
(`cand_501/raking_beauty/macro_00.png`), so it is surface, not paint.
`baked_fraction_ts` 0.0043 / 0.0039 sits an order below the photoscan
reference's 0.0369.

*Recess interior: ghost-class failure, both candidates.* At 1:1 on
`cand_203/studio_albedo/gameplay_01.png` and
`cand_501/studio_albedo/gameplay_01.png` the recess base colour contains:

- **Four phantom candle flames** with painted wick and wax-top bases — two
  flanking the modelled candle at its own height, two higher on the back wall.
  Only **one** candle exists in geometry.
- **A saturated amber light-glow wash** across the back and right interior
  walls, brightest at the modelled flame's height and falling off toward the
  corners — a light source written into base colour.
- **A phantom horizontal ledge/rail** spanning the recess with no supporting
  geometry.
- **Phantom dark wedge forms** upper-right, and painted arched altar-back
  silhouettes behind the candle.
- **A warm gradient painted onto the modelled candle's own wax body**, gold at
  the base.
- A visible UV seam running vertically through one of the painted flames.

Confirmed as albedo, not lighting: the three lighting arms' albedo frames are
pixel-identical (max diff 0.0). Confirmed as texture, not geometry:
`cand_501/raking_beauty/gameplay_01.png` drops the recess into shadow and only
the one modelled candle catches light and holds form — every phantom flame and
phantom candle body flattens into the dark wall.

Visible at the gate's own distance without magnification: the flanking phantom
flames read plainly in `cand_203/ship_beauty/gameplay_01.png` and
`cand_501/ship_beauty/gameplay_01.png` at native resolution, and the amber
glow reads in `cand_203/studio_beauty/gameplay_00.png` and
`cand_501/studio_beauty/gameplay_00.png`.

Scored 2 rather than 0 in recognition of the genuinely clean shaft, which is
the majority of the prop's visible surface area.

### Axis 3 — no-regression vs comparators

**cand_203 — 4/10. cand_501 — 4/10.**

*Against the interleaved photoscan reference.* At matched macro framing the
reference (`cand_501/studio_beauty/ref_macro_01.png`) shows multi-scale
geological structure with mineral colour independent of relief. Both candidates
show a single-scale vertical flow relief carrying a uniform craquelure albedo
with no weathering logic (`*/raking_beauty/macro_00.png`,
`*/studio_albedo/macro_00.png`). Allowing for material difference — a dressed
limestone post is legitimately smoother than a weathered outcrop — the shaft
is a credible if generic pale stone and does not read catastrophically below
the reference. The recess is far below anything the reference offers: no
photoscan artifact contains painted phantom light sources.
`normal_lap_std` 0.066 against the reference's 0.288 quantifies the micro-relief
gap; `albedo_sat` 0.160 / 0.138 against 0.348 quantifies the colour-variety gap.

*Against the blind band.* Blind placement was 4 and 3 against the shipped
generated band of 2.5–4 — at or just below the band, not above it. The clause
additionally requires no "shading painted in" tell named against the candidate;
**tells were named against both blind candidate letters** (items 1–3 of §1),
and the labeled evidence confirms them as real. The clause fails on its own
terms for both candidates.

---

## 4. Axis 4 — selection

Winner needs ≥7 on axes 1–3.

| candidate | axis 1 | axis 2 | axis 3 | result |
|-----------|--------|--------|--------|--------|
| cand_203 | 5 | 2 | 4 | fail |
| cand_501 | 5 | 2 | 4 | fail |

**Class `limestone` FAILS. No winner.**

**Blocking defect — painted lit-shrine interior in the albedo (ghost-class).**
Both candidates' recess interiors carry, in the base-colour channel, four
phantom candle flames with wax and wick bases, an amber light-glow wash keyed
to the modelled flame's position, a phantom horizontal ledge, phantom dark
forms, and a warm glow painted onto the modelled candle's own wax. None of it
exists in geometry. It is light-invariant and it is legible at gameplay
framing.

Frame citations:
`target/prop-g3/limestone/cand_203/studio_albedo/gameplay_01.png`,
`target/prop-g3/limestone/cand_501/studio_albedo/gameplay_01.png`,
`target/prop-g3/limestone/cand_203/ship_beauty/gameplay_01.png`,
`target/prop-g3/limestone/cand_501/ship_beauty/gameplay_01.png`,
`target/prop-g3/limestone/cand_203/studio_beauty/gameplay_00.png`,
`target/prop-g3/limestone/cand_501/studio_beauty/gameplay_00.png`,
`target/prop-g3/limestone/cand_501/raking_beauty/gameplay_01.png` (the
geometry cross-check).

The defect is shared because the two candidates share one mesh and one interior
texture family; it is a class-level failure, not a candidate-selection problem.

---

## 5. Residuals — reported, non-blocking

- **`ship_beauty/macro_00` hue 353.76 (cand_203)** — circular-mean seam artifact
  at s=0.072. The frame is neutral pale stone with no tint defect.
- **`roughness_std = 0.000` on both** — a single constant 0.85 for stone, wax
  and recess. No material separation in the roughness channel.
- **Hood form** — pitched gable with a ridge on both; the registry spec says
  flat slab hood.
- **Spec'd soot absent** — the recess carries warm brown paint, not thin
  dark-grey soot. (Soot was pre-declared as content, not a defect; what is
  present is not soot.)
- **Warm cast, cand_203** — a\* 1.440 against the July warm-cast baseline
  1.436 and the lightning-adopted neutral −0.03. cand_501 at 0.847 is closer
  but still warm of neutral.
- **cand_501 face inconsistency** — sandy flecks on one shaft face of four;
  the other three are 203's cream marble.
- **Candle is non-emissive** — the recess goes fully black when the external
  key is removed, despite a lit candle being the subject's defining element.
- **Shaft albedo is clean** on both, and the vein network is geometry-backed —
  the ghost problem is confined to the recess interior.
- **Blind-set discriminability caveat** — the control is a rock face and the
  candidates are shrine pillars, so identifying the photoscan required no
  surface judgement. The credibility *ranking* is the informative part of §1;
  the identification is not.

---

## Disposition

Class `limestone` fails G3 on axis 2 (both candidates 2/10) and axis 3 (both
4/10); no candidate installs.
