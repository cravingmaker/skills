-- Read-only logical examples. SQLite is the offline fixture adapter.
-- Use native equivalents with the actual model; never install this as a schema.
WITH
identifiers(issuer, code, first_day, last_day, entity) AS (
  VALUES ('A', 'X', 1, 10, 'alpha'), ('A', 'X', 10, 20, 'beta'),
         ('B', 'X', 1, 20, 'gamma')
),
trades(id, issuer, code, day, quantity) AS (
  VALUES ('t1', 'A', 'X', 3, 5), ('t2', 'A', 'X', 12, 7),
         ('t3', 'A', 'UNKNOWN', 12, 7)
),
links AS (
  SELECT t.id, t.quantity, i.entity
  FROM trades AS t LEFT JOIN identifiers AS i
    ON t.issuer = i.issuer AND t.code = i.code
   AND t.day >= i.first_day AND t.day < i.last_day
),
candidates(record_id, entity, accepted) AS (
  VALUES ('Q', 'alpha', 0), ('Q', 'beta', 0)
),
claims(id, recorded_day, quantity) AS (
  VALUES ('c1', 1, 10), ('c1', 5, 12)
),
lines(order_id, line_id, quantity) AS (
  VALUES ('o1', 'l1', 5), ('o1', 'l2', 7)
),
tags(order_id, tag) AS (VALUES ('o1', 'red'), ('o1', 'blue')),
totals AS (SELECT order_id, SUM(quantity) AS quantity FROM lines GROUP BY order_id)
SELECT 'reuse_early' AS test_case, entity AS observed FROM links WHERE id = 't1'
UNION ALL SELECT 'reuse_late', entity FROM links WHERE id = 't2'
UNION ALL SELECT 'ambiguous_candidates', CAST(COUNT(*) AS TEXT)
  FROM candidates WHERE record_id = 'Q'
UNION ALL SELECT 'ambiguous_accepted', CAST(COUNT(*) AS TEXT)
  FROM candidates WHERE record_id = 'Q' AND accepted = 1
UNION ALL SELECT 'missing_quantity', CAST(SUM(quantity) AS TEXT)
  FROM links WHERE entity IS NULL
UNION ALL SELECT 'correction_before', CAST(quantity AS TEXT) FROM claims
  WHERE id = 'c1' AND recorded_day = (SELECT MAX(recorded_day) FROM claims WHERE id = 'c1' AND recorded_day <= 2)
UNION ALL SELECT 'correction_after', CAST(quantity AS TEXT) FROM claims
  WHERE id = 'c1' AND recorded_day = (SELECT MAX(recorded_day) FROM claims WHERE id = 'c1' AND recorded_day <= 6)
UNION ALL SELECT 'fanout_total', CAST(quantity AS TEXT) FROM totals
  WHERE EXISTS (SELECT 1 FROM tags WHERE tags.order_id = totals.order_id);
