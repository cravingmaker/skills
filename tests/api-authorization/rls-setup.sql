-- Roles and data for the rls-policy.sql test. Runs as the bootstrap superuser of a disposable server.
CREATE ROLE owner_role NOLOGIN;
CREATE ROLE app_api LOGIN;
CREATE ROLE app_jobs LOGIN;
CREATE ROLE bi_reader LOGIN BYPASSRLS;
CREATE TABLE invoices (tenant_id uuid NOT NULL, id integer NOT NULL, amount integer NOT NULL, PRIMARY KEY (tenant_id, id));
ALTER TABLE invoices OWNER TO owner_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON invoices TO app_api, app_jobs;
GRANT SELECT ON invoices TO bi_reader;
INSERT INTO invoices VALUES
  ('00000000-0000-0000-0000-00000000000a', 1, 10),
  ('00000000-0000-0000-0000-00000000000a', 2, 20),
  ('00000000-0000-0000-0000-00000000000b', 3, 30);
CREATE FUNCTION expect(label text, got anyelement, want anyelement) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  IF got IS DISTINCT FROM want THEN
    RAISE EXCEPTION 'FAIL: % (got %, want %)', label, got, want;
  END IF;
END $$;
