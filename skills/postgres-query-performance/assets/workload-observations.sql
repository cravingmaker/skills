-- Original read-only observation starter, for comparison with the repository.
-- Inspect deployed PostgreSQL/pg_stat_statements columns and schema first.
-- Supply pgss_schema explicitly as a psql identifier variable. This file does
-- not install/reset extensions or change indexes. Use approved private output.
-- LIMIT 20 bounds this sample; it is neither coverage nor an index decision.
BEGIN READ ONLY;
SET LOCAL search_path = pg_catalog;

SELECT current_setting('server_version_num') AS server_version_num,
       pg_postmaster_start_time() AS server_started_at,
       clock_timestamp() AS observed_at;

SELECT datid, stats_reset
FROM pg_stat_database
WHERE datname = current_database();

-- Run only when the deployed extension exposes this reset-epoch view.
SELECT stats_reset, dealloc
FROM :"pgss_schema".pg_stat_statements_info;

-- Query IDs only: deliberately omit query text, relation names and literals.
-- Scope every comparison to the same database/user visibility and reset epoch.
SELECT queryid, calls, total_exec_time, mean_exec_time, rows,
       shared_blks_hit, shared_blks_read, temp_blks_read, temp_blks_written
FROM :"pgss_schema".pg_stat_statements
WHERE dbid = (SELECT oid FROM pg_database WHERE datname = current_database())
ORDER BY total_exec_time DESC
LIMIT 20;

-- Low sampled usage is a review lead, never permission to DROP or REINDEX.
SELECT relid, indexrelid, idx_scan, idx_tup_read, idx_tup_fetch,
       pg_relation_size(indexrelid) AS index_bytes,
       EXISTS (SELECT 1 FROM pg_constraint WHERE conindid = indexrelid) AS constraint_dependency
FROM pg_stat_user_indexes
ORDER BY idx_scan, pg_relation_size(indexrelid) DESC
LIMIT 20;

ROLLBACK;
