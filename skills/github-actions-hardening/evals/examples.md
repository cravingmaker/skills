# Examples

Run matched prompts with and without the skill only under the coordinator's model-evaluation authority.
These drafts remain unevaluated; the fixture tests are deterministic checks, not paired model results.

## Activation

- "Lock down our GitHub Actions token scopes and fork PR paths." Expect: Build the event-to-consumer matrix and fix confirmed crossings.
- "Our AI review job reads PR bodies and can push commits. Harden it." Expect: Treat prompt input as an injection sink and constrain authority before any write gate.
- "Verify action pins and stop privileged release jobs consuming untrusted caches." Expect: Resolve upstream references live and trace implicit cache/artifact consumers.

## Near miss

- "Write a new matrix workflow for our build targets." Expect: The github-actions-workflow-authoring scope owns the requested graph; security checks accompany it without replacing it.
- "The latest hosted unit test fails; diagnose the causal error." Expect: The fix-ci scope owns failure triage.
- "Run deploy-checklist and decide whether the release is ready." Expect: Go/no-go assessment is broader than the trust-path audit.
- "Start incident-response and assign responders for our outage." Expect: Incident command does not load this static/inert security audit.

- "Set up a cloud role trust policy for our deploy identity." Expect: The workload-identity-federation scope owns provider-side trust and denial tests.
- "Verify image signatures and build attestations." Expect: The software-supply-chain-provenance scope owns artifact verification.
- "Install the repository-wide workflow security gate." Expect: The project-guardrails scope owns enforcement wiring; deeper trust-path findings use this audit.
- "Provision ephemeral runner hosts and restrict their network." Expect: Runner infrastructure and host isolation belong to their infrastructure owner.

## Outcome

- "Prove a hostile PR title stays inert." Expect: In a disposable directory, pass the literal string $(touch marker) through the actual changed shell step. Assert exact captured bytes and that marker does not exist; inspect downstream uses and native analyzer output.
- "Reject a release input produced through the wrong trust path." Expect: An owned inert fixture has separate low-trust and release jobs, a shared cache path, and an artifact with altered bytes or producer identity. The proposed controls reject the crossing before execution; an attacker-supplied matching checksum does not establish origin.
- "Check a direct action, annotated tag and reusable call." Expect: Offline REST fixtures return exact refs and peeled tag objects. Matching synthetic full pins pass; tag-only references, wrong commits and missing tag evidence fail. No real API or token is used by fixtures. A production claim still needs live upstream readback.
