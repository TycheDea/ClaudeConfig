# P3.1 — RUN-C1 concept list (8 concepts × 8 seeds)

Authoring only. **Zero GPU spent by this document.** It defines what C1
generates, how it is dispatched, and what makes a candidate a PASS at the Opus
concept screen that gates every H-chain.

Binding inputs, read not restated:

- `docs/town-premise.md` — §2 colour law, §3 closed material vocabulary, §7
  prompt contract.
- `~/.claude/plans/zippy-wibbling-pancake.md` — D1 (Hi3DGen heroes ≤ 5.5 m),
  §8 GPU table (C1 = 35 min; H1..H7 = 30 candidates ≈ 5.5 h).
- `tasks/town/p30-chapel-legibility.md` §6 — the H1 ruling and the three
  filters it establishes.
- `tasks/todo.md:581-694` — P3.0's binding ruling as recorded.

---

## 0. The three filters (P3.0 §6, generalised)

The chapel-portal cancellation was not a chapel fact. It was three independent
tests, each sufficient on its own to move a subject from hero to kit. They are
applied to every chain below.

**F-mate — does the piece have a mating contract?** A Hi3DGen extraction lands
in its own voxel frame with no flat-back and no dimensional guarantee. Any
subject that must be coplanar with a 0.6 m wall, concentric with an authored
opening, or hinged on an authored jamb fails. `verify.py`'s open-face and
joint-gap checks cannot see across a prop boundary, so a mating defect ships
silently.

**F-atlas — does the piece read as its own object?** A hero carries its own
baked atlas: different limestone, at a different texel density, from the kit's
tiling material at 6.4 mm/texel. When the hero abuts kit of the *same* material
family, that seam is the asset-internal split that scored G2 Q1 at **3/10**.
The seam is survivable only where the material family changes at the same edge
(oak against stone) or where nothing abuts at all.

**F-form — is there anything to generate?** Rocalba is poor (premise §1). If
the honest answer for a poor village is a plain repeated form — a plain
voussoir ring, a plain plank, a lathed barrel, a boarded box — a Blender script
produces it *better* (exact, parameterised, variable per instance) and the
chain buys nothing but a lumpy one-off.

A fourth consideration, not a filter but a cost: **F-repeat**. A prop placed in
multiples is worse as a hero by construction, because generation yields one
instance repeated N times while the kit yields N parameterised variants.

---

## 1. Allocation argument

### 1.1 The chain list, judged

| chain | subject as planned | verdict |
|---|---|---|
| H1 ×4 | chapel portal / `chapel_arch` re-roll | portal half **already cancelled** (P3.0 §6); arch re-roll **survives** |
| H2 ×4 | fountain | **CANCEL — no fountain exists in Rocalba** (§1.2) |
| H3 ×4 | retablo | **survives — the strongest hero in the campaign** |
| H4 ×3 | shrine niche | **survives, re-scoped** to a freestanding shrine pillar (§2.4) |
| H5 ×3 | gate doors | **CANCEL — kit** (§1.3); slot re-allocated to the gate brazier |
| H6 ×9 | cart / barrel / crate | cart **survives**; barrel and crate **CANCEL — kit** (§1.4) |
| H7 ×3 | votive stand | **survives, but its feasibility is itself the screen** (§2.6) |

Five chains survive plus one re-allocation. A concept image is consumed
one-per-asset by `stage_geometry`, so **every distinct downstream asset needs
at least one slot**; that floor is six. The two remaining slots go where the
screen resolves a decision that no document already settles.

### 1.2 H2 fountain — cancelled outright

There is no fountain in Rocalba. `docs/town-premise.md` §4 places a **well
basin** south of spawn, §5 registers `well_basin` as a kit type ("bucket rope
hanging slack down the shaft"), and `content/models/assets.json` already
carries `well_basin` as `kind: "kit"` — built and shipped. "Fountain" is
plan-era wording from D1's example list, written before the premise existed;
the premise then made it a well and Phase 2 built it.

The one part of the well that is not yet built — the windlass headgear and its
slack rope — fails **F-mate** (it must sit on an authored basin rim), **F-form**
(a frame, a drum, a crank) and the plan's own risk-table entry on thin iron.
It is kit. No slot is re-allocated to it: the well is complete enough for the
premise beat, which is a rope going down a shaft, not a machine above it.

**4 chain candidates released.**

### 1.3 H5 gate doors — kit, slot re-allocated

A gate leaf is vertical planks, horizontal ledges, iron straps, boss nails: the
**F-form** case verbatim, and one where a script gives dead-straight planks and
evenly-pitched nails that Hi3DGen will not. It also fails **F-mate** — the leaf
hangs on the authored jamb of the kit `gate_arch`, whose intrados is 1.94 m
over a 3.2 m opening (a defect already queued under P3.0), so the mating
geometry is not even stable yet. And premise §5 rules the gates **open** on the
night of vespers, so both leaves lie flat against the wall and are seen edge-on
from the road.

The gate's actual generation-shaped object is the one premise §1 and §5 both
name and no asset provides: **the porter's brazier, still lit**. Freestanding,
~1 m, no mating contract, and it carries the town's signature candle-gold
emissive at the one place the player enters the zone. That is concept C8.

### 1.4 H6 — cart survives; barrel and crate are kit

- **Barrel.** A solid of revolution: staves, two iron hoops, a chime, a bung.
  **F-form** exactly, and **F-repeat** — premise §4 places "cart and barrel
  dressing at the edges", plural. A generated barrel is one lumpy revolution
  with smeared hoops, instanced; a kit barrel is exact and varies by parameter.
  It also binds `oak_dark` + `iron_wrought` from the shared kit set instead of
  minting a private atlas for one of the smallest props in town — the same
  cohesion argument P3.0 used to keep the chapel bell in the kit.
- **Crate.** Six boards and a corner frame — **F-form** at its purest. It is
  also wrong for the period: late-15th-century Castile moved goods in sacks,
  wicker panniers, baskets and barrels. The nailed shipping crate is a modern
  game-dressing reflex, and the premise never asks for one.
- **Cart survives.** Irregular by construction, no mating contract, a real
  silhouette read at plaza scale, and a directly named premise beat ("a cart
  abandoned mid-load", §1). It is also the highest geometry risk in the list,
  which is precisely why it is screened.

Cancelling a chain does not cancel the prop. The barrel still ships — from
`build_town_kit.py`, alongside the crate's period-correct replacement if one is
wanted (see OPEN-2).

**6 chain candidates released** (9 → 3).

### 1.5 Where the two free slots go

Six assets, eight slots. The two spare slots are spent only where a **real
two-way decision** exists that no binding document settles, and where the two
answers diverge downstream.

**Retablo ×2 (C2, C3).** Premise §6 fixes the *materials* — dark oak frame,
painted panels in ambient-world values, gilt that glints candle-gold — but not
the *silhouette*. A flat panelled reredos board and a three-bay frame with a
crowning pediment are different objects: one reads as a plank at 8 m, the other
reads as the chapel's east-end landmark. This is the interior's entire payoff
and the one hero the player will stand in front of. Two silhouettes, screened
against each other, is the cheapest way to settle it.

**Votive stand ×2 (C6, C7).** This slot buys a **feasibility** answer, not a
taste answer. D1 already routes thin ironwork away from generation ("Iron rejas
= Blender curves + iron material") and the plan's risk table lists "thin iron /
carving legibility" as a medium risk. A tall pricket stand (slender post,
tripod foot, one tray) is the thin case; a low tiered rack (heavy square frame,
stepped tiers, flat feet) carries far more mass per element. If both come back
smeared, H7 is cancelled at the screen and votive stands go procedural like the
rejas — a decision worth 8 GPU-minutes to reach before 26 chain-minutes are
spent on it.

**Two slots deliberately NOT spent:**

- *Cart, second silhouette.* The premise settles it: "abandoned mid-load" fixes
  it upright and loaded, and the Castilian **carreta** is two-wheeled with solid
  disc wheels — which is also the Hi3DGen-safe geometry. Spoked wheels would be
  both wrong and fragile. Ruled here at zero cost; no slot needed.
- *Retablo, figural variant.* Premise §6 says painted panels and gilt details.
  It names no statue. A saint figure is the exact melted-carving slop this
  screen exists to catch, and the premise gives no mandate for it. Every
  retablo candidate is therefore **aniconic in three dimensions** — painted
  figures on flat panels are fine, carved ones are an instant fail.

### 1.6 Slot table

| slot | subject | chain | asset name (proposed) | height_m | surface_class |
|---|---|---|---|---|---|
| C1 | ruined freestanding arch | H1 | `chapel_arch` (exists) | 5.497 | `limestone` |
| C2 | retablo — flat panelled reredos | H3 | `retablo` | 3.0 | `oak_dark` |
| C3 | retablo — three-bay with pediment | H3 | `retablo` | 3.0 | `oak_dark` |
| C4 | wayside shrine pillar | H4 | `shrine_pillar` | 2.0 | `limestone` |
| C5 | ox cart abandoned mid-load | H6 | `cart` | 1.6 | `oak_dark` |
| C6 | votive stand — tall pricket | H7 | `candelabra_shrine` (exists) | 1.3 | `painted_metal` |
| C7 | votive stand — low tiered rack | H7 | `candelabra_shrine` (exists) | 0.9 | `painted_metal` |
| C8 | gate brazier, lit | H5→ | `gate_brazier` | 1.0 | `painted_metal` |

Every height is inside D1's 5.5 m cap; `chapel_arch` clears it by 3 mm, which
is why P3.0 kept it.

Registry entries are **not** written now. C1 is dispatched without them (§4),
and writing an `assets.json` entry for an unapproved concept would register an
asset that may never exist.

### 1.7 Chain budget after the cancellations

At the plan's 8.5 min/candidate:

| chain | candidates | wall |
|---|---|---|
| H1 `chapel_arch` | 4 | 34 min |
| H3 retablo (winning silhouette) | 6 | 51 min |
| H4 shrine pillar | 3 | 26 min |
| H6 cart | 3 | 26 min |
| H7 votive stand *(only if C6/C7 pass)* | 3 | 26 min |
| H5→ gate brazier | 3 | 26 min |
| **total** | **22** | **≈ 3.1 h** |

Against the approved 30 candidates / ~5.5 h. **~2.4 h of approved GPU budget
released**, and no new go-ahead is needed — the run shrank, it did not grow.
The retablo takes 6 rather than 4 because it is the campaign's one interior
landmark and the freed budget is already paid for.

---

## 2. The concepts

### Prompt format — what the pipeline actually consumes

`scripts/ai-pipeline/workflows/prop_concept.json` node `4` is a single
`CLIPTextEncode` whose text is:

```
{subject}, single object centered, plain grey background
```

So **a concept spec supplies exactly one string: `subject`.** The framing
suffix is appended by the workflow and must not be repeated in the prompt.
Node `5` is `ConditioningZeroOut` of the positive, and node `8` samples at
`cfg 1.0` — see §4 for what that means for negatives.

**Token budget.** The 77-token event on record (`tasks/todo.md:163`) belongs to
`gen_material.py`, which drives **SDXL** through diffusers. This workflow does
not: it loads `qwen_3_4b_fp8_mixed.safetensors` as a `lumina2`-type encoder for
Z-Image Turbo, an LLM text encoder with no 77-token cap. The constraint the
brief cites **does not bind these prompts**.

The discipline still holds, for the correct reason: every prompt below stays
inside ~60 tokens to match the register of the shipped `assets.json` subjects
(the only prompts this workflow is known-good on), and **the premise citation
stays out of the prompt entirely** — `place: Rocalba (docs/town-premise.md)` is
provenance, not description, and spending conditioning on a file path degrades
the image. Premise §7.1 is satisfied by the citation column below; §7.2 is
satisfied by lifting §3's colour clauses **verbatim** into each prompt.

**Exclusions are stated affirmatively.** With no working negative channel,
"no X" is an unreliable instruction to a turbo model. Every exclusion below is
phrased as a positive property ("plain", "undecorated", "unhitched") wherever
that is possible; the two places a bare negation survives ("no carving") are
flagged as belt-and-braces, with the real enforcement in the screening
criterion.

---

### C1 — `chapel_arch` re-roll

**Chain:** H1 (the only surviving half). **Premise:** §3 dressed limestone,
§4 old ruin cluster at (−26, −34).

**Decision screened.** The installed `chapel_arch` shipped with visible melted
carving, and its defect *was already present in its concept* — this slot exists
to catch that before 34 minutes of chain time. It also screens a wording defect
in the current registry subject: `assets.json:43` says "gothic archway
fragment" and "soot-darkened carvings", both wrong for a poor Castilian village
church and both invitations to the exact slop that convicted the shipped asset.
If the new prompt returns a plain round arch with crisp voussoir joints, the
re-roll proceeds; if it still returns carved mush, the failure is the model,
not the prompt, and H1 is re-argued as kit.

**Downstream if different.** A clean plain-arch concept replaces
`chapel_arch`'s registry subject and the ruin cluster keeps a generated arch.
A failure means the ruin arch becomes a `barrel_shell` in the kit and H1's last
4 candidates are released.

**Positive prompt (`subject`):**

```
ruined freestanding stone archway fragment, plain round arch of dressed voussoirs, undecorated, broken masonry stumps at both feet, pale grey dressed limestone ashlar, cool light grey with faint sandy flecks, matte, thin dark-grey soot settled in the joints, edges rounded by wear
```

**Negative prompt:** none — inert in this workflow (§4). Recorded intent, for
the screening criterion only: *gothic tracery, foliate carving, figures,
crockets, marble, brick, warm sandstone, ground plane, extra props.*

**Premise citation:** `place: Rocalba (docs/town-premise.md)` §3 dressed
limestone (colour clause verbatim), §1 perimeter decay.

**Args:** default. `height_m 5.497`, `texture_size 2048`, `view_res 1536`,
`tri_budget 14000` (unchanged from the shipped entry).

---

### C2 — retablo, flat panelled reredos

**Chain:** H3. **Premise:** §6 ("dark oak frame, painted panels in
ambient-world values, gilt details that glint candle-gold — the richest surface
in town, and still modest").

**Decision screened.** Silhouette A of two. Does the humblest possible retablo
— a rectangular framed board of three flat panels — read as an altarpiece at
the chapel's east end, or as a plank? This is the question §1.5 could not
settle from the premise.

**Downstream if different.** If A reads and B does not, the retablo is a
low-relief object with a small tri budget and no overhangs, the easiest
possible Hi3DGen subject. If only B reads, the chain carries real depth and the
cleanup stage must preserve it.

**Positive prompt (`subject`):**

```
small poor parish altarpiece, plain rectangular dark oak frame around three flat painted panels, muted desaturated painting, thin gilt beading catching warm candle-gold, dark oak, deep near-black brown, silvered light-grey weathering on raised grain, modest village work, undecorated
```

**Negative prompt:** none. Recorded intent: *carved statues, gilded baroque
scrollwork, marble, bright saturated colour, altar table, candles, church
interior background.*

**Premise citation:** §6 retablo clause; §3 dark oak (colour clause verbatim);
§2 candle-gold 35°–50°.

**Args:** default; proposed `height_m 3.0`, `texture_size 2048`,
`view_res 1536`, `tri_budget 12000`.

---

### C3 — retablo, three-bay with pediment

**Chain:** H3. Same premise clause as C2.

**Decision screened.** Silhouette B. A three-bay frame with a shallow **empty**
central niche and a plain low pediment above — articulated enough to read as a
landmark, still poor enough for Rocalba. The niche is empty by ruling (§1.5):
no carved figure at any candidate, both because the premise names none and
because a melted saint is the defect class this screen exists to catch. An
empty niche is also on-premise — the town is emptied.

**Downstream if different.** If B wins, the chapel's east end gets a real
depth read against the vault shafts (premise §6 lighting intent) and H3's 6
candidates run on this silhouette. If both pass, B wins on landmark value and A
is discarded — this is not a both-ship slot.

**Positive prompt (`subject`):**

```
small poor parish altarpiece, three-bay dark oak frame, shallow empty central niche flanked by flat painted panels, plain low pediment above, thin gilt beading catching warm candle-gold, dark oak, deep near-black brown, silvered light-grey weathering on raised grain, modest village work
```

**Negative prompt:** none. Recorded intent as C2, plus *statue in the niche,
figure, saint, sculpture.*

**Premise citation:** §6 retablo clause; §3 dark oak (verbatim); §2
candle-gold.

**Args:** as C2.

---

### C4 — wayside shrine pillar

**Chain:** H4. **Premise:** §4 "wayside shrines (crucero, shrine niche) on the
east road and the chapel path".

**Decision screened, and a re-scope.** The chain's planned name — "shrine
niche" — describes two different objects, and one of them is not generable. A
niche *set into a casa wall* is a mating contract against a kit facade and a
limestone-on-limestone atlas seam: **F-mate + F-atlas**, the cancelled-portal
class exactly. The generable object is the freestanding **humilladero** post: a
square stone pillar with a hooded recess near the top. This concept depicts
that, and the screen tests whether the hood-and-recess silhouette survives at
2 m — the recess is the only depth the object has.

**Downstream if different.** A shallow or filled-in recess means the shrine is
a plain post and belongs in the kit alongside the wall segments, releasing
another 3 candidates. A clean deep recess with a legible candle inside gives
the approach roads their premise beat.

**Positive prompt (`subject`):**

```
freestanding wayside shrine pillar, plain square stone post with a deep hooded recess near the top, flat slab hood, one lit white wax candle standing inside the recess, warm candle-gold flame, pale grey dressed limestone ashlar, cool light grey with faint sandy flecks, matte, thin dark-grey soot in the recess, undecorated
```

**Negative prompt:** none. Recorded intent: *statue, saint figure, crucifix,
relief carving, inscription plaque, iron railing, ground plane.*

**Premise citation:** §4 approaches; §3 dressed limestone (verbatim); §1
candles burning everywhere; §2 candle-gold.

**Args:** proposed `height_m 2.0`, `texture_size 2048`, `view_res 1536`,
`tri_budget 9000`, `azimuths [0, 60, 180, 300]` (matching `crucero`, whose
front/back asymmetry is the same shape of problem).

---

### C5 — ox cart abandoned mid-load

**Chain:** H6 (the surviving third). **Premise:** §1 "a cart abandoned
mid-load"; §4 "cart and barrel dressing at the edges".

**Decision screened.** The highest geometry risk in the list. Wheels are the
classic Hi3DGen failure — a spoked wheel comes back as a disc or a smear. The
premise and the period both give the safe answer (the Castilian **carreta** has
solid disc wheels), so this slot screens whether even *that* survives: two
clean disc wheels, a readable plank bed, and a draught pole that does not fuse
into the bed. It also screens the load — sacks, not crates (§1.4).

**Downstream if different.** Fused wheels or a lost pole means the cart is
assembled in the kit from a generated bed plus procedural wheels, or dropped to
kit entirely. A clean read means the plaza gets its largest dressing silhouette
from one chain.

**Positive prompt (`subject`):**

```
abandoned two-wheeled Castilian ox cart, two solid disc wooden wheels, plain plank bed, long straight draught pole resting on the ground, half loaded with slumped cloth sacks, unhitched and empty, dark oak, deep near-black brown, silvered light-grey weathering on raised grain, matte black wrought iron tyres and nail heads
```

**Negative prompt:** none. Recorded intent: *spoked wheels, oxen, horses,
people, four-wheeled wagon, canvas tilt, crates, barrels, ground plane, road.*

**Premise citation:** §1 evidence of interruption, zero NPCs; §3 dark oak and
wrought iron (both colour clauses verbatim).

**Args:** proposed `height_m 1.6`, `texture_size 2048`, `view_res 1536`,
`tri_budget 16000` (the most articulated subject in the list).

---

### C6 — votive stand, tall pricket

**Chain:** H7. **Premise:** §6 "votive stands flanking the retablo and along
the nave piers: wrought iron, dense with lit candles".

**Decision screened — feasibility, not taste.** Silhouette A of a pair whose
purpose is to answer *whether H7 runs at all*. A slender post on a tripod foot
with one candle tray is the thin-iron case that D1 routes away from generation
for the rejas. If it comes back as a legible stand, H7 proceeds; if it comes
back as a smeared column, the answer is procedural.

**Downstream if different.** A failure here plus a failure at C7 cancels H7
outright and moves votive stands to `build_town_kit.py` as iron curves,
releasing 3 candidates. A pass at C6 alone gives the nave piers their vertical
accent.

**Positive prompt (`subject`):**

```
tall wrought iron votive candle stand, single slender post on a three-legged foot, one round tray at the top holding bright pure white wax candles in iron drip cups, warm candle-gold flames, matte black wrought iron, charcoal-grey worn highlights on edges, sparse desaturated brown rust at the rivets, plain smith work
```

**Negative prompt:** none. Recorded intent: *bright orange rust, brass, gold
metal, scrollwork, church interior background, altar, people.*

**Premise citation:** §6 votive stands; §3 wrought iron (verbatim, including
"never bright orange"); §2 candle-gold 35°–50°.

**Args:** the shipped `candelabra_shrine` entry —`height_m 1.3`,
`texture_size 1024`, `view_res 1024`, `tri_budget 5000`,
`azimuths [0, 60, 180, 300]`, `surface_class painted_metal`. Note
`painted_metal` is `metallic 0.0`; that is deliberate and correct here — the
`iron_wrought` class is `metallic 1.0` with a near-black albedo, which P3.0b
carried to G4 as reading very dark under IBL.

---

### C7 — votive stand, low tiered rack

**Chain:** H7. Same premise clause as C6.

**Decision screened.** Silhouette B: the mass-carrying alternative. Two stepped
horizontal tiers in a heavy square frame on flat feet — every element several
times thicker than C6's post, so if C6 fails on thinness and C7 passes, the
diagnosis is confirmed and H7 runs on B. If both fail, the diagnosis is that
Hi3DGen cannot do dense candle arrays at all, which is a stronger and cheaper
conclusion than discovering it 26 minutes into a chain.

**Downstream if different.** C7 winning changes the chapel's interior read
from vertical accents to low pools of light along the nave floor — a lighting
consequence Phase 4 must know before it places PointLights.

**Positive prompt (`subject`):**

```
low wrought iron votive candle rack, two stepped horizontal tiers of bright pure white wax candles in iron drip cups, heavy square frame on flat feet, warm candle-gold flames, matte black wrought iron, charcoal-grey worn highlights on edges, sparse desaturated brown rust at the rivets, plain smith work
```

**Negative prompt:** none. Recorded intent as C6.

**Premise citation:** as C6.

**Args:** as C6 but `height_m 0.9`.

---

### C8 — gate brazier, lit

**Chain:** H5 re-allocated (§1.3). **Premise:** §1 "the gate brazier"; §5 east
gate arch, "porter's brazier still lit".

**Decision screened.** Whether the brazier is a generable object at all — an
openwork iron basket is a lattice, and a lattice is the second-hardest thing
for a voxel extraction after thin rods. The concept screens the basket: does it
read as a vessel with a wall, or as a solid bowl, or as noise?

**It also screens the campaign's one live colour-law hazard.** A burning
brazier is the single subject in this list that a diffusion model will
instinctively render in the reserved **threat band (hue 350°–25°, S 0.7–1.0)** —
red embers, orange fire. Premise §2 reserves that band absolutely and forbids
it on architecture and props. The prompt pushes hard toward candle-gold, and
the screening criterion (§3) rejects red on sight. This is the concept most
likely to fail its first grid, and finding that out here costs 4 GPU-minutes
instead of a shipped asset that has to be re-textured.

**Downstream if different.** A solid-bowl read means the brazier is a kit
lathe form with a generated coal bed, or kit outright. A red-fire read that
survives re-prompting means the brazier ships **unlit**, with its light coming
entirely from a prefab PointLight — acceptable, but Phase 4 needs to know.

**Positive prompt (`subject`):**

```
wrought iron fire brazier, deep round openwork basket on three splayed legs, burning with a pale warm gold flame, yellow-gold firelight, glowing pale gold embers, matte black wrought iron, charcoal-grey worn highlights on edges, sparse desaturated brown rust at the rivets, plain smith work
```

**Negative prompt:** none. Recorded intent, and the most load-bearing in the
document: *red fire, orange flame, crimson embers, scarlet glow, bright orange
rust, brass, smoke plume, ground plane.*

**Premise citation:** §1 gate brazier; §5 porter's brazier still lit; §3
wrought iron (verbatim); **§2 threat band 350°–25° reserved, candle-gold
35°–50° only**.

**Args:** proposed `height_m 1.0`, `texture_size 1024`, `view_res 1024`,
`tri_budget 7000`, `azimuths [0, 60, 180, 300]`.

---

## 3. Screening rubric

Opus screens 64 images (8 × 8) before any chain runs. **No on-disk instrument
grades a concept PNG** — `color_cast.py` reads a baked candidate's
`final.textures/manifest.json` and cannot be pointed at a concept. The criteria
below are therefore written to be applied to pixels by eye, with an optional
scratch HSV histogram (background excluded) named where a number would settle a
borderline call.

### 3.1 Universal gates — any one failing kills the candidate

| id | gate | how it is read |
|---|---|---|
| **U1** | **One object, fully inside the frame.** | No ground plane, no cast-shadow floor, no second prop, no architectural background. Hi3DGen extracts everything it sees; a floor becomes a slab welded to the prop. |
| **U2** | **Closed silhouette.** | The outline is readable at 128 px. Elements that dissolve into the grey background at thumbnail size will not survive extraction. |
| **U3** | **Material legality.** | Only premise §3 materials visible. **Instant fail** on brick, thatch, half-timber, marble — and on painted or coloured plaster. |
| **U4** | **Ambient-world colour band.** | Non-emissive surfaces read desaturated and mid-dark (§2: S ≤ 0.35, V ≤ 0.6). A candidate that reads as warm sandstone or cream instead of cool pale grey fails — this is the exact drift that produced the arch atlas at R−B +31. |
| **U5** | **Threat band clear.** | No pixel cluster at hue 350°–25° with S ≥ 0.7. Binds hardest on C8 (fire) and anywhere rust appears. §2 reserves this band for telegraphs and it must never appear on a prop. |
| **U6** | **No melted carving.** | Every moulding, bead, arris and joint reads as an *edge* at 100 % zoom, not a smear. This gate is the reason C1 exists: the shipped arch's defect was legible in its own concept and was not caught. |
| **U7** | **Poverty.** | No moulding richer than a single bead; no foliate, heraldic or figural carving; no ecclesiastical grandeur. Rocalba was poor, devout and small (§1). |
| **U8** | **Aniconic in 3D.** | No carved or modelled human or animal figure anywhere in the list. Painted figures on a flat panel are permitted (C2/C3 only). |
| **U9** | **Extractable geometry.** | No unsupported element thinner than ~3 cm at the stated `height_m`; no fully enclosed interior void. |

### 3.2 Per-concept PASS criterion

A candidate PASSES only if it clears all of §3.1 **and** its own criterion.

| slot | PASS criterion |
|---|---|
| **C1** | The arch is a **round** arch; individual voussoirs are countable with visible joints; both springing feet terminate in broken stumps, not clean cuts; the ring is undecorated. |
| **C2** | The three panels are distinguishable from the frame by depth, not only by colour; the frame reads as oak (dark, near-black brown with grey silvered grain), not as gilt; gilt is confined to a thin line. |
| **C3** | The three bays are legible as separate bays at 256 px; the central niche has visible depth (a shadowed interior, not a painted rectangle); the niche is **empty**; the pediment is a plain triangle or a plain cornice, not scrolled. |
| **C4** | The recess is deep enough to shadow its own interior; the hood casts a distinct line; the candle inside is legible as a candle and its flame is gold, not white-hot; the post is plainly square with no plinth mouldings. |
| **C5** | Two wheels, both **solid discs**, both separated from the bed by visible air; the draught pole is a single continuous member touching the ground and is not fused to the bed; the load reads as slumped sacks; no draught animal, no figure. |
| **C6** | The post is a single continuous member from foot to tray with no waisting or breaks; the tripod feet are three distinct legs; at least four candles are individually countable; flames are gold. |
| **C7** | Two tiers are separated by visible air; candles are countable on **both** tiers; the frame members are visibly thicker than C6's post; flames are gold. |
| **C8** | The basket reads as a **vessel with a wall** — an inside distinguishable from an outside; three legs are distinct and meet the basket; **the fire is gold-to-pale-yellow with zero red or orange** (U5, judged strictly here). |

### 3.3 Grid-level decisions Opus records

Screening the 8 × 8 produces four outputs, not one:

1. **Per-concept pass count out of 8.** A concept with **0 or 1** passes is a
   failed subject, not a failed seed — its chain is cancelled and its budget
   released. A concept with ≥ 3 passes is approved and its best candidate's
   `concept.png` is carried forward.
2. **The retablo A/B verdict** (C2 vs C3): exactly one silhouette proceeds to
   H3, and the loser is deleted.
3. **The votive-stand feasibility verdict** (C6/C7): both fail → H7 cancelled
   and votive stands go procedural; one passes → H7 runs on that silhouette.
4. **The brazier colour verdict** (C8): if no candidate clears U5, the brazier
   ships unlit and Phase 4 owns its light.

The approved image is carried into H-chains via
`gen_prop.py --skip-concept <path>`, which copies it in and records its
sha256 — so a chain never silently re-rolls an approved concept.

---

## 4. Dispatch notes — read before running C1

**Negative prompts do not exist in this workflow, and must not be added.**
Node `5` is `ConditioningZeroOut` applied to the *positive* conditioning, and
node `8` samples at `cfg 1.0`. At CFG 1.0 the negative branch is mathematically
unused, so a negative prompt would be inert even if a `CLIPTextEncode` were
wired in its place. Raising CFG to make it live would break the model: Z-Image
**Turbo** is a distilled 8-step sampler whose operating point *is* cfg 1.0, and
it would also roughly double the run's wall time. The "Negative prompt: none"
lines above are the honest state, and every exclusion is carried instead by
affirmative prompt wording plus the §3 screening criteria.

**Do not dispatch C1 through `gen_prop.py`.** Two reasons:

1. **Cost.** `stage_concept` opens `comfy_run.server()` *per seed*
   (`gen_prop.py:126`, called once per seed from the loop at `:310`). Eight
   concepts × eight seeds = **64 ComfyUI cold starts**, each reloading Z-Image
   and the Qwen3-4B encoder. At ~30 s of sampling per seed the plan's 35-minute
   budget has no room for 63 redundant model loads; the estimate only holds
   with **one resident server for the whole run**.
2. **Registry.** `gen_prop.py --asset` resolves through
   `proptex.registry.resolve`, which refuses any name absent from
   `assets.json`. Five of these eight subjects are not registered and **should
   not be** until they are approved.

The correct C1 dispatch is one ComfyUI server held up for the run, with
`comfy_run.run_workflow` submitting 64 prompts against it — the concept
workflow with node `4`'s `text` set to `"<subject>, single object centered,
plain grey background"` and node `8`'s `seed` set per submit. Keep
`batch_size: 1`, `steps: 8`, `cfg: 1.0`, `res_multistep/simple`, 1024²
unchanged: that is the exact operating point every shipped concept was drawn
at, and C1 is a screening run, not the place to move it.

Suggested layout: `target/prop-batch/c1/<slot>/seed_<n>.png`, one
`manifest.json` per submit (`comfy_run` writes it), so provenance is intact
without any new script.

`gen_prop.py` remains the right tool for H1..H7, where its per-stage server
lifecycle exists to keep ComfyUI out of VRAM while Hi3DGen runs.

---

## OPEN

**OPEN-1 — the released GPU budget.** Cancelling H2, H5-as-doors, and two
thirds of H6 releases ~2.4 h of the approved 5.5 h. This document spends none
of it beyond raising H3 from 4 to 6 candidates. The surplus can be banked, or
spent on a second H-pass for whichever class G3 scores worst. **Decision is the
user's** (it is scope), but no decision is needed *before* C1 — the run is
unaffected either way.

**OPEN-2 — period-correct dressing to replace the crate.** §1.4 cancels the
crate as an anachronism as well as a plain form. The period-correct
alternatives — slumped grain sacks, a wicker pannier, a stacked basket pile —
are genuinely generation-shaped (irregular, organic, no mating contract, no
repeated-form problem) and would be strong heroes. But **the premise names
none of them**, and inventing assets to spend a released budget is exactly the
padding this list refuses. Raised, not slotted. Note that C5's cart is already
prompted with sacks as its load, so the screen will incidentally show whether
sacks generate well.

**OPEN-3 — `shrine_pillar` versus the existing `crucero`.** `assets.json`
already carries `crucero` ("weathered stone wayside cross", 3.5 m) and
`gravestone` ("weathered stone wayside cross, carved religious stele", 1.5 m) —
two generated assets with nearly identical subject strings, both already
installed. C4 adds a third wayside stone object to the same approaches. I
believe the hooded-recess pillar is visually distinct enough to earn its place
(the crucero is a cross on a shaft; this is a post with a lit niche), and the
candle inside is a premise beat the crucero cannot carry. But if the approaches
already read as crowded at zone_review, C4 is the cheapest of the eight to
drop. Flagged for the screen, not blocking it.

**OPEN-4 — premise §6 does not name the votive stand's form.** It says
"votive stands ... wrought iron, dense with lit candles" and nothing about
height or arrangement, which is why C6/C7 exist. If the user has a picture in
mind, saying so before the run collapses two slots into one and frees a slot
for OPEN-2's sacks. Not blocking: the two-silhouette screen is a valid way to
settle it without asking.
