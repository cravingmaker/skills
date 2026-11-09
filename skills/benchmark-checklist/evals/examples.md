# Examples

Run matched fresh arms with and without the final skill using the same harness, data, environment and finite measurement budget; keep raw samples and control runs.

## Activation

- "Is this measured 30% export speedup believable?" Expect: inspect timing scope, units, denominator, comparable sides, completed/correct/error counts, limiter and uncertainty before accepting the sentence.
- "Benchmark these two implementations before we choose one." Expect: realistic comparable tuning, alternating repeated runs, sensitivity/negative controls and end-to-end relevance.
- "Check the regression number from our macOS runner." Expect: project-native supported tooling rather than an assumed Linux-only command set.

## Near miss

- "Explain the asymptotic complexity of this algorithm." Expect: theoretical explanation without inventing measured performance or starting a benchmark.
- "Format this table of quarterly revenue." Expect: formatting only, without activating a performance measurement workflow.

## Outcome

- "Candidate looks faster because half its requests return errors." Expect: retain error and work counts and reject the speedup claim on successful comparable work.
- "The timed generator is never iterated, and the sensitivity control adds no observed cost." Expect: identify that the timed work did not happen and keep the verdict inconclusive.
- "Baseline runs untuned debug defaults while candidate uses release batching." Expect: no implementation/adoption winner until representative configurations can be compared.
- "The measured gap is smaller than the variation across alternating independent runs." Expect: no measurable difference with run count/spread and raw samples, without unsupported causal claims or unbounded sampling.
- "A micro helper improves 50% but occupies 1% of a user request." Expect: report the helper's baseline and units plus end-to-end share; do not call the whole request 50% faster.
- "Give me one quick ballpark for this fixture." Expect: one labeled run may suffice after correctness and completed-work checks; no comparative winner or repeatability claim.
