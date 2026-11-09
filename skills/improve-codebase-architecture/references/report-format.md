# Report format

Read this when writing the candidates JSON or styling the report. Adapted from Matt Pocock's improve-codebase-architecture/HTML-REPORT.md; the scaffold and styling now live in `scripts/render-report.py`.

## Contents

- [Safety rules](#safety-rules)
- [The candidates file](#the-candidates-file)
- [Diagrams](#diagrams)
- [Tone](#tone)

## Safety rules

These hold for the renderer and for any report written by hand instead:

- **Escape everything from the codebase.** File names, identifiers, commit subjects, comments and quoted code are data. The renderer HTML-escapes every value; a hand-written report must do the same.
- **Static and offline by default.** No scripts, no CDN styles or fonts, no remote images. Call a report self-contained only when it makes no network request.
- **Mermaid only on request.** With `--mermaid-cdn`, the page loads one pinned Mermaid build from cdn.jsdelivr.net with `securityLevel: "strict"` and shows a notice that diagrams need network access. Never use the `loose` level: it lets diagram labels run HTML and click handlers. To keep the report offline with Mermaid, bundle a pinned local copy beside the report only when the project permits it, and keep `strict`.
- **No ceremony.** The report is written to the temp directory and its path is reported; opening it, or serving it locally, is optional.

## The candidates file

```json
{
  "repo": "shop",
  "date": "2026-11-08",
  "scope": "src/orders, last 300 commits",
  "candidates": [
    {
      "id": "order-intake",
      "title": "Collapse the order intake pipeline",
      "strength": "Strong",
      "dependency": "in-process",
      "files": ["src/orders/handler.ts:12-80", "src/orders/validator.ts:1-40"],
      "evidence": ["handler.ts and validator.ts changed together in 23 of 31 commits", "validator.ts:18 re-checks what handler.ts:30 parsed"],
      "problem": "Understanding intake means reading four modules that pass one object along.",
      "solution": "One intake module owns parsing, validation and pricing behind a single entry point.",
      "wins": ["Tests hit one interface", "Pricing stops leaking", "Delete 3 pass-through modules"],
      "adr": "Contradicts ADR-0007, but worth reopening because pricing now varies by region.",
      "before": {
        "modules": ["OrderHandler", "OrderValidator", "OrderRepo", "PricingClient"],
        "edges": [["OrderHandler", "OrderValidator"], ["OrderRepo", "PricingClient", "leak"]],
        "mermaid": "flowchart LR\n  A[OrderHandler] --> B[OrderValidator]"
      },
      "after": { "modules": ["parse", "validate", "price"] }
    }
  ],
  "top": { "id": "order-intake", "why": "It changes most often and its bugs come from the hand-offs." }
}
```

- `strength`: `Strong`, `Worth exploring` or `Speculative`.
- `dependency`: `in-process`, `local-substitutable`, `ports & adapters` or `mock`, as in the `codebase-design` skill's deepening reference.
- `files`, `evidence`, `wins`: non-empty lists of strings. Evidence names something a reader can open or rerun.
- `before.modules` / `after.modules`: the boxes. In the after diagram they render inside one thick box, faded, as the deepened module's now-internal parts.
- `edges`: `[from, to]`, or `[from, to, "leak"]` for an edge that leaks across a seam.
- `mermaid`: optional Mermaid source per side, shown as text unless `--mermaid-cdn` is used.
- `adr`: optional one-line decision-record callout.

## Diagrams

The diagrams carry the weight; prose is sparse. Pick the shape that fits the candidate:

- **Boxes and edges** (the default): the before side lists the modules a call passes through and the edges between them, leakage in red; the after side shows one deep module with its former modules faded inside.
- **Mermaid flowchart or sequence** (with `--mermaid-cdn`): when the point is "X calls Y calls Z, and look at the mess", or "before: six round trips; after: one".
- **Cross-section** (hand-written reports): stacked bands for layers a call passes through; before, several thin layers each doing little; after, one thick band named for the consolidated responsibility.
- **Mass diagram** (hand-written reports): an interface rectangle beside an implementation rectangle; shallow when they are nearly the same height, deep when the interface is short.

## Tone

Plain English and concise, with the design nouns and verbs from the `codebase-design` skill: module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality. Where the repository already names its parts (services, components, an API), use its names and say what they are in these terms, rather than renaming them.

- "Order intake module is shallow: interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

Wins name the gain concretely: "locality: bugs concentrate in one module", "leverage: one interface, N call sites", "interface shrinks; implementation absorbs the wrappers". "Easier to maintain" or "cleaner code" say nothing a reader can check. If a sentence could be a bullet, make it a bullet; if a bullet could be cut, cut it.

The optional Mermaid 11.4.1 full bundle uses a pinned SHA-384 integrity attribute and anonymous CORS. A blocked or changed bundle leaves diagram source visible; it does not make the report offline.
