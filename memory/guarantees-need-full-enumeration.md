---
name: guarantees-need-full-enumeration
description: "User asked for a guarantee (\"never prompts\") — enumerate and close EVERY source of the behavior, never ship a partial fix as complete"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8246bce-3b07-4b7a-986c-d3e802f2dca4
---

When the user asks for an absolute guarantee ("make it never ask", "permission to everything", "always/never X"), enumerate every mechanism that can produce the unwanted behavior and close each one, then report the list. Do not declare done after handling the obvious mechanism.

**Why:** The user asked for a no-prompt /implement-finding flow. I added permission allow rules only; the next worker run was interrupted six times by sandbox-escalation prompts ("run unsandboxed?") — a prompt source allow rules don't touch. The user called this out as laziness: "Stop the lazyness and the 'this is enough'."

**How to apply:** For Claude Code permission prompts specifically, the sources are: (1) permissions.allow rules — use the wildcard form `"Bash(*)"`, the bare `"Bash"` form empirically failed to suppress prompts for piped/compound commands, (2) sandbox escalation → close with `sandbox.enabled: false` or domain/path allowances, (3) permission-mode dialogs → `defaultMode: "bypassPermissions"` + `skipDangerousModePermissionPrompt: true`, and (4) **session latching** — permission mode and possibly rules are bound at session start, so settings edits do nothing for the running session; a restart (or Shift+Tab to cycle to bypass mode in-session) is part of the fix and must be stated as REQUIRED, not optional. All of this lives in this repo's `.claude/settings.local.json`. Generally: before claiming a guarantee holds, ask "what are ALL the paths to the bad outcome?" and verify each is closed — see also [[finding-review-alignment-only]] for the audit workflow this protects.
