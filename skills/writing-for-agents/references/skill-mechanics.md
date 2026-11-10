# Skill mechanics in this repository

Read this when creating or changing a skill, its invocation, dependencies, or provenance. The local AGENTS.md, authoring guide, catalog schema, and current validator remain authoritative.

## One capability and its package

A capability has a distinct trigger, reusable deliverable, evidence standard, and checkable definition of done. Put detail without an independent job in the capability's references. `agent-orchestrator` is the collection's one router: it reads capabilities before use, routes conditional flows, identifies adjacent ownership, and states completion evidence. Keep one owned generic procedure; capability methods supply domain-specific evidence rather than copying its controller.

Use `skills/<name>/SKILL.md`, optional references, scripts, assets, and required `evals/examples.md`. Use the capability template in `template/`, without placing skills inside it. Check the catalog and actual supported host inventory for collisions, including independent built-in reservations.

## Frontmatter and invocation

Use only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. The name matches its directory: 1–64 lowercase letters, digits, and single hyphens, with no leading or trailing hyphen. The description states what the capability does and when to use it, preferably within about 300 characters and always within the spec's 1024-character limit. Keep a trigger per real branch and add near misses for adjacent jobs; a short description is no substitute for reading the body. Metadata values are strings; quote numbers, versions, and space-separated dependencies.

Invocation preference lives in the catalog: `model` by default or `user` when agreed. Generated host adapters carry that preference; host-only frontmatter is not part of SKILL.md. Manual entry is a discovery preference, not an authority boundary or a prohibition on a genuine required dependency. Preserve stricter existing host/user settings and inspect supported installed behavior before changing settings within scope. Authoring a description alone does not establish host discovery or suppression.

## Dependencies and pointers

Declare only real installation prerequisites under quoted, space-separated `metadata.requires`. Use no `metadata.handoffs`; optional related methods are conditional prose. Write cross-skill references as "the `<name>` skill", resolve them through the installed inventory, and read their SKILL.md before use. If a required method is unavailable, name the prerequisite and stop that flow. An optional pointer becomes executable guidance only when its target is available; do not advertise a future owner as shipped. One source of shared reference can support several entries without copying it or making them duplicate capabilities.

## Size, scripts, and evidence

Keep SKILL.md below 500 lines and aim near 200, with roughly 5000 tokens or less. Link detail one level deep from SKILL.md and state when each reference should be read. References over 100 lines need a contents list. Keep static templates in assets and executable helpers in scripts; do not run an asset as if it were a shipped checker. Use self-contained Python 3.12+ standard library or POSIX shell for shipped helpers, with any declared runtime exception explicit. Help exits 0 without effects; document data on stdout, diagnostics on stderr, exits 0 pass, 1 findings, 2 usage, and preview for writes. Exercise meaningful rejecting, accepting, malformed-input, and repeat cases for changed checks. Use the project's existing deterministic mechanism before inventing a helper.

## Provenance and repository integration

Read every selected source file and linked contribution in full before adapting it; hashes alone are insufficient. Use the immutable source revision and exact pre-adaptation hash for each retained contribution. Declare license, one pinned primary source URL, its full SHA, source files, and local changes in metadata. Keep every contributor's complete license, relevant secondary credit and notices, and a header naming the adapted local files. Provide a linked per-file manifest with sources, hashes, destinations, retained material, changes, and legal files; retain reproducible source-to-destination diffs. Excluded or unverified secondary material stays link-only until its actual provenance and reuse terms are established.

Add catalog, coverage, and README entries for new skills, regenerate profiles and owned host files after dependency/invocation changes, and release only the applicable source reservation. Run the pinned skills-ref validator and repository checks on the reconstructed head, with required Vale availability. Keep new or materially changed skills unevaluated until final-skill and no-skill examples have the required matched records. Packaging checks establish package consistency; behavior, authority preservation, and benefit need their own evidence.
