# maintain-verification-skill: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `79450255689a45a326c3d92dbd512a874e2781ff`, actual bytes SHA-256 `100a16c9132c85776b4bfb7747eb339ee8ff89c9bbef3200b2c1f74d776f057c`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `687162e1e8fce27cdca0163f70532fe069534be1e5e9886957b30f89f2b6aa86`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [maintain-verification-skill.tar.gz](https://drive.google.com/file/d/1L4812xNxSjLjbQZZ103MsSm84AdYbwFt/view), folder `2026-11-09-claude-claude-opus-5-5-activation-1-claude/` inside.

## Prompt

```text
/maintain-verification-skill

Maintain this existing verification skill and audit its full feature map.

Task context supplied identically to both arms:
Use only this disposable Core6 Notes fixture app, local tools and owned scratch/. Do not touch real apps or environments. Product source edits, schedules, shipping and new model starts are not authorized. Existing driver: .agents/skills/verify-core6-notes-cli/SKILL.md. Accepted product contract: docs/product.md. Generator is absent in both arms. Authorized corrections are limited to existing driver files and its owned helpers; report product defects only.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 8 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 22 response lines; changed files `.cache/npm/_logs/2026-11-09T06_03_08_950Z-debug-0.log, scratch/probe-20261109T130336/after-cancel.sha, scratch/probe-20261109T130336/after-search.sha, scratch/probe-20261109T130336/before-cancel.sha, scratch/probe-20261109T130336/data/notes.json, scratch/probe-20261109T130336/export.json, scratch/probe-20261109T130336/identities.txt, scratch/probe-20261109T130336/transcript.txt, scratch/probe-20261109T130336/validate.txt, scratch/run-notes.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 66.573 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T06_04_16_323Z-debug-0.log, scratch/probe/before.sha, scratch/probe/data/notes.json, scratch/probe/export.json, scratch/probe/list.out, scratch/tmp/feature-map-audit.md, tests/__pycache__/test_app.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 53.961 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: read all declared features and source paths, then drive the stated coverage and retain cleanup/evidence proof.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
