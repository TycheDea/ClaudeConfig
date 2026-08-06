# PRIME Agent identity and source lock

**Audit date / mutable-source retrieval date:** 2026-08-06

**Scope:** identity and exact-release source lock only; no feasibility, rights, runtime, or adoption verdict

## Finding

The user-selected product is identified without a homonym conflict: Prime Intellect's product is **Prime Agent**, published by **Prime Intellect, Inc.**, and its canonical public repository is **`PrimeIntellect-ai/prime-agent`** (GitHub repository ID `1232493406`, node ID `R_kgDOSXZbXg`). The official launch article is titled **“Prime Agent: A self-improving RLM agent”** and displays **AUG 05TH, 2026**. It directly names the product, says “Today, we are launching Prime Agent,” calls it a self-improving coding harness, and links the canonical repository. [S1] Repository metadata independently resolves that URL to an organization-owned public repository named `prime-agent`; organization metadata maps `PrimeIntellect-ai` to the display name “Prime Intellect” and the vendor domain. [S2][S3]

The **source revision of the announced launch is not locked**. The article links an unversioned repository and an unversioned “latest stable” installer; it gives no version, tag, commit, package digest, or publication time. On the article's displayed date, the repository published three non-prerelease GitHub releases:

| GitHub release object | Title/tag | Published (UTC) | Lightweight tag currently resolves to | Relationship to article |
|---|---|---:|---|---|
| `365289118` [S4] | `v0.6.0` | 2026-08-05T04:36:20Z | `7db7b69c60be0f7b271faf948864891813b27182` [S7] | Same calendar date; article does not name it. |
| `365606154` [S5] | `v0.6.1` | 2026-08-05T14:55:26Z | `8bd7c18f16bfdc356c1cd20fb9fcf01119147cda` [S8] | Same calendar date; article does not name it. |
| `365741496` [S6] | `v0.7.0` | 2026-08-05T18:41:37Z | `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387` [S9] | Same calendar date and latest of the three, but temporal proximity is not an explicit source binding. |

`v0.7.0` is therefore a **candidate**, not a safe substitute for the exact launch revision. Its release commit is a verified GitHub commit whose message is “chore(release): prepare v0.7.0 (#636),” but its described change concerns agent-message delivery and related fixes, not the launch announcement. [S10] Selecting it merely because it is the last same-day release would infer the missing link the audit plan forbids.

## Identity tuple

| Field | Result | Evidence and exact-release applicability | State |
|---|---|---|---|
| Canonical publisher / owner | **Prime Intellect, Inc.**; product brand **Prime Intellect** | The official article is authored in part by “Prime Intellect Team” and the official page footer identifies Prime Intellect, Inc.; GitHub organization `PrimeIntellect-ai` has display name “Prime Intellect,” vendor blog [https://primeintellect.ai/](https://primeintellect.ai/), and node ID `O_kgDOCNMXhA`. [S1][S2] | resolved |
| Exact product | **Prime Agent**, described by its publisher as a self-improving coding harness / RLM agent | Official article title and opening paragraph. [S1] Candidate source README uses “Prime Agent: A Self-Improving RLM Agent” and identifies it as an open-source coding and research agent. [S11] | resolved |
| Canonical repository | **[https://github.com/PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent)**; repository ID `1232493406`; node ID `R_kgDOSXZbXg`; owner node ID `O_kgDOCNMXhA` | Official article's open-source link plus GitHub repository metadata. [S1][S3] | resolved |
| Launch record | Official article **“Prime Agent: A self-improving RLM agent”** | The page displays 2026-08-05 and says “Today, we are launching Prime Agent.” [S1] | resolved |
| Launch publication date | **2026-08-05** | First-party date displayed as “AUG 05TH, 2026.” [S1] | resolved to day, not time |
| Exact software release title/version | Unknown | `v0.6.0`, `v0.6.1`, and `v0.7.0` are all first-party releases on 2026-08-05; the article names none. [S1][S4][S5][S6] | unresolved |
| Exact release/tag object | Unknown | All three same-day tags are lightweight refs (`type: commit`), and no source binds one ref to the article. [S7][S8][S9] | unresolved |
| Exact source commit SHA | Unknown | Candidate SHAs are the three values in the table above. A unique launch SHA is not published. | unresolved |
| Exact package/release artifacts | Unknown for the launch; fully enumerated below for candidate `v0.7.0` | The article's installer is unversioned. The `v0.7.0` release object exposes seven assets, but the article does not bind itself to that object. [S1][S6] | unresolved for launch |
| Package identifiers in candidate source | Root workspace `prime-agent@0.7.0` (private); published workspace names `@earendil-works/pi-coding-agent@0.7.0`, `@earendil-works/pi-agent-core@0.7.0`, `@earendil-works/pi-ai@0.7.0`, and `@earendil-works/pi-tui@0.7.0` | Commit-pinned package manifests. [S12][S13][S14][S15][S16] These are identifiers in the candidate source, not proof of registry publication or proof that `v0.7.0` is the launch revision. | resolved for candidate only |
| Container identifiers/digests | None exposed | Neither the launch article nor the candidate `v0.7.0` GitHub release object exposes a container name or digest. [S1][S6] Absence is limited to these records, not a claim that no container exists elsewhere. | not exposed |
| Model / weight identifiers or revision hashes | None exposed as a product dependency lock | The article discusses models used in evaluations and explicitly says no model had yet been trained around Prime Agent or its core feature set, but it publishes no model/weight revision as part of the product release. [S1] | not exposed |
| Documentation identifier | No standalone docs version; candidate docs are the paths under commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`, especially `README.md`, `packages/coding-agent/docs/index.md`, and `packages/coding-agent/docs/rlm.md` | Candidate README's documentation index and commit-pinned RLM document. [S11][S17] | resolved for candidate only; launch docs unresolved |

## The release's own terminology

### “RLM”

The launch article defines its **Recursive Language Model (RLM)** abstraction as follows:

> “The Recursive Language Model (RLM) treats context as a variable and subagent delegation as function calls inside a REPL. The persistent REPL gives the model programmatic access to its history, sub-agents, and tools, allowing it to write language model programs as actions over its own context.” [S1]

The candidate `v0.7.0` source is consistent and more operationally specific: it says context is treated as variables, recursive subagents are function calls inside a persistent REPL, and the model works in a persistent Python control environment while provider calls, persistence, lifecycle, scheduling, and policy remain in the TypeScript host. [S11][S17]

Thus, in the product's own usage, **RLM names the harness/runtime programming pattern**. It is not a model/weight identifier.

### “Self-improving”

The article grounds “self-improving” in its second abstraction, **Continual Harness**:

> “Continual Harness treats the harness's own state, abstracted as its prompts, skills, memory, and sub-agents, as something the agent can create, read, update, and delete (CRUD) from its own trajectory.” [S1]

It then defines `/refine` as a pipeline that reads the agent's trajectory and applies a small CRUD edit to a prompt note, memory, skill, or sub-agent specification, records trigger and outcome, writes changes to disk, and supports rollback. It also says the base system prompt remains immutable. [S1] Candidate source states the same boundary: `/refine` can update **supplemental harness state**, never rewrites the immutable base system prompt, and records snapshots for rollback. [S11]

Accordingly, **the release's own “self-improving” claim means trajectory-informed, durable refinement of supplemental harness state**. The launch record does not define it as training or updating model weights; indeed, the article says that, at publication, no model had been trained around Prime Agent or its core feature set. [S1]

## Candidate `v0.7.0` source and distribution manifest

This is an immutable-identifier manifest for the strongest same-day candidate. It is retained to prevent later branch drift, but it does **not** resolve the missing announcement-to-version edge.

### Source objects

| Object | Immutable/current identifier | Evidence | Mutability caveat |
|---|---|---|---|
| Repository | GitHub repository ID `1232493406`, node ID `R_kgDOSXZbXg` | [S3] | Repository metadata and default branch are mutable. |
| Candidate release | Release ID `365741496`, title/tag `v0.7.0`, published `2026-08-05T18:41:37Z` | [S6] | GitHub API reports `immutable: false`; title/body/assets can therefore change. |
| Candidate tag ref | `refs/tags/v0.7.0` -> commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`; ref object type `commit` | [S9] | This is a lightweight mutable ref, not an annotated/signed tag object. The recorded commit SHA, not the ref name, is the durable source identifier. |
| Commit | `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387` | [S10] | Content-addressed commit; GitHub reports signature verification `verified: true`, reason `valid`. |
| Source tree | `0625a8fd0550a8de7ff05e8d9248e75563e5b520` | [S10] | Content-addressed tree. |
| Root version manifest | `package.json` at candidate commit, `prime-agent@0.7.0` | [S12] | Root package is marked private. |
| Package manifests | Four commit-pinned package paths and identifiers listed in the identity tuple | [S13][S14][S15][S16] | Manifest identifiers do not establish external registry bytes. |
| Documentation | `README.md`; `packages/coding-agent/docs/index.md`; `packages/coding-agent/docs/rlm.md`, all under candidate commit | [S11][S17] | No separate documentation version or docs build digest is exposed. |

### Release assets reported by GitHub

No bytes were acquired. The following names, asset IDs, sizes, and SHA-256 digests are the GitHub release API's metadata as retrieved on 2026-08-06. [S6]

| Asset | Asset ID | Size (bytes) | API-reported digest |
|---|---:|---:|---|
| `latest.json` | `502961048` | 820 | `sha256:65af98a9541d109df58679bf8ecab633f8744b4ccb6fea8308d15cb33540bac0` |
| `prime-agent-0.7.0.tgz` | `502961047` | 9,323,789 | `sha256:88b6578518c72cd51a825bc80f28e0fef9a64c67de4a7d6fd7afd7ca1b34da0b` |
| `prime-agent-ai-0.7.0.tgz` | `502961049` | 533,591 | `sha256:7cdbb3e835f48dd103325f7a351ce540b27af4d161aeb9c7b9bdcc12fe7909af` |
| `prime-agent-core-0.7.0.tgz` | `502961050` | 62,815 | `sha256:0313373089831d9a2ce06e874fab8b9c05762c0094ff9fc202908cf7db7f99cd` |
| `prime-agent-tui-0.7.0.tgz` | `502961057` | 444,299 | `sha256:3225f7f92e87db80fe2c9005d1f7770735ae625c32935ef2283688fc9bd33951` |
| `SHA256SUMS` | `502961051` | 364 | `sha256:424d629dc97dfe07a7fc5806c2698bf7eb1d1d49e249159792073aad83a5abd7` |
| `stable` | `502961058` | 7 | `sha256:22d24eb4aeab009537ebbd099e54562d35ce546add330e4cdecd28ede260c83c` |

Because release object `365741496` is mutable, this table is a dated observation. Each digest is an immutable byte identity if independently matched, but the audit did not download the assets and the launch article does not identify this asset set.

## Mutable-source ledger

All mutable sources below were opened and retrieved on **2026-08-06**. Search and social snippets were used only for discovery and are not evidence.

| ID | Source / author | Tier | Canonical URL | Publication/effective metadata | Exact section or excerpt | Applicability and caveat |
|---|---|---:|---|---|---|---|
| S1 | “Prime Agent: A self-improving RLM agent,” Seth Karten, Alex L. Zhang, Kevin Thomas, Sebastian Müller, and Prime Intellect Team | 2, first-party launch record | https://www.primeintellect.ai/blog/prime-agent | Published/displayed 2026-08-05; no publication time or revision/effective date exposed; retrieved 2026-08-06 | Page metadata “AUG 05TH, 2026”; opening “Today, we are launching Prime Agent”; sections “RLM and Programmatic Tool-Calling,” “Self-Improvement via the Continual Harness,” “Evaluating Prime Agent,” and “Citation” | Controls product name, date, repository link, and vendor definitions. Mutable and unversioned; cannot lock source revision. |
| S2 | GitHub organization API, `PrimeIntellect-ai` | 2, primary repository metadata | https://api.github.com/orgs/PrimeIntellect-ai | `updated_at` 2026-07-25T19:08:27Z; retrieved 2026-08-06 | `login`, `id`, `node_id`, `name`, `blog`, `type` | Maps organization login to Prime Intellect; API metadata is mutable and GitHub reports `is_verified: false`, so the official article/repository link remains the ownership anchor. |
| S3 | GitHub repository API, `PrimeIntellect-ai/prime-agent` | 2, primary repository metadata | https://api.github.com/repos/PrimeIntellect-ai/prime-agent | Repository created 2026-05-08T01:42:41Z; `updated_at` 2026-08-06T18:31:39Z; `pushed_at` 2026-08-06T18:25:42Z; retrieved 2026-08-06 | `id`, `node_id`, `full_name`, owner, description, default branch | Controls repository identity, not launch revision; mutable current-state record. |
| S4 | GitHub release object `365289118` | 1 for recorded revision/digests, but release object mutable | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/365289118 | Created 2026-08-05T04:34:03Z; published/updated 2026-08-05T04:36:20Z; retrieved 2026-08-06 | `tag_name`, `target_commitish`, `name`, asset metadata | Same-day candidate only; article does not bind it. |
| S5 | GitHub release object `365606154` | 1 for recorded revision/digests, but release object mutable | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/365606154 | Created 2026-08-05T14:53:29Z; published/updated 2026-08-05T14:55:26Z; retrieved 2026-08-06 | `tag_name`, `target_commitish`, `name`, asset metadata | Same-day candidate only; article does not bind it. |
| S6 | GitHub release object `365741496` | 1 for recorded revision/digests, but release object explicitly mutable | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/365741496 | Created 2026-08-05T18:39:13Z; published/updated 2026-08-05T18:41:37Z; retrieved 2026-08-06 | `tag_name`, `target_commitish`, `name`, `immutable: false`, and complete `assets` array | Strongest same-day candidate and source of candidate asset manifest; no explicit article linkage. |
| S7 | GitHub tag ref API, `v0.6.0` | 1, current ref metadata | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/git/refs/tags/v0.6.0 | No publication/effective date exposed; retrieved 2026-08-06 | `ref`, object `sha`, object `type` | Ref is mutable; recorded SHA identifies candidate source. |
| S8 | GitHub tag ref API, `v0.6.1` | 1, current ref metadata | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/git/refs/tags/v0.6.1 | No publication/effective date exposed; retrieved 2026-08-06 | `ref`, object `sha`, object `type` | Ref is mutable; recorded SHA identifies candidate source. |
| S9 | GitHub tag ref API, `v0.7.0` | 1, current ref metadata | https://api.github.com/repos/PrimeIntellect-ai/prime-agent/git/refs/tags/v0.7.0 | No publication/effective date exposed; retrieved 2026-08-06 | `ref`, object `sha`, object `type` | Ref is mutable; recorded SHA identifies candidate source. |

## Immutable code citations

These links are commit-SHA permalinks and were opened on 2026-08-06:

- **S10 — candidate release commit:** https://github.com/PrimeIntellect-ai/prime-agent/commit/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387 — commit, tree, message, author/committer time, and signature status.
- **S11 — candidate product identity and definitions:** https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/README.md#L12-L40 and https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/README.md#L50-L54 and https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/README.md#L80-L96.
- **S12 — candidate root workspace/version:** https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/package.json#L1-L8 and https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/package.json#L48-L55.
- **S13 — candidate coding-agent package/config:** https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/packages/coding-agent/package.json#L1-L10.
- **S14 — candidate agent-core package:** https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/packages/agent/package.json#L1-L8.
- **S15 — candidate AI package:** https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/packages/ai/package.json#L1-L8.
- **S16 — candidate TUI package:** https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/packages/tui/package.json#L1-L8.
- **S17 — candidate RLM documentation:** https://github.com/PrimeIntellect-ai/prime-agent/blob/be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387/packages/coding-agent/docs/rlm.md#L1-L23.

## Rejected homonyms and adjacent candidates

| Candidate | Why it could be confused | Primary evidence | Disposition |
|---|---|---|---|
| `PrimeIntellect-ai/prime-rl` | Same owner, PRIME branding, and its own `v0.7.0` release; it is model-training infrastructure. | Repository description is “Agentic RL Training at Scale.” API metadata retrieved 2026-08-06, repository `updated_at` 2026-08-06T18:34:28Z: https://api.github.com/repos/PrimeIntellect-ai/prime-rl | Rejected: the launch article links `prime-agent`, not `prime-rl`; product and repository IDs differ. |
| `PrimeIntellect-ai/rlm-harness` | Same owner and “RLM harness” terminology. | Repository description is “Harness for RLM-style rollouts. Only for RL training.” API metadata retrieved 2026-08-06, repository `updated_at` 2026-08-06T17:50:30Z: https://api.github.com/repos/PrimeIntellect-ai/rlm-harness | Rejected: explicitly training-only and a different repository; not the linked coding/research agent. |
| `badlogic/pi-mono`, `earendil-works/pi`, or package names under `@earendil-works` | Prime Agent is derived from pi and retains package namespace/attribution, so source/package searches can land on the upstream. | Candidate README acknowledges that its agent/TUI is built on pi while its canonical repository URL remains Prime Intellect's. [S11][S13] | Rejected as product identity: upstream/lineage, not the Prime Intellect launch owner or repository. |
| Generic Recursive Language Model papers, including the RLM paper linked by the article | The acronym is the architecture's named source. | Official article links the paper while separately naming and linking the Prime Agent product/repository. [S1] | Rejected as product identity: conceptual antecedent, not the released agent. |
| `prime-agent` `v0.1.0` | First numbered release and therefore a plausible “launch” guess absent date checking. | GitHub release object `338289229` was published 2026-06-11T22:56:19Z: https://api.github.com/repos/PrimeIntellect-ai/prime-agent/releases/338289229 (retrieved 2026-08-06). | Rejected for the user-selected 2026-08-05 launch: publication predates it by nearly two months. |
| Mutable `main`, current README/docs, beta builds, or installer “latest” state | Official links are unversioned and can move after launch. | Repository metadata shows pushes on 2026-08-06; candidate release exposes mutable pointer assets `latest.json` and `stable`. [S3][S6] | Rejected as an exact-launch lock: later/mutable state cannot establish launch bytes. |
| `v0.6.0`, `v0.6.1`, and `v0.7.0` | All are correct-product, same-day release candidates. | [S4]–[S10] | None may be selected without a first-party binding to the announcement. They are candidates, not homonyms. |

## Unresolved fields and precise falsifiers

| Unresolved field | Missing evidence | Evidence that would falsify this finding and resolve the field |
|---|---|---|
| Announcement-to-version binding | Article has no version/tag/commit and no publication time; three releases share its date. | A first-party, date-preserved record explicitly saying that the 2026-08-05 announcement launched a named tag/release, or an archived launch-page/installer manifest whose effective timestamp and contents uniquely identify that release. |
| Exact launch commit | No unique tag/release follows from the article. | The binding above plus a tag/release object that resolves to one full commit SHA, or a first-party launch manifest that directly records the full SHA. If a tag is cited, its historical ref value must be preserved rather than assumed from its current mutable value. |
| Exact launch distribution bytes | Article points only to an unversioned installer; no artifact names/digests appear in it. | A first-party launch manifest binding the exact version to every shipped asset and cryptographic digest (or an immutable GitHub release object with those fields), with no extra unenumerated distribution channel claimed as part of that release. |
| Launch package registry revisions | Candidate package manifests expose package names/version, but registry publication and bytes were not exposed by the launch record. | First-party package registry records or release provenance binding each package name/version and integrity digest to the exact launch commit/release. |
| Container, model, and weight revisions | Launch and candidate release records expose none. | A first-party exact-release manifest explicitly declaring these fields absent, or listing every applicable image/model/weight with digest or immutable revision and binding them to the launch release. |
| Exact launch documentation | Official article and repository links are mutable; candidate docs are only conditionally pinned. | A first-party version mapping or archived docs manifest binding the launch to a commit/revision and enumerating the authoritative documentation paths/build digest. |

## Gate justification

Primary evidence is sufficient to lock the owner, product, canonical repository, announcement title, date, and the publisher's meanings of RLM and self-improvement. It is insufficient to lock the required release/tag/commit tuple: the announcement names no source revision, while three distinct releases and commits exist on its displayed date. The candidate `v0.7.0` manifest is reproducible by commit and hashes but cannot be promoted to the launch manifest by chronology alone. Downstream tasks that require a unique P1 identity must therefore stop until one of the precise first-party falsifiers above supplies the missing binding.

UNRESOLVED