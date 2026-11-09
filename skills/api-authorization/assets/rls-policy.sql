-- Tenant row-level security starter (PostgreSQL), from the api-authorization skill.
-- Compare with the repository's schema and roles; adapt names and types, never apply blindly.
-- Assumes: invoices.tenant_id uuid; app_api and app_jobs own nothing, are not superusers and lack BYPASSRLS;
-- each transaction runs SELECT set_config('app.tenant_id', <tenant from the authenticated principal>, true).

ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
-- Without FORCE, the table owner skips every policy.
ALTER TABLE invoices FORCE ROW LEVEL SECURITY;

-- nullif turns an empty setting into NULL; a comparison with NULL matches no row, so a missing tenant denies.
CREATE POLICY invoices_tenant ON invoices
  FOR ALL
  TO app_api, app_jobs
  USING (tenant_id = nullif(current_setting('app.tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = nullif(current_setting('app.tenant_id', true), '')::uuid);
