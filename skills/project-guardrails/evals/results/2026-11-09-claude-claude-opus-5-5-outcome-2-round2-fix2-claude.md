# project-guardrails: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Wire the existing lint command into scripts/validate.sh. Prove the changed guardrail rejects a planted debugger statement, accepts valid source, and repeating the same setup leaves no content delta. Use an owned scratch copy for probes; preserve original source.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 17 | 0 |
| baseline | n/a | false | 17 | 0 |

Treatment: 42 response lines; changed files `.cache/npm/_logs/2026-11-09T15_19_48_807Z-debug-0.log, scratch/check-now.sha256, scratch/final.sha256, scratch/inventory/.github/workflows/check.yml, scratch/inventory/CLAUDE.md, scratch/inventory/CONTRIBUTING.md, scratch/inventory/README.md, scratch/inventory/eslint.config.mjs, scratch/inventory/package.json, scratch/inventory/paragraph.md, scratch/inventory/scripts/check.py, scratch/inventory/scripts/validate.sh, scratch/inventory/sources/workflow-actions.md, scratch/inventory/src/helper.py, scratch/inventory/src/index.ts, scratch/inventory/tests/sum.test.mjs, scratch/inventory/tests/test_smoke.py, scratch/npm-cache/_logs/2026-11-09T15_20_37_295Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_37_702Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_37_888Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_44_738Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_44_920Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_20_45_125Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/original.sha256, scratch/original/.github/workflows/check.yml, scratch/original/CLAUDE.md, scratch/original/CONTRIBUTING.md, scratch/original/README.md, scratch/original/eslint.config.mjs, scratch/original/package.json, scratch/original/paragraph.md, scratch/original/scripts/check.py, scratch/original/scripts/validate.sh, scratch/original/sources/workflow-actions.md, scratch/original/src/helper.py, scratch/original/src/index.ts, scratch/original/tests/sum.test.mjs, scratch/original/tests/test_smoke.py, scratch/out.txt, scratch/postedit-after.sha256, scratch/postedit-before.sha256, scratch/postedit/.github/workflows/check.yml, scratch/postedit/CLAUDE.md, scratch/postedit/CONTRIBUTING.md, scratch/postedit/README.md, scratch/postedit/eslint.config.mjs, scratch/postedit/package.json, scratch/postedit/paragraph.md, scratch/postedit/scripts/check.py, scratch/postedit/scripts/validate.sh, scratch/postedit/sources/workflow-actions.md, scratch/postedit/src/helper.py, scratch/postedit/src/index.ts, scratch/postedit/tests/sum.test.mjs, scratch/postedit/tests/test_smoke.py, scratch/probe/.github/workflows/check.yml, scratch/probe/CLAUDE.md, scratch/probe/CONTRIBUTING.md, scratch/probe/README.md, scratch/probe/eslint.config.mjs, scratch/probe/package.json, scratch/probe/paragraph.md, scratch/probe/scripts/check.py, scratch/probe/scripts/validate.sh, scratch/probe/sources/workflow-actions.md, scratch/probe/src/helper.py, scratch/probe/src/index.ts, scratch/probe/tests/sum.test.mjs, scratch/probe/tests/test_smoke.py, scratch/setup/.github/workflows/check.yml, scratch/setup/CLAUDE.md, scratch/setup/CONTRIBUTING.md, scratch/setup/README.md, scratch/setup/eslint.config.mjs, scratch/setup/package.json, scratch/setup/paragraph.md, scratch/setup/scripts/check.py, scratch/setup/scripts/validate.sh, scratch/setup/sources/workflow-actions.md, scratch/setup/src/helper.py, scratch/setup/src/index.ts, scratch/setup/tests/sum.test.mjs, scratch/setup/tests/test_smoke.py, scratch/setup1.sha256, scratch/setup2.sha256, scratch/tools/probe.sh, scratch/tools/wire-lint.sh, scripts/validate.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 137.158 seconds and 17 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T15_22_05_981Z-debug-0.log, scratch/after.sha, scratch/bad.log, scratch/bad/.github/workflows/check.yml, scratch/bad/CLAUDE.md, scratch/bad/CONTRIBUTING.md, scratch/bad/README.md, scratch/bad/eslint.config.mjs, scratch/bad/package.json, scratch/bad/paragraph.md, scratch/bad/scripts/check.py, scratch/bad/scripts/validate.sh, scratch/bad/sources/workflow-actions.md, scratch/bad/src/helper.py, scratch/bad/src/index.ts, scratch/bad/tests/sum.test.mjs, scratch/bad/tests/test_smoke.py, scratch/good.log, scratch/good/.github/workflows/check.yml, scratch/good/CLAUDE.md, scratch/good/CONTRIBUTING.md, scratch/good/README.md, scratch/good/eslint.config.mjs, scratch/good/package.json, scratch/good/paragraph.md, scratch/good/scripts/check.py, scratch/good/scripts/validate.sh, scratch/good/sources/workflow-actions.md, scratch/good/src/helper.py, scratch/good/src/index.ts, scratch/good/tests/__pycache__/test_smoke.cpython-315.pyc, scratch/good/tests/sum.test.mjs, scratch/good/tests/test_smoke.py, scratch/npm-cache/_logs/2026-11-09T15_22_44_482Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_22_45_587Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_22_59_935Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_23_04_327Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_23_09_911Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/probe.sh, scratch/rep1/.github/workflows/check.yml, scratch/rep1/CLAUDE.md, scratch/rep1/CONTRIBUTING.md, scratch/rep1/README.md, scratch/rep1/eslint.config.mjs, scratch/rep1/package.json, scratch/rep1/paragraph.md, scratch/rep1/scripts/check.py, scratch/rep1/scripts/validate.sh, scratch/rep1/sources/workflow-actions.md, scratch/rep1/src/helper.py, scratch/rep1/src/index.ts, scratch/rep1/tests/sum.test.mjs, scratch/rep1/tests/test_smoke.py, scratch/rep2/.github/workflows/check.yml, scratch/rep2/CLAUDE.md, scratch/rep2/CONTRIBUTING.md, scratch/rep2/README.md, scratch/rep2/eslint.config.mjs, scratch/rep2/package.json, scratch/rep2/paragraph.md, scratch/rep2/scripts/check.py, scratch/rep2/scripts/validate.sh, scratch/rep2/sources/workflow-actions.md, scratch/rep2/src/helper.py, scratch/rep2/src/index.ts, scratch/rep2/tests/sum.test.mjs, scratch/rep2/tests/test_smoke.py, scripts/validate.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 99.261 seconds and 17 tool calls; token usage is in the JSON record.


Expected deliverable: Each changed guardrail rejects a planted violation, accepts valid code, and running the setup a second time changes nothing.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: partial. Treatment: yes. Value: added.

Treatment changes only the requested validator, runs actual direct lint reject/accept on owned copies, and replays the setup transformation with zero content delta. It also demonstrates and fixes a wrong-current-directory false pass. Baseline proves direct lint reject/accept but its repeat compares copies rather than reapplying setup. Both disclose npm EPERM and preserve original source.
