# Upgrade report template

```markdown
## Toolchain upgrade: <packages>

| Package | From | To | Release notes |
| --- | --- | --- | --- |
| eslint-plugin-example | 4.2.0 | 5.0.1 | <link> |

Policy: <exact pins, minimum release age, commit rules>, met.

### Effective changes and decisions

| Change | Kind | Decision | Reason |
| --- | --- | --- | --- |
| `example/new-rule` | added by the recommended preset | off, explicitly | The policy enables new rules only after review |
| `example/old-rule` | removed | replaced by `example/new-name` | Same check, renamed upstream |
| `example/some-rule` option `max` | default changed 3 → 5 | set to 3 explicitly | Keeps current behavior |

### Compatibility

Runtime: <requirement> (project supports <range>). Peers: <checks>. Overrides: <reviewed or changed>.

### Verification

- `<full check command>`: passed.
- <focused test or consumer smoke test>: passed.

### Not verified

<anything without release notes, or any behavior no check covers>
```
