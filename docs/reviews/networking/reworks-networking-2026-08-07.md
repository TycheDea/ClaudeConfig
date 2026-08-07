# Networking & Server Reworks — 2026-08-07

Rework-scale companion to `audit-networking-2026-08-07.md`: findings that
need a design pass before implementation. Consumed by /plan-rework, which
turns one rework into a plan of fix-sized steps for /implement-finding.

All three entries are carried forward from `reworks-networking-2026-07-11.md`
(deleted; git history keeps it), re-verified against the current tree and
renumbered: old rework 2 → **1**, old rework 6 → **2**, old rework 9 → **3**.
Old reworks 1, 3, 4, 5, 7, 8, 10, 11 are resolved — see "Resolved since last
report". No carried rework names a plan file; all plan files in this folder
belonged to resolved reworks and were deleted with them.

## Findings (implementation order)

Cross-type queue (mirrored verbatim from `audit-networking-2026-08-07.md`):

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

### 1. QUIC connection migration for seamless network switching (carried; was rework 2 of 2026-07-11)

- **Evidence:** re-verified open. The client reconnect state machine treats
  every connection loss identically: full teardown of the replicated world,
  backoff redial, relogin, fresh AOI/prediction state
  (`client/vordar-client/src/net/lifecycle.rs:149-184` teardown,
  `:219-232` disconnect handling, `:238-265` redial). A mere network path
  change (Wi-Fi → cellular, NAT rebind) goes through that whole cycle even
  though QUIC supports migrating a live connection. Server-side, the
  transport config addresses only stream caps and idle timeout
  (`smirk/engine-net/src/common.rs:124-131`) — quinn's migration/path-
  validation behavior is whatever the default is, unexamined and untested.
  The impairment layer (`smirk/engine-net/src/impair.rs`) has latency, loss,
  jitter, and clock skew, but no knob for a mid-session client address
  switch, so migration behavior cannot be exercised headless today.
- **Ideal:** quinn's connection migration keeps the session alive across
  client address changes — no relogin, no world teardown, no visible
  interruption beyond a latency blip.
- **Gap:** every path change costs a full disconnect/reconnect cycle and its
  gameplay interruption; on mobile-style networks that is frequent, not
  exceptional.
- **Suggestion:** design pass on enabling and validating quinn's migration
  support server-side (path validation, anti-amplification interplay with
  the accept-loop retry gate, `smirk/engine-net/src/server.rs:441-448`) and
  on the session-identity implications: sessions are keyed by `ConnId` with
  the login token held on `PlayerConn`
  (`server/vordar-server/src/net/mod.rs:134-143`), so the design must show a
  migrated path cannot become a session-hijack vector.
- **Outcome:** `7/10` — seamless roaming for the connection classes real
  players actually have; meaningless on loopback, which is why it is
  WAN-triggered.
- **Confidence:** `6/10` — the gap is a code-read certainty; the outcome
  score rests on quinn's migration machinery working as documented, which
  nothing in this repo has exercised yet.
- **Cost:** `6/10`
- **Path:** (1) design: quinn migration config + security analysis against
  the flood controls; (2) impairment-layer knob for mid-session address
  switching; (3) e2e test migrating a session mid-combat with no relogin.

### 2. Certificate story and `Redirect { addr: SocketAddr }` — the final trust model cannot be swapped in without a protocol change (carried; was rework 6 of 2026-07-11)

- **Evidence:** re-verified open, all five legs. Fresh self-signed cert for
  `"localhost"` per boot (`smirk/engine-net/src/common.rs:97-115`); the
  client disables verification via `SkipServerVerification`
  (`common.rs:138-150`, `:152-188`) — unconditionally compiled, not
  feature-gated; SNI hardcoded `"localhost"`
  (`smirk/engine-net/src/client.rs:192`); `Redirect` carries a bare
  `SocketAddr` (`game/vordar-protocol/src/lib.rs:150`); the zone directory
  is IP:port arithmetic (`server/vordar-server/src/main.rs:44-49`).
  Hostname-validated TLS needs names the protocol doesn't speak.
- **Ideal:** zone directory and `Redirect` carry hostnames; the client
  verifies against a real chain (public CA or pinned private game CA);
  skip-verification feature-gated out of release builds.
- **Gap:** every wire byte is encrypted but unauthenticated — a MITM can be
  any zone. Fine on loopback by design; a hard blocker for the first
  non-loopback deployment, and the protocol shape (addr, not hostname) is
  what makes it a rework rather than a config change.
- **Suggestion:** one design pass covering: hostname in `Redirect` + the
  directory (protocol bump); an SNI parameter on `NetClient::connect`;
  feature-gating the dev verifier; real CA + pinned root at deployment.
  Fold in (from the audit's deferred section): refuse non-loopback bind
  while the dev verifier is compiled in (default bind `127.0.0.1:5151`,
  `main.rs:35-39`), and consider binding session tokens to a TLS channel
  exporter. Handshake reason codes already exist (`Ctrl::Reject`,
  `common.rs:22-27`), so cert failures can be surfaced distinctly.
- **Outcome:** `9/10` — the trust model becomes real; everything else about
  WAN deployment stands on this.
- **Confidence:** `8/10` — the gap and the protocol dependency are code-read
  certainties; the CA/deployment leg is standard practice argued from
  comparable systems, not yet exercised here.
- **Cost:** `6/10`
- **Path:** (1) hostname in `Redirect` + directory (protocol bump); (2) SNI
  parameter on `NetClient::connect`; (3) feature-gate the dev verifier +
  non-loopback bind refusal; (4) real CA + pinned root at deployment;
  (5) MITM regression test (connection to a wrong-cert server must fail
  closed with a surfaced reason).

### 3. Multi-core network runtime sharding — PARKED (carried; was rework 9 of 2026-07-11)

**Parked, not ordered.** Gate: ">50% of a core at target load." Last
measurement: the restored 200-bot soak recorded `net_busy_pct=13.6`. The
gate could not be re-evaluated this audit (re-running the soak is heavy
compute, not authorized by an audit contract); the busy-time instrumentation
that feeds it is live (`smirk/engine-net/src/server.rs:412-428`,
`NetMetrics::busy_micros`, surfaced via `NetServerState::metrics`).

- **Evidence:** re-verified: `tokio::runtime::Builder::new_current_thread()`
  at `smirk/engine-net/src/server.rs:207` — all connections' TLS, packet
  processing, and framing share one OS thread per endpoint (client mirror at
  `client.rs:83`).
- **Ideal:** network capacity scales with cores: runtime pool sharded by
  `ConnId`, no cross-shard locks on the per-frame paths.
- **Gap:** one core of QUIC crypto is the zone's hard vertical ceiling —
  but measurement says the ceiling is ~7× away at the current target load,
  which is exactly why this stays parked.
- **Suggestion:** only design this once the soak shows the gate crossed;
  then decide the sharding boundary (per-connection vs per-endpoint), what
  state crosses shards, and how the sim-thread channel model changes.
- **Outcome:** `7/10` at fleet scale; `1/10` before the gate is crossed.
- **Confidence:** `7/10` — the single-thread ceiling is architectural fact;
  the "not yet needed" half rests on the 13.6 % soak number, which is real
  but from a prior date.
- **Cost:** `8/10`
- **Path:** (1) prerequisite: a soak run crossing the gate; (2) design:
  shard boundary + state ownership; (3) implement behind the same public
  `NetServer` API; (4) soak comparison proving scaling.

## Carried forward from previous report

Reworks 1–3 above, from `reworks-networking-2026-07-11.md` (its reworks 2,
6, 9), each re-verified against the current tree with fresh evidence anchors.

## Resolved since last report

From the 2026-07-11 reworks file, verified resolved in code (their plan
files, listed per entry, were deleted alongside the superseded reports):

- **Old rework 1** (accounts, tokens, cooldown persistence;
  `plan-networking-rework-1-2026-07-13.md`) — accounts table + migration
  ladder (`server/vordar-server/src/db.rs:34-53`), token-bearing `Login`
  verified against `sha256(token)` (`game/vordar-protocol/src/lib.rs:52-57`,
  `db.rs:350-391`), token-gated session takeover
  (`receive.rs:194-242`), per-IP failed-login rate limiting
  (`net/login.rs`), cooldown remainders persisted and restored
  (`server/vordar-server/src/net/mod.rs:286-301`, `receive.rs:539-547`).
  The transfer-ticket
  remainder lives in the audit's deferred section.
- **Old rework 3** (message classes on one stream;
  `plan-networking-rework-3-2026-07-13.md`) — snapshots + acks and move
  intents ride datagrams (`broadcast.rs:216-232`,
  `client/vordar-client/src/net/prediction.rs:240-246`), clock pings ride
  the datagram lane bypassing the writer queue
  (`smirk/engine-net/src/client.rs:277-297`, `server.rs:602-650`),
  both-direction loss impairment exists
  (`impair.rs:29-50`).
- **Old rework 4** (jitter buffer;
  `plan-networking-rework-4-2026-07-14.md`) — tick-indexed `NetBuffer` +
  fixed-delay playback + capped extrapolation
  (`client/.../interpolate.rs`).
- **Old rework 5** (wire format waste;
  `plan-networking-rework-5-2026-07-13.md`) — zone-local u32 wire ids
  (`net/repl_ids.rs`), quantized `WirePos`
  (`game/vordar-protocol/src/lib.rs:203-243`), u16 prefab table
  (`lib.rs:73-86`), `hp: Option<i32>` (`lib.rs:186-191`). (The one
  leftover String is the new audit's finding 6.)
- **Old rework 7** (collision-aware replay;
  `plan-networking-rework-7-2026-07-14.md`) — replay folds `predict_step`
  with anchored statics
  (`client/vordar-client/src/net/prediction.rs:112-135`), wall-hug test in
  place (`prediction.rs:384-424`).
- **Old rework 8** (persistence lifecycle;
  `plan-networking-rework-8-2026-07-12.md`) — `user_version` migration
  runner refusing newer schemas (`db.rs:61-79`), signal-driven
  drain-save-exit shutdown (`main.rs:56-69`, `net/shutdown.rs`),
  `NetServer` deterministic Drop shutdown
  (`smirk/engine-net/src/server.rs:335-348`, `:510-515`). The
  durability-classes
  remainder lives in the audit's deferred section (trigger: first
  transactional feature).
- **Old rework 10** (zone-thread watchdog;
  `plan-networking-rework-10-2026-07-12.md`) — `supervise_zone` rebuilds a
  panicked zone on the same address under a restart budget
  (`supervisor.rs:79-97`), enabled by the rework-8 shutdown path;
  `DbHandle::fork()` keeps rebuilt reply channels isolated
  (`db.rs:194-201`).
- **Old rework 11** (RESYNC vs extrapolation-cap interaction;
  `plan-networking-rework-11-2026-07-16.md`) — the playback cursor clamps at
  `latest_state_tick + EXTRAP_CAP_TICKS` and resyncs forward-only
  (`client/vordar-client/src/net/interpolate.rs:26-43`, `:134-144`); the
  sustained-stall,
  short-resume, and reconnect-scale tests all assert no backward step
  (`interpolate.rs:297-551`).
