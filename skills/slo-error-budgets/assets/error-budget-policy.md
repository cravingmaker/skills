# Error-budget policy

Compare with the project's policy and retain the owner's approved decisions; this outline supplies no target or release authority.

| Decision | Owner-approved value and evidence |
| --- | --- |
| Objective | Service boundary, SLI source, eligibility, target, window, calendar/timezone rules |
| Budget accounting | Measured eligible/bad counts, exclusions, delayed data and remaining-budget calculation |
| Alert response | Long/short windows, spend fractions, traffic floor, owner, severity and runbook |
| Telemetry gaps | Distinguish healthy zero errors, no eligible traffic and unknown reliability |
| Release decision | Conditions to continue, limit or pause releases and which release classes apply |
| Reliability work | What work receives priority, who owns it and the review cadence |
| Exception | Named approver, reason, scope, expiry and effect on budget |
| Resume | Observable recovery condition and who restores normal release policy |
| Evidence | Contract/rule versions, native tests and actual notification checks if authorized |

A spent budget informs the agreed policy; it does not grant an agent permission to freeze releases or change production traffic.

## Budget states

Fill the thresholds, actions and decision owners with the service owner; these rows grant no release authority.

| State | Owner-approved condition | Action and actor |
| --- | --- | --- |
| Healthy | Remaining budget and burn within agreed bounds | Normal release policy and accountable owner |
| Burning fast | Named burn alert and response deadline | Mitigation and any agreed release restriction |
| Low | Measured remaining budget crosses the chosen limit | Review requirement and reliability-work priority |
| Exhausted | Measured remaining budget is zero or negative | Agreed release scope, exceptions and resumption evidence |

Record how a single large incident and dependency failures affect accounting and follow-up; retain the contract's exclusions.
