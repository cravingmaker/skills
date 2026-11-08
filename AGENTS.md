# AGENTS.md

This repo holds personal Agent Skills that follow the [Agent Skills specification](https://agentskills.io/specification).

## Structure

- `skills/<skill-name>/SKILL.md` — one directory per skill. Nothing else goes in `skills/`.
- `template/` — copy this to start a new skill. Do not add skills here.
- `scripts/validate.sh` — runs the reference validator (`skills-ref`) on every skill.

## Authoring rules

- `name`: 1–64 chars, lowercase `a-z`, `0-9` and `-` only, no leading, trailing or doubled hyphens. Must equal the directory name.
- `description`: 1–1024 chars. State what the skill does **and** when to use it, with the keywords a user would say.
- Optional frontmatter: `license`, `compatibility` (only for real environment requirements), `metadata` (string → string map), `allowed-tools` (experimental).
- Keep `SKILL.md` under 500 lines (~5000 tokens). Move detail into `references/`, code into `scripts/`, static files into `assets/`.
- Reference bundled files with relative paths from the skill root, one level deep.
- Scripts must be self-contained or document their dependencies, and fail with helpful messages.

## Workflow

1. `cp -r template skills/<skill-name>` and edit `SKILL.md`.
2. Run `./scripts/validate.sh` and fix every error.
3. Add the skill to the table in `README.md`.
