# project-guardrails: claude activation-1

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `19d23957b323b07f81d893869fa718d2fc4d2bea`, actual bytes SHA-256 `8c38dc1412508ef8db646c18de40214dd3c62a551651c9ac0fd938ec06c79fd8`; dirty: `False`.
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
| treatment | true | true | 27 | 0 |
| baseline | false | false | 12 | 0 |

Treatment: 57 response lines; changed files `.cache/npm/_logs/2026-11-09T03_52_58_562Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_52_59_545Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_53_00_082Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_53_00_524Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_53_05_496Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_53_11_319Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_53_15_087Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_55_06_947Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_55_07_274Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_55_07_652Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_55_08_056Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, CLAUDE.md, package.json, scripts/check.py, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 217.274 seconds and 27 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T03_57_12_912Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_57_34_399Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_57_34_860Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_57_35_137Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_57_38_051Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_57_38_242Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_57_38_411Z-debug-0.log, .cache/npm/_update-notifier-last-checked, .github/workflows/check.yml, package.json, scripts/check.py, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 68.992 seconds and 12 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: an inventory first, then the smallest changes that wire format, lint, type, and test checks into one command used locally and in CI, with reject, accept, and rerun proof for each.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-timeout-retry-claude/baseline/artifacts/`.

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
