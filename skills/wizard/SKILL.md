---
name: wizard
description: Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/wizard/SKILL.md"
  source-files: "skills/engineering/wizard/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  local-changes: "Replaced the shell-quoted dotenv writer and reader with a declared-format serializer that refuses unsupported values before writing; removed the no-edit rule for the library; added destination, symlink and git-tracking checks, --help and --dry-run, and parser round-trip tests; moved the template to assets/."
---

# Wizard

A **wizard** is a bash script that walks a human, step by step, through a manual procedure that's tedious to do by hand and tedious to re-explain to an AI every time. It opens each URL, says exactly what to click and copy, captures the values, writes them where they belong (`.env`, GitHub secrets), confirms at every stage, and shows how many stages are left. It might configure third-party services, run a one-off migration, or move the project from one state to another.

[assets/template.sh](assets/template.sh) supplies the UX: stage-by-stage progress, confirmation gates, cross-platform URL opening (including WSL), hidden secret entry, `.env` upserts that refuse values the file format cannot hold, `gh secret`/`gh variable` writes, `--dry-run`, and a closing summary. Your job is to scope the procedure and author its stages. The library above the `STAGES` marker is shared; change it when the procedure needs it, and keep the round-trip check below passing.

The generated script needs Bash 3.2 or later (the macOS default works); `gh` is optional. A wizard is ephemeral by default: built for one run, saved to a scratch or `scripts/` path, deleted when the job's done. Commit it only when the user wants a repeatable setup path that should live in the repo, and only within the current authority to commit.

## Process

### 1. Scope the procedure

Work out every manual step the human must take and every value that gets captured along the way. Read the repo first, don't ask cold:

- For setup: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework config, and `.github/workflows/*` (every `secrets.*` / `vars.*` reference is a value the wizard must produce).
- The **loader**: what actually reads the environment file (npm `dotenv`, Node's `--env-file`, python-dotenv, Compose, a framework, or `source .env` in a script). It decides `ENV_FORMAT` in step 3.
- Existing setup paths: a setup script, a documented `make` target, or a secret manager the project already uses. Prefer extending or pointing to those; a wizard fills only the human-only gaps.
- For a migration or transition: the current state, the target state, and the irreversible actions between them.

Then show the user the ordered list of stages and the values each produces, and confirm: they may add, drop, or reorder. Skip the confirmation when the user already supplied the stage list.

**Done when:** every stage is named in order, and for each captured value you know (a) where the human gets it, (b) where it's written (`.env`, a GitHub secret, both, or nowhere; some stages are pure actions), and (c) whether it's secret (hidden entry) or public.

### 2. Map each stage's journey

For each stage, write the precise path a human follows: which URL to open, what to do there, where a value is shown, which variable it fills: e.g. "Dashboard → Developers → API keys → Reveal test key → copy". Where you don't actually know the current UI or the exact command, say so and ask the user or check the docs: never invent steps that may not exist.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Copy `assets/template.sh` to the target path. Replace the example stage with one `stage` per step, in dependency order. Use the library helpers: `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, `pause`/`confirm`. Set `TOTAL_STAGES` and `WIZARD_TITLE`, and keep `wizard_init "$@"` first in `run_wizard`.

Hold the bar the template sets: open the URL before asking for its value, use `ask_secret` for anything secret, `write_env` every persisted value, `set_secret` only the values CI actually needs, and `confirm` before any irreversible action. Each `stage` clears the screen so only the current step is visible: keep a stage to one focused task so nothing the human needs scrolls away. Make every stage safe to repeat: a re-run offers saved values as defaults, and an action stage should check or `confirm` whether it is already done.

Set the environment-file format for the loader you found:

- `ENV_FORMAT=dotenv` (default) writes only values that npm `dotenv`, Node's built-in parser, python-dotenv and a POSIX shell all read back unchanged. It refuses, before the file changes, a backslash, a line break, `${`, and a single quote together with `"`, `$` or a backtick.
- `ENV_FORMAT=shell` is for files that only `sh`/`bash` source. It quotes every value for the shell and refuses only line breaks.

A refused value stops the wizard with exit 1 and a message that names the key, never the value; the human then sets it by hand or in the project's secret store. If the loader adds interpolation (`dotenv-expand`, Compose), values containing `$` still need the round-trip check below. `ENV_FILE` must stay inside the directory the wizard runs in; the library also refuses a symlink or a git-tracked file unless the human opts in with the variable it names.

### 4. Verify and hand off

- `bash -n <script>`; run `shellcheck` if available. `./<script> --help` must exit 0 with no effect.
- `chmod +x <script>`.
- Round-trip the environment file: run the wizard library's `write_env` against a scratch copy of the destination with dummy values shaped like the real ones (an apostrophe, `$`, `#`, spaces, an empty value), then read that copy with the project's actual loader and compare exactly. Syntax success or a successful write does not prove the stored value is the one the human typed.
- Don't run it end-to-end yourself: it opens browsers and blocks on human input. Trace it statically instead: every value from step 1 is captured and lands where step 1 said, and every `set_secret` name exactly matches a `secrets.*` reference in CI. `--dry-run` lets the human rehearse it without writing anything.
- Tell the user how to run it. If it's a repeatable setup path and committing is authorized, commit it and link it from the README so the next person runs the script instead of asking an AI.

**Done when:** the script passes `bash -n` and `--help`, the dummy round trip through the project's loader matches exactly, every captured value has its destination, and the user knows the command to run. Secret writes and infrastructure changes happen only when the human runs the wizard, within the authority they already have.

## Edge cases

- **The loader is not one the formats cover** (a YAML or JSON config, a custom parser): write that format's serializer into the copied library and round-trip it through the real parser, or have the wizard print where the human pastes the value.
- **A value the format refuses** is common for private keys and Windows paths. Point the human to the project's secret store or a manual edit; do not loosen the refusal without a round-trip test that proves the loader reads the new form.
- **A key that already spans several lines** in the file is refused rather than rewritten; other multi-line values are preserved byte for byte.

## Provenance

Adapted from Matt Pocock's wizard skill; see [references/SOURCES.md](references/SOURCES.md) and `LICENSE-mattpocock`. The repository test `tests/wizard/run.sh` exercises the template against python-dotenv, Node's built-in parser and `sh`.
