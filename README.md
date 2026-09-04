---
license: CC-BY-4.0
---

# aeonite-specs

`aeonite-specs` is the canonical public repository for formal AEON-family specification sources.

The formal corpus is authored as AEON envelopes containing embedded `&ND` documents. Repository
documentation such as this README, authority statements, licensing policy, and contribution guidance
remains Markdown because it describes the repository rather than forming part of the specification
corpus.

## Authority

This repository is authoritative for:

- AEON, AES, AEOS, SANSA, NEON, and &ND specifications;
- appendices, conventions, proposals, drafts, and publication metadata;
- versioned contract registries, profiles, schemas, and other normative resources.

It does not own implementation code, official CTS ownership, website presentation, generated
projections, or deployment configuration.

## Layout

```text
sources/
  aeon/v1/
  aes/v0/
  aeos/v1/
  sansa/v1/
  neon/v1/
  and/v1/
  and/v2/
  appendices/v1/
  conventions/v1/
  contracts/v1/
resources/
  contracts/v1/
publication/
  spec-document-profile.md
  aeon-example-expectations.json
metadata/
  document-date-provenance.json
```

Lifecycle, standing, normativity, relationships, ordering, and publication paths are declared in each
AEON source envelope. Directory names organize the corpus but do not override envelope metadata.

Generated HTML, Markdown, standalone &ND, search indexes, and catalogs are not checked into this
repository. The private `aeonite-website` publisher consumes a reviewed revision of this public
source tree and produces those artifacts for [`aeonite.org`](https://aeonite.org/). Published
document pages provide downloadable Markdown, &ND, and original AEON-source projections.

## Validation

Before committing, run:

```sh
bash ./scripts/pre-commit-check.sh
```

This checks portable paths, the 85-document source inventory, required envelope declarations,
identifier uniqueness, date ordering, and the contract-resource bundle. Full AEON and &ND parsing,
projection tests, and website checks run in the consuming publication build.

## Public repositories

- [`aeonite-org/aeonite-specs`](https://github.com/aeonite-org/aeonite-specs) is the canonical specification source.
- [`aeonite-org/aeonite-cts`](https://github.com/aeonite-org/aeonite-cts) owns public conformance suites, runners, and CTS protocol material.

## Licensing

This repository uses artifact-specific licenses. Normative specifications and appendices use
`CC-BY-4.0`, conventions and reusable examples use `CC0-1.0`, and repository maintenance scripts use
`MIT`, unless an AEON envelope or file declares otherwise. See `LICENSE.md` and `LICENSES/`.
