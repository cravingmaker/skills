# Quality scenarios

Read this when a review request uses broad terms such as reliable, maintainable, or fast.

Write a scenario with a source, stimulus, affected artifact, environment, response, and response measure. Reuse agreed thresholds; ask for a consequential missing requirement rather than inventing one. An example with no agreed target is an illustration, not an acceptance criterion.

A concrete recovery scenario can use these fields; take its threshold from the project rather than treating this illustration as an agreed objective.

| Field | Example |
| --- | --- |
| Source | Payment worker |
| Stimulus | Crash after database commit, before acknowledgement |
| Artifact | Charge job and order state |
| Environment | Declared workload and replica topology |
| Response | Resume without losing or duplicating the acknowledged effect |
| Measure | Exact final state matches the oracle within the agreed recovery objective |

Group scenarios by the quality they exercise, then prioritize by business importance and technical uncertainty. Use ISO's [product quality model](https://www.iso.org/standard/78176.html) only when a shared quality vocabulary is needed. Verify the applicable edition before stating its taxonomy. No edition-specific list is cached here.

For recovery, trace a crash after commit but before acknowledgement and compare the final durable result with an independent oracle. For modifiability, trace a real substitution through affected callers instead of counting interfaces. For latency, name arrival pattern, payload, concurrency, cache state, errors, and resources.

Map each scenario to a tactic and evidence. Identify sensitivity points and trade-off points, then keep untested assumptions as probes with owners and stop conditions. Do not turn ordinal priorities into a precise weighted architecture score.

The method paraphrases the SEI's [ATAM collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) and its quality-scenario method. It is a proportional review; call it a full ATAM evaluation only when that process was performed.
