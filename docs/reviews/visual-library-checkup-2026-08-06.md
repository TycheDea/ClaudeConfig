# Visual library checkup — 2026-08-06

**Kind:** fast library-wide visual grade (not a G3 ship gate).  
**Judge:** interactive session (pi / Grok path); eyeball only.  
**Bar:** AA semi-realistic religious dark fantasy (VQ-A1+) + Rocalba premise.  
**Evidence:** on-disk frames listed in §Evidence. Mostly studio turntables =
**compare-only** under `memory/visual-verification.md` (turntables never clear
a ship). Zone sheet and kit street previews are closer to in-world read.

**Purpose:** snapshot of how good shipped / staged models look *now*, so
migration and campaign priority have a written baseline. Re-run after major
prop/kit/character landings; do not treat scores as frozen law.

---

## 1. Scale

| Score | Meaning |
|------:|---------|
| 1–3 | Blocks AA read / wrong subject or register |
| 4–5 | Direction only; material or geo fails at gameplay |
| 6 | Usable far/mid; fails macro honesty |
| ≥7 | Directionally shippable on that axis (still needs real gate) |
| 8–9 | Near reference / kit ceiling |
| 10 | Photoscan-class (reserved) |

Overall column ≈ mean of axes with extra weight on **material honesty** and
**AA register**.

---

## 2. Evidence used

| Path | What |
|------|------|
| `target/b3-install-review/{chapel_arch,broken_column,stone_cross,crucero,olive_stump,cypress}/contact_sheet.png` | B3 prop turntables |
| `target/b3-install-review/chapel_arch/frame_00.png` | Arch macro side |
| `target/candelabra-review/contact_sheet.png` | Candelabra turntable |
| `target/char-mpfb/cand_mpfb/turntable_idle/contact_sheet.png` | MPFB monk |
| `target/detail-phase/after/zone/contact_sheet.png` | Zone / scale sheet |
| `target/cypress-build/preview.png` | Procedural cypress rebuild |
| `target/kit-rebuild/raw/previews/{casa_small_a_street,chapel_street,gate_arch}.png` | Kit buildings |
| `content/models/townkit_textures/{encalado_diff,terracotta_tile_diff}.png` | Kit albedos |

Not used: fresh `asset_inspect` gameplay packs, G3 blind sets, live sandbox.

---

## 3. Hero props (generated)

| Asset | Subject / sil. | Geo fidelity | Material honesty | Micro-detail | Color / cast | Premise fit | Cohesion w/ kit | **Overall** | One-line |
|-------|---------------:|-------------:|-----------------:|-------------:|-------------:|------------:|----------------:|------------:|----------|
| gravestone | 8 | 7 | 6 | 6 | 5 | 8 | 6 | **7** | Best gen prop; clear stele+cross; still warm/plastic |
| crucero | 8 | 7 | 7 | 6 | 6 | 9 | 7 | **7** | Clean wayside cross; simplest = most honest stone |
| broken_column | 8 | 6 | 6 | 5 | 5 | 8 | 6 | **6** | Readable ruin; melted flutes; amber studio look |
| chapel_arch | 8 | 5 | 5 | 4 | 4 | 7 | 5 | **5** | Strong icon; clay-melt + gold flecks kill limestone |
| olive_stump | 7 | 7 | 4 | 6 | 4 | 6 | 5 | **5** | Cool root mass; waxy/metal wood ≠ grey olive |
| candelabra_shrine | 7 | 5 | 3 | 4 | 3 | 5 | 4 | **4** | Shape OK; chrome/pewter ≠ dark iron shrine |
| cypress (old B3 sheet) | 3 | 2 | 3 | 2 | 4 | 2 | 2 | **2** | Cauliflower blob — correctly retired |
| cypress (rebuild preview) | 8 | 7 | 6 | 6 | 5 | 8 | 7 | **7** | Right column + needle cards; preview value still rough |

### Prop ranking (best → worst)

1. crucero / gravestone (tie band)  
2. broken_column  
3. cypress rebuild  
4. chapel_arch / olive_stump  
5. candelabra_shrine  
6. old B3 cypress (do not ship)

---

## 4. Buildings / kit (hybrid procedural)

| Asset | Massing | Hard edges | Material set | Texel / tiling | Wear | Premise | **Overall** | One-line |
|-------|--------:|-----------:|-------------:|---------------:|-----:|--------:|------------:|----------|
| casa_small_a | 8 | 8 | 8 | 7 | 5 | 8 | **8** | Whitewash + terracotta read Castilian; a bit “new” |
| gate_arch (kit) | 8 | 8 | 7 | 7 | 5 | 8 | **8** | Clear town gate; block stone legible |
| chapel (kit) | 8 | 8 | 7 | 6 | 5 | 8 | **7** | Right ruined-chapel mass; ashlar a bit regular |
| townkit textures (encalado / terracotta) | — | — | 8–9 | 8 | 7 | 9 | **8** | Strongest pure materials in the project |

**Conclusion:** kit path is the quality ceiling for architecture. Confirms D1
(hybrid buildings; Hi3DGen heroes only when small).

---

## 5. Characters

| Asset | Silhouette | Proportions | Surface | AA register | Combat read | **Overall** | One-line |
|-------|-----------:|------------:|--------:|------------:|------------:|------------:|----------|
| human_gen (MPFB monk) | 7 | 6 | 4 | 3 | 6 | **4** | Hooded monk reads; mannequin cloth, not semi-real AA |
| human / dwarf / elf / valkyrie (KayKit-era) | — | — | — | **1–2** | — | **placeholder** | Rejected art direction; not target look |
| zone mannequin | 2 | — | 1 | 1 | 5 | **ref only** | Scale stick, not content |

**Conclusion:** character track is furthest from the bar.

---

## 6. Scene / set (zone contact sheet)

| Element | Gameplay read | Scale vs player | Lighting response | Set cohesion | **Overall** |
|---------|--------------:|----------------:|------------------:|-------------:|------------:|
| cracked earth ground | 8 | 8 | 7 | 7 | **8** |
| photoscan rock | 8 | 8 | 8 | 8 | **8** |
| gen props @ distance | 6–7 | 7 | 5–6 | 5 | **6** |
| old cypress in sheet | 3 | 5 | 4 | 2 | **3** |
| full zone as AA town | 4 | 6 | 5 | 4 | **4** |

**Conclusion:** ground + rock carry the plate; full zone is not yet a town.

---

## 7. Cross-cutting library grades

| Property | Score | Note |
|----------|------:|------|
| Subject identity | **7** | Arch, cross, stele, casa read fast |
| AA semi-realistic bar (VQ-A1) | **4** | Kit materials approach; Hi3DGen heroes mostly don’t |
| PBR honesty | **4** | Ghost gold, wax wood, chrome iron |
| Micro-detail @ ~1–2 m | **4** | Noise ≠ carved stone / wood fiber |
| Hard architectural edges | **3 gen / 8 kit** | Pipeline split is obvious and correct |
| Color discipline (bleached, low chroma) | **4** | Studio amber + warm zone fight overcast lock |
| Premise / religious dark fantasy | **6** | Symbols right; finish often “gen showcase” |
| Cohesion (one world) | **5** | Kit vs gen vs character = three registers |
| Ship-ready hero props | **5** | Gravestone/crucero closest |
| Ship-ready buildings | **7–8** | Best path |
| Ship-ready player | **3–4** | Off the AA curve |

---

## 8. Shared defects (ordered by eye cost)

1. **Warm plastic stone** on gen props (amber albedo + soft specular).  
2. **Melted Hi3DGen silhouettes** (chapel_arch profile especially).  
3. **Wrong BSDF class** (chrome candelabra, metallic stump).  
4. **Gold/metal flecks** on limestone (arch).  
5. **Three art registers** in one frame: kit buildings / gen props / mannequin player.

---

## 9. Bottom line

The library is **not** a coherent AA town yet. It is three tracks:

| Track | State | Priority implication |
|-------|--------|----------------------|
| **Kit buildings + townkit materials** | Strongest; directionally AA | Keep investing; wear/aging pass |
| **Generated hero props** | Mixed; 2–3 near-OK, several material fails | Fix material honesty before more subjects |
| **Characters** | Prototype / rejected placeholders | Separate campaign; don’t mix into town gates |

**Closest to good:** casa/gate + terracotta, crucero/gravestone, ground/rock, cypress rebuild direction.  
**Furthest:** old cypress blob, candelabra metal, player mesh, chapel_arch at macro.

---

## 10. Follow-ups (optional; not a queue)

- Stricter re-grade: gameplay-distance `asset_inspect` only (studio + ship + albedo) for shortlist: crucero, gravestone, chapel_arch, candelabra, cypress rebuild, casa_small_a.  
- Do not use this doc as a G3 pass — run `tasks/town/p33-g3-gate.md` (or successor) for ship.  
- When scores move, append a dated §Delta section here or write `visual-library-checkup-YYYY-MM-DD.md` and leave this file as baseline.

---

## 11. Related

- Bar: `docs/visual-quality.md`  
- Premise: `docs/town-premise.md`  
- Verification rules: `memory/visual-verification.md`  
- Art direction lock: `memory/aa-art-direction.md`  
- Example ship gate: `tasks/town/p33-g3-gate.md`  
- Prop gate records: `docs/reviews/props/`  
