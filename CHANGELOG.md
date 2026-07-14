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
- Added SANSA draft overview, addressing, Resolve, and Query documents.
- Added SANSA lifecycle placeholders for `sansa/v1/proposals/` and `sansa/v1/published/`.

### Changed

- Changed AEON draft encoding-family literal syntax from `$payload` to `&payload`.
- Changed NEON draft AEON integration examples and text-preservation guidance to use `&...` encoding literals.
- Updated the repository README layout to include SANSA as a first-class specification family.
- Updated the repository README to point to this changelog as the release-facing change history.

### Fixed

- None.

### Removed

- None.

### Spec Impact

- Introduces draft SANSA specification text for semantic addressing, deterministic structural resolution, and read-only query semantics.
- Starts the encoding-family literal migration by reserving `&` for `encoding`, `base64`, `embed`, and `inline` payload literals in draft spec text.
- Keeps the payload alphabet and payload capture semantics unchanged; the payload excludes the literal prefix.
- Frees `$` for the planned SANSA address literal in the AEON language specification.
- Migration: update encoding-family literals from `$payload` to `&payload`.

### CTS Impact

- No CTS changes yet.
- Future CTS work is expected for SANSA address parsing/canonicalization and the AEON encoding literal prefix migration.
