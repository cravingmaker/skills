# council: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `645edc1b3f8b5c5c00854bc61d0d6fc29130ffbc`, actual bytes SHA-256 `b24055566d7c79f421cbb22a5ec0337e4290b06d7d90fb76b6c3191c0957771d`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `749f11848f70e4f8e72ff39a89415ec0508ac07cf14146b8af6a58564efd564e`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [council.tar.gz](https://drive.google.com/file/d/16Fwd_YCT92OpsAO0jn1JZOimKVhnrawP/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/` inside.

## Prompt

```text
Write a PR body describing the council results already supplied.

Task context supplied identically to both arms:
Draft PR body from supplied-results.md in conversation only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 2 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T05_57_02_564Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 26.951 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T05_57_23_275Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 28.592 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: body drafting only; no new reviews, code edits, push or PR mutation.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/artifacts/`.
