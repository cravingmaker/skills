# Intake record and report template

## Per task

Record one entry per dispatched task in the run record, in the order the results arrived.

```markdown
### <task ID>: <one-line goal>

Brief: <path>. Started from: <revision>. Raw report: <path> (arrived <time>), or "none: <reason>".
Outputs: <path at revision or hash: present | missing>.
Contract: <complete | missing: field, field>.
Scope: <as briefed | unrequested: what>.
Boundary: `check-ownership.sh <base> <globs>` → exit <n>; <paths outside, if any>.
Reruns: `<command>` → <matches | differs: what the report said, what you saw>.
Source checks: <claim> → <verified | false | unverifiable>, via <what you opened>.
Decision: <accepted | rejected | unresolved>, because <evidence>.
```

## Unresolved results

Each of these leaves the task unresolved, never passed:

- no report, an empty report, or a report that cannot be parsed;
- a PARTIAL or BLOCKED status, for the part it did not finish;
- a timeout, a cancellation, or a host error;
- an evaluator that reached no verdict, or a review that did not pass its format check after one return;
- a budget that ran out before the task finished;
- a check that could not be run, for lack of environment, credentials, or authority.

An unresolved required task blocks the run's acceptance until it is reassigned within the budget, or until the user removes it from scope. A successful sibling does not cover it.

## Integration receipt

```markdown
Integrated revision: <commit or hash>. Included: <task IDs>. Excluded: <task IDs and why>.
Conflicts: <files or claims, and how each was settled>.

| Acceptance criterion | Check | Command | Result |
| --- | --- | --- | --- |
| <criterion> | <what proves it> | `<command>` | <exit code and the decisive output line> |
```

## Report to the user

```markdown
<Outcome: accepted | partly accepted | unresolved>, at <revision>.

Acceptance: <criterion → command → result, one line each>.
Verified: <reruns and source checks, and any claim found false>.
Unresolved: <item, reason, and the decision or resource it needs>.
Cost: <workers started, retries, review rounds, against the budget>.
```

Lead with the outcome. Report a failing check as failing, with its output; never round a partial result up to done.
