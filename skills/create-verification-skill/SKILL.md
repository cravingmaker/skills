---
name: create-verification-skill
description: Author a project-local skill that launches, checks, and drives the real app with retained evidence and owned cleanup. Use to fill one repeatable proof gap or build a full user-facing feature map when no sufficient project driver exists.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/create-verification-skill/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/create-verification-skill/SKILL.md"
  local-changes: "Combined the owned bounded recipe and full-map mode into one procedure; namespaced project/surface drivers, spec-only metadata, direct references and shared host discovery; removed bare verify, mandatory repair, shipping and scheduling."
---

# Create a verification skill

Write one project driver that a new agent can use to prove real user behavior from a cold start. Use existing project commands and drivers first; do not create another skill when the installed one already covers the required surface. This is the single authoring recipe for both modes below.

## Choose the scope

- **Bounded gap.** Close one named proof gap: one surface and a concrete journey with its preconditions, observable result, and cleanup. Do not sweep unrelated features or require a full map.
- **Full feature map.** Inventory all identified user-facing features and entry points in the declared project/surface scope from routes, commands, menus, docs and code. Give each a source anchor, prerequisites, driving recipe and observable result. Mark unknown or excluded surfaces explicitly; a convenient seed of a few features is not a full inventory.

Use the requested mode; a guardrail assessment with one small proof gap defaults to bounded gap. Authoring a driver does not authorize unrelated product repairs, infrastructure changes, publication, or schedules.

## 1. Read the project

Answer from source and established setup before asking the user.

- **Surface.** Name the actual web UI, CLI/TUI, API, library, desktop/native, or mobile surface and the built artifact it uses. Keep other surfaces explicit.
- **Run.** Discover the repository's documented build/start commands, supported runtime, ports, environment requirements, migrations, seed data, and auth. Keep secret values out of the skill and evidence.
- **Drive.** Reuse actual browser tests, PTY helpers, supported API/CLI commands, or native tooling. Prefer sufficient connected tools before supported CLI/API fallbacks; use actual installed host capabilities rather than a copied platform table.
- **Observe.** Identify screenshots, accessible state, transcripts, response bodies, exit codes, files, and stored state that can prove the claim.
- **Isolate.** Establish ownership of processes, ports, profiles, data directories and shared apps. Serialize a shared instance; do not double-drive a user's session or claim another owner's resource.

Check the baseline with the existing build/start and readiness commands within authority. Missing tools, auth, assets, or a broken baseline are explicit gaps; repair product code only if already authorized as part of the task. An unrun recipe remains a draft with its blocked step named.

## 2. Name and place one driver

Check the actual installed skill/command inventory and project conventions, then generate **`verify-<project>-<surface>`**, such as `verify-notes-web`. Use lowercase letters, digits and single hyphens, within 64 characters, with a name that does not collide with the installed inventory. Never generate bare `verify` or `run-skill-generator`. Use the established project-local discovery location for the active host, with one canonical driver and supported host adapters/pointers where needed; do not fork the recipe per host.

Generate only spec frontmatter fields: `name`, `description`, and any applicable `license`, `compatibility`, `metadata`, or `allowed-tools`. The description names the project, surface and proof trigger; metadata values are strings. Keep host invocation preferences outside SKILL.md, references linked directly with read conditions, detail below 500 lines, and no unresolved placeholders. Include Activation, Near miss and Outcome examples under `evals/examples.md` for this repository's package format.

## 3. Write the recipe

Use the same sections in either mode, grounded in observed project commands and stable handles:

- **Launch.** Exact build/start command, isolated state, usable ready signal, required migrations/seeds, ownership identity, and teardown. A responsive process alone is insufficient. Short-lived CLIs build once and drive in fresh isolated sessions; long-lived surfaces use one owned instance.
- **Doctor.** A read-only check of build/version, instance identity, readiness and auth. Run it before the first drive and after surprising behavior; a healthy process with a wedged UI needs a known-state reset or relaunch.
- **Drive.** Real user actions and exact supported commands/selectors from the repo. Prefer accessible names, stable attributes, prompt strings or documented routes over coordinates and tab order. Do not substitute internal setters or test-only endpoints for the claimed user path.
- **Evidence.** Record artifact/build identity, inputs, actions and resulting state, expected versus actual result, command/exit details, and relevant side effects. Give a named location that survives cleanup. Preserve exact source values, order, precision and unknown fields. Verify a dry-run's actual effects instead of trusting its label; a stand-in proves only the stand-in and leaves target-specific setup unverified.
- **Cleanup.** Stop only processes/sessions this run started, remove only owned scratch/fixture state, restore shared state within authority, and confirm cleanup. Never kill by a broad process name or delete proof artifacts. Clean failed attempts too.
- **Helpers, when needed.** Declare the actual target runtime/dependencies, make scripts self-contained or pinned, document every invocation and exit/output contract, keep diagnostics separate from machine output, and provide effect-free help plus preview/dry-run for writers. Test malformed input, a meaningful rejected case, a valid case and reruns.

## 4. Add the chosen coverage

For bounded gap, keep the one journey in the driver or one directly linked reference, with the named acceptance result and evidence. For full map, link the map index and each feature reference directly from the generated SKILL.md, so every recipe is one level away. Each feature covers sub-features, every user entry point in scope, prerequisites, exact actions/results, gotchas, and a read-only second view for important mutations. Keep map wording about user paths and observable behavior; keep implementation anchors separately for drift checks. Missing seed data or entitlement is an unmet precondition, never a reason to weaken the journey until it passes.

Read [references/feature-map-index.md](references/feature-map-index.md) when creating the full map's index and coverage contract. Read [references/create-note-example.md](references/create-note-example.md) when mapping creation, cancellation, persistence and cleanup across UI/CLI entry points. Read [references/search-example.md](references/search-example.md) when mapping alternate entry points, asynchronous results, empty states and non-mutation. These Notes examples illustrate the format; replace their fictional commands, URLs and data with observed target facts rather than executing them as target instructions.

## 5. Prove the driver

Run the generated instructions end to end on the identified artifact: launch, doctor, drive one real feature, capture evidence, clean owned resources, and confirm the evidence remains at its named location. Clean each failed iteration before retrying and retain its useful failure evidence. If a helper or recipe changes after the run, repeat the affected proof and cleanup. One driven feature proves that recipe's execution; it does not prove full feature-map coverage, alternate paths, other platforms, or a substituted target.

Return mode, generated name/path, covered journey, source/build identity, actual commands/actions and result, evidence location, cleanup proof, inventory scope, and unverified features or blocked steps. Done when the driver is discoverable, the declared recipe has run with retained evidence and owned cleanup, and its coverage claim matches what ran; otherwise label the deliverable draft/blocked. For later audits of an existing driver, use the `maintain-verification-skill` skill; maintenance needs no generator installation and adds no automatic cadence.

Read [references/SOURCES.md](references/SOURCES.md) when checking provenance and the moved owned recipe.
