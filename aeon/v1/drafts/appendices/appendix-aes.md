---
id: appendix-aes-v1
title: Appendix - Assignment Event Stream (AES)
description: Assignment event stream structure and event-level consistency expectations.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-aes-v1
---

# Appendix — Assignment Event Stream (AES)

**Appendix to:** AEON Specification v1
**Status:** Normative

This appendix defines the Assignment Event Stream — the canonical, lossless intermediate representation produced by AEON Core. v1 updates cover `TupleLiteral` value kind, indexed canonical paths, and annotation stream separation.

---

## 1. Overview

The **Assignment Event Stream (AES)** is the canonical, lossless intermediate representation produced by an AEON processor after successful parsing, validation, and enforcement phases.

AES represents an AEON document as an **ordered stream of immutable Assignment Events**, each describing a single binding operation expressed in the source text.

AES is the **sole semantic output** of AEON Core.
AEON does **not** produce objects, graphs, or materialized values.

**v1 note:** The annotation stream (structured comment records) is a separate output parallel to the AES. It does NOT appear in the AES and MUST NOT affect it. See *Appendix: Annotation Stream*.

---

## 2. Design Rationale

Traditional configuration formats materialize documents into hierarchical data structures (e.g., objects or trees). This approach loses critical information:

- source order
- assignment intent
- reference identity
- provenance and spans
- symbolic structure

AES preserves **what was written**, not what it might mean to a consumer.

This enables:
- Deterministic processing
- Auditable configuration
- Symbolic references (`~`, `~>`)
- Multiple independent interpretations of the same document
- Deferred semantics (schemas, processors, resolution)

---

## 3. Definition

An **Assignment Event** represents a single binding expressed in an AEON document.

Formally:

> *An Assignment Event records that a value was assigned to a canonical path at a specific location in the source document, optionally annotated with a type hint and attributes.*

An **Assignment Event Stream (AES)** is an ordered sequence of Assignment Events.

---

## 4. Assignment Event Structure

Each Assignment Event MUST contain the following fields:

```ebnf
AssignmentEvent ::= {
  path        : CanonicalPath,
  value       : ASTValue,
  span        : SourceSpan,
  datatype?   : TypeHint,
  attributes? : AttributeList
}
```

### 4.1 `path`

- A **Canonical Path** uniquely identifying the binding target
- Derived during Phase 3 (Canonical Path Resolution)
- MUST be unique across the AES
- v1: may include indexed segments (`$.items[0]`)

### 4.2 `value`

- The **original AST value node** associated with the binding
- MUST NOT be coerced, normalized, resolved, or evaluated
- MAY contain symbolic references (`~`, `~>`)

Value kinds:
- `StringLiteral("hello")`
- `NumberLiteral(120)`
- `BooleanLiteral(true)`
- `ObjectNode`
- `ListNode` — `[...]` surface form
- `TupleLiteral` — `(...)` surface form (v1)
- `CloneReference("$.x")`
- `PointerReference("$.x")`

### 4.3 `span`

- The source location of the binding
- Used for diagnostics, auditing, and tooling
- MUST refer to the original source text

### 4.4 `datatype` (optional)

- Explicit type annotation provided in the source
- Example: `string`, `int32`, `switch`, `tuple<string,int32>`
- Presence and enforcement depend on mode

### 4.5 `attributes` (optional)

- Attribute annotations associated with the binding
- Semantics are profile- or schema-defined
- AEON Core MUST treat attributes as opaque metadata

---

## 5. `ListNode` vs `TupleLiteral` (v1)

In v1, AEON Core distinguishes two ordered sequence value kinds:

| Surface | AES Value Kind | Description                |
| ------- | -------------- | -------------------------- |
| `[...]` | `ListNode`     | Homogeneous-element intent |
| `(...)` | `TupleLiteral` | Positional/arity intent    |

These MUST NOT be normalized or collapsed into a single kind by AEON Core.

Downstream consumers (AEOS, Tonic) observe the distinction.

---

## 6. Indexed Canonical Paths in AES (v1)

When indexed path segments are active (v1 baseline), list and tuple elements receive canonical paths with index segments:

```
$.a[0]    // first element of binding a
$.a[1]    // second element
```

These paths follow all addressing rules (zero-based, decimal, no leading zeros). Attribute metadata remains binding-attached rather than index-segment identity. See *Appendix: Addressing Model*.

---

## 7. Ordering Guarantees

AES preserves **lexical source order**.

Assignment Events MUST appear in the stream in the same order as their corresponding bindings appear in the AEON document.

This ordering is:
- Deterministic
- Stable
- Significant

Consumers MUST NOT reorder events unless explicitly operating on a derived representation.

---

## 8. Immutability and Uniqueness

- Each Canonical Path MUST appear **at most once** in an AES
- Duplicate canonical paths are a validation error and MUST result in fail-closed behavior unless recovery is enabled
- Assignment Events are immutable once emitted

---

## 9. Annotation Stream Separation

Annotation stream records from structured comment channels are NOT Assignment Events.

- They are emitted in Phase 4, in parallel with Assignment Events
- They do NOT appear in the AES
- AES content is identical whether or not comments are present

See *Appendix: Annotation Stream* for annotation record format and binding rules.

---

## 10. Relationship to AEON Processing Phases

AES is produced after completion of:
1. Lexing
2. Parsing
3. Canonical Path Resolution
4. Assignment Event Emission
5. Reference Validation
6. Mode Enforcement

If any phase fails and recovery is disabled, AES MUST be empty (fail-closed).

---

## 11. What AES Is Not

AES is explicitly **not**:
- An object tree
- A JSON document
- A resolved graph
- A runtime configuration
- A canonical serialization

Any such representations MUST be constructed by downstream consumers.

---

## 12. Consumers of AES

Typical consumers include:
- Tonics / application-specific materializers
- Schema validators (AEOS)
- Linters and static analysis tools
- Inspection and debugging tools
- Canonicalization and integrity layers
- Annotation stream processors

Each consumer interprets AES according to its own semantics.

---

## 13. Relationship to Schema (AEOS)

AEOS operates **on AES**, not on source text.

Schemas:
- Validate structure and constraints of Assignment Events
- May provide type guarantees
- In v1: distinguish `ListNode` from `TupleLiteral` via `TYPE_IS`
- MUST NOT rewrite or coerce AES values

---

## 14. Summary

- AES is the canonical semantic output of AEON Core
- It preserves intent, order, and provenance
- It defers meaning to downstream consumers
- It enables deterministic, auditable configuration processing
- The annotation stream is a parallel, non-AES output for structured comment records

> **AEON does not produce values.
> AEON produces assignments.**

---

*End of AES Appendix — v1*
