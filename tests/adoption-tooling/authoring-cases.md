# Authoring review cases

These accept/reject pairs cover authoring judgments that a deterministic checker cannot infer from wording. Review them with the authoring guide; no model evaluation is claimed. Code, closure, provenance, host policy and CLI behavior have executable fixtures in check.py.

| Rule | Reject | Accept | Review evidence |
| --- | --- | --- | --- |
| Main use case first | Description begins with background and a long list of secondary uses before saying it repairs a brief. | Description begins: Write a self-contained task brief for a fresh agent. | The existing agent-briefing description leads with that main use case. |
| Conditional reference reads | Read every stack reference before every guardrails task. | Read the TypeScript profile when assessing a TypeScript project; read the Python profile for Python. | Authoring-guide size/disclosure rule names the branch condition. |
| Advisory size | Treat 5000 tokens as a validator failure or hide a long procedure in an always-read appendix. | Aim for about 5000 tokens; keep the hard under-500-line limit and disclose branch-specific detail. | The guide distinguishes advisory size from the enforced line limit. |
| Engineering composition | Add a second generic workflow router for each engineering domain. | Use one generic owned workflow and add domain-specific role methods. | The guide states the composition rule; this change introduces zero skills or routers. |
| Source review | Treat a correctly shaped SHA string and an existing legal file as proof of complete attribution. | Reproduce the pinned input hash/destination diff and review all secondary contributions and legal text. | The guide and manifests explain the automated boundary and reproduction commands. |

Reference length has an executable boundary fixture: a 102-line reference without contents fails, then a table of contents makes it pass twice. These authoring judgments remain review obligations for future adoption PRs.
