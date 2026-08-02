---
id: sansa-v1-mutate
title: SANSA.Mutate v1
description: Proposal-stage boundary and conservative core model for deterministic semantic mutation intent.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/mutate
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-resolve
  - sansa-v1-query
  - sansa-v1-instruction
  - sansa-v1-conformance
  - sansa-v1-meaning-validation-integration
---

# SANSA.Mutate v1

Status: Proposal
Scope: authority-bearing mutation planning built on SANSA Addressing, Resolve, and restricted read-only predicate evaluation.

## 1. Overview

SANSA.Mutate describes intentional semantic change over a namespace.

It is not part of SANSA.Query. Query remains read-only. Mutate may consume SANSA addresses, Binding Sets, and Query-like preconditions, but mutation crosses a stronger trust boundary than read-only resolution or evaluation.

SANSA.Mutate produces deterministic change intent as an immutable mutation plan. It does not decide authorization, transaction semantics, storage layout, orchestration, migrations, retries, or conflict policy.

Human-authored SANSA Instruction syntax, if adopted, sits above this layer. An
instruction may combine Query-style selection with mutation verbs, but it must
lower into exact structured Mutate operations before consumer policy or
authorization, target-surface validation, and apply.

## 2. Design Principles

SANSA.Mutate should be:

- explicit about requested changes;
- deterministic before apply;
- authority-aware;
- precondition-driven;
- side-effect free during planning;
- separate from read-only Query;
- independent of host storage engines;
- compatible with ASP orchestration without becoming ASP.

SANSA.Mutate should not be:

- a database API;
- a transaction engine;
- an authorization system;
- a migration language;
- an execution language embedded in documents;
- a way to reinterpret runtime strings as executable SANSA source.

## 3. Capability Boundary

The capability stack remains:

```text
SANSA.Addressing
  defines address structure and selector vocabulary

SANSA.Resolve
  resolves addresses into ordered Binding Sets

SANSA.Query
  reads, filters, orders, slices, and projects bindings

SANSA.Mutate
  describes intended changes to addressed bindings

SANSA.Subscribe
  observes future changes affecting bindings or query results

SANSA.History
  inspects historical states, events, or revisions
```

Dynamic address activation is a shared facility, not a separate top-level capability. A structured SANSA Address Literal may supply a target to Resolve, Query, Mutate, Subscribe, or History, but runtime data must not become executable SANSA source text.

Example shared activation form:

```text
path($.<"params">.target)
```

Shared activation does not imply shared authority. Reading the parameter value
and resolving the activated address are separate authorization decisions. Each
consumer must apply its own host-supplied activation policy before target
resolution. AEOS or another validator may check whether a path-valued slot is
legal under an externally supplied schema, but SANSA.Mutate remains responsible
only for mutation intent and planning; neither the path value nor the document
being mutated may grant its own activation or mutation authority.

## 4. Conceptual Mutation Pipeline

A mutation-capable consumer distinguishes these phases:

```text
1. Target
   Resolve intended bindings against one namespace state.

2. Preconditions
   Evaluate restricted read-only predicates against that state.

3. Plan
   Freeze exact targets and produce an immutable mutation plan.

4. Consumer Policy / Authorization
   Consumer approves or denies each proposed operation.

5. Target Surface
   Validate that the planned operations can be represented by the intended
   host format or adapter surface.

6. Apply
   Consumer or adapter maps the plan to namespace changes.

7. Report
   Return affected bindings, resulting addresses, and diagnostics.
```

SANSA.Mutate owns the semantic contract for Target, Preconditions, Plan, and
portable result reporting. Consumer policy or authorization and target-surface
validation are post-plan checks. A host or tool may run them in either order,
provided both happen after the plan is inspectable and before apply. Physical
Apply behavior, transactions, storage behavior, and orchestration remain
consumer responsibilities.

For diagnostics and interoperable tooling, the post-plan authorization phase is
reported as `policy`. The phase name covers consumer policy, host
authorization, delegated approval checks, and other trusted authority decisions.
The `target` phase is reserved for target-surface representability failures.

Planning is side-effect free. An implementation must not partially apply changes
while it is still resolving targets, evaluating preconditions, or constructing a
plan.

## 5. Relationship To Query

Query can select candidate targets and evaluate read-only conditions:

```text
from $.users.*
where .version == 14
select .
```

Mutate may consume the resulting Binding Set, but mutation clauses do not become
part of SANSA.Query. Query evaluates state; Mutate expresses requested state
changes.

When candidate targets originate from a selector or Query, the complete candidate
set must be resolved against one namespace state before planning continues. The
planner then expands the candidate set into exact mutation operations. Apply must
not rerun the original selector or Query.

This snapshot rule prevents a mutation from changing its own target set while it
is being applied.

## 6. Structured Plan First

The interoperable center of SANSA.Mutate is a structured plan model, not a
human-authored mutation language.

A readable syntax may be standardized later. Examples such as:

```text
insert "X" before $.items[2]
move $.items[4] after $.items[1]
```

are explanatory notation only in this proposal. They do not define a parser
surface.

Conceptual plan model:

```text
MutationPlan
  planVersion
  planId?
  namespaceState
  operations[]
  preconditions[]
  sourceProvenance?
  portabilityWarnings?
  diagnostics[]
```

Conceptual exact target reference:

```text
MutationTarget
  requestedAddress
  canonicalAddress
  bindingHandle?
  observedState?
  portabilityWarnings?
```

Conceptual operation:

```text
MutationOperation
  op
  target?
  parent?
  source?
  placement?
  name?
  value?
  datatype?
  kind?
  provenance?
```

`requestedAddress` preserves what the caller supplied. `canonicalAddress`
identifies the resolved binding at planning time. `bindingHandle` is an optional
opaque adapter identity. `observedState` is an adapter-defined revision, version,
fingerprint, or equivalent precondition.

Opaque binding handles are local execution artifacts. SANSA does not require
them to be portable or serializable across implementations.

Current mutation plans are inspectable execution artifacts, not portable
serialized plan documents. A plan may retain live resolver bindings and
adapter-local continuity artifacts such as `bindingHandle` and `observedState`.
Serialized or cloned plans must not be assumed executable unless a future
profile defines a portable serialization and rehydration contract.

`sourceProvenance` is inert request-level metadata preserved for audit and
diagnostics. Operation-level `provenance` is similarly inert metadata on the
planned operation. Provenance must not be interpreted as SANSA source text,
authorization policy, validation policy, resolver configuration, or mutation
profile.

The conservative mutation request surface is closed. Request envelopes support
only `operations`, `preconditions`, and `provenance`; known operation requests
support only the fields defined for that operation plus optional inert
`provenance`. Unsupported fields fail closed rather than being ignored. This
keeps future-looking authority or rewrite fields, such as `policy`, `by`,
`actor`, `principal`, or `rewrite`, outside the core planner until a trusted
host envelope or later profile explicitly defines them.

`portabilityWarnings` carries diagnostics for locally accepted SANSA inputs that
exceed the portable v1 floor. For example, an implementation may accept a
position index above the portable ceiling under an explicit local limit. If the
target resolves exactly, the plan remains inspectable but should preserve the
warning so consumers do not mistake the plan for portable SANSA v1 behavior.

`datatype` and `kind` are optional value-intent hints on value-carrying
operations. `datatype` preserves semantic type intent, while `kind` preserves
representation or literal-family intent. SANSA.Mutate preserves these fields but
does not decide whether the supplied value is legal for the hinted datatype or
kind.

Structured Mutate requests keep `datatype` and `kind` as separate intent fields
until a consumer, schema, profile, or target surface evaluates them. This is a
deliberate difference from SANSA Instruction syntax: Instruction parses one
human-authored value literal and may reject known datatype/literal-family
mismatches before lowering. Structured Mutate instead preserves the requested
intent. For example, a target surface may accept `datatype=brandColor` with
`kind=hex`, because `brandColor` is custom semantic intent carried by a hex
literal family, while rejecting `datatype=number` with `kind=string` because
both families are known and incompatible for that target.

Target surfaces define what planned operations can be represented by a host
format, storage adapter, or interchange profile. For example, an AEON target
surface may reject a datatype hint that is not legal for AEON values, while a
JSON-compatible target surface may reject AEON attributes, node or tuple
containers, references, non-finite numbers, or SANSA selector literals. This is
not a mutation-planning failure. It means the plan is valid SANSA.Mutate intent
that the selected target cannot carry.

The plan must be inspectable before authorization or apply. Producing it must not
mutate the namespace.

## 7. Conservative Core Operations

The conservative operation vocabulary is:

- `create`
- `replace`
- `remove`
- `insert`
- `move`

These operations express semantic intent. They do not expose physical storage
operations.

### 7.1 Create

`create` adds one named binding to an exact existing parent binding.

Conceptual fields:

```text
op = create
parent = <exact existing parent>
name = <new exposed member name>
value = <structured semantic value>
datatype? = <semantic type hint>
kind? = <representation or literal-family hint>
```

The parent must resolve exactly once. The requested name must not already exist
in that parent under the adapter's exposed member-name rules. `create` is not
upsert and must not silently replace an existing binding.

A missing destination address is not itself a resolved mutation target. Creation
therefore targets the existing parent and carries the requested child name
separately.

### 7.2 Replace

`replace` changes the semantic value of one exact existing binding while
preserving that binding's identity and structural location.

Conceptual fields:

```text
op = replace
target = <exact existing binding>
value = <structured semantic value>
datatype? = <semantic type hint>
kind? = <representation or literal-family hint>
```

Replacement does not implicitly rename, move, merge, patch, follow, clone, or
retype a binding. Attributes that are independently exposed as bindings may be
targeted through their own exact SANSA addresses.

### 7.3 Remove

`remove` removes one exact existing binding from its containing semantic
structure.

Conceptual fields:

```text
op = remove
target = <exact existing binding>
```

Removing the namespace root is outside the conservative core. Cascading,
referential cleanup, tombstones, history retention, and physical deletion are
consumer or storage concerns.

### 7.4 Insert

`insert` adds one new binding to an exact exposed ordered container.

Conceptual fields:

```text
op = insert
container = <exact ordered container>
placement = <first | last | before anchor | after anchor>
value = <structured semantic value>
datatype? = <semantic type hint>
kind? = <representation or literal-family hint>
```

Conceptual placements:

```text
first  in <container>
last   in <container>
before <anchor>
after  <anchor>
```

For `before` and `after`, the anchor must be an exact existing positional child
of the target container. `first` and `last` also support insertion into an empty
container.

The operation preserves relative-order intent. SANSA does not prescribe whether
the adapter implements that intent using an array, linked list, rank key, tree,
cursor, event projection, or another representation.

### 7.5 Move

`move` relocates one exact existing positional binding within the same exposed
ordered container.

Its placement uses the same `first`, `last`, `before`, and `after` forms as
`insert`. The source binding retains semantic identity; `move` is not remove plus
create and is not copy.

Moving relative to the same source binding is invalid. Cross-container movement
is outside the conservative core because identity, ownership, validation, and
referential behavior may change across container boundaries.

## 8. Exact Targets And Cardinality

Every executable operation in a plan uses exact resolved bindings.

A plan may retain a selector or Query as source provenance for explanation,
auditing, diagnostics, and explicit replanning. Apply must not depend on
unresolved selector expansion.

The conservative cardinality rules are:

- `create` requires exactly one parent;
- `replace` and `remove` each require exactly one target per operation;
- `insert` requires exactly one container and, when used, exactly one anchor;
- `move` requires exactly one source, one container, and, when used, one anchor.

A caller may explicitly request bulk `replace` or bulk `remove`. The planner must
freeze the complete Binding Set and emit one exact operation per binding in
deterministic Binding Set order.

Bulk behavior is not inferred merely because a selector happens to return
multiple bindings. A request that expects one binding and receives more than one
fails with a target multiplicity diagnostic.

Because SANSA.Resolve does not implicitly deduplicate Binding Sets, a planner
must detect when the same binding would receive conflicting or repeated
destructive operations in one plan. The conservative core rejects such a plan
unless a later composition contract defines the interaction explicitly.

## 9. Target Stability And Index Drift

A canonical positional address alone is not sufficient to preserve a target
between planning and apply.

For example:

```text
$.items[2]
```

may identify a different binding after another operation inserts at position
zero.

An executable adapter must therefore preserve each resolved target by at least
one reliable mechanism, such as:

- an opaque stable binding handle plus an observed namespace revision;
- an exact address plus an expected state token that detects structural drift;
- another adapter contract that proves the target still denotes the same
  binding.

If the adapter cannot prove target continuity, it must reject the plan as stale.
It must not apply the operation to whichever binding now occupies the old
position.

The same rule applies to ordered anchors. Relative-order intent is evaluated
against the resolved source and anchor identities, not against unprotected
numeric indexes retained from planning.

## 10. Preconditions And Value Semantics

Preconditions should reuse a restricted read-only SANSA.Query predicate surface
where possible.

All target resolution and precondition evaluation for one plan occur against the
same logical namespace state. A failed precondition produces no executable plan.

Comparison, ordering, temporal interpretation, case behavior, and other value
operations use the consumer-selected Shared AEON Value Semantics profile. The
document being mutated must not select a more permissive comparison, validation,
authorization, or mutation profile for itself.

Preconditions describe expected state. They do not authorize the requested
change and do not replace stale-target checks.

## 11. Values, Validation, And References

Mutation values are structured semantic values. Runtime strings must not be
reinterpreted as SANSA source or executable mutation text.

SANSA.Mutate does not decide whether a supplied value is legal under an AEON
datatype, AEOS schema, application rule, or domain profile. The responsible
consumer validates proposed values before apply.

Optional `datatype` and `kind` hints are preserved as operation intent. They do
not retype an existing binding by themselves, do not authorize the operation, and
do not make a value schema-valid. A host adapter or validator may consume them to
materialize host-specific literal forms, apply schema rules, or reject the
operation.

A target-surface check may reject planned values before policy or apply
when the intended host format cannot represent them. This check is distinct from
schema validation. For example, JSON target validation can reject an AEON
attribute mutation because JSON has no attribute-space representation, while an
AEON schema validator may separately reject a value whose datatype is
representable but not allowed at that address. An AEON target surface may also
reject a planned `date` value such as `"2025-02-29"` because the value is not a
valid AEON date literal payload, even though the structured Mutate plan can
still preserve the requested `datatype` and `kind` intent for inspection.
Structured datatype/kind contradictions between known families, such as
`datatype=number` with `kind=string`, are also target-surface representability
failures. Custom semantic datatypes remain open until a schema, profile, or
target surface assigns meaning to them, so `datatype=brandColor` with
`kind=hex` can remain representable as custom intent.
Likewise, an AEON target surface may reject malformed reserved datatype
metadata such as `radix[03]`, unsupported reserved-looking aliases such as
`radix16`, or malformed source-family payloads such as radix `1__0` or
encoding `abc+/==`. Separator representability is checked in the same layer:
`root/main` is not an AEON separator payload without quoting, `sep[","]` is not
valid AEON Core separator metadata, and `kadot[...]` metadata is not an AEON
Core `kadot` surface. Quoted separator payloads such as
`"hello world"|"this, [is] fine"` remain representable. This is still
representability validation. AEON target validation also checks datatype
expression shape and Core-owned binding-side container restrictions, such as
rejecting malformed datatype intent or `node<string>` over a node binding while
accepting `node<node>` and custom profile/domain claims such as `node<html>`.
That check does not enforce child content; child semantics remain schema or
profile concerns. An AEON target surface may accept selector-shaped `:sansa`
address values because they are address data, while rejecting reference-family
values whose target text is not an exact AEON target path. Reference existence,
forward-reference legality, and self-reference legality remain AEON Core
document-validation responsibilities, not Mutate target-surface checks.
Base-specific radix digit meaning, decoded encoding meaning, separator-field
meaning, color meaning, version meaning, reference following, and other domain
semantics remain schema, profile, or consumer concerns.

Target-surface validation is also distinct from mutation policy. Policy answers
whether a trusted consumer allows the planned operation. Target-surface
validation answers whether the intended format or adapter surface can represent
the planned value and address role.

Implementations and workbenches may expose target-profile metadata alongside
target-surface validation results to help technical users understand the
selected representability boundary. Such metadata may include the normalized
target surface id, a statement that the boundary is representability, and a
human-readable summary of the target surface. This metadata is descriptive. It
does not replace `phase: "target"` diagnostics, does not make target-surface
validation part of planning, and does not define schema approval or
authorization semantics. Portable diagnostics continue to use `targetFormat`
for the selected target identity.

An exact target that carries a reference identifies the reference binding
itself. Mutate does not implicitly follow the reference and modify its target.
Any future followed-target operation must be explicit, authorized separately,
and preserve the distinction between inspecting a referenced value and changing
reference identity or target state.

Copy, clone, rebind, reference redirection, recursive merge, structural patch,
and implicit coercion are outside the conservative core.

## 12. Apply And Result Contract

SANSA.Mutate defines the plan's semantic intent but does not define a storage
transaction engine.

An adapter should advertise capabilities such as:

```text
supportsCreate
supportsReplace
supportsRemove
supportsOrderedInsert
supportsMove
supportsStableBindingIdentity
supportsAtomicApply
```

A read-only namespace may support Addressing, Resolve, and Query while rejecting
Mutate entirely. A mutation adapter may support only a subset of core operation
kinds and must reject unsupported operations explicitly.

If an operation capability flag is omitted, an implementation may infer support
from the corresponding adapter hook. If an operation capability flag is
explicitly `false`, apply must reject that operation before invoking mutation
hooks. `supportsStableBindingIdentity` advertises an adapter's ability to prove
target continuity through opaque handles, observed state, address/state tokens,
or an equivalent adapter contract. `supportsAtomicApply` is required only when a
consumer selects atomic apply.

Plan construction is all-or-nothing: a planning failure must not produce a
partially executable plan. Apply atomicity is a consumer requirement and adapter
capability, not an implicit transaction promise made by the plan itself. When a
consumer requires atomic apply and the adapter does not advertise it, the
consumer must reject the operation before apply. A consumer-selected non-atomic
execution mode is implementation-specific. Partial success in such a mode must
never be reported as full plan success.

If a mutation hook rejects or fails during non-atomic apply, the overall result
must fail. The result may include operation records for hooks that completed
before the failure, but those records describe partial execution only. Rollback,
retry, compensation, and transaction semantics remain adapter or consumer
responsibilities.

Conceptual result model:

```text
MutationResult
  planId?
  stateBefore?
  stateAfter?
  operationResults[]
  diagnostics[]

MutationOperationResult
  operationIndex
  status
  targetAddress?
  parentAddress?
  containerAddress?
  sourceAddress?
  anchorAddress?
  previousAddress?
  affectedAddress?
  resultingAddress?
  affectedBinding?
```

Role addresses such as `targetAddress`, `parentAddress`, `containerAddress`,
`sourceAddress`, and `anchorAddress` describe the planned mutation intent.
`previousAddress` identifies the pre-apply address for operations that change or
remove an existing binding. `affectedAddress` identifies the binding affected by
the operation when known. `resultingAddress` identifies the post-apply binding
address when such a binding exists or is reported by the adapter. A remove
operation affects the removed binding but does not invent a resulting address.

Resulting canonical addresses matter because insert and move operations may
change positional addresses even when semantic binding identities remain stable.

## 13. Representation And ASP Boundary

SANSA.Mutate defines observable semantic intent, not substrate mechanics.

| Concern | Owner |
| --- | --- |
| Meaning of create, replace, remove, insert, and move | SANSA.Mutate |
| Address and selector structure | SANSA.Addressing |
| Target resolution and Binding Set order | SANSA.Resolve |
| Read-only predicates and candidate selection | SANSA.Query |
| Stable internal binding identity | namespace adapter or ASP |
| Array, link, rank, tree, cursor, event, or CRDT representation | namespace adapter or storage |
| Value and schema legality | consumer, AEOS, or domain validator |
| Authorization | consumer or ASP |
| Atomic commit, rollback, and retries | ASP or storage transaction |
| Events, audit, and history retention | AES, ASP, or persistence layer |

ASP may consume a SANSA mutation plan and translate it into stable identities,
ordering changes, derived writes, and storage operations:

```text
SANSA.Mutate
  semantic operation
        |
        v
ASP mutation adapter
  stable identities and ordering model
        |
        v
storage transaction
```

SANSA does not decide how many records are touched, whether rank keys are
rebalanced, whether links are rewritten, whether derived writes are required, or
how rollback is implemented.

## 14. Authority And Safety

Mutation authority is separate from read authority.

A consumer may support:

```text
SANSA.Addressing  yes
SANSA.Resolve     yes
SANSA.Query       yes
SANSA.Mutate      no
```

or may allow mutation only for specific namespaces, address spaces, operation
kinds, principals, or budgets.

Authorization occurs after a plan is inspectable and before apply. Consumers may
also reject requests earlier to avoid disclosing protected namespace structure.

Mutation policy is consumer authority, not document authority. A trusted
consumer, host, ASP layer, application, or adapter may evaluate a mutation plan
against policy before apply. An externally selected AEOS schema or validator may
determine whether the proposed state is legal, but it does not own Mutate and
does not grant mutation authority. The document being mutated must not define
the policy that authorizes its own change.

A policy layer may consider:

- operation kind;
- exact target, parent, source, container, or anchor addresses;
- matched namespace or address space;
- supplied or inferred datatype and representation-kind intent;
- proposed value payload shape;
- principal, role, session, tenancy, or other external authority context;
- consumer budgets, rate limits, or product rules.

These checks authorize or deny already planned intent. They must not silently
rewrite the plan, reinterpret runtime strings as SANSA Instruction source, or
make schema-invalid values valid. If a policy wants a different operation, the
consumer should request and plan that operation explicitly.

Policy inputs should fail closed on unsupported fields rather than ignoring
them. This prevents claimed provenance such as Instruction `by` metadata, or
future-looking fields such as `rewrite`, from being mistaken for active
authorization behavior.

The current experimental policy surface used by implementation workbenches is a
plan filter, not a general authorization language. Its shape is intentionally
small:

```json
{
  "default": "deny",
  "rules": [
    {
      "allow": true,
      "operations": ["replace"],
      "target": "$.inventory.sku",
      "datatypes": ["string"]
    }
  ]
}
```

`default` is either `allow` or `deny`. Each rule declares `allow` as `true` or
`false` and may narrow by operation, address role, datatype, representation
kind, member name, or literal value. The supported rule fields in this
experimental surface are:

- `operation` or `operations`;
- `target`;
- `parent`;
- `source`;
- `container`;
- `anchor`;
- `datatype` or `datatypes`;
- `kind` or `kinds`;
- `name` or `names`;
- `value` or `values`.

Singular and plural matcher fields are equivalent. Plural fields accept a list
of accepted values. Operation lists may use `*` as an explicit wildcard.
Address-role fields contain SANSA address expressions evaluated by the consumer
against the same namespace view used for policy checking; the resolved canonical
addresses are matched against the corresponding planned operation role. Invalid
address matchers fail closed as policy errors. Because matchers are SANSA
addresses rather than raw string prefixes, quoted member selectors and escaped
quoted member selectors match by resolved binding identity and canonical
planned address, for example `$.inventory.["display tags"]` or
`$.inventory.["quote\"key"]`.
An `anchor` matcher applies only when the planned operation has a resolved
`before` or `after` placement anchor; it does not match `first` or `last`
placements.

Experimental policy diagnostics should preserve enough context for tools to
identify the failed operation, rule, policy field, policy scope, and invalid
matcher address where available. Suggested context fields are `operationIndex`,
`ruleIndex`, `policyField`, `policyScope`, and `policyAddress`.

This policy surface deliberately does not include `by`, `because`, `actor`,
`principal`, `role`, `rewrite`, `schema`, or executable function fields.
Principal identity, delegation, authentication, signatures, audit evidence, and
host-specific policy functions belong to the trusted host envelope or a
separate authorization system. Provenance preserved on an Instruction or plan
may be displayed to a policy decision-maker, but it is not itself policy
authority.

Planning and apply should expose budgets for target count, operation count,
resolved bindings, predicate work, supplied value size, and implementation
resource limits. Limit exhaustion must fail explicitly and must not produce a
partial executable plan.

Budget diagnostics should name the phase, budget, limit, and observed count when
available. The first implementation slice exposes `maxOperations`,
`maxPreconditions`, `maxValueNodes`, `maxValueDepth`, and `maxStringLength`
budgets for planning and apply. `maxValueNodes` counts all supplied value nodes
for value-carrying operations, with arrays and objects counting as one node plus
their entries. `maxValueDepth` limits the deepest supplied value tree, with
scalar values at depth `1`. `maxStringLength` limits the longest supplied string
payload. When a supplied value budget fails because of a nested value, the
diagnostic should include `valuePath` when available so tools can identify the
offending payload location without confusing the failure with target-surface
representability. Later implementations may add target-count, resolved-binding,
predicate-work, or implementation-resource budgets without changing the
all-or-nothing failure rule.

## 15. Diagnostics

SANSA.Mutate planning diagnostics should distinguish:

- invalid plan shape or unsupported mutation syntax;
- unsupported operation or placement;
- unsupported adapter operation or disabled operation capability;
- target miss;
- target multiplicity violation;
- duplicate or conflicting target;
- invalid move relationship;
- precondition failure;
- stale target or anchor;
- non-portable but locally accepted target diagnostics;
- target-surface representability failure;
- implementation limit exhaustion.

Target-surface representability diagnostics should preserve target context when
available, including `targetFormat`, rejected `datatype`, and rejected
`valuePath` for value representability failures. When the rejected value is
inside a supplied container payload, `valuePath` should identify the nested
location rather than only the root operation value. Diagnostic value paths use
dot segments for identifier-safe object keys, numeric bracket segments for list
positions, and JSON-quoted bracket segments for empty or non-identifier object
keys.

Tools that expose richer target-profile metadata should keep it descriptive and
separate from diagnostics. For example, a workbench may report that
`json-compatible` normalized to the `json` target surface and that the target
boundary is representability, while the diagnostic still carries
`targetFormat: "json"` and the rejected datatype or value path.

Consumer, ASP, or host-storage diagnostics should distinguish:

- authorization denial;
- value or schema validation failure;
- unsupported adapter capability;
- apply failure;
- storage conflict;
- atomicity unavailable;
- transaction failure;
- migration or orchestration failure;
- audit or subscription delivery failure.

## 16. Deliberately Deferred Growth Path

The following capabilities may be useful, but they are not folded into Mutate
Core:

| Future surface | Likely owner |
| --- | --- |
| `copy`, cross-container move, rename, upsert, increment, clear, and structured Mutate append/prepend operation aliases | later Mutate extensions |
| nested binding-tree materialization with per-child datatype or kind intent | later Mutate or Instruction extension |
| map, filter, sort, deduplicate, merge, patch, and structural reshaping | `SANSA.Transform` |
| atomic groups, cross-binding invariants, expected revisions, and commit semantics | possible `SANSA.Transaction` |
| migrations, business rules, mirrored writes, retries, and conflict workflows | ASP orchestrator |
| authorization policy and principal evaluation | consumer or ASP |
| storage representation and physical change operations | adapter or storage engine |

Nested binding-tree materialization would need an explicit future surface rather
than silently extending conservative `create` or `replace`. Such a surface would
make nested members executable binding creation or replacement intent, preserve
per-child datatype or kind metadata, and require its own policy, target-surface,
diagnostic, failure, and atomicity rules.

An integrated human-authored Query-and-mutation syntax, correlated writes,
conditional branches, compositional dynamic target construction, arithmetic
updates, and transaction syntax are also deferred. They require independent
contracts for snapshotting, cost, authority, operation ordering, failure
propagation, and atomicity. This does not prevent a planner from consuming an
already resolved Binding Set under the bulk `replace` and `remove` rules above.

This boundary leaves a clear growth path without turning Mutate Core into Query,
Transform, Transaction, authorization, and orchestration at once.

## 17. Proposal Status

This proposal defines the intended conservative boundary for implementation
experiments. It does not make SANSA.Mutate part of required SANSA v1 Addressing,
Resolve, Query, or Transform conformance.

The first implementation slice should:

1. expose a structured mutation-plan API;
2. implement exact-target planning for `create`, `replace`, and `remove`;
3. add representation-neutral `insert` and same-container `move`;
4. preserve target and anchor identity or reject stale plans;
5. keep authorization and physical apply behind a consumer adapter;
6. expose post-plan `policy` and `target` diagnostics without treating either
   as a planning failure;
7. report affected bindings and resulting canonical addresses;
8. preserve inert provenance and portability warnings on inspectable plans;
9. expose explicit operation, precondition, capability, stale-target, and apply
   diagnostics;
10. preserve datatype/kind value intent and enforce operation, precondition, and
   supplied-value budgets.

Human-authored syntax, portable plan serialization, cross-process opaque target
identity, broad bulk mutation syntax, Transform operations, and transaction
composition remain later design work.
