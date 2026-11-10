# clear-communication: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `3c1d6e767164d88cf2ea77ef9eb49d73e360bb7c`, actual bytes SHA-256 `50e5d3e75b98078be5aef095c579602f97be163c257098372291d64bb340a4d1`; dirty: `True`.
- **Fixture.** `near-miss-3`, SHA-256 `9b185f81d0ccc703e4d9ebbdf947a01fb85e20e43a3981f8cfbf3ae1f73e2da3`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [clear-communication.tar.gz](https://drive.google.com/file/d/1aeIJGrgJVddiMx2OHdnS48QfZC4ZRETW/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/` inside.

## Prompt

```text
Quote the log line containing bro and wait-what.

Task context supplied to both arms:
Use events.log exactly.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 1 | 0 |
| baseline | false | false | 1 | 0 |

Treatment: 5 response lines; changed files `.cache/npm/_logs/2026-11-09T03_59_04_088Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 6.245 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 5 response lines; changed files `.cache/npm/_logs/2026-11-09T03_59_29_439Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 8.488 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: exact source text, without selecting either manual entry.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-description-fix-claude/baseline/artifacts/`.
