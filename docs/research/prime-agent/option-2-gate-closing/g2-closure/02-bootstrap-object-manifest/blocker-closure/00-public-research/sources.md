# Option 2 G2 blocker closure — public primary-source research

## Status

- Schema version: `1.0.0`
- Research date: `2026-08-07`
- Retained route ID: `ubuntu-noble-keyring-deb-2023.11.28.1`
- Retained verifier route ID: `task1-git-for-windows-gpgv-2.4.9`
- Status: `BLOCKED`
- Repository changes: none
- Candidate-object body bytes acquired: 0
- Host inspection or probing: none
- Alternative key members selected: none

## Alignment correction

The retained trust member is exactly:

`etc/apt/trusted.gpg.d/ubuntu-keyring-2012-cdimage.gpg`

It is expected, but not yet verified by extraction, to contain fingerprint
`843938DF228D22F7B3742BC0D94AA3F0EFE21092` and UID
`Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>`.

The earlier draft named a different package member. Replacing that draft value
with the retained CD-image member is alignment only. It does not change the
retained package, route, expected key identity, license statement, blocker,
status, or fallback list. No alternative key member is selected.

The member bytes, member size, member SHA-256, primary-key count, UID packet,
packet order, packet count, and complete packet sequence remain `UNKNOWN`.
The fingerprint and UID above are expectations inherited from the retained
Task-2 packet, not extracted facts.

## First causal gap

The first causal gap remains the one recorded by retained Task 2: the selected
Debian `ar` package stores its payload in `data.tar.zst`, but no
Task-1-approved zstd-capable extractor and no extracted retained-member bytes,
member digest, or packet sequence exist.

Public research cannot close that gap without selecting or using an
unapproved extractor or acquiring and extracting object bodies. Neither action
occurred.

Independent additional blockers are:

1. no candidate endpoint has a measured zero redirect count or observed HTTP
   status;
2. no authoritative SHA-256 was located for the Ubuntu 24.04.4
   `SHA256SUMS` or `SHA256SUMS.gpg` objects;
3. the exact size of the MSYS2 GnuPG binary package remains `UNKNOWN`;
4. the exact size and authoritative digest of
   `gnupg-2.4.9-1.src.tar.zst` remain `UNKNOWN`;
5. the official MSYS2 record directly associates its binary package with the
   named source-only package, but does not bind either object to recipe commit
   `705cff2db01a907c02352781fc5cd2fcac61b50b`;
6. Git-for-Windows documentation does not identify the exact provenance of
   the retained observed `gpgv.EXE` or bind it to the MSYS2 candidate;
7. the recipe's 16 runtime dependencies are unversioned, so exact dependency
   packages, sources, notices, licenses, and transitive dependencies remain
   `UNKNOWN`;
8. notice and license closure is incomplete; and
9. complete object count, complete bytes, and storage ceiling remain
   `UNKNOWN`.

No observed-host digest is used as pretrust, and no host/package byte-equality
claim is made.

## Research method and boundaries

Only the retained approval packet, retained Task-2 JSON artifacts, retained
Task-1 observations, and public primary-source HTML/API/text records were used.
Searches located public records only.

No package, source archive, ISO, checksum file, signature, executable, patch,
or other planned object body was acquired. No host filesystem, command,
process, registry, environment, `PATH`, Git installation, package manager,
VM, WSL, Docker, GPU, credential, or global state was accessed.

## Ubuntu Noble keyring package

### Binary identity and direct source binding

Canonical records identify:

- package: `ubuntu-keyring`
- version: `2023.11.28.1`
- architecture: `all`
- binary filename: `ubuntu-keyring_2023.11.28.1_all.deb`
- exact size: `11124` bytes
- SHA-256:
  `36de43b15853ccae0028e9a767613770c704833f82586f28eb262f0311adb8a8`
- source package: `ubuntu-keyring` version `2023.11.28.1`

Sources:

- <https://packages.ubuntu.com/noble/ubuntu-keyring>
- <https://packages.ubuntu.com/noble/all/ubuntu-keyring/download>
- <https://api.launchpad.net/1.0/ubuntu/+archive/primary?ws.op=getPublishedBinaries&binary_name=ubuntu-keyring&version=2023.11.28.1&exact_match=true&distro_arch_series=https://api.launchpad.net/1.0/ubuntu/noble/amd64>
- <https://api.launchpad.net/1.0/ubuntu/+archive/primary?ws.op=getPublishedSources&source_name=ubuntu-keyring&version=2023.11.28.1&exact_match=true&ordered=true>

The binary/source relationship is directly stated by Canonical and Launchpad;
it is not inferred from matching version text.

### Source objects

Canonical's Noble acceptance record gives:

| Object | Bytes | SHA-256 |
|---|---:|---|
| `ubuntu-keyring_2023.11.28.1.dsc` | 1872 | `c71c8e5a1dd5e8ef682b7104645a88f0bc9eeb9380bf64288adcf78f40bcf68b` |
| `ubuntu-keyring_2023.11.28.1.tar.xz` | 20236 | `aecd455ae15561371d6e454f121f079f0641d5e1b579a5563a2bc363fc74aa2e` |

Sources:

- <https://lists.snapcraft.io/archives/noble-changes/2023-November/003972.html>
- <https://launchpad.net/ubuntu/noble/+source/ubuntu-keyring/2023.11.28.1>
- <https://api.launchpad.net/1.0/ubuntu/+archive/primary/+sourcepub/15417590?ws.op=sourceFileUrls>

### Retained trust member

The sole retained member is:

`etc/apt/trusted.gpg.d/ubuntu-keyring-2012-cdimage.gpg`

Source:

- <https://packages.ubuntu.com/noble/all/ubuntu-keyring/filelist>

Expected-but-unverified identity:

- expected fingerprint:
  `843938DF228D22F7B3742BC0D94AA3F0EFE21092`
- expected UID:
  `Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>`
- expected primary-key count: `1`
- expected extra packets: none

Observed extraction facts:

- member bytes: `UNKNOWN`
- member size: `UNKNOWN`
- member SHA-256: `UNKNOWN`
- observed fingerprint: `UNKNOWN`
- observed UID: `UNKNOWN`
- observed primary-key count: `UNKNOWN`
- packet sequence: `UNKNOWN`

The packaged copyright record is:

`usr/share/doc/ubuntu-keyring/copyright`

Canonical's versioned copyright text states that the key material does not
fall under copyright and that other package support files are offered under
GPL version 2 or later:

- <https://changelogs.ubuntu.com/changelogs/pool/main/u/ubuntu-keyring/ubuntu-keyring_2023.11.28.1/copyright>

This records a source declaration only. It is not a new project license
verdict.

## Ubuntu 24.04.4 checksum fixtures

Canonical's version-specific release directory lists:

| Object | Last modified | Bytes |
|---|---|---:|
| `SHA256SUMS` | `2026-02-12 14:46` | 594 |
| `SHA256SUMS.gpg` | `2026-02-12 14:46` | 833 |
| `ubuntu-24.04.4-live-server-amd64.iso` | `2026-02-10 06:53` | displayed as 3.2G |

Source:

- <https://releases.ubuntu.com/24.04.4/>

Candidate URLs:

- <https://releases.ubuntu.com/24.04.4/SHA256SUMS>
- <https://releases.ubuntu.com/24.04.4/SHA256SUMS.gpg>

The directory proves advertised names, version-specific location,
modification dates, and exact checksum/signature sizes. It does not provide an
authoritative SHA-256 for either object itself, prove endpoint immutability, or
prove zero redirects.

Both objects are therefore ineligible. Their bodies were not acquired. The ISO
is retained elsewhere in Task 2 and is not counted in this bounded
public-research blocker-object ledger.

## MSYS2 GnuPG candidate

The official MSYS2 record identifies:

- package: `gnupg`
- repository/environment: `msys`, `x86_64`
- version: `2.4.9-1`
- binary package: `gnupg-2.4.9-1-x86_64.pkg.tar.zst`
- binary SHA-256:
  `cd95fe16cc87700372549294a21f35b4adeed8bf57451cd2147e7f82f9e582eb`
- source-only package: `gnupg-2.4.9-1.src.tar.zst`
- declared member: `/usr/bin/gpgv.exe`
- package license declaration: `GPL`

Sources:

- <https://packages.msys2.org/packages/gnupg?variant=x86_64>
- <https://packages.msys2.org/base/gnupg>

The official record directly associates the binary record with the named
source-only package. This is not a version-only join. The source package's
exact size and authoritative digest remain `UNKNOWN`, and the record does not
bind the published binary or source package to a recipe commit.

Candidate URLs:

- <https://repo.msys2.org/msys/x86_64/gnupg-2.4.9-1-x86_64.pkg.tar.zst>
- <https://repo.msys2.org/msys/sources/gnupg-2.4.9-1.src.tar.zst>

The MSYS2 objects are research candidates only. They do not replace the
retained Git-for-Windows verifier route. `mirror.msys2.org` is a
geo-redirector and is ineligible as an acquisition route.

## Immutable MSYS2 recipe and patches

Candidate recipe commit:

- commit: `705cff2db01a907c02352781fc5cd2fcac61b50b`
- date: `2025-12-31T12:06:23Z`
- subject: `gnupg: Update to 2.4.9 (#5915)`

Sources:

- <https://github.com/msys2/MSYS2-packages/commit/705cff2db01a907c02352781fc5cd2fcac61b50b>
- <https://api.github.com/repos/msys2/MSYS2-packages/commits/705cff2db01a907c02352781fc5cd2fcac61b50b>

The immutable commit records `pkgver=2.4.9`, `pkgrel=1`, the upstream source
and digest, 16 unversioned runtime dependencies, and 26 ordered patches with
digests. It does not prove that the published binary was built from that
commit. Build-time proximity is not used as binding evidence.

The complete ordered patch list is preserved in `package-candidates.json`.

## Upstream GnuPG 2.4.9 source

The candidate recipe names:

- URL:
  <https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.4.9.tar.bz2>
- exact size: `8086407` bytes
- SHA-256:
  `dd17ab2e9a04fd79d39d853f599cbc852062ddb9ab52a4ddeb4176fd8b302964`
- release date: `2025-12-30`

Sources:

- <https://www.gnupg.org/download/integrity_check.html>
- <https://gnupg.org/ftp/gcrypt/gnupg/>
- <https://dev.gnupg.org/T8001>
- the immutable MSYS2 recipe commit above

The body was not acquired. Status and redirect count remain `UNKNOWN`.
Selection by the candidate recipe does not prove that this tarball is
corresponding source for the retained Git-for-Windows executable.

## Runtime dependency candidates

The recipe declares 16 unversioned direct runtime dependencies:

`bzip2`, `libassuan`, `libbz2`, `libcurl`, `libgcrypt`,
`libgpg-error`, `libgnutls`, `libiconv`, `libintl`, `libksba`,
`libnpth`, `libreadline`, `libsqlite`, `nettle`, `pinentry`, and `zlib`.

For each dependency, exact version, binary object, source object, digest,
size, notices, license inventory, and transitive dependencies remain
`UNKNOWN`. Mutable current package records cannot bind a historical package or
the retained observed host.

No zstd package, source, or license candidate is selected. A different
extractor is not authorized.

## Notices and licenses

The MSYS2 package record lists `/usr/share/doc/gnupg/DCO` and other
documentation, but no inspected record closes the exact binary package's
complete notice and license-file inventory.

GnuPG's contributor documentation states that GnuPG is GPLv3+ with some files
under mixed LGPLv3+/GPLv2+ terms:

- <https://www.gnupg.org/faq/HACKING.html>

The generic MSYS2 `GPL` declaration does not replace a release-specific
per-file inventory. Exact source notices, copying files, patch notices,
binary-package notices, and dependency licenses remain unresolved. No license
verdict is made.

## Git-for-Windows provenance

Primary documentation establishes that Git for Windows is based on MSYS2,
uses Pacman-style packages, consumes many packages built by MSYS2, and also
builds some components from its own package repositories:

- <https://gitforwindows.org/package-management>
- <https://gitforwindows.org/building-new-package-versions.html>
- <https://api.github.com/repos/git-for-windows/MSYS2-packages>
- <https://api.github.com/repos/git-for-windows/MSYS2-packages/commits?path=gnupg&per_page=10>

The inspected Git-for-Windows recipe history most recently showed its own
GnuPG update to 2.4.7 at commit
`e0b18bfd49c3787dbb72dcbc39cca61dc5ac5493`. It did not expose a 2.4.9 recipe
commit in that path history.

This does not prove whether the observed 2.4.9 executable was built by Git for
Windows or copied unchanged from MSYS2. Therefore:

- exact provenance remains `UNKNOWN`;
- host/package byte equality remains `UNKNOWN`;
- byte equality is not claimed; and
- observed SHA-256
  `f4d13204d77fdf63c02b0e6742230f83a833128c28f7b715709c2c63a96c427b`
  remains observation evidence, not acquisition pretrust.

## GnuPG support state

GnuPG's official download page states:

- branch: `2.4`
- birth: `2021-04-07`
- end of life: `2026-06-30`

Source:

- <https://www.gnupg.org/download/index.html>

As of `2026-08-07`, branch 2.4 is end-of-life. This fact does not authorize a
substitution for the retained 2.4.9 verifier route.

## Candidate-object arithmetic

The bounded public endpoint ledger contains eight candidate bodies:

```text
candidate_body_count = 8
known_size_body_count = 6
unknown_size_body_count = 2

known_bytes =
    11124
  + 1872
  + 20236
  + 594
  + 833
  + 8086407
  = 8121066

unknown_bytes =
    size(gnupg-2.4.9-1-x86_64.pkg.tar.zst)
  + size(gnupg-2.4.9-1.src.tar.zst)
  = UNKNOWN
```

A human-readable package size is not promoted to exact bytes. `UNKNOWN` is not
converted to zero.

Because recursive dependencies and runtime objects are not closed:

```text
direct_dependency_count = 16
patch_count = 26
blocker_count = 10
complete_candidate_body_count = UNKNOWN
complete_candidate_bytes = UNKNOWN
storage_ceiling_bytes = UNKNOWN
```

This blocker-object arithmetic is distinct from the retained Task-2 ISO
approval arithmetic and does not authorize acquisition.

## Common blocker set

1. `RETAINED_KEY_MEMBER_EXTRACTION_CLOSURE_UNKNOWN`
2. `NO_MEASURED_ZERO_REDIRECT_ENDPOINT`
3. `UBUNTU_CHECKSUM_OBJECT_DIGESTS_UNKNOWN`
4. `MSYS2_BINARY_PACKAGE_EXACT_SIZE_UNKNOWN`
5. `MSYS2_SOURCE_PACKAGE_SIZE_AND_DIGEST_UNKNOWN`
6. `MSYS2_BINARY_TO_RECIPE_COMMIT_BINDING_UNKNOWN`
7. `GIT_FOR_WINDOWS_HOST_PACKAGE_BINDING_UNKNOWN`
8. `RECURSIVE_DEPENDENCY_PACKAGE_SOURCE_LICENSE_CLOSURE_UNKNOWN`
9. `NOTICE_AND_LICENSE_CLOSURE_INCOMPLETE`
10. `COMPLETE_OBJECT_COUNT_BYTES_AND_STORAGE_UNKNOWN`

## Hostile RED/GREEN evaluation

| Case | Result |
|---|---|
| malformed JSON or missing required key | `REJECT` |
| mutable or not-proven-immutable URL | `REJECT` |
| `UNKNOWN` or nonzero redirect count | `REJECT` |
| missing authoritative digest or exact size | `REJECT` |
| missing package source, notice, or license | `REJECT` |
| source relation based only on matching version | `REJECT` |
| observed host digest used as acquisition trust | `REJECT` |
| selected member differs from the retained CD-image member | `REJECT` |
| route, object, count, arithmetic, blocker, or status mismatch across files | `REJECT` |
| alternate key, package, verifier, extractor, mirror, route, or fallback | `REJECT` |
| intact evidence with complete immutable zero-redirect closure | `NOT SATISFIED` |
| all four artifacts agree on retained route and current terminal status | `PASS` |

## Assumptions and risks

- Versioned filenames are candidate identities, not proof of immutable serving
  behavior.
- Directory listings establish advertised metadata, not acquired-body
  identity, redirect behavior, or availability.
- Recipe hashes establish recipe declarations, not published-binary
  provenance.
- Mutable package indexes were used only as research records and do not
  qualify acquisition endpoints.
- Historical objects may disappear or begin redirecting.
- The retained host may drift before any separately approved supplement.
- GnuPG 2.4 is already end-of-life.
- No fallback or alternate trust member is authorized.

BLOCKED
