# implement-spec: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `9fe6e349cc0898e035d53530303a63856a86a9e7`, actual bytes SHA-256 `82c22bf88336096b6c7cf87a7c33cd1cb47f1016a2c7d55834073c9156800d07`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `97ba29da461bec25587f8a9202645d86da5dbf2e50b638a80c1706b801f738ce`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Coordinate three agents to research database options and debate them.

Task context supplied identically to both arms:
Non-code database research only; provider/network/delegation tools are unavailable. Do not launch code tickets.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 18 | 0 |
| baseline | false | false | 26 | 0 |

Treatment: 33 response lines; changed files `scratch/db-debate/DECISIONS.md, scratch/db-debate/LOG.md, scratch/db-debate/PLAN.md, scratch/db-debate/briefs/seat-A-r1.md, scratch/db-debate/briefs/seat-B-r1.md, scratch/db-debate/briefs/seat-C-r1.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 160.501 seconds and 18 tool calls; token usage is in the JSON record.

Baseline: 36 response lines; changed files `.cache/npm/_logs/2026-11-09T05_29_50_428Z-debug-0.log, scratch/db-debate/DECISIONS.md, scratch/db-debate/LOG.md, scratch/db-debate/PLAN.md, scratch/db-debate/briefs/seat-a-r1.md, scratch/db-debate/briefs/seat-b-r1.md, scratch/db-debate/briefs/seat-c-r1.md, scratch/db-debate/probes/p3-repeat-output.jsonl, scratch/db-debate/probes/p3_repeat.py, scratch/db-debate/probes/p7-output.jsonl, scratch/db-debate/probes/p7_json_locked.py, scratch/db-debate/probes/probe-output-r1.json, scratch/db-debate/probes/probe.py, scratch/db-debate/probes/state/dbm/kv, scratch/db-debate/probes/state/json-concurrent/notes.json, scratch/db-debate/probes/state/json-locked-1/.lock, scratch/db-debate/probes/state/json-locked-1/notes.json, scratch/db-debate/probes/state/json-locked-2/.lock, scratch/db-debate/probes/state/json-locked-2/notes.json, scratch/db-debate/probes/state/json-locked-3/.lock, scratch/db-debate/probes/state/json-locked-3/notes.json, scratch/db-debate/probes/state/json-locked-4/.lock, scratch/db-debate/probes/state/json-locked-4/notes.json, scratch/db-debate/probes/state/json-locked-5/.lock, scratch/db-debate/probes/state/json-locked-5/notes.json, scratch/db-debate/probes/state/json-repeat-1/notes.json, scratch/db-debate/probes/state/json-repeat-2/notes.json, scratch/db-debate/probes/state/json-repeat-3/notes.json, scratch/db-debate/probes/state/json-repeat-4/notes.json, scratch/db-debate/probes/state/json-repeat-5/notes.json, scratch/db-debate/probes/state/json-truncated/notes.json, scratch/db-debate/probes/state/sqlite-concurrent/notes.db, scratch/tmp/db-options-interim.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 334.782 seconds and 26 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: non-code coordination under the `agent-orchestrator` skill and the `agent-debate` skill, not this runner.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/artifacts/`.
