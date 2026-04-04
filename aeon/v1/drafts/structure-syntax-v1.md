---
id: aeon-core-v1-structure-syntax
title: AEON v1 Structure Syntax Reference
description: Reference for binding shape, keys, attributes, separator specs, newline rules, and structural grammar decisions in AEON Core v1.
group: Core References
path: specification/aeon-v1-documentation/aeon-v1-structure-syntax-reference
links:
  - aeon-core-v1
  - aeon-core-v1-addressing-references
  - aeon-core-v1-value-types
---

# AEON v1 Structure Syntax Reference

Status: official v1 companion reference  
Scope: key syntax, attributes, separator specs, list/tuple separators, and newline behavior.

## 1. Binding Shape

Canonical binding surface:

```aeon
key@{attributes}:type = value
```

Transport form may omit attributes and datatype:

```aeon
key = value
```

Strict form requires datatype presence, but not generic arguments:

```aeon
name:string = "AEON"
items:list = ["a", "b"]
point:tuple = (1, 2)
```

Core grammar summary:

```ebnf
Binding        = Key AttributeList? TypeAnnotation? "=" Value ;
AttributeList  = Attribute* ;
Attribute      = "@{" AttributeEntryList? "}" ;
AttributeEntryList = AttributeEntry (AttributeSep AttributeEntry)* AttributeSep? ;
AttributeEntry = Key AttributeList? TypeAnnotation? "=" Value ;
AttributeSep   = "," | Newline ;
TypeAnnotation = ":" TypeName GenericArgs? SeparatorSpec* ;
SeparatorSpec  = "[" SeparatorChar "]" ;
```

Nuances:
- canonical order is `key@{...}:type = value`;
- reversed order such as `key:type@{...} = value` is not Core v1 canonical syntax;
- attributes may appear without datatype;
- datatype may appear without attributes.

## 2. Keys

### 2.1 Supported Key Forms

Valid key forms in all key positions:

```aeon
user = 1
'user name' = 2
"a.b" = 3
```

Unsupported as core keys:

```aeon
`user` = 1
```

Key grammar:

```ebnf
Key = Identifier | SingleQuotedKey | DoubleQuotedKey ;
Identifier = IdentifierStart IdentifierContinue* ;
IdentifierStart = "A".."Z" | "a".."z" | "_" ;
IdentifierContinue = IdentifierStart | "0".."9" ;
```

Nuances:
- bare keys are best used when the key is identifier-safe;
- quoted keys are required for spaces, dots-as-data, and other non-bare characters;
- single and double quotes are both valid key delimiters;
- quoted keys must not be empty;
- backtick-quoted keys are not part of AEON Core v1 key syntax.

Canonical notes:
- canonical paths render non-bare keys using bracketed double-quoted form, for example `$.["a.b"]`;
- `'a.b'` and `"a.b"` are the same key identity when parsed as keys.

AES notes:
- key form is structural and does not create a distinct value kind;
- canonical path identity uses member and index segments only.

## 3. Attributes

Attributes attach opaque metadata to a binding or node head:

```aeon
user@{role="admin", level=5} = {
  id = 1
}

content = <span@{id="text", class="dark"}("hello")
```

Grammar:

```ebnf
Attribute      = "@{" AttributeEntryList? "}" ;
AttributeEntryList = AttributeEntry (AttributeSep AttributeEntry)* AttributeSep? ;
AttributeEntry = Key AttributeList? TypeAnnotation? "=" Value ;
AttributeSep   = "," | Newline ;
```

Nuances:
- attribute entries are key/value pairs;
- attribute entry heads may themselves carry attributes;
- attribute entry datatypes are allowed;
- attribute containers may be empty: `@{}`;
- attribute entry separators may be commas or newlines;
- trailing attribute separator is accepted by current parser behavior.
- binding-attached attributes are valid on any binding head, including bindings whose values are objects, lists, tuples, or other literals;
- postfix literal attributes are not part of Core v1 syntax: `a = [0]@{b=2}` is invalid and fails closed;
- nested bindings inside container values may carry their own attributes, for example `a = [{x@{b=0}=1}]`.
- nested attribute heads are part of Core v1 and count against `max_attribute_depth`.

Reference/addressing forms:

```aeon
~user@role
$.user@role
$.user@["profile.name"]
$.user@["profile.name"].["display.name"]
~user@meta.["x.y"]
```

Canonical notes:
- attributes are selectors in addressing expressions, not canonical path identity segments;
- data namespace and attribute namespace remain distinct.
- quoted bracket member segments may follow ordinary member or attribute traversal using `.[\"...\"]`.
- quoted attribute selectors may be followed by ordinary member, quoted member, or index traversal.
- empty quoted member segments, empty quoted attribute selectors, and incomplete forms such as `~a@` or `~$.a@[` are invalid.

Examples:

```aeon
a@{b=1} = [0]
a = [{x@{b=0}=1}]
f@{ns@{origin:string="core"}:string = "aeon"}:string = "fractal"
```

Namespace note:
- AEON Core v1 has no dedicated namespace syntax for ordinary keys;
- `#` has no intrinsic namespace meaning in core key syntax;
- when a consumer or ecosystem convention needs namespace labeling, the recommended metadata convention is `@{ns="..."}` as defined by `aeon.gp.convention.v1`:

```aeon
key@{ns="aeon"} = "value"
```

Policy notes:
- implementations expose `max_attribute_depth`;
- default lock is `1`;
- capability floor is at least `8`.

## 4. Separator Specs

Separator specs decorate datatypes:

```aeon
size:sep[x] = ^300x250
triple:set[x][y][z] = ^100x200y300z
```

Grammar:

```ebnf
TypeAnnotation = ":" TypeName GenericArgs? SeparatorSpec* ;
SeparatorSpec  = "[" SeparatorChar "]" ;
SeparatorChar  = ASCIIPrintableNoReservedSeparator ;
```

Generic-depth notes:
- generic depth counts nested type annotations that appear inside generic arguments;
- `tuple<n, n>` has generic depth `0`;
- `tuple<tuple<n, n>, tuple<n, n>>` has generic depth `1`;
- `tuple<tuple<tuple<n, n>, n>, n>` has generic depth `2`;
- implementations expose `max_generic_depth`;
- default runtime lock is `1`;
- capability floor is at least `8`.

Current official v1 rules:
- exactly one printable ASCII character;
- horizontal whitespace and newlines may appear around the separator character inside brackets, but the payload itself must remain contiguous;
- `,`, `[`, and `]` are forbidden separator chars;
- separator depth is the number of `[...]` segments.

Nuances:
- `size:sep[x]` has separator depth `1`;
- `triple:set[x][y][z]` has separator depth `3`;
- `sep[x]`, `sep[ x ]`, and `sep[\nx\n]` are legal;
- `sep[xy]` and any form that splits the payload into more than one character are invalid;
- repeated separator specs are legal and preserved structurally, including duplicate chars;
- default runtime lock is `1`;
- capability floor is at least `8`.

Canonical notes:
- separator specs remain attached to the datatype surface;
- AEON Core parses separator specs but does not impose splitting semantics on payloads.

## 5. Assignment and Element Separators

### 5.1 Top-Level and Object Bindings

At document and object level, bindings may be separated by newline or comma:

```aeon
a = 1
b = 2
```

```aeon
a = 1, b = 2
obj = { a = 1, b = 2 }
```

Core v1 rules:
- newline and comma are structural binding separators at document and object level;
- plain spaces alone are never structural separators;
- `;` is not a structural separator.

### 5.2 Lists

List examples:

```aeon
items = ["a", "b", "c"]
items = [
  "a"
  "b"
  "c"
]
```

Grammar summary:

```ebnf
List = "[" (Value ListSep?)* "]" ;
ListSep = "," | Newline ;
```

Nuances:
- list elements may be separated by commas or newlines;
- mixed comma/newline list formatting is accepted by parser behavior;
- indexed elements are addressable as `[0]`, `[1]`, and so on.

### 5.3 Tuples

Tuple examples:

```aeon
point = (1, 2)
point = (
  1
  2
)
```

Grammar summary:

```ebnf
Tuple = "(" (Value TupleSep?)* ")" ;
TupleSep = "," | Newline ;
```

Nuances:
- tuple elements follow the same separator surface as lists;
- tuple semantics differ from list semantics, but the element separator grammar is the same.

### 5.4 Node Children

Node child separators follow the same broad rule:

```aeon
content = <div("hello", <br>, "world")>
content = <div(
  "hello"
  <br>
  "world"
)>
icon = <glyph>
```

Grammar summary:

```ebnf
Node = "<" Identifier AttributeList? TypeAnnotation? ( ">" | "(" (Value NodeSep?)* ")" ">" ) ;
NodeSep = "," | Newline ;
```

Nuances:
- node children accept comma and newline separators;
- empty-node shorthand uses `>` immediately after the tag metadata and is equivalent to an empty child list;
- child-bearing nodes require a closing `>` after the closing `)`;
- canonical printed form uses the closing `>` and prefers `<tag>` over `<tag()>` for empty nodes;
- node heads MAY carry an inline datatype syntactically, but strict mode limits this form to `:node`;
- transport/custom forms MAY use other inline node-head datatypes, for example `<tag:pair("x", "y")>`;
- trailing child separator acceptance is implementation-supported and documented in node appendices.

## 6. Newline Rules

Newlines are structural in AEON, but only in specific places.

Between structural tokens, a newline is otherwise treated the same as ordinary inter-token whitespace. A newline becomes special only when the surrounding grammar consumes it as a separator, or when inserting it would split a compact token that must remain contiguous.

### 6.1 Newline as Separator

Newline can separate:
- bindings in documents and objects;
- list elements;
- tuple elements;
- attribute entries;
- node children.

### 6.2 Newline Forbidden in Compact Tokens

Newline is not allowed inside:
- bare identifiers;
- single-quoted or double-quoted keys;
- single-quoted or double-quoted strings;
- separator specs (`[x]`);
- numbers;
- hex, radix, encoding, date, datetime, and separator literal tokens.

Notes:
- backtick strings may span newlines as string values, but backtick keys are not valid core keys;
- trimticks are multiline string values introduced by a contiguous `>` through `>>>>` marker immediately before a backtick string opener;
- trimticks trim the first empty line, trailing empty lines, and common left indentation according to the marker's tab policy;
- separator literals may terminate at newline, comma, or closing container boundary depending on enclosing grammar context.
- for worked boundary examples, see `appendices/appendix-whitespace-boundaries.md`.

### 6.3 Comments and Newlines

Comments do not become separators by themselves.

Implications:
- a structured or plain comment may appear between bindings or elements;
- comment binding rules determine attachment, but comments do not redefine the surrounding grammar;
- line comments end at newline;
- block comments may span newlines.

## 7. Addressing Interaction

Key and attribute syntax affects addressing and references:

```aeon
"a.b" = 2
ref0 = ~"a.b"
ref1 = ~["a.b"]
ref2 = ~$.["a.b"]

user@{profile.name="dark"} = 1
ref3 = ~user@["profile.name"]
```

Nuances:
- `~a.b` means traversal through two member segments;
- `~"a.b"` and `~["a.b"]` are equivalent initial quoted-member forms;
- `~["a.b"]` means one quoted member segment;
- `@key` and `@["key"]` both address attribute namespace segments.

## 8. Minimum Conformance Reminders

Implementations targeting Core v1 must at minimum:
- accept bare, single-quoted, and double-quoted keys;
- reject backtick keys;
- expose `max_attribute_depth` and `max_separator_depth`;
- support capability floor `>=8` for both depth knobs;
- enforce the official separator-char exclusions;
- handle newline/comma binding separation deterministically;
- reject space-only and semicolon binding separation deterministically.
