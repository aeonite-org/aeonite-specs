---
id: aeon-v1-release-governance
title: AEON v1 Release Governance
description: Governance policy for AEON v1 releases, changelog rules, version claims, and how conformance claims relate to released artifacts.
group: Core Specifications
path: specification/aeon-v1-documentation/aeon-v1-release-governance
links:
  - aeon-core-v1
  - aeon-core-v1-compliance
  - aeon-v1-conformance-matrix
---

# AEON v1 Release Governance

Status: official v1 governance policy  
Scope: release tags, branching, changelog/migration rules, and conformance-claim format for AEON v1.

## 1. Purpose

This document defines how AEON v1 releases are cut, identified, and claimed.

It exists to keep four things stable:
- immutable public release history
- unambiguous spec-to-implementation mapping
- clear migration signaling
- version-scoped conformance claims

## 2. Release Units

AEON release governance tracks three related but distinct release units:

1. specification line
- example: `AEON v1`
- governs normative language behavior and contracts

2. contract artifacts
- examples:
  - `aeon.gp.profile.v1`
  - `aeon.gp.schema.v1`
- governed by contract-layer identifiers and contract artifact versions

3. implementation packages
- examples:
  - `@aeon/core`
  - `@aeon/cli`
  - `@aeon/aeos`
- governed by package semver

Patch or implementation fixes do not change the specification-line identity unless normative behavior changes.

### 2.1 Locked Layer Naming

Specification line:
- `AEON v1`

Code-layer release labels:
- `AEON.core v1.0.0`
- `AEON.schema v1.0.0`
- `AEON.gp.tonic v1.0.0`

Contract-layer identifiers:
- `aeon.gp.profile.v1`
- `aeon.gp.schema.v1`

## 3. Tag Strategy

Release tags MUST be immutable.

Required rules:
- use annotated git tags for public releases
- never retag an existing released version
- if a release is bad, publish a new version; do not move the old tag

Recommended tag forms:
- spec baseline tags:
  - `spec/v1.0.0`
  - `spec/v1.0.1`
- repository release tags:
  - `release/v1.0.0`
  - `release/v1.0.1`

Practical rule:
- `spec/*` identifies the normative documentation/contracts baseline
- `release/*` identifies the repository snapshot that ships that baseline

If only one tag family is maintained, use `release/vX.Y.Z` and ensure the release notes explicitly name the matching spec baseline.

## 4. Branch Strategy

AEON uses a simple trunk-plus-release-branch model.

Branches:
- `main`
  - integration branch for the next unreleased change set
- `release/v1`
  - stabilization branch for the active v1 release line
- short-lived topic branches
  - recommended prefix: `codex/` or contributor-specific topic names

Rules:
- feature work lands in topic branches, then merges into `main`
- once release hardening begins for v1, cut `release/v1` from `main`
- patch releases for v1 are cut from `release/v1`
- `main` may continue with future work after the release branch is cut
- fixes needed in both places should land in `release/v1` and be forward-merged to `main`, or land in `main` and be cherry-picked with explicit tracking

Non-goal:
- no long-lived archive branches per historical release

Immutable tags are the archive.

## 5. Release Process

Minimum release process for a public AEON v1 release:

1. freeze target scope
- accepted proposals for the release must already be reflected in:
  - canonical docs
  - CTS
  - shipped implementation behavior

2. run release gate
- run required test and CTS commands for the target implementation set
- run canonical CTS lane (`bash ./scripts/canonical-cts.sh --mode all --brief`)
- confirm contract artifacts and registry hashes are current

3. update release metadata
- changelog entry
- release notes summary
- conformance claim statement

4. cut tag
- create immutable annotated release tag

5. publish artifacts
- source snapshot
- contract artifacts
- package artifacts if applicable

## 6. Changelog and Migration Requirements

Every public release MUST include a changelog entry.

Changelog sections:
- Added
- Changed
- Fixed
- Removed
- Spec Impact
- CTS Impact

Migration notes are REQUIRED when any of the following occur:
- normative behavior changes
- diagnostics relied on by CTS/users change
- contract document shape changes
- CLI/runtime flags change
- canonical examples or accepted syntax forms change

If no migration action is required, state:
- `Migration: none`

## 7. Conformance Claim Format

Conformance claims MUST be explicit about:
- implementation identity
- implementation version
- specification line
- CTS protocol version
- lanes executed
- result date

Recommended format:

```text
Implementation: @aeon/cli 1.0.0
Claims: AEON Core v1.0.0, AEOS v1.0.0
CTS Protocol: cts.protocol.v1
CTS Lanes:
- cts/core/v1
- cts/aes/v1
- cts/annotations/v1
- cts/aeos/v1
Result: pass
Date: 2026-03-06
```

Rules:
- claims are version-scoped
- passing one lane does not imply passing all lanes
- a package may claim only the layers/lane coverage it actually passed
- contract IDs and implementation package versions must not be conflated

## 8. Archive Policy

AEON does not require a separate archive repository.

Policy:
- immutable git tags and release artifacts are the archive
- old release lines remain available through tags/releases
- superseded docs may remain in-repo as historical material if clearly labeled, but active conformance claims point only to the canonical v1 surface

## 9. Branching Model Publication

This document is the published branching model for AEON v1.

It supersedes the older checklist placeholder target:
- `setup/branching-release-model.md`

The branching model is intentionally kept inside the versioned spec/governance surface so release policy evolves alongside the language and CTS.
