# agent-orchestrator: claude activation-7

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-7` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `f9c2a7c444908e3c42830e844e3a504c3dbca24e`, actual bytes SHA-256 `a097ef64bd1371905586cf9a3ffe9c093f377046497666f8e5ca76da6f3e5aac`; dirty: `False`.
- **Fixture.** `activation-7`, SHA-256 `97ba29da461bec25587f8a9202645d86da5dbf2e50b638a80c1706b801f738ce`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Act as the orchestrator: run this approved code-ticket graph at configured nondefault paths.

Task context supplied identically to both arms:
Use docs/agents/issue-tracker.md nondefault paths, approved docs/specs/sync.md, .planning/work-items/sync/, current run/ and remaining budget. No re-interview or new controller. Dispatch is unavailable.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 14 | 0 |
| baseline | false | false | 27 | 0 |

Treatment: 41 response lines; changed files `.cache/npm/_logs/2026-11-09T10_17_51_601Z-debug-0.log, run/DECISIONS.md, run/LOG.md, run/PLAN.md, scratch/check-plan.txt, scratch/export.json, scratch/import.err, scratch/import.json, scratch/plan.json, scratch/preflight.md, scratch/probes/01a-create.txt, scratch/probes/01b-list-fresh.txt, scratch/probes/02-list.txt, scratch/probes/03-compare.txt, scratch/probes/03-export.txt, scratch/probes/04-email-empty.txt, scratch/probes/04-email-ws.txt, scratch/probes/05-search-exactcase.txt, scratch/probes/05-search.txt, scratch/probes/app.sha256, scratch/probes/validate.txt, scratch/state/notes.json, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 196.98 seconds and 14 tool calls; token usage is in the JSON record.

Baseline: 35 response lines; changed files `.cache/npm/_logs/2026-11-09T10_21_08_580Z-debug-0.log, app.py, run/DECISIONS.md, run/LOG.md, run/PLAN.md, scratch/baseline/app.py.orig, scratch/baseline/export.json, scratch/baseline/state/notes.json, scratch/export.json, scratch/integration/app.diff, scratch/integration/compat-export.json, scratch/integration/compat-state/notes.json, scratch/integration/list.out, scratch/integration/proof.txt, scratch/state/notes.json, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 228.747 seconds and 27 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: read the `implement-spec` skill under the current coordinator, record and remaining budget. If dispatch is unavailable, prove only source-bound preflight and report worker execution and integration acceptance as blocked.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-7-adapter-retry-claude/baseline/artifacts/`.
