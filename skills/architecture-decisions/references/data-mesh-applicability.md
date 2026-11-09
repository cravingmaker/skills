# Data mesh applicability

Read this only when a data architecture choice is also a choice about organizational ownership.

Establish whether separate domain teams can own a data product's meaning, access, support, and lifecycle. Check their actual ability to provide stable interfaces and recovery evidence. Shared tooling without delegated accountability does not establish domain ownership. For a single team, compare a simpler shared platform before introducing product governance across domains.

Compare options on named consumers, semantic ownership, platform support cost, interoperability, privacy authority, and incident recovery. Name which team can change a field, approve access, restore a product, and resolve a cross-domain disagreement. Test one representative producer-to-consumer journey and its recovery path. Keep missing capabilities visible rather than prescribing a reorganization to justify the chosen technology.

Return an applicability argument and the evidence that would change it. Use the established ADR authoring method only if the durable choice needs a record. This branch adds no mesh implementation workflow or separate router.

Concepts are paraphrased from [Zhamak Dehghani's data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html); no source text or canvas is copied.
