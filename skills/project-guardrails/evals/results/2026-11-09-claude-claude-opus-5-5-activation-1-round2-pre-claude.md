# project-guardrails: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Set up guardrails for this new TypeScript package.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 21 | 0 |
| baseline | false | false | 18 | 0 |

Treatment: 54 response lines; changed files `.cache/npm/_logs/2026-11-09T11_27_22_894Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_23_242Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_23_543Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_23_925Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_24_485Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_24_958Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_25_538Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_25_721Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_25_928Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_26_152Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_27_26_739Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, CLAUDE.md, package.json, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 182.582 seconds and 21 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T11_30_15_738Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_30_40_091Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_30_40_615Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_30_40_798Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_31_10_931Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_31_17_162Z-debug-0.log, .cache/npm/_logs/2026-11-09T11_31_17_516Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, package.json, scripts/check.py, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 91.463 seconds and 18 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: an inventory first, then the smallest changes that wire format, lint, type, and test checks into one command used locally and in CI, with reject, accept, and rerun proof for each.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/artifacts/`.
