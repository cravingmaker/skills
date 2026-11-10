# Examples

Run each prompt with and without the final skill before changing its catalog status from unevaluated. Offline fixtures establish helper behavior only.

## Activation

- "Review this saved OpenTofu plan before we apply it; will it delete our database?" Expect: digest/target binding, every replace/delete and recovery evidence, with a review-only verdict unless application is already authorized.
- "Our Terraform CI wrapper treats detailed exit code 2 as an error. Check the plan review path." Expect: the actual wrapper is tested with 0/1/2 synthetic exits, with engine errors kept distinct from planned changes.
- "Check this saved plan for unknown IAM permissions, public buckets and estimated cost changes." Expect: private value inspection, policy evidence, current pricing assumptions and conditions for material unknowns.

## Near miss

- "Rename a Terraform address without recreating the resource and move the backend." Expect: the `terraform-state-operations` skill owns the operation; plan review alone is insufficient.
- "Explain HCL variable types and write a reusable module." Expect: module authoring, without loading this saved-plan reviewer.
- "Set up OIDC so our Terraform job stops using stored cloud keys." Expect: the `workload-identity-federation` skill owns the trust change.
- "Use engineering deploy-checklist to coordinate tonight's release." Expect: deployment coordination; this skill stays inactive unless a specific saved plan needs review.
- "Use engineering incident-response: production is down after a deployment." Expect: incident coordination; this skill does not become an incident commander.

## Outcome

- "Summarize a synthetic plan with format_version 1.2, planned_values {}, and a managed aws_db_instance change with actions [delete, create], replace_paths [[storage, synthetic-private-key]], and before/after containing SYNTHETIC_PAYLOAD_MUST_NOT_APPEAR." Expect: helper exit 1, replacement/stateful flag and forcing root `storage`; neither values nor nested synthetic key appear in either stream. Repeat with [create, delete] and [delete].
- "Check captured engine exits using an empty native-shaped plan for 0, any plan for 1, and a managed update plan for 2." Expect: helper acceptance for consistent 0/2, engine error with no stdout for 1, findings for inconsistent status/artifact pairs. Test the repository wrapper separately with a fake engine; this helper result is not evidence that an unseen wrapper works.
- "Review only JSON without its binary plan, then replace the binary artifact after review." Expect: JSON digest and missing binding are reported; no apply-ready verdict from JSON alone, and the changed binary invalidates the prior review. No apply, cloud call or sensitive body appears in evidence.
- "Summarize a plan with a string instance key, nested unknown mask, changed output, incomplete flag and an unfamiliar action string." Expect: string instance key and unfamiliar action are withheld, unknown/output metadata remain visible, and incompleteness/unsupported work cannot pass as a complete review.
- "Test the captured-status classifier through a fail-fast shell wrapper and a fake engine exiting 0, 1, 2 and 3." Expect: success/false, error with no stdout, success/true, and error with no stdout. The helper invokes no engine or cloud command; the repository's actual wrapper still needs its own test.
- "Delete a vendor_retained_object resource while adding --stateful-type vendor_retained_object." Expect: helper exit 1 with a stateful-destruction finding; no payload is emitted, and the option does not exempt other findings.
