---
name: glob-absence-needs-ls
description: Fires whenever a Glob/search miss is about to become a claim that a file or script does not exist
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2b9bcc16-1481-4d32-8e26-91e194d90a1e
  modified: 2026-08-07T09:54:07.275Z
---

A Glob "No files found" is not evidence of absence in this environment. Reproduced 2026-08-07: `**/lint-findings.sh`, `scripts/*.sh`, and `scripts/*.py` all returned "No files found" while the files existed (`ls scripts/lint-findings.sh` succeeded); the exact literal `scripts/campaign_report.py` did match. Wildcards under the game repo's `scripts/` reliably false-negative.

**Why:** an absence claim built on a glob miss propagated into four audit dispatch briefs as "lint-findings.sh no longer exists"; every worker had to contradict it.

**How to apply:** before asserting a file is missing (or telling a worker to skip a gate because of it), confirm with `ls <path>` or a direct Read. Artifact: the gate notes in all four `docs/reviews/*/audit-*-2026-08-07.md` headers record the corrected claim.
