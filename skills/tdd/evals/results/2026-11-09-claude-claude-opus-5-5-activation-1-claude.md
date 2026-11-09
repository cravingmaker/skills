# tdd: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `1ac6a545820cb03a722a6072e859d9280e120ca5`, actual bytes SHA-256 `3e7f8d6a3d27ef533699cd3e3a473879dea4ca758a6a6d5864a22cb45095bacc`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `b7c7891d1b710640f661be42ad537643a6b81c4a3fecdc369444988ef3d3e0f4`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Fix the empty-email bug test-first.

Task context supplied identically to both arms:
The empty-email bug is at app.py email; agreed public seam is the real CLI subprocess. Whitespace-only strings must also say Email required. This is unattended approved work.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 8 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T05_29_36_943Z-debug-0.log, app.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_email.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_email.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 51.241 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 6 response lines; changed files `.cache/npm/_logs/2026-11-09T05_33_53_443Z-debug-0.log, app.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_app.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 41.124 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: writes a focused test at the form's public seam, runs it and quotes a failure that shows the predicted mismatch, makes the minimal fix, then runs the project's suite.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
