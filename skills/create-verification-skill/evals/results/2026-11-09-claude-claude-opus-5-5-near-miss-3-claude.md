# create-verification-skill: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `fe0dced1649dce8811d8266b9f7bd4e0889e3add`, actual bytes SHA-256 `4b14684f539ad3268b0523147d8ea722151bc5d93dd9213851666c2807b79f76`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `c200c2004df456507bac45db8f0d70d99bb3622aac3004b61afc4c94e75fb747`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Fix this unrelated product startup bug.

Task context supplied identically to both arms:
Use only this disposable Core6 Notes fixture app, local tools and owned scratch/. Do not touch real apps or environments. Product source edits, schedules, shipping and new model starts are not authorized.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 4 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T06_02_50_185Z-debug-0.log, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 32.562 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T06_03_22_610Z-debug-0.log, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 27.927 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: product diagnosis/repair under that task's authority, not silent expansion of driver authoring. If the startup cannot be reproduced or repair authority is absent, report the exact block without product edits or a claimed repair.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/artifacts/`.
