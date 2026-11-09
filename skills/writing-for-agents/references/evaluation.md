# Evaluate the instructions that will ship

Read this when writing eval examples, comparing wording, diagnosing a missed pointer, or making an evaluated-status claim. Use the repository's current eval harness and documentation; do not create another model controller.

## Define observable cases

Create `evals/examples.md` with Activation, Near miss, and Outcome sections and at least one straight-quoted prompt item in each. Activation checks the intended ordinary or explicit request. Near miss checks a similar job, incidental name, or quoted command that should stay outside the skill. Outcome checks the actual artifact, decision, evidence, and scope boundary, including failures and unavailable inputs. For a manual entry, test explicit selection and ordinary/quoted non-selection. For a merged skill, exercise each distinctive retained branch and changed boundary.

Judge the result rather than asking the model to recite the skill. For instruction pointers, inspect evidence of discovery, body reads, reference access, action, and completion. A name in the answer is insufficient evidence that the skill was read or followed. Use realistic task conditions and an observable wrong action or omission, without invented pressure rhetoric or claims about universal compliance.

## Keep the comparison valid

Use a fresh restored fixture for each arm, one with the final skill available and one without it. Hold the prompt, fixture bytes, required dependency closure, standing rules, host/model/settings/tools, and budget constant. Exclude equivalent upstream and sibling-copied methods from the baseline; removing just the candidate's folder is insufficient when another discovery source supplies the same content. Verify treatment availability, baseline absence, and identical non-candidate inventories through actual supported discovery evidence. Keep fixture instructions in the form the current harness permits rather than injecting an uncontrolled host configuration. Record canonical and dependency hashes, exact loaded skills, input revisions, raw outputs, calls/results, artifacts, and failures.

Each model-powered arm, retry, or judge consumes the coordinator's shared budget and active slot pool. Use finite starts, rounds, and explicit authorization; absent authority means prepare cases and run deterministic checks without model calls. Do not prescribe a fixed sample count, provider panel, or required TDD background for all authoring. Static authoring checks can pass while behavior remains unevaluated.

## Read the result honestly

Separate comparison validity, activation, near-miss routing, deliverable correctness, authority preservation, and unnecessary work. A valid comparison can contain a failed outcome. Both arms succeeding establishes parity on those cases, rather than an automatic benefit claim. Missing or failed arms remain visible; several retries of one case are not independent cases. Self-reported reasoning is weaker evidence than observed calls and artifacts.

If a trigger fails, distinguish unavailable discovery from a weak description and from a body that was loaded but not followed. If wording variants differ, change one relevant instruction at a time and retain the no-skill control. Inspect every flagged output: quoted examples and template echoes can resemble a violation without being one. An agent's explanation of its mistake can suggest a hypothesis, but does not prove causality. Correct the demonstrated defect and rerun affected cases within the remaining budget.

Keep the catalog unevaluated until the repository's required matched records and outcome review exist. Report unrun cases, unavailable hosts, inconclusive differences, and coordination cost explicitly. Further specialized measurement belongs with its installed domain owner rather than a second evaluation engine here.
