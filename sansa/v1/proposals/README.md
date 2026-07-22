---
id: sansa-v1-proposals
title: SANSA v1 Proposals
description: Proposal-stage specification set for SANSA addressing, resolution, and query semantics.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals
license: CC-BY-4.0
---

# SANSA v1 Proposals

SANSA is the Semantic Address NameSpace Abstraction. It defines a common way for consumers to address, resolve, and query semantic information without depending on the physical implementation that stores or generates that information.

SANSA is independent within the Aeonite ecosystem. AEON, AEOS, AES, runtime object graphs, databases, services, and other systems may implement SANSA, but none of those systems owns the abstraction.

## Proposal Set

- `addressing-v1.md` defines the SANSA address model and selector vocabulary.
- `resolve-v1.md` defines deterministic structural resolution over SANSA address expressions.
- `query-v1.md` defines the initial read-only semantic query pipeline built on SANSA.Resolve.
- `conformance-v1.md` defines capability names, conformance profiles, and extension advertisement.
- `extensions-v1.md` records candidate selector and query-helper extensions before they enter the core v1 conformance surface.

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
  v
SANSA.Query
  |
  v
Result Set
```

SANSA.Resolve discovers semantic structure. SANSA.Query evaluates and transforms semantic bindings while consuming Shared AEON Value Semantics for comparison, ordering, and related value behavior.

## Capability Families

This proposal set covers these conformance capabilities:

- `SANSA.Addressing`
- `SANSA.Resolve`
- `SANSA.Query`

Implementations should advertise supported capabilities rather than claim unqualified support for "SANSA". For example, a parser may support `SANSA.Addressing` without supporting `SANSA.Resolve`, and a resolver may support `SANSA.Resolve` without supporting `SANSA.Query`.

Future specifications may cover:

- `SANSA.Mutate`
- `SANSA.Subscribe`
- `SANSA.History`
- self-description and capability discovery

## Design Boundaries

SANSA separates semantic interaction from representation, validation, persistence, and runtime implementation.

- AEON defines how meaning is represented.
- AEOS defines how meaning is constrained.
- AES defines how meaning is persisted.
- SANSA defines how meaning is accessed.

SANSA does not require data to originate from AEON. It requires only that a conforming implementation expose a deterministic semantic namespace to consumers.
