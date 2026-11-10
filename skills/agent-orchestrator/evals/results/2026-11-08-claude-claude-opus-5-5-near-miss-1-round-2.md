# agent-orchestrator: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `2a837f3af035d5e0285c43d2c92078dbd4219bda`, tree `a2d39c2a9b5f9f7c3ddc1add2295602fee81dfea`, actual bytes SHA-256 `4c2ebd3c394051f8654eda949a66b880eae650d11503dc79b55be53b8ac1f6e6`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/routine`, SHA-256 `235b5423636a31cbd44df8be888962f13d2fd93b86385308c67b908430e4e52d`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-orchestrator.tar.gz](https://drive.google.com/file/d/1TnL4LV36IBdB0QS37EPg7G9Q9ZBKafvB/view), folder `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/` inside.

## Prompt

```text
Fix this typo in the README.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 4 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 3 response lines; changed files `README.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 18.18 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 5 response lines; changed files `README.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 19.188 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the fix, done directly; no plan, briefs, or agents.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-1-round-2/baseline/artifacts/`.
