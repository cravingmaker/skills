# why: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `afffb8170f4b21e1d54f2c2086a6617c81f6463a`, actual bytes SHA-256 `ef2f7537a0b8b6081f418609391fa5a3a928afe9a83f5f52e74e0ac8dab868ca`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `a2c1df86b6a5774b313063cfecbb17600cf1545fb97fb4e1202d5b14b1817dc1`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Why did we cap this batch at 100? Separate the documented reason from guesses.

Task context supplied to both arms:
Target MAX_BATCH=100 in src/retry.py. Available primary history is history/pr-17.md; fixture contains no Git metadata and remote PR access is unavailable.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 5 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T11_39_30_154Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 42.009 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 21 response lines; changed files `.cache/npm/_logs/2026-11-09T11_41_51_401Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 20.247 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a bounded history search and calibrated rationale, with current behavior kept distinct from intent.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/artifacts/`.
