# PRIME Agent learning-loop pilot — PHASE 1 COMPLETE; OPTION 2 G1 COMPLETE / G2 BLOCKED

## User direction

Pause the current texture A/B loop and evaluate Prime Intellect's **PRIME
Agent** as a possible way for the repeated asset/model-quality campaign to
retain learning across iterations. The user confirmed that product identity and
authorized **`v0.7.0` commit
`be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`** as the immutable phase-1 audit
baseline. This does **not** establish that commit as the 2026-08-05 launch
revision; that historical binding remains unresolved.

Pi and PRIME must coexist on this intermittently powered machine. Any later
eligible pilot must recover correctly after both orderly shutdown and abrupt
host loss, preserve and separate Pi/PRIME state, and expose the disposition of
in-flight work. Docker is not assumed to be installed, required, supported, or
the recovery mechanism.

This remains an architecture/setup fork, not permission to install or run
PRIME. PRIME must demonstrate persistent learning from trajectories, rewards,
and replay; merely changing agent harnesses does not improve asset quality.

On 2026-08-06, the user selected option 2: a separate gate-closing campaign for
the sandboxed PRIME sidecar path, with Pi remaining orchestrator/control. On
2026-08-07, the queued Sol planning finding landed at
[`prime-agent-option2-gate-closing-plan.md`](prime-agent-option2-gate-closing-plan.md).
G0 was rerun on 2026-08-07 after the campaign plan reconciled the observed
drift and ends `FRESH`. G1’s read-only host inventory is complete. G2 retains a
dedicated Hyper-V Ubuntu candidate but ends `BLOCKED` at Task 2. No guest was
downloaded, created, or started; no concurrent VFX/effects/particles work was
touched.

## Goal

Establish whether PRIME can run Vordar's long asset-quality loop with durable,
measurable improvement across episodes while preserving the existing licensing,
visual-judgment, provenance, and one-heavy-GPU-job gates.

Observable success requires all of:

1. An isolated episode uses a frozen real Vordar asset task and cannot write to
   shipping paths.
2. Inputs, tool calls, artifacts, metrics, judge outcomes, reward, and failure
   causes are persisted in a replayable trajectory.
3. A later matched episode demonstrably uses retained learning and improves the
   priced outcome rather than only its own proxy.
4. The comparison reports artifact quality, failure rate, wall/GPU time, token
   cost, licensing state, and operational complexity against Pi as the control.
5. Independent Sol visual judgment remains separate from frame production;
   metrics pre-screen but do not ship visuals.
6. Pi and PRIME coexist without state or resource collision and recover with
   observable outcomes after orderly shutdown and abrupt host loss.

## Phase-1 result and resume

Phase 1 is complete under the [audit
plan](prime-agent-feasibility-audit-plan.md), with findings retained in the
[P1–P10 directory](../docs/research/prime-agent/phase-1/). The final [P10
synthesis](../docs/research/prime-agent/phase-1/10-vordar-boundary-synthesis.md)
sets the phase-2 matched-pilot planning gate to **`INSUFFICIENT EVIDENCE`**.
Phase 2 is therefore not yet authorized or eligible. Option 2 has been selected
only as the direction for a separate gate-closing planning campaign; PRIME has
not been adopted and no setup is authorized.

Evidence-backed resume facts from P10:

- Source demonstrates durable supplemental-context refinement reaching a later
  prompt, but not weight learning, observed reward-to-update learning, or
  matched improvement.
- Complete trajectory/reward/replay evidence is not source-satisfied. Required
  identity, artifact/reward provenance, learned-artifact linkage, later-use
  receipt, deterministic replay/re-execution, and crash-safe disposition remain
  absent or unresolved.
- Reproducible source/runtime closure and execution/rights closure are blocked.
- Still-image input exists through a declared image-capable remote model, but
  the Vordar visual gate remains external: PRIME supplies no capture pipeline,
  visual reward, reviewed-frame binding, or independent-judge enforcement.
- Linux/macOS are official packaged targets; native Windows RLM is unsupported,
  WSL2 is unknown, and core Docker support is absent.
- Intermittent-host recovery and Pi/PRIME coexistence remain unmeasured and
  require a later executable red-proof covering orderly shutdown, abrupt host
  loss, persisted-byte integrity, in-flight disposition, idempotent
  resume/replay, restart ordering, state separation, and resource contention.
- No qualifying head-to-head against installed Pi `0.80.6` exists.

P10 records these independent options exactly:

| Option | Expected outcome | Confidence |
|---|---:|---:|
| Replace Pi as campaign harness | `4/10` | `2/10` |
| Sandboxed PRIME sidecar; Pi remains orchestrator/control | `7/10` | `3/10` |
| No adoption; continue Pi `0.80.6` | `5/10` | `6/10` |

Direct phase-1 findings:
[P1](../docs/research/prime-agent/phase-1/01-identity-source-lock.md) ·
[P2](../docs/research/prime-agent/phase-1/02-component-runtime-closure.md) ·
[P3](../docs/research/prime-agent/phase-1/03-license-weights-service-closure.md) ·
[P4](../docs/research/prime-agent/phase-1/04-learning-persistence-dataflow.md) ·
[P5](../docs/research/prime-agent/phase-1/05-observability-replay-failures.md) ·
[P6](../docs/research/prime-agent/phase-1/06-multimodal-visual-support.md) ·
[P7](../docs/research/prime-agent/phase-1/07-platform-gpu-vram.md) ·
[P8](../docs/research/prime-agent/phase-1/08-pricing-operations.md) ·
[P9](../docs/research/prime-agent/phase-1/09-comparative-practitioner-evidence.md) ·
[P10](../docs/research/prime-agent/phase-1/10-vordar-boundary-synthesis.md).

**Current PRIME checkpoint / exact next action:** G0 is `FRESH`; G1 is complete at
commit `52e2c56` with artifact
[`01-host-preflight/`](../docs/research/prime-agent/option-2-gate-closing/g2-closure/01-host-preflight/).
The original G2 closure queue remains `BLOCKED` at its original Task 2
(commit `48b063c`, existing bootstrap-object manifest), while the follow-on
blocker-closure queue is `BLOCKED` at Task 1, as recorded in the
[`G2 blocker-closure plan`](prime-agent-option2-g2-blocker-closure-plan.md),
plan commit `34260dc`. Task-1 public research is committed as `90728fd` at
`.claude/docs/research/prime-agent/option-2-gate-closing/g2-closure/02-bootstrap-object-manifest/blocker-closure/00-public-research/`
and ends `BLOCKED`. The aligned retained member is
`etc/apt/trusted.gpg.d/ubuntu-keyring-2012-cdimage.gpg`; the discarded draft
member was never persisted as selected. The exact public ledger is 8 candidate
bodies, 6 known sizes, 2 unknown sizes, 8,121,066 known bytes, UNKNOWN complete
bytes/storage, 0 eligible bodies, 16 direct dependency declarations, 26
patches, and 10 blockers. The first causal gap remains no Task-1-approved zstd
extraction/member byte-digest-packet closure; additional endpoint, Ubuntu
checksum digest, MSYS2 package/source/build binding, Git-for-Windows
provenance, dependency/license, and ceiling gaps remain. **Exact next action:
stop.** Blocker Tasks 2–8 and original Tasks 3–14 are parked; no blocker Task 2
host supplement, original Task 3, or G3 may occur. Any continuation requires a
new explicit user decision on a fresh Sol plan and does not imply host-probe
approval. No host probe, body acquisition, extraction, execution, credentials,
VM/WSL/Docker/GPU, fallback, or original Task 3 occurred; installation/download,
user-global changes, phase-2 matched-pilot planning, adoption, and VFX/effects/
particles remain unauthorized.

## Execution model

Finding before change, serial gates, exact-path commits, Pi retained as the
control until PRIME wins a matched pilot.

1. **COMPLETE — Sol analysis, product and feasibility audit.** Executed under
   the [phase-1 plan](prime-agent-feasibility-audit-plan.md); retained artifacts
   are in the [P1–P10 finding
   directory](../docs/research/prime-agent/phase-1/). P10's final gate is
   **`INSUFFICIENT EVIDENCE`**.
2. **BLOCKED / NOT AUTHORIZED — Sol planning, matched pilot protocol.** Phase-2
   planning is not eligible until P10's entry gates close. A later eligible
   protocol must freeze one real task, artifact inputs, reward channels, red
   proofs, independent visual gate, sandbox write boundary, Pi control arm,
   recovery/coexistence proof, success/failure thresholds, expected wall/GPU
   time, and rollback. It must prove learning across episodes rather than a
   one-off stronger model.
3. **COMPLETE — Sol planning finding for option 2.** The dependency-ordered
   campaign is recorded in
   [`prime-agent-option2-gate-closing-plan.md`](prime-agent-option2-gate-closing-plan.md)
   and committed as `065f29a`. Execution awaits review/approval; G1 additionally
   requires explicit host-probe approval.
4. **NOT AUTHORIZED — Bounded setup change.** Only after all prior gates and
   explicit approval: Luna performs exact mechanical acquisition; Terra or Sol
   hard-implement handles integration according to sensitivity; security/license
   and reproducibility gates run before access to project tools.
5. **NOT AUTHORIZED — Matched pilot and verdict.** Serialize heavy jobs, keep Pi
   as control, preserve every ruling-cited artifact, use a separate Sol visual
   judge, and adopt PRIME only on a measured quality win with no licensing or
   provenance regression.

## Do not touch or decide

- Do not replace or disable Pi before the matched verdict.
- Do not install/download PRIME, alter user-global configuration, provide
  credentials, change license verdicts, or run training/GPU jobs without a later
  explicit authorization and satisfied gates.
- Do not let PRIME train on or emit shipping assets until the sandbox,
  provenance, and license gates pass.
- Do not treat self-reported reward, a single successful episode, or faster wall
  time as evidence of retained learning.
- Exclude `reference/` unless the user explicitly asks to study it.

## Resume state from the interrupted texture loop

- Game commit `185af6b` cleanly fixes separate export/final provenance and
  installs the approved retablo candidate. Retablo source, installed bytes, and
  manifest SHA are `e3d331f1b4bc60f5b1c1ab2222c30ea7b5570fce677a9871521d2821dae8aecb`.
- Queue item 1 was recorded complete in ClaudeConfig commit `f20b192`.
- Texture A/B queue item 2 is **HELD for this Prime decision**.
- The attempted zero-GPU P1b closeout under
  `target/texgen-ab/p1b-closeout/` is invalid, not decision evidence. Its
  reproducer used ordinal canvas slots and swapped the second/third source
  views for all six cart/votive candidates, causing authentic mean calibration
  MAD 8.58–20.28/255 against a required ≤0.5/255. Its corruption proof only
  changed unused copied bytes and is also invalid.
- If the texture loop resumes under either harness, its exact next technical
  step is a bounded correction of that target-local reproducer: derive
  generated-image/view mapping from each generate record and blend key, verify
  producer and consumer hashes, require one-to-one mapping, red-proof by
  deliberately swapping the same pair through the real validator, and stop
  unless all six authentic means calibrate ≤0.5/255. No production edit is
  currently justified.
- Retablo apse placement remains behind texture queue item 2 by the user's
  recorded ordering.

## Known unrelated game-tree dirt to preserve

- `docs/observability/phoenix.md`
- `tools/pi-phoenix/package-lock.json`
- `tools/pi-phoenix/package.json`
- `tools/pi-phoenix/src/startup.ts`
- `tools/pi-phoenix/test/startup.test.ts`
