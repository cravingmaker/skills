# Source selection

Read this when choosing which evidence can close the current rationale gap. These are conditional methods, not a roster of mandatory searches or providers.

| Evidence need | Useful source |
| --- | --- |
| Implementation-time intent or evolution | Commits, reviews, code comments, tests, ADRs |
| Product or business constraint | Tickets, parent issues, attached project documents |
| Long-form design rationale | Specs, ADRs, meeting notes, accepted decisions |
| Attributable deliberation missing from docs | Relevant complete chat threads |
| Runtime condition or threshold | Telemetry, monitors, traces, incidents |
| Specific failure behind a defense | Error events, release history, resolution notes |
| Usage, experiments, or data constraints | Confirmed analytics tables and lineage |

Read only the relevant methods linked directly from SKILL.md. Their service names are examples; inspect the actual tool inventory and supported operations.

Start from the strongest relevant source already available. Expand only for an unanswered consequential question or conflicting evidence, within a finite search budget.

Record relevant sources as consulted, empty within the stated search, unavailable, limited, or unsearched. Do not call a category empty because no matching connector exists.

For defensive code, the incident method can guide a search in an already relevant source. A historical incident does not automatically authorize removing or changing the defense.
