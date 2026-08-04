---
name: commit-style-no-attribution
description: Commit messages — never add Co-Authored-By/Claude attribution; short pure descriptions of the change itself
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ab728cd2-e492-4e09-86a2-dbae33319a99
---

Never add "Co-Authored-By: Claude", "Generated with Claude Code", or any AI attribution to commits or PRs in this repo. Keep commit messages short, pure descriptions of the job itself.

**Why:** User instruction: "dont add co authored by claude or anything like that, pure descriptions short descriptions of the job itself." This overrides the harness default trailer.

**How to apply:** One summary line, optionally a couple of body lines describing what changed — no trailers, no attribution, no marketing.
