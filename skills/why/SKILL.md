---
name: why
description: "Reconstruct why a design or behavior exists, or check whether agent notes match the user's original instruction. Use for design rationale, incidents, historical constraints, thresholds, or disputed human rulings; separate attributable evidence from inference."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/why/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/why/SKILL.md"
  local-changes: "Kept confidence tiers, scoped human rulings, history and conditional service methods; removed category-wide fan-out, tool/provider maps, secret-bearing discovery, and assumed history availability."
---

# Why

Reconstruct the forces behind a design from historical evidence. Current code shows the mechanism; it does not prove the author's intent.

## Anchor the question

Identify the target file, symbol, behavior, or decision and the version or period in question. Reuse the user's context, existing source anchors, and known rulings.

Read [the epistemics rules](references/epistemics.md) when classifying rationale or claims about human decisions. Preserve the attributable original wording and scope of a relevant human ruling. A copied agent summary remains an interpretation, however often it appears.

## Select evidence that can answer it

Start with nearby rationale, comments, tests, ADRs, and available history. Follow the change through renames, its introducing commits, associated PR discussion, and linked issues when accessible. Git history, PR access, and service history are not guaranteed.

Select further sources because they could resolve a concrete gap. A sufficient direct answer can be reported inline. There is no requirement to query every category or spawn investigators.

- Read [the source-selection guide](references/source-playbook.md) when choosing among relevant sources.
- Read [code archaeology](references/code-archaeology.md) when tracing commits, reviews, comments, or tests.
- Read [ticket history](references/linear.md) when product requirements or issue discussion may explain the change.
- Read [design documents](references/notion.md) when ADRs, specs, or meeting records may hold the rationale.
- Read [chat history](references/slack.md) when attributable deliberation may be missing from durable records.
- Read [runtime telemetry](references/datadog.md) when an infrastructure condition may have motivated the code.
- Read [error history](references/sentry.md) when a specific failure or defensive check needs context.
- Read [analytics evidence](references/databricks.md) when usage, experiments, data shape, or thresholds may matter.
- Read [incident context](references/incident-postmortem.md) when the target may be a response to an incident.

The service names label examples, not required providers. Use sufficient current connected tools and discover their supported read operations. Inspect capability metadata without dumping secret-bearing configs, environment values, or unrelated transcripts.

Keep searches scoped to target, relevant actors, and time. Record actual queries, locators, limits, empty results, unavailable sources, and useful unsearched leads. Unsearched or unavailable history cannot support a claim that no rationale exists.

If useful independent investigation is authorized, the coordinator reserves its starts and retries within the finite shared budget and the lower host/user limit. A leaf returns evidence and gaps; it does not launch another controller. Read [the investigator prompt](references/investigator-prompt.md) only for a scoped evidence pass and [the synthesis prompt](references/synthesizer-prompt.md) only when reconciling multiple findings. Inline work remains valid.

## State what the record supports

Separate these classes explicitly, using only as much structure as the answer needs:

- **Direct.** An attributable statement explains the target. Cite it.
- **Supported.** Independent indirect evidence converges. Cite the evidence and say the conclusion is derived.
- **Inferred.** A reasonable interpretation needs an explicit chain and uncertainty.
- **Speculative.** Competing explanations still fit; label each as a possibility.
- **Unknown.** The relevant answer is missing, inaccessible, or unsearched. Name the limit.

Show contradictions with both sources. Check the user's hypothesis as a candidate rather than confirming it by default. Several copies of one summary are one evidence chain.

Use the `how` skill, when installed, for a separate explanation of the present mechanism; read it before use. A research answer stays read-only unless requested notes or changes have separate authority. No posting, repair, or removal of a defense follows from discovering its history.

If a change is already planned, return constraints supported by that history: what to preserve, what may change, what to avoid, and the remaining risk. Do not turn uncertain lineage into a new permission or restriction.

Done when consequential intent claims have attributable sources or calibrated uncertainty, human rulings retain their actual scope, and the answer names its real coverage and unresolved questions.

## Provenance

Read [the per-file sources](references/SOURCES.md) when checking attribution, original hashes, destinations, and adaptation.
