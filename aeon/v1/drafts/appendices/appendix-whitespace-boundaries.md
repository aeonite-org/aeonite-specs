---
id: appendix-whitespace-boundaries-v1
title: Appendix - Whitespace Boundaries
description: Clarifies where line breaks behave like ordinary whitespace and where compact tokens must remain contiguous.
family: appendices-v1
group: Core Syntax
path: specification/appendices/appendix-whitespace-boundaries-v1
---

# Appendix - Whitespace Boundaries

Status: informative clarification for consolidated v1

Canonical topic owner: `../structure-syntax-v1.md`

If this appendix conflicts with the canonical v1 spec set, the canonical v1 spec set wins.

## 1. Purpose

This appendix clarifies the practical reading of the Core v1 newline rules:

- between structural tokens, a line break behaves the same as ordinary inter-token whitespace;
- a line break becomes structurally significant only when the grammar consumes it as a separator;
- a line break is forbidden when it would split a compact token that must remain contiguous.

## 2. Structural-Boundary Rule

AEON parsers should treat the following two categories differently:

- inter-token whitespace at structural boundaries;
- interior characters of a single lexical token.

If a line break appears at a structural boundary, it is accepted on the same basis as an ordinary space.

If a line break appears inside a compact token, the token is broken and the form is invalid unless that token family explicitly permits embedded newlines.

## 3. Accepted Structural Examples

These examples are valid because the line breaks appear between structural tokens rather than inside a compact token body.

Datatype and generic boundaries:

```aeon
a
:
list
<
  n
>
=
[
  2
  3
]
```

Attribute and node-head boundaries:

```aeon
value
@{
  meta
  :
  n
  =
  1
}
:
node
=
<tag
@{
  role = "demo"
}
>
```

Node children:

```aeon
content = <a(
  <b(1, 2, 3)>
  [1, 2]
  (1, 2)
)>
```

## 4. Rejected Compact-Token Splits

These examples are invalid because the line break splits a token that must remain contiguous.

Separator literal payload:

```aeon
a =
^
0.0
```

Separator spec bracket:

```aeon
size:sep
[
x
]
= ^300x250
```

Bare identifier:

```aeon
hel
lo = 1
```

The same compact-token rule applies to numbers, bare identifiers, quoted keys, quoted strings, separator specs, and literal families whose lexical body is defined as contiguous in Core v1.

## 5. Reading Rule

When deciding whether a line break is valid, the first question is not "is this the same line?" but rather "is this boundary between tokens, or inside one token?"

If it is between structural tokens, the line break is ordinarily acceptable.

If it is inside one token body, it is ordinarily forbidden unless that token family explicitly defines multiline behavior.
