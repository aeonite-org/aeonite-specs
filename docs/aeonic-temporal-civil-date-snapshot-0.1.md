# Aeonic civil-date snapshot 0.1

Frozen locally on 2026-11-15 as
`aeonic-temporal-civil-date-specs-v1-snapshot-0.1`. The source and closed schema
are under `resources/aeonic-operations/v1/snapshots/0.1/`, with distinct snapshot
identities and schema links. The working semantics and selected profile are
unchanged; proposal lifecycle and disabled publication are retained.

The two independently claimable complete capabilities are Relations
(`equal`, `compare`, `relate`) and Calendar (`shift`, `step`, `materialize`).
Both share canonical nonempty exact date-range sets within years 0001–9999,
origin granularity, sticky clamping history, explicit profile selection,
fail-closed diagnostics and portable calendar-piece work admission. A broader
containing-period display must never widen coverage used by later operations.

The parallel target is `aeonic-temporal-civil-date-cts-v1-snapshot-0.1`.
It pins this source/schema and its own binding, suites and helper artifacts.
A stable implementation claim requires successful semantic execution at the
claimed capability selection and selected limits. Artifact checks alone cannot
establish conformance. Independent default-capacity calibration remains separate;
selected dimensions do not promise their Cartesian product, a whole-chain budget
or machine-time/heap bounds. Clock, timezone, WTC, database/calendar authority
resolution, package publication and SANSA integration remain separate work.

The mutable CTS target advances to snapshot 0.2. Working source and schema stay
at their existing paths for future changes. Existing snapshots retain their
bytes; changed interpretations require a newer snapshot.
