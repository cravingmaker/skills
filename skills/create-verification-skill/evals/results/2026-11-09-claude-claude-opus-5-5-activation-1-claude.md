# create-verification-skill: claude activation-1

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

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
| treatment | true | true | 33 | 0 |
| baseline | false | unavailable | unavailable | 143 |

Treatment: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T06_01_08_181Z-debug-0.log, scratch/evidence/verify-core6-notes-web/20261109-proof1/SUPERSEDED.txt, scratch/evidence/verify-core6-notes-web/20261109-proof1/identity.txt, scratch/evidence/verify-core6-notes-web/20261109-proof1/launch-web-py.txt, scratch/evidence/verify-core6-notes-web/20261109-proof1/new-note-link.json, scratch/evidence/verify-core6-notes-web/20261109-proof1/page-shell.json, scratch/evidence/verify-core6-notes-web/20261109-proof2/SUPERSEDED.txt, scratch/evidence/verify-core6-notes-web/20261109-proof2/cancel.json, scratch/evidence/verify-core6-notes-web/20261109-proof2/create-rerun.json, scratch/evidence/verify-core6-notes-web/20261109-proof2/create.json, scratch/evidence/verify-core6-notes-web/20261109-proof2/identity.txt, scratch/evidence/verify-core6-notes-web/20261109-proof2/launch.err, scratch/evidence/verify-core6-notes-web/20261109-proof2/launch.json, scratch/evidence/verify-core6-notes-web/20261109-proof2/new-note-link.json, scratch/evidence/verify-core6-notes-web/20261109-proof2/page-shell.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/RESULT.md, scratch/evidence/verify-core6-notes-web/20261109-proof3/cancel.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/create-dry-run.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/create-from-new.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/create.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/doctor.err, scratch/evidence/verify-core6-notes-web/20261109-proof3/doctor.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/identity.txt, scratch/evidence/verify-core6-notes-web/20261109-proof3/launch-dry-run.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/launch.err, scratch/evidence/verify-core6-notes-web/20261109-proof3/launch.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/new-note-link.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/page-shell.json, scratch/evidence/verify-core6-notes-web/20261109-proof3/rejected.err, scratch/evidence/verify-core6-notes-web/20261109-proof3/search-shell.json, scratch/verify-core6-notes-web/SKILL.md, scratch/verify-core6-notes-web/evals/examples.md, scratch/verify-core6-notes-web/references/anchors.md, scratch/verify-core6-notes-web/references/cancel-draft.md, scratch/verify-core6-notes-web/references/create-note.md, scratch/verify-core6-notes-web/references/feature-map.md, scratch/verify-core6-notes-web/references/new-note-link.md, scratch/verify-core6-notes-web/references/page-shell.md, scratch/verify-core6-notes-web/references/reload-persistence.md, scratch/verify-core6-notes-web/references/search.md, scratch/verify-core6-notes-web/scripts/notes_web.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 361.534 seconds and 33 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: one namespaced project/surface driver, a complete declared inventory, direct references and the single launch/doctor/drive/evidence/cleanup recipe.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json).

## Invalid comparison

- claude baseline failed (exit 143, timeout True); inspect stderr and trace

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.

## Quota limit

Claude five-hour quota exhausted; advertised reset2026-11-09 09:50 UTC /16:50 Asia/Jakarta. This trial is invalid and has no comparative credit.
