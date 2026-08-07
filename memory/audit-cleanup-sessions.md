---
name: audit-cleanup-sessions
description: "Fires when the user asks to \"make audits and clean up done audits/reviews\" (audit-and-remove-only sessions)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2b9bcc16-1481-4d32-8e26-91e194d90a1e
  modified: 2026-08-07T09:54:13.881Z
---

In these sessions the only permitted actions are running audits and removing/trimming report files — no implementation, no source edits (user ruling 2026-08-07, restated three times).

**How to apply:**
- Cleanup follows `audit-base.md` §Superseded reports. For a stale domain, dispatching a fresh audit IS the cleanup: the worker re-verifies and carries open items forward, then deletes the whole superseded set. Manually delete only sets no new audit will touch (resolved plan files, fully-closed superseded pairs).
- For a report file that is mostly done but holds live items, trim by pure deletion (user instruction 2026-08-07): remove closed done-records; keep parked gates, open Path steps, user rulings, watch items, and baselines future gates must consult; when in doubt, keep. Verify the trim diff adds no non-blank lines.
- Respect explicit retention rulings before deleting a fully-done set — e.g. the devloop 2026-07-17 pair is kept as telemetry corpus ([[keep-verification-artifacts]]).
- Other sessions may be working concurrently: check `.claude` repo status first, stage exact pathspecs only, commit and push per verified artifact ([[dispatch-discipline]]).
