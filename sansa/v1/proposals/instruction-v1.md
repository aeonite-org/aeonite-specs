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
mutation operations before target-surface validation, authorization, and apply.

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
because "manual correction"
by "Bob"
from $.inventory.items.*
where .qty == 0
require .status == "open"
replace .qty with :int32, 10
```

The `because` and `by` clauses carry source-level claimed provenance. The
`from`, `where`, and `require` clauses use SANSA.Query expression vocabulary.
The contextual address `.qty` comes from SANSA.Addressing. The `replace` verb
comes from SANSA.Mutate.

The instruction above means:

1. Resolve `$.inventory.items.*`.
2. Keep candidates whose `.qty` value is zero.
3. Preserve a candidate-scoped Mutate precondition that `.status` remains
   `"open"`.
4. For each surviving candidate, resolve `.qty` relative to that candidate.
5. Produce an exact `replace` operation with datatype intent `int32`, number
   representation, and value `10`.

The final mutation plan must contain exact targets. Expanded selectors and
candidate-relative paths are instruction/query conveniences before planning;
they are not stored as executable mutation targets.

`because` and `by` are inert source metadata. `because` records a
human-readable reason. `by` records claimed attribution. Neither clause grants
authorization, proves authentication, signs the instruction, records approval,
or replaces a host audit trail. Actor identity, delegation, policy authority,
signatures, and audit evidence belong to the host envelope or mutation adapter.

`where` and `require` have different authority roles. `where` selects which
candidate bindings participate in lowering. `require` creates fail-closed
SANSA.Mutate preconditions that are evaluated during planning and may be
rechecked before apply. For candidate-relative instructions, each surviving
candidate receives its own precondition target.

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

These examples use contextual `create`, where the current candidate binding is
the parent. Exact destination forms are described in the core verb vocabulary.

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
append .tags with "sale"
move .tags[0] after .tags[2] in .tags
```

The portable core forms are:

```text
create <member-destination> with <instruction-value>
replace <target-address> with <instruction-value>
remove <target-address>
insert <placement> in <container-address> with <instruction-value>
append <container-address> with <instruction-value>
append in <container-address> with <instruction-value>
move <source-address> <placement> in <container-address>
```

where:

```text
placement =
  first
  last
  before <anchor-address>
  after <anchor-address>
```

Each accepted instruction must lower to the existing structured operation
model:

- `create`
- `replace`
- `remove`
- `insert`
- `move`

`append` is source-level sugar for `insert last in <container-address> with
<instruction-value>`. It must lower to the existing `insert` operation with
`placement: "last"` and must not introduce a distinct SANSA.Mutate operation.

### 7.1 Create

`create` adds one named binding under an exact existing parent.

Contextual form:

```sansa
from $.inventory
create status with "active"
```

This lowers to:

```json
{
  "op": "create",
  "parent": "$.inventory",
  "name": "status",
  "kind": "string",
  "value": "active"
}
```

Destination-address form:

```sansa
create $.inventory.status with "active"
```

This also lowers to `parent = $.inventory` and `name = status`. The destination
address must end in a member selector that can be split into an exact existing
parent address plus a new member name. Creating positional children by spelling
a missing position address is not part of `create`; ordered insertion uses
`insert`.

`create` is not `upsert`. The named member must not already exist under the
resolved parent.

### 7.2 Replace

`replace` changes the value of one exact existing binding while preserving its
binding identity and structural location:

```sansa
replace $.inventory.items[1].qty with :int32, 10
```

Candidate-relative form:

```sansa
from $.inventory.items.*
where .qty == 0
replace .qty with :int32, 10
```

Each surviving candidate resolves `.qty` relative to itself. Each resolved
target must be exact before lowering into a structured `replace` operation.

### 7.3 Remove

`remove` deletes one exact existing binding:

```sansa
remove $.inventory.oldStatus
```

Candidate-relative form:

```sansa
from $.inventory.items.*
where .discontinued == true
remove .status
```

`remove` never removes the root binding. If the target selector expands to
multiple bindings, the instruction must either lower through candidate
selection into exact operations or fail before producing a plan.

### 7.4 Insert

`insert` adds a value to an ordered container. The portable form names the
container explicitly:

```sansa
insert first in .tags with "new"
insert last in .tags with "sale"
insert before .tags[2] in .tags with :string, "featured"
insert after .tags[2] in .tags with :string, "clearance"
```

`insert` lowers to a structured `insert` operation with:

- `container` from the `in` address;
- `placement` from `first`, `last`, `before`, or `after`;
- optional `anchor` for `before` and `after`;
- value, datatype intent, and representation family from the instruction value.

The container must resolve to one ordered container. Anchor addresses must
resolve to children of that container.

### 7.5 Move

`move` repositions an existing binding within one ordered container:

```sansa
move .tags[0] first in .tags
move .tags[0] last in .tags
move .tags[0] before .tags[2] in .tags
move .tags[0] after .tags[2] in .tags
```

`move` lowers to a structured `move` operation with `source`, `container`, and
`placement`. The source must be a child of the named container. For `before` and
`after`, the anchor must also be a child of the same container. Cross-container
move remains outside the conservative core.

Internally, each accepted verb can be modeled as a normalized verb plus target
and argument fields before lowering into a structured Mutate operation. This
normal form is an implementation aid, not a user-visible syntax requirement.

### 7.6 Lowering Examples

The following examples show instruction surface forms and their corresponding
structured operation intent. These examples omit plan metadata, frozen binding
identity, preconditions, and diagnostics.

| Instruction | Structured operation intent |
| --- | --- |
| `create $.inventory.status with "active"` | `op=create`, `parent=$.inventory`, `name=status`, `kind=string`, `value="active"` |
| `replace $.inventory.qty with :int32, 10` | `op=replace`, `target=$.inventory.qty`, `datatype=int32`, `kind=number`, `value=10` |
| `remove $.inventory.oldStatus` | `op=remove`, `target=$.inventory.oldStatus` |
| `insert first in $.tags with "new"` | `op=insert`, `container=$.tags`, `placement=first`, `kind=string`, `value="new"` |
| `append $.tags with "new"` | `op=insert`, `container=$.tags`, `placement=last`, `kind=string`, `value="new"` |
| `insert before $.tags[2] in $.tags with :string, "featured"` | `op=insert`, `container=$.tags`, `placement=before`, `anchor=$.tags[2]`, `datatype=string`, `kind=string`, `value="featured"` |
| `move $.tags[0] after $.tags[2] in $.tags` | `op=move`, `source=$.tags[0]`, `container=$.tags`, `placement=after`, `anchor=$.tags[2]` |

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
- followed-target replace or rebind operations
- reference redirection
- multi-target bulk mutation syntax

Each deferred verb needs its own target shape, identity semantics, cardinality
rules, authorization boundary, and apply/result contract before it can enter
the instruction vocabulary.

## 9. Rejected Core Forms

The conservative instruction surface should reject forms that look convenient
but would hide important mutation semantics.

### 9.1 Positional Create

Creating a missing positional child by spelling a destination position is not a
core `create` form:

```sansa
create $.tags[2] with "sale"
```

Use ordered `insert` instead:

```sansa
insert after $.tags[1] in $.tags with "sale"
```

### 9.2 Implicit Upsert

`create` must not silently replace an existing member, and `replace` must not
silently create a missing member:

```sansa
create $.inventory.status with "active"   // fails if status already exists
replace $.inventory.status with "active"  // fails if status is missing
```

An eventual `upsert` verb may define this behavior explicitly.

### 9.3 Cross-Container Move

Moving across containers is outside the conservative core:

```sansa
move $.todo[0] last in $.done
```

Cross-container movement changes ownership and validation context. It needs a
separate operation contract before entering the instruction vocabulary.

### 9.4 Ambiguous Ordered Insert

Ordered insertion should not infer the container only from an anchor:

```sansa
insert "sale" after $.tags[1]
```

The portable form names the container:

```sansa
insert after $.tags[1] in $.tags with "sale"
```

### 9.5 Multi-Verb Instruction

One Instruction contains one mutation intent. Multiple verbs in one source unit
are outside the core surface:

```sansa
replace .qty with 10
remove .oldQty
```

A future batch format may contain multiple Instructions, but batching does not
change the identity of one Instruction.

### 9.6 Runtime Source Reinterpretation

Instruction consumers must not construct executable instruction text by
concatenating runtime values:

```sansa
replace .target with <runtime text>
```

Runtime data may provide structured values or structured address literals
through explicit host APIs, but it must not become executable SANSA Instruction
source text.

## 10. Provisional Surface Grammar

This proposal uses the following grammar sketch to make the intended source
shape explicit. It is explanatory and may be refined before implementation.

```text
Instruction
  = [ BecauseClause ]
    [ ByClause ]
    [ FromClause ]
    [ WhereClause ]
    { RequireClause }
    MutationClause

BecauseClause
  = "because" QuotedText

ByClause
  = "by" QuotedText

FromClause
  = "from" AddressExpression

WhereClause
  = "where" QueryExpression

RequireClause
  = "require" QueryExpression

MutationClause
  = CreateClause
  | ReplaceClause
  | RemoveClause
  | InsertClause
  | AppendClause
  | MoveClause

CreateClause
  = "create" MemberDestination "with" InstructionValue

ReplaceClause
  = "replace" AddressExpression "with" InstructionValue

RemoveClause
  = "remove" AddressExpression

InsertClause
  = "insert" Placement "in" AddressExpression "with" InstructionValue

AppendClause
  = "append" [ "in" ] AddressExpression "with" InstructionValue

MoveClause
  = "move" AddressExpression Placement "in" AddressExpression

Placement
  = "first"
  | "last"
  | "before" AddressExpression
  | "after" AddressExpression

InstructionValue
  = [ ":" DatatypeExpression [ "," ] ] ValueLiteral
```

`AddressExpression` is parsed by SANSA.Addressing. `QueryExpression` is parsed
by the SANSA.Query expression grammar and evaluated as a read-only predicate.
`DatatypeExpression` preserves datatype intent; it does not validate the value.
`ValueLiteral` is the instruction value payload and supplies representation
family when the literal form is unambiguous.
`QuotedText` uses the same quoted payload rules as SANSA string payloads and is
preserved as source provenance without semantic authority.

`MemberDestination` is either a bare or quoted member name relative to the
current candidate parent, or a SANSA address expression that can be split into
an exact parent address plus a final member name. A destination that ends in a
position selector is not a valid `create` destination in the conservative core.

The initial grammar admits at most one `because` clause, at most one `by`
clause, at most one `from` clause, and at most one `where` clause, followed by
zero or more `require` clauses, in that order. Additional query clauses such as
`order by`, `offset`, `limit`, or projection are not part of the conservative
instruction surface. Candidate selection should remain simple until mutation
ordering, target cardinality, and authorization behavior are specified for
broader query-shaped instructions.

## 11. Lowering Boundary

Instruction parsing produces instruction intent, not an executable plan.

A consumer lowers an instruction by:

1. parsing source syntax;
2. preserving inert `because` and `by` source provenance, if present;
3. resolving `from` candidates, if present;
4. evaluating `where` predicates, if present;
5. lowering `require` predicates into structured SANSA.Mutate preconditions;
6. resolving candidate-relative mutation targets;
7. producing exact structured mutation operations;
8. applying normal SANSA.Mutate planning, budgets, and stale-target checks;
9. validating the plan against the intended target surface, if one is selected;
10. applying authorization, adapter apply rules, and result reporting.

This preserves the existing boundary:

- source text is human-authored instruction;
- `because` and `by` are claimed source provenance, not execution authority;
- structured mutation plans are same-process execution artifacts;
- target-surface checks decide whether the plan can be represented by the
  intended host format or adapter surface;
- authorization, validation, transactions, retries, and storage mapping remain
  consumer or adapter responsibilities.

Tooling may expose each lowering step for preview and audit:

```text
Instruction Source
  -> Parsed Instruction
  -> Candidate Binding Set
  -> Structured Mutation Operations
  -> Mutation Plan
  -> Target Surface Check
  -> Preview / Authorize / Apply
```

This makes Instruction useful for editors and workbenches without turning it
into a runtime execution language.

## 12. Diagnostics

SANSA Instruction diagnostics should distinguish parse-time failures,
lowering-time failures, downstream Mutate planning failures, target-surface
failures, authorization failures, and apply failures.

Instruction parse diagnostics include:

- missing mutation verb;
- unknown mutation verb;
- malformed instruction value;
- malformed datatype annotation;
- comma delimiter used outside `:datatype, value`;
- malformed `because` or `by` provenance clause;
- malformed `require` clause;
- duplicate or out-of-order instruction clause;
- unsupported query clause in instruction source;
- multiple mutation verbs in one Instruction;
- unsupported or deferred verb syntax;
- ambiguous ordered insertion without an explicit container.

Instruction lowering diagnostics include:

- candidate selector produced a Resolve diagnostic;
- candidate selector produced no candidates where the consumer requires at
  least one;
- candidate-relative target failed to resolve;
- target resolved no bindings;
- target resolved multiple bindings where the verb requires one exact binding;
- destination-address `create` could not split into parent and member name;
- `create` destination already exists;
- `replace` or `remove` target is missing;
- `insert` or `move` container is not ordered;
- ordered anchor is not a child of the named container;
- `move` source is not a child of the named container;
- cross-container move attempt;
- root removal attempt.

Downstream Mutate planning diagnostics keep their SANSA.Mutate identity. An
Instruction consumer should not collapse Mutate diagnostics into generic
Instruction failures, because the lowered plan boundary is useful for tooling,
auditing, and user repair.

Target-surface diagnostics keep their target identity. For example, an
Instruction may lower to valid SANSA.Mutate intent while an AEON target surface
rejects a datatype annotation that AEON cannot express, or a JSON-compatible
target surface rejects attributes, tuples, nodes, references, non-finite
numbers, or SANSA selector literals. These failures are not Instruction parse
or lowering errors.

Diagnostics should preserve enough context for authoring tools to identify:

- instruction phase: parse, lower, plan, target, authorize, or apply;
- source span or clause when available;
- candidate address when the failure occurs inside candidate-relative lowering;
- lowered operation index when the failure occurs after operations are emitted;
- original downstream diagnostic when the failure comes from Resolve, Query, or
  Mutate.

## 13. Parser And Lowering Fixture Seeds

The following examples are intended as seed material for future parser and
lowering fixtures. They are not a complete CTS surface.

### 13.1 Positive Parse And Lowering Seeds

| Source | Expected lowering shape |
| --- | --- |
| `create $.inventory.status with "active"` | one `create` operation, parent `$.inventory`, name `status`, kind `string` |
| `create $.inventory.total with :int32, 344` | one `create` operation, parent `$.inventory`, name `total`, datatype `int32`, kind `number` |
| `replace $.inventory.color with #fff` | one `replace` operation, target `$.inventory.color`, kind `hex` |
| `replace $.inventory.selector with :sansa, $.inventory.items.*:number` | one `replace` operation, datatype `sansa`, kind `sansa` |
| `remove $.inventory.oldStatus` | one `remove` operation, target `$.inventory.oldStatus` |
| `insert last in $.tags with "sale"` | one `insert` operation, container `$.tags`, placement `last`, kind `string` |
| `insert before $.tags[2] in $.tags with :string, "featured"` | one `insert` operation, container `$.tags`, placement `before`, anchor `$.tags[2]`, datatype `string` |
| `move $.tags[0] after $.tags[2] in $.tags` | one `move` operation, source `$.tags[0]`, container `$.tags`, placement `after`, anchor `$.tags[2]` |
| `because "manual correction"\nby "Bob"\nreplace $.inventory.qty with :int32, 10` | one `replace` operation with source provenance reason `manual correction` and claimed author `Bob` |

Candidate-relative seeds:

| Source | Expected lowering shape |
| --- | --- |
| `from $.inventory\ncreate status with "active"` | one `create` operation per candidate, parent from candidate, name `status` |
| `from $.inventory.items.*\nwhere .qty == 0\nreplace .qty with :int32, 10` | one `replace` operation per surviving candidate, target `.qty` resolved relative to candidate |
| `from $.inventory.items.*\nwhere .sku == "A-100"\nrequire .qty == 7\nreplace .qty with :int32, 10` | one `replace` operation with one candidate-scoped Mutate precondition |
| `from $.inventory.items.*\nwhere .discontinued == true\nremove .status` | one `remove` operation per surviving candidate, target `.status` resolved relative to candidate |
| `from $.inventory.items.*\ninsert last in .tags with "sale"` | one `insert` operation per candidate, container `.tags` resolved relative to candidate |
| `from $.inventory.items.*\nappend .tags with "sale"` | one `insert` operation per candidate with `placement: "last"`, container `.tags` resolved relative to candidate |

### 13.2 Negative Parse Seeds

| Source | Expected failure class |
| --- | --- |
| `from $.inventory.items.*` | missing mutation verb |
| `rename $.inventory.sku to code` | unsupported or deferred verb syntax |
| `create $.inventory.status, "active"` | malformed `create` clause; expected `with` |
| `create $.inventory.status with :int32,, 344` | malformed instruction value |
| `create $.inventory.status with :int32 344,` | comma delimiter used outside `:datatype, value` |
| `because Bob\nreplace $.inventory.qty with 1` | malformed `because` clause; expected quoted text |
| `by\nreplace $.inventory.qty with 1` | malformed `by` clause; expected quoted text |
| `because "a"\nbecause "b"\nreplace $.inventory.qty with 1` | duplicate provenance clause |
| `require\nreplace $.inventory.qty with 1` | malformed `require` clause |
| `from $.items.*\norder by .sku\nreplace .qty with 1` | unsupported query clause in instruction source |
| `replace .qty with 10\nremove .oldQty` | multiple mutation verbs in one Instruction |
| `insert "sale" after $.tags[1]` | ambiguous ordered insertion without explicit container |

### 13.3 Negative Lowering Seeds

| Source | Expected failure class |
| --- | --- |
| `create $.tags[2] with "sale"` | destination-address `create` ends in a position selector |
| `create $ with "active"` | destination-address `create` cannot split root into parent and member name |
| `replace $.inventory.missing with "active"` | `replace` target resolved no bindings |
| `remove $` | root removal attempt |
| `insert last in $.inventory.sku with "sale"` | `insert` container is not ordered |
| `insert before $.otherTags[0] in $.tags with "sale"` | ordered anchor is not a child of the named container |
| `move $.todo[0] last in $.done` | cross-container move attempt |
| `move $.tags[0] before $.tags[0] in $.tags` | invalid move relationship; source and anchor are the same binding |
