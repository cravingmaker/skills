# Legacy characterization

Read this when a refactor needs a record of reviewed current behavior.

Capture a small set of representative inputs and outputs from the current implementation at its real boundary. Review every retained fixture, including errors, nulls, precision, ordering and nondeterministic fields. Label the fixtures as current behavior; an existing defect does not become a product requirement because it appears in a snapshot. Keep private inputs and unstable credentials out of captured artifacts.

Normalize only fields declared irrelevant to the behavior, such as an explicitly nondeterministic trace identifier. Keep amounts, signs, field presence, nulls and meaningful ordering exact. Record the normalizer and original capture identity so a reviewer can inspect what it removed.

Use a behavior-preserving refactor as an acceptance case and a meaningful changed output as a rejecting case. A broad snapshot that no one reviewed cannot supply an independent expected result. For business rules, add hand-derived expected cases beside characterization fixtures.

Run the same selected cases through old and new code with fresh isolated fixtures. Classify each difference as a defect, an intended approved change or an unknown requiring investigation. Replace temporary characterization cases with stronger semantic assertions when the behavior is understood; give remaining snapshots an owner and removal condition.

Use the `tdd` skill for implementing a new behavior; this reference supplies an old-behavior fixture mode only.
