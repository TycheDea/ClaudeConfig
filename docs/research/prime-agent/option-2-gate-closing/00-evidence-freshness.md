# G0 — Evidence Freshness and Scope Reconciliation

## Run record

- **Previous evidence snapshot:** `2026-08-06`
- **Refresh date:** `2026-08-07`
- **Method:** public, unauthenticated, read-only HTTP retrieval only. No downloads, execution, installation, accounts, credentials, purchases, host probes, or repository changes.
- **Identity rule:** commit, tree, and Git-blob SHAs are immutable evidence. Tags, release objects, installer endpoints, documentation, policies, package-registry metadata, and pricing pages are mutable even when they currently advertise digests.
- **Mutable-page limitation:** where the public response exposes no content hash, identity is the exact URL, retrieval date, page title or effective date, and the quoted decision-bearing fact.
- **Comparison basis:** the Phase-1 findings, especially `01-identity-source-lock.md`, `03-license-weights-service-closure.md`, `07-platform-gpu-vram.md`, and `08-pricing-operations.md`, against the current public sources.
- The previous source-access failure is cleared for the decision-bearing repository, release, platform, service, policy, and provider-pricing sources. Some optional mutable sources remain incomplete as recorded below.

## Authorized baseline lock

The authorized baseline does not change:

| Field | Current identity | Evidence class |
|---|---|---|
| Repository | `PrimeIntellect-ai/prime-agent`, repository ID `1232493406`; organization display name `Prime Intellect` | Mutable repository metadata, retrieved `2026-08-07` |
| Version | `v0.7.0` | Mutable tag/release name |
| Commit | `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387` | Immutable commit identity |
| Tree | `0625a8fd0550a8de7ff05e8d9248e75563e5b520` | Immutable tree identity |
| Baseline license blob | `e15dcd837b11cfb1f627e388561f3ea6405097c1` | Immutable Git-blob identity |

Current lightweight tag targets are:

- `v0.6.0` → `7db7b69c60be0f7b271faf948864891813b27182`
- `v0.6.1` → `8bd7c18f16bfdc356c1cd20fb9fcf01119147cda`
- `v0.7.0` → `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`

The stable release object remains release ID `365741496`, published `2026-08-05T18:41:37Z`, targeting the authorized commit. Its `immutable` field is `false`; therefore the release object and tag remain mutable references, not substitutes for the commit/tree lock.

The unresolved launch-revision binding identified in `01-identity-source-lock.md` remains unresolved. Neither the stable release record nor the beta channel proves that the authorized baseline is the exact launch revision.

## Freshness and drift ledger

| ID | Domain and prior state (`2026-08-06`) | Current evidence (`2026-08-07`) | Drift classification | Downstream control and impact |
|---|---|---|---|---|
| R1 | **Stable release:** `v0.7.0` targeted the authorized commit. The release API supplied an asset inventory but no recorded content digests. | [Release list](https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases) still places stable `v0.7.0` at commit `be9e2fa…`. The same release object now exposes SHA-256 digests for every stable asset. | **Metadata drift; no stable-code drift.** Server-advertised asset digests are newly available relative to P1. | Baseline remains unchanged. Reconcile the G4 acquisition manifest to asset ID, URL, advertised digest, retrieval date, and expected size. G5 must independently compute post-acquisition SHA-256; mutable release metadata is not the byte check itself. G6 must reconcile the verified objects to the authorized release assets. **Material inventory impact.** |
| R2 | **Prerelease channel:** beta/build references were excluded from the authorized baseline; no post-snapshot beta identity was recorded. | Mutable release ID `355959266`, tag `beta`, is now titled `Beta (v0.7.0-beta.460.1.b9a4461)` and targets `b9a4461149419156599d60174dddf15458e2b9ee`. It is `prerelease: true`, `immutable: false`, created `2026-08-07T02:40:56Z`, updated `2026-08-07T02:42:30Z`, while retaining an older `published_at` date. The current ordered release list shows this beta object first and stable `v0.7.0` second; beta is the displayed object with post-snapshot creation/update timestamps. | **Material mutable-channel drift.** This is a beta build/channel mutation, not proof of a newly published stable version and not an authorized upgrade. | The beta identity must not be selected by G2, admitted to the G4 manifest or G5 object store, accepted by G6 or G7, installed by G13, or qualified by G14. Later tasks inherit the authorized stable baseline. The plan requires a checkpoint rather than silent baseline adaptation. **Blocking.** |
| R3 | **Packages:** exact acquired-package hashes were absent. Source package names and release assets were known only incompletely. | Commit-pinned manifests now establish exact source identities listed below. Exact public npm registry lookups for all four scoped packages at `0.7.0` returned HTTP `404 Not Found`; GitHub release assets remain the public package source evidenced for this version. | **Evidence closure plus package-source clarification.** Registry publication is not established; the stable release assets now have advertised digests. | G4 must manifest only the approved stable release assets and exact resolution inputs. G5 must acquire those manifested objects and must never infer equivalent bytes from a package name or mutable installer. A registry 404 does not prove absence from private registries and is not a G7 license or service verdict. **Material G4/G5/G7 impact.** |
| R4 | **Installer/platform:** P7 required Node `>=22.8.0`, treated WSL2 as unproved until execution, and documented native-Windows defects. | Mutable [installer](https://app.primeintellect.ai/install.sh) currently defaults to channel `stable` and R2 base `https://pub-728493de92a943e2a9b2d17b4719f318.r2.dev`. Its preflight checks `20.6.0`, while the immutable baseline root manifest requires Node `>=22.8.0`. Native-Windows issues [#660](https://github.com/PrimeIntellect-ai/prime-agent/issues/660) and [#665](https://github.com/PrimeIntellect-ai/prime-agent/issues/665) remain open. No direct source proving WSL2 support was found. | **No platform closure; mutable installer/package-floor mismatch persists.** No evidence supports extending native-Windows reports to WSL2. | Preserve the stricter baseline Node floor in G4’s runtime inputs and G6’s byte closure. G5 must not execute the mutable installer. G13 remains responsible for actual Linux/WSL runtime execution and platform smoke evidence; G14 owns the resulting runtime/platform verdict. **No baseline change, but platform risk remains open.** |
| R5 | **License/upstream:** baseline was MIT; the exact upstream fork base and retained/dropped path provenance were unresolved. | Baseline LICENSE remains Git blob `e15dcd…`. The transferred upstream route `badlogic/pi-mono` resolves to `earendil-works/pi`; current mutable `main` is `709aa03194301afd008a07d64ff1bf12e4f7ece6`, dated `2026-08-07T09:27:41Z`, and current upstream LICENSE is blob `b0a8e9b81083294360c69b4ec45d3d39a2b28197`. This moving head does not identify PRIME’s fork base. | **Moving-reference and ownership-route clarification; provenance gap unchanged.** | G7 must derive provenance from immutable history and G5/G6 acquired-byte evidence, not current upstream `main`. No legal conclusion follows from matching license labels alone. **G7 remains blocking.** |
| R6 | **Prime services and prices:** Prime Inference documented token billing without public per-model rates; sandbox rates were mutable; hosted execution needed explicit cost attribution. | [Inference Overview](https://docs.primeintellect.ai/inference/overview) still says input/output tokens are billed by model but that detailed rates will be provided later and through the models endpoint. Hosted evaluations state that default Prime Inference does not separately bill sandbox runtime, while a custom endpoint incurs Prime sandbox compute plus external-provider token charges. [Sandboxes Overview](https://docs.primeintellect.ai/sandboxes/overview) currently states `$0.05/core-hour`, `$0.01/GB-memory-hour`, and `$0.001/GB-disk-hour`; GPU sandboxes remain roadmap-only. A dedicated pricing URL no longer yielded the complete readable table, but the overview did. A static current GPU availability/rate table was not recoverable through the permitted read-only fetch. | **Rates unchanged where revalidated; source-location/rendering drift and unresolved Prime model/GPU rates.** | Replan G2’s candidate provider/account/model class, G7’s enabled-service and account-class closure, and G15’s executable recovery profile so the selected provider/model, rate source, retrieval date, and call/token assumptions are pinned before execution. G18’s approval packet must state the final exact dollar ceiling. Do not reuse P8 GPU examples or infer Prime model rates. **Material pricing-source impact.** |
| R7 | **Provider prices:** P8 used GPT-5.2 and Claude 4.x examples to exercise the cost formulas. | [OpenAI pricing](https://openai.com/api/pricing/) now foregrounds GPT-5.6: Sol short-context input/cached-input/cache-write/output is `$5.00/$0.50/$6.25/$30.00` per million tokens; Terra is `$2.00/$0.20/$2.50/$12.00`; Luna is `$0.20/$0.02/$0.25/$1.20`. [Anthropic pricing](https://www.anthropic.com/pricing) now lists Fable 5 at `$10/$50`, Opus 5 at `$5/$25`, Sonnet 5 at introductory `$2/$10` through `2026-08-31` and `$3/$15` thereafter, and Haiku 4.5 at `$1/$5` per million input/output tokens. | **Material model-catalog and pricing drift.** Some tier rates are unchanged, but identities, current defaults, cache charges, long-context treatment, and temporary pricing differ from P8’s examples. | P8 formulas remain usable, but its model examples are not current campaign quotes. G2 must select the candidate provider/account/model class; G7 must close the selected service, terms, account, and rights profile; G15 must pin the exact executable provider/model/rate profile and its retrieval date for the recovery matrix. G18 must enforce the approved exact execution ceiling without substitution. Provider selection and pricing do not belong to the G9 isolation verifier, G10 isolation implementation, or G11 isolation execution. **Blocking plan/inventory drift.** |
| R8 | **Legal/service/privacy:** P3 recorded mutable service terms and privacy sources, with Notion’s exact MCP profile unresolved. | Current dated identities include: npm Open-Source Terms last updated `2022-03-10`; GitHub Terms effective `2026-04-27`; Prime Terms and Privacy updated `2024-02-23`; OpenAI Services Agreement effective `2026-01-01`; Linear Terms effective `2026-06-09`; Linear Privacy effective `2025-03-17`. Anthropic Commercial Terms and Privacy pages were readable but exposed no stable content hash or explicit fixed page-version identifier in the fetched body. OpenAI’s fetched privacy page likewise exposed no fixed page-version identity. Notion’s prior MCP terms URL returned “page couldn’t be found”; its general terms URL redirects to the external terms hub and its privacy route did not expose the needed MCP-specific profile. | **No observed date drift among sources with displayed dates; mutable-page identity limits and Notion gap persist.** | G7 must retain URL, retrieval date, displayed effective/update date, and quoted technical data-handling facts for every enabled service edge. Keep optional Notion integration disabled unless its exact service profile is reviewed. G3 is dedicated guest provisioning and does not own rights or service closure. This ledger is technical provenance, not legal advice or a license/service verdict. |
| R9 | **Launch and scope reconciliation:** P1/P10 could not bind the launch revision or close all installation, provenance, service, and price gates. | Stable commit/tree identity is unchanged, but the beta mutation, newly exposed stable asset digests, package-source clarification, and provider catalog/rate changes alter the evidence inventory used by acquisition and provider-dependent tasks. | **Material plan/inventory drift.** | Preserve the authorized baseline and scope, but reconcile the plan’s G4 manifest, G5 acquisition controls, G2/G7/G15 provider profile and rate controls, and G18 execution ceiling before dispatching G1. **Blocking.** |

## Exact baseline package identities

These are immutable Git-blob identities at the authorized commit, not npm-registry publication evidence:

| Source package | Version/state | Git blob |
|---|---|---|
| Root `prime-agent` monorepo | `0.7.0`, private | `0794d88d295f935bcf3ef2e5a7bafc110160eb51` |
| `@earendil-works/pi-coding-agent` | `0.7.0` | `b498e5b9e1a0642d6ec99912046ea71cdf605f8c` |
| `@earendil-works/pi-ai` | `0.7.0` | `555069c83ec41c9802e1f9ac3effd43df5480bb4` |
| `@earendil-works/pi-agent-core` | `0.7.0` | `ac3b56f1d74f94ea3889db1bab2bf51a74f7a6c8` |
| `@earendil-works/pi-tui` | `0.7.0` | `fc79d23d6fe9db7114b7ed75ea03d16e0a2bfbeb` |

Exact public npm lookups returning HTTP 404 on `2026-08-07`:

- `https://registry.npmjs.org/@earendil-works%2fpi-coding-agent/0.7.0`
- `https://registry.npmjs.org/@earendil-works%2fpi-ai/0.7.0`
- `https://registry.npmjs.org/@earendil-works%2fpi-agent-core/0.7.0`
- `https://registry.npmjs.org/@earendil-works%2fpi-tui/0.7.0`

## Stable release asset identities

The mutable stable release record currently advertises:

| Asset | Asset ID | Size | Advertised SHA-256 |
|---|---:|---:|---|
| `latest.json` | `502961048` | 820 | `65af98a9541d109df58679bf8ecab633f8744b4ccb6fea8308d15cb33540bac0` |
| `prime-agent-0.7.0.tgz` | `502961047` | 9,323,789 | `88b6578518c72cd51a825bc80f28e0fef9a64c67de4a7d6fd7afd7ca1b34da0b` |
| `prime-agent-ai-0.7.0.tgz` | `502961049` | 533,591 | `7cdbb3e835f48dd103325f7a351ce540b27af4d161aeb9c7b9bdcc12fe7909af` |
| `prime-agent-core-0.7.0.tgz` | `502961050` | 62,815 | `0313373089831d9a2ce06e874fab8b9c05762c0094ff9fc202908cf7db7f99cd` |
| `prime-agent-tui-0.7.0.tgz` | `502961057` | 444,299 | `3225f7f92e87db80fe2c9005d1f7770735ae625c32935ef2283688fc9bd33951` |
| `SHA256SUMS` | `502961051` | 364 | `424d629dc97dfe07a7fc5806c2698bf7eb1d1d49e249159792073aad83a5abd7` |
| `stable` | `502961058` | 7 | `22d24eb4aeab009537ebbd099e54562d35ce546add330e4cdecd28ede260c83c` |

These are server-advertised identities only. G4 must record them as expected acquisition identities. G5 must independently hash each acquired object and reject any mismatch against both the pinned manifest and the acquired `SHA256SUMS`; G6 must independently reconcile the verified objects to the authorized runtime graph.

## Required reconciliation before another G0 pass

1. Preserve `v0.7.0` commit/tree as the sole authorized baseline.
2. Update the plan’s **Evidence baseline and freshness** section to record the `2026-08-07` refresh, release ID `355959266`, and commit `b9a4461…` as explicitly excluded beta-channel drift rather than continuing to describe all mutable evidence as last retrieved on `2026-08-06`.
3. Update G4’s planned source manifest to include stable asset IDs, URLs, sizes, and advertised SHA-256 values. Keep G4 manifest-only: acquisition occurs in G5, where independent byte hashing is the actual gate; G6 owns runtime-byte reconciliation.
4. Reconcile the plan’s provider-dependent controls: G2 selects the candidate provider/account/model class; G7 closes its rights, service, account, privacy, retention, and credential-boundary profile; G15 pins the exact provider/model/rate profile, retrieval date, run count, and call/token assumptions; G18’s approval packet states and enforces the exact dollar ceiling. Remove reliance on P8’s GPT-5.2 and Claude 4.x examples as current quotes. Do not assign this work to G9, G10, or G11.
5. Preserve the stricter Node `>=22.8.0` floor. Keep mutable-installer execution out of G5. Assign observed Linux/WSL runtime behavior to G13 and its qualification verdict to G14.
6. Keep rights, hosted-service terms, provenance, and credential-boundary closure in G7, not G3. Keep Notion disabled and retain the unresolved upstream-base and launch-revision bindings as open gates.
7. Reconcile the plan’s **Serial gate order**, **Approval checkpoints**, G4, and G5 wording so the immutable manifest precedes the displayed acquisition approval and G5 quarantine acquisition. Target/guest approval remains after G2 and before G3.
8. Rerun G0 after those plan and evidence-inventory corrections. Do not dispatch G1 until G0 returns `FRESH`.

## Task-reference mapping audit

| Citation | Actual option-2 task |
|---|---|
| G0 | Refresh the evidence and baseline ledger |
| G1 | Capture the judgment-free host and guest-capability inventory; blocked unless G0 is `FRESH` |
| G2 | Select the target and minimal enabled execution profile, including the candidate provider/account/model class |
| G3 | Provision only the dedicated Linux guest boundary; not rights/service closure |
| G4 | Specify the immutable acquisition and resolution manifest; no acquisition |
| G5 | Acquire into quarantine and resolve with scripts disabled |
| G6 | Issue the runtime-byte closure verdict |
| G7 | Close rights, hosted-service terms, provenance, and credential boundaries |
| G9 | Implement the independent isolation verifier; no provider/profile/rate selection |
| G10 | Implement the selected isolation boundary; no provider/profile/rate selection |
| G11 | Execute isolation qualification and retain raw evidence; no provider/profile/rate selection |
| G13 | Install the locked runtime offline and run platform smoke checks, including measured Linux/WSL behavior |
| G14 | Issue the runtime and platform qualification verdict |
| G15 | Define the executable recovery protocol and matrix, including the selected execution profile and exact call/token assumptions |
| G18 | Execute the recovery matrix under the user-approved exact provider-call and dollar ceiling |

## RED-proof fixtures

Each ledger record must contain:

`claim_id`, `prior_retrieved_at`, `current_retrieved_at`, `prior_identity`, `current_identity`, `prior_value`, `current_value`, `drift`, `downstream_control`, and `impact`.

### Fixture A — missing date and identity

```yaml
claim_id: legal-notion-mcp
prior_retrieved_at: 2026-08-06
current_retrieved_at:
prior_identity: prior Notion MCP terms URL
current_identity:
drift: NONE
```

**Expected result:** fail with missing `current_retrieved_at` and `current_identity`; the record cannot support a freshness decision.

### Fixture B — falsely labeled no drift

```yaml
claim_id: provider-price-profile
prior_retrieved_at: 2026-08-06
current_retrieved_at: 2026-08-07
prior_identity: OpenAI GPT-5.2 pricing example
current_identity: OpenAI GPT-5.6 Sol pricing table
prior_value: input=1.75,cached_input=0.175,output=14.00
current_value: input=5.00,cached_input=0.50,cache_write=6.25,output=30.00
drift: NONE
```

**Expected result:** fail because normalized model identity and rate fields differ. A no-drift classification must be impossible when any decision-bearing identity or value changes.

Allowed G0 verdict enum: `FRESH`, `DRIFT REQUIRES REPLAN`, or `SOURCE UNAVAILABLE`.

**Verdict:** `DRIFT REQUIRES REPLAN`

**G1 may proceed:** No.
