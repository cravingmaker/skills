# project-guardrails: claude near-miss-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-4` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `19d23957b323b07f81d893869fa718d2fc4d2bea`, actual bytes SHA-256 `8c38dc1412508ef8db646c18de40214dd3c62a551651c9ac0fd938ec06c79fd8`; dirty: `False`.
- **Fixture.** `near-miss-4`, SHA-256 `155e0b6530ddb96dd595599578740a711c8e4f4268f87e6fdc1199c8ed2d5589`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
The audit finds one missing CLI proof; keep the fix small.

Task context supplied identically to both arms:
Audit gap is only CLI export file proof. Author just its bounded recipe in the disposable fixture; no full map or hook change.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 12 | 0 |
| baseline | false | false | 14 | 0 |

Treatment: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T03_26_05_944Z-debug-0.log, scratch/evidence/export-20261109T032730Z-83405/build.txt, scratch/evidence/export-20261109T032730Z-83405/create.out, scratch/evidence/export-20261109T032730Z-83405/doctor.out, scratch/evidence/export-20261109T032730Z-83405/export.err, scratch/evidence/export-20261109T032730Z-83405/export.exit, scratch/evidence/export-20261109T032730Z-83405/export.json, scratch/evidence/export-20261109T032730Z-83405/export.out, scratch/evidence/export-20261109T032730Z-83405/list-after.out, scratch/evidence/export-20261109T032730Z-83405/list-before.out, scratch/evidence/export-20261109T032730Z-83405/ls-before-reject.txt, scratch/evidence/export-20261109T032730Z-83405/notes-after.sha256, scratch/evidence/export-20261109T032730Z-83405/notes-before.sha256, scratch/evidence/export-20261109T032730Z-83405/reject.err, scratch/evidence/export-20261109T032730Z-83405/reject.exit, scratch/evidence/export-20261109T032730Z-83405/reject.out, scratch/evidence/export-20261109T032730Z-83405/result.txt, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/tmp/recipe.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 106.015 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T03_28_37_811Z-debug-0.log, scratch/evidence/export-20261109T033030Z-32674/create1.exit, scratch/evidence/export-20261109T033030Z-32674/create1.stderr, scratch/evidence/export-20261109T033030Z-32674/create1.stdout, scratch/evidence/export-20261109T033030Z-32674/create2.exit, scratch/evidence/export-20261109T033030Z-32674/create2.stderr, scratch/evidence/export-20261109T033030Z-32674/create2.stdout, scratch/evidence/export-20261109T033030Z-32674/doctor.exit, scratch/evidence/export-20261109T033030Z-32674/doctor.stderr, scratch/evidence/export-20261109T033030Z-32674/doctor.stdout, scratch/evidence/export-20261109T033030Z-32674/export.exit, scratch/evidence/export-20261109T033030Z-32674/export.json, scratch/evidence/export-20261109T033030Z-32674/export.stderr, scratch/evidence/export-20261109T033030Z-32674/export.stdout, scratch/evidence/export-20261109T033030Z-32674/identity.txt, scratch/evidence/export-20261109T033030Z-32674/list.exit, scratch/evidence/export-20261109T033030Z-32674/list.stderr, scratch/evidence/export-20261109T033030Z-32674/list.stdout, scratch/evidence/export-20261109T033030Z-32674/reject.exit, scratch/evidence/export-20261109T033030Z-32674/reject.stderr, scratch/evidence/export-20261109T033030Z-32674/reject.stdout, scratch/evidence/export-20261109T033030Z-32674/rerun.exit, scratch/evidence/export-20261109T033030Z-32674/rerun.stderr, scratch/evidence/export-20261109T033030Z-32674/rerun.stdout, scratch/evidence/export-20261109T033030Z-32674/store-after.sha256, scratch/evidence/export-20261109T033030Z-32674/store-before.sha256, scratch/evidence/export-20261109T033030Z-32674/transcript.txt, scratch/evidence/export-20261109T033030Z-32674/verdict.txt, scratch/evidence/export-20261109T033046Z-34195/create1.exit, scratch/evidence/export-20261109T033046Z-34195/create1.stderr, scratch/evidence/export-20261109T033046Z-34195/create1.stdout, scratch/evidence/export-20261109T033046Z-34195/create2.exit, scratch/evidence/export-20261109T033046Z-34195/create2.stderr, scratch/evidence/export-20261109T033046Z-34195/create2.stdout, scratch/evidence/export-20261109T033046Z-34195/doctor.exit, scratch/evidence/export-20261109T033046Z-34195/doctor.stderr, scratch/evidence/export-20261109T033046Z-34195/doctor.stdout, scratch/evidence/export-20261109T033046Z-34195/export.exit, scratch/evidence/export-20261109T033046Z-34195/export.json, scratch/evidence/export-20261109T033046Z-34195/export.stderr, scratch/evidence/export-20261109T033046Z-34195/export.stdout, scratch/evidence/export-20261109T033046Z-34195/identity.txt, scratch/evidence/export-20261109T033046Z-34195/list.exit, scratch/evidence/export-20261109T033046Z-34195/list.stderr, scratch/evidence/export-20261109T033046Z-34195/list.stdout, scratch/evidence/export-20261109T033046Z-34195/reject.exit, scratch/evidence/export-20261109T033046Z-34195/reject.stderr, scratch/evidence/export-20261109T033046Z-34195/reject.stdout, scratch/evidence/export-20261109T033046Z-34195/rerun.exit, scratch/evidence/export-20261109T033046Z-34195/rerun.stderr, scratch/evidence/export-20261109T033046Z-34195/rerun.stdout, scratch/evidence/export-20261109T033046Z-34195/store-after.sha256, scratch/evidence/export-20261109T033046Z-34195/store-before.sha256, scratch/evidence/export-20261109T033046Z-34195/transcript.txt, scratch/evidence/export-20261109T033046Z-34195/verdict.txt, scratch/probe/data/notes.json, scratch/probe/empty.json, scratch/probe/export.json, scratch/probe/list.out, scratch/skills/verify-core6-notes-cli/SKILL.md, scratch/skills/verify-core6-notes-cli/evals/examples.md, scratch/tmp/block1.sh, scratch/tmp/block2.sh, scratch/tmp/recipe.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 141.255 seconds and 14 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: discover existing commands and use the `create-verification-skill` skill for bounded authoring; no guardrail audit, full feature sweep or hook/policy changes are needed for this isolated proof task.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/artifacts/`.
