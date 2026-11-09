# Reading saved plans

Read this when interpreting the summary or comparing plans.

## Rows and loops

Compare `Plan Rows` with `Actual Rows` at the same node. Actual rows are per-loop averages; the helper also reports rows times loops as approximate total row work. Compare a per-loop estimate with a per-loop actual, not with the total. When loops are zero the node did not execute; a zero row count there is not an estimate-error measurement. When one of the executed estimate/actual counts is zero and the other positive, report that distinction instead of dividing by zero.

A `LIMIT` or another demand-limited parent can stop an input before its full estimated row count is produced. The helper conservatively marks a large shortfall below a `Limit` as `possibly_stopped_early`; inspect blocking operators and actual demand before calling it an estimate error. A shortfall outside that path can still reflect another early-stop cause.

The helper walks `Plans`, including subplans, and keeps node paths stable within each saved tree. Parallel worker records are reported separately; leader totals can already include worker work, so do not sum them into the leader a second time. Different plan shapes require reading the corresponding operations; equal tree positions do not prove that two nodes perform the same job.

## Buffers, time and spill

The helper retains rows removed by filters and rechecks, and includes them in approximate examined rows for scan triage. A scan returning one row can still filter many rows; approximate examined rows are not a physical page or storage-I/O count.

Worker disk sorts, temp I/O and hash batches produce a separate worker-spill flag without adding worker counters into the leader.

Parent buffer counts and timings can include child work. The helper preserves node-level counts and the root's inclusive buffer counts; it does not add the tree's counters into a fabricated total. Shared reads describe page accesses, not necessarily physical storage misses; cache, OS and provider storage change that interpretation. Planner cost units are not milliseconds.

Compare planned and launched parallel workers; `fewer_workers` is an availability lead, not proof that parallelism would improve the query.

Check disk sorts, temporary reads/writes and hash batches as separate spill clues. A high loop count is a triage flag, not proof of N+1 application requests. Count those requests at the application boundary.

## Before and after

`--compare` returns two independent summaries and the execution-time difference when both top-level measurements exist. It deliberately emits no speedup verdict or schema-change recommendation. Attach workload identity, safe parameter-class identity, data scale and skew, statistics state, cache state, concurrency and settings beside the plans. Exclude connection setup from one side only if it is excluded from both, and report any provider compute replacement.

Default thresholds are documented in `--help` and can be changed for the workload. Exit 1 means a triage flag exists on at least one side; it is not a regression-test verdict. Raw query, relation, index, filter, alias and output expressions are omitted from stdout. Unknown future node kinds are labeled `Other` rather than echoing arbitrary input strings. Private raw plan retention still matters because the summary is intentionally incomplete.
