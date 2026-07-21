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
  - aeon-v1-value-semantics
---

# SANSA.Query v1

Status: Proposal  
Scope: read-only semantic query pipeline, expression model, and bounded evaluator contract.

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

## 5. Implementation Conformance Slice

The current implementation slices validate query source shape, return structural models, and evaluate a deliberately bounded subset over host-neutral Binding Sets.

The clause parser covers:

- clause detection and normative clause order
- required `from` and terminal `select`
- duplicate clause rejection
- `from` as one literal SANSA address expression or `path(...)` source expression
- `order by` split into top-level order keys
- omitted order direction canonicalized to `asc`
- `offset` and `limit` as non-negative integers without leading zeroes
- source comments as lexical trivia removed from canonical rendering

The expression parser covers the syntax AST for `where`, `select`, and order-key expressions.

The expression parser covers:

- resolution expressions beginning with `.`, `$`, or `?`
- string, number, and Boolean literals
- comparison operators
- membership operator shape
- Boolean operators with the precedence defined in this proposal
- parenthesized groups
- existence operator shape
- cardinality operator shape
- deterministic function-call shape
- projection expression shape

The expression parser intentionally does not evaluate expressions, resolve addresses, assign function semantics, compare semantic values, enforce authorization, or decide datatype compatibility.

The evaluator slice is intentionally narrower than the full grammar. It covers execution of `from`, Boolean `where`, `order by`, `offset`, `limit`, and `select` over scalar literals, resolution expressions, comparison expressions, Boolean expressions, membership expressions, string and number order keys, existence predicates over resolution expressions, cardinality predicates over resolved Binding Sets, built-in string functions, structured address activation with `path(...)`, missing-aware fallback with `fallback(...)`, dynamic container lookup with `lookup(...)`, ordered binding-set object construction with `objectFrom(...)`, ordinary value predicates, null predicates, special numeric predicates, and projection expressions.

The evaluator slice explicitly rejects:

- unsupported function names
- invalid built-in function arity or argument types
- cardinality expressions that do not contain a supported binding-set predicate
- cross-type comparisons
- missing scalar values in scalar context
- multiple bindings in scalar context

The CTS owner is:

```text
aeonite-cts/cts/sansa/v1/suites/04-query-parser.json
aeonite-cts/cts/sansa/v1/suites/05-query-expression-parser.json
aeonite-cts/cts/sansa/v1/suites/06-query-evaluate.json
```

This evaluator slice is not the complete SANSA.Query v1 evaluation contract. It is an implementation milestone used to validate the parser, resolver, and expression model together.

## 6. Clauses

### 6.1 From

The `from` clause provides the initial Binding Set.

```text
from $.users.*
```

A literal SANSA.Resolve expression may be used directly.

```text
from path($.<"params">.source)
```

`path(...)` may also be used in the `from` clause to activate a structured SANSA Address Literal value as the query source. The activated address supplies the initial Binding Set for the query.

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

The value must be a non-negative integer. Implementations may bound accepted
offset values according to their integer model and evaluator resource policy.

### 6.5 Limit

The `limit` clause restricts the Binding Set to at most the specified number of bindings.

```text
limit 10
```

The value must be a non-negative integer. `limit 0` produces an empty Binding
Set. Implementations may bound accepted limit values according to their integer
model and evaluator resource policy.

### 6.6 Select

The `select` clause produces the final Result Set.

Each result record represents one candidate binding that survives filtering, ordering, offset, and limit. When the namespace exposes a canonical address for that candidate, the result record carries that address as the result address. The selected value remains separate from the candidate address.

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
- membership expressions
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

Initial value predicates:

```text
isValue(...)
isNull(...)
isNullReason(..., "reason")
isNaN(...)
isInfinity(...)
```

`isValue(expression)` returns true when the expression evaluates to one ordinary scalar value: string, Boolean, or finite number. It may inspect scalar expressions directly or consume a Binding Set produced by a resolution expression or `path(...)`. It returns false for missing operands, non-scalar bindings, explicit null, NaN, and infinity. If the operand resolves more than one binding, evaluation produces `CardinalityError`.

`isNull(expression)` returns true when the expression resolves exactly one explicit null binding.

`isNullReason(expression, reason)` returns true when the expression resolves exactly one explicit null binding and that binding's surfaced null reason equals `reason`.

`isNaN(expression)` returns true when the expression resolves exactly one explicit NaN binding.

`isInfinity(expression)` returns true when the expression resolves exactly one explicit positive or negative infinity binding.

These predicates are value-semantic tests, not binding-presence tests. `isValue(...)` is explicitly missing-aware and returns false when its operand resolves zero bindings. The stricter null and special numeric predicates produce `Missing` when their operand resolves zero bindings; use `exists(...)` or `absent(...)` when binding presence itself is the question.

Example:

```text
where isValue(.id) and .id > 2
where isValue(path($.<"params">.statusField))
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

Boolean context accepts explicit Boolean scalar values and single resolved bindings that expose a Boolean scalar. It does not apply host-language truthiness to strings, numbers, nulls, objects, or Binding Sets.

Boolean `not` evaluates its operand in Boolean context and returns the negated value.

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
in
```

Comparison semantics are defined by Shared AEON Value Semantics, not by the runtime host language.

The runtime must not define:

- numeric comparison
- string comparison
- temporal comparison
- datatype compatibility
- null behavior
- absence behavior

Cross-type comparison is invalid unless an applicable shared value-semantics contract explicitly defines compatibility.

The initial comparison policy mirrors the Shared AEON Value Semantics minimum v1 consumer contract:

| Operands | Equality | Ordering | Notes |
| --- | --- | --- | --- |
| number and number | allowed | allowed | Finite numbers compare by numeric value. |
| string and string | allowed | allowed | String ordering requires the active value-semantics string ordering profile. |
| boolean and boolean | allowed | error | Booleans are not ordered. |
| explicit null | error | error | Use `isNull(...)` or `isNullReason(...)`. |
| NaN | error | error | Use `isNaN(...)`. |
| infinity and number | allowed | allowed | Infinity compares as a numeric bound when numeric comparison is supported. |
| mixed types | error | error | No implicit coercion. |

`NaN` is not comparable. Equality, inequality, ordering, and order-key evaluation over `NaN` must fail with a comparison diagnostic. Queries test explicit NaN values with `isNaN(...)`.

Infinity values are explicit numeric special values. Where an applicable value-semantics numeric comparison profile accepts infinity, positive and negative infinity compare as numeric bounds. Queries may test for either infinity form with `isInfinity(...)`.

The `in` operator tests scalar membership in a Binding Set:

```text
where "admin" in .roles.*
```

The left operand is consumed in scalar context. The right operand is consumed as a Binding Set. Each right-side binding is consumed as a scalar and compared to the left value using equality comparison rules. Empty Binding Sets and non-matching sets evaluate to false. Membership does not skip incompatible bindings: explicit null, NaN, missing scalar, cardinality, and mixed-type comparison failures surface as diagnostics.

`in` is not string containment and does not introduce list literals. String containment uses an explicit function such as `contains(...)`.

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
endsWith(.filename, ".aeon")
lower(.name)
upper(.name)
lookup($.jobs, .job)
objectFrom($.table.header.*, .*)
concat(.firstName, " ", .lastName)
isNull(.status)
isNullReason(.status, "notSet")
isValue(.id)
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

Ordinary value-producing functions evaluate their arguments before invocation. Resolution-expression arguments are consumed in single-binding scalar context:

- zero bindings produce `Missing`;
- more than one binding produces `CardinalityError`;
- explicit null values are passed only to functions that declare null handling;
- NaN and infinity are passed only to functions that declare special numeric handling;
- unsupported scalar types produce a function-argument diagnostic.

The initial built-in string functions are `contains`, `startsWith`, `endsWith`, `lower`, `upper`, and `concat`. They require string arguments and do not accept explicit null, NaN, infinity, Boolean, number, object, or Binding Set arguments.

String comparison, ordering, and case mapping are value-semantics concerns. Until the Shared AEON Value Semantics canonical string and case-mapping profiles are locked, the initial evaluator slice uses Unicode scalar-value ordering for string comparison and `order by`. Normative behavior must not depend on host locale, process locale, database collation, or host-language defaults. Case mapping for `lower(...)` and `upper(...)` remains tied to the shared value-semantics profile; implementations must document any provisional behavior.

Value predicates such as `isValue(...)`, `isNull(...)`, `isNullReason(...)`, `isNaN(...)`, and `isInfinity(...)` define their own argument contracts.

String concatenation must use an explicit function such as `concat`. The `+` operator is reserved for numeric addition.

### Dynamic Address Activation

`path(value)` activates a structured SANSA Address Literal value as an address expression.

Conceptual syntax:

```text
path(<value>)
```

The operand is consumed in scalar value context and must be a SANSA Address Literal value. A plain string that happens to contain address-like text is not a SANSA Address Literal and must not be parsed as address syntax by `path`.

In expression positions, `path(...)` returns the Binding Set produced by resolving the activated address in the current candidate context. This supports dynamic selected fields, predicates, and order keys:

```text
select path($.<"params">.field)
order by path($.<"params">.sortField) asc
```

In the `from` clause, `path(...)` activates a structured SANSA Address Literal value as the query source:

```text
from path($.<"params">.source)
select .sku
```

The activated address supplies the source Binding Set for the query. A source expression that does not evaluate to a Binding Set is invalid.

## 16. Fallback

`fallback` is a deterministic missing-aware expression, not an ordinary eager function.

Conceptual syntax:

```text
fallback(<primary>, <replacement>)
```

The primary operand is consumed in scalar value context. If the primary operand resolves zero bindings, or otherwise produces a missing-scalar diagnostic, the replacement operand is evaluated and consumed in the same scalar value context. If the primary operand succeeds, the replacement operand is not evaluated.

`fallback` handles only missing primary values. Explicit null values, cardinality errors, type errors, comparison errors, unsupported functions, invalid references, and authorization failures do not trigger fallback.

## 17. Lookup

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

String keys select direct member children. Non-negative integer keys select direct positional children. Other key shapes are not part of the initial lookup surface.

Multiple base or key bindings produce a cardinality error. A missing target produces no binding. The consuming context determines whether that is acceptable.

## 18. Object From

`objectFrom` is a deterministic projection helper for ordered binding sets.

Conceptual syntax:

```text
objectFrom(<keys>, <values>)
```

Example:

```text
from $.table.content.*
select objectFrom($.table.header.*, .*)
```

For SANSA.Query v1, `objectFrom` requires:

- both arguments to be resolution expressions;
- the key and value Binding Sets to have equal length;
- every key binding to expose a string scalar value;
- every value binding to expose one scalar value;
- generated keys to be unique.

The helper pairs key and value bindings by their resolved order and constructs one derived object. Duplicate keys, mismatched lengths, non-string keys, and non-scalar values produce diagnostics. The helper does not modify the source namespace or assign semantics to row-like structures.

## 19. Projection

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

## 20. Comments

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

## 21. Local Address-Space Binding

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

## 22. Security and Policy

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

## 23. Query Recipes

This section is non-normative. These recipe patterns illustrate how the v1 surface composes without adding additional syntax.

### 23.1 Dynamic Address Parameters

Dynamic address literals can parameterize source, predicate, ordering, and projection. The comparison is guarded with `isValue(...)` so explicit null, NaN, infinity, non-scalar, and missing values do not enter scalar comparison.

```text
from path($.<"params">.source)
where isValue(path($.<"params">.statusField)) and path($.<"params">.statusField) == "active"
order by path($.<"params">.sortField) asc
select path($.<"params">.field)
```

### 23.2 Status Presence

Ordinary values, explicit nulls, and missing bindings are distinct. A query can include ordinary status values and explicit null status values while excluding missing status bindings:

```text
from $.inventory.items.*
where isValue(.status) or (exists(.status) and isNull(.status))
select { sku = .sku status = fallback(.status, "missing") }
```

### 23.3 Lookup with Fallback

`lookup(...)` and `fallback(...)` can compose inside projections:

```text
from $.inventory.items.*
where .qty >= 4
select { sku = .sku category = lookup($.inventory.categoryLabels, .category) status = fallback(.status, "missing") }
```

### 23.4 Table Rows

`objectFrom(...)` can project ordered row values into objects using a separate ordered header Binding Set:

```text
from $.table.content.*
select objectFrom($.table.header.*, .*)
```

## 24. Diagnostics

SANSA.Query evaluation is fail-fast in v1. A query either produces a Result Set or a Diagnostics Set.

Evaluation diagnostics must identify the error category with a stable code and message. They should also include query context when available:

- `phase`: one of `parse`, `from`, `where`, `order`, or `select`
- `candidateAddress`: the canonical address of the candidate binding being evaluated, when the failure occurs in candidate context

`phase` and `candidateAddress` are diagnostic context. They do not define additional query semantics and must not be used to infer authorization, data visibility, or partial success.

## 25. Out of Scope

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
- arbitrary dynamic query-source construction beyond structured SANSA Address Literal activation with `path(...)`

These require separate proposals or future versions.
