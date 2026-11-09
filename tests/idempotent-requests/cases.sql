-- Schema-asset fixtures only: no application handler or provider guarantee is tested.
CREATE FUNCTION expect(label text, got anyelement, want anyelement) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  IF got IS DISTINCT FROM want THEN RAISE EXCEPTION 'FAIL: % (got %, want %)', label, got, want; END IF;
END $$;
CREATE FUNCTION fixture_insert(t text, p text, o text, k text) RETURNS bigint LANGUAGE sql AS $$
  WITH admitted AS (
    INSERT INTO request_idempotency (tenant_id,principal_id,operation,idempotency_key,request_fingerprint,expires_at)
    VALUES (t,p,o,k,decode(repeat('00',32),'hex'),CURRENT_TIMESTAMP + interval '1 day')
    ON CONFLICT DO NOTHING RETURNING 1
  ) SELECT count(*) FROM admitted;
$$;
SELECT expect('first key', fixture_insert('t','u','create','k'), 1::bigint);
SELECT expect('duplicate full scope', fixture_insert('t','u','create','k'), 0::bigint);
SELECT expect('separate tenant', fixture_insert('other','u','create','k'), 1::bigint);
SELECT expect('separate principal', fixture_insert('t','other','create','k'), 1::bigint);
SELECT expect('separate operation', fixture_insert('t','u','other','k'), 1::bigint);
DO $$
BEGIN
  BEGIN
    UPDATE request_idempotency SET phase='completed',response_status=201 WHERE tenant_id='t' AND principal_id='u' AND operation='create';
    RAISE EXCEPTION 'FAIL: incomplete completed result accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
  BEGIN
    UPDATE request_idempotency SET phase='provider_pending' WHERE tenant_id='t' AND principal_id='u' AND operation='create';
    RAISE EXCEPTION 'FAIL: provider_pending without identity accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
  BEGIN
    UPDATE request_idempotency SET request_fingerprint='\x01' WHERE tenant_id='t';
    RAISE EXCEPTION 'FAIL: invalid fingerprint length accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
  BEGIN
    UPDATE request_idempotency SET expires_at=created_at WHERE tenant_id='t';
    RAISE EXCEPTION 'FAIL: invalid retention interval accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
END $$;
UPDATE request_idempotency SET phase='provider_pending',provider_key='synthetic-provider-key'
 WHERE tenant_id='t' AND principal_id='u' AND operation='create';
UPDATE request_idempotency SET phase='completed',response_status=201,response_headers='{}',response_body=convert_to('synthetic-result','UTF8')
 WHERE tenant_id='t' AND principal_id='u' AND operation='create';
SELECT expect('completed result admitted', (SELECT response_status::integer FROM request_idempotency WHERE tenant_id='t' AND principal_id='u' AND operation='create'), 201);
DO $$
BEGIN
  BEGIN
    UPDATE request_idempotency SET phase='admitted' WHERE tenant_id='t' AND principal_id='u' AND operation='create';
    RAISE EXCEPTION 'FAIL: nonfinal row with replay metadata accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
END $$;
