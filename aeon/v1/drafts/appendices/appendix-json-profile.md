---
id: appendix-json-profile-v1
title: Appendix - AEON JSON Profile
description: Informative appendix describing the AEON-to-JSON interoperability profile and transformation expectations.
family: appendices-v1
group: Profiles and Extensions
path: specification/appendices/appendix-json-profile-v1
---

# AEON JSON Profile — Appendix

**Profile Identifier:** `"json"`

---

## Purpose

The JSON Profile defines AEON → JSON transformation for interoperability with REST APIs, databases, and JSON tooling.

---

## Declaration

```aeon
aeon:header = {
  profile = "json"
}
```

---

## Transformation Rules

### Objects → JSON Objects

```aeon
person = { name = "Patrik" }
```
→
```json
{ "person": { "name": "Patrik" } }
```

### Lists → JSON Arrays

Direct mapping. Order preserved.

### Booleans → JSON Booleans

`true`/`false` pass through.

### Switch → JSON Boolean

| AEON        | JSON    |
| ----------- | ------- |
| `yes`, `on` | `true`  |
| `no`, `off` | `false` |

### Numbers → JSON Numbers

- If within safe range (±2^53): number
- If exceeds range: string (unless schema forbids)

### Strings → JSON Strings

- Use double quotes
- Normalize escapes

### References → Resolved Values
Reference handling is profile/consumer policy:
- if references are resolved upstream, JSON output contains materialized values
- if unresolved references are passed through, JSON output may retain reference tokens and emit diagnostics

Resolved example:

```aeon
a = [1]
b = ~a      // clone-intent
c = ~>a     // alias-intent
```

→

```json
{ "a": [1], "b": [1], "c": [1] }
```

> Note: JSON cannot preserve clone/pointer identity semantics. Interoperability output may lose aliasing information.

### Attributes → `@` Projection

```aeon
title@{lang="en"} = "Hello"
```
→
```json
{
  "title": "Hello",
  "@": { "title": { "lang": "en" } }
}
```

Nested object attributes stay local to the object that owns the attributed bindings:

```aeon
a@{b = 1} = {
  c@{d = 3} = 2
}
```
→
```json
{
  "a": {
    "c": 2,
    "@": {
      "c": { "d": 3 }
    }
  },
  "@": {
    "a": { "b": 1 }
  }
}
```

Notes:
- `@` is reserved in finalized/materialized JSON projection for attributes;
- exact collisions on `@` are profile errors;
- keys like `@a` remain ordinary user keys.

### Projected Materialization

Consumers may request projected materialization instead of whole-document materialization.

Projected materialization rules:
- the source AEON/AES may contain additional bindings;
- only the requested canonical paths are materialized into the JSON output;
- ancestors needed to reach the requested paths are preserved;
- this is a materialization policy, not a schema failure by itself.

Illustrative policy:

```ts
{
  materialization: 'projected',
  includePaths: ['$.app.name']
}
```

This produces a JSON object containing only the materialized `$.app.name` branch.

If a processor also needs to reject unexpected bindings rather than merely omit them from output, that is controlled by AEOS schema `world = "closed"`, not by the JSON profile itself.

### Type Annotations → Stripped

Type information is not preserved in JSON output.

### Temporal Types → Strings

```aeon
created:datetime = 2025-01-01T10:00:00Z
```
→
```json
{ "created": "2025-01-01T10:00:00Z" }
```

ZRUT literals preserve the `&` syntax in the string.

### Separator Literals → String or Array

Baseline JSON finalization preserves separator payload as string:

```aeon
size:sep[x] = ^300x250
```
```json
{ "size": "300x250" }
```

Schema- or consumer-driven split/materialization into arrays is an optional downstream transform.

### Comments → Removed

---

## Excluded Features

The following are NOT supported in JSON profile:
- unresolved semantic aliasing (`~>` identity cannot be represented natively in JSON)
- NaN, Infinity

---

## Error Model

| Error            | Condition                   |
| ---------------- | --------------------------- |
| SyntaxError      | Invalid AEON                |
| ReferenceError   | Unresolved reference        |
| SchemaError      | Cannot represent in JSON    |
| JSONProfileError | Domain constraint violation |

---

*End of JSON Profile Appendix*
