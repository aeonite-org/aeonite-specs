---
id: contracts-artifacts-overview
title: v1 Contract Artifacts
description: "Overview of the published contract artifacts, including the general-purpose profile, general-purpose schema, and registry files."
family: contracts
group: Contracts Overview
status: Draft
license: CC-BY-4.0
path: specification/contracts/v1-contract-artifacts
links:
  - aeon-v1-contracts
---

# v1 Contract Artifacts

This page lists the published baseline contract artifacts for:

- `aeon.gp.profile.v1`
- `aeon.gp.schema.v1`

## Published artifacts

### `profiles/aeon.gp.profile.v1.aeon`

The baseline general-purpose profile artifact. This is the published profile identifier implementers can match against when selecting shared processing behavior for AEON v1 documents.

### `schemas/aeon.gp.schema.v1.aeon`

The baseline general-purpose schema artifact. This is the published schema identifier and schema definition surface used for validation-oriented contract selection.

### `registry.json`

The registry file that maps published contract ids to their authoritative artifact paths. Consumers and tooling can use this as the trusted lookup surface for baseline contract resolution.

These files are the published artifact surface used by runtime and CLI contract selection flows. For the surrounding rules and authority boundaries, see the [AEON v1 Contracts Specification](./contracts-v1.md).
