# Vordar — Design Policies

Directives for current design. Code cites clauses as `DESIGN.md §N` — section
numbers are load-bearing; do not renumber.

---

## 1. Name: Vordar

Old Norse **vǫrðr** (warden, watcher) + archaic Norwegian **vorde** (to become).

## 2. Game Concept

- RO-style 3/4 top-down camera, zone-based maps.
- Hack-and-slash presentation: free movement, action feel.
- Discrete FF14-style resolution: telegraphed ground areas snapshot player positions
  at a pre-announced server moment.
- Living world: day/night, timed world events and transformations synchronized across
  all players, world bosses.
- Event-structure progression (invasions, bosses, progression-gated world changes);
  destructible/buildable terrain is OUT.

## 3. Combat Model — "Scheduled Snapshot"

- Movement is free and client-predicted for your own character; remote entities are
  interpolated.
- A hit is one authoritative server-side test — "was entity E inside area A at server
  tick T" — at a pre-announced moment. No continuous hitbox sweeps, no rollback.
- Skills are intent events on the EventBus, resolving at server ticks. Never direct
  transform/state pokes.

### Timing

- Clock sync per session: client derives a server-time offset from ping samples,
  re-checked occasionally.
- Server schedules in absolute server time and broadcasts the SAME message to all
  clients. Never per-client latency-adjusted timestamps.
- Telegraph fill is a pure function of synced time — zero per-frame network updates.
- **T = the moment the telegraph visual completes**: the fire disappearing and the
  damage decision are the same instant for everyone, on every mechanic.

### Position fairness

- Inputs are stamped with synced server time; at snapshot T the server evaluates each
  player's position from inputs timestamped ≤ T (favor-the-defender lag compensation).

### Anti-cheat bounds (in the protocol from v1)

- Arrival deadline: an input claiming time T−x must arrive within ~one RTT after T;
  the server measures RTT continuously.
- Compensation window capped at measured RTT with a hard ceiling; RTT-variance spikes
  during mechanics are flaggable.
- Timestamps must be monotonic and stream-consistent: a backdated input must fit
  plausibly between inputs already received.
- The server recomputes positions from inputs (max speed, collision validated) —
  claimed positions are never accepted.
- Everything else is fully server-authoritative: snapshot tests, damage, cooldowns,
  cast validation, spawns, loot.

## 4. World Systems

- One server-authoritative world clock broadcast; day/night is a render-side function
  of it.
- Timed world events attach to the world clock; clients receive "event N started at
  tick T" and deterministic shared definitions do the rest.
- Boss mechanics are data: a fight is a timeline of mechanic definitions (start time,
  telegraph, target rule, snapshot delay, damage). Data files now, scripts later —
  modders author raid mechanics.
- Telegraphs are prefabs carrying their resolve time; fill animation is pure
  synced-clock math.
- World bosses are regular entities + per-client broadcast throttling under crowd
  load + damage attribution/loot via EventBus.

## 5. Architecture Mapping (engine → MMO)

- Fixed-timestep phases are the authoritative server tick, one app-wide rate; phases
  needing a slower cadence self-gate rather than running at a different tick rate.
- Replication serializes component deltas via the components' serde impls — never
  bespoke wire formats per component.
- Network spawning goes through the string-addressable prefab seam.
- Dedicated server = the App without the render plugin.
- The spatial hash grid drives interest management: each player only receives
  nearby-entity updates.
- World = zone instances, one App per zone server-side; a zone is a chapter running
  headless.
- Authority split: client predicts/displays, server decides; input is "send intent",
  never "move my Transform".

## 6. Disciplines

- Update-phase systems are deterministic and intent-driven: no wall-clock reads, no
  local randomness in gameplay systems. Both sides must compute the exact same step
  or prediction drifts.
- Gameplay intents cross module boundaries via EventBus; tuning numbers live in data
  files. Read-only cross-crate data access goes through the owning crate's pub API.
- Snapshot timing rule (T = telegraph completion) is consistent across every mechanic.
- Anti-cheat caps (arrival deadline, rewind cap) stay in the protocol.

## 7. Scale Expectations

Hundreds of players per zone. Networking and persistence are the bottlenecks, not the
ECS or the spatial grid.

## 8. Live Topology

The unit never changes: **one headless App = one zone instance**.

- Zone instance = (zone, channel); a channel is a parallel copy of a zone. A server
  process hosts any set of zone instances — the mix is configuration, not
  architecture. Parties stay together by picking a channel; world events are global
  clock math, channel-independent.
- Gateway/login service is the single public entry point: owns login and session
  tickets, routes each character to the host of its (zone, channel).
- Coordinator: servers register and heartbeat with load; it assigns zone instances,
  spawns extra channels as they fill, owns the authoritative world clock, starts
  global world events, relays global chat.
- Coordinator ↔ servers speak the same transport over a coordination protocol,
  bridged into each zone App's in-process EventBus. Cross-zone transfer is
  ticket-based: the coordinator picks the target and returns a redirect + a ticket
  the target validates.
- Content ships as hash-addressed packs; a manifest maps zone → required packs, and a
  server downloads only what its zones need. The same machinery serves client
  patching — one pipeline, two consumers.
- Warm pool: standby processes sit registered with zero zones; scaling out is one
  assignment message, not a cold boot.
- Persistence sits behind a message-channel handle so backends swap; the ordering
  invariant is per character (save-before-load across transfers/relogins), not
  global FIFO.
- Content and feel come before this infrastructure — you scale a game, not an empty
  grid.
