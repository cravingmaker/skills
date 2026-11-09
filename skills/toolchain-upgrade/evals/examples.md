# Examples

Run each prompt with and without this skill on a fixture copy of a project with a lint config. Record the observed behavior against the expectation.

## Activation

- "Bump the ESLint plugins to their latest versions." Expect: versions checked against the project's release-age and pinning policy, a before-and-after effective-config comparison, an explicit decision for every added or changed rule, and a report.
- "Dependabot opened a PR updating typescript-eslint. Is it safe to merge?" Expect: release notes read for every skipped version, effective-config differences listed with decisions, and the full checks run.

## Near miss

- "Add lodash as a dependency." Expect: a normal dependency addition, no toolchain comparison.
- "Why does this ESLint rule fire here?" Expect: an explanation of the rule; no upgrade.

## Outcome

- In a fixture where the new plugin version's preset turns on a new rule, the report names that rule and records an explicit decision; the rule does not change state silently.
- A target version younger than the project's minimum release age is held back and reported.
- A changed default is caught by the before-and-after comparison even when CI passes.
