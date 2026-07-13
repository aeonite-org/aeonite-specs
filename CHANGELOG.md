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

- Updated the repository README layout to include SANSA as a first-class specification family.
- Updated the repository README to point to this changelog as the release-facing change history.

### Fixed

- None.

### Removed

- None.

### Spec Impact

- Introduces draft SANSA specification text for semantic addressing, deterministic structural resolution, and read-only query semantics.
- Documents the planned dependency that AEON encoding-family literals move from `$` to `&` before `$` is used for SANSA address literals in the AEON language specification.
- Migration: none for current published specifications; SANSA material is draft-only.

### CTS Impact

- No CTS changes yet.
- Future CTS work is expected for SANSA address parsing/canonicalization and the AEON encoding literal prefix migration.

