# agent-orchestrator: claude activation-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-5` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `f9c2a7c444908e3c42830e844e3a504c3dbca24e`, actual bytes SHA-256 `a097ef64bd1371905586cf9a3ffe9c093f377046497666f8e5ca76da6f3e5aac`; dirty: `False`.
- **Fixture.** `activation-5`, SHA-256 `97ba29da461bec25587f8a9202645d86da5dbf2e50b638a80c1706b801f738ce`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Pick up the agent run from yesterday and finish it.

Task context supplied identically to both arms:
Read run/ first. Ticket 01 accepted; two starts used of eight, remaining six; ticket 02 has pending proof. Do not repeat completed work or reset budget.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 12 | 0 |
| baseline | false | false | 13 | 0 |

Treatment: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T10_17_51_022Z-debug-0.log, app.py, run/DECISIONS.md, run/LOG.md, run/PLAN.md, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_cli.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_cli.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 87.282 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `.cache/npm/_logs/2026-11-09T10_19_18_546Z-debug-0.log, app.py, run/DECISIONS.md, run/LOG.md, run/PLAN.md, run/raw/baseline-proofs-app-29932473.txt, run/raw/final-tests.txt, run/raw/integrated-proofs-app-9875fd81.txt, run/raw/red-tests-app-29932473.txt, scratch/export.json, scratch/state/notes.json, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc, tests/test_app.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 97.04 seconds and 13 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the run record read first, completed work not repeated, and the next unmet task resumed.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-5-adapter-retry-claude/baseline/artifacts/`.
