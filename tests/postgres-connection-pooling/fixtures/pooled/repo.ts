export async function tenantQuery(client, tenant) {
  await client.query("SET search_path TO tenant_" + tenant);
  await client.query(`SET statement_timeout = 5000`);
  await client.query("SELECT set_config('app.tenant', $1, false)", [tenant]);
  await client.query("SELECT pg_advisory_lock(42)");
  await client.query("LISTEN jobs");
  await client.query("PREPARE get_user AS SELECT * FROM users WHERE id = $1");
  await client.query("CREATE TEMP TABLE scratch (id int)");
  await client.query("DECLARE c CURSOR WITH HOLD FOR SELECT 1");
  await client.query("RESET ALL");
  await client.query("SET ROLE reporting");
}
