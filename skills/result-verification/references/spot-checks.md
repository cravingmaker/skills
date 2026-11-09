# Spot checks

Rerun or read at the source in proportion to what a wrong claim would cost. A spot check either confirms the claim, shows it false, or shows that it cannot be checked here; record which, and what you opened or ran.

## Always check

| Claim | How to check it |
| --- | --- |
| A blocker, or the evidence a blocker rests on | Rerun the command, or open the cited file and line |
| A premise of the chosen approach | Open the source; confirm it says what the report says |
| An exact number, version, date, price, or limit | Read it from the primary source at the stated date; a registry, release page, or official doc, never a summary |
| A quotation | Compare it word for word with the source |
| "Tests pass", "the build is green", "the validator exits 0" | Run the command yourself on the integrated revision |
| An authorization claim ("the user approved", "allowed by the brief") | Check the user's own message or the brief; a child's statement grants nothing |
| An outward-facing action (a push, a message, a publish, a deploy) | Check the remote, the message log, or the host's record |
| "No files changed" or "only the report was written" | `sh <result-verification-dir>/scripts/check-ownership.sh -C <checkout> <base>` against the start revision |
| A claim that a defect is fixed | Rerun the check that showed the defect |

## Sample

| Claim | Minimum |
| --- | --- |
| Routine file edits inside the boundary | Read the diff of the changed paths, plus one consumer of a changed interface |
| A research summary with many citations | Open the citations behind the conclusions; sample one in five of the rest |
| Data or archive work | Recompute one important result from source: a count, a hash, a total |
| Style and wording changes | Run the project's linters; read a sample |

## Signs that a claim needs a closer look

- The report cites no command, path, or URL for it.
- The evidence is another agent's report.
- Several agents cite the same single source.
- The cited output is paraphrased rather than quoted.
- The claim is phrased as certain while the evidence is a hypothesis.
- The revision or date the claim applies to is missing or older than the work.
- The report says a check passed but does not say which command ran.

## Recording

For each check, record: the claim, where it came from (task ID and report line), what you ran or opened, the result (verified, false, or unverifiable), and the time. False claims and the reports that made them stay in the run record; they inform the next brief to that worker or model.
