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

## Licensing

This repository is released under the MIT License. See `LICENSE`.
