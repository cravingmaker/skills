> **Human documentation.** Agents should not read this page unless a person asks them to.

# Supported harnesses

Claude Code and Codex CLI have recorded installation, discovery, invocation, and paired-evaluation evidence. T3 Code is a front end for those providers; it is not a third independently evaluated model host in this repository.

## Contents

- [Read the support levels](#read-the-support-levels)
- [Recorded host versions](#recorded-host-versions)
- [What installation proves](#what-installation-proves)
- [What discovery and routing prove](#what-discovery-and-routing-prove)
- [What evaluation proves](#what-evaluation-proves)
- [Other hosts and future versions](#other-hosts-and-future-versions)
- [Recorded summaries by host](#recorded-summaries-by-host)
- [Platforms](#platforms)

## Read the support levels

"Supported" is scoped to the evidence, rather than a promise that every host implements the same tools or policy.

| Level | Meaning |
| --- | --- |
| Format | The package follows the Agent Skills specification |
| Installed | The owned installer produced and checked the required files/settings |
| Discovered | A host inventory or fresh session exposed the expected names |
| Invoked | A supported native event or body read establishes selection |
| Evaluated | Matched candidate/no-candidate sessions exist for the required examples |
| Surface verified | The actual named behavior was driven on the identified artifact |

Installation does not establish activation. Activation does not establish semantic correctness. A fixture-local pass does not establish deployment or production behavior.

## Recorded host versions

The recorded cutover and host campaigns use these versions; newer versions need fresh checks.

| Surface | Recorded version/model context | Evidence scope |
| --- | --- | --- |
| Claude Code | 2.1.311; Claude evaluation sweep used `claude-opus-5-5`, high effort | User installation, manual visibility, fresh-session discovery, paired examples |
| Codex CLI | 0.167.0; retained default-model runs report `gpt-6.1-sol` | User installation, generated invocation policy, discovery, paired examples |
| T3 Code | No separate front-end release version bound by the cited tests | Runs Claude or Codex and may expose dispatch, isolation, PR linking, and watch tools |
| Other Agent Skills hosts | No recorded version or behavioral campaign here | Spec-compatible packaging; installation adapters and behavior untested |

The [host campaign PR](https://github.com/cravingmaker/skills/pull/9), [cutover PR](https://github.com/cravingmaker/skills/pull/10), and [discovery proof](install-and-discovery-proof.md) provide the public anchors. The different effective models are part of the observation, not a controlled host-only comparison.

## What installation proves

The owned installer resolves the transitive required closure, detects conflicts, records ownership, and supports copy or symlink mode. The host generator checks Codex's manual policy files. Claude's explicit adapter checks the native schema and settings precedence before changing selected overrides.

Recorded copy and symlink discovery checks ran outside the source checkout on both real CLIs. The observed cutover installed the complete owned core to each host's user skill directory and verified repeat installation without change. The [installation guide](getting-started.md) gives the current commands.

## What discovery and routing prove

Early discovery measurements used a pinned smaller role profile, existing-skill snapshots, and synthetic added roles/descriptions. They show the tested inventories and rendered prompts, including Codex description shortening in a wider-cache case. They do not establish a live production model's exact listing budget.

The recorded routing experiment matched its fixed allowed first-selection sets in the tested scenarios. It tested initial selection under an explicit routing-only instruction, with different default models. It did not execute the full delegated workflows, establish universal routing accuracy, or reproduce every live plugin tool and managed source.

Fresh cutover sessions provide later evidence for the full core's installed names and manual visibility. Use the [generated profile](routing.md) for current dependencies rather than replaying an old profile count.

## What evaluation proves

The paired harness prepares private homes, configurations, caches, fixtures, and fresh sessions. It verifies matching noncandidate inventory and model within a pair. It keeps activation, result correctness, and unnecessary workflow cost separate.

Claude and Codex have different activation traces and sandbox behavior. The [harness-differences guide](harness-differences.md) explains both. The public summaries preserve invalid attempts and specific semantic or protocol caveats; invalid attempts supply no result credit.

There is no blanket promise of live browser/native tooling, hosted CI, real PR service gates, independent provider panels, or successful production merges. Read the [known limits](known-issues.md#what-remains-untested).

## Other hosts and future versions

An Agent Skills-compatible host may read the same spec-compliant `SKILL.md`. That alone does not implement Claude `skillOverrides`, Codex `agents/openai.yaml`, this installer's receipts, or a particular delegation API.

Before claiming equivalent support, verify the host's actual discovery roots, explicit command names, manual suppression, required closure, settings precedence, tools, sandbox, and activation evidence. Use a disposable environment and preserve version/source identities. A host upgrade can change those facts, so the recorded version is a useful boundary rather than a permanent claim.

## Recorded summaries by host

The generated table counts retained historical summaries at all revisions. Valid means an isolated completed comparison; it does not certify correctness or final-byte coverage.

<!-- BEGIN GENERATED eval-records: generated by scripts/build-docs.py; edit the catalog or SKILL.md files, then rerun it -->

| Host as recorded | Effective model | Valid | Invalid | Total |
| --- | --- | ---: | ---: | ---: |
| `2.1.311 (Claude Code)` | `claude-opus-5-5` | 593 | 108 | 701 |
| `2.1.311 (Claude Code)` | `default` | 0 | 2 | 2 |
| `codex-cli 0.167.0` | `default` | 0 | 3 | 3 |
| `codex-cli 0.167.0` | `gpt-6.1-sol` | 770 | 0 | 770 |
| All | | 1363 | 113 | 1476 |

<!-- END GENERATED eval-records -->

## Platforms

Recorded host sessions ran on macOS. Repository CI runs deterministic checks and fixtures on Ubuntu; it does not run either model host. Linux and Windows host discovery and invocation remain untested.
