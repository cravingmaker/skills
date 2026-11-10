> **Human documentation.** Agents should not read this page unless a person asks them to.

Language: [English](maintaining-docs.md) · [Bahasa Indonesia](id/maintaining-docs.md)

# Maintaining this handbook

Edit explanations where judgment belongs and regenerate inventories from their source files. The generator also fails when an agent-facing pointer enters the human handbook.

## Contents

- [Source ownership](#source-ownership)
- [Generate and check](#generate-and-check)
- [Keep both languages together](#keep-both-languages-together)
- [Understand the checks](#understand-the-checks)
- [Keep agents out by default](#keep-agents-out-by-default)
- [Refresh evidence without overstating it](#refresh-evidence-without-overstating-it)

## Source ownership

| Content | Source of truth |
| --- | --- |
| Skill membership, kind, coverage assignment, aliases, invocation preference, evaluation status | `catalog/skills.yaml` |
| Description, required edges, conditional named method pointers | Each `skills/*/SKILL.md` and directly linked owned Markdown references/assets |
| Activation, near-miss, and outcome examples | Each skill's `evals/examples.md` |
| Evaluation results | Committed Markdown records under `skills/*/evals/results/`, their tables and reviewed Value lines, compared with current skill-package digests |
| Profile membership | Required closure, checked against `catalog/profiles/` |
| Explanations, worked journeys, status qualifications | Authored handbook text with public source links |
| Changelog | Merged PR metadata and main history |

Generated sections carry paired `BEGIN GENERATED` and `END GENERATED` markers. Edit their source rather than their rendered rows. The catalog owns membership and modes. `handbook/intent-guide.json` adds editorial intent, prompt and neighboring-job explanations, without copying status or required edges. Its groups set the heading and row order of the README's visible tables. Every catalog entry needs exactly one nonempty guidance row; unknown, missing, and duplicate rows fail. Every group also needs `heading_id`; every row needs `want_id` and `neighbor_id`. The `prompt` field stays in English in both editions.

## Generate and check

Use Python 3.12 or newer. The generator uses only the standard library and does not call a model or host.

```sh
python3.12 scripts/build-docs.py --help
python3.12 scripts/build-docs.py
python3.12 scripts/build-docs.py --record-sync
python3.12 scripts/build-docs.py --check
tests/build-docs/run.sh
REQUIRE_VALE=1 ./scripts/validate.sh
```

When the shell's Python is older, use `uv run --python '>=3.12' python` in place of `python3.12`. Default mode writes the generated sections in both languages. `--record-sync` writes only the authored-text hash manifest after validating both editions; it refuses mismatched structure, stale generated sections and invalid links. Check mode reads only and exits 1 on generated or bilingual hash drift, missing intent guidance or input/link findings. All source, marker and link checks run before write mode changes any output. Every successful mode prints a JSON summary on stdout; diagnostics go to stderr.

Data and help go to stdout. Diagnostics go to stderr. Exit 0 means success; 1 means drift, a forbidden pointer, or invalid input; 2 means command-line usage. The small YAML reader deliberately rejects unsupported forms instead of guessing; extending the source schema requires a matching parser fixture.

## Keep both languages together

Update the English page and its `handbook/id/` counterpart in the same change whenever either edition changes. Keep the same page set, section order, heading levels, tables, lists, code blocks and link destinations. Translate the prose and heading labels; preserve commands, identifiers and code. Point local handbook links to that edition and its translated heading. Each page starts with its language's human-only notice and offers a language switch.

The generator writes every handbook block into both editions. Its label table translates fixed presentation text; source descriptions, examples and catalog values stay verbatim. Editorial intent fields have both languages. A new generated block automatically gains its Indonesian home.

Run the generator, review both editions, then run `scripts/build-docs.py --record-sync`. `handbook/id/SYNC.json` records SHA-256 for both pages with generated blocks stripped, including authored code and language switches. `--check` rejects a missing counterpart, mismatched ordered structure or mapped link targets, or either hash differing from the manifest. Its diagnostic names both pages and tells the editor to update both languages and record sync. Recording refuses structurally mismatched pairs and does not translate or certify semantic equivalence; the reviewer owns faithful wording.

Vale continues to lint English handbook pages through the existing `handbook/*.md` selection in `scripts/validate.sh`. Indonesian pages live one level deeper and are excluded from that English-only selection. The English style and every existing English target remain unchanged.

## Understand the checks

The validator calls `uv run --quiet --python '>=3.12' python scripts/build-docs.py --check` after the profile and host-policy checks. It explicitly runs `tests/build-docs/run.sh` because the skill-test loop runs only directories with a matching skill package. It also checks prose in the handbook and changelog.

A new skill must have useful intent guidance in exactly one group in `handbook/intent-guide.json`. Regenerate every changed page and add a detailed command section for any new manual entry. Missing guidance remains a hard error.

The fixtures prove clean output, deterministic repeat generation, visible README category order, missing and duplicate skill rejection, drift rejection, malformed metadata rejection, missing required dependency rejection, profile drift rejection, and forbidden links in representative agent-facing files. Bilingual fixtures also reject missing pages, stale hashes in either language, missing Indonesian intent fields and ordered structure/link differences, and prove that recording refuses mismatches. Evaluation fixtures parse current records, separate invalid and stale-byte history, and reject missing record-link destinations. A deliberately broken generator copy must fail those tests. They do not evaluate prose quality, future host behavior, or raw private evaluation evidence.

## Keep agents out by default

The handbook lives outside the installer's `skills/` tree. No default instruction, skill, reference, asset, template, or script points into it. The short README is the human entry point. Each handbook page begins with a human-documentation notice.

The guard rejects paths into the human directory from agent-facing files, including Markdown/HTML links, reference definitions, code-font pointers and encoded paths. Explicitly human review reports, the generator, its tests and the validator are the bounded exceptions. It does not claim to understand every possible dynamically assembled path or natural-language hint. A broad filesystem search or an explicit human instruction can still reach these files.

Host ignore settings may reduce incidental indexing, but this task has no recorded cross-host proof of their exact behavior. Hard read-deny rules would also block a person from asking an agent to read the handbook. Neither is added here. The separation, installer boundary, notices, and tested pointer check are useful defaults without imposing that restriction.

## Refresh evidence without overstating it

Update an issue only when its current revision and claimed surface have evidence. Keep historical failures and invalid attempts labeled. A clean deterministic docs build is not a new live-host or model-evaluation result.

The changelog uses one entry per merged PR, newest first, with stack landing distinguished from earlier stacked merges. Label open and closed-unmerged work separately from those entries. Public prose must omit private paths, personal identities, credentials, and review transcripts.
