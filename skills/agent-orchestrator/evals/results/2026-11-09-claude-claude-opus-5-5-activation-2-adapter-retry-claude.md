# agent-orchestrator: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `f9c2a7c444908e3c42830e844e3a504c3dbca24e`, actual bytes SHA-256 `a097ef64bd1371905586cf9a3ffe9c093f377046497666f8e5ca76da6f3e5aac`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `3e52212eb142aa854b2e04a3f47dc543db466740a02c838dcd9d6af9131a0b13`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Coordinate full-stop preparation and then review this session workflow.
Existing run record: run/PLAN.md. The scoped session is history/session-target.jsonl; no extra workers may be launched.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 37 | 0 |
| baseline | false | false | 14 | 0 |

Treatment: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T10_17_21_907Z-debug-0.log, .fixture/check-output.txt, .fixture/events.jsonl, .fixture/remote.git/objects/1f/23828c0134e961348f2456bde3c136b898b07f, .fixture/remote.git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .fixture/remote.git/objects/d7/e8e178abdc4a9836165a66685817fa9c43ecaf, .fixture/remote.git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .fixture/remote.git/refs/heads/feature, .fixture/state.json, .git/COMMIT_EDITMSG, .git/index, .git/objects/1f/23828c0134e961348f2456bde3c136b898b07f, .git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .git/objects/d7/e8e178abdc4a9836165a66685817fa9c43ecaf, .git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .git/refs/heads/feature, .git/refs/remotes/origin/HEAD, .git/refs/remotes/origin/feature, run/DECISIONS.md, run/LOG.md, run/PLAN.md, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/__pycache__/queue.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 311.244 seconds and 37 tool calls; token usage is in the JSON record.

Baseline: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T10_22_33_180Z-debug-0.log, .fixture/events.jsonl, .git/index, run/DECISIONS.md, run/LOG.md, run/PLAN.md, run/session-review.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 159.574 seconds and 14 tool calls; token usage is in the JSON record.


Expected deliverable: Expect prepare-only no-merge through helpers, root-only authorized waiting, and retro in the same record and budget.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-adapter-retry-claude/baseline/artifacts/`.
