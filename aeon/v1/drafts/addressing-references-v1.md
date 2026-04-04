---
id: aeon-core-v1-addressing-references
title: AEON v1 Addressing and References Reference
description: Reference for canonical paths, quoted segments, attribute selectors, reference forms, and reference legality in AEON Core v1.
group: Core References
path: specification/aeon-v1-documentation/aeon-v1-addressing-and-references-reference
links:
  - aeon-core-v1
  - aeon-core-v1-structure-syntax
  - aeon-core-v1-comments-annotations
---

# AEON v1 Addressing and References Reference

Status: official v1 companion reference  
Scope: canonical paths, reference forms, quoted segments, attribute selectors, and reference legality.

## 1. Canonical Path Model

Canonical path identity in AEON v1 uses only:
- member segments
- index segments

Examples:

```aeon
$.user
$.user.name
$.items[0]
$.["a.b"]
```

Identity rules:
- `a.b` means two member segments;
- `["a.b"]` means one member key that contains a dot;
- attribute selectors are valid in addressing expressions, but are not canonical path identity segments.

Authoritative grammar sketch:

```ebnf
CanonicalPath = "$" RootPathMember* ;
RootPathMember = "." BareKey | ".[" QuotedKey "]" | "[" Number "]" ;
PathMember = "." BareKey | ".[" QuotedKey "]" | "[" Number "]" ;
```

Canonical notes:
- non-bare keys are rendered in double-quoted bracket form;
- lists and tuples use numeric index segments;
- canonical path identity is deterministic across equivalent quoted spellings.
- quoted root-member traversal uses the explicit dot form `$.["..."]`;
- bare root-bracket member traversal such as `$["a"]` is not part of the Core v1 path grammar.

## 2. Key Segment Forms

### 2.1 Member Traversal

Bare member traversal:

```aeon
$.user.name
~user.name
```

Quoted member traversal:

```aeon
$.["user name"]
$.["a.b"]
~["a.b"]
~a.["b.c"]
```

Nuances:
- `~a.b` resolves member `a`, then member `b`;
- `~["a.b"]` resolves a single key literally named `a.b`;
- `~a.["b.c"]` resolves member `a`, then a quoted member literally named `b.c`;
- `~$.["a.b"]` is the explicit root-prefixed quoted-member form;
- `~$["a.b"]` is not part of the Core v1 reference grammar;
- quoted segment decoding occurs before identity comparison.

### 2.2 Indexed Traversal

List/tuple addressing:

```aeon
$.items[0]
~items[1]
```

Nuances:
- index segments are positional and zero-based;
- index segments participate in canonical path identity;
- index segments may be followed by member traversal or attribute selectors.

## 3. Attribute Selectors

Attributes live in a distinct namespace from data members.

Attribute selector forms:

```aeon
$.user@role
$.user@["profile.name"]
$.user@["profile.name"].["display.name"]
~user@role
~user@["profile.name"]
~user@meta.["x.y"]
```

Grammar sketch:

```ebnf
RefPath = RefStart RefSegment* ;
RefStart = BareKey | QuotedMember | "$" ;
RefSegment = MemberSegment | IndexSegment | AttributeSegment ;
AttributeSegment = "@" BareKey | "@[" QuotedKey "]" ;
```

Nuances:
- `@key` addresses a bare attribute key;
- `@["key with spaces"]` addresses a quoted attribute key;
- quoted member and attribute-key segments must not be empty;
- quoted bracket member segments may follow attribute selectors using `.[\"...\"]`;
- quoted attribute selectors may be followed by ordinary member traversal, quoted member traversal, or index traversal;
- mixed traversal such as `~a@["x.y"].z`, `~a@meta.["x.y"]`, and `~$.a@["profile.name"][0]` is valid when each traversed segment exists and is otherwise legal;
- malformed or incomplete forms such as `~a@`, `~$.a@[`, and `~.["a"]` are invalid;
- attribute selectors are part of reference/addressing syntax, not canonical path identity;
- data namespace and attribute namespace are distinct and must not be merged.

## 4. Reference Forms

AEON v1 supports:
- clone/reference form: `~path`
- alias/pointer form: `~>path`

Examples:

```aeon
a = 1
b = ~a
c = ~$.a
d = ~["a.b"]
e = ~>a
f = ~user@role
```

Nuances:
- `~path` references the target value;
- `~>path` preserves alias/pointer intent in the AST/AES model;
- both forms use the same path grammar after the introducer.

AES notes:
- clone and alias remain distinct value kinds;
- path text is preserved structurally rather than flattened to one raw string.

## 5. Disambiguation Rules

### 5.1 Dot vs Quoted Key

```aeon
a = { b = 1 }
"a.b" = 2
```

Then:

```aeon
~a        // object { b = 1 }
~a.b      // 1
~["a.b"]  // 2
$.a.b     // canonical path to nested member
$.["a.b"] // canonical path to quoted single key
```

### 5.2 Attribute vs Data Namespace

```aeon
user@{role="admin"} = 1
a = [{x@{b=0}=1}]
```

Then:

```aeon
~user        // data binding value
~user@role   // attribute namespace value
~a[0].x@b    // nested binding attribute inside container
~a@meta.["x.y"] // quoted member traversal after attribute selection
```

These are not the same target.

Attachment-scope note:
- attributes attach to bindings (or node heads), not to already-completed literal values;
- binding-attached attributes remain addressable wherever the binding itself is addressable;
- therefore `a@{b=1} = [0]` exposes `$.a@b`, and `a = [{x@{b=0}=1}]` exposes `$.a[0].x@b`;
- postfix literal forms such as `a = [0]@{b=2}` are invalid Core v1 syntax.

## 6. Reference Legality

Reference legality is deterministic in Core v1.

Invalid:
- forward references
- missing targets
- self-references

Examples:

```aeon
b = ~a
a = 1
```

```aeon
a = ~missing
```

```aeon
a = ~a
```

Nuances:
- no-forward and no-self checks apply independently per namespace;
- explicit attribute references use the same legality model;
- quoted member traversal after attribute selection does not change legality rules; it continues to resolve against the selected attribute value using ordinary member/index traversal;
- legality is a Core concern, not AEOS/schema responsibility.

## 7. Duplicate Identity and Decoding

Quoted spellings are decoded before identity comparison.

Implications:
- duplicate-key checks use decoded identity;
- duplicate canonical-path checks also use decoded identity;
- escaped equivalents must not create distinct addresses.

Example:

```aeon
"a\"b" = 1
'a"b' = 2
```

These resolve to the same decoded key identity and should conflict.

## 8. Canonical Rendering Notes

Canonical output conventions:
- root marker is `$`;
- bare member segments use `.name`;
- non-bare members use `["..."]`;
- attribute selectors use `@name` or `@["..."]`;
- numeric indices use `[n]`.

Examples:

```aeon
$.contacts[3].email
$.["a.b"]
$.user@meta
$.user@["profile.name"]
$.user@["profile.name"].["display.name"]
$.a@meta.["x.y"]
```

## 9. Node Model Boundary

Node children do not receive canonical paths in the current v1 node model.

Implications:
- the binding that owns the node has a canonical path;
- node child ordering is structural, not canonical-path addressed;
- addressing/reference syntax applies to bindings, list/tuple elements, and attribute selectors, not arbitrary node children.

## 10. Minimum Conformance Reminders

Implementations targeting Core v1 must at minimum:
- support quoted member segments in paths;
- support quoted attribute segments in paths;
- preserve dot-vs-quoted-key disambiguation;
- reject forward references deterministically;
- reject missing targets deterministically;
- reject self-references deterministically;
- report canonical paths consistently in diagnostics and emitted events.
