# Review lenses

Use these lenses on changed behavior and affected callers, under the Standards or Spec axis that supports the finding.

## Standards and structure

Treat smells as questions to investigate, with the repository's documented choices taking precedence. A count of lines, adapters, duplicate reports, or branches cannot decide whether a change is wrong.

| Cue | Question and possible remedy |
| --- | --- |
| Mysterious name | Does the name reveal its domain meaning? Rename only when the new name makes the actual contract clearer. |
| Duplicated code | Do the copies share one invariant and reason to change? Reuse a canonical owner when that preserves behavior. |
| Feature envy | Is behavior reaching through another owner's internals? Consider moving the behavior to that owner. |
| Data clumps | Do the same fields travel together as one concept? Consider a small domain type. |
| Primitive obsession | Does a primitive hide a domain constraint? Prefer an honest type with required runtime validation. |
| Repeated switches | Do repeated branches encode one policy? Consider a shared model or dispatch point. |
| Shotgun surgery | Does one logical change require scattered consumer edits? Check ownership and compatibility before moving code. |
| Divergent change | Is one module changing for unrelated reasons? Consider a cohesive split. |
| Speculative generality | Do new options, hooks, or layers serve an actual requirement? Suggest removing unused flexibility. |
| Message chains | Does the caller depend on another module's internal walk? Consider an interface that hides it. |
| Middle man | Does delegation hide useful complexity or merely add a hop? Preserve a real compatibility or security seam. |
| Refused bequest | Does an implementation discard its inherited contract? Check substitutability and consider composition. |

Look for simplifications that remove concepts, scattered policy branches, or duplicate ownership while preserving the public contract. Moving complexity to more files does not itself simplify it. Check thin wrappers, optional states, casts, shared-helper duplication, feature logic in general paths, and partial updates for a concrete maintenance or correctness cost. Parallel work is useful only when independence and resource ownership are real; required serialization and defensive validation can be the correct design. Give design advice a proposed alternative and its trade-off, without turning an attractive rewrite into a review blocker.

## Correctness, security, and developer setup

Trace caller-to-callee effects across packages, initialization, teardown, errors, retries, cancellation, and concurrent state updates. Check schema and migration compatibility, exported types and runtime exports, data fidelity, build/install flows, and independently deployed consumers. Validate privilege transitions and feature gates from the caller through the enforcement point; an internal caller may still cross a trust boundary. Inspect changes to environment names, secret-loading mechanisms, ports, networking, and required setup steps for developer regressions; keep secret values out of evidence. Distinguish an explicitly accepted removal from an unintended consequence; report undisclosed security or data-loss consequences by their actual impact. Finish available client/server tracing before reporting; inaccessible evidence belongs in the limitations.

## Feedback and attribution

For an independent panel, complete the initial audit before reading other reviewers' conclusions. Then read relevant existing discussion with supported connected tools, validate its claims, attribute retained evidence, and keep unresolved feedback visible. Repetition identifies a shared root cause; it is not a vote that establishes truth or severity. Keep useful detailed evidence in an existing report location when one is requested; scale the summary to the task instead of imposing a report directory or line count.
