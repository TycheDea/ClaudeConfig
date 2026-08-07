# Option 2 bootstrap object manifest — approval packet

**Status:** `BLOCKED`
**Evidence date:** 2026-08-07
**Task 1 evidence:** commit `52e2c56`; [`raw.json`](../01-host-preflight/raw.json), SHA-256 `b8861db61ebd57c28770ea52eb947d2ec2e7194cca4d94081dedb5ca95ec2c72`.

## Contract result

Exactly one trust route is selected: `ubuntu-noble-keyring-deb-2023.11.28.1`. Exactly one verifier route is selected: `task1-git-for-windows-gpgv-2.4.9`. The fallback list is empty. Acquisition is not authorized. G0 remains FRESH at [`.claude/docs/research/prime-agent/option-2-gate-closing/00-evidence-freshness.md`](../../00-evidence-freshness.md). The durable queue and closure plan remain `.claude/tasks/prime-agent-option2-gate-closing-plan.md` and `.claude/tasks/prime-agent-option2-g2-closure-plan.md`; this G2 closure path remains BLOCKED.

## Selected trust route

The pretrusted package is [ubuntu-keyring_2023.11.28.1_all.deb](https://archive.ubuntu.com/ubuntu/pool/main/u/ubuntu-keyring/ubuntu-keyring_2023.11.28.1_all.deb): 11,124 bytes and authoritative SHA-256 `36de43b15853ccae0028e9a767613770c704833f82586f28eb262f0311adb8a8`. Its required member is `etc/apt/trusted.gpg.d/ubuntu-keyring-2012-cdimage.gpg`, expected to contain exactly one primary key, fingerprint `843938DF228D22F7B3742BC0D94AA3F0EFE21092`, UID `Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>`, and no extra packets.

Primary citations: Ubuntu [package download](https://archive.ubuntu.com/ubuntu/pool/main/u/ubuntu-keyring/ubuntu-keyring_2023.11.28.1_all.deb), [package file list](https://packages.ubuntu.com/noble/all/ubuntu-keyring/filelist), and [security image verification guidance](https://ubuntu.com/tutorials/how-to-verify-ubuntu#1-overview). The versioned [`.dsc`](https://archive.ubuntu.com/ubuntu/pool/main/u/ubuntu-keyring/ubuntu-keyring_2023.11.28.1.dsc), [source tarball](https://archive.ubuntu.com/ubuntu/pool/main/u/ubuntu-keyring/ubuntu-keyring_2023.11.28.1.tar.xz), and [package copyright source](https://changelogs.ubuntu.com/changelogs/pool/main/u/ubuntu-keyring/ubuntu-keyring_2023.11.28.1/copyright) identify package-source provenance: source bytes are 20,236 with SHA-256 `aecd455ae15561371d6e454f121f079f0641d5e1b579a5563a2bc363fc74aa2e`; key bytes are not copyrighted and support files are GPL-2.0-or-later. This records no project-license-verdict change.

The package is Debian `ar` with the member below `data.tar.zst`. No Task1-approved zstd extractor, extracted member bytes/digest, or packet sequence exists. This is the first causal blocker.

## Selected verifier route

Task 1 observed `C:\Program Files\Git\usr\bin\gpgv.EXE`: gpgv 2.4.9, 514,306 bytes, SHA-256 `f4d13204d77fdf63c02b0e6742230f83a833128c28f7b715709c2c63a96c427b`, Authenticode status 2. It is an observed candidate only, intended for a task-local verifier root and isolated explicit invocation. It is blocked: PE and delay imports, private DLLs, API/system leaves, data/config, exact Git-for-Windows binary package/build recipe, notices/licenses, and corresponding sources are unknown. The [Git for Windows package-management page](https://gitforwindows.org/package-management) is cited as the Sol primary package-management source, not as a closure of these missing facts.

The non-trust-bearing upstream source candidate is [GnuPG 2.4.9](https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.4.9.tar.bz2), SHA-256 `dd17ab2e9a04fd79d39d853f599cbc852062ddb9ab52a4ddeb4176fd8b302964`, ceiling 8,388,608 bytes. [GnuPG integrity information](https://gnupg.org/download/integrity_check.html) is cited. That tarball is explicitly not proven corresponding source for Git-for-Windows.

## Proposed objects and arithmetic

| Object | Bytes / ceiling | Disposition |
|---|---:|---|
| Ubuntu 24.04.4 server ISO | 3,405,469,696 | authenticated SHA-256 `e907d92eeec9df64163a7e454cbc8d7755e8ddc7ed42f99dbc80c40f1a138433` |
| `SHA256SUMS` | 594 | signed metadata |
| `SHA256SUMS.gpg` | 833 | signature input |
| Keyring `.deb` | 11,124 | pretrusted package |
| Keyring source | 20,236 | package-source identity only |
| GnuPG source | 8,388,608 ceiling | unproven corresponding source |

All endpoints are HTTPS, version-specific, zero-redirect, and limited to `releases.ubuntu.com`, `archive.ubuntu.com`, and `gnupg.org`. Known bytes are `3,405,502,483`; hard network/quarantine ceiling is `3,405,502,483 + 8,388,608 = 3,413,891,091`. Runtime and combined storage are UNKNOWN; no acquisition is authorized. A post-acquisition observed digest cannot bootstrap pretrusted identity.

## RED disposition

Mutable URLs, redirects, size or digest mismatch, observed-only trust, keyserver trust, packet extras, unmeasured helpers, unclosed dependencies/licenses, or global mutation are RED. Unknown/system/private/extra dependencies, `PATH` use, global state, and extra keys are also RED. Version-only source inference, missing DLL mapping, treating UNKNOWN as closed, omitted source/notice, license-verdict change, and mutable/global routes remain RED.

Task 3 is unauthorized. The extraction blocker is first; the verifier/runtime/license and unknown runtime/combined-storage blockers additionally remain open.

BLOCKED