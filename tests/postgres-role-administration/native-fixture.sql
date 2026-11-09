-- Only the suite's owned disposable cluster runs these statements.
CREATE ROLE fixture_owner NOLOGIN;
CREATE ROLE fixture_migrator LOGIN NOINHERIT;
GRANT fixture_owner TO fixture_migrator;
CREATE ROLE fixture_runtime LOGIN;
CREATE ROLE fixture_reader LOGIN;
CREATE ROLE fixture_read_group NOLOGIN;
GRANT fixture_read_group TO fixture_reader;
CREATE SCHEMA fixture_app AUTHORIZATION fixture_owner;
GRANT USAGE ON SCHEMA fixture_app TO fixture_runtime, fixture_read_group;
SET ROLE fixture_owner;
ALTER DEFAULT PRIVILEGES IN SCHEMA fixture_app GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO fixture_runtime;
ALTER DEFAULT PRIVILEGES IN SCHEMA fixture_app GRANT SELECT ON TABLES TO fixture_read_group;
ALTER DEFAULT PRIVILEGES IN SCHEMA fixture_app GRANT USAGE, SELECT ON SEQUENCES TO fixture_runtime;
ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA fixture_app GRANT EXECUTE ON FUNCTIONS TO fixture_runtime;
CREATE TABLE fixture_app.orders (id bigint PRIMARY KEY, tenant_id integer NOT NULL, quantity numeric NOT NULL);
INSERT INTO fixture_app.orders VALUES (1, 1, 10), (2, 2, 20);
ALTER TABLE fixture_app.orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant ON fixture_app.orders USING (tenant_id = current_setting('fixture.tenant', true)::integer);
CREATE SEQUENCE fixture_app.issued;
CREATE FUNCTION fixture_app.bump() RETURNS integer LANGUAGE plpgsql SECURITY DEFINER
  SET search_path = pg_catalog, fixture_app, pg_temp AS $$
BEGIN UPDATE fixture_app.orders SET quantity = quantity + 1 WHERE id = 1; RETURN 1; END $$;
RESET ROLE;
