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
  aes/v1/
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

## Coordinated implementation releases

The [shared AEON 0.17.0 checklist](https://github.com/AltoPelago/roadmap/blob/main/aeon/work-in-progress/release-0.17.0-checklist.md)
uses implementation betas while work lands and RCs once declared scope is complete.
Record exact reviewed specification revisions and any required immutable resource
snapshots before implementation RC acceptance. Keep normative review, snapshot
identifiers and language versions under this repository's existing authority;
an implementation beta/RC does not publish or rename a specification snapshot.
Retain historical snapshot bytes and distinguish proposed contracts from adopted
ones. Run this repository's validation and consuming publisher checks for changes.

## Validation

Before committing, run:

```sh
bash ./scripts/pre-commit-check.sh
```

This checks portable paths, the 98-document source inventory, required envelope declarations,
identifier uniqueness, date ordering, related-document IDs, publication links and anchors, referenced
publication assets, and the contract-resource bundle. Full AEON and &ND parsing, projection tests, and
website checks run in the consuming publication build.

## Public repositories

- [`aeonite-org/aeonite-specs`](https://github.com/aeonite-org/aeonite-specs) is the canonical specification source.
- [`aeonite-org/aeonite-cts`](https://github.com/aeonite-org/aeonite-cts) owns public conformance suites, runners, and CTS protocol material.

## Licensing

This repository uses artifact-specific licenses. Normative specifications and appendices use
`CC-BY-4.0`, conventions and reusable examples use `CC0-1.0`, and repository maintenance scripts use
`MIT`, unless an AEON envelope or file declares otherwise. See `LICENSE.md` and `LICENSES/`.


## Exact arithmetic snapshot 0.1

`resources/aeonic-operations/v1/snapshots/0.1/aeonic-arithmetic-v1.aeon`
and its `arithmetic-contract.schema.json` freeze
`aeonic-arithmetic-specs-v1-snapshot-0.1`. They cover exact addition,
subtraction, multiplication, chaining, history and explicit materialization.
The parallel CTS target is `aeonic-arithmetic-cts-v1-snapshot-0.1`.
Snapshot source/schema bytes are immutable; working source and schema retain
separate paths for future changes. The proposal remains unpublished and
comparison snapshots retain their existing scope.

## Rational arithmetic working draft

`sources/aes/v1/aeonic-rational-arithmetic-v1.aeon` and
`resources/aeonic-operations/v1/rational-arithmetic-contract.schema.json` define
the separate, explicitly selected `aeonic.operations.arithmetic.rational.v1`
proposal. It covers exact rational chaining, seven explicit grid-rounding modes,
history, deterministic diagnostics and portable workspace admission. Its CTS
lane is `aeonic-rational-arithmetic`; the working target remains mutable.
Publication is disabled. Existing finite/comparison snapshots and defaults retain
their contracts. No implementation conformance or capacity is established by
this draft; independent-runtime calibration is required before a snapshot.

## Rational arithmetic snapshot 0.2

The [snapshot record](docs/aeonic-rational-arithmetic-snapshot-0.2.md) identifies
`aeonic-rational-arithmetic-specs-v1-snapshot-0.2`. Its source and closed schema
are under `resources/aeonic-operations/v1/snapshots/0.2/`, aligned with the
parallel CTS snapshot. The six-operation profile, exact chaining, explicit
rounding, history and fail-closed diagnostics retain the tested working semantics.
The mutable source remains separate; lifecycle, publication and existing defaults
are unchanged. Snapshot preparation is separate from an implementation's claim.

## Civil-date temporal working contract

[`aeonic-temporal-civil-date-v1.aeon`](sources/aes/v1/aeonic-temporal-civil-date-v1.aeon)
and its [closed schema](resources/aeonic-operations/v1/civil-date-contract.schema.json)
define the explicitly selected `aeonic.operations.temporal.civil-date.v1`
proposal. Relations and calendar arithmetic are independently claimable complete
capabilities sharing exact canonical date ranges, declared origin/clamping
history, fail-closed diagnostics and portable calendar-work admission. ISO civil
dates stay within years 0001–9999. Clock, WTC, timezone and non-ISO resolution
remain outside this profile. The source is unpublished and mutable; no temporal
implementation, frozen snapshot or capacity claim is established here.

## Deferred value semantics guidance

The informative, unpublished proposals
[`aeonic-value-types-risk-analysis-v1.aeon`](sources/aes/v1/aeonic-value-types-risk-analysis-v1.aeon)
and [`aeonic-deferred-value-guidance-v1.aeon`](sources/aes/v1/aeonic-deferred-value-guidance-v1.aeon)
retain the exploratory value-type risk report and guidance for future operations.
They distinguish value identity from interpretation, infinity from indeterminate
outcomes, and explicit skip/stop processing policies from arithmetic values.
Scores remain provisional; unresolved behavior requires a future contract.
These documents introduce no implementation, CTS capability or snapshot changes.

## Unicode hardening regression data

The [candidate regression contract and capability inventory](docs/unicode-hardening-regression-contract.md) records existing identity, casing, wildcard, UTF-16 length and search responsibilities. This implementation-test work does not promote an immutable snapshot or add a released profile/CTS claim.

## Civil-date temporal snapshot 0.1

The [snapshot record](docs/aeonic-temporal-civil-date-snapshot-0.1.md) identifies
`aeonic-temporal-civil-date-specs-v1-snapshot-0.1`. Its source and closed schema
are frozen under `resources/aeonic-operations/v1/snapshots/0.1/`, aligned with
the parallel CTS snapshot. Relations and Calendar remain independent complete
capabilities. Working source/schema retain separate mutable paths; publication,
profile selection and all earlier snapshots remain unchanged. Implementation
claims must retain actual frozen-target executions and separate capacity evidence.

## Unqualified civil date-time working contract

[`aeonic-temporal-civil-datetime-v1.aeon`](sources/aes/v1/aeonic-temporal-civil-datetime-v1.aeon)
and its [closed schema](resources/aeonic-operations/v1/civil-datetime-contract.schema.json)
define a separate explicitly selected, unpublished working profile. Complete
Relations and Arithmetic capabilities share exact canonical point/interval sets,
independent origins and sticky clamping/approximation histories. Calendar shifts,
finite-decimal clock-coordinate shifts, complete-period steps and exact
materialization preserve gaps and endpoint membership. Portable admission guards
expansion and exact fractional arithmetic before allocation. Timezone/WTC,
elapsed-time authority and existing frozen snapshots remain separate. The
mutable CTS lane is `aeonic-temporal-civil-datetime`; this working contract
establishes no implementation conformance or native capacity.

## Property-selector candidate

The unpublished [property-selector proposal](sources/sansa/v1/property-selectors-v1.aeon)
and [0.1 contract resource](resources/sansa/v1/property-selectors-candidate.json)
prepare exact key/tag predicates, authorized property scope, additive adapter APIs
and bounded experimental verification. They add no runtime support or released
conformance claim. Positions and broader consumer admission remain separate;
publication, implementation adoption and release/deployment are not implied.
