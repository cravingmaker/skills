# improve-codebase-architecture: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `112730a60b96ddc7f4e0b0817e5fee67f4824763`, actual bytes SHA-256 `f2ebc82b0263b946b25f6308383f1363731ea26728333d874fc3c893c540afbd`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `4c7f4e00bc441adc626f7ff1cecd9a21aef5165b2ad6f4b1627bbdd4a0f20a8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Refactor OrderHandler into one module now.

Task context supplied identically to both arms:
Agreed scope is src/billing/order_service.py and its two controlled callers; preserve existing public data behavior.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 10 | 0 |
| baseline | false | false | 10 | 0 |

Treatment: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T05_06_56_302Z-debug-0.log, scratch/after.json, scratch/baseline.json, scratch/probe.py, src/billing/__pycache__/caller.cpython-315.pyc, src/billing/__pycache__/order_service.cpython-315.pyc, src/billing/__pycache__/renewal.cpython-315.pyc, src/billing/caller.py, src/billing/order_service.py, src/billing/renewal.py, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 53.683 seconds and 10 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T05_09_20_506Z-debug-0.log, scratch/after.json, scratch/before.json, scratch/probe.py, src/billing/__pycache__/caller.cpython-315.pyc, src/billing/__pycache__/order_service.cpython-315.pyc, src/billing/__pycache__/renewal.cpython-315.pyc, src/billing/caller.py, src/billing/order_service.py, src/billing/renewal.py, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 49.144 seconds and 10 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a scoped refactor with no survey report; the manual `implement` entry is tested only when explicitly invoked.

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
