# PRIME Agent option 2 — Task-2 blocker closure plan

## Status and retained contract

**Status:** **BLOCKED AT TASK 1 — Tasks 2–8 parked**

Task 1 public research is committed as `90728fd` at `.claude/docs/research/prime-agent/option-2-gate-closing/g2-closure/02-bootstrap-object-manifest/blocker-closure/00-public-research/` and ends `BLOCKED`. The aligned retained member is `etc/apt/trusted.gpg.d/ubuntu-keyring-2012-cdimage.gpg`; the discarded draft member was never persisted as selected.

The exact public ledger is: 8 candidate bodies, 6 known sizes, 2 unknown sizes, 8,121,066 known bytes, UNKNOWN complete bytes/storage, 0 eligible bodies, 16 direct dependency declarations, 26 patches, and 10 blockers.

The first causal gap remains no Task-1-approved zstd extraction/member byte-digest-packet closure. Additional endpoint, Ubuntu checksum digest, MSYS2 package/source/build binding, Git-for-Windows provenance, dependency/license, and ceiling gaps remain. No host probe, body acquisition, extraction, execution, credentials, VM/WSL/Docker/GPU, fallback, or original Task 3 occurred. Exact next action: stop. Blocker Tasks 2–8 and original Tasks 3–14 are parked. Any continuation requires a new explicit user decision on a fresh Sol plan; this does not imply host-probe approval.

This is a Sol analysis plan limited to existing Task 1, Task 2, and G2 evidence plus public primary sources. The retained route is limited to the Ubuntu Noble keyring and the Task-1-observed Git-for-Windows `gpgv` 2.4.9 route. No fallback, credentials, host probe until separately approved, global-state change, or change to retained decisions is allowed.

## Measured checkpoint

Task 1 observed:

- Path: `C:\Program Files\Git\usr\bin\gpgv.EXE`
- Version: 2.4.9
- Size: 514306 bytes
- SHA-256: `f4d13204d77fdf63c02b0e6742230f83a833128c28f7b715709c2c63a96c427b`
- GNU tar 1.35 was observed, but no zstd decoder/function/dependencies/license closure was established.

Current Task 2 blockers:

- The key package's `data.tar.zst` extraction, member digest, and packets are unresolved.
- The exact `gpgv` package/build/runtime/data/license/source, local invocation, and storage are unresolved.

## Public candidate facts and research constraints

- Ubuntu Noble keyring deb: 11124 bytes; SHA-256 `36de43b15853ccae0028e9a767613770c704833f82586f28eb262f0311adb8a8`.
- Ubuntu Noble keyring source tarball: 20236 bytes; SHA-256 `aecd455ae15561371d6e454f121f079f0641d5e1b579a5563a2bc363fc74aa2e`.
- MSYS2 `gnupg` 2.4.9 recipe commit: `705cff2db01a907c02352781fc5cd2fcac61b50b`.
- Candidate package: `gnupg-2.4.9-1-x86_64.pkg.tar.zst`.
- Candidate package SHA-256: `cd95fe16cc87700372549294a21f35b4adeed8bf57451cd2147e7f82f9e582eb`.
- Byte equality between the observed Git-for-Windows `gpgv` and the candidate package member is not proven.
- Git for Windows package-management/build sources and MSYS2 provenance must be proven.
- GNU tar `--zstd` support is not proof of extraction capability when external zstd is absent.
- `mirror.msys2.org` is an ineligible geo-redirector. Only zero-redirect immutable endpoints may qualify.
- GnuPG 2.4 is end-of-life, but no newer substitute is allowed.

Candidate endpoint set for Task 1 research:

- Exact versioned Ubuntu deb, dsc, and tar.xz objects.
- `https://repo.msys2.org/msys/x86_64/gnupg-2.4.9-1-x86_64.pkg.tar.zst`
- `https://repo.msys2.org/msys/sources/gnupg-2.4.9-1.src.tar.zst`
- The upstream GnuPG 2.4.9 tarball.
- Exact package/source pairs for every private DLL and the selected extractor.
- Version-specific Ubuntu `SHA256SUMS` and `SHA256SUMS.gpg`.

A redirect, unavailable historical object, or missing authoritative digest or size is blocking.

## Execution model and approval boundary

Execute serially:

1. Public research.
2. An explicitly approved fixed-path host probe.
3. A Sol exact acquisition manifest.
4. A Terra independent closure checker, completed before acquisition.
5. Approved Luna acquisition.
6. Approved Terra offline extraction and static closure.
7. A separately approved Sol hard isolated exercise.
8. An independent Sol Task 2 verdict.

No source inference from a version, alternate verifier, alternate key package, alternate zstd route, or custom OpenPGP implementation is permitted.

## Task 1 — Public primary-source research

**MODEL SEAT:** Sol analysis.

**DELIVERABLE:** `.claude/docs/research/prime-agent/option-2-gate-closing/g2-closure/02-bootstrap-object-manifest/blocker-closure/00-public-research/` containing `sources.md`, `endpoint-ledger.json`, `package-candidates.json`, and `license-candidates.json`.

**SCOPE:** Revalidate the Ubuntu package, dsc, source, and member; MSYS2 binary/source identity, immutable recipe, upstream source, every dependency package/source/license; and each exact URL, body size, authoritative digest, status, and redirect. Record the GnuPG support state without substitution.

**DO NOT TOUCH OR DECIDE:** No host access, body acquisition, extraction, source/version inference, license verdict, mirror fallback, mutable URL, or substitution.

**VERIFY:** RED rejects a missing authoritative digest or size, mutable ref, GitHub or mirror redirector, nonzero redirect, version-only package/source join, absent notice/license, or unknown ceiling. GREEN requires dated source identity for every candidate plus a zero-redirect immutable candidate set; otherwise report the exact blocker and terminal outcome `BLOCKED`.

**TYPE:** Finding.

**APPROVAL CHECKPOINT:** No approval beyond this accepted plan. Estimate: 2–4 hours, 0 object-download bytes, browser/API reads, and 0 GPU.

## Task 2 — Fixed-path host supplement

**MODEL SEAT:** Luna mechanical.

**DELIVERABLE:** Sibling `01-host-supplement/` containing `raw.json`, `commands.json`, `stderr.log`, `sha256.txt`, `red-fixture.json`, `red.log`, `green.log`, and `schema_check.py`.

**SCOPE:** Inspect only fixed paths under `C:\Program Files\Git\`. Record hashes, sizes, and version metadata for `gpgv`, `gpg`, `tar`, and `zstd` if present; fixed package/version files; `etc\package-versions.txt`; applicable pacman local `desc`, `files`, and `mtree`; installer/build identity files; and fixed private DLLs. Metadata-only `--version` and `--help` invocations are allowed only after the displayed approval.

**DO NOT TOUCH OR DECIDE:** No PATH search, environment capture, package manager, registry mutation, network, extraction, cryptography, WSL, VM, Docker, installation, copying, or global change.

**VERIFY:** RED rejects a missing ledger, changed `gpgv`, PATH resolution, false package metadata, omitted zstd absence, or mutation. GREEN records every required value exactly or as `UNKNOWN`, preserves identity, and proves no mutation. No fixed zstd, or an unclosable package/source/license identity, yields terminal outcome `BLOCKED`; do not acquire an extractor.

**TYPE:** Finding.

**APPROVAL CHECKPOINT:** Requires an explicit approval packet showing exact paths and commands, no environment capture, 0 network, no more than 10 minutes wall time, no more than 2 CPU-minutes, no more than 10 MiB output/storage, and 0 GPU.

## Task 3 — Exact acquisition plan

**MODEL SEAT:** Sol analysis.

**DELIVERABLE:** Sibling `02-acquisition-plan/` containing `bootstrap-manifest.json`, `dependency-graph.json`, `source-license-graph.json`, `storage-ledger.json`, and `approval-packet.md`.

**SCOPE:** Use only the fixed Task 1 and host-supplement PowerShell-plus-zstd route and the observed `gpgv`. Specify exact Ubuntu, MSYS2, and upstream objects; patches, notices, licenses, private/system leaves; destinations; and caps.

**DO NOT TOUCH OR DECIDE:** No acquisition, execution, extraction, byte-equality claim, packet claim, source inference, unknown value, fallback, or original Task 3 work.

**VERIFY:** RED rejects any unknown count, byte value, or cap; redirect; absent digest, URL, or zstd; missing pair, dependency, or license; version-only source binding; or treatment of an observed hash as pretrust. GREEN terminates exactly `ACQUISITION READY`; otherwise terminate exactly `BLOCKED`.

**TYPE:** Finding.

**APPROVAL CHECKPOINT:** This task prepares the acquisition approval packet but does not authorize acquisition. Continue only from completed Task 1 and an explicitly approved, completed Task 2 host supplement.

### Required integer arithmetic

All terms are exact integers:

- `B_boot`: exact blocker network bytes.
- `N_boot`: exact blocker object count.
- `B_all`: final Task 2 object bytes, including the 3405469696-byte ISO.
- `R_extract`: maximum simultaneous extraction workspace.
- `R_analysis`: analysis-only task runtime storage cap.
- `R_verify`: final verifier runtime storage cap.
- `E`: evidence cap.

Required equations:

```text
blocker_closure_storage_ceiling = B_boot + R_extract + R_analysis + R_verify + E
corrected_task2_combined_storage_ceiling = B_all + R_extract + R_analysis + R_verify + E
original_task3_remaining_network_bytes = B_all - bytes_of_already_present_digest-addressed_objects
```

Any unknown or double count is RED.

## Task 4 — Independent closure checker

**MODEL SEAT:** Terra default implement.

**DELIVERABLE:** Sibling `verifier/` containing `verify.ps1`, schemas, `verify-all.ps1`, hostile fixtures, an intact fixture, tests, and `README`.

**SCOPE:** Independently check manifest and evidence identities, package/source bindings, PE imports, packets, invocation, counts, bytes, redirects, licenses, and storage. The checker must not import producer logic.

**DO NOT TOUCH OR DECIDE:** No acquisition, producer implementation, executable invocation, source inference, license verdict, or fallback.

**VERIFY:** Every hostile fixture fails for its named reason, and the intact fixture passes. Hostile fixtures cover wrong/missing extractor or script; wrong/missing/duplicate/traversing key member; changed key, fingerprint, UID, packet count/order, or extra packet; import/delay import; DLL/API/system leaf; dynamic/data/config dependency; wrong package or metadata or host/package mismatch; version-inferred or incorrect source recipe/patch/tar; license/notice/dependency omission; redirect; length/size/digest mismatch; global mutation; PATH dependence; and unknown totals/caps.

**TYPE:** Change.

**APPROVAL CHECKPOINT:** Build and pass this independent checker after the exact Task 3 plan and before any Task 5 acquisition. This task grants no acquisition or execution authority.

## Task 5 — Exact-object acquisition

**MODEL SEAT:** Luna mechanical.

**DELIVERABLE:** Digest-addressed objects under the task-local root and sibling `03-acquisition-receipt/`.

**SCOPE:** Acquire only Task 3 objects with redirects disabled. Record receipt URL, status, headers, absence of `Location`, bytes, hash, time, destination, and process. Acquire the real Ubuntu checksum and signature, but not the ISO.

**DO NOT TOUCH OR DECIDE:** No execution, extraction, installation, package manager, verifier implementation, original Task 3 work, mutable mirror, or fallback.

**VERIFY:** The exact object count, total bytes, digests, destinations, and independent checker must agree. Any mismatch blocks.

**TYPE:** Change.

**APPROVAL CHECKPOINT:** Requires explicit approval after `ACQUISITION READY`, showing exact `N_boot`, `B_boot`, hosts, URLs, storage, free disk, and wall time. Limits: 0 GPU, no more than 10 CPU-minutes per GiB for hashing, no more than 60 minutes wall time, and exactly `B_boot` network bytes.

## Task 6 — Offline extraction and static closure

**MODEL SEAT:** Terra default implement.

**DELIVERABLE:** Sibling `04-offline-analysis/`, a task-local extractor root, and a task-local candidate verifier root.

**SCOPE:** Deny network; copy the approved fixed extractor; use absolute PowerShell and zstd paths; perform reviewed archive parsing; extract the exact key member and hash it; extract packages; byte-compare observed `gpgv` and private files; recursively close PE/delay imports, APIs, system leaves, and static/dynamic/data dependencies; and reconcile package build metadata, source, recipe, patches, upstream source, notices, and licenses.

**DO NOT TOUCH OR DECIDE:** No PATH resolution, package installation, network, cryptography, OpenPGP parsing, custom implementation, user keyring, global state, independent-verifier execution, or substitution.

**VERIFY:** Produce two clean, byte-identical extraction manifests. RED rejects a wrong extractor, member, package, import, dependency, source, notice, size, hash, or cap. GREEN requires exact key bytes/digest and complete static graphs.

**TYPE:** Change.

**APPROVAL CHECKPOINT:** Execution requires approval of the exact command, inputs, outputs, and workspace. Limits: no more than 30 minutes wall time, 0 download bytes, no more than 20 CPU-minutes, and 0 GPU.

## Task 7 — Isolated runtime exercise

**MODEL SEAT:** Sol hard implement.

**DELIVERABLE:** Sibling `05-isolated-runtime/` containing packet output, normalized invocation/status, poison results, pre/post manifests, and a ledger.

**SCOPE:** Use same-package task-local `gpg` only as a `list-packets` instrument, not as the verifier; establish the exact packet sequence, fingerprint, and UID. Run task-local `gpgv` over the acquired Ubuntu checksum, signature, and keyring using absolute paths, `--no-options`, an explicit isolated read-only home/keyring, fixed current directory, machine-readable status, allowlisted locale/time, an empty or proven-irrelevant PATH, and no network.

**DO NOT TOUCH OR DECIDE:** No user keyring, default home, registry, service, updater, global config, PATH resolution, other verifier, private key, original Task 3 work, or repair.

**VERIFY:** Prove poisoned global state and PATH cannot influence results. Fake files are rejected. A changed signature, checksum, key, packet set, DLL, system leaf, invocation, environment, or runtime fails. The intact expected signer passes. Any undeclared access, global/PATH influence, signer mismatch, package mismatch, or packet ambiguity yields terminal outcome `BLOCKED`.

**TYPE:** Change.

**APPROVAL CHECKPOINT:** Requires separate execution approval showing the exact runtime, invocation, network-denial mechanism, and poison fixtures. Limits: no more than 20 minutes wall time, 0 download bytes, no more than 10 CPU-minutes, and 0 GPU.

## Task 8 — Independent Task 2 verdict

**MODEL SEAT:** Sol analysis, independent of the Task 4, Task 6, and Task 7 authors.

**DELIVERABLE:** Sibling `06-independent-verdict.md` plus corrected Task 2 `manifest.json`, `dependency-expectations.json`, `license-sources.json`, and `approval-packet.md`.

**SCOPE:** Recompute object count, bytes, redirects, key digest/packets, package/build/source binding, PE/private/API/data closure, license closure, runtime/invocation, and storage. Rerun every RED and GREEN check.

**DO NOT TOUCH OR DECIDE:** No repair, acquisition, extraction, execution, fallback, original Task 3 work, source inference, or waiver.

**VERIFY:** Run verifier `verify-all.ps1` over the evidence root. Any missing value, mismatch, unknown, redirect, global-state dependence, PATH dependence, or broken test yields terminal outcome `BLOCKED`.

**TYPE:** Finding.

**APPROVAL CHECKPOINT:** The independent verdict follows completed Tasks 1–7 and grants no original Task 3 authority unless the dual exact terminal-line gate below passes and the orchestrator independently verifies it.

## Exact final gate

`MANIFEST READY` is permitted only when all of the following are proven:

- The exact Ubuntu object, member, and packet set are closed.
- The fixed approved extractor, its package/source/dependencies/licenses, and its task-local use are closed.
- The observed `gpgv` is exactly byte-equal to the immutable package member.
- Metadata binds the exact source package, recipe, patches, upstream source, and license—not merely a version.
- Every runtime, data, and system leaf is closed.
- Everything is task-local except explicitly bounded Windows leaves.
- Invocation is absolute, isolated, network-free, and PATH-independent.
- Every count, byte value, and cap is an integer.
- Redirect count is zero.
- Every RED fixture fails and every GREEN fixture passes.

Both the approval packet and independent verdict must end with the terminal line exactly `MANIFEST READY`. Otherwise each must identify the first causal gap and end with the terminal line exactly `BLOCKED`.

## Stop and resume rule

Original Tasks 3–14 are parked throughout blocker Tasks 1–7. Original Task 3 may resume only after Task 8 produces dual `MANIFEST READY` and the orchestrator independently verifies the artifacts. Reuse digest-addressed objects and authorize only the exact remaining bytes. Any blocker permanently stops this retained route; there is no fallback.

## Risks retained without waiver

- Fixed host bytes may drift.
- zstd may be absent and terminal.
- MSYS2 package equality remains unproven.
- Historical objects may be unavailable or redirect.
- The GnuPG 2.4 branch is end-of-life.
- Windows OS leaves must be bound to the exact build.
- No license verdict or credits edit is authorized.

Original Tasks 3–14 remain parked until dual `MANIFEST READY`.
