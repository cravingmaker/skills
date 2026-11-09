# babysit-pr: claude activation-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `3332374526e0f239865e83dc34b763e14402e409`, actual bytes SHA-256 `1fd029e5d1986b10900275e221e265ec18ec04872ea46693a3a8a1b817d43062`; dirty: `False`.
- **Fixture.** `activation-4`, SHA-256 `8ae328a90612a6d4a075365a113f638a3e53dd2a29562b23ac288c3ccf5c096b`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Full send was explicitly authorized for this fixture PR; its merge is still pending. Continue that pending delivery.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 13 | 0 |
| baseline | false | false | 9 | 0 |

Treatment: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T11_21_56_780Z-debug-0.log, .fixture/check-output.txt, .fixture/events.jsonl, .fixture/state.json, .git/refs/remotes/origin/HEAD, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 93.861 seconds and 13 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T11_24_38_508Z-debug-0.log, .fixture/events.jsonl, .fixture/state.json, .git/index, .git/refs/remotes/origin/HEAD, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 69.658 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the root keeps watching because an authorized action is pending, and unwatches before any handoff or question.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-round2-confirm-claude/baseline/artifacts/`.
