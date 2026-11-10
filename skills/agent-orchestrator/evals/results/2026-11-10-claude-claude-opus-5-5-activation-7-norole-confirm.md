# agent-orchestrator: claude activation-7

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-7` in `evals/examples.md`.
- **Skill revision.** Commit `775737f530620cee9710c42e6dc69e960f58b101`, tree `336f4df6607f88de29e3062e1d9b18239ec29ce6`, actual bytes SHA-256 `00e5ac2fd75175858c8aba7278d9b9c858aab87ef7edc46c63f95d742259e586`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/routine`, SHA-256 `235b5423636a31cbd44df8be888962f13d2fd93b86385308c67b908430e4e52d`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-orchestrator.tar.gz](https://drive.google.com/file/d/1TnL4LV36IBdB0QS37EPg7G9Q9ZBKafvB/view), folder `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/` inside.

## Prompt

```text
Act as the orchestrator: run this approved code-ticket graph at configured nondefault paths.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 5 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 14 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.555 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 19 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 35.846 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: read the `implement-spec` skill under the current coordinator, record and remaining budget. If dispatch is unavailable, prove only source-bound preflight and report worker execution and integration acceptance as blocked.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-7-norole-confirm/baseline/artifacts/`.
