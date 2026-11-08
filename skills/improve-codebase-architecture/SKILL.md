---
name: improve-codebase-architecture
description: Survey a codebase for deepening opportunities, present source-backed candidates as a static HTML report, then explore whichever one the user picks. Use when the user asks to improve a codebase's architecture or to find refactors that make it more testable and easier for agents to navigate.
license: MIT
metadata:
  verified: "2026-11"
  requires: "codebase-design"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture/SKILL.md"
  source-files: "skills/engineering/improve-codebase-architecture/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  local-changes: "Kept hotspot-first scoping, the friction questions, deletion test, candidate cards and the pick-then-explore loop; the report is now rendered by a script that escapes all content and is static and offline by default, with optional pinned Mermaid in strict mode and a stated network dependency; repository terms are kept; no product edits before the user picks; no mandatory sub-agent, local server or auto-open."
---

# Improve codebase architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and navigability for agents and people. The deliverable is a bounded, read-only report; no product code changes until the user picks a candidate and authorizes the work.

This skill is informed by the project's domain model and built on a shared design vocabulary:

- Read the `codebase-design` skill (required) for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", adapter counts as a heuristic). Use these terms in your reasoning; in the report, keep the repository's own names for its parts and map them to these terms where it helps.
- The project's domain glossary and decision records (at its configured paths, often `GLOSSARY.md` and `docs/adr/`) name good seams and record decisions this survey should not re-litigate.

## Process

### 1. Explore

**Scope before you scan.** Deepening a module pays off by making future changes to it easier, so weight the parts of the codebase that change often. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline --name-only`) to find the hot spots, the files and areas that keep coming up, and let those pull your attention first. If changes are scattered with no clear hot spot, widen the net.

Read the domain glossary and any decision records in the area first. Then walk the code and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, while the real bugs hide in how they're called (no **locality**)?
- Where do tightly coupled modules leak across their seams?
- Which parts are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? "Concentrates" is the signal you want. A separate exploration agent is optional, for a large codebase, and is charged to any shared run budget.

**Done when** each candidate has evidence a reader can check: file paths with line ranges, the commits or change counts behind the hot spot, and the friction observed. Claims stay as narrow as that evidence; a survey of one subsystem says nothing about the rest.

### 2. Present candidates as an HTML report

Write the candidates as JSON in the shape [references/report-format.md](references/report-format.md) describes, then render and check them:

```sh
python3 <skill-dir>/scripts/render-report.py candidates.json --check
python3 <skill-dir>/scripts/render-report.py candidates.json --output "<tmpdir>/architecture-review-<timestamp>.html"
```

Python 3.12 or later is required; no packages are needed. Exit 0 rendered, 1 findings in the JSON (`--check` lists them as JSON), 2 usage or unreadable input. Resolve `<tmpdir>` from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), so nothing lands in the repo and each run gets a fresh file. The renderer escapes every value and produces a static page with no scripts or network requests. Add `--mermaid-cdn` only when the user accepts that diagrams load a pinned Mermaid build from a CDN; the page then says so. Tell the user the absolute path; open it only if they ask and the host can.

Each candidate card shows:

- **Files**: which files and modules are involved, with line ranges
- **Problem**: why the current architecture causes friction
- **Solution**: plain-English description of what would change
- **Wins**: in terms of locality and leverage, and how tests would improve
- **Before / after diagram**: the shallowness and the deepening, side by side
- **Evidence**: the commits, counts and lines behind the claim
- **Recommendation strength**: `Strong`, `Worth exploring` or `Speculative`

End with a **top recommendation**: which candidate you'd tackle first and why.

**Decision-record conflicts**: if a candidate contradicts an existing decision record, surface it only when the friction is real enough to warrant revisiting that decision, and mark it in the card (for example, "contradicts ADR-0007, but worth reopening because…"). Don't list every theoretical refactor a decision forbids.

Do not propose interfaces yet. After the report is written, ask the user: "Which of these would you like to explore?"

### 3. Explore the chosen candidate

Once the user picks a candidate, walk the decision with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, which tests survive. The `grilling` skill structures that interview; the `architect` skill produces interface alternatives and the design artifact.

Keep the domain model current as decisions crystallize, within the authority to edit docs (the `domain-modeling` skill):

- **Naming a deepened module after a concept not in the glossary?** Add the term, creating the glossary lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update the glossary right there.
- **User rejects the candidate with a load-bearing reason?** Offer a decision record, framed as: "Want me to record this so future architecture reviews don't re-suggest it?" Offer only when a future explorer would need the reason; skip ephemeral and self-evident ones.

Done when the user has the report, every candidate's evidence is checkable, and any chosen candidate has moved into design with its decisions recorded where the project keeps them.

## Provenance

Adapted from Matt Pocock's improve-codebase-architecture skill and its HTML-REPORT reference. See [references/SOURCES.md](references/SOURCES.md) and `LICENSE-mattpocock`. The repository test `tests/improve-codebase-architecture/run.sh` renders hostile content and checks escaping, offline output and the Mermaid settings.
