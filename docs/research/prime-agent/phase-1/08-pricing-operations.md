# PRIME Agent pricing and operational closure

**Baseline:** user-authorized Prime Intellect PRIME Agent `v0.7.0`, commit
`be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`. P1's launch-revision binding
remains **UNRESOLVED**. **Audit/retrieval date:** 2026-08-06. No account,
quote, purchase, authentication, API call, download, install, host probe,
container, render, GPU, evaluation, or training run was used.

## Central verdict

**TOTAL COST IS NOT CLOSED; confidence in a campaign total is 2/10.** Core
PRIME has no purchase price evidenced in the baseline, but it is not “free”:
its packaged/source acquisition leaves Node/npm, Python/uv/wheels, managed
helpers, host disk/network, setup labor, and upgrades unpriced; one model
provider path is required for each model turn and no provider/account/model was
selected. Prime Inference publishes token billing but not public model rates;
Prime telemetry retention/pricing and local hardware/electricity are unknown.
[P2][P3][P7][U1]

Known public units permit auditable formulas, not a quote. Optional Prime hosted
training, GPU, disk, evaluation, and Docker sandbox prices apply only if those
separate services are selected; they are not core requirements or evidence of
fit. Recovery is an exposed reserve because abrupt loss can leave provider/tool/
refinement outcomes uncertain, split or corrupt state, and replay/duplicate
charges. [P2][P4][P5][P7]

## Accounting rules and symbols

All dollars are USD. Decimal `GB` and binary `GiB` stay distinct. A displayed
zero means zero units selected, never zero labor/hardware. `w` = loaded
$/person-hour; `pL` = local GPU+electricity+amortization $/GPU-hour; `pD` = local
storage+backup $/GB-month; all three are **unknown** without private labor and
host facts. `I/O/C` = million input/output/cached-input tokens; `A` = API calls;
`m` = GPU minutes; `D` = retained GB-month; `q` = fraction of a run budget
reserved for replay/duplicate exposure.

Provider formula: `Cmodel = I*pi + O*po + C*pc + A*pa + tool fees`. For direct
OpenAI API `gpt-5.6-sol`, official public units are `pi=$5`, `po=$30`,
`pc=$0.50` per 1M tokens; requests over 272K input are 2× input and 1.5× output,
cache writes 1.25× uncached input, and tool-call fees may add cost. The page
lists Tier-1 500 RPM/500,000 TPM/1,500,000 batch-queue tokens; actual account
tier is unknown. This rate is an arithmetic comparator only: PRIME's cataloged
Codex/OAuth route and the current Pi account are not proven to use API billing.
[U2][P6]

Recovery reserve: `Crecovery = hrec*w + q*(Cmodel + m*pL/60 + external-tool
cost) + Drepair*pD`; `q` prices exposure, not an assertion that replay is safe.
An `uncertain` remote call may already be billed or committed, while a new-ID
retry can duplicate semantic work. [P4][P5]

## Acquisition and setup closure

| Path/item | One-time quantity and direct price | Labor/disk/account consequence | Status |
|---|---|---|---|
| Packaged B tarballs | Four recorded tarballs total `10,364,494 B = 10.364494 MB = 9.884352 MiB`; public artifact checkout price not stated | External npm graph, extraction and installed disk unknown; verify four P1 SHA-256 identities | known-byte floor; total unknown |
| Source/package install | source checkout GB unknown; 428 external lock paths, 259 without both resolution+integrity | Node `>=22.8`, npm version, checkout/build/node_modules GB and `hsrc*w` unknown | optional source route; unknown |
| Shipped npm install | retained semver ranges; no shipped lock | registry download GB, installed tree/disk, integrity review and `hnpm*w` unknown | required packaged route; unknown |
| Python/RLM | Python 3.11 request; uv/Python/wheel/helper download and disk GB unknown | no Python lock; venv setup/integrity `hpy*w`; native Windows managed-kernel path unsupported | required for RLM pilot; unknown |
| `fd`/`rg` | mutable GitHub `latest`; download/disk GB unknown | disable or pin/check bytes; `htool*w` | optional/degradable; unknown |
| Dynamic packages/MCP/Prime CLI | npm/git/local/`latest`; download/disk and subscriptions unknown | each enabled edge needs account/credential/terms/integrity work | optional; otherwise zero units |
| Pi/Prime coexistence | Prime paths `~/.prime/agent`, project `.prime/agent`; Pi footprint unknown | separate dirs, auth, env, temp, IPC and process inventory; `hiso*w`; no shared override | required operational gate |
| Platform choice | Linux/macOS packaged path official; WSL2 unknown; native-Windows installer and managed kernel unsupported | environment acquisition/migration and validation `hos*w`; VM/WSL GB unknown | setup blocker/variable |
| Docker | core images/containers `0`; same-host example uses bubblewrap/`sandbox-exec` | no local Docker acquisition, daemon, image, volume, backup or recovery cost belongs in core total | **not applicable to core** |

One-time setup formula:
`Csetup = (hacq+hterms+hiso+hos+hverify)*w + Dinstall*pD + network/egress +
credential funding + optional environment/hardware acquisition`, where every
`h*`, `Dinstall`, network rate, funding floor and hardware price remains a
measured/user-supplied variable. P3's blocked package/provider/service terms
make setup authorization unavailable; price does not waive that gate. [P3]

## Complete P2 service/operation ledger

| P2 class | Placement; requiredness | Dated price/units | Quota, retention, recovery and operator cost |
|---|---|---|---|
| Core client/daemon/catalog/worker/kernel | local; required set depends on daemon/RLM path | software purchase price not evidenced; CPU/RAM/RSS/energy unknown | process counts scale with roots/kernels; operator start/stop, state checks and host-resource cost remain variables |
| Core DB/broker/object store/container | absent | `0` selected core units | no hidden container/service charge; local files remain operator-owned state |
| GitHub/R2 release + npm | remote acquisition; packaged route required | subscription/GB price not stated; known B tarballs above | mutable channel and ranged dependencies require hash/tree capture, backup and upgrade rollback labor |
| Astral/uv, Python, PyPI wheels | acquisition/local runtime; RLM-required | unit prices/download/install GB unknown | no exact lock; rebuild and offline recovery bytes unknown |
| Model provider N6 | remote normally; one path required per turn | selected rate unknown; formula above; OpenAI comparator [U2] | model/account quotas, retention, routing, request idempotency and billing reconciliation unknown |
| OAuth/account paths | remote; optional alternative credentials | plan/subscription price unknown; no account selected | create/fund, least privilege, rotation, revocation, backup codes and recovery `hcred*w`; secrets must not mix Pi/Prime |
| Linear/Notion/custom MCP | remote; optional/auth-gated | API/subscription/call prices and quotas unknown | remote effect/retry/retention terms vary; disabled means 0 calls, not “free” |
| Local logs/traces | local; logs operational, trace upload optional/default off | local `Dlog*pD`; Prime upload/egress price unknown | local rotation exists; session/harness TTL absent; dropped writes and remote retention/export unknown |
| Prime Inference | remote; optional provider/hosted-eval default | token-billed; public model unit rates absent; `I*pPIi+O*pPIo` [U1] | Prime account/API key/balance; pricing from authenticated models API, so `pPI*` stays unknown here |
| Hosted evaluation | remote; optional | Prime Inference mode: sandbox runtime not separately billed; custom endpoint: Prime sandbox + external tokens [U3] | published environment, account/billing/secrets; timeout 120–1440 min, default 1440; logs/results retained but duration/egress price unknown |
| Hosted training | remote; optional | e.g. `Qwen3.5-35B-A3B`: `$0.25I+$0.75O+$1.00T`; 1M of each = `$2.00` [U4] | all supported rates mutable; run token totals, calls, quotas, adapter storage/download/retention/egress unknown |
| Remote GPU pod | remote; optional | dated docs example: 2×H100 80GB at `$5.40/config-hour = $0.09/config-min = $0.045/GPU-min` [U5] | dynamic stock/region/rate; boot/idle/failure minutes, image/data transfer, minimum billing and recovery unknown |
| Network disk | remote; optional with pods/training | displayed range `$0.00007000–0.00011546/GB-hour`; at 730 h: `$0.05110–0.0842858/GB-month` [U6] | persists after instance; size cannot be changed; backup, snapshot, retention and egress prices not stated |
| Prime Docker sandbox | remote CPU-only; optional, not core | `$0.05/core-h + $0.01/GB-RAM-h + $0.001/GB-disk-h`; default 1 core+2 GB+10 GB = `$0.08/h` [U7] | 1–1440 min timeout (default 60); account limits 512 active/512 cores/1024 GB RAM/5120 GB storage; images/registry egress and retained outputs unknown |
| Tunnel/instance permissions | remote; optional hosted eval/tool path | price unknown | extra temporary scopes and external resources can outlive/fail independently; reconcile before retry |
| Custom/local model server | local or operator-rented; optional | `m*pL/60` local or `m*prented/60`; model, VRAM, power, disk GB unknown | separate weights/cache/service/driver/port/health/backup; one-heavy-job lock required |
| Visual renderer | external local/rented; required by Vordar visual evidence, not supplied by PRIME | `mrender*pL/60` or selected rented model-minutes; exact renderer GPU/VRAM unknown | serialize with every local model/training job; retain source/render/reviewed hashes |
| Independent Sol judge | remote model plus retained frames; required by project law | `Ijudge*pi+Ojudge*po+Cjudge*pc+Ajudge*pa`; OpenAI comparator applies only if direct API selected | image tokens count as input; separate producer/judge identity, reviewed-byte hash and verdict retention labor |

The displayed `$0.00` models on [U4] are not used as zero-cost scenarios: account,
labor, traffic, storage, rights, monitoring and recovery remain nonzero/unknown.

## Matched-pilot accounting envelopes

These are **arithmetic planning assumptions, not workload requirements,
protocol design, predictions, or authorization**. One normalized matched block
is only a costing unit: one Pi control episode plus a PRIME pre/post pair. The
actual phase-2 planner must replace every quantity. Direct-API Sol rates [U2]
are used solely so arithmetic can be recalculated; actual Pi/Prime provider
rates replace them. Each row assumes every request is `<=272K` input tokens,
uncached input, and no paid model tools; otherwise [U2]'s multipliers/cache/tool
units apply. Calls have `$0` only where [U2] lists no per-request fee.

| Envelope | Blocks / episodes; calls | Input/output MTok (agent + judge) | Labor; local/rented visual | Direct-API arithmetic |
|---|---|---|---|---|
| Low | `1 / 3`; `60+3` calls | `0.60/0.12 + 0.12/0.015` | setup 12 h + ops 4 h; 30 GPU-min | agent `$3+$3.60=$6.60`; judge `$0.60+$0.45=$1.05`; **`$7.65 + 16w + 0.5pL`** |
| Expected | `3 / 9`; `300+15` | `3.0/0.60 + 0.60/0.075` | setup 32 h + ops 12 h + recovery 4 h; 180 min; `q=.5` | base `$33+$5.25=$38.25`; replay reserve `.5×38.25=$19.125`; **`$57.375 + 48w + 4.5pL`** |
| High | `5 / 15`; `1200+60` | `12/2.4 + 2.4/0.30` | setup 80 h + ops 32 h + recovery 16 h; 720 min; `q=1` | base `$132+$21=$153`; replay reserve `$153`; **`$306 + 128w + 24pL`** |

GPU coefficients include replay (`30/60=.5`; `180/60×1.5=4.5`;
`720/60×2=24`). If, and only if, the U5 two-H100 configuration were compatible
and substituted, visual+replay would be `$2.70`, `$24.30`, `$129.60`; those are
`30×.09`, `270×.09`, `1440×.09`, not a recommended GPU or availability claim.
Install/state/backup GB, cached tokens, tool calls, egress, subscriptions and
failed external side effects are excluded only because their quantities/rates
are unknown; add them before presenting a budget.

## Ongoing campaign envelopes (per month)

Again these are replaceable accounting loads, not requirements. Retain three
copies (live + two backups) only as a visible assumption; local `pD` is unknown.

| Envelope | Blocks; agent + judge MTok I/O; calls | Labor / render / live state | API + replay reserve; storage formula |
|---|---|---|---|
| Low | `1`; `.60/.12 + .12/.015`; `63` | ops 8 h + recovery 2 h + upgrade 1 h; 60 min; 5 GB | `$7.65×1.10=$8.415`; **`$8.415+11w+1.1pL+15pD/month`** |
| Expected | `4`; `4/.8 + .8/.1`; `500` | 32+8+4 h; 720 min; 25 GB | `($44+$7)×1.25=$63.75`; **`$63.75+44w+15pL+75pD/month`** |
| High | `12`; `48/9.6 + 9.6/1.2`; `6000` | 96+24+12 h; 4320 min; 100 GB | `($528+$84)×1.50=$918`; **`$918+132w+108pL+300pD/month`** |

GPU terms include 10/25/50% replay (`60/60×1.1=1.1`,
`720/60×1.25=15`, `4320/60×1.5=108`). If remote network disk were applicable,
15/75/300 GB-month at [U6] would be `$0.7665–1.264287`,
`$3.8325–6.321435`, and `$15.33–25.28574`; this does not include egress or
backup service. One-time setup is separate and not amortized here.

## Operations and recovery runbook cost surface

- **Each start:** `status/doctor`, verify Prime/Pi paths/env/credentials/processes,
  state hashes and heavy-GPU ownership; then Pi control and Prime supervisor →
  catalog/worker → session+harness → kernel/forkserver → provider/optional
  services. Cost `hstart*w`; source supplies no cross-harness coordinator.
- **Each orderly stop:** block new heavy work, obtain explicit episode/refinement
  disposition, retain/export hashes, stop worker children/kernels via
  `prime-agent shutdown`, then verify no resident Prime/heavy process. Cost
  `hstop*w`; closing TUI alone can detach.
- **Abrupt loss:** preserve suspect bytes; hash/parse session, harness/history,
  checkpoint and journals; classify provider/tool/refine as completed/failed/
  cancelled/uncertain; reconcile billing/remote effects; restore dependencies in
  order; retry only with explicit same/new identity. Cost is `Crecovery` above.
- **Integrity/backup:** baseline has no transaction/checksum/TTL for all stores.
  Backup validated Prime state separately from Pi, retain exact episode/render/
  judge bytes, and test restore. Cost `(Dlive×copies×months)*pD + hbackup*w`;
  remote trace/eval storage is not a backup while retention/export is unknown.
- **Monitoring:** local logs plus `status/doctor`; Prime traces default off.
  Reserve `hmonitor*w + Dlog*pD`; hosted dashboards do not close hard-death or
  dropped-log outcomes.
- **Upgrade:** capture package/source/dependency identities, orderly checkpoint,
  replace, restart new supervisor, validate manifests/state, and retain rollback
  bytes. Cost `hupgrade*w + downloadGB*pnet + rollbackGB*pD`; update atomicity
  under power loss is unproven.
- **Contention:** every local renderer/model/training GPU minute includes queue
  wait/operator scheduling and rejected overlap. Remote compute is separate and
  never subtracted from local CPU/RAM/network/state costs.

## Unknowns that block a price commitment

Required: selected Pi and PRIME provider/account/model rates, actual token/image/
call/tool units, rate tier, retry policy, local labor rate, install/state/log/
artifact GB, Pi+Prime CPU/RAM/disk footprint, electricity/hardware amortization,
and provider retention/idempotency. Optional but still unresolved when enabled:
Prime Inference model rates, hosted-eval result/log retention, traces, GPU live
availability/minimum billing, storage backup/egress, training checkpoint/adapter
retention/download, sandbox images/registry egress, MCP subscriptions, and
credential recovery. Each unknown remains a variable in the formulas; none is
silently `$0`.

Phase 2 must meter actual per-call tokens/cost, calls, local/rented GPU model and
minutes, wall time, peak state/log/render GB, failed attempts, duplicate/replay
exposure and person-hours for a frozen real task. It must test orderly and abrupt
loss before replacing these reserves with evidence. Current result remains
**INSUFFICIENT EVIDENCE FOR A PURCHASE OR CAMPAIGN BUDGET**.

## Evidence ledger

Local dependencies (authorized B): **P1–P7**, `.claude/docs/research/prime-agent/phase-1/01-identity-source-lock.md`
through `07-platform-gpu-vram.md`, audited/retrieved 2026-08-06.

All web pages below are mutable official first-party sources, retrieved
**2026-08-06**; none supplies a publication/effective date unless stated.

- **U1:** Prime Intellect, “Inference Overview,” token billing/account balance,
  public model prices deferred to models API: https://docs.primeintellect.ai/inference/overview
- **U2:** OpenAI, “GPT-5.6 Sol Model,” prices, long-context multipliers and rate
  tiers: https://developers.openai.com/api/docs/models/gpt-5.6-sol
- **U3:** Prime Intellect, “Hosted Evaluations,” billing modes, prerequisites,
  timeout and stored logs/results: https://docs.primeintellect.ai/tutorials-environments/hosted-evaluations
- **U4:** Prime Intellect, “Models & Pricing,” hosted-training token rates:
  https://docs.primeintellect.ai/hosted-training/models-and-pricing
- **U5:** Prime Intellect, “Get Availability Information,” displayed dynamic
  2×H100 configuration/rate: https://docs.primeintellect.ai/cli-reference/check-gpu-availability
- **U6:** Prime Intellect, “Managing Disks,” displayed dynamic rates and lifecycle:
  https://docs.primeintellect.ai/cli-reference/managing-disks
- **U7:** Prime Intellect, “Sandboxes Overview,” effective price date not stated;
  CPU/RAM/disk rates, limits, CPU-only Docker service:
  https://docs.primeintellect.ai/sandboxes/overview
- **Terms context:** Prime Terms and Privacy both display updated **2024-02-23**,
  retrieved 2026-08-06: https://www.primeintellect.ai/terms-of-service and
  https://www.primeintellect.ai/privacy-policy . P3 controls the unresolved
  execution-rights finding; this report makes no license verdict.
