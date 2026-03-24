---
id: appendix-node-model-v1
title: Appendix - Node Model
description: Node literal model and representation boundaries relative to canonical pathing.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-node-model-v1
---

# Appendix N — Node Model

## Status

**Optional, profile-gated feature**
**Not enabled in AEON Core v1 by default**
**Active freeze draft:** `specs/01-proposals/r8/r8-node-model-v1-freeze.md`

---

## 1. Purpose

The Node Model introduces a **non-binding structural container** intended for:

* mixed content
* ordered, non-addressable children
* structural grouping without introducing canonical paths

Nodes exist to represent **structure without identity**.

They are explicitly *not* objects, lists, or bindings.

---

## 2. Design Principles

The Node Model is governed by the following invariants:

1. **Nodes do not introduce bindings**
2. **Node children never receive canonical paths**
3. **Nodes are opaque to AEON Core**
4. **Nodes do not affect Assignment Event semantics**
5. **Nodes preserve ordering**

Nodes are structural only.
They do not participate in identity, reference resolution, or assignment.

---

## 3. Syntax

### 3.1 Node Declaration

A node is declared using the following syntax:

```aeon
<tag(child1, child2, child3)>
<tag>
```

Where:

* `tag` is an identifier naming the node type
* `<tag(...)>` encloses an **ordered list of node children**
* `<tag>` is the empty-node shorthand and is exactly equivalent to `<tag()>`

Whitespace and separators between children are significant only for ordering.

---

### 3.2 Node as Binding Value

A node may appear **only as the value of a binding**:

```aeon
content = <paragraph("Hello ", <strong("world")>)>
```

In this example:

* `$.content` is a canonical binding
* `paragraph` and `strong` are node tags
* Node children have **no canonical paths**

---

## 4. Node Children

### 4.1 Child Types

A node child MAY be any of the following:

* literal value
* object literal
* list literal
* node
* reference (`~`, `~>`)

### 4.2 Ordering

Node children are:

* strictly ordered
* preserved exactly as written
* not sorted, normalized, or deduplicated

Ordering is observable only by consumers that interpret node values.

---

## 5. Canonical Path Semantics

### 5.1 Nodes

A node itself **does not receive a canonical path**.

Only the **binding that owns the node** has a canonical path.

```aeon
p = <paragraph("text")>
```

Canonical paths:

* `$.p` ✔
* `$.p[0]` ✘
* `$.p.text` ✘

---

### 5.2 Bindings Inside Node Children

If a node child contains an object literal with bindings:

```aeon
p = <paragraph({ emphasis = "strong" })>
```

Then:

* `$.p` is a binding
* `$.p.emphasis` **is a binding**
* The object literal behaves normally
* The node does not introduce path segments

---

## 6. Assignment Events

Nodes do **not** emit Assignment Events.

Only bindings emit Assignment Events.

If a binding’s value is a node, the node appears as the **opaque value** of the event.

```aeon
title = <heading("Hello")>
```

Emitted event:

* path: `$.title`
* value: Node(`heading`, children…)

No events are emitted for:

* node tag
* node children
* child positions

---

## 7. References

References (`~`, `~>`) inside node children are:

* syntactically valid
* symbolically preserved
* validated normally (missing, forward, self)

However:

* nodes themselves are **not reference targets**
* references may only target canonical binding paths

---

## 8. Profiles and Enablement

Node syntax is **not enabled by default**.

A processor/profile must explicitly enable node syntax.

Example:

```aeon
aeon:profile = "node"
```

Document profile declaration is advisory under zero-trust processing.
Processors MUST select from an explicit whitelist/registry and verify profile compatibility before enabling node syntax.

Without processor/profile enablement:

* node syntax MUST produce a ProfileError
* parsing MUST fail-closed

---

## 9. Mode Interaction

Node semantics are **mode-agnostic**.

* `transport` vs `strict` does not change node behavior
* typing rules apply only to bindings, not node structure

---

## 10. Non-Goals (Explicitly Excluded)

The Node Model does **not** provide:

* automatic traversal semantics
* indexing or addressing of children
* implicit binding creation
* execution or evaluation
* rendering rules

Any such behavior must be implemented **outside AEON Core**.

---

## 11. Rationale

The Node Model exists to support **structure without identity**.

It allows AEON to express:

* mixed content
* hierarchical grouping
* ordered, non-addressable elements

…without violating AEON’s core invariants:

* immutability
* explicit identity
* canonical path determinism
* auditability

---

## 12. Summary

* Nodes are **structural containers**
* Bindings are the **only identity-bearing construct**
* Node children are **ordered, opaque, and non-addressable**
* Nodes are **profile-gated and optional**
* AEON Core remains a **binding-centric system**
