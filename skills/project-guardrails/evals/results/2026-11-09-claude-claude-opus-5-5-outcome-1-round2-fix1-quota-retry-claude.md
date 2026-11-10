# project-guardrails: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/` inside.

## Prompt

```text
The repository has an existing deterministic lint check that CI does not call. Wire that existing linter into the local validation command and CI before considering a new tool. Keep the change scoped; use real local commands and prove reject, accept and repeat behavior.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 17 | 0 |
| baseline | n/a | false | 15 | 0 |

Treatment: 40 response lines; changed files `.cache/npm/_logs/2026-11-09T14_55_18_170Z-debug-0.log, .cache/npm/_logs/2026-11-09T14_55_47_931Z-debug-0.log, .cache/npm/_logs/2026-11-09T14_55_48_331Z-debug-0.log, .cache/npm/_logs/2026-11-09T14_55_48_549Z-debug-0.log, .cache/npm/_logs/2026-11-09T14_55_48_728Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, package.json, scratch/after.txt, scratch/apply.py, scratch/before.txt, scratch/copy.py, scratch/fresh/.cache/npm/_logs/2026-11-09T14_55_18_170Z-debug-0.log, scratch/fresh/.cache/npm/_logs/2026-11-09T14_55_47_931Z-debug-0.log, scratch/fresh/.cache/npm/_logs/2026-11-09T14_55_48_331Z-debug-0.log, scratch/fresh/.cache/npm/_logs/2026-11-09T14_55_48_549Z-debug-0.log, scratch/fresh/.cache/npm/_logs/2026-11-09T14_55_48_728Z-debug-0.log, scratch/fresh/.cache/npm/_update-notifier-last-checked, scratch/fresh/.github/workflows/check.yml, scratch/fresh/CLAUDE.md, scratch/fresh/CONTRIBUTING.md, scratch/fresh/README.md, scratch/fresh/eslint.config.mjs, scratch/fresh/package.json, scratch/fresh/paragraph.md, scratch/fresh/scripts/check.py, scratch/fresh/scripts/validate.sh, scratch/fresh/sources/workflow-actions.md, scratch/fresh/src/helper.py, scratch/fresh/src/index.ts, scratch/fresh/tests/sum.test.mjs, scratch/fresh/tests/test_smoke.py, scratch/post-edit.txt, scratch/reject/.cache/npm/_logs/2026-11-09T14_55_18_170Z-debug-0.log, scratch/reject/.cache/npm/_logs/2026-11-09T14_55_47_931Z-debug-0.log, scratch/reject/.cache/npm/_logs/2026-11-09T14_55_48_331Z-debug-0.log, scratch/reject/.cache/npm/_logs/2026-11-09T14_55_48_549Z-debug-0.log, scratch/reject/.cache/npm/_logs/2026-11-09T14_55_48_728Z-debug-0.log, scratch/reject/.cache/npm/_update-notifier-last-checked, scratch/reject/.github/workflows/check.yml, scratch/reject/CLAUDE.md, scratch/reject/CONTRIBUTING.md, scratch/reject/README.md, scratch/reject/eslint.config.mjs, scratch/reject/package.json, scratch/reject/paragraph.md, scratch/reject/scripts/check.py, scratch/reject/scripts/validate.sh, scratch/reject/sources/workflow-actions.md, scratch/reject/src/helper.py, scratch/reject/src/index.ts, scratch/reject/tests/sum.test.mjs, scratch/reject/tests/test_smoke.py, scratch/repeat/.cache/npm/_logs/2026-11-09T14_55_18_170Z-debug-0.log, scratch/repeat/.cache/npm/_logs/2026-11-09T14_55_47_931Z-debug-0.log, scratch/repeat/.cache/npm/_logs/2026-11-09T14_55_48_331Z-debug-0.log, scratch/repeat/.cache/npm/_logs/2026-11-09T14_55_48_549Z-debug-0.log, scratch/repeat/.cache/npm/_logs/2026-11-09T14_55_48_728Z-debug-0.log, scratch/repeat/.cache/npm/_update-notifier-last-checked, scratch/repeat/.github/workflows/check.yml, scratch/repeat/CLAUDE.md, scratch/repeat/CONTRIBUTING.md, scratch/repeat/README.md, scratch/repeat/eslint.config.mjs, scratch/repeat/package.json, scratch/repeat/paragraph.md, scratch/repeat/scripts/check.py, scratch/repeat/scripts/validate.sh, scratch/repeat/sources/workflow-actions.md, scratch/repeat/src/helper.py, scratch/repeat/src/index.ts, scratch/repeat/tests/sum.test.mjs, scratch/repeat/tests/test_smoke.py, scratch/rerun1.txt, scratch/rerun2.txt, scratch/run_script.py, scratch/snapshot.py, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 139.777 seconds and 17 tool calls; token usage is in the JSON record.

Baseline: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T14_57_47_631Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, package.json, scratch/clean/.github/workflows/check.yml, scratch/clean/package.json, scratch/clean/scripts/check.py, scratch/clean/scripts/validate.sh, scratch/clean/src/helper.py, scratch/clean/src/index.ts, scratch/clean/tests/sum.test.mjs, scratch/clean/tests/test_smoke.py, scratch/dirty/.github/workflows/check.yml, scratch/dirty/package.json, scratch/dirty/scripts/check.py, scratch/dirty/scripts/validate.sh, scratch/dirty/src/helper.py, scratch/dirty/src/index.ts, scratch/dirty/tests/sum.test.mjs, scratch/dirty/tests/test_smoke.py, scratch/probe.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 108.551 seconds and 15 tool calls; token usage is in the JSON record.


Expected deliverable: A fixture project with a configured but unwired linter gets it wired into CI before any new tool is added.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-quota-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
