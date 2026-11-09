# work-decomposition: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `a2c45cd7b96032bbf48ce4911176ac7b3af7c9c2`, actual bytes SHA-256 `a83da8598f67faed667175b6c6782ffa69bb79ece6034a6591a00d2b2a60caaf`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `e966fe23e6fee51c1497d60cd19b67f33adae73a0513a390b7a6c3db91cde659`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Import the approved local ticket graph and spec at the configured nondefault paths without rewording or another breakdown.

Task context supplied to both arms:
Approved spec: docs/specs/saved-searches.md. Approved tickets: .planning/work-items/search/. Preserve exact sources. Planning only; 4 starts, 2 concurrent, reserve 1.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 12 | 0 |
| baseline | false | false | 18 | 0 |

Treatment: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T11_13_19_326Z-debug-0.log, .planning/runs/saved-searches-01/DECISIONS.md, .planning/runs/saved-searches-01/LOG.md, .planning/runs/saved-searches-01/PLAN.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 110.939 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `.cache/npm/_logs/2026-11-09T11_16_40_117Z-debug-0.log, .planning/runs/saved-searches/DECISIONS.md, .planning/runs/saved-searches/LOG.md, .planning/runs/saved-searches/PLAN.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 175.334 seconds and 18 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/artifacts/`.
