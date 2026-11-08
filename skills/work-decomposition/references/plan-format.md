# Checked work-plan format

Use a JSON file or exactly one unindented fenced `json` block in PLAN.md. Keep prose, status notes, acceptance detail, and the dispatch ledger outside that block. The checker rejects duplicate keys and non-finite numbers; it reads the file without changing it.

```json
{
  "run_id": "api-consumers-01",
  "workspace": "/workspace/project",
  "integration_owner": "coordinator",
  "tasks": [
    {
      "id": "contract",
      "owner": "coordinator",
      "execution": "direct",
      "depends_on": [],
      "write_paths": ["contracts/response.json"],
      "inputs": ["requirements.md at recorded revision"],
      "outputs": ["contracts/response.json"],
      "acceptance": ["The schema includes the agreed error states"],
      "shared_resources": []
    },
    {
      "id": "client-a",
      "owner": "worker-a",
      "execution": "independent-parallel-work",
      "reason": "This consumer can be implemented against the fixed contract",
      "depends_on": ["contract"],
      "write_paths": ["clients/a", "runs/api-consumers-01/raw/a-r1.md"],
      "inputs": ["contracts/response.json at the frozen hash"],
      "outputs": ["clients/a"],
      "acceptance": ["Consumer A passes its contract checks"],
      "shared_resources": []
    },
    {
      "id": "client-b",
      "owner": "worker-b",
      "execution": "independent-parallel-work",
      "reason": "This second consumer owns disjoint implementation paths",
      "depends_on": ["contract"],
      "write_paths": ["clients/b", "runs/api-consumers-01/raw/b-r1.md"],
      "inputs": ["contracts/response.json at the frozen hash"],
      "outputs": ["clients/b"],
      "acceptance": ["Consumer B passes its contract checks"],
      "shared_resources": []
    },
    {
      "id": "integrate",
      "owner": "coordinator",
      "execution": "direct",
      "depends_on": ["client-a", "client-b"],
      "write_paths": ["clients", "contracts", "runs/api-consumers-01"],
      "inputs": ["Accepted component revisions"],
      "outputs": ["The integrated revision and check receipts"],
      "acceptance": ["Both consumers pass against the final schema"],
      "shared_resources": ["integration-check-environment"]
    }
  ],
  "budget": {
    "coordinator": "coordinator",
    "worker_starts": {"limit": 5, "used": 0},
    "retries": {"limit": 1, "used": 0},
    "review_rounds": {"limit": 2, "used": 0},
    "concurrency": {"ceiling": 2, "active": 0},
    "reserve": {
      "worker_starts": 1,
      "plan": "Coordinator integrates; reserve one independent verification run"
    }
  }
}
```

## Fields the checker enforces

- **Identity.** `run_id`, `workspace`, `integration_owner`, and `budget.coordinator` are non-empty strings; workspace is absolute in the checking environment.
- **Tasks.** A non-empty list; each task has a unique `id`, one non-empty `owner`, an `execution`, `depends_on`, and `write_paths`.
- **Gate.** `execution` is `direct`, `context-isolation`, `independent-parallel-work`, `independent-verification`, or `different-capability`; each delegated task also has a non-empty `reason` explaining its value.
- **Dependencies.** References exist, are unique within a task, and form an acyclic graph; a transitive dependency orders writers just as a direct dependency does.
- **Paths.** Literal POSIX file or directory roots, with no glob syntax, backslashes, newlines, or `..` segments; `[]` explicitly declares no writes.
- **Budget.** `worker_starts`, `retries`, and `review_rounds` each have non-negative integer `limit` and `used` fields; booleans are rejected; used cannot exceed limit.
- **Concurrency.** `ceiling` is an integer from 1 through 8; `active` is a non-negative integer no larger than ceiling or charged starts.
- **Reserve.** `worker_starts` is a non-negative integer and `plan` names how integration and verification will happen; used starts plus the remaining reserve, and delegated task count plus that reserve, each fit within the total start limit.

## Path and scheduling meaning

Relative write paths use `workspace` as their root; absolute report paths are also accepted. Use the final integration namespace for separate checkouts, so two workers cannot claim the same eventual file by spelling different checkout roots. The checker expands existing local symlink aliases and compares path components: `src/a` conflicts with `src/a/file.ts`, while `src/ab` does not. Every path grants the entire named subtree conservatively, even when the path looks like a file. Every pair without dependency ordering is potentially parallel; owner names and task status do not excuse overlapping claims. When one owner will execute conflicting tasks in sequence, record the dependency.

This is a static preflight, not a scheduler, sandbox, or complete schema validator. Inputs, outputs, acceptance checks, shared resources, live task receipts, and the actual meaning of a reason require inspection. It cannot see missing declarations, remote filesystem aliases, case-insensitive aliases, hard links, future symlink changes, or shared external state. Resolve those conflicts before dispatch and inspect actual changes on intake. The count of delegated tasks is a minimum allocation check; the ledger separately accounts for retries, review participants, descendants, and eval sessions.
