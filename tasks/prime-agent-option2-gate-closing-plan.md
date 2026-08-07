# PRIME Agent option 2 gate-closing campaign plan

**Status:** planning finding only; no gate execution, setup, acquisition, credentials, adoption, or matched-pilot planning is authorized by this document.

**Planning date:** 2026-08-07

**Authorized PRIME baseline:** `v0.7.0`, commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`. This remains distinct from the unresolved 2026-08-05 launch revision.

## Goal

Close or explicitly fail the platform, immutable-runtime, rights/service, Pi/PRIME isolation, and intermittent-host recovery gates for a sandboxed PRIME sidecar while Pi remains the sole orchestrator and control.

## Evidence baseline and freshness

This plan is grounded in:

- [PRIME learning-loop pilot](prime-agent-learning-pilot.md)
- [Phase-1 audit plan](prime-agent-feasibility-audit-plan.md)
- [P1 identity lock](../docs/research/prime-agent/phase-1/01-identity-source-lock.md)
- [P2 runtime closure](../docs/research/prime-agent/phase-1/02-component-runtime-closure.md)
- [P3 rights/service closure](../docs/research/prime-agent/phase-1/03-license-weights-service-closure.md)
- [P4 persistence dataflow](../docs/research/prime-agent/phase-1/04-learning-persistence-dataflow.md)
- [P5 observability/recovery](../docs/research/prime-agent/phase-1/05-observability-replay-failures.md)
- [P7 platform envelope](../docs/research/prime-agent/phase-1/07-platform-gpu-vram.md)
- [P8 operational costing](../docs/research/prime-agent/phase-1/08-pricing-operations.md)
- [P10 synthesis](../docs/research/prime-agent/phase-1/10-vordar-boundary-synthesis.md)

Freshness re-check on 2026-08-07:

1. Commit-SHA source citations remain content-pinned and do not drift, but the `v0.7.0` lightweight tag and GitHub release object are mutable. P1’s recorded commit and asset digests—not the current tag value—remain authoritative.
2. Mutable platform documentation, issues, service terms, privacy policies, pricing pages, package metadata, and release metadata were last retrieved on 2026-08-06. They must be refreshed before any dependent task is dispatched.
3. A newly published PRIME version must not silently replace the authorized baseline. Source drift produces a user checkpoint, not an automatic upgrade.
4. P2 and P3 remain `BLOCKED`; P5 remains not source-satisfied; P7 remains `INSUFFICIENT EVIDENCE`. No later repository artifact currently supersedes those findings.
5. WSL2 remains unknown, native Windows RLM remains unsupported at the authorized baseline, Linux is the only official packaged target, and core Docker support remains absent.
6. Pi `0.80.6` is the recorded control, but its current host process, state, and resource footprint were not probed in this planning task.

## Acceptance Criteria

- One dedicated Linux execution boundary is selected and qualified. It may be a dedicated WSL2 distribution only if measured compatibility passes; otherwise it must be a separately approved Linux guest with an external power-cut equivalent. Native Windows and bare-metal host process isolation do not satisfy this gate.
- Every enabled PRIME, Node, npm, Python, wheel, helper, isolation, and service dependency is recursively enumerated and bound to immutable bytes or an immutable service revision. Wildcards, mutable channels, `latest`, unresolved semver ranges, dynamic extension acquisition, and silent fallback are absent from the enabled path.
- The exact acquired object store can reconstruct the selected runtime with networking disabled, and an independent verifier goes red when any object, manifest edge, or installed byte is changed or omitted.
- Raw licenses, notices, provenance, model/weight terms, output rights, hosted-service terms, privacy/retention terms, territory restrictions, and account class close for every enabled node. Unknown or NC-bearing paths remain disabled and cannot influence a shipping path.
- No worker handles or records a credential value. A user-mediated, PRIME-only credential slot is separated from Pi state and environment; evidence records only slot identity, permissions, provider/account class, and redacted presence.
- PRIME has no access to the Vordar repository, shipping paths, Pi state, Pi credentials, shared temp/IPC, unrestricted host processes, unapproved network destinations, or a local GPU device.
- PRIME writes only within `/var/lib/vordar-prime-option2/`, `/srv/vordar-prime-option2/work/`, `/var/log/vordar-prime-option2/`, and `/run/vordar-prime-option2/` inside the selected guest. Its immutable runtime is rooted at `/opt/vordar-prime-option2/runtime/<manifest-sha256>/`.
- The recovery gate exercises orderly shutdown and abrupt loss of the complete PRIME guest, includes nonzero downtime and immediate retry, and verifies the exact bytes restart consumers read.
- Recovery evidence covers persisted-byte integrity, in-flight disposition, safe same-ID and new-ID retry, idempotent resume or explicit replay refusal, dependency restart order, Pi/PRIME state separation, orphan cleanup, network denial, and GPU/resource contention.
- Every request under test ends durably as `completed`, `failed`, `cancelled`, or `uncertain`; silence and silent-empty corruption recovery fail the gate.
- A deliberately broken runtime hash, isolation boundary, recovery link, restart order, idempotency result, state boundary, or GPU admission rule makes its independent verifier red before intact evidence may count.
- Pi remains orchestrator, control, recovery authority, judge dispatcher, shipping authority, and heavy-GPU admission owner throughout.
- No phase-2 matched-pilot plan, PRIME adoption, Pi replacement, Vordar task exposure, asset generation, visual verdict, or shipping-path output is produced.
- The final artifact maps the new evidence back to P10’s in-scope blockers. P10’s out-of-scope learning, complete trajectory/reward, visual, matched-comparison, and campaign-budget gates remain `NOT EVALUATED` and therefore keep the overall phase-2 planning result at `INSUFFICIENT EVIDENCE`.

## Execution model

### Finding before change

Every decision-bearing step is a Sol analysis finding. A change is dispatched only after its governing finding is reviewed against the artifact itself. No worker receives “investigate and fix.”

### Semantic seats

- **Sol analysis:** freshness, target selection, runtime closure, rights/terms, isolation design/verdict, recovery protocol/verdict, and P10 recheck.
- **Sol hard implement:** security-sensitive guest isolation and recovery fault-injection machinery.
- **Terra default implement:** independent verifiers and bounded offline runtime assembly.
- **Luna mechanical:** exact host inventory, approved downloads, deterministic commands, and raw matrix execution without judgment.

### Serial gate order

The exact order is:

1. Evidence freshness
2. Raw host inventory
3. Target and minimal execution-profile decision
4. User target/provisioning/acquisition approval
5. Dedicated guest provisioning
6. Immutable acquisition manifest
7. Quarantine acquisition and dependency resolution
8. Runtime-byte closure
9. Rights/service/credential-boundary closure
10. User terms/setup approval
11. Isolation design
12. Independent isolation verifier
13. Isolation implementation
14. Isolation execution and verdict
15. Offline runtime installation and platform qualification
16. Recovery protocol
17. Independent recovery verifier
18. Recovery harness
19. User credential/cost/disruptive-test approval
20. Recovery execution and verdict
21. P10 in-scope recheck

No task may be dispatched if an earlier gate could make it moot. Before each dispatch, re-open its named artifact dependencies and record drift.

### Approval checkpoints

1. **After target selection:** user approval is required for the exact WSL2/Linux guest mechanism, any user-global guest registration, the download/storage estimate, and public-byte acquisition.
2. **After rights closure:** user approval is required before installing or running PRIME, applying privileged isolation configuration, or selecting a hosted account/model path.
3. **Before recovery execution:** user approval is required for user-mediated credential injection, paid provider calls, guest termination, and the final displayed call/token/dollar ceiling.

No GPU job is planned. If any implementation requests a GPU workload rather than proving GPU absence/admission denial, stop and obtain a new explicit approval.

### Artifact ownership and commits

- Planning, findings, compact raw evidence, verifiers, and harness source live only under `.claude/docs/research/prime-agent/option-2-gate-closing/`.
- Downloaded/runtime bytes and bulky transient evidence live only under `target/prime-agent-option2/`; they are never shipping inputs.
- Review and commit `.claude/` separately from the game tree using exact pathspecs.
- Do not sweep-add either repository.
- Preserve every verdict-cited raw artifact or record its content digest and retained external location.

## Campaign stop conditions

Stop immediately and write the owning task’s blocked result if any of the following occurs:

- The authorized commit or recorded release-asset digest no longer matches the acquired object.
- A newer release appears and would require changing the authorized baseline.
- No dedicated Linux guest can provide an external abrupt-loss boundary without mounting Vordar or exposing Pi state.
- WSL2 qualification fails or requires a PRIME source patch; do not improvise a compatibility shim.
- Any required runtime dependency remains ranged, dynamically acquired, unsigned where signature evidence was promised, or missing from the object store.
- Offline reconstruction accesses the network or produces different installed bytes.
- Pi fork provenance, package rights, selected model/weight/output rights, hosted-service terms, or required attribution remains blocked or unknown.
- Optional unknown services, updates, traces, MCP, package installation, local models, Prime-hosted products, or extension paths cannot be disabled by construction.
- Isolation cannot deny host/Vordar/Pi paths, shared credentials, unrestricted egress, or GPU visibility.
- A red fixture remains green, or an intact fixture remains red.
- Any orderly or abrupt case ends silently, loses suspect bytes, overwrites corrupt state, duplicates a semantic effect without detection, or cannot produce a safe retry decision.
- Restart correctness depends on Docker, a hidden database/service, or an unrecorded manual step.
- The guest cannot be terminated independently of Pi for the abrupt-host-loss equivalent.
- The resource or paid-call ceiling cannot be fixed before execution.
- Work would expose a real Vordar task, plan a matched pilot, alter license verdicts, or replace Pi.

A stopped campaign does not fall through to another platform, provider, runtime revision, sandbox, or service. That requires a new finding and user approval.

## Plan

### 1. G0 — Refresh the evidence and baseline ledger

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md`; table fields: claim, prior source, prior retrieval date, current source, current retrieval date, immutable revision/content hash, drift, controlling task, and impact.
- **Scope:** Re-open relevant P1–P5, P7, P8, and P10 primary citations; refresh release metadata, platform docs/issues, legal/service/privacy text, package metadata, and pricing used only for approval ceilings.
- **Boundary:** No download of PRIME bytes, account access, terms acceptance, host probe, baseline change, or feasibility redesign.
- **Red-proof/artifact check:** Review fails if any mutable source lacks both prior/current retrieval dates and a preserved current content identity, or if a changed source is silently treated as unchanged. The report must end `FRESH`, `DRIFT REQUIRES REPLAN`, or `SOURCE UNAVAILABLE`.
- **Dependencies:** Phase-1 artifacts and the authorized baseline.
- **Exit gate:** `FRESH`; otherwise stop before host work.
- **Estimate/resources:** 2–4 person-hours; web reads only; 0 GPU; 0 credentials.
- **Approval need:** None for public read-only research.

### 2. G1 — Capture a judgment-free host and guest-capability inventory

- **Type:** finding.
- **Semantic seat:** Luna mechanical.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/01-host-platform-inventory/` containing `raw.json`, `commands.json`, `stderr.log`, and `sha256.txt`. No environment or credential values may be captured.
- **Scope:** Record Windows build, CPU architecture/cores, RAM, free disk, WSL feature/version, installed distributions, available virtualization, filesystem locations, current mount/interop defaults, cgroup/systemd capability where already present, GPU device exposure, and installed Pi version/process/state-path names.
- **Boundary:** Read-only probes only; no WSL/Docker/VM installation, distro start if it would mutate state, package changes, credentials, or PRIME access.
- **Red-proof/artifact check:** A schema check must reject a fixture missing OS build, WSL state, external guest-termination capability, free disk, Pi identity, or GPU-exposure fields. Actual output fails if a probe is represented only by exit code without its value and source.
- **Dependencies:** G0 `FRESH`.
- **Exit gate:** Complete raw inventory or explicit `UNKNOWN` per field; no recommendation.
- **Estimate/resources:** 0.5–1 person-hour; seconds-scale CPU probes; less than 10 MiB output; 0 GPU.
- **Approval need:** Explicit user approval before dispatch because host probing was excluded from this planning task.

### 3. G2 — Select the target and minimal enabled execution profile

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/02-target-and-profile-decision.md`.
- **Scope:** Compare only a dedicated WSL2 distribution and a dedicated Linux guest. Select one external guest-termination mechanism, immutable OS image identity strategy, filesystem layout, process supervisor, resource-control mechanism, egress-control mechanism, secret-slot mechanism, and minimal PRIME profile. The profile must enumerate every enabled/disabled P2 node and one candidate provider/account/model class.
- **Boundary:** No provisioning, host change, credentials, provider call, Docker assumption, bare-metal process sandbox, phase-2 task selection, or newer PRIME baseline.
- **Red-proof/artifact check:** Fail if Windows/WSL/Linux are merged; if the selected target lacks an external abrupt-loss boundary; if any P2 optional edge is omitted; or if “disabled” lacks an enforceable mechanism and later verification. The artifact ends `TARGET SELECTED` or `BLOCKED`.
- **Dependencies:** G0 and G1.
- **Exit gate:** One target and one minimal profile selected, with no fallback hidden in the result.
- **Estimate/resources:** 4–8 person-hours; no execution; 0 GPU.
- **Approval need:** User must approve the selected target, guest registration/global impact, profile, and preliminary resource envelope before G3.

### 4. G3 — Provision only the dedicated Linux guest boundary

- **Type:** change.
- **Semantic seat:** Luna mechanical under the exact G2 recipe.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/03-platform-provision-receipt/` containing image/source hashes, command transcript, guest identity, mount/interop state, package baseline, termination command, and redacted host-impact inventory.
- **Scope:** Create or register the approved WSL2/Linux guest; disable host/Vordar mounts and cross-OS process interop from first boot; establish the fixed `/opt`, `/var/lib`, `/srv`, `/var/log`, and `/run` roots.
- **Boundary:** Do not acquire or run PRIME, Docker, model providers, development tools beyond the approved bootstrap, credentials, Vordar bytes, or GPU jobs.
- **Red-proof/artifact check:** Before green, a deliberately permissive guest fixture with host automount or interop enabled must fail the receipt check. Green requires an externally invocable guest termination and proof that the Vordar path is absent inside the guest.
- **Dependencies:** G2 and the first user approval checkpoint.
- **Exit gate:** Guest exists with recorded immutable image identity, no PRIME bytes, no repository mount, and an external termination boundary.
- **Estimate/resources:** 1–3 person-hours plus guest acquisition time; network/disk equal the G2 displayed image size plus less than 2 GiB working headroom; 0 GPU.
- **Approval need:** Required for download, guest registration, disk allocation, and any user-global virtualization change.

### 5. G4 — Specify the immutable acquisition and resolution manifest

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/04-acquisition-manifest/` containing `manifest.json`, `enabled-graph.json`, `resolve-plan.md`, and `expected-sources.json`.
- **Scope:** Enumerate release tarballs, Node/npm, uv, Python, npm transitives, Python wheels/build backends, enabled helpers, isolation dependencies, provider schemas, and every acquisition tool. Define script-disabled resolution, object-store paths, expected hashes/signatures, and offline reconstruction.
- **Boundary:** Do not acquire bytes, resolve against mutable defaults, enable updates, include Docker, or leave a wildcard/dynamic edge.
- **Red-proof/artifact check:** An independent schema fixture containing one `latest`, unresolved range, missing digest, missing source, or undeclared subprocess must fail. The manifest must give an exact expected object count or state which resolution step will produce it.
- **Dependencies:** G2 and G3.
- **Exit gate:** Complete executable acquisition recipe with no hidden package scripts.
- **Estimate/resources:** 3–6 person-hours; metadata only; less than 100 MiB working data; 0 GPU.
- **Approval need:** None beyond the approved public-research boundary; acquisition still waits for G5 approval.

### 6. G5 — Acquire into quarantine and resolve with scripts disabled

- **Type:** change.
- **Semantic seat:** Luna mechanical.
- **Artifact:** `target/prime-agent-option2/object-store/` plus `.claude/docs/research/prime-agent/option-2-gate-closing/05-acquisition-receipt/` containing `objects.json`, `network-ledger.json`, `process-ledger.json`, `resolved-node-lock.json`, `resolved-python-lock.json`, and `sha256.txt`.
- **Scope:** Fetch only G4-listed objects; verify upstream digests/signatures; resolve npm and Python graphs without lifecycle scripts; retain every selected tarball/wheel and raw license/notice candidate.
- **Boundary:** No install, postinstall, PRIME execution, arbitrary shell from acquired packages, dynamic extension/tool fetch, credentials, provider calls, or Vordar access.
- **Red-proof/artifact check:** Alter one copied object and show the independent manifest check fail before restoring it. Process evidence must show no acquired package lifecycle script or PRIME entrypoint executed. Unexpected network destinations or objects fail immediately.
- **Dependencies:** G4 and explicit approval of the displayed total download/storage quantities.
- **Exit gate:** Every resolved node maps to one verified object; no unresolved ranges remain.
- **Estimate/resources:** 1–2 person-hours plus download; network bytes equal the G4-computed object sum; disk requires at least twice that sum for quarantine and reconstruction; 0 GPU.
- **Approval need:** Required after G4 reports exact byte totals and endpoints.

### 7. G6 — Issue the runtime-byte closure verdict

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/06-runtime-byte-closure.md`.
- **Scope:** Reconcile every P2 enabled node and edge to G5 objects; verify release assets against P1; reconstruct the candidate tree twice with networking denied; compare complete path, mode, size, and SHA-256 manifests.
- **Boundary:** No installation into the operational prefix, package script execution, rights conclusion, or missing-edge waiver.
- **Red-proof/artifact check:** Remove one transitive object, change one byte, alter one mode, and add one undeclared file in separate fixtures; each must fail independently. Two clean reconstructions must be byte-identical.
- **Dependencies:** G5.
- **Exit gate:** `CLOSED` only if every enabled runtime/dependency byte is immutable and offline-reconstructable; otherwise `BLOCKED`.
- **Estimate/resources:** 4–8 person-hours; two script-disabled reconstructions; disk up to three times G4’s object sum; 0 GPU.
- **Approval need:** No new approval within the previously approved byte ceiling.

### 8. G7 — Close rights, hosted-service terms, provenance, and credential boundaries

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/07-rights-service-credential-closure.md`.
- **Scope:** One row for every G6 object and enabled service edge. Inspect raw licenses/notices, pi fork provenance, redistribution/attribution/patent obligations, model/base-weight/output terms, commercial and territory restrictions, data-use/training, privacy/retention, service automation terms, account class, and credential lifecycle. Verify disabled optional edges cannot reactivate.
- **Boundary:** No legal advice, license-verdict change, `content/source/CREDITS.md` edit, account creation, terms acceptance, credential handling, or service call.
- **Red-proof/artifact check:** A matrix fixture missing any G6 node, raw legal object, effective/retrieval date, output/data-use field, or disabled-edge proof must fail. `Compatible` may not be emitted while a transitive node or pi provenance edge remains unknown.
- **Dependencies:** G0 freshness and G6 `CLOSED`.
- **Exit gate:** `CLOSED` for the exact non-shipping profile or `BLOCKED`. Unknown is blocking.
- **Estimate/resources:** 8–16 person-hours; public/legal-source review only; 0 GPU.
- **Approval need:** None for research. User acknowledgement and setup/service approval are required after a closed result.

### 9. G8 — Design the Pi/PRIME isolation and qualification specification

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/08-isolation-design.md`.
- **Scope:** Specify the selected platform’s filesystem, user, process tree, cgroup/job limits, temp, IPC, environment, secret slot, network allowlist, logging, state, backup, teardown, and GPU-denial boundaries. Define benign adversarial probes and exact expected outcomes.
- **Boundary:** No implementation, PRIME run, real credential, Vordar mount, Docker, or recovery verdict.
- **Red-proof/artifact check:** The design fails if any boundary lacks an attack probe, observable denial, retained evidence path, and rollback. Naming separate directories alone is insufficient.
- **Dependencies:** G2, G6 `CLOSED`, G7 `CLOSED`.
- **Exit gate:** Complete implementation contract with no open security mechanism.
- **Estimate/resources:** 4–8 person-hours; no execution; 0 GPU.
- **Approval need:** User approval required before applying privileged guest configuration.

### 10. G9 — Implement an independent isolation verifier first

- **Type:** change.
- **Semantic seat:** Terra default implement.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/isolation-verifier/` containing `verify.mjs`, schema, fixtures, tests, and `README.md`.
- **Scope:** Verify G8’s evidence without importing or invoking the isolation implementation. Read raw process, mount, path, environment-name, socket, egress, credential-slot, cgroup, and GPU-device evidence.
- **Boundary:** Do not implement the sandbox/policy, run PRIME, inspect credential values, or grade only exit codes.
- **Red-proof/artifact check:** Add failing fixtures first for host mount present, Pi path readable, shared temp, inherited `PI_*`, open denied egress, credential value leaked, escaped child process, GPU visible, and overlapping heavy job accepted. Expected RED is a named boundary failure for every fixture.
- **Dependencies:** G8.
- **Exit gate:** All broken fixtures red; one specification-only complete fixture green.
- **Estimate/resources:** 4–8 person-hours; seconds-scale tests; 0 GPU.
- **Approval need:** None.

### 11. G10 — Implement the selected isolation boundary

- **Type:** change.
- **Semantic seat:** Sol hard implement.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/isolation-harness/` containing reviewed guest policy/config templates, apply/rollback scripts, probe producer, and tests.
- **Scope:** Implement only G8’s selected mechanism and fixed guest paths. Deny host mounts, Pi paths/state, unapproved environment, shared temp/IPC, unapproved egress, escaped descendants, and GPU devices. Add resource ceilings and a PRIME-only ephemeral secret slot.
- **Boundary:** Do not install/run PRIME, add alternate sandbox mechanisms, create credentials, mount Vordar, enable local models, or alter host Pi configuration.
- **Red-proof/artifact check:** Run G9 against the intentionally permissive pre-policy guest and observe RED; apply the minimal policy; rerun benign probes to green. G10 code may not be imported by G9.
- **Dependencies:** G9 and the post-G7 user setup approval.
- **Exit gate:** Policy and rollback are reviewable and satisfy G9 on benign probes.
- **Estimate/resources:** 8–16 person-hours; privileged guest changes; less than 1 GiB additional disk; 0 GPU.
- **Approval need:** Required for privileged guest configuration.

### 12. G11 — Execute isolation qualification and retain raw evidence

- **Type:** change.
- **Semantic seat:** Luna mechanical.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/09-isolation-evidence/<run-id>/` containing `index.json`, raw probe outputs, process/mount/network/GPU ledgers, pre/post Pi state tree hashes, and verifier output.
- **Scope:** Run G10’s benign adversarial probes while a temporary Pi control process remains independently active on the host. Verify actual Pi state bytes are unchanged without exporting their contents.
- **Boundary:** No PRIME installation, real credential, provider call, Vordar exposure, GPU workload, or policy repair.
- **Red-proof/artifact check:** Re-run at least one denied path, egress, process escape, state collision, and GPU-visibility mutation and confirm G9 reports RED. The intact run must be green.
- **Dependencies:** G10.
- **Exit gate:** Complete raw evidence; no judgment.
- **Estimate/resources:** 1–2 person-hours; seconds-scale probes; 0 paid calls; 0 GPU.
- **Approval need:** Covered by the privileged-isolation approval.

### 13. G12 — Issue the isolation verdict

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/10-isolation-verdict.md`.
- **Scope:** Review G11 against G8 and P2/P7/P10. Confirm filesystem, process, network, credential, GPU, state, temp, IPC, and rollback boundaries independently.
- **Boundary:** No repair, runtime install, or “architecturally separated” inference without measured evidence.
- **Red-proof/artifact check:** Fail if any claimed denial lacks both a deliberately broken red result and intact green evidence, or if Pi pre/post hashes differ.
- **Dependencies:** G11.
- **Exit gate:** `CLOSED` or `BLOCKED`.
- **Estimate/resources:** 2–4 person-hours; no execution; 0 GPU.
- **Approval need:** None.

### 14. G13 — Install the locked runtime offline and run platform smoke checks

- **Type:** change.
- **Semantic seat:** Terra default implement.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/11-runtime-platform-evidence/<run-id>/` containing install transcript, network-denial proof, installed-tree manifest, process tree, `doctor` output, daemon lifecycle output, kernel/RLM smoke output, and rollback receipt.
- **Scope:** Reconstruct and install G6 bytes into `/opt/vordar-prime-option2/runtime/<manifest-sha256>/` with networking denied; run only version, doctor, daemon start/status/shutdown, shell denial, and kernel/RLM lifecycle smoke checks using neutral fixture data.
- **Boundary:** No provider credential/call, Vordar input, refine claim, dynamic acquisition, update, MCP, trace upload, local model, Docker, GPU, or source patch.
- **Red-proof/artifact check:** First change one staged object and show install verification RED. Green requires the installed tree to match G6 and all unexpected network attempts to fail visibly. A WSL/path/kernel failure blocks; it is not shimmed.
- **Dependencies:** G6, G7, and G12 all `CLOSED`.
- **Exit gate:** Complete raw runtime/platform evidence.
- **Estimate/resources:** 2–4 person-hours; offline install; disk equal G4’s installed-size calculation plus one rollback copy; 0 GPU.
- **Approval need:** Explicit user approval required because this is the first PRIME installation and execution.

### 15. G14 — Issue the runtime and platform qualification verdict

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/12-runtime-platform-verdict.md`.
- **Scope:** Confirm exact installed bytes, offline reconstruction, selected Linux/WSL behavior, shell/kernel/process operation, disabled dynamic edges, and rollback.
- **Boundary:** No compatibility patch, target switch, provider call, recovery conclusion, or pilot eligibility.
- **Red-proof/artifact check:** Fail if the installed tree differs from G6, any acquisition occurs at first use, WSL2 behavior is inferred rather than observed, or a smoke check relies only on exit status.
- **Dependencies:** G13.
- **Exit gate:** `CLOSED` or `BLOCKED`.
- **Estimate/resources:** 2–4 person-hours; no new execution; 0 GPU.
- **Approval need:** None.

### 16. G15 — Define the executable recovery protocol and matrix

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/13-recovery-protocol.md`.
- **Scope:** Define exact operation IDs, durable dispositions, same-byte consumers, kill triggers, downtime, restart sequence, retry rules, remote reconciliation, and expected outcomes for:
  1. orderly shutdown;
  2. abrupt client death;
  3. worker death during provider request;
  4. complete guest termination during provider request;
  5. guest termination after tool effect but before transcript result;
  6. termination during session append;
  7. termination during checkpoint publication;
  8. termination before harness rename;
  9. termination after harness rename but before global history;
  10. termination after global history but before session history;
  11. broken dependency restart order;
  12. same-ID immediate retry;
  13. new-ID immediate retry;
  14. duplicate concurrent command;
  15. torn transcript;
  16. corrupt harness;
  17. corrupt checkpoint;
  18. attempted Pi/PRIME state collision;
  19. orphan descendant;
  20. denied egress/service outage;
  21. attempted GPU/heavy-owner overlap.
- **Boundary:** No execution, Vordar task, deterministic replay claim, matched pilot, visual work, or adoption threshold.
- **Red-proof/artifact check:** Every case must identify producer, exact bytes, restart consumer, independent check, expected terminal disposition, retry decision, and a mutation that must make the verifier red.
- **Dependencies:** G7, G12, and G14 `CLOSED`.
- **Exit gate:** Complete bounded matrix with exact run count, call/token ceiling, wall estimate, and rollback.
- **Estimate/resources:** 4–8 person-hours; no execution; 0 GPU.
- **Approval need:** None until execution.

### 17. G16 — Implement the independent recovery verifier first

- **Type:** change.
- **Semantic seat:** Terra default implement.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/recovery-verifier/` containing `verify.mjs`, schemas, mutation fixtures, tests, and `README.md`.
- **Scope:** Independently verify operation identity, exact surviving bytes, disposition, process tree, restart sequence, state separation, provider/tool reconciliation, retry outcome, and resource admission. It must not import recovery-harness code.
- **Boundary:** Do not implement fault injection, run PRIME, use credentials, or equate logs/exit codes with recovery.
- **Red-proof/artifact check:** Add failing fixtures first for missing disposition, altered consumed byte, missing provider reconciliation, duplicate effect, unsafe retry, wrong restart order, corrupt-state silent success, mixed Pi state, orphan child, open egress, and accepted GPU overlap. Each fixture must fail for its named reason.
- **Dependencies:** G15.
- **Exit gate:** All broken fixtures red and one complete synthetic schema fixture green.
- **Estimate/resources:** 4–8 person-hours; seconds-scale tests; 0 GPU.
- **Approval need:** None.

### 18. G17 — Implement the external recovery and fault-injection harness

- **Type:** change.
- **Semantic seat:** Sol hard implement.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/recovery-harness/` containing producer code, guest-termination controller, operation journal, byte hasher/parser, provider/tool barriers, process/resource sampler, runbook, and tests.
- **Scope:** Implement G15 without modifying PRIME bytes. The harness must run outside PRIME’s trust boundary, preserve suspect bytes, control neutral provider/tool fixtures, invoke the external guest termination, and emit evidence consumed by G16.
- **Boundary:** No PRIME source patch, Vordar data, self-judging verifier, automatic retry of `uncertain` work, credential capture, or GPU workload.
- **Red-proof/artifact check:** Run G16 against intentionally incomplete harness outputs and observe RED before implementing the corresponding producer fields. Producer and verifier share no modules.
- **Dependencies:** G16.
- **Exit gate:** Dry runs with neutral local fixtures produce G16-green evidence, while every retained broken fixture remains red.
- **Estimate/resources:** 8–16 person-hours; local/guest CPU only; less than 5 GiB temporary evidence; 0 GPU.
- **Approval need:** None for local fixtures; real service and termination execution waits for the final checkpoint.

### 19. G18 — Execute the orderly and abrupt recovery matrix

- **Type:** change.
- **Semantic seat:** Luna mechanical.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/14-recovery-evidence/<run-id>/` containing one immutable case directory per G15 case, `index.json`, exact byte manifests, process/resource samples, provider/tool receipts, Pi pre/post state hashes, verifier output, and rollback receipt.
- **Scope:** Execute all 21 cases serially. Use neutral non-Vordar inputs. Start and verify Pi control independently, then isolation supervisor/egress boundary, PRIME supervisor, catalog/worker, session/global-local harness, kernel/forkserver, and selected provider. Terminate the complete guest for host-loss cases, wait nonzero downtime, then restart in the prescribed order.
- **Boundary:** No judgment, repair, extra case, unapproved paid call, credential logging, Vordar bytes, local model, render, training, or GPU job.
- **Red-proof/artifact check:** Execute the registered broken mutations and require G16 RED. Green requires every intact case to report exact surviving bytes and one of `completed`, `failed`, `cancelled`, or `uncertain`; `uncertain` must refuse unsafe replay until reconciliation.
- **Dependencies:** G17 plus final user approval and user-mediated secret injection.
- **Exit gate:** Complete raw matrix or immediate blocked stop at the first unsafe result.
- **Estimate/resources:** 4–8 wall-hours; no heavy GPU; at most 12 real provider calls, 0.5M input tokens, and 0.1M output tokens including retries. The approval packet must replace these maxima with the selected provider’s exact dollar ceiling and include a 100% duplicate-charge reserve.
- **Approval need:** Required for credential injection, paid calls, guest termination, and the displayed wall/token/dollar ceiling.

### 20. G19 — Issue the recovery, coexistence, and contention verdict

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/15-recovery-verdict.md`.
- **Scope:** Review every G18 case against P2, P4, P5, P7, P10, and G15. Judge persisted-byte integrity, in-flight disposition, resume/retry safety, restart order, state separation, orphan handling, resource ceilings, network behavior, and GPU denial/admission.
- **Boundary:** No repair, rerun beyond one separately approved bounded falsifier check, matched-pilot design, or adoption conclusion.
- **Red-proof/artifact check:** Fail if any case is absent, a broken mutation stays green, a consumer reads different bytes from those hashed, a request ends silently, Pi bytes change, restart order is inferred, or GPU overlap is merely observed instead of rejected.
- **Dependencies:** G18.
- **Exit gate:** `CLOSED` only if all required cases pass; otherwise `BLOCKED` with the first causal failure and retained evidence.
- **Estimate/resources:** 4–8 person-hours; no new run; 0 GPU.
- **Approval need:** None.

### 21. G20 — Recheck P10’s in-scope gates and close the campaign

- **Type:** finding.
- **Semantic seat:** Sol analysis.
- **Artifact:** `.claude/docs/research/prime-agent/option-2-gate-closing/16-p10-in-scope-recheck.md`.
- **Scope:** Map:
  - P10 identity/runtime/platform gate to G0, G6, and G14;
  - P10 rights/service gate to G7;
  - P10 boundary/coexistence gate to G12;
  - P10 recovery gate to G19.
  Report each as `CLOSED`, `BLOCKED`, or `NOT EVALUATED`, with exact artifact and evidence links.
- **Boundary:** Do not edit P10, the pilot task, license verdicts, or phase-2 plans; do not claim learning, visual, matched-comparison, budget, pilot eligibility, or adoption.
- **Red-proof/artifact check:** A campaign-evidence checker must fail if a `CLOSED` row lacks a passing verdict, retained raw index, red proof, intact green proof, and exact dependency chain. Out-of-scope P10 rows must remain explicit.
- **Dependencies:** G19 and all prior verdicts.
- **Exit gate:** Campaign result is `IN-SCOPE GATES CLOSED` only if G6, G7, G12, G14, and G19 are all closed. Otherwise `GATE-CLOSING CAMPAIGN BLOCKED`. Overall P10 remains `INSUFFICIENT EVIDENCE` because out-of-scope gates are untouched.
- **Estimate/resources:** 2–4 person-hours; no execution; 0 GPU.
- **Approval need:** None.

## Files to Modify

No existing production, game, content, design, license-verdict, Pi installation, or phase-1 finding file is modified.

Generated target-only state may be created under:

- `target/prime-agent-option2/object-store/` — quarantined immutable objects
- `target/prime-agent-option2/work/` — transient reconstruction and execution outputs

Inside the approved Linux guest, bounded operational changes are limited to:

- `/opt/vordar-prime-option2/runtime/<manifest-sha256>/`
- `/var/lib/vordar-prime-option2/`
- `/srv/vordar-prime-option2/work/`
- `/var/log/vordar-prime-option2/`
- `/run/vordar-prime-option2/`
- `/run/credentials/vordar-prime-option2/`

## New Files

All committed campaign artifacts are new files under:

- `.claude/docs/research/prime-agent/option-2-gate-closing/` — findings, compact evidence, independent verifiers, and bounded test harnesses

The exact task-owned paths are listed in G0–G20. A worker may touch only its named artifact path and approved guest/target paths.

## Verification

After each task:

1. Read the exact artifact and its cited dependencies.
2. Run the task’s independent red fixture and confirm a nonzero result with the named failure.
3. Run the intact fixture or evidence index and confirm green.
4. Inspect exact-path diffs in the correct repository.
5. Account for every worktree-status line before staging.

Expected campaign verifier commands after their implementation:

```bash
node .claude/docs/research/prime-agent/option-2-gate-closing/isolation-verifier/verify.mjs \
  .claude/docs/research/prime-agent/option-2-gate-closing/09-isolation-evidence/<run-id>/index.json

node .claude/docs/research/prime-agent/option-2-gate-closing/recovery-verifier/verify.mjs \
  .claude/docs/research/prime-agent/option-2-gate-closing/14-recovery-evidence/<run-id>/index.json
```

Required red checks:

```bash
node .claude/docs/research/prime-agent/option-2-gate-closing/isolation-verifier/verify.mjs \
  .claude/docs/research/prime-agent/option-2-gate-closing/isolation-verifier/fixtures/permissive-policy/index.json

node .claude/docs/research/prime-agent/option-2-gate-closing/recovery-verifier/verify.mjs \
  .claude/docs/research/prime-agent/option-2-gate-closing/recovery-verifier/fixtures/duplicate-effect/index.json
```

Both red commands must fail for their named reason.

Repository review:

```bash
git -C .claude status --short
git -C .claude diff -- docs/research/prime-agent/option-2-gate-closing
git status --short -- target/prime-agent-option2
```

Stage and commit only exact completed artifact paths. Never use `git add -A`, directory-wide staging that can sweep unrelated work, or `git commit -a`.

## Risks and Open Questions

- P3’s pi-fork provenance and packaged/transitive rights gaps may be impossible to close from public evidence. That is a valid blocking outcome.
- WSL2 may run the Linux build but still fail filesystem durability, process isolation, egress control, external termination, or GPU denial. Passing a smoke check alone is insufficient.
- A dedicated Linux guest may require user-global virtualization changes, substantial disk, or a new licensed OS/runtime component.
- Immutable dependency closure may reveal platform-selected native packages or first-use downloads absent from source analysis.
- Selected provider/model terms may not expose immutable model revisions, request reconciliation, output rights, or idempotency needed by the recovery gate.
- PRIME’s arbitrary shell and inherited environment make same-user isolation inadequate; the dedicated guest boundary is mandatory.
- A provider request interrupted by guest loss may remain irreconcilably `uncertain`. If safe replay cannot be refused or reconciled, recovery remains blocked.
- P5 establishes that deterministic trajectory replay is absent. This campaign can prove safe session/command resume or explicit replay refusal; it must not rename that as deterministic replay.
- No actual local GPU work is planned. Coexistence closes only if the guest has no GPU exposure and overlapping heavy work is denied before launch.
- Estimates remain planning ranges until G4 and G15 replace them with exact bytes, calls, tokens, wall time, and provider rates.
- Even a fully green campaign does not establish retained learning, visual quality, complete trajectory/reward provenance, matched improvement over Pi, campaign budget, pilot eligibility, or adoption.
