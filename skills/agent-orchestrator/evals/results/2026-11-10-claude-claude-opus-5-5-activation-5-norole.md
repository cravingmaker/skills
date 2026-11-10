# agent-orchestrator: claude activation-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-5` in `evals/examples.md`.
- **Skill revision.** Commit `775737f530620cee9710c42e6dc69e960f58b101`, tree `336f4df6607f88de29e3062e1d9b18239ec29ce6`, actual bytes SHA-256 `00e5ac2fd75175858c8aba7278d9b9c858aab87ef7edc46c63f95d742259e586`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/resume`, SHA-256 `5deb91a0e51776433edd47ce0f62bcf1809a9f6b002fee1b0fb758527dc60092`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-orchestrator.tar.gz](https://drive.google.com/file/d/1TnL4LV36IBdB0QS37EPg7G9Q9ZBKafvB/view), folder `2026-11-10-claude-claude-opus-5-5-activation-5-norole/` inside.

## Prompt

```text
Pick up the agent run from yesterday and finish it.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 7 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 14 response lines; changed files `run/DECISIONS.md, run/LOG.md, run/PLAN.json, run/drafts/frontend-client.v1.py, run/drafts/frontend-client.v1.validate.txt`; removed files `none`; validation command present: `requires review`. Workflow cost: 49.503 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 13 response lines; changed files `run/DECISIONS.md, run/LOG.md, run/PLAN.json, run/evidence/validate-2026-11-10.out`; removed files `none`; validation command present: `requires review`. Workflow cost: 50.491 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the run record read first, completed work not repeated, and the next unmet task resumed.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-5-norole/baseline/artifacts/`.
