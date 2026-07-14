---
id: sansa-v1-addressing
title: SANSA v1 Addressing
description: Draft address model and selector vocabulary for SANSA.
family: sansa
group: SANSA
status: Draft
path: specification/sansa/v1/addressing
license: CC-BY-4.0
links:
  - sansa-v1-resolve
  - sansa-v1-query
---

# SANSA v1 Addressing

Status: Draft  
Scope: structural address model and selector vocabulary for SANSA v1.

## 1. Overview

SANSA addressing defines a deterministic notation for identifying semantic bindings in a semantic address namespace.

An address describes structure. It does not, by itself, require traversal, execution, mutation, authorization, or value evaluation. Those responsibilities belong to a resolving consumer, SANSA.Resolve, SANSA.Query, or another capability layered above the address model.

## 2. Terms

A **namespace** is the addressable semantic structure exposed by a SANSA implementation.

A **binding** is an addressable semantic unit exposed by a namespace.

A **Binding Set** is an ordered collection of bindings.

A **selector** is one navigation or filtering operation in an address expression.

A **canonical address** is an exact address that identifies at most one binding in a namespace.

An **address expression** may identify zero, one, or many bindings when resolved. It may contain expansion, filter, pattern, or local address-space selectors.

## 3. Address Roots

### 3.1 Absolute Root

The absolute root is written:

```text
$
```

It means:

> Begin from the primary root supplied by the resolving consumer.

Examples:

```text
$.contact.name
$.contacts[0]
$.message.@.id
```

### 3.2 Contextual Root

The contextual root is written:

```text
?
```

It means:

> Begin from the contextual root supplied by the resolving consumer.

Examples:

```text
?.name
?.address.city
?.items[0]
```

Contextual-root expressions are structurally valid without a context, but they cannot be resolved unless the consumer supplies one.

### 3.3 Relative Selector Fragments

Some consumers, including SANSA.Query, allow selector fragments that begin with a selector rather than a root:

```text
.name
.roles.*
.@.metadata
```

Such fragments are not complete absolute addresses. Their starting point is supplied by the consuming capability.

## 4. Exact Selectors

Exact selectors preserve a path that can identify at most one binding.

### 4.1 Named Binding

```text
.name
```

Selects a direct named child binding.

Names that cannot be written safely in bare form use a quoted member segment:

```text
.["member.with.dots"]
.["spaced name"]
```

### 4.2 Positional Binding

```text
[0]
[12]
```

Selects the binding at the specified zero-based position in the ordered sequence exposed by the current binding.

Positional syntax is representation independent. It does not itself distinguish lists, tuples, nodes, or implementation-specific ordered structures.

### 4.3 Attribute Address Space

```text
.@
```

Enters the attribute address space of the current binding.

Once inside the attribute address space, ordinary SANSA navigation applies.

Examples:

```text
$.message.@.id
$.message.@.properties.caller.@.by
```

Compact forms such as `$.message@id` are not normative in SANSA v1. Consumers may accept them as compatibility sugar, but the canonical SANSA form uses `.@`.

### 4.4 Local Address Space

```text
.<"namespace">
```

Enters a named local address space at the current resolution point.

Examples:

```text
$.document.<"sections">.introduction
$.page.<"html-id">.navigation
$.<"params">.username
$.<"session">.user_id
```

A local address-space segment identifies an address-space transition, not an ordinary child binding. Therefore these two addresses are not equivalent:

```text
$.document.contact
$.document.<"contact">
```

The first selects an ordinary child named `contact`. The second enters a local address space named `contact`.

## 5. Expanded Selectors

Expanded selectors may produce zero or more bindings.

### 5.1 Direct Expansion

```text
.*
```

Expands all direct child bindings of the current binding.

### 5.2 Descendant Expansion

```text
.**
```

Expands descendants reachable through the ordinary value hierarchy. The current binding is not included.

Attribute address spaces and local address spaces are not traversed implicitly. They require explicit selectors.

### 5.3 Name Pattern Selector

```text
.("id-*")
.("*-id")
.("*id*")
.("item-__")
```

Name patterns match complete binding names.

| Operator | Meaning |
| --- | --- |
| `*` | zero or more characters |
| `_` | exactly one character |

Regular expressions are intentionally excluded from SANSA v1 addressing.

## 6. Filter Selectors

Filter selectors filter the current Binding Set. They do not evaluate values.

### 6.1 Semantic Type Filter

```text
#type
```

Filters by semantic datatype identity.

Example:

```text
$.content.*#text
```

### 6.2 Representation Kind Filter

```text
%kind
```

Filters by representation kind.

Example:

```text
$.content.*%stringLiteral
```

Semantic datatype and representation kind are distinct.

```aeon
content = {
  a:text = "I am text"
  b:string = "I am string"
}
```

The expression `$.content.*#text` selects only `a`. The expression `$.content.*%stringLiteral` selects both `a` and `b`.

## 7. Canonical Addresses

Canonical addresses identify at most one binding.

Examples:

```text
$
$.member
$.["member.with.dots"]
$.list[0]
$.message.@.id
$.message.@.properties.caller.@.by
```

Expanded address expressions are not canonical addresses, even though each binding produced by such an expression has its own canonical address.

Examples of non-canonical address expressions:

```text
$.users.*
$.content.*#text
$.content.("id-*")
$.**
```

## 8. Local Address-Space Boundaries

Local address spaces are isolated scopes.

A local address space may only be entered through an explicit local address-space selector:

```text
.<"namespace">
```

There is no fallback between primary and local address spaces. A reference to `$.<"params">.username` must not fall back to `$.params.username`.

Traversal must not cross a local address-space boundary implicitly. SANSA v1 defines no parent selector that can leave a local address space.

Local address spaces exist only when explicitly exposed or mounted by the resolving consumer, environment, or addressed resource. A syntactically valid local address-space selector does not imply authorization to resolve that space.

## 9. Opaque Local Semantics

SANSA standardizes the transition into a named local address space. It does not standardize the internal meaning of every local namespace.

Examples of possible local address spaces include:

- query parameters
- session data
- request data
- sections exposed by an embedded document processor
- HTML identifiers exposed by an HTML processor
- named destinations exposed by a PDF processor
- application-defined resource views

The provider of a local address space owns its internal semantics, subject to SANSA resolution rules and consumer policy.

## 10. Superseded Anchor Form

Earlier design notes explored postfix anchor selectors such as:

```text
$.document<"contact">
```

SANSA v1 drafts prefer the local address-space segment:

```text
$.document.<"contact">
```

The local address-space form makes the transition explicit as a selector and allows additional navigation within the local space.

## 11. Relationship to AEON Literals

The SANSA address model is independent of AEON Core syntax. AEON may define a native SANSA address literal based on this grammar.

When used as an AEON literal, a SANSA address remains declarative. AEON Core is expected to validate structural syntax and transport the value, not resolve the address or evaluate query semantics.

