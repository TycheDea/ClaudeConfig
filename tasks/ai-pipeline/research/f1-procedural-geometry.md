# F1 — Procedural geometry: can non-AI authoring beat generative AI for 150 armor variants?

Research date: 2026-07-21. Structure and sourcing discipline follow `c1-texturing-geometry.md`:
every license clause and price is fetched from the vendor's own pricing/EULA page or a repo's own
LICENSE/API wherever one exists; every capability claim is checked against a primary document
(Blender's own release notes, a project-tracker PR) where one exists; anything that only turned up
in a marketing blog, forum aggregation, or WebSearch summary is labeled **[secondary]** and never
used as the sole basis for the verdict. EUR figures are **approximate USD→EUR conversions
(≈0.92, not independently sourced this pass)** unless a vendor's own EUR price is quoted directly —
flagged inline every time.

**This report reframes the question it was asked to answer, and says so up front, per this
project's own standing rule that a wall in the plan is information, not an obstacle to route
around.** The brief (and `BACKLOG.md`'s F1 entry) frames this as "Geometry Nodes vs. generative
AI." Both the primary-source capability research below and every real shipped-game precedent found
say that framing is not where the actual decision lives. Read the Verdict section first.

**Verification pass (2026-07-21, orchestrator).** Blender 5.2 confirmed as the project's actual
version (`scripts/ai-pipeline/gen_prop.py:43`). The report's own stated main open risk — "whether
the engine's material system already supports per-zone tint uniforms" — was resolved by reading the
renderer, and the answer changes the recommended mechanism. See § Verification.

---

## Verdict up front

**Neither "Blender Geometry Nodes" nor "generative AI" is the right unit of comparison. The
option that actually wins 150-variants-over-10-shells is a mechanism neither name describes: a
shared material-ID/tint-mask shader system plus Python-driven combinatorial reassembly of a
hand-modeled trim/kit-piece library.** This is not a hedge — it is a specific, ranked,
falsifiable claim, argued below.

**1. Which approach wins, and by what margin?** Material-ID tinting + modular kit assembly wins,
by a decisive margin, for the ~70-90% of the 150-item matrix that is genuinely a *variant*
(same silhouette family, different material/color/trim) rather than a new hero shape. Its marginal
cost per variant is a shader-parameter change plus a rendered contact sheet for QA — no GPU job,
no new mesh, no new UV bake. This is not a novel proposal; it is the confirmed shipping mechanism
behind Guild Wars 2's dye-channel system and Dawn of War 2's team-color RGBA masks (both verified
below), and it is what the one directly-comparable commercial asset kit found in this pass
(Unreal Marketplace's "Fantasy Modular Armor Sets" — 21 sets, 6 parts each, explicit
tint-compatible palette) is built around. **Geometry Nodes wins, by a real but much smaller
margin, for the remaining 10-30% of the matrix that needs an actual silhouette change** (a
different pauldron count, a longer tabard, relocated rivets) — there it is the correct tool for
*parameterizing* variation on top of hand-authored parts, not for authoring the parts themselves.
**Generative AI geometry (image-to-3D applied to armor shapes) does not clear the bar at all** —
see finding 2. **Generative AI texturing (C1's domain) is not competitive with tinting for the
color/material axis** because tinting is strictly cheaper (zero GPU-seconds vs. C1's own measured
~3 min/4-view Z-Image pass) and, being a shader parameter rather than a rendered image, is
consistent across all 150 variants *by construction* — the exact property C1 could not deliver.

**2. Where is the crossover point?** **The crossover-point framing itself does not survive
contact with the geometry-side evidence, and that is the single most important finding in this
report.** `BACKLOG.md`'s F1 entry assumes AI-geometry-per-variant is a real alternative whose
cost crosses procedural's fixed cost at some variant count N (it guesses "30+"). It isn't: AI
image-to-3D geometry generation (Hi3DGen-class, already the project's own cleared production
backbone per `scripts/ai-pipeline/README.md`) produces unstructured, non-quad, high-triangle-count
meshes with no relationship to an existing skeleton. This project's own architecture requires
every garment/armor mesh to bind to the shared body skeleton through MPFB2's `.mhclo` proxy format,
which needs either a nearest-surface-point weight transfer (works on *arbitrary* clean topology
draped near the body) or an explicit hand-authored `weights.json` (works on *any* topology, at the
cost of manual weighting) — confirmed by the MakeHuman Community's own documentation
([mpfb2 issue #64](https://github.com/makehumancommunity/mpfb2/issues/64),
[Rigging Mesh Assets](https://static.makehumancommunity.org/mpfb/docs/rigging_mesh_assets.html)).
A raw image-to-3D output satisfies neither path without a full manual retopology-and-reweight
pass *per variant* — at which point the AI stage has saved nothing, because that manual pass is
the same labor a hand-modeled variant would have needed anyway. **There is no N at which
AI-geometry crosses over, because it never clears the technical bar in the first place — this
isn't a cost comparison, it's a disqualification.** The crossover that *does* exist and matters is
procedural/kitbash's fixed authoring cost (the parts library + tint-mask shader graph, built once)
against hand-modeling every one of the 150 pieces individually — and that crossover sits at
**the second variant of any shell**, i.e., already paid back at this project's committed scale
(10 shells × 15 variants each) before a single variant ships. No sourced, per-hour "procedural
authoring cost" figure for armor specifically exists (flagged, see Gaps) — this is a structural
argument from marginal cost, not a benchmarked number, and is reported as such.

**3. Is the honest answer a hybrid, and what's the division of labour?** **Yes, and the split is
precise, not "some of both":**
- **Procedural (Python + Geometry Nodes), doing the geometry and the material-zone plumbing**:
  author ~10 base shells and a shared hard-surface trim/kit-piece library once (buckles, rivets,
  scroll-edge trim, pauldron variants) by hand in Blender (ZBrush-adjacent hand-sculpting is still
  the right tool for the *hero* shapes — every AAA precedent found does this, see § "Blender
  Geometry Nodes"); write a Python script (in the same `--background --python` idiom already used
  four times in `scripts/ai-pipeline/`) that (a) assigns each mesh island a material-ID channel
  (metal-primary / metal-secondary / cloth-leather / trim-accent — the same four-channel convention
  Dawn of War 2 shipped, confirmed below), (b) combinatorially swaps/repositions kit pieces along
  the shell's attachment points, and (c) drives MPFB2's existing `.mhclo` proxy/weight-transfer
  step per generated variant.
- **AI (C1's own Z-Image stack), doing color and one-off hero authoring only**: a tint LUT or
  4-color palette per variant (no per-variant GPU job needed at all — this is a shader uniform, not
  a generation), reserved for the smaller set of *unique* hero/legendary pieces the design calls
  for genuine one-off texture authorship, using exactly the sequential-img2img fix C1 already
  specified.
- **Normal-map surface detail stays a real Cycles high-to-low bake** (unchanged from the existing
  `prop_texture.py` convention) regardless of which layer above produced the base mesh.

**4. Effect on C1's recommendation.** **C1's sequential-img2img fix is not made moot — its scope
shrinks, and its priority drops.** C1 already flagged, in its own words, that "every candidate in
this report... solves at best cross-view consistency... None of them solve cross-variant
consistency across the ~150 armor variants" and predicted that if F1 turned out competitive, "AI
texturing survives only for the smaller subset of hero/unique props." That is exactly this
report's finding. C1's fix remains the correct one-day change *for that smaller subset* — hero
pieces still get independently AI-textured views, and those views still disagree with each other
under the incumbent's `seed*100+i` scheme, so the fix is still worth doing. But it is no longer the
mechanism carrying the 150-item art book's coherence; the tint-mask/kit system carries that, by
construction, before C1's fix is ever invoked. **Sequencing recommendation: build the F1 parts
library + tint shader first (it is the critical path for the 150-variant goal); implement C1's
sequential-img2img fix whenever hero-prop texturing work is next scheduled, not before.**

**What would falsify this**: (1) a hands-on prototype of the tint-mask shader on this project's
actual PBR pipeline finds the metallic/roughness split can't be cleanly separated per material
zone (the same measurement problem A6.1 already found for *auto-detecting* metal vs. non-metal —
worth checking, since tinting assumes zones are already known/authored, which sidesteps A6.1's
problem, but this hasn't been verified hands-on); (2) MPFB2's nearest-surface weight transfer
produces visibly broken deformation on a genuinely novel silhouette (a long cloak, a wide pauldron)
that a hand-authored `weights.json` would have avoided — this is a real, unresolved risk flagged
in Gaps, not dismissed.

---

## Why the brief's framing needed correcting — the load-bearing technical fact

MPFB2's clothing/proxy format (`.mhclo`) is explicitly **the same file format and pipeline for
clothes, hair, and body-part proxies** — MakeHuman's own FAQ states "clothes is a broad term that
encompasses not only clothing per se, but all mesh assets such as hair, body parts, and proxy
meshes... proxies are pretty much the same things as clothes" and that a proxy "could optionally
include a weight file with manually polished weighting," loaded on top of an interpolated default
([mpfb2 issue #64](https://github.com/makehumancommunity/mpfb2/issues/64)). This is a
**spatial-proximity weight-transfer system**, not a fixed vertex-correspondence rig: any mesh that
drapes near the body surface can be weight-transferred automatically, regardless of its exact
topology or vertex count, as long as it's clean enough to weight sensibly. That single fact is why
procedural/kitbash geometry is a structurally sound fit for this pipeline (every generated variant
re-enters the same proxy step every other garment already uses) and why raw AI-generated meshes are
not (they are neither clean-enough topology for a good automatic transfer, nor pre-supplied with a
`weights.json` — confirmed by the general image-to-3D rigging literature: "if edge loops don't
follow joint areas... deformation will look broken," "triangles cause shading artifacts and
skinning issues," full remesh-to-quad passes are the stated fix
**[secondary, aggregated practitioner/vendor guidance, not specific to this project's meshes]**).

Note for the record: `scripts/ai-pipeline/README.md` (read in full for this pass) does not yet
document an MPFB2/`.mhclo` automation stage — the character/garment pipeline (`BACKLOG.md`'s D1-D4)
hasn't run yet. This report designs the future stage per the project context given in the brief; it
is not patching a live script the way C1 patched `prop_texture.py`.

---

## Options table

| Option | License / cost (solo EU dev) | Compute (12 GB fit?) | Wall-time / variant | One-time authoring cost | Maturity | Verdict |
|---|---|---|---|---|---|---|
| **Material-ID / tint-mask shader system** | €0 (a shader + a Python export tag) | Trivial — CPU, no inference | Seconds (parameter change + render QA) | ~1-2 days per shell (author 4 material-ID zones + a tint shader) | Production-proven since ≥2009 (Dawn of War 2) | **Winner, color/material axis** |
| **Kitbash / modular parts-library assembly (Python-driven)** | €0 (reuses existing `bpy`/headless-Blender idiom) | Trivial | Seconds-to-minutes (script run) + manual QA pass | Days-to-weeks (hand-model the trim/kit library once) | Real, shipped at asset-store tier; not confirmed at D4/PoE2 hero tier | **Winner, silhouette axis** |
| **Blender Geometry Nodes** | €0 (built into Blender 5.2, already installed) | Trivial (viewport-cost only, no VRAM contention with AI stages) | Seconds per variant once graph exists | Node-graph authoring: hours-to-days per parametric family | GN core is production-proven for procedural scatter/detail; hard-surface-specific gaps still closing (see below) | Tool for parameterizing #2, not for hero-shape authoring |
| **Blender Python scripting** | €0 | Trivial | N/A (glue layer) | Low — reuses existing repo idiom | Production-proven (this project already runs 5+ headless-Blender Python scripts) | Required glue for #1 and #2 |
| **Generative AI geometry (image-to-3D on armor)** | Free-to-rented, but see verdict | Fits 12 GB (Hi3DGen already does) | ~minutes/variant, **before** the disqualifying rework | N/A — disqualified before cost matters | Production-proven for standalone props (this project's own A3 fixture); **not evaluated for rigged garments** | **Disqualified** — topology/rigging mismatch |
| **Substance 3D (Designer/Painter/Sampler)** | $24.99/mo or $249.88/yr (Texturing plan) ≈ €23/€230; Painter perpetual $199.99 ≈ €185 | Trivial (material-side, no inference) | N/A (materials, not geometry) | Learning curve, days | Industry-standard, decades mature | Relevant to F2, not F1's geometry axis |
| **Material Maker** | €0, MIT, open source | Trivial | N/A | Days (learning + graph authoring) | Active, 5.7k★, v1.7 shipped July 2026 | Free Substance-adjacent option, F2's territory |
| **ArmorLab / ArmorPaint** | ArmorLab: dead since 2023; ArmorPaint: alive, GPL-adjacent, ~$19-40 | Trivial | N/A | N/A | ArmorLab archived; not an armor-geometry tool at all | **Naming correction — not a geometry option** |
| **Houdini (Indie)** | $299/yr ($449/2yr) ≈ €275/yr, capped at $100K revenue / $1M funding | Trivial (CPU-bound, same class as Blender GN) | Seconds-to-minutes once HDA exists | Second DCC to learn; days-to-weeks | Production-proven industry-wide for procedural work | Non-starter for this codebase — see below |
| **Sloyd.ai** | Plus $11-15/mo ≈ €10-14, Pro $50/mo ≈ €46 | N/A (cloud service) | Seconds (real-time parametric) | None (rented parametric templates) | Real, funded (a16z Speedrun, NVIDIA-recognized), young | Wrong register + no MHCLO integration — watch item |
| **Hybrid (procedural geometry + AI texturing)** | Sum of the above, mostly €0 | Fits 12 GB | Mixed per layer | Mixed per layer | — | **Recommended architecture** |

---

## Per-option assessments

### Material-ID / tint-mask shader variant system — the option the brief's list didn't name

**Extended description**: instead of generating or painting a distinct texture per variant, author
one shared texture set per shell with a grayscale/RGBA **mask** channel that assigns each pixel to
a material zone (e.g., red = primary metal, green = secondary metal/trim, blue = cloth/leather,
alpha = accent/filigree), then drive the *actual* per-variant color, metalness, and roughness for
each zone as shader uniforms (or a small per-variant lookup texture) at render/bake time. The base
albedo/normal/roughness texture is authored once per shell; the 15 variants of that shell differ
only in the mask-to-material mapping.

**Underlying technology**: a 4-channel mask texture (already a natural fit for this project's own
declared-constant MR convention from A6.1 — the mask replaces "one global metallic/roughness
constant per prop" with "one constant per material zone per variant," a strict generalization, not
a new mechanism) plus either an engine-side shader (ideal — zero bake cost, purely data-driven) or
a bake-time compositing step if the engine's material system doesn't support per-zone tinting yet
(this project's renderer support was not checked in this pass — flagged as a scope item for
whoever implements this, not a research gap).

**License + real cost**: **€0.** This is a shader technique and a texture-authoring convention, not
a licensed product. The only cost is artist time to author the mask and pick material-zone counts
per shell — a few days per shell, once.

**Compute/VRAM**: trivial. No inference, no GPU job of any kind for the variant step itself (only
for authoring the one shared base texture per shell, which can use the existing C1 stack or be
hand-painted).

**Wall-time per variant vs. one-time authoring cost**: per-variant cost is **seconds** — pick 3-4
colors and metal/rough values per zone, render a contact sheet, done. One-time cost is authoring
the mask (part of building the shell's texture set, not additional work beyond what any textured
shell needs) plus, if the engine doesn't already support per-material-zone tinting, an engine-side
shader feature (a real but bounded engineering cost, not researched further here — out of scope for
a research-only pass).

**Pros**: zero marginal GPU cost; **guarantees cross-variant consistency by construction** — this
is precisely the axis C1 could not close and this bullet exists to answer; trivially art-directable
(a human picks the palette, sees it instantly, iterates); composes with every other option in this
report (the mask can sit on a hand-sculpted shell, a kitbashed shell, or a Geometry-Nodes-varied
shell equally well).

**Cons**: does not by itself create silhouette variety — a straight reskin of the same shape reads
as "the same armor in a different color" past some variant density, which is exactly why the
industry pairs it with modular kitbashing (below) rather than using it alone; requires the base
shell's texture to be authored with zone boundaries in mind from the start (retrofitting zones onto
an already-baked texture is possible but wasteful — this needs to be a day-one decision for each
shell's texture pass, not an afterthought).

**How much worse than a human artist, and where**: for the *specific* task of "produce a coherent
color/material variant of an already-designed shell," this is not worse than a human artist —
it *is* what a human artist would do (a technical artist picks the palette; nothing about picking
three colors well benefits from more manual labor). It is meaningfully worse than a human artist
at *designing a genuinely new silhouette*, which it doesn't attempt to do — that's the kitbash
option's job, not this one's.

**1-2 shipped games at comparable quality, with what their pipeline actually was**:
- **Guild Wars 2** (ArenaNet, shipped 2012, live-serviced through 2026): every piece of armor has
  1-4 dye channels, each a distinct region a player can independently recolor; the wiki's own
  description of "up to four colors... each color confined to a specific area" is the player-facing
  face of exactly this mask-driven mechanism
  ([wiki.guildwars2.com/wiki/Dye](https://wiki.guildwars2.com/wiki/Dye)). Not confirmed at the
  shader/texture-format level from a primary ArenaNet source in this pass (no dev blog or GDC talk
  on the underlying tech was found — flagged in Gaps) — the mechanism description here is inferred
  from the player-facing behavior, which unambiguously implies a mask, not per-variant painted
  textures (four independently recolorable regions per item × the game's item count would be
  infeasible any other way).
- **Dawn of War II** (Relic Entertainment, shipped 2009): confirmed via a primary technical
  artifact — a community-maintained tool
  ([github.com/Jaccouille/dow2-texture-painter](https://github.com/Jaccouille/dow2-texture-painter))
  whose own description states "the team color file contains RGBA color masks which are necessary
  for mapping the colored part of the diffuse texture" — this is the RGBA-mask-per-material-zone
  mechanism this section describes, shipped and moddable in a real RTS/hack-and-slash-adjacent
  title. Not an ARPG and not D4/PoE2-tier fidelity, but the mechanism itself is identical and the
  source is a working tool, not a claim.

**Maturity flag**: **production-proven, and has been for over 15 years** (DOW2 shipped 2009; GW2
shipped 2012 and the dye system is still live in 2026). This is the most mature option in this
entire report by a wide margin — more mature than any AI method in C1, more mature than modern
Geometry Nodes.

---

### Kitbash / modular parts-library assembly (Python-driven combinatorial reassembly)

**Extended description**: build a library of hard-surface trim pieces (rivets, buckles, clasps,
scroll-edge trim, pauldron variants, hem shapes) once per shell family, hand-modeled to the same
D4/PoE2-register quality bar as the hero shells themselves, then write a Python script that
combinatorially selects, scales, and attaches a subset of that library onto each of the 10 base
shells to produce silhouette-level variety, before the tint-mask system (above) handles color.

**Underlying technology**: this is not a single piece of software — it's a data-driven assembly
convention implemented as a headless-Blender Python script, structurally identical to
`gen_prop.py`'s existing chain pattern (`scripts/ai-pipeline/gen_prop.py`): a manifest describing
which kit pieces attach to which socket on which shell, a script that instantiates and merges them,
then hands the result to the same MPFB2 `.mhclo` export step every hand-modeled garment already
goes through. Commercially, the closest packaged example of exactly this idea is Unreal
Marketplace's **"Fantasy Modular Armor Sets"**: 21 armor sets across heavy/medium/light weight
classes, each with 6 parts (head/shoulder/chest/arms/legs/feet), with an explicit "tint coloring
system... so colors of set pieces will be compatible with each other"
**[secondary, WebFetch of the product page returned HTTP 403 — this description is from a search
snippet, not independently re-verified against the listing itself in this pass]**. That pack
combines this section's mechanism with the previous section's tint system in exactly the
combination this report recommends — real evidence the two-layer approach is a known, packaged
commercial pattern, not a novel proposal.

**License + real cost**: **€0 for the technique itself** (it's a Python script pattern, not a
licensed product). If the marketplace kit above (or similar: "RoE Medieval fantasy modular
character," "Modular Heavy Armour") were used as a reference/study asset rather than shipped
content, its license (Fab Standard License, successor to the legacy UE Marketplace License) is
**engine-agnostic per Epic's own documentation summary** — "usage is not limited to Unreal
Engine... can be used with any compatible tools"
([dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab](https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab))
**[secondary — Epic's summary page, not the binding EULA text itself; `fab.com/eula` returned a
Cloudflare JS challenge to both WebFetch and a scripted `curl` fetch in this pass and could not be
read directly]**. Two caveats found: (1) assets migrated from the old UE Marketplace may still
carry a "legacy UE Marketplace License" with different (possibly engine-restricted) terms —
verify per-listing before relying on any specific pack; (2) **this project's own art-direction
mandate is that designs must be unique and not sourced from any existing asset ecosystem** (per
project context) — a marketplace kit's actual meshes are therefore not shippable content
regardless of license terms, only a reference for building an in-house-original parts library. Not
independently priced in this pass (the product page 403'd before a price could be extracted).
Separately, **KitBash3D** (the most prominent kitbash marketplace brand, $59-99/mo ≈ €54-91,
commercial license included with no per-project fee, per
[kitbash3d.com/pages/pricing](https://kitbash3d.com/pages/pricing)) was checked specifically and
**carries no character/armor kits at all — it is environment- and prop-only**
("20,000+ textured models... 300+ hero props/vehicles" — no armor/character category on its own
pricing page). This is a genuine negative-space finding: the kitbash-marketplace industry has not
built a "buy an armor trim library" product the way it has for environment art.

**Compute/VRAM**: trivial — CPU-side mesh assembly, no inference of any kind.

**Wall-time per variant vs. one-time authoring cost**: per-variant assembly is a script run —
seconds, matching the general-purpose Geometry-Nodes-to-Python claim found for prop variants ("one
node graph can generate dozens of prop variants... a Python workflow can scale to 50 variants in
seconds instead of 50 manual export sessions" **[secondary, BitSoul/general-purpose blog claim, not
independently benchmarked against this project's own meshes in this pass]**). The one-time cost is
the real investment: hand-modeling a trim/kit-piece library at D4/PoE2 fidelity is the same class
of labor as hand-modeling any hero prop — **no sourced hours-per-piece figure specific to trim
pieces was found**; the closest proxy figure found (armor-piece full-pipeline authoring, "20-40
hours for a single complex prop or armor piece... traditional pipeline"
**[secondary, an AI-tool marketing blog (triverse.ai) with an obvious incentive to make manual
authoring look expensive — treated with corresponding skepticism, not load-bearing]**) is for a
*complete* hero piece via full ZBrush→retopo→bake pipeline, not a small trim element, so it likely
overstates per-piece kit-trim cost substantially. **Flagged: no reliable, unbiased source for
"hours to model one trim/kit piece" was found in this pass** — this is a real gap, not a resolved
number.

**Pros**: this is the mechanism that actually produces *silhouette* variety (not just recolors),
which the tint-mask system alone cannot; every generated variant re-enters the same MPFB2 export
step every hand-modeled garment already uses, so no new engine-side or rigging work is needed; the
Python glue is a direct, low-risk extension of a pattern this project already runs four times over.

**Cons**: the one-time library-authoring cost is real hand-modeling labor at hero-prop quality, not
a shortcut around it — this option does not reduce the *total* amount of hand-authored geometry
needed nearly as much as "procedural" sounds like it should; it reduces the amount needed **per
final variant**, by amortizing a fixed library across many combinations. Combinatorial assembly can
produce visually incoherent results if attachment sockets and scale rules aren't curated
carefully — this is a design/QA cost, not a licensing or compute one, and was not measured in this
pass (no hands-on prototype was run, per the brief's no-generation-workloads instruction).

**How much worse than a human artist, and where**: **not worse at all for genuinely combinatorial
variety** (a human artist doing the same "10 shells, swap the trim" job would write the same kind
of assembly logic manually in the DCC, just slower); it is worse than a human artist specifically
at **judging when a combination doesn't read well** — a trained eye catches "these two trim pieces
clash" faster than any rule-based script does, so a human QA pass per generated variant (fast — a
turntable render and a glance, the same review step `gen_prop.py`'s pipeline already performs) is
still required and is the correct division of labor, not a gap to be automated away.

**1-2 shipped games at comparable quality, with what their pipeline actually was**: **this is the
report's most important negative-space finding.** No primary source in this pass confirmed that
Diablo IV's or Path of Exile 2's *character armor* (as opposed to environment art) is produced via
a kitbash/parts-library system. Diablo IV's own GDC 2024 talk ("The Art of Open World Sanctuary")
describes exactly this modular-kit methodology, but explicitly for **environment tile-sets and
props** ("a variety of tile-sets that could be cleverly reused and paired with different props...
culture kits like the Drowned kit" — **[secondary, ArtStation summary of the talk, not the GDC
Vault recording itself]**). Independently, breakdowns of Diablo-IV-inspired character work describe
a **fully hand-sculpted** pipeline — "utilized the first subdivision from ZBrush," baked in
Substance 3D Painter, cloth elements "manually sculpted... for more freedom" even where simulation
was tested and rejected
([80.lv breakdown](https://80.lv/articles/creating-diablo-iv-inspired-female-warrior-with-substance-3d-ue5)
**[secondary, a fan-recreation tutorial, not a Blizzard-authored source, but consistent with every
other Diablo IV character-art source found]**). **Read plainly: at D4/PoE2 fidelity, AAA studios
reach character-armor variety by paying artists to hand-sculpt many unique hero pieces, not by
running a kitbash system on armor specifically — kitbashing at that studio tier is confirmed only
for environment art.** The confirmed character-armor kitbash precedent found is one tier down:
commercial marketplace kits (Fantasy Modular Armor Sets, RoE Medieval, Modular Heavy Armour) at
asset-store fidelity, not shipped-AAA-game fidelity. **This tempers the recommendation honestly**:
kitbashing plus tinting is the right *cost* lever for reaching "150 variants of 10 shells" (which
is, by the project's own framing, a request for *variants*, not 150 unique hero sculpts — exactly
the class of asset no AAA studio hand-sculpts individually either), but it will not by itself
produce D4/PoE2 fidelity unless the underlying kit-piece library is hand-modeled to that bar first.
The quality ceiling is set by the hand-modeled parts library, not by the assembly mechanism.

**Maturity flag**: the *mechanism* (modular kit + tint) is production-proven at asset-store tier
(the marketplace kits exist and ship in real, if not AAA, commercial titles) and at AAA tier for
environment art (Diablo IV, confirmed). It is **not independently confirmed at AAA tier for
character armor specifically** — an honest gap, not a claim either way.

---

### Blender Geometry Nodes — current capability for hard-surface/armor work, specifically

**Extended description**: Blender's node-based procedural mesh-editing system. For this bullet, its
correct role is **parameterizing variation on top of hand-authored shapes** (spike count, panel
subdivisions, scatter density of rivets along a curve) — not authoring the base hero shapes from
scratch, a distinction the research below supports directly.

**Underlying technology, and what changed recently (dated, primary-source verified)**: this
project's pipeline already runs **Blender 5.2** (`scripts/ai-pipeline/README.md`), so version-exact
capability matters. Checked directly against Blender's own developer release notes:
- **Blender 5.2 LTS (July 2026, the exact version in use) shipped the Mesh Bevel node**: "The long
  awaited Mesh Bevel node is now available. It provides detailed control over the edges or vertices
  to bevel"
  ([developer.blender.org/docs/release_notes/5.2/geometry_nodes](https://developer.blender.org/docs/release_notes/5.2/geometry_nodes/)).
  This closes a historically real hard-surface gap — bevel-with-selection-control inside a pure
  node graph was the single most commonly cited missing piece for hard-surface GN work, and it
  landed in exactly the version this project runs.
- **Blender 5.2 also shipped Lists, Geometry Bundles, and a Collection Children node** (same
  source) — primitives that materially help build a data-driven kit-piece selection/assembly
  system natively inside GN (filter/sort a list of candidate trim pieces, bundle arbitrary
  per-variant data alongside geometry across object boundaries).
- **What is genuinely still missing, verified by checking the actual PR, not a summary**: native
  **armature/pose deformation inside a Geometry Nodes graph** is unshipped. PR **#142075**,
  "Geometry Nodes: Armature deformation node," is confirmed **Draft** status as of this pass — its
  own page's status badge reads "Draft" (fetched directly:
  [projects.blender.org/blender/blender/pulls/142075](https://projects.blender.org/blender/blender/pulls/142075)),
  authored by Lukas Tønne, 41 commits on a feature branch, not merged into 5.2 or any release.
  **This does not block this project's use case**, because MPFB2's proxy/weight-transfer step
  (above) happens *after* export, outside Geometry Nodes entirely, exactly like every other
  hand-modeled garment in this pipeline — it would only matter if the plan were to preview
  cloth-like draping against a *posed, moving* character natively inside a GN graph, which is not
  what this bullet needs. Reported as a genuine, dated, verified capability gap, correctly scoped
  to not being load-bearing for this project's actual architecture.
- A related in-flight PR, **#149020** ("WIP: Accelerate ArmatureModifier via GPU Compute, Improves
  performance by 10-15x"), confirms the *existing* (non-GN) Armature modifier's performance is
  itself still an active optimization target — orthogonal to this bullet but worth flagging as
  context for the broader character pipeline.

**License + real cost**: **€0.** Geometry Nodes ships in vanilla Blender (GPL). If hand-authoring
the base hero shells benefits from destructive boolean tooling (the historically dominant
hard-surface workflow, see below), **Hard Ops / BoxCutter Ultimate Bundle is $38 one-time
("for life") ≈ €35**, confirmed directly from the vendor listing
([superhivemarket.com/products/hard-ops--boxcutter-ultimate-bundle](https://superhivemarket.com/products/hard-ops--boxcutter-ultimate-bundle)).

**Compute/VRAM**: trivial — CPU/viewport cost only, no GPU inference, no contention with any AI
stage's VRAM budget. This is the concrete "procedural is largely CPU-bound" advantage the brief
asked to have quantified: it is not merely non-competing with the 12 GB card's AI workloads, it can
run *concurrently* with them without any sequencing concern (unlike the project's own documented
VRAM-sequencing rule for Hi3DGen-vs-ComfyUI in `gen_prop.py`).

**Wall-time per variant vs. one-time authoring cost**: once a parametric node graph exists for a
shell, per-variant generation is seconds (exposing "a handful of number inputs" and looping a
Python export, per the general BitSoul claim above — **[secondary, unverified against this
project's own meshes]**). Node-graph authoring itself is hours-to-days per parametric family,
comparable to writing any other reusable tool.

**Pros**: free, already installed, zero VRAM contention, genuinely improved for hard-surface work
in exactly the version this project runs (Mesh Bevel, Lists/Bundles), composes naturally with the
tint-mask and kitbash options above (GN can drive *which* kit pieces get instanced and where, then
hand off to the same MPFB2 export).

**Cons — what it is genuinely bad at, verified**: (1) **hero-shape authoring from scratch is not
where practitioners actually use it** — the destructive boolean workflow (Hard Ops/BoxCutter) "is
used by AAA studios" for exactly this class of work
**[secondary, aggregated practitioner consensus, not a single citable primary source]**, and GN's
own manual/community discussion confirms this is a *complementary* pairing, not a replacement:
"these aren't mutually exclusive... HardOps and Boxcutter work best together, while Geometry Nodes
complement them for procedural, parametric, and repeatable asset generation." (2) **Native
per-scene-graph armature deformation is unshipped** (Draft PR, above) — real but correctly scoped
as non-blocking. (3) Export friction is real and specific: **realized geometry only** — an
un-"Realize Instances"'d GN mesh exports empty to FBX; procedural UVs must be baked before the
modifier is applied; the exporter's auto-triangulation on GN output "can produce inconsistent
results," and GN "sometimes produces loose vertices or zero-area faces at seams" needing an
explicit merge-by-distance cleanup pass **[secondary, BitSoul blog checklist, plausible and
consistent with GN's known non-destructive-modifier architecture, but not independently verified
against this project's own export path in this pass]**. None of these are exotic — they are the
same kind of "bake before ship" step this project's pipeline already performs everywhere else
(`prop_cleanup.py`'s decimate step, `bake_textures.mjs`'s DDS bake) — but they are real, not
hypothetical, friction specific to GN's modifier-stack model.

**How much worse than a human artist, and where**: **not worse, and not really comparable** for
the *parameterization* role this report recommends it for — a human artist manually re-modeling 15
rivet-count variants of the same pauldron is doing strictly more repetitive labor for the identical
result a parametric graph produces instantly. It would be substantially worse than a human artist
if used for the hero-shape-design role (novel silhouette invention, reading concept art and making
judgment calls about proportion and readability) — which is exactly why this report does not
recommend it for that role.

**1-2 shipped games at comparable quality, with what their pipeline actually was**: **none found
using Geometry Nodes specifically for shipped character-armor production at D4/PoE2 tier** — this
is expected and consistent with GN's own recency (the modifier-stack system is a 2022-era Blender
feature, still actively gaining capability as shown by the 5.2 changes above); AAA armor pipelines
found in this pass (Diablo IV) use ZBrush/Substance, not Blender GN, for hero pieces. Geometry
Nodes' own confirmed production use in this pass is for **environment/prop procedural generation**
(the general "geometry nodes to Unreal Engine" production-pipeline pattern
**[secondary, multiple blog sources describing the same general pattern, none naming a specific
shipped AAA title]**), not for character armor.

**Maturity flag**: **the core toolset is production-proven for scatter/environment/procedural-prop
work; the hard-surface-specific capability (bevel-with-selection) is newly production-proven as of
the exact version this project runs (5.2 LTS, July 2026); native armature integration is
cutting-edge/unshipped.** A mixed maturity picture, reported honestly rather than rounded to a
single label.

---

### Blender Python scripting — the glue layer, not a competing option

**Extended description**: direct `bpy`/`bmesh` scripting for mesh authoring, modifier-stack
automation driven by data files, and batch export — the mechanism that actually ties the two
winning options above (tint-mask assignment, kit-piece assembly) into a repeatable pipeline, and
the natural home for driving MPFB2's `.mhclo` export per generated variant.

**Underlying technology**: Blender's Python API, run headless via `--background --python`, exactly
the invocation pattern already used by `prop_cleanup.py`, `prop_texture.py`, `mixamo_to_glb.py`
(per `character-mesh-pipeline` project memory), and `gen_prop.py`'s chain assembly.

**License + real cost**: **€0** — no new dependency, no new tool, no new license surface at all.
This is the single lowest-risk item in this entire report specifically because it adds nothing new
to the project's dependency/license ledger.

**Compute/VRAM**: trivial.

**Wall-time per variant vs. one-time authoring cost**: not separately meaningful — this *is* the
automation substrate the other options' per-variant/one-time numbers already assume.

**Pros**: zero new licensing surface; directly reuses a pattern this project has already proven out
five times over; is the only option in this report that is simultaneously required by both winning
mechanisms (tint-mask assignment needs a script to paint/assign material-ID zones per mesh island;
kitbash assembly needs a script to combinatorially instantiate and export).

**Cons**: none specific to this option — its only "cost" is the engineering time to write the
assembly/export scripts, already accounted for in the kitbash option's one-time cost above.

**How much worse than a human artist, and where**: not applicable — this is automation of a
mechanical export/assembly step a human would otherwise do by hand in the DCC UI, not a creative
substitute for artist judgment.

**1-2 shipped games at comparable quality**: not a named, published "tool" with its own
shipped-game citations — it is the implementation substrate under every option in this report that
claims one (Guild Wars 2's and Dawn of War 2's mask systems, whatever their engine, are necessarily
backed by equivalent data-driven scripting at the DCC/pipeline level, even though neither's specific
DCC tooling was documented in any source found).

**Maturity flag**: production-proven — within this project itself, today.

---

### Generative AI geometry (image-to-3D applied to armor/garment shapes)

**Extended description**: the geometry half of the brief's "generative AI texturing/geometry
pipeline" framing — using an image-to-3D model (this project's own cleared production backbone,
Hi3DGen, or any comparable tool) to generate a distinct mesh per armor variant from a concept image,
the same way `prop_hi3dgen.py` already does for standalone props.

**Underlying technology**: Hi3DGen (`Stable-X/Hi3DGen`, MIT, already installed and licensed clean
per `scripts/ai-pipeline/README.md` and `content/source/CREDITS.md`) — no new licensing research
needed; this option is evaluated purely on **fit**, not on licensing, and fails on fit.

**License + real cost**: moot — already cleared, already installed, €0 marginal license cost. Not
the disqualifying factor.

**Compute/VRAM**: fits 12 GB (measured 11.5 GiB peak per the README) — also not the disqualifying
factor.

**Wall-time per variant vs. one-time authoring cost**: minutes per variant for the raw generation
step — genuinely fast, **before** the disqualifying rework described below is accounted for.

**Pros**: fast per-variant raw generation; zero new licensing exposure (reuses an already-cleared
tool); could be a legitimate *concepting* aid (generate a rough shape to sculpt reference from) even
where it isn't a shippable-mesh source.

**Cons — the disqualifying one**: image-to-3D output has no relationship to the project's existing
character skeleton and is not clean, quad-dominant, joint-aware topology — the general image-to-3D
rigging literature is explicit that "animation-ready topology" is not a default property of
generative 3D output, that edge loops must follow joint areas for clean deformation, and that
"high-poly or unstructured meshes... may produce poor skinning results," requiring a full
remesh-to-quad-topology pass with deliberately placed joint edge loops before an object is even
rigging-*attempted* **[secondary, aggregated vendor/practitioner guidance (Meshy, Threedium, Tripo
blogs), not specific to Hi3DGen or to this project's own meshes, but consistent across every source
checked]**. Applied to this project specifically: even where MPFB2's proximity-based weight
transfer could technically ingest arbitrary topology (per the finding above), a raw Hi3DGen output
is a closed, high-triangle-count blob with no concept of "which part is the shoulder strap vs. the
chest plate" — the material-ID zoning the winning tint-mask option depends on has no natural
anchor on such a mesh either. The manual work required to fix this (retopology + material-zone
authoring + weight cleanup) is not smaller than modeling the variant by hand in the first place.

**How much worse than a human artist, and where**: **worse specifically at producing
rigging-ready, zone-labeled geometry** — precisely the two properties this project's pipeline
needs from every garment mesh and that a human artist (or the kitbash system, which inherits clean
topology from its hand-modeled source pieces) delivers by default.

**1-2 shipped games at comparable quality**: none — this project's own pipeline uses Hi3DGen only
for standalone, non-rigged props (`content/models/props/candelabra_shrine/`), never for
character-attached, rigged geometry, and no external source found documents any shipped game using
image-to-3D generation for rigged character armor at any quality tier.

**Maturity flag**: production-proven **for its actual designed use case (standalone props)**;
**not evaluated by anyone, anywhere, for rigged garment geometry** — this is a category mismatch,
not an immaturity gap to wait out.

---

### Substance 3D (Designer / Painter / Sampler)

**Extended description**: Adobe's node-based procedural material-authoring suite — the
industry-standard tool named explicitly in the brief. Belongs primarily to F2 (materials), included
here per the brief's instruction that it be evaluated under F1 too, since node-based material
graphs are the natural texture-authoring partner for the tint-mask system's base texture layer.

**License + real cost**: **Substance 3D Texturing plan (Designer + Painter + Sampler): $24.99/mo or
$249.88/yr ≈ €23/mo or €230/yr** (approximate conversion). **Substance 3D Painter 2026, perpetual
license via Steam: $199.99 ≈ €185 one-time** (Painter only, not Designer)
([store.steampowered.com/app/4329260](https://store.steampowered.com/app/4329260/Substance_3D_Painter_2026/)).
Pricing confirmed to have risen 2025-03-25 (Collection: $49.99→$59.99/mo; annual $549.88→$599.88)
per [CG Channel](https://www.cgchannel.com/2025/02/adobe-to-raise-the-price-of-substance-3d-subscriptions/)
and [Adobe's own blog](https://blog.adobe.com/en/publish/2025/02/20/substance-3d-innovations-pricing-updates).
Commercial-use terms: **"no revenue limit" on the Steam edition, usable for any commercial
work** **[secondary, aggregated Steam-community/forum claims, consistent across multiple sources
but not independently confirmed against Adobe's own binding Substance 3D Product-Specific Terms —
the `helpx.adobe.com` localized pricing page returned a connection error in this pass and was not
re-fetched]**.

**Compute/VRAM**: trivial (material authoring, no inference).

**Wall-time / one-time cost**: not a geometry-axis question — see F2 for the real evaluation.

**Pros/Cons/artist-gap/shipped-games/maturity**: out of scope for a rigorous F1 treatment; flagged
here only so the ledger is complete. Deferred to F2.

---

### Material Maker

**Extended description**: free, open-source, node-based material authoring tool explicitly modeled
on Substance Designer's workflow — "all nodes are actually shaders, so Material Maker works as fast
as your GPU," GLSL-based, exports to Unreal/Unity/Godot.

**License + real cost**: **MIT, €0**, confirmed via direct repo fetch
([github.com/RodZill4/material-maker](https://github.com/RodZill4/material-maker)) — "Unless
otherwise specified, files in this repository are licensed under the MIT license." Fully
unrestricted commercial use of generated output.

**Compute/VRAM**: GPU-accelerated shader evaluation, trivial relative to any AI inference workload;
runs on "modest hardware" per its own positioning.

**Maturity flag**: **active and real** — 5.7k★, v1.7 shipped **2026-07-14** (one week before this
research pass), 4,537 commits, Steam listing incoming per
[CG Channel's release coverage](https://www.cgchannel.com/2026/07/open-source-material-authoring-software-material-maker-1-7-is-out/).
The free Substance-adjacent option — F2's territory primarily, noted here for completeness per the
brief.

---

### ArmorLab / ArmorPaint — a naming correction, not a geometry option

**Extended description**: the brief names "ArmorLab" alongside Substance Designer and Material
Maker as a node-based procedural-authoring alternative. **This is a naming mismatch worth
surfacing rather than quietly working around, per this project's own standing rule that a spec
that doesn't fit reality should be corrected, not patched past.** ArmorLab is not an armor-geometry
generator at all — it is (per its own site) **"a software for AI-powered texture authoring"**
that generates PBR textures from text prompts or photo drag-and-drop
([armorlab.org/download](https://armorlab.org/download)). Its sibling project, **ArmorPaint**, is
the actual live product in this family — a standalone PBR texture-painting application, not a
geometry tool either.

**License + real cost**: ArmorLab's own repository is **archived** — "archived by the owner on
Feb 8, 2023... now read-only," moved to a consolidated `armortools` monorepo
([github.com/armory3d/armorlab](https://github.com/armory3d/armorlab)) — effectively dead as a
standalone product. ArmorPaint remains live, ~$19-40 depending on bundle, GitHub source available.

**Verdict for F1 specifically**: **not applicable — neither tool touches geometry.** Mentioned here
only to close out the brief's explicit ask and to record that ArmorLab specifically is dead, so it
should not appear on any future shortlist without this caveat attached.

---

### Houdini (Indie license)

**Extended description**: SideFX's procedural 3D suite — VEX/VOPs/HDAs are Geometry Nodes' direct
ancestor and, by wide practitioner consensus, still the deeper, more mature procedural-modeling
environment. Evaluated here specifically for whether it's worth adding as a second DCC alongside
this project's existing Blender-centric codebase.

**License + real cost, verified against SideFX's own pages**:
**$299/1yr or $449/2yr** ≈ **€275/yr** (approximate conversion), confirmed directly from
[sidefx.com/products/houdini-indie](https://www.sidefx.com/products/houdini-indie/). Eligibility,
confirmed from SideFX's own FAQ pages
([sidefx.com/faq/indie-new](https://www.sidefx.com/faq/indie-new/),
[sidefx.com/faq/question/indie-restrictions](https://www.sidefx.com/faq/question/indie-restrictions/)):
**annual gross revenue under $100K USD and under $1M USD in funding**, up to 3 Indie licenses per
entity, **cannot be used in the same pipeline as commercial (non-Indie) Houdini**, uses its own
proprietary scene/asset file format. **Correction to a secondary claim found during this pass**: one
aggregated WebSearch summary claimed a "4K render resolution limit" for Indie — SideFX's own current
FAQ, fetched directly, states plainly **"There are no resolution restrictions for generating images
with Houdini Indie and any third party renderers"** — the resolution-cap claim is stale/wrong and
is explicitly rejected here in favor of the primary source, per this project's own
read-the-text-not-the-summary discipline. **The revenue cliff is the real, live cost risk**: if this
project's own commercial revenue ever exceeds $100K, Houdini Indie becomes non-compliant and the
same functionality jumps to **Houdini FX at $3,195/yr (node-locked annual) or $4,495 perpetual**
**[secondary for the FX figures — a pricing-aggregator blog, not re-verified against SideFX's own
buy page in this pass, unlike the Indie figures above which were fetched directly]** — a >10×
price jump triggered by the game's own success, not by anything Houdini-side changing.

**Compute/VRAM**: trivial, same CPU-bound class as Blender GN — genuinely fits 12 GB with room to
spare, no contention with AI workloads.

**Wall-time per variant vs. one-time authoring cost**: comparable to Geometry Nodes once an HDA
(Houdini Digital Asset) exists — real practitioner evidence exists for procedural armor
specifically: Houdini "can be used to generate armor or a second skin on top of a character model
completely procedurally, with the... possibility to automatically generate multiple variations of
the armor with the PDG export system" **[secondary, aggregated marketing/tutorial-page claims
(ArtStation/Gumroad product pages, Fiverr listings) for a generic "procedural sci-fi armor" workflow
concept, not a specific shipped-game citation]** — real as a *technique* (this is a well-known
Houdini production pattern, e.g. via Voronoi fracture + VDB detailing), not verified against this
project's own art-direction register.

**Pros**: deeper, more mature procedural toolset than Blender GN today, especially for the kind of
scatter-and-detail work armor trim benefits from; PDG (Procedural Dependency Graph) is a genuinely
more mature batch-variant-generation system than anything Blender ships natively.

**Cons — why it's a non-starter regardless of capability**: (1) **the revenue-cliff risk above** —
a real, live cost trap tied directly to this specific project's own commercial success, not a
generic pricing quibble; (2) **a second DCC adds a context-switch and a file-format boundary this
project's Blender-centric codebase doesn't currently have** — every downstream step (MPFB2's
`.mhclo` proxy/weight-transfer, `gltf-transform` preprocessing, the existing headless-Blender
Python scripts) is Blender/Python-native; introducing Houdini would mean authoring geometry in one
tool and doing every subsequent pipeline step in another, importing across an FBX/glTF boundary for
every iteration — a real workflow-friction cost with no corresponding capability this project
actually lacks, since Blender 5.2's own GN improvements (above) close much of the gap that would
have justified the switch a year or two ago; (3) the proprietary Indie file format is itself a
lock-in — if revenue crosses the cap, re-editing existing HDAs requires the $3,195+/yr upgrade,
though already-exported/shipped meshes remain usable regardless.

**How much worse than a human artist, and where**: not applicable to Houdini's own capability
(it is not worse at procedural armor detailing than Blender GN — arguably better, per its maturity)
— the "worse" here is entirely a pipeline-fit cost, not a quality one.

**1-2 shipped games at comparable quality, with what their pipeline actually was**: Houdini's
general use in AAA game production is well-established (cited at "Gameloft" for production tooling
**[secondary, single-line aggregated claim, not independently verified]**) but **no source in this
pass named a specific D4/PoE2-tier ARPG's character-armor pipeline as Houdini-based** — the
procedural-armor examples found are individual artists' portfolio/tutorial pieces
(ArtStation/Gumroad), not documented studio production pipelines.

**Maturity flag**: **the software itself is production-proven industry-wide**; its fit for *this
project specifically* is the disqualifying factor, not its maturity.

---

### Sloyd.ai — the 2025-2026 hybrid tool a search would otherwise miss

**Extended description**: a genuinely novel 2025-2026 category — "AI-powered 3D creation platform"
combining text-to-3D, image-to-3D, **and real-time parametric templates with sliders**, positioned
explicitly as a hybrid of generative AI and procedural/parametric modeling. Recognized by a16z
Speedrun and cited by NVIDIA; ships Unity/Unreal plugins and Roblox avatar support.

**License + real cost**: **Free Starter tier; Plus $11/mo (yearly) or $15/mo (monthly) ≈ €10-14;
Pro $50/mo ≈ €46**; Studio/Enterprise custom
**[secondary, aggregated pricing-comparison sources, cross-checked across three independent
listings that agreed]**. Commercial license included on paid plans, but **explicitly distinguishes
"art/games/animation" commercial use from redistribution, marketplace resale, 3D printing, and
AI-training rights** — the last three remain restricted even on paid tiers
**[secondary, same sources]** — worth re-checking the actual ToS text before relying on it for
anything beyond "use the model in our own shipped game," which does appear to be squarely
permitted.

**Compute/VRAM**: N/A — cloud service, no local GPU/VRAM cost at all (a genuine advantage over
every locally-run AI-geometry option in this report).

**Wall-time per variant vs. one-time authoring cost**: seconds, real-time parametric slider
adjustment — the fastest per-variant iteration loop of anything in this report, by design.

**Pros**: zero local compute cost; genuinely fast iteration; a real, funded, actively-developed
2025-2026-era product that legitimately blends the two paradigms this bullet is about.

**Cons — why it's a watch item, not an adoption**: (1) **register mismatch** — its own asset
library is described as "crates, rocks, buildings, weapons... low-poly and mid-poly game assets,"
the same "wrong register" problem `a5-comparative.md` already found for general-purpose AI base
models against this project's specific D4/PoE2 semi-realistic dark-fantasy bar; (2) **no MHCLO/
MPFB2 integration of any kind** — it is a rented, closed-source cloud service with no path to
respect this project's own skeleton/weight-transfer requirements any better than any other
generic image-to-3D tool (same disqualification as the "Generative AI geometry" section above,
inherited rather than independently re-argued); (3) parametric templates are **Sloyd's own,
pre-authored by their team** — it is not a tool this project builds its *own* parts library
inside, unlike Blender GN/Python, so it doesn't actually reduce this project's own one-time
authoring cost, it substitutes a rented, generic one.

**How much worse than a human artist, and where**: worse specifically at producing this project's
own unique, art-directed silhouette language — its templates are shared across every Sloyd customer
by design, which directly conflicts with the project's stated requirement that designs be unique
and not sourced from any existing ecosystem.

**1-2 shipped games at comparable quality**: none found at D4/PoE2 tier; its own positioning and
asset-library register target indie/prototype-tier low-to-mid-poly work.

**Maturity flag**: real and funded, but young — no specific launch date found, recent
(a16z Speedrun-era, i.e., 2024-2026) company, genuinely cutting-edge rather than production-proven
at this project's target fidelity.

---

## Hybrid — the recommended architecture (restated in full, per the brief's requirement)

**Extended description**: hand-model 10 base shells and a shared hard-surface trim/kit-piece
library once, at D4/PoE2 fidelity (ZBrush-adjacent hand-sculpting, or Blender's own
HardOps/BoxCutter-class destructive-boolean workflow — either is consistent with every AAA
precedent found in this pass). Author each shell's texture with an explicit material-ID mask from
day one. Write a headless-Blender Python script (reusing the exact `--background --python` idiom
already proven in this repo) that (a) combinatorially assembles kit pieces onto each shell per a
manifest, (b) exports through MPFB2's existing `.mhclo` proxy/weight-transfer step, and (c) tags
each output with a tint-mask-driven material-ID palette. Reserve C1's Z-Image texturing stack
(with its own sequential-img2img fix) for the smaller subset of unique hero/legendary pieces where
per-item hand-authored texture design is explicitly wanted, exactly as C1 itself already concluded.

**License + real cost**: **€0 in new licensing surface** — every load-bearing piece (Blender,
Python, MPFB2's CC0 asset pack, Z-Image/ComfyUI) is already cleared and installed per
`content/source/CREDITS.md` and `scripts/ai-pipeline/README.md`. The only real cost is artist-hours
for the parts library and shell texture authoring — a one-time, already-necessary cost regardless
of which downstream variant mechanism is chosen (even a "hand-model all 150" plan would need the
10 shells authored first).

**Compute/VRAM**: fits 12 GB trivially at every stage — the procedural stages add no GPU load at
all, and the AI stage is scoped down to a small hero-prop subset rather than all 150 items, which
*reduces* this project's total GPU-time budget relative to C1's original all-AI framing.

**Wall-time per variant vs. one-time authoring cost**: per-variant cost for the ~70-90% of the
matrix that's tint+kit-only is **seconds to minutes** (script run + QA render). One-time cost is
the parts-library/shell authoring, already required regardless of downstream choice. The AI-texture
subset (hero pieces) keeps C1's own measured ~3 min/4-view number.

**Pros**: solves cross-variant consistency by construction (the axis C1 could not close); adds
zero new licensing exposure; reuses this project's existing Blender+Python idiom rather than
introducing a second DCC or a rented cloud service; scopes AI spend down to where it's actually
earning its cost (unique hero authorship), which is a better use of both GPU-hours and artist
review time than generating 150 independent AI passes and hoping they cohere.

**Cons**: requires the hard-surface parts library to actually be authored to a high bar — this
recommendation does not eliminate hand-modeling labor, it amortizes it; requires engine-side support
for material-ID-driven tinting to be built or confirmed (a real, un-researched engineering item,
flagged in Gaps, not assumed away).

**How much worse than a human artist, and where**: for the recommended architecture as a whole,
not worse at the *variant* layer (that is precisely what a human technical artist would build by
hand, just slower); the ceiling is still set by the human-hand-modeled parts library and hero
pieces, exactly as it would be under any pipeline.

**1-2 shipped games at comparable quality, with what their pipeline actually was**: this exact
two-layer combination (tint mask + modular kit) is the one directly-cited commercial precedent in
this whole report — Unreal Marketplace's "Fantasy Modular Armor Sets" — plus the two independent
mechanism precedents (Guild Wars 2's dye channels, Dawn of War 2's RGBA masks) that demonstrate each
layer shipping separately at real commercial scale.

**Maturity flag**: **each individual layer is production-proven** (tint masks since 2009, Blender
Python scripting within this project today, Z-Image texturing per C1); **the specific combination,
applied to this project's specific MHCLO-based character pipeline, is un-built** — this is a
synthesis recommendation, not a turnkey product, and should be read that way.

---

## License / cost ledger (summary)

| Tool | License | Cost (approx EUR, solo EU dev) | Commercial-output restriction found? |
|---|---|---|---|
| Blender (GN + Python) | GPL | €0 | None — GPL covers add-on/engine code only; your own generated meshes/renders are unencumbered, standard Blender-community understanding, not independently litigated-tested |
| Hard Ops / BoxCutter | Proprietary (Blender-Market/Superhive add-on) | €35 one-time | None found |
| Material Maker | MIT | €0 | None |
| Substance 3D Texturing plan | Adobe proprietary subscription | ≈€23/mo or €230/yr | None found for Steam-edition commercial use **[secondary]** |
| Substance 3D Painter perpetual | Adobe proprietary | ≈€185 one-time | Painter only, no Designer/Sampler |
| ArmorPaint | GPL-family (live); ArmorLab (dead) | ~€18-37 | Not evaluated — not a geometry tool |
| Houdini Indie | SideFX proprietary, Indie EULA | ≈€275/yr | **Revenue cap $100K / funding cap $1M — hard cliff to Houdini FX (≈€2,950-4,140) if exceeded** |
| Sloyd.ai | Proprietary SaaS | €0-46/mo | Commercial art/games use permitted; resale/AI-training/marketplace resale restricted on all tiers **[secondary]** |
| Marketplace armor kits (Fab/UE) | Fab Standard License (new) or legacy UE Marketplace License (grandfathered) | Not priced (403'd) | Standard License is engine-agnostic per Epic's own summary **[secondary]**; legacy-license listings may differ — verify per purchase; **not shippable regardless**, per this project's own uniqueness mandate |
| KitBash3D | Proprietary SaaS/library | ≈€54-91/mo | No armor/character content exists in the catalog at all |

**Structural finding worth stating plainly**: unlike C1's licensing ledger (which had to Block half
its candidates on NC clauses, EU-exclusion territory clauses, or vendored-code provenance fraud),
**nothing in this report's option space is licensing-Blocked.** Every tool here permits ordinary EU
commercial use of its output; the only real cost traps are Houdini's revenue cliff and (for
marketplace kits) the project's own self-imposed uniqueness requirement, not a vendor restriction.
This asymmetry — the procedural/node-tooling world simply doesn't carry the same NC/territory
minefield the generative-AI-model world does — is itself a point in procedural's favor that the
brief didn't explicitly ask for but is worth recording.

---

## Gaps and unknowns — searched for, not found, or not verifiable by reading

- **No sourced, unbiased figure for "hours to hand-model one hard-surface trim/kit piece"
  exists.** The one number found (20-40 hrs/complex-prop-or-armor-piece) is from an AI-tool
  marketing blog with an obvious incentive to inflate manual-authoring cost, and describes a
  *complete hero piece*, not a small trim element — not used as load-bearing evidence anywhere in
  this report's verdict.
- **No primary ArenaNet or Relic source on Guild Wars 2's or Dawn of War 2's underlying shader/
  texture-format implementation was found** — GW2's dye-channel mechanism is inferred from
  player-facing wiki behavior (strong circumstantial evidence, not a dev-blog confirmation); DOW2's
  is confirmed via a community reverse-engineering tool's own description, which is closer to
  primary but still not an official Relic document.
- **No GDC talk, postmortem, or dev blog was found describing any AAA ARPG's *character-armor*
  pipeline as kitbash/procedural, at D4/PoE2 fidelity specifically.** Every character-art source
  found for Diablo IV describes full hand-sculpting; the only confirmed AAA kitbash precedent is
  Diablo IV's own *environment* art. This is the report's single most important negative-space
  finding and is treated as such in the Verdict, not glossed over.
- **No hands-on test of the tint-mask/material-ID system against this project's own PBR shader
  pipeline was run** (out of scope — a research pass, no generation workloads permitted per the
  brief). Whether the engine's material system already supports per-zone tint uniforms, or needs
  new shader work, is unverified and should be the first thing checked before committing to this
  recommendation.
- **MPFB2's nearest-surface weight-transfer quality on genuinely novel kitbashed silhouettes
  (long cloaks, wide asymmetric pauldrons) was not tested** — the documentation confirms the
  mechanism exists and is designed for arbitrary topology, but not that it produces *good* results
  on an unbounded range of shapes without per-variant manual weight polish. Flagged as the report's
  main technical risk, not dismissed.
- **The Fab Standard License's binding text could not be read directly** — both WebFetch and a
  scripted `curl` fetch hit a Cloudflare JavaScript challenge on `fab.com/eula`; the engine-agnostic
  claim rests on Epic's own documentation *summary* page, not the EULA text itself, and is flagged
  as secondary throughout.
- **Exact pricing for the three specific UE-Marketplace/Fab armor kits named (Fantasy Modular
  Armor Sets, RoE Medieval, Modular Heavy Armour) could not be extracted** — all three product
  pages returned HTTP 403 to WebFetch in this pass. Moot for the final recommendation (this
  project's own uniqueness mandate rules out shipping their content regardless), but a gap if
  anyone wants to actually study them as reference.
- **Houdini FX's exact current price ($3,195/yr, $4,495 perpetual) is secondary** (a
  pricing-aggregator blog), not independently re-verified against `sidefx.com/buy` directly in this
  pass, unlike the Indie figures which were fetched from SideFX's own pages.
- **Whether Blender 5.2's new List/Bundle primitives are actually sufficient to build a full
  kit-piece selection system natively in Geometry Nodes (vs. needing Python regardless) was not
  tested hands-on** — the release notes confirm the primitives exist; whether they're ergonomically
  adequate for this specific use case is an implementation question, not a research one.

---

## Verification pass — the tint mechanism, checked against the renderer

The report flags as its main open risk: *"Whether the engine's material system already supports
per-zone tint uniforms, or needs new shader work, is unverified and should be the first thing
checked before committing to this recommendation."* It was checked. Two facts, one of which
redirects the mechanism.

**1. A whole-mesh tint already exists, plumbed end-to-end.** `MeshInstance` (`mesh_pipeline.rs:29`)
is `model: [[f32;4];4]` + `tint: [f32;4]`, 80 bytes; the skinned pass carries the same field
(`skinned_pipeline.rs:33`). It reaches the shader as a vertex attribute and lands in
`let albedo = albedo_s.rgb * material.base_color.rgb * in.tint.rgb;` — `mesh_shader.wgsl:84` and
`skinned_mesh_shader.wgsl:97`, identically. It is already load-bearing content: class identity
rides it (`vfx.rs:243 class_tint`, ravager ember-red / wayfarer steel-cyan).

So the *pattern* is proven, but it is **one global multiply per instance**, not four zones. A
search for `material_id`/`MaterialId` returns nothing. The report's proposed RGBA material-ID mask
would need a mask texture per shell, the instance tint widened 16 → 64 bytes, and a fragment
change — across two pipelines and two shaders.

**2. That work is probably unnecessary, because material zones already exist as glTF primitives.**
`MaterialUniform` (`mesh_pipeline.rs:39`) is documented **per-primitive** — "Per-primitive PBR
factors (glTF material), bound at group 1 binding 6" — carrying its own `base_color`, `emissive`
and `mr`. A four-zone armor piece is therefore already expressible with **zero renderer changes**:
author the shell as four glTF materials (metal-primary / metal-secondary / cloth-leather /
trim-accent) and have the variant script write four `baseColorFactor`s into the GLB. The renderer
binds them per-primitive today. This is also the convention A6.1 already moved toward when it
retired MR zoning from a 1024² map onto the glTF scalar factors.

**The trade is disk vs. shader work, and it falls the same way A6.1 fell.** Per-primitive
materials mean each variant is a baked GLB (~150 files, no runtime recolor); the mask route means
~10 GLBs recolorable at runtime from instance uniforms. This pipeline generates assets offline and
the client loads them by path, so the baked route needs no engine change, no new mask-authoring
step, and no contention with the instance tint channel class identity is already using. Take it.
Revisit the mask route only if player-facing dye/customization becomes a design requirement — that,
not variant count, is what would justify the shader work.

**Effect on the verdict:** the recommendation strengthens. Its riskiest dependency turned out to be
already satisfied by an existing, simpler mechanism than the one proposed, and the four-zone
convention lands as a *content* convention for the Blender variant script rather than as renderer
work. The report's other flagged risk — MPFB2 weight-transfer quality on novel kitbashed
silhouettes — was settled by measurement; see the next section.

---

## Drape test — MPFB2 fit and weight transfer on novel kitbash shells (2026-07-21, measured)

Harness: `f1_drape_probe.py`, Blender 5.2 headless, MPFB2 2.0.17, CPU only. Two shells authored as
clean all-quad grids the way a parts library would emit them, placed from MPFB joint-group
centroids: an asymmetric spherical-cap **pauldron** over the left shoulder (143 verts, standoff
mean 51 mm) and a flared **cloak** back panel from shoulders to below the knee (357 verts, standoff
mean 134 mm). A third shell reuses the cloak geometry bound to MPFB's `helper-skirt` cage.

**The mechanism is not free-form nearest-surface.** `VertexMatch` restricts its search to basemesh
faces inside the vertex group named on the clothes vertex, and `interpolate_weights` then inherits
skin weights barycentrically from the three matched verts. But the matchable vocabulary is coarse:
of 152 basemesh groups, 125 are `joint-*` landmarks, and the only bindable surfaces are a single
`body` group covering all skin plus the `helper-skirt` / `helper-tights` standoff cages. So a part
with no matching cage can only say "somewhere on the body" — there is no way to declare intent.

### Result 1 — fit and conform: PASS, and this is the load-bearing one

Both novel shells pass `mesh_is_valid_as_clothes` unmodified and match without a single failed
vertex. Pushing the body to weight 0.95 / muscle 0.85 / height 0.9 — a 1.67 m → 2.23 m change,
far past anything four playable races need — refitting the armature *and* the shells:

| shell | standoff before | standoff after | verts inside body (rest / posed / conformed) |
|---|---|---|---|
| pauldron | 52 mm | 70 mm | 0 / 0 / 0 |
| cloak | 129 mm | 192 mm | 0 / 0 / 0 |
| cloak (caged) | 134 mm | 183 mm | 0 / 0 / 0 |

Standoff scales ~1.4× against 1.34× body growth with zero interpenetration at any stage. **One
authored shell re-fits across body types instead of being re-modelled per race** — the economic
premise of the parts-library recommendation — and it holds under an abusive test.

Two harness corrections were needed before those numbers meant anything, and both are constraints
on the real generation script:

- **The armature must be refit alongside the body** (`RigService.refit_existing_armature`).
  Refitting only the shells leaves them skinned to a rig still sized for the old body: rest
  positions measure correct while everything the armature modifier displays is wrong.
- **Penetration needs a signed test.** Nearest-vertex distance cannot detect it — a vertex 5 cm
  buried scores identically to one 5 cm proud — so `closest_point_on_mesh` and the sign of
  `(p − hit) · normal` is the only valid check. Under the distance metric the pauldron read a
  healthy 2.5 mm minimum gap while 20 of its 143 vertices were in fact up to 78 mm *inside* the
  torso, and conform amplified that to 104 mm because offsets scale with the body.

That penetration was an authoring error — the cap was built around the shoulder *joint*, which is
an interior point — and projecting the shell onto the skin before matching (23 vertices lifted)
clears it completely. The finding that survives is about MPFB, not the cap: **it preserves whatever
interpenetration it is handed, warns about none of it, and conform scales the error up with the
body.** Parts must be projected onto the surface at authoring time and asserted with a signed test.

### Result 2 — weight transfer: PASS only where a cage exists

Skinning weights, and displacement under a 60° `mixamorig:LeftArm` raise:

| shell | dominant transferred weights | max displacement | verts moved |
|---|---|---|---|
| pauldron (`body`) | Spine2 39.7%, **LeftArm 24.9%**, LeftShoulder 14.8%, **Head 11.4%** | 48% of upper-arm length | 84 / 143 |
| cloak (`body`) | RightUpLeg 18.5%, LeftUpLeg 17.0%, Hips 16.6% — no spine | 139% of upper-arm length | 29 / 357 |
| cloak (`helper-skirt`) | Spine 28.2%, UpLegs 43.3%, Hips 12.2% | 0.0000 | 0 / 357 |

Bound to raw skin, a correctly surface-projected shoulder pauldron still inherits **25% upper-arm
and 11% head weight** against only 15% for the shoulder it should ride — nearest-face matching
reaches the arm below and the neck above — and it swings 48% of an upper-arm length. The
uncaged cloak is skinned to the legs with no spine contribution, and 29 vertices tear away when an
arm that is nowhere near them is raised. Bound to the cage, the same cloak geometry is inert under
the arm raise and carries a coherent spine-plus-legs distribution.

**Every one of these failures passes validation silently.** `mesh_is_valid_as_clothes` returns
`all_checks_ok: True` for the head-weighted pauldron, and did so equally for the version with 20
vertices buried in the torso. It validates topology and scale, never whether a match landed
somewhere anatomically absurd. The generation script must assert on the transferred-weight
distribution and on signed penetration itself, because MPFB checks neither.

### Consequence — the recommendation changes shape, not direction

The parts library survives intact; what changes is that parts split into three rigging classes:

1. **Loose geometry below the waist** (skirts, robe skirts, tassets) — bind to `helper-skirt` /
   `helper-tights`. Works today, measured above.
2. **Rigid armor** (pauldrons, bracers, greaves, helms) — take the mhclo *fit*, which works, and
   **discard the transferred weights**, assigning the piece rigidly to its one bone. Rigid armor has
   no drape to solve; skinning it to a surface is what produced the head-weighted pauldron.
3. **Loose geometry above the waist** (capes, tabards, hoods) — the real gap, and no cage exists.
   Weights must be authored once per shell. This is a handful of shells, not 150, and it is paid
   once and amortised over every variant, so it is a cost rather than a blocker.

### Upstream bug found (relevant to writing the real script)

`create_mhclo_from_clothes_matching` leaves offsets in MakeHuman's frame as `(dx, dz, -dy)`;
only `Mhclo.load` converts them back, as `(d0, -d2, d1)`. An mhclo handed straight from the matcher
to `fit_clothes_to_human` therefore has its standoff vector **rotated**, not restored. Measured on
an identity refit against an unchanged body: 82 mm mean drift for the pauldron, 196 mm for the
cloak — error magnitude `sqrt(2(dy² + dz²))`, matching prediction. Writing the `.mhclo` to disk and
reloading it round-trips exactly (0.1–0.3 mm, the file's 4-decimal precision). **The generation
script must author through the file**, never through the in-memory shortcut. This bit the first two
runs of this very test and produced a plausible-looking false negative.

---

## Sources

Primary (vendor pricing/EULA pages, repo LICENSE/API, project-tracker PRs, official release notes,
official documentation, fetched directly in this pass):
- [SideFX — Houdini Indie FAQ](https://www.sidefx.com/faq/indie-new/), [Indie restrictions FAQ](https://www.sidefx.com/faq/question/indie-restrictions/), [Houdini Indie product page](https://www.sidefx.com/products/houdini-indie/)
- [github.com/RodZill4/material-maker](https://github.com/RodZill4/material-maker) (MIT LICENSE, fetched directly)
- [github.com/armory3d/armorlab](https://github.com/armory3d/armorlab) (archived status, fetched directly), [armorlab.org/download](https://armorlab.org/download)
- [Blender 5.2 LTS Geometry Nodes release notes](https://developer.blender.org/docs/release_notes/5.2/geometry_nodes/) (Mesh Bevel, Lists, Geometry Bundles — fetched directly)
- [Blender PR #142075 — Geometry Nodes: Armature deformation node](https://projects.blender.org/blender/blender/pulls/142075) (Draft status confirmed via direct fetch)
- [Blender PR #149020 — GPU-accelerated ArmatureModifier (WIP)](https://projects.blender.org/blender/blender/pulls/149020) (referenced from #142075's own page)
- [Superhive — Hard Ops/Boxcutter Ultimate Bundle](https://superhivemarket.com/products/hard-ops--boxcutter-ultimate-bundle) ($38, fetched via search + confirmed)
- [github.com/makehumancommunity/mpfb2 — Issue #64](https://github.com/makehumancommunity/mpfb2/issues/64), [Rigging Mesh Assets docs](https://static.makehumancommunity.org/mpfb/docs/rigging_mesh_assets.html)
- [github.com/Jaccouille/dow2-texture-painter](https://github.com/Jaccouille/dow2-texture-painter) (Dawn of War 2 RGBA team-color mask mechanism)
- [wiki.guildwars2.com/wiki/Dye](https://wiki.guildwars2.com/wiki/Dye)
- [kitbash3d.com/pages/pricing](https://kitbash3d.com/pages/pricing) (fetched directly — no armor/character kits confirmed)
- [dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab](https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab) (Epic's own summary; binding `fab.com/eula` text blocked by Cloudflare in this pass)
- [store.steampowered.com/app/4329260 — Substance 3D Painter 2026](https://store.steampowered.com/app/4329260/Substance_3D_Painter_2026/)
- [cgchannel.com — Adobe Substance 3D price increase](https://www.cgchannel.com/2025/02/adobe-to-raise-the-price-of-substance-3d-subscriptions/), [blog.adobe.com pricing update](https://blog.adobe.com/en/publish/2025/02/20/substance-3d-innovations-pricing-updates)
- [cgchannel.com — Material Maker 1.7](https://www.cgchannel.com/2026/07/open-source-material-authoring-software-material-maker-1-7-is-out/)
- In-repo: `scripts/ai-pipeline/README.md`, `content/source/CREDITS.md`, `tasks/ai-pipeline/research/c1-texturing-geometry.md`, `tasks/ai-pipeline/research/BACKLOG.md`, `tasks/character-direction-notes.md`

Secondary (flagged inline where used; practitioner blogs, aggregators, marketing content, or
search-snippet-only sources not independently re-verified against a primary document):
- StraySpark, BitSoul, CGWire blog posts on Geometry Nodes production pipelines and game-asset
  automation claims (60-70% time savings, "50 variants in seconds" — unverified against this
  project's own meshes)
- 80.lv breakdown of a fan-made Diablo-IV-inspired character (ZBrush/Substance workflow)
- ArtStation summary of Diablo IV's GDC 2024 "Art of Open World Sanctuary" talk (GDC Vault
  recording itself not accessed)
- triverse.ai AI-tooling marketing blog's "20-40 hours per armor piece" claim (treated with
  skepticism, not load-bearing)
- Sloyd.ai's own site and third-party pricing-comparison aggregators (toolworthy.ai, dailyaitools.io)
- gianty.com's summary of a GDC 2026 developer-sentiment survey (52% negative on generative AI)
- WebSearch-aggregated claims for Houdini FX's exact current price, Fantasy Modular Armor Sets'
  price/content (product page 403'd), and general "Houdini used at Gameloft" production claims
