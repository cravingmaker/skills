# to-questionnaire: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `d182f33df014c363bacf919ab5f006da84708540`, tree `489394fc4fe9d8db9da5076f497dfcad6915e8d1`, actual bytes SHA-256 `9777b373857bd5166887896f0eaa90ef0ddd21e6da2918744ace78528b18cdf4`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [to-questionnaire.tar.gz](https://drive.google.com/file/d/1rPGKscV6MIt5Gkv8TQRpHS1DoWAnUmuk/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/` inside.

## Prompt

```text
Write a customer satisfaction survey for our users.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 4 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T11_27_43_521Z-debug-0.log, customer-satisfaction-survey.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.524 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 12 response lines; changed files `.cache/npm/_logs/2026-11-09T11_30_49_754Z-debug-0.log, customer-satisfaction-survey.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 40.433 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a survey for many respondents, not a one-recipient discovery questionnaire.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude/baseline/artifacts/`.

## Filesystem-read confirmation

Manual review of every treatment tool call finds no candidate-body read or native Skill call. The treatment writes a survey for many respondents. This repeat skips the candidate, so the earlier one-off filesystem body load remains unconfirmed as a repeated trigger. No complete filesystem suppression claim follows from this pair.

## Round 2 review

Baseline: yes. Treatment: yes. Value: matched.

Manual review of every treatment tool call finds no Skill call or candidate-body file read/pipeline. Both write a survey for many respondents. The repeat skips the body, so the earlier single filesystem load is not a confirmed repeated trigger.
