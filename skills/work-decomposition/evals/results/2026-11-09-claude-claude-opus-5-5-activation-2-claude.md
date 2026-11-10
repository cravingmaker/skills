# work-decomposition: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `7a576f6c0cbf17fcc0a2a47e0dec8e13d2e36291`, actual bytes SHA-256 `a83da8598f67faed667175b6c6782ffa69bb79ece6034a6591a00d2b2a60caaf`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `e5b6fd079d07d2029e41ba74561b8a67231f4b37c168b0d40950a00cab80f3f8`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [work-decomposition.tar.gz](https://drive.google.com/file/d/1Qgx8gOA_xs_qEmchFWh7wpjg1bDz1mv5/view), folder `2026-11-09-claude-claude-opus-5-5-activation-2-claude/` inside.

## Prompt

```text
Split two consumers of this fixed API contract across agents and reserve room to integrate them.

Task context supplied to both arms:
Planning only. Fixed API contract contracts/status.json; source inputs backend/service.py and frontend/client.py. Finite shared start allowance 4, concurrency 2, reserve 1 integration/verification. No model or dispatch route is available.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 13 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T03_43_28_765Z-debug-0.log, runs/status-consumers-01/BUDGET.md, runs/status-consumers-01/DECISIONS.md, runs/status-consumers-01/LOG.md, runs/status-consumers-01/PLAN.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 122.771 seconds and 13 tool calls; token usage is in the JSON record.

Baseline: 40 response lines; changed files `.cache/npm/_logs/2026-11-09T03_45_32_550Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 30.126 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: disjoint writes, an explicit integration owner, dependencies, and a finite allowance.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.
