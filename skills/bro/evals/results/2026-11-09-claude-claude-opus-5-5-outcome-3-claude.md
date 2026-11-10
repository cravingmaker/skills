# bro: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `20aa7feebf75db7c9ad6765c371f6cb456f1fc87`, actual bytes SHA-256 `b88e494bfaa31f0babf7014a866715fac33e9d9ac5ed83ad1e569027df4bc663`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `b4a7e81156efb335f6897c42d7a367286264a2b79d5904b1c7f467d2a09b64a8`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [bro.tar.gz](https://drive.google.com/file/d/1C3LuMQDCXBnZnI7Hxe2hM_ar7Amiadb-/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/` inside.

## Prompt

```text
/bro Bro, restate a claim that passed only static review.

Supplied task context:
Previous assistant answer, supplied as context: Static inspection found the missing authorization check at src/order.py:7. No runtime probe ran. The clear-communication parent skill is absent from this installed inventory.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 1 | 0 |
| baseline | n/a | false | 0 | 0 |

Treatment: 7 response lines; changed files `.cache/npm/_logs/2026-11-09T05_05_11_393Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 8.105 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 7 response lines; changed files `.cache/npm/_logs/2026-11-09T05_05_51_816Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 6.208 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: "Bro, restate a claim that passed only static review." Check: facts and proof limits stay exact; a parent missing from the installed inventory is reported rather than improvised.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **added**. Baseline criterion: partial; treatment criterion: yes.

Treatment checks the missing clear-communication parent, stops the repair rather than improvising it, and preserves the exact static finding/source location and unrun-runtime limit. Baseline discloses absence but still performs a substitute restatement.
