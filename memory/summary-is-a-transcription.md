---
name: summary-is-a-transcription
description: Progress summaries drift — read the row's own cell, and for load-bearing claims the artifact (source, git log, test output); never repeat a summary as state
metadata:
  type: feedback
---

Fires when reading or writing a "done so far" line in a plan, or carrying phase state into a report, checkpoint message, or fresh context after a compact.

**Why:** a plan's progress paragraph read "rows 1–23 done" while a row's feature existed in zero source files — the overclaim lived only in the summary, was repeated to the user, and later rows were sequenced against a state that did not exist.

**How to apply:** a row is done only if its own cell records the verify command and output. Summary vs table: the table wins. Table vs artifact: the artifact wins. A cell carrying its own verification record is the record, not a transcription.
