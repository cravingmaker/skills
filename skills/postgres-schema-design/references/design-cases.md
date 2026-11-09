# Design cases

Read this when translating logical identity, relationships or temporal rules into physical PostgreSQL constraints.

| Logical rule | Physical proof |
| --- | --- |
| Code X can be reused by an issuer. | Store the source issuer and generation/effective period separately from the stable entity key. Keep both historical mappings; reject duplicate source identity within a generation. |
| A relationship belongs to one tenant. | Reference `(tenant_id, entity_id)` through a matching composite candidate key; a foreign key on `entity_id` alone does not encode tenant equality. |
| An issuer's code has at most one identity at an effective instant. | Choose a supported non-overlap constraint or a proved transaction protocol; a unique start time does not prevent overlapping periods. Test touching endpoints, empty ranges, NULL and overlaps. |
| One fact can have many tags. | Keep the fact grain stable and aggregate before attaching multivalued attributes where the consumer needs one fact row. Compare exact totals with the logical counterexample. |
| Quantity is exact and nonnegative. | Declare scale and unit, test client decoding and rounding/rejection policy, and pair required values with `NOT NULL`. A floating-point round trip is insufficient. |
| A JSON document changes shape. | Give it an explicit version and reader transition rule. Test old documents and unknown versions rather than assuming stored JSON is current. |

The starter uses an explicit source generation supplied by the logical crosswalk. It proves reuse and tenant relationships, not non-overlap over arbitrary time ranges. When the source has no reliable generation, resolve or preserve the ambiguity before adopting that starter.

Use the installed major's official documentation for exclusion and temporal keys and verify required operator classes/extensions on the provider. Treat a length limit as a domain rule with evidence; `varchar(n)` is not a general performance improvement. A catalog flag for a money-like float column is only a clue until the field's unit and meaning are known.

Constraint fixtures need independent expected errors: catch `23505` for a duplicate, `23503` for an invalid relationship, `23502` for required NULL and `23514` for an invalid check value. The expected constraint name distinguishes the intended rejection from a setup failure. Run each negative case inside its own recoverable test transaction or savepoint so one expected error cannot abort all later checks.
