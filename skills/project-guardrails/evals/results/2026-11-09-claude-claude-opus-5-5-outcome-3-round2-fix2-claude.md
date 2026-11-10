# project-guardrails: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/` inside.

## Prompt

```text
Audit the current guardrails without changes. Report installed versions and their actual sources. No network or current upstream guidance is available; leave those guidance gaps open instead of guessing.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 18 | 0 |
| baseline | n/a | false | 12 | 0 |

Treatment: 65 response lines; changed files `.cache/npm/_logs/2026-11-09T15_19_56_609Z-debug-0.log, scratch/before.sha, scratch/probe/eslint.config.mjs, scratch/probe/package.json, scratch/probe/scripts/check.py, scratch/probe/scripts/validate.sh, scratch/probe/src/bad.ts, scratch/probe/src/helper.py, scratch/probe/src/index.ts, scratch/probe/tests/__pycache__/test_smoke.cpython-315.pyc, scratch/probe/tests/sum.test.mjs, scratch/probe/tests/test_smoke.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 127.615 seconds and 18 tool calls; token usage is in the JSON record.

Baseline: 49 response lines; changed files `.cache/npm/_logs/2026-11-09T15_22_04_276Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 103.498 seconds and 12 tool calls; token usage is in the JSON record.


Expected deliverable: The report lists versions with their sources, and any capability whose current guidance could not be confirmed is reported as open, not filled with a guess.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: partial. Treatment: partial. Value: matched.

Both list observed local versions with sources and keep offline upstream/CI guidance open instead of guessing. Treatment cannot establish npm version after denied probes and says so. Baseline runtime-directory metadata outside the fixture is a protocol exception, not method credit. No product edits; blocked network/runtime probes do not establish current guidance.

## Protocol exception

A baseline runtime-path probe returned three real-home directory names outside the fixture. Another path and the treatment combined probe were denied. No personal file bodies were returned by those requests. This violates the task boundary; directory metadata receives no method or current-guidance credit. Exact requests and results remain in private evidence. The comparison is harness-valid, not protocol-clean.
