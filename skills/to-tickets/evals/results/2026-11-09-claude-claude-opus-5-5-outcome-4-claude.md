# to-tickets: claude outcome-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-4` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `53fcbe1f3ae919ea22005551d33abacb7444ae55`, actual bytes SHA-256 `c2c9142422c2683ce739a32d14977452722ef88981b15a86793613fcc5911dab`; dirty: `False`.
- **Fixture.** `outcome-4`, SHA-256 `e78360dd94459172836461a45a01d53ad27717be0ab41db816b6a123774ac7a2`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [to-tickets.tar.gz](https://drive.google.com/file/d/1Yma5TJENr43nnGVl4saovTa9TOBF-C1O/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/` inside.

## Prompt

```text
/to-tickets

Use the `to-tickets` skill explicitly for this request.

to-tickets docs/specs/saved-searches.md

Task context supplied to both arms:
Prior settled discussion: Save, list, and rerun named searches for the signed-in shopper; reject blank names; newest first. Use local per-user JSON; no sharing/cloud sync. CLI surface is agreed. No implementation is authorized.

Supplied task context:
No tracker setup exists here. Return ticket drafts in the response; no guessed file destination is authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 3 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 60 response lines; changed files `.cache/npm/_logs/2026-11-09T03_33_47_754Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 56.508 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 77 response lines; changed files `.cache/npm/_logs/2026-11-09T03_34_51_732Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 56.458 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Filing happens only at the destination the tracker setup names; without setup, the tickets come back as drafts.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

With tracker setup removed, both return drafts and leave all tracker/spec/product documents unchanged. Treatment labels illustrative ticket drafts ready-for-agent while also noting unresolved prerequisites; no ready ticket is actually filed.
