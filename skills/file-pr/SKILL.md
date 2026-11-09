---
name: file-pr
description: Write a pull request title and body grounded in the actual diff, as a local draft by default, and create or update the PR only when that is asked for or already authorized. Use when the user asks to write or fix a PR description, or to file, open, create or update a pull request.
license: MIT
metadata:
  requires: "clear-communication"
  source: https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/file-pr/SKILL.md
  source-revision: 1085050f3baed1ac724caa4a8166145fb2ac88af
  source-license: "MIT; see LICENSE-tstack, LICENSE-mattpocock, LICENSE-humanlayer, LICENSE-pstack, LICENSE-pstack-claude, LICENSE-cursor-team-kit and NOTICE-pstack-claude.md"
  source-files: "skills/file-pr/SKILL.md"
  local-changes: "Added a body-only default with no remote mutation; repository template and merged PRs decide the body style; dropped mandatory model branding, fixed section counts, always-ready status, comment stripping and Cursor/Origin/Graphite tooling; connected tools before the gh fallback; filing never starts a watch; added the shared delivery contract."
---

# File PR

A PR body is a short briefing for a reviewer who has the diff. This skill writes one from the actual change, and files or updates the PR only when that is asked for or already authorized.

## Choose the mode

- **Body only** (the default): a request to write, draft or improve a PR title or body. Write them locally and return them. Push nothing, create or edit no PR, post no comment and start no watch.
- **File or update**: the user asked to file, open, create or update the PR, or the current task already authorizes it, such as the `full-send` skill's finish mode. Make the remote change, then return the link and the current state.

Writing a body grants no filing. Filing grants no push to other branches, no merge and no watch. A narrower user or repository constraint wins.

When the task runs in no-merge mode (the `full-stop` skill), keep it: never enable auto-merge or add the PR to a merge queue.

## Ground it in the change

1. Find the base: the existing PR's base, or the repository's default branch. Fetch it. Check whether a PR already exists for this branch, and update that one instead of opening a second.
2. Read the full diff against the base, the commits, and the user's original request. Confirm the contents match the goal. Name or split out unrelated changes; never hide a behavior change inside "cleanup".
3. Read the repository's PR template, its contributing guide and several recently merged PRs. Their title convention and body style decide the shape. The sections below apply only where the repository has no convention.
4. Use the project's domain terms, from its glossary when it has one. Write in the house style of the `clear-communication` skill.
5. Check the title, body, quotes and attachments for secrets and private details.

## Title

PR titles usually become commit messages, so follow the repository's convention, for example Conventional Commits `type(scope): subject`. Prefer a short, human-readable title that says why the change matters:

> Bad: perf(server): negotiate permessage-deflate on the websocket
>
> Good: perf(server): cut websocket frame size by 70%+ with gzipping

## Body

Open with the problem in the user's terms, then the solution. Do not lead with an implementation inventory:

> Bad: Removed implicit workspace carry-over from every "new thread" entry point (cmd+n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads inherit only the project from context; branch, worktree, and env mode always come from the configured defaults. Deleted buildContextualThreadOptions, startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.
>
> Good: My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

Where the repository has no convention, use these sections in this order and drop any with nothing to say:

- **Why:** the problem and the approach, in one to three short sentences. No SHAs, rebase history or "based on main" preamble.
- **What changed:** one to three bullets. Name a symbol or path only when it carries the change; name both sides of a rename or retarget.
- **Scope:** what it covers and what it deliberately leaves out.
- **Evidence:** proof that the change works, in proportion to its risk. A before-and-after screenshot is the best evidence for a visual change when the environment can produce one. For other changes, show command output or the exact test that failed before and passes now. Every claim refers to the current head.
- **Risk:** is the change a one-way or a two-way door, and what is its blast radius: who or what it touches, and why that is safe or risky. A cheap rollback is a two-way door; a destructive or hard-to-reverse change is a one-way door.
- **Tradeoffs:** only rejected alternatives a reviewer would otherwise ask about.

Keep the body short; it often becomes the squash commit body. Full SHAs, run logs and file-by-file checklists go in a linked artifact, not the body.

When a picture makes the change clear faster than prose, add one small visual next to the text it supports. Read [references/visual-summary.md](references/visual-summary.md) when choosing one.

To make an existing PR easier to review (a stale description, noisy commits, mixed mechanical and logic changes), read [references/reviewability.md](references/reviewability.md). History cleanup needs the user's go-ahead and a tree check.

## Credit and attribution

The visual method retains [Matt's credit note](references/credits.md) and LICENSE-humanlayer.

Preserve original authorship and existing co-author trailers, and credit the original contributors when continuing someone else's work. Add model or harness attribution only when the user or the repository convention asks for it.

## File or update

Only in file-or-update mode:

1. Use the host's PR tool or a connected forge tool when one is available and covers the operation. Otherwise use the `gh` CLI. If `gh pr create` fails because the GraphQL rate limit is used up, use REST: `gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@<file>`.
2. Open the PR ready or as a draft as the user or the repository convention says. A ready PR starts review bots; a draft often does not.
3. For a stack, the root PR targets trunk and each child targets its parent's branch. Return every created or updated layer.
4. Read the PR back: link, state, draft flag, head SHA, base, and checks and unresolved threads at that head. When the host links PRs to the session, link every layer you created or updated.
5. Post no follow-up comment unless it serves the request. For one that does, use the `leaving-pr-comments` skill.

Filing ends with the link and state. Monitoring is a separate request: only the root agent continues with the `babysit-pr` skill, and only when the user asked for monitoring or an authorized action is still pending.

## Delivery contract

- Bind every check result, proof and readiness claim to the current head and base. A result for an older head or base is history, not evidence.
- An unresolved review thread stays relevant, whatever its age or the pushes since, until it is addressed or explicitly disposed of with a written reason.
- Required checks, bots and approvals come from repository policy: branch protection, rulesets, CODEOWNERS and documented process. A vendor name or model confidence never makes a gate optional.
- Run at most three review/fix rounds. A larger bounded allowance applies only if it was declared before the run. Renaming or rewording a finding never resets the count.
- Only the root agent watches a PR, and only on a monitoring request or while an already authorized action is pending. Filing alone returns the link and current state. A child returns state and never watches.

## Done

- **Body only:** the title and body are returned, match the diff and the repository's style, and nothing remote changed.
- **Filed or updated:** the link to every created or updated layer, with its head SHA, base, draft flag, current checks and unresolved threads. No watch was started by filing.

Provenance and the per-file manifest: [references/SOURCES.md](references/SOURCES.md).
