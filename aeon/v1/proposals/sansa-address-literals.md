---
id: aeon-v1-sansa-address-literals
title: AEON SANSA Address Literals
description: "Proposal for embedding SANSA address literals in AEON values."
status: proposal
family: official-v1
group: Proposals
license: CC-BY-4.0
path: specification/aeon-v1-documentation/proposals/sansa-address-literals
links:
  - aeon-core-v1-value-types
  - sansa-v1-addressing
---
# Proposal: AEON SANSA Address Literals

Status: proposal

## Purpose

AEON may embed SANSA address literals as ordinary values.

```aeon
address:sansa = $.inventory.items[2].sku
context:sansa = ?.name
```

The `$` and `?` prefixes are available for SANSA because encoding-family literals use `&`. `$` denotes an absolute SANSA root. `?` denotes a contextual SANSA root.

AEON parses and preserves the SANSA address literal. AEON Core does not resolve the address, traverse the target namespace, evaluate selectors, or assign semantic meaning to qualifiers.

SANSA is namespace- and domain-neutral. An AEON document may carry SANSA address literals for AEON-backed namespaces or for other SANSA-compatible domains. The address syntax does not by itself say that member selectors are AEON binding keys, object keys, graph terms, database fields, service resources, filesystem nodes, or runtime object properties.

SANSA member selectors describe semantic traversal rather than object traversal. AEON-backed consumers may map that traversal to the AEON binding model and canonical paths, but that mapping is an AEON namespace adapter concern rather than a SANSA grammar rule.

## Boundary

SANSA defines the address grammar. AEON Core accepts the embedded value when it is a syntactically valid SANSA address literal.

AEON-internal consumers may define narrower interpretation surfaces when they resolve, validate, or act on an address. Those restrictions are consumer semantics, not Core parse restrictions.

For example, an AEON-backed consumer may resolve this against AEON bindings and canonical paths:

```aeon
aeonPath:sansa = $.inventory.items[2].sku
```

Another consumer may treat the same SANSA grammar as an address language over an RDF-like semantic graph:

```aeon
rdfLike:sansa = $.["john"].isLocatedAt.["Brussels"]
```

Both are valid SANSA address literals when they satisfy the address grammar. Only the resolving consumer decides which namespace, profile, and authorization rules apply.

## Value Shape

A SANSA address literal begins with `$` or `?` and is parsed according to the SANSA Addressing proposal.

```aeon
root:sansa = $
context:sansa = ?
member:sansa = $.member
context_member:sansa = ?.member
quoted:sansa = $.["member.with.dots"]
indexed:sansa = $.matrix[2][2]
attribute:sansa = $.message.@.id
local:sansa = $.document.<"sections">.intro
rich:sansa = $.items.*#text%stringLiteral.("item?*")
rdfLike:sansa = $.["john"].isLocatedAt.["Brussels"]
```

The `sansa` datatype annotation is the reserved AEON datatype for SANSA address literal values. Strict mode requires SANSA address literal values to carry `:sansa`. The literal prefix remains the syntactic indicator; transport-oriented profiles may preserve untyped SANSA literals only when that profile explicitly allows them.

## Qualified Literals

AEON accepts qualified SANSA address literals when they are syntactically valid SANSA.

```aeon
result:sansa = $.result:number|nan
items:sansa = $.inventory:list<string>
point:sansa = $.path:tuple<x><y>
field:sansa = $.field:sep[.]
bits:sansa = $.bits:radix[16]
csv:sansa = $.inventory:csv[","]
external:sansa = $.value:type<type>[arg]
```

Qualifier terms are parsed by SANSA. AEON Core preserves the parsed qualifier structure and assigns no meaning to the qualifier.

Some qualifier forms may not have AEON datatype-expression counterparts:

```aeon
external:sansa = $.value:type<type>[arg]
```

That does not make them invalid AEON values. It only means AEON-internal consumers should not assume they can interpret the qualifier as an AEON datatype expression.

Repeated type-parameter groups avoid raw comma in AEON value contexts:

```aeon
point:sansa = $.path:tuple<x><y>
```

AEON can still define internal meanings for the qualifier terms it standardizes. For example, an AEON consumer may understand:

```aeon
field:sansa = $.field:sep[.]
hex:sansa = $.bits:radix[16]
```

The same AEON document may also carry addresses for another system:

```aeon
csv:sansa = $.inventory:csv[","]
```

Consumers decide whether to interpret, ignore, or reject qualifier meanings at use time.

## Parser Responsibility

An AEON parser that implements this proposal should:

- parse the address literal using the SANSA address parser
- preserve the parsed address structure
- expose the canonical SANSA rendering
- reject SANSA syntax errors as AEON syntax errors
- treat `sansa` as a reserved datatype whose value class is `SansaAddressLiteral`
- leave address resolution and qualifier interpretation to consumers

## Open Questions

- Should AEON expose qualifier terms as parsed structure in public AST contracts, or only through the embedded SANSA address object?
- Which AEON-internal consumers should define restricted qualifier interpretation surfaces?
