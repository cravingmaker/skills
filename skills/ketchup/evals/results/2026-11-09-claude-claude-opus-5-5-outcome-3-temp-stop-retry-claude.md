# ketchup: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `3857041fad3d36252578c8c68143a95a2f550159`, actual bytes SHA-256 `8add78dd29059f38b0a06b88d3444b640b0080dcb7eba3aad9e9b87990969bb3`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `416013b08efd2e88b733de820be14236968c96f429684f24561197a4b33a470d`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [ketchup.tar.gz](https://drive.google.com/file/d/1J_ap53vEN9if1shTpcE-Adf79FZ1ZqXt/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/` inside.

## Prompt

```text
/ketchup The agent has authority to finish testing, but needs one actual product choice from me.

Supplied task context:
Use only history/current-chat.jsonl, history/index.json and docs/choices.json for this fixture; today is 2026-11-09 Asia/Jakarta. Status inspection is read-only; no CI rerun, watcher, push, merge or new helper. Testing remains authorized agent work; auth-choice is the only product choice.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 2 | 0 |
| baseline | n/a | false | 1 | 0 |

Treatment: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T05_50_15_087Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 35.899 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T05_52_32_888Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 24.883 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: "The agent has authority to finish testing, but needs one actual product choice from me." Expect: agent work is separate and only the unresolved product choice is presented as user-owned.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-temp-stop-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both keep already-authorized current-head testing in agent work and present only auth-choice as the actual user product decision, with immediate-denial/TTL options and the stale-authorization risk. Both flag stale12-choice/retention metadata rather than invent additional current choices; no tests, watchers or mutations start in this read-only catch-up.
