---
id: sansa-v1-mutate
title: SANSA.Mutate v1
description: Proposal-stage future capability outline for deterministic semantic mutation intent.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/mutate
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-resolve
  - sansa-v1-query
  - sansa-v1-conformance
  - sansa-v1-meaning-validation-integration
---

# SANSA.Mutate v1

Status: Proposal outline  
Scope: future authority-bearing mutation capability built on SANSA Addressing, Resolve, and read-only predicate evaluation.

## 1. Overview

SANSA.Mutate is a future capability for describing intentional semantic change.

It is not part of SANSA.Query. Query remains read-only. Mutate may consume SANSA addresses, Binding Sets, and Query-like preconditions, but mutation crosses a stronger trust boundary than read-only resolution or evaluation.

SANSA.Mutate should produce deterministic change intent or immutable mutation plans. It should not decide authorization, transaction semantics, storage layout, orchestration, migrations, retries, or conflict policy.

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

## 4. Conceptual Mutation Pipeline

A mutation-capable consumer should distinguish these phases:

```text
1. Target
   Resolve the intended bindings.

2. Preconditions
   Evaluate read-only predicates.

3. Plan
   Produce an immutable mutation plan.

4. Authorize
   Consumer approves each proposed operation.

5. Apply
   Consumer applies the plan atomically where supported.

6. Report
   Return affected bindings and diagnostics.
```

SANSA.Mutate owns Target, Preconditions, and Plan shape only to the extent required to produce deterministic change intent. Authorization, Apply, transactions, storage behavior, and orchestration remain consumer responsibilities.

## 5. Relationship To Query

Query can select targets and evaluate preconditions:

```text
from $.users.alice
where .version == 14
select .handle
```

A future mutation surface may reuse those read-only concepts, but must not add mutation clauses to SANSA.Query.

The following style is intentionally out of scope for Query:

```text
from $.users.alice
where .version == 14
set .handle = "alice"
```

The design direction is that Query evaluates state, while Mutate expresses requested state changes.

## 6. Mutation Plan Model

A mutation plan is an immutable description of intended changes after target resolution and precondition evaluation.

Conceptual model:

```text
MutationPlan
  operations[]
  preconditions[]
  targetProvenance?
  diagnostics?
  portabilityWarnings?
```

Conceptual operation:

```text
MutationOperation
  op
  target
  value?
  expected?
  provenance?
```

The plan should be inspectable before authorization or apply. Producing a plan must not mutate the namespace.

## 7. Initial Operation Vocabulary

The first mutation operation vocabulary should be conservative:

- replace binding value;
- create binding;
- delete binding.

More complex operations should remain out of the initial surface until identity, ordering, concurrency, and conflict semantics are clearer:

- move;
- copy;
- ordered insertion;
- ordered reindexing;
- merge;
- patch;
- structural migration.

These may become extensions or later promoted operations.

## 8. ASP Boundary

ASP may use SANSA.Mutate as the semantic change-intent layer.

Likely ASP relationship:

```text
Request
  |
  v
SANSA.Query
  determine targets and evaluate preconditions
  |
  v
Authorization
  determine whether the requested operation is permitted
  |
  v
SANSA.Mutate
  produce deterministic change intent
  |
  v
ASP Orchestrator
  expand rules, migrations, mirrored writes, and invariants
  |
  v
Storage Transaction
  commit atomically
  |
  v
History / Subscription
```

ASP remains responsible for:

- authorization;
- orchestration;
- migrations;
- transactions;
- retries;
- storage-specific conflict handling;
- versioning;
- audit behavior.

SANSA.Mutate should not decide whether a requested change is permitted, how many storage records are touched, whether derived writes are required, or how rollback is implemented.

## 9. Authority And Safety

Mutation authority must be separate from read authority.

A consumer may support:

```text
SANSA.Addressing  yes
SANSA.Resolve     yes
SANSA.Query       yes
SANSA.Mutate      no
```

or may allow mutation only for specific address spaces, operation kinds, or authenticated principals.

Mutation diagnostics should distinguish:

- invalid mutation syntax;
- unsupported operation;
- target miss;
- target multiplicity violation;
- precondition failure;
- authorization denial;
- apply failure;
- storage conflict;
- implementation limit exhaustion.

## 10. Future Design Questions

The following questions are for future `SANSA.Mutate`, ASP, and host-storage
design work. They are not required SANSA v1 conformance decisions.

- Should SANSA.Mutate expose a human-authored mutation language, a structured plan format, or both?
- Should preconditions be expressed as restricted SANSA.Query predicates, a separate predicate grammar, or consumer-owned rule objects?
- Should replace/create/delete be enough for the first experimental implementation?
- Should operation targets require exact addresses after planning, or may a plan retain selector provenance?
- Which mutation diagnostics belong to SANSA and which belong to ASP or host storage?
- Should atomic multi-operation plans later become `SANSA.Transaction`, or remain a consumer execution contract?
