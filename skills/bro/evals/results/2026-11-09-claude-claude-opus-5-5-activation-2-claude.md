# bro: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `20aa7feebf75db7c9ad6765c371f6cb456f1fc87`, actual bytes SHA-256 `b88e494bfaa31f0babf7014a866715fac33e9d9ac5ed83ad1e569027df4bc663`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `b4a7e81156efb335f6897c42d7a367286264a2b79d5904b1c7f467d2a09b64a8`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/bro

Use the `bro` skill explicitly for this request.

Bro, make the last read-only council findings understandable.

Task context supplied to both arms:
Previous assistant answer (supplied verbatim as context): "cfg → validator, fail → exit 1, no write. The value is 0.50%, amount=1.2300, optional=null. Source: 'capture pending'. Unit tests passed; no UI was driven. The read-only council found a missing authorization check in src/order.py; static finding only. No fixes, PR filing, push, watch, merge, or helpers are authorized."
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 1 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 11 response lines; changed files `.cache/npm/_logs/2026-11-09T04_56_36_919Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 11.133 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 11 response lines; changed files `.cache/npm/_logs/2026-11-09T04_56_48_024Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 23.153 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: repair the wording of the findings; start no fix loop or remote action.

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
