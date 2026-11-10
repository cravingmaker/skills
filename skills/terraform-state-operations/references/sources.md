# Sources

Read this when verifying block syntax, backend locking, migration direction, encryption or recovery commands. Sources are link-only; no third-party text or code is retained.

- [Terraform state](https://developer.hashicorp.com/terraform/language/state): check state behavior, sensitive content and supported recovery commands.
- [Terraform refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring), [import](https://developer.hashicorp.com/terraform/language/import) and [remove resources](https://developer.hashicorp.com/terraform/language/resources/syntax): verify the installed release's declarative move/import/removal behavior before drafting blocks.
- [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3): check native lockfile support, older locking compatibility, permissions and migration requirements across every writer.
- [Terraform force-unlock](https://developer.hashicorp.com/terraform/cli/commands/force-unlock): check the exact command and locking behavior only after proving the old writer has stopped.
- [OpenTofu migration](https://opentofu.org/docs/intro/migration/) and [state encryption](https://opentofu.org/docs/language/state/encryption/): verify the exact source/destination release pair, key availability, backend and downgrade constraints.
- [Terraform JSON format](https://developer.hashicorp.com/terraform/internals/json-format) and [plan command](https://developer.hashicorp.com/terraform/cli/commands/plan): verify import/move/action fields and detailed exit behavior on the target engine.

Resolve engine/provider versions, lock support and licenses at use time. A vendor's current migration guide may not cover the installed versions or the opposite migration direction.
