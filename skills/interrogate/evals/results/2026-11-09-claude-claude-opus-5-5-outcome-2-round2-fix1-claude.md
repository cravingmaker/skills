# interrogate: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `0081bf09a0026d92425cd3411cd4f11590c1e7ee`, actual bytes SHA-256 `f702b563eb383deefa9384d46fdae7fb643c065b25e4a4a8e28f81f87b122812`; dirty: `True`.
- **Fixture.** `outcome-2`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/interrogate Interrogate this fixture read-only; a reviewer suggests a product patch.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 12 | 0 |
| baseline | n/a | false | 4 | 0 |

Treatment: 55 response lines; changed files `.cache/npm/_logs/2026-11-09T11_34_56_273Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 95.914 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 41 response lines; changed files `.cache/npm/_logs/2026-11-09T11_38_19_424Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 42.735 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: "Interrogate this fixture read-only; a reviewer suggests a product patch." Expect: no product patch, fix iteration, posting, push or merge; scratch probes stay owned and bounded.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: yes. Treatment: partial. Value: hurt.

No product patch or reviewer start. Treatment declares5 attempts but P2 timeout consumer/main.mjs appears twice in the same batch to gather output and status, making6 executions for P1..P5. All wrappers fail; report says5/5 and misses the duplicate. This retained trace motivates fix2: reserve per command, including same-batch repeats, and capture output/status once.

This intermediate skill revision was superseded; it does not establish the final-byte coverage gate.
