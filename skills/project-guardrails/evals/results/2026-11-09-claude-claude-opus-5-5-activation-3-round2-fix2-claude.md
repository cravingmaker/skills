# project-guardrails: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `activation-3`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Harden the CI workflows.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 18 | 0 |
| baseline | false | false | 9 | 0 |

Treatment: 35 response lines; changed files `.cache/npm/_logs/2026-11-09T15_18_49_250Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_19_17_739Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_19_18_228Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_19_18_458Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_19_18_715Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, package.json, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 143.05 seconds and 18 tool calls; token usage is in the JSON record.

Baseline: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T15_21_11_614Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_21_36_838Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_21_40_708Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml`; removed files `none`; validation command present: `requires review`. Workflow cost: 44.83 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: pinned SHAs, least-privilege `permissions`, and workflow analysis assessed and proven, without unrelated changes.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-fix2-claude/baseline/artifacts/`.
