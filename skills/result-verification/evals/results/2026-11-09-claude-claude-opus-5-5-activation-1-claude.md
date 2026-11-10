# result-verification: claude activation-1

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `0069ed4e943922369e1c9b207e421b315a375088`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `af67bdf0ce3edc9407efa84494da726c46ec8a76c21f8b9bc2acf1b214d13d12`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [result-verification.tar.gz](https://drive.google.com/file/d/1rG3ldD66TlC28hZZt7xINNlgtOv3GBsY/view), folder `2026-11-09-claude-claude-opus-5-5-activation-1-claude/` inside.

## Prompt

```text
The three sub-agents are done. Merge their work and tell me whether it is ready.

Task context supplied identically to both arms:
Returned fixture reports and briefs are in inbox/ and briefs/. No live Git metadata or commits are available; ownership cannot be fully checked, report that limit. Execute actual named checks rather than trusting reports.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 14 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T03_51_18_854Z-debug-0.log, scratch/receipts/hashes.txt, scratch/receipts/inbox-mtimes.txt, scratch/receipts/intake-time.txt, scratch/receipts/ownership-backend.txt, scratch/receipts/ownership-frontend.txt, scratch/receipts/ownership-qa.txt, scratch/receipts/proof-labels.txt, scratch/receipts/reports-ls.txt, scratch/receipts/validate.txt, scratch/run/DECISIONS.md, scratch/run/LOG.md, scratch/run/PLAN.md, scratch/run/briefs/backend.md, scratch/run/briefs/frontend.md, scratch/run/briefs/qa.md, scratch/run/raw/backend.md, scratch/run/raw/frontend.md, scratch/run/raw/qa.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 134.773 seconds and 14 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T03_54_04_867Z-debug-0.log, scratch/hashes-before.txt, scratch/merge-decision.md, scratch/raw-reports/briefs/backend.md, scratch/raw-reports/briefs/frontend.md, scratch/raw-reports/briefs/qa.md, scratch/raw-reports/report-backend.md, scratch/raw-reports/report-frontend.md, scratch/raw-reports/report-qa.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 49.132 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: each raw report saved before judging; each checked against its brief; `scripts/check-ownership.sh` run for each writer; at least one cited command rerun per child; the project's validator run on the integrated revision; "ready" only if every acceptance check passes there.

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

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
