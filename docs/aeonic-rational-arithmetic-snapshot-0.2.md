# Aeonic rational arithmetic snapshot 0.2

Frozen locally on 2026-11-14. Documentation marker:
`aeonic-rational-arithmetic-specs-v1-snapshot-0.2`.

The captured source and closed request/result schema are under
`resources/aeonic-operations/v1/snapshots/0.2/`. Their snapshot identities and
resource links are distinct from the mutable source/schema. Numerical semantics,
validation precedence, workspace recipes and seven rounding modes are retained.
Proposal lifecycle and disabled publication remain unchanged.

The complete capability is exact addition, subtraction, multiplication and
division over authored finite and normalized derived decimal/rational operands,
explicit positive-increment quantization, and exact Number materialization.
History and current-operation evaluation remain separate; all errors fail closed.
This introduces no fraction literal, implicit rounding, default profile change,
package release or application convenience result contract.

The parallel CTS target is `aeonic-rational-arithmetic-cts-v1-snapshot-0.2`.
It pins these bytes and its own binding/suites/shared helper, with an explicit
selected limit map. Independent JavaScript and Python implementations have
passed the working target and separate capacity probes; implementation claims
must retain their actual frozen-target executions and exact fingerprints.
Artifact-only validation is not semantic conformance. A finite test suite is
evidence rather than a proof, and capacity dimensions do not promise their
Cartesian product, whole-chain budget or machine-time/memory guarantees.

The mutable `.next.json` CTS target advances to snapshot 0.3. The working source
and schema remain available for follow-up work; older comparison and finite
arithmetic snapshots retain their existing bytes and scope. New interpretations
require a newer snapshot rather than edits to these frozen resources.
