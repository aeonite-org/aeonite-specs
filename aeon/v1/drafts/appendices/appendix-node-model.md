---
id: appendix-node-model-v1
title: Appendix - Node Model
description: Node literal model and representation boundaries relative to canonical pathing.
family: appendices-v1
group: Core Semantics
status: "Optional, profile-gated feature"
license: CC-BY-4.0
path: specification/appendices/appendix-node-model-v1
---
# Appendix N — Node Model

## Status

Status: optional, profile-gated feature.

The Node Model is not enabled in AEON Core v1 by default.

Canonical topic owner: profile or processor specifications that explicitly enable node syntax.

---

## 1. Purpose

The Node Model introduces a **non-binding structural container** intended for:

* mixed content
* ordered child slots
* structural grouping without introducing named binding identity

Nodes exist to represent **structure without named binding identity**.

They are explicitly *not* objects, lists, or bindings.

---

## 2. Design Principles

The Node Model is governed by the following invariants:

1. **Nodes do not introduce bindings**
2. **Node children use indexed canonical path segments**
3. **Nodes are opaque to AEON Core**
4. **Nodes do not create named Assignment Events**
5. **Nodes preserve ordering**

Nodes are structural only.
They preserve ordered child structure while exposing child slots through the same bracket-index path model used by lists and tuples.

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
* the first node child is addressable as `$.content[0]`

---

## 4. Node Children

### 4.1 Child Types

A node child MAY be any of the following:

* literal value
* object literal
* list literal
* node
* reference (`~`, `~>`)
* anonymous typed value (`:type = value`)

Anonymous typed children annotate only the immediate child value. They do not
create named bindings or ordering side effects:

```aeon
page:node = <page(
  :string = "hello"
  <tag>
  :int32 = 3
)>
```

Nested anonymous typed values such as `:n = :n = 3` are invalid.

### 4.2 Ordering

Node children are:

* strictly ordered
* preserved exactly as written
* not sorted, normalized, or deduplicated

Ordering is observable only by consumers that interpret node values.

---

## 5. Canonical Path Semantics

### 5.1 Nodes

A node literal is reached through the canonical path of its owning value slot.
When a node is the value of a binding, the binding path identifies the node value.
Node children then use bracket-index segments beneath that path.

```aeon
p = <paragraph("text")>
```

Canonical paths:

* `$.p` ✔
* `$.p[0]` ✔
* `$.p.text` ✘

---

### 5.2 Bindings Inside Node Children

If a node child contains an object literal with bindings:

```aeon
p = <paragraph({ emphasis = "strong" })>
```

Then:

* `$.p` is a binding
* `$.p[0]` is the anonymous object child
* `$.p[0].emphasis` **is a binding**
* The object literal behaves normally
* The node child slot uses the same bracket-index path form as list and tuple elements

---

## 6. Assignment Events

Nodes do **not** emit named Assignment Events.

Bindings emit ordinary named Assignment Events. Ordered child slots, including node children, may emit synthetic indexed AES events so downstream tooling can validate, project, and materialize them consistently.

If a binding’s value is a node, the node appears as the value of the binding event and its children may be surfaced through indexed child paths.

```aeon
title = <heading("Hello")>
```

Emitted event:

* path: `$.title`
* value: Node(`heading`, children…)

Synthetic indexed child events may be emitted for:

* child positions
* anonymous typed child values
* bindings contained inside object children

---

## 7. References

References (`~`, `~>`) inside node children are:

* syntactically valid
* symbolically preserved
* validated normally (missing, forward, self)

However:

* node child targets use numeric index segments, for example `$.page[0]`
* node tags are not independent reference targets
* references target canonical paths, not raw source positions

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
* ordered child elements

…without violating AEON’s core invariants:

* immutability
* explicit identity
* canonical path determinism
* auditability

---

## 12. Summary

* Nodes are **structural containers**
* Bindings are the **only named identity-bearing construct**
* Node children are **ordered and bracket-index addressable**
* Nodes are **profile-gated and optional**
* AEON Core remains a **binding-centric system**
