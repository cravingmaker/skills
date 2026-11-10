# project-guardrails: claude activation-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `custom-hook`, SHA-256 `67a3757d431e39232095e8fdcbf6fecb55dcc6cae6102e95274dda6986592b74`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/` inside.

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
| treatment | true | true | 16 | 0 |
| baseline | false | false | 22 | 0 |

Treatment: 38 response lines; changed files `.cache/npm/_logs/2026-11-09T11_25_30_612Z-debug-0.log, hooks/pre-commit, scratch/npm-cache/_logs/2026-11-09T11_27_19_521Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/npm-logs/2026-11-09T11_26_06_206Z-debug-0.log, scratch/npm-logs/2026-11-09T11_26_06_574Z-debug-0.log, scratch/npm-logs/2026-11-09T11_26_06_787Z-debug-0.log, scratch/npm-logs/2026-11-09T11_26_06_980Z-debug-0.log, scratch/npm-logs/2026-11-09T11_26_16_079Z-debug-0.log, scratch/npm-logs/2026-11-09T11_26_16_286Z-debug-0.log, scratch/npm-logs/2026-11-09T11_26_16_465Z-debug-0.log, scratch/npm-logs/2026-11-09T11_26_23_581Z-debug-0.log, scratch/npm-logs/_update-notifier-last-checked, scratch/pre-commit.orig, scratch/tmp/fixture/hooks/pre-commit, scratch/tmp/fixture/package.json, scratch/tmp/fixture/scripts/check.py, scratch/tmp/fixture/scripts/validate.sh, scratch/tmp/fixture/src/helper.py, scratch/tmp/fixture/src/index.ts, scratch/tmp/npmprobe/package.json, scratch/tmp/shim/npm, scratch/tmp/snap-after1.txt, scratch/tmp/snap-after2.txt, scratch/tmp/snap-before.txt, scratch/wire-pre-commit.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 128.803 seconds and 16 tool calls; token usage is in the JSON record.

Baseline: 22 response lines; changed files `.cache/npm/_logs/2026-11-09T11_29_28_718Z-debug-0.log, .cache/npm/_update-notifier-last-checked, hooks/pre-commit, scratch/npm-cache/_logs/2026-11-09T11_30_01_939Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T11_30_10_153Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T11_30_13_386Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/probe/src/probe.ts, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 87.01 seconds and 22 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-fix1-claude/baseline/artifacts/`.
