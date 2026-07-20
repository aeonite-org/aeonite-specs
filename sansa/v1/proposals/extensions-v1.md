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
---

# SANSA v1 Extension Candidates

Status: Proposal candidate  
Scope: candidate selector and query-helper extensions under design review.

This document records candidate extensions before they are accepted into the core SANSA v1 addressing, resolution, or query proposals.

The features in this document are not part of the current conformance surface until promoted into the corresponding addressing, resolve, query, and CTS documents.

## 1. Design Constraints

Candidate extensions should preserve these SANSA boundaries:

- selectors describe navigation or filtering, not mutation;
- fixed canonical addresses remain exact and stable;
- selector expressions may resolve zero, one, or many bindings;
- consumers own authorization and exposed namespace capabilities;
- host profiles may restrict semantics without violating SANSA syntax;
- documents must not define executable behavior.

## 2. Parent Selector

The parent selector is a candidate selector that moves from the current binding to its exposed parent binding.

Proposed syntax:

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

### 2.1 Proposed Resolution Semantics

`.^` selects the immediate parent binding exposed by the resolver.

The selector resolves to:

- one binding when the current binding has an exposed parent;
- an empty Binding Set when the current binding is the effective resolution root;
- a diagnostic when the consumer forbids parent traversal or the traversal would escape an authorized boundary.

Parent traversal must be explicitly authorized by the resolving consumer. It must not bypass local address-space, attribute address-space, profile, or capability boundaries.

For attribute and local address spaces, the proposed default is immediate address-space parent traversal. For example, resolving parent from inside an attribute address space returns the containing attribute-space binding, not necessarily the owning primary binding. A later proposal may define a separate owner-style selector if that capability is needed.

## 3. Position Range Selector

The position range selector is a candidate selector that selects a contiguous inclusive range of positional children.

Proposed syntax:

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

The range endpoints use the same unsigned decimal index syntax as positional selectors.

The following forms are intentionally invalid:

```text
$.items[..]
$.items[-1]
$.items[2..-1]
```

### 3.1 Proposed Resolution Semantics

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

## 4. Tabular Projection Helper

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

The unresolved design question is how to link header positions to row positions and construct an object whose field names come from the header row.

Candidate conceptual helper:

```text
zipObject($.table.header.*, .*)
```

Example:

```text
from $.table.content.*
select zipObject($.table.header.*, .*)
```

Conceptual result:

```text
$.table.content[0] = {"name":"Bob","age":22}
$.table.content[1] = {"name":"Alice","age":31}
```

This belongs to SANSA.Query projection semantics, not the address selector language. It pairs two ordered Binding Sets by position and uses the left side as object keys and the right side as object values.

### 4.1 Open Questions

- Should the helper be named `zipObject`, `objectFrom`, `records`, or something else?
- Should key bindings be required to expose string scalar values?
- Should duplicate keys be rejected, keep first value, keep last value, or produce a multi-value representation?
- Should mismatched lengths produce a diagnostic or truncate to the shorter side?
- Should non-scalar row values preserve binding identity or render as derived values?

Until these questions are resolved, table-style projection remains expressible manually with positional selectors.

## 5. String Case Helper

The current SANSA.Query string helper set includes:

```text
contains(...)
startsWith(...)
endsWith(...)
lower(...)
concat(...)
```

The candidate companion helper is:

```text
upper(...)
```

Example:

```text
select upper(.name)
```

`upper(...)` should follow the same argument contract as `lower(...)`:

- exactly one argument;
- the argument must evaluate to one string scalar;
- missing bindings produce `Missing`;
- multiple bindings produce `CardinalityError`;
- explicit null, NaN, infinity, Boolean, number, object, and Binding Set arguments produce a function-argument diagnostic.

The proposed surface uses `upper(...)` rather than `uppercase(...)`, matching the existing `lower(...)` helper and avoiding aliases in the initial conformance surface.

Case mapping is semantic-profile-defined. An implementation slice may use its host runtime's default Unicode case mapping, but the specification should not depend on host locale behavior.

## 6. Promotion Checklist

Before any candidate in this document becomes part of the implemented v1 surface:

- update the core addressing, resolve, or query proposal;
- add positive and negative CTS cases;
- update implementation tests and stress tests;
- update parser and AST contracts;
- update resolver or evaluator contracts;
- update user-facing documentation and playground examples.
