---
id: aeon-core-v1-addressing-references
title: AEON v1 Addressing, SANSA Literals, and References Reference
description: "Reference for AEON canonical paths, SANSA address literal adoption, reference forms, and reference legality in AEON Core v1."
family: official-v1
group: Core References
status: official v1 companion reference
license: CC-BY-4.0
path: specification/aeon-v1-documentation/aeon-v1-addressing-and-references-reference
links:
  - aeon-core-v1
  - aeon-core-v1-structure-syntax
  - aeon-core-v1-comments-annotations
---
# AEON v1 Addressing, SANSA Literals, and References Reference

Status: official v1 companion reference  
Scope: canonical AEON paths, SANSA address literal adoption, reference forms, quoted segments, attribute selectors, and reference legality.

## 0. Relationship to SANSA

SANSA means **Semantic Address NameSpace Abstraction**.

SANSA defines the broader address language used to describe paths and selectors over a semantic address namespace. AEON Core adopts SANSA address literals through the reserved `sansa` datatype, and AEON tooling may use SANSA selectors for schema rules, playground extraction, and consumer-defined lookup.

SANSA is namespace- and domain-neutral. SANSA member selectors describe semantic traversal rather than object traversal. In an AEON-backed namespace, that traversal maps to AEON bindings and canonical paths; in another namespace, the same syntax may map to graph terms, database entities, service resources, filesystem nodes, runtime objects, or another semantic model.

AEON references are related, but narrower:

- `value:sansa = $.contact.name` stores a SANSA address literal as data;
- `selector:sansa = $.inventory.items.*.sku` stores a SANSA selector as data;
- `copy = ~contact.name` is an AEON clone reference to an existing target;
- `pointer = ~>contact` is an AEON pointer reference to an existing target.

The SANSA address language can express selectors such as `*`, `**`, quoted name patterns, local address spaces, and qualified address literals. AEON reference forms do not evaluate SANSA selectors. A reference target must resolve deterministically to an already-bound AEON path under the reference legality rules in this document.

In short:

- SANSA owns the portable address and selector notation;
- AEON owns reference syntax, reference legality, and the `sansa` literal carrier;
- consumers own resolution, selector evaluation, authorization, and domain meaning beyond Core syntax.

## 1. Canonical Path Model

Canonical path identity in AEON v1 is the exact-path subset used for AES identity and reference targets. It uses only:
- member segments
- index segments

Examples:

```aeon
$.user
$.user.name
$.items[0]
$.["a.b"]
$.page[0]
$.page[0].a
$.user.@.role
```

Identity rules:
- `a.b` means two member segments;
- `["a.b"]` means one member key that contains a dot;
- attribute traversal uses the SANSA-derived `.@.` address-space transition;
- attribute selectors are valid in addressing expressions, but attribute metadata remains distinct from ordinary member identity.

Authoritative grammar sketch:

```ebnf
CanonicalPath = "$" PathSegment* ;
PathSegment = "." BareKey | ".[" QuotedKey "]" | "[" Number "]" | ".@." AttributeKey ;
AttributeKey = BareKey | "[" QuotedKey "]" ;
```

Canonical notes:
- non-bare keys are rendered in double-quoted bracket form;
- lists and tuples use numeric index segments;
- node children also use numeric index segments;
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
~"a.b"
~["a.b"]
~a.["b.c"]
```

Nuances:
- `~a.b` resolves member `a`, then member `b`;
- `~"a.b"` and `~["a.b"]` are equivalent initial-segment forms for one quoted member key literally named `a.b`;
- `~["a.b"]` resolves a single key literally named `a.b`;
- `~a.["b.c"]` resolves member `a`, then a quoted member literally named `b.c`;
- `~$.["a.b"]` is the explicit root-prefixed quoted-member form;
- `~$["a.b"]` is not part of the Core v1 reference grammar;
- quoted segment decoding occurs before identity comparison.

### 2.2 Indexed Traversal

List/tuple/node-child addressing:

```aeon
$.items[0]
~items[1]
$.page[0]
~page[0].a
```

Nuances:
- index segments are positional and zero-based;
- index segments participate in canonical path identity;
- index segments may be followed by member traversal or attribute selectors.
- node-child addressing uses the same bracket index form as list and tuple addressing.

## 3. Attribute Address Space

Attributes live in a distinct namespace from data members.

AEON v1 uses the SANSA-derived `.@.` transition to enter the attribute address space:

```aeon
$.user.@.role
$.user.@.["profile.name"]
$.user.@.["profile.name"].["display.name"]
~user.@.role
~user.@.["profile.name"]
~user.@.meta.["x.y"]
```

Grammar sketch:

```ebnf
RefPath = RefStart RefSegment* ;
RefStart = BareKey | QuotedMember | "$" ;
RefSegment = MemberSegment | IndexSegment | AttributeSegment ;
AttributeSegment = ".@." (BareKey | "[" QuotedKey "]") ;
```

Nuances:
- `.@.key` addresses a bare attribute key;
- `.@.["key with spaces"]` addresses a quoted attribute key;
- quoted member and attribute-key segments must not be empty;
- quoted bracket member segments may follow attribute selectors using `.[\"...\"]`;
- quoted attribute selectors may be followed by ordinary member traversal, quoted member traversal, or index traversal;
- mixed traversal such as `~a.@.["x.y"].z`, `~a.@.meta.["x.y"]`, and `~$.a.@.["profile.name"][0]` is valid when each traversed segment exists and is otherwise legal;
- compact forms such as `~a@role` and `$.a@role` are not valid AEON v1 reference or address spellings;
- malformed or incomplete forms such as `~a.@`, `~$.a.@.[`, and `~.["a"]` are invalid;
- attribute selectors are part of reference/addressing syntax, not canonical path identity;
- data namespace and attribute namespace are distinct and must not be merged.

## 3.1 SANSA Address Literal Values

The reserved datatype label `sansa` carries SANSA address text as an AEON value:

```aeon
path:sansa = $.contact.name
selector:sansa = $.inventory.items.*.sku
attribute:sansa = $.contact.name.@.unit
pattern:sansa = $.items.("item?*").sku
qualified:sansa = $.result:number|nan
```

For lexical purposes, a SANSA literal begins where the value begins and continues until ASCII whitespace, a comma, or a line break that closes the value in the current AEON context.

AEON Core validates and preserves the address literal form it accepts. It does not resolve the address, evaluate selectors, apply qualifiers, or prove that the address is meaningful for any particular consumer.

Host implementations may restrict the accepted SANSA qualifier surface while still allowing documents to carry syntactically valid SANSA addresses for other systems.

## 4. Reference Forms

AEON v1 supports:
- clone/reference form: `~path`
- alias/pointer form: `~>path`

Examples:

```aeon
a = 1
b = ~a
c = ~$.a
d = ~"a.b"
d2 = ~["a.b"]
e = ~>a
f = ~user.@.role
```

Nuances:
- `~path` references the target value;
- `~>path` preserves alias/pointer intent in the AST/AES model;
- ASCII inter-token whitespace may appear between `~` or `~>` and the following reference path, but canonical formatting removes it;
- both forms use the same path grammar after the introducer;
- reference paths use exact AEON target paths; SANSA selector expansion is not part of `~` or `~>` reference resolution.

AES notes:
- clone and alias remain distinct value kinds;
- path text is preserved structurally rather than flattened to one raw string.

Reference-form semantics:
- reference-form identity compares reference kind plus canonical exact target path;
- `~a` and `~$.a` identify the same clone-reference form after canonical path normalization;
- `~a` and `~>a` do not identify the same reference form because clone intent and pointer intent are distinct;
- comparing, validating, or rendering the reference form does not follow the reference.

Followed-value semantics:
- following a reference is a read-only consumer operation, conceptually `follow(reference)`;
- following walks the target path and inspects the target value without rewriting, substituting, inlining, aliasing, or erasing the original reference form;
- after following, value semantics apply to the target value;
- consumers that follow references must preserve diagnostics for both the reference source and the target path;
- following must not erase the original reference form from AES or other representation-preserving outputs.

Reference resolution:
- resolving a reference is a materialization/substitution operation, not the same operation as following;
- resolution may produce an inlined clone, an alias, an explicit runtime reference, or another consumer-defined representation according to clone/pointer policy;
- resolution belongs to Tonics, runtime materializers, storage adapters, or explicit consumer profiles, not AEON Core parsing.

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
~"a.b"    // 2
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
~user.@.role   // attribute namespace value
~a[0].x.@.b    // nested binding attribute inside container
~a.@.meta.["x.y"] // quoted member traversal after attribute selection
```

These are not the same target.

Attachment-scope note:
- attributes attach to bindings (or node heads), not to already-completed literal values;
- binding-attached attributes remain addressable wherever the binding itself is addressable;
- therefore `a@{b=1} = [0]` exposes `$.a.@.b`, and `a = [{x@{b=0}=1}]` exposes `$.a[0].x.@.b`;
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
- attribute address-space traversal uses `.@.name` or `.@.["..."]`;
- numeric indices use `[n]`.

Examples:

```aeon
$.contacts[3].email
$.["a.b"]
$.user.@.meta
$.user.@.["profile.name"]
$.user.@.["profile.name"].["display.name"]
$.a.@.meta.["x.y"]
```

## 9. Node Model Boundary

Node children use numeric index segments in canonical paths, matching the ordered child-slot model used by lists and tuples.

Implications:
- the binding that owns the node has a canonical path for the node value;
- node child ordering is structural and reflected through bracket indices such as `$.page[0]`;
- object members inside node children continue normal member traversal, for example `$.page[0].title`;
- node tags are not independent canonical path segments.

## 10. Minimum Conformance Reminders

Implementations targeting Core v1 must at minimum:
- support quoted member segments in paths;
- support quoted attribute segments in paths;
- preserve dot-vs-quoted-key disambiguation;
- reject forward references deterministically;
- reject missing targets deterministically;
- reject self-references deterministically;
- report canonical paths consistently in diagnostics and emitted events.
