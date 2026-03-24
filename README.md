# aeonite-specs

`aeonite-specs` is the canonical public repository for formal AEON-family specification text.

It is the source of truth for:

- AEON specifications
- AEOS specifications
- NEON specifications
- versioned spec lifecycle state across proposals, drafts, and published releases

## Authority

This repo is specification-authoritative.

It is intended to own the formal text that was previously spread across organizational documents and temporary working areas.

It is not intended to own:

- implementation code
- official CTS ownership
- project planning trackers
- migration-only scaffolding

## Layout

```text
aeon/
  v1/
    proposals/
    drafts/
    published/
aeos/
  v1/
    proposals/
    drafts/
    published/
neon/
  v1/
    proposals/
    drafts/
    published/
```

Repository-level spec-maintenance utilities may also live under:

- `scripts/`

## Initial migration model

During the first migration wave:

- AEON and AEOS draft material in this repo is seeded from the migrated v1 working line
- NEON draft material in this repo is seeded from the migrated Neon v1 design source
- frozen publication text should move into `published/` only once it is explicitly treated as released

## Current status

This repo is being populated as a fresh authority surface.

Until migration is complete, some upstream material may still exist in `overview` or private staging areas, but those locations should be treated as transitional rather than permanent authority.
