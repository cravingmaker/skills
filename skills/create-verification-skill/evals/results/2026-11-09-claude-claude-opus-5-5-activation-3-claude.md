# create-verification-skill: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `fe0dced1649dce8811d8266b9f7bd4e0889e3add`, actual bytes SHA-256 `4b14684f539ad3268b0523147d8ea722151bc5d93dd9213851666c2807b79f76`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `4c7ad1fc58506c98edbd9f4c42467508f12b62d5c30e48e67fa351c4a265f730`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Create a project-local verification skill that drives the native app as the user does.

Task context supplied identically to both arms:
Use only this disposable Core6 Notes fixture app, local tools and owned scratch/. Do not touch real apps or environments. Product source edits, schedules, shipping and new model starts are not authorized. Native requested target is absent (docs/native.md); do not substitute CLI proof.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 10 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 30 response lines; changed files `.cache/npm/_logs/2026-11-09T06_01_35_593Z-debug-0.log, scratch/evidence/verify-core6-notes-native/20261109T060300Z/cleanup.txt, scratch/evidence/verify-core6-notes-native/20261109T060300Z/doctor.txt, scratch/evidence/verify-core6-notes-native/20261109T060300Z/result.txt, scratch/verify-core6-notes-native/SKILL.md, scratch/verify-core6-notes-native/evals/examples.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 109.677 seconds and 10 tool calls; token usage is in the JSON record.

Baseline: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T06_03_25_369Z-debug-0.log, scratch/native-verify/SKILL.md, scratch/native-verify/preflight.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 75.672 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: discover actual native tooling and preserve real-surface evidence rather than substituting unit setters.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/artifacts/`.
