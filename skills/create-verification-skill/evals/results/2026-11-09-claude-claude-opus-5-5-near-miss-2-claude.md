# create-verification-skill: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `fe0dced1649dce8811d8266b9f7bd4e0889e3add`, actual bytes SHA-256 `4b14684f539ad3268b0523147d8ea722151bc5d93dd9213851666c2807b79f76`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `687162e1e8fce27cdca0163f70532fe069534be1e5e9886957b30f89f2b6aa86`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Audit the existing verification skill and map.

Task context supplied identically to both arms:
Use only this disposable Core6 Notes fixture app, local tools and owned scratch/. Do not touch real apps or environments. Product source edits, schedules, shipping and new model starts are not authorized. Read-only audit only; no driver edits.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 8 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 26 response lines; changed files `.cache/npm/_logs/2026-11-09T06_02_16_232Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 62.905 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 31 response lines; changed files `.cache/npm/_logs/2026-11-09T06_03_19_153Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 64.458 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: maintenance can use the existing driver directly, without requiring this generator.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/artifacts/`.
