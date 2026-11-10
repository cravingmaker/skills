# agent-orchestrator: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `66f8700b5f86ced76eeb64d9f42201df5ea9f2be`, tree `faaa8ba405c30dfde02825ff9252ba1ae0502737`, actual bytes SHA-256 `493634536f354182ae89b53b5abf929de6658f5428087aad7149db43c22ee675`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/multitask`, SHA-256 `9f2478f72c4e5fa5d08c40b48adcc3f41bb274a5015366ba0ab65535dcb8de0a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-orchestrator.tar.gz](https://drive.google.com/file/d/1TnL4LV36IBdB0QS37EPg7G9Q9ZBKafvB/view), folder `2026-11-08-claude-claude-opus-5-5-activation-2/` inside.

## Prompt

```text
Manage backend, frontend, and QA agents to build this feature.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 9 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 17 response lines; changed files `backend/service.py, frontend/client.py, reports/backend.md, reports/frontend.md, reports/plan.md, reports/qa.md, tests/test_contract.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 55.8 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `backend/service.py, frontend/client.py, reports/backend.md, reports/coordinator.md, reports/frontend.md, reports/qa.md, tests/test_contract.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 45.503 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: tasks with dependencies, one integration owner, disjoint write boundaries, briefs a fresh agent can execute, and acceptance checks run on the integrated result.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-activation-2/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/artifacts/`.
