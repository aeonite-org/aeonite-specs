---
id: sansa-v1-instruction
title: SANSA Instruction v1
description: Proposal-stage human-authored instruction surface combining SANSA Addressing, Query, and Mutate vocabulary.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/instruction
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-resolve
  - sansa-v1-query
  - sansa-v1-mutate
  - aeon-v1-value-semantics
---

# SANSA Instruction v1

Status: Proposal
Scope: human-authored instruction syntax that composes SANSA Addressing,
Resolve, Query, and Mutate vocabulary into one declared change intent.

## 1. Overview

SANSA Instruction does not define new addressing, query, or mutation semantics.
It is a human authoring surface that composes existing SANSA vocabularies into
one declared change intent.

It is not a replacement for SANSA.Addressing, SANSA.Query, or SANSA.Mutate.
Instead, it combines their vocabularies:

- Addressing identifies semantic locations.
- Resolve turns address expressions into Binding Sets.
- Query narrows candidate bindings with read-only conditions.
- Mutate describes requested changes.
- Instruction packages those pieces into a human-authored source form.

SANSA.Query describes which bindings are selected. SANSA.Mutate describes how
exact bindings change. SANSA.Instruction combines both into a single
human-authored declaration while preserving the existing execution boundary.

The conservative SANSA.Mutate structured-plan API remains the execution
boundary. An Instruction is parsed, resolved, checked, and lowered into exact
mutation operations before authorization and apply.

An Instruction is a single declared change intent, not an arbitrary sequence of
commands.

## 2. Design Principles

SANSA Instruction should be:

- vocabulary composition, not a new addressing model;
- explicit about mutation verbs;
- readable beside AEON source;
- compatible with the conservative Mutate plan model;
- side-effect free until lowered, authorized, and applied by a consumer;
- clear about datatype intent versus literal representation.

SANSA Instruction should not be:

- a general-purpose programming language;
- a transaction syntax;
- an authorization policy language;
- a schema validation language;
- a portable serialized mutation-plan format;
- a way to reinterpret runtime strings as executable SANSA source.

## 3. Conceptual Shape

Instruction source may combine Query-shaped selection with Mutate verbs:

```sansa
from $.inventory.items.*
where .qty == 0
replace .qty with :int32, 10
```

The `from` and `where` clauses come from SANSA.Query vocabulary. The contextual
address `.qty` comes from SANSA.Addressing. The `replace` verb comes from
SANSA.Mutate.

The instruction above means:

1. Resolve `$.inventory.items.*`.
2. Keep candidates whose `.qty` value is zero.
3. For each surviving candidate, resolve `.qty` relative to that candidate.
4. Produce an exact `replace` operation with datatype intent `int32`, number
   representation, and value `10`.

The final mutation plan must contain exact targets. Expanded selectors and
candidate-relative paths are instruction/query conveniences before planning;
they are not stored as executable mutation targets.

## 4. Instruction Values

An Instruction value has three conceptual parts:

```text
InstructionValue
  datatypeIntent?        optional semantic datatype hint
  representationFamily   literal family or representation kind
  literalPayload          parsed value payload
```

For example:

```sansa
replace .qty with :int32, 10
```

contains datatype intent `int32`, number-literal representation, and numeric
payload `10`.

Instruction value syntax is type-first:

```sansa
ValueIntent =
  [ ":" Datatype [ "," ] ] ValueLiteral
```

The optional `:Datatype` prefix preserves semantic datatype intent. The literal
payload determines the representation or literal family when it is unambiguous.

Both of these are equivalent:

```sansa
create total with :int32 344
create total with :int32, 344
```

The comma is optional and may appear only immediately after an explicit
datatype annotation. It is a readability delimiter between datatype intent and
the value payload; it is not a general instruction separator.

### 4.1 Type-First Rationale

SANSA Instruction uses type-first value annotation because AEON bindings place
type before value:

```aeon
total:int32 = 344
```

Instruction syntax mirrors that reading order without copying AEON binding
syntax:

```sansa
create total with :int32, 344
```

This avoids the ambiguity of value-first forms such as:

```sansa
replace .selector with $.name:string
```

In that example `:string` may be part of the SANSA address qualifier rather
than the instruction value datatype. Type-first syntax keeps the instruction
datatype outside the address expression:

```sansa
replace .selector with :sansa, $.name:string
```

## 5. Representation Family

When no datatype annotation is present, the value literal may still carry an
obvious representation family:

```sansa
create status with "active"
create color with #fff
create enabled with true
create count with 10
create state with yes
create selector with $.inventory.items.*
```

These lower to mutation operations with representation intent inferred from the
literal family. For example:

```sansa
create color with #fff
```

may lower to:

```json
{
  "op": "create",
  "parent": ".",
  "name": "color",
  "kind": "hex",
  "value": "fff"
}
```

Datatype intent is included only when the instruction supplies it:

```sansa
create color with :brandColor, #fff
create selector with :sansa, $.inventory.items.*:number
create total with :int32, 344
```

These preserve semantic type intent while still allowing the literal family to
provide representation intent.

## 6. Instruction Identity

An Instruction contains a single mutation intent. The source may use Query-shaped
clauses to select candidates, but the mutation section describes one verb
applied over those candidates.

```sansa
from $.inventory.items.*
where .qty == 0
replace .qty with 10
```

This is one Instruction with one `replace` intent. It may lower to multiple
structured `replace` operations if multiple candidate bindings survive the
selection clauses.

Future documents may define an instruction batch or script format, but that is a
different layer. A batch would contain multiple Instructions; it would not make
one Instruction into a general command sequence.

## 7. Core Mutation Verbs

Initial instruction verbs should map directly to the conservative
SANSA.Mutate operation vocabulary:

```sansa
create status with "active"
replace .qty with :int32, 10
remove .deprecated
insert last in .tags with "sale"
move .tags[0] after .tags[2]
```

The exact spelling of ordered `insert` and `move` forms remains provisional.
The important constraint is that each accepted instruction must lower to the
existing structured operation model:

- `create`
- `replace`
- `remove`
- `insert`
- `move`

Internally, each accepted verb can be modeled as a normalized verb plus target
and argument fields before lowering into a structured Mutate operation. This
normal form is an implementation aid, not a user-visible syntax requirement.

## 8. Deferred Verbs

The following verbs are useful vocabulary candidates but are outside the
conservative instruction surface until separately specified:

- `rename`
- `copy`
- `clone`
- `merge`
- `patch`
- `upsert`
- `clear`
- `append`
- followed-target replace or rebind operations
- reference redirection
- multi-target bulk mutation syntax

Each deferred verb needs its own target shape, identity semantics, cardinality
rules, authorization boundary, and apply/result contract before it can enter
the instruction vocabulary.

## 9. Lowering Boundary

Instruction parsing produces instruction intent, not an executable plan.

A consumer lowers an instruction by:

1. parsing source syntax;
2. resolving `from` candidates, if present;
3. evaluating `where` predicates, if present;
4. resolving candidate-relative mutation targets;
5. producing exact structured mutation operations;
6. applying normal SANSA.Mutate planning, authorization, budgets, stale-target
   checks, and adapter apply rules.

This preserves the existing boundary:

- source text is human-authored instruction;
- structured mutation plans are same-process execution artifacts;
- authorization, validation, transactions, retries, and storage mapping remain
  consumer or adapter responsibilities.

Tooling may expose each lowering step for preview and audit:

```text
Instruction Source
  -> Parsed Instruction
  -> Candidate Binding Set
  -> Structured Mutation Operations
  -> Mutation Plan
  -> Preview / Authorize / Apply
```

This makes Instruction useful for editors and workbenches without turning it
into a runtime execution language.
