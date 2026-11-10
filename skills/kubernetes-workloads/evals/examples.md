# Examples

Run matched prompts with and without the final skill before changing evaluation status. These cases are prepared, not model-evaluated.

## Activation

- "Review all rendered variants of this Deployment before it ships." Expect the target/schema set, selected policy checks, lifecycle contract and evidence for every variant.
- "Our app restarts whenever its database blips; fix the liveness and readiness manifests." Expect a dependency-independent liveness contract with an outage fixture and measured startup/shutdown behavior.
- "Add a Kustomize production overlay with resource requests, a PDB and topology spread." Expect final rendered checks, capacity/PDB reasoning and an authorized disruption test or named gap.

## Near miss

- "Diagnose the live ImagePullBackOff in this namespace." Expect the `kubernetes-troubleshooting` skill.
- "Build a distributable Helm chart with a values schema." Expect the chart-packaging owner; rendered workload review is one separate check.
- "Design default-deny network policy and tenant RBAC for the cluster." Expect cluster/security policy work.
- "Profile this app to choose CPU and memory capacity." Expect measured sizing work, not fabricated request values.
- "Fix our application SIGTERM handler and health endpoint." Expect the `service-resilience` skill for application code.
- "Run the installed engineering plugin's deploy-checklist for this release." Expect release readiness, not unsolicited manifest changes.
- "Run the installed engineering plugin's incident-response for customer impact." Expect incident coordination; use live diagnosis only where that task calls for it.

## Outcome

- "Reject deliberate bad rendered workloads." Fixture: `tests/kubernetes-workloads/fixtures/valid.json`, then separate variants with privileged true, missing CPU or memory request and a Deployment selector that differs from its Pod labels. With an installed kube-linter and assets/kube-linter.yaml, expect positive pass and each negative to fail with its expected check; absent kube-linter is an explicit skip, not passing runtime evidence. Removing limits alone must still pass, preserving the measured decision.
- "Check the comparison assets at the right gate." Fixture: assets/workload.example.yaml and each assets/negative file. Expect the example to pass native lint, the three lint negatives to fail exactly their header's named checks, and unknown-field.yaml to fail strict target schema validation. Run no cluster command from these inert fixtures.
- "Validate all target and CRD schemas." Fixture: two shipped overlays, with a CRD used only by the second and its schema initially absent. Expect the second variant's required gate to fail until its target-matching CRD schema is supplied; no global ignore. Record render/schema identities and exit codes for both.
- "Separate dependency failure from process failure." Fixture: an owned disposable app whose ready endpoint depends on a fake database while its live endpoint tests local process progress. Drop the fake database. Expect readiness to fail and liveness to keep its declared contract; a variant where liveness calls the fake database must fail the contract test.
- "Prove graceful drain and controller-aware recovery." Fixture: a named disposable target with two healthy replicas, in-flight work, an eviction budget and a delivery controller. Expect the user result across authorized eviction, bounded shutdown and a tested retained artifact/config path; document that deadline failure alone does not auto-rollback and local emulation does not prove managed policy.
