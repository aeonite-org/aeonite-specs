---
id: aeon-v1-parameterized-object-node-claims
title: Parameterized Object and Node Claims
description: "Accepted informative design note recording the rationale and boundaries for parameterized object<T> and node<T> claims in AEON v1."
status: accepted informative design note
family: official-v1
group: Design Notes
license: CC-BY-4.0
path: specification/aeon-v1-documentation/parameterized-object-node-claims
links:
  - aeon-core-v1-value-types
  - aeon-core-v1-structure-syntax
  - aeon-core-v1-compliance
---
# Accepted Design Note: Parameterized Object and Node Claims in AEON

Status: accepted informative design note. The normative requirements live in `../drafts/value-types-v1.md`, `../drafts/structure-syntax-v1.md`, `../drafts/aeon-core-compliance-v1.md`, and related appendices. This note records the rationale and boundaries.

## Purpose

AEON already supports parameterized container claims for lists and tuples:

```aeon
values:list<number> = [1, 2, 3]
point:tuple<number, number> = (144.9631, -37.8136)
```

These claims are preserved by Core and enforced by schema, profile, convention, or consumer validation. Consolidated AEON v1 extends the same surface to `object<T>` and `node<T>`.

## `object<T>`

`object<T>` describes an object whose member values are expected to satisfy the given type claim.

```aeon
scores:object<number> = {
  alice:number = 10
  bob:number = 12
}
```

Core preserves `object<number>` and validates only that the bound value is an object. It does not enforce member values.

## `node<T>`

`node<T>` has two context-sensitive readings.

On ordinary bindings, it claims that the bound node value belongs to a profile, domain, or materialization target:

```aeon
doc:node<html> = <html(<head>, <body>)>
child:node<node> = <tag>
```

Binding-side `node<T>` is deliberately narrower than node-head `node<T>`.
The argument may be `node` itself or a custom profile/domain/materialization target such as `html`.
Reserved non-`node` value datatypes are invalid on ordinary bindings:

```aeon
tag:node<string> = <tag>
```

On node heads, it claims the expected type of that node's direct children:

```aeon
title:node = <title:node<string>("Hello world")>
```

Core preserves the claim in both positions. It rejects reserved non-`node` binding-side arguments and does not validate node-head children against `T`.

## Non-Goals

This does not introduce arbitrary generic reserved datatypes.

Invalid Core v1 examples remain invalid:

```aeon
number<cm> = 3
string<markdown> = "body"
<tag:pair<string, number>("x", 1)>
```

The structural generic family described by this note is:

```text
list<T>
tuple<T...>
object<T>
node<T>
```

Other limited parameterized reserved datatypes, such as absence and non-finite domain claims, are defined by the value-types draft when present. They are outside this note's object/node scope.

## Validation

Validation belongs above Core.

For example, AEOS can express object member intent with selectors:

```json
[
  { "path": "$.scores", "constraints": { "type": "ObjectNode", "datatype": "object<number>" } },
  { "selector": "$.scores.*", "constraints": { "type": "NumberLiteral" } }
]
```

Node child intent can be expressed with indexed child rules:

```json
[
  { "path": "$.title[*]", "constraints": { "type": "StringLiteral" } }
]
```
