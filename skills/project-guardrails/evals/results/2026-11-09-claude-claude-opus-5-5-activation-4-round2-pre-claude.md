# project-guardrails: claude activation-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8c38dc1412508ef8db646c18de40214dd3c62a551651c9ac0fd938ec06c79fd8`; dirty: `False`.
- **Fixture.** `activation-4`, SHA-256 `8bebc401d289685af35ea4c6260968fa1a4bfb22c8eaa28b17255091f6d89b54`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Wire the already-authorized staged lint hook using this project's existing package manager and hook setup.

Task context supplied identically to both arms:
Wire only existing staged command into existing .husky/pre-commit. Full staged parity remains unavailable without a real index.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 7 | 0 |
| baseline | false | false | 9 | 0 |

Treatment: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T11_16_55_130Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 35.744 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T11_19_33_407Z-debug-0.log, .husky/pre-commit, scratch/npm-cache/_logs/2026-11-09T11_19_58_447Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T11_20_02_378Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked`; removed files `none`; validation command present: `requires review`. Workflow cost: 41.093 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-pre-claude/baseline/artifacts/`.
