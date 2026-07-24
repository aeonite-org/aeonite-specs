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

SANSA.Query queries Binding Sets, not AEON documents directly. A Binding Set may be produced by an AEON-backed resolver, RDF-like graph resolver, SQL resolver, filesystem resolver, service-resource resolver, runtime object resolver, or another namespace adapter. The resolver determines how a SANSA address becomes bindings; Query then operates over those bindings.

Resolve answers:

> Which bindings match?

Query answers:

> What values and derived results can be obtained from those bindings in a declared query context?

## 2. Design Principles

SANSA.Query v1 is:

- declarative
- read-only
- deterministic
- based on Binding Sets
- namespace- and domain-neutral
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

### 3.1 Query Evaluation Invariants

SANSA.Query v1 follows these evaluation invariants:

1. Query clauses execute in normative written order.
2. Every clause consumes the complete result of the previous clause.
3. Candidate evaluation follows Binding Set order.
4. Resolution expressions always produce Binding Sets.
5. Scalar contexts require exactly one binding.
6. Missing is distinct from every explicit value.
7. No implicit coercion, host truthiness, flattening, or deduplication occurs.
8. Boolean and membership short-circuiting are normative where specified.
9. Evaluation stops at the first diagnostic in deterministic evaluation order.
10. No partial Result Set is returned on failure.

Fail-fast behavior depends on deterministic evaluation order:

- `from` resolves before any other clause;
- `where` evaluates candidates in Binding Set order;
- `order by` evaluates candidate keys in Binding Set order and key order;
- `offset` and `limit` apply only after filtering and ordering;
- `select` evaluates candidates in the Binding Set order entering projection.

### 3.2 Result Set Model

A successful query produces a Result Set: an ordered sequence of ResultRecords.

Conceptual model:

```text
ResultRecord
  candidateAddress?
  value
  valueAddress?
  kind = binding | derived
  provenance?
```

`candidateAddress` identifies the candidate binding processed by the pipeline when the namespace exposes a canonical address for that candidate.

`value` is the selected query value. It may be a Binding Set, scalar value, or derived constructed value according to the projection expression.

`valueAddress` is present only when projection preserves one existing binding identity. If the selected value is a multi-binding Binding Set, each binding in that set retains its own canonical address instead of collapsing to one `valueAddress`.

Derived values, including constructed projection objects and function results, do not become addressable namespace bindings.

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
- SANSA Address selector parsing, including parent traversal, position ranges, filters, attributes, and local address spaces
- `order by` split into top-level order keys
- omitted order direction canonicalized to `asc`
- `offset` and `limit` as non-negative integers without leading zeroes
- source comments as lexical trivia removed from canonical rendering

The expression parser covers the syntax AST for `where`, `select`, and order-key expressions.

The expression parser covers:

- resolution expressions beginning with `.`, `$`, or `?`
- string, number, Boolean, AEON toggle literals, and AEON scalar source
  literal families such as hex, radix, encoding, separator, explicit-null, and
  temporal-looking literals
- comparison operators
- membership operator shape
- Boolean operators with the precedence defined in this proposal
- parenthesized groups
- existence operator shape
- cardinality operator shape
- deterministic function-call shape
- projection expression shape

The expression parser intentionally does not evaluate expressions, resolve addresses, assign function semantics, compare semantic values, enforce authorization, or decide datatype compatibility.

The evaluator slice is intentionally narrower than the full grammar. It covers execution of `from`, Boolean `where`, `order by`, `offset`, `limit`, and `select` over scalar literals including AEON toggle literal spellings (`yes`, `no`, `on`, `off`) and selected AEON scalar source literal families (`#hex`, `%radix`, `&encoding`, `^separator`, `!null`, and temporal-looking literals), resolution expressions, comparison expressions including same-kind structural container equality, Boolean expressions, membership expressions, string and number order keys, existence predicates over resolution expressions, cardinality predicates over resolved Binding Sets, built-in string functions, structured address activation with `path(...)`, missing-aware fallback with `fallback(...)`, dynamic direct-child resolution with `resolveChild(...)`, explicit reference following with `follow(...)`, concrete-value predicates, null predicates, special numeric predicates, and candidate-local projection expressions.

Some implementations may also expose transform-library helpers such as `objectFrom(...)` and `fieldsFrom(...)`. These helpers operate across multiple Binding Sets and are not part of SANSA.Query v1 core conformance.

The evaluator slice explicitly rejects:

- unsupported function names
- invalid built-in function arity or argument types
- cardinality expressions that do not contain a supported binding-set predicate
- cross-type comparisons
- missing scalar values in scalar context
- multiple bindings in scalar context

The implementation slice inherits SANSA Address portability rules. Portable query expressions must not require addressable positional indexes above `999999`. Implementations may support higher local limits, but accepted indexes above that portable ceiling are non-portable and should surface a warning when the host API supports non-fatal diagnostics.

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

The pre-order Binding Set entering the `order by` stage is the tie-preservation basis.

Ordering semantics are supplied by active Shared AEON Value Semantics profiles. SANSA.Query owns candidate ordering, stable tie preservation, diagnostics, and Binding Set flow. It does not define string collation, temporal comparison, null ordering, or datatype conversion locally.

An order key that evaluates to Missing, explicit null, NaN, a non-scalar value, or multiple bindings produces an evaluation diagnostic unless a future explicit missing-order policy is present. SANSA.Query v1 does not define null-first, null-last, missing-omit, or host-default ordering.

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

Projection does not flatten candidates. Each candidate produces at most one ResultRecord. If the projection expression is a resolution expression that resolves multiple bindings, the selected value is a Binding Set carried by that candidate's ResultRecord. Scalar-consuming functions, comparisons, order keys, and projection fields may still reject multi-binding values when their own contracts require one scalar.

For example:

```text
from $.inventory.items[0]
select .roles.*
```

produces one ResultRecord for candidate `$.inventory.items[0]`. The selected value is a Binding Set containing the matching role bindings. It does not produce one ResultRecord per role.

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
- active Shared AEON Value Semantics profiles
- deterministic function definitions

SANSA.Query v1 recognizes these conceptual expression categories:

- literal expressions
- current-binding expressions
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

The expression `.` by itself means the current candidate binding as a one-binding Binding Set. It is useful when the query source already selected the bindings to test or project:

```text
from $.inventory.items.*.roles.*
where contains(., "min")
select .
```

Query resolution expressions use SANSA Address selector syntax. Query does not introduce a separate path language. The same structural selector meanings apply:

```text
.*              direct expansion
.**             descendant expansion
.^              parent traversal
.[2]            positional child of the current candidate binding
.[2..5]         inclusive positional range from the current candidate binding
.[2..]          range from position 2 through the final exposed positional child
.[..5]          range from position 0 through position 5
.("item?*")     direct member name pattern
.@.origin       explicit attribute-space traversal
.<"params">     explicit local address-space traversal
#number         semantic type filter on the current Binding Set
%string         representation kind filter on the current Binding Set
```

Position ranges are selector expressions, not slice clauses. They select bindings by addressable position before scalar consumption. `[..]` is invalid because it does not state either bound. Negative positions are not part of SANSA Address v1.

The `.[n]` and `.[a..b]` forms are SANSA.Query current-binding shorthand for positional selection from the current candidate. They are equivalent to contextual SANSA Address expressions such as `?[n]`, but keep query notation parallel with member selection such as `.name`.

Parent traversal is selector-only surface. It is not part of an exact canonical address because it depends on the current candidate context and the namespace's exposed parent relation.

Semantic filters and representation-kind filters operate on the current Binding Set. They may be used as guards before scalar comparison:

```text
where exists(.id#number) and .id > 2
```

The grammar accepts filters anywhere SANSA Address selector syntax allows them. Consumers decide which semantic type and representation kind names they understand.

## 9. Scalar Context

Some expression positions require exactly one semantic value.

Examples:

```text
.age >= 18
order by .name
resolveChild($.jobs, .job)
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

`isValue(expression)` returns true when the expression evaluates to exactly one concrete value as defined by Shared AEON Value Semantics. It may inspect value expressions directly or consume a Binding Set produced by a resolution expression or `path(...)`. It returns false for missing operands, explicit null, explicit absence values, and NaN. Finite numbers, infinities, strings, Booleans, toggles, temporal values, lexical structured scalars, SANSA address literals, objects, lists, tuples, nodes, and legal reference forms are concrete values for this predicate. If the operand resolves more than one binding, evaluation produces `CardinalityError`.

`isNull(expression)` returns true when the expression resolves exactly one explicit null binding.

`isNullReason(expression, reason)` returns true when the expression resolves exactly one explicit null binding and that binding's surfaced null reason equals `reason`.

`isNaN(expression)` returns true when the expression resolves exactly one explicit NaN binding.

`isInfinity(expression)` returns true when the expression resolves exactly one explicit positive or negative infinity binding.

These predicates are value-semantic tests, not binding-presence tests. `isValue(...)` is explicitly missing-aware and returns false when its operand resolves zero bindings. The stricter null and special numeric predicates produce `Missing` when their operand resolves zero bindings; use `exists(...)` or `absent(...)` when binding presence itself is the question.

`isValue(...)` is not a scalar-comparison guard. Use semantic filters such as `#number`, `#string`, or profile-defined predicates when a following expression needs a specific comparable domain.

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
| toggle and toggle | allowed | error | Toggle equality is exact token equality; `yes` does not equal `on`, and `no` does not equal `off`. |
| toggle and boolean | error | error | Boolean compatibility requires explicit conversion or a profile-defined comparison domain. |
| hex and hex | allowed | error | Uses canonical hex-payload identity; no numeric, byte, color, hash, or radix interpretation. |
| radix and radix | allowed | error | Uses preserved radix payload and radix-family metadata identity; no numeric base conversion. |
| hex and radix | error | error | Hex and radix are distinct value families even when payload characters overlap. |
| encoding and encoding | allowed | allowed | Uses naïve payload order over preserved encoded payload characters; no decoding. |
| separator and separator | allowed | allowed | Uses naïve separator order over whole canonical separator payloads; no splitting occurs unless a trusted profile supplies domain order. |
| SANSA address and SANSA address | allowed | allowed | Uses canonical address-expression identity and naïve address-expression order; no resolution or selector equivalence. |
| object and object | allowed | error | Structural member equality; object member order is not significant. |
| list and list | allowed | error | Ordered structural equality by index; no portable default order. |
| tuple and tuple | allowed | error | Ordered structural equality by position and arity; no portable default order. |
| node and node | allowed | error | Structural equality by tag, attributes, and ordered child slots; no portable default order. |
| list and tuple | error | error | Requires explicit coercion or a profile-defined compatibility domain. |
| reference form and reference form | allowed | error | Reference-kind identity and canonical target-path identity; no implicit follow. |
| followed reference value | as target value | as target value | Requires explicit `follow(...)` or consumer-declared followed-value mode. |
| date and date | allowed | allowed | Uses the active temporal value-semantics profile; the minimum profile orders canonical ISO-style date payloads. |
| time and time | allowed | allowed | Uses the active temporal value-semantics profile; the minimum profile orders canonical time payloads. |
| datetime and datetime | allowed | allowed | Uses the active temporal value-semantics profile; the minimum profile orders canonical datetime payloads. |
| zrut and zrut | allowed | allowed | Uses the active temporal value-semantics profile; named-zone authority may be required by richer profiles. |
| explicit null | error | error | Use `isNull(...)` or `isNullReason(...)`. |
| NaN | error | error | Use `isNaN(...)`. |
| infinity and finite number | allowed | allowed | Infinity is not equal to finite numeric values and compares as a numeric bound when numeric comparison is supported. |
| infinity and infinity | allowed | allowed | Equal infinities compare equal; negative infinity sorts before positive infinity. |
| mixed types | error | error | No implicit coercion. |

`NaN` is not comparable. Equality, inequality, ordering, and order-key evaluation over `NaN` must fail with a comparison diagnostic. Queries test explicit NaN values with `isNaN(...)`.

Infinity values are explicit numeric special values. Where an applicable value-semantics numeric comparison profile accepts infinity, positive and negative infinity compare as numeric bounds. Queries may test for either infinity form with `isInfinity(...)`.

Temporal values are not ordinary strings. A host may expose AEON `date`, `time`, `datetime`, or `zrut` values through a string-like transport representation, but SANSA.Query compares or orders them through Shared AEON Value Semantics, not string collation. The minimum profile supports same-family canonical temporal payload comparison. Cross-family temporal comparison fails closed unless a richer active profile explicitly defines compatibility.

Temporal query literals may be parsed as source literals so query syntax can carry the same lexical family as AEON values:

```text
from $.types.*#date
where . > 2025-01-01
select .
```

The semantic filter constrains the Binding Set to date values before comparison. A `date` literal does not implicitly compare with `datetime`, `time`, `zrut`, or string values.

The `in` operator tests scalar membership in a Binding Set:

```text
where "admin" in .roles.*
```

The left operand is consumed in scalar context. The right operand is consumed as a Binding Set. Right-side bindings are evaluated in Binding Set order. Each right-side binding is consumed as a scalar and compared to the left value using equality comparison rules.

Membership short-circuits:

- the first successful equality match returns `true`;
- incompatible values encountered before a successful match fail immediately;
- values after a successful match are not evaluated;
- empty Binding Sets and fully evaluated non-matching sets return `false`.

Membership does not skip incompatible bindings before a match: explicit null, NaN, missing scalar, cardinality, and mixed-type comparison failures surface as diagnostics.

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
where any(contains(.roles.*, "min"))
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

The initial evaluator slice supports two cardinality predicate forms:

- a comparison expression with exactly one Binding Set side, such as `.roles.* == "admin"`;
- a deterministic Boolean function call with exactly one Binding Set argument, such as `contains(.roles.*, "min")`.

For function-call predicates, the Binding Set argument is substituted one binding at a time. The function result must be a Boolean scalar for each binding.

## 15. Functions

Functions are deterministic value-producing expressions.

Examples:

```text
contains(.description, "developer")
startsWith(.code, "AU-")
endsWith(.filename, ".aeon")
lower(.name)
upper(.name)
resolveChild($.jobs, .job)
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

Function names use lower camel case. Function-name matching is case-sensitive; `objectFrom(...)` and `objectfrom(...)` are different identifiers.

Ordinary value-producing functions evaluate their arguments before invocation. Resolution-expression arguments are consumed in single-binding scalar context:

- zero bindings produce `Missing`;
- more than one binding produces `CardinalityError`;
- explicit null values are passed only to functions that declare null handling;
- NaN and infinity are passed only to functions that declare special numeric handling;
- unsupported scalar types produce a function-argument diagnostic.

The initial built-in string functions are `contains`, `startsWith`, `endsWith`, `lower`, `upper`, and `concat`. They require string arguments and do not accept explicit null, NaN, infinity, Boolean, number, object, reference form, or Binding Set arguments.

String comparison, ordering, and case mapping are value-semantics concerns. Until the Shared AEON Value Semantics canonical string and case-mapping profiles are locked, the initial evaluator slice uses Unicode scalar-value ordering for string comparison and `order by`. Normative behavior must not depend on host locale, process locale, database collation, or host-language defaults. Case mapping for `lower(...)` and `upper(...)` remains tied to the shared value-semantics profile; implementations must document any provisional behavior.

Consumers may configure accepted value-semantics profiles. Documents cannot select a more permissive comparison, ordering, conversion, or case-mapping profile without consumer authorization. Unsupported profile-dependent operations should be rejected rather than evaluated with host defaults.

Value predicates such as `isValue(...)`, `isNull(...)`, `isNullReason(...)`, `isNaN(...)`, and `isInfinity(...)` define their own argument contracts.

String concatenation must use an explicit function such as `concat`. The `+` operator is reserved for numeric addition.

### Reference Following

`follow(reference)` explicitly evaluates the target value of a legal AEON reference.

Conceptual syntax:

```text
follow(<reference>)
```

Without `follow(...)`, a reference is evaluated as a reference form. Reference-form comparison uses the reference kind and canonical exact target path, and does not inspect the target value.

With `follow(...)`, SANSA.Query walks the reference target path under the consumer's reference policy and then applies active Shared AEON Value Semantics to the target value.

For example:

```text
where follow(.priceRef) > 10
```

Following a reference must be bounded, non-mutating, and diagnostic-preserving. It does not rewrite, inline, clone, alias, or erase the reference form. A query diagnostic should identify both the source reference binding and the referenced target path when following fails.

Pointer references may carry aliasing or mutation-authority semantics outside Query. SANSA.Query only consumes followed target values for read-only evaluation unless a future mutation-capable consumer explicitly declares broader behavior.

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

Fallback propagation:

| Primary result | Replacement evaluated? | Result |
| --- | ---: | --- |
| Value | no | primary value |
| Missing | yes | replacement result |
| CardinalityError | no | diagnostic |
| EvaluationError | no | diagnostic |
| Explicit null | no | explicit null |
| NaN | no | NaN |
| Infinity | no | infinity |

## 17. Dynamic Child Resolution

`resolveChild` is a deterministic structural evaluation form, not an ordinary value function and not a pipeline clause.

Conceptual syntax:

```text
resolveChild(<base>, <key>)
```

Example:

```text
from $.contacts.*
select {
  name = .name
  title = resolveChild($.jobs, .job)
}
```

For SANSA.Query v1, `resolveChild` requires:

- the base to resolve to exactly one addressable container;
- the key to resolve to exactly one scalar value;
- the target to resolve to zero or one binding.

String keys select direct member children. Non-negative integer keys select direct positional children. Other key shapes are not part of the initial `resolveChild` surface.

Multiple base or key bindings produce a cardinality error. A missing target produces no binding. The consuming context determines whether that is acceptable.

## 18. Transform-Library Helpers

Transform-library helpers operate across multiple Binding Sets to construct derived structures. They are useful in projections, but they are not part of SANSA.Query v1 core conformance because they correlate independently resolved Binding Sets by order, cardinality, or interpretation.

Examples include:

```text
objectFrom($.table.header.*, .*)
fieldsFrom($.table.header.*, .*, "age")
```

Implementations that expose these helpers must advertise them as extensions under a transform-library capability such as `SANSA.Transform`.

## 19. Projection

Projection may preserve existing bindings or construct derived results.

Binding projection preserves identity, address, and provenance.

For a binding projection:

```text
from $.users.*
select .name
```

the candidate address identifies the input candidate, while the selected Binding Set preserves the projected binding address or addresses.

A multi-binding projection remains candidate-local:

```text
from $.users[0]
select .roles.*
```

The ResultRecord candidate address remains `$.users[0]`. The selected Binding Set contains the projected role binding addresses.

For a derived projection:

```text
from $.users.*
select concat(.firstName, " ", .lastName)
```

the ResultRecord retains candidate provenance, but the derived value has no canonical namespace address.

For a constructed object projection:

```text
from $.users.*
select { name = .name active = .active }
```

the constructed object is a derived value. It does not become an addressable namespace binding.

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

## 21. Comments

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

## 22. Local Address-Space Binding

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

## 23. Security and Policy

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

Implementations may impose local resource limits for parsing and evaluation, including maximum address depth, maximum selector count, maximum query source size, maximum result count, maximum traversal cost, maximum sort input, and maximum accepted positional index. Local limits may be stricter than the portable SANSA minimum only when the implementation documents the restriction. Local limits may be broader than the portable minimum, but values that rely on broader limits are not portable.

## 24. Query Recipes

This section is non-normative. These recipe patterns illustrate how the v1 surface composes without adding additional syntax.

### 24.1 Scalar Parameters

Scalar values exposed through a mounted local address space are consumed directly in scalar expression contexts.

```text
from $.inventory.items.*
where .name == $.<"params">.name
select .sku
```

Local-space selector names use quoted syntax. In this example, `$.<"params">.name` resolves a string scalar from the mounted `params` namespace.

### 24.2 Dynamic Address Parameters

Dynamic address literals can parameterize source, predicate, ordering, and projection. The comparison is guarded with `isValue(...)` so explicit null, NaN, and missing values do not enter scalar comparison. The selected binding must still be string-compatible or the comparison fails with a deterministic diagnostic.

```text
from path($.<"params">.source)
where isValue(path($.<"params">.statusField)) and path($.<"params">.statusField) == "active"
order by path($.<"params">.sortField) asc
select path($.<"params">.field)
```

When the address is static, semantic filters can be used as an additional domain guard:

```text
from $.inventory.items.*
where isValue(.status) and exists(.status#string) and .status == "active"
select .sku
```

### 24.3 Status Presence

Concrete values, explicit nulls, and missing bindings are distinct. A query can include concrete status values and explicit null status values while excluding missing status bindings:

```text
from $.inventory.items.*
where isValue(.status) or (exists(.status) and isNull(.status))
select { sku = .sku status = fallback(.status, "missing") }
```

### 24.4 Dynamic Child Resolution with Fallback

`resolveChild(...)` and `fallback(...)` can compose inside projections:

```text
from $.inventory.items.*
where .qty >= 4
select { sku = .sku category = resolveChild($.inventory.categoryLabels, .category) status = fallback(.status, "missing") }
```

### 24.5 Transform-Library Table Rows

An implementation that advertises `SANSA.Transform` may expose helpers for ordered row/header shaping. For example, `objectFrom(...)` can project ordered row values into objects using a separate ordered header Binding Set:

```text
from $.table.content.*
select objectFrom($.table.header.*, .*)
```

Experimental field projection can select a named subset from the same ordered row/header shape:

```text
from $.table.content.*
select fieldsFrom($.table.header.*, .*, "age")
```

### 24.6 Parent Context

Parent traversal lets a selector move from a selected child back to its exposed parent before continuing:

```text
from $.inventory.items[1].sku
select .^.qty
```

This is useful for selectors that begin at a precise binding but need sibling values. It remains namespace-adapted: a host that does not expose parent traversal must fail explicitly rather than inventing a parent relation.

### 24.7 Position Ranges

Position ranges select contiguous ordered children before later query clauses run:

```text
from $.inventory.items[1..3]
order by .sku asc
select { sku = .sku qty = .qty }
```

Ranges are inclusive. Open start means zero. Open end means through the final exposed positional child. Query portability follows SANSA Address portability: positions `0` through `999999` are the portable required surface.

## 25. Diagnostics

SANSA.Query evaluation is fail-fast in v1. A query either produces a Result Set or a Diagnostics Set.

Budget exhaustion is an evaluation failure, never implicit truncation. Implementations should use stable budget diagnostics such as `SANSA_QUERY_BUDGET_EXCEEDED` with context naming the budget, limit, observed count, and phase when available.

Evaluation diagnostics must identify the error category with a stable code and message. They should also include query context when available:

- `phase`: one of `parse`, `policy`, `from`, `where`, `order`, or `select`
- `candidateAddress`: the canonical address of the candidate binding being evaluated, when the failure occurs in candidate context
- `budget`: the implementation or caller-supplied budget that was exceeded, when the failure is a budget failure
- `limit`: the configured budget limit, when the failure is a budget failure
- `observed`: the observed count that exceeded the limit, when the failure is a budget failure

`phase`, `candidateAddress`, `budget`, `limit`, and `observed` are diagnostic context. They do not define additional query semantics and must not be used to infer authorization, data visibility, or partial success.

Non-fatal diagnostics may be surfaced as warnings. Warnings do not change the parsed query or the successful result set. They are intended for portability and policy visibility, such as accepting an address position beyond the portable SANSA Address ceiling under an implementation-specific local limit.

## 26. Policy-Restricted Evaluation

Consumers may evaluate SANSA.Query under policy restrictions. A policy restriction constrains the accepted query surface before evaluation; it does not create document-controlled validation semantics and does not create a separate Query conformance profile.

The proposal-stage validation policy is intended for read-only schema or meaning-validation consumers. It may reject presentation and transform behavior such as `order by`, `offset`, `limit`, object projection expressions, and transform-library helpers. Rejection should use a stable policy diagnostic such as `SANSA_QUERY_POLICY_VIOLATION` with `phase: policy`.

For SANSA.Query v1, validation is a named policy value such as `validation`, not a `SANSA.Query.Validation` capability. Implementations that support it should advertise policy support under their Query capability metadata.

## 27. Out of Scope

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
