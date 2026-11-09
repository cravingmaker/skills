-- Original comparison starter: separate fragments, not one runnable migration.
-- Validate syntax against the project's PostgreSQL version in a disposable DB.
-- No server/library version is pinned by this asset.
-- IDs and fingerprints come from the application; retain original message
-- identity and a canonical/source-preserving payload fingerprint across retries.
-- A relay scans pending state, not an ID high-water mark: ID allocation order
-- is not commit order, so a later-committing row could otherwise be skipped.

CREATE TABLE outbox_messages (
    tenant_id text NOT NULL,
    event_id uuid NOT NULL,
    aggregate_key text NOT NULL,
    aggregate_sequence bigint NOT NULL CHECK (aggregate_sequence >= 0),
    event_type text NOT NULL,
    schema_version integer NOT NULL CHECK (schema_version > 0),
    payload jsonb NOT NULL,
    payload_fingerprint text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    available_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    max_attempts integer NOT NULL CHECK (max_attempts > 0),
    lease_generation bigint NOT NULL DEFAULT 0 CHECK (lease_generation >= 0),
    lease_until timestamptz,
    state text NOT NULL DEFAULT 'pending'
        CHECK (state IN ('pending', 'leased', 'complete', 'dead')),
    failure_code text,
    PRIMARY KEY (tenant_id, event_id),
    CHECK ((state = 'leased') = (lease_until IS NOT NULL))
);

CREATE INDEX outbox_claimable ON outbox_messages (available_at, created_at)
    WHERE state IN ('pending', 'leased');

CREATE TABLE consumer_inbox (
    consumer_name text NOT NULL,
    tenant_id text NOT NULL,
    event_id uuid NOT NULL,
    payload_fingerprint text NOT NULL,
    completed_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    PRIMARY KEY (consumer_name, tenant_id, event_id)
);

-- Enqueue: use the SAME checked-out connection and transaction as the business
-- write. The caller supplies all identity/version fields. Commit both or neither.
-- INSERT INTO outbox_messages (...) VALUES (...);

-- Claim: $1 bounded batch size; $2 lease interval. Validate positive bounds in
-- application config. Commit the claim before network work. SKIP LOCKED does
-- not guarantee aggregate order; add a per-key sequence gate where required.
WITH claimable AS (
    SELECT tenant_id, event_id
    FROM outbox_messages
    WHERE available_at <= clock_timestamp()
      AND attempts < max_attempts
      AND (state = 'pending'
           OR (state = 'leased' AND lease_until <= clock_timestamp()))
    ORDER BY available_at, created_at, event_id
    LIMIT $1
    FOR UPDATE SKIP LOCKED
)
UPDATE outbox_messages AS message
SET state = 'leased',
    attempts = message.attempts + 1,
    lease_generation = message.lease_generation + 1,
    lease_until = clock_timestamp() + $2::interval
FROM claimable
WHERE message.tenant_id = claimable.tenant_id
  AND message.event_id = claimable.event_id
RETURNING message.*;

-- Complete: $1 tenant, $2 event ID, $3 claimed generation.
-- Exactly one returned row is success. Zero rows means ownership was lost.
-- A relay uses this only after destination acceptance; a local worker locks and
-- verifies this row in the SAME transaction as its local business effect.
-- If conditional completion returns no row, ROLLBACK that local transaction:
-- never commit the business effect after losing ownership.
-- This condition cannot fence a remote provider; use its key/reconciliation.
UPDATE outbox_messages
SET state = 'complete', lease_until = NULL
WHERE tenant_id = $1 AND event_id = $2 AND lease_generation = $3
  AND state = 'leased' AND lease_until > clock_timestamp()
RETURNING event_id;

-- Consumer admission: $1 consumer, $2 tenant, $3 ID, $4 fingerprint.
-- Run this and the local effect in ONE transaction. Execute the effect ONLY
-- when one row returns. On zero rows read/compare the existing fingerprint:
-- mismatch is quarantine, match is a duplicate. Acknowledge after commit.
INSERT INTO consumer_inbox (consumer_name, tenant_id, event_id, payload_fingerprint)
VALUES ($1, $2, $3, $4)
ON CONFLICT DO NOTHING
RETURNING event_id;

-- Final-attempt crash sweep: expired exhausted claims become retained dead
-- letters. Fence again so an old worker cannot change this terminal record.
-- For transient failures with attempts remaining, the owner conditionally sets
-- pending + bounded available_at and clears lease_until in its own statement.
UPDATE outbox_messages
SET state = 'dead', lease_until = NULL,
    lease_generation = lease_generation + 1,
    failure_code = 'attempts_exhausted'
WHERE attempts >= max_attempts
  AND (state = 'pending'
       OR (state = 'leased' AND lease_until <= clock_timestamp()))
RETURNING tenant_id, event_id;
