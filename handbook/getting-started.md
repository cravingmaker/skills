> **Human documentation.** Agents should not read this page unless a person asks them to.

# Getting started

Install a small useful set, preserve the host's invocation policy, then verify discovery in a fresh session. Installing a skill supplies instructions and resources; it grants no new tools, credentials, subscriptions, or task authority.

## Contents

- [Prepare the source](#prepare-the-source)
- [Install on Codex](#install-on-codex)
- [Install on Claude Code](#install-on-claude-code)
- [Install a role or several skills](#install-a-role-or-several-skills)
- [Know what changes](#know-what-changes)
- [Verify the installation](#verify-the-installation)
- [Update, move, and remove an install](#update-move-and-remove-an-install)
- [Set up a project for the main flow](#set-up-a-project-for-the-main-flow)
- [Make everyday answers follow the house style](#make-everyday-answers-follow-the-house-style)
- [Other installation methods](#other-installation-methods)
- [When something fails](#when-something-fails)

## Prepare the source

Use a reviewed checkout and preview each install before applying it. Run from the repository root; replace the example project path with your actual project.

```sh
git clone https://github.com/cravingmaker/skills.git
cd skills
scripts/install-skills.py --help
scripts/build-host-config.py --check
```

The repository scripts run through uv, request Python 3.12 or newer, and pin PyYAML. A missing uv installation is a setup error; use [uv's installation instructions](https://docs.astral.sh/uv/getting-started/installation/). The host CLI must already be installed and usable. No model call is needed for the installer.

## Install on Codex

The installer checks the generated source policy on every path. `--host codex` is accepted but currently adds no behavior; it makes the intended host visible in the command. For the default user installation, the recorded cutover used `~/.codex/skills`.

```sh
scripts/install-skills.py --host codex --target ~/.codex/skills clear-communication
scripts/install-skills.py --host codex --target ~/.codex/skills --apply clear-communication
```

If you changed invocation preferences in a source checkout, preview and apply the generated host files there first:

```sh
scripts/build-host-config.py
scripts/build-host-config.py --apply
scripts/build-host-config.py --check
```

Manual entries carry `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. The installer checks those files; it does not generate them through an installed symlink. If you set a custom `CODEX_HOME`, resolve that host's actual skill location instead of installing a second accidental copy at the default path. Codex can also discover skills through other locations, including `~/.agents/skills`; a complete discovery check must account for them.

## Install on Claude Code

Supply the actual skill directory, settings file, settings scope, and project root. The default user configuration directory is `~/.claude`; when `CLAUDE_CONFIG_DIR` is set, use that directory instead.

```sh
project_dir=/absolute/path/to/your/project
claude_config_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

scripts/install-skills.py --host claude \
  --target "$claude_config_dir/skills" \
  --settings "$claude_config_dir/settings.json" \
  --settings-scope user --project-root "$project_dir" clear-communication

scripts/install-skills.py --host claude \
  --target "$claude_config_dir/skills" \
  --settings "$claude_config_dir/settings.json" \
  --settings-scope user --project-root "$project_dir" --apply clear-communication
```

These variables are example destinations, not overrides of the shell's home directory. For a project-scoped install, select `<project>/.claude/skills`, `<project>/.claude/settings.json`, and `--settings-scope project`. Local settings use the same skill directory, `settings.local.json`, and `--settings-scope local`.

The adapter checks the installed native Claude binary's supported `skillOverrides` schema and calls `--version`. It writes `user-invocable-only` for manual entries while preserving a stricter `off`. Use `--claude-bin /path/to/native/claude` when the command on PATH is a wrapper.

The current adapter accepts a standalone project or its main checkout root. It rejects linked Git worktrees, separate Git directories, and repository subdirectories before writing. Choose a supported root rather than guessing which settings file would take precedence. See the [canonical adapter contract](../docs/installing.md#claude-code).

## Install a role or several skills

Pass several names in one invocation to install the union of their required dependencies. A role's install is its router plus the transitive required closure; overlapping requirements are installed once.

```sh
scripts/install-skills.py --host codex --target ~/.codex/skills \
  agent-briefing decision-log
scripts/install-skills.py --host codex --target ~/.codex/skills --apply \
  agent-briefing decision-log
scripts/install-skills.py --host codex --target ~/.codex/skills agent-orchestrator
scripts/install-skills.py --host codex --target ~/.codex/skills --apply agent-orchestrator
```

Use the same names in the Claude commands above for Claude's adapter. Check the [generated role and profile reference](routing.md#roles-and-their-routers) before choosing a role. A role listed as planned is unavailable on main, even if existing generic capabilities already mention that role.

A required external skill is reported with its upstream source and installation instructions. The installer does not fetch it automatically. The current owned orchestrator profile has no external prerequisite.

## Know what changes

The preview prints JSON on stdout and diagnostics on stderr. Without `--apply`, it writes nothing.

| Location | Effect |
| --- | --- |
| Target skill directory | One folder or symlink per skill in the required closure |
| `<skills-dir>/.skills-installer.json` | Ownership receipt for this source checkout and installed contents |
| Claude settings file, when its adapter is selected | Only the selected skill visibility overrides; unrelated settings stay intact |
| `<settings-file>.skills-installer.json` | Ownership receipt for Claude settings changes |
| Source checkout, only when host generation is applied | Owned Codex policy files for manual entries |

Copy mode is the default. It preserves installed file identities and executable modes while excluding `evals/results/`. It does not copy the repository README, handbook, catalog, authoring docs, or repository validation scripts. Resources elsewhere named `results` are retained.

Symlink mode keeps a live connection to the source skill folders. Keep the source checkout available; changing it changes the linked installation. Because the whole folder is linked, source evaluation files remain reachable through that link. Copy mode is the simpler choice for a stable reviewed install.

## Verify the installation

Rerun the same install command after applying it. A matching owned installation reports `keep`; a repeated apply should leave content and settings unchanged.

Start a fresh host session and inspect its actual skill inventory. In Claude Code, compare the available slash-command entries with the model-visible list. Manual entries can remain available to the user while absent from the model's list. In Codex, use explicit skill selection and confirm that the selected installed body is used; listing a name is not proof of activation.

For a small end-to-end check, install the interview entry and try an explicit command on a harmless hypothetical plan. Use the [generated command reference](typed-commands.md) for the host syntax. The expected interview writes no project files and waits for confirmation of its close.

Recorded discovery evidence exists for copy and symlink installs on both hosts. That early experiment covered a smaller historical profile; the current generated profile is authoritative for today's closure. The [support page](harnesses.md) explains what those tests establish.

## Update, move, and remove an install

Update the same source checkout, inspect its diff, regenerate policy if needed, and preview another install. An unchanged source yields `keep`. An owned unchanged destination whose source changed requires `--force` to update.

```sh
scripts/install-skills.py --host codex --target ~/.codex/skills \
  --force clear-communication
scripts/install-skills.py --host codex --target ~/.codex/skills \
  --force --apply clear-communication
```

Here `--force` permits updating a destination the installer still owns. It does not overwrite a foreign folder, a locally edited copy, or an edited ownership receipt. Reconcile the named conflict first. The receipt binds the source checkout location; moving the source may also require reconciliation.

The installer has no general uninstall command. Removing an installed package or settings override requires scoped ownership inspection; deleting a folder alone can leave settings or dependent packages behind. Use the [cutover checklist](cutover.md) when replacing upstream collections, and preserve a rollback record for the affected files and settings.

## Set up a project for the main flow

The shaping skills read a small project contract: where the tracker is, what the triage labels are called, and where the glossary and ADRs live. Create it once per project by typing `/setup-agent-skills` (Claude Code) or `$setup-agent-skills` (Codex) in that project.

It writes one `## Agent skills` block in your `AGENTS.md` or `CLAUDE.md` and up to three files: `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md` and `docs/agents/domain.md`. Glossary and ADR files are created later, when the first term or decision is recorded.

Without that contract, `to-spec` and `to-tickets` return drafts in the conversation instead of filing them, and `grill-with-docs` offers a plain interview with no doc writes.

## Make everyday answers follow the house style

For ordinary answers to follow the communication rules without loading any skill, paste the standing contract from [`skills/clear-communication/references/house-style.md`](../skills/clear-communication/references/house-style.md) into your `AGENTS.md`, `CLAUDE.md` or the host's global instructions. It is seven lines: lead with the answer, use the fewest words that stay accurate, keep facts exact, use plain words, ask only questions that change the outcome, state reversible assumptions, and restate only what is uncertain.


## Other installation methods

The README previously advertised `npx skills add cravingmaker/skills`, and individual folders can be copied manually into a host skill directory. Those methods do not establish that this repository's required closure or Claude settings adapter ran. Use the owned installer when you need dependency resolution, ownership receipts, and manual-entry policy together.

Other hosts may understand the Agent Skills format but have different invocation controls. Treat their behavior as untested until you verify it; see [supported harnesses](harnesses.md).

## When something fails

| Message or symptom | What to do |
| --- | --- |
| `... is required but is neither in .../skills nor an external skill in the catalog` | A required skill is missing from the source you install from. Pull the full repository; do not install from a partial copy. |
| `foreign or edited destination conflict; reconcile it explicitly (--force cannot overwrite it)` | The folder exists and is not the installer's unchanged copy. Inspect ownership and reconcile it before installing again. |
| `owned installation changed at source; preview with --force to update it` | You pulled new versions. Preview and apply with `--force`. |
| `host configuration drift; preview scripts/build-host-config.py, then run it with --apply` | The generated Codex policy is out of date in your clone. Run `scripts/build-host-config.py --apply` in a clean clone, or pull again. |
| `Claude settings in linked Git worktrees, separate Git directories or repository subdirectories are unsupported` | Pass `--project-root` the main checkout root or a standalone project, not a worktree. |
| `Claude user and project settings overlap; choose a separate project root` | You passed your home folder as `--project-root`. Pass a project folder instead. |
| `Claude skillOverrides support not found ...` | The `claude` on your `PATH` is a wrapper or an unsupported build. Pass the native executable with `--claude-bin`. |
| `a higher-precedence Claude settings file exposes this user entry` | A project or local settings file turns the skill back on. Install at that scope, or remove that override. |

More symptoms, with causes and fixes, are on [Gotchas](gotchas.md).
