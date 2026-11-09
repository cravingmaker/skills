# Boundary parsing

Read this when choosing a decoder, configuration schema, unknown-key policy, or exact numeric representation.

Use the repository's schema library first. Verify its current API and any [Standard Schema](https://standardschema.dev/) adapter support before composing validators. Standard Schema describes an interface; it does not choose the validation policy.

Treat a static request annotation, `JSON.parse` cast, brand, or non-null assertion as no runtime proof. Decode `unknown` into a domain value at its trust boundary. Separate syntax, shape, domain invariants, and authorization so failures keep their meaning.

| Boundary | Policy to decide |
| --- | --- |
| Writable command | Reject unexpected writable fields when they could change protected state; allowlist the update separately |
| Forward-compatible response | Tolerate or preserve additions according to the consumer contract |
| Source archive | Preserve raw bytes or lossless values and unknown fields before deriving convenient types |
| Stored JSON or queued event | Decode by explicit schema version and retain an upgrade or rejection path |
| Configuration | Distinguish missing, empty, invalid, and defaulted values; fail before listening |

Coercion is a domain rule. Test strings such as `"false"`, zero, empty strings, whitespace, and malformed numbers against the chosen boolean and numeric parser. Decide absent versus null, decimal scale, timestamp zone, Unicode normalization, and maximum lengths. Ordinary JavaScript JSON numeric parsing can round a large integer before a schema sees it. For exact values, choose contractual strings/decimals or a source-preserving parser; casting a rounded number cannot recover the original value.

Configuration errors name the key and expected shape, never secret input. Run missing-key and invalid-value startup fixtures with synthetic values. Check raw application stderr as well as telemetry so redaction is not proved only by a suppressing wrapper.

Sources: [TypeScript compiler options](https://www.typescriptlang.org/tsconfig/), [Node TypeScript execution](https://nodejs.org/api/typescript.html), [Standard Schema](https://standardschema.dev/), and [JSON numeric interoperability](https://www.rfc-editor.org/rfc/rfc8259.html). Verify the selected library's behavior with executable cases rather than assuming every schema library coerces or strips unknown keys the same way.
