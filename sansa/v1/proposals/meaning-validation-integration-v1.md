---
id: sansa-v1-meaning-validation-integration
title: SANSA v1 AEON, AEOS, and Meaning Validation Integration
description: Proposal-stage integration boundary between SANSA Resolve/Query, AEON, AEOS, and meaning-validation consumers.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/meaning-validation-integration
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-resolve
  - sansa-v1-query
  - sansa-v1-conformance
  - aeos-v1
---

# SANSA v1 AEON, AEOS, and Meaning Validation Integration

Status: Proposal  
Scope: integration boundaries for using SANSA with AEON source, AES representation, AEOS schemas, and meaning-validation consumers.

## 1. Overview

SANSA defines semantic addressing, structural resolution, and read-only query evaluation. It does not define domain truth, schema authority, mutation authority, or validation outcomes.

Within the Aeonite ecosystem, SANSA is the semantic interaction layer. AEON, AES, AEOS, validators, tools, and future ASP systems may use SANSA, but they do not transfer their responsibilities to SANSA.

Conceptual stack:

```text
AEON Core
  parses source and emits AES

AEOS
  validates representation and structure
  may use SANSA.Resolve for rule targeting

Meaning Validation
  uses SANSA.Resolve for binding discovery
  uses restricted SANSA.Query policy for read-only semantic predicates
  owns domain rules and diagnostics

Tonic / Tools / Transformations / ASP
  materialize, transform, authorize, or act on accepted meaning
```

## 2. Layer Responsibilities

### 2.1 AEON Core

AEON Core owns source-level correctness:

- lexing and parsing;
- datatype annotation syntax;
- canonical path assignment;
- reference syntax and Core reference legality;
- emitting AES events.

AEON Core may parse and preserve SANSA address literals. It does not resolve those addresses, decide their consumer meaning, or validate domain rules implied by them.

### 2.2 AES

AES is the emitted representation consumed by downstream systems.

SANSA implementations over AES expose an addressable namespace from AES events, values, paths, attributes, datatypes, representation kinds, and other host-provided metadata. AES itself does not decide whether a SANSA selector is a schema rule, a query, a UI affordance, or an external-system reference.

### 2.3 AEOS

AEOS owns schema-declared representation and structural validation over AES.

AEOS may use SANSA.Resolve to identify the AES events targeted by schema rules:

```aeon
path:sansa = $.contact.name
selector:sansa = $.contact.measurements.*
```

The schema or validator decides that these SANSA literals are rule targets. The source document being validated does not gain authority to decide which rule, policy, or meaning-validation behavior applies to itself.

### 2.4 SANSA.Resolve

SANSA.Resolve discovers bindings in a namespace. It answers which bindings match a SANSA address or selector expression.

Resolve is structural. It does not compare values, apply domain rules, select violations, mutate data, or decide whether a matched binding is valid.

### 2.5 SANSA.Query

SANSA.Query evaluates read-only predicates and projections over resolved Binding Sets.

Query can be useful to meaning-validation consumers because it provides deterministic filtering, existence checks, cardinality checks, comparisons, and approved value functions. Query still does not own domain meaning. A query result becomes a validation result only when a validator or consumer assigns that role.

### 2.6 Meaning Validators

Meaning validators own domain rules, validation policy, diagnostics, and result envelopes above AEOS structural validation.

A meaning validator may use:

- SANSA.Resolve for binding discovery;
- SANSA.Query under a validation policy for read-only semantic predicates;
- AEON Shared Value Semantics for comparison and scalar behavior;
- local schema, contract, or product rules.

The validator decides what constitutes a violation and how diagnostics are reported.

## 3. Rule Targeting Versus Meaning Predicates

A rule target identifies where a rule applies.

```aeon
selector:sansa = $.inventory.items.*
```

A meaning predicate decides whether each targeted binding satisfies a consumer-owned rule.

```text
from $.inventory.items.*
where exists(.id#number) and isValue(.status)
select .
```

These are separate concerns. A SANSA selector can target candidate bindings without expressing a rule. A SANSA query can find bindings without making them validation failures.

This distinction allows the same SANSA grammar to support:

- AEOS schema rule targeting;
- diagnostic exploration tools;
- read-only query workbenches;
- external system references;
- future ASP planning and mutation workflows.

## 4. Document Authority Boundary

An AEON document may contain SANSA address literals:

```aeon
path:sansa = $.contact.name
external:sansa = $.inventory:csv[","]
```

The presence of a SANSA literal in a document does not authorize that document to:

- choose the schema used to validate itself;
- instruct AEOS how to interpret its constraints;
- grant access to local address spaces;
- enable Query extensions;
- enable mutation or transformation behavior;
- assign domain semantics to qualifier expressions.

Consumers decide whether a SANSA literal is data, a schema target, a query parameter, an external-system reference, or unsupported input.

This boundary is especially important for container semantics. A document can express a value such as `node<node>` when the grammar allows it. Whether child values are required to be nodes is a schema or consumer responsibility, not a directive from the value to the schema engine.

## 5. Validation-Safe Query Policy

Meaning-validation consumers should not need the full presentation-oriented Query surface.

The proposal-stage validation policy is a restricted `SANSA.Query` policy intended for read-only semantic predicates. It is not a new syntax form, not a separate v1 conformance profile, and not controlled by the source document.

A validation policy may allow:

- `from`;
- `where`;
- exact and selector-based resolution expressions;
- existence predicates;
- cardinality predicates;
- comparisons using Shared AEON Value Semantics;
- Boolean composition;
- approved deterministic value functions;
- binding-preserving projection when the consumer needs candidate identity.

A validation policy should reject:

- `order by`;
- `offset`;
- `limit`;
- presentation object projection;
- transform-library helpers such as `objectFrom(...)` and `fieldsFrom(...)`;
- implementation-specific executable functions;
- mutation, subscription, or side-effecting behavior.

Policy rejection is a policy diagnostic, not an ordinary query miss.

## 6. Diagnostics Ownership

SANSA diagnostics identify address, resolve, query, policy, capability, and limit failures.

AEOS diagnostics identify schema and representation-validation failures.

Meaning-validation diagnostics identify consumer-owned semantic rule failures.

Implementations should preserve this distinction so that downstream users can tell the difference between:

- invalid SANSA syntax;
- an unsupported selector;
- a valid query that finds no bindings;
- a query rejected by validation policy;
- a schema target that matches no required AES events;
- a domain rule violation.

## 7. Open Questions

- Should AEOS directly use SANSA.Resolve for selector expansion, or should a separate meaning-validation layer own all Resolve usage above exact path lookup?
- Should meaning validation use assertion-style rules, violation-selection rules, or support both?
- Which diagnostics should be standardized by AEOS versus a future meaning-validation specification?
