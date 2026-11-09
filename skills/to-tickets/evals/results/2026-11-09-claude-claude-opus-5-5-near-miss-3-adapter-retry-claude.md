# to-tickets: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `53fcbe1f3ae919ea22005551d33abacb7444ae55`, actual bytes SHA-256 `c2c9142422c2683ce739a32d14977452722ef88981b15a86793613fcc5911dab`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `1aaff2b0e4a28127b049de33231732b9e84968bb2e7fb462bed73c674362a037`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Implement ticket 02.

Task context supplied to both arms:
Ticket 02 is .planning/work-items/search/02-list-saved-searches.md. Implement only the list behavior; ticket 01 is complete for this task. No re-ticketing.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 8 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T10_15_38_658Z-debug-0.log, .planning/work-items/search/02-list-saved-searches.md, app.py, src/__pycache__/saved_searches.cpython-315.pyc, src/saved_searches.py, tests/__pycache__/test_list_cli.cpython-315.pyc, tests/test_list_cli.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 63.663 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T10_16_42_174Z-debug-0.log, .planning/work-items/search/02-list-saved-searches.md, app.py, src/__pycache__/saved_searches.cpython-315.pyc, src/saved_searches.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 63.468 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: implementation of that ticket, not a new breakdown.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-adapter-retry-claude/baseline/artifacts/`.
