# Redact a copy and retain its evidence

Read this before creating a shareable incident report, issue draft, or bundle. Work only on derived copies; preserve raw evidence and access controls. The intended audience and authorized export scope determine what may leave the original location.

## Remove sensitive values

| Category | Handling |
| --- | --- |
| Credentials and secrets | Replace keys, tokens, passwords, bearer strings, private keys, and secret URL parameters with stable SECRET placeholders |
| People and accounts | Remove unnecessary names, email addresses, handles, tenant/account/team IDs, and private author metadata |
| Hosts and repositories | Replace private hosts, addresses, internal links, private repository names and remotes unless their disclosure is authorized |
| Home paths | Remove the personal account segment while retaining a safe path mapping for the intended reader |
| Proprietary terms | Replace terms the user identifies as proprietary, consistently throughout the copy |
| Opaque payloads | Omit encrypted or opaque values that add no inspectable support; preserve safe event relationships |

Retain usable session/event identity, source markers, tool names, versions, and line numbers when safe. A private repository name does not make every command or result secret; preserve the safe mechanism and result structure needed to understand the finding. Use the same placeholder for the same value across all exported files and mark substitutions within quotations as redactions. Keep a log of placeholder categories, counts, and safe locations, without original values or a plaintext reversal map. Classifications that cannot be resolved safely remain an explicit export limitation.

## Review privacy and support separately

Inspect every exported file, including source excerpts, commands, results, author fields, URLs, metadata, and the redaction log. Automated matching can help find leaks but cannot certify the export is safe. Report unresolved categories without repeating the sensitive value. An independent privacy check is useful when authorized and budgeted; state whether it occurred.

Then verify each material finding using only the proposed export. Its citation must reach included evidence and that evidence must still prove the claim after redaction. If withholding removes support, narrow or withhold the claim and record the limitation. A clean privacy check does not prove evidence support, and resolvable line numbers alone do not prove a finding. Repeat the affected checks after any content change.
