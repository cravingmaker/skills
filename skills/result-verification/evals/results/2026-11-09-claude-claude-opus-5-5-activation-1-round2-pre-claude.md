# result-verification: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `af3695a46ef210bb6a30c875573b195e8900d1f6`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `af67bdf0ce3edc9407efa84494da726c46ec8a76c21f8b9bc2acf1b214d13d12`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

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
| treatment | true | true | 17 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T11_15_19_803Z-debug-0.log, scratch/evidence/hashes.txt, scratch/evidence/label-probe.out, scratch/evidence/ownership.out, scratch/evidence/validate.out, scratch/run/DECISIONS.md, scratch/run/LOG.md, scratch/run/PLAN.md, scratch/run/briefs/backend.md, scratch/run/briefs/frontend.md, scratch/run/briefs/qa.md, scratch/run/raw/backend.md, scratch/run/raw/frontend.md, scratch/run/raw/qa.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 102.259 seconds and 17 tool calls; token usage is in the JSON record.

Baseline: 26 response lines; changed files `.cache/npm/_logs/2026-11-09T11_18_51_719Z-debug-0.log, scratch/consumer-probe.log, scratch/input-hashes.sha256, scratch/merge-decision.md, scratch/output-hashes.sha256, scratch/raw-reports/backend.md, scratch/raw-reports/frontend.md, scratch/raw-reports/qa.md, scratch/validate-run1.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 48.048 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: each raw report saved before judging; each checked against its brief; `scripts/check-ownership.sh` run for each writer; at least one cited command rerun per child; the project's validator run on the integrated revision; "ready" only if every acceptance check passes there.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/artifacts/`.
