# AGENTS.md

This repo holds personal Agent Skills that follow the [Agent Skills specification](https://agentskills.io/specification).

## Structure

- `skills/<skill-name>/` holds one skill: `SKILL.md`, optional `references/`, `scripts/`, `assets/`, and a required `evals/examples.md`. The only host-file exception is owned, generated `agents/openai.yaml` for catalog entries with `invocation: user`; preview `scripts/build-host-config.py`, then use `--apply`. Check it with `--check`. Nothing else goes in `skills/`.
- `template/` starts a capability skill. Do not add skills to it.
- `catalog/skills.yaml` lists every skill (kind, roles, evaluation status) and the upstream skills routers may name; `catalog/coverage.md` maps every job the collection covers to skills; `catalog/profiles/` holds generated install lists, one per router; `catalog/reserved-names.txt` lists names already taken by the user's other skills.
- `docs/authoring-guide.md` is the bar every skill meets. Read it before writing or reviewing a skill.
- `scripts/validate.sh` runs every check: the pinned `skills-ref` validator, `check-skills.py`, `check-catalog.py`, `build-profiles.py --check`, `check-freshness.py`, zizmor, the Vale style on the repo's docs, and the fixture tests in `tests/`.
- `scripts/install-skills.py` installs named skills with everything they require.

## Authoring rules

- `name`: 1 to 64 characters, lowercase `a-z`, `0-9`, and `-` only, with no leading, trailing, or doubled hyphens. It equals the directory name.
- `description`: 1 to 1024 characters. State what the skill does and when to use it, with the words a user would say. Keep it narrow enough that ordinary requests do not load the skill.
- Frontmatter uses only the spec's fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Entry preference belongs in `catalog/skills.yaml` as `invocation: model | user`, defaulting to `model`. Host adapters implement it; no host fields go in `SKILL.md`.
- `metadata` values are strings. Quote numbers and versions.
- Keep `SKILL.md` under 500 lines. Move detail into `references/`, code into `scripts/`, and static files into `assets/`, linked one level deep from `SKILL.md`.
- Scripts are self-contained or declare their dependencies, pin versions, and fail with a message that names the fix.

## Provenance

A skill that adapts third-party material sets `license`, `metadata.source` (the upstream URL), `metadata.source-revision` (the full commit SHA), and keeps the upstream license text in a `LICENSE-<upstream>` file inside the skill folder, with a header naming the adapted files. Apache-2.0 material also keeps any upstream `NOTICE` and marks changed files. Link the per-file manifest from `SKILL.md` as `references/SOURCES.md` (or `references/sources.csv`); use the schema in [docs/authoring-guide.md](docs/authoring-guide.md). Each contributor needs its own legal file. `scripts/check-skills.py` checks the manifest schema, full revisions, hash syntax, legal headers and file existence; reviewing the source establishes that the attribution is complete.

## Evals

`evals/examples.md` has three sections, each with at least one `- ` item: `## Activation` (prompts that should load the skill), `## Near miss` (similar prompts that should not), and `## Outcome` (results a reviewer can check). When adopting or materially changing a skill, run the examples with and without it and record what happened.

Before writing a new skill, write its examples and fixture and run them without the skill. Draft the skill only when that baseline fails an expected Outcome; when it passes, the model already does the job and no skill is needed. Prefer a project check (CI, lint, hook) over a skill when the gap is a rule a script can enforce. Skills earn their place with checks, authority limits and required evidence, not domain knowledge the model already has.

## Writing

Docs in this repo follow `skills/clear-communication`: lead with the point, plain words, one line per paragraph. `./scripts/validate.sh` lints them with its Vale style when Vale is installed.

## Dependencies

Declare dependencies in `SKILL.md` as quoted, space-separated strings: `metadata.requires` for skills this one cannot work without. Optional routes are conditional prose pointers and do not add installation edges. Refer to other skills in prose as "the `name` skill". After changing dependencies, run `scripts/build-profiles.py` and include changed `catalog/profiles/` files.

## Workflow

1. `cp -r template skills/<skill-name>`, then edit `SKILL.md` and `evals/examples.md`.
2. Add the skill to `catalog/skills.yaml` and update `catalog/coverage.md`.
3. Run `scripts/build-profiles.py`, preview/apply `scripts/build-host-config.py` if invocation policy changed, then run `./scripts/validate.sh` and fix every error.
4. Run `scripts/build-docs.py`, then fix whatever `scripts/build-docs.py --check` reports; it generates the README skill index and asks for the human guidance a new skill needs.

## Common tasks

Read the matching procedure before starting; each names its commands, checks, and done criterion. Commands run from the repository root with uv and Python 3.12 or newer.

| Task | Procedure |
| --- | --- |
| Create a new capability skill | [Create a skill](docs/skill-workflows.md#create-a-skill) |
| Adopt or update upstream material | [Adopt an upstream method](docs/skill-workflows.md#adopt-or-update-an-upstream-method) |
| Change a skill and select evals | [Change a skill](docs/skill-workflows.md#change-a-skill) |
| Audit or review a skill | [Review a skill](docs/skill-workflows.md#review-a-skill) |
| Run paired evals within a fixed budget | [Run and review evals](docs/running-evals.md) |
| Install or update on Claude Code or Codex | [Install and update](docs/installing.md#install-or-update-skills) |
| Validate a candidate or prepare stacked PRs | [Validate and prepare delivery](docs/validating.md) |
