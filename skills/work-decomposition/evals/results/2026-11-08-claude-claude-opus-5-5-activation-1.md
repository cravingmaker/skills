# work-decomposition: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `66f8700b5f86ced76eeb64d9f42201df5ea9f2be`, tree `6002c3edb4a8cbb3dd935a915d342c9f929e7d2d`, actual bytes SHA-256 `1a9113a9514d820a377848388890239c098fa6eb3f0fe74714707faeb30f46ee`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/multitask`, SHA-256 `9f2478f72c4e5fa5d08c40b48adcc3f41bb274a5015366ba0ab65535dcb8de0a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.

## Prompt

```text
Decide whether agents would help this migration, then give the useful workers ownership and a budget.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 12 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 18 response lines; changed files `backend/service.py, frontend/client.py, reports/status-migration-01/DECISIONS.md, reports/status-migration-01/LOG.md, reports/status-migration-01/PLAN.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 73.291 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 16 response lines; changed files `backend/service.py, frontend/client.py, reports/migration-agent-decision.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 30.662 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a reasoned direct/delegated choice and a checked graph before dispatch.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-08-claude-claude-opus-5-5-activation-1/comparison.json](2026-11-08-claude-claude-opus-5-5-activation-1/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-1/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-1/baseline/artifacts/`.
