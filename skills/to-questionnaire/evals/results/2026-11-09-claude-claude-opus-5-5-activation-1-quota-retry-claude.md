# to-questionnaire: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `60736f06b92f0a37372e5ab047ccb75a0ae85c03`, actual bytes SHA-256 `9777b373857bd5166887896f0eaa90ef0ddd21e6da2918744ace78528b18cdf4`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/to-questionnaire

Use the `to-questionnaire` skill explicitly for this request.

to-questionnaire: I need to pick a payment provider but our finance lead, Dana, knows the settlement and refund constraints. I need to know which settlement windows and chargeback rules we must support. It goes to Dana by email next week.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 1 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 11 response lines; changed files `.cache/npm/_logs/2026-11-09T04_50_16_608Z-debug-0.log, to-questionnaire-payment-provider-settlement-chargebacks.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 28.132 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 45 response lines; changed files `.cache/npm/_logs/2026-11-09T04_50_44_639Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 30.786 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: no questions to the user; a draft file whose questions cover settlement windows and chargeback rules, pitched to a finance lead.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-quota-retry-claude/baseline/artifacts/`.
