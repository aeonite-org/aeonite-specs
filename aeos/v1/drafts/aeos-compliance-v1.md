---
id: aeos-v1-compliance
title: AEOS v1 Compliance Specification
description: Conformance requirements for AEOS-specific validator and profile behavior layered on top of AEON core.
group: AEOS Specifications
path: specification/aeos-v1-documentation/aeos-v1-compliance-specification
links:
  - aeos-v1
  - aeon-core-v1-compliance
---

# AEOS v1 Compliance Specification

Status: draft scaffold  
Scope: normative conformance requirements for AEOS-specific behavior layered on top of AEON core.

This document is intentionally introduced as a separate compliance line so AEON core compliance and AEOS compliance are not treated as the same surface.

## 1. Conformance Target

An implementation claiming AEOS v1 conformance SHALL satisfy:
- language and authority-boundary requirements in `AEOS-spec-v1.md`
- AEON Core prerequisites required by the AEOS surface
- `cts.protocol.v1` runner and AEOS lane requirements in `cts/protocol/v1`
- the published AEOS validator manifest:
  - `cts/aeos/v1/aeos-validator-cts.v1.json`

AEOS conformance is validator-surface conformance. It does not replace or weaken AEON Core conformance requirements.

## 2. AEOS Behavior Families

AEOS compliance SHALL be evaluated against validator behavior families, not only by isolated suite success.

The current AEOS behavior families are:
- result-envelope and validator output contract
- schema rule-index integrity
- presence and forbid semantics
- representational type and datatype-label constraints
- reference-form, reference-target, and resolved-reference constraints
- numeric lexical-form constraints
- string length and pattern constraints
- guarantee emission
- container-kind and tuple-arity constraints
- indexed-path validation and tuple positional checks
- separator-literal policy enforcement
- structural container item validation
- Core-versus-AEOS authority boundary preservation

The current anti-drift coverage accounting for these families is tracked in `aeonite-cts/CONFORMANCE-COVERAGE.md`.

## 3. Authority Boundary

An AEOS-conforming implementation MUST:
- consume Core/AES output rather than redefining Core legality
- preserve the ResultEnvelope contract
- preserve canonical-path diagnostics within the AEOS validator surface
- avoid treating Core-owned legality failures as schema-validation failures
- preserve bounded, deterministic behavior for opt-in resolved-reference validation

AEOS conformance is not satisfied by passing only representative examples if validator behavior drifts across one of the AEOS behavior families listed above.

## 4. Status

Detailed AEOS-specific compliance requirements still need to be extracted and consolidated into this document, but the authority split and anti-drift conformance model are now fixed.
