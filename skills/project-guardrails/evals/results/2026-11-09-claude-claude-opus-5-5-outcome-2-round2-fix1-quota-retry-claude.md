# project-guardrails: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/` inside.

## Prompt

```text
Wire the existing lint command into scripts/validate.sh. Prove the changed guardrail rejects a planted debugger statement, accepts valid source, and repeating the same setup leaves no content delta. Use an owned scratch copy for probes; preserve original source.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 40 | 0 |
| baseline | n/a | false | 12 | 0 |

Treatment: 30 response lines; changed files `.cache/npm/_logs/2026-11-09T14_55_24_424Z-debug-0.log, scratch/orig/eslint.config.mjs, scratch/orig/package.json, scratch/orig/scripts/check.py, scratch/orig/scripts/validate.sh, scratch/orig/src/helper.py, scratch/orig/src/index.ts, scratch/orig/tests/sum.test.mjs, scratch/orig/tests/test_smoke.py, scratch/probe/eslint.config.mjs, scratch/probe/package.json, scratch/probe/scripts/check.py, scratch/probe/scripts/validate.sh, scratch/probe/src/helper.py, scratch/probe/src/index.ts, scratch/probe/tests/__pycache__/test_smoke.cpython-315.pyc, scratch/probe/tests/sum.test.mjs, scratch/probe/tests/test_smoke.py, scratch/setup.sh, scratch/snap.sh, scratch/snap1.txt, scratch/snap2.txt, scripts/validate.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 192.7 seconds and 40 tool calls; token usage is in the JSON record.

Baseline: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T14_58_56_144Z-debug-0.log, scratch/bad.log, scratch/bad/package.json, scratch/bad/scripts/check.py, scratch/bad/scripts/validate.sh, scratch/bad/src/helper.py, scratch/bad/src/index.ts, scratch/bad/src/planted.ts, scratch/bad/tests/sum.test.mjs, scratch/bad/tests/test_smoke.py, scratch/good.log, scratch/good/package.json, scratch/good/scripts/check.py, scratch/good/scripts/validate.sh, scratch/good/src/helper.py, scratch/good/src/index.ts, scratch/good/tests/sum.test.mjs, scratch/good/tests/test_smoke.py, scratch/npm-cache/_logs/2026-11-09T14_59_44_051Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_59_44_513Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_59_44_703Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_59_44_915Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T14_59_51_420Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/orig.sha, scratch/probe.sh, scratch/rep/package.json, scratch/rep/scripts/check.py, scratch/rep/scripts/validate.sh, scratch/rep/src/helper.py, scratch/rep/src/index.ts, scratch/rep/tests/sum.test.mjs, scratch/rep/tests/test_smoke.py, scratch/rep1.sha, scratch/rep2.sha, scripts/validate.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 85.99 seconds and 12 tool calls; token usage is in the JSON record.


Expected deliverable: Each changed guardrail rejects a planted violation, accepts valid code, and running the setup a second time changes nothing.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-quota-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
