---
name: project-guardrails
description: Set up or audit a project's guardrails (formatter, linter, strict types, tests, CI, dependency and workflow security, git and agent hooks) so a wrong change fails a check, ordered by readability, maintainability, security, then performance. Use when starting or adopting a project, auditing what a repo enforces, or when the user asks to harden, tighten, or add guardrails.
license: MIT
metadata:
  source: https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack
  source-revision: 6b0300214a09fd6029cfb7077043125758cd1fd2
  source-license: MIT, see LICENSE-pstack
  source-files: "pstack/skills/create-verification-skill/SKILL.md"
  local-changes: "Kept a conditional launch, doctor, drive, evidence, and cleanup recipe; omitted feature sweeps and maintenance loops."
---

# Project guardrails

A **guardrail** is a check that fails when a change is wrong, runs the same way locally and in CI, and names the fix. Guardrails turn review comments into deterministic failures, so the agent's work is right because the environment rejects the wrong version.

The goal order is fixed: readability, then maintainability, then security, then performance. When two choices conflict, the earlier goal wins.

The checklist in [references/capabilities.md](references/capabilities.md) lists capabilities to assess, not tools to install. A project that already enforces a capability with a different tool keeps its tool.

## Steps

1. **Scope.** Settle what was asked: a new project, an audit, or one capability. Resolve consequential ambiguity in one message before changing files.
2. **Inventory what exists.** Read the scripts (`package.json`, `pyproject.toml`, `Makefile`), the tool configs, the CI workflows, the git hooks, and the agent instructions. Run the existing checks. Mark each one as **enforced** (runs locally and in CI and fails on violations), **unwired** (configured but not run in CI, or not failing the build), or **broken**. Fixing an unwired or broken check comes before adding a new one.
3. **Pin down versions and policy.** Record the installed and intended versions, the supported runtimes, and the project's update policy (exact pins, minimum release age, lockfiles). Read guidance for those versions from official documentation and release notes. A docs MCP server is one way to retrieve them, not proof that they are current. When a version or its guidance cannot be established, say so and leave the default unchanged.
4. **Assess each capability** in scope, in goal order, using [references/capabilities.md](references/capabilities.md) and the stack profile: [TypeScript](references/typescript.md) or [Python](references/python.md). Status per capability: enforced, unwired, broken, missing, or not applicable, each with its evidence.
5. **Plan the smallest authorized change** for each gap. Prefer the user's shared configs and the project's established commands. Ask before adding a tool, a dependency, or a CI job the user has not approved.
6. **Apply** the changes. Wire every check into one repository command that runs locally and in CI.
7. **Prove each changed guardrail.** Show it rejecting a representative violation and accepting valid code, in the real project or a temporary fixture copy. Then run the setup again and show that it changes nothing: `git status --porcelain` (or the project's equivalent) is empty after the second run. Report the command and its output; a guardrail without this rerun proof is not done.
8. **Report** with the template below.

Done when every capability in scope has a status with evidence, every changed guardrail has its reject, accept, and rerun proof, and every gap left open names its reason and source.

## Optional parts

- **Agent hooks** give the agent fast feedback while it edits. They are host-specific adapters around repository commands, never the enforcement itself: [references/agent-hooks.md](references/agent-hooks.md).
- **Verification of real behavior.** When the project has no repeatable way to launch and drive the real app, build one: [references/verification-recipe.md](references/verification-recipe.md).

## Report template

```markdown
## Guardrails: <project>

Scope: <what was asked>. Versions: <tool@version, runtime@version>, sources: <links>.

| Goal | Capability | Status | Evidence |
| --- | --- | --- | --- |
| Readability | Formatter | enforced | `npm run format:check` in CI job `static` |

Changes: <file: what changed>.
Proof: <guardrail: violation rejected (command, output); valid code accepted; rerun clean>.
Open: <gap: reason, source, next step>.
```
