-- Comparison starter; creates only temporary tables in a disposable fixture.
-- Generation is supplied by the logical crosswalk, not inferred from a code.
CREATE TEMP TABLE model_entities (
  tenant_id text NOT NULL,
  entity_id text NOT NULL,
  CONSTRAINT model_entities_pk PRIMARY KEY (tenant_id, entity_id)
);
CREATE TEMP TABLE model_identifiers (
  tenant_id text NOT NULL,
  issuer text NOT NULL,
  code text NOT NULL,
  generation integer NOT NULL,
  entity_id text NOT NULL,
  valid_from date NOT NULL,
  valid_until date,
  CONSTRAINT model_identifiers_pk PRIMARY KEY (tenant_id, issuer, code, generation),
  CONSTRAINT model_identifiers_entity_fk FOREIGN KEY (tenant_id, entity_id)
    REFERENCES model_entities (tenant_id, entity_id) ON DELETE RESTRICT,
  CONSTRAINT model_identifiers_period CHECK (valid_until IS NULL OR valid_until > valid_from)
);
CREATE INDEX model_identifiers_entity_idx ON model_identifiers (tenant_id, entity_id);
CREATE TEMP TABLE model_trades (
  tenant_id text NOT NULL,
  trade_id text NOT NULL,
  issuer text NOT NULL,
  code text NOT NULL,
  generation integer NOT NULL,
  quantity numeric(20,4) NOT NULL,
  happened_at timestamptz NOT NULL,
  CONSTRAINT model_trades_pk PRIMARY KEY (tenant_id, trade_id),
  CONSTRAINT model_trades_identifier_fk FOREIGN KEY (tenant_id, issuer, code, generation)
    REFERENCES model_identifiers (tenant_id, issuer, code, generation) ON DELETE RESTRICT,
  CONSTRAINT model_trades_quantity CHECK (quantity >= 0)
);
CREATE INDEX model_trades_identifier_idx ON model_trades (tenant_id, issuer, code, generation);
