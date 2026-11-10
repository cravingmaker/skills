# Sources

Read this when verifying plan fields, installed engine behavior, policy tools, pricing or licenses. These are link-only sources; all instructions and helpers are original work.

- [Terraform plan command](https://developer.hashicorp.com/terraform/cli/commands/plan): verify detailed exits, saved-plan behavior and available flags against the installed release.
- [Terraform JSON format](https://developer.hashicorp.com/terraform/internals/json-format): verify actions, replacement paths, unknowns, checks and completeness fields before relying on them.
- [Terraform sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data): verify persistence and provider support for secret-avoiding arguments.
- [OpenTofu documentation](https://opentofu.org/docs/): check the chosen engine's JSON, plan encryption, migration and feature support independently.
- [TFLint](https://github.com/terraform-linters/tflint), [Checkov](https://www.checkov.io/), [Conftest](https://www.conftest.dev/) and [Infracost](https://www.infracost.io/docs/): resolve supported releases and project configuration live; estimates also need the actual cloud provider's current price sheet.
- [Terraform source and license](https://github.com/hashicorp/terraform) and [OpenTofu source and license](https://github.com/opentofu/opentofu): inspect the selected release's legal terms when engine choice matters; this skill copies no vendor text or code.

Do not carry forward a dossier's release numbers, feature dates, field assumptions or cost figures. Use the repository's pinned engine/provider/tool choices and record any compatibility limits in the review receipt.
