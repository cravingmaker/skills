---
name: slo-error-budgets
description: Define an event or latency SLI, owner-approved SLO and error-budget policy when setting reliability goals or paging on budget burn. Calculate thresholds from the chosen window, generate multiwindow alerts, and test fast burn, slow burn, sparse traffic, resets and no data.
license: MIT
---

# SLO error budgets

Deliver an owner-approved reliability contract, a decision policy and tested burn alerts.

## Define what counts

Inspect existing counters, bucket boundaries, scrape/evaluation intervals, historical traffic and the project's SLO generator before choosing a target. Read [references/sources.md](references/sources.md) when selecting generator syntax or checking current SLO and Prometheus behavior. Compare [assets/slo-contract.json](assets/slo-contract.json) with the project's contract; fill its null fields from evidence and owner decisions, never overwrite an existing contract blindly.

Record numerator, denominator, event source, eligible population, units, service boundary, window, exclusions, late events, traffic floor and telemetry-loss behavior. Availability is good eligible events divided by all eligible events; latency is the fraction of eligible events within a named threshold. Use the same population and window for both terms; retries and internal probes need explicit inclusion rules. A percentile averaged across instances cannot supply a service latency SLI, and biased sampled traces cannot silently replace complete event counts.

Set the target and response policy with the accountable owner; neither a calculator nor a familiar target approves them. State rolling versus calendar windows and timezone/boundary semantics. For calendar objectives, supply the actual window duration for each calculation. Define whether a quiet service has enough evidence to make a reliability claim; zero requests, zero errors and missing observations are separate states.

Done when the owner has approved the eligibility, target, objective window, traffic floor and no-data policy, or the unresolved choices are explicitly returned as a draft.

## Derive the alert thresholds

Read [references/burn-math.md](references/burn-math.md) when calculating thresholds or deciding whether a short window has enough traffic. The allowed bad-event fraction is `1 - target`; burn is the observed bad-event fraction divided by that allowance. An alert that would spend budget fraction `f` over long window `L` uses burn threshold `f * objective_window / L` under constant eligible traffic. Actual event-budget consumption comes from eligible and bad event counts; varying traffic can break the time-proportion approximation.

```sh
python3 scripts/burn-rate.py path/to/approved-slo-contract.json
python3 scripts/burn-rate.py path/to/approved-slo-contract.json --emit rules
```

The Python 3.12 standard-library helper reads only the explicit JSON file and emits JSON calculations on stdout, with diagnostics on stderr. Exit 0 means coherent inputs, 1 means a threshold is unattainable or one event can cross it at the supplied traffic floor, and 2 means malformed input or usage. `--help` exits 0 without inspecting files or writing. A finding returns calculations for review; rule generation refuses until findings are resolved. `--emit rules` emits native Prometheus rules as JSON, which its YAML reader accepts, for explicitly named eligible and subset bad counters with a bounded service label. Use the existing project generator for histogram SLIs or a richer eligibility/query contract; the helper supports only conventional counter identifiers, not arbitrary PromQL. The helper does not parse YAML, validate PromQL, select a target or establish actual observed budget consumption.

Choose long/short confirmation windows, spend fractions, minimum eligible events and response urgency from detection and recovery needs. Both windows must cross their own error-ratio threshold with adequate traffic for a multiwindow alert to fire. Sparse services need an explicit alternative, such as a longer window, separate synthetic availability checks or a nonpaging event threshold; suppressing burn alerts alone leaves a coverage gap. Use [assets/error-budget-policy.md](assets/error-budget-policy.md) when recording the owner's release/reliability decisions, exceptions and resumption evidence.

Done when each alert has derived arithmetic, meaningful traffic assumptions and an owner-approved response; retain any low-volume finding until that owner resolves it.

## Generate and prove the rules

Use the project's existing pinned Sloth, Pyrra, OpenSLO adapter or native generator; verify its installed schema and output against its official documentation. OpenSLO describes intent; it is not itself evidence that a deployed alert was generated correctly. If no generator exists, use the helper for its supported counter contract or author minimal native rules from the approved contract; retain the math beside them. Use the `prometheus-alerting-rules` skill, when installed, for rendered-rule semantics, aggregation, runbook labels, native tests and routing, reading its `SKILL.md` first. If unavailable, report that limit and still run the project's native rule checker and tests; do not claim delivery from rule evaluation.

Test the rendered artifacts consumed by Prometheus with `promtool check rules` and `promtool test rules`. Build independent expected cases for sustained fast burn, sustained slow burn below the page threshold, a long-only historical burn, threshold equality, recovery, no traffic, no data, sparse bad events and independent counter resets. Assert numerator/denominator behavior as well as firing labels; `or vector(0)` must not conceal collector failure. Change a confirmation `and` to `or` and prove the long-only case rejects it; restore and repeat. Before any deployment or external notification, require explicit authorization for that scope and confirm account/project/region/cluster/receiver identities immediately before the mutation. Any automated rehearsal that writes must require an explicit disposable target; the shipped calculator has no mutation path.

Done when the contract, policy, calculations and rendered rules agree, selected native tests pass, and missing owner approval or runtime delivery proof is reported without a readiness claim. Return the approved inputs, derived thresholds, generator/rule hashes and versions, tested cases, remaining budget source and policy decisions.
