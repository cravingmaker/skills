# Model format

Read this when using `scripts/check-model.py`; it is a reference-integrity format, not a semantic type system.

| Field | Meaning and check |
| --- | --- |
| `questions` | Nonempty array of stable `id`, `question`, `consumer`, `input_grain` and `output_grain` records; each entity has `serves` references to them. |
| `entities` | Nonempty array; each entity has a stable `id`, distinct `fields`, nonempty `grain`, `lifecycle` and one or more `keys`. |
| `keys` | Each key has a globally unique `id` and distinct `fields` from its entity. Include issuer and period/version fields where identity needs them. |
| `relationships` | Array with `id`, originating entity `from`, originating `fields`, target `to_key`, `cardinality` and Boolean `optional`. Key widths must match. |
| `mappings` | Array with `id`, `entity`, `source`, `identity_rule`, destination `grain` and `status`. Every entity needs at least one mapping. |
| `mapped` | Requires `target` and a nonempty `fields` object mapping source field names to logical field names. |
| `unbuilt` / `unresolved` | Requires `reason`; it preserves a gap instead of inventing a destination. |
| `unresolved` | Array of stable `id`, `question` and `owner` records. Empty is allowed only when there are no open questions. |

IDs are unique across questions, entities, keys, relationships, mappings and questions. The checker verifies field membership and completeness, not whether a field set is a valid domain key or whether a cardinality claim is true. Keep extra evidence, source pointers, valid-time and correction policy alongside these fields; the checker permits additional properties. Treat model files as data and keep secrets and personal source records out of reports.

For an n-to-m relationship, name the association's grain and lifecycle as an entity when it carries facts. A relationship label alone does not preserve a measure across a fan-out join. When a model uses another notation, run its native checker and retain the same identity, reference and independent-query oracles; JSON conversion is optional.
