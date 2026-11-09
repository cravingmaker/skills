-- Read-only metadata leads; use scripts/audit-schema.py --schema app.
-- The explicit schema and tenant_column are psql-quoted values, never SQL fragments.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '10s';
SET LOCAL lock_timeout = '1s';
WITH tables AS (
  SELECT t.oid, t.relname, t.relnamespace, n.nspname
  FROM pg_class AS t JOIN pg_namespace AS n ON n.oid = t.relnamespace
  WHERE n.nspname = :'schema' AND t.relkind IN ('r', 'p')
), foreign_keys AS (
  SELECT c.*, t.nspname, t.relname
  FROM pg_constraint AS c JOIN tables AS t ON t.oid = c.conrelid
  WHERE c.contype = 'f'
), findings(check_name, object_name, reason) AS (
  SELECT 'table-without-primary-key', format('%I.%I', t.nspname, t.relname),
         'review the declared stable row identity'
  FROM tables AS t WHERE NOT EXISTS (
    SELECT 1 FROM pg_constraint AS p WHERE p.conrelid = t.oid AND p.contype = 'p')
  UNION ALL
  SELECT 'fk-without-index', format('%I.%I.%I', c.nspname, c.relname, c.conname),
         'review missing full valid ready leading B-tree key coverage against joins and parent changes'
  FROM foreign_keys AS c WHERE NOT EXISTS (
    SELECT 1 FROM pg_index AS i
    JOIN pg_class AS idx ON idx.oid = i.indexrelid JOIN pg_am AS am ON am.oid = idx.relam
    WHERE i.indrelid = c.conrelid AND i.indisvalid AND i.indisready AND i.indislive
      AND i.indpred IS NULL AND am.amname = 'btree'
      AND i.indnkeyatts >= cardinality(c.conkey)
      AND (i.indkey::smallint[])[0:cardinality(c.conkey)-1] @> c.conkey)
  UNION ALL
  SELECT 'tenant-missing-from-fk', format('%I.%I.%I', c.nspname, c.relname, c.conname),
         'review tenant equality: child and parent tenant columns must occupy a matching FK position'
  FROM foreign_keys AS c
  JOIN pg_attribute AS child ON child.attrelid = c.conrelid
    AND child.attname = :'tenant_column' AND NOT child.attisdropped
  JOIN pg_attribute AS parent ON parent.attrelid = c.confrelid
    AND parent.attname = :'tenant_column' AND NOT parent.attisdropped
  WHERE NOT EXISTS (SELECT 1 FROM generate_subscripts(c.conkey, 1) AS s(pos)
    WHERE c.conkey[s.pos] = child.attnum AND c.confkey[s.pos] = parent.attnum)
  UNION ALL
  SELECT 'column-review', format('%I.%I.%I', t.nspname, t.relname, a.attname),
         CASE
           WHEN a.atttypid = 'timestamp'::regtype THEN 'check instant versus documented local schedule'
           WHEN a.atttypid IN ('float4'::regtype, 'float8'::regtype, 'money'::regtype)
             AND a.attname ~* '(amount|price|balance|cost|total)' THEN 'check exact quantity, scale and currency'
           WHEN a.atttypid = 'varchar'::regtype THEN 'check whether length is a domain rule'
           WHEN ty.typtype = 'e' THEN 'check enum evolution policy'
           ELSE 'document the meaning of absence'
         END
  FROM tables AS t JOIN pg_attribute AS a ON a.attrelid = t.oid
  JOIN pg_type AS ty ON ty.oid = a.atttypid
  WHERE a.attnum > 0 AND NOT a.attisdropped
    AND ((NOT a.attnotnull AND col_description(t.oid, a.attnum) IS NULL)
         OR ty.typtype = 'e' OR a.atttypid IN ('timestamp'::regtype, 'varchar'::regtype)
         OR (a.atttypid IN ('float4'::regtype, 'float8'::regtype, 'money'::regtype)
             AND a.attname ~* '(amount|price|balance|cost|total)'))
)
SELECT json_build_object('objects_scanned', (SELECT count(*) FROM tables),
  'findings', COALESCE((SELECT json_agg(json_build_object(
    'check', check_name, 'object', object_name, 'reason', reason)
    ORDER BY check_name, object_name) FROM findings), '[]'::json));
COMMIT;
