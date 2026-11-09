-- A real app_api login, with isolated row-policy checks; all writes roll back.
SELECT expect('actual app login', session_user::text, 'app_api'::text);
SELECT expect('missing context', (SELECT count(*) FROM invoices), 0::bigint);
BEGIN;
SELECT set_config('app.tenant_id', '00000000-0000-0000-0000-00000000000a', true);
SELECT expect('tenant A allows its rows', (SELECT count(*) FROM invoices), 2::bigint);
UPDATE invoices SET amount = amount + 1 WHERE id = 1;
SELECT expect('own write permitted', (SELECT amount FROM invoices WHERE id=1), 11);
INSERT INTO invoices VALUES ('00000000-0000-0000-0000-00000000000a', 9, 1);
DELETE FROM invoices WHERE id=9;
DO $$
DECLARE changed bigint;
BEGIN
  UPDATE invoices SET amount = 0 WHERE id = 3;
  GET DIAGNOSTICS changed = ROW_COUNT;
  PERFORM expect('cross-tenant write denied', changed, 0::bigint);
  DELETE FROM invoices WHERE id = 3;
  GET DIAGNOSTICS changed = ROW_COUNT;
  PERFORM expect('cross-tenant delete denied', changed, 0::bigint);
  BEGIN
    INSERT INTO invoices VALUES ('00000000-0000-0000-0000-00000000000b', 9, 1);
    RAISE EXCEPTION 'FAIL: cross-tenant insert accepted';
  EXCEPTION WHEN insufficient_privilege THEN NULL;
  END;
  BEGIN
    UPDATE invoices SET tenant_id='00000000-0000-0000-0000-00000000000b' WHERE id=1;
    RAISE EXCEPTION 'FAIL: row moved into another tenant';
  EXCEPTION WHEN insufficient_privilege THEN NULL;
  END;
  BEGIN
    TRUNCATE invoices;
    RAISE EXCEPTION 'FAIL: runtime role has TRUNCATE privilege';
  EXCEPTION WHEN insufficient_privilege THEN NULL;
  END;
END $$;
ROLLBACK;
SELECT expect('empty context after transaction', (SELECT count(*) FROM invoices), 0::bigint);
BEGIN;
SELECT set_config('app.tenant_id', '00000000-0000-0000-0000-00000000000b', true);
SELECT expect('tenant B after A on same connection', (SELECT count(*) FROM invoices), 1::bigint);
COMMIT;
SELECT expect('context cleared after B', (SELECT count(*) FROM invoices), 0::bigint);
