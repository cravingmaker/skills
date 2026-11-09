# Rationale template

Read this when writing the rationale that ships with a type sketch. One page, sentence-case headings, no boilerplate. Replace the italic notes with actual content. Adapted from pstack's architect/references/rationale-template.md and the pstack-claude port's reconciliation section.

## Problem

*One paragraph. What we're trying to do, and what about the existing system or constraints makes the shape non-obvious. Name the constraints Phase A surfaced (existing types to interoperate with, callers we can't break, invariants, trust boundaries) so the reader sees the same constraints you saw.*

## Usage (caller's view)

*Write this first, before the type sketch. Show the README or quickstart the consumer reads, plus two or three realistic call sites in their own code: what they import, what they call, what comes back. The type sketch in [Shape](#shape) is derived from this, and the two must agree; when they diverge, reconcile the sketch to the usage. The caller's experience is the spec.*

## Shape

*The recommended architecture. Data structures first, then how data flows through the signatures. Name the load-bearing decisions. State which invariants are encoded in types, where validation lives, and what the system deliberately does not do. Judge interface depth explicitly: what complexity the public surface hides, what remains exposed to callers, and why the interface is no larger than needed. Cite the principle behind each decision (for example, "validate at trust boundaries") without restating it.*

## Synthesis decision

*How the chosen design was reached. When the `agent-debate` skill produced the candidates, record its result: which candidate became the base and why, what was grafted from the others, and what was rejected and why. When you wrote the candidates yourself, say so and record the same three things.*

## Tradeoffs accepted

*One bullet per tradeoff the chosen shape makes, in the form "we accept X in exchange for Y". Name anything a future reader might mistake for an oversight, including things that look like premature optimization or premature simplification.*

## Alternatives considered

*Required. Name at least one concrete alternative shape, with one line on why it lost. Judge each alternative on interface depth, not implementation simplicity alone: the complexity it exposes to callers and the complexity it hides. Two or three alternatives belong here when the design space had real contenders. One is fine when the constraints forced the answer, phrased as "this was the only viable shape because...". Avoid listing flavors of the same shape.*

## Implementation reconciliation

*During implementation, record accepted deviations and their acceptance sources here, and update the affected usage, outcome contracts, signatures and ownership in this design. Record why local deviations leave the shared contract valid. Keep unaccepted changes unresolved. Reconcile before closing a unit or handing its contract to the next worker.*

## Open questions and risks

*Things the human needs to weigh in on, and risks worth flagging before implementation starts. Phrase them as questions, so the human's answer is the resolution.*

## Next implementation step

*The first thing to build against the sketch, in one sentence.*
