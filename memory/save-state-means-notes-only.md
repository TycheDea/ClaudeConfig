---
name: save-state-means-notes-only
description: "\"Save the state\" / \"we'll continue tomorrow\" means write notes and stop — no new code, no runs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b4432896-ecfa-45b8-b5ff-e31e2bc7c901
  modified: 2026-07-25T22:22:49.951Z
---

When the user says to save the current state or that work resumes later, the
deliverable is **notes only**: update the plan/task files and end the turn. Do not
create scripts, refactor, or launch runs — even ones that would be justified
mid-task.

**Why:** they are closing the session. Anything started at that point either
lands unverified or blocks the close; a 5-minute job is not "quick" when the
answer wanted was "state is saved, you can stop".

**How to apply:** at a save-state request, write the files, list what is done and
what is next, and stop. If something genuinely needs building to make the state
reproducible, write it down as the next task instead of doing it. Related:
[[commit-style-no-attribution]] (session-close hygiene), and CLAUDE.md §9's
phase-gate rule, which this narrows — §9's "persist all state to files" means
notes, not artifacts.
