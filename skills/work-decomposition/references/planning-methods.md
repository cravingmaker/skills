# Planning methods

Apply the branch the task needs. Accepted tickets and the run's PLAN.md remain authoritative.

## A recurring workflow

Name its trigger, observable stop predicate, owner, and any human checkpoint. Use a checkpoint only for an actual decision or authority boundary. Prepare the concrete reviewable artifact before that checkpoint; repeat neither a settled interview nor an approval already given. A recurring task requires no AI, schedule, or extra controller unless its scope does.

## An unknown that could invalidate the plan

Put a bounded probe before work that depends on its answer. State the hypothesis, realistic input, observation that could disprove it, finite allowance, and evidence path. Measure the smallest authorized experiment against the actual artifact, then keep or revise the plan from its result. Inconclusive stays unresolved. Record the decision in the existing run record instead of adding another log.

Use stronger evidence for an irreversible or consequential choice. A cheap reversible step can proceed within existing authority. Independent verification consumes the same start/slot budget; a leaf never starts a second controller.

## Contracts across phases

Keep exact spec constraints, formats, values, supported public contracts, and accepted testing seams. For each dependency, name the input consumed and output produced, exact interface or content identity, and the task that owns it. Check coverage, contradictions, missing definitions, and signature consistency before fan-out. Proportional detail is enough: carry decisions a builder cannot infer, not an implementation transcript.

Each unit ends at a named observation before dependent work proceeds. Temporary red evidence may remain in an isolated experiment when scoped and reversible; exposed PR heads still meet the project's contract. Judge the accepted end state and integration checks, preserving public or independently deployed compatibility obligations.

## Independent work and real shared state

Parallelize only problems that can be understood and changed independently. Related failures or a shared diagnosis may need one owner. Give independent writers separate artifacts, keys, or drafts and combine at the integration boundary. Two fields in one shared JSON file are still one mutable object. When one canonical writer is necessary, use structural serialization rather than an instruction to be careful.

Include path aliases and live resources such as browser sessions, ports, databases, branches, generated outputs, and locks. Distinct checkouts do not establish disjoint ownership of the integrated result.

## Workspace isolation

Inspect the current checkout and record its baseline and pre-existing changes. Distinguish a linked worktree from a submodule before creating anything. Use the active host's checkout mechanism when it owns isolation; do not create a shell checkout for a host-managed child or silently fall back to a shared dirty checkout. When the required mechanism is unavailable, record that limitation and continue only independent permitted work.

Run the existing relevant baseline checks without automatic dependency installs or unrelated cleanup. Record failures against that baseline. Keep a receipt for each resource created by this run. Cleanup may remove only proven-owned resources after checking their live users and recoverable work; preserve all other checkouts, branches, apps, caches, and dirty files.
