# result-verification: claude near-miss-6

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-6` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `0069ed4e943922369e1c9b207e421b315a375088`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
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
| treatment | false | false | 11 | 0 |
| baseline | false | false | 14 | 0 |

Treatment: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T03_55_52_660Z-debug-0.log, scratch/evidence/export/final-1/export.json, scratch/evidence/export/final-1/report.json, scratch/evidence/export/final-1/seeded-export.json, scratch/evidence/export/negative-1/export.json, scratch/evidence/export/negative-1/report.json, scratch/evidence/export/negative-1/seeded-export.json, scratch/evidence/export/proof-1/export.json, scratch/evidence/export/proof-1/report.json, scratch/evidence/export/proof-1/seeded-export.json, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/skills/verify-core6-notes-cli/scripts/export_proof.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 132.262 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T03_58_21_581Z-debug-0.log, scratch/evidence/export-run1/export-seeded.json, scratch/evidence/export-run1/export.json, scratch/evidence/export-run1/list-seeded.stdout, scratch/evidence/export-run1/list.stdout, scratch/evidence/export-run1/state-notes.json, scratch/evidence/export-run1/transcript.jsonl, scratch/evidence/export-run1/verdict.json, scratch/evidence/export-run2/export-seeded.json, scratch/evidence/export-run2/export.json, scratch/evidence/export-run2/list-seeded.stdout, scratch/evidence/export-run2/list.stdout, scratch/evidence/export-run2/state-notes.json, scratch/evidence/export-run2/transcript.jsonl, scratch/evidence/export-run2/verdict.json, scratch/evidence/export-run3/export-seeded.json, scratch/evidence/export-run3/export.json, scratch/evidence/export-run3/list-seeded.stdout, scratch/evidence/export-run3/list.stdout, scratch/evidence/export-run3/state-notes.json, scratch/evidence/export-run3/transcript.jsonl, scratch/evidence/export-run3/verdict.json, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/skills/verify-core6-notes-cli/scripts/export_proof.py, scratch/tmp/after.txt, scratch/tmp/before.txt, scratch/tmp/helper-tests.txt, scratch/tmp/run1.stderr, scratch/tmp/run1.stdout, scratch/tmp/run2.stderr, scratch/tmp/run2.stdout, scratch/tmp/run3.stderr, scratch/tmp/run3.stdout, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 173.241 seconds and 14 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: bounded authoring through the `create-verification-skill` skill, without delegated-result intake or acceptance when no worker result was returned.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-6-claude/baseline/artifacts/`.

## Follow-up isolation audit

Successful shell redirection wrote before.txt in the shared host temporary directory; the prior read-only classification was incorrect. All behavioral and trigger conclusions from this pair are untrusted. The original JSON and Markdown are preserved in the ignored raw record directory. No replacement fits the remaining paired-run budget.
