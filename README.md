# cravingmaker/skills

[![CI](https://github.com/cravingmaker/skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/cravingmaker/skills/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/github/license/cravingmaker/skills)](https://github.com/cravingmaker/skills/blob/main/LICENSE)

Craving Maker's opinionated collection of [Agent Skills](https://agentskills.io). Each skill is a folder of instructions, scripts, and resources that an agent loads when a task calls for it.

- **One open format.** Every skill follows the [Agent Skills specification](https://agentskills.io/specification), so it works in Claude Code, Codex, Cursor, and the other [skills-compatible clients](https://agentskills.io/clients).
- **Small until needed.** An agent reads only the `name` and `description` of a skill at startup, and the rest of it when a task matches.
- **Validated on every change.** CI checks each skill with [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref), the reference validator of the specification.

## Contents

- [Skills](#skills)
- [Installation](#installation)
- [Layout](#layout)
- [Adding a skill](#adding-a-skill)
- [Contributing and security](#contributing-and-security)
- [License](#license)

## Skills

None yet.

| Skill | Description |
| ----- | ----------- |

## Installation

Install the skills into any supported agent with the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add cravingmaker/skills
```

To install one skill by hand, copy its folder from `skills/` into the skills directory of the agent, for example `~/.claude/skills/` for Claude Code.

## Layout

```
.
├── skills/                 # One folder per skill
│   └── <skill-name>/
│       ├── SKILL.md        # Required: frontmatter and instructions
│       ├── scripts/        # Optional: executable code
│       ├── references/     # Optional: documentation loaded on demand
│       └── assets/         # Optional: templates, data, and images
├── template/               # Starting point for a new skill
└── scripts/validate.sh     # Validates the template and every skill
```

## Adding a skill

Copy the template to a folder named after the skill. The folder name must match the `name` field of its `SKILL.md`:

```bash
cp -r template skills/my-skill
```

Set `name` and write a `description` that says what the skill does and when to use it. Then validate, which needs [uv](https://docs.astral.sh/uv/):

```bash
./scripts/validate.sh
```

Add the skill to the table in [Skills](#skills). [AGENTS.md](AGENTS.md) lists the authoring rules.

## Contributing and security

Follow the [Code of Conduct](https://github.com/cravingmaker/.github/blob/main/CODE_OF_CONDUCT.md) when participating in the project. Report vulnerabilities privately as described in the [security policy](https://github.com/cravingmaker/.github/blob/main/SECURITY.md).

## License

MIT © [cravingmaker](https://github.com/cravingmaker)
