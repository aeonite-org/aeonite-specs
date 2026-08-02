---
license: CC-BY-4.0
---

# aeonite-specs

`aeonite-specs` is the canonical public repository for formal AEON-family specification text.

It is the source of truth for:

- AEON specifications
- AEOS specifications
- SANSA specifications
- NEON specifications
- versioned spec lifecycle state across proposals, drafts, and published releases

## Authority

This repo is specification-authoritative.

It is intended to own the formal text that was previously spread across organizational documents and temporary working areas.

It is not intended to own:

- implementation code
- official CTS ownership
- project planning trackers

## Public repositories

- [`aeonite-org/aeonite-specs`](https://github.com/aeonite-org/aeonite-specs) is the canonical specification source.
- [`aeonite-org/aeonite-cts`](https://github.com/aeonite-org/aeonite-cts) owns the public conformance suites, runners, and CTS protocol material.

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
sansa/
  v1/
    proposals/
    drafts/
    published/
neon/
  v1/
    proposals/
    drafts/
    published/
and/
  v1/
    drafts/
  v2/
    proposals/
contracts/
  v1/
    drafts/
      artifacts/
conventions/
  v1/
    drafts/
```

Repository-level spec-maintenance utilities may also live under:

- `scripts/`

Release-facing change history is tracked in:

- `CHANGELOG.md`

Specification snapshots use explicit documentation identifiers such as
`sansa-query-specs-v1-snapshot-0.1`. They are intended to align spec text with
CTS compatibility snapshots without replacing proposal, draft, or published
lifecycle status. See `docs/spec-snapshot-versioning.md`.

Before committing, run:

```bash
bash ./scripts/pre-commit-check.sh
```

This keeps portable spec text from accidentally picking up local filesystem
paths.

## Licensing

This repository uses artifact-specific licenses. Normative specifications and
appendices use `CC-BY-4.0`, conventions and reusable examples use `CC0-1.0`,
and repository maintenance scripts use `MIT`, unless a file declares otherwise.

See `LICENSE` and `LICENSE.md` for the licensing policy, and `LICENSES/` for
the full license texts.
