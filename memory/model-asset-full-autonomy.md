---
name: model-asset-full-autonomy
description: "On 3D model/character asset work, user wants full autonomy — choose assets and details, don't ask"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2d778b7d-2409-4416-aa90-32e5cddf17a6
  modified: 2026-07-23T09:49:10.507Z
---

For the mesh/model/character-asset visual work (glTF models, rigs, animation clips,
which CC0 pack/character to use), the user wants **full autonomy**: "choose what fits
more to our game, don't ask me about anything, everything about this model is done by
you." Rejected an AskUserQuestion about which rigged asset to use.

**Why:** They trust engineering judgment on asset selection and see asking as friction;
the game direction (humanoid ARPG combatants — ravager, the four races) is enough context
to pick well. Fits the broader [[serious-project-not-learning]] stance.

**How to apply:** Pick the asset that best fits the game (humanoid rig + full clip set for
characters) and proceed. Don't surface asset-choice questions. Still note what was chosen
and why in the summary so it's visible, but decide it yourself. Distinct from architectural
planning, which they still want (project CLAUDE.md's plan-mode rule).

**Bounded by a premise (user correction):** autonomy does not mean picking assets one at a time — that produces a set with no thesis ("the objects you decided to model have no connexion at all"). Before generating an asset for a place, the place must have a written premise — what it is, who left it, what era and material vocabulary — and each new asset cites it or is not made. Autonomy applies to *which asset satisfies the premise*, never to whether one exists; without a premise, gaps (the player's sword still a cuboid while decorative props ship) stay invisible. Also settled: an object's nominal substance is not its surface class — painted iron is a dielectric; read the surface, not the noun.
