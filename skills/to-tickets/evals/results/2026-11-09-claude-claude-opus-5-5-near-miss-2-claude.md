# to-tickets: claude near-miss-2

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `53fcbe1f3ae919ea22005551d33abacb7444ae55`, actual bytes SHA-256 `c2c9142422c2683ce739a32d14977452722ef88981b15a86793613fcc5911dab`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `1aaff2b0e4a28127b049de33231732b9e84968bb2e7fb462bed73c674362a037`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Plan how three agents should build these approved tickets.

Task context supplied to both arms:
Tickets in .planning/work-items/search/ are already approved and stable; use docs/specs/saved-searches.md. Plan only, no dispatch; shared start allowance 4, concurrency 2, reserve 1 for integration.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 13 | 0 |
| baseline | false | unavailable | unavailable | not run |

Treatment: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T03_35_24_065Z-debug-0.log, .planning/runs/saved-searches-01/BUDGET.md, .planning/runs/saved-searches-01/DECISIONS.md, .planning/runs/saved-searches-01/LOG.md, .planning/runs/saved-searches-01/PLAN.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 124.52 seconds and 13 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the `work-decomposition` skill imports the tickets; no new tickets are written.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json).

## Invalid comparison

- Shared budget limit reached

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
