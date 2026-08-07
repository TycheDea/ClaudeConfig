# G0 — Evidence Freshness and Scope Reconciliation

## Run record

- **Model seat:** Sol analysis
- **Type:** finding
- **Plan under review:** `.claude/tasks/prime-agent-option2-gate-closing-plan.md`, commit `69cb44d`
- **Deliverable:** complete replacement body for `.claude/docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md`
- **Scope:** Re-open P1–P5, P7, P8, and P10 evidence; refresh mutable release, package, platform, upstream-provenance, service, pricing, legal, and privacy sources; reconcile every G0–G20 task against the revised plan.
- **Do not touch or decide:** No setup, artifact acquisition, package download, installer execution, account access, credential handling, host probing, provider call, plan edit, baseline adoption, license verdict, or feasibility redesign.
- **Verification criterion:** Every mutable decision-bearing source has a current retrieval identity or explicit failure state; changed evidence is classified rather than called unchanged; the immutable baseline and exclusions remain intact; every G-number and RED condition maps to the revised plan; G1 authorization is stated.
- **Previous snapshot:** `2026-08-07`
- **Current retrieval date:** `2026-08-07`
- **Method:** Public, unauthenticated, read-only API/metadata/HTML retrieval. Release assets and package bodies were not acquired.
- **Mutable-page identity rule:** Where no content digest or fixed revision is exposed, the preserved identity is the exact URL, retrieval date, title or displayed effective date, and the quoted decision-bearing fact.
- **Repository assumption:** The inspected plan body is the content committed as `69cb44d`; no branch, tag, or commit was changed during this finding.

## Authorized immutable baseline

| Field | Verified identity | Evidence |
|---|---|---|
| Repository | `PrimeIntellect-ai/prime-agent`, repository ID `1232493406` | Mutable repository metadata, retrieved `2026-08-07` |
| Stable version | `v0.7.0` | Mutable tag/release label |
| Commit | `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387` | [Commit API](https://api.github.com/repos/PrimeIntellect-ai/prime-agent/commits/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387), immutable |
| Tree | `0625a8fd0550a8de7ff05e8d9248e75563e5b520` | Commit’s immutable tree |
| Root manifest | Git blob `0794d88d295f935bcf3ef2e5a7bafc110160eb51`; version `0.7.0`; Node `>=22.8.0` | Immutable baseline source |
| Baseline license | Git blob `e15dcd837b11cfb1f627e388561f3ea6405097c1` | Immutable baseline source |

The authorized baseline is unchanged. The stable release record remains mutable and does not replace the commit/tree lock. Neither the stable record nor the excluded beta channel proves that this baseline is the exact launch revision; the launch-revision binding remains unresolved as required by P1 and the revised plan.

## Stable release metadata refresh

[Stable release ID `365741496`](https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/365741496) still reports:

- tag/name `v0.7.0`;
- target `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`;
- `prerelease: false`;
- `immutable: false`;
- `updated_at: 2026-08-05T18:41:37Z`.

Its seven advertised asset identities are unchanged:

| Asset | Asset ID | Size | Advertised SHA-256 |
|---|---:|---:|---|
| `latest.json` | `502961048` | 820 | `65af98a9541d109df58679bf8ecab633f8744b4ccb6fea8308d15cb33540bac0` |
| `prime-agent-0.7.0.tgz` | `502961047` | 9,323,789 | `88b6578518c72cd51a825bc80f28e0fef9a64c67de4a7d6fd7afd7ca1b34da0b` |
| `prime-agent-ai-0.7.0.tgz` | `502961049` | 533,591 | `7cdbb3e835f48dd103325f7a351ce540b27af4d161aeb9c7b9bdcc12fe7909af` |
| `prime-agent-core-0.7.0.tgz` | `502961050` | 62,815 | `0313373089831d9a2ce06e874fab8b9c05762c0094ff9fc202908cf7db7f99cd` |
| `prime-agent-tui-0.7.0.tgz` | `502961057` | 444,299 | `3225f7f92e87db80fe2c9005d1f7770735ae625c32935ef2283688fc9bd33951` |
| `SHA256SUMS` | `502961051` | 364 | `424d629dc97dfe07a7fc5806c2698bf7eb1d1d49e249159792073aad83a5abd7` |
| `stable` | `502961058` | 7 | `22d24eb4aeab009537ebbd099e54562d35ce546add330e4cdecd28ede260c83c` |

These remain mutable server-advertised expectations only. The revised plan correctly assigns metadata capture to G4, acquisition and independent hashing to G5, and runtime reconciliation to G6.

## Excluded beta refresh

[Beta release ID `355959266`](https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/355959266) remains:

- tag `beta`;
- name `Beta (v0.7.0-beta.460.1.b9a4461)`;
- target `b9a4461149419156599d60174dddf15458e2b9ee`;
- `prerelease: true`;
- `immutable: false`;
- `updated_at: 2026-08-07T02:42:30Z`.

The revised plan excludes this release ID, commit, channel, and its assets globally, with explicit rejection in G2, G4–G6, G13, and G14; G7 and later tasks inherit only the authorized stable inputs from their closed dependencies. No evidence authorizes a baseline change.

## Mutable-source refresh ledger

All rows were retrieved `2026-08-07`.

| ID | Current source identity and observed fact | Drift classification | Revised-plan control |
|---|---|---|---|
| M1 | Stable release ID `365741496` and its seven asset IDs, sizes, and advertised digests remain as recorded above. | No new stable-release metadata drift. | G4 records; G5 independently hashes; G6 reconciles. |
| M2 | Beta release ID `355959266` still targets `b9a4461…` and remains a mutable prerelease. | No new beta-object drift; exclusion remains mandatory. | Global exclusion in the baseline, acceptance criteria, and stop conditions; explicit task rejection in G2, G4–G6, G13, and G14; G7 and later tasks inherit only authorized stable inputs from closed dependencies. |
| M3 | Exact public npm version endpoints for `@earendil-works/pi-coding-agent`, `pi-ai`, `pi-agent-core`, and `pi-tui` at `0.7.0` each returned HTTP 404. | Public exact-version metadata remains unavailable. A 404 does not establish absence from private registries or identify equivalent bytes. | G4 may use only exact approved sources; G5 cannot infer bytes from names; G6 closes the actual acquired graph. |
| M4 | `https://app.primeintellect.ai/install.sh` now serves a branded 404 representation rather than the previously observed installer script. | **Changed mutable endpoint.** The prior lower installer preflight floor is historical, not current endpoint evidence. | No replan required: the installer is prohibited in G4, G5, and G13; the immutable root manifest independently controls Node `>=22.8.0`. |
| M5 | Native-Windows issues [#660](https://github.com/PrimeIntellect-ai/prime-agent/issues/660) and [#665](https://github.com/PrimeIntellect-ai/prime-agent/issues/665) remain open. No first-party source establishes WSL2 compatibility. | Platform gap unchanged. | G1 inventories capabilities; G2 selects the target; G13 measures Linux/WSL behavior; G14 owns qualification. |
| M6 | `earendil-works/pi` remains public. Mutable `main` advanced during refresh and was last observed at `4bf1bba203c699a0b79da669b084052c72b7a35a`, tree `134eda145611f258c262a16ec86a2ba01f5a4ec3`, dated `2026-08-07T10:32:20Z`; parent `958c13f25080b59d4b736193f972a8502a7a2f8b`. | Continuing moving-head drift; not fork-base evidence. | G7 must use immutable history and G5/G6 bytes. The revised plan expressly forbids treating mutable `main` as provenance proof. |
| M7 | [Prime Inference Overview](https://docs.primeintellect.ai/inference/overview) still states model-specific input/output token billing while public detailed rates are deferred to model data/API. | Required Prime model rates remain unresolved if Prime Inference is selected. | G2 selects a candidate class; G7 closes the selected service/account; G15 pins executable rates; G18 enforces the approved ceiling. |
| M8 | [Hosted Evaluations](https://docs.primeintellect.ai/tutorials-environments/hosted-evaluations) still requires publishing/access/authentication and configured billing. Default Prime Inference and custom-endpoint billing paths remain distinct. | No sequencing-changing drift. | Prime-hosted products remain optional and disabled unless explicitly selected and closed by G2/G7/G15. |
| M9 | [Sandboxes Overview](https://docs.primeintellect.ai/sandboxes/overview) still displays `$0.05/core-hour`, `$0.01/GB-memory-hour`, and `$0.001/GB-disk-hour`; GPU sandboxes remain non-core. | Displayed sandbox rates revalidated. | Docker/Prime sandbox is excluded from the selected core path unless separately selected; no G0 ceiling depends on it. |
| M10 | [Hosted-training Models & Pricing](https://docs.primeintellect.ai/hosted-training/models-and-pricing) has materially changed model inventory, including newer Qwen 3.5/3.6 entries and revised catalog content. | Material optional-service catalog drift. | No replan required because hosted training is not enabled by the campaign. If enabled later, G2/G7/G15 must bind the exact profile. |
| M11 | [GPU availability](https://docs.primeintellect.ai/cli-reference/check-gpu-availability) and [disk management](https://docs.primeintellect.ai/cli-reference/managing-disks) expose mutable live/example availability and rates rather than an immutable quote. | Live-rate evidence remains unsuitable as a campaign quote. | No GPU job is planned. G15 must retrieve and pin any selected executable rate; G18 cannot substitute live data. |
| M12 | `https://openai.com/api/pricing/` currently resolves to business-plan content rather than a complete API model-rate table. [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol) separately displays `$5.00/M` input, `$0.50/M` cached input, and `$30.00/M` output. | Provider pricing route/content mismatch; exact model page remains available. | P8 examples are not campaign quotes. G2 selects; G7 closes; G15 pins the exact model/rate source and date; G18 enforces it. |
| M13 | [Anthropic pricing](https://www.anthropic.com/pricing) currently foregrounds consumer/product plans and is not sufficient by itself to pin API execution rates. | Source-purpose mismatch; no executable Anthropic quote established. | Same G2/G7/G15/G18 ownership. No provider has yet been selected. |
| M14 | [npm terms](https://docs.npmjs.com/policies/open-source-terms) still display `2022-03-10`; [GitHub Terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) remain effective `2026-04-27`; [Prime Terms](https://www.primeintellect.ai/terms-of-service) and [Privacy](https://www.primeintellect.ai/privacy-policy) display `2024-02-23`; OpenAI’s Services Agreement remains effective `2026-01-01`; [Linear Terms](https://linear.app/terms) display `2026-06-09`; Linear Privacy displays `2025-03-17`. | No observed displayed-date drift among these dated sources. They remain mutable and do not close an unselected service profile. | G7 retains exact legal objects, dates, account class, data-use, privacy, retention, and disabled-edge proof. No legal conclusion is made here. |
| M15 | Anthropic Commercial Terms and Privacy and OpenAI privacy pages remain publicly readable but expose no stable content digest or fixed page-version identity in the fetched representation. | Mutable-page identity limitation persists. | G7 must preserve URL, retrieval date, displayed identity where present, and quoted technical fields for any enabled service. |
| M16 | Notion’s terms hub now resolves publicly; its privacy page states an effective date of `2025-04-10`. Current Notion MCP documentation identifies the remote MCP endpoint and workspace read/write capability, but technical documentation does not supply an exact closed MCP service profile. | Access improved relative to the prior failed route; service-profile gap remains. | Notion stays disabled. Enabling it would require separate G7 review and must make the G7 RED fixture fail until complete. |

### Exact npm 404 identities

- `https://registry.npmjs.org/@earendil-works%2fpi-coding-agent/0.7.0`
- `https://registry.npmjs.org/@earendil-works%2fpi-ai/0.7.0`
- `https://registry.npmjs.org/@earendil-works%2fpi-agent-core/0.7.0`
- `https://registry.npmjs.org/@earendil-works%2fpi-tui/0.7.0`

These failures are recorded source outcomes, not package-absence, rights, or provenance conclusions.

## Reconciliation against the prior G0 requirements

| Prior required correction | Revised-plan evidence | Result |
|---|---|---|
| Preserve stable `v0.7.0`, commit, and tree | Authorized baseline, acceptance criteria, stop conditions, G2, G4, G6, G13, and G14 preserve `be9e2fa…` / `0625a8f…`. | Reconciled |
| Exclude beta ID `355959266` and commit `b9a4461…` | Explicit plan-level exclusion plus task-specific rejection and stop conditions. | Reconciled |
| Separate metadata, acquisition, and runtime closure | G4 is metadata/manifest only; G5 acquires and independently hashes; G6 reconciles the runtime graph. | Reconciled |
| Record stable asset IDs, URLs, sizes, and advertised digests | G4 contains all seven current stable assets and their exact fields. | Reconciled |
| Preserve Node `>=22.8.0` | G4, G6, G13, and G14 use the immutable manifest floor. Installer execution is prohibited. | Reconciled |
| Assign provider/account/model and rates correctly | G2 selects the candidate; G7 closes service/account/rights; G15 pins executable identity and rates; G18 enforces exact approved ceilings. G9–G11 expressly do not own selection. | Reconciled |
| Put runtime measurement in G13 and judgment in G14 | G13 requires measured Linux/WSL evidence; G14 issues the qualification result. | Reconciled |
| Keep rights, service, provenance, and credential boundaries in G7 | G3 is provisioning only; G7 owns the complete closure matrix. | Reconciled |
| Split provisioning and acquisition approvals | Approval checkpoint after G2 precedes G3; separate endpoint/byte/storage approval after G4 precedes G5. | Reconciled |
| Keep Notion disabled | Acceptance criteria, G7, and stop conditions retain disabled-by-construction treatment. | Reconciled |
| Preserve unresolved launch revision and Pi-fork provenance | Baseline section, G6, G7, G14, and G20 prohibit inference of either unresolved binding. | Reconciled |
| Block G1 until a successful G0 rerun | Plan status, serial order, G0 exit gate, G1 dependency, and stop conditions all enforce it. | Reconciled |

The newly observed installer 404, moving upstream head, hosted-training catalog change, and provider-pricing route mismatch do not invalidate the revised serial sequence. Each affected source is either excluded from execution or assigned to a later gate that must bind exact current evidence before use. None changes the immutable stable baseline or authorizes a fallback.

## Complete G0–G20 ownership and RED map

| Gate | Revised-plan ownership | Required RED or negative condition |
|---|---|---|
| G0 | Refresh evidence and reconcile the plan before host work. | Missing date/current identity, silently unchanged drift, or misassigned G2/G4–G7/G13–G15/G18 ownership fails. |
| G1 | Capture judgment-free host and guest-capability inventory. | Missing OS, WSL, termination, disk, Pi, or GPU fields—or recording only an exit code—fails. |
| G2 | Select one guest target, minimal profile, and candidate provider/account/model class. | Merged platforms, no external termination, omitted P2 edge, unenforceable disabled edge, absent provider class, or beta ingress fails. |
| G3 | Provision only the approved dedicated Linux guest. | Host automount/interop enabled, Vordar visible, or no external termination boundary fails. |
| G4 | Produce the immutable acquisition/resolution manifest without acquisition. | `latest`, a range, missing asset metadata, undeclared source/subprocess, beta identity, or Node below `22.8.0` fails. |
| G5 | Acquire only approved objects into quarantine and hash independently. | A changed object, unexpected endpoint/object/identity/size/hash, lifecycle script, installer, PRIME entrypoint, or beta object fails. |
| G6 | Reconcile the complete runtime graph and two offline reconstructions. | Missing transitive, altered byte/mode, undeclared file, beta substitution, lower Node floor, network use, or unequal reconstruction fails. |
| G7 | Close rights, service, provenance, account, privacy, retention, and credential boundaries. | Missing node/legal object/provenance/date/data/account/credential field, unresolved enabled edge, or enabled Notion profile fails. |
| G8 | Specify the Pi/PRIME isolation contract. | Any boundary without an attack probe, observable denial, retained evidence, and rollback fails. |
| G9 | Implement an independent isolation verifier. | Host mount, readable Pi path, shared temp, inherited `PI_*`, denied-egress escape, secret leakage, escaped child, visible GPU, or heavy-job overlap must be red. |
| G10 | Implement only G8’s isolation mechanism. | The permissive pre-policy guest must be red under G9; importing implementation code into G9 or leaving a boundary open fails. |
| G11 | Execute isolation probes and retain raw evidence. | Mutated path, egress, process, state, or GPU evidence must turn G9 red; intact evidence must remain green. |
| G12 | Judge isolation evidence against G8 and prior findings. | A denial without both broken-red and intact-green evidence, or changed Pi state hashes, fails. |
| G13 | Install G6 bytes offline and run measured platform smoke checks. | Altered staged object, Node below floor, unexpected network success, inferred platform behavior, source patch, beta byte, or WSL/kernel failure fails. |
| G14 | Judge exact runtime and selected-platform qualification. | Installed-tree mismatch, first-use acquisition, low Node, inferred rather than observed behavior, beta presence, or exit-code-only evidence fails. |
| G15 | Define the exact executable recovery matrix and cost profile. | Any case missing producer/bytes/consumer/check/disposition/retry/mutation, or any missing provider/model/account/rate/date/run/call/token field, fails. |
| G16 | Implement an independent recovery verifier. | Missing disposition, changed consumed byte, unreconciled provider result, duplicate effect, unsafe retry, wrong order, silent corrupt success, mixed state, orphan, open egress, GPU overlap, provider substitution, or ceiling overrun must be red. |
| G17 | Implement the external recovery/fault harness. | Incomplete producer output, provider substitution, or over-ceiling output must be rejected by G16; shared verifier modules fail independence. |
| G18 | Execute all 21 cases under the exact approved profile and ceilings. | Registered mutations, provider substitution, or one-unit overrun must be refused and red; silence or unsafe replay fails. |
| G19 | Judge recovery, coexistence, and contention evidence. | Missing case, green mutation, consumer/hash mismatch, silent request, changed Pi bytes, inferred restart order, unenforced profile/ceiling, or accepted GPU overlap fails. |
| G20 | Recheck only P10’s in-scope gates. | A closed row without its passing judgment, raw index, red proof, green proof, and dependency chain fails; out-of-scope rows cannot be omitted. |

## G0 RED fixtures

Every freshness record must contain:

`claim_id`, `prior_retrieved_at`, `current_retrieved_at`, `prior_identity`, `current_identity`, `prior_value`, `current_value`, `drift`, `downstream_control`, and `impact`.

### Fixture A — missing current identity

```yaml
claim_id: installer-endpoint
prior_retrieved_at: 2026-08-07
current_retrieved_at:
prior_identity: https://app.primeintellect.ai/install.sh; installer script
current_identity:
prior_value: executable installer body
current_value:
drift: NONE
downstream_control: G5
impact: NONE
```

**Expected RED:** reject missing retrieval date and identity; the source cannot be classified.

### Fixture B — changed endpoint called unchanged

```yaml
claim_id: installer-endpoint
prior_retrieved_at: 2026-08-07
current_retrieved_at: 2026-08-07
prior_identity: https://app.primeintellect.ai/install.sh; installer script
current_identity: https://app.primeintellect.ai/install.sh; branded 404 representation
prior_value: script with mutable runtime preflight
current_value: installer body unavailable at route
drift: NONE
downstream_control: G5 prohibits installer execution
impact: NONE
```

**Expected RED:** reject `drift: NONE`; the representation changed even though the stronger downstream exclusion means no replan is needed.

### Fixture C — unauthorized beta substitution

```yaml
claim_id: authorized-release
prior_retrieved_at: 2026-08-07
current_retrieved_at: 2026-08-07
prior_identity: stable release 365741496
current_identity: beta release 355959266
prior_value: be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387
current_value: b9a4461149419156599d60174dddf15458e2b9ee
drift: ACCEPTED
downstream_control: G4
impact: baseline updated
```

**Expected RED:** reject the unauthorized channel, baseline change, and beta ingress before G1.

## Assumptions and residual risks

- Public 404 responses establish only the current public endpoint result, not universal package or artifact absence.
- Mutable pages can change after retrieval; the plan’s dispatch-time evidence refresh remains necessary.
- Provider, account, model, and rate identities remain deliberately unselected. G15 cannot proceed without a current executable rate source.
- WSL2 compatibility remains unknown until G13 measurement and G14 review.
- Pi-fork provenance and the exact launch-revision binding remain unresolved blocking gates.
- This finding makes no legal, licensing, adoption, purchasing, platform-qualification, or service-acceptance decision.

## G1 dispatch decision

G1 may proceed because the revised plan now reconciles the prior G0 requirements and the new mutable-source drift is either excluded or owned by a later fail-closed gate. Dispatch still requires the explicit user approval for read-only host probing specified by G1, and G1 must perform no setup or mutation.

**Verdict:** `FRESH`
