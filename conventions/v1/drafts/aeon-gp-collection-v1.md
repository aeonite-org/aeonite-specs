---
id: aeon-gp-collection-v1
title: AEON GP Collection v1
description: Draft general-purpose convention for describing collection intent, ordering, uniqueness, addressing, and materialization hints without extending AEON Core containers.
family: conventions
group: General-Purpose Conventions
status: Draft collection convention
license: CC0-1.0
path: specification/conventions/aeon-gp-collection-v1
links:
  - aeon-conventions-overview
  - aeon-core-v1-structure-syntax
---
# AEON GP Collection v1

## Status

Draft collection convention

Convention identifier: `aeon.gp.collection.v1`

---

# 1. Purpose

`aeon.gp.collection.v1` defines a standard metadata vocabulary for describing collection intent on top of ordinary AEON containers.

It applies to Core structural containers such as:

- `list`
- `tuple`
- `object` / `map`
- `node`

The convention separates:

| Concern | Responsibility |
| ------- | -------------- |
| Container syntax and structure | AEON Core |
| Collection interpretation policy | `aeon.gp.collection.v1` metadata |
| Validation and materialization | AEOS, profiles, Tonics, processors, or host runtimes |

This convention does not extend AEON Core syntax and does not introduce native runtime collections such as sets, queues, stacks, or dictionaries.

Documents using this convention should declare it in the header:

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.collection.v1"
  ]
}
```

---

# 2. Design Intent

AEON Core provides transport-level structures. It does not define host-language collection behavior.

For example, a Core `list` preserves order and supports indexed addressing, but Core does not say whether the list should be treated as:

- a sequence
- a set
- a bag
- a queue
- a stack
- a stream

Likewise, a Core object or map provides keyed structure, but a convention may still identify that structure as a lookup table, registry, or other keyed collection pattern.

`aeon.gp.collection.v1` records that intent as explicit metadata while preserving the underlying AEON value.

Example:

```aeon
tags@{
  collection = "set"
  order = "insignificant"
  uniqueness = "unique"
}:list<string> = [
  "transport",
  "deterministic",
  "typed"
]
```

The value remains structurally a `list`; the metadata states how a cooperating consumer may validate or materialize it.

---

# 3. Scope

This convention defines collection interpretation metadata.

It does not define:

- new Core container syntax
- native mathematical sets
- host-language object identity
- hashing or equality algorithms
- mutation behavior
- automatic sorting
- automatic duplicate removal
- mandatory runtime materialization

Consumers that do not understand this convention should preserve the attributes as ordinary AEON metadata or fail according to their convention-adoption policy.

---

# 4. Fields

The following attribute keys are defined by `aeon.gp.collection.v1`.

## 4.1 `collection`

`collection` describes conceptual collection intent.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"sequence"` | Ordered collection |
| `"set"` | Unordered unique collection |
| `"bag"` | Unordered duplicate-capable collection |
| `"queue"` | First-in, first-out collection |
| `"stack"` | Last-in, first-out collection |
| `"lookup"` | Keyed lookup structure |
| `"registry"` | Symbolic keyed mapping |
| `"stream"` | Progressive or lazy sequence |

This field is informational unless enforced by a schema, profile, processor, or application policy.

Examples:

```aeon
jobs@{
  collection = "queue"
  order = "significant"
}:list<string> = [
  "compile",
  "test",
  "deploy"
]
```

```aeon
status_codes@{
  collection = "lookup"
  address = "key"
}:object = {
  ok = 200
  not_found = 404
}
```

## 4.2 `order`

`order` describes whether element order carries semantic meaning.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"significant"` | Position matters |
| `"insignificant"` | Position should not affect meaning |
| `"stable"` | Insertion or author order should be preserved |
| `"sorted"` | The collection is expected to be sorted |

`order = "insignificant"` does not permit a Core processor to reorder serialized data. It is an interpretation hint for cooperating consumers and downstream validation or materialization layers.

Example:

```aeon
permissions@{
  collection = "set"
  order = "insignificant"
  uniqueness = "unique"
}:list<string> = [
  "read",
  "write",
  "execute"
]
```

## 4.3 `uniqueness`

`uniqueness` describes duplicate policy.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"allow"` | Duplicates are permitted |
| `"unique"` | Duplicates are forbidden |
| `"unique-by"` | Uniqueness is determined by a derived property or external rule |

`uniqueness = "unique-by"` requires an accompanying convention, schema, profile, or application rule to identify the property used for uniqueness.

### 4.3.1 `uniqueBy`

`uniqueBy` identifies the property, key, or rule name used when `uniqueness = "unique-by"`.

The value should be a string unless a profile or schema defines a structured form.

Example:

```aeon
users@{
  collection = "set"
  uniqueness = "unique-by"
  uniqueBy = "id"
}:list<object> = [
  { id:string = "u1", name:string = "Ari" }
  { id:string = "u2", name:string = "Bo" }
]
```

## 4.4 `address`

`address` describes the expected addressing strategy for collection members.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"index"` | Address by numeric index |
| `"value"` | Address by contained value |
| `"key"` | Address by object/map key |
| `"path"` | Address by canonical path |

Example:

```aeon
routes@{
  collection = "registry"
  address = "key"
}:object = {
  home = "/"
  docs = "/docs"
}
```

## 4.5 `semantics`

`semantics` describes structural interpretation.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"homogeneous"` | Members are expected to share a type or shape |
| `"heterogeneous"` | Members may intentionally mix types or shapes |
| `"tuple-like"` | Members have positional roles |
| `"sparse"` | Gaps or absent positions are meaningful |

Example:

```aeon
rgb@{
  semantics = "tuple-like"
}:list<number> = [255, 128, 0]
```

## 4.6 `mutability`

`mutability` is an optional materialization hint.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"mutable"` | Materialized collection may change |
| `"immutable"` | Materialized collection should not change |
| `"append-only"` | Materialized collection should only grow |

AEON Core does not enforce mutability.

Example:

```aeon
audit_events@{
  collection = "sequence"
  order = "stable"
  mutability = "append-only"
}:list<object> = [
  { action:string = "created" }
  { action:string = "approved" }
]
```

---

# 5. Dictionaries, Objects, and Maps

AEON Core already provides first-class keyed structure through objects/maps.

This convention does not define a separate dictionary container. Use an AEON object/map for keyed data and add collection metadata only when the document needs to communicate extra interpretation.

Example:

```aeon
labels@{
  collection = "lookup"
  address = "key"
}:object = {
  en = "Hello"
  fr = "Bonjour"
}
```

The object remains an object. The convention states that cooperating consumers may treat it as a lookup collection.

---

# 6. Sets

AEON Core does not define native mathematical sets.

Set-like data should be represented as a `list` with explicit collection metadata:

```aeon
features@{
  collection = "set"
  order = "insignificant"
  uniqueness = "unique"
}:list<string> = [
  "offline"
  "sync"
  "audit"
]
```

A schema, profile, processor, or application may reject duplicates or materialize the list as a host-language set. Core AEON remains neutral.

---

# 7. Validation

This convention defines vocabulary, not enforcement.

Validation may be supplied by:

- AEOS schemas
- profiles
- convention-aware processors
- materializers
- application policy

Recommended validation behavior:

- reject values outside the allowed vocabulary for each field;
- reject contradictory combinations when a profile or schema defines them;
- enforce uniqueness only when the applicable validation layer requires it;
- preserve source order unless a downstream layer explicitly performs a materialization step.

---

# 8. Relationship to Core

`aeon.gp.collection.v1` does not change AEON Core container behavior.

Core still defines:

- list element order and indexed structure;
- tuple positional structure;
- object/map keyed structure;
- node child structure;
- canonical paths and canonical serialization rules.

This convention adds interpretation metadata around those structures.

---

# 9. Summary

`aeon.gp.collection.v1` provides a general-purpose way to describe collection semantics such as set-like lists, lookup objects, ordering policy, uniqueness policy, addressing strategy, structural intent, and materialization hints while keeping AEON Core transport-focused and runtime-neutral.
