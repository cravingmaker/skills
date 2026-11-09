# implement: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `4d2edd1ceee34651e3fc4a1c31b85fb17decad30`, actual bytes SHA-256 `90a506e5718f8627b0602045b117b5276a408a4b7db65757d8c71e01338765aa`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `9d287a275c7afc7da4dd468776b828942620e00a97e3cd0660bd4b360928676a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/implement

Implement ticket #42 from the tracker.

Task context supplied identically to both arms:
The configured local ticket #42 is tracker/42.md. Approved CLI seam; implement only this ticket.

Supplied task context:
Implement only ticket #42. Preserve unrelated owner work in notes/owner-draft.txt and existing trust-boundary checks.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 8 | 0 |
| baseline | n/a | false | 8 | 0 |

Treatment: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T03_35_51_426Z-debug-0.log, app.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_app.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.048 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T03_36_34_510Z-debug-0.log, app.py, run/DECISIONS.md, run/LOG.md, run/PLAN.md, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_app.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.538 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: The diff contains only the slice: cleanup is limited to lines the agent introduced, and defensive checks at real trust boundaries and others' work are kept.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **added**. Baseline criterion: yes; treatment criterion: yes.

Both preserve the owner draft and trust-boundary validator byte-for-byte. Treatment keeps edits to app.py and its CLI tests; baseline additionally creates three run-record documents. The gain is narrower workflow/write cost, not a claim that baseline damaged product behavior.
