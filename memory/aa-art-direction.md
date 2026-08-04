---
name: aa-art-direction
description: "Art direction locked — semi-realistic dark fantasy AA; KayKit/low-poly rejected as \"cheap/mobile\"; scope = player + environment only"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f5ac28ff-ba15-42e5-a1d4-3a86622a498f
  modified: 2026-07-23T09:49:07.979Z
---

The user rejected the current visuals as "a minigame" and, critically, rejected **KayKit / stylized low-poly entirely**: "I don't like KayKit at all. It looks cheap, a mobile game, that's not AA."

**Locked decisions:**
- Art direction: **semi-realistic dark fantasy** (Diablo IV / Lost Ark vibe), chosen via AskUserQuestion. Full PBR + normal maps + IBL + shadows + HDR/bloom is required — the low-poly shortcut (skip tangents/normal maps) no longer applies.
- Visual scope: **player + environment only** — "ignore enemies… later we will introduce real enemies with their attack patterns, movements, stats". Goal is "a high end prototype for the looks. A starting point to base the theme of the game." Enemies stay ShapeGroup blobs for now (consistent with [[pre-content-foundation-stage]]).
- Asset strategy: Mixamo for characters/animations (manual user download — no API), Poly Haven/ambientCG CC0 for PBR environment textures/HDRIs/props, Khronos samples as renderer test fixtures. Supersedes the earlier KayKit-based character pipeline (retired).

**Why:** the user's bar for "AA" is shading realism + asset fidelity, not animation/pipeline completeness.

**How to apply:** never propose low-poly/stylized packs (KayKit, Quaternius, Kenney 3D, Synty) for characters or environment. Full plan (quality rules VQ-xx + phases 0–8) saved at `.claude/tasks/aa-visual-upgrade-plan.md` — resume from Phase 0 there; blender not installed yet (winget step in plan). Procedural primitives are sim scaffolding only — label them as placeholders whenever shown, never present them as the visual direction; the bar is real assets (glTF models + textures).
