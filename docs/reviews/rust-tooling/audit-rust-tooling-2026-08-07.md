# Rust & Tooling Audit — 2026-08-07

Second audit in this domain. Prior reports (2026-07-17 pair) processed per
audit-base step 1: findings 1–12 and 13 verified resolved, finding 14
re-verified still red and carried forward as finding 2 below. Close-out gate
note: the dispatch brief stated `scripts/lint-findings.sh` no longer exists;
it does exist (game repo, `scripts/lint-findings.sh:1`) and was run against
both reports before superseding — the brief's claim was stale, not the script.

## Ideal end state

`cargo clippy --workspace --all-targets -- -D warnings` is green — and stays
green for every individual `-p <crate>` scoping, so per-crate gates are
usable, not just the feature-unified workspace run. The lockfile tracks
latest-compatible routinely; no dependency sits a major behind without a pin
comment stating a reason that is still true; every shared dep has exactly one
version declaration. The bench regression gate's durable log actually
receives its lines, and BASELINE.md's tables and machine block describe the
tree that produced them.

## Findings (implementation order)

Cross-type queue (no rework-scale findings this audit — the queue is all
fixes; `reworks-rust-tooling-2026-08-07.md` mirrors this note):

> **finding 1 → finding 2 → finding 3 → finding 4 → finding 5 → finding 6 →
> finding 7.**
>
> Finding 1 goes first because it repairs the bench gate's durable log before
> any later step runs that gate. Finding 2 makes scoped clippy usable as the
> per-crate verification every later diff cites. 3 precedes 4 so the lock
> refresh resolves through single declarations. 4 precedes 5–6 so the
> compatible-refresh diff is isolated from the semver-major diffs. 7 is last
> because 4, 5, and 6 each move codegen and would stale a fresh baseline.

### 1. `bench-gate.ps1` appends its durable gate log to a directory that no longer exists

- **Evidence:** `scripts/bench-gate.ps1:23` computes the log path as
  `$repoRoot\docs\benchmarks\gate-log.txt` and `scripts/bench-gate.ps1:78`
  region appends to it via `Add-Content`. Commit 5e251c0 (2026-08-04,
  "Remove docs folder (moved to ClaudeConfig)") deleted the game repo's
  `docs/benchmarks/` — the game-tree `docs/` now contains only
  `observability/` (checked 2026-08-07). The durable log the docs describe
  lives at `.claude/docs/benchmarks/gate-log.txt:1` (single line,
  2026-07-23). `Add-Content` to a missing directory is a non-terminating
  error, so the script still prints its verdict and exits by threshold —
  the gate "passes" while its durable history silently stops accruing. The
  header comment (`scripts/bench-gate.ps1:13`) states the old path too.
- **Ideal:** every gate run lands one line in the one real log
  (`.claude/docs/benchmarks/gate-log.txt`), and a failed append fails the
  run loudly — a check must fail when its promised behavior is broken.
- **Gap:** since the docs move, any gate run appends into the void; the
  criterion baselines are gitignored, so the log was the only durable
  record.
- **Suggestion:** point `$gateLog` at
  `.claude\docs\benchmarks\gate-log.txt`, wrap the append so a failure
  exits non-zero, and fix the header comment.
- **Outcome:** `7/10` — restores the durable-history half of the regression
  gate; the pass/fail half was never broken.
- **Confidence:** `8/10` — code read plus verified directory state
  (game-tree `docs/benchmarks/` absent, `.claude` log present); the failure
  mode is PowerShell's documented non-terminating `Add-Content` behavior,
  not observed live. Running the gate once after the fix demonstrates it.
- **Cost:** `1/10` — three-line script edit.
- **Path:** (1) repoint `$gateLog`, add an error check on the append; (2)
  fix the header comment; (3) run
  `powershell scripts/bench-gate.ps1 -Bench snapshot` once; proof: a new
  dated line appears in `.claude/docs/benchmarks/gate-log.txt`.

### 2. Offscreen-only renderer items are not cfg-gated, so scoped clippy is red (carried from 2026-07-17 reworks finding 14, now root-caused)

- **Evidence:** re-verified 2026-08-07:
  `cargo clippy -p vordar-benches --all-targets -- -D warnings` exits 101
  with 5 `dead_code` errors — `smirk/engine-renderer/src/camera.rs:104`
  (`fit_bounds`), `camera.rs:116` (`look_at`), `camera.rs:210`
  (`write_viewport`), `smirk/engine-renderer/src/ssao.rs:279`
  (`SsaoTargets.ao`), `ssao.rs:353` (`WhiteAo`) / `ssao.rs:359`
  (`WhiteAo::new`). The error set has evolved since 07-17 (fit_bounds and
  look_at are new; the old width/height/blurred_ao field errors are gone).
  Root cause, settled this pass: every consumer of these items lives in
  `smirk/engine-renderer/src/offscreen.rs` (`:410` reads `.ao`, `:490`
  fit_bounds, `:514` look_at, `:778` write_viewport, `:203`/`:299` WhiteAo),
  and that module is feature-gated (`smirk/engine-renderer/src/lib.rs:18-19`,
  `#[cfg(feature = "offscreen")]`) — but the items themselves are not. The
  workspace-wide clippy run is green only because vordar-client's
  dev-dependency (`client/vordar-client/Cargo.toml:83`) enables
  `offscreen` and feature unification switches it on everywhere; any
  consumer built alone without that dev-edge (vordar-benches, or
  engine-renderer's own lib target) sees dead code.
- **Ideal:** items that exist only for the offscreen harness compile only
  when the harness does; clippy is green for every crate scoping, so
  per-crate gates work.
- **Gap:** the per-crate gate a worker would naturally run on the bench
  crate has been red since at least 07-17, and the workspace green is an
  artifact of test-dependency feature leakage, not of clean gating.
- **Suggestion:** `#[cfg(feature = "offscreen")]` on `fit_bounds`,
  `look_at`, `write_viewport`, `WhiteAo`, and `WhiteAo::new`. The `ao`
  field is written unconditionally by `SsaoTargets`' constructor, so gate
  it with `#[cfg_attr(not(feature = "offscreen"), expect(dead_code))]`
  plus a one-line constraint comment instead of restructuring the
  constructor.
- **Outcome:** `7/10` — unblocks per-crate clippy as a usable gate and
  removes the last standing red from the 07-17 campaign.
- **Confidence:** `9/10` — the failing command was run today and every
  consumer site was traced to the gated module; only the exact attribute
  spelling is untested.
- **Cost:** `2/10` — six attribute sites in two files.
- **Path:** (1) add the cfg gates; (2)
  `cargo clippy -p vordar-benches --all-targets -- -D warnings` exits 0;
  (3) `cargo clippy --workspace --all-targets -- -D warnings` still exits 0
  (offscreen path still compiles via vordar-client's dev-edge); proof:
  both commands green.

### 3. `image` and `serde_json` drifted back out of `[workspace.dependencies]`

- **Evidence:** the root manifest's rule "Shared versions — all crates pull
  from here" (`Cargo.toml:28`). `image = "0.25"` is declared independently
  in `smirk/engine-renderer/Cargo.toml:44` (features hdr/png/jpeg) and
  `client/vordar-client/Cargo.toml:76` (feature png); `serde_json = "1"`
  independently in `smirk/engine-renderer/Cargo.toml:41` and
  `game/vordar-game/Cargo.toml:27` (dev-dep). Same drift class the 07-17
  finding 5 fixed for smallvec/wgpu/egui-* — these entries postdate that
  fix.
- **Ideal:** every dep used by ≥2 crates has exactly one version
  declaration; per-crate feature additions ride on
  `{ workspace = true, features = [...] }`.
- **Gap:** two shared deps where a future bump is a multi-manifest hunt the
  root comment promises away.
- **Suggestion:** hoist both to `[workspace.dependencies]`
  (`image = { version = "0.25", default-features = false }`;
  `serde_json = "1"`), and switch the three consuming manifests to
  `workspace = true` with their crate-specific `features` lists.
- **Outcome:** `6/10` — manifest truthfulness; resolved versions unchanged.
- **Confidence:** `8/10` — pure manifest read; cargo's additive
  workspace-dep feature semantics are documented behavior.
- **Cost:** `1/10` — four manifests, no code.
- **Path:** (1) hoist + rewire; (2)
  `cargo check --workspace --all-targets`; proof: `Cargo.lock` unchanged.

### 4. The lockfile is 137 packages behind latest-compatible, including patch fixes for the live stack

- **Evidence:** `cargo update --dry-run --verbose` (2026-08-07) lists 137
  pending compatible updates, among them wgpu/naga 29.0.0 → 29.0.4 (four
  patch releases on the renderer's own backend), quinn 0.11.9 → 0.11.11,
  rustls 0.23.40 → 0.23.43, tokio 1.52.3 → 1.53.1, hecs 0.11.0 → 0.11.1,
  plus nine `windows*-0.42` crates that drop out entirely. Last
  Rust-touching commits are 2026-08-05; the lock has not been refreshed
  across the 07-18 → 08-05 stretch.
- **Ideal:** the lock tracks latest-compatible as routine hygiene — bugfix
  patches on wgpu/naga/quinn/rustls arrive without ceremony, verified by
  the standing gate.
- **Gap:** the tree runs on .0 releases whose .1–.4 successors are
  bugfix-only and free under semver.
- **Suggestion:** `cargo update`, then the full gate plus one bench smoke
  (`cargo bench -p vordar-benches -- --quick`) since criterion timings can
  shift with dep codegen.
- **Outcome:** `6/10` — bugfixes and a smaller tree for zero API cost.
- **Confidence:** `7/10` — the pending list is cargo's own output; the
  claim that nothing breaks rests on semver discipline, which the gate run
  checks directly.
- **Cost:** `2/10` — one command plus a gate run.
- **Path:** (1) `cargo update`; (2) full gate + bench smoke; proof: gate
  green, `Cargo.lock` at latest-compatible.

### 5. Six dependencies sit a major behind with no pin comment holding them

- **Evidence:** from the same dry-run's `(available:)` column, all
  uncommented in their manifests: `ddsfile 0.5.2 → 0.6.0`
  (`smirk/engine-renderer/Cargo.toml:33`) — 0.6's manifest (registry cache,
  read 2026-08-07) moves to enum-primitive-derive 0.3, which retires the
  workspace's only syn 1.0.109 chain (`cargo tree -d`); `pollster 0.4.0 →
  1.0.1` (`smirk/engine-renderer/Cargo.toml:29`); `getrandom 0.3.4 → 0.4.3`
  (`Cargo.toml:64`, sole call site
  `client/vordar-client/src/credentials.rs:46`) — the tree carries three
  getrandom majors (0.2 via ring, 0.3 ours, 0.4 via quinn's rand) and this
  bump collapses ours into quinn's; `rcgen 0.13.2 → 0.14.8`
  (`Cargo.toml:45`); `sha2 0.10.9 → 0.11.0` (`Cargo.toml:56`); `glam 0.32.1
  → 0.33.3` (`Cargo.toml:29`). The 07-17 audit's expired-pin lesson
  (rusqlite) argues for not letting uncommented majors age.
- **Ideal:** every dep is on its current major, or pinned with a comment
  stating a reason that is still true.
- **Gap:** six silent majors, two of which (ddsfile, getrandom) actively
  pay duplicate-tree cost today.
- **Suggestion:** bump in one pass, smallest risk first: ddsfile, pollster,
  getrandom (mechanical); rcgen (cert-mint API in engine-net may shift);
  sha2 (digest-0.11 trait changes at the server hashing sites); glam last
  and workspace-wide (serde feature must survive; renderer golden tests are
  the behavior check). Any bump that turns out non-trivial gets its own
  pin comment instead — stating why it waits.
- **Outcome:** `6/10` — current majors, syn-1 chain gone, getrandom set
  shrunk.
- **Confidence:** `6/10` — versions and the ddsfile dep-drop are verified
  from cargo and the registry manifest; the API-migration sizes for
  rcgen/sha2/glam are unverified until compiled.
- **Cost:** `4/10` — mostly mechanical, but glam touches every crate and
  sha2 touches auth-adjacent code.
- **Path:** (1) ddsfile+pollster+getrandom, gate; (2) rcgen, engine-net
  tests; (3) sha2, server persistence/auth tests; (4) glam, full gate
  incl. renderer golden tests; proof: gate green, `cargo tree -d` shows no
  syn 1.x and only two getrandom majors.

### 6. The egui/wgpu family is a coordinated generation behind (egui 0.34 → 0.36, wgpu 29 → 30)

- **Evidence:** dry-run availability column: egui/egui-wgpu/egui-winit
  0.34.x with 0.36.0 available, wgpu 29.0.x with 30.0.0 available — the
  four are one version-locked family (`Cargo.toml:35-38`), plus
  `egui_kittest = "0.34"` (`client/vordar-client/Cargo.toml:80`) which must
  move in lockstep. The 07-17 audit moved this family into
  `[workspace.dependencies]` precisely so the bump is a one-place edit.
- **Ideal:** the renderer's two core surface APIs track current, so wgpu
  fixes/features and egui fixes arrive while each migration is one
  generation instead of a compound jump later.
- **Gap:** one full generation of accumulated migration debt on the
  workspace's largest dependency family.
- **Suggestion:** bump the family together after finding 5 settles.
  Step 1 is a fact-check, not code: confirm from egui-wgpu 0.36's
  metadata which wgpu major it binds (if it still binds 29, park the wgpu
  half and bump egui alone).
- **Outcome:** `6/10` — currency on the heaviest family; no feature need
  drives it, which caps the score.
- **Confidence:** `5/10` — availability is verified; the egui-0.36/wgpu-30
  pairing and the migration surface in the renderer are unverified until
  step 1 runs.
- **Cost:** `6/10` — wgpu majors historically ripple through
  surface/limits/naga touchpoints across the renderer.
- **Path:** (1) verify the pairing from the registry metadata; (2) bump
  the five entries, fix compile fallout; (3) full gate incl. renderer
  golden tests and one offscreen render; proof: gate green on the new
  family.

### 7. BASELINE.md's baseline predates three weeks of perf-relevant commits — the mixed-vintage problem is recurring a third time

- **Evidence:** machine block reads rustc 1.97.1, Date 2026-07-18
  (`.claude/docs/benchmarks/BASELINE.md:88`). Rust-moving commits since:
  12c7e4b (2026-08-04, alpha-mask sampling added to depth prepass, shadow,
  and SSAO passes), f154d2e (2026-08-05, whole-frame GPU timing bracket on
  the render path), 8df21f6 (datagram counters on the snapshot path),
  3794018 (separate cast sequence lane in receive), e9ff97e (per-connection
  RTT tracking) — the render_cpu, snapshot, and client_netcode benches all
  cover touched paths. The file's own rule: "Update it after any change
  that moves a number" (`BASELINE.md:55`). The same staleness was fixed by
  the 07-04 weakpoints pass and again by the 07-17 audit's finding 12.
- **Ideal:** `--baseline main` comparisons measure the change under test,
  not three weeks of drift; the machine block names the tree the numbers
  came from.
- **Gap:** the saved baseline and the durable tables describe a 07-18 tree
  that five perf-relevant commits have since moved.
- **Suggestion:** after findings 4–6 settle (each moves codegen), re-run
  the full suite with `--save-baseline main` and refresh the tables plus
  machine block in one commit. The recurrence pattern says the re-save
  belongs at the end of every codegen-moving batch as routine, not as a
  rediscovered audit finding — the now-working gate log (finding 1) is
  where that routine leaves its trace.
- **Outcome:** `6/10` — trustworthy comparisons; same value it had the
  last two times.
- **Confidence:** `8/10` — dates and commit list are read off git and the
  file; whether any given bench number actually moved is exactly what the
  re-run measures.
- **Cost:** `3/10` — ~6 min bench run plus table refresh, on a quiet box.
- **Path:** (1) `cargo bench -p vordar-benches -- --save-baseline main`;
  (2) refresh tables + machine block; proof: BASELINE.md's date, rustc,
  and every row come from one tree.

## Carried forward from previous report

- **Finding 14 (reworks-rust-tooling-2026-07-17)** → finding 2 above.
  Re-verified red 2026-08-07 with an evolved error set (5 errors, was 4);
  root cause settled this pass (offscreen feature gating), converting it
  from an investigation into a bounded fix.

## Resolved since last report

- **Findings 1–12 (audit-rust-tooling-2026-07-17):** all done 2026-07-18;
  spot re-verified this pass — `[workspace.lints]` present with all 15
  members inheriting (`Cargo.toml:21-25`), every crate on edition 2024,
  `cargo clippy --workspace --all-targets -- -D warnings` exits 0, rusqlite
  0.40.1 / criterion 0.8 / notify 8.2 (optional, winit-gated) landed,
  slotmap/rand/gilrs/kira/parry3d absent from the tree, the profiling
  recipe is documented with a verified samply run
  (`.claude/docs/benchmarks/BASELINE.md:39-52`), and the baseline was
  re-saved 07-18.
- **Decision record preserved from finding 10:** dev-profile dependency
  opt-level was measured 2026-07-17 and REJECTED — `[profile.dev.package."*"]
  opt-level = 1` cost +42% clean-build wall for a 1.7% e2e improvement
  against a ≥10% bar; `[profile.dev]` stays `debug = 1` only. Do not
  refile without new numbers.
- **Finding 13 (reworks-rust-tooling-2026-07-17):** resolved —
  `cargo clippy -p vordar-client --all-targets -- -D warnings` exits 0 on
  rustc 1.97.1 (run 2026-08-07); the six `float_literal_f32_fallback`
  sites in action_bar.rs/minimap.rs no longer fire.
