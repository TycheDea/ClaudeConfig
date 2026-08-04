---
name: dev-singleplayer-pack
description: During development vordar ships as a single-player-style server+client pack — no accounts/auth — but all architecture stays MMO-shaped
metadata: 
  node_type: memory
  type: project
  originSessionId: 880ad8c5-4877-4c84-878b-150275bdd665
---

Decided while scoping Phase 6: resource constraints mean the game is
treated as a single-player title during development — server + client shipped as a
pack emulating single player — and moves to full MMO once there is enough content.
All design still targets the MMO; single-player is a simplification, not a goal.

Consequences: authentication (accounts table, argon2, passwords) is deferred —
Phase 6 became persistence-only with plain-username identity
(`ClientMsg::Login { name }`, env `VORDAR_USER`). The `characters` schema keeps an
accounts-FK path open. When scoping future phases, don't add multi-tenant/auth
surface yet, but never bake in single-player-only assumptions.
