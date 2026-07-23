---
id: sansa-v1-drafts
title: SANSA v1 Drafts
description: Draft-stage specification set for the SANSA v1 foundation layer.
family: sansa
group: SANSA
status: Draft
path: specification/sansa/v1/drafts
license: CC-BY-4.0
---

# SANSA v1 Drafts

SANSA is the Semantic Address NameSpace Abstraction. It defines a common way for consumers to address, resolve, and query semantic information without depending on the physical implementation that stores or generates that information.

SANSA is independent within the Aeonite ecosystem. AEON, AEOS, AES, runtime object graphs, databases, services, and other systems may implement SANSA, but none of those systems owns the abstraction.

## Draft Set

- `addressing-v1.md` defines the SANSA address model and selector vocabulary.
- `resolve-v1.md` defines deterministic structural resolution over SANSA address expressions.

These documents are draft-stage because their foundation-layer behavior is now implemented and exercised by AEON TypeScript and the standalone `@altopelago/sansa` implementation.

## Related Proposals

The following SANSA v1 documents remain in `../proposals/` while their surfaces continue to evolve:

- `query-v1.md`
- `conformance-v1.md`
- `extensions-v1.md`
- `meaning-validation-integration-v1.md`
- `mutate-v1.md`

## Design Boundaries

SANSA separates semantic interaction from representation, validation, persistence, and runtime implementation.

- AEON defines how meaning is represented.
- AEOS defines how meaning is constrained.
- AES defines how meaning is persisted.
- SANSA defines how meaning is accessed.
- Meaning validators define how domain rules are interpreted and reported.
- Future mutation consumers define how accepted change intent is authorized, orchestrated, and applied.

SANSA does not require data to originate from AEON. It requires only that a conforming implementation expose a deterministic semantic namespace to consumers.
