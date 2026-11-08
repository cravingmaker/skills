---
name: setup-agent-skills
description: "Configure a project's Agent skills block, issue tracker, triage vocabulary, and domain-document paths. Use when the user asks to set up or change that project contract."
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/setup-matt-pocock-skills/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/engineering/setup-matt-pocock-skills/SKILL.md"
  local-changes: "Renamed for owned project setup; made edits idempotent and scoped; preserved configured paths and lazy domain files; replaced CLI mandates with capability discovery; omitted global model sheets, hooks, and bootstrap."
---

# Setup agent skills

Maintain the project's `## Agent skills` contract and its `docs/agents/` files. Read existing configuration first; keep the user's tracker, vocabulary, and domain layout unless this task changes them.

This is project setup, not a prerequisite ceremony for ordinary work. A missing glossary or ADR directory alone does not mean setup is missing.

## Discover the current contract

1. Read the effective project instructions, any `## Agent skills` block, and `docs/agents/issue-tracker.md`, `domain.md`, and `triage-labels.md` that exist.
2. Identify the repository and tracker from existing configuration and safe remote metadata. Keep credentials out of notes and output.
3. Find existing glossary, glossary-map, ADR, and local-ticket paths. A workspace file or several packages is a reason to inspect domain boundaries, not to impose multiple glossaries.
4. Check the installed skill inventory to see whether the `triage` skill is available. Discover sufficient connected tracker tools first; use supported CLI/API equivalents only where needed.
5. Resolve the one project instruction file this setup will maintain. Use the configured target and active host's effective instructions. If both AGENTS.md and CLAUDE.md exist, preserve their existing relationship; edit only the selected target. If neither exists, use the current host's established project target, asking only if that choice remains consequential.

Done when tracker identity, instruction target, domain paths, and any triage mapping are known or explicitly unresolved. Do not dump global host configuration to discover capabilities.

## Resolve only missing choices

Configured values win over remote guesses and template defaults. Reuse supplied answers and current authorization.

- **Tracker.** Keep GitHub, GitLab, local Markdown, or the established other tracker. If no workflow is configured, recommend the remote's tracker when supported; otherwise use local Markdown as a reversible local default. Publishing remains within the task's authority.
- **Triage.** When the `triage` skill is installed, preserve existing role-to-label mappings. For a new mapping use `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix` unless the user chose other labels. Omit a new triage file and subsection when that skill is absent; preserve an existing custom file.
- **Domain.** Reuse the actual configured layout. For a new single-context setup, use `GLOSSARY.md` and `docs/adr/`. Use a glossary map only when distinct contexts justify it. Record the paths now; create semantic files lazily when terms or decisions are resolved.

Ask only choices whose answers would change these outputs. Continue independent local work while a necessary answer is pending. Prior approval is not reopened.

## Maintain the files

Use the seeds only for missing content, replacing examples with actual configured values:

- Read [the GitHub seed](assets/issue-tracker-github.md) only for a GitHub tracker.
- Read [the GitLab seed](assets/issue-tracker-gitlab.md) only for a GitLab tracker.
- Read [the local tracker seed](assets/issue-tracker-local.md) only for local Markdown.
- Read [the domain seed](assets/domain.md) when recording domain paths and consumer rules.
- Read [the triage seed](assets/triage-labels.md) only when recording the installed triage flow.

For another tracker, record its actual supported operations and identifiers in the same project contract.

Maintain one `## Agent skills` section in the selected instruction file:

```markdown
## Agent skills

### Issue tracker

Issues and specs follow the configured workflow in `docs/agents/issue-tracker.md`.

### Triage labels

The configured role-to-label mapping is in `docs/agents/triage-labels.md`.

### Domain docs

Domain paths and consumer rules are in `docs/agents/domain.md`.
```

Omit the triage subsection when no triage contract is being maintained. Update existing matching subsections in place, respecting heading boundaries outside code fences. Preserve other instructions, notes, custom tracker operations, and unrelated sections. Do not add a second block to another instruction file.

In `docs/agents/`, seed missing files and patch only the configuration fields this task changes. Preserve custom prose and existing identifiers rather than replacing an edited file with its seed. Existing nondefault paths stay authoritative. A conflicting duplicate block or contradictory configuration is a gap to resolve, not permission to overwrite both.

Show the resulting diff as the reviewable result. A setup request authorizes its scoped local edits; ask for further approval only when an unresolved choice or action actually needs it. Merely recording a remote tracker does not authorize creating issues, posting comments, or changing labels. Create missing remote labels only if those changes are already authorized.

Host invocation preferences belong to the owned installation tooling. If they are requested, inspect that tooling's current help and supported target before using it. This skill writes no global model rules, provider defaults, startup hooks, always-on routes, branded installs, or upstream-cache edits.

## Check the result

Re-read the maintained files and confirm that their paths, repository identity, label strings, and read/write conventions agree. Check that every block pointer resolves to an intended file. A domain pointer may name a glossary or ADR location that is still absent.

Compare the diff with the intended write set: the selected Agent skills block and its `docs/agents/` configuration only. Reapplying the same choices must leave no new diff, duplicate heading, label, or file.

Done when one consistent contract exists, unrelated content is preserved, lazy domain files remain lazy, and the user has the paths and any tool or authorization limits.

## Provenance

Read [the per-file sources](references/SOURCES.md) when checking attribution, original hashes, destinations, and adaptation.
