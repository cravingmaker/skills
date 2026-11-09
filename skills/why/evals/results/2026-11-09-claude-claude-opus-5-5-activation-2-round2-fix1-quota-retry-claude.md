# why: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `afffb8170f4b21e1d54f2c2086a6617c81f6463a`, actual bytes SHA-256 `ef2f7537a0b8b6081f418609391fa5a3a928afe9a83f5f52e74e0ac8dab868ca`; dirty: `True`.
- **Fixture.** `activation-2`, SHA-256 `a2c1df86b6a5774b313063cfecbb17600cf1545fb97fb4e1202d5b14b1817dc1`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Was this guard added after an incident, or is that only an assumption?

Task context supplied to both arms:
Target MAX_RETRIES=3 in src/retry.py; compare history/incident-8.md. No Git history or remote PR access.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 5 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T14_54_06_039Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 31.003 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 7 response lines; changed files `.cache/npm/_logs/2026-11-09T14_54_37_151Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 16.046 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: relevant code/history/incident evidence only, exact locators, and contradictions or gaps preserved.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix1-quota-retry-claude/baseline/artifacts/`.
