CREATE SCHEMA good;
CREATE TABLE good.account (tenant_id bigint NOT NULL, id bigint NOT NULL,
  PRIMARY KEY (tenant_id, id), UNIQUE (id, tenant_id));
CREATE TABLE good.payment (tenant_id bigint NOT NULL, id bigint NOT NULL, account_id bigint NOT NULL,
  PRIMARY KEY (tenant_id, id), FOREIGN KEY (tenant_id, account_id) REFERENCES good.account (tenant_id, id));
-- Equality on all FK columns can use the reversed leading key order.
CREATE INDEX ON good.payment (account_id, tenant_id);
CREATE TABLE good.measurement (id bigint PRIMARY KEY, reading double precision NOT NULL);
CREATE SCHEMA bad;
CREATE TABLE bad.payment (tenant_id bigint NOT NULL, id bigint PRIMARY KEY, account_id bigint NOT NULL,
  balance double precision NOT NULL, opened_at timestamp NOT NULL,
  FOREIGN KEY (account_id, tenant_id) REFERENCES good.account (id, tenant_id));
CREATE TABLE bad.wrong_pair (tenant_id bigint NOT NULL, account_id bigint NOT NULL, id bigint PRIMARY KEY,
  FOREIGN KEY (tenant_id, account_id) REFERENCES good.account (id, tenant_id));
CREATE INDEX ON bad.wrong_pair (tenant_id, account_id);
CREATE TABLE bad.included (tenant_id bigint NOT NULL, account_id bigint NOT NULL, id bigint PRIMARY KEY,
  FOREIGN KEY (tenant_id, account_id) REFERENCES good.account (tenant_id, id));
CREATE INDEX ON bad.included (tenant_id) INCLUDE (account_id);
CREATE TABLE bad.invalid_fk (id bigint PRIMARY KEY, tenant_id bigint NOT NULL, account_id bigint NOT NULL,
  FOREIGN KEY (tenant_id, account_id) REFERENCES good.account (tenant_id, id));
INSERT INTO good.account VALUES (1, 1);
INSERT INTO bad.invalid_fk VALUES (1, 1, 1), (2, 1, 1);
CREATE TABLE bad.log_line (body text NOT NULL);
CREATE TABLE bad.ready_fk (id bigint PRIMARY KEY, tenant_id bigint NOT NULL, account_id bigint NOT NULL,
  FOREIGN KEY (tenant_id, account_id) REFERENCES good.account (tenant_id, id));
INSERT INTO bad.ready_fk VALUES (1, 1, 1);
