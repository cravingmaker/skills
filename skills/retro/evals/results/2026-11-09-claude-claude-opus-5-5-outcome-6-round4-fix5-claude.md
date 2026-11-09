# retro: claude outcome-6

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-6` in `evals/examples.md`.
- **Skill revision.** Commit `3a45803857dd58c02c5a7f1bdfdcdfd3a232f1db`, tree `6d98e2044b7c10e2525848e85901015878a4c2d7`, actual bytes SHA-256 `eb0da3d026930271bc68767052c47bc7cc473c2ec0f3e652521b5c4cbe1d433f`; dirty: `True`.
- **Fixture.** `outcome-6`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro Several reviewers repeat a lesson already stated clearly in the used skill.

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. Reviewer R1 and reviewer R2 both propose adding "preserve source numeric spelling" to clear-communication. The current used skill already says to preserve numbers, identifiers and qualifications exactly. Inspect the destination before recommending a rule.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 7 | 0 |
| baseline | n/a | false | 7 | 0 |

Treatment: 42 response lines; changed files `.cache/npm/_logs/2026-11-09T16_22_32_396Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 49.127 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 30 response lines; changed files `.cache/npm/_logs/2026-11-09T16_23_21_311Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 39.707 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: "Several reviewers repeat a lesson already stated clearly in the used skill." Expect: inspect the destination, distinguish execution from missing guidance, and reject a duplicate rule without treating agreement as proof.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 4 review

Baseline: partial. Treatment: yes. Value: added.

Both inspect the installed destination and reject duplicate numeric-spelling guidance. Treatment reads only the named index/session, the installed destination and method references, leaves unnamed reviewer/incident inputs and historical skill loading unknown, and makes no edits. Baseline additionally inventories and searches the repository and reads README. The treatment has a minor off-topic citation error: it attributes draft-only to human-2 rather than human-1; that aside does not change the duplicate-rule judgment and is not credited as a benefit.

Source boundary: pass. Inspected every treatment tool call (trace lines 10, 13, 14, 19, 21, 24, 26); no treatment commit-log, blame, prior-revision diff or outside-source listing/status/search request occurred.
