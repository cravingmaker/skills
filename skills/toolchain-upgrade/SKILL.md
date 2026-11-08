---
name: toolchain-upgrade
description: Upgrade linters, formatters, type checkers, their plugins, and other dev tooling without silent drift, by comparing the effective configuration before and after, deciding every changed rule explicitly, and checking compatibility. Use when bumping dev dependencies or lint, format, or type tooling, or when Dependabot or Renovate opens such an update.
license: MIT
---

# Toolchain upgrade

An upgrade is safe when every change in **effective behavior** is known and decided. A version bump that passes CI can still change what the tools enforce: a new rule turned on by a preset, a changed default, a removed rule, a different autofix. This skill makes those changes visible and deliberate.

## Steps

1. **Scope the upgrade.** List the packages to upgrade and their target versions. Respect the project's update policy: exact pins, minimum release age, and one upgrade per commit when the project asks for that. A target version that violates the policy waits.
2. **Capture the before state.** Record resolved versions (the lockfile, not the ranges) and the effective configuration. Use the project's own inventories first: a policy-diff script, rule-coverage or rule-option tests, a printed resolved config (`eslint --print-config <file>`, `tsc --showConfig`, `prettier --find-config-path` with the resolved options).
3. **Read the release notes** for every version between the current and the target, from the official changelog or release page. Note breaking changes, new and removed rules, changed defaults and options, preset changes, autofix changes, and runtime or peer requirements.
4. **Upgrade** the packages and refresh the lockfile with the project's package manager.
5. **Capture the after state** the same way as step 2 and compare. Account for every difference:
   - added, removed, deprecated, and renamed rules
   - changed options and defaults
   - preset membership changes
   - autofix behavior changes
   - runtime and peer-dependency compatibility, including overrides and resolutions that now pin something stale
6. **Decide each difference.** Accept it, configure it explicitly, or reject the upgrade. When the project's policy says new rules stay off until the policy covers them, set them off explicitly. Record the reason for each decision.
7. **Verify.** Run the project's full checks, focused tests for any behavior that changed, and consumer checks when the project is a package others install (pack it and import it in a clean consumer).
8. **Report** with [references/upgrade-report.md](references/upgrade-report.md).

Done when every difference between the before and after states has a recorded decision, the full checks pass, and the report lists anything left unverified. Say the effective behavior is unchanged only when the comparison output is empty, and quote that output; a difference you configured back to its old value is still a decision to record.

## Rules

- One concern per change: the upgrade and its configuration decisions land together; unrelated fixes land separately.
- A failing check after an upgrade gets a decision, not a blanket disable. Disabling a rule is a recorded policy decision with a reason.
- When release notes are missing or unclear for a version, say so in the report and rely on the before-and-after comparison.
