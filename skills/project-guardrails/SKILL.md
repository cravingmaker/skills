---
name: project-guardrails
description: "Set up or audit project guardrails so wrong changes fail checks: format, lint, types, tests, CI, dependencies, and hooks. Use for project setup, enforcement audits, CI hardening, or wiring an authorized staged hook with the existing package manager and hook setup."
license: MIT
metadata:
  source: https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack
  source-revision: 6b0300214a09fd6029cfb7077043125758cd1fd2
  source-license: MIT, see LICENSE-pstack
  source-files: "pstack/skills/create-verification-skill/SKILL.md"
  local-changes: "Retained gap assessment and existing deterministic checks; added recurring-gap tooling and an explicitly authorized native hook branch; moved the sole bounded/full-map authoring recipe to create-verification-skill and kept a conditional pointer without new prerequisites."
---

# Project guardrails

A **guardrail** is a check that fails when a change is wrong, runs the same way locally and in CI, and names the fix. Guardrails turn review comments into deterministic failures, so the agent's work is right because the environment rejects the wrong version.

The goal order is fixed: readability, then maintainability, then security, then performance. When two choices conflict, the earlier goal wins.

The checklist in [references/capabilities.md](references/capabilities.md) lists capabilities to assess, not tools to install. A project that already enforces a capability with a different tool keeps its tool.

When the request only reports an already identified proof gap, keep the answer on that gap and its supplied evidence. If the named verification helper is unavailable, report the gap, missing helper, and open proof, then stop that flow. A missing helper does not call for another inventory, version lookup, or replacement procedure.

## Steps

1. **Scope.** Settle what was asked: a new project, an audit, or one capability. Resolve consequential ambiguity in one message before changing files.
2. **Inventory what exists.** Read the scripts (`package.json`, `pyproject.toml`, `Makefile`), the tool configs, the CI workflows, the git hooks, and the agent instructions. Run the existing checks. Mark each one as **enforced** (runs locally and in CI and fails on violations), **unwired** (configured but not run in CI, or not failing the build), or **broken**. Fixing an unwired or broken check comes before adding a new one.
3. **Pin down versions and policy.** Record the installed and intended versions, the supported runtimes, and the project's update policy (exact pins, minimum release age, lockfiles). Read guidance for those versions from official documentation and release notes. A docs MCP server is one way to retrieve them, not proof that they are current. When a version or its guidance cannot be established, say so and leave the default unchanged.
4. **Assess each capability** in scope, in goal order, using [references/capabilities.md](references/capabilities.md) and the stack profile: [TypeScript](references/typescript.md) or [Python](references/python.md). Status per capability: enforced, unwired, broken, missing, or not applicable, each with its evidence.
5. **Plan the smallest authorized change** for each gap. Prefer the user's shared configs and an existing deterministic project command. Build a new tool only for a recurring gap existing checks cannot cover; make it repeat-safe and prove it on a representative unit. Keep new dependencies, CI jobs and policy changes within current authority.
6. **Apply** the changes. Wire every check into one repository command that runs locally and in CI.
7. **Prove each changed guardrail.** Show it rejecting a representative violation and accepting valid code, in the real project or a temporary fixture copy. Record the file state produced by the first setup. For a setup command or script, rerun it. For a one-off manual edit, record the edit steps, then repeat the same inventory and intended setup on a temporary copy of that post-edit state; show that no further edit is needed. In both cases, show an empty content delta against the recorded state, including created or deleted files. Report the setup command or manual steps, comparison commands, exit statuses, and output. Use `git status --porcelain` only when a clean baseline has already been established; otherwise compare snapshots without changing existing work. When repeatability cannot be demonstrated, report it as open; final-state checks alone do not prove it. A guardrail without this repeat proof is not done.
8. **Report** with the template below.

Done when every capability in scope has a status with evidence, every changed guardrail has its reject, accept, and rerun proof, and every gap left open names its reason and source.

## Optional parts

- **Agent hooks** give the agent fast feedback while it edits. They are host-specific adapters around repository commands, never the enforcement itself: [references/agent-hooks.md](references/agent-hooks.md).
- **Verification of real behavior.** Assess whether the existing project commands or driver prove the named real surface. Only when a repeatable proof gap remains, read the `create-verification-skill` skill and select its bounded-gap mode within current authority. If that skill is unavailable, report the gap and missing helper; do not copy another authoring procedure here.

- **Staged checks and hooks.** When hook setup is explicitly authorized, preserve the installed package manager, formatter and hook configuration. Reuse the project's hook manager and staged-file command; wire only the missing hook. Compare staged/local/CI behavior, prove a representative rejection and valid acceptance, then repeat setup without a content delta. A hook supplements the repository's CI enforcement. An audit alone installs nothing.

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

Per-file provenance: [references/SOURCES.md](references/SOURCES.md).
