---
id: appendix-json-profile-v1
title: Appendix - AEON JSON Profile
description: Informative appendix describing the AEON-to-JSON interoperability profile and transformation expectations.
family: appendices-v1
group: Profiles and Extensions
status: informative profile appendix for consolidated v1
license: CC-BY-4.0
path: specification/appendices/appendix-json-profile-v1
---
# Appendix — AEON JSON Profile

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

AEON member names are data. The JSON profile does not make ordinary member
names invalid merely because a later host runtime treats those names specially.
However, a JSON finalizer that materializes AEON-derived members into a
host-language object graph MUST prevent source-controlled member names from
mutating, shadowing, or escaping into host object metadata, prototypes,
constructors, reflection surfaces, or framework control fields.

For JavaScript-family object materialization, `__proto__`, `constructor`, and
`prototype` are host-dangerous names because they can participate in prototype
pollution when projected into ordinary objects or later merged into ordinary
objects. A JavaScript-family JSON materializer MUST defend against that class of
attack by using a safe representation such as maps or null-prototype objects,
escaping the dangerous names, or rejecting the projection fail-closed.

This is a materialization/export boundary, not an AEON Core syntax boundary.
Core and AES may preserve these names as inert member names.

### Lists → JSON Arrays

Direct mapping. Order preserved.

### Booleans → JSON Booleans

`true`/`false` pass through.

### Toggle → JSON Boolean

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

Indexed child attributes may be projected under reserved `@items` metadata on
the owning binding:

```json
{
  "width": [3],
  "@": {
    "width": {
      "@items": {
        "0": {
          "unit": "cm"
        }
      }
    }
  }
}
```

Profile notes:
- `@items` is reserved in finalized/materialized JSON projection for indexed child attributes;
- this is a projection/profile convention, not a core canonical-path syntax change;
- exact collisions on `@items` are profile errors.

### Transitive Host-Object Risk

Host-object safety is transitive across processing boundaries.

A processor may be safe in its own implementation language while still exporting
AEON-derived names into a later runtime where those names become dangerous. For
example, a Rust service can parse AEON safely, emit JSON containing a
`__proto__` member, and later deliver that JSON to browser JavaScript where an
application merge step could trigger prototype pollution.

Non-JavaScript implementations are not required to reject JavaScript-specific
member names merely because they parse AEON. They MUST NOT, however, describe an
export as JavaScript-object-safe or host-object-safe unless the export either:

- emits an inert representation that cannot affect the target runtime's object
  metadata or prototype system;
- rejects or escapes target-runtime-dangerous names; or
- documents that the output is transport JSON only and must be revalidated or
  safely materialized before host-object use.

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

Legal AEON infinity literals are not representable in the strict JSON profile.
Processors claiming strict JSON-profile conformance MUST fail closed rather than silently rewriting them.
Loose or compatibility-oriented exporters MAY preserve `Infinity` and `-Infinity` as strings, but that behavior is outside the strict JSON profile contract.

### Hex and Radix Literals → JSON Strings

Hex and radix literals finalize as JSON strings of their payload form rather than as JSON numbers.

- hex finalized strings exclude the leading `#`;
- radix finalized strings exclude the leading `%`;
- `_` visual separators are removed during finalized JSON materialization;
- hex finalized strings preserve source letter case unless a stricter downstream profile defines canonical normalization.

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
