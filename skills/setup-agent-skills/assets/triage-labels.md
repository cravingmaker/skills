# Triage labels

Seed for `docs/agents/triage-labels.md` only when the `triage` skill is installed. Preserve existing tracker labels and state strings.

| Canonical role | Tracker label or state | Meaning |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | A maintainer needs to classify the issue. |
| `needs-info` | `needs-info` | The reporter must supply missing information. |
| `ready-for-agent` | `ready-for-agent` | The issue is specified for agent implementation. |
| `ready-for-human` | `ready-for-human` | The issue needs human implementation. |
| `wontfix` | `wontfix` | The issue will not be implemented. |

Use the configured value when a workflow names a canonical role. Readiness describes context; it does not grant implementation or remote-write authority.

Change only the tracker column for an existing vocabulary. Recording this mapping does not itself create remote labels.
