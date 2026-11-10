# result-verification: claude near-miss-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-5` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `af3695a46ef210bb6a30c875573b195e8900d1f6`, actual bytes SHA-256 `8520be2fd79af262847aa01258c7cf87f21037b5a2954c6a796d7cbbfe00d193`; dirty: `False`.
- **Fixture.** `near-miss-5`, SHA-256 `fded7101a88e33ae2704950ed55c0f5f47d2340cfe898e453cf75002ff0fee27`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [result-verification.tar.gz](https://drive.google.com/file/d/1rG3ldD66TlC28hZZt7xINNlgtOv3GBsY/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/` inside.

## Prompt

```text
Maintain the existing collector CLI project driver without returned worker results. Audit its declared bounded journey against current source and run the actual CLI; update only .agents/skills/verify-collector-cli/ and retain evidence. There is no delegated result to accept. No product repairs, commits, pushes or agents.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 10 | 0 |
| baseline | false | false | 26 | 0 |

Treatment: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T11_19_20_569Z-debug-0.log, .fixture/events.jsonl, .git/index`; removed files `none`; validation command present: `requires review`. Workflow cost: 61.124 seconds and 10 tool calls; token usage is in the JSON record.

Baseline: 34 response lines; changed files `.agents/skills/verify-collector-cli/SKILL.md, .agents/skills/verify-collector-cli/evals/examples.md, .agents/skills/verify-collector-cli/evidence/20261109T112334Z-integration.json, .agents/skills/verify-collector-cli/evidence/20261109T112335Z-integration.json, .agents/skills/verify-collector-cli/evidence/20261109T112335Z-worker.json, .agents/skills/verify-collector-cli/evidence/20261109T112401Z-integration-1.json, .agents/skills/verify-collector-cli/evidence/20261109T112401Z-integration.json, .agents/skills/verify-collector-cli/evidence/20261109T112402Z-worker.json, .agents/skills/verify-collector-cli/evidence/20261109T112436Z-integration.json, .agents/skills/verify-collector-cli/evidence/README.md, .agents/skills/verify-collector-cli/scripts/drive.py, .cache/npm/_logs/2026-11-09T11_21_42_706Z-debug-0.log, .fixture/events.jsonl, .git/index`; removed files `none`; validation command present: `requires review`. Workflow cost: 205.047 seconds and 26 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the `maintain-verification-skill` skill, without invented acceptance.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-5-round2-pre-claude/baseline/artifacts/`.
