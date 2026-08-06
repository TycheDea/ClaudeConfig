import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  REQUIRED_CONTEXT_RELATIVE_PATHS,
  evaluateCommand,
  loadRequiredContext,
  registerVordarBootstrap,
  runPostWriteHooks,
  type HookInvocation,
} from "./index.ts";

function fixture(): string {
  const root = mkdtempSync(join(tmpdir(), "vordar-bootstrap-"));
  mkdirSync(join(root, ".claude", "memory"), { recursive: true });
  writeFileSync(join(root, ".claude", "CLAUDE.md"), "canonical law\n");
  writeFileSync(join(root, ".claude", "memory", "MEMORY.md"), "memory index\n");
  return root;
}

test("loads exactly the canonical law and memory index bodies", () => {
  const root = fixture();
  try {
    const files = loadRequiredContext(root);
    assert.deepEqual(files.map((file) => file.relativePath), REQUIRED_CONTEXT_RELATIVE_PATHS);
    assert.deepEqual(files.map((file) => file.body), ["canonical law\n", "memory index\n"]);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("fails visibly when either required context file cannot be read", () => {
  const root = fixture();
  try {
    rmSync(join(root, ".claude", "memory", "MEMORY.md"));
    assert.throws(
      () => loadRequiredContext(root),
      /Required Vordar context file is missing or unreadable: .*MEMORY\.md/,
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("allows ordinary commands and blocks commands confirmed by the existing policy", () => {
  const repoRoot = join(import.meta.dirname, "../../../..");
  assert.deepEqual(evaluateCommand(repoRoot, "git status"), { blocked: false });

  const forcePush = evaluateCommand(repoRoot, "git push --force origin main");
  assert.equal(forcePush.blocked, true);
  assert.match(forcePush.blocked ? forcePush.reason : "", /force-push/);

  const recursiveDelete = evaluateCommand(repoRoot, "rm -rf definitely-not-executed");
  assert.equal(recursiveDelete.blocked, true);
  assert.match(recursiveDelete.blocked ? recursiveDelete.reason : "", /recursive force-delete/);
});

test("wires bash, hypa_shell, user !, context deduplication, and post-write hooks", async () => {
  const root = fixture();
  const handlers = new Map<string, (...args: any[]) => any>();
  const seen: HookInvocation[] = [];
  const runner = (invocation: HookInvocation) => {
    seen.push(invocation);
    const command = (invocation.payload.tool_input as { command?: string }).command;
    return command?.includes("--force")
      ? { status: 2, stderr: "deny_dangerous: blocked\n" }
      : { status: 0, stderr: "" };
  };
  const pi = {
    on(name: string, handler: (...args: any[]) => any) {
      handlers.set(name, handler);
    },
  };

  try {
    registerVordarBootstrap(pi as any, runner);
    await handlers.get("session_start")?.({}, {
      cwd: root,
      hasUI: false,
      ui: { notify() {} },
    });

    const first = await handlers.get("before_agent_start")?.({ systemPrompt: "base" });
    const second = await handlers.get("before_agent_start")?.({ systemPrompt: first.systemPrompt });
    assert.equal(first.systemPrompt.match(/<project-file /g)?.length, 2);
    assert.equal(second, undefined);

    assert.equal(await handlers.get("tool_call")?.({ toolName: "bash", input: { command: "git status" } }), undefined);
    assert.deepEqual(
      await handlers.get("tool_call")?.({ toolName: "bash", input: { command: "git push --force origin main" } }),
      { block: true, reason: "deny_dangerous: blocked" },
    );
    assert.deepEqual(
      await handlers.get("tool_call")?.({ toolName: "hypa_shell", input: { command: "git push --force origin main" } }),
      { block: true, reason: "deny_dangerous: blocked" },
    );
    assert.equal(await handlers.get("user_bash")?.({ command: "git status" }), undefined);
    assert.equal((await handlers.get("user_bash")?.({ command: "git push --force origin main" })).result.exitCode, 2);

    const content = [{ type: "text", text: "ok" }];
    assert.equal(
      await handlers.get("tool_result")?.({
        toolName: "edit",
        input: { path: "game/src/edit.rs" },
        content,
        isError: false,
      }),
      undefined,
    );
    assert.equal(
      await handlers.get("tool_result")?.({
        toolName: "write",
        input: { path: "game/src/write.rs" },
        content,
        isError: false,
      }),
      undefined,
    );

    const postPayloads = seen.filter((entry) => !entry.scriptPath.endsWith("deny_dangerous.mjs"));
    assert.equal(postPayloads.length, 6);
    assert.deepEqual(
      [...new Set(postPayloads.map((entry) => (entry.payload.tool_input as { file_path: string }).file_path))],
      [join(root, "game/src/edit.rs"), join(root, "game/src/write.rs")],
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("marks rejected post-write lint results as errors without replacing existing content", async () => {
  const root = fixture();
  const handlers = new Map<string, (...args: any[]) => any>();
  const seen: HookInvocation[] = [];
  const runner = (invocation: HookInvocation) => {
    seen.push(invocation);
    return invocation.scriptPath.endsWith("comment_lint_hook.mjs")
      ? { status: 2, stderr: "comment_lint: rejected material issue\n" }
      : { status: 0, stderr: "" };
  };
  const pi = {
    on(name: string, handler: (...args: any[]) => any) {
      handlers.set(name, handler);
    },
  };

  try {
    registerVordarBootstrap(pi as any, runner);
    await handlers.get("session_start")?.({}, {
      cwd: root,
      hasUI: false,
      ui: { notify() {} },
    });

    const existingContent = [{ type: "text", text: "write completed" }];
    const result = await handlers.get("tool_result")?.({
      toolName: "write",
      input: { path: "game/src/rejected.rs" },
      content: existingContent,
      isError: false,
    });

    assert.deepEqual(result, {
      content: [
        ...existingContent,
        { type: "text", text: "Post-write checks failed:\ncomment_lint: rejected material issue" },
      ],
      isError: true,
    });
    assert.deepEqual(existingContent, [{ type: "text", text: "write completed" }]);
    assert.equal(seen.length, 3);
    assert.ok(
      seen.every(
        (entry) =>
          (entry.payload.tool_input as { file_path: string }).file_path === join(root, "game/src/rejected.rs"),
      ),
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("translates edit/write paths to Claude hook file_path payloads", () => {
  const root = fixture();
  const seen: HookInvocation[] = [];
  try {
    const failures = runPostWriteHooks(root, { path: "game/src/lib.rs" }, (invocation) => {
      seen.push(invocation);
      return { status: 0, stderr: "" };
    });

    assert.deepEqual(failures, []);
    assert.deepEqual(
      seen.map((entry) => entry.scriptPath.split(/[\\/]/).at(-1)),
      ["comment_lint_hook.mjs", "wgsl_hook.mjs", "test_shape_hook.mjs"],
    );
    assert.ok(
      seen.every(
        (entry) =>
          (entry.payload.tool_input as { file_path: string }).file_path === join(root, "game/src/lib.rs"),
      ),
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
