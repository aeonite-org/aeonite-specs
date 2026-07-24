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
- Clarified SANSA.Query consumes active Shared AEON Value Semantics profiles for ordering, comparison, case mapping, and future temporal behavior.
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
- Migration: update encoding-family literals from `$payload` to `&payload`.

### CTS Impact

- No CTS changes yet.
- Future CTS work is expected for SANSA address parsing/canonicalization and the AEON encoding literal prefix migration.
