# ADR format

Read this when writing or superseding an ADR.

ADRs live in the ADR directory the project's domain setup names, numbered in sequence: `0001-slug.md`, `0002-slug.md`. Create the directory only when the first ADR is needed. An existing project ADR format wins over this one.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

An ADR can be a single paragraph. Its value is recording that a decision was made and why, not filling out sections.

## Optional sections

Include these only when they add real value:

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`): useful when decisions are revisited.
- **Considered Options:** only when the rejected alternatives are worth remembering.
- **Consequences:** only when non-obvious downstream effects need calling out.

## Numbering

Scan the ADR directory for the highest number and add one.

## Changing a decision

An accepted ADR is immutable. Write a new ADR that states the new decision and names the one it replaces. Then change only the old ADR's status to `superseded by ADR-NNNN`. Its text stays as written, so the history of the reasoning survives.

## When to offer an ADR

All three must be true:

1. **Hard to reverse:** changing your mind later costs something meaningful.
2. **Surprising without context:** a future reader will look at the code and wonder why on earth it was done this way.
3. **A real trade-off:** there were genuine alternatives and one was picked for specific reasons.

If a decision is easy to reverse, skip it: you will just reverse it. If it is not surprising, nobody will wonder why. If there was no real alternative, there is nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library: only the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no's are as valuable as the yes's.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it; otherwise someone will suggest GraphQL again in six months.

### What does not qualify

- Implementation details a reader can see in the code.
- Choices inside one multi-agent run; those belong to the run's decision records.
