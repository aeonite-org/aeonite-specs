---
id: appendix-tuples-v1
title: Appendix - Tuples and Indexed Paths
description: Tuple semantics and indexed path behavior at parse, pathing, and validation boundaries.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-tuples-v1
---

# Appendix — Tuples and Indexed Paths

**Appendix to:** AEON Specification v1
**Status:** informative summary for consolidated v1

Canonical topic owners: `../value-types-v1.md`, `../structure-syntax-v1.md`, `../addressing-references-v1.md`

If this appendix conflicts with the canonical v1 references, the canonical v1 references win.

This appendix defines the tuple/list structural distinction, grammar surface, indexed canonical paths, AES emission, and the Core-versus-validation authority boundary.

> **Gating:** Features in this appendix are part of the consolidated v1 language line unless explicitly profile-gated.

---

## 1. Design Goals

This chapter:
- Separates list and tuple shapes in syntax and AES value kinds
- Uses indexed canonical paths for positional addressing
- Keeps validation authority outside AEON Core
- Preserves deterministic parse/print/resolution behavior

---

## 2. Terminology

| Surface Syntax | AES/AST Value Kind | Type Constructor | Semantics                  |
| -------------- | ------------------ | ---------------- | -------------------------- |
| `[...]`        | `ListNode`         | `list<T>`        | Homogeneous-element intent |
| `(...)`        | `TupleLiteral`     | `tuple<T1..TN>`  | Positional/arity intent    |

AEON uses "list" and "tuple" terminology, not "array".

---

## 3. Grammar Surface

### 3.1 Value Production

```ebnf
Value = Literal | Reference | Object | List | Tuple ;
TypedValue = TypeAnnotation "=" Value ;

List  = AttributeList? "[" ListBody? "]" ;
Tuple = AttributeList? "(" TupleBody? ")" ;

ListBody  = ( (Value | TypedValue) ListSeparator? )* ;
TupleBody = ( (Value | TypedValue) ListSeparator? )* ;

ListSeparator = "," | Newline ;
```

### 3.2 `()` Interpretation

- `()` is always a `TupleLiteral`
- There is no grouping-parentheses syntax in AEON Core
- An empty `()` is an empty tuple

### 3.3 Generic Type Annotation

```ebnf
TypeAnnotation = ":" TypeRef SeparatorSpec? ;

TypeRef = TypeIdent GenericArgs? ( "." TypeIdent GenericArgs? )* ;

GenericArgs = "<" Ws? TypeRef ( Ws? "," Ws? TypeRef )* Ws? ">" ;
```

Examples:

```aeon
items:list<string> = ["a", "b"]
point:tuple<int32,int32> = (10, 20)
score:tuple<string,int32> = ("alice", 95)
values:list = [:int32 = 3, :string = "4"]
pair:tuple = (:float64 = 10.5, :float64 = 2.0)
```

---

## 4. `<` Disambiguation

| Context                              | `<` Meaning          |
| ------------------------------------ | -------------------- |
| TypeContext (after `:`)              | Begins `GenericArgs` |
| ValueContext with `< Identifier "("` | Node introducer form |
| Other ValueContext                   | Currently invalid    |

Whitespace is not semantically significant for this disambiguation.

---

## 5. Indexed Canonical Paths

Tuples and lists use indexed segments in canonical paths:

```
$.a[0]      // first element of a
$.a[1][2]   // third element of second element of a
$.a[0]@meta // attribute on first element
```

Index segment model aligns with the addressing appendix (`member / index` identity segments with attribute selectors in addressing expressions).

Canonicalization constraints (same as addressing rules):
- Zero-based
- Decimal digits only
- No sign prefix
- No leading zeros unless index is `0`
- Malformed index forms produce diagnostic `invalid_index_format`

---

## 6. AES Emission

AEON Core emits distinct value kinds for the two sequence forms:

| Source Form | Emitted Kind               |
| ----------- | -------------------------- |
| `[...]`     | `ListNode(elements[])`     |
| `(...)`     | `TupleLiteral(elements[])` |

Spans and source-order determinism remain unchanged from the baseline AES model.

Assignment Events for sequence elements:
- Each element of a list/tuple is addressable via its indexed canonical path
- Elements emit as nested Assignment Events under the container's path

---

## 7. Reference Behavior with Indexed Targets

Reference grammar supports indexed segments in path references:

```ebnf
Reference = "~" Path | "~>" Path ;
Path = Root? Segment+ | Root ;
Segment = MemberSegment | IndexSegment | AttrSegment ;
```

Example:

```aeon
items  = (10, 20, 30)
second = ~items[1]     // clone of second tuple element (value: 20)
```

Reference visibility and no-forward rules remain governed by the addressing model.

---

## 8. Type Constructor Intent

### `list<T>`

- Exactly one type argument
- Indicates homogeneous-element intent
- Example: `list<string>`, `list<int32>`

### `tuple<T1..TN>`

- One or more type arguments
- Indicates positional/arity intent
- Example: `tuple<string,int32>`, `tuple<int32,int32,float64>`

### Core Parsing Role

AEON Core:
- Parses these forms syntactically
- Preserves `ListNode` / `TupleLiteral` shape in AST/AES

AEON Core does NOT enforce:
- Tuple arity conformance
- Per-position type conformance
- List element homogeneity

---

## 9. Validation Authority Boundary

Structural tuple validation belongs to schema/profile stages, not AEON Core.

| Layer         | Responsibility                                                     |
| ------------- | ------------------------------------------------------------------ |
| AEON Core     | Parse syntax, emit `ListNode`/`TupleLiteral`, assign indexed paths |
| AEOS          | Enforce arity via `LENGTH_EXACT`                                   |
|               | enforce per-position types via indexed-path `TYPE_IS`              |
| Profile/Tonic | Semantic interpretation, materialization                           |

Type hint annotations (`:tuple<string,int32>`) on a binding do NOT automatically enforce arity or per-position type constraints. Schema rules must explicitly declare them.

---

## 10. Compatibility and Gating

Tuple/generic/indexed-path behavior is part of the consolidated v1 baseline.

In v1:
- `(...)` tuple syntax is valid
- Generic `<...>` type arguments are valid
- Indexed reference paths are valid

---

## 11. Implementation Touchpoints

- Parser: tuple literal production, generic type surface
- Path parser/printer: index segments
- Reference resolver: indexed targets
- AES emitter: `TupleLiteral` value kind, element sub-events
- Diagnostics: `invalid_index_format`, generic arity mismatch
- Validator/path matcher: indexed path matching
- CTS fixtures: golden AES outputs for tuple/list inputs

---

## 12. Open Items

- Finalize grammar production names and chapter-level EBNF style for publication
- Confirm final diagnostics set for generic arity and index format errors
- Decide if any ValueContext `<` forms beyond node syntax are needed later

---

## 13. Related v1 Sections

- `specs/04-official/v1/AEON-spec-v1.md` (tuple/index path grammar and conformance)
- `specs/04-official/v1/AEOS-spec-v1.md` (validator-facing tuple/index constraints)
- `specs/04-official/v1/appendices/appendix-aes.md` (event model implications for tuple/list)
- `specs/04-official/v1/appendices/appendix-addressing.md` (indexed canonical path rendering)
