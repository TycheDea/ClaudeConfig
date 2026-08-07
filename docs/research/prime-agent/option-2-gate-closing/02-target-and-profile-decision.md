# G2 — Target and Minimal Execution-Profile Decision

## Run record

- **Model seat:** Sol analysis
- **Type:** finding
- **Deliverable:** exact body for `.claude/docs/research/prime-agent/option-2-gate-closing/02-target-and-profile-decision.md`
- **Scope:** G0 `FRESH`, retained G1 inventory, P2/P3/P4/P5/P7/P8/P10, and current public primary platform/provider documentation.
- **Do not touch or decide:** No host probe, provisioning, download, install, guest or WSL lifecycle command, Docker/GPU/process workload, credential/account action, provider call, phase-2 plan, compatibility shim, fallback, Vordar/game/content/VFX/effects/particles access, or concurrent `.claude` edit.
- **Verification criterion:** Exactly one target and one provider profile; WSL2 and the separate Linux guest remain distinct; external power-cut equivalent exists; every P2 node/edge is classified; every disabled path has enforcement and a later check; image/resource approval quantities are exact enough for G3; mutable installers and beta cannot enter.
- **Retrieval date:** 2026-08-07

## Decision

Select one new **Ubuntu Server 24.04.4 LTS AMD64 Generation-2 Hyper-V virtual machine**, named `VordarPrimeOption2`, with no fallback.

The selected external abrupt-loss mechanism is:

```powershell
Stop-VM -Name 'VordarPrimeOption2' -TurnOff -Confirm:$false
```

Microsoft defines `Stop-VM -TurnOff` as equivalent to disconnecting power from the VM. The recovery controller must bind the recorded Hyper-V `VMId` as well as the exact name before invoking it. Failure to provision or qualify this target blocks the campaign; it does not fall through to WSL2.

The retained PRIME baseline remains exactly:

- version `v0.7.0`;
- commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`;
- tree `0625a8fd0550a8de7ff05e8d9248e75563e5b520`;
- Node engine floor `>=22.8.0`;
- beta release ID `355959266`, tag `beta`, and commit `b9a4461149419156599d60174dddf15458e2b9ee` prohibited;
- no mutable installer, update channel, Docker dependency, local model, or local GPU.

## Controlling repository evidence

G0 ends `FRESH` and preserves the stable commit/tree, Node floor, beta exclusion, task ownership, and mutable-source cautions: `.claude/docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md`.

Exact retained G1 fields from `.claude/docs/research/prime-agent/option-2-gate-closing/01-host-platform-inventory/raw.json` are:

| Field | Retained value | Decision use |
|---|---|---|
| `host.windows.build.value.caption` | `Microsoft Windows 11 Pro` | Windows client Hyper-V host |
| `host.windows.build.value.version` / `ubr` | `10.0.26200` / `8973` | Recorded host baseline |
| `host.cpu.logical_cores.value` | `20` | VM CPU ceiling |
| `host.memory.total_ram_bytes.value` | `34134220800` | VM RAM ceiling |
| `host.virtualization.value.hypervisor_present` | `true` | Active host hypervisor evidence |
| `host.windows_optional_features.value[name=Microsoft-Hyper-V-Hypervisor].install_state` | `1` | Microsoft documents `1` as enabled |
| `storage.candidate_guest_storage_volume.free_bytes.value` | `181652307968` | Guest-storage approval basis |
| `wsl.version.value` | WSL `2.4.13.0`, kernel `5.15.167.4-1` | WSL candidate identity, not selected target |
| `wsl.registered_distributions.value` | `Ubuntu` stopped; `docker-desktop` running | Must remain uninspected and untouched |
| `wsl.external_guest_termination_capability.value` | `--terminate` and `--shutdown` listed, neither invoked | WSL comparison only |
| `wsl.filesystem_mount_defaults`, `interop_defaults`, `cgroup_capability`, `systemd_capability` | `UNKNOWN` | Cannot be promoted into measured WSL support |
| `gpu.host_adapters.value` | Intel UHD 770 and RTX 3080 Ti | Selected VM receives neither |
| `gpu.wsl_guest_visibility.value` | `UNKNOWN` | No WSL GPU inference |
| `pi.installed_version.value` | `0.80.6` | Pi remains host orchestrator/control |
| `pi.state_path_names_existence_metadata_only` | host/project Pi roots recorded | Guest must not mount or read them |

The G1 command transcript records `distribution_entered_or_started:false`, `termination_command_invoked:false`, and `configuration_changed:false`. Its retained `raw.json` SHA-256 is `a922eb4e76f88e35228004afd627092655f96b9d7e311e67ae5e4b2e49c8a3f4`.

P2 establishes Linux as the official packaged path, the complete EP/N/E/P graph, no core Docker layer, unrestricted same-user shell exposure, and open Node/Python/dynamic dependencies. P3 blocks unresolved bytes, provenance, services, and optional paths. P4/P5 require explicit refinement and recovery-state evidence rather than replay inference. P7 leaves WSL2 and quantitative host fit unknown. P8 supplies formulas rather than a current provider quote. P10 requires a dedicated guest, disabled optional edges, Pi separation, and external recovery proof.

## Target comparison — not merged

| Criterion | New dedicated WSL2 distribution | New dedicated Hyper-V Linux guest |
|---|---|---|
| Candidate OS object | Canonical `ubuntu-24.04.4-wsl-amd64.wsl`, `391541571` bytes, SHA-256 `9b2f7730dc68227dd04a9f3e5eab86ad85caf556b8606ad94f1f29ff5c4fd3f5` | Canonical `ubuntu-24.04.4-live-server-amd64.iso`, `3405469696` bytes, SHA-256 `e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433` |
| Linux status for PRIME | WSL2 remains unnamed and unmeasured by PRIME’s source/CI | Native Linux is the documented packaged target |
| External loss | `wsl.exe --terminate <name>` stops one distribution | `Stop-VM -TurnOff` is documented as power disconnection |
| Hypervisor boundary | Shares the WSL2 utility-VM/kernel facility | Independent Generation-2 VM and VHDX |
| Hard RAM/CPU boundary | `.wslconfig` controls the shared WSL2 VM globally; Microsoft says it applies to all WSL2 distributions | Per-VM processor and fixed-memory settings |
| Existing guest impact | Global WSL settings or `wsl --shutdown` could affect the retained Ubuntu and running `docker-desktop`; this is prohibited | No WSL command, registration, kernel setting, or distribution state is involved |
| Mount/interop isolation | Per-distribution `wsl.conf` can disable automount/interop, but G1 measured both defaults as `UNKNOWN` | No host filesystem device or enhanced guest-service sharing is attached |
| GPU denial | Per-distribution configuration exists, but G1 visibility is `UNKNOWN` and WSL GPU plumbing is shared host infrastructure | No GPU partition/DDA device is assigned; compute-device absence is independently testable |
| Egress | Per-distribution controls coexist with shared WSL networking/firewall behavior | Dedicated internal virtual switch and no default route |
| Rollback identity | Rootfs export plus shared mutable WSL kernel/package identity | Offline installed-root manifest plus immutable clean VHDX digest |
| Selection result | **Rejected** | **Selected** |

WSL2 is rejected because its VM-level CPU/RAM configuration is global to WSL2 while G1 records another distribution running, and because the WSL kernel/runtime, cgroup/systemd behavior, filesystem defaults, and GPU visibility are not measured. The dedicated distribution could be terminated externally, but it is not the stronger independent boundary on this host.

## Selected guest and immutable OS identity

### Installation object

- **Product:** Ubuntu Server 24.04.4 LTS, AMD64, no GUI
- **Endpoint:** `https://releases.ubuntu.com/24.04/ubuntu-24.04.4-live-server-amd64.iso`
- **Exact size:** `3,405,469,696` bytes
- **Expected SHA-256:** `e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433`
- **Checksum endpoint:** `https://releases.ubuntu.com/24.04/SHA256SUMS`
- **Checksum body size:** `594` bytes
- **Signature endpoint:** `https://releases.ubuntu.com/24.04/SHA256SUMS.gpg`
- **Signature body size:** `833` bytes

The versioned filename plus independently computed digest controls identity; the mutable directory name or current-release page does not. G3 must use an already approved exact endpoint, compute the ISO hash independently, verify the signed checksum using a separately recorded Ubuntu signing-key identity, and block on disagreement.

### Installed-image identity strategy

G3 must install with the VM NIC disconnected and installer refresh, package updates, third-party repositories, snaps, remote SSH acquisition, and unattended upgrades disabled. Identity consists of:

1. ISO filename, URL, exact size, computed SHA-256, `SHA256SUMS`, signature, and signing-key fingerprint;
2. SHA-256 of the unattended-install seed or exact manual answer transcript;
3. Generation-2 VM configuration manifest and Hyper-V `VMId`;
4. installed package/version/architecture manifest;
5. complete offline root manifest of path, type, mode, owner, size, and SHA-256;
6. clean shutdown followed by a SHA-256 of the clean golden VHDX;
7. an operational VHDX cloned from that golden object.

The clean golden VHDX is never booted again. Rollback destroys the operational clone and creates another clone from the verified golden object. An ISO mismatch, network access during installation, package refresh, mutable Ubuntu channel substitution, or unmanifested installed byte blocks G3.

## Boundary and operating profile

### Host placement

All host-side VM material is confined to:

```text
C:\Users\egm_8\AppData\Local\VordarPrimeOption2\
```

This root contains the approved ISO/checksum objects, Hyper-V configuration, active VHDX, golden rollback VHDX, and receipts. It is outside the Vordar tree, `.claude`, user Pi state, project Pi state, existing WSL registrations, Docker storage, and game/content/VFX paths.

No host directory is mounted into the VM. Hyper-V Guest Service Interface, drive sharing, clipboard/file redirection, enhanced-session sharing, automatic checkpoints, GPU partitioning, and discrete-device assignment remain disabled.

### Guest filesystem

| Path | Owner/mode and purpose |
|---|---|
| `/opt/vordar-prime-option2/runtime/<manifest-sha256>/` | `root:root`, non-writable; exact G6 runtime |
| `/var/lib/vordar-prime-option2/home/` | fixed `vordar-prime` home and PRIME global state |
| `/var/lib/vordar-prime-option2/state/` | recovery journals and external disposition records |
| `/srv/vordar-prime-option2/work/` | only working-data root |
| `/var/log/vordar-prime-option2/` | local bounded logs |
| `/run/vordar-prime-option2/` | tmpfs IPC/temp and transient controller state |
| `/run/credentials/vordar-prime-option2.service/` | systemd credential mount; one named slot, no retained value |

`/home`, `/mnt`, `/media`, `/workspace`, `/vordar`, host-drive paths, Pi paths, Docker sockets, and shared temp are absent from the service mount namespace. `HOME`, `TMPDIR`, PRIME state overrides, PATH, and locale are supplied from a root-owned allowlist; inherited `PI_*`, host, user-session, SSH-agent, cloud, Docker, and GPU environment names are removed.

### Supervisor

Ubuntu’s pinned `systemd` is PID 1. A root-owned `vordar-prime-option2.target` owns:

1. isolation/egress policy;
2. PRIME daemon supervisor;
3. catalog and worker descendants;
4. kernel/forkserver descendants;
5. controlled shutdown and evidence collection.

PRIME runs as fixed no-login user `vordar-prime`. The VM is configured with automatic start action `Nothing` and automatic stop action `ShutDown`; only the external campaign controller starts it. Closing a client cannot be treated as stopping the daemon.

### Resource mechanisms

External Hyper-V ceiling:

- 4 virtual processors;
- fixed 8 GiB RAM; Dynamic Memory disabled;
- one dynamically allocated VHDX with a 32 GiB virtual maximum;
- no host swap guarantee and no assigned GPU;
- no nested virtualization;
- no VM automatic start;
- no checkpoint growth.

Internal cgroup-v2/systemd ceiling for the complete PRIME slice:

- `MemoryMax=6G`;
- `MemorySwapMax=0`;
- `CPUQuota=300%`;
- `TasksMax=512`;
- bounded open files and process IDs;
- log and work-directory quotas whose totals must fit within the 32 GiB guest-disk ceiling.

G8 must convert these preliminary values into exact unit properties and attack probes. G11 must inspect the actual cgroup files and process ancestry. Exceeding a configured ceiling is a failure, not authority to enlarge it.

### Network and egress

The VM uses one dedicated Hyper-V **internal** virtual switch, `VordarPrimeOption2-Internal`, with a fixed host/guest `/30` subnet. It receives:

- no external-switch attachment;
- no NAT;
- no default route;
- no guest DNS server;
- no inbound forwarding;
- no access to host LAN addresses or services.

During later approved provider execution, a host-controlled TCP relay binds only the internal-switch host address and forwards only TLS port 443 to the G7/G15-pinned provider hostname. The guest maps that provider hostname to the relay address, preserving end-to-end TLS hostname validation. Host and guest firewall rules permit only the fixed guest address to that one relay listener. All other traffic is rejected.

For the selected candidate, the only runtime service hostname is `api.openai.com`. If G7 discovers another required hostname, the candidate is blocked; this finding does not authorize widening or substituting a provider. G5 acquisition occurs into the approved host quarantine and G13 installs offline, so package, GitHub, npm, PyPI, Astral, update, trace, MCP, and model-catalog endpoints are never runtime egress.

### Secret slot

The sole candidate slot is:

```text
/run/credentials/vordar-prime-option2.service/openai-api-key
```

It is populated later by the user through the guest console after approval, exposed through systemd’s read-only credential mount, and removed when the unit stops. A root-owned launcher reads it without echoing and sets the one PRIME provider variable only in the PRIME service environment. No value enters PowerShell, Pi, `.claude`, host environment, command history, unit files, `auth.json`, logs, or evidence.

Evidence records only slot name, provider, account/project class, owner/mode, redacted presence, and lifecycle timestamps. Missing presence blocks execution. A fixture containing the value in any transcript or environment dump must fail.

### GPU boundary

No `Add-VMGpuPartitionAdapter`, DDA assignment, CUDA device, WSL GPU bridge, or local model is permitted. Later verification requires:

- no Hyper-V GPU partition adapter for the recorded VM;
- no `/dev/dxg`, `/dev/nvidia*`, or `/dev/dri/render*`;
- no CUDA/NVIDIA process;
- an attempted GPU/heavy-owner admission rejected before launch.

The basic virtual console display is not evidence of compute-GPU exposure.

### Rollback

Before PRIME acquisition, rollback is:

1. stop only `VordarPrimeOption2`;
2. remove only its Hyper-V registration;
3. remove only `VordarPrimeOption2-Internal` and its exact firewall/relay rules;
4. delete only `C:\Users\egm_8\AppData\Local\VordarPrimeOption2\`;
5. confirm the task-owned receipt lists every removed object.

After the clean golden VHDX exists, operational rollback replaces the active clone from the hash-verified golden VHDX. No checkpoint chain, WSL unregister, Docker operation, Pi change, repository edit, or VFX/content path participates.

The retained `Ubuntu` and running `docker-desktop` distributions are neither inspected nor acted upon. G3’s transcript must contain no `wsl.exe`, WSL registry write, Docker command, game/content/VFX/effects/particles path, or project-tree path.

## Candidate provider/account/model decision

### Minimal comparison

| Candidate | Current evidence | Fit |
|---|---|---|
| Prime Inference | Public documentation says token billing but defers executable model rates to authenticated data; P3 records unresolved service-specific terms and automation/commercial tension | Rejected |
| Direct Anthropic API | Commercial terms are public, but G0 did not establish a current exact executable model/rate/revision source for this campaign | Rejected |
| Direct OpenAI API | Business/developer agreement effective 2026-01-01; project-scoped service accounts; exact dated model snapshot; public token rates; Responses API exposes response IDs/status and retrieval | Selected |

### Selected candidate

- **Provider:** direct OpenAI API, provider ID `openai`
- **Account class:** business/developer API organization, one dedicated project, one project-scoped service account, not consumer OAuth
- **Model candidate:** `gpt-5.2-2025-12-11`
- **Adapter:** `openai-responses`
- **Endpoint class:** `/v1/responses`
- **Runtime hostname:** `api.openai.com`
- **Provider tools:** all disabled
- **Fallback/routing:** none
- **Local model/GPU:** none

The current model page identifies `gpt-5.2-2025-12-11` as a snapshot and displays, per 1M tokens, `$1.75` input, `$0.175` cached input, and `$14.00` output. These are current candidate evidence, not G15 execution authority.

The OpenAI Services Agreement states that the customer retains input and owns output, and that customer content is not used to improve services unless explicitly agreed. Current data documentation says API data is not used for training by default, abuse-monitoring logs may be retained up to 30 days, and stored Responses API application state is retained for at least 30 days. Responses can be retrieved by response ID. This supports later reconciliation better than the compared candidates, but does not eliminate the interval before a response ID is durably recorded. Such a request must remain `uncertain` and must not be automatically retried.

G7 must still close the exact account, project, territory, service terms, privacy/retention, output use, model availability, credential lifecycle, and whether `store:true` is acceptable. G15 must refresh and pin the exact model ID, current rates, retrieval date, calls/tokens, and dollar ceiling. If the snapshot, endpoint, rate fields, stored-response behavior, or account class cannot be fixed, the campaign blocks without provider substitution.

## Complete P2 execution-profile enumeration

“Disabled” means its effect cannot influence the selected runtime through configuration, filesystem, executable admission, credential, or network access. Mere non-use is not the mechanism.

### Entrypoints EP1–EP10

| ID | State | Enforcement | Later verification |
|---|---|---|---|
| EP1 release `prime-agent` | Enabled | Exact G6 stable bundle only; root-owned immutable prefix | Installed-tree manifest and version/commit reconciliation |
| EP2 source/package `pi` bin | Disabled | Source path absent; no `pi` command exposed in service PATH | `command -v pi` fails; no Pi-named executable in runtime PATH |
| EP3 `prime-agent.sh` | Disabled | Source checkout and `tsx` absent | Path and process-ledger absence |
| EP4 compiled Bun `dist/pi` | Disabled | Bun and binary omitted from G4 graph | Object/install manifests reject Bun or `dist/pi` |
| EP5 `pi-ai` CLI | Disabled; library remains internal | CLI bin not linked into PATH; executable admission denies direct entry | Direct invocation fails; no separate process |
| EP6 modes | Interactive/text client and daemon-backed operation enabled; `json`, `rpc`, and `acp` modes disabled | External controller allowlists the selected client/daemon path; no ACP/RPC listener | Process/socket ledger contains only selected mode |
| EP7 public commands | `agents`, `list`, `attach`, `rename`, `send`, `stop`, `status`, `doctor`, `shutdown` enabled. `schedule`, `package`, `update`, `model`, `login`, `logout`, `mcp`, `traces`, `config` disabled | Controller command allowlist; scheduled-job/config/auth/package paths denied or root-read-only; no acquisition/service egress | Invoke every disabled command against a disposable fixture; require denial or zero state change plus unchanged manifests |
| EP8 `postinstall.cjs` | Disabled | G5 resolves scripts-disabled; hook absent from execution ledger; runtime preassembled offline | Process ledger rejects lifecycle scripts; first start makes no acquisition |
| EP9 SDK/embed entry | Disabled | No embedding caller or import path outside packaged CLI | Process/import ledger contains no embedder |
| EP10 Python scripts/modules | Enabled: `agent_message`, `agent_observe`, `compact`, `goal`, `refine`, `rlm_heartbeat`. Disabled: `attach_image`, `edit`, `websearch`, `linear`, `notion` | Only enabled projects enter the locked venv and skill allowlist; disabled service credentials/egress absent | Import/entrypoint matrix: enabled succeeds offline; every disabled module/command is unavailable |

### Runtime nodes N1–N16

| ID | State | Enforcement | Later verification |
|---|---|---|---|
| N1 CLI client | Enabled | Controller-owned client, no host paths | Exact process ancestry and socket evidence |
| N2 daemon supervisor | Enabled | systemd service and private guest IPC | Start/status/shutdown and abrupt restart evidence |
| N3 catalog subprocess | Enabled | Child of N2 only | Process tree and restart-order receipt |
| N4 session worker | Enabled, one root tree | systemd/cgroup slice and admission count | More than one root is refused |
| N5 AgentSession/Agent | Enabled | Selected stable code and bounded state roots | Session and terminal-disposition evidence |
| N6 adapter/provider | Enabled only for direct OpenAI `gpt-5.2-2025-12-11` | One root-owned model entry, one credential slot, one relay hostname, no fallback | Requested/response provider+model IDs must match; substitution red |
| N7 IPython kernel | Enabled | Locked Python 3.11 environment, private loopback/IPC | Kernel lifecycle and exact venv manifest |
| N8 Linux forkserver | Enabled | Exact stable implementation, private `/run` socket | Forkserver identity, child ancestry, cleanup and fallback-fire detection |
| N9 RLM shim/selected skills | Enabled only for EP10 allowlist | Locked venv and root-owned skill manifest | Import and process ledger |
| N10 RLM child AgentSession | Enabled, maximum depth 1 and one active child | External admission plus cgroup/task limits | Second/deeper child refused |
| N11 shell/tool subprocess tree | Enabled but guest-confined | No host mount/default route; immutable executable set; cgroup/AppArmor descendants | Attempt host path, dynamic acquisition, escape, and orphan; all denied/reaped |
| N12 MCP/HTTP service | Disabled, including Linear, Notion, custom MCP | No MCP package/credential/config; E8 denied; only OpenAI relay exists | MCP catalog empty; connection and Notion fixture red |
| N13 continual refine | Enabled only by explicit manual local/global request; automatic refine disabled | Root-owned setting disables auto trigger; no background refinement admission | No refine without registered operation; explicit refine emits exact ID |
| N14 telemetry/logging | Local bounded logs enabled; Prime trace upload disabled | Trace setting off, no trace credential/hostname, E14 denied | Local logs exist; upload attempt denied |
| N15 installer/updater | Disabled | Installer absent; `/opt` read-only; channels unreachable; update/config writes denied | Installer/update process fixture red; runtime tree unchanged |
| N16 sandbox/container | Disabled/not applicable | No Docker socket, binary, image, bubblewrap extension, sandbox package, or Prime platform service | Container/socket/image scan empty; attempted Docker access denied |

### Process/service edges E1–E16

| Edge | State | Enforcement and later check |
|---|---|---|
| E1 N1→N2 local JSONL socket | Enabled | Private `/run` socket; verify permissions, cursor outcome, and restart |
| E2 N2→N4 private framed socket | Enabled | Private guest IPC/token; verify generation fencing and adoption |
| E3 N2→N3 spawn/pipe | Enabled | N2-only child; kill fixture must fail catalog request and restart in order |
| E4 N4→N5 in-process | Enabled | Stable bundle only; worker-death fixture must expose disposition |
| E5 N5/N10→N6 inference | Enabled only for selected OpenAI snapshot | One credential and relay; provider/model/hostname substitution rejected |
| E6 N5→N7 Jupyter | Enabled | Loopback/private temp only; inspect five ephemeral sockets and cleanup |
| E7 N7→N5 host calls | Enabled for selected RLM modules | Typed call allowlist; unlisted host call rejected |
| E8 N7→N12 MCP | Disabled | N12 absent, no credential or egress; direct and configured MCP probes fail |
| E9 N5→N10 child admission | Enabled with depth/count ceiling | Second/deeper/concurrent child probe rejected |
| E10 N5/N7→N11 subprocess | Enabled inside guest boundary | AppArmor/cgroup/mount/network constraints; escape/acquisition/orphan probes red |
| E11 N5→N13 refine | Enabled only for explicit registered operation | Auto trigger disabled; unregistered refine rejected |
| E12 N13→P3 harness | Enabled | Exact local/global paths; state/history bytes hashed before and after |
| E13 N4→P2 persistence | Enabled | Guest-local persistent state only; torn/corrupt fixtures preserve bytes and block silence |
| E14 N4→N14 trace upload | Disabled | Trace config/credential absent and hostname unreachable; upload probe denied |
| E15 N15→EP1 replacement | Disabled | N15 absent, `/opt` immutable, no release/network path; changed-byte fixture red |
| E16 N15→N2 update restart | Disabled | No update manifest/coordinator; injected update checkpoint rejected |

### Persistence stores P1–P8

| Store | State | Enforcement and later check |
|---|---|---|
| P1 config/auth/resources | Root-owned settings/model/skill manifests enabled; on-disk `auth.json`, project resources, extensions, themes and package roots disabled | Verify immutable config hashes, absent auth value, and rejected writes |
| P2 sessions/artifacts | Enabled under `/var/lib/vordar-prime-option2/home/.prime/agent/` | Hash exact restart-consumed bytes; torn-tail fixture red |
| P3 harness/refine | Enabled for explicit local/global refinement | Hash state/history/session links; split-publication fixtures red |
| P4 daemon control | Enabled | Fsynced journal and descriptor identities retained; same-ID cases checked |
| P5 queues/schedules | Live queues enabled; schedules disabled | Deny `scheduled-jobs.json`; no scheduled process/tick after restart |
| P6 goals/child registry | Enabled for the bounded child path | Parent/child IDs and artifacts joined; orphan/missing registry red |
| P7 logs/traces | Local rotated logs enabled; remote traces disabled | Quota/rotation measured; no remote request |
| P8 kernel/tool temp | Enabled only in private `/run/vordar-prime-option2/` and private work temp | `PrivateTmp`, no `pi-extensions`, no host temp; stale socket/process cleanup verified |

### Acquisition/runtime classes

| Class | Profile disposition |
|---|---|
| Four stable PRIME 0.7.0 release packages | Enabled only after G4–G6 exact-byte closure |
| Root/source npm workspace and developer graph | Disabled |
| Shipped npm transitive runtime | Enabled only as exact G4/G5 objects; no ranges remain |
| Node | Enabled at one exact G4 version satisfying `>=22.8.0` |
| npm | Assembly-only, exact version; unavailable to operational PRIME |
| Python 3.11, uv, wheels, build backends | Enabled only as exact offline G4/G5 objects; uv/build tooling unavailable operationally |
| Selected Python skills | Enabled only as EP10 allowlist |
| Managed `fd`/`rg` from `releases/latest` | Disabled; mutable helper download unreachable |
| Packages/extensions/git/local capability acquisition | Disabled |
| Prime platform skill/CLI/services | Disabled |
| Bun/source build/test/benchmark/CI tools | Disabled |
| Docker, OCI, Compose, remote sandbox | Disabled/not applicable |
| Local model server/weights | Disabled |
| Updates/version checks/catalog regeneration | Disabled |
| Beta release/assets/commit | Globally rejected |

### Provider and adapter closure

Enabled provider ID: `openai`.

Disabled provider IDs: `amazon-bedrock`, `anthropic`, `azure-openai-responses`, `cerebras`, `cloudflare-ai-gateway`, `cloudflare-workers-ai`, `deepseek`, `fireworks`, `github-copilot`, `google`, `google-vertex`, `groq`, `huggingface`, `kimi-coding`, `minimax`, `minimax-cn`, `mistral`, `moonshotai`, `moonshotai-cn`, `openai-codex`, `opencode`, `opencode-go`, `openrouter`, `prime-inference`, `vercel-ai-gateway`, `xai`, `xiaomi`, `xiaomi-token-plan-ams`, `xiaomi-token-plan-cn`, `xiaomi-token-plan-sgp`, and `zai`.

Enabled adapter: `openai-responses`.

Disabled adapters: `anthropic-messages`, `openai-completions`, `mistral-conversations`, `azure-openai-responses`, `openai-codex-responses`, `google-generative-ai`, `google-vertex`, and `bedrock-converse-stream`.

Enforcement is one root-owned model entry, no custom `models.json`, no OAuth, one provider credential slot, one relay hostname, and a startup assertion that the effective provider/model/adapter tuple is exact. Later verification mutates each tuple field and requires refusal before a request.

## Exact G3 approval packet

Approval of this packet authorizes guest provisioning only, not PRIME/runtime acquisition or execution.

### Object and network quantity

| Object | Bytes |
|---|---:|
| Ubuntu ISO | `3,405,469,696` |
| `SHA256SUMS` | `594` |
| `SHA256SUMS.gpg` | `833` |
| **Expected HTTP body total** | **`3,405,471,123`** |

Protocol overhead is not part of file-body size. The approved transfer must stop if body size exceeds the listed object size or redirects outside `releases.ubuntu.com`.

### Guest and host ceilings

- VM name: `VordarPrimeOption2`
- Generation: 2
- CPU: 4 vCPUs; PRIME slice `CPUQuota=300%`
- RAM: fixed 8 GiB; Dynamic Memory off; PRIME `MemoryMax=6G`, swap off
- Guest VHDX: dynamic, maximum 32 GiB
- Worst-case host disk reservation:
  - active VHDX: 32 GiB;
  - clean golden VHDX: 32 GiB;
  - ISO/checksum material: under 3.18 GiB;
  - configuration/transcript headroom: under 2.82 GiB;
  - **hard approval ceiling: 70 GiB**
- G1 free-space basis: `181652307968` bytes
- GPU: zero assigned compute adapters
- Network: one new internal switch, no NAT/default route
- Wall estimate: 2.5 hours expected; **4 wall-hours hard approval ceiling**
- Provider calls/credentials/GPU work: zero

### Host/global impact

G3 requires administrative Hyper-V operations, one VM registration, one internal virtual switch, fixed RAM while the VM is running, CPU scheduling for four vCPUs, up to 70 GiB task-owned host storage, and the displayed public download. It does not change WSL settings, start/stop/register/unregister a WSL distribution, invoke Docker, alter Pi, inspect or touch the concurrent VFX/effects/particles work, or edit either repository.

If Hyper-V cmdlets, Generation-2 boot, Secure Boot with the Microsoft UEFI Certificate Authority template, storage, or the exact external turn-off operation fail on this host, G3 returns blocked. It does not retry using WSL2 or another image.

## RED-proof mapping

| Claim | Required RED mutation and expected failure |
|---|---|
| Platforms remain distinct | Replace Hyper-V fields with WSL fields or include `wsl.exe` in the selected recipe → `TARGET_MERGED` |
| External abrupt boundary | Remove `-TurnOff`, use wildcard VM selection, or mismatch recorded `VMId` → `NO_POWER_CUT_EQUIVALENT` |
| Immutable image | Alter one ISO byte, size, endpoint, checksum, signature, seed, installed manifest, or golden VHDX → `IMAGE_IDENTITY_MISMATCH` |
| Offline provisioning | Record any installer/package network destination → `MUTABLE_INSTALL_PATH` |
| Resource ceiling | Configure more than 4 vCPU, 8 GiB RAM, 32 GiB guest disk, 70 GiB host disk, or any GPU adapter → `RESOURCE_ENVELOPE_EXCEEDED` |
| P2 completeness | Remove any EP1–EP10, N1–N16, E1–E16, P1–P8, provider ID, or adapter disposition → `PROFILE_NODE_OR_EDGE_MISSING` |
| Disabled edge | Mark disabled without configuration/filesystem/executable/credential/network enforcement and a later probe → `DISABLE_NOT_ENFORCED` |
| Stable baseline | Insert release ID `355959266`, beta tag/commit, another commit/tree, `latest`, or mutable installer → `UNAUTHORIZED_BASELINE` |
| Node floor | Select or install Node below `22.8.0` → `NODE_FLOOR_VIOLATION` |
| Provider identity | Change provider, account class, model, adapter, hostname, or enable fallback → `PROVIDER_PROFILE_SUBSTITUTION` |
| Secret boundary | Place a credential value in host/Pi environment, file, command, transcript, or log → `SECRET_LEAK` |
| Host isolation | Expose any Vordar/Pi/host path, shared temp, host process channel, or unrestricted route → `HOST_BOUNDARY_OPEN` |
| Existing WSL/Docker | Invoke a WSL/Docker lifecycle/configuration command or write their storage/registration paths → `EXISTING_GUEST_TOUCHED` |
| GPU denial | Add a GPU partition/DDA adapter or expose a compute device → `GPU_VISIBLE` |
| No fallback | On selected-target or provider failure, attempt WSL2, another VM, provider, model, image, or revision → `FALLBACK_FORBIDDEN` |

The intact decision is green only when all required identifiers are present, every negative fixture fails for its named reason, and the selected tuple is exactly:

```text
Hyper-V Generation 2
Ubuntu Server 24.04.4 AMD64
VordarPrimeOption2
OpenAI business/developer API project service account
openai / openai-responses / gpt-5.2-2025-12-11
```

## Assumptions and blocking risks

- G1 demonstrates an active hypervisor and enabled Hyper-V hypervisor feature, but did not execute Hyper-V cmdlets. G3 owns the first approved creation test.
- Ubuntu’s endpoint is mutable; only the independently computed approved digest and retained signed metadata count.
- The 8 GiB/4-vCPU/32-GiB envelope is a hard qualification ceiling, not a measured minimum. If the locked runtime cannot operate within it, the target blocks.
- Hyper-V host overhead beyond configured guest memory is not measured here and must be recorded by G3/G11 without enlarging the approved envelope.
- OS package rights, PRIME provenance, transitive packages, and the selected OpenAI profile remain G7 closure work.
- Stored OpenAI responses improve post-ID reconciliation but cannot prove the outcome of a request whose response ID was never durably observed. Such work remains `uncertain`.
- The selected model’s current availability and rates can drift. G15 must refresh and pin them; drift blocks rather than substitutes.
- WSL2 qualification, phase-2 planning, adoption, Vordar exposure, visual work, and the unresolved launch-revision binding remain outside this decision.

## Primary sources

### Repository evidence

- `.claude/tasks/prime-agent-option2-gate-closing-plan.md`
- `.claude/docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md`
- `.claude/docs/research/prime-agent/option-2-gate-closing/01-host-platform-inventory/raw.json`
- `.claude/docs/research/prime-agent/option-2-gate-closing/01-host-platform-inventory/commands.json`
- `.claude/docs/research/prime-agent/phase-1/02-component-runtime-closure.md`
- `.claude/docs/research/prime-agent/phase-1/03-license-weights-service-closure.md`
- `.claude/docs/research/prime-agent/phase-1/04-learning-persistence-dataflow.md`
- `.claude/docs/research/prime-agent/phase-1/05-observability-replay-failures.md`
- `.claude/docs/research/prime-agent/phase-1/07-platform-gpu-vram.md`
- `.claude/docs/research/prime-agent/phase-1/08-pricing-operations.md`
- `.claude/docs/research/prime-agent/phase-1/10-vordar-boundary-synthesis.md`

### Current public primary documentation

- Ubuntu 24.04.4 release objects: <https://releases.ubuntu.com/24.04/>
- Ubuntu checksums: <https://releases.ubuntu.com/24.04/SHA256SUMS>
- Hyper-V VM creation: <https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/create-a-virtual-machine-in-hyper-v>
- Hyper-V abrupt turn-off: <https://learn.microsoft.com/en-us/powershell/module/hyper-v/stop-vm?view=windowsserver2025-ps>
- WSL commands and termination: <https://learn.microsoft.com/en-us/windows/wsl/basic-commands>
- WSL global/per-distribution configuration: <https://learn.microsoft.com/en-us/windows/wsl/wsl-config>
- Windows optional-feature state values: <https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-optionalfeature>
- OpenAI GPT-5.2 snapshot and rates: <https://developers.openai.com/api/docs/models/gpt-5.2>
- OpenAI Responses retrieval: <https://developers.openai.com/api/reference/resources/responses/methods/retrieve/>
- OpenAI API data controls and retention: <https://developers.openai.com/api/docs/guides/your-data>
- OpenAI project/service-account scope: <https://help.openai.com/en/articles/9186755-managing-your-work-in-the-api-platform-with-projects>
- OpenAI Services Agreement, effective 2026-01-01: <https://openai.com/policies/business-terms/>

TARGET SELECTED
