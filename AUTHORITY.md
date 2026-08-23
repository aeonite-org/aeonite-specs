---
license: CC-BY-4.0
---

# Authority

`aeonite-specs` is the sole long-term source of truth for formal AEON-family specification sources
and their authoritative non-prose resources.

It is authoritative for:

- normative spec drafts
- published spec releases
- proposal-stage spec text intended to enter the lifecycle
- appendix and supporting spec text that belongs to a published or draft line
- AEON envelope metadata governing publication, lifecycle, relationships, and licensing
- versioned contract registries, profiles, schemas, and related normative artifacts

It is not authoritative for:

- implementation source code
- official CTS ownership
- implementation-specific project planning
- generated HTML, Markdown, standalone &ND, catalogs, search indexes, and website presentation

## Repository boundaries

The repository boundary is:

- `altopelago/aeon`: implementation authority
- [`aeonite-org/aeonite-specs`](https://github.com/aeonite-org/aeonite-specs): specification authority
- [`aeonite-org/aeonite-cts`](https://github.com/aeonite-org/aeonite-cts): conformance authority
- `AltoPelago/aeonite-website` (private): presentation, projection, and deployment authority for `aeonite.org`

Formal documents live under `sources/` as AEON envelopes with embedded &ND bodies. Repository-level
documentation remains Markdown and is not part of the formal corpus.
