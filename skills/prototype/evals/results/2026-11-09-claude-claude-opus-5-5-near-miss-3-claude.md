# prototype: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `1b6e410e5d7bba2adc9d9a5c88e7d2b0980deae2`, actual bytes SHA-256 `2fb4cdaf107ded26057a1f1591cdc997edf9980bec726ff7af7a1aa5099e9bf9`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `b4a7e81156efb335f6897c42d7a367286264a2b79d5904b1c7f467d2a09b64a8`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [prototype.tar.gz](https://drive.google.com/file/d/1Rv_qtYdd-oR2lwSJsU6BlCDP6YUTIkRc/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/` inside.

## Prompt

```text
What is a prototype?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 0 | 0 |
| baseline | false | false | 0 | 0 |

Treatment: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T04_53_01_271Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 10.468 seconds and 0 tool calls; token usage is in the JSON record.

Baseline: 35 response lines; changed files `.cache/npm/_logs/2026-11-09T04_53_12_435Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 11.546 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a short explanation without creating an artifact.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/artifacts/`.
