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

## Remaining foundation acceptance evidence

The agreed design also calls for routing correctness with the existing inventory plus one role and several overlapping roles. This proof measures discovery and listing size only. Thirty distinct placeholders do not test shared-capability deduplication or model routing. Those acceptance checks remain open; record the role profiles, shared closure, fixed routing prompts, expected selections, observed selections, and host/model revisions before treating that part of the foundation as complete.

F1-08 remains an acceptance gate for PR #2. Keep the foundation in draft until both hosts have the required overlap and routing evidence, or the user explicitly changes that scope. Waiting for the next real role can schedule the evidence work, but does not close the gate. A disposable distribution with overlapping role profiles can establish install deduplication without adding another role to this PR; the existing downstream role already permits the single-role routing trial.

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

All nine [offline probe tests](../tests/discovery-cost.py), installer fixtures, and 17 eval-harness isolation tests passed without model calls. `./scripts/validate.sh` exited `0`, including the pinned skill validator, catalog/profile checks, skill fixtures, freshness checks, and zizmor. Vale was not installed, so the suite skipped prose lint; the separate prose command exited `2` with that setup diagnostic. Run `uv run --script tests/discovery-cost.py`, `tests/install/run.sh`, and `tests/eval-harness/run.sh` to repeat the focused checks.
