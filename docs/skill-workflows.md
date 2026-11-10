# Create, change, or review a skill

Read the [authoring guide](authoring-guide.md) before writing or reviewing a skill. It owns the content bar, package rules, and provenance schema. These procedures run from the repository root; replace the example name with the skill you are working on.

## Create a skill

Use this when a reusable job needs its own trigger and checkable deliverable. Extend an existing skill or its references when the job does not justify a separate entry.

1. Check `catalog/skills.yaml`, `catalog/reserved-names.txt`, and nearby skills for an existing owner. Choose a canonical name and create the package:

   ```sh
   task_skill=example-capability
   cp -R template "skills/$task_skill"
   ```

2. **Baseline first.** Write `evals/examples.md` and the Outcome fixture before the skill body: each Activation and Near miss gets a concrete quoted prompt and expectation, each Outcome an observable result. Run the Outcome prompts without any skill (one host session in a disposable copy of the fixture, or the harness's baseline arm with a frontmatter-only `SKILL.md`). If the baseline already meets the Outcome, stop: the model does the job and no skill is needed. If the gap is a rule a script can enforce, prefer a project check through the `project-guardrails` or `correct` skill. Done when a recorded baseline fails an expected Outcome.
3. Write `SKILL.md` around what the baseline missed: checks, authority limits and required evidence, not domain knowledge the model already has. Declare only required dependencies in `metadata.requires`; link optional methods conditionally. Done when the trigger, deliverable, evidence, and stop conditions meet the authoring bar.
4. Add a capability entry in `catalog/skills.yaml` with `roles: [all]` or `[agent-orchestrator]`, `status: unevaluated`, and `invocation: user` only for explicit selection. Update `catalog/coverage.md`. Done when the new job has one owner and its dependencies resolve.
5. Generate the inventories and host policy:

   ```sh
   scripts/check-skills.py "skills/$task_skill"
   scripts/build-profiles.py
   scripts/build-host-config.py
   scripts/build-host-config.py --apply
   scripts/build-host-config.py --check
   scripts/build-docs.py
   scripts/build-docs.py --check
   ```

   Review the host-policy preview before applying it. If the docs builder requests intent guidance, add one useful row at the file it names, in exactly one category, then rerun it. Follow its command-section diagnostic for a new explicit entry. Done when generated output and its checks agree with the new package.
6. Run [paired evaluations](running-evals.md) when authorized, and [validate the candidate](validating.md). Include the package, catalog, coverage, generated files, and reviewed public results in the change. Done when checks pass and the evaluation status matches the evidence; without authorized model runs, leave it unevaluated and report that limit.

## Adopt or update an upstream method

Use this when retaining third-party wording, methods, scripts, prompts, or assets, including updates to an already adapted skill.

1. Follow the create or change procedure for the owned destination. Review the upstream license before copying anything. Pin each contributor to a full commit SHA and list every retained input; a primary source URL alone misses secondary contributions.
2. Export each pinned file and verify its original byte hash. Set `task_upstream` to the upstream checkout, `task_revision` to the full SHA, and `task_path` to one source file:

   ```sh
   task_input=$(mktemp)
   git -C "$task_upstream" show "$task_revision:$task_path" > "$task_input"
   shasum -a 256 "$task_input"
   git diff --no-index -- "$task_input" "skills/$task_skill/SKILL.md"
   rm -- "$task_input"
   ```

   A diff exits 1 when files differ; inspect those differences. For other destinations, use the actual receiving file. Done when each retained input has a verified hash and reproducible comparison.
3. Apply the [provenance manifest schema](authoring-guide.md#provenance-manifests): set `license`, `metadata.source`, `metadata.source-revision`, `metadata.source-files`, and `metadata.local-changes`; link `references/SOURCES.md` directly from `SKILL.md`. Keep a complete `LICENSE-<source>` per contributor, with the required adapted-file header. Preserve Apache notices and mark changed files. On an update, keep attribution for older contributions that remain. Done when every retained contribution has its manifest row and legal files.
4. Run `scripts/check-skills.py "skills/$task_skill"` and manually compare the manifest against the pinned inputs and full legal texts. Then follow the change procedure's eval selection and [candidate validation](validating.md). Done when provenance is complete, checks pass, and claims refer to the tested owned bytes.

## Change a skill

Use this for an existing skill's description, instructions, scripts, references, dependencies, or invocation policy.

1. Read the skill, its linked resources, examples, public results, required callers, and optional routes. Inspect the diff with `git diff -- "skills/$task_skill" catalog/skills.yaml`. Name the behavior being changed and its affected callers before editing.
2. Select evidence by the changed behavior:

   | Change | Evidence to rerun |
   | --- | --- |
   | Description, trigger, or invocation | All Activation and Near miss examples; affected explicit-entry and host-policy checks |
   | Method, linked instructions, or required dependencies | Affected Outcomes and caller flows; all Activation and Near miss pairs at the final bytes before restoring evaluated status |
   | Shipped script | Its offline fixture suite and affected Outcomes; prove rejection, acceptance, and repeat behavior for a changed guardrail |
   | Spelling, formatting, or legal metadata with unchanged behavior | Deterministic checks and source review; record why behavioral reruns add no evidence |

3. Mark a materially changed skill `unevaluated` while matching paired coverage is missing. Preserve older and invalid records as history. When dependencies or invocation change, rerun the generation commands above. Done when the implementation, callers, examples, and generated files agree.
4. Run the selected checks, [paired evals](running-evals.md) within authority, and [candidate validation](validating.md). Done when results refer to the final bytes, comparative regressions are resolved or reported, and the catalog status is justified.

## Review a skill

Use this for a read-only audit or a scoped change review. Make edits only when the task authorizes them.

1. Read the [authoring bar](authoring-guide.md#the-bar-for-a-capability-skill), the package and its linked resources, catalog entry, callers, and evaluation records. For adapted material, perform the pinned-source and legal review above.
2. Run these checks and the skill's `tests/<name>/run.sh` when it exists:

   ```sh
   scripts/check-skills.py "skills/$task_skill"
   scripts/check-catalog.py
   scripts/build-profiles.py --check
   scripts/build-host-config.py --check
   scripts/build-docs.py --check
   ```

3. Check trigger scope, decision rules, completion evidence, portable scripts, required versus optional links, freshness, provenance, and whether the skill changes the baseline result. Mechanical success proves package consistency; read responses and artifacts for behavioral claims. Request any new model runs through the [eval procedure](running-evals.md) rather than starting them as part of a deterministic audit.
4. Report each finding with a file and line, violated requirement, concrete failure, and smallest fix. Separate reproduced defects, unrun checks, and optional improvements. Done when every authoring requirement has a verdict and the reported checks describe the candidate actually reviewed. A read-only review ends with the report.
