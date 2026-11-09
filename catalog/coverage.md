# Coverage

Every role and specialty the user asked for, mapped to the skills that cover it. A role's PR is complete when each of its rows is covered or explicitly deferred with a reason. Status: planned, in PR, covered, deferred.

Coverage rows describe scope; only `metadata.requires` defines installation edges. Optional routes are conditional prose pointers checked against shipped names or the supported external inventory. Engineering roles add domain methods around the same owned generic workflow.

Roadmaps from [roadmap.sh](https://roadmap.sh/roadmaps) are coverage references only; their content is not reproduced here.

| Role | Specialty the user named | Capabilities | Upstream providers | Status |
| --- | --- | --- | --- | --- |
| agent-orchestrator | Manage other agents like a product or project manager | `agent-orchestrator` (router), `work-decomposition`, `agent-briefing`, `result-verification`, `decision-log` | none | in PR |
| agent-orchestrator | Agents discuss and debate to find the best approach | `agent-debate`, `decision-log` | none | in PR |
| backend-engineer | JavaScript and TypeScript | `typescript-node-services`, `service-resilience`, `opentelemetry-instrumentation`; shared guardrails and tooling | none | in PR |
| backend-engineer | Rust | `rust-async-services`, `architecture-fitness-functions`; shared guardrails and tooling | none | in PR |
| backend-engineer | API design | `api-design`, `api-compatibility`, `api-authorization`, `idempotent-requests` | none | in PR |
| backend-engineer | Software architecture | `backend-engineer` (router), `architecture-decisions`, `architecture-review`, `architecture-fitness-functions`, `codebase-design`, `architect`, `improve-codebase-architecture`, `domain-modeling`; wider modernization and model tooling deferred | none | in PR |
| frontend-engineer | Plain HTML, CSS, and JavaScript | planned | none | planned |
| frontend-engineer | React, Astro, Svelte | planned | none | planned |
| frontend-engineer | GPUI and desktop | planned | none | planned |
| frontend-engineer | Software architecture | `codebase-design`, `architect`, `improve-codebase-architecture`; domain methods planned | none | planned |
| mobile-engineer | Swift (iOS) | planned | none | planned |
| mobile-engineer | Android | planned | Google `android/skills` | planned |
| mobile-engineer | Software architecture | planned (shared architecture capabilities) | none | planned |
| ui-ux-designer | UI and UX design | `prototype`, `domain-modeling`; remaining methods planned | none | planned |
| qa-engineer | Quality assurance and testing | `tdd`, `change-review`; remaining QA methods planned | none | planned |
| devops-engineer | Shell: zsh on macOS, bash on Linux | planned | none | planned |
| devops-engineer | CI/CD | `fix-ci`; remaining delivery methods planned | none | planned |
| devops-engineer | Docker and Kubernetes | planned | none | planned |
| sysadmin | Shell, Linux, and system administration | planned | none | planned |
| sysadmin | Network | planned | none | planned |
| sysadmin | Hardware and software | planned | none | planned |
| security-engineer | Red team | planned | none | planned |
| security-engineer | Blue team | planned | none | planned |
| data-engineer | Data engineering | planned | none | planned |
| data-scientist | Data science | planned | none | planned |
| data-analyst | Data analysis | planned | none | planned |
| technical-writer | Technical writing | planned; builds on `clear-communication` | none | planned |
| seo-engineer | Search engine optimization | planned | none | planned |
| business-analyst | Business analysis | planned | none | planned |
| financial-analyst | Financial analysis | planned | none | planned |
| marketing-expert | Marketing | planned | none | planned |
| copywriter | Copywriting | planned; builds on `clear-communication` | none | planned |
| all roles | Clear, lean communication in both directions | `clear-communication` | none | in PR |
| engineering, data, systems, security, QA | An enforcement environment that makes work right by construction | `project-guardrails`, `toolchain-upgrade`, `correct` | none | in PR |
| agent-orchestrator | Shape an idea into approved, source-bound work | `grilling`, `grill-with-docs`, `to-spec`, `to-tickets`, `domain-modeling`, `grill-me` | none | in PR |
| agent-orchestrator | Import exact tickets and verify their actual Proof | `work-decomposition`, `agent-briefing`, `decision-log`, `result-verification` | none | in PR |
| agent-orchestrator | Configure tracker paths and triage incoming work | `setup-agent-skills`, `triage` | none | in PR |
| agent-orchestrator | Resolve an unclear destination and outside knowledge | `wayfinder`, `research`, `prototype`, `to-questionnaire` | none | in PR |
| backend-engineer, frontend-engineer, mobile-engineer | Explore a bounded design question | `prototype`; role routers planned | none | in PR |
| business-analyst | Domain understanding, specs and approved tickets | `domain-modeling`, `to-spec`, `to-tickets`; role router planned | none | in PR |
| data-analyst, data-scientist, technical-writer, seo-engineer, financial-analyst, marketing-expert | Primary research for a bounded decision | `research`; role methods and routers planned | none | in PR |
| all roles | Explain mechanism and intent, refine a prompt, repair an unclear answer | `how`, `why`, `sharpen`, `bro`, `wait-what`, `clear-communication` | none | in PR |
| agent-orchestrator | Run approved code tickets through one coordinator | `implement-spec`, `implement`, `work-decomposition`, `result-verification`; shared record and budget | none | in PR |
| engineering and QA | Deep modules, design alternatives and architecture reports | `codebase-design`, `architect`, `improve-codebase-architecture`; domain methods and routers planned | none | in PR |
| engineering, QA and systems | Build and diagnose an authorized slice | `implement`, `tdd`, `diagnosing-bugs`; domain methods planned | none | in PR |
| agent-orchestrator, devops-engineer | Resumable setup for human-only steps | `wizard`; devops router planned | none | in PR |
| engineering, QA, security and data | Code review, bounded fix loops and downstream effects | `change-review`, `sol-loop`, `interrogate`, `blast-radius` | none | in PR |
| all roles | Explicit code, design or read-only provider panels | `council`, `sol-loop`, `agent-debate`; requested mode preserves authority | none | in PR |
| engineering, QA, systems and data-scientist | Comparable benchmarks and explainable numbers | `benchmark-checklist`; domain methods planned | none | in PR |
| engineering, QA and systems | Real-surface project drivers and feature-map maintenance | `create-verification-skill`, `maintain-verification-skill`; scope and actual proof gaps decide mode | none | in PR |
| agent-orchestrator | Draft, file and continue verified PR delivery | `file-pr`, `pr`, `babysit-pr`, `leaving-pr-comments`, `modernize`, `takeover`, `full-send`, `full-stop`; root-only authorized monitoring | none | in PR |
| agent-orchestrator, backend-engineer, frontend-engineer, mobile-engineer, qa-engineer, devops-engineer, data-engineer | CI failure triage and repair | `fix-ci`, `diagnosing-bugs`; search aliases ci-failure-triage and ci-failure-diagnosis | none | in PR |
| all roles | Session evidence, continuation and instruction craft | `retro`, `handoff`, `writing-for-agents`, `recall`, `decision-log`; one authoritative record | none | in PR |
| all roles | Grounded teaching and read-only catch-up | `teach`, `ketchup`, `clear-communication`; learning workspace and wider status window only on request | none | in PR |
| agent-orchestrator, backend-engineer, frontend-engineer, mobile-engineer, devops-engineer, sysadmin, security-engineer, data-engineer, data-analyst, data-scientist | Durable architecture integrity and comparable domain option trials | `architecture-decisions`; authorized ADR writing remains with `domain-modeling` | none | in PR |
| backend-engineer, frontend-engineer, mobile-engineer, qa-engineer, devops-engineer, security-engineer, data-engineer | Architecture quality, dependency, data-ownership, and recovery evidence | `architecture-review` | none | in PR |
| backend-engineer, frontend-engineer, mobile-engineer, qa-engineer, devops-engineer, security-engineer, data-engineer | Import direction, public entry points, crate layers, and writer-component boundaries | `architecture-fitness-functions` | none | in PR |
| frontend-engineer | HTTP contracts and client retry/access behavior | `api-design`, `api-compatibility`, `api-authorization`, `idempotent-requests` | none | in PR |
| mobile-engineer | Deployed-client HTTP compatibility and retry/access behavior | `api-design`, `api-compatibility`, `api-authorization`, `idempotent-requests` | none | in PR |
| qa-engineer | HTTP contract, old-client, denial, and retry proof | `api-design`, `api-compatibility`, `api-authorization`, `idempotent-requests` | none | in PR |
| security-engineer | HTTP boundary contracts and access enforcement | `api-design`, `api-authorization` | none | in PR |
| data-engineer | Tenant authorization across PostgreSQL, jobs, and exports | `api-authorization` | none | in PR |
| technical-writer | Source-backed HTTP contracts and deprecation lifecycle | `api-design`, `api-compatibility` | none | in PR |
| `api-design` | Design HTTP operation contracts and prove schema, generated-caller, and wire agreement. |
| `api-compatibility` | Check deployed-consumer compatibility and evidence-backed deprecation/removal. |
| `api-authorization` | Enforce access and tenant policy across primary and alternate paths with a denial matrix. |
| `idempotent-requests` | Define durable request admission, replay, expiry, and external-effect reconciliation. |
| backend-engineer, data-engineer, data-analyst, data-scientist, business-analyst, financial-analyst | Cross-store entities, identity, cardinality, grain and lifecycle | `logical-data-modeling` | none | in PR |
| backend-engineer, mobile-engineer, data-engineer, data-analyst | PostgreSQL physical schema and constraint proofs preserving the logical crosswalk | `postgres-schema-design` | none | in PR |
| backend-engineer, qa-engineer, devops-engineer, data-engineer | Live PostgreSQL schema evolution, mixed-version compatibility and resumable backfill | `postgres-migrations` | none | in PR |
| agent-orchestrator, backend-engineer, qa-engineer, devops-engineer, sysadmin, security-engineer, data-engineer, data-analyst | Target-bound direct database changes with exact effects and independent verification | `postgres-change-execution` | none | in PR |
| agent-orchestrator, backend-engineer, qa-engineer, devops-engineer, sysadmin, security-engineer, data-engineer, data-analyst, data-scientist | Effective roles, future-object grants, agent access and authentication/TLS transitions | `postgres-role-administration` | none | in PR |
| backend-engineer, qa-engineer, data-engineer | PostgreSQL concurrent writers and invariants | `postgres-concurrency-control`; atomic updates, constraints, ordered locks and whole-transaction retries with two-session evidence | none | in PR |
| backend-engineer, devops-engineer, data-engineer | PostgreSQL connection topology and pool budgets | `postgres-connection-pooling`; peak deployment accounting and actual transport/session compatibility | none | in PR |
| backend-engineer, sysadmin, data-engineer, data-analyst, data-scientist | PostgreSQL query and index performance | `postgres-query-performance`; workload/reset context, representative plans and bounded index decisions | none | in PR |
| backend-engineer, frontend-engineer, mobile-engineer, qa-engineer, devops-engineer, data-engineer | Real dependency and runtime integration tests | `integration-test-harness`; PostgreSQL, native-framework, Vitest/MSW and legacy-characterization adapters with independent oracles and interruption cleanup | none | in PR |
| backend-engineer | Service reliability, background jobs, and application telemetry | `async-messaging`, `service-resilience`, `opentelemetry-instrumentation` | none | in PR |
| backend-engineer, mobile-engineer, qa-engineer, devops-engineer, data-engineer, seo-engineer | Durable service events and URL change notifications | `async-messaging`, including URL change notification reference | none | in PR |
| backend-engineer, frontend-engineer, mobile-engineer, devops-engineer, data-engineer | Dependency bounds and service draining | `service-resilience` | none | in PR |
| backend-engineer, frontend-engineer, mobile-engineer, devops-engineer, sysadmin, security-engineer, data-engineer | Application instrumentation and security event contracts | `opentelemetry-instrumentation`, including security event contract reference | none | in PR |
| backend-engineer, frontend-engineer, qa-engineer | Checked Node TypeScript deployment artifacts | `typescript-node-services`; Bun and Deno verified only for an actual target | none | in PR |
| backend-engineer, frontend-engineer | Tokio/Axum service runtime behavior | `rust-async-services`; desktop Rust/GPUI remains separate | none | in PR |
