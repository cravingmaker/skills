# setup-agent-skills: claude activation-4

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `734f2745f73f6eaa05e54519a92bec84358234eb`, actual bytes SHA-256 `124ab76b9bbe51a2ae051c0c4680a13419b8c816e87e9fec1be9df5265bb766a`; dirty: `False`.
- **Fixture.** `activation-4`, SHA-256 `e4f5e820dd859f3c212b6bf67bdd2f6770f3f9732d5e15dac8aba8b485465a2b`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [setup-agent-skills.tar.gz](https://drive.google.com/file/d/1pUpGJxKajtFwlD5HpOyZfbNpuEBYYXEw/view), folder `2026-11-09-claude-claude-opus-5-5-activation-4-claude/` inside.

## Prompt

```text
/setup-agent-skills

Use the `setup-agent-skills` skill explicitly for this request.

Set up this repo with GitHub Issues. Use the connected GitHub tool; no CLI is installed.

Task context supplied to both arms:
The selected project instruction target is PROJECT-INSTRUCTIONS.md, an ordinary fixture substitute for the live host instruction file. Do not alter the harness AGENTS.md. Existing domain paths and GitLab identity are authoritative. No remote writes. Connected GitHub tools are unavailable under the harness. Record that exact access limit; do not substitute a CLI.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 12 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 31 response lines; changed files `.cache/npm/_logs/2026-11-09T04_51_29_694Z-debug-0.log, PROJECT-INSTRUCTIONS.md, docs/agents/issue-tracker.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 52.281 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T04_52_21_975Z-debug-0.log, docs/agents/issue-tracker.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 31.657 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: supported connected reads suffice, and no CLI, model sheet, startup hook, or upstream cache is installed.

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

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
