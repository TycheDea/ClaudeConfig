---
name: finding-review-alignment-only
description: "Reviewing a finding-worker's output = check alignment with the audit finding, not /code-review"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8246bce-3b07-4b7a-986c-d3e802f2dca4
---

When the user asks to review a finding-worker subagent's diff (pi or Claude Code, via [[dev-singleplayer-pack]] audit workflow), do NOT invoke the /code-review skill — read the diff directly and check it against the audit finding's Evidence/Ideal/Suggestion/Path sections, verify the test is real (fail-first, calls production code, constructs the named scenario), confirm scope is surgical, run the tests, then commit if asked.

**Why:** The user interrupted a /code-review invocation and said "dont use code review, just check it alligns what is expected from the audit finding." The audit finding is the spec; alignment plus test verification is the whole review.

**How to apply:** For worker-output reviews: diff → compare to finding text → run new test + crate suite → report alignment verdict. Reserve /code-review for when the user explicitly asks for a general review of their own changes.
