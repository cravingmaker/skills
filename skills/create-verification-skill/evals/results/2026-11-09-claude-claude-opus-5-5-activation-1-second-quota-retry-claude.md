# create-verification-skill: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `fe0dced1649dce8811d8266b9f7bd4e0889e3add`, actual bytes SHA-256 `4b14684f539ad3268b0523147d8ea722151bc5d93dd9213851666c2807b79f76`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `efed674675fd4b565462174b353e2a24c4cd6070e1ecc645a4a18affacf1f977`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Make a driver skill for this repo's web app with a full feature map.

Task context supplied identically to both arms:
Use only this disposable Core6 Notes fixture app, local tools and owned scratch/. Do not touch real apps or environments. Product source edits, schedules, shipping and new model starts are not authorized. Requested full map is the web surface in docs/web.md; CLI is a separate surface. Baseline web scaffold/tool limits stay explicit.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 23 | 0 |
| baseline | false | false | 15 | 0 |

Treatment: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T10_25_13_929Z-debug-0.log, .cache/npm/_logs/2026-11-09T10_26_00_464Z-debug-0.log, scratch/skills/verify-core6-notes-web/SKILL.md, scratch/skills/verify-core6-notes-web/evals/examples.md, scratch/skills/verify-core6-notes-web/references/anchors.md, scratch/skills/verify-core6-notes-web/references/feature-map.md, scratch/skills/verify-core6-notes-web/references/features/cancel-draft.md, scratch/skills/verify-core6-notes-web/references/features/create-note.md, scratch/skills/verify-core6-notes-web/references/features/reload-persistence.md, scratch/skills/verify-core6-notes-web/references/features/search-notes.md, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/build.sha256, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/cleanup.txt, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/env.sh, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/health.txt, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/precheck.txt, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/python.txt, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/result.md, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/server.log, scratch/verify-core6-notes-web/runs/20261109T102945Z-78458/server.pid, scratch/verify-core6-notes-web/runs/baseline-1794219961/NOTE.txt, scratch/verify-core6-notes-web/runs/baseline-1794219961/health.txt, scratch/verify-core6-notes-web/runs/baseline-1794219961/server.log, scratch/verify-core6-notes-web/runs/baseline-1794219961/server.pid`; removed files `none`; validation command present: `requires review`. Workflow cost: 317.272 seconds and 23 tool calls; token usage is in the JSON record.

Baseline: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T10_30_31_468Z-debug-0.log, .cache/npm/_logs/2026-11-09T10_30_53_470Z-debug-0.log, scratch/probe/inproc-output.txt, scratch/probe/inproc.py, scratch/runs/web-1/web-report.json, scratch/runs/web-1/web-report.md, scratch/runs/web-2/web-report.json, scratch/runs/web-2/web-report.md, scratch/skills/core6-notes-web-driver/SKILL.md, scratch/skills/core6-notes-web-driver/scripts/drive_web.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 174.014 seconds and 15 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: one namespaced project/surface driver, a complete declared inventory, direct references and the single launch/doctor/drive/evidence/cleanup recipe.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-second-quota-retry-claude/baseline/artifacts/`.
