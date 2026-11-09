# full-send: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `484196e75bb76b60eb18ff64f7e4b0c3d33a4e1e`, actual bytes SHA-256 `80ae4ecb34360151758bccbfdd576fca17074a74c90090bb3829293ebef43b74`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `599847a7fac2056b23fd201b4d6efd7bcb1850a4c50f5ecc611bb58ee12ea147`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/full-send
Full send this, I'm heading out.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 14 | 0 |
| baseline | false | false | 20 | 0 |

Treatment: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T10_01_12_861Z-debug-0.log, .fixture/events.jsonl, .git/index, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 106.945 seconds and 14 tool calls; token usage is in the JSON record.

Baseline: 21 response lines; changed files `.cache/npm/_logs/2026-11-09T10_02_59_542Z-debug-0.log, .fixture/check-output.txt, .fixture/checkout/.git, .fixture/checkout/.github/CODEOWNERS, .fixture/checkout/.github/PULL_REQUEST_TEMPLATE.md, .fixture/checkout/.gitignore, .fixture/checkout/AGENTS.example.md, .fixture/checkout/CLAUDE.md, .fixture/checkout/CONTRIBUTING.md, .fixture/checkout/GLOSSARY.md, .fixture/checkout/README.md, .fixture/checkout/docs/authoring-guide.md, .fixture/checkout/docs/change.md, .fixture/checkout/docs/choices.json, .fixture/checkout/docs/handoff-context.md, .fixture/checkout/docs/inherited-thread.md, .fixture/checkout/docs/merged-prs.md, .fixture/checkout/docs/queue.md, .fixture/checkout/docs/task.md, .fixture/checkout/docs/tickets.json, .fixture/checkout/drafts/sample/SKILL.md, .fixture/checkout/drafts/sample/evals/examples.md, .fixture/checkout/drafts/sample/references/detail.md, .fixture/checkout/heading.md, .fixture/checkout/history/README.md, .fixture/checkout/history/conventions.md, .fixture/checkout/history/current-chat.jsonl, .fixture/checkout/history/index.json, .fixture/checkout/history/session-child.jsonl, .fixture/checkout/history/session-target.jsonl, .fixture/checkout/history/session-unrelated.jsonl, .fixture/checkout/learning/notes.md, .fixture/checkout/notes.md, .fixture/checkout/package-lock.json, .fixture/checkout/package.json, .fixture/checkout/run/DECISIONS.md, .fixture/checkout/run/LOG.md, .fixture/checkout/run/PLAN.md, .fixture/checkout/run/host-receipts.json, .fixture/checkout/run/questions.md, .fixture/checkout/run/raw/a.md, .fixture/checkout/setup.json, .fixture/checkout/src/__pycache__/cache.cpython-315.pyc, .fixture/checkout/src/__pycache__/pager.cpython-315.pyc, .fixture/checkout/src/cache.py, .fixture/checkout/src/pager.py, .fixture/checkout/src/queue.py, .fixture/checkout/tests/__pycache__/test_pager.cpython-315.pyc, .fixture/checkout/tests/test_pager.py, .fixture/checkout/tools/check-draft.py, .fixture/checkout/tools/forge.py, .fixture/checkout/tools/gh, .fixture/checkout/tools/git, .fixture/checkout/tools/lint.py, .fixture/events.jsonl, .fixture/remote.git/objects/16/a87f8cadd49893c57a0acba861a8c4aeaee1cf, .fixture/remote.git/objects/bc/4d8b7268ff01f5ac63afe69e3c935d2f6a7fb7, .fixture/remote.git/objects/e1/8f8d33a4496a82a685cd59e0c2c292ff2e8e81, .fixture/remote.git/objects/f8/0a9ffcc36de75c0d131190384078e9f886c4d6, .fixture/remote.git/objects/fb/b7886015b14c0cc6c85561c986a3669af016a9, .fixture/remote.git/refs/heads/feature, .fixture/state.json, .git/index, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 154.003 seconds and 20 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the same flow, with sensible defaults decided and listed, and questions asked only through the harness's question tool.

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
