# Install and discovery proof

Copy and symlink installs made exactly the seven `agent-orchestrator` profile skills discoverable on both real hosts outside this checkout. The installer rejected an incomplete distribution with a named prerequisite error.

Measured on macOS on 2026-11-08 using the downstream `feat/role-agent-orchestrator` tree at `822565a127508fe88dd0909a7d9587a81d304c3e`, Codex CLI `0.167.0`, and Claude Code `2.1.311`. The foundation branch contains no role router or generated role profile; these measurements require that downstream source distribution.

## Method and isolation

The [discovery probe](../scripts/measure-skill-discovery.py) calls `install-skills.py` from a fresh temporary working directory into a private temporary `$HOME/.codex/skills` or `$HOME/.claude/skills`. It uses the eval harness's environment allowlist and host configuration, with private home, configuration, cache, and temporary directories. The original home, installed caches, settings, and credentials receive no writes. The probe does not read or copy authentication.

Codex discovery uses app-server `initialize`, `initialized`, then `skills/list` with `forceReload: true`. Claude discovery sends the SDK `initialize` control request without a user message; its response contains the installed commands and full descriptions. Built-in commands are counted separately, bundled skills are disabled, and Claude's remaining `plugin-authoring` skill is switched off in temporary settings. Claude's `get_context_usage` with `detail: summary` also reports local estimates, with `apiUsage: null`.

To measure the actual rendered listing, the probe directs the real CLI to a loopback-only request sink, using an authentication-free Codex provider or a dummy Claude API key. The sink captures the pending request; the probe stops the CLI before returning any response. This performs zero model inferences and uses no subscription quota. Temporary host homes and raw requests are deleted; exported JSON contains discovery metadata and the rendered listing.

## Install results

| Host | Install mode | Installed / discovered | Profile symlinks | Source `SKILL.md` bytes match |
| --- | --- | ---: | ---: | --- |
| Codex | Copy | 7 / 7 | 0 | Yes |
| Codex | Symlink | 7 / 7 | 7 | Yes |
| Claude Code | Copy | 7 / 7 | 0 | Yes |
| Claude Code | Symlink | 7 / 7 | 7 | Yes |

Each inventory was exactly `agent-briefing`, `agent-debate`, `agent-orchestrator`, `clear-communication`, `decision-log`, `result-verification`, and `work-decomposition`. Copy and symlink installs produced identical normalized listings within each host.

For each host, the missing-dependency proof removed `result-verification` from its temporary copy install, exposed that install as a disposable distribution's `skills/`, and supplied a temporary copy of `catalog/skills.yaml`. Installing the router from that distribution exited `1`, reported `result-verification is required but is neither in .../skills nor an external skill in the catalog`, and created no target folder. Reinstalling from the complete checkout with `--force` restored the dependency; both hosts rediscovered all seven skills. The installer resolves the supplied distribution; it does not audit an arbitrary existing target automatically. The router's prerequisite-and-stop rule was read, but no model execution of that rule is claimed.

## Discovery cost

Characters count the rendered skill rows, plus Codex's shared roots table and headings; fixed host instructions, JSON encoding, tools, and skill bodies are excluded. Temporary home prefixes are normalized to `$HOME`; raw measured sizes are also shown. The common token estimate is `ceil(normalized characters / 4)` and is not an exact tokenizer count.

The installed snapshot replays metadata and visibility policy from Codex's enabled local plugin registrations plus five system skills (42 existing skills), and Claude's registered plugin plus 16 synced skills (43 existing skills). Plugin declarations exclude unpublished folders and embedded test fixtures. Existing skill bodies, hooks, tools, connectors, and personal configuration are excluded from the replay. The synthetic case adds 30 distinct placeholders, each with a 288-character description; it estimates additional listing cost without claiming that several real role profiles exist.

| Host | Scenario | Discovered | Listed | Characters, normalized (raw) | Estimated tokens | Shortened descriptions | Omitted by visibility policy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex | Profile alone | 7 | 7 | 2,353 (2,434) | 589 | 0 | 0 |
| Codex | Profile + installed snapshot | 49 | 32 | 9,601 (9,682) | 2,401 | 0 | 17 |
| Codex | Snapshot + 30 placeholders | 79 | 62 | 19,861 (19,942) | 4,966 | 0 | 17 |
| Claude Code | Profile alone | 7 | 7 | 2,026 (2,026) | 507 | 0 | 0 |
| Claude Code | Profile + installed snapshot | 50 | 34 | 15,147 (15,147) | 3,787 | 0 | 16 |
| Claude Code | Snapshot + 30 placeholders | 80 | 64 | 24,357 (24,357) | 6,090 | 0 | 16 |

Neither discovery interface shortened descriptions in these scenarios; both returned every installed name. Claude normalized whitespace in the synced `learn` description from 982 to 979 characters; the text was not cut for budget. Claude's separate SDK estimates for these three scenarios were 673, 5,038, and 8,098 tokens; these local estimates use a different method from the common character-based estimate.

As a second reading of the synthetic request, profile + 30 placeholders alone measured 12,613 characters / about 3,154 tokens on Codex and 11,236 characters / about 2,809 tokens on Claude, with all 37 descriptions intact.

The wider Codex cache replay includes top-level cached packages' declared skills, the manifest-free Neon's seven immediate `skills/*/SKILL.md` files, and the system skills, including dormant packages; it is an upper bound rather than an assertion that all cached packages are enabled. It discovered 140 skills, listed 98 after visibility policy, shortened 75 descriptions, and used 21,786 normalized characters (21,867 raw), about 5,447 tokens. Adding 30 placeholders discovered 170, listed 128, shortened 121 descriptions, and used 21,812 characters (21,893 raw), about 5,453 tokens. All descriptions remained full in `skills/list`; the reductions appeared only in the captured prompt. The router's 317-character description fell to 178 characters in the wider-cache case and 118 with placeholders. Neither wider-cache run omitted an additional skill for budget.

## Budgets and limits

[Codex documents](https://learn.chatgpt.com/docs/build-skills) a default initial-list budget of 2% of the model context, an 8,000-character fallback when context size is unknown, shortening descriptions before omitting skills with a warning, and a configurable `skills.max_context_tokens` maximum of 10,000 tokens. The captures demonstrate shortening on the installed CLI. The loopback Codex provider uses an unknown model name and the CLI's fallback model metadata; this does not establish the budget of a production model or independently exercise the unknown-context 8,000-character branch.

[Claude documents](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) a default listing budget of 1% of model context, a 1,536-character per-description cap, and dropping descriptions while retaining names when the listing exceeds its budget. No tested Claude listing needed that reduction. The SDK summary reported a one-million-token context using its default model metadata; the independent request capture selected `haiku`.

The replay preserves source names, descriptions, manual-only flags, and Codex `agents/openai.yaml` policy, but installs metadata as standalone skills. Plugin namespaces and original plugin paths can add characters in a live plugin session. Server-managed plugin enablement, usage-based ranking, and routing correctness are outside this local listing proof. Cache contents and host versions can change, so reruns retain their own source hashes and counts.

## Routing correctness with existing skills

All 32 valid routing trials matched the selection sets fixed before execution: eight prompts, two profile scenarios, and both hosts. There were no unexpected first selections or diversions into the existing installed skills. This supplies the routing observations requested by F2-02 and fleet-design-v3 §F4 for the scenarios below; it does not establish a general routing error rate.

Measured on 2026-11-08 against the downstream `feat/role-agent-orchestrator` worktree at `10fa1016a0a87e8c1c501d1adde11a9bde6fd683`. Claude Code `2.1.311` reported effective model `claude-opus-5-5`; Codex CLI `0.167.0` reported `gpt-6.1-sol`. Both used the host default in a clean generated configuration. Claude's `system.init` and Codex's session rollout establish those model names; no more specific backend weight revision was exposed.

### Profiles and shared dependency closures

The single-role scenario installed `agent-orchestrator` alongside the user's existing installed skills. The overlap scenario installed it with three synthetic role routers from a disposable distribution outside every repository. The synthetic skills are test fixtures, not shipped roles.

| Profile | Complete required closure |
| --- | --- |
| `agent-orchestrator` | `agent-briefing`, `agent-debate`, `agent-orchestrator`, `clear-communication`, `decision-log`, `result-verification`, `work-decomposition` |
| `proof-quality-lead` | `agent-briefing`, `agent-debate`, `clear-communication`, `decision-log`, `proof-quality-lead`, `proof-quality-review`, `result-verification`, `work-decomposition` |
| `proof-release-lead` | `clear-communication`, `decision-log`, `proof-release-lead`, `proof-release-plan`, `work-decomposition` |
| `proof-design-chair` | `agent-briefing`, `agent-debate`, `clear-communication`, `decision-log`, `proof-design-chair`, `proof-design-options`, `work-decomposition` |

The four closures contain 27 entries in total and resolve to 13 distinct skill directories, avoiding 14 duplicate copies. Each shared capability appeared once in each installed profile inventory. In particular, `agent-debate` is shared by the orchestrator, quality lead, and design chair. The synthetic capabilities deliberately resemble `result-verification`, `work-decomposition`, and `agent-debate` in their descriptions, while their bodies distinguish human QA, human releases, and proposed design comparisons.

Every model session used the real `install-skills.py --root DISTRIBUTION --target PRIVATE_SKILLS --mode copy NAME...` from a fresh workspace outside the checkout. The installer received one role name or all four together; its output and installed bytes were checked against the declared union. Optional handoffs were not added to the profile closure.

The existing inventory was copied with full skill bodies, resources, and original visibility fields, including Codex `agents/openai.yaml`. Its source set matches the registered-plugin/system or synced snapshot used above: 42 existing Codex skill names and 43 Claude skill names. All 85 source `SKILL.md` hashes still matched after the experiment. Existing plugin execution, connectors, hooks, and personal settings were excluded; these were standalone copies of the installed skills.

| Host | Single-role inventory | Overlapping-role inventory |
| --- | ---: | ---: |
| Claude Code | 50 user skill names | 56 user skill names |
| Codex | 50 records, 49 distinct names | 56 records, 55 distinct names |

The extra Codex record is a byte-identical `starter-workflow` template nested inside the existing `create-plugin` assets as well as installed at top level; it is unrelated to profile dependencies. Claude additionally advertised the SDK-declared built-in `doctor` skill in every valid startup trace; it was never invoked. The discovery and startup inventories were checked for uncontrolled sources.

### Fixed prompts and expected selections

The prompt set and selection rubric were written at `2026-11-08T10:04:29Z`, before the first model start at `10:05:43Z`. The SHA-256 of the sorted JSON case set is `b27947959471894da745bbd6843176ed63fc75ddc59002767791aa71e4eb9718`. Each session received the same standing communication contract and a routing-only boundary: select and read relevant skills, give the next action, and stop before executing the larger task, writing artifacts, or dispatching workers.

The first confirmed activation must be in the stated set. `None` requires no skill activation; the absent-role controls also require reporting that role unavailable. Subsequent reads may load required prerequisites or justified task-relevant capabilities. The ambiguous prompts deliberately allow several acceptable entry points; they do not test a unique winning skill.

| ID | Exact prompt | Expected first selection, single role | Expected first selection, overlap |
| --- | --- | --- | --- |
| R1 | Act as agent-orchestrator. Plan a fleet of three AI agents to compare data-migration approaches, with one integration owner, disjoint write paths, at most two concurrent workers, and six total worker starts. Give the initial plan only; do not dispatch. | `agent-orchestrator` | `agent-orchestrator` |
| R2 | Coordinate a resumed multi-agent run. One worker report is saved, a second worker has no receipt, and two incompatible approaches remain. Describe reconciliation and the next step before starting more agents. | `agent-orchestrator` or `decision-log` | Same |
| R3 | Act as proof-quality-lead. Assess this human QA handoff: the criterion is that all five exports open; the handoff says exports pass but supplies screenshots for only two. Identify the acceptance gap and next check. If that role is unavailable, report it unavailable and stop. | None; role unavailable | `proof-quality-lead` |
| R4 | Act as proof-release-lead. Plan a human release with database, documentation, and support owners; database and documentation both change release-notes.md, and the release budget is not yet set. Identify ownership, order, and the first budget decision. If that role is unavailable, report it unavailable and stop. | None; role unavailable | `proof-release-lead` |
| R5 | Compare two proposed database migration approaches with an evidence rubric and a bounded disagreement process. Give the process only; no workers or live checks. | `agent-debate` | `agent-debate`, `proof-design-chair`, or `proof-design-options` |
| R6 | The plan has tasks, owners, shared files, and an unknown worker budget. Check whether splitting it is worthwhile and identify the first budget decision. Do not start anyone. | `work-decomposition` or `agent-orchestrator` | Same |
| R7 | What does the English word 'orchestrator' mean? Answer in one sentence. | None | None |
| R8 | Compute 19 + 23. Reply with only the number. | None | None |

### Observed selections and trace evidence

| Prompt | Claude, single | Codex, single | Claude, overlap | Codex, overlap |
| --- | --- | --- | --- | --- |
| R1 | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` |
| R2 | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` |
| R3 | None; unavailable | None; unavailable | `proof-quality-lead` | `proof-quality-lead` |
| R4 | None; unavailable | None; unavailable | `proof-release-lead` | `proof-release-lead` |
| R5 | `agent-debate` | `agent-debate` | `proof-design-options` | `proof-design-options` |
| R6 | `work-decomposition` | `work-decomposition` | `work-decomposition` | `work-decomposition` |
| R7 | None | None | None | None |
| R8 | None | None | None | None |

A successful Claude `Skill` call or direct `Read` of the installed body counts as activation. Codex needs a successful simple reader command containing the absolute `SKILL.md` path and visible body text, using the harness's rule. Skill names in answers, searches, failed commands, and inventory entries do not count. All 60 recorded activation events were checked against their raw trace lines. The only unclassified Codex command, single-role R4 at trace line 5, was `rg --files`; manual inspection confirmed that it listed paths without reading a skill body, so no activation was added.

The raw evidence stays outside this public repository, as raw eval evidence does: the frozen experiment, run ledger, integrity checks, each run's activation sequence, raw trace, and result record, the profiles, exact prompts, source hashes, configurations, effective inventories, models, sessions, usage, installer output, and the manual trace decision. Codex records also include the session rollout. None of the 32 valid fixtures changed, and all sessions were distinct.

### Misroutes, budget, and limits

No unexpected first selection occurred under the fixed rubric. Both hosts changed R5 from `agent-debate` to `proof-design-options` when the overlap profiles were present; that was an allowed selection. The synthetic description closely matches the prompt's evidence-rubric and bounded-disagreement wording, a likely explanation for the shift rather than a demonstrated causal result. This does not establish that a role router should always take precedence over a directly matching capability.

The absent-role controls exposed a separate output issue: Claude looked for native agent definitions and suggested a `.claude/agents` file for the missing role. It still loaded no skill and met the routing expectation, but that suggestion does not reproduce this repository's role-skill installation workflow. Codex sometimes reread a capability body, including `agent-debate` during resumption; those extra reads are retained in the report rather than counted as new skill selections.

There were 33 model starts, including one discarded Claude startup-validation trial, with a peak of two active runs and seven starts left under the 40-run cap. The first local parser incorrectly rejected the declared built-in `doctor` entry. That first trial's trace was not retained and supports no routing claim; R1 was repeated once. R2's retained trace was reclassified after the parser correction without another model call, with its initial parser record preserved. No prompt or expected selection changed. Four initial discovery preflights used zero model turns.

These are single trials per host, prompt, and profile scenario, with different host-default models. They test initial selection, not completed delegation, exhaustive prerequisite reading, final deliverable quality, or a causal effect of descriptions. The generic routing boundary explicitly asks models to read relevant instructions, so the observations are not an unprompted activation-rate estimate. Plugin namespaces, plugin tools, server-managed discovery, dormant cached packages, and production routing with live plugin configuration are not reproduced. There was no production-model listing-budget measurement in these trials. The existing discovery-cost captures above remain separate evidence.

Each run used a fresh private home, configuration, cache, temporary directory, and workspace with the eval harness's environment allowlist and generated host settings. Only authentication was copied into mode-0600 temporary files; it was never exported or printed. Exported evidence was checked for the known credential values. All private host homes were removed, and the retained evidence contains no authentication files. The user's installed folders received no writes.

## Reproduce and validate

Run the current foundation probe against a separate source distribution containing the role. With the measured downstream commit available locally, export it without changing either checkout, then run from the temporary directory:

```sh
repo=$(pwd -P)
proof_root=$(mktemp -d)
mkdir "$proof_root/source"
git -C "$repo" archive 822565a127508fe88dd0909a7d9587a81d304c3e | tar -x -C "$proof_root/source"
cd "$proof_root"
export UV_CACHE_DIR="$proof_root/uv-cache" PYTHONDONTWRITEBYTECODE=1
for host in codex claude; do
  for mode in copy symlink; do
    "$repo/scripts/measure-skill-discovery.py" --root "$proof_root/source" --host "$host" --mode "$mode" \
      --output "$proof_root/$host-$mode.json"
  done
done
"$repo/scripts/measure-skill-discovery.py" --root "$proof_root/source" --host codex --placeholders 30 \
  --output "$proof_root/codex-synthetic.json"
```

For the installed snapshot, add `--plugin-root /absolute/cache/package/version` for each selected registration and `--extra-skill /absolute/SKILL.md` for system or synced metadata. Add `--placeholders 30` to that same command for the combined synthetic case. The worker report retains the exact expanded commands and source names with description lengths. Each JSON record includes the host version, installer result, discovery rows, listing text and hash, policy flags, and per-description outcomes; snapshot records also include hashes of the existing source files.

All nine [offline probe tests](../tests/discovery-cost.py), installer fixtures, and 22 eval-harness isolation tests passed without model calls. `./scripts/validate.sh` exited `0`, including the pinned skill validator, catalog/profile checks, skill fixtures, freshness checks, and zizmor. Vale was not installed, so the suite skipped prose lint; the separate prose command exited `2` with that setup diagnostic. Run `uv run --script tests/discovery-cost.py`, `tests/install/run.sh`, and `tests/eval-harness/run.sh` to repeat the focused checks.

The routing experiment used a one-off local driver built on the existing harness adapters and the real installer; no new repository script was needed. The driver preserved the frozen prompts, refused to overwrite run records, checked the source snapshot before preparing, rejected unmanaged inventory changes, reserved each model start in a ledger before launch, and removed each host home on success or failure. It is not a supported public routing harness, so a replay needs a new driver and a new, explicitly allocated budget of 32 model sessions.
