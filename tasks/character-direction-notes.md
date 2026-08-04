# Character direction — notes

Durable-architecture conclusions from 2026-07-08/09, updated 2026-07-23 for
the B1 direction lock (Castilian/Andalusian religious dark fantasy). The
architecture below survived every body-source question that has come up
since; the B1 section adds what B4's planner needs for the production
character swap.

## Durable architecture (survives any body-source swap)

1. **Skeleton convention + clip library are the durable assets.** The
   Mixamo bone-name convention (`mixamorig:*` rest pose) plus its clip
   library (idle/walk/run/attack/hit/death and the extra combat/traversal
   clips) is what every rig must carry — any mesh sharing this skeleton's
   names and rest pose plays the whole library natively, zero retargeting.
2. **Mixamo as a service is retired; the A4 pipeline replaced it.** Rather
   than uploading a base mesh to Mixamo's auto-rigger for a fresh skeleton,
   the canonical skeleton is transplanted onto the mesh directly:
   `char_rig.py` fits the existing canonical armature to a generated body
   and computes skin weights (SkinTokens/auto-weights route), while
   `char_mpfb.py` binds MPFB2 parametric bodies through authored
   name-matched vertex groups (no weight solver). The clip library still
   attaches with zero retargeting, because the transplanted skeleton keeps
   the same bone names and rest pose. Full pipeline, fixture, and
   decision-gate history: `tasks/ai-pipeline/a4.md`.
3. **Hair = rigid attachment on the `head` socket** (sockets already
   published via `SocketConfig`). Hairstyles become data.
4. **Armor-on-top needs one engine feature: skinned attachments** — the
   modular-armor engine seam ("Phase 5-bis"), still deferred. Multiple glbs
   sharing one skeleton + one joint palette + one AnimationPlayer per
   entity. Rigid pieces (helmets, weapons) already work via sockets;
   deforming pieces (chest/legs) need this.

## B1 character direction (for B4) — per-race silhouette registers

Castilian/Andalusian religious dark fantasy identity per race/class,
locked at the B1 gate. Palette and lighting language for all of these is
`docs/visual-quality.md` §A (VQ-A1 direction, VQ-A4 color roles — votive
cool player VFX, candle-gold environmental emissive, red-orange→crimson
threat, desaturated warm-stone ambient — VQ-A5 amber-dusk lighting mood).

- **Human** (wayfarer) → penitent pilgrim.
- **Dwarf** → crypt/reliquary mason.
- **Elf** → sacred-grove / olive-warden.
- **Valkyrie** → winged seraph-militant.
- **Ravager** (class) → penitent-fury duelist.

**Risk carried from A4, flagged not resolved:** valkyrie wings are
mesh-generation exotica. A4 deliberately excluded the valkyrie from its
fixture and generalization proof to avoid confounding wing-geometry
generation with rig-chain failures on the pipeline's first outing
(`tasks/ai-pipeline/a4.md`); B4 has to solve wing generation and rigging
fresh, with no A4 evidence to lean on.
