# setup-agent-skills: claude activation-2

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `734f2745f73f6eaa05e54519a92bec84358234eb`, actual bytes SHA-256 `124ab76b9bbe51a2ae051c0c4680a13419b8c816e87e9fec1be9df5265bb766a`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `586374fe46e16d75da0244b9cfb7eddf8fe34eb84ed01729068caedebd62e2c0`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/setup-agent-skills

Use the `setup-agent-skills` skill explicitly for this request.

Configure local Markdown tickets for this repo; triage is installed and our ready label is bot-ready.

Task context supplied to both arms:
The selected project instruction target is PROJECT-INSTRUCTIONS.md, an ordinary fixture substitute for the live host instruction file. Do not alter the harness AGENTS.md. Existing domain paths and GitLab identity are authoritative. No remote writes. Use local Markdown at .planning/team-tickets/; triage is installed, ready label bot-ready.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T04_51_16_876Z-debug-0.log, PROJECT-INSTRUCTIONS.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 40.619 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T04_51_57_160Z-debug-0.log, PROJECT-INSTRUCTIONS.md, docs/agents/issue-tracker.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 42.157 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: local tracker seed is adapted to the configured ticket root, the role mapping keeps `bot-ready`, and no remote labels or issues are created.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
