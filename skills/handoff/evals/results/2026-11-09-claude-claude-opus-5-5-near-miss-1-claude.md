# handoff: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `02b9d2fe295ee8d583403fa3d796c93e622822c8`, actual bytes SHA-256 `7a627b2814d77e06bea1ff0c353cb00cef26839cad04c51d1d8b5b0b69aed3a7`; dirty: `False`.
- **Fixture.** `near-miss-1`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Continue the known run at this checkpoint.
The known checkpoint is run/PLAN.md; all ten questions are in run/questions.md.
Authoritative continuation inputs are run/PLAN.md, run/questions.md, docs/task.md and docs/handoff-context.md.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 10 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 21 response lines; changed files `.cache/npm/_logs/2026-11-09T10_08_20_325Z-debug-0.log, .fixture/events.jsonl, .git/index, run/DECISIONS.md, run/LOG.md, run/PLAN.md, run/evidence/lint-da5b9f5.txt, run/evidence/unittest-da5b9f5.txt, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 98.103 seconds and 10 tool calls; token usage is in the JSON record.

Baseline: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T10_09_58_760Z-debug-0.log, .fixture/events.jsonl, .git/index, run/DECISIONS.md, run/LOG.md, run/PLAN.md, run/raw/c2-pager-proof.md, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 60.597 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: decision-log reconciliation, without replacing its authoritative state with a handoff summary.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/artifacts/`.
