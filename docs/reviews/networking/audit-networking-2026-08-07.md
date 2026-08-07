# Networking & Server Audit — 2026-08-07

Fresh full sweep (client action end-to-end: input → datagram send → server
validate → simulate → replicate → client apply; persistence round-trip:
save → FIFO worker → reload) plus re-verification of every prior finding.
Prior state processed: `audit-networking-2026-07-28.md` (queue fully cleared
2026-08-02 — all nine strike commits verified in git, see Resolved) and
`reworks-networking-2026-07-11.md` (reworks 2, 6 still open, 9 parked —
re-verified and carried into `reworks-networking-2026-08-07.md` as reworks
1, 2, 3). Note: the dispatch brief stated `scripts/lint-findings.sh` no
longer exists; it does exist in the game repo and was run as the close-out
gate.

What held up under this sweep, verified in code: split cast/move sequence
lanes (`cast_seq`/`cast_t` on `PlayerConn`, protocol v16); warmed-RTT
arrival deadline with the 200 ms bootstrap floor; fail-closed persistence
(health clamp into prefab bounds, corrupt-cooldown lockout, FK enforcement,
migration ladder with `user_version` refusal of newer schemas); constant-time
token compares at all three sites; pre-login pending reaper; per-conn EWMA
RTT baseline with k·σ spike logs at cast arrival and mechanic resolve;
datagram counters + snapshot-bytes gauge on the periodic metrics line with
the 1200 B debug assert; fixed-delay playback with capped extrapolation,
forward-only resync, and the horizon clamp (rework 11's fix); collision-aware
prediction replay through `predict_step`; zone supervision with restart
budget and `NetServer`'s deterministic Drop shutdown; the shared FIFO
DbWorker with batched transactions and `fork()` reply isolation; and the
`docs/online-play.mmd` diagram (now at `.claude/docs/online-play.mmd`), which
matches the code on every lane, lifecycle, and denial path checked.

## Ideal end state

Every connection is accountable from the first UDP packet to login or
closure — no state at any layer where a hostile client can hold a slot
without a running deadline. Persistence failures are visible and fail
toward denial, never toward a silent hang. The client reacts to each denial
reason with the recovery that reason permits. Every inbound message class is
rate-bounded by the same budget discipline, and no wire message carries a
string a table index already covers.

## Findings (implementation order)

Cross-type queue (mirrored verbatim in `reworks-networking-2026-08-07.md`):

> **finding 1 → finding 2 → finding 3 → finding 4 → finding 5 → finding 6 →
> rework 1 → rework 2.** Rework 3 is **parked**, not ordered: its gate is
> ">50% of a core at target load" and the last 200-bot soak measured
> `net_busy_pct=13.6`.
>
> 1–3 are the connection-accountability cluster: 1 first because 2's
> guarantee ("every accepted connection reaches `Connected` or dies") rests
> on the transport level closing its own gap; 3 after 2 because its new
> denial exit should flow through the budget 2 installs. 4 after 3: the
> client's reason-differentiated denial handling must know every reason the
> server can send, including any variant 3 adds. 5 and 6 are independent
> hardening/wire cleanups, impact-ordered. Reworks last: both are
> WAN-triggered design passes independent of the fixes; rework 2
> additionally fires on any non-loopback deployment.

### 1. Server-side handshake has no deadline — a connection that never sends `Hello` is unaccountable at every level

- **Evidence:** `smirk/engine-net/src/server.rs:566-572` — `incoming.await`,
  `connection.accept_bi().await`, and `handshake(...)` run with no timeout;
  the client side bounds its half at 5 s (`smirk/engine-net/src/client.rs:28`,
  `:205-207`) but the server waits forever. The connection-cap reservation is
  taken before any of this (`server.rs:453-465`), while `ServerEvent::Connected`
  fires only after the handshake succeeds (`server.rs:585`) — so the
  app-level pre-login reaper (`server/vordar-server/src/net/receive.rs:134-152`,
  the `b0f789b` fix) never sees this connection. The only reaper left is the
  30 s idle timeout (`smirk/engine-net/src/common.rs:127-130`), which any
  packet resets: a hostile client that completes the QUIC handshake, never
  opens the bidi stream (or sends a partial `Hello` frame), and emits
  QUIC-level pings holds a per-IP slot indefinitely.
- **Ideal:** "handshake → login within a deadline, or the server closes it"
  holds at the transport level too, so the app-level guarantee has no floor
  below it that leaks.
- **Gap:** the 2026-07-28 finding 4 closed the post-`Connected` half of
  pre-login slot-holding; this is the pre-`Connected` half of the same
  guarantee — a "never X" that wasn't closed at every source.
- **Suggestion:** wrap the accept_bi + handshake sequence in
  `tokio::time::timeout` (~10 s); the error path already runs the standard
  cleanup (cap release, no `Disconnected` since `Connected` never fired).
- **Outcome:** `8/10` — the last unbudgeted pre-login state closes; flood
  posture becomes uniform from first packet to login.
- **Confidence:** `8/10` — code read of both levels plus the prior finding's
  app-level analysis; that QUIC pings reset the idle timer is spec behavior
  (RFC 9000 §10.1), not measured here — the regression test proves the fix
  observable either way.
- **Cost:** `2/10`
- **Path:** (1) timeout constant + wrap in `handle_connection`; (2) test: a
  raw quinn connection completes the QUIC handshake, never sends `Hello`,
  and must be closed within the deadline while a normal `NetClient` connect
  still succeeds; (3) flood suite green.

### 2. A denied or redirected login leaves the connection in no map — unbounded slot-holding after `complete_db_load`

- **Evidence:** `server/vordar-server/src/net/receive.rs:442-484` —
  `complete_db_load` removes the conn from `loading` (`:447`) on every
  outcome, then: `BadToken` (`:452-464`) sends `LoginDenied` and returns;
  login-routing `Redirect` (`:469-483`) sends the redirect and returns;
  spawn failure (`:577`) logs and falls through — in all three the
  connection is now in none of `pending`/`loading`/`conns`. The protocol is
  deliberately client-closes (`game/vordar-protocol/src/lib.rs:145-161`),
  which only polite clients honor, and the reaper scans only `pending`
  (`receive.rs:137-143`). A hostile client that presents a wrong token for a
  claimed name and ignores the denial holds its slot indefinitely — the
  exact state the pre-login deadline (`b0f789b`) was built to forbid. The
  synchronous denials inside `handle_login` (rate-limit `:179-182`, bad name
  `:184-189`, takeover mismatch `:209-214`, in-flight mismatch `:234-238`)
  all return before `pending.remove` at `:244`, so those paths stay
  budgeted — only the async-outcome exits leak.
- **Ideal:** every non-grant login outcome re-arms the same bounded budget:
  the client gets its window to close politely, and the reaper closes it
  otherwise.
- **Gap:** the "every connection accounted for from accept to login" ideal
  the 07-28 report stated is broken specifically for connections that DID
  log in and were turned away.
- **Suggestion:** at each non-grant exit of `complete_db_load` (BadToken,
  Redirect, unknown-zone is already a disconnect, spawn failure), insert the
  conn back into `pending` stamped `now` — the existing reaper then closes
  it within `PENDING_LOGIN_DEADLINE_MICROS` if the client doesn't.
- **Outcome:** `8/10` — closes the remaining slot-exhaustion channel above
  the transport.
- **Confidence:** `9/10` — pure code-flow read with every login exit path
  enumerated above.
- **Cost:** `2/10`
- **Path:** (1) re-arm `pending` at the three exits; (2) e2e test: login
  with a mismatched token, ignore the denial, assert the server closes the
  connection within the deadline (and that a redirected connection that does
  close promptly is untouched); (3) security suite green.

### 3. A DB error during login is swallowed — the connection hangs in `loading` forever and saves fail silent

- **Evidence:** `server/vordar-server/src/db.rs:264-269` — the worker's
  `Login` arm on a rusqlite error does `log::error!` and sends no reply, so
  `DbLoaded` never arrives and the conn sits in `state.loading` permanently
  (the reaper explicitly excludes `loading`, `receive.rs:141-143`); the
  client shows an infinite "logging in" hang (it sends `Login` once per
  `Connected`, `client/vordar-client/src/net/lifecycle.rs:65-76`). Related
  fail-silent shape: `DbHandle::login`/`save` discard channel-send errors
  (`db.rs:207-215`, `:219-221`), so if the worker thread ever dies, every
  subsequent save is dropped and every login hangs with no log line at the
  call site.
- **Ideal:** a persistence failure during login is an explicit denial the
  client can see and the server can budget; a dead worker channel is loud.
- **Gap:** disk-full, file-corruption, or a worker bug turns into an
  invisible hang plus an unreapable slot instead of an error.
- **Suggestion:** add an error outcome (e.g. `DbLoginOutcome::Error`) the
  worker replies with on rusqlite failure; `complete_db_load` maps it to
  `LoginDenied` + the finding-2 re-armed budget and disconnects. Log at
  error level when a `DbHandle` send fails because the channel is closed.
- **Outcome:** `7/10` — persistence failures become observable denials.
- **Confidence:** `8/10` — code read; an induced-failure test (drop the
  `characters` table out from under a login via a raw connection) confirms
  the end-to-end path.
- **Cost:** `3/10`
- **Path:** (1) error variant + worker reply; (2) map to denial in
  `complete_db_load` (after finding 2 so the exit is budgeted); (3) induced
  SQL-failure test asserting the client receives a denial rather than
  hanging; (4) closed-channel send logging.

### 4. The client latches `login_denied` on `RateLimited` — a transient denial permanently stops reconnection

- **Evidence:** `client/vordar-client/src/net/lifecycle.rs:119-129` — both
  `LoginDenyReason`s set `state.login_denied = true`;
  `client/vordar-client/src/net/mod.rs:122-126` documents the latch;
  `maybe_reconnect` (`lifecycle.rs:239-241`) and `handle_disconnected`
  (`:223-227`) then refuse every future redial. But `RateLimited`
  (`game/vordar-protocol/src/lib.rs:165-172`) is a property of the source IP
  over a 10 s window (`server/vordar-server/src/net/login.rs:6-9`) — e.g. a
  NAT-shared address where another client burned the budget. The only
  recovery is restarting the game.
- **Ideal:** the client's reaction matches what each reason permits:
  credentials that will never work stop the redial; a rate limit that
  expires in seconds retries after a long backoff.
- **Gap:** the latch was designed for BadCredentials ("retrying with the
  same bad credential would only be denied again") and over-applies to a
  reason whose premise expires by definition.
- **Suggestion:** latch only on `BadCredentials`; on `RateLimited` schedule
  a redial at the top of the backoff ladder (`RECONNECT_MAX_BACKOFF`, 8 s —
  conveniently just under the 10 s failure window).
- **Outcome:** `7/10` — removes a restart-the-client dead end that will
  surface the first time two players share an IP.
- **Confidence:** `9/10` — code read of both sides; the window constant
  makes the transience definitional, not speculative.
- **Cost:** `2/10`
- **Path:** (1) branch on reason in the `LoginDenied` arm; (2) test: a
  rate-limited denial followed by a later granted login succeeds without a
  process restart, while a BadCredentials denial still stops redialing;
  (3) e2e suite green.

### 5. Inbound rate limiting misses two message classes: ctrl-ping datagrams and oversized `MoveIntents` batches

- **Evidence:** two verified asymmetries. (a)
  `smirk/engine-net/src/server.rs:614-650` — the datagram task's `TAG_CTRL`
  arm (`:620-630`) answers every ping with a pong outside the token bucket;
  the bucket guards only `TAG_APP` (`:631-646`). A hostile client can spam
  ping datagrams at line rate for free server work (equal-size reflection to
  an address QUIC already validated — CPU cost on the net thread, no
  amplification; the stream-side ping arm is self-limiting via the
  writer-queue kick, `server.rs:156-171`). (b)
  `server/vordar-server/src/net/receive.rs:722-753` — `queue_move_intents`
  iterates every entry of `ClientMsg::MoveIntents`, whose `Vec` is unbounded
  by the protocol (`game/vordar-protocol/src/lib.rs:33-42` — the contract
  says "up to the two previous"); the 1 KiB inbound frame cap
  (`smirk/engine-net/src/common.rs:10`) bounds it at ~50 entries, ~17× the
  contract, each fully validated.
- **Ideal:** every inbound message class is charged against the same budget
  discipline, and every wire collection has its contract enforced at the
  top of its handler — the rule finding `4da2655` established for skill ids.
- **Gap:** both residuals are CPU-only, bounded by the attacker's own
  bandwidth — hygiene, not a hole; same class as the 07-28 skill-id bound.
- **Suggestion:** move the datagram task's bucket refill/charge above the
  tag match so ctrl and app datagrams share it; reject batches longer than
  `MOVE_RING_LEN` (3, `client/vordar-client/src/net/prediction.rs:30`) plus
  a small slack, counted through `record_reject`.
- **Outcome:** `6/10` — uniform inbound budgeting; removes the two remaining
  free-work paths.
- **Confidence:** `8/10` — code read; magnitudes derived arithmetically from
  the frame cap, not measured under load.
- **Cost:** `2/10`
- **Path:** (1) bucket the ctrl datagram arm (clock sync tolerates a
  throttled ping — the burst is 8 pings at 100 ms,
  `smirk/engine-net/src/clock.rs:12-13`, far under the 120/s refill);
  (2) batch-length check + unit test (over-length batch rejected, length-3
  batch untouched); (3) flood suite green.

### 6. `MechanicScheduled.telegraph_prefab` re-sends a `String` the connection's prefab table already indexes

- **Evidence:** `game/vordar-protocol/src/lib.rs:126-133` — the field is a
  `String`, encoded per AOI recipient per cast at
  `server/vordar-server/src/net/receive.rs:354-361` (Scheduled) and
  `:421-428` (Leap); the client resolves it by name
  (`client/vordar-client/src/net/lifecycle.rs:102-105`). The same connection
  already holds the zone's `PrefabTable` (`receive.rs:568-571`), and every
  `EntityState.prefab` rides as a `u16` index (`lib.rs:180-184`) — this is
  the one remaining prefab-by-String on the wire.
- **Ideal:** one prefab-naming scheme on the wire: the table index,
  everywhere.
- **Gap:** consistency plus a few dozen bytes per cast on the reliable
  stream — low rate, low impact; last in the fix queue.
- **Suggestion:** change the field to `u16`, encode via the server's
  `prefab_table` reverse index, resolve client-side through `prefab_names`
  exactly like AOI enters; `PROTOCOL_VERSION` bump.
- **Outcome:** `5/10`
- **Confidence:** `9/10` — code read; both sides of the table already exist
  and are exercised by the AOI path.
- **Cost:** `2/10`
- **Path:** (1) protocol field + version bump; (2) server encode via reverse
  index (telegraph prefabs load from the same `PrefabLibrary` the table is
  built from); (3) client resolve + error-skip like
  `apply_aoi_delta`; (4) roundtrip + telegraph e2e tests.

## Deferred until multiplayer (verified once — not in the queue)

Carried forward from 2026-07-28, cross-references updated to this report's
numbering; facts re-checked on the current tree where the fixes since then
touched them. Triggers: real accounts/hosting work, or any non-loopback
deployment.

- **TLS trust** — `SkipServerVerification` accepts any cert
  (`smirk/engine-net/src/common.rs:152-188`; per-boot self-signed at
  `:97-115`). Queued as **rework 2** in `reworks-networking-2026-08-07.md`
  (hostname-carrying Redirect, feature-gated dev verifier, real CA) —
  execute that plan; fold in: refuse non-loopback bind while the dev
  verifier is compiled in (default bind `127.0.0.1:5151`,
  `server/vordar-server/src/main.rs:35-39`, zone ports `base + i`), and
  consider binding session tokens to a TLS channel exporter.
- **TOFU auth** — name claim = ownership forever; token is a plaintext-hex
  bearer file client-side (`client/vordar-client/src/credentials.rs:34-57`),
  SHA-256 hash at rest server-side (`db.rs:351`). Unsalted SHA-256 of a
  random 32-byte token is cryptographically fine at rest — the real gaps are
  lifecycle (rotation, revocation, recovery, multi-device). Replacement is
  DESIGN §8's gateway (argon2id or OAuth → short-lived zone tickets).
- **Transfer tickets** — Redirect is save-then-`{zone, addr}` with no signed
  proof (`server/vordar-server/src/net/transfer.rs:61-72`; login re-routing
  off DB zone at `receive.rs:469-484`). The addr is not client-influenceable
  today; MITM amplification belongs entirely to the TLS item. Ticket design
  is DESIGN §8 verbatim.
- **Cross-zone session uniqueness** — emergent from one process + one FIFO
  DB channel (every login routes by DB zone ownership before spawn; transfer
  removes the `PlayerConn` in the tick it saves the target zone; the single
  FIFO `DbWorker` orders every save before the next load). The fleet design
  must replace those two assumptions with an explicit session lease
  (CAS-acquire, heartbeat, revocation).
- **Process isolation** — one process, thread-per-zone, shared DbWorker;
  `supervise_zone` restarts a panicked zone on the same address with budget
  3 (`server/vordar-server/src/supervisor.rs:48`, `:79-97`); once the budget
  is spent the listener stays bound but dead and other zones keep
  redirecting into it (`supervisor.rs:19-30` logs this loudly). Process-per-
  zone and a live directory are DESIGN §8 coordinator work.
- **Anti-cheat telemetry** — implemented baseline verified: intents-only
  wire, per-lane seq/time monotonicity, 50 ms future slack, dir cap, queue
  cap 16, server-time scheduling, applied-velocity rewind capped at 200 ms,
  AOI-scoped combat meta, EWMA RTT baseline + k·σ spike logs. Live movement
  is collision-validated; the only uncollided path is the ≤200 ms rewind
  reconstruction (`server/vordar-server/src/net/mechanics.rs:138-147`
  replays `step` + `PlayRadius`
  without statics). Behavioral detection and rewind-tightening policy need a
  design pass at hardening time.
- **World clock authority** — per-process `Instant` origin
  (`main.rs:53`); restart resets world time. The seam exists (all reads go
  through `NetServerState::world_at`/`world_micros`,
  `server/vordar-server/src/net/mod.rs:276-283`) —
  pin process clocks to coordinator samples when a second process appears.
- **Fleet-scale snapshot cost** — thread-per-zone + AOI + stagger is the
  right dev shape; past ~100 concurrent, pre-sorted AOI gather, encode
  scratch reuse, and interest tiers are the candidates, gated on the soak
  suite's `net_busy_pct` (13.6 % at 200 bots — same gate as rework 3).
- **Capability negotiation** — single `u8` version with hard `Reject` is
  correct pre-launch; reserve a capabilities bitfield or min/max range in
  `Hello` before external playtests.
- **DoS remainder** — flood baseline verified live (buckets, caps, retry
  validation, login limiter, writer-queue kick, pre-login reaper). Unbounded
  account-row creation from fresh-name spam is real but WAN-only; creation
  rate-limiting belongs with the gateway, which removes direct zone `Login`
  anyway.
- **Secrets/ops/durability** — credentials-file ACLs/keychain, Linux
  `deny.toml` triple (trigger: "when server hosting lands"), backup/migrate
  runbook, RPO ≈ one 30 s autosave window
  (`server/vordar-server/src/net/autosave.rs:9`), `synchronous = NORMAL`
  tradeoff documented at
  `db.rs:155-159`. Durability classes (some writes synchronous-confirmed)
  land with the first transactional feature (items/trades) — the schema
  migration runner they need already exists. Near-free hygiene piece:
  `#![forbid(unsafe_code)]` on vordar-server/vordar-protocol/vordar-game.
  Fleet-class security tests (cross-zone twin, transfer forgery, MITM
  regression) land with their respective reworks.

## Carried forward from previous report

No open fix-scale findings: the 2026-07-28 queue was fully cleared
2026-08-02 and every strike commit was verified present in git history
(`3794018`, `3373566`, `4c69d44`, `b0f789b`, `a652467`, `4da2655`,
`e9ff97e`, `8df21f6`, `59be85c`). The "Deferred until multiplayer" section
above is the carried material, re-anchored to current line numbers. The open
reworks carry in `reworks-networking-2026-08-07.md`.

## Resolved since last report

All nine 2026-07-28 findings, re-verified against the current tree:

1. **Cast/move sequence split** — `PlayerConn.cast_seq`/`cast_t`
   (`server/vordar-server/src/net/mod.rs:155-160`), `dispatch_cast`
   validates only against them (`receive.rs:302-308`),
   `PROTOCOL_VERSION = 16` with the move-only ack documented
   (`game/vordar-protocol/src/lib.rs:16`, `:103-113`).
2. **Warmed arrival deadline** — `max_age = if rtt == 0 { MAX_REWIND } else
   { rtt } + margin` (`receive.rs:704-711`) with boundary tests at 20 ms and
   180 ms (`receive.rs:817-846`).
3. **Fail-closed persistence** — health clamp `[1, hp.max]`
   (`receive.rs:515-523`), corrupt-cooldown full lockout via
   `cooldowns_corrupt` (`receive.rs:526-547`, `db.rs:93-97`, `:324-330`),
   `PRAGMA foreign_keys = ON` (`db.rs:160-165`).
4. **Pre-login deadline** — `pending` map + reaper at 10 s
   (`receive.rs:43-47`, `:134-152`). (Finding 2 above is the post-loading
   completion of the same guarantee.)
5. **Constant-time token compares** — `subtle::ConstantTimeEq` at takeover
   (`receive.rs:209`), in-flight eviction (`:234`), and the DB digest
   compare (`db.rs:375-380`).
6. **Skill-id bound** — `skill_id.len() > 64` rejected through
   `record_reject` at the top of `dispatch_cast` (`receive.rs:294-298`).
7. **RTT-variance tracking** — per-conn EWMA mean/variance
   (`smirk/engine-net/src/server.rs:56-103`), spike logs at cast arrival and
   mechanic resolve (`server/vordar-server/src/net/mod.rs:344-352`,
   `receive.rs:300`, `mechanics.rs:83-86`).
8. **Datagram metrics + snapshot budget** — three datagram counters and the
   snapshot gauge on the periodic line (`broadcast.rs:92-107`), 1200 B
   debug assert + gauge at the send site (`broadcast.rs:221-232`).
9. **HitResult client presentation** — `handle_hit_result` drives the VFX
   burst seam for known ids (`client/vordar-client/src/net/apply.rs:63-78`,
   `lifecycle.rs:107-110`).
