# Performance, runtime and trace playbooks

Read this for a performance regression, a spinning or leaking live process, or a diagnosis from an existing capture. Adapted from pstack's perf-issue, runtime-forensics and trace-forensics playbooks.

## Performance issue

Tie every fix to a measurement; do not read source instead of measuring.

1. Capture a baseline on the matching surface with a realistic workload. Vet the baseline, and every later number you will claim, with the `benchmark-checklist` skill.
2. Ground hypotheses in the code path, and identify the limiting resource (CPU, I/O, memory, locks, network). Don't claim a ceiling without running it.
3. Try the performance mantras in order, cheapest first, and stop at the first that meets the target:
   1. Don't do it. Stop work whose result nothing uses.
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when they're not looking.
   6. Do it concurrently.
   7. Do it cheaper.
4. Verify each attempt before trying the next. Capture a post-fix measurement on the same surface and workload, and compare the artifacts directly (parse them; diff them). An inconclusive or wrong-surface result is not a pass; say so.
5. Report the baseline, the post-fix number, the delta, the workload and the artifact paths.

## Runtime forensics

The deliverable is a cited diagnosis from the live process, not a fix.

1. Capture a real signal on the matching surface: a CPU profile for a spinning process, a heap snapshot for a leak, a performance or DevTools trace for a visual glitch.
2. Reduce the artifact to the decisive finding: the function on the hot path, the retainer chain from the leaked object to a GC root, the loop firing without input. Parse large artifacts with a script and keep only the reduced finding in your context.
3. Prove the mechanism cheaply before believing it. Reading a capture is read-only; injecting instrumentation into a running process or hot-patching code changes it, so do that only when authorized and in an environment you own.
4. Map the finding to source: file, symbol, and the line that allocates or schedules.
5. Report the signal captured, the reduced finding, how the mechanism was confirmed, the source location and the artifact paths. Return to the main loop once the cause is known.

## Trace forensics

The capture already exists. It is a fixed dataset: read it, don't re-run it.

1. Identify the format (cpuprofile, `.json.gz` trace, spindump, heap snapshot) and load it with the right tool.
2. Transform it into a queryable form, such as one row per sample, frame or node in SQLite, before reading.
3. Narrow to the cause: the frames holding the most time and the call tree to the hot path; for a leak, the retainer chain; for a spindump, the stuck or blocked thread and its wait reason.
4. Attribute to source through the artifact's own symbols. A frame with no source mapping is not yet a diagnosis: resolve the symbols, or say the artifact does not carry them.
5. Keep observation and hypothesis apart. With a paired before/after capture, diff them to confirm. Without one, report the finding as the strongest hypothesis the artifact supports, not a confirmed cause, and say what capture would confirm it.
