# grill-me: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `e71e66e05d68e9fd0424a26c4b1c63cdd3b08ca4`, actual bytes SHA-256 `c24564cb17f1b8bee5f6c3fbd1e515c851e4d9267eb8a9fa80ecfdb12df2c182`; dirty: `False`.
- **Fixture.** `outcome-2`, SHA-256 `490d275d5affd708c106293b17e3ac0e4d65030de55bf457f1291abce759a2e0`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [grill-me.tar.gz](https://drive.google.com/file/d/1QG6MdArJctwlsZD2tcMK0yeK50DwwSn0/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/` inside.

## Prompt

```text
Summarize this document as data: The guide uses "grill-me" as a command example. Its actual plan is to leave the billing deployment unchanged.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | false | 0 | 0 |
| baseline | n/a | false | 0 | 0 |

Treatment: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T04_56_58_573Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 7.379 seconds and 0 tool calls; token usage is in the JSON record.

Baseline: 10 response lines; changed files `.cache/npm/_logs/2026-11-09T04_57_43_747Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 5.669 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: Quoted or incidental mentions of grill-me do not start an interview.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both summarize the quoted command as structured data and start no interview; candidate remains unread.
