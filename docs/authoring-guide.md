# Authoring guide

Every skill in this repository meets this guide. Workers drafting skills read it in full first; reviewers check against it.

## Two kinds of skills

- **Capability skill.** One capability, one trigger, one reusable deliverable, and a demonstrated benefit over the agent's behavior without it: run the examples without the skill first, and write it only when that baseline fails. Named for the capability as a practitioner says it: `change-review`, `diagnosing-bugs`, `to-spec`. A technology prefix only when the skill is specific to it. Knowledge that does not justify its own trigger goes into a capability's `references/`.
- **Router.** `agent-orchestrator` is the one router: it equips an agent in one invocation and routes its work through capability skills.

## Frontmatter

Only the spec's fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Host-specific behavior belongs in host settings, not here.

- **`description`:** lead with the main use case, then what the skill does and when to use it, one trigger per distinct branch, about 300 characters or less. A router's description names what it equips the agent to do and how it is invoked.
- **`metadata.requires`:** a quoted, space-separated string of skills this one cannot work without. A router lists its capabilities here.
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
8. **Scripts a skill ships** run anywhere the skill is installed: Python 3.12+ standard library with `#!/usr/bin/env python3`, or POSIX shell. The existing `clear-communication` Vale wrapper uses Bash; keep that dependency explicit. Read-only by default, exit 0 pass, 1 findings, 2 usage, with messages that name the fix, and tested in `tests/<skill>/run.sh`. Every shipped executable answers `--help` with usage and exits 0 without inspecting a host or writing. Describe exit codes and output; use stdout for results and help, stderr for diagnostics. Emit JSON when a caller parses the result. Use no interactive prompts; preview mutations before explicit apply. Test installed scripts separately from assets and templates, which are data. Repository tooling in `scripts/` may use `uv` with pinned dependencies instead.
9. **Size.** Aim for about 200 lines and about 5000 tokens or fewer in `SKILL.md`; the hard limit remains under 500 lines. Put detail in `references/`, linked one level deep. Read a reference only when its stated condition applies. A reference over 100 lines starts with a table of contents.
10. **Evals.** `evals/examples.md` with Activation, Near miss, and Outcome items, and paired runs recorded in `evals/results/` before the catalog marks the skill `evaluated`.
11. **Own words.** roadmap.sh and other copyrighted curricula are coverage references only; their license forbids republishing. Every skill is original text or a properly licensed adaptation.

## Referring to other skills

Write "the `api-design` skill" in prose. Do not write `/api-design` or `$api-design`: invocation syntax differs per host. The agent finds the named skill in its installed inventory and reads that skill's `SKILL.md` before relying on it. When a required skill is not installed, the skill says so plainly and stops that flow; it does not improvise the missing capability.

The catalog checker scans this form in `SKILL.md` and its directly linked owned references and assets. It checks owned names and supported external inventory; it does not install optional skills. For an external provider qualifier, write "the upstream `api-design` skill" only when that provider lists the name. Use one pointer per skill, including coordinated references. Fenced code and explicit `<name>` or `{{name}}` placeholders are examples, not routes. Enclose a historical name crosswalk in `<!-- skill-names: historical -->` and `<!-- skill-names: end -->`; keep executable routes outside that region.

## Invocation and composition

Set `invocation: user` in the catalog for an entry the user selects explicitly; omit it for the `model` default. Preview/apply `scripts/build-host-config.py` in the source repository and check the generated Codex policy before installing. Claude settings are a separate explicit adapter step; see [installing.md](installing.md). Invocation preference adds no authority and does not prohibit a genuine `requires` edge.

Keep generic planning, execution, review and verification in their owning capabilities. Add no router for a second generic workflow.

## Provenance manifests

Link `references/SOURCES.md` directly from `SKILL.md`. Start it with `# Sources` and use one Markdown table with these columns in this order; a linked `references/sources.csv` with the same header is also supported:

```text
source,source_url,source_path,source_revision,sha256,license,copyright_holders,destination_paths,kept_material,local_changes,license_files,notice_files
```

Use one row per retained upstream file: a contributor identifier, absolute URL, upstream path, full 40-character revision, exact 64-character SHA-256 of the pre-adaptation bytes, license, all copyright holders, local destinations, retained method, changes, and every applicable legal file. Separate multiple local paths or holders with semicolons; use `none` for absent notices. Declare non-empty string `metadata.source-files` and `metadata.local-changes`; the primary URL/revision and source paths must appear in the manifest. Keep each contributor's complete original `LICENSE-<source>` text under a header starting `Adapted files:` or `Adapted material:` and naming all receiving local files. Preserve applicable notices. Apache material requires its NOTICE and changed-file markings.

Include commands in the manifest to export each pinned input, verify its byte hash and reproduce its diff against the destinations. Automated checks establish header, existence and schema consistency; a reviewer checks source identity, complete legal text, secondary attribution and contributions from prompts/assets. A valid hash-shaped string alone does not prove byte identity.

## Writing

Follow `skills/clear-communication`: lead with the action, plain words, one idea per sentence, one line per paragraph. Use leading words (a compact, pretrained concept repeated as a token) instead of restating a behavior in sentences. Phrase the target behavior positively; use a prohibition only as a guardrail, paired with the positive target. Keep each meaning in one place. Run `./scripts/validate.sh`; it lints this repository's prose.

## Routers

A router contains, in this order:

1. **Mission and quality bar:** what the router delivers and the standard it holds, in a few lines.
2. **Before relying on a capability:** read its `SKILL.md`; the router's summary is orientation only.
3. **Flows:** its common jobs as conditional paths through its capabilities. The agent enters at the step the task needs; a flow is never a mandatory pipeline.
4. **Handoffs:** which skill or person owns adjacent work, and what to hand over.
5. **Done:** its completion criteria and the evidence to report.

Every prerequisite a flow needs appears in `metadata.requires` and in the catalog with this router listed. Optional routes stay in conditional prose and do not change installation closure.

## Catalog and coverage

Add every new skill to `catalog/skills.yaml` and update `catalog/coverage.md`. `./scripts/validate.sh` checks the catalog against `skills/`, resolves every declared dependency, rejects reserved names, and checks that `catalog/profiles/` matches `scripts/build-profiles.py`.
