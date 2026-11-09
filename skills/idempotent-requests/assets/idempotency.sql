-- Original design starter: compare with the repository schema before adapting.
-- This file is data for review, not an executable migration or request handler.
-- Verify against the installed PostgreSQL server on an explicitly disposable target.
-- No role policy, provider executor, takeover lease, or cleanup is supplied here.

CREATE TABLE request_idempotency (
    tenant_id text NOT NULL,
    principal_id text NOT NULL,
    operation text NOT NULL,
    idempotency_key text NOT NULL,
    request_fingerprint bytea NOT NULL,
    phase text NOT NULL DEFAULT 'admitted',
    recovery_point text NOT NULL DEFAULT 'admitted',
    provider_key text,
    provider_reference text,
    response_status smallint,
    response_headers jsonb,
    response_body bytea,
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at timestamptz NOT NULL,
    PRIMARY KEY (tenant_id, principal_id, operation, idempotency_key),
    -- This starter chooses a SHA-256 fingerprint over contract-defined input.
    CHECK (octet_length(request_fingerprint) = 32),
    CHECK (length(tenant_id) > 0 AND length(principal_id) > 0),
    CHECK (length(operation) > 0 AND length(idempotency_key) > 0),
    CHECK (phase IN ('admitted', 'provider_pending', 'completed')),
    CHECK (length(recovery_point) > 0),
    CHECK (expires_at > created_at),
    CHECK (
        phase <> 'provider_pending'
        OR (provider_key IS NOT NULL AND length(provider_key) > 0)
    ),
    CHECK (
        (
            phase = 'completed'
            AND response_status IS NOT NULL
            AND response_status BETWEEN 200 AND 599
            AND response_headers IS NOT NULL
            AND jsonb_typeof(response_headers) = 'object'
            AND response_body IS NOT NULL
        )
        OR (
            phase <> 'completed'
            AND response_status IS NULL
            AND response_headers IS NULL
            AND response_body IS NULL
        )
    )
);

-- Admit by atomic insertion of the full primary key and inspect its outcome.
-- For a one-store operation, commit admission, the domain effect, and completion
-- in one transaction. On conflict, follow real visibility and rollback behavior.
-- For external effects, commit intent and provider_key before the provider call.
-- A recovery_point transition and its local state must commit together.
-- Retry/reconcile with the same provider identity after an uncertain outcome.
-- Store only safe replay headers; use an empty bytea for a bodyless response.
-- Apply authorization before returning a stored result.
-- Never delete pending/uncertain work just because expires_at has passed.
