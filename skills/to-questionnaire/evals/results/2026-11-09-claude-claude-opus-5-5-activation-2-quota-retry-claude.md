# to-questionnaire: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `60736f06b92f0a37372e5ab047ccb75a0ae85c03`, actual bytes SHA-256 `9777b373857bd5166887896f0eaa90ef0ddd21e6da2918744ace78528b18cdf4`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [to-questionnaire.tar.gz](https://drive.google.com/file/d/1rPGKscV6MIt5Gkv8TQRpHS1DoWAnUmuk/view), folder `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/` inside.

## Prompt

```text
/to-questionnaire

Use the `to-questionnaire` skill explicitly for this request.

Make a questionnaire for our infra contractor about the migration.

Task context supplied to both arms:
Recipient: our infra contractor. Purpose: determine the safe migration plan. The specific facts we need back have not been supplied.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 2 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T10_21_01_277Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 19.204 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 51 response lines; changed files `.cache/npm/_logs/2026-11-09T10_21_20_595Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 30.971 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: one message asking only what the user needs back; then the draft.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-quota-retry-claude/baseline/artifacts/`.
