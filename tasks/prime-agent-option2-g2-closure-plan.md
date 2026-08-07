# PRIME Agent option 2 — G2 closure queue

**Status:** **APPROVED — execute serially until first blocker**

**User decision (2026-08-07):** Continue through this queue until a blocker. This approval authorizes only the settled retained candidate and the serial task contracts below. It does not authorize a fallback, expansion, credential, irreversible fork, or G3 absent the final checkpoint interpretation below.

## Goal

Close the G2 platform/provisioning gaps or fail closed. G2 may end `TARGET SELECTED` only when exact trust-anchor bytes/fingerprint, verifier runtime/dependencies/licenses/invocation, image authentication, zero-touch offline install, credential-free bootstrap, deterministic seed/receipt, Hyper-V profile, no-collateral proof, exact counts/bytes/storage ceiling, and every RED fixture are closed. Otherwise it ends `BLOCKED`.

## Immutable retained candidate

- Ubuntu Server 24.04.4 LTS AMD64 only.
- Hyper-V Generation 2 VM `VordarPrimeOption2` only, with Secure Boot template `MicrosoftUEFICertificateAuthority`.
- PRIME stable `v0.7.0`, commit `be9e2fa0714e7cd1c6bd9bdb1b554d2cc6550387`, tree `0625a8fd0550a8de7ff05e8d9248e75563e5b520` only.
- No WSL2, alternate image, hypervisor, provider, model, adapter, mutable installer, shim, or fallback.

## Evidence baseline

The queue preserves the identifiers and evidence state in:

- `docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md` (`FRESH`, 2026-08-07);
- `docs/research/prime-agent/option-2-gate-closing/01-host-platform-inventory/` (including raw inventory SHA-256 `a922eb4e76f88e35228004afd627092655f96b9d7e311e67ae5e4b2e49c8a3f4`);
- `docs/research/prime-agent/option-2-gate-closing/02-target-and-profile-decision.md`; and
- `tasks/prime-agent-learning-pilot.md`.

The retained host baseline is Windows `10.0.26200` / UBR `8973`, 20 logical CPUs, `34,134,220,800` bytes RAM, and `181,652,307,968` free bytes on `C:` at inventory capture. Existing `Ubuntu` and `docker-desktop` WSL registrations must remain untouched. These measured values are not a qualification result; Task 1 refreshes the relevant facts before any action.

## Observable acceptance criteria and fixed qualification mechanism

The only mechanism that may qualify the target is:

1. Authenticate the original Ubuntu ISO cryptographically.
2. Byte-copy it and apply exactly one manifest-driven, same-size patch to proven default GRUB configuration bytes adding `autoinstall`. Do not change signed EFI, shim, GRUB executable, kernel, or initrd bytes.
3. Attach the derived ISO and deterministic ISO9660 `CIDATA` seed as two DVDs; install while the VM NIC is disconnected; require poweroff.
4. Detach both DVDs; connect only to `VordarPrimeOption2-Internal`; receive one bounded guest-initiated receipt over the fixed host/guest `/30`; power off; hash the clean VHDX; roll back the qualification VM and switch.

A successful qualification proves all of the following, with retained evidence: authenticated image and pinned signer; closed verifier/key/runtime/license graph; default Gen2 boot path and exact patch bytes; deterministic derived ISO and seed; no prompt, input, timing judgment, credentials, user, password, SSH/key, external route, DNS, package acquisition, share, Guest Service, transcription, GPU, provider call, or fallback; exact VM/profile/resources/topology; one receipt within its bound; exactly two boots; clean VHDX hash; exact rollback; and equality of protected WSL/game state before and after.

Failure is blocking. No remaster tool, keystroke, another image, fallback, or repair path is authorized.

## Initial fixed ledger

| Item | Quantity / limit |
|---|---:|
| Ubuntu ISO | `3,405,469,696` bytes |
| `SHA256SUMS` | `594` bytes |
| `SHA256SUMS.gpg` | `833` bytes |
| Known public subtotal | 3 objects / `3,405,471,123` bytes |
| Qualification VM / internal switch / NIC | 1 / 1 / 1 |
| Media | installer DVD + seed DVD |
| Disk | one 32-GiB dynamic VHDX |
| VM resources | fixed 8 GiB RAM; 4 vCPU |
| Seed ISO ceiling | `1,048,576` bytes |
| Receipt ceiling | `8,192` bytes |
| Boots | exactly 2 |
| GPU/provider calls/credentials | 0 / 0 / 0 |

Trust-anchor and verifier totals remain unknown until their closure. No acquisition or storage ceiling is approved until exact totals are computed.

## Execution model and approval interpretation

Findings and changes are separate. Execute contracts strictly in dependency order and stop at the first blocker. Preserve and display the governing checkpoint packet before its governed action; do not ask again unless a blocker, measured conflict, scope/ceiling expansion, credential, fallback, or irreversible fork appears.

Checkpoints:

1. Before Task 1: retain the read-only probe packet.
2. After Task 2 and before Task 3: display exact endpoints, counts, bytes, network, and storage.
3. After Task 4 and before Task 5: display exact hashes, dependencies, licenses, and key packet.
4. After Task 12 and before Task 13: display exact scripts, hashes, totals, storage, mutations, resources, rollback, and `<=120 min` qualification bound.
5. After Task 14: G3 remains separately gated unless the user instruction still expressly covers the exact final recipe without expansion.

## Dependency-ordered task contracts

### 1. Host preflight

- **MODEL SEAT:** Luna mechanical.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/01-host-preflight/` containing exact `raw.json`, `commands.json`, `stderr.log`, `sha256.txt`, and schema checker.
- **SCOPE:** Read-only measurement of present verifier/extraction candidates (`gpg`, `gpgv`, `sqop`, `tar`, `7z`), executable identities/version/hash/Authenticode/PE imports/licenses; PowerShell identity/language/elevation; exact Hyper-V/NetTCPIP/firewall cmdlets and parameters; Secure Boot template; VM/switch/MAC/address/route collisions; normalized WSL registrations; and full game-repository status digest.
- **DO NOT TOUCH/DECIDE:** No verifier use, download, mutation, target selection, or host-state change.
- **VERIFY:** **RED:** schema checker rejects a missing required field. **GREEN:** intact schema and every listed field is captured as a value or explicit `UNKNOWN` with source; no mutation occurs.
- **TYPE:** finding.

### 2. Bootstrap object manifest

- **MODEL SEAT:** Sol analysis.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/02-bootstrap-object-manifest/` containing exact `manifest.json`, `dependency-expectations.json`, `license-sources.json`, and `approval-packet.md`.
- **SCOPE:** Select the exact Ubuntu key object, preferably the exact Noble `ubuntu-keyring` package member `ubuntu-keyring-2012-cdimage.gpg`; select a Task-1-proven verifier or an exact official task-local Windows GnuPG/Gpg4win distribution and Task-1-proven extraction helper; recursively close URLs, digests, sizes, dependencies, and licenses.
- **DO NOT TOUCH/DECIDE:** No acquisition. Reject mutable `latest`, keyserver-as-trust, unknown ceiling, global installer, or unmeasured helper.
- **VERIFY:** **RED:** manifest validation rejects a mutable/keyserver trust source, unknown size/dependency/license, global installer, or unmeasured helper. **GREEN:** packet is complete and ends `MANIFEST READY`; otherwise it ends `BLOCKED`.
- **TYPE:** finding.

### 3. Approved-object acquisition

- **MODEL SEAT:** Luna mechanical.
- **DELIVERABLE:** bytes only under `C:\Users\egm_8\AppData\Local\VordarPrimeOption2\objects\sha256\<digest>\`; receipt at `docs/research/prime-agent/option-2-gate-closing/g2-closure/03-acquisition-receipt/`.
- **SCOPE:** Download only Task-2 URLs within exact approved ceilings; record redirect, headers, bytes, hash, time, and destination.
- **DO NOT TOUCH/DECIDE:** No execution, extraction, verification, install, or VM operation.
- **VERIFY:** **RED:** an unexpected redirect, size, object, or digest blocks. **GREEN:** each acquired object matches its Task-2 URL, ceiling, destination, and hash receipt.
- **TYPE:** change.

### 4. Verifier runtime closure

- **MODEL SEAT:** Terra default implement.
- **DELIVERABLE:** task-local runtime under `C:\Users\egm_8\AppData\Local\VordarPrimeOption2\verifier\<runtime-manifest-sha256>\`; manifests at `docs/research/prime-agent/option-2-gate-closing/g2-closure/04-verifier-runtime/`.
- **SCOPE:** Extract only approved objects/helpers; recursively hash; resolve PE imports to task-local leaves or explicitly bounded Windows system-DLL leaves; extract the exact CD-image keyring member; enumerate packets, fingerprint, UID, and subkeys; map licenses.
- **DO NOT TOUCH/DECIDE:** No keyserver, user keyring, registry, `PATH`, service, update, or verifier execution.
- **VERIFY:** **RED:** extra/missing file, key, dependency, or license fails. **GREEN:** two independent extractions are byte-identical and every import/key/license is closed.
- **TYPE:** change.

### 5. Independent crypto verifier

- **MODEL SEAT:** Terra default implement.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/crypto-verifier/`.
- **SCOPE:** Test first; implement an independent wrapper that verifies runtime/dependency/keyring manifests using explicit isolated home and paths, machine-readable status, exactly one valid signature/fingerprint `843938DF228D22F7B3742BC0D94AA3F0EFE21092`, expected algorithms, checksum row, and independent ISO hash.
- **DO NOT TOUCH/DECIDE:** No network, private key, or provisioning.
- **VERIFY:** **RED:** changed key, verifier, DLL, checksum, signature, or ISO; missing dependency/license; duplicate signature; unexpected signer/digest algorithm; extra or missing row each fail by named reason. **GREEN:** exact intact fixture passes only with the one expected signature, fingerprint, checksum row, and ISO digest.
- **TYPE:** change.

### 6. Cryptographic-input closure

- **MODEL SEAT:** Sol analysis.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/05-cryptographic-input-closure.md`.
- **SCOPE:** Independently review and run the approved verifier; reconcile every identity, license, and RED result.
- **DO NOT TOUCH/DECIDE:** No repair, reacquisition, substitution, or provisioning.
- **VERIFY:** **RED:** any unreconciled identity/license or failing RED blocks. **GREEN:** report ends exactly `CRYPTOGRAPHIC INPUTS CLOSED`; otherwise it ends exactly `BLOCKED`.
- **TYPE:** finding.

### 7. Authenticated ISO layout evidence

- **MODEL SEAT:** Luna mechanical.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/06-iso-layout/` containing full ISO tree, boot catalog, GRUB configs, signed boot files, and hashes.
- **SCOPE:** Read only the authenticated ISO; prove the default Gen2 boot path and all kernel-argument inputs.
- **DO NOT TOUCH/DECIDE:** No derived ISO, VM, or content change.
- **VERIFY:** **RED:** unresolved default path, traversal, duplicate, or byte mismatch fails. **GREEN:** complete evidence identifies the sole default Gen2 GRUB-byte patch location while preserving every signed executable/kernel/initrd identity.
- **TYPE:** change.

### 8. Provisioning protocol

- **MODEL SEAT:** Sol analysis.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/07-provisioning-protocol.md`.
- **SCOPE:** Specify exact same-size patch offsets/bytes/output identity; deterministic CIDATA `user-data`/`meta-data`; helper allowlist/provenance; VM/switch/MAC/address/firewall; rollback journal; receipt schema/frame/retry/ack/timeout/replay; and host/guest observations.
- **DO NOT TOUCH/DECIDE:** No identity account, `users: []`, root disabled, SSH/key/password absent, refresh/geoip/update/snaps/drivers/OEM/codecs/network acquisition off, offline fallback, poweroff, NIC disconnected. Fix one `/30` and TCP port with no gateway, DNS, or NAT. No prompt/key/timing/secret/share/Guest Service/external route/unbounded receipt/unsigned executable change.
- **VERIFY:** **RED:** any prohibited field/path or unbounded/non-idempotent receipt blocks. **GREEN:** report ends `PROTOCOL SETTLED` only with every field fixed; otherwise `BLOCKED`.
- **TYPE:** finding.

### 9. Independent provisioning verifier

- **MODEL SEAT:** Terra default implement.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/provisioning-verifier/`.
- **SCOPE:** Independently test generated bytes, ledgers, topology, Hyper-V receipts, guest receipt, rollback, WSL/game status, and no fallback.
- **DO NOT TOUCH/DECIDE:** No producer implementation or qualification execution.
- **VERIFY:** **RED:** missing `autoinstall`; changed patch or signed file; nondeterministic seed; user/password/key/SSH; external switch/NAT/route/DNS/install NIC/package acquisition; Guest Service/Copy-VMFile/mount/transcription; receipt failure; wrong VM/profile/template/resources/GPU; WSL/game status change; or fallback must fail. **GREEN:** one complete synthetic fixture passes.
- **TYPE:** change.

### 10. Provisioning bundle

- **MODEL SEAT:** Sol hard implement.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/provisioning-bundle/`; future generated state only in the task root.
- **SCOPE:** Implement the exact Task-8 object-verifier invocation, deterministic ISO patcher/CIDATA writer, preflight, bounded listener, Hyper-V controller, embedded receipt producer, and rollback.
- **DO NOT TOUCH/DECIDE:** No host/VM execution, acquisition, fallback, broad cleanup, WSL, Docker, Pi, VFX, credentials, or self-verifier import.
- **VERIFY:** **RED:** Task 9 must reject each minimal producer output before its corresponding producer work. **GREEN:** all static bundle outputs satisfy Task 9 without importing the verifier.
- **TYPE:** change.

### 11. Static generation evidence

- **MODEL SEAT:** Luna mechanical.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/08-static-evidence/<run-id>/`.
- **SCOPE:** Generate the derived ISO and seed twice, byte-compare them, and run every RED plus intact static-evidence check.
- **DO NOT TOUCH/DECIDE:** No Hyper-V, listener, firewall, VM, WSL, Docker, network, credential, or repair action.
- **VERIFY:** **RED:** any drift or retained RED failure blocks. **GREEN:** both generation pairs are byte-identical and all intact static checks pass.
- **TYPE:** change.

### 12. Qualification approval packet

- **MODEL SEAT:** Luna mechanical.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/09-qualification-approval-packet.md`.
- **SCOPE:** Refresh Task-1 preflights; record exact object/extracted/generated counts and bytes, free disk, hard storage ceiling, VM/switch/address/firewall mutations, `<=120 min` resources/rollback, and pre-run protected-state digests.
- **DO NOT TOUCH/DECIDE:** No mutation, process, or VM.
- **VERIFY:** **RED:** changed/missing preflight, false elevation, collision, insufficient disk, or uncomputed ceiling blocks. **GREEN:** packet ends `READY FOR QUALIFICATION APPROVAL`; otherwise `BLOCKED`.
- **TYPE:** finding.

### 13. One qualification run

- **MODEL SEAT:** Luna mechanical.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/10-qualification-evidence/<run-id>/`.
- **SCOPE:** Under retained approval execute once: verify bytes; journal; create exact switch/address/VM/VHDX/profile/Secure Boot; disable Guest Service and prove no GPU; attach DVDs with NIC disconnected; one unattended install to poweroff; detach/set VHD first; connect only internal; bounded firewall/listener; one boot/receipt/poweroff; hash; independently verify; remove exact task VM/switch/address/rule/transients; prove pre/post protected equality.
- **DO NOT TOUCH/DECIDE:** No VMConnect/input/delay/fallback/retry/extra boot/repair/credential/provider/external network/share/Guest Service copy/WSL/Docker/Pi/GPU.
- **VERIFY:** **RED:** first unsafe result, intact RED, or protected-state difference stops and triggers only exact rollback. **GREEN:** exactly two boots, one bounded valid receipt, clean VHDX hash, all verifier checks pass, and exact rollback/protected equality are evidenced.
- **TYPE:** change.

### 14. Final independent G2 gate

- **MODEL SEAT:** Sol analysis.
- **DELIVERABLE:** `docs/research/prime-agent/option-2-gate-closing/g2-closure/11-final-independent-gate.md` plus replacement G2 body.
- **SCOPE:** A fresh worker who authored none of Tasks 5, 9, or 10 recomputes every closure, count/byte/ceiling, no-fallback proof, and protected-state invariance; reruns all REDs and the intact index; preserves the full profile; cites artifacts; and gives the exact Luna G3 recipe.
- **DO NOT TOUCH/DECIDE:** No repair or rerun.
- **VERIFY:** **RED:** missing evidence, count/byte/ceiling mismatch, unclosed red, broken green, fallback, or protected-state drift fails the gate. **GREEN:** only if all checks pass may the final G2 line be exactly `TARGET SELECTED`; otherwise state the first causal gap and end exactly `BLOCKED`.
- **TYPE:** finding.

## Campaign stop conditions

Stop immediately at: unknown/untrusted key bytes; open verifier/dependency/extraction/license; crypto RED failure; no deterministic same-size default-boot patch; signed executable/kernel/initrd change; prompt/input/timing; credential/user/SSH/external route/DNS/package acquisition/extra boot; receipt requiring secret/mount/Guest Service/transcription or exhibiting unbounded/non-idempotent behavior; missing Hyper-V cmdlet/parameter/template/elevation/space or collision; any intact RED or broken GREEN; WSL/game status drift; fallback; rollback ambiguity; or uncomputed exact totals/ceiling.

## Risks

The initial public-object subtotal is knowingly incomplete until Task 2 and cannot authorize acquisition/storage. Hyper-V cmdlet/template/elevation, exact verifier/extraction closure, deterministic autoinstall patchability, noninteractive installer behavior, and receipt topology are all fail-closed dependencies. Any measured conflict is a blocker, not permission to redesign.

## Final gate

Task 14 is the final G2 gate. It must fail when a promised behavior is broken: every stated closure requires both its named hostile RED and intact GREEN evidence, independent recomputation, exact counts/bytes/ceiling, no-fallback proof, and protected-state equality. Only then may the replacement G2 body end `TARGET SELECTED`; otherwise its final line must be `BLOCKED`.
