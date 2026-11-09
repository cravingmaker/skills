# prototype: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `1b6e410e5d7bba2adc9d9a5c88e7d2b0980deae2`, actual bytes SHA-256 `2fb4cdaf107ded26057a1f1591cdc997edf9980bec726ff7af7a1aa5099e9bf9`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `b4a7e81156efb335f6897c42d7a367286264a2b79d5904b1c7f467d2a09b64a8`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
I want to compare two API shapes from the importing developer's perspective before choosing.

Task context supplied to both arms:
Compare flat upload(file, retries=3) with client.upload(file, policy={max_attempts:4}) for an importing developer. Exercise a successful upload, retried 503, permanent 400 and cancellation. Offline stubs only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 9 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T04_52_50_062Z-debug-0.log, prototypes/upload-api-shape/compare.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 70.627 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T04_54_00_652Z-debug-0.log, prototypes/upload_shapes/__pycache__/_core.cpython-315.pyc, prototypes/upload_shapes/__pycache__/client.cpython-315.pyc, prototypes/upload_shapes/__pycache__/consumer_client.cpython-315.pyc, prototypes/upload_shapes/__pycache__/consumer_flat.cpython-315.pyc, prototypes/upload_shapes/__pycache__/flat.cpython-315.pyc, prototypes/upload_shapes/__pycache__/stubs.cpython-315.pyc, prototypes/upload_shapes/_core.py, prototypes/upload_shapes/client.py, prototypes/upload_shapes/consumer_client.py, prototypes/upload_shapes/consumer_flat.py, prototypes/upload_shapes/flat.py, prototypes/upload_shapes/run.py, prototypes/upload_shapes/stubs.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 77.046 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a small consumer-oriented experiment compares the requested alternatives and records a supported conclusion.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/artifacts/`.
