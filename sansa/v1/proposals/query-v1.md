---
id: sansa-v1-query
title: SANSA.Query v1
description: Proposal-stage read-only semantic query model built on SANSA.Resolve.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/query
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-resolve
---

# SANSA.Query v1

Status: Proposal  
Scope: read-only semantic query pipeline and initial expression model.

## 1. Overview

SANSA.Query is a declarative, read-only semantic transformation interface.

It builds on SANSA.Resolve. Resolve discovers bindings. Query evaluates, filters, orders, slices, and projects them.

Resolve answers:

> Which bindings match?

Query answers:

> What do those bindings mean?

## 2. Design Principles

SANSA.Query v1 is:

- declarative
- read-only
- deterministic
- based on Binding Sets
- independent of host programming languages
- explicit about missing and multi-binding behavior
- side-effect free
- not a general-purpose programming language
- not based on relational algebra

## 3. Conceptual Pipeline

```text
Resolve
  |
  v
Binding Set
  |
  v
Filter
  |
  v
Binding Set
  |
  v
Order
  |
  v
Binding Set
  |
  v
Slice
  |
  v
Binding Set
  |
  v
Project
  |
  v
Result Set
```

Each stage has a single responsibility and produces a new logical result.

## 4. Surface Syntax

A query consists of ordered clauses.

```text
from <resolve-expression>
where <boolean-expression>
order by <value-expression> [asc | desc]
offset <non-negative-integer>
limit <non-negative-integer>
select <projection-expression>
```

The minimum complete query is:

```text
from <resolve-expression>
select <projection-expression>
```

Example:

```text
from $.users.*
select .name
```

The normative clause order is:

```text
from
where
order by
offset
limit
select
```

The written order mirrors the logical evaluation order.

## 5. Parser Conformance Slice

The first implementation slices for SANSA.Query are parser-only. They validate query source shape and return structural models, but do not evaluate expressions or produce query results.

This slice covers:

- clause detection and normative clause order
- required `from` and terminal `select`
- duplicate clause rejection
- `from` as exactly one SANSA address expression
- `order by` split into top-level order keys
- omitted order direction canonicalized to `asc`
- `offset` and `limit` as non-negative integers without leading zeroes
- source comments as lexical trivia removed from canonical rendering

The clause parser covers the outer query pipeline. The expression parser covers the initial syntax AST for `where`, `select`, and order-key expressions.

The expression parser covers:

- resolution expressions beginning with `.`, `$`, or `?`
- string, number, and Boolean literals
- comparison operators
- Boolean operators with the precedence defined in this proposal
- parenthesized groups
- cardinality operator shape
- deterministic function-call shape
- projection expression shape

The expression parser intentionally does not evaluate expressions, resolve addresses, assign function semantics, compare semantic values, enforce authorization, or decide datatype compatibility.

The initial CTS owner is:

```text
aeonite-cts/cts/sansa/v1/sansa-query-parser-cts.v1.json
```

The first evaluator scaffold is intentionally narrower than the full grammar. It covers execution of `from`, Boolean `where`, `order by`, `offset`, `limit`, and `select` over scalar literals, resolution expressions, comparison expressions, Boolean expressions, string and number order keys, cardinality predicates over resolved binding sets, and projection expressions.

The evaluator scaffold explicitly rejects:

- function-call expressions
- cardinality expressions that do not contain a supported binding-set predicate
- cross-type comparisons
- missing scalar values in scalar context
- multiple bindings in scalar context

This evaluator scaffold is not the complete SANSA.Query v1 evaluation contract. It is an implementation milestone used to validate the parser, resolver, and expression model together.

## 6. Clauses

### 6.1 From

The `from` clause provides the initial SANSA.Resolve expression.

```text
from $.users.*
```

Any valid SANSA.Resolve expression may be used.

### 6.2 Where

The `where` clause filters the current Binding Set.

```text
where .age >= 18
```

The expression is evaluated for each candidate binding. A candidate remains in the Binding Set only when the expression evaluates to Boolean `true`.

Boolean evaluation does not use truthiness.

### 6.3 Order By

The `order by` clause deterministically reorders the current Binding Set.

```text
order by .lastName asc, .firstName asc
```

If direction is omitted, `asc` is assumed.

Ordering keys are evaluated from left to right. Later keys act as tie-breakers. Ordering must be stable. Bindings that compare equal across every specified key retain their existing relative order.

### 6.4 Offset

The `offset` clause removes the first specified number of bindings from the working Binding Set.

```text
offset 20
```

The value must be a non-negative integer.

### 6.5 Limit

The `limit` clause restricts the Binding Set to at most the specified number of bindings.

```text
limit 10
```

The value must be a non-negative integer. `limit 0` produces an empty Binding Set.

### 6.6 Select

The `select` clause produces the final Result Set.

```text
select .name
```

```text
select {
  name = .name
  age = .age
}
```

Projection is terminal in SANSA.Query v1. No pipeline clause may follow `select`.

## 7. Expressions

Expressions are evaluated within a candidate context containing:

- the current binding
- the namespace root
- mounted local address spaces
- the query environment
- datatype and semantic contracts
- deterministic function definitions

SANSA.Query v1 recognizes these conceptual expression categories:

- literal expressions
- relative resolution expressions
- root resolution expressions
- comparison expressions
- Boolean expressions
- cardinality expressions
- existence expressions
- function expressions
- projection expressions

## 8. Resolution Expressions

A leading dot resolves relative to the current candidate binding.

```text
.name
.address.city
.roles.*
.@.metadata
```

A leading `$` resolves from the namespace root.

```text
$.jobs
$.settings.locale
$.<"params">.username
```

Resolution expressions always produce Binding Sets. Expression contexts determine how those Binding Sets may be consumed.

## 9. Scalar Context

Some expression positions require exactly one semantic value.

Examples:

```text
.age >= 18
order by .name
lookup($.jobs, .job)
```

When a resolution expression is consumed in scalar context, it produces one of four outcomes:

- `Value`: exactly one binding resolved successfully.
- `Missing`: no binding resolved.
- `CardinalityError`: more than one binding resolved without an explicit cardinality operator.
- `EvaluationError`: evaluation failed for another specified reason.

`Missing` is an evaluation state. It is not null, false, an empty string, zero, an explicit AEON absence value, or an accepted empty scalar.

## 10. Missing and Absence

Missing bindings and explicit absence values are distinct.

These are different states:

- `.email` does not resolve.
- `.email` resolves to an explicit `notSet` value.
- `.email` resolves to an explicit `notApplicable` value.
- `.email` resolves to an explicit tombstone value.

Comparison operators must not silently treat these as equivalent.

Existence tests inspect binding presence only:

```text
exists(.email)
absent(.deletedAt)
```

Explicit absence values require distinct tests, with exact names defined by the relevant Aeonite absence-value specification.

## 11. Boolean Expressions

Initial Boolean operators:

```text
and
or
not
```

Initial precedence:

1. parenthesized expressions
2. unary `not`
3. comparison expressions
4. `and`
5. `or`

Example:

```text
where .active == true and (.age >= 18 or .role == "admin")
```

## 12. Comparison Expressions

Initial comparison operators:

```text
==
!=
<
<=
>
>=
```

Comparison semantics are defined by the Aeonite semantic model, not by the runtime host language.

The runtime must not define:

- numeric comparison
- string comparison
- temporal comparison
- datatype compatibility
- null behavior
- absence behavior

Cross-type comparison is invalid unless an applicable semantic contract explicitly defines compatibility.

## 13. Cardinality Operators

SANSA.Query does not implicitly collapse Binding Sets into scalar values.

Initial cardinality operators:

```text
any(...)
all(...)
none(...)
```

Examples:

```text
where any(.roles.* == "admin")
where all(.scores.* >= 50)
where none(.flags.* == "blocked")
```

Empty Binding Set semantics are:

```text
any(empty)  = false
all(empty)  = true
none(empty) = true
```

These semantics are normative for SANSA.Query v1.

Cardinality operators are not ordinary functions. They evaluate their operand repeatedly across the relevant Binding Set.

## 14. Functions

Functions are deterministic value-producing expressions.

Examples:

```text
contains(.description, "developer")
startsWith(.code, "AU-")
lower(.name)
lookup($.jobs, .job)
concat(.firstName, " ", .lastName)
```

Functions must be:

- specification-defined or profile-defined
- deterministic
- side-effect free
- non-mutating
- capability-declared
- unavailable unless authorized by the consumer

Documents must not define executable functions.

Function names use lower camel case.

String concatenation must use an explicit function such as `concat`. The `+` operator is reserved for numeric addition.

## 15. Lookup

`lookup` is a deterministic value-producing expression, not a pipeline clause.

Conceptual syntax:

```text
lookup(<base>, <key>)
```

Example:

```text
from $.contacts.*
select {
  name = .name
  title = lookup($.jobs, .job)
}
```

For SANSA.Query v1, `lookup` requires:

- the base to resolve to exactly one addressable container;
- the key to resolve to exactly one scalar value;
- the target to resolve to zero or one binding.

Multiple base or key bindings produce a cardinality error. A missing target produces no binding. The consuming context determines whether that is acceptable.

## 16. Projection

Projection may preserve existing bindings or construct derived results.

Binding projection preserves identity, address, and provenance.

```text
select .name
```

Constructive projection creates derived output without modifying the source namespace.

```text
select {
  displayName = concat(.firstName, " ", .lastName)
}
```

Constructed values have derived identity and are not written back into the namespace.

## 17. Comments

SANSA.Query supports source comments.

Single-line:

```text
// comment
```

Multi-line:

```text
/*
  comment
*/
```

Comments are lexical trivia. They may appear wherever whitespace is permitted, do not affect query semantics, and are removed from canonical query representations.

## 18. Local Address-Space Binding

Runtime values intended for use by a query should be supplied through explicitly mounted local address spaces rather than incorporated into query source text.

Example:

```text
from $.contacts.*
where .name == $.<"params">.username
select .name
```

The resolving consumer supplies `$.<"params">.username` as structured evaluation data. The supplied value is resolved only after the query has been parsed and must not be reinterpreted as SANSA.Query syntax.

Implementations should expose APIs that accept query source and mounted local address spaces as separate inputs.

```text
query source
  +
primary address space
  +
mounted local address spaces
  |
  v
parsed query evaluation
```

There must be no fallback between primary and local address spaces.

## 19. Security and Policy

Consumers receiving SANSA.Query expressions from outside their trust boundary may:

- reject all local namespace references;
- allow only named local namespaces;
- restrict accessible paths within each namespace;
- expose reduced namespace views;
- set maximum local address-space depth;
- reject queries whose cost or traversal exceeds consumer-defined limits.

A syntactically valid local address does not imply authorization to resolve it.

Mounted local namespaces are read-only evaluation inputs in SANSA.Query.

Local address-space binding prevents runtime values from being interpreted as SANSA.Query syntax. It does not by itself prevent unauthorized data access, excessive traversal, excessive result generation, expensive ordering, or information disclosure through permitted namespaces.

## 20. Out of Scope

SANSA.Query v1 does not define:

- mutation
- subscription
- history resolution
- general joins
- subqueries
- grouping
- aggregation
- arithmetic beyond reserved numeric addition semantics
- custom executable functions
- implicit type coercion
- regular expressions
- dynamic query-source construction

These require separate proposals or future versions.
