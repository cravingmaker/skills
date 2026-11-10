# wayfinder: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `4fbc19104eb3977020c3b7730ec008e2fed3b747`, actual bytes SHA-256 `9aa5238f82f9edd5f4c8580e0b7b34e7d8e4c38d8d89fc51c271b3be96a9aea7`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `73fec0d7fb4088ef7969634837226a6f96eb91bfa95ee190c49feff5508cbcfd`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [wayfinder.tar.gz](https://drive.google.com/file/d/1JwLCmS9xRZYC3csBrCeIgzvtDKp-oyrQ/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/` inside.

## Prompt

```text
Break the approved migration spec into tickets.

Task context supplied to both arms:
The approved spec is docs/specs/saved-searches.md. Present build tickets for review.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 3 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 57 response lines; changed files `.cache/npm/_logs/2026-11-09T04_06_43_182Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 39.818 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 66 response lines; changed files `.cache/npm/_logs/2026-11-09T04_07_23_077Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.328 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the `to-tickets` skill, with build tickets, not decision tickets.

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
