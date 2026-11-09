# Issue tracker: GitHub

Seed for `docs/agents/issue-tracker.md`. Replace the repository example with the configured identity and preserve existing custom operations.

Repository: `<owner>/<repo>`.

Issues and specs live in that repository's GitHub Issues. Use sufficient connected GitHub tools first. Where needed, use supported CLI/API equivalents after checking the installed tool's help and access.

## Operations

- **Read.** Fetch an issue's number, title, complete body, labels, state, and relevant comments.
- **List.** Scope by repository, state, and configured labels. Follow pagination before claiming complete coverage.
- **Publish.** Create a GitHub issue only when publication is authorized. A draft can remain local.
- **Comment, label, or close.** Use the operation supported by the current tool and task authority. Record the explanation before a close when the flow requires one.
- **Parent and blockers.** Prefer supported native sub-issues and issue dependencies. Resolve their actual identifier requirements before writing. If unavailable, retain `Part of #<parent>` and a task list in the parent, with an unambiguous `Blocked by: #<n>, #<n>` or `Blocked by: None` line in each child.

GitHub shares issue and PR numbers. Resolve whether a reference names an issue or PR rather than assuming.

## Pull requests as a triage surface

**PRs as a request surface: no.**

Set this to yes only when the project's triage contract includes external PRs. In that mode, read the PR body, diff, comments, and reviews; apply the configured states within existing authority.

## Wayfinding operations

The map is one issue with Notes, Decisions-so-far, and Fog. Keep child decision tickets separate from delivery tickets. A child's type is `research`, `prototype`, `grilling`, or `task`; the configured label may be `wayfinder:<type>`.

List the map's open children in map order. A child is eligible only when all known blockers are complete and it is unclaimed. Claim before work only within current tracker authority; preserve existing assignments.

After the question is resolved, record its answer and evidence, then its configured completion state and a gist plus link in the map. Decision completion does not authorize implementation or delivery-ticket closure.
