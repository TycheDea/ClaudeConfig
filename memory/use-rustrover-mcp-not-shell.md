---
name: use-rustrover-mcp-not-shell
description: User correction — never use Bash sed/grep for reading or editing code in vordar; use rustrover-index MCP tools for navigation and Edit/Write for changes
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ab728cd2-e492-4e09-86a2-dbae33319a99
---

In the vordar repo, do not use Bash commands (sed, grep, cat) to read or modify source files.

**Why:** The user was explicit ("stop using expensive commands to read files, use the rustrover mcp"), and the project CLAUDE.md already says to prefer rustrover-index MCP tools for code navigation and refactoring.

**How to apply:** For finding definitions/references/files use `mcp__rustrover-index__ide_find_definition`, `ide_find_references`, `ide_search_text`, `ide_find_file`. For edits use the Edit/Write tools only. Reserve Bash for builds, tests, git, and asset downloads.
