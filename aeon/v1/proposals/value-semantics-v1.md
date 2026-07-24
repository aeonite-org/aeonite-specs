---
id: aeon-v1-value-semantics
title: Shared AEON Value Semantics
description: "Architectural proposal for shared deterministic value behavior across AEON, AEOS, SANSA, Tonics, and future ecosystem components."
status: proposal
family: official-v1
group: Proposals
license: CC-BY-4.0
path: specification/aeon-v1-documentation/proposals/value-semantics
links:
  - aeon-core-v1-value-types
  - aeos-v1
  - sansa-v1-query
---

# Proposal: Shared AEON Value Semantics

Status: proposal  
Scope: architectural ownership of deterministic value behavior across the AEON ecosystem.

## 1. Purpose

Shared AEON Value Semantics defines deterministic behavior for values after AEON Core has recognized their representation.

AEON Core answers:

> What was written?

Value Semantics answers:

> How do values relate to one another?

This proposal centralizes semantic contracts that would otherwise be duplicated across AEON-family consumers such as AEOS, SANSA, Tonics, and future runtime or storage layers.

## 2. Motivation

Several ecosystem components need the same value behavior.

| Concept | AEOS | SANSA | Tonics |
| --- | --- | --- | --- |
| Numeric ordering | range validation | `<`, `>`, `order by` | runtime comparisons |
| String ordering | pattern and range validation | comparison, `order by` | sorting |
| Type conversion | coercion profiles | conversion functions | materialization |
| Cardinality | presence constraints | `exists`, `count` candidates | collection handling |
| Length | string/list validation | `length` candidates | runtime APIs |

These contracts describe values themselves. They do not belong exclusively to any one consumer.

If each consumer defines its own comparison, conversion, ordering, measurement, and arithmetic behavior, the ecosystem will drift. A query, a schema, and a runtime object may then disagree about the same value.

## 3. Architectural Position

The AEON ecosystem separates representation, shared value behavior, and consumer-specific application:

```text
AEON Core
  |
  v
Shared AEON Value Semantics
  |
  +-- AEOS
  +-- SANSA
  +-- Tonics
  +-- future ecosystem components
```

### 3.1 AEON Core

AEON Core defines:

- lexical grammar;
- value families;
- parsing;
- Assignment Event Stream;
- canonical representation.

Core does not define broad semantic behavior such as ordering domains, conversion policy, locale-sensitive collation, or arithmetic.

### 3.2 Shared Value Semantics

Shared Value Semantics defines:

- equality domains;
- comparison domains;
- ordering contracts;
- string and collation profiles;
- conversion contracts;
- measurement contracts;
- future arithmetic domains.

Shared Value Semantics begins only after a valid value representation exists.

### 3.3 Consumers

Consumers apply shared semantic contracts to their own domains:

- AEOS validates whether represented values satisfy schema/profile constraints.
- SANSA.Query evaluates query expressions over resolved semantic bindings.
- Tonics materialize validated values into runtime environments.
- Storage and transport layers may use shared semantics for indexing, sorting, and compatibility checks.

Consumers own their domain logic. They do not redefine the shared operation itself.

## 4. Ownership

The following concepts belong to Shared Value Semantics.

### 4.1 Equality Domains

Equality domains define:

- which value families may compare for equality;
- exact equality semantics within a family;
- cross-family equality rules, when any are allowed;
- behavior for explicit absence values, nulls, NaN, infinity, and other special values.

Consumers reference equality domains rather than defining local equality behavior.

### 4.2 Comparison Domains

Comparison domains define relational comparison for values such as:

- numbers;
- strings;
- dates;
- times;
- datetimes;
- instants;
- future domain-specific values.

Consumers use these domains for:

```text
where .age > 18
order by .name
min(...)
max(...)
range validation
```

Where no comparison domain is defined, comparison must fail closed with a deterministic diagnostic.

### 4.3 Ordering and Collation Contracts

String ordering belongs to Shared Value Semantics, not to SANSA.Query alone.

Collation profiles define how text is compared for ordering. A profile must be:

- deterministic;
- platform independent;
- versionable;
- explicit;
- independent of host operating-system locale defaults.

A canonical locale-independent profile should provide a stable default. Locale-aware, natural-sort, and domain-specific ordering profiles may be defined later as named profiles.

Consumer syntax such as:

```text
order by .name
```

uses the active value-semantics ordering profile. Future syntax may allow an explicit profile selection, but profile selection is separate from defining what the profile means.

### 4.4 String Case Mapping

Case mapping belongs beside string ordering because it raises the same Unicode, locale, normalization, and profile-selection questions.

Functions such as:

```text
lower(...)
upper(...)
```

must use a deterministic string case-mapping contract. An implementation slice may temporarily use host runtime Unicode case mapping, but normative behavior must not depend on process locale, operating-system locale, database collation, or host-language defaults.

### 4.5 Conversion Contracts

Conversion contracts define deterministic conversion between value families.

Examples:

```text
number("42")
string(42)
date("2026-07-21")
```

Each conversion must reuse the lexical contract already defined by AEON Core. Consumers must not define alternative parsing rules for the same conversion.

### 4.6 Measurement Contracts

Measurement contracts define deterministic measurements such as:

```text
length(...)
count(...)
```

Examples include string length, collection count, byte length, and domain-specific measurements.

The measurement unit must be explicit in the contract. For example, string length may mean Unicode scalar count, grapheme-cluster count, byte count, or another profile-defined measure; consumers must not silently choose different meanings.

### 4.7 Arithmetic Domains

Arithmetic is a future value-semantics area.

Potential operations include:

```text
+
-
*
/
sum(...)
average(...)
median(...)
```

Arithmetic domains belong to Shared Value Semantics so that query evaluation, validation, materialization, and future computation layers do not invent incompatible numeric behavior.

## 5. Reuse Principle

Every semantic contract should exist exactly once.

For example:

```text
AEON numeric grammar
  |
  v
Number Conversion Contract
  |
  +-- AEOS coercion
  +-- SANSA number(...)
  +-- Tonics materialization
```

All consumers observe identical behavior.

Whenever a semantic operation derives, compares, orders, converts, measures, or combines values, it should reference the shared Value Semantics contract.

Consumers must not define equivalent behavior locally when a shared contract exists.

## 6. Profiles

Profiles extend or select semantic behavior without changing the core contract.

Examples:

- canonical string ordering;
- locale-specific collation;
- natural numeric-region sorting;
- decimal precision policy;
- temporal comparison policy;
- domain-specific conversion surfaces.

Profiles must be deterministic and versionable. A profile must not introduce executable behavior into documents.

Consumers may restrict which profiles they accept.

### 6.1 Profile Selection

The active value-semantics context is selected by the consumer, runtime, schema profile, or trusted host configuration.

Documents may carry values that become inputs to semantic operations, but a document must not grant itself a more permissive semantic profile. Profile selection is an authority-bearing consumer boundary, not a document-level escape hatch.

A consumer must make profile selection explicit when behavior would otherwise depend on:

- process locale;
- operating-system locale;
- database collation;
- host-language comparison defaults;
- installed Unicode, ICU, CLDR, or timezone database versions.

Implementations must not silently inherit those host defaults as normative AEON behavior unless the inherited behavior is identified as part of a named, versioned profile.

### 6.2 Profile Advertisement

Consumers should advertise the value-semantics profiles they support.

Example profile identifiers:

```text
aeon.value.minimum.v1
aeon.value.string.codepoint.v1
aeon.value.string.case.default.v1
aeon.value.temporal.iso8601.v1
```

Profile identifiers are examples until promoted by a focused contract document. Implementations may expose local profile identifiers, but local identifiers should be clearly marked as non-portable.

### 6.3 Failure Without an Active Contract

Profile-dependent operations fail closed when no active contract defines their behavior.

This includes:

- string ordering;
- locale-aware string comparison;
- temporal comparison;
- case mapping;
- string-to-temporal conversion;
- numeric, decimal, or version-like natural sorting.

Consumers must report a deterministic diagnostic rather than falling back to host defaults.

### 6.4 AEON-Shaped Configuration

Consumer configuration may be represented as ordinary AEON data.

For example:

```aeon
valueSemantics:object = {
  profiles:list<string> = [
    "aeon.value.minimum.v1"
    "aeon.value.string.codepoint.v1"
    "aeon.value.temporal.iso8601.v1"
  ]
  stringOrder:object = {
    profile:string = "aeon.value.string.codepoint.v1"
  }
  temporal:object = {
    profile:string = "aeon.value.temporal.iso8601.v1"
    timezoneAuthority:string = "iana"
    tzdbVersion:string = "2026a"
  }
}
```

This shape is illustrative until a profile-configuration contract is promoted. The important boundary is authority: a trusted consumer, schema profile, runtime, or host configuration may select this context; an arbitrary document being queried or mutated does not select its own value-semantics authority.

### 6.5 Value Family Semantic Classification

AEON Core value families do not all enter the same semantic domain.

Some families have intrinsic shared semantics. Some reuse a shared string, numeric, temporal, or structural contract. Others are only lexical carriers until a consumer, schema, convention, or profile selects a more specific interpretation.

A consumer must not treat every represented payload as a string merely because it has a textual source form. Textual transport and semantic string behavior are different contracts.

Initial classification:

| AEON family or label | Semantic basis | Minimum shared behavior | Profile or consumer surface |
| --- | --- | --- | --- |
| `string` | string | exact decoded string equality; string ordering only through active string profile | locale collation, natural sort, normalization, case mapping |
| `trimtick`, `prose` | string plus formatting convention | string value after trimtick normalization | prose format semantics such as Markdown belong to conventions or applications |
| `number` | numeric | finite numeric equality and ordering | integer-only, unsigned-only, width, precision, decimal policy, arithmetic |
| `int`, `uint`, `int32`, `float64`, and other reserved numeric labels | numeric plus profile/schema constraints | inherit finite numeric comparison after compatibility is established | range, width, signedness, integer-only, float-family behavior |
| `infinity` | numeric special value | equality and ordering only where active numeric profile admits infinities | domain parameter such as `infinity<speedofmass>` is profile/schema-defined |
| `nan` | numeric special non-value | not equality-comparable or orderable in the minimum profile | explicit predicates and domain-specific missing/error semantics |
| `boolean` | Boolean | Boolean equality | Boolean ordering is not in the minimum profile |
| `toggle` | toggle | exact toggle-domain equality when exposed as toggle | conversion or materialization to Boolean is profile-defined; no implicit Boolean comparison |
| `null` and null reasons | absence/null | explicit null identity and reason preservation | null equality, null ordering, and absence-domain meaning are profile/schema-defined |
| `hex` | lexical structured scalar | exact payload preservation | color, byte sequence, identifier, numeric, or other interpretation is profile-defined |
| `radix`, `radix2`, `radix8`, and related labels | radix numeric representation | exact representation preservation; base metadata preservation | base-specific numeric validity, conversion, equality, and ordering are profile-defined |
| `encoding`, `base64`, `embed`, `inline` | encoded payload | exact payload preservation | byte identity, media type, decoding, hashing, or ordering are profile-defined |
| `date` | temporal | literal recognition and preservation | equality, ordering, precision, calendar, and conversion require an active temporal profile |
| `time` | temporal | literal recognition and preservation | equality, ordering, offset handling, and date-context rules require an active temporal profile |
| `datetime` | temporal | literal recognition and preservation | equality, ordering, offset normalization, precision, and instant semantics require an active temporal profile |
| `zrut` | temporal with named-zone data | literal recognition and zone payload preservation | equality and ordering require a named-zone authority and timezone database profile |
| `sep`, `kadot` | separator-structured lexical scalar | literal-family recognition and raw payload preservation | IP address, semantic version, dimensions, product codes, and similar meanings are profile-defined |
| `sansa` | address expression | address literal parsing and preservation | resolution, selector expansion, canonical-address equality, authorization, and qualifier meaning belong to SANSA consumers |
| `object`, `obj`, `o`, `envelope` | structural container | member identity and Core object shape | deep equality, ordering, envelope meaning, and member-value constraints are profile/schema-defined |
| `list` | structural collection | element order preservation and index-addressability | whether order is semantically meaningful, element constraints, and deep equality are profile/schema-defined |
| `tuple` | positional structural collection | positional element preservation | arity, element constraints, positional meaning, and tuple equality are profile/schema-defined |
| `node` | tagged structural value | tag, attributes, child order, and child slots are preserved | tag vocabulary, child-content semantics, rendering, and deep equality are profile/schema-defined |
| clone reference `~...` | reference operation | Core reference legality and resolved clone behavior | post-resolution value semantics apply to the resolved value |
| pointer reference `~>...` | reference operation | Core reference legality and pointer identity preservation | aliasing, mutation authority, and dereference behavior belong to consumers/profiles |
| custom datatype labels | host/profile semantic claim over a Core-compatible value family | no shared meaning by label alone | consumer, schema, convention, or profile defines accepted semantics |

Separator literals illustrate why this classification is necessary:

```aeon
ip:kadot = ^192.3.3.222
dim:sep[x] = ^300x250
semver:kadot = ^3.14.15
```

All three values share separator-literal mechanics. They do not share one ordering contract.

An IP profile might compare numeric address components. A dimensions profile might compare width, height, area, or aspect ratio. A semantic-version profile might compare major, minor, and patch segments with version-specific pre-release rules. A generic string collation profile is not a safe fallback for any of those meanings unless the consumer explicitly selects string treatment.

When no active shared or profile-defined semantic basis exists for an operation, the operation fails closed.

## 7. Minimum v1 Consumer Contract

The first shared contract should cover the behavior already exercised by SANSA.Query and expected by AEOS-style validation.

This section is a candidate minimum profile. It is intentionally small and should become the first shared CTS surface when promoted.

### 7.1 Scalar Value Categories

The minimum profile recognizes these scalar categories:

- finite number;
- positive infinity;
- negative infinity;
- NaN;
- string;
- Boolean;
- explicit null;
- explicit absence value, when exposed by a consumer;
- missing binding, when resolution produces no binding.

Missing binding is not a value. It is an evaluation state produced by a consumer such as SANSA.Resolve or AEOS path selection.

Explicit null and explicit absence values are values. They must not be collapsed into missing, false, an empty string, or zero.

For minimum-profile consumer predicates, an **ordinary scalar value** means one finite number, string, or Boolean value. Positive infinity, negative infinity, NaN, explicit null, explicit absence values, containers, Binding Sets, and Missing are not ordinary scalar values unless a later profile explicitly widens that predicate.

### 7.2 Equality

The minimum equality surface is:

| Operands | Equality | Notes |
| --- | --- | --- |
| finite number and finite number | allowed | Numeric value equality. |
| infinity and finite number | allowed | Positive and negative infinity are not equal to finite numeric values. |
| infinity and infinity | allowed | Positive infinity equals positive infinity; negative infinity equals negative infinity; opposite infinities are not equal. |
| string and string | allowed | Exact decoded string equality under the active string equality profile. |
| Boolean and Boolean | allowed | `true` equals `true`; `false` equals `false`. |
| explicit null | profile-defined or error | Consumers must use an explicit contract such as `isNull(...)` when no equality contract is active. |
| explicit absence value | profile-defined or error | Absence-value equality belongs to the applicable absence-value contract. |
| NaN | error | NaN is not equality-comparable in the minimum profile; equality and inequality tests over NaN fail closed. |
| mixed categories | error | No implicit coercion. |

Consumers must not coerce strings, numbers, Booleans, nulls, or absence values to make equality succeed.

### 7.3 Ordering

The minimum ordering surface is:

| Operands | Ordering | Notes |
| --- | --- | --- |
| finite number and finite number | allowed | Numeric order. |
| infinity and finite number | allowed | Negative infinity sorts before finite numbers; positive infinity sorts after finite numbers. |
| infinity and infinity | allowed | Equal infinities compare equal; negative infinity sorts before positive infinity. |
| string and string | allowed | Uses the active string ordering profile. |
| Boolean and Boolean | error | Boolean ordering is not part of the minimum profile. |
| explicit null | error | Use explicit null predicates or profile-defined null ordering. |
| explicit absence value | error | Use explicit absence predicates or profile-defined absence ordering. |
| NaN | error | NaN is not orderable. |
| mixed categories | error | No implicit coercion. |

Ordering must fail closed when the active profile does not define the compared category pair.

### 7.4 Value Predicate Basis

Consumers may expose predicates that classify scalar evaluation results. Those predicates should be defined in terms of the shared scalar categories rather than by host-language truthiness.

For example, a minimum-profile `isValue(...)` predicate should return true for exactly one ordinary scalar value and false for Missing, explicit null, explicit absence values, NaN, infinity, non-scalar containers, and Binding Sets. A predicate that needs to accept infinity, null, or a specific absence value should use a distinct name or a profile-defined contract.

### 7.5 Canonical String Profile Placeholder

The minimum profile requires a deterministic string equality and ordering profile, but this proposal does not yet define the final collation algorithm.

Until that algorithm is promoted, consumers should treat string ordering as a named value-semantics dependency rather than redefining it locally.

The canonical string profile must eventually define:

- Unicode unit of comparison;
- normalization policy;
- case sensitivity;
- accent and combining-mark behavior;
- total-order tie breakers;
- behavior for invalid or unpaired Unicode representations, if exposed by a host.

Locale-aware, natural-sort, and domain-specific profiles remain future extensions.

### 7.6 Canonical Codepoint String Profile Candidate

The first portable string ordering candidate is a codepoint profile.

Candidate identifier:

```text
aeon.value.string.codepoint.v1
```

The candidate profile orders strings by decoded Unicode scalar values from left to right.

The candidate profile:

- performs no normalization;
- performs no case folding;
- does not ignore accents, combining marks, punctuation, or whitespace;
- compares each decoded scalar value numerically;
- sorts the shorter string first when every shared scalar compares equal.

Exact string equality compares the decoded scalar sequence exactly.

This profile is a stable portability floor. It is not intended to model human-language collation.

### 7.7 String Collation Profile Framework

Richer string ordering profiles must define the full ordering contract they apply.

A string collation profile should define:

- normalization behavior before comparison;
- case-sensitive or case-insensitive behavior;
- accent and combining-mark behavior;
- ignored characters, if any;
- punctuation grouping;
- contraction and expansion rules;
- numeric-region recognition;
- decimal, version-like, or segmented-number behavior;
- tie-breaker behavior when primary comparison keys match.

Numeric-looking regions must not require fixed-width machine-number conversion. Profiles that support natural sorting should compare numeric regions by a deterministic arbitrary-precision or digit-sequence algorithm.

For example, a natural-sort profile must explicitly define whether:

```text
job-2 < job-10
1.10 < 1.2
```

and why.

### 7.8 Case Mapping

The minimum case-mapping surface is:

```text
lower(string) -> string
upper(string) -> string
```

Case mapping is deterministic and profile-defined. It must not depend on process locale, operating-system locale, database collation, or host-language defaults.

The canonical case-mapping profile must eventually define:

- Unicode case-mapping table or referenced version;
- locale-sensitive exceptions, if any;
- normalization behavior before and after mapping;
- whether one input scalar may expand to multiple output scalars.

Until the canonical case-mapping profile is locked, consumer implementations may expose `lower(...)` or `upper(...)` as implementation-slice behavior, but should document that normative behavior is still owned by Shared Value Semantics.

### 7.9 Temporal Profile Candidate

AEON Core recognizes temporal datatype names such as:

- `date`;
- `time`;
- `datetime`;
- `zrut`.

Shared Value Semantics must define temporal comparison before consumers rely on temporal ordering, validation, or mutation compatibility.

Candidate identifier:

```text
aeon.value.temporal.iso8601.v1
```

A temporal profile should define:

- recognized temporal categories;
- equality and ordering domains for each category;
- whether cross-category comparison is allowed;
- normalization before comparison;
- relationship to applicable temporal conventions such as `aeon.gp.temporal.v1`;
- timezone offset behavior;
- named-zone authority and timezone database version, when applicable;
- precision and fractional-second behavior;
- diagnostics for unsupported or ambiguous temporal values.

A conservative temporal comparison surface is:

| Operands | Equality | Ordering | Notes |
| --- | --- | --- | --- |
| date and date | profile-defined | profile-defined | Calendar-date comparison. |
| time and time | profile-defined | profile-defined | Time-of-day comparison only when the profile does not require date or timezone context. |
| datetime and datetime | profile-defined | profile-defined | The profile must define offset and instant normalization. |
| zrut and zrut | profile-defined | profile-defined | Requires a named-zone authority and versioned timezone database. |
| temporal and string | error | error | No implicit string comparison. |
| mixed temporal categories | error | error | Allowed only when a profile explicitly defines cross-category comparison. |

Temporal transport as text does not imply string comparison. Without an active temporal profile, temporal comparison and temporal ordering fail closed.

### 7.10 Mutation Compatibility

Future mutation operations should consume the same Shared Value Semantics contracts used by query and validation.

Mutation compatibility includes:

- whether a write value is compatible with a target datatype;
- whether conversion is allowed;
- which normalization, if any, is applied before storage;
- how null, absence values, and Missing interact with a write target;
- how temporal precision, timezone offsets, and named zones are preserved or normalized.

SANSA.Mutate, AEOS, Tonics, and storage adapters should not define separate compatibility behavior for the same AEON value family.

For example:

```text
set $.invoice.dueDate:date = 2026-07-24
```

SANSA.Mutate identifies the target and operation. AEON Core parses the represented value. Shared Value Semantics decides whether the represented value is compatible with `date` and what normalization, if any, is required. The host or schema authority decides whether the mutation is authorized.

### 7.11 Consumer Handoff

Consumers own where an operation appears and what diagnostic context is produced.

Shared Value Semantics owns what the operation means.

For example:

```text
where .age > 18
```

SANSA.Query owns `where`, candidate filtering, Binding Set handling, and query diagnostics. Shared Value Semantics owns numeric comparison.

For example:

```text
age minimum 18
```

AEOS owns the schema rule and validation diagnostic. Shared Value Semantics owns numeric comparison.

## 8. CTS Ownership

Shared Value Semantics should have its own conformance coverage once individual contracts become normative.

The proposal-stage CTS scaffold is:

```text
aeonite-cts/cts/value-semantics/v1/value-semantics-cts.v1.json
aeonite-cts/cts/value-semantics/v1/suites/01-minimum-consumer-contract.json
```

Shared CTS cases can then be reused by consumers:

```text
AEON literal fixture
  |
  v
Value Semantics contract
  |
  +-- AEOS validation case
  +-- SANSA query case
  +-- Tonics materialization case
```

This keeps conformance behavior aligned across implementations without duplicating normative definitions.

## 9. Non-Goals

This proposal does not yet define:

- the complete numeric comparison contract;
- the final canonical string collation algorithm beyond the codepoint candidate;
- final locale profile identifiers;
- final temporal profile identifiers or timezone database authority;
- conversion syntax in any consumer;
- arithmetic operators;
- consumer-specific authorization;
- runtime APIs.

Those belong in focused follow-up proposals or contract documents.

## 10. Relationship to SANSA.Query

SANSA.Query is the first AEON-family consumer that exercises a broad portion of shared value behavior.

SANSA.Query should reference Shared AEON Value Semantics for:

- scalar equality;
- relational comparison;
- string ordering;
- case mapping;
- conversion functions;
- measurement functions;
- future arithmetic or aggregation.

SANSA.Query still owns query syntax, Binding Set evaluation, candidate filtering, projection, result construction, diagnostics, and resolver integration.

## 11. Relationship to AEOS

AEOS consumes Shared Value Semantics when validating value relationships.

For example, an AEOS rule may require:

```text
age > 18
```

AEOS owns the validation rule and diagnostic context. Shared Value Semantics owns what numeric comparison means.

## 12. Relationship to Tonics

Tonics consume Shared Value Semantics when materializing values into runtime environments.

Tonics may expose runtime-specific APIs, but the behavior of shared conversions, comparisons, measurements, and ordering must remain aligned with the shared contracts unless a profile explicitly defines a different accepted surface.

## 13. Design Philosophy

AEON Core defines representation.

Shared AEON Value Semantics defines deterministic behavior.

Consumers apply that behavior to their own domains.

This keeps representation, validation, evaluation, materialization, and future computation separated while preserving one semantic contract for every value family.
