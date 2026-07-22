---
id: sansa-v1-extensions
title: SANSA v1 Extension Candidates
description: Proposal-stage candidate extensions for SANSA selectors and query helpers.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/extensions
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-resolve
  - sansa-v1-query
  - aeon-v1-value-semantics
---

# SANSA v1 Extension Candidates

Status: Proposal candidate  
Scope: candidate selector and query-helper extensions under design review.

This document records candidate extensions before they are accepted into the core SANSA v1 addressing, resolution, or query proposals.

The features in this document are not part of the current conformance surface until promoted into the corresponding addressing, resolve, query, and CTS documents.

Extensions have two broad categories:

- **Language extensions** change SANSA syntax, selector vocabulary, AST shape, or parse/render contracts.
- **Library extensions** add named helpers, functions, or evaluator forms without changing the language grammar.

Extensions have maturity:

- **Draft**: recorded design idea with no implementation expectation.
- **Experimental**: implemented or prototyped for evaluation, but not part of core conformance.
- **Candidate**: considered stable enough for promotion review.
- **Promoted**: moved into the relevant core proposal and CTS conformance surface.
- **Deprecated**: retained for compatibility but no longer recommended.
- **Removed**: no longer part of the active extension surface.

Candidate and experimental extensions do not modify SANSA v1 conformance. Implementations may expose them only as explicitly documented implementation extensions until promotion.

Each extension should declare an owning capability, such as `SANSA.Addressing`, `SANSA.Resolve`, `SANSA.Query`, or a future capability.

## 1. Design Constraints

Candidate extensions should preserve these SANSA boundaries:

- selectors describe navigation or filtering, not mutation;
- fixed canonical addresses remain exact and stable;
- selector expressions may resolve zero, one, or many bindings;
- consumers own authorization and exposed namespace capabilities;
- host profiles may restrict semantics without violating SANSA syntax;
- documents must not define executable behavior.

## 2. Promoted Parent Selector

The parent selector was originally tracked here as a candidate extension. It has been promoted into the SANSA Addressing and Resolve v1 proposals.

Surface syntax:

```text
.^
```

Examples:

```text
?.^.id
?.^.sibling
$.inventory.items[2].^.metadata
```

The parent selector is a selector, not part of a fixed canonical address. An address expression containing `.^` is therefore non-canonical even when it resolves to exactly one binding.

The caret character is not a bare member selector. A binding literally named `^` remains addressable with a quoted member selector:

```text
.["^"]
```

### 2.1 Resolution Semantics

`.^` selects the immediate parent binding exposed by the resolver.

The selector resolves to:

- one binding when the current binding has an exposed parent;
- an empty Binding Set when the current binding is the effective resolution root;
- a diagnostic when the consumer forbids parent traversal or the traversal would escape an authorized boundary.

Parent traversal must be explicitly authorized by the resolving consumer. It must not bypass local address-space, attribute address-space, profile, or capability boundaries.

For attribute and local address spaces, the proposed default is immediate address-space parent traversal. For example, resolving parent from inside an attribute address space returns the containing attribute-space binding, not necessarily the owning primary binding. A later proposal may define a separate owner-style selector if that capability is needed.

## 3. Promoted Position Range Selector

The position range selector was originally tracked here as a candidate extension. It has been promoted into the SANSA Addressing and Resolve v1 proposals.

Surface syntax:

```text
[start..end]
[start..]
[..end]
```

Examples:

```text
$.items[2..5]
$.items[2..]
$.items[..5]
```

The range endpoints use the same unsigned decimal index syntax as positional selectors. SANSA v1 portable implementations must support endpoints through at least `999999`, representing one million addressable positions from `0` through `999999`; larger accepted values are implementation-defined and non-portable. Implementations that accept larger endpoints should surface `SANSA_NON_PORTABLE_POSITION_INDEX` through a non-fatal diagnostic channel when available.

The following forms are intentionally invalid:

```text
$.items[..]
$.items[-1]
$.items[2..-1]
```

### 3.1 Resolution Semantics

Ranges are inclusive:

```text
$.items[2..5]
```

selects positions `2`, `3`, `4`, and `5`.

Open start means position `0`. Open end means through the final exposed positional child.

If `start > end`, the selector resolves to an empty Binding Set rather than a diagnostic.

Position range selectors are non-exact selectors. An expression containing a range is not a fixed canonical address even when the selected range contains exactly one binding.

SANSA syntax does not assign container semantics to ranges. Lists, tuples, nodes, and other host structures may expose ordered positional children, but whether a binding has meaningful ordered positional children is a profile or host decision.

Proposed AST shape:

```js
{
  type: "positionRange",
  start: 2,
  end: 5
}
```

Open endpoints are represented as `null`:

```js
{ type: "positionRange", start: 2, end: null }
{ type: "positionRange", start: null, end: 5 }
```

## 4. Experimental Transform-Library Helpers

Category: Transform library extension  
Maturity: Experimental  
Capability: `SANSA.Transform`

The `objectFrom(...)` and `fieldsFrom(...)` helpers are experimental transform-library helpers for ordered row-like Binding Sets. They are usable from Query projection contexts in implementations that advertise the relevant extension, but they are not part of required SANSA.Query v1 core conformance.

SANSA.Addressing already supports positional access into ordered row-like structures:

```aeon
table = {
  header:list = ["name", "age"]
  content:list = [
    ("Bob", 22)
    ("Alice", 31)
  ]
}
```

Current SANSA.Query can project tuple positions manually:

```text
from $.table.content.*
select {
  user_name = .[0]
  user_age = .[1]
}
```

`objectFrom(...)` links header positions to row positions and constructs an object whose field names come from the header row.

Surface syntax:

```text
objectFrom($.table.header.*, .*)
fieldsFrom($.table.header.*, .*, "age")
```

Example:

```text
from $.table.content.*
select objectFrom($.table.header.*, .*)
```

Result:

```text
$.table.content[0] = {"name":"Bob","age":22}
$.table.content[1] = {"name":"Alice","age":31}
```

These helpers belong to the transform-library surface, not the address selector language and not Query core. They pair two ordered Binding Sets by position and use the left side as object keys and the right side as object values.

### 4.1 `objectFrom(...)` Contract

- Key bindings must expose string scalar values.
- Duplicate keys produce a diagnostic.
- Mismatched key and value lengths produce a cardinality diagnostic.
- Value bindings must expose scalar values.

## 5. Promoted String Case Helper

The `upper(...)` helper was originally tracked here as a candidate companion to `lower(...)`.

It has been promoted into the SANSA.Query v1 proposal as part of the initial string helper set:

```text
select upper(.name)
```

`upper(...)` follows the same argument contract as `lower(...)`:

- exactly one argument;
- the argument must evaluate to one string scalar;
- missing bindings produce `Missing`;
- multiple bindings produce `CardinalityError`;
- explicit null, NaN, infinity, Boolean, number, object, and Binding Set arguments produce a function-argument diagnostic.

The promoted surface uses `upper(...)` rather than `uppercase(...)`, matching the existing `lower(...)` helper and avoiding aliases in the initial conformance surface.

Case mapping is defined by Shared AEON Value Semantics. An implementation slice may use its host runtime's default Unicode case mapping while the shared contract is still proposal-stage, but normative behavior should not depend on host locale, process locale, database collation, or host-language defaults.

## 6. Experimental Field Projection Helper

Category: Transform library extension  
Maturity: Experimental  
Capability: `SANSA.Transform`

The `fieldsFrom(...)` helper is an experimental companion to `objectFrom(...)`.

Surface syntax:

```text
fieldsFrom(<keys>, <values>, <field-name>, ...)
```

Example:

```text
from $.table.content.*
select fieldsFrom($.table.header.*, .*, "age")
```

Result:

```text
$.table.content[0] = {"age":22}
$.table.content[1] = {"age":31}
```

The helper pairs an ordered key Binding Set with an ordered value Binding Set, then emits only the requested string-named fields. It is useful for testing row/header projection without adding dynamic selectors to SANSA.Query.

Experimental contract:

- the first two arguments are resolution expressions;
- key and value Binding Sets have equal length;
- key bindings expose string scalar values;
- selected value bindings expose scalar values;
- at least one requested field name is supplied;
- requested field names are unique string scalars;
- every requested field exists exactly once in the key Binding Set.

`fieldsFrom(...)` is not part of required SANSA.Query v1 conformance. Implementations that expose it must advertise it as an experimental `SANSA.Transform` extension.

## 7. Promotion Checklist

Before any candidate in this document becomes part of the implemented v1 surface:

- update the core addressing, resolve, or query proposal;
- add positive and negative CTS cases;
- update implementation tests and stress tests;
- update parser and AST contracts;
- update resolver or evaluator contracts;
- update user-facing documentation and playground examples.
