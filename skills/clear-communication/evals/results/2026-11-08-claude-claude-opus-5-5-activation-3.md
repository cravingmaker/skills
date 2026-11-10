# clear-communication: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `97a8b69edec8455ea722e2d579a544cfb76a58b9`, tree `43c2f515a6aa21072f1b21412038256bb8bf6346`, actual bytes SHA-256 `73c620f3304358409a4cce2b107386c30c26249f74912d1cbf8a50b1f724040a`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/release`, SHA-256 `0fe8378e0eab00243dd8d4239f46c71db87523513d9440f4884b9718cc0e5d49`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [clear-communication.tar.gz](https://drive.google.com/file/d/1aeIJGrgJVddiMx2OHdnS48QfZC4ZRETW/view), folder `2026-11-08-claude-claude-opus-5-5-activation-3/` inside.

## Prompt

```text
Set up the release pipeline for this repo.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 2 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 11 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 19.496 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 10 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 25.856 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: (The repo has two package managers' lockfiles and no CI.) Expect: one numbered message with the consequential questions answerable now, each with a recommended answer, and no questions about details the files already answer.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-activation-3/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/artifacts/`.
