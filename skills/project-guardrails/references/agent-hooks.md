# Agent hooks

Agent hooks run a command when the agent does something, such as editing a file. They give fast feedback; they never replace the repository's checks. Final validation and CI remain the authority, and asynchronous feedback is not a passing gate.

## Rules

- **Adapters, not enforcement.** A hook calls a repository command. The same command runs locally and in CI without the hook.
- **Cheap per edit.** Per-edit hooks run only fast, changed-file checks, such as a format check or a lint of the edited file. Measure the latency on the real project and keep the hook only when it is acceptable.
- **Expensive work at a boundary.** Run the type check, the full lint, and the tests at a batch or completion boundary, not after every edit.
- **One writer.** Avoid a hook that rewrites files while the agent or another tool is also writing them. Prefer check modes that report over autofix modes that write.
- **Verify coverage on the installed host.** Confirm which events fire, which tools they cover, and how failures reach the agent, for the host version in use.

## Claude Code notes

Verify these against the hooks documentation for the installed version before relying on them:

- Hooks are configured in settings files under `hooks`, keyed by event such as `PostToolUse`, with a `matcher` on tool names.
- Command hooks block the agent until they finish; asynchronous hooks cannot block.
- A matcher on `Edit|Write` misses files changed through `Bash` or outside the agent, so a hook is never the only check.
- `PostToolUse` runs after the edit has happened; it reports, it does not prevent.

Example: a per-edit format check on the edited file, reporting only. This npm example requires `jq` and the project's pinned local Prettier. Map it to the project's existing commands; these scripts share the same check, and CI runs `format:check`:

```json
{
  "scripts": {
    "format:check:file": "prettier --check --ignore-unknown",
    "format:check": "npm run format:check:file -- ."
  }
}
```

For `PostToolUse`, return exit status 2 with diagnostics on stderr so Claude receives the failure; the edit has already happened. Preserve the path as one argument:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "file=$(jq -er '.tool_input.file_path | select(type == \"string\" and length > 0)') || { echo 'hook input needs tool_input.file_path' >&2; exit 2; }; cd \"$CLAUDE_PROJECT_DIR\" || exit 2; npm run --silent format:check:file -- \"$file\" >&2 || exit 2"
          }
        ]
      }
    ]
  }
}
```

## Other hosts

Codex, Gemini, and other agents have their own hook or rule mechanisms, or none. Document per host what is verified. When a host has no hook support, the agent runs the repository command itself before reporting work as done.
