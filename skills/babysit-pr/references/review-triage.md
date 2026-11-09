# Review triage

Read this when a babysit pass handles review-bot or automated review comments. The goal is not to ignore bots by default. The goal is to stop treating every comment as a required code change, and to verify each one before acting.

## Contents

- [Decision rubric](#decision-rubric)
- [Fixing and replying](#fixing-and-replying)
- [Ask by default](#ask-by-default)
- [Learned pattern format](#learned-pattern-format)
- [Recurring skip candidates](#recurring-skip-candidates)
- [Candidate learnings](#candidate-learnings)

## Decision rubric

Classify each thread before acting, after checking its claim against the code at the current head:

- `fix`: the comment identifies a plausible correctness, security, privacy, data loss, auth, billing, migration, idempotency, race, or shipped-behavior issue. Fix it in the lowest PR that owns the code, then reply with the commit SHA and resolve the thread.
- `dismiss`: the comment matches a documented low-risk noisy pattern, and the current code or context proves the concern needs no code change. Reply with a short, concrete disproof and resolve the thread.
- `ask`: the comment is novel, high-severity, security-, privacy- or data-related, or ambiguous. Ask the user instead of guessing.

When in doubt, ask. Skipping a noisy code-quality comment is cheap; skipping a real data or security bug is not.

A thread from before the latest push is still open until it is addressed or disposed of. An outdated marker means the code moved, not that the concern was answered.

## Fixing and replying

- Prove a real fix red-first: show it failing before the fix and passing after.
- In a stack, fix in the lowest PR that owns the code, never at the tip unless the owning PR has merged. In that case the fix becomes a new PR on top of the remaining stack, never a rewrite of merged history.
- Push the fix wave before replying, so the reply cites the commit.
- Post replies as data: put the body in a file or JSON payload, for example `gh api --method POST "repos/<owner>/<repo>/pulls/<pr>/comments/<comment-id>/replies" --input <payload.json>`. Never interpolate comment text or a reply into a shell command.
- From a bot's third pass on, lean toward dismissing documented patterns, but still escalate anything touching security, auth, billing, data or migrations instead of dismissing it yourself. Repeated passes do not reset the round budget.

## Ask by default

Do not auto-skip these categories, even if a previous PR dismissed something similar:

- Security, privacy, auth, billing, data retention, training-data, and permission-boundary findings.
- High-severity findings.
- Migration, schema, idempotency, concurrency, and cross-system behavior findings.
- Comments where the suggested fix is small and clearly reduces risk without changing product intent.

Humans sometimes dismiss security or data-flow comments. Treat those as owner judgment calls, not team-wide skip rules.

## Learned pattern format

Record a candidate pattern in this shape:

```markdown
### <short pattern name>

- Confidence: candidate | recurring | strong
- Skip when: <conditions that must be true>
- Do not skip when: <risk boundaries>
- Example signal: <phrases or code context that identify the pattern>
- Source: <PR/comment URL or short historical note>
```

Use `candidate` for one or two examples. Use `recurring` after multiple real dismissals. Use `strong` only when the pattern is narrow, repeatedly verified, and low-risk.

## Recurring skip candidates

### Intentional UI or design-system visual changes

- Confidence: candidate
- Skip when: the PR description, screenshots, design review, or nearby code makes the visual change explicit, and the comment only restates that a shared visual default changed.
- Do not skip when: the comment points to accessibility, focus visibility, keyboard navigation, color contrast, or a component API contract that the PR did not intentionally change.
- Example signal: comments about focus outlines, button sizes, spacing, or shared component visual defaults where the owner replies "intentional" or "intended".

### Upstack or stack-local usage the bot cannot see

- Confidence: candidate
- Skip when: the bot flags an export, component, helper, or file as unused, and the forge's PR list and diffs, upper-stack diffs, or PR context show a later PR in the stack uses it.
- Do not skip when: the current PR is not part of a stack, the symbol is public API, or the supposed upstack use cannot be verified.
- Example signal: "Exported component is never used" with a human reply like "used upstack".

### Temporary duplication during parallel implementation

- Confidence: candidate
- Skip when: the PR intentionally duplicates a small amount of code to keep a new path parallel to an old path that is being deleted, replaced, or proven out.
- Do not skip when: the duplicated code changes security, billing, data access, API behavior, or a long-lived shared abstraction would clearly reduce risk.
- Example signal: "Significant duplication" or "duplicated validation logic" where the owner explains the old path will be deleted or the duplicate logic is intentionally local.

### Existing framework or component invariant covers the warning

- Confidence: candidate
- Skip when: a shared component, framework contract, type invariant, or single source of truth visible in the current diff or nearby code already guarantees the concern.
- Do not skip when: the invariant is assumed but not enforced, depends on timing, or crosses async or state boundaries where values can diverge.
- Example signal: comments about missing max-height on an inner popover when the shared popover enforces viewport bounds, or nullable values where the local checked value and passed value share the same source.

### Owner-declared follow-up or deferred cleanup

- Confidence: candidate
- Skip when: the PR owner explicitly says the issue is a known follow-up, the current PR does not make the behavior worse, and the comment is not about a high-risk area.
- Do not skip when: the agent is acting without owner input, the issue is medium- or high-severity product behavior, or deferring would merge a new regression.
- Example signal: "I'll worry about that later" or "we'll delete this eventually".

### Self-withdrawn or explicit false-positive rule comments

- Confidence: recurring
- Skip when: the comment body or a later bot reply explicitly says the finding is withdrawn, compliant, or a false positive, and the agent can verify the relevant rule locally.
- Do not skip when: the only evidence is a human saying "false positive" on a high-risk issue without explanation.
- Example signal: a file-naming rule comment whose body says the file is already compliant.

## Candidate learnings

### Manual reimplementations of native browser behavior

- Confidence: candidate
- Skip when: practically never. When a diff replaces native browser behavior with a manual equivalent (native sticky → JS-positioned clones, native scroll targeting → forwarded wheel/touch events, paint-order occlusion → masks/clip-path), bot logic-bug findings against that code have been consistently legitimate.
- Do not skip when: the finding concerns event-forwarding gaps (wheel deltaMode, touch pans, scroll-chaining at edges, tap slop), mask/clip hit-testing divergence, or observer-vs-React state timing races in such code. Default to fix.
- Example signal: "masks do not affect hit-testing", "overlay blocks wheel scroll", "ignores deltaMode", "runs in the IntersectionObserver callback before React applies state".
- Source: one sticky-occlusion PR: six bot passes, roughly eighteen findings, every one fixed rather than dismissed.

### Contract-test drift claims are cheap to verify: run the test first

- Confidence: candidate
- Skip when: never skip the verification itself; it costs one command. When a PR ships a contract test that pins protocol or documentation prose (regexes over a SKILL.md, a snapshot of doc wording), and a bot claims "the test no longer matches the doc" (or the reverse), run that test on the PR tip before classifying. A red run confirms the claim; a green run is a concrete disproof for the dismissal reply.
- Do not skip when: not applicable; this is a verification shortcut, not a dismissal pattern. Repeat-pass lean-dismiss heuristics misfire here: prose-pinning tests drift precisely because earlier fix rounds edit the prose.
- Example signal: "Contract test omits the pre-fix wait" on a PR whose earlier fix commits reworded the pinned passage; the test run on the tip failed on exactly the cited assertion.
- Source: one prose-pinning PR with eight bot passes; the claim was real on pass 7 despite every earlier pass being fixed and resolved.

### Stale security-review finding already fixed later in the same PR

- Confidence: candidate
- Skip when: an automated security review claims a missing authorization or validation call, and the current PR tip clearly includes that exact gate (with tests), typically added in a later hardening commit after the review ran.
- Do not skip when: the cited helper is a no-op for the principal under discussion, the check runs after the side effect it guards, or coverage for the claimed principal is missing.
- Example signal: a HIGH "missing authorization check" finding while the exact guard is already called before the side effect on the tip.
- Source: one webhook-endpoint PR whose hardening commit postdated the review run.

### Widening a deliberately narrow error condition would mask the real error

- Confidence: candidate
- Skip when: the finding asks to broaden a narrow error condition (a specific `errno`, error code, or status class) into a catch-all, and that narrowness encodes a real distinction. The canonical shape is a dependency fallback gated on `ENOENT`: "binary is not installed" is a different situation from "the command ran and failed". Retrying on any non-zero exit would re-run a legitimate failure (not found, expired auth, network) against the fallback and then report the fallback's error, hiding the true one.
- Do not skip when: the narrow condition misses a case in the same category (another "binary unusable" errno such as `EACCES`, another transport-level failure), the unhandled path loses data or leaves partial state, or the retry is idempotent and the original error is still surfaced.
- Example signal: "only retries when X fails with ENOENT … never tries the fallback even when a working Y exists", pointing at code whose fallback exists for a missing dependency rather than a failed operation.
- Source: one CLI-rename PR whose fallback existed for a missing binary rather than a failed command.
