-- Read-only, scoped metadata. psql -X -v role=app_reader -v schema=app -f privilege-audit.sql
-- Membership edges are candidates, not a version-independent effective ACL engine.
BEGIN READ ONLY;
SET LOCAL statement_timeout = '10s';
SET LOCAL lock_timeout = '1s';

SELECT r.rolname, r.rolcanlogin, r.rolsuper, r.rolbypassrls,
       r.rolcreaterole, r.rolcreatedb, r.rolinherit, r.rolconnlimit
FROM pg_roles AS r WHERE r.rolname = :'role';

-- Native reachability keeps inheritance and switching distinct. SET is available
-- with membership options; earlier majors use MEMBER for switch reachability.
SELECT 'reach' AS evidence_kind, r.rolname,
       pg_has_role(:'role', r.oid, 'USAGE') AS inherits_privileges,
       CASE WHEN current_setting('server_version_num')::integer >= 160000
            THEN pg_has_role(:'role', r.oid, 'SET')
            ELSE pg_has_role(:'role', r.oid, 'MEMBER') END AS can_switch
FROM pg_roles AS r
WHERE pg_has_role(:'role', r.oid, 'MEMBER') ORDER BY r.rolname;

SELECT d.datname AS database_name, owner.rolname AS owner,
       has_database_privilege(:'role', d.oid, 'CONNECT') AS can_connect,
       has_database_privilege(:'role', d.oid, 'CREATE') AS can_create,
       has_database_privilege(:'role', d.oid, 'TEMP') AS can_create_temp,
       COALESCE(d.datacl, acldefault('d', d.datdba)) AS database_acl
FROM pg_database AS d JOIN pg_roles AS owner ON owner.oid = d.datdba
WHERE d.datname = current_database();

SELECT n.nspname AS schema_name, owner.rolname AS owner,
       has_schema_privilege(:'role', n.oid, 'USAGE') AS can_use,
       has_schema_privilege(:'role', n.oid, 'CREATE') AS can_create,
       COALESCE(n.nspacl, acldefault('n', n.nspowner)) AS schema_acl
FROM pg_namespace AS n JOIN pg_roles AS owner ON owner.oid = n.nspowner
WHERE n.nspname = :'schema';

WITH RECURSIVE candidates(oid) AS (
  SELECT oid FROM pg_roles WHERE rolname = :'role'
  UNION
  SELECT m.roleid FROM pg_auth_members AS m JOIN candidates AS c ON c.oid = m.member
)
SELECT parent.rolname AS granted_role, child.rolname AS member_role, m.admin_option,
       to_jsonb(m)->>'inherit_option' AS inherit_option,
       to_jsonb(m)->>'set_option' AS set_option
FROM pg_auth_members AS m
JOIN candidates AS c ON c.oid = m.member
JOIN pg_roles AS parent ON parent.oid = m.roleid
JOIN pg_roles AS child ON child.oid = m.member;

SELECT 'object' AS evidence_kind, n.nspname AS schema_name, t.relname AS object_name, owner.rolname AS owner,
       t.relkind, t.relrowsecurity, t.relforcerowsecurity,
       COALESCE(t.relacl, acldefault('r', t.relowner)) AS object_acl,
       has_table_privilege(:'role', t.oid, 'SELECT') AS can_select,
       has_table_privilege(:'role', t.oid, 'INSERT') AS can_insert,
       has_table_privilege(:'role', t.oid, 'UPDATE') AS can_update,
       has_table_privilege(:'role', t.oid, 'DELETE') AS can_delete,
       has_table_privilege(:'role', t.oid, 'TRUNCATE') AS can_truncate
FROM pg_class AS t JOIN pg_namespace AS n ON n.oid = t.relnamespace
JOIN pg_roles AS owner ON owner.oid = t.relowner
WHERE n.nspname = :'schema' AND t.relkind IN ('r', 'p', 'v', 'm', 'f');

SELECT n.nspname AS schema_name, owner.rolname AS creator, d.defaclobjtype, d.defaclacl
FROM pg_default_acl AS d LEFT JOIN pg_namespace AS n ON n.oid = d.defaclnamespace
JOIN pg_roles AS owner ON owner.oid = d.defaclrole
WHERE d.defaclnamespace = 0 OR n.nspname = :'schema';

SELECT n.nspname AS schema_name, p.proname AS function_name,
       pg_get_function_identity_arguments(p.oid) AS argument_identity,
       owner.rolname AS owner, p.prosecdef AS security_definer,
       COALESCE(p.proacl, acldefault('f', p.proowner)) AS function_acl,
       has_function_privilege(:'role', p.oid, 'EXECUTE') AS can_execute
FROM pg_proc AS p JOIN pg_namespace AS n ON n.oid = p.pronamespace
JOIN pg_roles AS owner ON owner.oid = p.proowner WHERE n.nspname = :'schema';

SELECT n.nspname AS schema_name, t.relname AS sequence_name,
       COALESCE(t.relacl, acldefault('s', t.relowner)) AS sequence_acl,
       has_sequence_privilege(:'role', t.oid, 'USAGE') AS can_use,
       has_sequence_privilege(:'role', t.oid, 'UPDATE') AS can_mutate
FROM pg_class AS t JOIN pg_namespace AS n ON n.oid = t.relnamespace
WHERE n.nspname = :'schema' AND t.relkind = 'S';
COMMIT;
