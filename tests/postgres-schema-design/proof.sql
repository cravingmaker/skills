INSERT INTO model_entities VALUES ('A', 'alpha'), ('A', 'beta'), ('B', 'other');
INSERT INTO model_identifiers VALUES
  ('A', 'issuer', 'X', 1, 'alpha', '2000-01-01', '2000-02-01'),
  ('A', 'issuer', 'X', 2, 'beta', '2000-02-01', NULL);
INSERT INTO model_trades VALUES
  ('A', 't1', 'issuer', 'X', 1, 0.1000, '2000-01-03T00:00:00Z'),
  ('A', 't2', 'issuer', 'X', 2, 12.0000, '2000-02-03T00:00:00Z');
DO $$
DECLARE observed_constraint text; rejected boolean; entities text[]; exact_quantity text;
BEGIN
  SELECT array_agg(i.entity_id ORDER BY t.trade_id) INTO entities
  FROM model_trades AS t JOIN model_identifiers AS i
    USING (tenant_id, issuer, code, generation);
  IF entities IS DISTINCT FROM ARRAY['alpha', 'beta'] THEN RAISE EXCEPTION 'identity mapping changed'; END IF;
  SELECT quantity::text INTO exact_quantity FROM model_trades WHERE trade_id = 't1';
  IF exact_quantity IS DISTINCT FROM '0.1000' THEN RAISE EXCEPTION 'quantity precision changed'; END IF;

  rejected := false;
  BEGIN
    INSERT INTO model_identifiers VALUES ('A', 'issuer', 'X', 1, 'beta', '2000-03-01', NULL);
  EXCEPTION WHEN unique_violation THEN
    GET STACKED DIAGNOSTICS observed_constraint = CONSTRAINT_NAME;
    rejected := observed_constraint = 'model_identifiers_pk';
  END;
  IF NOT rejected THEN RAISE EXCEPTION 'duplicate identity was not rejected by its key'; END IF;

  rejected := false;
  BEGIN
    INSERT INTO model_trades VALUES ('B', 't3', 'issuer', 'X', 1, 1, now());
  EXCEPTION WHEN foreign_key_violation THEN
    GET STACKED DIAGNOSTICS observed_constraint = CONSTRAINT_NAME;
    rejected := observed_constraint = 'model_trades_identifier_fk';
  END;
  IF NOT rejected THEN RAISE EXCEPTION 'cross-tenant link was not rejected by its FK'; END IF;

  rejected := false;
  BEGIN
    INSERT INTO model_trades VALUES ('A', 't4', 'issuer', 'X', 1, -1, now());
  EXCEPTION WHEN check_violation THEN
    GET STACKED DIAGNOSTICS observed_constraint = CONSTRAINT_NAME;
    rejected := observed_constraint = 'model_trades_quantity';
  END;
  IF NOT rejected THEN RAISE EXCEPTION 'negative quantity was not rejected by its check'; END IF;

  rejected := false;
  BEGIN
    INSERT INTO model_trades VALUES ('A', 't5', 'issuer', 'X', 1, NULL, now());
  EXCEPTION WHEN not_null_violation THEN rejected := true;
  END;
  IF NOT rejected THEN RAISE EXCEPTION 'required quantity accepted NULL'; END IF;
END $$;
