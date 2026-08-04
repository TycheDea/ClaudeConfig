# Procedural cypress (alpha cards) — T9 visual gate

Date: 2026-08-04. Opus visual judgment of the procedural cypress rebuild that
replaces the Hi3DGen blob at all five start-zone placements. Judged against the
nine T9 criteria of `.claude/plans/peaceful-cuddling-kurzweil.md`. The prior
failure on record is the P2.4 re-judgment's F2 cost note
(`docs/reviews/town/p24-layout-review-2026-07-31.md`): at ×5 the old asset was
"a 9 m wall of half-metre dark shards" with no trunk.

Evidence: `target/review/cypress/` — `MANIFEST.md`, `zone/` (31 `zone_review`
frames), `inspect/` (288 `asset_inspect` frames + 8 index sheets), `stats.txt`,
`concept.png`, `atlas_report.json`.

Numeric claims below were re-derived by this judgment from the shipped pixels and
the shipped `cypress.glb` (scratch scripts), **not** taken from `stats.txt` or the
manifest — see §5, where the shipped `--stats` instrument is shown not to measure
the subject at all.

## Verdict

# FAIL — 1 blocker, 3 required fixes, 3 minor

The rebuild is a large, real success on eight of nine criteria and the named prior
failure is definitively gone: at 2.3 m the foliage reads as fine fern-like needle
spray, not shards, and the tree has a proper basal bole. Silhouette, opacity,
distance survival, grounding and colour all clear their gates with margin, several
of them handsomely.

One thing fails, and it fails at every azimuth and in the in-zone close shot: **the
alpha cards read as rectangles.** Every spray island in the shipped atlas carries
opaque alpha out to at least one of its rect borders, and every card samples its
island corner-to-corner with zero inset — so a card's quad boundary slices a frond
in half, and wherever a card stands proud against sky the cut shows as a hard
straight edge with square corners. Criterion 2 is written precisely to catch this
class, and this is that class. It does not ship.

It is also not a redesign. The mesh, the profile, the normals, the core spindle,
the scale and the colour are all correct and none of them move. The fix is one
constraint in the atlas builder plus a re-crop, and there are 14,336 unused
triangles of budget available to buy the fineness the concept asks for at the same
time.

| # | Criterion | Score | |
|---|---|---|---|
| 1 | Columnar (h/w 4–6) | **9** / 10 | PASS |
| 2 | Fine, not shard-like | **4** / 10 | **FAIL** |
| 3 | No sky holes | **9** / 10 | PASS |
| 4 | Distance survival at 55 m | **9** / 10 | PASS |
| 5 | Colour law | **8** / 10 | PASS (instrument broken) |
| 6 | Trunk = basal bole only | **8** / 10 | PASS |
| 7 | Grounding, all five | **10** / 10 | PASS |
| 8 | Five read as five | **7** / 10 | PASS |
| 9 | Concept fidelity | **6** / 10 | PARTIAL |

---

## 1. Columnar — 9/10, PASS

**Geometry of record.** `cypress.glb` POSITION accessor: min `(-0.968, 0, -0.997)`,
max `(0.975, 9.001, 0.986)` → h 9.001 m, footprint 1.943 × 1.983 m.
**h/w = 4.54** (max axis) / 4.58 (mean axis). Inside the 4–6 band.

**Rendered silhouette, level camera.** The `far` arm aims eye and target both at
y = 1.60 (`asset_inspect.rs:346-360`, `EYE_HEIGHT` 1.6, `FAR_DISTANCE` 55.0), so
`far` is the only undistorted vertical read in the set. Measured bbox h/w over the
six azimuths of `ship_beauty/far_*.png`: **4.62, 4.71, 4.97, 5.11, 5.85** (az 05
excluded from the dark-threshold pass — backlit; visually identical proportion in
the zoom montage). Every value in band.

**The `full` frames disagree, and they are the ones lying.** `ship_albedo/full_*`
measures h/w 3.17–3.43. That is entirely the turntable camera's pitch:
`set_camera_turntable` → `Camera::new` pitch = **0.8 rad = 45.8°**
(`camera.rs:54`), and 4.54 × cos(0.8) = **3.17** — the measurement to two decimals.
A 46°-down view foreshortens a vertical rod and cannot be used for this criterion.
No asset defect here; recorded so the next round does not chase it.

Reading, not just ratio: `wide.png` shows all five as slim dark exclamation marks
bracketing the settlement under fog, which is exactly the premise beat P2.4 §4 asked
for and the old asset could not deliver.

## 2. Fine, not shard-like — 4/10, **FAIL**

**The prior failure is gone.** `zone/close_cypress.png` (2.3 m, player beside the
tree) and all six `ship_beauty/gameplay_*.png` show fine, fern-like, multiply
branched needle spray. Nothing in any frame reads as a half-metre plate. There is no
X / cross-plane read at any azimuth — the single-quad architecture (D2) did its job
and the crossed-quad rejection was right.

**But readable rectangle edges are present at all six azimuths and in the in-zone
close shot.** In `ship_beauty/gameplay_00.png` the left fringe card is cut by a hard
vertical line at x ≈ 137 running y ≈ 60→330 with square corners top and bottom; the
right fringe card is cut at x ≈ 820, y ≈ 370→560. `close_cypress.png` shows the same
thing larger: a straight vertical at x ≈ 1080 from y ≈ 70 to y ≈ 370 with a
horizontal step, and a second at x ≈ 1040, y ≈ 390→600. A 2× brightened montage of
the sky-backed upper canopy at all six azimuths shows the outer silhouette as a
staircase of straight-sided rectangles at every one of them. The `normal` and `ao`
channels render the same rectangles as clean geometric blocks, which confirms they
are card boundaries and not a shading artifact.

**Root cause, measured on the shipped atlas.** Fraction of each spray island's
border texels with alpha above the shipped `alphaCutoff` 0.35:

| island | top | bottom | left | right |
|---|---|---|---|---|
| spray_top_left_rot90 | **0.731** | 0.000 | 0.000 | **0.617** |
| spray_top_left | 0.000 | **0.617** | 0.000 | **0.731** |
| spray_top_right | 0.000 | **0.392** | **0.734** | 0.000 |
| spray_bottom_left | **0.623** | 0.008 | 0.000 | **0.483** |
| spray_bottom_right | **0.383** | 0.000 | **0.497** | 0.000 |
| **spray_center** | **0.662** | **0.412** | **0.558** | **0.438** |
| **spray_center_rot180** | **0.412** | **0.662** | **0.438** | **0.558** |
| spray_dry_bottom_right | **0.383** | 0.000 | **0.497** | 0.000 |
| spray_dry_top_right | 0.000 | **0.392** | **0.734** | 0.000 |

Every island is opaque on at least two borders. `spray_center` and its rot180 are
opaque on **all four** — any card carrying them is a fully framed rectangle, and
they are the two highest-coverage islands in the atlas (0.631 vs 0.205–0.385), i.e.
the ones most likely to be picked for canopy fill.

And the cards sample the whole rect. UV pixel extents against every declared island
rect: **inset = (0, 0, 0, 0) px on all four sides, for all eleven islands.** So the
quad edge lands exactly on the island border, where the frond is opaque, and cuts it.

The islands are quadrant crops of a larger scan (`spray_top_left`,
`spray_bottom_right`, …), so fronds are severed at the crop boundary by
construction. This was inevitable from D7's packing step and no assert in
`atlas.py` looks at it — `atlas_report.json`'s five red-proof fixtures cover
saturation, normal tilt, sparse alpha, constant AO and the mip ladder, none of them
border alpha.

Score 4 rather than lower because the needle register itself is genuinely good and
the failure is a border condition on an otherwise correct texture, not a wrong
architecture.

## 3. No sky holes — 9/10, PASS

Measured on `ship_normal/*` where the sky background is pure black, so an enclosed
background pixel inside the filled silhouette is unambiguously a hole:

| distance | silhouette px | enclosed holes | interior holes (>3 px in) |
|---|---|---|---|
| far (6 az) | ~3 530–3 580 | 0–8 px (**0.00–0.23 %**) | **0 px (0.00 %)** |
| gameplay (6 az) | 288 909–324 880 | 1 755–4 247 px (**0.57–1.31 %**) | 0.58–1.35 % |

Zero interior holes at 55 m; sub-1.4 % pinholes at 2.3 m, which is what a real tree
does. The solid core spindle is doing exactly the job D2 assigned it. Confirmed
visually in `wide.png`, both pair mids and `mid_graveyard.png` — the canopy is an
unbroken mass at every framing.

## 4. Distance survival at 55 m — 9/10, PASS

`ship_beauty/far_*.png`, zoomed 3× (all six azimuths): a coherent dark columnar mass
with a ragged edge and a small pale bole at the base. Not lacy, not transparent, no
dissolve. Bbox fill inside the silhouette is 0.72–0.77 across azimuths 01–04 — an
ellipse fills 0.785 of its bbox, so the mass is essentially solid. Azimuths 00 and
05 are sun-backlit and fog-bloomed, and still read as a solid spire.

The atlas mip ladder is `[1.026, 1.059, 1.129, 1.241]` (mip 1→4 vs mip 0), i.e.
coverage *rises* through the chain rather than thinning; the D6 gate needed ≥ 0.55.
**The frames agree with the ladder** — if anything the far read is slightly heavier
and smoother-edged than mip 0, which is the opposite of the failure mode D6 was
written against. **The deferred Castaño per-mip rescale in `bake_textures.mjs` is
not triggered and stays deferred.**

## 5. Colour law — 8/10, PASS on all three ceilings — **but the shipped instrument
does not measure the tree**

### The instrument

`print_stats` (`asset_inspect.rs:443-465`) skips a pixel only when it is *exactly
equal* to pixel (0,0). Against `ship` lighting that background is a rendered cloudy
sky over a textured ground, so almost no pixel matches. The proof is in the numbers
the manifest publishes: `px=1048438`, `px=1048508`, `px=1048564` … against a
1024² = **1 048 576** px frame. The reported h/s/v are whole-frame means dominated
by sky and ground.

Concretely: the manifest's headline "gameplay: h≈203° s≈0.072 v≈0.433" is the
**sky's** blue and the ground's brightness. Had the tree been threat-band red, a
203° frame mean would still have cleared the "hue outside 350°–25°" gate. The T7
red-proofs (`S ≥ 0.7` fixture, zeroed-alpha atlas) both exercise a flat background
and cannot detect this. **The number the plan built to make the colour ceiling
judgeable is not measuring the subject.** Required fix F1.

### The tree's actual colour, re-measured here

Subject pixels only (background-difference mask on the flat-background `full`
frames; V < 0.50 mask on `gameplay`), 6 azimuths each, circular hue mean weighted
by saturation:

| measurement | hue | S | V |
|---|---|---|---|
| `ship_albedo` full (map as shipped) | **55.2°** | **0.283** | **0.198** |
| `ship_beauty` gameplay (rendered) | **66.8°** | **0.099** | **0.125** |
| `ship_beauty` full (rendered) | 97.6° | 0.067 | 0.161 |
| atlas spray texels above cutoff | 52.7° | 0.309 | 0.191 |
| **`concept.png` tree pixels** | **52.7°** | **0.331** | **0.194** |

- **S ≤ 0.35** — PASS with wide margin (0.099 rendered, 0.283 albedo).
- **V ≤ 0.6** — PASS with wide margin (0.125 at gameplay).
- **hue outside 350°–25°** — PASS (66.8° rendered, 55.2° albedo; olive, per the law).

### What the fog does to the far numbers

Nothing to the tree's own colour that this judgment needed to correct for, because
the far numbers in `stats.txt` are frame means and never described the tree. The
real far-frame fog effect, read off the zoom montage rather than a statistic, is a
value lift and a contrast crush: the 55 m silhouette sits only ~0.05–0.10 V below
the fog behind it, and at azimuths 00/05 the sun bloom washes the upper canopy to
near the background value. That is the authored zone fog doing its job (P2.4 already
recorded density 0.0055 erasing the town) and it is not a colour-law event.

Held at 8, not 10, for one honest observation: the rendered tree is much darker and
flatter than both its own albedo and the concept (V 0.125 vs 0.194, S 0.099 vs
0.331). At mid distance in `mid_cypress_nw/se.png` it reads as a near-black cutout
against pale ground rather than the dark-olive mass of the concept. Every stated
ceiling is respected — this is a lighting-response note, not a violation, and it is
recorded as a watch item, not a fix.

## 6. Trunk — 8/10, PASS

Base zoom across three azimuths of `ship_beauty/full_*.png`: a small bole at the
very base and nothing else. No bare trunk through mid-canopy at any azimuth, at any
of the three distances; the canopy skirt closes over it completely. The far frames
show the same stub at 55 m. This is the second half of the P2.4 F2 complaint ("and
there is no trunk") and it is answered.

Deduction: the bole renders **pale cream-tan and is the brightest thing on the
tree** — at 55 m it is a light pip under a near-black column, and the criterion asks
for a *dark* bole. Minor fix M1.

## 7. Grounding — 10/10, PASS

All five placements make visible base contact with a contact shadow, no float and
no sink:

- NW pair (−48, 42) s 1.00 and (−42, 48) s 0.85 — `mid_cypress_nw.png`, both boles
  meeting the ground with their own shadow.
- SE pair (30, −52) s 1.10 and (36, −46) s 0.90 — `mid_cypress_se.png`, same.
- Graveyard (−34, −40) s 0.95 — `mid_graveyard.png`, planted beside the chapel at
  credible height against the building, and `wide.png` shows it with its shadow.
- `wide.png` carries all five simultaneously, each with a ground shadow at its base.

## 8. Variety — 7/10, PASS

Four trees across the two pair mids read as four: the scale spread (0.85–1.10) is
legible between neighbours in both frames, and free yaw gives each a different
fringe-bump pattern along its silhouette. The fifth reads independently against the
chapel.

Held at 7 because the *envelope* is identical at all five — same profile, same
taper, same blunt-rounded crown. Scale and yaw are the only differentiators, and at
wide framing (`wide.png`) the four field cypresses are visually interchangeable.
Acceptable for a formal planted row, which is what the premise asks for; worth a
profile-jitter parameter if these ever appear in a naturalistic grouping.

## 9. Concept fidelity — 6/10, PARTIAL

Side-by-side at matched tree width (concept upper canopy vs `ship_beauty/full_02`
upper canopy, both normalised to 500 px of tree width):

**Colour — excellent, effectively exact.** Atlas spray mean 52.7° / 0.309 / 0.191
against concept tree pixels 52.7° / 0.331 / 0.194; the report's own masked-Lab ΔE is
3.54. The regrade (D7) is the best-executed part of this asset.

**Silhouette character — matches.** Columnar with proud fringe sprigs breaking the
envelope, ragged crown, foliage carried nearly to the ground. The concept's read.

**Needle-spray fineness register — does not match.** At matched tree width the
render's fringe units span roughly **twice** the concept's sprig scale, and the
silhouette edge is blocky and stepped where the concept's is finely serrated. The
concept's edge is made of many small sprigs; the render's is made of fewer large
fronds whose card corners are visible (criterion 2). Two contributing facts:

- The atlas declares 9 spray islands but carries only **5 unique alpha cutouts** —
  `spray_top_left` is `spray_top_left_rot90` rotated, `spray_center_rot180` is
  `spray_center` rotated, and both `spray_dry_*` islands are **byte-identical** in
  alpha to `spray_bottom_right` / `spray_top_right` (recolours, not new shapes).
  D7 asked for 6–10 spray islands; the alpha variety actually shipped is 5, spread
  over 1050 cards.
- The mesh is **9 664 tris against a 24 000 budget** — 14 336 triangles unspent. D2
  is explicit that headroom is spent on card COUNT, never card size. It was not
  spent.

---

## Fix list

**Blocker — 1. Nothing ships until this clears.**

- **B1 — no card may cut an opaque frond.** Guarantee alpha ≤ `alphaCutoff` (0.35)
  in a margin band inside every spray island's rect, so the quad boundary always
  lands in transparent texels. Two ways, and the first is the honest one:
  1. Re-crop the spray islands from the source scan so each island is a *whole*
     spray with clear space around it, instead of a quadrant of a larger image
     (`spray_top_left`, `spray_bottom_right`, … are crop coordinates, and that is
     the defect's origin). This also raises the 5 unique cutouts toward D7's 6–10.
  2. Failing that, feather each island's outer 8–16 px to zero alpha before packing
     — cheaper, but it eats the frond tips and will read as a soft rectangle rather
     than a hard one.

  Then **add the numeric assert to `cypressgen/atlas.py`** that would have caught
  it: for every spray island, the fraction of border-row and border-column texels
  above `alphaCutoff` must be ≈ 0 (the shipped atlas scores 0.383–0.734 on at least
  two borders of every island, and 0.412–0.662 on all four of `spray_center`).
  Red-proof it with an un-inset island, per the T1 pattern.

  Optionally also inset card UVs 2–4 px inside the rect — but that is belt-and-braces
  and does not substitute for the assert; UV inset is currently (0,0,0,0) px on all
  eleven islands.

  Verify on re-render: the 2× brightened sky-backed upper canopy at all six
  `gameplay` azimuths, plus `close_cypress.png`. No straight run with square corners
  on any card boundary.

**Required — 3. These ride the same rebuild round as B1.**

- **F1 — fix `print_stats` so it measures the subject.** `asset_inspect.rs:443-465`
  excludes only pixels exactly equal to pixel (0,0), which against a rendered sky
  excludes essentially nothing — every `ship` line in `stats.txt` counts ~1 048 500
  of 1 048 576 px. The published colour numbers are sky means. Mask the subject
  properly (alpha/stencil from the render, or the flat-background channels), and
  red-proof it with a fixture whose *background* is threat-band red and whose subject
  is not: the current red-proofs cannot fail this way. Until this lands, the colour
  criterion cannot be gated from `stats.txt` — this round's §5 numbers were
  re-derived by hand and that must not be the standing arrangement.
- **F2 — spend the triangle headroom on card count, not card size.** 9 664 / 24 000
  tris used. Raise the card count and reduce per-card world size so the fringe unit
  scale halves toward the concept's sprig register (criterion 9). D2 already names
  this as the sanctioned use of the headroom, and it directly improves the ragged-edge
  read that B1's re-crop also touches — do them together and re-judge once.
- **F3 — darken the trunk bole.** It currently renders pale cream-tan and is the
  brightest element on the tree at every distance, including 55 m where it is a light
  pip under a near-black column. Criterion 6 asks for a *dark* bole; regrade the bark
  island toward the canopy's value range.

**Minor — 3**

- **M1 — magenta filaments.** Thin pink/violet lines are visible through the canopy
  in both beauty and albedo at gameplay framing (`sbs` crop of
  `ship_beauty/full_02`). Only 0.26 % of opaque spray texels sit in hue [260, 350),
  but against a V≈0.125 canopy they read. Likely the −38.8° global hue rotation in
  the regrade dragging reddish stem texels past red into magenta. Clamp or mask the
  stem hues.
- **M2 — 7.65 % of opaque spray texels land in the forbidden 350°–25° band** (the
  dry-brown variants). The law gates the *mean*, and the mean is 52.7°, so this is
  not a violation — recorded because a future tightening of the law to a percentile
  would trip on it.
- **M3 — profile jitter.** All five placements share one envelope; only scale and yaw
  distinguish them (criterion 8). A per-instance profile seed would matter if these
  ever appear outside a formal planted row.

## Regression spot-check — clean

`zone/contact_sheet.png` plus `mid_plaza.png` opened directly: the plaza well and
paving, the chapel exterior and both interiors, all four casa types, gate arch,
wall segment, crucero, gravestone, broken column, candelabra shrine, olive stump and
all three rock props render normally — no black frames, no missing textures, no
changed framing, nothing disturbed. `mid_graveyard.png` shows the chapel, the three
jittered markers and the arch exactly as the P2.4 re-judgment left them. The cypress
change touched nothing else, as planned (`Not touched: renderer, bake_textures.mjs,
townkit/, footprints.ron`).

## Non-gating observations from the debug channels

- **Normals are correct and are the quiet win.** `ship_normal/gameplay_00.png` shows
  a smooth radial gradient across the whole canopy (blue-violet on the left face,
  salmon through the centre, yellow-green on the right) that is continuous *across*
  card boundaries — no per-card flat facets. The D2 decision to author canopy-surface
  normals (radial + 0.3·up) instead of card normals is vindicated, and it is why
  `raking_beauty/full_01.png` shows a clean vertical terminator with no card banding
  on a 1050-card mesh.
- **AO is clean.** `ship_ao/gameplay_00.png` is mostly white with soft grey
  variation, no flat read and no ringing; report gate mean 0.919, std 0.112. The
  synthesized edge-distance AO (D7, no Cycles) was sufficient.
- Both channels render the B1 rectangles as sharp geometric blocks, which is what
  confirmed the defect is geometry/UV rather than shading.
- **Shadows are correct through the alpha mask** — the cast shadow in
  `raking_beauty/full_01.png` and both pair mids is a tapered tree shape, not a
  quad blob. The `12c7e4b` renderer prerequisite (MASK respected in
  shadow/depth-prepass/SSAO) is working on the shipped asset.

## Watch items carried

- **The rendered tree is much darker and flatter than its albedo** (V 0.125 vs
  0.198; S 0.099 vs 0.283). At mid distance it reads as a black cutout rather than
  the concept's dark olive. Inside every stated ceiling, so not a fix — but if the
  zone ever wants the cypresses to read as *foliage* rather than *silhouette* at
  30–50 m, this is the number that has to move, and it is a lighting/exposure
  question, not an asset one.
- **The mip ladder rises rather than falls** (1.026 → 1.241). Safe here, and the
  reason criterion 4 passes so cleanly, but it means the 55 m read is slightly
  heavier and smoother-edged than the near read. If B1's re-crop and F2's smaller
  cards shrink the alpha features, re-check the ladder — smaller features are what
  makes box mips thin, and the D6 gate is the tripwire.
- **`asset_inspect`'s `full` arm is a 45.8°-pitch turntable** and cannot be used to
  judge any vertical-proportion criterion. Recorded so the next judgment does not
  repeat the reconciliation done in §1.
- **`zone_review` still has no authored per-cypress-pair shot.** `mid_cypress_nw.png`
  and `mid_cypress_se.png` exist only because T8 temporarily added two `NamedShot`
  entries to `ROCALBA_SHOTS` and reverted them (`MANIFEST.md` §1). Criteria 7 and 8
  lean on those two frames and they are not reproducible from a clean checkout.
  P2.4's F7 raised the same shot-coverage gap; it is still open.
- `target/review/cypress/zone_pairs/` is leftover duplicate output from that
  temporary run — target/ trash, superseded by `zone/`.
