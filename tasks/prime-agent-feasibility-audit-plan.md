# PRIME Agent phase-1 feasibility audit plan

**Status:** planned only; no product research, setup, or adoption decision has been performed.

## Question and fixed premise

The user identifies the target as Prime Intellect's **PRIME Agent**, launched
2026-08-05, and describes it as a self-improving RLM. Those statements select
the subject of this plan; they are not substitutes for source verification. The
first audit task must lock the exact release before any downstream claim is
accepted.

Phase 1 asks whether that exact release is sufficiently identified, permitted,
observable, operable, and evidenced to justify designing a matched Vordar pilot.
It does not install or run the product and does not decide adoption.

## Execution model

- **Finding before change.** All tasks below are `type=finding`. Phase 1 may
  produce a decision packet and pilot-entry gates, but no setup, integration,
  benchmark, training, or production change.
- **Sol-only analysis.** The work is decision-bearing source interpretation,
  closure enumeration, and comparison. Each task uses the Sol analysis seat;
  evidence capture is part of that bounded finding rather than a separate
  lower-seat judgment.
- **Serial gates.** Run tasks in order. Identity/source lock gates every other
  task. Component/runtime closure gates the license, learning, platform, and
  operating-cost analyses. Dataflow gates observability. Do not dispatch work
  that an earlier finding could moot. Before each dispatch, re-open its named
  dependencies and report source or path drift.
- **One artifact per dispatch.** A worker may modify only its exact deliverable
  path. The orchestrator reads the artifact and its exact-path diff before the
  next dispatch; worker prose is not verification.
- **Unknown is an outcome.** Inaccessible source, service-internal behavior,
  missing exact-release evidence, or an unclosed dependency is recorded as
  `unknown`, not inferred from marketing or predecessor releases. An unknown in
  identity, rights, runtime closure, or the learning/persistence critical path
  blocks a pilot-eligible conclusion.
- **No execution side effects.** Workers may use public read-only web sources.
  They may not install, download, clone, authenticate, call paid/private APIs,
  run PRIME/training/GPU jobs, alter user-global configuration, inspect
  `reference/`, or edit game/production files. They may not change license
  verdicts. Expensive execution is outside phase 1 and requires a later user
  checkpoint.
- **Exact-path integration.** The `.claude/` repository is separate. Review,
  stage, and commit only named phase-1 artifact paths; never use a sweep add or
  commit while unrelated work exists.

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

1. The exact project, owner, release/tag, commit, package/container/model
   revisions, and release date are either locked with immutable primary
   citations or explicitly unresolved; homonymous products cannot be mixed.
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
- **Scope:** Starting only from P1's locked identifiers, recursively enumerate
  executable entrypoints, packages and lockfiles, agent/orchestrator processes,
  model providers and weights, tool/sandbox layers, training/evaluation workers,
  databases/object stores, telemetry, queues, containers, relevant optional
  features, and local/remote services. For every node and edge record owner,
  exact version/revision, purpose, required/optional status, acquisition mode,
  runtime placement, and evidence. Include a process graph, bill of materials,
  service-boundary graph, enumeration method, and unresolved edges.
- **Do not touch / decide:** Do not install, clone, resolve dependencies locally,
  call services, perform license conclusions, assume optional means irrelevant,
  or design Vordar integration. Do not write outside the deliverable.
- **Verify:** Review the graph against every exact-release manifest, lockfile,
  entrypoint, setup path, and documented service call cited in the artifact.
  Fail if any discovered dependency has no node, any edge has no source and
  destination, any node lacks version/placement/requiredness, “etc.” hides a
  category, or completeness is asserted while an edge is unknown. Record a
  closed-world result or an explicit blocking frontier.
- **Dependencies:** P1 must be `LOCKED`.
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
- **Scope:** Trace exact-release source/data paths from task input through model
  inference, environment/tool actions, trajectory capture, reward production,
  optimization or other adaptation, checkpoint/memory publication, registry or
  storage, and loading into a later matched episode. Name what changes
  (weights, optimizer state, policy, prompts, memory, retrieval corpus, code, or
  another artifact), component ownership, serialization/schema, storage
  location, retention/lifecycle, restart/host durability, and whether learning
  is local or vendor-service-internal. Separate one-episode search from durable
  cross-episode improvement and identify every bypass/fallback path.
- **Do not touch / decide:** Do not run an episode, training, API, or persistence
  probe; do not treat marketing, a demo, replay, longer context, or service
  claims as proof of learning; do not design the pilot or decide fitness. Do not
  write outside the deliverable.
- **Verify:** The artifact must contain a node/edge dataflow and a claim matrix
  citing exact source/API/schema evidence for every critical edge. Fail if a
  later episode has no evidenced load edge, if the learned artifact is unnamed,
  if reward has no producer/consumer, if process/host restart survival is
  assumed, if fallback can silently bypass learning, or if service-internal
  behavior is labeled proven without inspectable evidence. Conclude
  `demonstrated by source`, `claimed but opaque`, `not present`, or `unknown`
  for each persistence mechanism.
- **Dependencies:** P1, P2; P3 must identify no terms barrier to continued
  read-only analysis.
- **Type:** finding.

### P5 — Trajectory, reward, replay, and failure observability

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/05-observability-replay-failures.md`.
- **Scope:** Enumerate exact-release observability for episode identity, inputs,
  prompts/model revision, tool calls/results, files/artifact hashes, timestamps,
  environment and code revision, trajectories, reward components and provenance,
  update/checkpoint IDs, later-load linkage, replay semantics, export, retention,
  and operator diagnostics. Close success, rejected action, timeout, crash,
  abrupt worker death, instant restart, duplicate episode, partial write,
  corrupt checkpoint, quota/auth failure, and unavailable service paths. State
  whether replay means deterministic playback, re-execution, or inspection.
- **Do not touch / decide:** Do not generate traces, invoke services, test crashes,
  invent a logging layer, or accept self-reported reward as priced outcome. Do
  not write outside the deliverable.
- **Verify:** Trace each required field from producer through persisted record to
  query/export surface, citing schemas or exact source. Fail if any lifecycle
  path can end silently, if reward cannot be tied to trajectory and learned
  artifact, if replay semantics are unnamed, if artifact bytes lack identity,
  or if retention/export is assumed. Include a falsification table naming the
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
- **Scope:** Establish exact-release support for native Windows, WSL2, and Linux;
  shells/containers; CPU architecture; drivers and CUDA/runtime; supported GPU
  families; declared minimum and practitioner-observed practical VRAM; system
  RAM, disk/download size, network, ports, filesystem semantics, process model,
  and local-versus-remote compute placement. Separate agent orchestration,
  inference, rollout, learning/update, and visual workloads and identify which
  can contend with Vordar's one-heavy-GPU-job rule.
- **Do not touch / decide:** Do not probe the host, install drivers/containers,
  download weights, run estimators or GPU jobs, change global config, or infer
  exact-release requirements from adjacent versions. Do not write outside the
  deliverable.
- **Verify:** Every requirement row must name workload, support level
  (`official`, `practitioner-observed`, `unsupported`, or `unknown`), exact
  release, source, and resource units. Fail if “GPU required” lacks task and
  VRAM quantity, if service compute is counted as local, if Windows and WSL2
  are merged, if minimum and practical needs are merged, or if an unsourced
  estimate is presented as a requirement.
- **Dependencies:** P1, P2, P4, P6.
- **Type:** finding.

### P8 — Pricing and operational closure

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/08-pricing-operations.md`.
- **Scope:** Price acquisition/setup and continuing operation across self-hosted
  and required service components: person-hours, downloads/storage, local or
  rented GPU model and minutes/hours, inference/training tokens and API calls,
  service subscriptions, telemetry/storage/egress, credentials/accounts,
  quotas/rate limits, retention, monitoring, backups, upgrades, incident and
  failed-run recovery. Build transparent low/expected/high matched-pilot and
  ongoing-campaign scenarios using dated official unit prices and explicit
  workload assumptions; report formulas where usage is genuinely unknown.
- **Do not touch / decide:** Do not purchase, authenticate, request quotes,
  create accounts, call APIs, run workloads, hide labor/operational cost, or
  rank options by cheapness. Do not write outside the deliverable.
- **Verify:** Recalculate every scenario from displayed quantities × dated unit
  prices and distinguish one-time, per-episode, monthly, GPU, token, storage,
  and labor costs. Fail if a required P2 service is absent, “free” omits
  hardware/labor, a mutable price lacks effective/retrieval date, ranges hide
  assumptions, or dollars are given without concrete workload units. Unknown
  prices stay unknown and propagate to confidence.
- **Dependencies:** P2, P3, P4, P7.
- **Type:** finding.

### P9 — Exact-release comparative and practitioner evidence

- **Model seat:** Sol analysis.
- **Deliverable:** `.claude/docs/research/prime-agent/phase-1/09-comparative-practitioner-evidence.md`.
- **Scope:** Search the 2026-08-05-to-retrieval window for independent evidence
  naming P1's exact release: head-to-head comparisons, migration reports,
  practitioner deployment accounts, issue reports with reproduction detail,
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
  the locked release or is visibly labeled non-exact context. Fail if isolated
  specifications are called comparison, dates fall outside the window without
  a stale/context label, vendor demos are called practitioner evidence,
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
  and control-arm boundaries. Present an unresolved-claims register and the
  minimum user-approved evidence gates for entering phase-2 pilot planning.
- **Do not touch / decide:** Do not inspect `reference/`, edit the pilot task,
  game/production files, license verdicts, design law, or user-global config;
  do not design/setup/run the pilot; do not choose or enact adoption. Do not
  convert an unknown into an assumption or write outside the deliverable.
- **Verify:** Read every synthesis statement back to a named P1–P9 claim and
  standing Vordar constraint. Fail if replacement, sidecar-worker, and
  no-adoption are not assessed independently; if any lacks context-agnostic
  outcome `/10`, confidence `/10`, concrete one-time/per-run/ongoing costs,
  assumptions, reversibility, and blockers; if confidence ignores evidence
  gaps; if no-adoption cost is treated as zero by default; or if the report
  declares adoption. The final gate is only `eligible`, `ineligible`, or
  `insufficient evidence` for **phase-2 matched-pilot planning**, followed by a
  user checkpoint before any install, credentials, global change, or heavy run.
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
