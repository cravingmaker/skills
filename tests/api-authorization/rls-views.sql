SELECT expect('actual login for view/function tests', session_user::text, 'app_api'::text);
BEGIN;
SELECT set_config('app.tenant_id', '00000000-0000-0000-0000-00000000000a', true);
SELECT expect('default owner view bypass', (SELECT count(*) FROM invoices_leaky), 3::bigint);
SELECT expect('invoker view uses caller policy', (SELECT count(*) FROM invoices_invoker), 2::bigint);
SELECT expect('definer function uses owner policy', invoice_count(), 3::bigint);
COMMIT;
