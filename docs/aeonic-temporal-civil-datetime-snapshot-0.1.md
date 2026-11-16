# Aeonic civil date-time snapshot 0.1

Frozen locally on 2026-11-16 as
`aeonic-temporal-civil-datetime-specs-v1-snapshot-0.1`. The source and closed schema
are under `resources/aeonic-operations/v1/snapshots/0.1/`, with distinct snapshot
identities and schema links. Proposal lifecycle and disabled publication remain.

Relations (`equal`, `compare`, `relate`) and Arithmetic (`shift`, `shiftClock`,
`step`, `materialize`) are independently complete capabilities. They share
canonical nonempty exact point/interval sets, included/excluded endpoints,
explicit profile selection, independent origins and sticky clamping/approximation
histories, no-value diagnostics and portable work/piece/numeric admission.
Containing displays cannot widen coverage used by chained operations.

The freeze makes existing finite Number grammar reuse explicit (no leading-zero
integer mantissas), uses scalar character counts consistently, and distinguishes
bounded input decoding from compact amount expansion. These match the merged
JavaScript/Python behavior; no new rounding or temporal interpretation is added.

The parallel CTS target is `aeonic-temporal-civil-datetime-cts-v1-snapshot-0.1`.
Only actual successful semantic execution at a complete selected capability set
and explicit limits can support a stable implementation claim. Artifact-only
checks, test replays and native capacity probes establish separate facts.
Mutable next advances to 0.2. Prior immutable snapshots retain their bytes.

This freeze is not a package release, website deployment or SANSA/Query adoption.
Known offsets, timezone/WTC, leap-second and elapsed-time authority remain separate.
