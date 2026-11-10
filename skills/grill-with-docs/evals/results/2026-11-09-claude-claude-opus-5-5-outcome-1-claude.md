# grill-with-docs: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `2282cb8988dbf2947e939c86d5e11a066ee2904a`, actual bytes SHA-256 `c9f78a46b3908ccbbb599b0c20187c2bae0c54c4ead56798ab03e97187dc1fde`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `0ef5b6872fa169dc4847f5c3ca4907883ce146a6acd310b4bb61723052277c54`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [grill-with-docs.tar.gz](https://drive.google.com/file/d/1S2CJ-9Em0BuaZOeC-XDrpv2zjIwfbRZ7/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/` inside.

## Prompt

```text
/grill-with-docs

Use the `grill-with-docs` skill explicitly for this request.

grill-with-docs: I want to add partial order cancellation.

Task context supplied to both arms:
Settled definition: Partial cancellation means cancelling selected uncaptured line-item quantities, never reversing captured amounts. Keep Order as the whole customer commitment. Open product choice: allow cancellation after shipment?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 12 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 48 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 79.062 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 49 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 46.83 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: No question asks for a fact the repo, the docs, or the conversation already answers, and no settled decision is reopened.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both read the configured domain sources, preserve partial-cancellation meaning and accepted Billing callbacks, and ask about genuinely open shipment/status choices.
