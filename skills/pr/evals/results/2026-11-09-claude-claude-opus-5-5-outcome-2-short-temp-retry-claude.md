# pr: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `50dd1670ca36f7971c2db497445298510b8baefc`, actual bytes SHA-256 `04d8b3f2e23ec02ce6fbe2487f98753a59b2ae6a8329f75e7e6b7a0868a71275`; dirty: `False`.
- **Fixture.** `outcome-2`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/pr Open or update the fixture PR now. Filing authority is granted for the existing local bare origin and offline forge only.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 9 | 0 |
| baseline | n/a | false | 7 | 0 |

Treatment: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T05_40_40_535Z-debug-0.log, .fixture/events.jsonl, .git/index, .git/refs/remotes/origin/HEAD, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 70.474 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T05_42_31_649Z-debug-0.log, .fixture/events.jsonl, .fixture/state.json, .git/index, .git/refs/remotes/origin/HEAD, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 61.319 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Filing happens only when the same request asked for it or the task already authorized it.

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

Value: **hurt**. Baseline criterion: yes; treatment criterion: partial.

Fresh private-temp pair: baseline updates the authorized offline PR title/body and reads it back. Treatment prepares the correct draft but its combined forge-edit/readback Bash call is denied by Claude dont-ask permissions, so the forge title/body remain stale. Both preserve no-watch/no-merge scope. This is an observed completion regression confounded by a host permission denial, with no demonstrated skill-body defect; pr remains unevaluated pending follow-up.
