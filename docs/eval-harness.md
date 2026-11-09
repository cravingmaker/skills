# Paired skill evaluations

Use `scripts/eval-skill.py` to compare one example with the candidate skill available and unavailable. Each arm starts a fresh headless host session in its own restored fixture and temporary home. A valid comparison can show that a skill failed its expectation; validity measures isolation and completion.

The script needs `uv`, Python 3.12 or newer, and the selected host CLI. Its inline dependency is pinned to `pyyaml==6.0.3`. The fixture tests need no host CLI, credentials, or model calls.

## Run an example

Example identifiers follow their section and position in `evals/examples.md`: `activation-1`, `activation-2`, `near-miss-1`, and so on. The parser accepts the repository's straight-quoted example prompts.

```sh
scripts/eval-skill.py --skill clear-communication --host claude \
  --example near-miss-1 --fixture tests/eval-harness/fixtures/package --dry-run

scripts/eval-skill.py --skill clear-communication --host codex \
  --example activation-1 --fixture tests/eval-harness/fixtures/package
```

Pass `--model NAME` to choose the model; otherwise the host chooses its default. The harness records the effective model and rejects a pair whose models differ. Pass `--binary PATH` for a particular host executable and `--timeout SECONDS` to change the 300-second limit per arm. Each invocation runs two model sessions serially. The caller must account for other running agents and its total model-run budget.

For an example with placeholder input, write the concrete prompt to a file and pass `--prompt-file FILE`. The record keeps both the source example and the actual prompt. Use `--record-id activation-1-trial-2` for another trial; existing records are never overwritten.

Required skills are installed in both arms through the candidate's transitive `metadata.requires` closure. A missing dependency stops the comparison before either model call. Pass `--dependency DIR` for each required skill maintained outside this repository. Optional prose routes are unavailable unless the fixture provides them identically to both arms.

## Prepare a fixture

Use a small directory containing the task's inputs and real commands. Host instruction files are supplied by the harness; put task context in `README.md`. The harness rejects symlinks, special files, Git metadata, credential filenames, existing host instruction files (including `AGENTS.override.md`), and custom host configuration. It supports project skill folders under `.claude/skills` and `.agents/skills`, including nested folders.

Every project copy whose frontmatter names the candidate is excluded from both restored fixtures, regardless of its folder name. The treatment receives one copy of the candidate in its temporary user skill folder. The record lists the excluded paths and hashes. Other project skills and declared dependencies stay identical. The source fixture and the user's installed skill folders are never modified.

The standing communication contract is the fenced Markdown block in `skills/clear-communication/references/house-style.md`. Both arms receive exactly that block and the same workspace guard in `CLAUDE.md` or `AGENTS.md`.

The harness snapshots fixture bytes before creating either arm. It checks file hashes and executable bits, rejects shared file inodes, writes a sentinel in arm 1 and proves it is absent in arm 2, then removes the sentinel. Immediately before each model call it checks that arm's input and the pristine snapshot again. An overwrite or new file in the first workspace cannot reach the second workspace through shared files.

## Discovery and authentication

Both adapters start from an environment allowlist. They set the child process's home, host configuration directory, cache directory, and temporary directory to private paths. Inherited provider settings, session identifiers, shell startup hooks, and plugin settings are excluded. The temporary homes are deleted on success and failure. Authentication files have mode `0600` and are never included in artifacts or logs. Known credential token values are checked in arm files, shared record fields, and the rendered public Markdown before evidence is exported; evidence containing them is withheld.

### Claude Code

The adapter uses `CLAUDE_CONFIG_DIR` and `--setting-sources user`, with a generated settings file, empty strict MCP configuration, no Chrome integration, and no session persistence. Personal and project settings, plugin installations, auto memory, hooks, claude.ai synchronization, and connectors are excluded. Shell commands use Claude's sandbox with no allowed network domains. The allowed tool set is the same in both arms and excludes delegation and web tools.

An empty settings-source list also hides user skills in Claude Code 2.1.311. The adapter therefore enables the controlled temporary user source. Built-in plugins can remain present even with an empty plugin configuration; only entries marked `builtin` are accepted, and their inventories must match across arms. External plugins or MCP servers make the comparison invalid.

The adapter reads only the existing credential file, or on macOS captures the default Claude Code Keychain credential into memory and writes a temporary credential file. It copies no personal settings. An unsupported credential store stops the run and names the login command. `--bare` is unsuitable for the subscription-authentication path because it skips OAuth and Keychain authentication, as documented in the installed CLI help.

The `system.init` trace must advertise the candidate in treatment and omit it in baseline. A matching `Skill` tool call or a direct candidate `Read` is activation evidence. Mentioning the skill in an answer is insufficient. Non-candidate skills, tools, built-in plugins, and effective models must match across arms.

Claude documents [skill visibility settings](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings), [settings precedence](https://code.claude.com/docs/en/settings), and [environment controls](https://code.claude.com/docs/en/env-vars). Plugin skills need separate control because `skillOverrides` does not apply to them. The harness excludes project candidate copies instead of depending on that override.

### Codex

The adapter sets both the child process's home and `CODEX_HOME`. This controls `$HOME/.agents/skills` as well as `$CODEX_HOME/skills`. Fixtures are outside configured repositories; ancestor instruction, configuration, Git, and skill sources are rejected. Bundled system skills, plugins, remote plugin discovery, apps, hooks, memories, and delegation are disabled identically in both arms. The sandbox permits workspace writes and blocks command network access. Web search is disabled.

The adapter copies only `auth.json` into the temporary home and selects the file credential store. It calls the local app server's `skills/list` without creating a model turn and verifies enabled skill names and paths against the computed inventory. A mismatch rejects the comparison before either model call. CLI execution uses `codex exec --json --skip-git-repo-check --ignore-rules`; each run creates a new session.

Codex has no `Skill` tool in this trace format. Explicit host selection is activation evidence when a rollout message has native `skills.selected_skill_instructions` and `skills` provenance, the exact installed candidate path and name, and its complete matching body. The content item must be `input_text`, with equally sized content, kind and provenance arrays. User-authored or quoted `<skill>` tags, unknown provenance, mismatched paths and altered bodies do not count. The adapter also counts one successful, simple read command whose inputs are all absolute paths to installed skill files, include the candidate `SKILL.md` path, and whose output shows a candidate body line that none of the other inputs contains. Agents often read several skills in one `cat`, so several installed inputs are allowed. Relative input paths remain unclassified. The accepted readers are:

- `cat`, `more`, or `less` with no options.
- `head` or `tail` with no options, a `-N` count, or `-n N` or `-c N`.
- `sed` with one `p` program, optionally addressed by a line number, `$`, or a range of those, optionally preceded by `-n` and then `-e`.

A final `--` before the files is allowed, and a shell wrapper counts only in the exact form `sh -c 'command'` or `-lc`. Anything else remains unclassified and requires trace review: other options, text-generating programs, inputs outside the installed skills, redirections, compound commands (including `&&` chains and separate lines), and other read mechanisms. Their output does not establish that the body text came from the candidate. A failed command, a search result, or a prose claim does not count. The local session rollout records the effective model and is exported separately from the CLI trace.

OpenAI documents [skill locations and enablement](https://learn.chatgpt.com/docs/build-skills), [configuration controls](https://learn.chatgpt.com/docs/config-file/config-reference), and the [app server inventory API](https://learn.chatgpt.com/docs/app-server). These pages and the installed CLI help were checked on 2026-11-08. Fetched documentation informs the adapter; it is never added to an evaluated model's instructions.

### Unsupported managed sources

The harness rejects local machine policy directories and known macOS managed preference files. Claude MDM preferences are checked without printing their contents. It never edits machine policy. Runtime inventory checks also reject uncontrolled discovery. Server-enforced settings that do not appear in the host trace cannot be fully attested by this local harness; use a clean machine or container when that assurance is required.

## Read the evidence

Real runs write `skills/<name>/evals/results/<UTC-date>-<host>-<effective-model>-<example-id>.md` and a sibling directory. Once both arms are prepared, a failed host preflight or execution is recorded as invalid, including a preflight failure before either model call. Earlier preparation rejections exit with an invalid-comparison diagnostic. No record is written by `--dry-run`.

Each arm has a raw JSON trace, standard error, observed response, discovery and input manifest, and final fixture artifacts. Codex also keeps its session rollout and discovery API response. The shared `comparison.json` records the prompt, source example, fixture hashes, skill Git commit and tree SHA, actual skill bytes, dirty state, dependency revisions, host version, model, configuration, inventories, session IDs, elapsed time, and token usage.

The record separates four checks: activation, near-miss behavior, deliverable correctness, and unnecessary workflow cost. Activation and simple near-miss measurements are automatic. Semantic correctness and whether extra work was justified require a reviewer to inspect the preserved response and artifacts. A model's claim that it ran a check is not an independent verification result.

Exit status is `0` for a valid comparison or successful dry run, `1` for an invalid or failed comparison, and `2` for a usage error. An activation mismatch is an evaluation finding and does not turn an isolated, completed comparison into an invalid one.

## Check isolation without models

```sh
tests/eval-harness/run.sh
```

The suite proves project candidate exclusion for both hosts, rejection of an injected baseline copy with an alias folder name, identical dependency inventories, fixture restoration, environment filtering, ancestor rejection, unsupported configuration rejection, and evidence-based activation detection. It calls neither host nor a model and reads no credentials. Its dependency resolution uses the same pinned inline-script convention as the repository's other Python checks.
