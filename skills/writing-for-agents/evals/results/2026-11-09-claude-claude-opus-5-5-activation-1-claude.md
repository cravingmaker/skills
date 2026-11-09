# writing-for-agents: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `b5f8a48fd2dd1a5df15eb4bcf5227909ffabc4bb`, actual bytes SHA-256 `050cda173069769d2b06dc3e520d9c435aaa5129a84858ccc7dc03402b98e331`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `408fbda0ac6d3293f09ef47ddb534169865f8bdad52ed4af2b6c15885ddbd265`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Rewrite this SKILL.md so the agent follows the right branch and knows when it is done.
The target is drafts/sample/SKILL.md; local authoring rules are in docs/authoring-guide.md.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 11 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T10_09_14_857Z-debug-0.log, .fixture/events.jsonl, .git/index, drafts/sample/SKILL.md, drafts/sample/evals/examples.md, drafts/sample/references/detail.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 84.386 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T10_10_39_691Z-debug-0.log, .fixture/events.jsonl, .git/index, drafts/sample/SKILL.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 45.199 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: precise context pointers, progressive disclosure, positive steps, checkable completion, and local authoring/provenance rules.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
