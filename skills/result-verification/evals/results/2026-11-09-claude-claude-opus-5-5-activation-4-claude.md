# result-verification: claude activation-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `0069ed4e943922369e1c9b207e421b315a375088`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `activation-4`, SHA-256 `8291ad191a9507134a1fe04004e89fae67d0ab03aed5733bcc87e1facd82d460`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [result-verification.tar.gz](https://drive.google.com/file/d/1rG3ldD66TlC28hZZt7xINNlgtOv3GBsY/view), folder `2026-11-09-claude-claude-opus-5-5-activation-4-claude/` inside.

## Prompt

```text
Accept these ticket results only after their named CLI Proof runs on each worker artifact and the integrated revision.

Task context supplied identically to both arms:
This request is the missing-observation step of existing delegated-result intake in run/. First read the returned raw inbox/export.md and briefs/export.md. The exact worker artifact is workers/export/app.py; the integration artifact is app.py. Each has its SHA-256 in the brief. No sufficient existing project driver is installed. Bounded driver authoring and local CLI rechecks on both provided artifacts are authorized; use only owned scratch resources. Do not edit either product artifact, expand to a feature map, close tickets or substitute unit tests for the named CLI file observation. Keep acceptance unresolved for any missing/failing worker or integration Proof.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 16 | 0 |
| baseline | false | false | 14 | 0 |

Treatment: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T03_52_34_231Z-debug-0.log, run/DECISIONS.md, run/LOG.md, scratch/evidence/integrated-1/data/notes.json, scratch/evidence/integrated-1/export.json, scratch/evidence/integrated-1/receipt.json, scratch/evidence/worker-1/data/notes.json, scratch/evidence/worker-1/export.json, scratch/evidence/worker-1/receipt.json, scratch/run/INTAKE.md, scratch/run/fixture-after.sha256, scratch/run/fixture-before.sha256, scratch/run/raw/T3-export.md, scratch/run/validate.out, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/skills/verify-core6-notes-cli/scripts/export-proof.py, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 144.288 seconds and 16 tool calls; token usage is in the JSON record.

Baseline: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T03_55_34_877Z-debug-0.log, run/DECISIONS.md, run/LOG.md, scratch/evidence/integration-29932473-rerun/evidence.json, scratch/evidence/integration-29932473-rerun/export.json, scratch/evidence/integration-29932473-rerun/notes.json.snapshot, scratch/evidence/integration-29932473/evidence.json, scratch/evidence/integration-29932473/export.json, scratch/evidence/integration-29932473/notes.json.snapshot, scratch/evidence/worker-bf87fd15/evidence.json, scratch/evidence/worker-bf87fd15/export.json, scratch/evidence/worker-bf87fd15/notes.json.snapshot, scratch/verify-core6-notes-cli/SKILL.md, scratch/verify-core6-notes-cli/evals/examples.md, scratch/verify-core6-notes-cli/export_proof.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 106.928 seconds and 14 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/artifacts/`.
