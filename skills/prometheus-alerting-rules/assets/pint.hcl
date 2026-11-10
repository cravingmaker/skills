# Starter pint configuration for comparison with a repository's own .pint.hcl.
# Written against pint v0.89.4 (checked 2026-11-10); check rule and option names
# against the installed version's documentation before relying on them.

rule {
  match {
    kind = "alerting"
  }

  annotation "runbook_url" {
    comment  = "Every alert links the runbook that starts from it."
    severity = "bug"
    value    = "https://.+"
    required = true
  }

  label "owner" {
    comment  = "Every alert names its routing owner."
    severity = "bug"
    value    = ".+"
    required = true
  }

  label "severity" {
    comment  = "Alertmanager routes on severity: page interrupts a person, ticket waits for working hours."
    severity = "bug"
    values   = ["page", "ticket"]
    required = true
  }
}
