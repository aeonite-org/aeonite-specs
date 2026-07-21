---
id: sansa-v1-resolve
title: SANSA.Resolve v1
description: Proposal-stage deterministic structural resolution capability for SANSA.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/resolve
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-query
---

# SANSA.Resolve v1

Status: Proposal  
Scope: deterministic structural resolution of SANSA address expressions.

## 1. Overview

SANSA.Resolve resolves semantic bindings within a namespace.

It answers:

> Which semantic bindings match this resolve expression?

Resolve is structural. It does not perform value comparison, filtering based on values, aggregation, projection, ordering clauses, or expression evaluation.

## 2. Inputs and Outputs

Input:

- a SANSA address expression
- a namespace context
- optional contextual root for `?` or relative use
- consumer policy and capability configuration

Output:

- an ordered Binding Set

Even exact resolution returns a Binding Set. An exact address therefore resolves to one binding or no bindings.

## 3. Binding Model

Resolve operates on semantic bindings rather than raw runtime values.

A resolved binding should expose, either directly or through implementation APIs:

- canonical address
- semantic value
- semantic datatype, when known
- representation kind, when known
- attributes
- provenance sufficient for diagnostics
- parent or containing context, when supported and authorized

The runtime representation of a binding is implementation specific.

## 4. Navigation Model

Resolution applies selectors from left to right.

```text
Binding Set
  |
  v
Selector
  |
  v
Binding Set
  |
  v
Selector
  |
  v
Binding Set
```

Every selector consumes the current Binding Set and produces a new Binding Set.

## 5. Exact Resolution

Exact resolution produces zero or one binding.

Examples:

```text
$.user.name
$.items[2]
$.message.@.id
?.address.city
```

Exact addresses use only exact selectors and do not include parent traversal, expansion, position ranges, pattern matching, semantic type filters, or representation kind filters.

## 6. Non-Exact Resolution

Non-exact resolution may produce zero or more bindings or depend on resolver context beyond a fixed canonical path.

Examples:

```text
$.users.*
$.content.*#text
$.content.("id-*")
$.items[2..5]
$.items[2].^
$.**.id
$.message.@.properties.*
```

Every resolved binding retains its own canonical address.

## 7. Selector Semantics

SANSA.Resolve uses the selector vocabulary defined by SANSA v1 Addressing.

Root selectors establish the starting Binding Set.

Named and positional selectors select direct children or ordered positions.

Position range selectors select inclusive ordered positional children:

```text
$.items[2..5]
$.items[2..]
$.items[..5]
```

Open start means position `0`. Open end means through the final exposed positional child. If `start > end`, the selector resolves to an empty Binding Set rather than a diagnostic.

All present position range endpoints must be within the implementation's configured position index maximum. SANSA v1 portable implementations must support endpoints up to at least `1000000`; larger accepted values are implementation-defined and non-portable. Implementations that accept larger endpoints should surface `SANSA_NON_PORTABLE_POSITION_INDEX` through a non-fatal diagnostic channel when available.

Position ranges are non-exact selectors. SANSA.Resolve does not infer container categories from range syntax; lists, tuples, nodes, and other host structures may expose ordered positional children according to their profile or host adapter.

Parent selectors select the immediate parent binding exposed by the resolver:

```text
$.items[2].^
?.^.sibling
```

Parent traversal resolves to one binding when the current binding has an exposed parent. It resolves to an empty Binding Set when the current binding is the effective resolution root. It fails explicitly when the consumer forbids parent traversal or when traversal would escape an authorized boundary.

Parent traversal is non-exact and must be explicitly supported by the resolving consumer. It must not bypass local address-space, attribute address-space, profile, or capability boundaries.

Attribute selectors enter the attribute address space.

Local address-space selectors enter a named local address space only when the resolving consumer exposes and authorizes that space.

If local address-space traversal is unsupported, the resolver must fail explicitly. If local address-space traversal is supported but the current binding does not expose the requested named space, normal resolution produces no bindings for that branch.

Expansion selectors broaden the Binding Set structurally.

The direct expansion selector `.*` selects the direct structural children of each binding in the current Binding Set.

The descendant expansion selector `.**` selects structural descendants in deterministic preorder. It does not include the current binding.

Expansion selectors do not implicitly enter attribute address spaces or local address spaces. Those spaces are entered only through explicit `.@` or `.<"name">` selectors.

Filter selectors filter by structural metadata such as semantic datatype or representation kind.

Name pattern selectors match complete binding names deterministically.

## 8. Attribute Semantics

Attributes are first-class semantic containers.

Attributes may themselves contain:

- named bindings
- ordered structures
- attributes
- semantic datatypes
- representation kinds

Nested attributes are addressable through ordinary SANSA navigation.

Example:

```aeon
msg@{
  properties = {
    id = 3
    caller@{by = "agent"} = "bot"
  }
} = "hello"
```

Example resolution:

```text
$.msg.@.properties.id
$.msg.@.properties.caller
$.msg.@.properties.caller.@.by
```

## 9. Representation Independence

SANSA.Resolve does not infer container categories from selector syntax.

The address:

```text
$.book[2]
```

means positional selection within the ordered sequence exposed by `$.book`. It does not itself assert that `book` is a list, tuple, node, database cursor, or implementation-specific ordered collection.

The implementation determines how the namespace exposes the relevant child sequence, subject to deterministic behavior.

## 10. Ordering

Binding order must be deterministic.

Rules:

- ordered structures preserve structural order;
- descendant expansion emits descendants in deterministic preorder;
- AES-backed namespaces preserve deterministic event-derived order;
- implementations without inherent stable order must expose deterministic ordering or report the operation unsupported.

Canonical sorting is not the default ordering.

## 11. Unsupported Operations

If an implementation cannot support a requested selector or address-space transition, it must fail explicitly or report the capability as unsupported.

It must not silently treat an unsupported selector as an empty result unless the specification for that selector explicitly permits empty result as normal resolution.

## 12. Out of Scope

SANSA.Resolve v1 does not include:

- value comparison
- predicates
- `where` expressions
- aggregation
- ordering clauses
- projection
- grouping
- functions
- regular expressions
- graph traversal beyond descendant expansion
- mutation
- subscription
- history reconstruction

These belong to SANSA.Query, future SANSA capabilities, or implementation-specific layers.

## 13. Relationship to SANSA.Query

SANSA.Query begins from SANSA.Resolve.

Example:

```text
from $.users.*#person
where .active == true
select .name
```

The `from` clause delegates to SANSA.Resolve. Query then evaluates the resulting Binding Set.
