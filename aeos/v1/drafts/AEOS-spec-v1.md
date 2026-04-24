---
id: aeos-v1
title: AEOS Specification v1
description: Validation-layer specification for AEOS, covering schema authority, active-schema evaluation, diagnostics, and result-envelope rules.
group: Core Specifications
path: specification/aeon-v1-documentation/aeos-specification-v1
links:
  - aeon-core-v1
  - aeon-core-v1-compliance
  - aeon-v1-contracts
---

# AEOS Specification v1

Status: official v1 normative spec  
Scope: AEOS validation contract, active schema model, result envelope, and phase authority boundaries for AEON v1.

## 1. What AEOS Is

AEOS is the schema and representation-validation layer for AEON.

AEOS operates on AES, not on raw source text. It validates representational form and schema-declared constraints after AEON Core has already completed:
- lexing
- parsing
- canonical path assignment
- reference legality

AEOS does not redefine Core behavior. It consumes Core output.

## 2. Authority Boundary

### 2.1 AEON Core Owns

AEON Core is authoritative for:
- lexical validity
- syntax validity
- canonical path assignment
- quoted-key and path disambiguation
- reference legality
  - missing targets
  - forward references
  - self-references
- mode/datatype enforcement at the Core layer

AEOS must not repeat or reinterpret those checks as if they were schema failures.

### 2.2 AEOS Owns

AEOS is authoritative for:
- rule-index validation
- presence checks
- representational type checks
- reference-form constraints on Core-emitted reference kinds
- reference-target constraints on Core-emitted target paths
- container-kind and arity checks
- numeric lexical-form checks
- string length and pattern checks
- datatype allowlist membership checks when configured in schema
- bounded resolved-endpoint validation when explicitly enabled by schema
- result-envelope emission

### 2.3 AEOS Does Not Own

AEOS must not:
- coerce values
- inject defaults
- mutate AES
- execute schema-side code
- impose domain/business semantics beyond the active schema constraint surface

Exception:
- when the active schema explicitly declares exact numeric bounds such as `min_value` or `max_value`,
  AEOS may compare numeric magnitudes to enforce those declared constraints.
- when a rule declares `resolve_reference_form: true`, AEOS may follow a bounded reference chain
  structurally in order to validate the terminal literal form against the referencing path.
  This does not transfer Core legality ownership, mutate AES, or authorize schema inheritance
  from the referenced path.

## 3. Inputs

AEOS validator input consists of:
- AES
- SchemaV1
- optional validator options

### 3.1 AES Input

AEOS consumes AES events keyed by canonical paths.

Relevant AEOS assumptions:
- canonical `path` is authoritative;
- `datatype` may be present or absent;
- `value.type` carries the Core-emitted literal/container/reference kind;
- `span` may be present as Core span data or tuple form.

Reference-bearing AES events may still be present in the stream, but AEOS treats their legality as already decided by Core. AEOS may validate schema constraints against the emitted reference kind, but it must not reinterpret missing-target, forward-reference, or self-reference conditions as schema failures.

### 3.2 Schema Contract Boundary

There are two schema layers to distinguish:

1. Contract document layer
- used by CLI/runtime contract loading
- canonical authoring form is an AEON `.aeos` document with top-level binding `aeos:schema`
- canonical path for the contract object is `$.aeos`
- the binding at `$.aeos` MUST carry datatype/type annotation `schema`
- canonical document fields:
 - `id`
  - `version`
  - `rules`
  - optional `world`
  - optional `reference_policy`
  - optional `datatype_allowlist`
  - optional `datatype_rules`
- authoring-oriented helper fields may also appear at this layer so long as they are projected away before validation
  - example: `reference_target_path`

3. Document header schema declaration layer
- used by documents that declare intended schema contracts in `aeon:header`
- canonical fields:
  - `schema`
  - optional `schemas`
- `schema` is singular and identifies the primary schema id declared by the document producer
- `schemas` is an optional object mapping named contexts to additional declared schema associations
  - recommended reserved keys:
    - `authoring`
    - `validation`
  - recommended custom keys use identifier-safe names with `_` separators
    - example: `vendor_acme`
- `schemas` entries are named associations, not cumulative instructions
- header schema declarations are descriptive metadata only; they do not dictate consumer processing behavior
- a consumer MAY choose to apply `schema`, MAY choose a context-specific entry from `schemas`, MAY ignore the declaration entirely, or MAY enforce a local schema instead
- when a consumer does select among declared header schema ids, `schema` is the default fallback when no context-specific association is used

2. In-memory `SchemaV1` validator layer
- the object actually consumed by `validate(aes, schema, options)`
- current shipped validator shape:

```ts
interface SchemaV1 {
  readonly rules: readonly SchemaRule[];
  readonly world?: 'open' | 'closed';
  readonly reference_policy?: 'allow' | 'forbid';
  readonly datatype_allowlist?: readonly string[];
  readonly datatype_rules?: Readonly<Record<string, ConstraintsV1>>;
}
```

The `.aeos` contract wrapper is handled before AEOS validation begins. AEOS validation itself operates on the in-memory schema object.
Loaders MUST parse the `.aeos` file as AEON, materialize the object at `$.aeos`, validate the document contract,
and project it into `SchemaV1` before invoking `validate(aes, schema, options)`.
Document header schema declarations are a separate concern from `.aeos` schema documents: they identify which schema id
the document declares for a given context, but they do not change the runtime `SchemaV1` shape and they do not prescribe how any consumer must process the document.

## 4. Active Schema Model

### 4.1 SchemaV1

Current normative validator model:

```ts
interface SchemaV1 {
  readonly rules: readonly SchemaRule[];
  readonly world?: 'open' | 'closed';
  readonly reference_policy?: 'allow' | 'forbid';
  readonly datatype_allowlist?: readonly string[];
  readonly datatype_rules?: Readonly<Record<string, ConstraintsV1>>;
}
```

### 4.2 SchemaRule

```ts
interface SchemaRule {
  readonly path: string;
  readonly constraints: ConstraintsV1;
}
```

Rules are keyed by canonical path strings.

### 4.3 ConstraintsV1

Active shipped constraint surface:

```ts
interface ConstraintsV1 {
  readonly required?: boolean;
  readonly type?: string;
  readonly reference?: 'allow' | 'forbid' | 'require';
  readonly reference_kind?: 'clone' | 'pointer' | 'either';
  readonly reference_target_pattern?: string;
  readonly resolve_reference_form?: boolean;
  readonly type_is?: 'list' | 'tuple';
  readonly length_exact?: number;
  readonly sign?: 'signed' | 'unsigned';
  readonly min_digits?: number;
  readonly max_digits?: number;
  readonly min_value?: string;
  readonly max_value?: string;
  readonly min_length?: number;
  readonly max_length?: number;
  readonly pattern?: string;
  readonly datatype?: string;
}
```

Unknown constraint keys are schema errors.

Additional schema-surface notes:
- `reference_policy?: 'allow' | 'forbid'` is a schema-wide form control.
- `.aeos` is the canonical authoring extension for schema documents; `SchemaV1` remains the canonical runtime object.
- `reference` and `reference_kind` constrain Core-emitted reference kinds without resolving them.
- `reference_kind` is valid only when `reference: 'require'`.
- `reference_target_path` is the preferred `.aeos` authoring constraint for target-domain matching.
- `reference_target_pattern` constrains the canonical target path declared by a reference.
- `resolve_reference_form` is boolean and opt-in.
- `reference_target_pattern` and `resolve_reference_form` are invalid when paired with `reference: 'forbid'`.
- `resolve_reference_form` is invalid when the rule still expects a reference type such as `CloneReference`
  or `PointerReference`.

## 5. Constraint Semantics

### 5.1 `required`

`required: true` means the canonical path must exist in AES.

Failure diagnostic:
- `missing_required_field`

Missing-path diagnostics use `span: null`.

### 5.2 `type`

`type` checks Core-emitted value kind.

Representative accepted names include:
- `StringLiteral`
- `BooleanLiteral`
- `NullLiteral`
- `NumberLiteral`
- `IntegerLiteral`
- `FloatLiteral`
- `ObjectNode`
- `ListNode`
- `TupleLiteral`
- `CloneReference`
- `PointerReference`

Current aliasing behavior:
- `NumberLiteral` satisfies `NumberLiteral`
- `IntegerLiteral` and `FloatLiteral` are distinguished from the raw numeric lexical form

Failure diagnostics:
- `type_mismatch`
- `tuple_element_type_mismatch` for indexed tuple/list element paths

Reference-form notes:
- `type: CloneReference` requires a clone reference at the constrained path.
- `type: PointerReference` requires a pointer reference at the constrained path.
- `reference: 'require'` accepts either `CloneReference` or `PointerReference`.
- `reference: 'forbid'` rejects both `CloneReference` and `PointerReference`.
- `reference_kind: 'clone' | 'pointer' | 'either'` refines `reference: 'require'` without evaluating the target.
- `reference_policy: 'forbid'` rejects reference-bearing AES events schema-wide.

### 5.3 `reference_target_pattern`

Target-domain constraint for reference-bearing paths:

```ts
reference_target_pattern?: string
```

Behavior:
- applies only to Core-emitted `CloneReference` and `PointerReference` events;
- validates the canonical target path string declared by the reference;
- does not resolve the referenced value;
- uses canonical formatting for quoted members, indexes, and attribute segments before matching.

Failure diagnostic:
- `reference_target_mismatch`

Schema-validation failures:
- `invalid_reference_constraint` for non-string patterns, invalid regexes, or contradictory combinations.

Authoring note:
- `.aeos` documents SHOULD prefer `reference_target_path` where the allowed target domain can be expressed
  as a path selector such as `$.ages[*]`.
- Loaders MUST project that selector into an equivalent internal target-matching form before AEOS validation.

### 5.4 `resolve_reference_form`

Opt-in resolved-endpoint validation:

```ts
resolve_reference_form?: boolean
```

Behavior:
- when `true`, AEOS may follow a bounded reference chain from the constrained path to its terminal literal endpoint;
- literal-form constraints such as `type`, `min_value`, `max_value`, `min_length`, `max_length`, `pattern`,
  and datatype-rule checks apply to the resolved terminal literal form;
- reference-form constraints such as `reference`, `reference_kind`, and `reference_target_pattern` continue to
  apply to the original reference event at the constrained path;
- AEOS does not mutate AES, inherit target-path schema obligations, or reinterpret Core legality failures.

Boundary notes:
- missing targets, forward references, self-references, and other Core legality failures remain Core-owned;
- cyclic or otherwise unresolvable chains do not become new AEOS schema errors merely because
  `resolve_reference_form` is enabled;
- resolved-endpoint validation is bounded and deterministic.

Schema-validation failures:
- `invalid_reference_constraint` for non-boolean values or contradictory combinations.

### 5.5 `type_is`

Container kind constraint:

```ts
type_is?: 'list' | 'tuple'
```

Behavior:
- `list` accepts `ListNode` / `ListLiteral`
- `tuple` accepts `TupleLiteral`

Failure diagnostic:
- `wrong_container_kind`

### 5.6 `length_exact`

Exact container arity constraint for tuple/list style containers.

Failure diagnostic:
- `tuple_arity_mismatch`

### 5.7 Numeric Form Constraints

Numeric lexical-form constraints:
- `sign`
- `min_digits`
- `max_digits`
- `min_value`
- `max_value`

Behavior:
- applies only to numeric literal forms;
- uses lexical representation for sign and digit-count checks;
- uses numeric magnitude only when `min_value` or `max_value` are explicitly declared;
- integer digit count excludes sign.

Failure diagnostic:
- `numeric_form_violation`

### 5.8 String Form Constraints

String constraints:
- `min_length`
- `max_length`
- `pattern`

Length semantics:
- measured in UTF-16 code units (`JavaScript string.length`)

Pattern semantics:
- ECMAScript regex strings
- full-string match semantics
- if anchors are omitted, AEOS adds `^` and `$`

Failure diagnostics:
- `string_length_violation`
- `pattern_mismatch`

### 5.9 `datatype`

Datatype constraint is a label-presence check only.

It does not perform semantic subtype reasoning. It validates the declared datatype string carried by AES when the rule requests one.

### 5.10 `datatype_allowlist`

Optional schema-level allowlist:

```ts
datatype_allowlist?: readonly string[]
```

Behavior:
- if present, any rule using `constraints.datatype` must reference an allowed datatype string;
- this is membership checking only.

Failure diagnostic:
- `datatype_allowlist_reject`

### 5.11 `world`

Optional schema-level world policy:

```ts
world?: 'open' | 'closed'
```

Behavior:
- `open` is the default;
- `open` validates declared schema rules and ignores unexpected AES binding paths;
- `closed` rejects any non-header AES binding path not explicitly covered by `schema.rules`;
- rejection happens before downstream materialization is trusted.

Failure diagnostic:
- `unexpected_binding`

### 5.12 `datatype_rules`

Optional schema-level datatype semantics:

```ts
datatype_rules?: Readonly<Record<string, ConstraintsV1>>
```

Behavior:
- keys are datatype base labels such as `uint`, `int32`, or `float64`;
- when an AES event carries a matching declared datatype, the mapped constraints are applied in addition to any path rule;
- this is how `aeon.gp.schema.v1` makes reserved numeric labels operational without moving those semantics into Core.

Typical uses:
- `uint` => `type = "IntegerLiteral"`, `sign = "unsigned"`
- `int32` => `type = "IntegerLiteral"`, `min_value = "-2147483648"`, `max_value = "2147483647"`
- `float32` => `type = "FloatLiteral"`

## 6. Validation Phases

Current shipped validator phases:

1. Envelope plumbing
2. Baseline invariants
3. Rule-index build / schema-shape validation
4. Presence checks
5. Type and reference checks
6. Container-kind checks
7. Numeric form checks
8. String form and pattern checks
9. Datatype allowlist enforcement during rule indexing
10. World-policy enforcement
11. Datatype-rule enforcement
12. Guarantees emission

### 6.1 Baseline Invariants

Active baseline checks include:
- duplicate AES binding paths
- invalid index segment shape in canonical paths
- optional trailing separator-delimiter policy

Active baseline checks do not include reference-legality validation. Missing targets, forward references, and self-references remain Core-owned even when reference events are present in AES.

Failure diagnostics include:
- `duplicate_binding`
- `invalid_index_format`
- `trailing_separator_delimiter`

## 7. Result Envelope

AEOS produces exactly one output shape.

```ts
interface Diag {
  readonly path: string;
  readonly span: [number, number] | null;
  readonly message: string;
  readonly phase: 'schema_validation';
  readonly code: string;
}

interface ResultEnvelope {
  readonly ok: boolean;
  readonly errors: readonly Diag[];
  readonly warnings: readonly Diag[];
  readonly guarantees: Readonly<Record<string, readonly string[]>>;
}
```

Normative rules:
- `ok` is `true` only when `errors.length === 0`
- `warnings` do not flip `ok` to `false`
- envelope must not include AES input
- diagnostics use canonical path strings
- `phase` is currently fixed to `schema_validation`

### 7.1 Tooling Metadata Is Separate

Consumer tools may wrap AEOS results in larger command or editor payloads.
Those wrappers are not part of the core `ResultEnvelope` contract.

In particular:
- CLI or editor output may expose declared contract metadata read from `aeon:header`
- runtime bind flows may expose both declared and applied contract ids
- such metadata is consumer/tooling provenance, not AEOS validator state

One valid tooling pattern is:

```json
{
  "document": { "...": "..." },
  "meta": {
    "errors": [],
    "warnings": [],
    "contracts": {
      "declared": {
        "profile": "aeon.gp.profile.v1",
        "schema": "altopelago.main_schema.v1",
        "schemas": {
          "authoring": "altopelago.authoring_schema.v1"
        }
      },
      "applied": {
        "profile": "altopelago.core.v1",
        "schema": "altopelago.main_schema.v1"
      }
    }
  }
}
```

Interpretation:
- `declared` reflects producer-declared header metadata only
- `applied` reflects the contract ids actually selected by the consumer
- `inspect`-style read-only surfaces may expose only `declared`
- `bind`-style runtime surfaces may expose both `declared` and `applied`

## 8. Guarantees

AEOS guarantees are advisory representation tags keyed by canonical path.

Current shipped guarantees include tags such as:
- `present`
- `integer-representable`
- `float-representable`
- `boolean-representable`
- `non-empty-string`

Guarantees are emitted only on passing envelopes.

## 9. Validator Options

Current shipped validator options:

```ts
interface ValidateOptions {
  readonly strict?: boolean;
  readonly trailingSeparatorDelimiterPolicy?: 'off' | 'warn' | 'error';
}
```

### 9.1 `strict`

Reserved for future AEOS-specific behavior.

Current validator does not materially change rule semantics based on this flag.

### 9.2 `trailingSeparatorDelimiterPolicy`

Optional policy for separator literal payloads ending in a declared separator.

Modes:
- `off` (default): ignore
- `warn`: emit warning
- `error`: emit error

This policy does not change Core parsing semantics.

## 10. Diagnostics

Current standard AEOS diagnostic codes include:

### 10.1 Baseline / Schema
- `duplicate_binding`
- `rule_missing_path`
- `duplicate_rule_path`
- `unknown_constraint_key`
- `invalid_reference_constraint`

### 10.2 Presence / Type / Container
- `missing_required_field`
- `type_mismatch`
- `wrong_container_kind`
- `tuple_arity_mismatch`
- `tuple_element_type_mismatch`
- `invalid_index_format`
- `reference_forbidden`
- `reference_required`
- `reference_kind_mismatch`
- `reference_target_mismatch`

### 10.3 Numeric / String / Datatype
- `numeric_form_violation`
- `string_length_violation`
- `pattern_mismatch`
- `datatype_allowlist_reject`
- `trailing_separator_delimiter`
- `constraint_inapplicable`

Vendor-prefixed diagnostics may use:

```text
vendor:code
```

Reference-legality diagnostics such as missing-target, forward-reference, and self-reference failures belong to Core/AES, not to AEOS.

## 11. CLI / Runner Adapter

The shipped AEOS CTS adapter:
- reads JSON from stdin
- expects `{ aes, schema, options }`
- writes `ResultEnvelope` JSON to stdout

The adapter is read-only and must not mutate validator behavior.

## 12. CTS Mapping

AEOS conformance should be reviewed by behavior family rather than by isolated test file.

Current v1 behavior-family anchors:
- result-envelope and validator output contract
  - `cts/aeos/v1/suites/00-envelope.json`
- baseline invariants and Core-versus-AEOS authority boundary
  - `cts/aeos/v1/suites/01-baseline.json`
- schema rule-index integrity
  - `cts/aeos/v1/suites/02-schema-rules.json`
- presence and forbid semantics
  - `cts/aeos/v1/suites/03-presence.json`
- representational type and datatype-label constraints
  - `cts/aeos/v1/suites/04-type.json`
  - `cts/aeos/v1/suites/08-datatype-labels.json`
- reference-form, reference-target, and resolved-reference constraints
  - `cts/aeos/v1/suites/16-reference-forms.json`
  - `cts/aeos/v1/suites/17-reference-targets.json`
  - `cts/aeos/v1/suites/18-resolved-reference-form.json`
  - `cts/aeos/v1/suites/19-reference-security.json`
- numeric lexical-form constraints
  - `cts/aeos/v1/suites/05-numeric-form.json`
- string length and pattern constraints
  - `cts/aeos/v1/suites/06-string-form.json`
  - `cts/aeos/v1/suites/07-pattern.json`
- guarantee emission
  - `cts/aeos/v1/suites/09-guarantees.json`
- container-kind and tuple-arity constraints
  - `cts/aeos/v1/suites/10-container-kinds.json`
  - `cts/aeos/v1/suites/11-tuple-arity.json`
- indexed-path validation and tuple positional checks
  - `cts/aeos/v1/suites/12-tuple-positional.json`
  - `cts/aeos/v1/suites/13-indexed-path-validation.json`
- separator-literal policy enforcement
  - `cts/aeos/v1/suites/14-separator-literal-policy.json`
- structural container item validation
  - `cts/aeos/v1/suites/15-structural-container-items.json`

Protocol governance:
- `cts/protocol/v1/runner-contract.md`
- `cts/protocol/v1/lane-aeos.md`

### 12.1 Mapping rule

When AEOS CTS grows, new suites should strengthen one of the behavior families above or introduce a newly documented AEOS behavior family explicitly.

AEOS CTS should not expand as an unclassified test pile.

## 13. Conformance Notes

A conforming AEOS v1 implementation must:
- consume canonical Core/AES output rather than redefining Core semantics;
- support the active `SchemaV1` constraint surface documented here;
- emit the canonical `ResultEnvelope` shape;
- preserve deterministic canonical-path diagnostics;
- fail closed on validation errors.

### 13.1 Anti-drift requirement

AEOS conformance is not satisfied by passing only representative examples.

An implementation must preserve behavior across the AEOS validation families defined in this document and their corresponding CTS lanes, especially:
- schema rule validation
- presence checks
- type and datatype-label enforcement
- reference-form, reference-target, and resolved-reference enforcement
- numeric and string-form constraints
- container and indexed-path validation
- separator policy enforcement
- result-envelope and guarantee behavior

Core-owned semantics must remain Core-owned. AEOS must not reinterpret Core legality failures as schema-validation failures.
