# Authoring guide

Every skill in this repository meets this guide. Workers drafting skills read it in full first; reviewers check against it.

## Two kinds of skills

- **Capability skill.** One capability, one trigger, one reusable deliverable, and a demonstrated benefit over the agent's behavior without it. Named for the capability as a practitioner says it: `api-design`, `postgres-schema-design`, `wcag-audit`. A technology prefix only when the skill is specific to it: `rust-async-services`, `swiftui-architecture`. Knowledge that does not justify its own trigger goes into a capability's `references/`.
- **Role router.** One per role: `backend-engineer`, `agent-orchestrator`. It equips an agent for the role in one invocation and routes the role's work through capability skills. Start from `template-role/`.

## Frontmatter

Only the spec's fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Host-specific behavior belongs in host settings, not here.

- **`description`:** what the skill does and when to use it, one trigger per distinct branch, about 300 characters or less. A role router's description names the role and its invocation ("Equip this agent as a backend engineer... Use when the user invokes backend-engineer or asks the agent to act as one.").
- **`metadata.requires`:** a quoted, space-separated string of skills this one cannot work without. A role router lists its capabilities here.
- **`metadata.handoffs`:** a quoted, space-separated string of optional related skills.
- **`metadata.verified`:** `"YYYY-MM"` when the skill states version-specific facts; sources go in `references/sources.md` with access dates.
- Adapted material: `license`, `metadata.source`, `metadata.source-revision`, `metadata.source-files`, `metadata.local-changes`, and a `LICENSE-<upstream>` file (see AGENTS.md).

## The bar for a capability skill

1. **Decision rules, not persona.** State the expert's frameworks, heuristics, and trade-offs as rules the agent applies. No "You are a world-class...". Every sentence changes behavior compared with the agent's default; delete sentences that do not.
2. **A checkable definition of done** for the deliverable, written as the step's completion criterion.
3. **An evidence standard.** What must be run, measured, or cited before a claim. What must be verified live (versions, platform support, policies, prices, laws).
4. **Pyramid order.** Prefer structural constraints; then static analysis; then executable verification; prose for remaining judgment. Reuse the repository's existing commands and working equivalents; inspect installed versions and update policy; change tooling only within the task's scope. A changed guardrail needs reject, accept, and repeat evidence (see `project-guardrails`).
5. **Failure modes as checks.** The specific mistakes average practitioners make, phrased as things to verify.
6. **Freshness.** No hard-coded versions unless recorded with `metadata.verified` and sources. Prefer instructions that make the agent read the installed version and the official docs.
7. **Safety and authorization** where relevant: written scope before offensive security work; dry runs, reversible changes, and stop points before destructive operations; no personalized financial advice; search-engine spam policies; consumer-protection and privacy law.
8. **Scripts a skill ships** run anywhere the skill is installed: Python 3.12+ standard library with `#!/usr/bin/env python3`, or POSIX shell. The existing `clear-communication` Vale wrapper uses Bash; keep that dependency explicit. Read-only by default, exit 0 pass, 1 findings, 2 usage, with messages that name the fix, and tested in `tests/<skill>/run.sh`. Repository tooling in `scripts/` may use `uv` with pinned dependencies instead.
9. **Size.** `SKILL.md` about 200 lines or fewer; detail in `references/`, linked one level deep.
10. **Evals.** `evals/examples.md` with Activation, Near miss, and Outcome items, and paired runs recorded in `evals/results/` before the catalog marks the skill `evaluated`.
11. **Own words.** roadmap.sh and other copyrighted curricula are coverage references only; their license forbids republishing. Every skill is original text or a properly licensed adaptation.

## Referring to other skills

Write "the `api-design` skill" in prose. Do not write `/api-design` or `$api-design`: invocation syntax differs per host. The agent finds the named skill in its installed inventory and reads that skill's `SKILL.md` before relying on it. When a required skill is not installed, the skill says so plainly and stops that flow; it does not improvise the missing capability.

## Writing

Follow `skills/clear-communication`: lead with the action, plain words, one idea per sentence, one line per paragraph. Use leading words (a compact, pretrained concept repeated as a token) instead of restating a behavior in sentences. Phrase the target behavior positively; use a prohibition only as a guardrail, paired with the positive target. Keep each meaning in one place. Run `./scripts/validate.sh`; it lints this repository's prose.

## Role routers

A router contains, in this order:

1. **Mission and quality bar:** what the role delivers and the standard it holds, in a few lines.
2. **Before relying on a capability:** read its `SKILL.md`; the router's summary is orientation only.
3. **Flows:** the role's common jobs as conditional paths through its capabilities. The agent enters at the step the task needs; a flow is never a mandatory pipeline.
4. **Handoffs:** which role owns adjacent work, and what to hand over.
5. **Done:** the role's completion criteria and the evidence to report.

Every capability a flow names appears in `metadata.requires` (needed) or `metadata.handoffs` (optional), and in the catalog with this role listed.

## Catalog and coverage

Add every new skill to `catalog/skills.yaml` and update `catalog/coverage.md`. `./scripts/validate.sh` checks the catalog against `skills/`, resolves every declared dependency, rejects reserved names, and checks that `catalog/profiles/` matches `scripts/build-profiles.py`.
