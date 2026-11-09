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
| [agent-orchestrator](skills/agent-orchestrator) | Role: equips an agent to run a fleet of agents as their product and project manager. |
| [work-decomposition](skills/work-decomposition) | Imports approved tickets with exact hashes and Proof, then checks ownership, dependencies and a finite budget. |
| [agent-briefing](skills/agent-briefing) | Writes briefs a fresh agent can execute with no history, with a checker for missing fields. |
| [agent-debate](skills/agent-debate) | Runs bounded, evidence-based reviews between agents, with a checker for review reports. |
| [result-verification](skills/result-verification) | Accepts agents' work by rerunning checks and verifying claims at the source, with a write-boundary checker. |
| [decision-log](skills/decision-log) | Keeps an on-disk run record (plan, log, decisions, raw reports) so multi-agent work survives interruption. |
| [grilling](skills/grilling) | Resolves consequential design questions in bounded interview rounds, reusing settled answers. |
| [grill-with-docs](skills/grill-with-docs) | Grounds an interview in configured domain docs and records resolved glossary terms and ADRs. |
| [domain-modeling](skills/domain-modeling) | Maintains domain vocabulary and immutable, superseded ADRs at configured paths. |
| [to-spec](skills/to-spec) | Writes an agreed spec with stable stories, source hashes, acceptance and named Proof. |
| [to-tickets](skills/to-tickets) | Files approved vertical slices with exact status, blockers, acceptance and Proof. |
| [triage](skills/triage) | Verifies tracker claims and routes issues and external PRs through configured triage states. |
| [wayfinder](skills/wayfinder) | Charts decision tickets for an unclear goal and resolves the next consequential question. |
| [to-questionnaire](skills/to-questionnaire) | Drafts recipient-specific questions from known facts and decision gaps without sending them. |
| [setup-agent-skills](skills/setup-agent-skills) | Maintains one Agent skills block and configured tracker, triage and domain paths. |
| [prototype](skills/prototype) | Builds and observes a bounded throwaway artifact to answer one design question. |
| [sharpen](skills/sharpen) | Refines a requested prompt without expanding or executing the task. |
| [research](skills/research) | Answers bounded questions from primary sources with explicit inference and search limits. |
| [how](skills/how) | Traces an actual execution path and responsibilities from source anchors. |
| [why](skills/why) | Reconstructs design intent from attributable history and calibrated uncertainty. |
| [grill-me](skills/grill-me) | Manual no-doc entry into the owned grilling interview. |
| [bro](skills/bro) | Manual entry that repairs the last answer through clear-communication. |
| [wait-what](skills/wait-what) | Manual entry that explains the last unclear point using the user's context. |

See [the catalog](catalog/skills.yaml) for evaluation status and each skill's `evals/results/` for outcomes and limits. Explicit entries use the catalog's `invocation: user`; host policy grants no additional task authority.

## Installation

Install the skills into any supported agent with the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add cravingmaker/skills
```

To install a role or a skill together with every skill it requires, clone this repository and run the installer (needs [uv](https://docs.astral.sh/uv/)):

```bash
scripts/install-skills.py --target ~/.claude/skills clear-communication
scripts/install-skills.py --target ~/.claude/skills --apply clear-communication
scripts/install-skills.py --target ~/.claude/skills --mode symlink --apply <role-or-skill>
```

The default prints a JSON preview; `--apply` writes. See [installation and host policy](docs/installing.md) for explicit Claude settings, Codex generation, ownership conflicts and temporary-host checks. It lists any upstream skills a role relies on so you can install them from their source. To install one skill by hand, copy its folder from `skills/` into the agent's skills directory, for example `~/.claude/skills/` for Claude Code.

For everyday answers to follow the communication rules without loading a skill, paste the standing contract from [clear-communication/references/house-style.md](skills/clear-communication/references/house-style.md) into your AGENTS.md or CLAUDE.md.

## Layout

```
.
├── skills/                 # One folder per skill
│   └── <skill-name>/
│       ├── SKILL.md        # Required: frontmatter and instructions
│       ├── evals/          # Required: activation, near-miss, and outcome examples
│       ├── agents/         # Generated openai.yaml only for invocation: user
│       ├── references/     # Optional: documentation loaded on demand
│       ├── scripts/        # Optional: executable code
│       └── assets/         # Optional: templates, configs, and data
├── template/               # Starting point for a capability skill
├── template-role/          # Starting point for a role router
├── catalog/                # Skill catalog, coverage matrix, install profiles, reserved names
├── docs/                   # Authoring guide
├── scripts/                # Validation, catalog, profile, freshness, and install scripts
└── tests/                  # Fixtures for every script and the Vale style
```

## Adding a skill

Copy the template to a folder named after the skill. The folder name must match the `name` field of its `SKILL.md`:

```bash
cp -r template skills/my-skill
```

Set `name`, write a `description` that says what the skill does and when to use it, and fill in `evals/examples.md`. Add the skill to [catalog/skills.yaml](catalog/skills.yaml) and update [catalog/coverage.md](catalog/coverage.md). Generate the profiles, then validate with [uv](https://docs.astral.sh/uv/) and, for the prose tests, [Vale](https://vale.sh) 3.26.0:

```bash
scripts/build-profiles.py
scripts/build-host-config.py --check
./scripts/validate.sh
```

Add the skill to the table in [Skills](#skills). The [authoring guide](docs/authoring-guide.md) sets the bar every skill meets; [AGENTS.md](AGENTS.md) lists the repository rules.

## Contributing and security

Follow the [Code of Conduct](https://github.com/cravingmaker/.github/blob/main/CODE_OF_CONDUCT.md) when participating in the project. Report vulnerabilities privately as described in the [security policy](https://github.com/cravingmaker/.github/blob/main/SECURITY.md).

## License

MIT © [cravingmaker](https://github.com/cravingmaker), except skills that carry their own `LICENSE-*` file for adapted third-party material.
