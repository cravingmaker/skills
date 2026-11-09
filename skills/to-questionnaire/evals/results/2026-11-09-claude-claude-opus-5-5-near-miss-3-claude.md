# to-questionnaire: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `60736f06b92f0a37372e5ab047ccb75a0ae85c03`, actual bytes SHA-256 `9777b373857bd5166887896f0eaa90ef0ddd21e6da2918744ace78528b18cdf4`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Write a customer satisfaction survey for our users.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | true | 5 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T04_51_16_679Z-debug-0.log, customer-satisfaction-survey.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 37.916 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T04_51_53_960Z-debug-0.log, customer-satisfaction-survey.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 32.804 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a survey for many respondents, not a one-recipient discovery questionnaire.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/artifacts/`.

## Activation observation correction

A manual review of the successful Bash pipeline verifies that its installed-candidate input and visible body match the recorded file hash. Activation is corrected to true. This ordinary survey prompt did not invoke a native skill command; the output remains a survey for many respondents. The body load is a single unconfirmed observation, and a repeat pair does not fit the campaign budget. The catalog remains evaluated under the valid-pair coverage policy; this unconfirmed body load remains a manual-suppression follow-up. Original JSON and Markdown remain in the ignored raw backup.
