---
name: github-actions-hardening
description: Audit and fix GitHub Actions trust paths, token permissions, action pins, untrusted inputs, caches, artifacts and runner exposure. Use to "secure our workflows", review fork-PR privilege risks, or harden AI steps that read issue or PR text.
license: MIT
compatibility: Python 3.12+ for the optional resolver; live resolution uses the GitHub REST API.
---

# GitHub Actions hardening

Trace untrusted input to every privileged consumer, then close each confirmed crossing with a small patch and a failing boundary test.
Limit security probes to static analysis or inert fixtures in repositories the user owns.

## Map authority

Read repository guidance, workflows, local/composite actions, reusable calls, scripts and dependency installation steps.
Record the actual repository, source SHA, relevant events and authorized changes.
Read [references/trust-matrix.md](references/trust-matrix.md) before mapping each event-to-consumer path.
Capture token scopes, OIDC, secrets, checkout source, runner isolation, cache access, artifacts and protected environments for every job.
Read back relevant repository and environment settings; an environment name in YAML does not establish protection.
Finish this step when every low-trust input has a named consumer and each write capability has a justified source of trust.

## Check and constrain

Run the repository-pinned actionlint and zizmor with its auditor persona; check current flags in installed help before collecting SARIF.
Review suppressions as decisions with an owner and rationale.
Resolve action, reusable workflow, container-action and downloaded-tool references live from primary upstreams.
Inspect transitive dependencies; a pinned top-level action can still fetch mutable code.
Read [references/action-refs.md](references/action-refs.md) when choosing full SHA pins or a supported native lockfile policy.
The optional resolver checks remote pins in parser-produced JSON against live upstream tag refs:

```sh
python3 <skill>/scripts/resolve-action-refs.py workflow.json --tags tags.json
```

The Python 3.12+ script uses the standard library and read-only GitHub REST requests.
It prints JSON findings and resolved commit IDs to stdout, generic setup diagnostics to stderr, and exits 0 pass, 1 findings or 2 invalid input/API failure.
Supply `GH_TOKEN` through the existing secret mechanism only when needed; it never prints the token or API bodies.
It supports strict SHA mode, not native workflow lockfile verification; use the platform's current lock checker for that branch.

- **Code.** Keep fork PR validation separate from release authority. Privileged trigger jobs execute only trusted code, including package scripts and downloaded tools. Inspect `pull_request_target`, `workflow_run`, issue and comment events even if checkout defaults appear protective.
- **Input.** Pass untrusted shell values through quoted environment variables or structured inputs. Follow values through later scripts, `eval`, command construction and template expansion; changing the first interpolation is insufficient.
- **AI.** Treat every AI step reading issue text, PR bodies, comments, diffs or repository files as an injection sink. Run it without secrets and with minimal read permissions; proposed writes need a maintainer-controlled gate that never executes the input as instructions.
- **Tokens.** Use an empty workflow permission baseline and minimal per-job grants. Disable persisted checkout credentials when unnecessary. A broader token or secret inheritance needs a stated reason and a narrower alternative assessment.
- **Caches.** Separate low-trust writers from privileged consumers; inspect implicit caches and overrides. Release and publication jobs restore no cache. A cache hit supplies bytes, not authenticated build provenance.
- **Artifacts.** Verify origin repository, event, source SHA, workflow, digest and authenticated producer before privileged use. Hashes supplied by the same untrusted producer prove consistency only. Bind the expected digest to a trusted source.
- **Runners.** Keep untrusted public contributions off persistent self-hosted runners. Inspect one-job lifecycle, network reach and credential persistence; workflow permissions cannot isolate the host.
- **Environments.** Read back protections, ref eligibility and bypass settings for the target plan and repository visibility. Serialize mutation without cancelling an active release or deployment.

Read [references/injection-and-artifacts.md](references/injection-and-artifacts.md) when changing shell/AI input handling, cache access or artifact promotion.
Finish this step when native findings are fixed or explicitly accepted with owner and reason, and every remaining trust assumption has readback or a test.

## Prove the boundary

Read [the inert payloads](references/hostile-inputs.txt) when choosing shell fixture inputs.
Pass each through the actual changed step, assert exact captured bytes, and require that no separate evaluated marker appears.
A disposable fixture may instead use a marker file and assert that it was not created.
Test AI handling with inert requests for a forbidden write; inspect available permissions and the maintainer gate instead of assuming a model will ignore instructions.
Use synthetic low-trust cache/artifact fixtures; a substituted digest and a wrong producer must be rejected before execution.
Include a positive trusted case and repeat it after the rejection case.
Keep fixtures local unless the task authorizes a disposable hosted target; never expose real secrets as canaries.
When hosted behavior is required, record the actual run, head, event and readback.
`act` does not prove GitHub's token, OIDC or environment behavior.

For graph restructuring, read the `github-actions-workflow-authoring` skill when installed.
For cloud trust claims, read the `workload-identity-federation` skill when installed.
For artifact signatures and attestations, read the `software-supply-chain-provenance` skill when installed.
For repository-wide enforcement, read the `project-guardrails` skill when installed.
Production mutations, credential rotation, traffic changes and force-push require explicit task authority; confirm repository/account/project/region/cluster as applicable immediately before any authorized mutation.

Done when each reported crossing has source evidence, a scoped fix, native check output and a positive/negative proof, with unavailable hosted evidence stated.
Report file locations, trigger-to-effect paths, exact resolved pins, tested source SHA and residual assumptions without secret values.
Read [references/sources.md](references/sources.md) when verifying current action defaults, cache policies, lockfile support, tool flags or plan-specific protection behavior.
