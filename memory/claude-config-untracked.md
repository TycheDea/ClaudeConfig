---
name: claude-config-untracked
description: .claude/ is invisible to the vordar repo but is its own nested git repo pushed to TycheDea/ClaudeConfig
metadata: 
  node_type: memory
  type: project
  originSessionId: a8246bce-3b07-4b7a-986c-d3e802f2dca4
---

`.claude/`, `.pi/`, and `/tasks/` are gitignored in the vordar repo (commit 9a61e9d); the only Claude-produced artifacts committed to vordar are the report files under `docs/reviews/`. `vordar/.claude/` is additionally its OWN nested git repo with remote https://github.com/TycheDea/ClaudeConfig.git (branch main) — skills/, agents/, CLAUDE.md, DESIGN.md, CHARACTER-SYSTEM.md, tasks/ are tracked there; `settings.local.json` and `scheduled_tasks.lock` stay untracked via its local .gitignore.

**Why:** the repo carries outputs (reports), not machinery — but the machinery is too valuable to lose, so it versions separately in ClaudeConfig.

Auto-memory and tasks also live here: the real files are `vordar/.claude/memory/` and `vordar/.claude/tasks/` (tracked in ClaudeConfig). Only the harness memory path is a junction: `~/.claude/projects/C--Users-egm-8-IdeaProjects-vordar/memory` points at `vordar/.claude/memory/`. `.claude/tasks/` has no junction — it is referenced by its real path (`vordar/.claude/tasks/...`, never a project-root `tasks/...` path). User ruling: Claude progress/user files (tasks, memory, plans) belong in the ClaudeConfig repo, never the vordar repo — vordar carries only files with application in the project. On a fresh machine or a second workspace for this project, recreate the memory junction (`New-Item -ItemType Junction`) — without it the harness silently starts an empty memory.

**How to apply:** never `git add -f` `.claude/` into vordar. After meaningful edits to skills/agents/CLAUDE.md, commit and push from inside `.claude/` to ClaudeConfig (short pure descriptions, no attribution trailers). The user-level `~/.claude/skills/` holds duplicate copies of `implement-finding/SKILL.md` and `audit-base.md` that the harness sometimes resolves INSTEAD of the project copies — after editing either project file, copy it over the user-level twin or the stale copy silently shadows the change. Related: [[commit-style-no-attribution]], [[reworks-queue-mark-done]].
