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

SANSA.Resolve discovers semantic structure. SANSA.Query evaluates and transforms semantic bindings according to the Aeonite semantic model.

## Capability Families

This proposal set covers:

- `SANSA.Addressing`
- `SANSA.Resolve`
- `SANSA.Query`

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
