---
id: appendix-processing-model-v1
title: Appendix - Processing Model
description: Conceptual phase pipeline from lexing through finalization, including assignment events.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-processing-model-v1
---

# Appendix — Processing Model

**Appendix to:** AEON Specification v1

**Status:** decision-needed for consolidated v1

Canonical topic owners: `../AEON-spec-v1.md`, `../AEOS-spec-v1.md`

This appendix predates the v1 phase-boundary cleanup and must not be treated as the primary authority for current phase ownership.
If this appendix conflicts with the canonical v1 spec set, the canonical v1 spec set wins.

This appendix defines AEON's normative processing phases, Assignment Events, Processor Registry, and v1 updates for tuple/indexed-path support and annotation stream emission.

> [!IMPORTANT]
> **v1 Baseline Additions**
>
> **New in v1 baseline:** Tuple literal parsing (`TupleLiteral`), indexed path segment assignment (`[n]`), annotation stream record emission, reference resolution for indexed targets.
>
> **Gated:** These additions are part of the consolidated v1 baseline unless otherwise profile-gated.

---

## 1. Processing Phases

Implementations MUST follow the behavior of these conceptual phases:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Lexing                                                         │
│   Input → Tokens; classify comment channel prefixes                     │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 2: Structural Parse                                               │
│   Tokens → AST (objects, lists, tuples, scalars, bindings)              │
│   v1: emit TupleLiteral for (...) forms                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 3: Canonical Path Resolution                                      │
│   Each node assigned a canonical path ($.foo.bar)                       │
│   v1: assign indexed segments to list/tuple elements ($.foo[0])         │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 4: Assignment Event Emission                                      │
│   Exactly one event per binding                                         │
│   v1: emit annotation stream records for structured comments            │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 5: Profile Interpretation                                         │
│   Processors invoked, datatype hints interpreted                        │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 6: Schema Validation                                              │
│   Constraints evaluated, violations reported                            │
│   v1: tuple constraints (TYPE_IS, LENGTH_EXACT, per-position)           │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 7: Reference Evaluation                                           │
│   References resolved to values or aliases                              │
│   v1: indexed path targets resolved ($.a[1])                            │
├─────────────────────────────────────────────────────────────────────────┤
│ Phase 8: Finalization                                                   │
│   Final document model materialized                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Assignment Events

### 2.1 Definition

An **Assignment Event** is a normalized record emitted for each binding.

### 2.2 Required Fields

| Field   | Type   | Description                                          |
| ------- | ------ | ---------------------------------------------------- |
| `path`  | string | Canonical path to the node                           |
| `key`   | string | Key name being bound                                 |
| `value` | Value  | Parsed AEON value (`ListNode`, `TupleLiteral`, etc.) |
| `span`  | Span   | Source location                                      |

### 2.3 Optional Fields

| Field         | Type   | Description              |
| ------------- | ------ | ------------------------ |
| `datatype`    | string | Datatype hint if present |
| `annotations` | map    | Assignment annotations   |
| `raw`         | string | Raw literal text         |

### 2.4 Example

```aeon
p:point@{style:color = #FF0000} = { x = 23, y = 3, z = 34 }
```

Assignment Event:
```json
{
  "path": "$.p",
  "key": "p",
  "datatype": "point",
  "annotations": { "style:color": "#FF0000" },
  "value": { "x": 23, "y": 3, "z": 34 }
}
```

### 2.5 Tuple Example (v1 baseline)

```aeon
score:tuple<string,int32> = ("alice", 95)
```

Assignment Events:
```json
{
  "path": "$.score",
  "key": "score",
  "datatype": "tuple<string,int32>",
  "value": { "kind": "TupleLiteral", "elements": ["alice", 95] }
}
```

Element sub-events (if emitting per-element events):
```json
{ "path": "$.score[0]", "value": { "kind": "StringLiteral", "raw": "alice" } }
{ "path": "$.score[1]", "value": { "kind": "NumberLiteral", "raw": "95" } }
```

---

## 3. Uniqueness (Const Semantics)

AEON documents are immutable by construction:

- For any canonical path, there MUST be **at most one** Assignment Event
- Duplicate path bindings MUST raise an error
- No implicit override, merge, or replacement semantics

---

## 4. Annotation Stream Emission (v1 baseline)

Annotation stream records are emitted in Phase 4, in parallel with Assignment Events. They do NOT appear in the AES.

See *Appendix: Annotation Stream* for record format and binding rules.

**Key invariants:**
- Annotation stream emission MUST NOT affect AES contents
- AES with all comments stripped MUST equal AES with comments present
- Annotation stream records are source-ordered

---

## 5. Processor Registry

### 5.1 Definition

A **Processor** is a deterministic transformation function applied to Assignment Events.

### 5.2 Design Principles

1. **No implicit execution** — Documents cannot invoke processors directly
2. **Profile-scoped authority** — Only the active profile enables processors
3. **Determinism** — Same input produces identical output
4. **No structural mutation** — Processors cannot add/remove nodes
5. **Explicit phase boundary** — Processors run in Phase 5 only

### 5.3 Processor Binding

Profiles declare processors bound to:
- Datatype hints (e.g., `point` → `geom.point`)
- Annotation keys (e.g., `style:color` → `core.hex`)
- Canonical paths

### 5.4 Invocation

During Phase 5, for each Assignment Event:
1. Profile determines applicable processors
2. Processors invoked in deterministic order
3. Each processor receives the event and current value
4. Processor may validate, transform, or attach metadata

### 5.5 Processor Input

Processors receive:
- `path` — canonical path
- `value` — current value (may be `ListNode` or `TupleLiteral` in v1)
- `datatype` — if present
- `annotations` — if present

### 5.6 Processor Output

Processors MAY:
- Return a transformed value
- Return the same value unchanged
- Raise a validation error

Processors MUST NOT:
- Return multiple values
- Alter the canonical path
- Emit new Assignment Events

---

## 6. Reference Evaluation Phase

### 6.1 Binding Visibility Rule

A binding becomes eligible as a reference target **only after** its Assignment Event has been committed.

Self-references (e.g., `a = ~a`) are therefore invalid.

### 6.2 No Forward References

References MUST target paths already bound earlier in the document.

The no-forward rule applies **independently per namespace** (data and attribute).

### 6.3 Indexed Reference Targets (v1 baseline)

In v1 mode, references may target indexed paths:

```aeon
items  = (10, 20, 30)
second = ~items[1]     // clone of element at $.items[1]
```

Resolution proceeds using the same no-forward rule (referenced indexed path must be already bound).

### 6.4 Resolution Semantics

| Operator       | Behavior                      |
| -------------- | ----------------------------- |
| `~` (clone)    | Resolve terminal value, copy  |
| `~>` (pointer) | Return alias to named binding |

### 6.5 Cycles

Because AEON forbids forward references, cycles are unrepresentable.

---

## 7. Error Reporting

All errors MUST reference:
- Canonical path
- Span (when available)
- Phase where error occurred

Example:
```
Error: Unknown processor "geom.point"
Path: $.p
Phase: Profile Interpretation
```

---

*End of Processing Model — v1*
