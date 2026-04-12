---
id: appendix-canonical-form-v1
title: Appendix - Canonical AEON Form
description: Canonicalization conventions and normalization outputs for stable interchange.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-canonical-form-v1
---

# Canonical AEON Form — Appendix

**Appendix to:** AEON Specification v1

---

## Overview

Canonical AEON defines a deterministic textual representation suitable for hashing, diffing, signing, and reproducible builds.

Canonical form is **optional** for parsing but REQUIRED for canonical emitters.

---

## Document Structure

### Header

If no header exists, emit the default:

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "transport"
  profile = "core"
  version = 1.0
}
```

Header fields sorted lexicographically.

### Top-Level Order

1. `aeon:header` first
2. All other bindings in lexicographic order

This ordering is not formatter-only advice:
- a structured header appearing after any body binding is invalid input;
- canonicalization MUST reject such input rather than reordering it into a valid document.

---

## Keys and Objects

- Object keys sorted lexicographically
- Attribute keys sorted lexicographically
- One key per line in multi-line objects

Canonical layout is structure-sensitive:

- inline object forms may remain inline when the enclosing canonical layout is inline;
- when an enclosing object or list is rendered as multiline canonical layout, nested object values also canonically expand to multiline object blocks rather than remaining inline;
- key sorting still applies at every level regardless of whether the object is rendered inline or multiline.

---

## Lists

- Element order preserved (never reordered)
- Single-line for simple scalars, multi-line for complex values

When a list is rendered multiline, complex object elements canonically expand to multiline object blocks.

---

## Scalars

### Numbers

- Canonicalization of `:n` values is value-normalizing while preserving the
  broad representation family chosen by the author:
  - integer family
  - decimal family
  - exponent family
- Remove all `_` separators
- No leading `+` sign
- Leading-dot decimals gain an explicit zero (`.5` → `0.5`)
- Decimal-family values trim redundant trailing fractional zeroes, but retain at
  least one fractional digit (`10.00` → `10.0`)
- Exponent-family values use lowercase `e`
- Exponent-family values remove redundant exponent sign and leading exponent
  zeroes (`1.0E+03` → `1e3`)
- Zero follows the same family model rather than a special ad hoc rule:
  - integer zero → `0` or `-0`
  - decimal zero → `0.0` or `-0.0`
  - exponent zero → `0e0` or `-0e0`

```aeon
// Non-canonical → Canonical
1_000_000   → 1000000
1.2300      → 1.23
.10         → 0.10
.5          → 0.5
1.0E+03     → 1e3
10.00       → 10.0
0.0e+0      → 0e0
```

### Radix

- Canonicalization of `:radix[...]` values remains representation-preserving
  rather than value-normalizing
- `_` separators are removed from the canonical payload
- the remaining digit sequence, decimal point placement, and leading zero width
  are otherwise preserved

```aeon
// Non-canonical → Canonical
%10_00      → %1000
%10.00      → %10.00
%0010.00    → %0010.00
```

### Booleans

Always `true` or `false` (lowercase).

### Switch

Preserve original literal (`yes`, `on`, etc.).

### Base Literals

- Hex: lowercase (`#ff00aa`)
- Remove `_` separators

### Strings

- Always double quotes (`"`)
- Minimal escaping
- Raw line breaks → `\n`
- Non-ASCII preserved as UTF-8

Multiline semantic strings canonically emit as spaces-only trimticks:

- canonical output never uses tabs in the trimtick gutter
- canonical equality is determined by the resulting trimmed string value
- single-line strings continue to emit as ordinary quoted strings
- trimticks may collapse to ordinary quoted strings in inline canonical contexts
- one-line normalized trimticks in inline containers emit as ordinary quoted strings
- multiline trimticks rendered inside inline object or attribute forms emit as escaped quoted strings rather than multiline trimtick blocks

### Separator Literals

Canonical separator literals:

- No whitespace between `=` and `^`
- No raw whitespace outside quoted segments
- Raw segments are emitted verbatim
- Quoted segments use canonical quoted-string escaping

```aeon
// Non-canonical → Canonical
size:sep[x] =^300x250   → size:sep[x] = ^300x250
```

Quoted segments preserve their string content:
```aeon
data:sep[|] = ^"one "|" two"   // preserved as-is
```

---

## References

References MUST preserve semantic intent:

- clone references remain clone references (`~...`)
- pointer references remain pointer references (`~>...`)

Canonical form MUST NOT:
- Change a clone-intent reference into a pointer-intent reference or vice versa
- Inline or resolve references
- Alter the logical value graph

Canonical reference rendering also applies these normalizations:
- explicit root prefixes are elided when redundant (`~$.a` → `~a`, `~>$.a` → `~>a`)
- quoted member or attribute selectors may collapse to bare identifier form when the decoded segment is already a canonical bare identifier (`~a@["meta"]` → `~a@meta`)

## Node Heads

Canonical node-head ordering is:
- `tag@{...}:datatype`

Canonical form preserves this order for node heads in the same way it preserves `key@{...}:type` ordering for bindings.

---

## Whitespace

- 2-space indentation (no tabs)
- One space around `=`
- LF line endings (`\n`)
- Opening brace on same line as binding
- Closing brace on own line

```aeon
user = {
  name = "Patrik"
  age = 49
}
```

---

## Non-Goals

Canonical form does NOT:
- Alter the logical value graph
- Inline references
- Change types
- Add or remove bindings (except default header)

---

*End of Canonical Form Appendix*
