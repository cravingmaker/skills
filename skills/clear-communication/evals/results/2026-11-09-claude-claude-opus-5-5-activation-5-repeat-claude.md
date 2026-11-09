# clear-communication: claude activation-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-5` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `3c1d6e767164d88cf2ea77ef9eb49d73e360bb7c`, actual bytes SHA-256 `0c1fe416999946256a92676611e65579c74ee68e42fb95e2a4dbf38a2ebfa4b2`; dirty: `False`.
- **Fixture.** `activation-5`, SHA-256 `16e92b82377241283f122410704bcd7ca07063d4c00646e5e14385c83ced60a6`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Wait-what. Explain the last point using our settlement terms.

Task context supplied to both arms:
Previous assistant answer: "cfg → validator, fail → exit 1, no write. Settlement transfers captured funds; capture alone is not settlement. Unit tests passed; no UI was driven. amount=1.2300, optional=null, rate=0.50%. Source quotation: 'capture pending'. Draft only, no filing, pushes, watches, merges, repairs, or helpers."
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 2 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T03_22_40_826Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 32.15 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T03_24_31_795Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 21.095 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: add only the needed project context and explain useful terms; no course, mandatory standard, or new files.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-5-repeat-claude/baseline/artifacts/`.
