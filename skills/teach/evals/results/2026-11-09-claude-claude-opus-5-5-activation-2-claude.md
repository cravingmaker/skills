# teach: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `8ded45db77efd9d9e0b01ab9d488327ad05a7e8a`, actual bytes SHA-256 `91f4c844035d2a9df43ca0a8ce47f8479c1d36cf75c3a39c7c5f003e2debd857`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/teach
Create a durable learning workspace here for my networking lessons; save progress across sessions.
The subsystem source is src/queue.py and docs/queue.md. Networking workspace destination is learning/; existing GLOSSARY.md remains project-owned.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 18 | 0 |
| baseline | false | false | 9 | 0 |

Treatment: 36 response lines; changed files `.cache/npm/_logs/2026-11-09T10_11_27_734Z-debug-0.log, .fixture/events.jsonl, .git/index, learning/MISSION.md, learning/RESOURCES.md, learning/lessons/0001-work-queue-as-a-buffer.html, learning/reference/GLOSSARY.md, src/__pycache__/queue.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 163.387 seconds and 18 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `.cache/npm/_logs/2026-11-09T10_14_11_374Z-debug-0.log, .fixture/events.jsonl, .git/index, learning/PROGRESS.md, learning/README.md, learning/lessons/01-queue-as-buffer.md, learning/terms.md, src/__pycache__/queue.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 71.882 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: explicit workspace mode, mission and trusted resources, one scoped lesson, evidence-based learning records when warranted, and preserved existing files.

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
