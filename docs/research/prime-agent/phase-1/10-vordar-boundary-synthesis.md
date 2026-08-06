# PRIME Agent phase-1 Vordar boundary synthesis

**Finding date:** 2026-08-06

**Authorized PRIME baseline:** `v0.7.0`, commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`; this is not proven to be the 2026-08-05 launch revision. [P1][PLAN]

**Inspected revisions:** game tree `185af6b0cd1d879805a11abe14f5d779867a0674`; `.claude` tree `bfe70f5396f41a8e7138808bc5a5c9bcb4732374`. The game tree already had unrelated modifications and an untracked `=22.8.0`; `.claude` was clean before this artifact. No game-tree file was changed. [REV]

**Decision boundary:** this is a finding, not an adoption choice, setup authorization, pilot design, or claim of pilot eligibility. [LAW][PLAN]

## Evidence key and synthesis rule

- **P1–P9:** sibling phase-1 findings `01-identity-source-lock.md` through `09-comparative-practitioner-evidence.md`.
- **REV:** read-only `git rev-parse HEAD` and exact worktree-status inspection in the game tree and `.claude` repository on 2026-08-06.
- **PLAN / PILOT:** `.claude/tasks/prime-agent-feasibility-audit-plan.md` and `.claude/tasks/prime-agent-learning-pilot.md`.
- **LAW:** `.claude/CLAUDE.md`.
- **NC / VIS / RED / MET / INST / REAL / IMP / KEEP / NUM / QUAL:** applicable memory rulings `strict-nc-tooling-ruling.md`, `visual-verification.md`, `checks-must-fail-when-broken.md`, `a-number-is-not-the-thing.md`, `instrument-cannot-grade-itself.md`, `synthetic-cannot-validate-real.md`, `test-the-impolite-path.md`, `keep-verification-artifacts.md`, `numeric-outcome-weights.md`, and `quality-over-cost-ruling.md`.

Every capability statement below is limited to these sources. P1–P9 evidence gaps remain with their owning artifacts; no new product research is introduced. Outcome, confidence, and cost are independent weights. [NUM][PLAN]

## Phase-1 facts that control all three paths

1. The immutable audit baseline is known, but its historical launch binding is unresolved. Its exact packaged Node/Python/dynamic dependency closure is not reproducible from source alone. [P1][P2]
2. The committed source is MIT, but pi-derived provenance, release-package notice/content, installed npm/Python graphs, selected model/weight/output rights, and hosted-service terms do not close. Prime-hosted execution is blocked on current terms evidence. Unknown/NC-involved tools and their outputs cannot enter a shipping path. [P3][NC]
3. PRIME source demonstrates global supplemental prompt/memory/skill/subagent-metadata refinement reaching a later prompt. It does not demonstrate weight learning, observed reward-to-update, exactly-once refinement, causal later use, or matched improvement. [P4]
4. Transcript inspection/resume exists, but required episode identity, artifact hashes, external reward provenance, learned-artifact linkage, later-use receipt, deterministic replay/re-execution, and crash-safe terminal disposition do not. [P5]
5. PRIME can transport still-image bytes to a declared image-capable remote model. It supplies no renderer, capture pipeline, visual reward, reviewed-frame digest, or independent-judge enforcement. [P6]
6. Linux/macOS are documented packaged targets; native Windows packaged setup and managed RLM kernel are unsupported at this baseline; WSL2 is unknown. Core Docker units are `0`: no Dockerfile, image, Compose, container launcher, or Docker recovery path exists. [P2][P7]
7. Provider-hosted inference can leave the local heavy-GPU lane free, but Pi/PRIME CPU, RAM, disk, process, state, credential, port/temp, and practical GPU coexistence are unmeasured. PRIME has no quota or one-heavy-job lock. [P2][P7]
8. Total setup/run/ongoing cost is open. P8 supplies auditable units and formulas but not a quote; its campaign-total confidence is `2/10`. [P8]
9. No qualifying comparison against installed Pi `0.80.6` exists. Exact-release practitioner evidence is one narrow smoke check plus sparse failures; comparative-performance confidence is `2/10`. [P9]
10. The pilot requires a frozen real Vordar task, non-shipping writes, complete trajectory/reward/replay evidence, later matched improvement, a Pi control, independent Sol visual judgment, and metrics only as pre-screen. None of P1–P9 authorizes execution. [PILOT][REAL][VIS][MET]

## Shared hard boundary for any PRIME path

Until the entry gates below close, PRIME receives no credentials, service account, API call, install, download, host access, Vordar bytes, or write capability. A later sandbox must permit writes only to a retained non-shipping experiment root; game/production and shipping-asset paths remain read-only or absent. Every input/output/frame/trajectory/reward/refinement/checkpoint must have a retained content digest and provenance edge. Unknown or NC-bearing code, weights, datasets, services, or outputs remain outside shipping paths. [P3][P5][P6][PILOT][NC][KEEP]

Pi remains installed and is the control. Pi and PRIME must not share global/project state directories, IPC, temp/package roots, credentials, environment overrides, process supervision, or recovery authority. Intended PRIME paths (`~/.prime/agent`, project `.prime/agent`) are only naming separation, not security isolation; inherited `PI_*`, same-user permissions, temp, PATH, environment credentials, and unrestricted subprocesses remain collision paths. [P2][P7][PLAN]

Docker is not assumed. Core cost and restart order contain zero containers. If a later approved plan selects an optional remote Docker sandbox or a separately installed host container layer, that becomes a new digest, rights, state, credential, service, cost, and recovery dependency and must be closed before use. [P2][P3][P7][P8]

Expected outcomes prioritize quality rather than convenience or price; licensing remains a hard gate. Cost never increases or decreases an outcome score. [QUAL][NC][NUM]

## A — Replace Pi as campaign harness

- **Expected outcome: `4/10`.** On present evidence, disruption and control loss are more likely than a demonstrated quality gain; PRIME's narrow durable context mechanism is real, but reward-linked improvement is not. [P4][P5][P9][PILOT]
- **Confidence: `2/10`.** No matched comparison exists, exact-release experience is sparse, and rights, runtime closure, recovery, host fit, and total cost remain blocked or unknown. [P2][P3][P7][P8][P9]
- **Assumptions:** selected immutable package/dependency bytes and provider/model rights close; an official Linux or separately proven WSL2 target is available; exact non-shipping isolation exists; the learning/observability gaps can be externally instrumented without calling them native; Pi `0.80.6` remains available as frozen control until a verdict. Native Windows and Docker are not assumptions. [P2–P7][P9][PLAN]
- **Reversible boundary:** do not replace the installed Pi binary, state, credentials, orchestration law, or campaign records. The maximum reversible step is a later, separately approved switch of campaign dispatch after matched evidence, with old Pi task/state and exact bytes retained for immediate rollback. [LAW][P9][PILOT]
- **Data/execution boundary:** task reads and all writes stay in the approved non-shipping root; PRIME uses separate credentials and only the selected provider egress, while traces/MCP/dynamic services remain disabled unless separately closed. An external verifier binds trajectory/reward/replay, a separate Sol judge binds exact frame bytes, and external admission serializes every local heavy GPU job. [P2–P7][PILOT][VIS]
- **One-time cost:** P8 expected planning comparator is `32 person-hours × w`, plus known tarball floor `10,364,494 B`, unknown npm/Python/install GB, `Dinstall×pD`, network/egress, credential funding, OS/environment acquisition, and additional replacement migration/parity labor `hmigrate×w`. Elapsed setup wall time is unknown; person-hours are not silently treated as wall hours. This is not a quote. [P8]
- **Per matched run:** for P8's expected three-block comparator, `3 Pi-control/PRIME-pre/post blocks`, `300+15 model/judge calls`, `3.0M/0.60M agent input/output tokens + 0.60M/0.075M judge input/output tokens`, and 180 base GPU-min produce `$38.25` model/judge arithmetic + `$19.125` recovery reserve + `16w` operations/recovery + `4.5pL`, i.e. **`$57.375 + 16w + 4.5pL`**, excluding the one-time `32w` and all unknown storage/tool/account charges. End-to-end wall time is unknown and must be metered independently from GPU minutes. [P8]
- **Ongoing cost:** P8 expected comparator is **`$63.75 + 44w + 15pL + 75pD/month`** for four blocks, 500 calls, 720 base render minutes, 25 GB live state with three copies, and 25% replay reserve; migration maintenance and Pi control retention add unknown labor/storage. [P8]
- **Quality upside:** persistent global supplemental context and recursive work could preserve campaign lessons across sessions. **Quality downside:** no observed reward consumer, exact later-use receipt, independent visual gate, or demonstrated matched improvement; proxy gaming is a vendor anecdote, not a Vordar result. [P4][P6][P9]
- **Rights/service blockers:** P3's packaged/transitive, pi-provenance, Python, selected model/weight/output, dynamic acquisition, and Prime service-term blocks all apply. [P3]
- **Rollback:** stop new PRIME work, classify in-flight work, retain/hash suspect PRIME bytes, shut down PRIME, revoke separate credentials, restore Pi-only dispatch from retained Pi state, and exclude all unclosed PRIME outputs from shipping. Source does not prove this cross-harness rollback; it is a required later gate. [P2][P3][P5][P7]
- **Pi-control impact:** replacement before a matched verdict would violate the pilot's fixed control rule. Even after evidence, Pi must remain an independently executable comparison/rollback control; PRIME cannot own Pi state or recovery. [PILOT][PLAN]

## B — Sandboxed PRIME sidecar; Pi remains orchestrator/control

- **Expected outcome: `7/10`.** This path has the best bounded chance to test retained-learning upside while preserving current capability and an independent control, but it still cannot run on current evidence. [P4][P9][PILOT][LAW]
- **Confidence: `3/10`.** The architectural boundary is reversible and PRIME names separate state, yet actual sandboxing, rights, observability, coexistence, and recovery are unproven. [P2][P3][P5][P7]
- **Assumptions:** Pi `0.80.6` alone orchestrates/adjudicates; PRIME gets one frozen real task and writes only retained non-shipping bytes; credentials and egress are separate/allowlisted; unknown dynamic acquisition, MCP, traces, Prime platform services, local models, and NC tools are disabled by construction; an external verifier supplies missing identities without pretending PRIME natively does. [P3–P7][PILOT][NC]
- **Reversible boundary:** one separately owned experiment root, PRIME state root, process tree, account/credential set, and service allowlist. Delete/disable the sidecar and revoke its credentials without changing Pi, game files, design law, license verdicts, or shipping manifests. [P2][P3][LAW]
- **Data/execution boundary:** Pi grants only frozen task reads and non-shipping writes, holds provider/service allowlists and separate credentials, records external reward/replay identities, dispatches the independent Sol judge over exact retained frames, and owns the one-heavy-GPU admission decision. PRIME has no shipping, judgment, or control authority. [P2–P7][PILOT][VIS]
- **One-time cost:** use P8's expected `32w` setup assumption for acquisition, terms, Pi/PRIME isolation, OS choice, and verification, plus `10,364,494 B` known tarballs, unknown dependency/install GB, `Dinstall×pD`, network/account funding, and any sandbox boundary labor included only after its mechanism is selected. Elapsed setup wall time is unknown. Docker cost remains not applicable to core. [P8]
- **Per matched run:** the P8 expected matched envelope is the same auditable comparator as above: **`$57.375 + 16w + 4.5pL`** after separating the one-time `32w`; quantities are three blocks, 300+15 calls, displayed token units, 180 base GPU-min, and 50% replay exposure. End-to-end wall time is unknown and must be metered. Replace comparator rates with actual Pi/PRIME account rates before budgeting. [P8]
- **Ongoing cost:** **`$63.75 + 44w + 15pL + 75pD/month`** under P8's expected assumptions, plus any selected sandbox/service/egress/backup charges. Disabled optional services consume zero service units, not zero labor or host cost. [P8]
- **Quality upside:** permits a causal matched pre/post test of global refinement while Pi preserves task framing, provenance, control execution, and independent judgment. **Quality downside:** sidecar instrumentation may reveal no improvement; PRIME still lacks native reward linkage/replay and may add process/operational failure. [P4–P6][P9]
- **Rights/service blockers:** identical to A for every executed PRIME component; non-shipping status does not waive terms, credentials, sandbox, provenance, or user approval. No PRIME-influenced output may ship while any required edge remains unknown/NC. [P3][NC][PILOT]
- **Rollback:** stop admission, obtain explicit disposition, preserve hashes/records, orderly-shut or recover PRIME, revoke only sidecar credentials, remove its process/state roots after retention, and continue Pi from untouched control state. Abrupt rollback safety remains unknown until the later recovery gate passes. [P2][P5][P7]
- **Pi-control impact:** Pi retains orchestration, queue state, comparison arm, judge dispatch, shipping authority, GPU admission, and recovery authority. PRIME is never a co-orchestrator and cannot mutate Pi prompts, packages, credentials, tasks, or state. [LAW][PILOT][P2]

## C — No adoption; continue Pi `0.80.6`

- **Expected outcome: `5/10`.** This preserves current campaign progress and the installed control, but leaves the stated cross-episode learning opportunity untested and the held texture loop's existing technical defect to correct. [PILOT][P9]
- **Confidence: `6/10`.** Current Pi identity and resume state are known, but Pi's own durability/resources/provider cost were not audited here and no completed matched quality baseline exists. [P9][PILOT]
- **Assumptions:** installed Pi `0.80.6` remains usable; the held loop resumes only at PILOT's bounded reproducer correction; all current license, provenance, visual-judge, red-proof, and GPU gates remain unchanged. No claim is made that Pi is cost-free or superior. [PILOT][P9][NC][VIS]
- **Reversible boundary:** no PRIME bytes/accounts/state are introduced. A later audit can reopen the sidecar question from retained P1–P10 evidence without changing production now. [LAW][KEEP]
- **Data/execution boundary:** no PRIME credentials, service egress, state, trajectory, or writes exist. Pi retains its current provider boundary, shipping authority, independent Sol judge, provenance records, and one-heavy-GPU rule; P9 did not audit those Pi execution edges. [P9][PILOT][VIS]
- **One-time cost:** **not zero**: `Cresume = hresume×w + Dfix×pD`, for person-hours and retained `Dfix` GB-month needed to correct and independently red-proof the target-local producer/consumer mapping; quantities, rates, and elapsed wall time are unmeasured. PRIME acquisition units are `0`, not campaign labor/storage. [PILOT][P8][RED]
- **Per run:** `Cpi-run = Ipi×pi + Opi×po + Cpi×pc + Api×pa + tool fees + hpi×w + mrender×pL/60 + Drun×pD + Crecovery`. Pi account rates, tokens/calls, labor, render minutes, wall time, storage, and recovery reserve are unknown and must be metered; P8's direct-API Sol rates must not be imputed to Pi's unbound account. [P8][P9]
- **Ongoing cost:** `Cpi-month = ΣCpi-run + hops×w + hbackup×w + Dlive×copies×pD + Crecovery`; quantities are unknown, but continuing campaign, judge, retained artifacts, upgrades, and recovery are nonzero work. Opportunity cost is the unknown difference between this outcome and a genuinely learned improvement, not `$0`. [P8][P9][KEEP]
- **Quality upside:** avoids introducing unclosed rights, platform, state, and recovery paths; preserves the current control and exact next correction. **Quality downside:** no built-in Pi mechanism in P9 demonstrates PRIME-like global refinement, and no evidence answers whether the sidecar could improve later matched quality. [P3][P4][P9]
- **Rights/service blockers:** existing Vordar/Pi provider and transitive closure were not audited by P9; standing strict-NC/provenance law still applies. PRIME-specific blockers are avoided only because no PRIME execution occurs. [P3][P9][NC]
- **Rollback:** revert only the bounded target-local experimental correction if its independent red/green evidence fails; retain current approved asset/provenance state. [PILOT][RED][KEEP]
- **Pi-control impact:** Pi remains sole campaign harness/control at installed version `0.80.6`; local package bytes still lack cryptographic binding to the upstream commit recorded by P9. [P9]

## Pilot success-criterion and boundary map

| Required observable or boundary | Phase-1 disposition | Minimum evidence owner |
|---|---|---|
| Frozen real Vordar task; non-shipping writes | Required; no sandbox mechanism selected or proven. Synthetic evidence cannot substitute. | PILOT, P2, P3, REAL |
| Strict NC exclusion and end-to-end provenance | Required; execution chain and output rights are blocked/unknown. | P3, NC |
| Inputs, root/child tool calls, artifacts, metrics, judge outcomes, reward, failures persisted | Transcript subset exists; episode/artifact/reward/provenance/terminal schemas are absent or unresolved. | P4, P5 |
| Replay semantics | Inspection/resume exists; deterministic replay and re-execution are absent, cursor replay is transport-only. | P5 |
| Later matched episode demonstrably loads learning and improves priced outcome | Prompt-load edge exists; use receipt, observed reward, causal match, and improvement evidence are absent. | P4, P5, P9 |
| Independent Sol visual judge, separate from producer | Organizationally composable only; PRIME does not enforce role/process/credential independence. | P6, VIS |
| Exact frame bytes and required gameplay framing | Still bytes can travel, but no capture/manifest/digest/verdict binding; ship evidence must be destination-lit gameplay close-up plus player-scale frame. | P6, VIS, KEEP |
| Metrics pre-screen only | Mandatory; metrics require independent red-proof and cannot clear visuals. | VIS, MET, INST, RED |
| Quality, failure rate, wall/GPU time, tokens/dollars, rights, complexity versus Pi | No matched evidence; P8 formulas exist, actual quantities do not. | P8, P9 |
| Failure/recovery and every request outcome | Source leaves hard-death tails and external effects uncertain; silence is failure. | P2, P4, P5, IMP |
| Pi/PRIME state, process, credential, egress separation | Intended directory naming is incomplete same-user isolation; no coexistence test. | P2, P7 |
| Intermittently powered host | Orderly process path exists; abrupt host durability and cross-harness restart correctness are unknown. | P2, P4, P5, P7 |
| Windows / WSL2 / Linux | Native Windows RLM unsupported; WSL2 unknown; Linux official. They cannot be merged. | P7 |
| Docker applicability | Core absent/not applicable; optional remote Docker is separate and unpinned. | P2, P3, P7, P8 |
| GPU serialization | Remote inference can avoid local GPU; renderer/local models remain heavy; no enforced lock or measured contention. | P7, LAW |
| Tokens, wall time, GPU minutes, dollars | Must be metered with P8 formulas; present campaign total confidence `2/10`. | P8 |
| Current Pi control | Installed Pi `0.80.6`; no qualifying PRIME comparison and no local-byte cryptographic binding. | P9 |

## Unresolved-claims register

| Claim not available | Why unresolved / blocker | Owning artifact and precise evidence needed |
|---|---|---|
| Launch revision equals B | Announcement names no unique same-day release. | P1: date-preserved first-party release/commit binding. |
| Reproducible executable B | Packaged npm, Python, dynamic acquisitions, models/services are open. | P2: digest-locked package/runtime/service manifest and offline recreation. |
| Execution and output rights close | Provenance, transitive raw terms, provider/model/weight/output and Prime service terms are missing/conflicting. | P3: immutable bytes, raw licenses/notices, selected service/account/model terms. |
| PRIME learns from observed reward | `outcome` is model-authored expectation; no reward producer/consumer. | P4: externally priced reward schema and trajectory→update→later-load identities. |
| Replayable complete trajectory | Required IDs, hashes, terminal events, deterministic replay/re-execution and later-use receipt are absent. | P5: producer→durable record→query/export closure and falsifiers. |
| Vordar visual gate is enforceable | Capture, reviewed-byte digest, independent verdict/reward binding are absent. | P6: exact source/render/reviewed hash chain and separate judge identity/verdict. |
| Host/platform/coexistence fits | WSL2 and resources unknown; Windows defect; no contention/separation test. | P7: approved platform-specific measurement and process/state/GPU inventory. |
| Budget is closed | Required rates/quantities, labor, storage and recovery exposure unknown. | P8: selected accounts/rates plus metered real-task units. |
| PRIME improves over Pi `0.80.6` | No qualifying matched head-to-head. | P9: retained matched real-task artifacts and independent outcomes. |
| Safe intermittent-host recovery | Source cannot prove byte durability, external disposition, semantic idempotency, or Pi separation. | P2/P4/P5/P7: later executable impolite-path test below. |

## Minimum evidence gates for any phase-2 matched-pilot planning

Gates 1–6 must close before a responsible plan can fix an executable baseline and budget; gate 7 is mandatory plan content and must pass later before pilot eligibility. [PLAN]

1. **Identity/runtime gate:** bind every proposed acquired byte to B (or explicitly authorize a newer immutable baseline), close packaged npm/Python/dynamic dependencies, select one supported OS path, and preserve P1's historical unknown. [P1][P2][P7]
2. **Rights/service gate:** close raw source/package/provenance/model/weight/output/service/account terms for the exact enabled path; disable every optional unknown edge by construction; prove no NC/unknown output reaches shipping. [P3][NC]
3. **Boundary gate:** name one already-on-disk real frozen task and exact input hashes; define an enforceable non-shipping write root plus separate Pi/PRIME state, process, temp, IPC, credential, environment and egress ownership. No setup occurs at this gate. [PILOT][P2][REAL]
4. **Observability gate:** require episode/task/attempt, input/output/artifact/trajectory/system/harness/checkpoint/code hashes, exact provider/model revision, complete root+child linkage, external reward provenance, refinement identity, later fresh-session load/use receipt, and queryable terminal disposition. Missing native fields remain explicit external requirements, not credited to PRIME. [P4][P5]
5. **Visual gate:** retain exact produced and reviewed frame bytes; bind camera/lighting/player-scale labels and frame hashes to a verdict-only result from a separately identified Sol judge. Independent metrics may reject before judging but may not ship. [P6][VIS][MET][INST][KEEP]
6. **Cost/resource gate:** replace P8 variables with selected account rates and bounded tokens/calls, person-hours, wall time, GPU model/minutes, storage/backup/egress, CPU/RAM/process growth, and recovery reserve; define external rejection of overlapping heavy GPU ownership. [P7][P8]
7. **Recovery test gate required in the phase-2 plan and required to pass before pilot eligibility:** retain all test outputs and use an independent verifier over the same bytes restart consumers read. [P2][P4][P5][P7][RED][IMP][KEEP]

### Mandatory executable recovery red-proof (later phase; not run or designed here)

The later approved test must compare an orderly `prime-agent shutdown` path with abrupt client/worker death and a host-power-loss equivalent, include nonzero downtime, then immediate same-ID and new-ID retry. At provider, tool, transcript/checkpoint, and pre/post refinement-publication boundaries it must produce a durable `completed`, `failed`, `cancelled`, or `uncertain` disposition; hash and parse exact surviving session, harness/history, checkpoint, frame, verdict, and journal bytes; reconcile remote effects before retry; and prove zero/one/duplicate semantic outcomes. [P2][P4][P5][P6]

Restart evidence must show dependency order rather than assume it: validate separate persistent roots and credentials/network; start and verify Pi control independently; start PRIME supervisor → catalog/worker → session plus global/local harness → kernel/forkserver → selected provider/optional service; and explicitly add any later container/database/service dependency. It must prove Pi and PRIME state/process/temp/IPC/credential bytes do not mix, known children are reaped, and a deliberately concurrent heavy-GPU launch is rejected rather than merely observed. [P2][P5][P7]

Fail-first mutations must independently remove/change the artifact byte, trajectory link, reward ID, refinement/checkpoint ID, later prompt entry, model revision, or reviewed frame byte and make the verifier red; corrupt/torn transcript, harness and checkpoint inputs must preserve suspect bytes and block silent-empty success. Breaking restart order, state separation, idempotency, or the GPU lock must also make the gate red. Green exit status, logs, path identity, or a self-grading metric is insufficient. [P4–P7][RED][MET][INST]

Passing a later recovery test is necessary, not sufficient, for a matched pilot or adoption. Until it passes, **pilot eligibility is unavailable** regardless of this planning gate. [PLAN]

## Final planning gate

Rights/service execution closure, reproducible runtime closure, complete reward/trajectory linkage, host coexistence, and recovery evidence are presently missing or blocked. Those gaps prevent responsible phase-2 matched-pilot planning from fixing an executable baseline and budget; they do not prove that PRIME can never qualify. [P2–P9][PLAN]

**INSUFFICIENT EVIDENCE**
