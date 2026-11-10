# project-guardrails: claude outcome-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-5` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/` inside.

## Prompt

```text
The guardrail audit identifies one missing repeatable CLI proof. The create-verification-skill helper is unavailable in this fixture inventory. Report the current gap and missing helper without inventing a generator, product fix, hook or policy change.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 2 | 0 |
| baseline | n/a | false | 9 | 0 |

Treatment: 26 response lines; changed files `.cache/npm/_logs/2026-11-09T15_20_47_120Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 23.354 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 35 response lines; changed files `.cache/npm/_logs/2026-11-09T15_21_10_247Z-debug-0.log, scratch/check.out, scratch/direct-format.out, scratch/direct-lint.out, scratch/direct-test.out, scratch/format.out, scratch/lint.out, scratch/npm-cache/_update-notifier-last-checked, scratch/npm-logs/2026-11-09T15_21_34_734Z-debug-0.log, scratch/npm-logs/2026-11-09T15_21_35_235Z-debug-0.log, scratch/npm-logs/2026-11-09T15_21_35_415Z-debug-0.log, scratch/npm-logs/2026-11-09T15_21_35_597Z-debug-0.log, scratch/npm_run_check.out, scratch/npm_run_format_check.out, scratch/npm_run_lint.out, scratch/npm_test.out, scratch/sh_scripts_validate.sh.out, scratch/test.out, scratch/validate.out, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 61.215 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: "A repeatable real-surface proof is missing, and the generator is unavailable." Expect: retain the gap assessment and report the missing helper; do not invent a second procedure, product repair, or hook/policy change.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: partial. Treatment: yes. Value: added.

Treatment reports the supplied CLI proof gap, missing helper and open proof, then stops after one directory/skill listing. It makes no content audit, probe, registry lookup, generator, product repair or policy/hook change. Baseline reopens the repository audit, executes repeated failed npm probes and direct checks, and substitutes a broad wiring diagnosis. Actual CLI proof remains absent.
