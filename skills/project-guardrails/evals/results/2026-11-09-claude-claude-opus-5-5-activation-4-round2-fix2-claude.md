# project-guardrails: claude activation-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `custom-hook`, SHA-256 `67a3757d431e39232095e8fdcbf6fecb55dcc6cae6102e95274dda6986592b74`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/` inside.

## Prompt

```text
Wire the already-authorized staged lint hook using this project's existing package manager and hook setup.

Task context supplied identically to both arms:
Wire only existing staged command into existing hooks/pre-commit. Full staged parity remains unavailable without a real index.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 14 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T15_00_42_293Z-debug-0.log, .cache/npm/_update-notifier-last-checked, hooks/pre-commit, scratch/baseline.sha, scratch/fixture/.github/workflows/check.yml, scratch/fixture/CLAUDE.md, scratch/fixture/CONTRIBUTING.md, scratch/fixture/README.md, scratch/fixture/docs/hooks.md, scratch/fixture/eslint.config.mjs, scratch/fixture/hooks/pre-commit, scratch/fixture/package.json, scratch/fixture/paragraph.md, scratch/fixture/scripts/check.py, scratch/fixture/scripts/validate.sh, scratch/fixture/sources/workflow-actions.md, scratch/fixture/src/helper.py, scratch/fixture/src/index.ts, scratch/fixture/tests/sum.test.mjs, scratch/fixture/tests/test_smoke.py, scratch/npm-logs/2026-11-09T15_01_09_251Z-debug-0.log, scratch/npm-logs/2026-11-09T15_01_09_568Z-debug-0.log, scratch/npm-logs/2026-11-09T15_01_14_993Z-debug-0.log, scratch/npm-logs/2026-11-09T15_01_19_601Z-debug-0.log, scratch/npm-logs/2026-11-09T15_01_19_796Z-debug-0.log, scratch/npm-logs/2026-11-09T15_01_19_971Z-debug-0.log, scratch/post-edit.sha, scratch/pre-commit.orig, scratch/rerun.sha, scratch/shim/npm, scratch/tmp/fromorig/.github/workflows/check.yml, scratch/tmp/fromorig/CLAUDE.md, scratch/tmp/fromorig/CONTRIBUTING.md, scratch/tmp/fromorig/README.md, scratch/tmp/fromorig/docs/hooks.md, scratch/tmp/fromorig/eslint.config.mjs, scratch/tmp/fromorig/hooks/pre-commit, scratch/tmp/fromorig/package.json, scratch/tmp/fromorig/paragraph.md, scratch/tmp/fromorig/scripts/check.py, scratch/tmp/fromorig/scripts/validate.sh, scratch/tmp/fromorig/sources/workflow-actions.md, scratch/tmp/fromorig/src/helper.py, scratch/tmp/fromorig/src/index.ts, scratch/tmp/fromorig/tests/sum.test.mjs, scratch/tmp/fromorig/tests/test_smoke.py, scratch/tmp/rerun/.github/workflows/check.yml, scratch/tmp/rerun/CLAUDE.md, scratch/tmp/rerun/CONTRIBUTING.md, scratch/tmp/rerun/README.md, scratch/tmp/rerun/docs/hooks.md, scratch/tmp/rerun/eslint.config.mjs, scratch/tmp/rerun/hooks/pre-commit, scratch/tmp/rerun/package.json, scratch/tmp/rerun/paragraph.md, scratch/tmp/rerun/scripts/check.py, scratch/tmp/rerun/scripts/validate.sh, scratch/tmp/rerun/sources/workflow-actions.md, scratch/tmp/rerun/src/helper.py, scratch/tmp/rerun/src/index.ts, scratch/tmp/rerun/tests/sum.test.mjs, scratch/tmp/rerun/tests/test_smoke.py, scratch/tmp/wire-hook.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 115.951 seconds and 14 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T15_03_27_830Z-debug-0.log, hooks/pre-commit, scratch/npm-cache/_logs/2026-11-09T15_04_03_739Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/pre-commit-probe.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 68.316 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix2-claude/baseline/artifacts/`.
