---
license: CC-BY-4.0
---

# Changelog

All notable changes to `aeonite-specs` are tracked here.

This changelog follows the release-governance sections used by the AEON v1 draft governance policy:

- Added
- Changed
- Fixed
- Removed
- Spec Impact
- CTS Impact

## Unreleased

### Added

- Added initial SANSA v1 draft specification tree under `sansa/v1/drafts/`.
- Promoted SANSA Addressing and Resolve documents to draft status.
- Added SANSA lifecycle placeholders for `sansa/v1/proposals/` and `sansa/v1/published/`.

### Changed

- Changed AEON draft encoding-family literal syntax from `$payload` to `&payload`.
- Changed NEON draft AEON integration examples and text-preservation guidance to use `&...` encoding literals.
- Expanded Shared AEON Value Semantics proposal with explicit profile-selection, string collation, temporal comparison, and mutation-compatibility guidance.
- Added a value-family semantic classification table covering AEON Core reserved value families, references, separator literals, SANSA literals, containers, and custom datatype labels.
- Added the missing `nan` entry to the AEON v1 reserved datatype-name table to match existing NaN examples and compatibility text.
- Clarified toggle semantics: toggle-token equality is exact, while Boolean compatibility requires explicit conversion or a profile-defined comparison domain.
- Broadened `isValue(...)` semantics to mean any concrete value outside the non-value group, rather than only finite number/string/Boolean scalar values.
- Clarified hex semantics: `HexLiteral` is distinct from `RadixLiteral`, canonical hex-payload identity is not numeric/radix/color/byte equality, and richer interpretations require explicit profiles.
- Clarified that `radix16` is not a reserved Core v1 shorthand; base-16 radix values use `radix[16]` and remain distinct from `hex`.
- Clarified encoding semantics: `EncodingLiteral` has payload-string identity by default, `base64` is not `radix[64]`, and decoding, byte identity, media type, and text interpretation require explicit profiles.
- Added encoding-family naïve payload order over preserved encoded payload characters.
- Added separator-literal naïve order over canonical separator payloads, while reserving IP, version, dimension, delimited-record, and other domain ordering for explicit profiles.
- Clarified that naïve separator order never splits payloads, and profile-defined splitting/order must treat separator specs as claims unless trusted or validated.
- Clarified SANSA address-literal semantics: address-expression identity/order are syntactic defaults, while exact target identity, selector equivalence, resolution, and AEON versus non-AEON namespace meaning belong to consumers.
- Strengthened SANSA namespace- and domain-neutrality language, clarifying that SANSA member selectors describe semantic traversal rather than AEON object traversal.
- Clarified structural container semantics for `object`, `list`, `tuple`, and `node`, including minimum structural equality, lack of default structural ordering, and schema/profile ownership of mutation compatibility.
- Clarified reference semantics by separating reference-form identity, read-only followed-value inspection through conceptual `follow(reference)`, and reference resolution/materialization.
- Renamed the schema proposal's reference-inspection control from `resolve_reference_form` to `follow_reference_form` to avoid implying materialization or value substitution.
- Clarified SANSA.Query consumes active Shared AEON Value Semantics profiles for ordering, comparison, case mapping, and future temporal behavior.
- Aligned Shared AEON Value Semantics proposal-stage profile identifiers with the implementation surface, including `aeon.value.default.v1`, `aeon.value.string.codepoint.v1`, and explicit locale profile examples such as `aeon.value.string.locale.fr.v1`.
- Updated the repository README layout to include SANSA as a first-class specification family.
- Updated the repository README to point to this changelog as the release-facing change history.

### Fixed

- None.

### Removed

- None.

### Spec Impact

- Introduces draft SANSA specification text for semantic addressing and deterministic structural resolution.
- Keeps read-only SANSA Query semantics in proposal status while the query surface continues to evolve.
- Starts the encoding-family literal migration by reserving `&` for `encoding`, `base64`, `embed`, and `inline` payload literals in draft spec text.
- Keeps the payload alphabet and payload capture semantics unchanged; the payload excludes the literal prefix.
- Frees `$` for the planned SANSA address literal in the AEON language specification.
- Establishes Shared AEON Value Semantics as the common prerequisite for SANSA.Query temporal comparison and future SANSA.Mutate typed write compatibility.
- Clarifies that separator literals and other textual source forms do not automatically fall back to string semantics; domain-specific comparison requires an active profile.
- Prevents `yes`, `on`, `no`, and `off` from being collapsed into Boolean equality by default.
- Defines the minimum non-value group for value predicates as Missing, explicit null, explicit absence values, and NaN.
- Prevents `hex` from being treated as a shorthand for `radix[16]` or another radix family by default.
- Keeps base-16 radix intent explicit through `radix[16]` rather than adding a potentially confusing `radix16` alias.
- Prevents encoding-family values from being treated as decoded bytes, decoded text, radix values, or generic string collation inputs by default.
- Gives encoding-family values a deterministic portable fallback order without assigning decoded-byte, decoded-text, media, hash, or radix meaning.
- Gives separator literals a deterministic portable fallback order without assigning domain meaning to separator characters.
- Prevents document-local separator specs such as `sep[.]` from silently authorizing semantic splitting, IP parsing, version parsing, or domain ordering.
- Prevents AEON-hosted `:sansa` values from being treated as AEON paths by default when they may target another SANSA-compatible semantic namespace.
- Makes AEON's relationship to SANSA explicit as an AEON binding-model namespace adapter rather than the owner of SANSA traversal semantics.
- Defines minimum structural equality for objects, lists, tuples, and nodes while keeping list/tuple coercion, structural ordering, and mutation behavior explicit.
- Prevents implicit reference following in comparison and validation contexts while keeping reference resolution/materialization separate from explicit read-only followed-value checks.
- Migration: update encoding-family literals from `$payload` to `&payload`.

### CTS Impact

- Updated proposal-stage Value Semantics CTS expectations so `isValue(...)` follows the concrete-value basis, including accepting infinity and container values while excluding Missing, explicit null, explicit absence values, and NaN.
- Added proposal-stage Value Semantics CTS coverage for portable `aeon.value.default.v1` and `aeon.value.string.codepoint.v1` profile selection.
- Updated SANSA.Query CTS expectations to align query `isValue(...)` behavior with the Shared AEON Value Semantics concrete-value basis.
- Future CTS work is expected for SANSA address parsing/canonicalization and the AEON encoding literal prefix migration.
