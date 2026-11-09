# Spec template

Read this before writing a spec. Fill every section; write "None" in a section that has nothing.

```markdown
## Problem Statement

The problem the user is facing, from the user's perspective.

## Solution

The solution, from the user's perspective.

## User Stories

1. As a <actor>, I want a <feature>, so that <benefit>
   - **Acceptance:** <observable condition>; <observable condition>
   - **Proof:** <surface to drive or source to open> → <result to observe>

## Implementation Decisions

- <decision>

## Testing Decisions

- <decision>

## Domain Pointers

- <glossary term or ADR, with its path or link>

## Out of Scope

- <thing>

## Open Questions

- <question>, decided by <who>

## Sources

- <path or link> <sha256:… for files>

## Further Notes

<notes>
```

## Section rules

**User Stories.** A numbered list that covers every behavior in scope. Example:

```markdown
1. As a mobile bank customer, I want to see the balance on my accounts, so that I can make better informed decisions about my spending
   - **Acceptance:** each account shows its current balance; a failed fetch shows "Balance unavailable", not zero
   - **Proof:** open the accounts screen in the app with the seeded test customer → the three seeded balances appear, and with the balance service stopped the screen shows "Balance unavailable"
```

**Implementation Decisions.** Decisions already made, such as:

- the modules that will be built or modified, and their interfaces
- technical clarifications from the developer
- architectural decisions, schema changes, and API contracts
- specific interactions

Leave out file paths and code snippets; they go stale fast. Exception: when a prototype produced a snippet that encodes a decision more precisely than prose (a state machine, a reducer, a schema, a type shape), inline the decision-rich part and note that it came from a prototype.

**Testing Decisions.**

- What makes a good test here: test external behavior, not implementation details.
- The agreed seams, and which modules are tested at them.
- Prior art: similar tests in the codebase.

**Domain Pointers.** The glossary terms and ADRs a builder must read, so they use the project's language and respect its decisions.

**Out of Scope.** What this spec does not cover.

**Open Questions.** Only points that remain open after the agreed understanding, each with who decides it. A spec with open questions is filed as a draft until they are settled.

**Sources.** Every document the spec relies on, bound by path or link and, for files, by SHA-256, so a later reader knows exactly which versions it was written against.
