# Authority

`aeonite-specs` is the sole long-term source of truth for formal AEON-family specification text.

It is authoritative for:

- normative spec drafts
- published spec releases
- proposal-stage spec text intended to enter the lifecycle
- appendix and supporting spec text that belongs to a published or draft line

It is not authoritative for:

- implementation source code
- official CTS ownership
- implementation-specific project planning
- internal migration governance

## Repository boundaries

The intended split is:

- `altopelago/aeon`: implementation authority
- `aeonite-org/aeonite-specs`: specification authority
- `aeonite-org/aeonite-cts`: conformance authority
- `overview`: organizational and migration authority only

## Migration rule

Once a document is promoted here as the accepted spec source, previous copies elsewhere should become pointers, archives, or be retired.

Two live sources of truth should not be maintained longer than necessary.
