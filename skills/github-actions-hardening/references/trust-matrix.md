# Trust matrix

Read this before auditing the complete event-to-consumer path.

Use one row per job and per privileged consumer; split rows when events change authority.

| Event and ref | Workflow/code source SHA | Untrusted fields or files | Runner/network | Token/OIDC scopes | Secret names only | Cache reads/writes | Artifact inputs/outputs | Privileged consumer and gate | Verdict and evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fill from YAML and setting readback | Include local/reusable actions | Include AI prompt inputs | Include persistent state | Include inherited limits | Never values | Include implicit setup caches | Include origin/digest checks | State which input becomes executable | Fixed, supported or open, with source/test evidence |

Fork validation, privileged PR metadata events, completed-workflow events, comments and manual inputs have different trust paths.
Derive the actual token and ref behavior from current GitHub docs and repository policy rather than memorizing an event's default.
A trusted workflow file can execute untrusted checked-out code; a trusted artifact name can select attacker-produced bytes.
Review local actions and install hooks at the exact executed source revision.

For each finding, record the input an outsider controls, the transformation, the privileged operation and the control that blocks it.
An unsupported environment gate, broad write token, persistent runner or unauthenticated artifact source remains an open assumption even after static checks pass.
