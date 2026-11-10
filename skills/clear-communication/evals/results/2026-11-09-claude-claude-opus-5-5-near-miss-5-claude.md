# clear-communication: claude near-miss-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-5` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `3c1d6e767164d88cf2ea77ef9eb49d73e360bb7c`, actual bytes SHA-256 `0c1fe416999946256a92676611e65579c74ee68e42fb95e2a4dbf38a2ebfa4b2`; dirty: `False`.
- **Fixture.** `near-miss-5`, SHA-256 `9b185f81d0ccc703e4d9ebbdf947a01fb85e20e43a3981f8cfbf3ae1f73e2da3`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [clear-communication.tar.gz](https://drive.google.com/file/d/1aeIJGrgJVddiMx2OHdnS48QfZC4ZRETW/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/` inside.

## Prompt

```text
Draft this PR body only.

Task context supplied to both arms:
PR draft facts: src/parser.ts changed bro to brother; two unit tests passed, no UI or CI. Return text only; no external action.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | true | 1 | 0 |
| baseline | false | false | 0 | 0 |

Treatment: 14 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 18.749 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 19 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 14.147 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a local draft, with no filing, push, watch, or merge inferred from the writing request.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/artifacts/`.
