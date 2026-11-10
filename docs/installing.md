# Installation and host policy

The installer keeps the multiple-name interface and resolves only the transitive `metadata.requires` closure. Optional prose pointers do not install packages. It reports upstream prerequisites for a separate installation; a listed name alone establishes neither installed discovery nor invocation authority.

## Install or update skills

Use this to install named skills or update an installation owned by this repository's installer. Use disposable targets for tests; an actual host install needs authority for that destination and its settings.

1. Run `scripts/install-skills.py --help` and `scripts/build-host-config.py --help`. Choose the names, host, target, and copy or symlink mode. Read [preview and apply](#preview-and-apply) for ownership rules. Done when the required closure and destination are known.
2. For Codex, follow the [source-policy generation and install commands](#codex). For Claude Code, use the [explicit target, settings, and scope commands](#claude-code) from a standalone project or main checkout; the adapter rejects linked worktrees. Preview before adding `--apply`. Done when the JSON plan contains only intended packages and settings, and applying it reports success.
3. To update, fetch and review the intended source revision, regenerate/check source policy, then use `--force` in both preview and apply. Set `task_skill` to the chosen skill and `task_skills` to its actual host target. For Codex:

   ```sh
   scripts/install-skills.py --host codex --target "$task_skills" --force "$task_skill"
   scripts/install-skills.py --host codex --target "$task_skills" --force --apply "$task_skill"
   ```

   For Claude, also set `task_settings` to the effective settings file, `task_scope` to `user`, `project`, or `local`, and `task_project` to the supported project root:

   ```sh
   scripts/install-skills.py --host claude --target "$task_skills" \
     --settings "$task_settings" --settings-scope "$task_scope" \
     --project-root "$task_project" --force "$task_skill"
   scripts/install-skills.py --host claude --target "$task_skills" \
     --settings "$task_settings" --settings-scope "$task_scope" \
     --project-root "$task_project" --force --apply "$task_skill"
   ```

   `--force` updates only unchanged owned content. Reconcile a foreign destination, edited install, or changed receipt source explicitly; the flag does not override them. Done when the reviewed revision is installed with its intended policy and unrelated content is preserved.
4. Repeat the same apply command and verify that matching content stays unchanged. For installer or adapter changes, run `tests/install/run.sh` and `tests/adoption-tooling/run.sh`, then [candidate validation](validating.md). Use [live-host checks](#live-host-checks) only within authorized session and model budgets. Done when installed bytes and receipts agree, a repeat install changes nothing, and discovery claims are either observed in a fresh isolated session or reported as untested.

## Preview and apply

Repository tools use Python 3.12 or later through uv with pinned dependencies. The installer and host generator print JSON plans on stdout and diagnostics on stderr, with no prompts. Exit 0 means success or a successful preview; 1 means findings, drift or a conflict; 2 means usage. `--help` exits 0 without host inspection or writes. Read-only checks never apply changes.

```sh
scripts/install-skills.py --target <skills-dir> agent-briefing decision-log
scripts/install-skills.py --target <skills-dir> --apply agent-briefing decision-log
scripts/install-skills.py --target <skills-dir> --mode symlink --apply agent-orchestrator
```

A repeat install verifies the actual tree against its receipt and leaves matching content unchanged. The receipt lives in `<skills-dir>/.skills-installer.json`. `--force` permits an update of an unchanged, previously owned install; it never authorizes replacement of a foreign or edited destination. Reconcile such conflicts explicitly. Copies omit private `evals/results` evidence; resources elsewhere named `results` remain included. Keep the source repository available for symlink installs.

## Codex

Catalog `invocation` is `model` by default or `user` for explicit entry. Generate the owned source policy in a controlled repository step before either a copy or symlink install:

```sh
scripts/build-host-config.py
scripts/build-host-config.py --apply
scripts/build-host-config.py --check
scripts/install-skills.py --host codex --target <codex-skills-dir> --apply <name> <other-name>
```

Only user entries get `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. Model entries have no generated policy file. Generation rejects foreign host files; a mode change removes only a file bearing the generator's ownership header. Installation checks the source policy and never generates through a symlink or modifies an upstream cache. Host-specific fields stay out of canonical `SKILL.md`.

## Claude Code

Use explicit host, skill target, actual settings target, scope, and project root. The adapter supports a standalone project or the main checkout root. Linked Git worktrees, separate Git directories and repository subdirectories fail before writes because their effective local settings may live elsewhere. For a personal install, `<config-dir>` is `CLAUDE_CONFIG_DIR` if set, otherwise `$HOME/.claude`. For project and local scopes, the skill target is `<project>/.claude/skills`; settings are respectively `<project>/.claude/settings.json` and `<project>/.claude/settings.local.json`.

```sh
scripts/install-skills.py --host claude --target <config-dir>/skills --settings <config-dir>/settings.json --settings-scope user --project-root <project> <name> <other-name>
scripts/install-skills.py --host claude --target <config-dir>/skills --settings <config-dir>/settings.json --settings-scope user --project-root <project> --apply <name> <other-name>
```

Before applying, the adapter inspects the installed native CLI's `skillOverrides` settings enum and runs only its `--version` command. It requires the reviewed `on`, `name-only`, `user-invocable-only`, `off` mapping. Pass `--claude-bin` to select the actual native executable; unsupported wrappers or changed schema packaging fail closed. This static capability gate uses no model call and does not establish actual discovery or compliance.

The preview shows the exact selected skill-key changes and effective states. User entries become `user-invocable-only` unless an existing stricter `off` applies. The adapter reads user, project and local settings in precedence order, preserves unrelated keys and disabled entries, and rejects a higher-precedence setting that would expose a user entry. Choose that effective target explicitly to resolve it. Managed and command-line policies remain authoritative; inspect them in the live-host check below.

Ownership is recorded beside the selected settings file as `<settings-file>.skills-installer.json`. On a change to model invocation, the adapter undoes only an unchanged override it wrote, restoring the prior value or removing its own new key. It preserves pre-existing manual/disabled choices and later user edits. Malformed JSON, duplicate keys, unknown override states, symlinks and malformed ownership records fail before writes. Settings stay outside installed content. Plugin skills are outside this adapter's scope.

The mapping and precedence follow [Claude's skill settings](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings) and [settings precedence](https://code.claude.com/docs/en/settings#settings-precedence). Fresh installed versions still need the capability gate and the session checks below.

## Live-host checks

Fixtures prove generation, settings preservation and installed bytes. For each supported installed host version, start a fresh isolated session and inspect actual discovery, exact explicit names, manual suppression and explicit selection. Give every test a temporary HOME, configuration, cache and project directory. A clean project alone does not isolate global plugins.

Inventory and isolate all four upstream collections (Matt, pstack/port, tstack and Superpowers), owned startup injections, user/project/local/managed settings and any command-line overrides in the test environment. Verify no source cache changed. Record host versions and source hashes. Run no behavioral evaluation against the user's real home or settings. Keep materially changed skills unevaluated until matched behavioral evidence is authorized and recorded.
