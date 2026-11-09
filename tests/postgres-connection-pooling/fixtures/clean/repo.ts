export async function reserve(client, id) {
  await client.query("BEGIN");
  await client.query("SET LOCAL statement_timeout = 5000");
  await client.query("SELECT set_config('app.tenant', $1, true)", ["t1"]);
  await client.query("SELECT pg_advisory_xact_lock(42)");
  await client.query(`UPDATE stock
     SET qty = qty - 1
   WHERE id = $1`, [id]);
  await client.query("UPDATE stock SET qty = 0 WHERE id = $1", [id]);
  await client.query("INSERT INTO t VALUES (1) ON CONFLICT (id) DO UPDATE SET n = t.n + 1");
  await client.query("CREATE TEMP TABLE scratch (id int) ON COMMIT DROP");
  await client.query("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE");
  await client.query("SET search_path TO app"); // pooler-ok: this module runs on the direct URL
  await client.query("COMMIT");
}
// A comment about SET search_path = x is prose, not a statement.
