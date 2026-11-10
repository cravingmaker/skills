# council: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `645edc1b3f8b5c5c00854bc61d0d6fc29130ffbc`, actual bytes SHA-256 `b24055566d7c79f421cbb22a5ec0337e4290b06d7d90fb76b6c3191c0957771d`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `c6a4f6092a051f8dcda2bda3debfd28763fe8dc66a92e944630fb3195124812f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [council.tar.gz](https://drive.google.com/file/d/16Fwd_YCT92OpsAO0jn1JZOimKVhnrawP/view), folder `2026-11-09-claude-claude-opus-5-5-activation-1-claude/` inside.

## Prompt

```text
/council

Council: review this code and fix verified issues using the distinct providers I named.

Task context supplied identically to both arms:
This is a continuation of the same council run, not a new allowance. Read and reuse authoritative review/existing-run/PLAN.md, LOG.md and DECISIONS.md plus bench-report.md. Shared cap 3 rounds with 2 used, cap 6 starts with 4 used; concurrency ceiling 2. Sol and Claude are still unavailable and no actual additional model starts are authorized. Repair only dist/index.mjs, recheck the actual package consumers, preserve IDs and unresolved native/provider evidence. No product edits outside that slice, commits, posting, push or merge. Snapshots are exported bytes, not Git history.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 16 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T05_54_31_749Z-debug-0.log, dist/index.mjs, review/existing-run/DECISIONS.md, review/existing-run/LOG.md, review/existing-run/PLAN.md, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 124.673 seconds and 16 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T05_56_39_795Z-debug-0.log, dist/index.mjs, review/existing-run/DECISIONS.md, review/existing-run/LOG.md, review/existing-run/PLAN.md, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 72.898 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the sol-loop skill in council panel mode, with the same provider request and finite budget.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
