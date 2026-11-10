# cravingmaker/skills

[![CI](https://github.com/cravingmaker/skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/cravingmaker/skills/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/github/license/cravingmaker/skills)](https://github.com/cravingmaker/skills/blob/main/LICENSE)

Craving Maker's opinionated collection of [Agent Skills](https://agentskills.io). Each skill is a folder of instructions, scripts, and resources that an agent loads when a task calls for it.

- **One open format.** Every skill follows the [Agent Skills specification](https://agentskills.io/specification), so it works in Claude Code, Codex, Cursor, and the other [skills-compatible clients](https://agentskills.io/clients).
- **Enforcement over instructions.** Where a rule can be a check (a linter, a type, a test, a CI job), the skill ships or sets up the check; prose covers only the judgment calls.
- **Validated on every change.** CI runs the pinned [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) validator, a repository checker for provenance and examples, and fixture tests for the bundled tools.

## Contents

- [Skills](#skills)
- [Installation](#installation)
- [Layout](#layout)
- [Adding a skill](#adding-a-skill)
- [Contributing and security](#contributing-and-security)
- [License](#license)

## Skills

| Skill | Description |
| ----- | ----------- |
| [clear-communication](skills/clear-communication) | Clear, lean, faithful communication in both directions: understanding the request and writing the result. Ships a standing contract for AGENTS.md and a Vale style. |
| [project-guardrails](skills/project-guardrails) | Sets up or audits the checks that make a wrong change fail, in the order readability, maintainability, security, performance. |
| [toolchain-upgrade](skills/toolchain-upgrade) | Upgrades lint, format, and type tooling by comparing effective configuration before and after and deciding every change. |
| [correct](skills/correct) | Turns a repeated agent mistake into a check that fails, at the highest layer that can hold it. |
| [agent-orchestrator](skills/agent-orchestrator) | Role: equips an agent to run a fleet of agents as their product and project manager. |
| [work-decomposition](skills/work-decomposition) | Imports approved tickets with exact hashes and Proof, then checks ownership, dependencies and a finite budget. |
| [agent-briefing](skills/agent-briefing) | Writes briefs a fresh agent can execute with no history, with a checker for missing fields. |
| [agent-debate](skills/agent-debate) | Runs bounded, evidence-based reviews between agents, with a checker for review reports. |
| [result-verification](skills/result-verification) | Accepts agents' work by rerunning checks and verifying claims at the source, with a write-boundary checker. |
| [decision-log](skills/decision-log) | Keeps an on-disk run record (plan, log, decisions, raw reports) so multi-agent work survives interruption. |
| [grilling](skills/grilling) | Resolves consequential design questions in bounded interview rounds, reusing settled answers. |
| [grill-with-docs](skills/grill-with-docs) | Grounds an interview in configured domain docs and records resolved glossary terms and ADRs. |
| [domain-modeling](skills/domain-modeling) | Maintains domain vocabulary and immutable, superseded ADRs at configured paths. |
| [to-spec](skills/to-spec) | Writes an agreed spec with stable stories, source hashes, acceptance and named Proof. |
| [to-tickets](skills/to-tickets) | Files approved vertical slices with exact status, blockers, acceptance and Proof. |
| [triage](skills/triage) | Verifies tracker claims and routes issues and external PRs through configured triage states. |
| [wayfinder](skills/wayfinder) | Charts decision tickets for an unclear goal and resolves the next consequential question. |
| [to-questionnaire](skills/to-questionnaire) | Drafts recipient-specific questions from known facts and decision gaps without sending them. |
| [setup-agent-skills](skills/setup-agent-skills) | Maintains one Agent skills block and configured tracker, triage and domain paths. |
| [prototype](skills/prototype) | Builds and observes a bounded throwaway artifact to answer one design question. |
| [sharpen](skills/sharpen) | Refines a requested prompt without expanding or executing the task. |
| [research](skills/research) | Answers bounded questions from primary sources with explicit inference and search limits. |
| [how](skills/how) | Traces an actual execution path and responsibilities from source anchors. |
| [why](skills/why) | Reconstructs design intent from attributable history and calibrated uncertainty. |
| [grill-me](skills/grill-me) | Manual no-doc entry into the owned grilling interview. |
| [bro](skills/bro) | Manual entry that repairs the last answer through clear-communication. |
| [wait-what](skills/wait-what) | Manual entry that explains the last unclear point using the user's context. |
| [codebase-design](skills/codebase-design) | Designs deep modules, precise interfaces and testable seams while preserving real trust boundaries. |
| [architect](skills/architect) | Compares grounded interface sketches and records a bounded design with trade-offs and rationale. |
| [improve-codebase-architecture](skills/improve-codebase-architecture) | Surveys architecture candidates and renders an escaped, offline report before product changes. |
| [implement](skills/implement) | Builds one authorized slice with appropriate behavior proof and scoped review. |
| [implement-spec](skills/implement-spec) | Runs the exact approved ticket graph with one coordinator, finite budget and integration acceptance. |
| [tdd](skills/tdd) | Proves meaningful red/green behavior at accepted seams, then refactors within the slice. |
| [diagnosing-bugs](skills/diagnosing-bugs) | Reproduces a symptom, discriminates causes and verifies the causal fix. |
| [wizard](skills/wizard) | Creates resumable setup wizards with parser round trips and scoped secret-safe writes. |
| [change-review](skills/change-review) | Reports separate Standards and Spec findings with source evidence and bounded probes. |
| [sol-loop](skills/sol-loop) | Runs authorized review, fix and recheck rounds with stable findings and an honest finite stop. |
| [council](skills/council) | Manual dispatch to the code-fix loop, design debate or a report-only provider panel. |
| [interrogate](skills/interrogate) | Manual report-only probe mode for change-review, preserving static and executed evidence. |
| [blast-radius](skills/blast-radius) | Traces real consumers and user-visible effects with claim-appropriate proof. |
| [benchmark-checklist](skills/benchmark-checklist) | Checks comparable workloads, correctness, sensitivity, noise and measurement meaning. |
| [create-verification-skill](skills/create-verification-skill) | Authors one namespaced project driver in bounded-gap or full-feature-map mode. |
| [maintain-verification-skill](skills/maintain-verification-skill) | Audits an existing driver and declared feature map, separating drift from product regressions. |
| [file-pr](skills/file-pr) | Drafts a diff-grounded PR body or files and updates within authority, returning links and state. |
| [pr](skills/pr) | Manual body-only entry into file-pr; remote filing requires its own task authority. |
| [babysit-pr](skills/babysit-pr) | Watches only at the root on request or for a pending authorized action, preserving required gates and old feedback. |
| [fix-ci](skills/fix-ci) | Triages the actual CI failure and applies an evidenced repair or one bounded retry. |
| [leaving-pr-comments](skills/leaving-pr-comments) | Collects, verifies and answers exact review threads within posting authority. |
| [modernize](skills/modernize) | Restores an aging PR against its real base with intent checks, conflict proof and captured leases. |
| [takeover](skills/takeover) | Reconstructs inherited work and verifies current claims before continuing the scoped task. |
| [full-send](skills/full-send) | Carries explicit finish authority through proof, review, filing, root waiting and guarded merge. |
| [full-stop](skills/full-stop) | Manual prepare-only entry that propagates no-merge and verifies no owned pending merge remains. |
| [retro](skills/retro) | Compares session evidence with the requested workflow and identifies the smallest supported improvement. |
| [handoff](skills/handoff) | Writes a temporary continuation note with exact pointers, proof limits, remaining budget and next action. |
| [writing-for-agents](skills/writing-for-agents) | Crafts discoverable instructions with clear completion criteria, progressive detail and honest evaluation. |
| [teach](skills/teach) | Explains grounded mechanism and intent; durable learning artifacts require an explicit workspace request. |
| [recall](skills/recall) | Finds an unknown prior-run locator through scoped supported history search and exact evidence. |
| [ketchup](skills/ketchup) | Reports read-only since-last-human state and every pending user choice, with current evidence. |
| [backend-engineer](skills/backend-engineer) | Role: routes service contracts, data, runtime, and failure behavior through owned capability skills. |
| [architecture-decisions](skills/architecture-decisions) | Audits decision history and runs comparable trials for consequential recovery, concurrency, precision, and operating constraints. |
| [architecture-review](skills/architecture-review) | Reviews system quality with dependency, churn, critical-journey, data-ownership, and recovery evidence. |
| [architecture-fitness-functions](skills/architecture-fitness-functions) | Enforces architectural dependency boundaries with allowed and forbidden fixtures and proof after setup reapplication. |
| [api-design](skills/api-design) | Designs an HTTP operation contract before its handler: resources, methods, errors, pagination, filters, limits, and conditional updates. |
| [api-compatibility](skills/api-compatibility) | Checks whether an API change breaks deployed consumers and plans its versioning or deprecation. |
| [api-authorization](skills/api-authorization) | Enforces object, property, function, and tenant authorization, then proves allowed and denied paths with a matrix. |
| [idempotent-requests](skills/idempotent-requests) | Makes a retried unsafe request produce one scoped durable effect: key admission, fingerprint, in-flight behavior, replay, expiry, and provider reconciliation. |
| [logical-data-modeling](skills/logical-data-modeling) | Defines entities, identity, cardinality, grain and lifecycle when source systems or consumers disagree about what records mean. |
| [postgres-schema-design](skills/postgres-schema-design) | Designs PostgreSQL tables and constraints that enforce supplied identity, relationship, type and tenancy rules. |
| [postgres-migrations](skills/postgres-migrations) | Plans and rehearses a PostgreSQL schema change on tables with traffic using expand, compatible deploy, resumable backfill, validation and contract. |
| [postgres-change-execution](skills/postgres-change-execution) | Prepares and executes a scoped direct PostgreSQL or Neon data fix, grant or emergency administrative change on a non-disposable target. |
| [postgres-role-administration](skills/postgres-role-administration) | Provisions or audits effective PostgreSQL roles, ownership, grants and future-object access. |
| [postgres-concurrency-control](skills/postgres-concurrency-control) | Prevents lost updates, write skew and double booking in PostgreSQL. |
| [postgres-connection-pooling](skills/postgres-connection-pooling) | Chooses PostgreSQL connection paths and budgets pools across peak app instances, workers, migrations and an operator reserve. |
| [postgres-query-performance](skills/postgres-query-performance) | Diagnoses slow PostgreSQL queries from workload statistics and representative plans. |
| [integration-test-harness](skills/integration-test-harness) | Builds or audits isolated tests when real database, cache, broker, storage or native runtime semantics matter. |
| [async-messaging](skills/async-messaging) | Makes event publication and background jobs survive duplicates and crashes. |
| [service-resilience](skills/service-resilience) | Bounds dependency time and work in service code. |
| [opentelemetry-instrumentation](skills/opentelemetry-instrumentation) | Adds or repairs telemetry in application code: service spans, correlated JSON logs, bounded metric labels, queue context, and security events. |
| [typescript-node-services](skills/typescript-node-services) | Builds or repairs a Node TypeScript service so its deployed entry matches what was checked. |
| [rust-async-services](skills/rust-async-services) | Builds or repairs a Tokio/Axum service's state, tasks, cancellation, middleware, and shutdown. |
| [devops-engineer](skills/devops-engineer) | Role: routes delivery and operations through owned capability skills with tool-backed validation and recovery evidence. |
| [shell-scripting](skills/shell-scripting) | Writes or repairs executable Bash, POSIX sh or zsh scripts for declared macOS and Linux targets. |
| [zsh-configuration](skills/zsh-configuration) | Diagnoses or changes macOS zsh startup and interactive state. |
| [runbook-authoring](skills/runbook-authoring) | Writes and rehearses alert-linked runbooks with diagnostic branches, bounded mitigations, abort, recovery and escalation. |
| [release-rollback-planning](skills/release-rollback-planning) | Writes and rehearses the undo before a deploy, bound to artifact digests, config, schema state and irreversible effects. |
| [github-actions-workflow-authoring](skills/github-actions-workflow-authoring) | Writes or restructures GitHub Actions workflows, job graphs, matrices, reusable workflows and composite actions. |
| [github-actions-hardening](skills/github-actions-hardening) | Audits and fixes GitHub Actions trust paths, token permissions, action pins, untrusted inputs, caches and artifacts. |
| [release-automation](skills/release-automation) | Automates versions, changelogs, tags and GitHub releases with release-please, Changesets or semantic-release. |
| [software-supply-chain-provenance](skills/software-supply-chain-provenance) | Produces and verifies SBOMs, build provenance and signatures for images, binaries and packages. |
| [dependency-vulnerability-triage](skills/dependency-vulnerability-triage) | Triages package, container image or OS advisories against installed or shipped software. |
| [container-image-build](skills/container-image-build) | Writes or improves a Dockerfile and proves the final image runs on its target architecture. |
| [container-runtime-hardening](skills/container-runtime-hardening) | Hardens how containers run on Docker or a single host outside Kubernetes. |
| [docker-compose-environments](skills/docker-compose-environments) | Builds or fixes Docker Compose environments for local development, CI integration tests or single-host deployment. |
| [kubernetes-workloads](skills/kubernetes-workloads) | Writes or reviews Kubernetes manifests and Kustomize overlays for probes, resources, shutdown, rollout and workload security. |
| [kubernetes-troubleshooting](skills/kubernetes-troubleshooting) | Diagnoses Pending pods, CrashLoopBackOff, OOMKilled, image pulls, failing probes, stuck rollouts and Service failures. |
| [terraform-plan-review](skills/terraform-plan-review) | Reviews a saved Terraform or OpenTofu plan for destructive changes, exposure, unknowns, policy and cost. |
| [terraform-state-operations](skills/terraform-state-operations) | Reconciles Terraform or OpenTofu state without accidental resource recreation. |
| [workload-identity-federation](skills/workload-identity-federation) | Configures or repairs OIDC workload federation from CI or Kubernetes service accounts to clouds and registries. |
| [secrets-management](skills/secrets-management) | Chooses and wires secret delivery and lifecycle for pipelines and workloads. |
| [prometheus-alerting-rules](skills/prometheus-alerting-rules) | Writes or repairs Prometheus recording rules, alerts and Alertmanager routes, with tests for rate, histogram and missing-data math. |
| [slo-error-budgets](skills/slo-error-budgets) | Defines SLIs, SLOs and error-budget policy, and generates and tests multiwindow burn-rate alerts. |
| [postgres-version-upgrades](skills/postgres-version-upgrades) | Plans and rehearses PostgreSQL minor updates and major-version transitions with compatibility, cutover and recovery evidence. |

See [the catalog](catalog/skills.yaml) for evaluation status and each skill's `evals/results/` for outcomes and limits. Explicit entries use the catalog's `invocation: user`; host policy grants no additional task authority.

## Installation

Install the skills into any supported agent with the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add cravingmaker/skills
```

To install a role or a skill together with every skill it requires, clone this repository and run the installer (needs [uv](https://docs.astral.sh/uv/)):

```bash
scripts/install-skills.py --target ~/.claude/skills clear-communication
scripts/install-skills.py --target ~/.claude/skills --apply clear-communication
scripts/install-skills.py --target ~/.claude/skills --mode symlink --apply <role-or-skill>
```

The default prints a JSON preview; `--apply` writes. For the gated upstream replacement, use [the cutover checklist](docs/cutover.md). See [installation and host policy](docs/installing.md) for explicit Claude settings, Codex generation, ownership conflicts and temporary-host checks. It lists any upstream skills a role relies on so you can install them from their source. To install one skill by hand, copy its folder from `skills/` into the agent's skills directory, for example `~/.claude/skills/` for Claude Code.

For everyday answers to follow the communication rules without loading a skill, paste the standing contract from [clear-communication/references/house-style.md](skills/clear-communication/references/house-style.md) into your AGENTS.md or CLAUDE.md.

## Layout

```
.
├── skills/                 # One folder per skill
│   └── <skill-name>/
│       ├── SKILL.md        # Required: frontmatter and instructions
│       ├── evals/          # Required: activation, near-miss, and outcome examples
│       ├── agents/         # Generated openai.yaml only for invocation: user
│       ├── references/     # Optional: documentation loaded on demand
│       ├── scripts/        # Optional: executable code
│       └── assets/         # Optional: templates, configs, and data
├── template/               # Starting point for a capability skill
├── template-role/          # Starting point for a role router
├── catalog/                # Skill catalog, coverage matrix, install profiles, reserved names
├── docs/                   # Authoring guide
├── scripts/                # Validation, catalog, profile, freshness, and install scripts
└── tests/                  # Fixtures for every script and the Vale style
```

## Adding a skill

Copy the template to a folder named after the skill. The folder name must match the `name` field of its `SKILL.md`:

```bash
cp -r template skills/my-skill
```

Set `name`, write a `description` that says what the skill does and when to use it, and fill in `evals/examples.md`. Add the skill to [catalog/skills.yaml](catalog/skills.yaml) and update [catalog/coverage.md](catalog/coverage.md). Generate the profiles, then validate with [uv](https://docs.astral.sh/uv/) and, for the prose tests, [Vale](https://vale.sh) 3.26.0:

```bash
scripts/build-profiles.py
scripts/build-host-config.py --check
./scripts/validate.sh
```

Add the skill to the table in [Skills](#skills). The [authoring guide](docs/authoring-guide.md) sets the bar every skill meets; [AGENTS.md](AGENTS.md) lists the repository rules.

## Contributing and security

Follow the [Code of Conduct](https://github.com/cravingmaker/.github/blob/main/CODE_OF_CONDUCT.md) when participating in the project. Report vulnerabilities privately as described in the [security policy](https://github.com/cravingmaker/.github/blob/main/SECURITY.md).

## License

MIT © [cravingmaker](https://github.com/cravingmaker), except skills that carry their own `LICENSE-*` file for adapted third-party material.
