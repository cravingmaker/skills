# agent-orchestrator: claude near-miss-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-4` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `f9c2a7c444908e3c42830e844e3a504c3dbca24e`, actual bytes SHA-256 `a097ef64bd1371905586cf9a3ffe9c093f377046497666f8e5ca76da6f3e5aac`; dirty: `False`.
- **Fixture.** `near-miss-4`, SHA-256 `97ba29da461bec25587f8a9202645d86da5dbf2e50b638a80c1706b801f738ce`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Explain the difference between a subagent and a skill.

Task context supplied identically to both arms:
Explain the difference between a subagent and a skill.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 0 | 0 |
| baseline | false | false | 0 | 0 |

Treatment: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T03_43_02_729Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 13.528 seconds and 0 tool calls; token usage is in the JSON record.

Baseline: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T03_43_15_608Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 12.454 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a direct explanation; nothing is dispatched.

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
