# AGENTS.md

This repo holds personal Agent Skills that follow the [Agent Skills specification](https://agentskills.io/specification).

## Structure

- `skills/<skill-name>/` holds one skill: `SKILL.md`, optional `references/`, `scripts/`, `assets/`, and a required `evals/examples.md`. Nothing else goes in `skills/`.
- `template/` is the starting point for a new skill. Do not add skills here.
- `scripts/validate.sh` runs every check: the pinned `skills-ref` validator, `scripts/check-skills.py`, and the fixture tests in `tests/`.
- `tests/` holds fixtures for the repository checker and for the `clear-communication` Vale style.

## Authoring rules

- `name`: 1 to 64 characters, lowercase `a-z`, `0-9`, and `-` only, with no leading, trailing, or doubled hyphens. It equals the directory name.
- `description`: 1 to 1024 characters. State what the skill does and when to use it, with the words a user would say. Keep it narrow enough that ordinary requests do not load the skill.
- Frontmatter uses only the spec's fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Host-specific behavior, such as manual-only invocation, belongs in the host's settings, not in `SKILL.md`.
- `metadata` values are strings. Quote numbers and versions.
- Keep `SKILL.md` under 500 lines. Move detail into `references/`, code into `scripts/`, and static files into `assets/`, linked one level deep from `SKILL.md`.
- Scripts are self-contained or declare their dependencies, pin versions, and fail with a message that names the fix.

## Provenance

A skill that adapts third-party material sets `license`, `metadata.source` (the upstream URL), `metadata.source-revision` (the full commit SHA), and keeps the upstream license text in a `LICENSE-<upstream>` file inside the skill folder, with a header naming the adapted files. Apache-2.0 material also keeps any upstream `NOTICE` and marks changed files. `scripts/check-skills.py` enforces the declared parts; reviewing the source establishes that the attribution is complete.

## Evals

`evals/examples.md` has three sections, each with at least one `- ` item: `## Activation` (prompts that should load the skill), `## Near miss` (similar prompts that should not), and `## Outcome` (results a reviewer can check). When adopting or materially changing a skill, run the examples with and without it and record what happened.

## Writing

Docs in this repo follow `skills/clear-communication`: lead with the point, plain words, one line per paragraph. `./scripts/validate.sh` lints them with its Vale style when Vale is installed.

## Workflow

1. `cp -r template skills/<skill-name>`, then edit `SKILL.md` and `evals/examples.md`.
2. Run `./scripts/validate.sh` and fix every error.
3. Add the skill to the table in `README.md`.
