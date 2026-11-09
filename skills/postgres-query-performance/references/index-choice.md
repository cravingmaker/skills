# Choosing an index

Read this when a plan shows a scan that does not match its predicate or ordering, or when someone asks whether to add an index.
An index can improve matching reads, adds storage and maintenance, and can increase write cost. Name the query it serves and the write cost you accept.

## B-tree column order

- Put columns compared with `=` first, then the one range or sort column. For `WHERE customer_id = $1 ORDER BY created_at DESC`, use `(customer_id, created_at DESC)`.
- Among equality columns, order matters less than many think; pick the order that also serves other frequent queries.
- Do not assume a multicolumn index is useless without its leading column. Newer majors can skip-scan a low-cardinality leading column; check the target major's docs before relying on it, and confirm with a plan.
- A sequential scan is not a bug. It is often the cheapest plan when a query reads a large fraction of the table.

## Other index shapes

| Shape | Use when | Watch for |
| --- | --- | --- |
| Partial (`WHERE status = 'open'`) | Queries target a small, stable subset. | The query's predicate must imply the index predicate, or the planner cannot use it. |
| Covering (`INCLUDE (total)`) | An index-only scan would avoid heap reads for a hot query. | Index-only scans need a mostly all-visible table, which depends on vacuum. |
| Expression (`lower(email)`) | Queries filter on the same expression. | The expression, operators and applicable collation must match a usable index expression. |
| GIN | `jsonb` containment, arrays, full-text search. | Slower writes; for `jsonb`, `jsonb_path_ops` is smaller but supports fewer operators. |
| BRIN | Very large tables whose rows are physically ordered by the column, such as append-only time series. | Poor correlation can make ranges too broad; test the actual plan and pages visited. |
| Unique | A rule must hold. | This is a constraint first; design it with the `postgres-schema-design` skill. |

## Foreign keys

PostgreSQL does not index the referencing columns of a foreign key automatically.
Index them when the application joins on them or deletes parent rows; otherwise each parent delete scans the child table.

## Before you add one

- Look for an existing index that a small change would make usable, such as adding a column or reordering.
- Check for duplicates: matching leading columns alone do not prove redundancy; also compare predicates, uniqueness, expressions, included columns and ordering.
- Estimate the write cost on the table's insert and update rate.
- For a live rollout, use the `postgres-migrations` skill when installed; concurrent builds still need lock, failure and resource planning.
