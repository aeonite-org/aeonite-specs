# Aeonic Operations comparison snapshot 0.1

Created locally on 2026-11-09. Documentation marker:
`aeonic-operations-specs-v1-snapshot-0.1`.

The frozen resources are under
`resources/aeonic-operations/v1/snapshots/0.1/`:

- `aeonic-semantic-language-v1.aeon`: the captured specification source, with a
  snapshot identity, unpublished projection path and pinned schema link.
- `comparison-contract.schema.json`: the captured operation request/result
  schema with an immutable snapshot resource identifier.

The captured source retains proposal lifecycle and mixed normativity. The
snapshot identifies a reproducible comparison contract; it does not promote
the full Aeonic Semantic Language document or stabilize deferred arithmetic,
temporal, sorting, collation or conversion surfaces.

Its scope is exact finite-number, Unicode-scalar string, Boolean and symbol
comparison, symbolic outputs, deterministic fail-closed diagnostics, resource
capacities, and separately selectable declared symbol ordering.

The parallel compatibility target is
`aeonic-operations-cts-v1-snapshot-0.1` in `aeonite-cts`. Its manifest pins the
exact source and schema SHA-256 digests, alongside its own binding and suites.
Changes require a newer snapshot; do not rewrite these resources in place.
The mutable source and schema remain available for follow-up work.
