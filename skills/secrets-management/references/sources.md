# Sources

Read this when checking a delivery system's current support, maintenance, encryption, rotation, reload or scanner behavior. Sources are link-only; all skill text and code are original.

- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html): lifecycle, ownership, delivery, rotation and audit questions.
- [Kubernetes Secrets practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/) and [encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/): check actual platform encryption, RBAC, workload creation and reload behavior.
- [SOPS](https://github.com/getsops/sops) and [age](https://github.com/FiloSottile/age): check supported formats, recipients and recovery-key handling for the installed versions.
- [External Secrets](https://external-secrets.io/): check current maintainer health, supported provider/auth adapters and installed controller reconciliation behavior before adopting it.
- [OpenBao](https://openbao.org/docs/) and [Vault](https://developer.hashicorp.com/vault/docs): check deployment, lease/revoke/reload, audit and recovery features for the actual system and its license.
- [Gitleaks](https://github.com/gitleaks/gitleaks) and [TruffleHog](https://github.com/trufflesecurity/trufflehog): resolve releases, verification, redaction flags, canary rules and scanning scope live.

For a cloud secret store, use that provider's current official docs for identity, versioning, rotation overlap, failure modes and access readback. No fixed store versions, product health claims, rotation limits or license classifications are embedded here.
