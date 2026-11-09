# diagnosing-bugs: claude near-miss-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-4` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `31d3414b1f15fe96c732cdc57d20dea93934de11`, actual bytes SHA-256 `b4acc5f6036f5cf30f051f33e21420535b1fe5e3f0a7e0c297c518257c37eaa9`; dirty: `False`.
- **Fixture.** `near-miss-4`, SHA-256 `c6751b05b004ac3bd241404bb66b71014a204b31ec7908f62bed438e8da19dca`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
This test fails only when run after another test.

Task context supplied identically to both arms:
Only tests/test_order.py exhibits order pollution; no specialized flaky-test skill is installed.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | true | 6 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T05_41_50_221Z-debug-0.log, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_order.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_order.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 35.956 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 10 response lines; changed files `.cache/npm/_logs/2026-11-09T05_43_25_882Z-debug-0.log, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_order.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_order.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 53.752 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: test-order pollution is specialist flaky-test work; this skill does not reproduce the polluter-bisection recipe.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/artifacts/`.
