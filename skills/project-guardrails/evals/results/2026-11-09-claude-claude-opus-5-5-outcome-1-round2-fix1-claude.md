# project-guardrails: claude outcome-1

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
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
| treatment | n/a | true | 12 | 0 |
| baseline | n/a | unavailable | unavailable | 1 |

Treatment: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T11_40_40_781Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, package.json, scratch/baseline/.github/workflows/check.yml, scratch/baseline/CLAUDE.md, scratch/baseline/CONTRIBUTING.md, scratch/baseline/README.md, scratch/baseline/eslint.config.mjs, scratch/baseline/package.json, scratch/baseline/paragraph.md, scratch/baseline/scripts/check.py, scratch/baseline/scripts/validate.sh, scratch/baseline/sources/workflow-actions.md, scratch/baseline/src/helper.py, scratch/baseline/src/index.ts, scratch/baseline/tests/sum.test.mjs, scratch/baseline/tests/test_smoke.py, scratch/bin/npm, scratch/fixture/.github/workflows/check.yml, scratch/fixture/CLAUDE.md, scratch/fixture/CONTRIBUTING.md, scratch/fixture/README.md, scratch/fixture/eslint.config.mjs, scratch/fixture/package.json, scratch/fixture/paragraph.md, scratch/fixture/scripts/check.py, scratch/fixture/scripts/validate.sh, scratch/fixture/sources/workflow-actions.md, scratch/fixture/src/helper.py, scratch/fixture/src/index.ts, scratch/fixture/tests/sum.test.mjs, scratch/fixture/tests/test_smoke.py, scratch/fresh/.github/workflows/check.yml, scratch/fresh/CLAUDE.md, scratch/fresh/CONTRIBUTING.md, scratch/fresh/README.md, scratch/fresh/eslint.config.mjs, scratch/fresh/package.json, scratch/fresh/paragraph.md, scratch/fresh/scripts/check.py, scratch/fresh/scripts/validate.sh, scratch/fresh/sources/workflow-actions.md, scratch/fresh/src/helper.py, scratch/fresh/src/index.ts, scratch/fresh/tests/sum.test.mjs, scratch/fresh/tests/test_smoke.py, scratch/index.ts.orig, scratch/m0-before.txt, scratch/m1-after-setup.txt, scratch/m2-after-rerun.txt, scratch/m3-fresh.txt, scratch/m4-repo-final.txt, scratch/manifest.sh, scratch/npm-cache/_logs/2026-11-09T11_42_28_079Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/wire-lint.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 137.734 seconds and 12 tool calls; token usage is in the JSON record.


Expected deliverable: A fixture project with a configured but unwired linter gets it wired into CI before any new tool is added.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/comparison.json).

## Invalid comparison

- claude baseline failed (exit 1, timeout False); inspect stderr and trace

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
