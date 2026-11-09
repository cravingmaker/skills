# Decision record integrity

Read this when selecting an ADR checker or interpreting its findings.

Use the repository's configured directory and format. The helper reads numbered Markdown names such as `0001-storage.md` or `ADR-0001-storage.md`; unrelated index pages are excluded. An empty scan is a finding. Numbers are unique across the directory and its subdirectories.

Supported status forms are a scalar frontmatter field, `Status: accepted`, a Markdown list field, or a `## Status` section. Recognized states are proposed, accepted, rejected, deprecated, and superseded. Short records without status remain `recorded`; this reports missing lifecycle classification without inventing acceptance. Under `--base`, their recorded reasoning is conservatively immutable too. The helper is not a general YAML parser; use a native checker for nested or custom metadata.

Declare `Supersedes:` and `Superseded by:` fields or sections using relative Markdown links, `ADR-NNNN`, or a bare number. A status such as `superseded by ADR-0002` also supplies the successor. Require present local targets and an acyclic successor chain. Effective supersession needs reciprocal links. A proposed or rejected replacement may name its predecessor without changing the current decision; a proposed or rejected record cannot become the active successor. Updating lifecycle fields leaves the accepted rationale unchanged.

`--base REF` resolves a commit and compares every historically accepted, deprecated, superseded, or statusless record. Deleting, renaming, or editing its reasoning fails. Only status and supersession metadata are excluded from the comparison. Frontmatter delimiters do not count as reasoning; all other fields and content do. A newly accepted file or any transition to accepted requires `--signed-off NUMBER` with `--base`; repeat the flag for multiple records. This is an explicit acknowledgement after user sign-off, not independent evidence of it. Without a trusted base the helper cannot distinguish a historical acceptance from a new one.

Use `--require-confirmation` only when the repository requires that field or section. Without the flag, a short ADR need not acquire a new section to pass. An empty, comment-only, or placeholder Confirmation such as TBD reports false in JSON. Inspect the linked evidence separately; a sentence promising a test is not an observed test result.

Output is JSON with `base`, `scanned`, `records`, and `findings`. Exit 0 means the selected mechanical checks passed, 1 means findings, and 2 means invalid or unreadable input. No record is rewritten.

The historical-record method is informed by [Nygard's ADR essay](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) and [ADR practices](https://adr.github.io/ad-practices/). These are cited methods; no upstream template is copied.
