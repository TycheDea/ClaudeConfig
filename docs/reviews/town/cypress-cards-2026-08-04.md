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

*Superseded for the shipped asset by **Round 3 — 2026-08-05** (below): B1 dead,
B2 dead, F4 verified. Round 3 verdict: PASS, minors only.*

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

---

# Round 2 — 2026-08-05 (fresh judge)

Subject: the rebuilt procedural cypress promoted 2026-08-05 (`1a5bf6c`),
`content/models/props/cypress/cypress.glb`, 2500 cards / 21 264 tris.
Evidence: `target/review/cypress-r2/` (32 zone frames, 288 `asset_inspect`
frames, 72 subject-masked `STATS` lines). Round 1's stale set
(`target/review/cypress/`) was re-measured alongside for every diff below.

Every number here was re-derived from the shipped pixels, the shipped
`cypress.glb` accessors and the shipped `target/cypress-build/atlas/`, by this
judgment. Nothing is taken from `MANIFEST.md`'s prose.

## Verdict

*Superseded for the shipped asset by **Round 3 — 2026-08-05** (below): B2 dead,
F4 verified. Round 3 verdict: PASS, minors only.*

# FAIL — 1 blocker, 1 required fix, 2 minor

**B1 is dead.** Not healed-with-residue — dead. The rebuild closed it at the
root (organic-matted islands, border alpha 0.000 on all nine sprays, a
red-proofed gate) and the pixels agree at every azimuth and every distance.
Seven of nine criteria pass, five of them better than round 1, and all three
round-1 required fixes plus both colour minors verify in pixels.

One new thing fails, and it fails on all five placements at every distance from
30 m in: **the core spindle is exposed at the crown as a bare, smooth,
untextured cone.** That is the same class round 1 blocked — a hard-edged
geometry read on a foliage silhouette — relocated from the card boundaries to
the apex. It does not ship.

| # | Criterion | R1 | R2 | |
|---|---|---|---|---|
| 1 | Columnar (h/w 4–6) | 9 | **9** / 10 | PASS |
| 2 | Fine, not shard-like | 4 | **8** / 10 | PASS |
| 3 | No sky holes | 9 | **9** / 10 | PASS |
| 4 | Distance survival at 55 m | 9 | **9** / 10 | PASS |
| 5 | Colour law | 8 | **9** / 10 | PASS (instrument now honest) |
| 6 | Trunk = basal bole only | 8 | **4** / 10 | **FAIL** |
| 7 | Grounding, all five | 10 | **10** / 10 | PASS |
| 8 | Five read as five | 7 | **6** / 10 | PASS |
| 9 | Concept fidelity | 6 | **6** / 10 | PARTIAL |

---

## B1 recheck — **DEAD**

Read at close range and at gameplay distance, all six azimuths, three channels.

- `zone/close_cypress.png` (2.3 m, player beside the tree). Round 1 named two
  specific defects here: a straight vertical at x ≈ 1080 running y ≈ 70→370
  with a horizontal step, and a second at x ≈ 1040, y ≈ 390→600. Both regions
  re-cropped at 2.4× brightness and 2× zoom: the R1 frame shows the two
  straight verticals with square corners exactly as recorded; the R2 frame has
  no straight run and no square corner anywhere on either flank. The silhouette
  is organic top to bottom.
- `inspect/ship_beauty/gameplay_00..05.png`, 2.6×-brightened sky-backed upper
  canopy montage, all six azimuths. Round 1's "staircase of straight-sided
  rectangles at every one of them" is gone; every azimuth shows individually
  shaped sprigs. The R1 montage rendered from the same crop still shows the
  staircase, so the difference is the asset, not the montage recipe.
- `inspect/ship_normal/gameplay_00.png` and `gameplay_03.png` — the channel that
  round 1 used to prove the rectangles were geometry. Continuous radial normal
  gradient across card boundaries, zero flat facets, zero geometric blocks.
- Longest straight vertical run on the left/right silhouette boundary in the
  sky band of `ship_normal/gameplay_*`: R1 9–40 px, R2 8–19 px.

Root cause closed at the atlas, not papered over: `atlas_report.json`
`border_alpha_gate` = **0.000 on all nine spray islands** (round 1: 0.383–0.734
on at least two borders of every island, 0.412–0.662 on all four of
`spray_center`), and `red_proofs.island_border_alpha` shows the gate failing an
un-inset probe at 0.483 — the assert round 1 asked for exists and is red-proofed.
The islands are no longer quadrant crops: nine independent window picks, each
multiplied by an `organic_vignette` that reaches literal zero alpha inside the
crop's own edge.

## Fix verification

**F1 — stats measure the subject. DONE, one residual.**
Round 1's `ship` lines counted ~1 048 500 of 1 048 576 px. Round 2's count
5 432–5 699 px at `far` and 474k–556k at `gameplay`. Sanity-checked against my
own masks (subject isolated from `ship_normal`, background classes sampled from
the frame corners):

| stats line | stats.txt | this judgment, independent mask |
|---|---|---|
| `ship_beauty/far_01` | h 215.47 s 0.085 v 0.404 px 5650 | h 216.9 s 0.071 v 0.415 px 5380 |
| `ship_beauty/gameplay_01` | h 59.13 s 0.115 v 0.197 px 548 977 | h 56.7 s 0.119 v 0.136 px 482 102 |

Hue agrees to ≤ 3°, saturation to ≤ 0.005. The instrument measures the tree.
Residual: the shipped mask runs ~14 % wider than a hard silhouette at
`gameplay` and the extra pixels are partially-covered edges carrying mostly
background, which lifts reported V by ≈ 0.06 (0.197 vs 0.136). Harmless against
a 0.6 ceiling; recorded as minor M4, not a blocker.

**F2 — headroom spent on card count. PARTIAL.**
1050 → 2500 cards, 9 664 → 21 264 tris against the 24 000 budget; per-card
length ×0.625. The *silhouette* did get finer — perimeter/area over the
sky-backed gameplay silhouette rises from 0.0178 to 0.0193 mean, enclosed holes
fall (below), detached fringe islands rise from 5–12 to 13–32 per frame. But
two things went the wrong way and both are visible:

- The *internal* needle register got coarser, not finer. At matched screen
  scale (`ship_beauty/gameplay_02`, identical crop, 3.2× brightness) R1's
  fronds resolve into pinnate fern branching; R2's are fat smooth-lobed
  branchlets with no serration. The cause is in the shipped atlas, not the
  render: all nine spray islands are 5–10 thick coral-like lobes (montage of
  every island from `cypress_base.png`). The window search picked a
  magnification at which individual branchlets fill the 384 px island.
- Crown card density is too low to cover the core (see B2).

**F3 — trunk bole darkened. DONE.**
`atlas_report.json.bark_regrade` pre H 42.745 S 0.4296 V 0.5407 — round 1's
measured pale cream to three decimals — regraded to H 30 / S 0.28 / V 0.20.
Re-measured on the shipped `cypress_base.png` bark island: **H 29.9, S 0.275,
V 0.200**. In pixels, `ship_beauty/full_01` base zoom: R1's bole is bright
cream-tan and the brightest element on the tree; R2's is a dark warm brown,
darker than the canopy skirt around it. No longer a light pip at 55 m.

**M1 — magenta filaments. DONE.** Subject-masked over 6 azimuths at gameplay,
2.88 M px: fraction in hue [260, 350) in `ship_albedo` is **0.000 %** at every
saturation threshold (R1: 0.116–0.165 %). In `ship_beauty` at S > 0.15,
0.481 % → **0.007 %**. The lavender sprigs still visible in a 3× brightened
crop are low-saturation blue-grey sky rim light, not asset magenta.

**M2 — threat-band texels. DONE.** `color_minor_fixes.threat_band_pct`
0.0556 → **0.0** on opaque spray texels. Rendered subject-masked albedo in
[350, 25) falls 7.44 % → 3.75 %, the remainder being the bark island (H 30)
and edge AA.

**M3 — profile jitter. OPEN, and now more visible.** See criterion 8.

---

## 1. Columnar — 9/10, PASS

`far` arm only (the `full` arm is a 45.8° turntable and still cannot judge
vertical proportion — it measures h/w 3.1–3.4 on the same asset). Silhouette
bbox over `ship_normal/far_*`, azimuths 01/02/04/05 (00 and 03 excluded: the
cast shadow merges with the tree in those two): **h/w = 4.55, 4.55, 4.41,
4.53.** GLB POSITION accessor: height 9.000 m, max radius 0.9517 m →
**h/w 4.73**. Every value in the 4–6 band, and slightly slimmer than round 1's
4.11–4.23. `wide.png` still reads as slim dark exclamation marks bracketing the
settlement.

## 2. Fine, not shard-like — 8/10, PASS

No plate, no shard, no cross-plane read, no card rectangle at any azimuth or
distance — see the B1 section. At shipped exposure `close_cypress.png` reads as
a dense dark columnar tree with a finely serrated edge and legible individual
sprigs.

Held at 8, not 9–10, for the register loss recorded under F2: the shipped
island alpha carries no needle serration, so under inspection the foliage unit
reads as a small fat lobed leaf rather than a needle spray. Not shard-like — but
not the fern-like spray round 1 praised either. The bare crown cone is a
hard-edged geometric read on this silhouette and is scored under criterion 6
rather than double-counted here.

## 3. No sky holes — 9/10, PASS

Enclosed background inside the filled silhouette, `ship_normal`, 6 azimuths:

| | gameplay, enclosed | gameplay, >4 px in |
|---|---|---|
| R1 | 0.81–1.93 % | 0.77–1.86 % |
| **R2** | **0.69–1.09 %** | **0.65–1.05 %** |

Improved over round 1 despite 2.4× the card count. At `far`, per-row coverage
inside the silhouette span is 0.986–0.989 and bbox fill 0.726–0.743 — no
enclosed hole survives at 55 m. Confirmed visually in `wide.png`, both pair mids
and `mid_graveyard.png`.

## 4. Distance survival at 55 m — 9/10, PASS. Mip watch item resolved.

`ship_beauty/far_01/02/04` at 4× zoom: a coherent dark columnar mass with a
ragged edge, no lacing, no dissolve, no transparency. Subject pixels 5 381 vs
round 1's 5 979 — 10 % fewer, from a genuinely slimmer tree (silhouette width
40 px vs 43), not from thinning.

**The round-1 watch item is answered.** The new atlas's mip coverage ladder is
`[1.009, 1.021, 1.056, 1.109]` — still *rising*, still far above the D6 gate of
0.55, and flatter than round 1's `[1.026, 1.059, 1.129, 1.241]`. Smaller cards
did **not** thin the chain. The Castaño per-mip rescale in `bake_textures.mjs`
stays deferred.

## 5. Colour law — 9/10, PASS on all three ceilings, instrument now honest

Subject-masked, 6 azimuths, gameplay, `ship`, 2.88 M px:

| | hue (sat-weighted circular mean) | S | V |
|---|---|---|---|
| `ship_beauty` | **58.8°** | **0.101** | **0.133** |
| `ship_albedo` | **52.5°** | **0.281** | **0.201** |
| concept tree pixels (round 1) | 52.7° | 0.331 | 0.194 |

- **S ≤ 0.35** — PASS (0.101 rendered, 0.281 albedo).
- **V ≤ 0.6** — PASS (0.133 rendered, 0.201 albedo).
- **hue outside 350°–25°** — PASS (58.8° rendered, 52.5° albedo).

Raised from 8 to 9 because the gate is now gateable from `stats.txt` (F1) and
both colour minors closed. Not 10 for the residual mask bias (M4) and the
far-distance caveat below.

### The far 217° reading — attribution rejected, conclusion accepted

The render worker attributes `ship_beauty/far_*` h ≈ 217° to "edge/AA
contribution in a small sample". **That attribution is wrong.** Two independent
disproofs, both on the identical pixel set:

1. Eroding the mask 1/2/3 px inward — which removes every edge and AA pixel —
   leaves the hue at 216.9 → 216.4 → 216.2 → 216.1° on `far_01`, and
   218.4° unchanged at every erosion step on `far_04`. Saturation *rises*
   (0.071 → 0.076) as edges are removed, the opposite of sky dilution.
2. The same pixels read **h 58.2° s 0.249 v 0.180** in `ship_albedo` and
   **h 57.7° s 0.222 v 0.076** in `raking_beauty`.

The mechanism is the `ship` preset's fog / aerial perspective repainting the
55 m silhouette in the fog's own blue-grey — the same phenomenon round 1
recorded in its §5, and the authored zone fog doing its job. The *conclusion*
stands: not a defect, and not a colour-law event (217° is outside the threat
band, S 0.08 ≤ 0.35, V 0.41 ≤ 0.6). But the consequence is a new watch item:
the `far` `ship_beauty` STATS rows measure the fog, not the asset, and cannot
gate the colour law for this asset under that preset.

## 6. Trunk — 4/10, **FAIL** — B2

**The bole half is fully answered.** F3 verified above: dark, no longer the
brightest element, no bare trunk through mid-canopy at any azimuth or distance,
canopy skirt closing over it completely (`ship_beauty/full_01` base zoom,
`raking_beauty/full_01`, `close_cypress.png`). On its own that half is a 9.

**The crown is not.** The core spindle is exposed above the canopy as a smooth,
untextured, straight-sided cone — a dark blade standing clear of the foliage.

Read in four places:
- `inspect/ship_normal/full_01.png`, apex crop: a continuous smooth radial
  normal gradient over a triangle with perfectly straight sides and **zero
  alpha cutouts**. Alpha cards always cut their own silhouette; solid geometry
  does not.
- `inspect/raking_beauty/full_01.png`: the cone is lit as a solid shaded
  surface with its own terminator, visibly distinct from the foliage grain
  around it.
- `inspect/ship_beauty/full_01.png` and `far_01/02/04`: the apex is a hard
  point at 55 m.
- **`zone/mid_cypress_nw.png` and `zone/mid_cypress_se.png`** — the frames that
  matter. At ~30 m all four crowns terminate in the same smooth hard-edged dark
  blade against the ground. `mid_graveyard.png` shows the fifth doing the same.

Measured cause, from the shipped GLB and the shipped atlas:
- The core spindle runs to the full **y = 9.000 m** (top spray vertex 8.878 m).
- Card centroids per height band: **37 cards in y ∈ [8.6, 9.0)** (92 /m, mean
  card length 0.186 m) against **602 in y ∈ [5.0, 7.0)** (301 /m, mean length
  0.402 m).
- Each island's vignetted alpha covers only 0.129–0.148 of its own quad.

37 tiny cards at ~14 % alpha coverage cannot clothe a 0.4 m cone. The fully
solid, cutout-free run measured from the apex is 0.17–0.23 m across azimuths,
and the cone's straight-sided profile stays legible for roughly 0.7 m — ~8 % of
the tree's height, on the asset's most prominent feature.

This is a regression: round 1's asset had a blunt-rounded card crown and no
exposed core.

## 7. Grounding — 10/10, PASS

`mid_cypress_nw.png` and `mid_cypress_se.png`: all four boles meet the ground,
each with its own tapered contact shadow, no float and no sink.
`mid_graveyard.png`: the fifth planted beside the chapel at credible height.
`wide.png` carries all five with ground shadows. The `12c7e4b` renderer
prerequisite still holds — every cast shadow is a tapered tree shape through
the alpha mask, not a quad blob.

## 8. Variety — 6/10, PASS

Four across the two pair mids read as four; the 0.85–1.10 scale spread is
legible between neighbours in both frames and free yaw varies the fringe bumps.
The fifth reads independently against the chapel.

Down one from round 1. The envelope is still identical at all five — one mesh,
scale and yaw the only differentiators — and the rebuild made the repeat *more*
legible, because every crown now terminates in the same distinctive hard blade
(criterion 6). Once B2 is fixed this returns to round 1's 7; M3 (per-instance
profile seed) stays open either way.

## 9. Concept fidelity — 6/10, PARTIAL

**Colour — effectively exact, and better than round 1.** Shipped albedo
H 52.5 / S 0.281 / V 0.201 against concept tree pixels H 52.7 / S 0.331 /
V 0.194; `atlas_report.json` masked-Lab ΔE **3.47**.

**Island variety — fixed.** Round 1 shipped 9 declared islands carrying only 5
unique alpha cutouts. Round 2 ships **9 distinct cutouts** (nine independent
window picks, each with its own vignette phase seed), meeting D7's 6–10.

**Silhouette envelope — closer.** Columnar, proud fringe sprigs breaking the
envelope, foliage carried to the ground, and the apex is now pointed as the
concept's is.

**Needle register — moved further away, not closer.** The concept's sprigs are
small sharp needles with fine serration; the shipped islands are 5–10 fat
smooth-lobed branchlets with none. Round 1's complaint was that the render's
fringe units were ~2× the concept's sprig scale but at least resolved as ferns;
round 2 halved the unit and lost the resolution. And the concept's crown is
needled foliage to the tip where the shipped one is bare geometry.

Held at 6 — the gains and the loss cancel.

## Regression spot-check — clean

`zone/contact_sheet.png` opened in full plus `mid_graveyard.png`,
`mid_cypress_nw/se.png`: the plaza well and paving, both chapel interiors, the
chapel exterior and skyline, all four casa types, gate arch, wall segment,
crucero, gravestone, broken column, candelabra shrine, olive stump and all
three rock props render normally — no black frames, no missing textures, no
changed framing. The cypress change disturbed nothing else.

## Non-gating observations

- **Normals remain the quiet win.** `ship_normal/gameplay_00/03` show a smooth
  radial gradient continuous *across* card boundaries on a 2500-card mesh, no
  per-card facets, and `raking_beauty/full_01` has a clean vertical terminator
  with no card banding.
- **AO is clean but darker.** `ship_ao/gameplay_00` is soft and even with no
  ringing; the atlas gate mean drops 0.919 → **0.739** (std 0.112 → 0.092).
  Consistent with the denser card mass; not a defect.

## Fix list

**Blocker — 1. Nothing ships until this clears.**

- **B2 — the core spindle must not read at the crown.** It is bare, smooth and
  hard-edged above the canopy on all five placements at every distance from
  30 m in. Two measured facts bound the fix: the spindle runs to y = 9.000 m
  while the topmost spray vertex is 8.878 m, and crown card density is 92 /m in
  the top 0.4 m against 301 /m at mid-canopy with each card covering only ~14 %
  of its quad. Either clothe the crown (more and/or longer cards in the top
  ~0.8 m, or a crown-specific island with higher alpha coverage) or end the
  spindle below the card band — the choice is the generator's, but the gate is
  the pixels.

  **Add the numeric assert that would have caught it** to `cypressgen/verify.py`:
  for the top N % of the envelope, the summed projected alpha coverage of the
  cards enclosing the core must exceed the core's projected silhouette there.
  Red-proof it by shortening the crown cards, per the T1 pattern.

  Verify on re-render: `zone/mid_cypress_nw.png`, `zone/mid_cypress_se.png`,
  `zone/mid_graveyard.png`, and `inspect/ship_normal/full_*` — no cutout-free,
  straight-sided run at the apex in the normal channel at any azimuth.

**Required — 1. Rides B2's rebuild round; a rebuild is happening anyway.**

- **F4 — restore the needle register in the atlas islands.** The nine shipped
  spray islands carry no serration: each is 5–10 thick smooth lobes
  (`target/cypress-build/atlas/cypress_base.png`). This is what keeps criteria
  2 and 9 off 9–10 and it moved *away* from the concept between rounds. The
  cause is the crop magnification, not the vignette: `find_crop_centers` picks
  384 px windows at native scan resolution, at which individual branchlets fill
  the window. Pick larger windows (or downsample the scan before the search) so
  each island carries a whole multiply-branched spray, then vignette as now —
  the border-alpha gate is orthogonal to window size and stays green.

**Minor — 2**

- **M3 (carried, worse) — profile jitter.** All five still share one envelope,
  and the identical crown blade makes the repeat more legible than in round 1.
  A per-instance profile seed. Re-assess after B2.
- **M4 — `print_stats` mask includes partially-covered edge pixels.** The
  gameplay mask runs ~14 % wider than a hard silhouette and the extra pixels
  carry mostly background, lifting reported V by ≈ 0.06 (0.197 vs an
  independent 0.136). Harmless against a 0.6 ceiling; tighten if the law is
  ever gated on V with less margin.

## Watch items carried

- **NEW — the `far` `ship_beauty` STATS rows measure the fog, not the asset.**
  Proved by erosion (hue immobile at 216–218° through 3 px of inward erosion,
  saturation rising) and by the same pixels reading h 58° in `ship_albedo` and
  `raking_beauty`. Every ceiling still clears, so it is not a colour-law event,
  but the colour law cannot be gated at `far` under `ship` — gate it at
  `gameplay`, or on `ship_albedo`.
- **The rendered tree is still much darker and flatter than its albedo**
  (V 0.133 vs 0.201, S 0.101 vs 0.281). Inside every ceiling. Carried unchanged
  from round 1; still a lighting/exposure question, not an asset one.
- **`asset_inspect`'s `full` arm is a 45.8°-pitch turntable** and still cannot
  judge vertical proportion — it reads h/w 3.1–3.4 where the level `far` arm
  reads 4.4–4.6 on the same asset. Carried.
- **Mip-ladder watch item — RESOLVED.** Smaller cards did not thin the chain
  (see criterion 4). Struck.
- **`zone_review` shot-coverage gap — CLOSED.** `cypress_nw` and `cypress_se`
  are permanent `ROCALBA_SHOTS` entries as of `1a5bf6c`; both frames are
  reproducible from a clean checkout and criteria 7 and 8 no longer lean on a
  temporary edit. Round 1's carry of P2.4's F7 for *this* asset is struck.

---

# Round 3 — 2026-08-05 (fresh judge)

Subject: the working-tree procedural cypress on top of `1a5bf6c`,
`content/models/props/cypress/cypress.glb`, 2 820 cards / 23 824 tris
(uncommitted `cypressgen/` + `asset_inspect.rs` `BG_EPS` 8→32 fixes).
Evidence: `target/review/cypress-r3/` (32 zone frames, 288 `asset_inspect`
frames, 72 subject-masked `STATS` lines). `cypress-r2/` and `cypress/` were
re-measured alongside for every diff below.

Every number here was re-derived by this judgment from the shipped pixels, the
shipped `cypress.glb` accessors and the shipped
`target/cypress-build/atlas/cypress_base.png`. Nothing is taken from
`MANIFEST.md`'s prose or from `generation_manifest.json`'s `verify` block —
the generator's own `crown_coverage` assert cannot grade its own candidate, so
B2 was re-measured from the render and from the vertex buffer instead.

## Verdict

# PASS — 0 blockers, 0 required fixes, 2 minor

**B2 is dead** and **B1 stayed dead**. The crown is clothed at every azimuth,
every distance and all five placements; the re-cropped atlas reintroduced no
border rectangles. F4 landed and is the round's biggest visible gain — the
foliage unit is a multiply-branched serrated spray again. Seven of nine
criteria hold or improve, none regressed, and every fix from rounds 1 and 2
still verifies in pixels.

| # | Criterion | R1 | R2 | R3 | |
|---|---|---|---|---|---|
| 1 | Columnar (h/w 4–6) | 9 | 9 | **9** / 10 | PASS |
| 2 | Fine, not shard-like | 4 | 8 | **9** / 10 | PASS |
| 3 | No sky holes | 9 | 9 | **9** / 10 | PASS |
| 4 | Distance survival at 55 m | 9 | 9 | **9** / 10 | PASS |
| 5 | Colour law | 8 | 9 | **9** / 10 | PASS |
| 6 | Trunk = basal bole only | 8 | 4 | **9** / 10 | PASS |
| 7 | Grounding, all five | 10 | 10 | **10** / 10 | PASS |
| 8 | Five read as five | 7 | 6 | **7** / 10 | PASS |
| 9 | Concept fidelity | 6 | 6 | **7** / 10 | PARTIAL |

---

## B2 recheck — **DEAD**, not healed-with-residue

Round 2 named four reads; all four were re-opened at the same crops.

- **`inspect/ship_normal/full_00..05`, apex crop (440,175)–(600,295) at 6×.**
  Round 2's frame shows the smooth straight-sided cone standing clear of the
  canopy with zero alpha cutouts. The round-3 frame at the identical crop shows
  the apex clothed in cards: cutout-punctured, ragged, no smooth spike, at
  **every one of the six azimuths**.
- **Cutout-free run measured down from the apex** (rows whose fill inside the
  silhouette span is 1.000): R2 **5–15 px** across the six azimuths, R3
  **0–3 px**. Apex boundary rms curvature over the top 60 rows rises
  2.7–6.2 px (R2) → 4.6–7.5 px (R3), i.e. the tip edge went from
  near-straight to foliage-ragged.
- **`inspect/raking_beauty/full_01`, apex at 5×/2.2 brightness.** R2's cone is
  a solid shaded surface with its own terminator; R3's terminator runs through
  card grain — no solid facet anywhere at the tip.
- **`inspect/ship_beauty/full_00..05`, six-azimuth apex montage at 2.2×.** R2:
  a grey cone spike on all six. R3: a foliage crown on all six.
- **`zone/mid_cypress_nw.png`, `zone/mid_cypress_se.png`, `zone/mid_graveyard.png`
  — the frames that decided round 2.** All five crowns terminate in ragged
  sprig-broken foliage. The R2 crop at (1120,70)–(1340,240) of
  `mid_cypress_nw.png` shows the black blade unmistakably; the R3 crop at the
  same coordinates shows none.
- At 55 m (`ship_normal/far_01`) the tip is blunter and more ragged than R2's
  needle point — the crown survives the distance without becoming a hard pip.

**Root cause closed at the generator, verified from the shipped vertex buffer**
(POSITION/TEXCOORD accessors parsed directly; the first 1 264 tris are the core
spindle, the remaining 22 560 are the 2 820 eight-triangle cards):

| | R2 (record) | R3 (measured here) |
|---|---|---|
| core radius at the crown | runs to y = 9.000 at full radius | rings at y ≈ 7.75 r = 0.177 m, at y ≈ 8.9 r = **0.0011 m** |
| topmost card vertex | 8.878 m | **8.9845 m** |
| cards centred in y ∈ [8.6, 9.0) | 37 (92 /m) | **129 (322 /m)** |
| cards centred in y ∈ [8.0, 8.6) | — | **329 (548 /m)**, above the 296 /m mid-band |

The core is geometrically absent where the cards thin, and the cards are denser
at the crown than at mid-canopy. Both halves of round 2's measured cause are
reversed.

## B1 recheck — **still DEAD** on the re-cropped atlas

The re-crop was the obvious way to reintroduce round 1's rectangles. It did not.

- **Border alpha re-measured from the shipped `cypress_base.png`** (not from
  `atlas_report.json`): fraction of border-row/column texels above the shipped
  `alphaCutoff` 0.35 is **0.0000 on all four borders of all nine spray
  islands**. Round 1 scored 0.383–0.734 on at least two borders of every island.
- **Longest straight vertical run on the sky-backed silhouette boundary**,
  `ship_normal/gameplay_00..05`: R1 9–40 px, R2 8–19 px, **R3 8–16 px**.
- **`ship_beauty/gameplay_00..05`, 2.6×-brightened sky-backed canopy montage**:
  individually shaped multiply-branched fronds at every azimuth, no straight
  run, no square corner.
- **`zone/close_cypress.png` (2.3 m, player beside the tree)**: organic
  silhouette top to bottom at both flanks; round 1's two named verticals
  (x ≈ 1080 and x ≈ 1040) have no counterpart.
- `ship_normal/gameplay_00` full frame: continuous radial normal gradient across
  card boundaries on a 2 820-card mesh, zero flat facets, zero geometric blocks.

## Fix verification

**F4 — needle register restored. DONE, and it is the round's biggest gain.**
Montage of all seven unique spray islands from the shipped atlas: each is now a
whole multiply-branched spray with serrated scale-leaf branchlets, replacing
round 2's 5–10 thick smooth coral lobes. In render, the identical crop of
`zone/close_cypress.png` at (480,60)–(820,320), 3×/1.9 brightness, shows R2's
blunt lobes against R3's pinnate serrated fronds. Numerically, perimeter/area
over the sky-backed gameplay silhouette rises **0.0190–0.0219 (R2) → 0.0256–0.0288
(R3)**, a 42 % gain in edge fineness at unchanged silhouette area.

**M4 — stats mask tightened. DONE.** Subject mask rebuilt independently from
`ship_normal` (sky = black, ground = flat plane colour) and applied to the
matching beauty frame:

| stats line | `stats.txt` | this judgment, independent mask |
|---|---|---|
| `ship_beauty/gameplay_01` | h 60.78 s 0.107 v 0.132 px 471 715 | h 61.33 s 0.106 v 0.137 px 475 171 |
| `ship_beauty/gameplay_03` | h 54.11 s 0.098 v 0.120 px 474 855 | h 57.47 s 0.096 v 0.125 px 478 993 |

Hue agrees to ≤ 3.4°, saturation to ≤ 0.002, **value to ≤ 0.005**, pixel count
to ≤ 0.9 %. Round 2's ≈ 0.06 V inflation is gone; the shipped mask now sits
just *inside* an any-coverage mask rather than 14 % outside it.

**F1 / F3 / M1 / M2 — no regression.** `stats.txt` counts 464k–481k of
1 048 576 px at gameplay (F1 holds). Bark island re-measured on the shipped
atlas: **H 28.9 S 0.266 V 0.194** — dark warm brown, and the base zoom of
`ship_beauty/full_01` shows a small bole that is no longer the brightest element
on the tree (F3 holds). Subject-masked `ship_albedo` over six gameplay azimuths,
219 400 sampled px: hue [260, 350) = **0.0000 %** (M1 holds); hue [350, 25) =
4.58 % against R2's 3.75 %, still the bark island plus edge AA and still not a
law event since the law gates the mean (M2 unchanged).

## M3 arbitration — the fix worker's judgment call is **upheld**

The fix worker shipped no separate mechanism for M3, on the escape clause
"unless the apex silhouette still reads copy-paste at mids". Arbitrated on
`zone/mid_cypress_nw.png` and `zone/mid_cypress_se.png` at 4× apex zoom, plus
`mid_graveyard.png` for the fifth:

- NW-left: blunt shoulder, tip carried left, one proud side sprig.
- NW-right: taller symmetric cone with a notch on the right shoulder.
- SE-left: broad stepped shoulder, tip is a wide tuft.
- SE-right: narrow sharp tip with a long clean right flank.
- Graveyard: full feathered tip, blunter than any of the four.

**No copy-paste cue.** Round 2's aggravating factor — every crown terminating in
the same distinctive hard blade — is gone, and because the crown is now foliage,
per-instance yaw rotates a different set of crown cards into the silhouette, so
the apexes differ without any new mechanism. The escape clause is satisfied and
no crown-specific fix is owed. Criterion 8 returns to round 1's 7; M3 stays open
at its original round-1 weight (one envelope, scale and yaw the only
differentiators), no longer aggravated.

---

## 1. Columnar — 9/10, PASS

GLB POSITION accessor: height **9.000 m**, max radius **0.9517 m** →
**h/w 4.73**. Rendered on the level `far` arm (`ship_normal/far_00..05`,
identical measurement recipe on both rounds): **R3 4.17–4.28, R2 4.07–4.30** —
unchanged and in the 4–6 band. `wide.png` still reads as five slim dark
exclamation marks bracketing the settlement under fog. The `full` arm's
45.8° turntable still measures 3.1–3.4 and still cannot judge this criterion.

## 2. Fine, not shard-like — 9/10, PASS

No plate, no shard, no cross-plane read, no card rectangle at any azimuth or
distance (B1 section). The register loss that held round 2 at 8 is repaired:
the shipped islands carry serrated multi-branchlet sprays and the sky-backed
perimeter/area rises 42 %. `zone/close_cypress.png` at shipped exposure reads
as a dense dark columnar tree with legible individual fern-like fronds.

Not 10 because at matched tree width the frond unit is still roughly **2×** the
concept's sprig (criterion 9), and the triangle budget that would buy the
halving is now spent.

## 3. No sky holes — 9/10, PASS

Enclosed background inside the sky-backed silhouette, `ship_normal`,
six azimuths at gameplay: **R3 0.94–1.28 %** against R2 0.69–1.09 % and R1
0.81–1.93 %. The small rise is the finer cutouts of F4 and sits inside the
range a real tree gives. At 55 m the tree's own component holds bbox fill
**0.724–0.725** with **15–36 px** enclosed — no hole survives the distance.
Confirmed visually in `wide.png`, both pair mids and `mid_graveyard.png`.

## 4. Distance survival at 55 m — 9/10, PASS

`ship_beauty/far_01/04` at 4× zoom: a coherent dark columnar mass with a ragged
edge and a small pale bole, no lacing, no dissolve, no transparency. Subject
px 4 806–5 096.

**The round-2 mip re-check is answered.** The re-cropped atlas's coverage ladder
is `[1.024, 1.054, 1.113, 1.209]` — still rising, still far above the D6 gate of
0.55, and flatter than round 1's. Finer alpha features did **not** thin the box
mips. The Castaño per-mip rescale in `bake_textures.mjs` stays deferred.

## 5. Colour law — 9/10, PASS on all three ceilings

Independent subject mask (from `ship_normal`), six gameplay azimuths,
saturation-weighted circular hue mean:

| | hue | S | V |
|---|---|---|---|
| `ship_beauty` | **57.5–106.9°** (mean ≈ 65°) | **0.076–0.113** | **0.125–0.147** |
| `ship_albedo` | **53.2–54.2°** | **0.265–0.272** | **0.193–0.196** |
| concept tree pixels (round 1) | 52.7° | 0.331 | 0.194 |

- **S ≤ 0.35** — PASS (0.113 worst rendered, 0.272 albedo).
- **V ≤ 0.6** — PASS (0.147 worst rendered, 0.196 albedo).
- **hue outside 350°–25°** — PASS (53–107° rendered, 53–54° albedo).

The az-05 outlier the manifest flags (`h = 84.96` in `stats.txt`, 106.9° on my
mask) is a low-saturation frame (s 0.076) where circular hue is unstable; it is
nowhere near the threat band and both other ceilings clear.

Held at 9 for two instrument caveats, neither asset-side: the `far` rows still
measure fog (below), and `raking_beauty/full_*` reads **h 25.7–26.6°** — inside
1.6° of the forbidden band under a warm grazing sun on the turntable arm, where
the same asset reads 36–40° at raking gameplay and 53° in albedo.

## 6. Trunk — 9/10, PASS

**Bole:** small, dark warm brown (bark island H 28.9 S 0.266 V 0.194), no bare
trunk through mid-canopy at any azimuth or distance, canopy skirt closing over
it completely. Not the brightest element at any distance including 55 m.

**Crown:** clothed — see the B2 section. The measured cause is closed at both
ends (core radius 0.0011 m above 8.8 m; crown card density 322–548 /m against a
296 /m mid-band).

Not 10: at 6× zoom on `ship_beauty/full_01` the bole is a visibly faceted
low-poly cylinder, and at 2.3 m the core shaft shows through canopy gaps as a
smooth dark surface. Both read as interior shadow at shipped exposure — a note,
not a defect.

## 7. Grounding — 10/10, PASS

`mid_cypress_nw.png` and `mid_cypress_se.png`: all four boles meet the ground,
each with its own tapered contact shadow, no float and no sink.
`mid_graveyard.png`: the fifth planted beside the chapel at credible height.
`wide.png` carries all five with ground shadows. The `12c7e4b` renderer
prerequisite still holds — every cast shadow is a tapered tree shape through the
alpha mask, not a quad blob.

## 8. Variety — 7/10, PASS

Four across the two pair mids read as four; the 0.85–1.10 scale spread is
legible between neighbours and free yaw varies both the fringe bumps and now the
crown tip. The fifth reads independently against the chapel. Up one from round 2
because the identical-blade cue is gone (M3 arbitration above). Held at 7, not
higher, because the envelope is still one mesh at all five and at `wide.png`
framing the four field cypresses remain interchangeable.

## 9. Concept fidelity — 7/10, PARTIAL

**Colour — effectively exact, marginally better than round 2.**
`atlas_report.json` masked-Lab ΔE **3.43** (R2 3.47); shipped albedo
H 53–54 / S 0.27 / V 0.19 against concept tree pixels H 52.7 / S 0.331 / V 0.194.

**Island variety — 7 unique alpha cutouts**, inside D7's 6–10. Correcting the
round-2 record: `spray_dry_00` and `spray_dry_01` are **byte-identical in alpha**
to `spray_02` and `spray_05` (md5 of the thresholded alpha), so the shipped
count is 7 distinct cutouts over nine declared islands, not 9.

**Silhouette envelope and crown — match.** Columnar, proud fringe sprigs
breaking the envelope, foliage to the ground, and the crown is needled to the
tip as the concept's is. Round 2's "the concept's crown is needled foliage where
the shipped one is bare geometry" is closed.

**Needle register — recovered, still one step short.** Side-by-side at matched
tree width (concept upper canopy vs `ship_beauty/gameplay_02` scaled to the same
tree width): the render's fronds are now multiply branched and serrated, but the
frond unit still spans roughly **twice** the concept's sprig, and the dark core
shows through canopy gaps where the concept is dense needle mass throughout.
Round 2's regression is undone; round 1's original register gap is not.

Raised to 7 — everything moved toward the concept and nothing away from it.

## Regression spot-check — clean

`zone/contact_sheet.png` opened in full plus `mid_graveyard.png` and both pair
mids: the plaza well and paving, both chapel interiors, the chapel exterior and
skyline, all four casa types, gate arch, wall segment, crucero, gravestone,
broken column, candelabra shrine, olive stump and all three rock props render
normally — no black frames, no missing textures, no changed framing. The cypress
change disturbed nothing else.

## Non-gating observations

- **Normals remain the quiet win.** `ship_normal/gameplay_00` shows a continuous
  radial gradient across card boundaries on a 2 820-card mesh with no per-card
  facets, and the pinnate branching of the new islands is legible in the channel.
- **AO gate** mean 0.748 std 0.080 (R2 0.739 / 0.092) — soft, even, no ringing.
- **`atlas_report.json` red-proofs all fire**, including
  `island_border_alpha` failing an un-inset probe at 0.311.

## Fix list

**Blockers — none. Required — none.**

**Minor — 2**

- **M3 (carried, no longer aggravated) — profile jitter.** All five placements
  share one envelope; scale and yaw are the only differentiators. Worth a
  per-instance profile seed if these ever appear outside a formal planted row.
  Round 2's aggravation (identical crown blade) is resolved and is not part of
  this item any more.
- **M5 (new) — the needle unit is still ~2× the concept's sprig**, and the
  lever round 1's F2 used is now spent: the mesh is **23 824 of 24 000 tris**,
  so card count cannot buy another halving. Closing the remaining gap needs
  finer island content (more branchlets per island at the same crop scale) or a
  budget raise, not more cards. Not gating — criterion 2 passes at 9 and
  criterion 9 at 7 with this open.

## Watch items carried

- **`far` `ship_beauty` STATS rows measure the fog, not the asset** (h 216–219°,
  v 0.36–0.37 at 55 m). Instrument-level, established in round 2 by erosion and
  cross-channel disproof; nothing in round 3 contradicts it. Gate the colour law
  at `gameplay`, or on `ship_albedo`. Not re-litigated.
- **NEW — `raking_beauty/full_*` reads h 25.7–26.6°**, within 1.6° of the
  forbidden 350°–25° band. A warm grazing sun on the 45.8° turntable arm, not
  the asset: the same pixels read 36–40° at raking gameplay and 53–54° in
  `ship_albedo`. If the law is ever gated on raking, this is the row that trips.
- **NEW — the triangle budget is effectively spent** (23 824 / 24 000). Any
  future fineness ask has to come from the atlas, not from card count. Recorded
  so a later round does not re-issue round 1's F2.
- **The rendered tree is still much darker and flatter than its albedo**
  (V 0.13 vs 0.19, S 0.10 vs 0.27). Inside every ceiling. Carried unchanged from
  rounds 1 and 2; a lighting/exposure question, not an asset one.
- **`asset_inspect`'s `full` arm is a 45.8°-pitch turntable** and cannot judge
  vertical proportion — 3.1–3.4 against the level `far` arm's 4.2–4.3 on the
  same asset. Carried.
- **Enclosed sky holes rose** 0.57–1.15 % → 0.94–1.28 % at gameplay with F4's
  finer cutouts. Well inside the passing range; the tripwire if a future round
  makes the islands finer again.
