# cravingmaker/skills

[![CI](https://github.com/cravingmaker/skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/cravingmaker/skills/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/github/license/cravingmaker/skills)](https://github.com/cravingmaker/skills/blob/main/LICENSE)

Craving Maker's opinionated collection of [Agent Skills](https://agentskills.io). Each skill is a folder of instructions, scripts, and resources that an agent loads when a task calls for it.

- **One open format.** Every skill follows the [Agent Skills specification](https://agentskills.io/specification), so it works in Claude Code, Codex, Cursor, and the other [skills-compatible clients](https://agentskills.io/clients).
- **Enforcement over instructions.** Where a rule can be a check (a linter, a type, a test, a CI job), the skill ships or sets up the check; prose covers only the judgment calls.
- **Validated on every change.** CI runs the pinned [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) validator, a repository checker for provenance and examples, and fixture tests for the bundled tools.

## Contents

- [Skills](#skills)
- [Installation](#installation)
- [Layout](#layout)
- [Adding a skill](#adding-a-skill)
- [Contributing and security](#contributing-and-security)
- [License](#license)

## Skills

| Skill | Description |
| ----- | ----------- |
| [clear-communication](skills/clear-communication) | Clear, lean, faithful communication in both directions: understanding the request and writing the result. Ships a standing contract for AGENTS.md and a Vale style. |
| [project-guardrails](skills/project-guardrails) | Sets up or audits the checks that make a wrong change fail, in the order readability, maintainability, security, performance. |
| [toolchain-upgrade](skills/toolchain-upgrade) | Upgrades lint, format, and type tooling by comparing effective configuration before and after and deciding every change. |
| [correct](skills/correct) | Turns a repeated agent mistake into a check that fails, at the highest layer that can hold it. |

## Installation

Install the skills into any supported agent with the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add cravingmaker/skills
```

To install one skill by hand, copy its folder from `skills/` into the skills directory of the agent, for example `~/.claude/skills/` for Claude Code.

For everyday answers to follow the communication rules without loading a skill, paste the standing contract from [clear-communication/references/house-style.md](skills/clear-communication/references/house-style.md) into your AGENTS.md or CLAUDE.md.

## Layout

```
.
├── skills/                 # One folder per skill
│   └── <skill-name>/
│       ├── SKILL.md        # Required: frontmatter and instructions
│       ├── evals/          # Required: activation, near-miss, and outcome examples
│       ├── references/     # Optional: documentation loaded on demand
│       ├── scripts/        # Optional: executable code
│       └── assets/         # Optional: templates, configs, and data
├── template/               # Starting point for a new skill
├── scripts/                # validate.sh and check-skills.py
└── tests/                  # Fixtures for the checker and the Vale style
```

## Adding a skill

Copy the template to a folder named after the skill. The folder name must match the `name` field of its `SKILL.md`:

```bash
cp -r template skills/my-skill
```

Set `name`, write a `description` that says what the skill does and when to use it, and fill in `evals/examples.md`. Then validate, which needs [uv](https://docs.astral.sh/uv/) and, for the prose tests, [Vale](https://vale.sh) 3.26.0:

```bash
./scripts/validate.sh
```

Add the skill to the table in [Skills](#skills). [AGENTS.md](AGENTS.md) lists the authoring and provenance rules.

## Contributing and security

Follow the [Code of Conduct](https://github.com/cravingmaker/.github/blob/main/CODE_OF_CONDUCT.md) when participating in the project. Report vulnerabilities privately as described in the [security policy](https://github.com/cravingmaker/.github/blob/main/SECURITY.md).

## License

MIT © [cravingmaker](https://github.com/cravingmaker), except skills that carry their own `LICENSE-*` file for adapted third-party material.
