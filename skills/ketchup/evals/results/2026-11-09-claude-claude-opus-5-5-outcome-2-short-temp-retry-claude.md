# ketchup: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `3857041fad3d36252578c8c68143a95a2f550159`, actual bytes SHA-256 `8add78dd29059f38b0a06b88d3444b640b0080dcb7eba3aad9e9b87990969bb3`; dirty: `False`.
- **Fixture.** `outcome-2`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/ketchup There are twelve separate pending product choices, including two PRs sharing one approval decision.

Supplied task context:
Use only history/current-chat.jsonl, history/index.json and docs/choices.json for this fixture; today is 2026-11-09 Asia/Jakarta. Status inspection is read-only; no CI rerun, watcher, push, merge or new helper.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 6 | 0 |
| baseline | n/a | false | 2 | 0 |

Treatment: 73 response lines; changed files `.cache/npm/_logs/2026-11-09T05_45_00_303Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 148.811 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 37 response lines; changed files `.fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 57.138 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: "There are twelve separate pending product choices, including two PRs sharing one approval decision." Expect: each item remains understandable with recommendation, evidence, risk, options and prerequisites, without dropping items for a word limit.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: partial; treatment criterion: partial.

Both retain all12 choice entries, group only the shared1/2 decision, and give common options/recommendation/risk without a word-limit cut. Treatment adds per-item links, live PR42 status and explicit unknown prerequisites. The concrete fixture says use only three files while also permitting read-only status inspection; baseline treats that cap strictly and treatment queries the offline forge. This input-scope ambiguity prevents clean boundary/method credit and is a follow-up candidate.
