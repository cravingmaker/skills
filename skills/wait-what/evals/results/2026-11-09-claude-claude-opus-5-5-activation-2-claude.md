# wait-what: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `112be18d25916e38f717a003de18fc07e9397c70`, actual bytes SHA-256 `f5c23c382ff1ae563601e3348904d31fac084a144d8f173032fea823724a437a`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `16e92b82377241283f122410704bcd7ca07063d4c00646e5e14385c83ced60a6`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [wait-what.tar.gz](https://drive.google.com/file/d/1OP3j7mbzEYU8O-Uxj4gG6mLOJYymeLqf/view), folder `2026-11-09-claude-claude-opus-5-5-activation-2-claude/` inside.

## Prompt

```text
/wait-what

Use the `wait-what` skill explicitly for this request.

Wait-what, I lost the connection between the upload and queue.

Task context supplied to both arms:
Previous assistant answer: "Upload → object key → queue; capture is not settlement. An Order is the customer commitment. Settlement transfers captured funds to the merchant; pending capture does not prove settlement. Static inspection only, no live UI or upload. No repairs, commits, PR filing, push, watch, merge, helpers, or course files are authorized."
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 1 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 9 response lines; changed files `.cache/npm/_logs/2026-11-09T04_57_48_780Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 10.303 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T04_58_34_066Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 24.972 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the parent explains that connection in the last answer; no new task or course starts.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.
