# PRIME Agent phase-1 feasibility audit plan

**Status:** phase 1 in progress; P1 is complete, with no setup or adoption decision performed.

## Question and fixed premise

The user identifies the target as Prime Intellect's **PRIME Agent**, launched
2026-08-05, and describes it as a self-improving RLM. Those statements select
the subject of this plan; they are not substitutes for source verification. P1
tested whether the launch article could be bound to an exact release before
accepting downstream claims.

Phase 1 asks whether the user-authorized immutable baseline is sufficiently
identified, permitted, observable, operable, and evidenced to justify designing
a matched Vordar pilot. It does not install or run the product and does not
decide adoption.

## Post-P1 decision record — 2026-08-06

P1 found that the 2026-08-05 launch article cannot be bound to a unique release,
tag, or source commit from the available primary evidence. That historical
finding remains **UNRESOLVED** and must remain visible in every downstream
artifact; this decision does not rewrite P1 or claim that any candidate was the
launch revision.

After reviewing that result, the user authorized Prime Agent **`v0.7.0`** at
immutable commit **`be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`** as the phase-1
audit baseline. P2–P10 may proceed against that exact baseline. Every downstream
claim must distinguish “applies to the user-authorized `v0.7.0` baseline” from
“applies to the unresolved launch revision”; no tag's current mutability may
replace the recorded commit SHA.

## Execution model

- **Finding before change.** All tasks below are `type=finding`. Phase 1 may
  produce a decision packet and pilot-entry gates, but no setup, integration,
  benchmark, training, or production change.
- **Sol-only analysis.** The work is decision-bearing source interpretation,
  closure enumeration, and comparison. Each task uses the Sol analysis seat;
  evidence capture is part of that bounded finding rather than a separate
  lower-seat judgment.
- **Serial gates.** Run tasks in order. P1 plus the dated user baseline decision
  gates every other task; P1's unresolved launch binding does not block analysis
  of the authorized immutable commit. Component/runtime closure gates the
  license, learning, platform, and operating-cost analyses. Dataflow gates
  observability. Do not dispatch work that an earlier finding could moot. Before
  each dispatch, re-open its named dependencies and report source or path drift.
- **One artifact per dispatch.** A worker may modify only its exact deliverable
  path. The orchestrator reads the artifact and its exact-path diff before the
  next dispatch; worker prose is not verification.
- **Unknown is an outcome.** Inaccessible source, service-internal behavior,
  missing exact-baseline evidence, or an unclosed dependency is recorded as
  `unknown`, not inferred from marketing or predecessor releases. The unresolved
  historical launch binding stays explicit but is not imputed to the authorized
  baseline. An unknown in baseline identity, rights, runtime closure, recovery,
  or the learning/persistence critical path blocks a pilot-eligible conclusion.
- **No execution side effects.** Workers may use public read-only web sources.
  They may not install, download, clone, authenticate, call paid/private APIs,
  run PRIME/training/GPU jobs, alter user-global configuration, inspect
  `reference/`, or edit game/production files. They may not change license
  verdicts. Expensive execution is outside phase 1 and requires a later user
  checkpoint.
- **Exact-path integration.** The `.claude/` repository is separate. Review,
  stage, and commit only named phase-1 artifact paths; never use a sweep add or
  commit while unrelated work exists.

## Cross-cutting coexistence and recovery requirement

Pi remains the control and must coexist with Prime on this intermittently
powered machine. Docker or any other container layer is a hypothesis for P2,
P7, P8, and P10 to assess from exact-baseline evidence; it is not assumed to be
required, supported, installed, or the recovery mechanism.

Across P2, P4, P5, P7, P8, and P10, the audit must close, with sourced behavior
or an explicit `unknown`: orderly shutdown; abrupt host power loss and process
death; restart after downtime; persisted state, checkpoint, and trajectory
integrity; disposition of an in-flight episode; idempotent resume or replay;
restart ordering for local services, containers if applicable, and databases;
explicit operator recovery steps; state separation between Pi and Prime; and
GPU/resource contention. Each named task must identify the relevant state,
process, producer/consumer, lifecycle transition, expected observable outcome,
and evidence or missing evidence rather than merely saying “restart supported.”

Phase 1 may establish eligibility only for phase-2 matched-pilot planning. Phase
2 must include and execute a recovery test that exercises both orderly shutdown
and impolite paths (abrupt death/power-loss equivalent, downtime, restart, and
immediate retry), inspects persisted bytes and episode outcomes, and red-proofs
idempotent resume/replay. Prime must not be described as pilot-eligible until
that later test passes without corrupting or mixing Pi state, losing an in-flight
episode silently, violating local dependency restart order, or allowing GPU and
other resource contention to escape the one-heavy-job gate.

## Source and evidence hierarchy

Use the highest available tier for each claim and state when only a lower tier
exists.

1. **Immutable exact-release primary evidence:** signed/tagged release objects,
   commit-SHA repository permalinks, source/manifest/lockfile blobs at that SHA,
   package or container digests, model/weight revision hashes, and versioned API
   schemas. These control identity, code behavior, and dependency claims.
2. **Exact-release first-party records:** release notes, documentation, model
   cards, service documentation, and announcements attributable to the vendor.
   If mutable, preserve an archive URL or quoted excerpt and record publication
   or effective date plus retrieval date.
3. **Primary legal and commercial text:** raw LICENSE/NOTICE bytes, weight and
   dataset terms, service terms, privacy/retention terms, and official pricing
   pages. Record artifact territory and effective/retrieval dates. A model-card
   tag, repository metadata, or summary is not a license.
4. **Independent exact-release evidence:** reproducible analyses, security or
   runtime reports, head-to-head comparisons, migration reports, and
   practitioner accounts that name the exact release and disclose conditions.
   Record publication and retrieval dates.
5. **Predecessor/general context:** earlier PRIME releases, generic RLM papers,
   vendor demos, search snippets, and unsourced commentary. These may identify
   questions only; they cannot prove exact-release behavior or practitioner
   outcomes.

Every material claim row must include: claim; source title/author; source tier;
URL; immutable commit/tag/revision/digest when available; exact section, lines,
or quoted excerpt; publication/effective date; retrieval date; exact-release
applicability; and caveat/conflict. GitHub citations must use commit-SHA blob
permalinks where possible. Mutable pages must carry an effective date when the
page supplies one and always a retrieval date. Conflicts remain visible and
are resolved by artifact specificity and tier, never by majority vote.

Comparative evidence is recency-bounded to the target release: search from
2026-08-05 through the audit retrieval date. Older or version-unspecified
experience is labeled context and never presented as exact-release evidence.
Absence of a head-to-head or practitioner record is itself a confidence limit,
not permission to substitute isolated specifications.

## Acceptance criteria

The phase-1 audit is complete only when all of the following are true:

1. The exact project and owner are locked; the user-authorized `v0.7.0` commit,
   package/container/model revisions, and release date are locked with immutable
   primary citations or explicitly unresolved. P1's unresolved launch binding
   remains separately visible, and homonymous products cannot be mixed.
2. A recursively enumerated component/runtime graph closes code, models/weights,
   data assets, local processes, optional relevant features, external services,
   persistence stores, and version/acquisition edges. Every node is classified
   as present, absent, not applicable, or unknown—never hidden under “etc.”
3. Code, vendored code, weights, datasets/base models, and services each have
   separately sourced rights/terms. Commercial, territory, output, data-use,
   redistribution, attribution, privacy, and retention constraints are mapped
   without editing Vordar's standing license verdicts.
4. A source-cited dataflow shows what actually changes during learning, who
   computes reward, where trajectories and updates persist, how a later episode
   loads them, and what survives process/host restart. Prompt memory, retrieval,
   context accumulation, replay, inference-time search, and weight/optimizer
   updates are not conflated.
5. Trajectory, reward, replay, tool/artifact, and failure observability are
   closed across success, rejection, timeout, crash, restart, partial write,
   and unavailable-service paths. Each request/episode path has a visible
   outcome or is marked as a gap.
6. Native and composable multimodal support is mapped separately for image/frame
   input, visual tool use, artifact inspection, visual reward/evaluation, and
   independent judge separation.
7. Windows, WSL2, and Linux support; CPU/RAM/storage/network needs; supported
   GPUs, drivers/runtime, minimum and practical VRAM; local-versus-service
   placement; and concurrency constraints are sourced or marked unknown. No
   hardware claim is inferred from an adjacent release.
8. Setup and recurring operations are priced in concrete units: person-hours,
   download/storage GB, GPU model/minutes or hours, tokens/API calls, dollars,
   service accounts, credentials, quotas, retention, monitoring, backup, and
   failure recovery. Estimates expose assumptions and ranges.
9. Exact-release comparison and practitioner evidence is reported independently
   from first-party capability claims. Missing, stale, sponsored, or
   version-ambiguous evidence lowers confidence visibly.
10. The synthesis compares **replacement**, **sidecar-worker**, and
    **no-adoption** independently. Each option has a context-agnostic outcome
    `/10`, confidence `/10`, and concrete setup/run/operations cost; scores are
    not blended and no option is declared adopted.
11. Vordar boundaries preserve Pi as the control, sandboxed non-shipping writes,
    strict NC-tool exclusion from shipping paths, provenance, replayability,
    independent Sol visual judgment, metrics as pre-screen only, and one heavy
    GPU job at a time.
12. Each promised property is verified from the artifact's cited evidence, not
    the worker's exit code. A required empty field, unpinned exact-version claim,
    unexplained graph edge, or unsupported score causes review failure.
13. Coexistence and recovery claims close every lifecycle in the cross-cutting
    requirement with observable outcomes and explicit unknowns. Phase-1 source
    evidence cannot substitute for the required phase-2 recovery test, and no
    phase-1 conclusion may claim that Prime is already pilot-eligible.

## Dependency-ordered tasks

### P1 — Identity and immutable source lock

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/01-identity-source-lock.md`.
- **Scope:** Resolve the canonical Prime Intellect organization, repository,
  product naming, exact 2026-08-05 release record, release/tag object, commit,
  distribution artifacts, package/container identifiers, model/weight revisions,
  documentation version, and the release's own definition of “RLM” and
  “self-improving.” Produce a homonym/disambiguation table and immutable source
  manifest. Treat the user's identity/date as the hypothesis under test.
- **Do not touch / decide:** Do not research broader feasibility, infer behavior
  from an announcement, install/download/clone/authenticate, or decide that PRIME
  is feasible or adoptable. Do not write outside the deliverable.
- **Verify:** Read the exact artifact and open every canonical citation. Review
  fails if two claims resolve to different products/releases, if a mutable URL
  stands in for an available commit/revision, if release date or ownership lacks
  primary evidence, or if any mutable source lacks retrieval date. The artifact
  must end with `LOCKED` or `UNRESOLVED` and list the precise falsifier for its
  status.
- **Dependencies:** None.
- **Type:** finding.

### P2 — Complete component and runtime closure

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/02-component-runtime-closure.md`.
- **Scope:** Starting only from P1's product/repository identity and the dated
  user-authorized `v0.7.0` commit baseline, recursively enumerate executable
  entrypoints, packages and lockfiles, agent/orchestrator processes, model
  providers and weights, tool/sandbox layers, training/evaluation workers,
  databases/object stores, telemetry, queues, containers, relevant optional
  features, and local/remote services. For every node and edge record owner,
  exact version/revision, purpose, required/optional status, acquisition mode,
  runtime placement, persistence ownership, shutdown behavior, restart
  prerequisite/order, and evidence. Treat Docker/container use as a hypothesis:
  distinguish required, optional, unsupported, absent, and unknown from source.
  Include a process graph, bill of materials, service-boundary graph,
  enumeration method, Pi/Prime state boundaries, resource ownership, and
  unresolved edges.
- **Do not touch / decide:** Do not install, clone, resolve dependencies locally,
  call services, perform license conclusions, assume optional means irrelevant,
  or design Vordar integration. Do not write outside the deliverable.
- **Verify:** Review the graph against every exact-baseline manifest, lockfile,
  entrypoint, setup path, and documented service call cited in the artifact.
  Fail if any discovered dependency has no node, any edge has no source and
  destination, any node lacks version/placement/requiredness, persistent-state
  ownership, shutdown behavior, or restart prerequisite; if Docker/container
  status is assumed; if Pi/Prime state or GPU/resource boundaries are merged;
  if “etc.” hides a category; or if completeness is asserted while an edge is
  unknown. Record a closed-world result or an explicit blocking frontier.
- **Dependencies:** P1 is complete as `UNRESOLVED`; the 2026-08-06 user decision
  supplies the immutable `v0.7.0` commit baseline required to proceed. P1's
  historical launch-binding finding remains unresolved.
- **Type:** finding.

### P3 — License, weights, datasets, and service-terms closure

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/03-license-weights-service-closure.md`.
- **Scope:** Evaluate every P2 node as a distinct artifact: source code, vendored
  modules, packages, containers, model weights/base models, datasets, generated
  data, hosted APIs, storage/telemetry, and other services. Capture raw primary
  terms and version/effective date; map commercial use, territory, output,
  training/data-use, redistribution, attribution/NOTICE, patent, privacy,
  retention, and service restrictions. Where code “builds upon” restricted
  upstream, compare immutable web-visible source/provenance where possible and
  otherwise mark provenance unknown. Apply the standing strict-NC shipping-path
  gate as a constraint, not a new verdict.
- **Do not touch / decide:** Do not alter `content/source/CREDITS.md`, any license
  verdict, or the non-commercial-tooling rule; do not offer legal advice,
  download artifacts, accept terms, create accounts, or declare adoption. Do
  not write outside the deliverable.
- **Verify:** Cross-check one matrix row for every P2 node and separate rows for
  code, weights, datasets, and services even when one vendor supplies them.
  Fail on model-card tags used as licenses, summarized rather than raw legal
  text, absent effective/retrieval dates, unexamined vendored provenance,
  omitted territory/output/data-use fields, or any `compatible` conclusion with
  an unresolved transitive artifact. The artifact reports preliminary
  compatibility, block, or unknown without changing standing verdicts.
- **Dependencies:** P1, P2.
- **Type:** finding.

### P4 — Actual learning and persistence dataflow

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/04-learning-persistence-dataflow.md`.
- **Scope:** Trace exact-baseline source/data paths from task input through model
  inference, environment/tool actions, trajectory capture, reward production,
  optimization or other adaptation, checkpoint/memory publication, registry or
  storage, and loading into a later matched episode. Name what changes
  (weights, optimizer state, policy, prompts, memory, retrieval corpus, code, or
  another artifact), component ownership, serialization/schema, storage
  location, retention/lifecycle, restart/host durability, and whether learning
  is local or vendor-service-internal. For orderly shutdown, abrupt power loss
  or process death, and restart after downtime, trace persisted-byte integrity,
  checkpoint/trajectory commit boundaries, in-flight episode disposition,
  resume/replay identity and idempotency, and required service/container/database
  ordering. Separate one-episode search from durable cross-episode improvement
  and identify every bypass/fallback path.
- **Do not touch / decide:** Do not run an episode, training, API, or persistence
  probe; do not treat marketing, a demo, replay, longer context, or service
  claims as proof of learning; do not design the pilot or decide fitness. Do not
  write outside the deliverable.
- **Verify:** The artifact must contain a node/edge dataflow and a claim matrix
  citing exact source/API/schema evidence for every critical edge and lifecycle
  transition. Fail if a later episode has no evidenced load edge, if the learned
  artifact is unnamed, if reward has no producer/consumer, if orderly or abrupt
  shutdown disposition is missing, if restart survival or persisted-byte
  integrity is assumed, if resume/replay can duplicate an update without an
  explicit outcome, if dependency ordering is omitted, if fallback can silently
  bypass learning, or if service-internal behavior is labeled proven without
  inspectable evidence. Conclude `demonstrated by source`, `claimed but opaque`,
  `not present`, or `unknown` for each persistence and recovery mechanism.
- **Dependencies:** P1, P2; P3 must identify no terms barrier to continued
  read-only analysis.
- **Type:** finding.

### P5 — Trajectory, reward, replay, and failure observability

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/05-observability-replay-failures.md`.
- **Scope:** Enumerate exact-baseline observability for episode identity, inputs,
  prompts/model revision, tool calls/results, files/artifact hashes, timestamps,
  environment and code revision, trajectories, reward components and provenance,
  update/checkpoint IDs, later-load linkage, replay semantics, export, retention,
  and operator diagnostics. Close orderly shutdown, success, rejected action,
  timeout, abrupt host power loss or worker/process death, downtime and restart,
  immediate retry, duplicate episode, partial write, corrupt checkpoint,
  quota/auth failure, and unavailable service paths. Record the observable
  disposition of every in-flight episode, checkpoint, and trajectory; whether
  resume/replay is idempotent; dependency restart-order events; and the explicit
  operator recovery surface. State whether replay means deterministic playback,
  re-execution, or inspection.
- **Do not touch / decide:** Do not generate traces, invoke services, test crashes,
  invent a logging layer, or accept self-reported reward as priced outcome. Do
  not write outside the deliverable.
- **Verify:** Trace each required field from producer through persisted record to
  query/export surface, citing schemas or exact source. Fail if orderly shutdown,
  abrupt loss, restart-after-downtime, immediate retry, or an in-flight episode
  can end silently; if reward cannot be tied to trajectory and learned artifact;
  if persisted-byte/checkpoint integrity or replay semantics are unnamed; if
  duplicate resume/replay has no observable outcome; if operator steps or local
  dependency ordering cannot be observed; if artifact bytes lack identity; or
  if retention/export is assumed. Include a falsification table naming the
  missing record or event that would make each observability claim false.
- **Dependencies:** P4.
- **Type:** finding.

### P6 — Multimodal and visual-support closure

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/06-multimodal-visual-support.md`.
- **Scope:** For the exact release, independently map image/frame ingestion,
  supported formats and limits, model/provider vision capability, screenshot or
  render tools, binary artifact access, temporal/multi-view handling, visual
  comparison, visual reward/evaluation inputs, and output persistence. Separate
  native support from user-composable tool calls and external services. Map
  whether an independent Sol visual judge can remain isolated from frame
  production and whether metrics can remain pre-screen only.
- **Do not touch / decide:** Do not run vision models, render frames, upload
  Vordar assets, score visual quality, design adapters, or claim that text/file
  support implies visual understanding. Do not write outside the deliverable.
- **Verify:** Require one exact-release evidence row for every modality stage and
  an end-to-end visual path with ownership and data boundaries. Fail if native,
  composable, and absent support are conflated; if limits/provider dependence
  are missing; if visual reward is self-judged by the producer without the gap
  being named; or if persisted trajectories cannot identify reviewed bytes.
- **Dependencies:** P2, P4, P5.
- **Type:** finding.

### P7 — OS, platform, GPU, and VRAM envelope

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/07-platform-gpu-vram.md`.
- **Scope:** Establish exact-baseline support for native Windows, WSL2, and
  Linux; shells and containers; CPU architecture; drivers and CUDA/runtime;
  supported GPU families; declared minimum and practitioner-observed practical
  VRAM; system RAM, disk/download size, network, ports, filesystem semantics,
  process model, and local-versus-remote compute placement. Treat Docker or
  another container runtime as a sourced hypothesis, not an assumed requirement
  or capability. Separate Pi and Prime agent orchestration, inference, rollout,
  learning/update, database/service, and visual workloads; map state/resource
  isolation, simultaneous residency, orderly and abrupt termination, local
  restart ordering after machine downtime, and contention with Vordar's
  one-heavy-GPU-job rule.
- **Do not touch / decide:** Do not probe the host, install drivers/containers,
  download weights, run estimators or GPU jobs, change global config, or infer
  exact-release requirements from adjacent versions. Do not write outside the
  deliverable.
- **Verify:** Every requirement row must name workload, support level
  (`official`, `practitioner-observed`, `unsupported`, or `unknown`), exact
  baseline, source, and resource units. Fail if “GPU required” lacks task and
  VRAM quantity; if Docker/container use is assumed; if service compute is
  counted as local; if Windows and WSL2 are merged; if minimum and practical
  needs are merged; if Pi/Prime CPU, RAM, disk, port, process, state, or GPU
  contention is omitted; if shutdown/restart ordering is absent; or if an
  unsourced estimate is presented as a requirement.
- **Dependencies:** P1, P2, P4, P6.
- **Type:** finding.

### P8 — Pricing and operational closure

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/08-pricing-operations.md`.
- **Scope:** Price acquisition/setup and continuing operation across self-hosted
  and required service components: person-hours, downloads/storage, local or
  rented GPU model and minutes/hours, inference/training tokens and API calls,
  service subscriptions, telemetry/storage/egress, credentials/accounts,
  quotas/rate limits, retention, monitoring, backups, upgrades, and incident,
  failed-run, and power-loss recovery. Price Pi/Prime coexistence and state
  separation, shutdown/restart operations, persisted-state integrity checks,
  in-flight episode disposition, idempotent resume/replay, dependency restart
  ordering, operator recovery steps, and GPU/resource contention. Price
  container acquisition/operation/recovery only where P2/P7 evidence makes it
  applicable; Docker is not a default assumption. Build transparent
  low/expected/high matched-pilot and ongoing-campaign scenarios using dated
  official unit prices and explicit workload assumptions; report formulas where
  usage is genuinely unknown.
- **Do not touch / decide:** Do not purchase, authenticate, request quotes,
  create accounts, call APIs, run workloads, hide labor/operational cost, or
  rank options by cheapness. Do not write outside the deliverable.
- **Verify:** Recalculate every scenario from displayed quantities × dated unit
  prices and distinguish one-time, per-episode, monthly, GPU, token, storage,
  and labor costs. Fail if a required P2 service is absent; “free” omits
  hardware/labor; container cost is assumed without applicability; orderly and
  abrupt recovery labor, restart-order dependencies, integrity verification,
  replay/duplicate-run exposure, Pi/Prime isolation, or contention cost is
  omitted; a mutable price lacks effective/retrieval date; ranges hide
  assumptions; or dollars are given without concrete workload units. Unknown
  prices stay unknown and propagate to confidence.
- **Dependencies:** P2, P3, P4, P7.
- **Type:** finding.

### P9 — Exact-release comparative and practitioner evidence

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/09-comparative-practitioner-evidence.md`.
- **Scope:** Search the 2026-08-05-to-retrieval window for independent evidence
  naming the user-authorized `v0.7.0` commit baseline: head-to-head comparisons,
  migration reports, practitioner deployment accounts, issue reports with
  reproduction detail,
  reliability/security analyses, and disclosed benchmarks. Compare PRIME's
  evidenced capabilities and operational failure modes with the current Pi
  control only on matched dimensions established by P2–P8. Keep vendor claims,
  independent measurements, anecdotes, and predecessor context in separate
  tables. Record search terms, venues, dates, sponsorship/conflicts, workload,
  hardware/model, sample size, and reproducibility.
- **Do not touch / decide:** Do not run benchmarks, install either harness,
  generalize from older PRIME versions, treat popularity as quality, fabricate a
  head-to-head, or decide adoption. Do not write outside the deliverable.
- **Verify:** Open every cited comparison/practitioner source and confirm it names
  the authorized baseline or is visibly labeled non-exact context. Fail if
  isolated specifications are called comparison, dates fall outside the window
  without a stale/context label, vendor demos are called practitioner evidence,
  conditions are omitted, or “no evidence” lacks a reproducible search ledger.
  Report sparse or absent evidence explicitly and lower confidence rather than
  filling the gap with predecessor claims.
- **Dependencies:** P1 through P8.
- **Type:** finding.

### P10 — Vordar boundary mapping and synthesis

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/10-vordar-boundary-synthesis.md`.
- **Scope:** Synthesize P1–P9 against `.claude/CLAUDE.md`, applicable standing
  memory rulings, and `.claude/tasks/prime-agent-learning-pilot.md`. Map exact
  integration boundaries for (a) replacing Pi as campaign harness, (b) using
  PRIME only as a sandboxed sidecar worker while Pi remains orchestrator/control,
  and (c) no adoption/resuming the existing Pi loop. For each, map read/write,
  credentials, services/data egress, provenance, license, trajectory/reward,
  independent visual-judge, replay, failure recovery, GPU scheduling, rollback,
  and control-arm boundaries. Explicitly map Pi/Prime coexistence and state
  separation on an intermittently powered machine; Docker/container
  applicability; orderly shutdown and abrupt loss/process death; downtime and
  restart; persisted state/checkpoint/trajectory integrity; in-flight episode
  disposition; idempotent resume/replay; local service/container/database
  ordering; operator recovery steps; and GPU/resource contention. Present an
  unresolved-claims register and the minimum user-approved evidence gates for
  entering phase-2 pilot planning, including the later recovery test required
  before pilot eligibility can be demonstrated.
- **Do not touch / decide:** Do not inspect `reference/`, edit the pilot task,
  game/production files, license verdicts, design law, or user-global config;
  do not design/setup/run the pilot; do not choose or enact adoption. Do not
  convert an unknown into an assumption or write outside the deliverable.
- **Verify:** Read every synthesis statement back to a named P1–P9 claim and
  standing Vordar constraint. Fail if replacement, sidecar-worker, and
  no-adoption are not assessed independently; if any lacks context-agnostic
  outcome `/10`, confidence `/10`, concrete one-time/per-run/ongoing costs,
  assumptions, reversibility, and blockers; if confidence ignores evidence
  gaps; if no-adoption cost is treated as zero by default; if Docker is assumed;
  if any cross-cutting coexistence/recovery lifecycle lacks a sourced outcome or
  explicit unknown; if the phase-2 gate omits an executable, red-proofed recovery
  test covering orderly shutdown, abrupt loss, downtime/restart, immediate
  retry, persisted-byte integrity, in-flight disposition, idempotent
  resume/replay, dependency ordering, Pi/Prime state separation, and resource
  contention; or if the report declares adoption or pilot eligibility. The
  final gate is only `eligible`, `ineligible`, or `insufficient evidence` for
  **phase-2 matched-pilot planning**, followed by a user checkpoint before any
  install, credentials, global change, or heavy run. Pilot eligibility remains
  unavailable until the later phase-2 recovery test passes.
- **Dependencies:** P1 through P9.
- **Type:** finding.

## Final review packet

The orchestrator presents P10 together with links to P1–P9, not a prose-only
summary. The three paths remain independent:

| Path | Required decision fields |
|---|---|
| Replacement | Outcome `/10`; confidence `/10`; setup person-hours and download/storage; per-run GPU/tokens/dollars; recurring operations; rights/service blockers; rollback and Pi-control impact |
| Sidecar-worker | Outcome `/10`; confidence `/10`; adapter/sandbox person-hours; per-run GPU/tokens/dollars; recurring operations; data/provenance boundaries; rollback and control-arm impact |
| No adoption | Outcome `/10`; confidence `/10`; immediate setup cost; continuing Pi campaign labor/GPU/tokens; opportunity and failure costs stated as ranges rather than disguised as zero |

Scores describe expected Vordar campaign outcome in plain, context-agnostic
terms and remain independent from confidence and cost. Quality outranks
convenience, while licensing remains a hard gate. The user—not the audit—decides
whether to authorize phase-2 pilot planning or any subsequent setup.

## Plan-artifact verification

Read back `.claude/tasks/prime-agent-feasibility-audit-plan.md`, then run:

```bash
git -C .claude add -N -- tasks/prime-agent-feasibility-audit-plan.md
git -C .claude diff -- tasks/prime-agent-feasibility-audit-plan.md
```

`git add -N` is only to expose the untracked file in the exact-path diff; it does
not authorize a commit. Review must confirm that every P1–P10 task contains the
model seat, exact deliverable, scope, do-not-touch/decide boundary, falsifiable
artifact verification, dependencies, and `Type: finding`, and that this planning
change touches only `.claude/tasks/prime-agent-feasibility-audit-plan.md`.
