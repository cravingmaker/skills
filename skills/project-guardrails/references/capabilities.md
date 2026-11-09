# Capabilities

Assess these in order. Each row names what the capability prevents and what counts as evidence that it is enforced. The tool column gives examples; a project's existing equivalent satisfies the row.

## Readability

| Capability | Prevents | Evidence of enforcement | Example tools |
| --- | --- | --- | --- |
| Formatter | Layout debates, noisy diffs | A `check` mode fails CI on unformatted files | Prettier, Ruff format |
| Linter with an explicit policy | Inconsistent patterns, unclear code | Lint fails CI; every rule has a deliberate setting | ESLint flat config, Ruff |
| Prose and doc checks | Unreadable docs and PR text | A prose linter runs on committed docs | Vale with `clear-communication`'s style |
| Consistent scripts | Different commands for the same job | One documented command per job (`lint`, `typecheck`, `test`, `validate`) used locally and in CI | `package.json` scripts, `Makefile` |

## Maintainability

| Capability | Prevents | Evidence of enforcement | Example tools |
| --- | --- | --- | --- |
| Strict type checking | Whole classes of runtime errors | Type check fails CI; strict flags on | `tsc --noEmit` with `strict`, a strict Python type checker |
| Behavior tests | Regressions | Tests run in CI; a deliberately broken behavior makes a test fail | Vitest, pytest |
| Dead code and unused dependencies | Drift and confusion | A check fails on unused files, exports, or dependencies | knip |
| Reproducible installs | "Works on my machine" | Lockfile committed; CI installs from it without changes | `npm ci`, `uv sync --locked` |
| Dependency policy | Surprise upgrades | Exact pins and a minimum release age, or the project's stated policy | `.npmrc` `save-exact`, `min-release-age` |
| Configuration drift checks | Settings that silently diverge from a template | A script compares settings with the reference and fails on drift | Template drift scripts |

## Security

| Capability | Prevents | Evidence of enforcement | Example tools |
| --- | --- | --- | --- |
| Pinned CI actions | Supply-chain swaps of action code | Every `uses:` pins a full commit SHA with a version comment | Manual pins, Dependabot for updates |
| Least-privilege workflow tokens | Token abuse | `permissions: {}` at the top; each job grants only what it needs | GitHub Actions `permissions` |
| Workflow static analysis | Injection, credential leaks in CI | Analyzer runs in CI and fails on findings | zizmor |
| Dependency vulnerability audit | Known-vulnerable dependencies | Audit runs in CI with a reviewed allowlist that expires | `npm audit` with audit-ci, pip-audit |
| Secret scanning | Committed credentials | Scanning enabled on the host or a scanner in CI | GitHub secret scanning, gitleaks |
| Repository settings | Unprotected main branch | Branch protection or rulesets require the CI checks | GitHub rulesets |

## Performance

Assess performance only where the project has a budget or a benchmark: a bundle-size limit, a benchmark job, a query-time threshold. A guardrail here fails when the measured number crosses the budget. Without a budget, report "not applicable" rather than inventing one.

## Verification

| Capability | Prevents | Evidence of enforcement |
| --- | --- | --- |
| Repeatable launch and drive | Claims about behavior nobody ran | An existing command or driver proves the named real surface; record a missing proof and conditionally use the `create-verification-skill` skill |
| Package smoke test | A published package that fails to import | CI packs the package and imports it in a clean consumer project |

## Agent environment

| Capability | Prevents | Evidence of enforcement |
| --- | --- | --- |
| Agent instructions point at the commands | Agents guessing how to check their work | AGENTS.md or CLAUDE.md names the validate command; no instruction restates what a config already enforces |
| Git hooks | Unformatted or failing commits | A pre-commit hook runs the fast checks on staged files |
| Agent hooks (optional) | Slow feedback while editing | See [agent-hooks.md](agent-hooks.md); CI remains the authority |
