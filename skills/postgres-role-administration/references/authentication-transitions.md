# Authentication transitions

Read this when changing login authentication, TLS, credential rotation or revocation. Use the same access matrix, with `connection` probes and stable classified failure codes, plus fresh SQL probes after successful authentication.

## Inventory and recovery

Identify server/provider, native/websocket/HTTP driver, client versions, direct/pooled route, credentials, intended networks and address families, and a recovery administrator path inside existing policy. Verify supported authentication methods and TLS semantics in the installed-major [password authentication](https://www.postgresql.org/docs/current/auth-password.html), [HBA](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html) and [libpq SSL](https://www.postgresql.org/docs/current/libpq-ssl.html) documentation, plus the actual driver's documentation. On Neon use supported provider/driver controls; do not propose editing an inaccessible host HBA file.

## Native checks

For self-hosted HBA changes, inspect authorized `pg_hba_file_rules` parse errors and first-match order against every intended source network and address family. Check replacement-password verifier type through a privileged adapter that returns only classification/counts; do not select or log verifier values. Client compatibility, configured authentication method and stored verifier type are separate facts. Rehearse the transition on a disposable target before a direct authorized change.

## Fresh-client matrix

- The intended hostname, trust roots, network/family and replacement credential must permit a fresh connection with the intended login and current role.
- Wrong CA, wrong hostname/identity and plaintext must fail where encrypted verified transport is required; encryption without server-identity verification is insufficient.
- The retired credential must fail a fresh attempt after rotation/revocation. Use the secret store's old-version handle without exposing the value.
- Disallowed networks/families and unsupported client/auth combinations must fail for the expected reason; DNS, syntax or an unreachable test endpoint is not proof of enforcement.
- Direct and pooled routes and every actual driver need their own applicable transport tests; a browser/HTTP connection does not establish native libpq behavior.

Keep the recovery path usable while making the smallest ordered change, then remove temporary grants and test again. Already-open sessions may survive credential changes; inspect them and use only authorized session revocation where required. Report fresh and existing-session results separately. Capture only allowlisted peer/transport/identity summaries; never include full URLs, passwords, verifier hashes or raw error messages with secrets. Certificate issuance, firewall persistence, identity-provider design and secret storage are adjacent jobs rather than database grant rules.
