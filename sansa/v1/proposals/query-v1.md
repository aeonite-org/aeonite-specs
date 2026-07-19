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
- existence operator shape
- cardinality operator shape
- deterministic function-call shape
- projection expression shape

The expression parser intentionally does not evaluate expressions, resolve addresses, assign function semantics, compare semantic values, enforce authorization, or decide datatype compatibility.

The initial CTS owner is:

```text
aeonite-cts/cts/sansa/v1/sansa-query-parser-cts.v1.json
```

The first evaluator scaffold is intentionally narrower than the full grammar. It covers execution of `from`, Boolean `where`, `order by`, `offset`, `limit`, and `select` over scalar literals, resolution expressions, comparison expressions, Boolean expressions, string and number order keys, existence predicates over resolution expressions, cardinality predicates over resolved binding sets, built-in string functions, value predicates for null and special numeric values, and projection expressions.

The evaluator scaffold explicitly rejects:

- unsupported function names
- invalid built-in function arity or argument types
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

Initial null predicates:

```text
isNull(...)
isNullReason(..., "reason")
```

`isNull(expression)` returns true when the expression resolves exactly one explicit null binding.

`isNullReason(expression, reason)` returns true when the expression resolves exactly one explicit null binding and that binding's surfaced null reason equals `reason`.

These predicates are value-semantic tests, not binding-presence tests. If the operand resolves zero bindings, evaluation produces `Missing`; use `exists(...)` or `absent(...)` when binding presence itself is the question.

Example:

```text
where exists(.status) and isNullReason(.status, "notSet")
```

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

Boolean `and` and `or` evaluate left to right and short-circuit:

- `a and b` does not evaluate `b` when `a` is false.
- `a or b` does not evaluate `b` when `a` is true.

Short-circuiting is part of the query semantics, not an implementation optimization. It allows guard predicates to prevent missing, cardinality, or type errors in later operands:

```text
where exists(.id#number) and .id > 2
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

Initial comparison policy:

| Operands | Equality | Ordering | Notes |
| --- | --- | --- | --- |
| number and number | allowed | allowed | Finite numbers compare by numeric value. |
| string and string | allowed | allowed | String ordering requires the active semantic comparison profile. |
| boolean and boolean | allowed | error | Booleans are not ordered. |
| explicit null | error | error | Use `isNull(...)` or `isNullReason(...)`. |
| NaN | error | error | Use `isNaN(...)`. |
| infinity and number | allowed | allowed | Infinity compares as a numeric bound when numeric comparison is supported. |
| mixed types | error | error | No implicit coercion. |

`NaN` is not comparable. Equality, inequality, ordering, and order-key evaluation over `NaN` must fail with a comparison diagnostic. Queries test explicit NaN values with `isNaN(...)`.

Infinity values are explicit numeric special values. Where an applicable numeric comparison profile accepts infinity, positive and negative infinity compare as numeric bounds. Queries may test for either infinity form with `isInfinity(...)`.

## 13. Existence Operators

Existence operators inspect resolution cardinality rather than scalar value:

```text
exists(...)
absent(...)
```

`exists(expression)` returns true when the resolution expression resolves one or more bindings.

`absent(expression)` returns true when the resolution expression resolves zero bindings.

The operand must be a SANSA resolution expression. Parenthesized grouping around the resolution expression is allowed.

Examples:

```text
where exists(.email)
where absent(.deletedAt)
where exists(.roles) and absent(.roles.*)
where exists(.id#number) and .id > 2
```

The final example means "the roles container exists, and it has no selected entries." `absent(.roles.*)` alone also matches candidates where `.roles` itself is missing.

Semantic and representation filters can be used inside existence operands to guard scalar comparison. In `exists(.id#number) and .id > 2`, the first predicate rejects candidates that do not expose a number-typed `.id` binding before the comparison evaluates. Without the semantic filter, a present non-number `.id` binding may produce a comparison error.

Existence operators are not ordinary functions. They do not evaluate their operand as a scalar value.

## 14. Cardinality Operators

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

`all(...)` is a universal quantifier. It means every binding in the evaluated Binding Set satisfies the predicate. It does not assert that the Binding Set is non-empty.

For example:

```text
where all(.roles.* == "admin")
```

matches bindings where every role is `"admin"`, including bindings where `.roles.*` resolves to an empty Binding Set.

To express "there is at least one role, and every role is admin", combine `any(...)` and `all(...)` explicitly:

```text
where any(.roles.* == "admin") and all(.roles.* == "admin")
```

SANSA.Query v1 does not define an `only(...)` cardinality operator. A future version may introduce `only(...)` as a shorthand for a non-empty all-match predicate, but implementations must not treat it as part of the v1 surface.

Cardinality operators are not ordinary functions. They evaluate their operand repeatedly across the relevant Binding Set.

## 15. Functions

Functions are deterministic value-producing expressions.

Examples:

```text
contains(.description, "developer")
startsWith(.code, "AU-")
lower(.name)
lookup($.jobs, .job)
concat(.firstName, " ", .lastName)
isNull(.status)
isNullReason(.status, "notSet")
isNaN(.metric)
isInfinity(.limit)
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

## 16. Lookup

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

## 17. Projection

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

## 18. Comments

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

## 19. Local Address-Space Binding

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

## 20. Security and Policy

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

## 21. Out of Scope

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
