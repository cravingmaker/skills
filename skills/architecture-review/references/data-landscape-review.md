# Data landscape review

Read this when the reviewed system owns, transforms, or distributes important data.

Pick one real source-to-consumer journey. For each hop, record source evidence, identity, logical meaning, physical storage, authoritative writer, transform version, access rule, ordering, precision, freshness, and recovery point. Follow the physical column or event field to the consumer's interpretation. Keep unresolved physical-to-semantic mappings explicit. Use the `logical-data-modeling` skill when resolving an actual domain relationship is a separate requested task.

Check every writer, including workers, admin tools, imports, and repair jobs. Look for shared writes across ownership boundaries and for enforcement below route-specific checks. Find the code, privilege, constraint, or dependency rule that enforces each claimed control. A glossary, contract registry, or ownership spreadsheet is evidence of intent. It cannot establish actual write isolation or data quality on its own.

Trace a durable acknowledgement through backup, restore, replay, and reconciliation. Check whether required source bytes or values survive each transform. Compare nulls, unknown fields, signs, units, time zones, order, and numeric precision where source fidelity matters. Show how a consumer detects a duplicate, missing revision, partial backfill, or stale projection.

For each gap, name the failing scenario, evidence, owner, and smallest discriminating probe. Keep privacy and governance policy decisions with the accountable owner. Do not widen this architecture review into a generic data audit.
