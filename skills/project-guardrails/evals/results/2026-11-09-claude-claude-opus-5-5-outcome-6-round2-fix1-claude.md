# project-guardrails: claude outcome-6

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-6` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `custom-hook`, SHA-256 `67a3757d431e39232095e8fdcbf6fecb55dcc6cae6102e95274dda6986592b74`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Wire only the existing staged lint command into the existing custom Husky hook hooks/pre-commit, preserving npm and formatter configuration. Prefer the existing checker. Demonstrate rejection, valid acceptance and repeat evidence where executable, and report unavailable staged/local/CI parity explicitly. This source archive has no Git index.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 15 | 0 |
| baseline | n/a | false | 9 | 0 |

Treatment: 36 response lines; changed files `.cache/npm/_logs/2026-11-09T14_51_51_780Z-debug-0.log, hooks/pre-commit, scratch/baseline.sha, scratch/bin/npm, scratch/fixture.json, scratch/fixture/.cache/npm/_logs/2026-11-09T14_51_51_780Z-debug-0.log, scratch/fixture/.github/workflows/check.yml, scratch/fixture/CLAUDE.md, scratch/fixture/CONTRIBUTING.md, scratch/fixture/README.md, scratch/fixture/docs/hooks.md, scratch/fixture/eslint.config.mjs, scratch/fixture/hooks/pre-commit, scratch/fixture/package.json, scratch/fixture/paragraph.md, scratch/fixture/scripts/check.py, scratch/fixture/scripts/validate.sh, scratch/fixture/sources/workflow-actions.md, scratch/fixture/src/helper.py, scratch/fixture/src/index.ts, scratch/fixture/tests/sum.test.mjs, scratch/fixture/tests/test_smoke.py, scratch/now.json, scratch/npm-cache/_logs/2026-11-09T14_52_22_747Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_52_22_928Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_52_23_127Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_52_23_324Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_52_27_813Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_53_35_072Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_53_39_731Z-debug-0.log, scratch/post-edit.json, scratch/post-edit.snap, scratch/probe/setup-hook.sh, scratch/probe/snap.sh, scratch/probe/tree.py, scratch/repA.json, scratch/repA/.cache/npm/_logs/2026-11-09T14_51_51_780Z-debug-0.log, scratch/repA/.github/workflows/check.yml, scratch/repA/CLAUDE.md, scratch/repA/CONTRIBUTING.md, scratch/repA/README.md, scratch/repA/docs/hooks.md, scratch/repA/eslint.config.mjs, scratch/repA/hooks/pre-commit, scratch/repA/package.json, scratch/repA/paragraph.md, scratch/repA/scripts/check.py, scratch/repA/scripts/validate.sh, scratch/repA/sources/workflow-actions.md, scratch/repA/src/helper.py, scratch/repA/src/index.ts, scratch/repA/tests/sum.test.mjs, scratch/repA/tests/test_smoke.py, scratch/repA2.json, scratch/repB.json, scratch/repB/.cache/npm/_logs/2026-11-09T14_51_51_780Z-debug-0.log, scratch/repB/.github/workflows/check.yml, scratch/repB/CLAUDE.md, scratch/repB/CONTRIBUTING.md, scratch/repB/README.md, scratch/repB/docs/hooks.md, scratch/repB/eslint.config.mjs, scratch/repB/hooks/pre-commit, scratch/repB/package.json, scratch/repB/paragraph.md, scratch/repB/scripts/check.py, scratch/repB/scripts/validate.sh, scratch/repB/sources/workflow-actions.md, scratch/repB/src/helper.py, scratch/repB/src/index.ts, scratch/repB/tests/sum.test.mjs, scratch/repB/tests/test_smoke.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 137.846 seconds and 15 tool calls; token usage is in the JSON record.

Baseline: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T14_54_09_678Z-debug-0.log, hooks/pre-commit, scratch/fx/hooks/pre-commit, scratch/fx/package.json, scratch/fx/scripts/check.py, scratch/fx/scripts/validate.sh, scratch/fx/src/helper.py, scratch/fx/src/index.ts, scratch/npm-cache/_logs/2026-11-09T14_54_39_182Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_54_39_378Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_54_39_566Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_54_39_749Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_54_39_926Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_54_40_130Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_54_51_203Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 73.732 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: An existing deterministic check wins. A recurring uncovered gap justifies a small repeat-safe tool; authorized hook setup preserves formatter/package-manager/configuration and demonstrates staged/local/CI reject, accept and repeat parity.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
