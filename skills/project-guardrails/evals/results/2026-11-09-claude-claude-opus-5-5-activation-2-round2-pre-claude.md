# project-guardrails: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `activation-2`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/` inside.

## Prompt

```text
Audit what this repo actually enforces.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 17 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 48 response lines; changed files `.cache/npm/_logs/2026-11-09T11_24_43_924Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 135.87 seconds and 17 tool calls; token usage is in the JSON record.

Baseline: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T11_28_36_043Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_28_50_173Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_28_50_511Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_28_50_688Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_28_50_876Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_28_51_131Z-debug-0.log, .cache/npm/_update-notifier-last-checked, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 46.04 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a capability table in goal order with enforced, unwired, broken, missing, or not applicable per row, each with evidence, and no changes made unless asked.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/artifacts/`.
