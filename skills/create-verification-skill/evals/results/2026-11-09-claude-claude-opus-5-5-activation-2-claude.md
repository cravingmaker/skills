# create-verification-skill: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `fe0dced1649dce8811d8266b9f7bd4e0889e3add`, actual bytes SHA-256 `4b14684f539ad3268b0523147d8ea722151bc5d93dd9213851666c2807b79f76`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `687162e1e8fce27cdca0163f70532fe069534be1e5e9886957b30f89f2b6aa86`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Our guardrail audit found one gap: prove this CLI command writes the expected file. Make a small repeatable recipe.

Task context supplied identically to both arms:
Use only this disposable Core6 Notes fixture app, local tools and owned scratch/. Do not touch real apps or environments. Product source edits, schedules, shipping and new model starts are not authorized. Bounded gap: real CLI `export --output PATH` must write JSON equal to list after create Lamps. Do not sweep other features. No sufficient existing export driver is installed.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 18 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 35 response lines; changed files `.cache/npm/_logs/2026-11-09T06_01_17_957Z-debug-0.log, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/create.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/doctor.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/export.json, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/export.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/list.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/notes.json.snapshot, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/result.json, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26389/transcript.json, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/create.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/doctor.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/export.json, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/export.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/list.stdout, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/notes.json.snapshot, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/result.json, scratch/evidence/verify-core6-notes-cli/run-20261109T130317-26491/transcript.json, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/skills/verify-core6-notes-cli/scripts/verify_export.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 141.452 seconds and 18 tool calls; token usage is in the JSON record.

Baseline: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T06_03_39_605Z-debug-0.log, scratch/mutant/app.py, scratch/prove_export.py, scratch/runs/export-07ehsiie/data/notes.json, scratch/runs/export-07ehsiie/out/export.json, scratch/runs/export-dj92iege/data/notes.json, scratch/runs/export-dj92iege/out/export.json, scratch/runs/export-nnjknakq/data/notes.json, scratch/runs/export-nnjknakq/out/export.json, scratch/runs/export-ti5kk_on/data/notes.json, scratch/runs/export-ti5kk_on/out/export.json, scratch/runs/export-zjsw2tel/data/notes.json, scratch/runs/export-zjsw2tel/out/export.json, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 56.247 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: bounded-gap mode for that journey, without a feature sweep or policy/hook changes.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.
