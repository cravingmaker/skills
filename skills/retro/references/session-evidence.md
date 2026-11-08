# Read a session as evidence

Read this when inspecting stored history, large records, historical environments, or usage counters.

## Locate and bound

Use the supplied session pointer directly when it resolves. Otherwise use supported host search, configured indexes, local help, or bounded inspection within the relevant project. Confirm identity through available run ID, workspace, timestamps, and matching human content. Record plausible rejected candidates and their distinguishing evidence when ambiguity matters. Associated child sessions count only when a parent receipt or other evidence establishes their relationship. The `recall` skill can find an unknown prior-run locator when installed; it does not replace this incident analysis.

Measure a file's bytes, lines, and long records before opening content. Locate matching line numbers, then extract selected fields or bounded chunks; narrow a record extract that exceeds about 500 characters. A JSONL record can embed a whole history, so avoid printing a whole file or whole matching record. Record the extraction command or query used so a reviewer can reproduce the pointer. Preserve raw records unchanged.

## Establish record meanings

Use actual records or the source's documentation to distinguish human prompts, assistant text, hooks, injected messages, parent dispatches, tool calls, and results. A child transcript's user role may be its parent agent. Match calls to results using the source's actual identifiers rather than adjacency assumptions. Record exact paths or host links, line/message IDs, available fields, and unresolved interpretations. Missing records are unknown; an unobserved action is not automatically an action that never happened.

For loaded skills and environments, separate historical evidence, an unverified retained snapshot, a current observation, and unknown state. Inspect available captured bodies or archives before calling historical material unavailable. A current installed version or modification time does not prove the version used in the incident. A skill mentioned in prose is weaker evidence than an actual recorded read or invocation.

## Account for time and usage

Establish units and whether each counter is incremental, cumulative, per-turn, or per-session before adding anything. Sum incremental values; difference compatible cumulative observations, checking resets and missing intervals. Do not add cumulative snapshots together or double-count child usage already included in a parent counter. Keep missing readings unknown rather than zero. Preserve the counter's original precision and show how a reported total was calculated.

For wall-clock claims, identify timestamp fields, zones, event boundaries, and the relevant interval. Attribute a gap to idle time, a tool, a worker, or the human only when the evidence shows that cause. Count compaction events only after establishing what their records mean. Keep unsupported prices, costs, and speedup claims out of the finding.

## Evidence bar

Each finding names an exact pointer, what it supports, confidence, and the material limitation. For local history use an absolute path with line locations; for a host use the exact run/message or event link. Preserve original human wording when its scope matters and label agent interpretations. Constrain lookups to the stated question and referenced context. If the transcript is unavailable, use the visible evidence with a coverage label rather than claiming to have audited it.
