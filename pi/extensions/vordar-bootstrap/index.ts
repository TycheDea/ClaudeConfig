import { spawnSync } from "node:child_process";
import { readFileSync, statSync } from "node:fs";
import { dirname, isAbsolute, join, parse, resolve } from "node:path";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export const REQUIRED_CONTEXT_RELATIVE_PATHS = [
  ".claude/CLAUDE.md",
  ".claude/memory/MEMORY.md",
] as const;

const CONTEXT_MARKER = "<vordar-required-project-context>";
const DENY_HOOK = "deny_dangerous.mjs";
const POST_WRITE_HOOKS = ["comment_lint_hook.mjs", "wgsl_hook.mjs", "test_shape_hook.mjs"] as const;

type HookPayload = { tool_input: Record<string, unknown> };

export interface HookInvocation {
  scriptPath: string;
  payload: HookPayload;
  cwd: string;
}

export interface HookResult {
  status: number | null;
  stderr: string;
}

export type HookRunner = (invocation: HookInvocation) => HookResult;

export interface RequiredContextFile {
  relativePath: (typeof REQUIRED_CONTEXT_RELATIVE_PATHS)[number];
  absolutePath: string;
  body: string;
}

export function resolveWorkspace(startCwd: string): string {
  let candidate = resolve(startCwd);
  const filesystemRoot = parse(candidate).root;

  while (true) {
    try {
      if (statSync(join(candidate, ".claude")).isDirectory()) return candidate;
    } catch {
      // Keep walking. The extension may have been loaded through a .pi junction.
    }
    if (candidate === filesystemRoot) break;
    candidate = dirname(candidate);
  }

  throw new Error(`Unable to locate the Vordar workspace from ${startCwd}`);
}

export function loadRequiredContext(repoRoot: string): RequiredContextFile[] {
  return REQUIRED_CONTEXT_RELATIVE_PATHS.map((relativePath) => {
    const absolutePath = join(repoRoot, ...relativePath.split("/"));
    try {
      return { relativePath, absolutePath, body: readFileSync(absolutePath, "utf8") };
    } catch (error) {
      const detail = error instanceof Error ? ` (${error.message})` : "";
      throw new Error(`Required Vordar context file is missing or unreadable: ${absolutePath}${detail}`);
    }
  });
}

export function renderRequiredContext(files: readonly RequiredContextFile[]): string {
  if (
    files.length !== REQUIRED_CONTEXT_RELATIVE_PATHS.length ||
    files.some((file, index) => file.relativePath !== REQUIRED_CONTEXT_RELATIVE_PATHS[index])
  ) {
    throw new Error("Vordar bootstrap context must contain only the canonical law and memory index");
  }

  const bodies = files
    .map((file) => `<project-file path="${file.relativePath}">\n${file.body}\n</project-file>`)
    .join("\n\n");
  return `${CONTEXT_MARKER}\n${bodies}\n</vordar-required-project-context>`;
}

export const runHook: HookRunner = ({ scriptPath, payload, cwd }) => {
  try {
    const result = spawnSync(process.execPath, [scriptPath], {
      cwd,
      input: JSON.stringify(payload),
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
    });
    return { status: result.status, stderr: result.stderr ?? "" };
  } catch {
    return { status: null, stderr: "" };
  }
};

export function evaluateCommand(
  repoRoot: string,
  command: string,
  runner: HookRunner = runHook,
): { blocked: false } | { blocked: true; reason: string } {
  const result = runner({
    scriptPath: join(repoRoot, "scripts", "hooks", DENY_HOOK),
    payload: { tool_input: { command } },
    cwd: repoRoot,
  });
  if (result.status !== 2) return { blocked: false };
  return { blocked: true, reason: result.stderr.trim() || "Dangerous command blocked by Vordar policy" };
}

export function runPostWriteHooks(
  repoRoot: string,
  input: { path?: unknown },
  runner: HookRunner = runHook,
): string[] {
  if (typeof input.path !== "string" || input.path.length === 0) return [];
  const filePath = isAbsolute(input.path) ? input.path : resolve(repoRoot, input.path);
  const payload = { tool_input: { file_path: filePath } };

  return POST_WRITE_HOOKS.flatMap((hookName) => {
    const result = runner({
      scriptPath: join(repoRoot, "scripts", "hooks", hookName),
      payload,
      cwd: repoRoot,
    });
    return result.status === 2 ? [result.stderr.trim() || `${hookName} rejected the edit`] : [];
  });
}

export function registerVordarBootstrap(pi: ExtensionAPI, runner: HookRunner = runHook): void {
  let repoRoot: string | undefined;
  let contextBlock: string | undefined;

  pi.on("session_start", async (_event, ctx) => {
    repoRoot = undefined;
    contextBlock = undefined;
    try {
      repoRoot = resolveWorkspace(ctx.cwd);
      contextBlock = renderRequiredContext(loadRequiredContext(repoRoot));
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      if (ctx.hasUI) ctx.ui.notify(message, "error");
      throw error;
    }
  });

  pi.on("before_agent_start", async (event) => {
    if (!contextBlock) {
      throw new Error("Vordar required project context was not loaded");
    }
    if (event.systemPrompt.includes(CONTEXT_MARKER)) return undefined;
    return { systemPrompt: `${event.systemPrompt}\n\n${contextBlock}` };
  });

  pi.on("tool_call", async (event) => {
    if (event.toolName !== "bash" && event.toolName !== "hypa_shell") return undefined;
    const command = (event.input as { command?: unknown }).command;
    if (!repoRoot || typeof command !== "string") return undefined;
    const decision = evaluateCommand(repoRoot, command, runner);
    return decision.blocked ? { block: true, reason: decision.reason } : undefined;
  });

  pi.on("user_bash", async (event) => {
    if (!repoRoot) return undefined;
    const decision = evaluateCommand(repoRoot, event.command, runner);
    if (!decision.blocked) return undefined;
    return {
      result: {
        output: `${decision.reason}\n`,
        exitCode: 2,
        cancelled: false,
        truncated: false,
      },
    };
  });

  pi.on("tool_result", async (event) => {
    if (!repoRoot || event.isError || (event.toolName !== "edit" && event.toolName !== "write")) {
      return undefined;
    }
    const failures = runPostWriteHooks(repoRoot, event.input as { path?: unknown }, runner);
    if (failures.length === 0) return undefined;
    return {
      content: [
        ...event.content,
        { type: "text" as const, text: `Post-write checks failed:\n${failures.join("\n")}` },
      ],
      isError: true,
    };
  });
}

export default function vordarBootstrap(pi: ExtensionAPI): void {
  registerVordarBootstrap(pi);
}
