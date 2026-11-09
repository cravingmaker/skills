# project-guardrails: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
The repository has an existing deterministic lint check that CI does not call. Wire that existing linter into the local validation command and CI before considering a new tool. Keep the change scoped; use real local commands and prove reject, accept and repeat behavior.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 20 | 0 |
| baseline | n/a | false | 15 | 0 |

Treatment: 39 response lines; changed files `.cache/npm/_logs/2026-11-09T15_19_16_446Z-debug-0.log, .github/workflows/check.yml, scratch/accept.out, scratch/accept/.cache/npm/_logs/2026-11-09T15_19_16_446Z-debug-0.log, scratch/accept/.github/workflows/check.yml, scratch/accept/CLAUDE.md, scratch/accept/CONTRIBUTING.md, scratch/accept/README.md, scratch/accept/eslint.config.mjs, scratch/accept/package.json, scratch/accept/paragraph.md, scratch/accept/scripts/check.py, scratch/accept/scripts/validate.sh, scratch/accept/sources/workflow-actions.md, scratch/accept/src/helper.py, scratch/accept/src/index.ts, scratch/accept/tests/sum.test.mjs, scratch/accept/tests/test_smoke.py, scratch/apply.py, scratch/base.list, scratch/baseline.sha, scratch/baseline/.cache/npm/_logs/2026-11-09T15_19_16_446Z-debug-0.log, scratch/baseline/.github/workflows/check.yml, scratch/baseline/CLAUDE.md, scratch/baseline/CONTRIBUTING.md, scratch/baseline/README.md, scratch/baseline/eslint.config.mjs, scratch/baseline/package.json, scratch/baseline/paragraph.md, scratch/baseline/scripts/check.py, scratch/baseline/scripts/validate.sh, scratch/baseline/sources/workflow-actions.md, scratch/baseline/src/helper.py, scratch/baseline/src/index.ts, scratch/baseline/tests/sum.test.mjs, scratch/baseline/tests/test_smoke.py, scratch/control/.cache/npm/_logs/2026-11-09T15_19_16_446Z-debug-0.log, scratch/control/.github/workflows/check.yml, scratch/control/CLAUDE.md, scratch/control/CONTRIBUTING.md, scratch/control/README.md, scratch/control/eslint.config.mjs, scratch/control/package.json, scratch/control/paragraph.md, scratch/control/scripts/check.py, scratch/control/scripts/validate.sh, scratch/control/sources/workflow-actions.md, scratch/control/src/helper.py, scratch/control/src/index.ts, scratch/control/tests/sum.test.mjs, scratch/control/tests/test_smoke.py, scratch/final.sha, scratch/fresh/.cache/npm/_logs/2026-11-09T15_19_16_446Z-debug-0.log, scratch/fresh/.github/workflows/check.yml, scratch/fresh/CLAUDE.md, scratch/fresh/CONTRIBUTING.md, scratch/fresh/README.md, scratch/fresh/eslint.config.mjs, scratch/fresh/package.json, scratch/fresh/paragraph.md, scratch/fresh/scripts/check.py, scratch/fresh/scripts/validate.sh, scratch/fresh/sources/workflow-actions.md, scratch/fresh/src/helper.py, scratch/fresh/src/index.ts, scratch/fresh/tests/sum.test.mjs, scratch/fresh/tests/test_smoke.py, scratch/fresh1.sha, scratch/fresh2.sha, scratch/now.list, scratch/npm-cache/_logs/2026-11-09T15_20_00_838Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_01_241Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_01_432Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_01_643Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_07_183Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_24_837Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_25_162Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/out.txt, scratch/post.sha, scratch/reject.out, scratch/reject/.cache/npm/_logs/2026-11-09T15_19_16_446Z-debug-0.log, scratch/reject/.github/workflows/check.yml, scratch/reject/CLAUDE.md, scratch/reject/CONTRIBUTING.md, scratch/reject/README.md, scratch/reject/eslint.config.mjs, scratch/reject/package.json, scratch/reject/paragraph.md, scratch/reject/scripts/check.py, scratch/reject/scripts/validate.sh, scratch/reject/sources/workflow-actions.md, scratch/reject/src/helper.py, scratch/reject/src/index.ts, scratch/reject/tests/sum.test.mjs, scratch/reject/tests/test_smoke.py, scratch/repeat.sha, scratch/repeat/.cache/npm/_logs/2026-11-09T15_19_16_446Z-debug-0.log, scratch/repeat/.github/workflows/check.yml, scratch/repeat/CLAUDE.md, scratch/repeat/CONTRIBUTING.md, scratch/repeat/README.md, scratch/repeat/eslint.config.mjs, scratch/repeat/package.json, scratch/repeat/paragraph.md, scratch/repeat/scripts/check.py, scratch/repeat/scripts/validate.sh, scratch/repeat/sources/workflow-actions.md, scratch/repeat/src/helper.py, scratch/repeat/src/index.ts, scratch/repeat/tests/sum.test.mjs, scratch/repeat/tests/test_smoke.py, scripts/validate.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 166.768 seconds and 20 tool calls; token usage is in the JSON record.

Baseline: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T15_22_03_044Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, package.json, scratch/orig/check.yml, scratch/orig/package.json, scratch/probe/.github/workflows/check.yml, scratch/probe/package.json, scratch/probe/scripts/check.py, scratch/probe/scripts/validate.sh, scratch/probe/src/bad.ts, scratch/probe/src/helper.py, scratch/probe/src/index.ts, scratch/probe/tests/sum.test.mjs, scratch/probe/tests/test_smoke.py, scratch/run.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 102.667 seconds and 15 tool calls; token usage is in the JSON record.


Expected deliverable: A fixture project with a configured but unwired linter gets it wired into CI before any new tool is added.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: partial. Treatment: partial. Value: matched.

Both wire the existing deterministic linter into local/CI configuration with no new tool. Treatment executes the direct validator reject/accept and an idempotent edit replay; baseline uses an npm-script interpreter stand-in. Real npm spawning is EPERM and hosted CI is unrun, so neither earns full npm/CI proof.
