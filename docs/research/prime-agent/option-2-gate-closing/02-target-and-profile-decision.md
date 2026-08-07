# G2 — Target and Minimal Execution-Profile Decision

## Run record

- **Model seat:** Sol analysis
- **Type:** finding correction
- **Deliverable:** complete replacement body for `.claude/docs/research/prime-agent/option-2-gate-closing/02-target-and-profile-decision.md`
- **Scope:** Current G2, campaign-plan G3, G0/G1, and current public Ubuntu, cloud-init, and Hyper-V primary documentation.
- **Do not touch or decide:** No probe, download, setup, VM/WSL/Docker lifecycle, GPU/process workload, credential access, repository edit, provider substitution, fallback, baseline change, game/VFX access, or concurrent work.
- **Verification criterion:** Luna must have a deterministic, offline, noninteractive G3 recipe using only approved or measured mechanisms; every input and signer must have exact identity and bytes; receipt export must require neither a host-folder mount nor a secret; quantities must be exact. Any unapproved tool, unmeasured helper, credential, interactive step, package installation, or weakened boundary blocks.
- **Retrieval date:** 2026-08-07

## Verdict

The selected candidate remains a dedicated Ubuntu Server 24.04.4 LTS AMD64 Generation-2 Hyper-V VM named `VordarPrimeOption2`. WSL2 is not a fallback and may not be invoked.

The provider/profile candidate remains:

```text
OpenAI business/developer API project service account
openai / openai-responses / gpt-5.2-2025-12-11
api.openai.com
no fallback
```

This candidate is **not implementation-ready for G3**. The current approval packet requires cryptographic verification of `SHA256SUMS.gpg`, but neither G0, G1, nor G2 supplies or approves:

1. the exact public-key object bytes used as the verification trust anchor; or
2. an exact OpenPGP verifier and its complete executable/runtime identity.

Ubuntu’s primary verification procedure requires an OpenPGP implementation and runs `gpg --verify SHA256SUMS.gpg SHA256SUMS`. Windows PowerShell’s measured `Get-FileHash` use in G1 can compute SHA-256 but does not verify an OpenPGP detached signature. G1 did not measure `gpg`, `gpgv`, another OpenPGP verifier, or an equivalent approved verifier object. Their absence is not inferred; their presence and immutable identity are `UNKNOWN`.

The task contract requires failure on an unmeasured helper and prohibits adding an unapproved tool. Consequently Luna cannot execute the first image-authentication step deterministically. No VM creation, seed construction, boot, or fallback is authorized.

## Retained immutable baseline

The PRIME baseline remains exactly:

- version `v0.7.0`;
- commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`;
- tree `0625a8fd0550a8de7ff05e8d9248e75563e5b520`;
- Node floor `>=22.8.0`;
- beta release ID `355959266`, tag `beta`, and commit `b9a4461149419156599d60174dddf15458e2b9ee` prohibited;
- no mutable installer, update channel, Docker dependency, local model, local GPU, compatibility shim, or fallback.

G0 ends `FRESH`. G1 records:

- Windows 11 Pro `10.0.26200`, UBR `8973`;
- 20 logical CPUs and `34,134,220,800` bytes RAM;
- an active hypervisor and enabled `Microsoft-Hyper-V-Hypervisor`;
- `181,652,307,968` free bytes on the candidate storage volume;
- existing `Ubuntu` and `docker-desktop` WSL registrations that must remain untouched;
- no guest entry/start, termination command, configuration change, Docker workload, or GPU workload;
- raw inventory SHA-256 `a922eb4e76f88e35228004afd627092655f96b9d7e311e67ae5e4b2e49c8a3f4`.

G1 did not test Hyper-V cmdlet availability, Secure Boot template availability, OpenPGP helpers, unattended installer behavior, or receipt transport.

## Candidate target retained without provisioning authorization

- **OS:** Ubuntu Server 24.04.4 LTS AMD64, no GUI
- **VM:** `VordarPrimeOption2`
- **Hypervisor:** Hyper-V
- **Generation:** 2
- **Abrupt-loss command:**

```powershell
Stop-VM -Name 'VordarPrimeOption2' -TurnOff -Confirm:$false
```

The controller must first bind both the exact VM name and recorded `VMId`. A missing VM, name/ID mismatch, wildcard selection, or command without `-TurnOff` fails. Microsoft documents `Stop-VM -TurnOff` as equivalent to disconnecting power.

Failure blocks the campaign. It does not authorize WSL2, another image, another VM provider, or manual provisioning.

## Ubuntu installation-object identity

| Field | Required value |
|---|---|
| Object | `ubuntu-24.04.4-live-server-amd64.iso` |
| URL | `https://releases.ubuntu.com/24.04/ubuntu-24.04.4-live-server-amd64.iso` |
| Size | `3,405,469,696` bytes |
| SHA-256 | `e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433` |
| Checksum object | `https://releases.ubuntu.com/24.04/SHA256SUMS` |
| Checksum size | `594` bytes |
| Signature object | `https://releases.ubuntu.com/24.04/SHA256SUMS.gpg` |
| Signature size | `833` bytes |
| Signature issuer fingerprint | `843938DF228D22F7B3742BC0D94AA3F0EFE21092` |
| Signer UID | `Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>` |

The fingerprint is exact: it is carried by the current detached signature and matches Ubuntu’s documented CD-image signing identity. It does not by itself supply a trust anchor.

### Unclosed signing-key bytes

Potential public sources include Ubuntu’s keyserver and the Ubuntu archive keyring, but the present G2 packet does not pin one exact response body by:

- URL;
- byte count;
- independently recorded SHA-256;
- exact exported packet set;
- signer fingerprint derived from those bytes; and
- approval as a G3 input object.

A keyserver lookup is mutable and can include certifications beyond the requested primary key. The archive keyring contains multiple keys. Neither may be reduced or selected manually during G3.

### Unclosed verifier

No approved G3 object provides:

- an OpenPGP verifier executable;
- its exact version, source, bytes, digest, dependencies, and license;
- an exact invocation that rejects an unexpected signer, additional valid signer, weak/different digest, malformed data, or signature over different checksum bytes.

A hash comparison against a value copied into this finding is not a substitute for the promised signature verification.

## Corrected object and quantity ledger

### Currently identified public objects

| Object | Count | Bytes |
|---|---:|---:|
| Ubuntu ISO | 1 | `3,405,469,696` |
| `SHA256SUMS` | 1 | `594` |
| `SHA256SUMS.gpg` | 1 | `833` |
| **Known subtotal** | **3** | **`3,405,471,123`** |

### Additional mandatory inputs

| Requirement | Minimum count | Bytes | Status |
|---|---:|---:|---|
| Exact signing-key object | 1 | `UNKNOWN` | Not selected, pinned, or approved |
| Exact OpenPGP verifier distribution | At least 1 | `UNKNOWN` | Not measured, manifested, or approved |
| Verifier runtime/dependencies | `UNKNOWN` | `UNKNOWN` | Not recursively enumerated |
| Autoinstall `user-data` | 1 generated object | `UNKNOWN` | Exact bytes not settled |
| NoCloud `meta-data` | 1 generated object | `UNKNOWN` | Exact bytes not settled |
| Seed carrier VHD/VHDX | 1 generated object | `UNKNOWN` | Exact byte identity not settled |
| Guest receipt | 1 generated object | `UNKNOWN` | Exact schema/export protocol not settled |
| Host receipt listener/controller | At least 1 generated object | `UNKNOWN` | Exact implementation not settled |

Therefore:

- exact public download object count: **at least 5**, final count `UNKNOWN`;
- exact approved HTTP body total: **greater than `3,405,471,123` bytes**, final total `UNKNOWN`;
- generated provisioning object count: **at least 5**, final count `UNKNOWN`;
- exact storage total and hard approval ceiling: **not computable from closed objects**.

The previous three-object, `3,405,471,123`-byte packet is incomplete and cannot authorize G3.

## Offline unattended provisioning status

Ubuntu documents NoCloud seed media containing `user-data` and `meta-data` on a filesystem labeled `CIDATA`. Ubuntu also documents that truly zero-touch Subiquity installation requires `autoinstall` on the kernel command line to bypass the destructive-action confirmation.

A possible seed carrier can be created with Windows/Hyper-V storage mechanisms and attached as a second virtual disk, but that alone does not establish how the unmodified Ubuntu ISO receives the required `autoinstall` kernel argument.

The current packet does not approve or specify any deterministic mechanism to:

1. inject that kernel argument before the installer starts;
2. remaster and re-sign the ISO;
3. synthesize boot keystrokes without timing or visual judgment; or
4. use a prebuilt cloud image proven compatible with the selected Gen2/Secure-Boot profile.

Interactive GRUB editing, VMConnect keystrokes, timed key injection, visual confirmation, ISO remastering with an unapproved authoring tool, network boot, package installation, or image substitution is forbidden.

This is an independent downstream blocker, but it is not reached because image-signature verification fails first.

## Seed, bootstrap, and receipt requirements not credited as closed

Any later corrected recipe would have to pin exact bytes for all of the following before Luna execution:

### NoCloud identity

- volume label exactly `CIDATA`;
- root files exactly `user-data` and `meta-data`;
- fixed `instance-id`;
- fixed `local-hostname`;
- top-level cloud-config `autoinstall` key;
- exact autoinstall schema version;
- update/refresh, SSH acquisition, third-party repository, snap refresh, and package-network paths disabled;
- NIC disconnected from external networks throughout installation.

### Credential-free bootstrap

- no plaintext or reusable password;
- no SSH authorized key;
- no host credential;
- no user-console secret;
- root login disabled;
- any bootstrap account locked;
- no passwordless interactive administrative account;
- all required G3 actions performed by installer/cloud-init directives already present in the approved seed.

An identity password hash, temporary password, manually typed console value, SSH key, or host secret would violate the boundary.

### Receipt export

Receipt export may not use:

- a host-folder mount;
- Hyper-V Guest Service file copy;
- enhanced-session drive sharing;
- clipboard transfer;
- SSH/SCP credential;
- Pi state;
- host environment secrets;
- guest credential;
- manual transcription.

An internal-switch, guest-initiated one-shot receipt transfer could satisfy the topology only after its listener, protocol, destination address, schema, byte limit, timeout, replay behavior, and red fixtures are exact and approved. Those details are not present.

## Hyper-V order and parameter requirements not credited as closed

A future executable recipe would have to bind and preflight exact identities for every required cmdlet before mutation, including at minimum:

- `New-VMSwitch`;
- `New-VHD`;
- `New-VM`;
- `Set-VM`;
- `Set-VMMemory`;
- `Set-VMProcessor`;
- `Set-VMFirmware`;
- `Add-VMDvdDrive`;
- `Add-VMHardDiskDrive`;
- `Connect-VMNetworkAdapter`;
- `Disconnect-VMNetworkAdapter`;
- `Start-VM`;
- `Stop-VM`;
- `Remove-VM`;
- `Remove-VMSwitch`;
- `Get-VM`;
- `Get-VMFirmware`;
- `Get-VMNetworkAdapter`;
- `Get-VMHardDiskDrive`;
- `Get-VMDvdDrive`.

The intended order remains:

1. authenticate all public image objects;
2. validate exact storage and object totals;
3. preflight cmdlets and Secure Boot template without mutation;
4. create the task root and rollback journal;
5. create the isolated internal switch;
6. create the 32-GiB dynamic VHDX;
7. create the Generation-2 VM with fixed 8-GiB RAM;
8. set four virtual processors and disable Dynamic Memory;
9. disable automatic checkpoints;
10. set automatic start to `Nothing` and stop to `ShutDown`;
11. enable Secure Boot with template `MicrosoftUEFICertificateAuthority`;
12. attach the authenticated installer ISO and exact seed carrier;
13. set DVD as first boot device for installation;
14. prove no external switch, NAT, default route, host share, GPU partition, DDA device, or Guest Service Interface;
15. start unattended installation;
16. receive the bounded non-secret receipt over the isolated path;
17. shut down cleanly;
18. detach installer and seed media;
19. set the installed VHDX first in firmware boot order;
20. boot once for receipt verification;
21. shut down cleanly;
22. hash the clean golden VHDX;
23. create an operational clone;
24. execute red checks;
25. retain exact rollback inventory.

The host has not been probed for these cmdlets or the named Secure Boot template. Their presence must not be assumed.

## Retained boundary profile

### Host placement

All task-owned VM material remains confined to:

```text
C:\Users\egm_8\AppData\Local\VordarPrimeOption2\
```

No Vordar, `.claude`, Pi, WSL, Docker, game, content, VFX, effects, or particles path may be read, mounted, copied, or modified.

No host directory is mounted into the VM. Guest Service Interface, drive sharing, clipboard/file redirection, enhanced-session sharing, automatic checkpoints, GPU partitioning, and discrete-device assignment remain disabled.

### Guest paths

| Path | Purpose |
|---|---|
| `/opt/vordar-prime-option2/runtime/<manifest-sha256>/` | Root-owned immutable G6 runtime |
| `/var/lib/vordar-prime-option2/home/` | Fixed PRIME home and global state |
| `/var/lib/vordar-prime-option2/state/` | Recovery journals and dispositions |
| `/srv/vordar-prime-option2/work/` | Only working-data root |
| `/var/log/vordar-prime-option2/` | Local bounded logs |
| `/run/vordar-prime-option2/` | Private transient IPC/temp |
| `/run/credentials/vordar-prime-option2.service/` | Future systemd credential mount; no G3 value |

`/home`, `/mnt`, `/media`, `/workspace`, `/vordar`, host-drive paths, Pi paths, Docker sockets, and shared temp remain outside the service mount namespace.

### Resource profile

- 4 virtual processors;
- fixed 8 GiB RAM;
- Dynamic Memory disabled;
- one dynamic VHDX with 32-GiB virtual maximum;
- no nested virtualization;
- no automatic checkpoints;
- no GPU assignment;
- PRIME slice: `MemoryMax=6G`, `MemorySwapMax=0`, `CPUQuota=300%`, `TasksMax=512`.

The prior 70-GiB host ceiling is not reauthorized because the mandatory verifier/key/seed/receipt object totals are incomplete.

### Network profile

- one dedicated internal switch: `VordarPrimeOption2-Internal`;
- fixed host/guest `/30`;
- no external-switch attachment;
- no NAT;
- no default route;
- no guest DNS server;
- no inbound forwarding;
- no LAN/service access during G3.

Later provider execution remains limited to a separately approved host relay for `api.openai.com:443`. G3 authorizes no provider traffic.

### Secret profile

G3 creates or reads no credential value. The future sole provider slot remains:

```text
/run/credentials/vordar-prime-option2.service/openai-api-key
```

No value may enter PowerShell, Pi, `.claude`, host environment, command history, unit files, `auth.json`, logs, or evidence.

### GPU profile

No `Add-VMGpuPartitionAdapter`, DDA assignment, CUDA device, WSL GPU bridge, local model, or GPU workload is permitted.

### Rollback profile

Rollback may remove only:

- VM registration `VordarPrimeOption2` after matching recorded `VMId`;
- switch `VordarPrimeOption2-Internal`;
- exact task-owned firewall/listener rules;
- `C:\Users\egm_8\AppData\Local\VordarPrimeOption2\`.

No WSL, Docker, Pi, repository, game, content, or VFX operation participates.

## Complete retained P2 disposition

### Entrypoints EP1–EP10

| ID | State |
|---|---|
| EP1 | Stable release `prime-agent` enabled only from exact G6 bytes |
| EP2 | Source/package `pi` bin disabled |
| EP3 | `prime-agent.sh` disabled |
| EP4 | Bun `dist/pi` disabled |
| EP5 | `pi-ai` CLI disabled; library internal only |
| EP6 | Interactive/text and daemon-backed paths enabled; JSON/RPC/ACP disabled |
| EP7 | `agents`, `list`, `attach`, `rename`, `send`, `stop`, `status`, `doctor`, `shutdown` enabled; `schedule`, `package`, `update`, `model`, `login`, `logout`, `mcp`, `traces`, `config` disabled |
| EP8 | `postinstall.cjs` disabled |
| EP9 | SDK/embed entry disabled |
| EP10 | `agent_message`, `agent_observe`, `compact`, `goal`, `refine`, `rlm_heartbeat` enabled; `attach_image`, `edit`, `websearch`, `linear`, `notion` disabled |

### Runtime nodes N1–N16

| ID | State |
|---|---|
| N1 | CLI client enabled |
| N2 | Daemon supervisor enabled |
| N3 | Catalog subprocess enabled |
| N4 | One session-worker root enabled |
| N5 | AgentSession/Agent enabled |
| N6 | Only `openai/openai-responses/gpt-5.2-2025-12-11` candidate enabled |
| N7 | Locked Python 3.11 IPython kernel enabled |
| N8 | Linux forkserver enabled |
| N9 | Selected RLM shim/skills enabled |
| N10 | One depth-1 child AgentSession enabled |
| N11 | Guest-confined shell/tool subprocess tree enabled |
| N12 | MCP/HTTP services disabled |
| N13 | Explicit registered refine only; automatic refine disabled |
| N14 | Local bounded logging enabled; trace upload disabled |
| N15 | Installer/updater disabled |
| N16 | Docker/container/sandbox path disabled |

### Edges E1–E16

| ID | State |
|---|---|
| E1 | N1→N2 private JSONL socket enabled |
| E2 | N2→N4 private framed socket enabled |
| E3 | N2→N3 spawn/pipe enabled |
| E4 | N4→N5 in-process enabled |
| E5 | N5/N10→N6 enabled only for selected provider tuple |
| E6 | N5→N7 Jupyter enabled |
| E7 | N7→N5 selected host calls enabled |
| E8 | N7→N12 MCP disabled |
| E9 | N5→N10 enabled within depth/count ceiling |
| E10 | N5/N7→N11 enabled inside guest boundary |
| E11 | N5→N13 explicit registered refine only |
| E12 | N13→P3 harness enabled |
| E13 | N4→P2 persistence enabled |
| E14 | N4→N14 trace upload disabled |
| E15 | N15→EP1 replacement disabled |
| E16 | N15→N2 update restart disabled |

### Persistence P1–P8

| ID | State |
|---|---|
| P1 | Root-owned selected settings/model/skill manifests only; auth, extensions, themes, package roots disabled |
| P2 | Guest-local sessions/artifacts enabled |
| P3 | Explicit local/global refinement state enabled |
| P4 | Daemon-control journal enabled |
| P5 | Live queues enabled; schedules disabled |
| P6 | Bounded child registry enabled |
| P7 | Local rotated logs enabled; remote traces disabled |
| P8 | Private `/run` and work temp only |

### Acquisition/runtime classes

| Class | Disposition |
|---|---|
| Stable PRIME 0.7.0 release packages | Enabled only after G4–G6 closure |
| Source npm workspace/developer graph | Disabled |
| npm transitive runtime | Exact G4/G5 objects only |
| Node | One exact version satisfying `>=22.8.0` |
| npm | Assembly-only; unavailable operationally |
| Python/uv/wheels/build backends | Exact offline objects only |
| Selected Python skills | EP10 allowlist only |
| Managed `fd`/`rg` from `latest` | Disabled |
| Package/extension/git/local acquisition | Disabled |
| Prime platform products | Disabled |
| Bun/build/test/benchmark/CI tools | Disabled |
| Docker/OCI/Compose/remote sandbox | Disabled |
| Local model/weights | Disabled |
| Updates/version checks/catalog regeneration | Disabled |
| Beta release/assets/commit | Rejected |

### Provider and adapter closure

Enabled provider candidate: `openai`.

Enabled adapter candidate: `openai-responses`.

All other provider IDs and adapters remain disabled by construction. No custom `models.json`, OAuth, fallback, alternate hostname, or routing substitution is allowed.

## RED-proof requirements

| Claim | Required failure |
|---|---|
| Signer identity | Different key fingerprint or unpinned key bytes → `IMAGE_SIGNER_MISMATCH` |
| Verifier identity | Missing, unmeasured, changed, or network-installed verifier → `UNAPPROVED_VERIFIER` |
| Image identity | Changed ISO/checksum/signature/key byte, size, URL, or digest → `IMAGE_IDENTITY_MISMATCH` |
| Zero-touch install | Confirmation prompt, VMConnect input, timed key injection, or visual judgment → `INTERACTIVE_PROVISIONING` |
| Seed identity | Changed/missing `CIDATA`, `user-data`, `meta-data`, instance ID, or seed digest → `SEED_IDENTITY_MISMATCH` |
| Credential-free bootstrap | Password, SSH key, console secret, or host secret required → `BOOTSTRAP_CREDENTIAL_REQUIRED` |
| Receipt export | Host mount, Guest Service copy, secret, manual transcription, or unbounded payload → `RECEIPT_BOUNDARY_OPEN` |
| Secure Boot | Wrong/absent template, disabled Secure Boot, or unmeasured template substitution → `SECURE_BOOT_PROFILE_MISMATCH` |
| Network | External switch, NAT, default route, DNS, LAN, or package destination → `MUTABLE_INSTALL_PATH` |
| Resource envelope | More than 4 vCPU, 8 GiB RAM, 32-GiB VHDX, or any GPU → `RESOURCE_ENVELOPE_EXCEEDED` |
| Existing guests | Any WSL/Docker lifecycle or configuration command → `EXISTING_GUEST_TOUCHED` |
| Stable baseline | Beta, mutable installer, `latest`, or another PRIME revision → `UNAUTHORIZED_BASELINE` |
| No fallback | WSL2, alternate image, VM provider, provider, model, or adapter attempt → `FALLBACK_FORBIDDEN` |
| Profile completeness | Missing EP/N/E/P or disabled-path enforcement → `PROFILE_NODE_OR_EDGE_MISSING` |

## Assumptions and risks

- The exact Ubuntu signer fingerprint is established, but fingerprint identity is not equivalent to approved trust-anchor bytes.
- G1’s lack of OpenPGP-helper evidence means `UNKNOWN`, not proven absence.
- Hyper-V enablement does not prove the required cmdlets or Secure Boot template are available.
- A NoCloud seed disk does not itself suppress Subiquity’s destructive-action confirmation.
- No downstream recipe, total, or green check may be credited while the first authentication dependency is unresolved.
- No fallback is permitted.

## Primary evidence

### Repository

- `.claude/tasks/prime-agent-option2-gate-closing-plan.md`, G2/G3
- `.claude/docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md`
- `.claude/docs/research/prime-agent/option-2-gate-closing/01-host-platform-inventory/raw.json`
- `.claude/docs/research/prime-agent/option-2-gate-closing/01-host-platform-inventory/commands.json`
- `.claude/docs/research/prime-agent/phase-1/02-component-runtime-closure.md`
- `.claude/docs/research/prime-agent/phase-1/10-vordar-boundary-synthesis.md`

### Public primary documentation

- Ubuntu 24.04 release objects: <https://releases.ubuntu.com/24.04/>
- Ubuntu checksums: <https://releases.ubuntu.com/24.04/SHA256SUMS>
- Ubuntu signature: <https://releases.ubuntu.com/24.04/SHA256SUMS.gpg>
- Ubuntu download verification: <https://ubuntu.com/tutorials/how-to-verify-ubuntu>
- Ubuntu zero-touch autoinstall: <https://canonical-subiquity.readthedocs-hosted.com/en/latest/explanation/zero-touch-autoinstall.html>
- Ubuntu autoinstall configuration delivery: <https://canonical-subiquity.readthedocs-hosted.com/en/latest/tutorial/providing-autoinstall.html>
- Cloud-init NoCloud datasource: <https://cloudinit.readthedocs.io/en/latest/reference/datasources/nocloud.html>
- Hyper-V cmdlets: <https://learn.microsoft.com/en-us/powershell/module/hyper-v/>
- Hyper-V firmware configuration: <https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmfirmware?view=windowsserver2025-ps>
- Hyper-V abrupt turn-off: <https://learn.microsoft.com/en-us/powershell/module/hyper-v/stop-vm?view=windowsserver2025-ps>

First causal gap: G3 requires OpenPGP verification before executing the Ubuntu ISO, but the exact trust-anchor bytes and exact verifier/runtime are neither measured nor approved; satisfying that requirement would add an unapproved tool/object set with unknown quantities.

BLOCKED
