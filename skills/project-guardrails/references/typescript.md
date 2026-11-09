# TypeScript profile

The reference implementation is the user's own stack. Read these repositories for the current settings instead of copying values from this file:

- **[cravingmaker/package-template](https://github.com/cravingmaker/package-template).** ESM-only TypeScript package layout, scripts, CI workflows, pinned actions, dependency policy, repository-settings and drift checks.
- **[cravingmaker/eslint-config](https://github.com/cravingmaker/eslint-config).** TypeScript-first flat config with an explicit setting for every rule.
- **[cravingmaker/prettier-config](https://github.com/cravingmaker/prettier-config).** Formatting, including `proseWrap: "never"` for Markdown.

## Where to look in a project

| Capability | Look at |
| --- | --- |
| Scripts | `package.json` `scripts`; one `validate` script that chains the checks |
| Formatter | `prettier.config.*` or the `prettier` key in `package.json`; a `format:check` script |
| Linter | `eslint.config.*`; a `lint` script with no warnings allowed |
| Types | `tsconfig.json`: `strict` and the stricter flags the reference template enables |
| Tests | `vitest.config.*`; a `test` script that CI runs |
| Dead code | `knip.json` or `knip.config.*` |
| Dependency policy | `.npmrc` (`save-exact`, `min-release-age`), the lockfile, Dependabot or Renovate config |
| Audit | an `audit` script or `audit-ci.json` |
| CI | `.github/workflows/*.yml`: pinned SHAs, `permissions`, which scripts run |
| Workflow analysis | a zizmor job |
| Git hooks | `.husky/`, `lint-staged` config |
| Releases | `release-please-config.json`, `.release-please-manifest.json` |

## Version rule

Use the versions the project pins. For a new project, take the versions the reference template pins today, then check each one's release notes for breaking changes before adopting it.
