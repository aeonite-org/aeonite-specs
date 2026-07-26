---
id: sansa-v1-proposals
title: SANSA v1 Proposals
description: Proposal-stage specification set for SANSA query, conformance, integration, extension, instruction, and future mutation semantics.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals
license: CC-BY-4.0
---

# SANSA v1 Proposals

SANSA is the Semantic Address NameSpace Abstraction. It defines a common way for consumers to address, resolve, and query semantic information without depending on the physical implementation that stores or generates that information.

SANSA is independent within the Aeonite ecosystem. AEON, AEOS, AES, runtime object graphs, databases, services, and other systems may implement SANSA, but none of those systems owns the abstraction.

## Draft Set

The foundation layer has moved to `../drafts/`:

- `../drafts/addressing-v1.md` defines the SANSA address model and selector vocabulary.
- `../drafts/resolve-v1.md` defines deterministic structural resolution over SANSA address expressions.

## Proposal Set

- `query-v1.md` defines the initial read-only semantic query pipeline built on SANSA.Resolve.
- `conformance-v1.md` defines capability names, conformance profiles, and extension advertisement.
- `extensions-v1.md` records candidate selector and query-helper extensions before they enter the core v1 conformance surface.
- `meaning-validation-integration-v1.md` defines the AEON, AEOS, SANSA, and meaning-validation responsibility boundaries.
- `mutate-v1.md` defines the conservative authority-bearing mutation-plan boundary and its growth path.
- `instruction-v1.md` defines a proposed human-authored source surface that combines Addressing, Query, and Mutate vocabulary.

## Conceptual Stack

```text
Namespace
  |
  v
SANSA.Resolve
  |
  v
Binding Set
  |
  +--> SANSA.Query  --> Result Set
  |
  +--> SANSA.Mutate --> Mutation Plan --> Consumer Apply
```

SANSA.Resolve discovers semantic structure. SANSA.Query evaluates semantic bindings without changing namespace state. SANSA.Mutate freezes exact targets and expresses change intent without owning authorization, transactions, orchestration, or physical storage behavior.

SANSA.Instruction is a proposed source-level composition layer. It is intended
to lower into structured Query and Mutate behavior rather than replace those
capabilities.

SANSA.Mutate reuses consumer-selected Shared AEON Value Semantics for preconditions. Value legality remains the responsibility of the consumer, AEOS schema, or domain validator; a document being mutated cannot select its own mutation, validation, or authorization policy.

## Capability Families

The SANSA v1 draft/proposal set covers these conformance capabilities:

- `SANSA.Addressing`
- `SANSA.Resolve`
- `SANSA.Query`

Implementations should advertise supported capabilities rather than claim unqualified support for "SANSA". For example, a parser may support `SANSA.Addressing` without supporting `SANSA.Resolve`, and a resolver may support `SANSA.Resolve` without supporting `SANSA.Query`.

Future specifications may cover:

- `SANSA.Mutate`
- `SANSA.Instruction`
- `SANSA.Subscribe`
- `SANSA.History`
- self-description and capability discovery

## Design Boundaries

SANSA separates semantic interaction from representation, validation, persistence, and runtime implementation.

- AEON defines how meaning is represented.
- AEOS defines how meaning is constrained.
- AES defines how meaning is persisted.
- SANSA defines how meaning is accessed and, through future Mutate capability, how change intent is expressed.
- Meaning validators define how domain rules are interpreted and reported.
- Future mutation consumers define how accepted change intent is authorized, orchestrated, and applied.

SANSA does not require data to originate from AEON. It requires only that a conforming implementation expose a deterministic semantic namespace to consumers.
