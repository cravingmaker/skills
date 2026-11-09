# how: claude near-miss-2

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `e24e666e7410c8edd7a869b3e85b55594cedb1ff`, actual bytes SHA-256 `99e0d7ad26faba68d1a78fdaa6b116f5026b1ac45c26422f5ad179a6be109646`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `094318e818389a17786801c3044856f54eb64c830917b39e66a00aed535aff49`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Implement the approved upload change.

Task context supplied to both arms:
Approved upload change: reject empty filename in src/handler.py with ValueError. Edit only that file.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 6 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T04_55_43_436Z-debug-0.log, src/handler.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 29.687 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T04_56_13_158Z-debug-0.log, src/__pycache__/handler.cpython-315.pyc, src/handler.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 20.176 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: authorized implementation, without an unsolicited onboarding report.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/artifacts/`.

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
