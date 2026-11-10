# result-verification: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `66f8700b5f86ced76eeb64d9f42201df5ea9f2be`, tree `bc3a90ce1649c8f9de8cc2c74ba6c8c939358cbe`, actual bytes SHA-256 `33d509a4aca15a6345bab0c6d83922342cece62504ef0c01052f0ef01607ab15`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/verification`, SHA-256 `306ecac54fc53b9d2b9a6c4fc76b7eda499707ef8c2fae9f951c4b97094d9382`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [result-verification.tar.gz](https://drive.google.com/file/d/1rG3ldD66TlC28hZZt7xINNlgtOv3GBsY/view), folder `2026-11-08-claude-claude-opus-5-5-activation-2/` inside.

## Prompt

```text
The worker says all tests pass. Can I merge?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 27 response lines; changed files `run/decisions.md, run/raw/MANIFEST.txt, run/raw/backend.md, run/raw/frontend.md, run/raw/qa.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 38.35 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 26 response lines; changed files `review/raw/SHA256SUMS, review/raw/backend.md, review/raw/frontend.md, review/raw/qa.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 24.243 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the agent runs the tests itself on the integrated revision and reports the command and its output; the worker's statement is not the evidence.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-activation-2/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/artifacts/`.
