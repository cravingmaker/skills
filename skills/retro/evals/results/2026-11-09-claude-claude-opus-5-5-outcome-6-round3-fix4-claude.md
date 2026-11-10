# retro: claude outcome-6

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-6` in `evals/examples.md`.
- **Skill revision.** Commit `e85790be565e2de21ee2ea7df6abf8ea385454e0`, tree `e96fda3e3d285b35cf382d8e88343ec8cf887173`, actual bytes SHA-256 `487306e29b693efee09f20313eee4384da506c690d7cb009e5445b6363046eb7`; dirty: `True`.
- **Fixture.** `outcome-6`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [retro.tar.gz](https://drive.google.com/file/d/1fuZeOlMvToGWFavSPGMb9rRp57N9rE7Q/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/` inside.

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
| treatment | n/a | true | 6 | 0 |
| baseline | n/a | false | 5 | 0 |

Treatment: 35 response lines; changed files `.cache/npm/_logs/2026-11-09T16_01_43_634Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 45.444 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 40 response lines; changed files `.cache/npm/_logs/2026-11-09T16_02_29_315Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 44.764 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: "Several reviewers repeat a lesson already stated clearly in the used skill." Expect: inspect the destination, distinguish execution from missing guidance, and reject a duplicate rule without treating agreement as proof.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-round3-fix4-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 3 review

Baseline: partial. Treatment: yes. Value: added.

Both inspect the current destination and reject duplicate numeric-spelling guidance. Treatment reads only named index/session and installed method/destination material, leaves unnamed reviewer/incident inputs and historical skill loading unknown, and makes no edits. Baseline additionally reads README, directory inventories and Git history, and searches the whole workspace before disclaiming its use.

Source boundary: pass. Inspected every treatment tool call (trace lines 9, 10, 11, 20, 22, 33); no treatment commit-log, blame, or prior-revision diff request occurred.
