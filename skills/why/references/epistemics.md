# Epistemics

Read this to calibrate historical claims. Code shows what it does; intent lives in incomplete, sometimes contradictory commits, PRs, tickets, documents, and conversations.

## Claims about human decisions

First identify the component or stage that owns the action and whether the question matters to the current task. Ownership elsewhere can make a question unnecessary, but does not end a relevant cross-component investigation.

When the exact scope of a human ruling matters, locate the person's original attributable words. Keep the source pointer, speaker, and enough wording to establish scope. Label an agent summary or interpretation as such, regardless of age. If the original is unavailable, leave its scope uncertain instead of inventing a restriction or permission.

For example, a temporary endpoint restriction during a migration does not establish a permanent ban. Report the original scope and any broader interpretation separately. Copies of that interpretation are one dependent evidence chain, not independent decisions. Ordinary factual reporting does not require verbatim quotes for every claim.

## Confidence tiers

- **Direct.** An attributable statement explicitly answers why. A PR, ticket, comment, ADR, or conversation names the reason for this target. State it plainly and cite it.
- **Supported.** Independent indirect evidence converges on a conclusion. Cite each contribution and state that the conclusion is derived, rather than attributing an unrecorded decision to a person.
- **Inferred.** A reasonable reading depends on an interpretation. Make the chain explicit: given A and B, C seems likely because D.
- **Speculative.** Several explanations fit thin evidence. Present each useful possibility as a hypothesis, with supporting and missing evidence.
- **Unknown.** The answer is not established. Distinguish searched-with-no-result, unavailable, retention-limited, and unsearched sources.

A change from `limit = 50` to `limit = 100` establishes a code change, not its motivation. An author's statement explaining that change may establish intent. A present-day test result may establish behavior, not historical causation.

## Phrase claims to match the evidence

Words such as `because`, `was designed to`, and `the team decided` imply evidence about intent. Put that source next to the claim. For derived claims, use wording such as `the evidence suggests` or `given A and B, C seems likely`.

Keep uncertainty where it changes the meaning. Removing a hedge can change an inference into an invented fact.

## Avoid rationalization

A design that makes sense today may have been written under different constraints or copied without a deliberate choice. Do not work backward from a tidy rationale.

Treat the user's suggested explanation as one candidate. Search for evidence that could disprove it as well as support it. An observed correlation or consistent pattern alone does not establish intent.

## Handle conflict and gaps

Show both sources when they disagree. A product ticket and PR description may describe different aspects of the work; surface that distinction rather than selecting the cleaner story.

Name the actual searches and their scope. A missing service, inaccessible thread, shallow checkout, or retention cliff is a coverage limit. It is not evidence that a decision never existed.

Before returning, check that each consequential claim has a source or an explicit uncertainty class. Keep genuine gaps visible, without inventing a gap merely to fill a section.
