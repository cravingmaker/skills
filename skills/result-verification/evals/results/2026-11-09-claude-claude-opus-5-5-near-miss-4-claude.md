# result-verification: claude near-miss-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-4` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `0069ed4e943922369e1c9b207e421b315a375088`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `near-miss-4`, SHA-256 `b7c7891d1b710640f661be42ad537643a6b81c4a3fecdc369444988ef3d3e0f4`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [result-verification.tar.gz](https://drive.google.com/file/d/1rG3ldD66TlC28hZZt7xINNlgtOv3GBsY/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/` inside.

## Prompt

```text
Author a way to drive this application

Task context supplied identically to both arms:
Named missing proof is CLI export writing exact listed notes to JSON. Author only that bounded driver; no worker acceptance or product repair is authorized unless actual returned results exist.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 12 | 0 |
| baseline | false | false | 11 | 0 |

Treatment: 32 response lines; changed files `.cache/npm/_logs/2026-11-09T03_55_35_533Z-debug-0.log, scratch/evidence/manual-1794196658/export.json, scratch/evidence/manual-1794196658/list.json, scratch/evidence/proof-1/fidelity-export.json, scratch/evidence/proof-1/fidelity-list.stdout, scratch/evidence/proof-1/fidelity-seed.json, scratch/evidence/proof-1/summary.json, scratch/evidence/proof-1/transcript.jsonl, scratch/evidence/proof-1/user-export.json, scratch/evidence/proof-1/user-list.stdout, scratch/tmp/bad-seed.json, scratch/tmp/mutant/app.py, scratch/tmp/mutant/scratch/evidence/negative-control/fidelity-export.json, scratch/tmp/mutant/scratch/evidence/negative-control/fidelity-list.stdout, scratch/tmp/mutant/scratch/evidence/negative-control/fidelity-seed.json, scratch/tmp/mutant/scratch/evidence/negative-control/summary.json, scratch/tmp/mutant/scratch/evidence/negative-control/transcript.jsonl, scratch/tmp/mutant/scratch/evidence/negative-control/user-export.json, scratch/tmp/mutant/scratch/evidence/negative-control/user-list.stdout, scratch/tmp/negative.stdout, scratch/tmp/proof-1.stdout, scratch/verify-core6-notes-cli/SKILL.md, scratch/verify-core6-notes-cli/evals/examples.md, scratch/verify-core6-notes-cli/scripts/export_probe.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 136.783 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T03_58_05_111Z-debug-0.log, scratch/runs/r1/evidence.json, scratch/runs/r1/export-cli.json, scratch/runs/r1/export-seeded.json, scratch/runs/r1/seed.json, scratch/runs/r1/store-cli.json, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/skills/verify-core6-notes-cli/scripts/drive_export.py, scratch/tmp/architecture-report.md, scratch/tmp/broken/app.py, scratch/tmp/broken/scratch/runs/neg/evidence.json, scratch/tmp/broken/scratch/runs/neg/export-cli.json, scratch/tmp/broken/scratch/runs/neg/export-seeded.json, scratch/tmp/broken/scratch/runs/neg/seed.json, scratch/tmp/broken/scratch/runs/neg/store-cli.json`; removed files `none`; validation command present: `requires review`. Workflow cost: 122.638 seconds and 11 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: scoped authoring only; no completed delegated result is being accepted.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/artifacts/`.
