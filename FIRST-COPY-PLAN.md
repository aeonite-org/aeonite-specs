# First Copy Plan

This document defines the first population wave for `aeonite-specs`.

It is based on the current migrated source inventory and boundary decisions.

## Wave 1 targets

### AEON draft line

Source root:

- migrated AEON v1 working-line material

Planned destination:

- `aeon/v1/drafts/`

Candidate documents:

- `AEON-spec-v1.md`
- `aeon-core-compliance-v1.md`
- `addressing-references-v1.md`
- `comments-annotations-v1.md`
- `conformance-matrix.md`
- `contracts-v1.md`
- `release-governance-v1.md`
- `structure-syntax-v1.md`
- `value-types-v1.md`

Additional candidate subtrees:

- `appendices/`
- `conventions/`
- `contracts/` subject to registry ownership decision

### AEOS draft line

Source root:

- migrated AEON v1 working-line material

Planned destination:

- `aeos/v1/drafts/`

Candidate documents:

- `AEOS-spec-v1.md`
- `aeos-compliance-v1.md` (new split target for AEOS-specific compliance)
- `appendices/appendix-aeos-charter.md` (AEOS-owned appendix)

### NEON draft line

Source root:

- migrated Neon v1 design material

Planned destination:

- `neon/v1/drafts/`

Candidate document:

- `neon-v1-design.md`

## Decision gates before copy completion

The following items need explicit classification during the first wave:

1. `aeon-core-compliance-v1.md`: AEON core compliance draft
2. `conformance-matrix.md`: CTS-owned conformance mapping document
3. `contracts/registry.json`: treat as normative artifact manifest unless later evidence contradicts that
4. `appendix-validator-conformance.md`: split boundary with pointer in specs and operational guidance in CTS
5. `appendix-aeos-charter.md`: AEOS-owned appendix

## Operational approach

For the first copy wave:

- keep this repo as the spec authority for migrated content
- preserve filenames unless renaming improves long-term clarity
- use pointer notes in former source locations rather than maintaining parallel authority
- avoid editing substantive normative text during structural migration unless a correction is intentional and reviewed
