# Burn math

Read this when deriving thresholds or assessing sparse traffic. Use decimal fractions for target and spend fraction, and seconds for every duration; a target of 99.9 percent is entered as 0.999.

For target `S`, objective window `T`, permitted spend fraction `f` and long alert window `L`:

- Allowed bad-event fraction: `e = 1 - S`.
- Burn threshold: `B = f * T / L`.
- Bad-event ratio threshold: `r = B * e`.
- Under constant eligible traffic, a burn of `B` for `L` spends fraction `f` of the objective budget.
- With measured objective counts, allowed bad events are `eligible * e`; remaining budget is that quantity minus actual bad events, which may be negative.

For the synthetic 0.999 target, 2592000-second objective, 3600-second long window and 0.02 spend fraction, `B = 14.4` and `r = 0.0144`. These constants are a hand-derived fixture, not a recommended policy or a fixed product limit. The short confirming window compares its own bad-event fraction to `r`; an `and` between long and short predicates requires both to be true at evaluation.

At a floor of `N` eligible events, one bad event contributes ratio `1 / N`. If `1 / N > r`, a single event can cross a strict greater-than threshold; a small sample may page without useful rate confidence. When `N = 0`, the ratio is undefined; the owner must define coverage for that state. When `r >= 1`, a strict greater-than bad-fraction alert cannot fire even if every event fails. The calculator reports these findings; it cannot decide the acceptable loss or pager policy for the owner.

A calendar window needs its actual duration, and an event-based budget needs measured counts. Changing traffic volume means elapsed time at a fixed burn threshold is only an approximation to budget consumed. Counter resets, delayed samples, uninitialized error series and scrape loss need native rule tests beyond arithmetic.

## Calculator contract

The asset's null values are intentionally incomplete; supply approved numeric values before running. The helper requires schema_version as the string 1, a target in (0, 1), a positive integral objective_window_seconds and a nonempty policies array. Each policy has a unique name matching `[a-z][a-z0-9_]*`, integral long_seconds and short_seconds with 0 < short < long <= objective window, budget_fraction in (0, 1], and nonnegative integral long_min_events and short_min_events. Rule generation additionally requires service and owner identifiers matching `[a-zA-Z][a-zA-Z0-9_-]*`, an HTTP(S) runbook_url without credentials, distinct conventional Prometheus counter names in sli.eligible_counter and sli.bad_counter, a page or ticket severity and nonnegative integral hold_seconds for each policy. The bad counter must describe a subset of eligible events; neither JSON validation nor the helper can establish that source invariant. Keep eligibility, source, exclusions, window and missing-data decisions beside these numeric inputs for owner review. The calculator reports coherent arithmetic separately from approved policy or actual measured reliability.
