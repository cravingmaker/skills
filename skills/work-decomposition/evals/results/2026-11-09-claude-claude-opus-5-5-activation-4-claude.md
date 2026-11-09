# work-decomposition: claude activation-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `7a576f6c0cbf17fcc0a2a47e0dec8e13d2e36291`, actual bytes SHA-256 `a83da8598f67faed667175b6c6782ffa69bb79ece6034a6591a00d2b2a60caaf`; dirty: `False`.
- **Fixture.** `activation-4`, SHA-256 `e966fe23e6fee51c1497d60cd19b67f33adae73a0513a390b7a6c3db91cde659`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Import these approved tickets for the `implement-spec` skill, retaining the one graph and shared budget.

Task context supplied identically to both arms:
Task context supplied to both arms:
Approved spec: docs/specs/saved-searches.md. Approved tickets: .planning/work-items/search/. Preserve exact sources. Planning only; 4 starts, 2 concurrent, reserve 1.

Use the one existing graph and shared allowance. No worker starts, graph runner, commits or tracker closure are authorized; import and coordinator preflight only.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 11 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 31 response lines; changed files `.cache/npm/_logs/2026-11-09T03_43_49_171Z-debug-0.log, scratch/runs/saved-searches-import/BUDGET.md, scratch/runs/saved-searches-import/DECISIONS.md, scratch/runs/saved-searches-import/LOG.md, scratch/runs/saved-searches-import/PLAN.md, scratch/runs/saved-searches-import/raw/check-plan-r1.txt, scratch/runs/saved-searches-import/raw/import-tickets.json, scratch/runs/saved-searches-import/raw/import-tickets.stderr`; removed files `none`; validation command present: `requires review`. Workflow cost: 115.154 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T03_45_44_987Z-debug-0.log, scratch/saved-searches/PLAN.md, scratch/saved-searches/preflight.md, scratch/saved-searches/probes/baseline-cli.txt, scratch/saved-searches/probes/baseline-validate.txt, scratch/saved-searches/sources.sha256, scratch/saved-searches/sources/.planning/work-items/search/01-save-a-search.md, scratch/saved-searches/sources/.planning/work-items/search/02-list-saved-searches.md, scratch/saved-searches/sources/docs/agents/issue-tracker.md, scratch/saved-searches/sources/docs/product/vocabulary.md, scratch/saved-searches/sources/docs/specs/saved-searches.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 92.579 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-4-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-4-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/artifacts/`.
