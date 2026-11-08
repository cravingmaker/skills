---
name: benchmark-checklist
description: Vet a measured speedup, slowdown, latency, or throughput claim before reporting it or choosing an option. Check comparable work, correctness, errors, the limiter, repeatability, noise, and end-to-end relevance.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/benchmark-checklist/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/benchmark-checklist/SKILL.md"
  local-changes: "Retained the seven measurement checks; added units, denominators, sensitivity and negative controls; made repetition cost/noise-aware and commands portable across project-native macOS/Linux tools."
---

# Benchmark checklist

Test the performance sentence you intend to report against evidence from comparable runs. A quick ballpark requested by the user may use one run, labeled as such, after confirming correct output and completed work; it cannot choose a winner or establish an improvement.

## Frame the number

Write the decision, the effect that would change it, and the expected noise floor before measuring. Name the unit, numerator, denominator, baseline, workload size and distribution, concurrency, timed boundary, and uncertainty. Read the harness: identify setup, warmup, caches, awaited work, result consumption, error counts, and what the timing excludes. Bind baseline and candidate source/build identities, input data, installed versions, runtime flags, environment, and measurement commands in one retained artifact. Use the project's established commands and supported system tools; do not install or tune infrastructure outside scope.

## Check the measurement

1. **Why not double?** Name the suspected limiter, then test it with a separate profile or counters mapped to source. Instrumented runs do not become clean timings. Check CPU, I/O, locks, network and load-generator saturation as relevant. Use available project-native tools on macOS or Linux; for example, `uptime` and the supported core-count command, `sysctl -n hw.logicalcpu` on macOS or `getconf _NPROCESSORS_ONLN` on Linux. A guess from reading code is a hypothesis, not a measured cause.
2. **Were the sides comparable?** Use realistic release builds, flags, data, cache state, batching, transaction settings, pools, and relevant version/configuration identity. Record necessary differences. An untuned default versus a tuned alternative compares those configurations; it cannot establish the implementation or adoption winner. If representative tuning is unavailable, keep the choice inconclusive.
3. **Do the limits allow it?** Compare bytes/time with bandwidth and operations × cost with CPU capacity. Check the changed portion's share of the whole: removing a piece taking 10% of elapsed time saves at most 10% of latency, about 11% more throughput under the same assumptions. A result beyond the bound may be timing skipped, cached, or incorrect work.
4. **Did it error?** Count attempts, completions, correct results, errors, retries and timeouts for each side. Validate output contents and side effects; a fast rejection is not faster successful work. Include failures rather than silently timing only successful attempts.
5. **Does the harness react?** Use a sensitivity control with a known extra cost or changed workload and a negative/no-op control where appropriate. Confirm the metric moves for the intended reason and is not dominated by timer, setup, cache, or unrelated work. Keep control data separate from the claimed timings.
6. **Does it repeat above noise?** Declare a finite sample/time budget proportionate to cost. For cheap runs, start with about five independent runs per side; alternate or counterbalance baseline/candidate order. Record warmup policy, machine load and background activity, median, spread and raw samples. Increase samples only for a justified unresolved decision within budget; do not treat dependent requests from one process as independent run replicates. A gap inside the observed noise supports no measurable difference, not a speedup. A suitable statistical method can quantify uncertainty without turning a tiny effect into a useful one.
7. **Does it matter end to end?** Pair a microbenchmark with the realistic user path and its share of total cost. Preserve realistic data sizes and concurrency. A faster helper that occupies 1% of the path can save at most that 1% of latency under the same assumptions. Name what remains unmeasured.
8. **Did the work happen?** Confirm the timed region contains actual requests, reads, writes, awaited asynchronous completion, and consumed results. Check counts and persisted state; uniterated generators, discarded computations, cache hits, or timed-out work can invalidate the sentence.

Keep a run table with side/build identity, order, input, duration/unit, completed/correct/error counts, environment, and evidence pointer. Observe both sides under comparable load; stop or label interference rather than silently favoring one side. Do not discard an outlier without a stated rule and evidence of what invalidated it.

## Report

Lead with faster, slower, no measurable difference, or inconclusive, scoped to the measured workload. Give the primary number with units, numerator/denominator, baseline, run count, spread, uncertainty, and limiter evidence. Keep raw runs, controls, profiles, correctness/error counts, environment and commands in a linked artifact. Missing correctness/work evidence, incomparable sides, an unexplained limit violation, or an unsupported causal claim keeps the relevant verdict inconclusive. Report a suspected limiter as suspected until profiling or counters support it; correlation alone does not prove the change caused the difference. Done when the decision sentence is no stronger than its evidence and every unresolved measurement gap is named. This skill validates a measurement; it does not own an optimization experiment loop or authorize product changes.

Read [references/SOURCES.md](references/SOURCES.md) when checking provenance and adaptations.
