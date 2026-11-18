# Aeonic civil clock snapshot 0.1

Frozen on 2026-11-18 as `aeonic-temporal-civil-clock-specs-v1-snapshot-0.1`.
The source and closed schema live under
`resources/aeonic-operations/v1/snapshots/0.1/`, with distinct snapshot identities
and schema links. Proposal lifecycle and disabled publication remain.

Relations (`equal`, `compare`, `relate`) and Arithmetic (`shiftClock`, `step`,
`materialize`) are independently complete. Canonical nonempty exact point/interval
sets retain signed relative days, included/excluded boundaries, origin and sticky
approximation history. Materialization requires exact coverage beginning on day
zero and cannot discard carry. Explicit profile selection, deterministic no-value
diagnostics and portable work/workspace/resource rules are unchanged by the freeze.

The corresponding CTS snapshot is
`aeonic-temporal-civil-clock-cts-v1-snapshot-0.1`. Only a successful genuine semantic
execution of a complete selected capability can support a stable implementation
claim. Artifact checks, fixture replays and native capacity probes establish
separate facts. Mutable next advances to 0.2 without changing the profile/defaults.

The merged JavaScript/Python source implementations provide the pre-freeze semantic
and native-capacity evidence. Frozen-target runs are verified separately; implementation
claims must explicitly adopt that target. This freeze changes status, identities and
asset links, not operation semantics, fixtures or resource allowances. Previous
immutable artifacts retain their bytes. It is not a package release, deployment,
SANSA/Query/Rust adoption or timezone/WTC/date-anchoring capability.
