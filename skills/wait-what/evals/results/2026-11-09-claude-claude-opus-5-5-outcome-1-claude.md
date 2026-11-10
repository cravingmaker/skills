# wait-what: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `112be18d25916e38f717a003de18fc07e9397c70`, actual bytes SHA-256 `f5c23c382ff1ae563601e3348904d31fac084a144d8f173032fea823724a437a`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `16e92b82377241283f122410704bcd7ca07063d4c00646e5e14385c83ced60a6`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [wait-what.tar.gz](https://drive.google.com/file/d/1OP3j7mbzEYU8O-Uxj4gG6mLOJYymeLqf/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/` inside.

## Prompt

```text
/wait-what Wait-what, explain the read-only council result.

Supplied task context:
Previous assistant answer, supplied as context: Read-only council found F-001 by static missing-export evidence, F-002 by a failed runtime probe, F-003 timing remains unrun. No fix loop or product edit is authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 1 | 0 |
| baseline | n/a | false | 1 | 0 |

Treatment: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T05_02_30_961Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 14.7 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T05_03_55_924Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 14.034 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: "Wait-what, explain the read-only council result." Check: clearer context only; no automatic fix loop.

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

Both restate the static missing-export, failed-runtime and unrun-timing distinction without product edits or a fix loop. Both unnecessarily rank runtime evidence above static; this shared wording issue is not a treatment-added regression.
