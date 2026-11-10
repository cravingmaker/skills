# agent-briefing: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `adc18eb7748758f2697df7788c1fe2db89539d6b`, actual bytes SHA-256 `6fe92fecbcc8d65a4b813c64b9259eb8d695ed47370bbfd9baf7a30df2c37c55`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `c42b5cb9b7bd00ab4d201b3a358661031285ae8c4850db8d368863b0433fadd2`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-briefing.tar.gz](https://drive.google.com/file/d/1FqpvKO1UwLeqNh4Svp5DeVQe_VEueOLL/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/` inside.

## Prompt

```text
Implement the small change described in this complete worker brief; do not delegate.

Task context supplied to both arms:
Complete worker brief: fix resutls to results in README.md only. No delegation, report the diff and no other edits.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 5 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 11 response lines; changed files `.cache/npm/_logs/2026-11-09T11_15_05_255Z-debug-0.log, README.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 14.925 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 9 response lines; changed files `.cache/npm/_logs/2026-11-09T11_17_05_953Z-debug-0.log, README.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 11.871 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: direct execution of the assignment without generating another brief.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-round2-pre-claude/baseline/artifacts/`.
