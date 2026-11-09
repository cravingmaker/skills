-- Known privileged exceptions in this disposable fixture only.
SELECT expect('bootstrap superuser bypasses FORCE', (SELECT count(*) FROM invoices), 3::bigint);
SET ROLE owner_role;
SELECT expect('owner with FORCE and no applicable policy', (SELECT count(*) FROM invoices), 0::bigint);
RESET ROLE;
ALTER TABLE invoices NO FORCE ROW LEVEL SECURITY;
SET ROLE owner_role;
SELECT expect('owner without FORCE', (SELECT count(*) FROM invoices), 3::bigint);
RESET ROLE;
CREATE VIEW invoices_leaky AS SELECT * FROM invoices;
ALTER VIEW invoices_leaky OWNER TO owner_role;
CREATE VIEW invoices_invoker WITH (security_invoker = true) AS SELECT * FROM invoices;
ALTER VIEW invoices_invoker OWNER TO owner_role;
GRANT SELECT ON invoices_leaky, invoices_invoker TO app_api;
CREATE FUNCTION invoice_count() RETURNS bigint LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog,public AS 'SELECT count(*) FROM public.invoices';
ALTER FUNCTION invoice_count() OWNER TO owner_role;
