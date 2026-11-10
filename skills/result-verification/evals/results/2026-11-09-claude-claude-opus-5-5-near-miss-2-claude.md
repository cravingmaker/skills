# result-verification: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `0069ed4e943922369e1c9b207e421b315a375088`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `2af81a50c9657061dc408762fd280185b9e176eccc48cc91e0f8092c3e6d68ed`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [result-verification.tar.gz](https://drive.google.com/file/d/1rG3ldD66TlC28hZZt7xINNlgtOv3GBsY/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/` inside.

## Prompt

```text
Review my pull request for bugs.

Task context supplied identically to both arms:
Review local exported package snapshot; no delegated result is being accepted, no product edits.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 9 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 26 response lines; changed files `.cache/npm/_logs/2026-11-09T03_54_50_441Z-debug-0.log, scratch/tmp/hashes.txt, scratch/tmp/probe-results.txt, scratch/tmp/probe/base/consumer/cli.mjs, scratch/tmp/probe/base/consumer/main.mjs, scratch/tmp/probe/base/dist/index.d.ts, scratch/tmp/probe/base/dist/index.mjs, scratch/tmp/probe/base/package.json, scratch/tmp/probe/head/consumer/cli.mjs, scratch/tmp/probe/head/consumer/main.mjs, scratch/tmp/probe/head/dist/index.d.ts, scratch/tmp/probe/head/dist/index.mjs, scratch/tmp/probe/head/package.json, scratch/tmp/validate.txt`; removed files `none`; validation command present: `requires review`. Workflow cost: 62.244 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T03_56_03_222Z-debug-0.log, scratch/tmp/probe/base/consumer/cli.mjs, scratch/tmp/probe/base/consumer/main.mjs, scratch/tmp/probe/base/node_modules/core6-export-fixture/dist/index.mjs, scratch/tmp/probe/base/node_modules/core6-export-fixture/package.json, scratch/tmp/probe/base/out.txt, scratch/tmp/probe/base/package.json, scratch/tmp/probe/consumers.log, scratch/tmp/probe/edge.log, scratch/tmp/probe/hashes.log, scratch/tmp/probe/head/consumer/cli.mjs, scratch/tmp/probe/head/consumer/main.mjs, scratch/tmp/probe/head/node_modules/core6-export-fixture/dist/index.d.ts, scratch/tmp/probe/head/node_modules/core6-export-fixture/dist/index.mjs, scratch/tmp/probe/head/node_modules/core6-export-fixture/package.json, scratch/tmp/probe/head/out.txt, scratch/tmp/probe/head/package.json, scratch/tmp/probe/number.log, scratch/tmp/validate.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 69.011 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a code review; no delegated results to verify.

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
