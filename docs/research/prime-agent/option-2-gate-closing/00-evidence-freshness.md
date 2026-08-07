# PRIME Agent option 2 evidence-freshness ledger

**Refresh date:** 2026-08-07
**Authorized baseline:** PRIME Agent `v0.7.0`, commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`, tree `0625a8fd0550a8de7ff05e8d9248e75563e5b520`
**Prior retrieval date:** 2026-08-06 unless a row states otherwise
**Scope:** G0 public read-only freshness review only; no bytes, accounts, credentials, host probes, setup, execution, or baseline change

## Retrieval result

The worker had repository-file read access but no network-capable fetch tool. Consequently, no external primary citation could be re-opened on 2026-08-07, no mutable page could receive a current content hash or HTTP identity, and no current release-list query could establish whether a newer PRIME release appeared.

This is an availability failure, not evidence of no drift. Every affected row below is explicitly marked unassessable. Prior preserved facts remain historical observations only and are not promoted to current facts.

## Immutable baseline ledger

Commit-SHA citations are content-addressed and cannot drift while they resolve to the recorded Git object. Their current online availability was not confirmed, but mutable branch or tag state cannot alter their identity.

| Claim | Prior source | Prior retrieval | Current source | Current retrieval | Immutable revision/content identity | Drift | Controlling downstream task | Impact |
|---|---|---:|---|---:|---|---|---|---|
| Authorized source baseline | https://github.com/PrimeIntellect-ai/prime-agent/commit/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387 | 2026-08-06 | Same commit permalink; not re-opened | 2026-08-07 attempted; inaccessible | Commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`; tree `0625a8fd0550a8de7ff05e8d9248e75563e5b520` | Content identity cannot drift; availability unconfirmed | G2, G4, G6, G14, G20 | Baseline identity remains recorded, but current tag/release association is not established. |
| Complete source-tree boundary | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/git/trees/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387?recursive=1 | 2026-08-06 | Same commit-tree endpoint; not re-opened | 2026-08-07 attempted; inaccessible | Tree `0625a8fd0550a8de7ff05e8d9248e75563e5b520`; prior response reported `1281` entries and `truncated:false` | Content identity cannot drift; current availability unconfirmed | G2, G4, G6, G7 | Prior closed-tree enumeration remains tied to the immutable tree, not to current repository state. |
| Source npm lock | https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/package-lock.json | 2026-08-06 | Same blob permalink; not re-opened | 2026-08-07 attempted; inaccessible | Git blob `909fda27b6f2846b4355433dda7f500bb72a5f1b`; lockfile v3; prior count `428` external install paths | Content identity cannot drift | G4, G6, G7 | The source lock remains historical exact-baseline evidence; it still does not close packaged installation bytes. |
| Internal package declarations | Commit-pinned root and `packages/{agent,ai,coding-agent,tui}/package.json` citations in P1–P3 | 2026-08-06 | Same commit-pinned paths; not re-opened | 2026-08-07 attempted; inaccessible | Root `prime-agent@0.7.0`; four internal `@earendil-works/*@0.7.0` declarations under the authorized commit | Content identity cannot drift | G4, G6, G7 | Manifest declarations remain pinned but do not prove registry publication or registry-byte identity. |
| Runtime, persistence, replay, platform, and isolation-relevant behavior | Commit-pinned citations listed in P2, P4, P5, and P7 | 2026-08-06 | Same SHA-pinned citations; not re-opened | 2026-08-07 attempted; inaccessible | All cited paths are under commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387` | Content identity cannot drift | G2, G8–G19 | Prior behavior findings remain exact-baseline findings; no claim is made about newer releases. |
| PRIME source license | https://raw.githubusercontent.com/PrimeIntellect-ai/prime-agent/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/LICENSE | 2026-08-06 | Same SHA-pinned raw object; not re-opened | 2026-08-07 attempted; inaccessible | Commit-pinned MIT text; copyright notices for Mario Zechner and Prime Intellect | Content identity cannot drift | G7 | Covers only the committed source; it does not close release-package notices, provenance, dependencies, models, or services. |

## Mutable release and identity ledger

| Claim | Prior source | Prior retrieval | Current source | Current retrieval | Preserved prior/current identity | Drift | Controlling downstream task | Impact |
|---|---|---:|---|---:|---|---|---|---|
| Product, launch date, and repository link | https://www.primeintellect.ai/blog/prime-agent | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior: displayed `AUG 05TH, 2026`, “Today, we are launching Prime Agent,” and linked `PrimeIntellect-ai/prime-agent`; no prior hash or revision marker. Current identity unavailable. | Unassessable | G0, G20 | Historical launch-to-release binding remains unresolved; page changes cannot be excluded. |
| Publisher organization identity | https://api.github.com/orgs/PrimeIntellect-ai | 2026-08-06 | Same API object; inaccessible | 2026-08-07 attempted | Prior: organization node `O_kgDOCNMXhA`, display name “Prime Intellect,” `updated_at=2026-07-25T19:08:27Z`. Current `updated_at` and body hash unavailable. | Unassessable | G0 | No current ownership-metadata comparison is available. |
| Canonical repository identity/current state | https://api.github.com/repos/PrimeIntellect-ai/prime-agent | 2026-08-06 | Same API object; inaccessible | 2026-08-07 attempted | Prior: repository ID `1232493406`, node `R_kgDOSXZbXg`, `updated_at=2026-08-06T18:31:39Z`, `pushed_at=2026-08-06T18:25:42Z`. Current timestamps/body hash unavailable. | Unassessable | G0, G2 | Repository identity is historically preserved, but current pushes/default-branch state cannot be assessed. |
| `v0.6.0` release metadata | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/365289118 | 2026-08-06 | Same release object; inaccessible | 2026-08-07 attempted | Prior: release ID `365289118`, published/updated `2026-08-05T04:36:20Z`; no preserved response hash. Current identity unavailable. | Unassessable | G0 | Same-day launch ambiguity cannot be refreshed. |
| `v0.6.1` release metadata | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/365606154 | 2026-08-06 | Same release object; inaccessible | 2026-08-07 attempted | Prior: release ID `365606154`, published/updated `2026-08-05T14:55:26Z`; no preserved response hash. Current identity unavailable. | Unassessable | G0 | Same-day launch ambiguity cannot be refreshed. |
| Authorized `v0.7.0` release metadata and asset list | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/365741496 | 2026-08-06 | Same release object; inaccessible | 2026-08-07 attempted | Prior: release ID `365741496`, `immutable:false`, published/updated `2026-08-05T18:41:37Z`; current body and asset-array identity unavailable. | Unassessable | G0, G4, G5, G6 | Current asset deletion, replacement, renaming, digest change, or metadata change cannot be excluded. Acquisition must not begin. |
| `v0.6.0` lightweight tag | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/git/refs/tags/v0.6.0 | 2026-08-06 | Same ref endpoint; inaccessible | 2026-08-07 attempted | Prior target `7db7b69c60be0f7b271faf948864891813b27182`; current ref target unavailable. | Unassessable | G0 | Current mutable ref cannot be treated as unchanged. |
| `v0.6.1` lightweight tag | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/git/refs/tags/v0.6.1 | 2026-08-06 | Same ref endpoint; inaccessible | 2026-08-07 attempted | Prior target `8bd7c18f16bfdc356c1cd20fb9fcf01119147cda`; current ref target unavailable. | Unassessable | G0 | Current mutable ref cannot be treated as unchanged. |
| Authorized `v0.7.0` lightweight tag | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/git/refs/tags/v0.7.0 | 2026-08-06 | Same ref endpoint; inaccessible | 2026-08-07 attempted | Prior target `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`; current ref target unavailable. | Unassessable | G0, G4, G6 | The recorded commit remains authoritative, but tag movement cannot be ruled out. |
| Whether a newer PRIME release exists | No prior complete release-list identity was preserved | Not established | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases?per_page=100 | 2026-08-07 attempted; inaccessible | No current release-list body, newest release ID/tag, `ETag`, `updated_at`, or body hash available | Unassessable | G0, G2 | The campaign cannot prove that source drift did not introduce a newer release requiring a user checkpoint. |

### Preserved `v0.7.0` asset observations

These are prior GitHub API observations, not acquired bytes and not current release-object facts.

| Asset ID | Prior name | Prior size | Prior API-reported digest | Current identity |
|---:|---|---:|---|---|
| `502961048` | `latest.json` | 820 B | `sha256:65af98a9541d109df58679bf8ecab633f8744b4ccb6fea8308d15cb33540bac0` | Unavailable |
| `502961047` | `prime-agent-0.7.0.tgz` | 9,323,789 B | `sha256:88b6578518c72cd51a825bc80f28e0fef9a64c67de4a7d6fd7afd7ca1b34da0b` | Unavailable |
| `502961049` | `prime-agent-ai-0.7.0.tgz` | 533,591 B | `sha256:7cdbb3e835f48dd103325f7a351ce540b27af4d161aeb9c7b9bdcc12fe7909af` | Unavailable |
| `502961050` | `prime-agent-core-0.7.0.tgz` | 62,815 B | `sha256:0313373089831d9a2ce06e874fab8b9c05762c0094ff9fc202908cf7db7f99cd` | Unavailable |
| `502961057` | `prime-agent-tui-0.7.0.tgz` | 444,299 B | `sha256:3225f7f92e87db80fe2c9005d1f7770735ae625c32935ef2283688fc9bd33951` | Unavailable |
| `502961051` | `SHA256SUMS` | 364 B | `sha256:424d629dc97dfe07a7fc5806c2698bf7eb1d1d49e249159792073aad83a5abd7` | Unavailable |
| `502961058` | `stable` | 7 B | `sha256:22d24eb4aeab009537ebbd099e54562d35ce546add330e4cdecd28ede260c83c` | Unavailable |

The four prior tarball sizes total `10,364,494` bytes. That remains a historical public-byte floor, not a current download or storage estimate.

## Mutable package and provenance ledger

| Claim | Prior source | Prior retrieval | Current source | Current retrieval | Preserved prior/current identity | Drift | Controlling downstream task | Impact |
|---|---|---:|---|---:|---|---|---|---|
| Registry identity for `@earendil-works/pi-coding-agent@0.7.0` | No registry object was bound in P1–P3; only the commit-pinned manifest was observed | 2026-08-06 gap | https://registry.npmjs.org/@earendil-works%2Fpi-coding-agent/0.7.0 | 2026-08-07 attempted; inaccessible | Prior immutable declaration exists; registry version, dist integrity, tarball URL, publication time, deprecation state, and response hash unavailable | Unassessable | G4, G6, G7 | Registry publication and byte identity remain unknown. |
| Registry identity for `@earendil-works/pi-agent-core@0.7.0` | No registry object previously bound | 2026-08-06 gap | https://registry.npmjs.org/@earendil-works%2Fpi-agent-core/0.7.0 | 2026-08-07 attempted; inaccessible | Current package metadata/content identity unavailable | Unassessable | G4, G6, G7 | Cannot bind source declaration to registry bytes. |
| Registry identity for `@earendil-works/pi-ai@0.7.0` | No registry object previously bound | 2026-08-06 gap | https://registry.npmjs.org/@earendil-works%2Fpi-ai/0.7.0 | 2026-08-07 attempted; inaccessible | Current package metadata/content identity unavailable | Unassessable | G4, G6, G7 | Cannot bind source declaration to registry bytes. |
| Registry identity for `@earendil-works/pi-tui@0.7.0` | No registry object previously bound | 2026-08-06 gap | https://registry.npmjs.org/@earendil-works%2Fpi-tui/0.7.0 | 2026-08-07 attempted; inaccessible | Current package metadata/content identity unavailable | Unassessable | G4, G6, G7 | Cannot bind source declaration to registry bytes. |
| Current upstream pi license comparison | https://raw.githubusercontent.com/badlogic/pi-mono/main/LICENSE | 2026-08-06 | Same mutable branch path; inaccessible | 2026-08-07 attempted | Prior observed Mario Zechner MIT text; no upstream commit or body hash was preserved. Current identity unavailable. | Unassessable | G7 | Does not close PRIME’s fork base, inherited-file map, or notice provenance. |
| Current `earendil-works/pi` license comparison | https://raw.githubusercontent.com/earendil-works/pi/main/LICENSE | 2026-08-06 | Same mutable branch path; inaccessible | 2026-08-07 attempted | Prior observed Mario Zechner MIT text; no upstream commit or body hash was preserved. Current identity unavailable. | Unassessable | G7 | Does not close fork provenance or release-package notice preservation. |

## Mutable legal, service, and privacy ledger

No current legal page was opened. The summaries below preserve the prior finding’s decision-bearing facts; they are not current legal conclusions.

| Claim | Prior source | Prior retrieval | Current source | Current retrieval | Preserved prior/current identity | Drift | Controlling downstream task | Impact |
|---|---|---:|---|---:|---|---|---|---|
| npm registry access terms | https://docs.npmjs.com/policies/open-source-terms | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior page said last updated `2022-03-10`; commercial/public API acquisition allowed while package rights remain publisher-controlled. No prior hash; current effective date/hash unavailable. | Unassessable | G7 | Registry-service compatibility and automation terms must be refreshed before closure. |
| Prime Intellect service terms | https://www.primeintellect.ai/terms-of-service | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior displayed update `2024-02-23`; preserved concerns included personal-use language, automation restrictions, commercial-use ambiguity, export/territory restrictions, and incorporated third-party terms. Current effective date/hash unavailable. | Unassessable | G2, G7 | Prime-hosted execution remains blocked; changed terms cannot be excluded. |
| Prime Intellect privacy policy | https://www.primeintellect.ai/privacy-policy | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior displayed update `2024-02-23`; permitted service/R&D analytics, provider/marketing sharing, international processing, and non-numeric retention. Current effective date/hash unavailable. | Unassessable | G7 | Data use, subprocessors, retention, deletion, and account-class requirements are not fresh. |
| OpenAI business/API terms | https://openai.com/policies/business-terms/ | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior effective date `2026-01-01`; preserved facts: customer retains input/owns output and no training without explicit agreement, subject to incorporated policies and account/model restrictions. Current identity unavailable. | Unassessable | G7, G15, G18 | Cannot select or budget an OpenAI path from stale terms. |
| Anthropic commercial terms | https://www.anthropic.com/legal/commercial-terms | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior page exposed no revision date; preserved facts: customer retains inputs/owns outputs and Anthropic stated it may not train on customer content. No prior or current hash. | Unassessable | G7, G15, G18 | Effective/current terms and account/model-specific additions remain unbound. |
| GitHub/Copilot terms | https://docs.github.com/en/site-policy/github-terms/github-terms-of-service | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior effective date `2026-04-27`; preserved facts included account-dependent AI training controls, output similarity/licensing risk, automation rules, and trade controls. Current identity unavailable. | Unassessable | G7 | Copilot/OAuth path cannot be approved from stale terms. |
| Linear service terms | https://linear.app/terms | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior effective date `2026-06-09`; preserved facts: internal business use, API limits, sanctions restrictions, and normally 30-day post-termination deletion. Current identity unavailable. | Unassessable | G7 | Optional MCP path must remain disabled unless refreshed and selected. |
| Notion MCP/service terms | No primary legal object was bound in P3 | 2026-08-06 gap | No current primary source could be discovered or opened | 2026-08-07 attempted | No prior or current content identity | Unassessable | G2, G7 | Notion MCP must remain disabled; it cannot be represented as rights-closed. |
| Arbitrary/custom MCP and provider terms | No finite source set exists until the profile selects exact services | 2026-08-06 gap | Not applicable until G2 selects one bounded profile | 2026-08-07 | No content identity | Open frontier, not unchanged | G2, G7 | G2 must disable these edges by construction or name exact sources for G7. |

## Mutable platform documentation and issue ledger

| Claim | Prior source | Prior retrieval | Current source | Current retrieval | Preserved prior/current identity | Drift | Controlling downstream task | Impact |
|---|---|---:|---|---:|---|---|---|---|
| Windows managed-kernel failure reported on `0.7.0` | https://github.com/PrimeIntellect-ai/prime-agent/issues/660 | 2026-08-06 | Same issue; inaccessible | 2026-08-07 attempted | Prior: created `2026-08-06T00:04:53Z`; Windows 11 Pro, Node `22.14.0`, npm `10.9.2`, uv `0.12.2`, Python `3.13.9`; commit omitted. Current issue state, edits, comments, labels, `updated_at`, and body hash unavailable. | Unassessable | G2, G14 | Prior issue only corroborates immutable source analysis; current resolution/workaround status is unknown. |
| Adjacent Windows installer issue | https://github.com/PrimeIntellect-ai/prime-agent/issues/665 | 2026-08-06 | Same issue; inaccessible | 2026-08-07 attempted | Prior: created `2026-08-06T00:21:11Z`; stated a different commit `c98941a2`. Current issue identity unavailable. | Unassessable | G2 | Must remain non-baseline context; closure or edits cannot be assessed. |
| Hosted-training placement/prerequisites | https://docs.primeintellect.ai/hosted-training/getting-started.md | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior mutable page said hosted training could launch from a CPU machine with no local GPU; no prior revision/hash. Current identity unavailable. | Unassessable | G2, G7 | Optional hosted training cannot enter the minimal profile on current evidence. |
| Self-managed `prime-rl` GPU context | https://docs.primeintellect.ai/prime-rl/overview.md | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior page listed NVIDIA RTX 3090/4090/5090, A100/H100/H200/B200 as adjacent current context, not baseline support. Current identity unavailable. | Unassessable | G2 | Must remain disabled and cannot establish baseline GPU support. |
| Dynamic GPU availability documentation | https://docs.primeintellect.ai/cli-reference/check-gpu-availability.md | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior page showed an `H100_80GB` example and a dynamic two-H100 configuration; no revision/hash. Current identity unavailable. | Unassessable | G2, G15, G18 | No current availability, region, stock, or rate can be used. |
| WSL2 support status | No exact-baseline source, issue, or official document named WSL2 | 2026-08-06 gap | Current repository issues/docs search unavailable | 2026-08-07 attempted | No current search result ledger or source identity | Unassessable | G2, G14 | WSL2 remains unknown; it cannot be selected without later measured qualification. |
| Core Docker support status | Immutable tree showed no Dockerfile, Compose, OCI manifest, image digest, or core launcher | 2026-08-06 | Mutable current docs/issues search unavailable; immutable baseline remains controlling | 2026-08-07 attempted | Baseline absence is pinned to tree `0625a8...`; current product documentation identity unavailable | Baseline result cannot drift; current-product context unassessable | G2, G14 | Core baseline still supplies no Docker path; no newer documentation may be imported automatically. |

## Mutable pricing ledger

All prices below are prior observations used only as arithmetic comparators. None is current enough for a user approval ceiling.

| Claim | Prior source | Prior retrieval | Current source | Current retrieval | Preserved prior/current identity | Drift | Controlling downstream task | Impact |
|---|---|---:|---|---:|---|---|---|---|
| Prime Inference billing model | https://docs.primeintellect.ai/inference/overview | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior: token billing/account balance; public model prices deferred to an authenticated models API. No public unit rate or page hash. | Unassessable | G2, G15, G18 | No Prime Inference dollar ceiling can be displayed. |
| OpenAI `gpt-5.6-sol` comparator | https://developers.openai.com/api/docs/models/gpt-5.6-sol | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior: `$5/M` input, `$30/M` output, `$0.50/M` cached input; long-context multipliers and Tier-1 limits were recorded. Current price/effective date/hash unavailable. | Unassessable | G15, G18 | Prior arithmetic cannot authorize paid calls. |
| Hosted-evaluation billing and timeout | https://docs.primeintellect.ai/tutorials-environments/hosted-evaluations | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior: Prime Inference mode did not separately bill sandbox runtime; custom endpoint mode added sandbox and external-token costs; timeout range `120–1440` minutes, default `1440`. Current identity unavailable. | Unassessable | G2, G7 | Optional hosted evaluation must remain disabled. |
| Hosted-training model rates | https://docs.primeintellect.ai/hosted-training/models-and-pricing | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior example `Qwen3.5-35B-A3B`: `$0.25/M` input, `$0.75/M` output, `$1.00/M` training tokens. Current model/rate list unavailable. | Unassessable | G2, G7 | Optional hosted training must remain disabled and unpriced. |
| Remote GPU example rate | https://docs.primeintellect.ai/cli-reference/check-gpu-availability | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior example: two H100 80GB GPUs at `$5.40/config-hour`, `$0.09/config-minute`, `$0.045/GPU-minute`. Current stock/rate/region identity unavailable. | Unassessable | G15, G18 | Cannot support an approval ceiling or availability assumption. |
| Network-disk rates | https://docs.primeintellect.ai/cli-reference/managing-disks | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior displayed `$0.00007000–0.00011546/GB-hour`, equivalent to `$0.05110–0.0842858/GB-month` at 730 hours. Current identity unavailable. | Unassessable | G2, G15 | No current storage ceiling; optional remote disk remains out of profile. |
| Prime sandbox rates and limits | https://docs.primeintellect.ai/sandboxes/overview | 2026-08-06 | Same page; inaccessible | 2026-08-07 attempted | Prior: `$0.05/core-hour + $0.01/GB-RAM-hour + $0.001/GB-disk-hour`; default 1 core, 2 GB RAM, 10 GB disk = `$0.08/hour`; timeout 1–1440 minutes, default 60. Current identity unavailable. | Unassessable | G2, G7 | Optional remote Docker sandbox cannot be selected or priced. |

## Drift judgment

1. The authorized commit and tree remain immutable identifiers. They are not replaced by a tag, release page, branch, or newer version.
2. No mutable source was successfully retrieved on 2026-08-07.
3. Current tag targets, release assets, newly published releases, registry metadata, issues, platform documentation, legal text, service/privacy terms, and pricing are therefore unknown.
4. No unavailable source is classified as unchanged.
5. No baseline switch, compatibility redesign, provider selection, service selection, or legal/license conclusion is made.
6. P2 and P3 remain blocked; P5 remains not source-satisfied; P7 remains insufficiently evidenced. This ledger supplies no new evidence capable of relaxing those findings.
7. The current public-byte total, selected-provider rate, exact call/token ceiling, and final dollar ceiling required by later approval checkpoints cannot be stated.

## RED-proof review fixtures

Review must reject each of the following fixtures:

| Fixture | Required failure |
|---|---|
| A mutable row omits either its 2026-08-06 prior retrieval date or 2026-08-07 current retrieval attempt | `missing retrieval date` |
| A mutable row says “unchanged” without a current response identity such as a body hash, immutable revision, `ETag` plus preserved body, or API `updated_at` plus preserved content | `missing current content identity` |
| A release/tag/API object changes target, asset digest, `updated_at`, effective date, or body hash but is labeled no drift | `drift mislabeled` |
| An inaccessible page is copied forward as current evidence | `unavailable source treated as current` |
| The release-list discovery check is absent, so a newly published PRIME version could be missed | `new-release check absent` |
| A page hash is supplied without retaining the quoted decision-bearing fact or effective metadata it identifies | `identity lacks reviewable content` |
| A SHA-pinned source is described as mutable merely because its branch, tag, or hosting page changed | `immutable and mutable identities conflated` |
| A mutable tag or release object is allowed to replace the authorized commit | `unauthorized baseline substitution` |

The actual ledger intentionally does not pass the positive freshness gate: mutable rows lack current source bodies and current content identities because retrieval was unavailable. Treating this report as positive freshness would itself trigger the fixtures above.

## Gate consequence

G1 may not proceed. The plan permits G1 only after G0 positively establishes freshness; this report cannot do so. The next permissible action is a new G0 retrieval using public read-only web access, preserving current bodies or hashes and comparing every row before any host probe is dispatched.

SOURCE UNAVAILABLE
