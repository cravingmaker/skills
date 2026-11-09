# wizard: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `15559f705666b52d92b17093c2948016f670d20e`, actual bytes SHA-256 `cf752a967fd312374401a921bf6a11ed58082a606198d9442104f3c3ab8a6d87`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `90eb9afcdc30a4ee9c44cc262ba377ced34d824fbfe958a21927e9eb86a033db`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Make a setup script that walks me through getting Stripe keys into .env and GitHub secrets.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 12 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 22 response lines; changed files `.cache/npm/_logs/2026-11-09T05_42_04_738Z-debug-0.log, scratch/.env, scripts/setup-stripe.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 137.53 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 26 response lines; changed files `scripts/setup-stripe.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 146.522 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: reads .env.example and the workflows, finds the env loader, confirms the stages, copies the template, authors stages, and round-trips dummy values through the project's loader.

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
