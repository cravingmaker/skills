# Skills

My personal collection of [Agent Skills](https://agentskills.io): portable folders of instructions, scripts and resources that AI agents load on demand.

Skills follow the open [Agent Skills specification](https://agentskills.io/specification), so they work in any skills-compatible agent (Claude Code, Claude.ai, Codex, Cursor, and [others](https://agentskills.io/clients)).

## Layout

```
.
├── skills/                 # One folder per skill
│   └── <skill-name>/
│       ├── SKILL.md        # Required: frontmatter + instructions
│       ├── scripts/        # Optional: executable code
│       ├── references/     # Optional: docs loaded on demand
│       └── assets/         # Optional: templates, data, images
├── template/               # Starting point for a new skill
├── scripts/validate.sh     # Validates every skill against the spec
└── .github/workflows/      # CI: validation on every push and PR
```

## Skills

_None yet._

| Skill | Description |
| ----- | ----------- |

## Using these skills

**Any agent (via the [`skills`](https://github.com/vercel-labs/skills) CLI):**

```bash
npx skills add cravingmaker/skills
```

**Manually:** copy a folder from `skills/` into your agent's skills directory, for example `~/.claude/skills/` for Claude Code.

## Adding a skill

1. Copy the template and rename it. The folder name must match the `name` field.

   ```bash
   cp -r template skills/my-skill
   ```

2. Edit `skills/my-skill/SKILL.md`: set `name` and write a `description` that says what the skill does and when to use it.
3. Validate:

   ```bash
   ./scripts/validate.sh
   ```

4. Add a row to the table above.

See [AGENTS.md](AGENTS.md) for the authoring rules.

## License

[MIT](LICENSE)
