# Specification Snapshot Versioning

Specification snapshots give AEON-family specs a stable documentation marker
that can be aligned with CTS compatibility snapshots.

They are documentation and coordination identifiers. They are not executable
test targets and do not replace proposal, draft, or published lifecycle status.

## Snapshot Identifiers

Use explicit snapshot identifiers:

```text
<surface>-specs-v<spec-version>-snapshot-<snapshot-version>
```

Examples:

```text
core-specs-v1-snapshot-0.1
aeos-validator-specs-v1-snapshot-0.1
sansa-address-specs-v1-snapshot-0.1
sansa-query-specs-v1-snapshot-0.1
mutate-specs-v1-snapshot-0.1
instruction-specs-v1-snapshot-0.1
```

The `v<spec-version>` segment names the specification line. The
`snapshot-<snapshot-version>` segment names a stable documentation point within
that line. Snapshot versions are independent of implementation package versions.

## Relation To CTS

CTS snapshots use the parallel form:

```text
<surface>-cts-v<spec-version>-snapshot-<snapshot-version>
```

For example:

```text
mutate-specs-v1-snapshot-0.1
mutate-cts-v1-snapshot-0.1
```

The spec snapshot identifies the specification text being implemented. The CTS
snapshot identifies the executable compatibility target used to verify behavior.

When the alignment is known, CTS manifests may record the corresponding spec
snapshot id. The spec snapshot remains documentation-facing; the CTS snapshot
remains the conformance target.

## Lifecycle

Snapshot identifiers do not promote a document through the lifecycle by
themselves. A proposal can have a snapshot, a draft can have a snapshot, and a
published specification can have a snapshot.

Released or externally claimed snapshots should not be rewritten in place. If
the text changes in a way that affects interpretation, create a newer snapshot
identifier, such as:

```text
sansa-query-specs-v1-snapshot-0.1
sansa-query-specs-v1-snapshot-0.2
```

Small editorial changes that do not affect meaning may remain part of the same
snapshot when maintainers explicitly treat them as non-normative cleanup.
