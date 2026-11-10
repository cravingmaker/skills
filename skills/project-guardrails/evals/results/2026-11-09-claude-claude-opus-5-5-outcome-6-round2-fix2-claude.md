# project-guardrails: claude outcome-6

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-6` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `custom-hook`, SHA-256 `67a3757d431e39232095e8fdcbf6fecb55dcc6cae6102e95274dda6986592b74`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/` inside.

## Prompt

```text
Wire only the existing staged lint command into the existing custom Husky hook hooks/pre-commit, preserving npm and formatter configuration. Prefer the existing checker. Demonstrate rejection, valid acceptance and repeat evidence where executable, and report unavailable staged/local/CI parity explicitly. This source archive has no Git index.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 10 | 0 |
| baseline | n/a | false | 10 | 0 |

Treatment: 30 response lines; changed files `.cache/npm/_logs/2026-11-09T15_21_57_971Z-debug-0.log, hooks/pre-commit, scratch/after-edit.sha, scratch/baseline.sha, scratch/final.sha, scratch/fixture/.github/workflows/check.yml, scratch/fixture/CLAUDE.md, scratch/fixture/CONTRIBUTING.md, scratch/fixture/README.md, scratch/fixture/docs/hooks.md, scratch/fixture/eslint.config.mjs, scratch/fixture/hooks/pre-commit, scratch/fixture/package.json, scratch/fixture/paragraph.md, scratch/fixture/scripts/check.py, scratch/fixture/scripts/validate.sh, scratch/fixture/sources/workflow-actions.md, scratch/fixture/src/helper.py, scratch/fixture/src/index.ts, scratch/fixture/tests/sum.test.mjs, scratch/fixture/tests/test_smoke.py, scratch/npm-cache/_logs/2026-11-09T15_22_31_803Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_22_32_024Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_22_32_319Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_22_32_623Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_22_38_334Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_23_02_008Z-debug-0.log, scratch/npm-cache/_update-notifier-last-checked, scratch/repeat.sha, scratch/repeat/.cache/npm/_logs/2026-11-09T15_21_57_971Z-debug-0.log, scratch/repeat/.github/workflows/check.yml, scratch/repeat/CLAUDE.md, scratch/repeat/CONTRIBUTING.md, scratch/repeat/README.md, scratch/repeat/docs/hooks.md, scratch/repeat/eslint.config.mjs, scratch/repeat/hooks/pre-commit, scratch/repeat/package.json, scratch/repeat/paragraph.md, scratch/repeat/scripts/check.py, scratch/repeat/scripts/validate.sh, scratch/repeat/sources/workflow-actions.md, scratch/repeat/src/helper.py, scratch/repeat/src/index.ts, scratch/repeat/tests/sum.test.mjs, scratch/repeat/tests/test_smoke.py, scratch/shim/npm`; removed files `none`; validation command present: `requires review`. Workflow cost: 93.869 seconds and 10 tool calls; token usage is in the JSON record.

Baseline: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T15_23_32_259Z-debug-0.log, hooks/pre-commit, scratch/fixture/hooks/pre-commit, scratch/fixture/package.json, scratch/fixture/scripts/check.py, scratch/fixture/scripts/validate.sh, scratch/fixture/src/helper.py, scratch/fixture/src/index.ts, scratch/npm-cache/_logs/2026-11-09T15_24_01_920Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_24_02_218Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_24_02_406Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_24_02_587Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_24_02_767Z-debug-0.log, scratch/npm-cache/_logs/2026-11-09T15_24_08_062Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 68.893 seconds and 10 tool calls; token usage is in the JSON record.


Expected deliverable: An existing deterministic check wins. A recurring uncovered gap justifies a small repeat-safe tool; authorized hook setup preserves formatter/package-manager/configuration and demonstrates staged/local/CI reject, accept and repeat parity.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: partial. Treatment: partial. Value: matched.

Both change only the authorized custom hook to the existing staged:lint command and preserve npm, formatter and checker bytes. Treatment demonstrates hook reject/accept/repeat through a clearly labeled npm stand-in; baseline executes the underlying checker directly. Real npm is EPERM, Git index/Husky activation absent and CI parity unproved; neither receives staged/local/CI parity credit.
