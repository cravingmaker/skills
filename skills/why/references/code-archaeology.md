# Code archaeology

Read this when repository history or review discussion could establish why the target changed.

## Available record

Use commits, PR discussion, code comments, ADRs, tests, release notes, and linked tickets. History tied to the code is useful, but a shallow checkout, imported snapshot, squash, or inaccessible review can omit the reason.

Prefer sufficient connected repository tools for PRs and issues. Use available local git for focused history; check the actual checkout before assuming it contains the needed revisions.

## Focused searches

With the real target path and identifiers substituted:

```sh
git log --follow --oneline -- <file>
git log -S '<exact_string>' -- <file>
git log -G '<pattern>' -- <file>
git blame -L <start>,<end> -- <file>
git show <commit> -- <file>
git log <old>..<new> -p -- <file>
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <file>
rg -l '<symbol>' --glob '*test*'
```

Read introducing changes and relevant earlier revisions, not only the latest touch. Follow linked PRs, comments, and decisions through the available tools. A test can show the motivating edge case without proving the author's full intent.

Return the exact revisions, paths or review locators, relevant rationale, contradictions, and any missing history. Do not declare all history searched after inspecting one commit.
