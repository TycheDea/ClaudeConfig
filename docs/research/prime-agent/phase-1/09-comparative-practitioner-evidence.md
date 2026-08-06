# PRIME Agent exact-release comparative and practitioner evidence

**Retrieval date:** 2026-08-06

**Search window:** publication/creation from 2026-08-05 through 2026-08-06
**Authorized PRIME baseline:** `v0.7.0`, commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387` (B). P1's launch-to-revision binding remains **UNRESOLVED**.

## Central verdict

**No qualifying independent head-to-head between B and this project's current Pi control was found.** No migration report, sustained practitioner deployment, independent security assessment, or independently reproduced model-backed benchmark naming B was found either. One independent author performed a one-machine install/build/CLI smoke check of version `0.7.0` without a model-backed task; five exact-version/commit GitHub reports describe reproducible setup, Windows, headless-login, recovery, or compaction failures. The strongest comparison-like report tests PRIME `0.7.0` against **Pi `0.80.10`**, not this project's Pi `0.80.6`, and its comparative diagnosis was AI-written. It is useful issue evidence, not a matched head-to-head.

The only disclosed multi-harness benchmark table is Prime Intellect's launch-day first-party table. It does compare Prime Agent with Pi-mono, but names no Prime Agent version/commit, cannot be bound to B under P1, omits enough run/hardware/method detail to prevent independent reproduction, and is therefore a **vendor claim, not practitioner evidence**. Isolated source/docs facts below are a dimension-aligned inventory only; they are not synthesized into a comparison result.

**Evidence confidence: 2/10 for comparative performance or reliability; 5/10 for the existence of the listed narrow failure modes.** Confidence is low because the release was at most one day old, exact-commit practitioner evidence is sparse, reports are single-environment, and no matched sample exists.

## Current Pi control identity (bounded identity lookup; no execution)

| Field | Current project control | Evidence / limit |
|---|---|---|
| Installed package | `@earendil-works/pi-coding-agent@0.80.6`; bin `pi`; repository `earendil-works/pi`; MIT; Node `>=22.19.0` | Local installed manifest [Q1]. The installed README calls Pi a minimal terminal coding harness and documents interactive/print/JSON/RPC/SDK modes [Q2]. |
| Installed dependency metadata | Package-owned `npm-shrinkwrap.json` also identifies root `0.80.6` and pins resolved dependency records | Local shrinkwrap [Q3]. This identifies installed package metadata, not host resource use. |
| Authoritative release mapping | Lightweight `refs/tags/v0.80.6` resolves to commit `2b3fda9921b5590f285165287bd442a25817f17b`, committed 2026-07-09T23:16:55Z; source manifest at that commit says `0.80.6` | GitHub ref/commit and immutable manifest [Q4-Q6]. |
| Byte-binding caveat | **Unresolved** | The local npm package has no `gitHead` or provenance field binding its bytes to Q4. Version agreement supports identity, not a cryptographic local-byte-to-commit proof. No command or benchmark was run. |

Thus the control available to this project is **installed Pi `0.80.6`**, not current upstream/latest and not the Pi `0.80.10` used in issue #674.

## Source facts on the matched P2-P8 dimensions — descriptive, not a head-to-head

| Matched dimension | PRIME B source finding | Pi `0.80.6` exact-control fact | Comparative limit |
|---|---|---|---|
| Architecture / lineage | Hard fork/built on Pi; adds daemon-owned workers, persistent IPython, recursive child sessions, and continual-harness state [P2]. | Minimal terminal harness with extension/skill/package surfaces; README says no built-in subagents or background bash [Q2]. | Architecture facts do not measure outcome. |
| Self-improvement | Global `/refine` can persist supplemental prompt/memory/skill/subagent metadata into later prompts; no reward→update chain, weight update, or demonstrated improvement [P4]. | No matching built-in self-refinement mechanism is documented in the exact README; extensions/skills can add behavior [Q2]. | Absence of a built-in is not a quality result; no matched learning task exists. |
| Persistence / replay / recovery | Session JSONL, daemon journals, harness state and best-effort kernel snapshot exist; deterministic replay and crash-safe episode/reward linkage do not [P4-P5]. | Version-3 JSONL session tree persists messages, model changes, compactions and extension entries; import/export/resume are documented [Q2,Q7]. | Pi recovery/durability was not audited here; session persistence is not deterministic replay. |
| Visual input / judging | Native still-image transport to image-capable providers; no native capture, temporal model, visual reward, reviewed-byte hash, or independent-judge enforcement [P6]. | `ImageContent` is part of persisted messages; README supports pasted/dragged/`@` images [Q2,Q7]. | Neither source establishes visual quality or an independent judge protocol. |
| Platform / Docker | Linux/macOS installer; WSL2 unknown; native-Windows kernel path fails on B; no core Docker layer [P7]. | Exact docs require Bash on Windows and separately document optional whole-process Docker, Gondolin, and OpenShell isolation [Q8-Q9]. | Support descriptions and single-host failures are not matched operability measurements. |
| Resource placement | Local Node daemon/workers/Python kernels; normal model inference is provider-hosted; no practical CPU/RAM/VRAM totals [P7]. | Local Node harness with provider-backed models; package requires Node `>=22.19.0` [Q1-Q2]. | No Pi or PRIME host-resource measurement was run or found. |
| Licensing / services | Commit source MIT, but packaged/transitive Python/model/service rights and Prime-hosted terms remain blocked/unknown [P3]. | Installed package declares MIT and carries a shrinkwrap; selected model/provider and complete transitive legal closure were not audited in P9 [Q1,Q3,Q10]. | A root license is not execution/service closure. |
| Cost | Software purchase price not evidenced; provider, labor, recovery, storage and optional services remain variables; campaign confidence 2/10 [P8]. | Software package is MIT; actual account/model/token/labor/resource cost was not identified by local metadata [Q1-Q2]. | No matched tokens, calls, wall time, GPU time, or dollars. |
| Evidence maturity | One-day launch window; no B-bound independent performance replication; narrow issue reports only. | Exact control released 2026-07-09, but no matched P9 control run or audit exists. | Age/popularity is not quality; no maturity winner is inferred. |

## Independent measurements / practitioner checks

| ID | Source; publication | Baseline; sponsorship/conflict | Workload / hardware / model / sample | Observed result; reproducibility and weight |
|---|---|---|---|---|
| I1 | Curtis Pyke, Kingy, review [I1a] and tutorial [I1b]; published 2026-08-05T22:51:01Z and 2026-08-06T01:39:05Z [I1m] | Prime Agent `0.7.0`; commit absent. Author/site independent of vendor; sponsorship and financial conflict **not stated**. The two posts are one author/one setup and are counted once. | Apple-silicon Mac; isolated npm prefix/disposable Node repo; cloned source, installed pinned npm dependencies, built, checked CLI/local session/diagnostics, and sent one unauthenticated no-session prompt. Node/RAM exact values missing; no provider/model; `n=1` setup. | Build/startup, `--version`, `status`, `doctor`, and expected no-credential stop passed. No paid/model-backed task, subagent, `/refine`, benchmark, sustained deployment, power-loss test, cost, or quality measurement. Repro steps are present but dependency-byte identities are not. **Qualifies only as a narrow smoke check.** |

No other independent measurement naming B or explicitly version `0.7.0` met the window and disclosure requirements.

## Independent anecdotes and reproducible issues

GitHub `author_association:NONE` is recorded where exposed; none of these authors disclosed sponsorship. Each is one reporter/environment unless stated, so none establishes prevalence.

| ID | Source; created | Baseline and conditions | Reproduction / result | Applicability and caveat |
|---|---|---|---|---|
| A1 | `skulitom`, issue #660 [A1], 2026-08-06T00:04:53Z | `0.7.0`, commit absent; Windows 11 Pro build 26200; Node 22.14.0, npm 10.9.2, uv 0.12.2, Python 3.13.9, Git Bash; official installer; model/hardware/sample beyond one host missing. | Default venv uses POSIX `bin/python`; kernel cannot start and retry recreates the venv. Command, errors, paths, workaround, and independent-grep check disclosed. | Exact-version source defect matches B [P7]. Strong narrow reproducibility; no frequency or broader reliability claim. |
| A2 | `myanvoos`, issue #643 [A2], 2026-08-05T21:50:56Z | **Exact B commit link**; headless/SSH login UI. OS, hardware, model and sample count missing; screenshot supplied. | Long OAuth URL is wrapped/padded and cannot reliably be mouse-copied when browser opening is unavailable. Source location and proposed copy action disclosed. | Exact-commit usability observation; not a deployment or security benchmark. |
| A3 | `asmartin-ai`, issue #666 [A3], 2026-08-06T00:56:10Z | `0.7.0`, commit absent; Windows 10 IoT Enterprise LTSC 2021 x64; Microsoft Node installer; Node/model/hardware/sample count missing. | Directory-handle `fsyncSync()` returns `EPERM`; daemon logs failure on each command acknowledgement; journal does not compact; one catalog process exited. | Repro is simple and log-backed. “Crash recovery does not work completely” is reporter interpretation, not an executed crash-recovery study. |
| A4 | `asmartin-ai`, issue #668 [A4], 2026-08-06T00:56:10Z | `0.7.0`, same Windows environment; Node/model/hardware/sample count missing. | Detached children lacking `windowsHide` open visible consoles; a recovery loop opened one per restart; one `--version` child remained >90 s. Spawn sites listed. | Narrow process-lifecycle observation; same author/time as A3, so not independent corroboration. |
| A5 | `paulbatum`, issue #674 [A5], 2026-08-06T02:50:56Z | `0.7.0`, commit absent; Ubuntu 22.04 on WSL2, Node 22.19.0; `gpt-5.6-luna` through `openai-codex`; explicit compaction settings; run count missing (“consistently”). | Print/JSON run exits after skipped compaction with exit 0/no terminal failure. Prompt/settings/event tail disclosed. Reporter says first integration into own benchmark. | Strongest Linux/WSL reliability report. Follow-on comparison is against Pi `0.80.10`, **not control `0.80.6`**, and text after the initial report is explicitly AI-written; not a qualifying head-to-head. |

## Vendor claims — never practitioner evidence

| Claim | Version/conditions disclosed | Disposition |
|---|---|---|
| Launch long-context table compares Prime Agent and Pi-mono-with-subagents on nine tasks using GLM-5.2 (high), plus Prime/Claude Code and Prime/Codex pairs with Opus 5 and GPT-5.6 Sol [V1]. | Prime Agent version/commit, hardware, prompts, run counts, variance, exact model snapshots, and full cost accounting missing. EmulatorBench separately says 16 reconstructions; that does not fill the nine-row table. | First-party direct comparison, but **not B-bound or independently reproducible**. It cannot answer this P9 head-to-head. |
| ARC-AGI-3: Opus 5 scores `[95.0,95.2,95.5]` over three Prime runs; Best@3 completes 183/183; native-harness figures partly yield to vendors' official results [V1]. | Model named; run count 3. Prime version/commit and hardware absent; mixed provenance for comparators. No matched Pi control. | Vendor benchmark only. |
| Factorio score rose run-over-run to `100K+` “in hours” using `/refine`, then the same loop learned reward-hacking via RCON [V1]. | Version, model, hardware, run count, trajectory/reward artifacts and matched baseline missing. | Useful vendor failure anecdote about proxy gaming; not evidence that B learns or improves on Vordar. |
| Kingy reproduces the vendor benchmark table and rates the product 8.3/10 [I1a]. | Kingy explicitly did **not** reproduce the benchmark suite or run a paid end-to-end model session. | Editorial assessment/spec comparison, not an independent benchmark or matched head-to-head. |

## Predecessor / adjacent context — not current evidence

| Context | Why excluded from current claims |
|---|---|
| RLM paper, Continual Harness paper, and Recursive Harness Self-Improvement study cited by Kingy | Different implementations/tasks; the latter includes synthetic tasks and an LLM judge. None names B. |
| Pi `0.80.10` fix/source comparison in A5 | Not this project's installed `0.80.6`; cannot be imputed backward. It explains lineage divergence but does not establish a control outcome. |
| Issue #665 and PR #663 | #665 names a different commit (`c98941a2`) despite saying `v0.7.0`; #663 tests a proposed fix commit and repeats A1's author/evidence. Neither is B behavior independent of A1. |
| Issue #645 (Copilot `service_tier` 400) | Created in-window but names no Prime version or commit. Exact-release applicability is unresolved. |
| Generic agent-security papers, Prime `verifiers`/`prime-rl`, similarly named `prime-agent` skills/products, and pre-window Pi reports | Wrong product/repository, version, or date; no current B experiential claim. |

## Reproducible search ledger

All searches were run/retrieved 2026-08-06; results were opened before classification.

| Venue | Search strings / filters | Result |
|---|---|---|
| General web (OpenAI web search; month recency where supported) | `"Prime Agent" "v0.7.0" comparison Pi coding agent August 2026`; `"Prime Agent" "0.7.0" review migration practitioner`; `"Prime Agent" Pi head-to-head benchmark`; `"Prime Agent" deployment reliability security issue August 6 2026`; `"PRIME Agent" self improving practitioner review` | Found Kingy I1, vendor V1, and issue discovery; no independent matched head-to-head/migration/deployment/security report. |
| General web, exact identity | `"be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387"`; `"prime-agent 0.7.0" benchmark`; `"Prime Agent" security review v0.7.0`; `"Prime Agent" vulnerability "0.7.0"` | Exact SHA search found no relevant third-party record; benchmark/security searches added no qualifier beyond I1/issues. |
| GitHub/web issue search | `site:github.com/PrimeIntellect-ai/prime-agent/issues "0.7.0"`; `"prime-agent 0.7.0"`; `"Prime Agent 0.7.0"`; window 2026-08-05..06 | Opened #643, #645, #660, #663, #665, #666, #668, #674 and API metadata. Qualifiers are A1-A5; others excluded above. |
| Comparative/migration variants | `"Prime Agent" "pi" "August 6, 2026"`; `"Prime Agent" "built on pi" review 0.7.0`; `"Prime Agent" "migrated" coding harness`; `site:x.com "Prime Agent" "v0.7.0"` | No qualifying migration or direct current-control comparison; X returned no usable result. |
| Pi control identity | local documented package path; `site:github.com/earendil-works/pi "0.80.6"`; `site:github.com/earendil-works/pi releases 0.80.6`; npm/version/gitHead query | Established Q1-Q10 and the missing local byte-to-commit binding; no benchmark executed. |

## Evidence ledger

- **P1-P8:** local phase artifacts `01-identity-source-lock.md` through `08-pricing-operations.md`, each audited/retrieved 2026-08-06 and applying to B where stated.
- **Q1-Q3 (local):** `C:/Users/egm_8/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/{package.json,README.md,npm-shrinkwrap.json}`.
- **Q4-Q6:** https://api.github.com/repos/earendil-works/pi/git/refs/tags/v0.80.6 ; https://github.com/earendil-works/pi/commit/2b3fda9921b5590f285165287bd442a25817f17b ; https://github.com/earendil-works/pi/blob/2b3fda9921b5590f285165287bd442a25817f17b/packages/coding-agent/package.json
- **Q7-Q9:** exact installed docs `docs/session-format.md`, `docs/windows.md`, `docs/containerization.md`; immutable upstream equivalents under commit Q5. **Q10:** https://raw.githubusercontent.com/earendil-works/pi/2b3fda9921b5590f285165287bd442a25817f17b/LICENSE
- **I1a/I1b:** https://kingy.ai/blog/prime-agent-review-self-improving-rlm-harness/ ; https://kingy.ai/blog/prime-agent-tutorial-install-recursive-subagents-refine-safely/ . **I1m:** WordPress records https://kingy.ai/wp-json/wp/v2/posts/927747 and `/927763`; author Curtis Pyke (`author:1`).
- **A1-A5:** https://github.com/PrimeIntellect-ai/prime-agent/issues/660 ; `/643`; `/666`; `/668`; `/674` (GitHub API timestamps/associations opened at corresponding `api.github.com/repos/.../issues/<id>` URLs).
- **V1:** Prime Intellect, “Prime Agent: A self-improving RLM agent,” displayed 2026-08-05, retrieved 2026-08-06: https://www.primeintellect.ai/blog/prime-agent

## P9 result

**ABSENT QUALIFYING HEAD-TO-HEAD; SPARSE EXACT-RELEASE PRACTITIONER EVIDENCE.** This finding supports no adoption, reliability, security, cost, or quality winner. A matched pilot remains the first possible comparative evidence for this project's Pi `0.80.6` control versus B, and P4-P8's unresolved execution, rights, recovery, visual-judge, resource, and cost gates remain unchanged.
