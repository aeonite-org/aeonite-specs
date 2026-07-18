---
id: sansa-v1-addressing
title: SANSA v1 Addressing
description: Proposal-stage address model and selector vocabulary for SANSA.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/addressing
license: CC-BY-4.0
links:
  - sansa-v1-resolve
  - sansa-v1-query
---

# SANSA v1 Addressing

Status: Proposal  
Scope: structural address model and selector vocabulary for SANSA v1.

## 1. Overview

SANSA addressing defines a deterministic notation for identifying semantic bindings in a semantic address namespace.

An address describes structure. It does not, by itself, require traversal, execution, mutation, authorization, or value evaluation. Those responsibilities belong to a resolving consumer, SANSA.Resolve, SANSA.Query, or another capability layered above the address model.

## 2. Terms

A **namespace** is the addressable semantic structure exposed by a SANSA implementation.

A **binding** is an addressable semantic unit exposed by a namespace.

A **Binding Set** is an ordered collection of bindings.

A **selector** is one navigation or filtering operation in an address expression.

A **canonical address** is an exact address that identifies at most one binding in a namespace.

An **address expression** may identify zero, one, or many bindings when resolved. It may contain expansion, filter, pattern, or local address-space selectors.

## 3. Lexical Model

SANSA address expressions use a small ASCII structural grammar outside quoted payloads.

Whitespace is not permitted outside quoted payloads.

Bare identifiers use:

```ebnf
Identifier = [A-Za-z_] [A-Za-z0-9_]* ;
```

Position indexes use unsigned decimal notation without leading zeroes:

```ebnf
Index = "0" | [1-9] [0-9]* ;
```

Quoted member names, local address-space names, name patterns, and quoted qualifier arguments use AEON double-quoted string payload rules. This allows characters that are not part of the bare ASCII selector grammar to be carried without making address parsing context-sensitive.

### 3.1 Qualified Address Literals

A qualified address literal is an address expression followed by an optional qualifier expression.

```ebnf
QualifiedAddressLiteral
    = AddressExpression [ ":" QualifierExpression ] ;

QualifierExpression
    = QualifierTerm ( "|" QualifierTerm )* ;

QualifierTerm
    = QualifierTypeName
      QualifierParameterGroup*
      QualifierArgumentGroup* ;

QualifierTypeName
    = Identifier ;

QualifierParameterGroup
    = "<" QualifierTypeParameter
      ( "," QualifierTypeParameter )*
      ">" ;

QualifierTypeParameter
    = QualifierTerm ;

QualifierArgumentGroup
    = "[" QualifierArgument "]" ;

QualifierArgument
    = QualifierArgumentToken
    | DoubleQuotedPayload ;

QualifierArgumentToken
    = QualifierArgumentChar+ ;

QualifierArgumentChar
    = one character from A-Za-z0-9!#$%&*+-.:;=?@^_|~<> ;
```

SANSA owns this qualifier grammar. Host implementations define the accepted qualifier surface.

SANSA Addressing assigns no semantics to qualifier expressions. Host implementations validate the syntax and qualifier surface they support, preserve accepted qualifier structure, and may reject qualifier forms they do not understand. Consumers decide whether to interpret, ignore, or reject accepted qualifiers.

Examples:

```text
$.result:number|nan
$.inventory:list<string>
$.inventory:csv[","]
$.path:tuple<x><y>
$.value:type<type>[arg]
```

The `|` operator is only valid at the top level of a qualifier expression. Nested qualifier unions are not valid in SANSA v1:

```text
$.value:list<string|number>
```

Qualifier parameter groups are repeatable. This permits embeddings that avoid raw comma syntax in contexts where comma has host-language meaning:

```text
$.path:tuple<x><y>
```

SANSA also permits comma-separated parameters inside one parameter group:

```text
$.path:tuple<x,y>
```

Host implementations may prefer or require the repeated-group form if that better fits their parser.

Qualifier argument groups are repeatable:

```text
$.key:string[","]["."]
```

Unquoted arguments intentionally form a simple lexical token. Raw comma is excluded from unquoted arguments. More complex payloads use quoted-string syntax:

```text
$.inventory:csv[","]
$.field:separator["::"]
$.line:terminator["\r\n"]
```

These examples are syntactically valid SANSA. A host implementation may still reject them if they are outside the qualifier surface it accepts.

### 3.2 AST Shape

Parsers should expose qualifier structure rather than treating it only as an opaque string.

```text
QualifiedAddress
  address
  qualifierExpression?

QualifierExpression
  terms[]

QualifierTerm
  typeName
  parameterGroups[]
  argumentGroups[]
```

Implementations may also expose flattened convenience views, but repeated parameter and argument groups must remain recoverable from the parse tree.

## 4. Address Roots

### 4.1 Absolute Root

The absolute root is written:

```text
$
```

It means:

> Begin from the primary root supplied by the resolving consumer.

Examples:

```text
$.contact.name
$.contacts[0]
$.message.@.id
```

### 4.2 Contextual Root

The contextual root is written:

```text
?
```

It means:

> Begin from the contextual root supplied by the resolving consumer.

Examples:

```text
?.name
?.address.city
?.items[0]
```

Contextual-root expressions are structurally valid without a context, but they cannot be resolved unless the consumer supplies one.

### 4.3 Relative Selector Fragments

Some consumers, including SANSA.Query, allow selector fragments that begin with a selector rather than a root:

```text
.name
.roles.*
.@.metadata
```

Such fragments are not complete absolute addresses. Their starting point is supplied by the consuming capability.

## 5. Exact Selectors

Exact selectors preserve a path that can identify at most one binding.

### 5.1 Named Binding

```text
.name
```

Selects a direct named child binding.

Names that cannot be written safely in bare form use a quoted member segment:

```text
.["member.with.dots"]
.["spaced name"]
```

### 5.2 Positional Binding

```text
[0]
[12]
```

Selects the binding at the specified zero-based position in the ordered sequence exposed by the current binding.

Positional syntax is representation independent. It does not itself distinguish lists, tuples, nodes, or implementation-specific ordered structures.

Chained positional selectors are syntactically valid:

```text
$.matrix[2][2]
```

Whether an intermediate binding is indexable is a resolution or schema question, not a lexical-addressing question.

### 5.3 Attribute Address Space

```text
.@
```

Enters the attribute address space of the current binding.

Once inside the attribute address space, ordinary SANSA navigation applies.

Examples:

```text
$.message.@.id
$.message.@.properties.caller.@.by
```

Compact forms such as `$.message@id` are not valid SANSA v1 address syntax. Attribute-space traversal uses the explicit `.@.` segment so attributes remain unambiguous from ordinary member names.

### 5.4 Local Address Space

```text
.<"namespace">
```

Enters a named local address space at the current resolution point.

Examples:

```text
$.document.<"sections">.introduction
$.page.<"html-id">.navigation
$.<"params">.username
$.<"session">.user_id
```

A local address-space segment identifies an address-space transition, not an ordinary child binding. Therefore these two addresses are not equivalent:

```text
$.document.contact
$.document.<"contact">
```

The first selects an ordinary child named `contact`. The second enters a local address space named `contact`.

## 6. Expanded Selectors

Expanded selectors may produce zero or more bindings.

### 6.1 Direct Expansion

```text
.*
```

Expands all direct child bindings of the current binding.

### 6.2 Descendant Expansion

```text
.**
```

Expands descendants reachable through the ordinary value hierarchy. The current binding is not included.

Attribute address spaces and local address spaces are not traversed implicitly. They require explicit selectors.

### 6.3 Name Pattern Selector

```text
.("id-*")
.("*-id")
.("*id*")
.("item-??")
```

Name patterns match complete binding names.

| Operator | Meaning |
| --- | --- |
| `*` | zero or more characters |
| `?` | exactly one character |

The underscore character `_` has no wildcard meaning in name patterns; it is matched as an ordinary name character.

Regular expressions are intentionally excluded from SANSA v1 addressing.

## 7. Filter Selectors

Filter selectors filter the current Binding Set. They do not evaluate values.

### 7.1 Semantic Type Filter

```text
#type
```

Filters by semantic datatype identity.

Example:

```text
$.content.*#text
```

### 7.2 Representation Kind Filter

```text
%kind
```

Filters by representation kind.

Example:

```text
$.content.*%stringLiteral
```

Semantic datatype and representation kind are distinct.

```aeon
content = {
  a:text = "I am text"
  b:string = "I am string"
}
```

The expression `$.content.*#text` selects only `a`. The expression `$.content.*%stringLiteral` selects both `a` and `b`.

## 8. Canonical Addresses

Canonical addresses identify at most one binding.

Examples:

```text
$
$.member
$.["member.with.dots"]
$.list[0]
$.message.@.id
$.message.@.properties.caller.@.by
```

Expanded address expressions are not canonical addresses, even though each binding produced by such an expression has its own canonical address.

Examples of non-canonical address expressions:

```text
$.users.*
$.content.*#text
$.content.("id-*")
$.**
```

Qualified address literals have a canonical address component and a qualifier component. Canonical rendering preserves repeated qualifier parameter and argument group boundaries.

## 9. Local Address-Space Boundaries

Local address spaces are isolated scopes.

A local address space may only be entered through an explicit local address-space selector:

```text
.<"namespace">
```

There is no fallback between primary and local address spaces. A reference to `$.<"params">.username` must not fall back to `$.params.username`.

Traversal must not cross a local address-space boundary implicitly. SANSA v1 defines no parent selector that can leave a local address space.

Local address spaces exist only when explicitly exposed or mounted by the resolving consumer, environment, or addressed resource. A syntactically valid local address-space selector does not imply authorization to resolve that space.

## 10. Opaque Local Semantics

SANSA standardizes the transition into a named local address space. It does not standardize the internal meaning of every local namespace.

Examples of possible local address spaces include:

- query parameters
- session data
- request data
- sections exposed by an embedded document processor
- HTML identifiers exposed by an HTML processor
- named destinations exposed by a PDF processor
- application-defined resource views

The provider of a local address space owns its internal semantics, subject to SANSA resolution rules and consumer policy.

## 11. Superseded Anchor Form

Earlier design notes explored postfix anchor selectors such as:

```text
$.document<"contact">
```

SANSA v1 proposals prefer the local address-space segment:

```text
$.document.<"contact">
```

The local address-space form makes the transition explicit as a selector and allows additional navigation within the local space.

## 12. Relationship to AEON Literals

The SANSA address model is independent of AEON Core syntax. AEON may define a native SANSA address literal based on this grammar.

When used as an AEON literal, a SANSA address remains declarative. AEON Core is expected to validate structural syntax and transport the value, not resolve the address or evaluate query semantics.

AEON is one host implementation of SANSA address literals. It may restrict the qualifier surface it accepts while still using the broader SANSA grammar as the address-language foundation.

## 13. Parser Requirements

Conforming SANSA Address parsers must reject:

- whitespace outside quoted payloads
- invalid bare identifiers
- empty quoted member names
- empty local address-space names
- position indexes with leading zeroes
- invalid quoted payload escapes
- unterminated or malformed qualifier syntax
- empty qualifier parameter or argument groups
- nested qualifier unions

Parsers must not assign semantic meaning to qualifier terms as part of address parsing. Semantic interpretation belongs to the host implementation or consuming capability.
