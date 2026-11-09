# result-verification: claude near-miss-6

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-6` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `af3695a46ef210bb6a30c875573b195e8900d1f6`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `near-miss-6`, SHA-256 `b7c7891d1b710640f661be42ad537643a6b81c4a3fecdc369444988ef3d3e0f4`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
The named CLI observation has no driver; author only the missing repeatable proof within this task's scope.

Task context supplied identically to both arms:
Named missing proof is CLI export writing exact listed notes to JSON. Author only that bounded driver; no worker acceptance or product repair is authorized unless actual returned results exist.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 13 | 0 |
| baseline | false | false | 15 | 0 |

Treatment: 36 response lines; changed files `.cache/npm/_logs/2026-11-09T11_19_43_703Z-debug-0.log, scratch/evidence/proof1/export-created.json, scratch/evidence/proof1/export-empty.json, scratch/evidence/proof1/export-seeded.json, scratch/evidence/proof1/list-created.json, scratch/evidence/proof1/list-empty.json, scratch/evidence/proof1/list-seeded.json, scratch/evidence/proof1/result.json, scratch/evidence/proof1/seed-notes.json, scratch/evidence/proof1/transcript.json, scratch/evidence/proof2/export-created.json, scratch/evidence/proof2/export-empty.json, scratch/evidence/proof2/export-seeded.json, scratch/evidence/proof2/list-created.json, scratch/evidence/proof2/list-empty.json, scratch/evidence/proof2/list-seeded.json, scratch/evidence/proof2/result.json, scratch/evidence/proof2/seed-notes.json, scratch/evidence/proof2/transcript.json, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/skills/verify-core6-notes-cli/scripts/export_proof.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 122.787 seconds and 13 tool calls; token usage is in the JSON record.

Baseline: 22 response lines; changed files `.cache/npm/_logs/2026-11-09T11_22_47_885Z-debug-0.log, scratch/evidence/export/20261109T112459Z-58342/files/created/export.json, scratch/evidence/export/20261109T112459Z-58342/files/created/state/notes.json, scratch/evidence/export/20261109T112459Z-58342/files/rejected/state/notes.json, scratch/evidence/export/20261109T112459Z-58342/files/seeded/export.json, scratch/evidence/export/20261109T112459Z-58342/files/seeded/state/notes.json, scratch/evidence/export/20261109T112459Z-58342/summary.json, scratch/evidence/export/proof1/files/created/export.json, scratch/evidence/export/proof1/files/created/state/notes.json, scratch/evidence/export/proof1/files/rejected/state/notes.json, scratch/evidence/export/proof1/files/seeded/export.json, scratch/evidence/export/proof1/files/seeded/state/notes.json, scratch/evidence/export/proof1/summary.json, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/skills/verify-core6-notes-cli/scripts/drive_export.py, scratch/tmp/mutant/app.py, scratch/tmp/mutant/scratch/evidence/export/mutant1/files/created/export.json, scratch/tmp/mutant/scratch/evidence/export/mutant1/files/created/state/notes.json, scratch/tmp/mutant/scratch/evidence/export/mutant1/files/rejected/state/notes.json, scratch/tmp/mutant/scratch/evidence/export/mutant1/files/seeded/export.json, scratch/tmp/mutant/scratch/evidence/export/mutant1/files/seeded/state/notes.json, scratch/tmp/mutant/scratch/evidence/export/mutant1/summary.json, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 156.692 seconds and 15 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: bounded authoring through the `create-verification-skill` skill, without delegated-result intake or acceptance when no worker result was returned.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-6-round2-pre-claude/baseline/artifacts/`.
