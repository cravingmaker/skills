# implement-spec: claude outcome-1

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `9fe6e349cc0898e035d53530303a63856a86a9e7`, actual bytes SHA-256 `82c22bf88336096b6c7cf87a7c33cd1cb47f1016a2c7d55834073c9156800d07`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `97ba29da461bec25587f8a9202645d86da5dbf2e50b638a80c1706b801f738ce`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/implement-spec

Implement the approved spec docs/specs/sync.md and its five tickets.

Task context supplied identically to both arms:
Use configured nondefault tracker paths in docs/agents/issue-tracker.md and existing run/. This host cannot dispatch workers or create Git checkouts; preserve blocked execution honestly and produce only in-scope preflight/record evidence. No commits or new controller.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.

Supplied task context:
The current authoritative run is run/PLAN.md; retain its spent budget. No worker, provider, extra model session, Git checkout or independent panel is available. Only preflight and checkpointing are authorized; no product or tracker closure. The user concurrency ceiling is two.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | unavailable | unavailable | 143 |
| baseline | n/a | unavailable | unavailable | not run |


Expected deliverable: One coordinator owns every worker, reviewer, replacement and retry start; live subagents never exceed eight or the lower host or user limit, and totals stay within the recorded budget.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json).

## Invalid comparison

- claude treatment failed (exit 143, timeout False); inspect stderr and trace

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
