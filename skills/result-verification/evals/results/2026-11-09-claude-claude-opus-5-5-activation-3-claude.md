# result-verification: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `0069ed4e943922369e1c9b207e421b315a375088`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `0476d6d105a509729af837a5c9e81acec012b1a3a16a524ebbd082e86f0b95f1`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
One research agent never returned. Finish the synthesis.

Task context supplied identically to both arms:
Returned fixture reports and briefs are in inbox/ and briefs/. No live Git metadata or commits are available; ownership cannot be fully checked, report that limit. Execute actual named checks rather than trusting reports. Missing research report remains required and unresolved.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 15 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T03_51_36_219Z-debug-0.log, scratch/receipts/hashes.txt, scratch/receipts/ownership.txt, scratch/receipts/raw-copies.txt, scratch/receipts/validate.txt, scratch/run/DECISIONS.md, scratch/run/LOG.md, scratch/run/PLAN.md, scratch/run/briefs/backend.md, scratch/run/briefs/frontend.md, scratch/run/briefs/qa.md, scratch/run/drafts/synthesis-r1.md, scratch/run/raw/a.md, scratch/run/raw/backend.md, scratch/run/raw/dispatches.json, scratch/run/raw/frontend.md, scratch/run/raw/qa.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 133.97 seconds and 15 tool calls; token usage is in the JSON record.

Baseline: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T03_54_37_755Z-debug-0.log, scratch/decisions.md, scratch/hashes.txt, scratch/synthesis.md, scratch/validate.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 50.749 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the missing slice is recorded as unresolved with its reason; the synthesis says what is missing and does not present itself as complete.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/artifacts/`.
