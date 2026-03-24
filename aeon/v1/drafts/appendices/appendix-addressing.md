---
id: appendix-addressing-v1
title: Appendix - Addressing
description: Detailed path addressing examples and canonical segment traversal clarifications.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-addressing-v1
---

# Appendix — Addressing

Status: informative summary for consolidated v1

Canonical topic owner: `../addressing-references-v1.md`

If this appendix conflicts with the canonical addressing reference, the canonical addressing reference wins.

## 1. Canonical Path Rendering

Member segments:

- bare: `$.a.b`
- quoted: `$.["a.b"]`

Address-expression attribute selectors:

- bare: `$.a@meta`
- quoted: `$.a@["profile.name"]`

Mixed address-expression examples:

- `$.["key"]@["a"].["b"]`
- `$.["array key"][2]`

Disambiguation examples:

- `a = { b = 1 }` -> `$.a` and `~a` resolve the object; `$.a.b` and `~a.b` resolve `1`.
- `"a.b" = 2` -> `$.["a.b"]` and `~["a.b"]` resolve `2` (single quoted member key, not traversal).

## 2. Attribute Segment Rule

- Bare attribute segment syntax is `@key`.
- Quoted-key attribute segment syntax is `@["key with spaces"]`.
- Attribute selectors participate in addressing expressions, not canonical path identity.

## 3. Decoding and Equivalence

- Quoted keys are decoded before identity/comparison.
- Duplicate-key and duplicate-path checks operate on decoded key values.
- Canonical path output uses double-quoted bracket form for non-bare keys.
- Equivalent escaped spellings resolve to the same decoded key identity.

## 4. Normalized Wildcard Path (Derived)

Implementations may expose a derived normalized path string for wildcard dispatch ergonomics:

- canonical (authoritative): `$.contacts[3].email`
- normalized (derived): `contacts[*].email`

Normalization rules:

1. Drop root marker.
2. Keep member names unchanged.
3. Replace numeric index segments with `[*]`.
4. Preserve member traversal dots.

Normalized path is non-authoritative convenience metadata only.

## 5. Namespace Neutrality

- No dedicated namespace syntax exists in AEON core.
- `#` has no intrinsic namespace semantics in core addressing.
- `@ns` is not reserved.
- Recommended ecosystem convention: `@{ns="namespace.v1"}` metadata.

## 6. Reference/Visibility Alignment

- Data and attribute namespaces remain distinct.
- Explicit attribute references are required for attribute namespace traversal.
- No-forward/self constraints apply per namespace.
