# Release policy: <project>

Owner: <name>. Reviewed: <date>.

## Public API

What consumers depend on, and so what a breaking change can touch:

- <library exports, CLI commands and flags, configuration keys, file formats, HTTP or event schemas>
- Supported runtimes and platforms: <list>; dropping one is <major | minor with notice>.

## Versioning

- Scheme: SemVer 2.0.0.
- Before 1.0.0: <breaking changes bump the minor; features bump the patch | other rule>.
- From 1.0.0: breaking → major, feature → minor, fix → patch.
- Prereleases: `<major>.<minor>.<patch>-<rc|beta>.<n>` from branch <name>.

## Commit format

- Conventional Commits; the message checked is <the PR title (squash merge) | every commit>.
- Breaking changes use `!` after the type or a `BREAKING CHANGE:` footer.
- Types that release under the configured engine: <types>. Types that do not release: <types>; test explicit breaking-change markers separately.

## Release

- Tool: <release-please | Changesets | semantic-release>.
- Tags: `<format>`; immutability: <verified target setting and protection scope>.
- Registry publication: <separate job and owner | none>.
- Who approves a release: <role>.
