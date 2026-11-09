# why: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `afffb8170f4b21e1d54f2c2086a6617c81f6463a`, actual bytes SHA-256 `ef2f7537a0b8b6081f418609391fa5a3a928afe9a83f5f52e74e0ac8dab868ca`; dirty: `True`.
- **Fixture.** `outcome-1`, SHA-256 `408821b5ca890b21a095c982c7c666c0f38f3803a55b30813f69081b1e14e028`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
The checkout has no Git metadata or archived history. The introducing PR is inaccessible and no history tool is exposed. Explain why src/worker.py caps batches at 100; the record cannot supply author intent.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 8 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T14_51_02_034Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 45.653 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 26 response lines; changed files `.cache/npm/_logs/2026-11-09T14_51_47_234Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 20.771 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: "The checkout has no git history, and the original PR is inaccessible." Check: unavailable history is named; no invented commit, rationale, or claim of absence.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: yes. Treatment: yes. Value: matched.

Both distinguish the present100-item mechanism from unavailable author intent, disclose missing Git/PR/history and label possible causes as guesses. No invented introducing commit, actual rationale or global claim that no rationale exists. No product edits.
