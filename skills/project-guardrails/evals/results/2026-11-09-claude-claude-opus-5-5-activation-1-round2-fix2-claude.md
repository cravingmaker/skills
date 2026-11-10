# project-guardrails: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/` inside.

## Prompt

```text
Set up guardrails for this new TypeScript package.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 12 | 0 |
| baseline | false | false | 15 | 0 |

Treatment: 46 response lines; changed files `.cache/npm/_logs/2026-11-09T15_04_36_592Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_05_23_263Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_05_29_212Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_05_29_923Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_05_30_336Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_05_44_262Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_05_58_181Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_05_58_709Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_06_07_232Z-debug-0.log, .cache/npm/_update-notifier-last-checked, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 126.868 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 21 response lines; changed files `.cache/npm/_logs/2026-11-09T15_06_46_300Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_07_05_643Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_07_06_102Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_07_06_299Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_07_12_394Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_07_25_884Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_07_30_887Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_07_35_706Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, .gitignore, package.json, scripts/check.py, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 96.295 seconds and 15 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: an inventory first, then the smallest changes that wire format, lint, type, and test checks into one command used locally and in CI, with reject, accept, and rerun proof for each.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix2-claude/baseline/artifacts/`.
