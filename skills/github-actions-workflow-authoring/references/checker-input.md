# Checker input

Read this when running `check-workflow-contract.py`.

Pass one or more JSON documents produced from the actual workflow YAML with the repository's established YAML parser.
Run actionlint first so duplicate keys, invalid job forms and expression mistakes are rejected before conversion.
Use a YAML schema that preserves the `on` key as a string; a conversion that turns it into `true` is invalid.
Record the source file SHA-256, parser version and conversion command beside the check output.
Do not hand-recreate a smaller graph in JSON.

For a repository already using Mike Farah's yq, check its installed help and version, then use its JSON output mode:

```sh
yq -o=json '.' .github/workflows/ci.yml > workflow.json
```

Other repository parsers are acceptable when their parsed document preserves the same mapping, sequences and scalar values.
The checker itself has no YAML dependency.

`--rules` accepts a JSON array of effective rule objects returned by each applicable ruleset detail endpoint, or an object with `rules`, or an array of those ruleset detail objects.
Fetch the current repository rulesets including inherited ones, then fetch each relevant detail body; also inspect legacy branch protection when it is in use.
Prefer the effective branch rules endpoint `repos/{owner}/{repo}/rules/branches/<branch>` when available; it returns rule objects for the chosen branch.
For legacy protection, pass the raw required-status-checks object with `contexts` and/or `checks`, or project it into rule objects while preserving the original readback.
Do not send API tokens, unrelated rule configuration or full workflow environment values to logs.

The checker matches contexts to unique non-matrix runner job names, falling back to job IDs when `name` is absent.
Provide all workflows that own the required contexts.
External check providers, expression-based names and caller-prefixed reusable checks need actual hosted check-run evidence; this helper cannot resolve them.
A passing comparison says only that the parsed graph contains matching static names, not that an event reaches them or that a gate's shell script rejects failure.
For environment jobs, both workflow and job cancellation settings are checked independently.
Release jobs without an `environment` and expression results still need source review and hosted evidence.
