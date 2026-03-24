---
id: appendix-bindings-v1
title: Appendix - Bindings and Identity
description: Binding identity model, uniqueness constraints, and canonical identity behavior.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-bindings-v1
---

# Appendix — Bindings and Identity

Status: informative summary for consolidated v1

Canonical topic owners: `../AEON-spec-v1.md`, `../structure-syntax-v1.md`, `../addressing-references-v1.md`

If this appendix conflicts with the canonical v1 spec set, the canonical v1 spec set wins.

## 1. Binding as Identity Unit

A binding has the form:

```aeon
path = value
```

Bindings are the identity unit in AEON. Identity-backed behaviors attach to bindings, not to arbitrary value fragments.

## 2. Why Bindings Matter

Bindings provide:
- canonical path identity
- source ordering
- source span anchoring
- uniqueness/immutability checks

These properties are required for deterministic references, diagnostics, schema matching, and canonicalization.

## 3. References Depend on Bindings

References (`~`, `~>`) target bindings via address expressions. A value without binding identity is not a legal reference target.

## 4. Containers and Identity

- Object members are bindings and therefore identity-bearing.
- List/tuple elements are positional values; they are addressable via index segments but are not independent named bindings.
- Attribute metadata is binding-attached and follows the binding target model.

## 5. Node Literals

Node literals are values. Node children do not implicitly create top-level binding identity unless they contain bindings.

Valid introducer example:

```aeon
content = <p("Hello", <strong("world"), { key = 1 })
```

Identity-bearing bindings in this example include `$.content` and `$.content.key`.

## 6. Validation and Diagnostics

Schema/validator rules operate on addressable targets derived from bindings and indexed container structure. Diagnostics should report canonical path plus span where available.

## 7. Summary

Bindings are the semantic spine of AEON: they anchor identity, determinism, and conformance behavior.
