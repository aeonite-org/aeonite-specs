---
id: appendix-tonic-v1
title: Appendix - Tonic Processor Governance
description: Governance model and operational constraints for tonic processor behavior.
family: appendices-v1
group: AEOS and Profiles
path: specification/appendices/appendix-tonic-v1
---

# Appendix — Tonic Processor Governance

**Appendix to:** AEON Specification v1
**Status:** informative appendix for consolidated v1

This appendix defines the canonical terminology for AEON's downstream materialization processor (Tonic), the phase boundary contract, reference policies, and determinism requirements.

Canonical topic owners: `../AEON-spec-v1.md`, `../AEOS-spec-v1.md`

This appendix covers downstream processor guidance and terminology.
If this appendix conflicts with the canonical v1 spec set, the canonical v1 spec set wins.

---

## 1. Terminology

**Tonic** is the canonical term for the downstream processor that consumes the Assignment Event Stream (AES) and materializes it into a runtime or domain representation.

- Previous terminology: "Elixir" — **deprecated**
- Public external naming: `AEON Tonic`
- Transitional aliases for the deprecated term are permitted for one major release cycle, with warnings

---

## 2. Pipeline Contract

```
Text → AEON Core → AES → AEOS (optional) → Tonic → Runtime
```

Key invariants:
- Tonic consumes AES, never raw text
- Tonic operates after AEOS validation (if any)
- Tonic does not re-enter the AEON Core parse phase
- The pipeline is strictly ordered and fail-closed

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  AEON Core  │ →  │     AES     │ →  │    AEOS     │ →  │    Tonic    │ →  │   Runtime   │
│  (Parse)    │    │  (Output)   │    │ (Optional)  │    │(Materialize)│    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 3. Tonic Responsibilities

A Tonic MAY:
- Perform domain materialization (e.g., AEON → TypeScript object)
- Apply policy-driven runtime shaping
- Resolve references according to its declared reference mode
- Apply profile-specified processors

A Tonic MUST NOT:
- Re-parse raw AEON text
- Mutate the AES
- Rewrite canonical paths
- Suppress core diagnostics
- Introduce implicit semantics based on document content

---

## 4. Determinism Requirements

A Tonic MUST be deterministic:

> Given identical AES + configuration, Tonic output and diagnostics MUST be identical.

Prohibited implicit dependencies:
- Current time or date
- Random values
- Network state
- Filesystem state (unless explicitly configured and stable)
- Process environment (beyond declared configuration)

---

## 5. Reference Policy Modes

Each Tonic explicitly declares one reference mode:

| Mode       | Behavior                                                              |
| ---------- | --------------------------------------------------------------------- |
| `preserve` | References are kept as symbolic tokens in output (default)            |
| `alias`    | References create named aliases in runtime representation             |
| `inline`   | References are resolved and values are inlined (explicit opt-in only) |

Reference mode MUST be declared in Tonic configuration, not inferred from document content.

DoS budgets are mandatory for non-trivial resolution behavior (particularly `alias` and `inline` modes).

### 5.1 Reference Diagnostic Transparency

Reference diagnostics MUST include:
- Origin anchor (the path of the reference source)
- Target anchor (the path being referenced)

---

## 6. Two-Stage Hook Model

Tonics that support processing hooks MUST follow a two-stage model:

### Stage A: Validate / Plan

- No mutation
- Produce diagnostics and an action plan

### Stage B: Apply / Materialize

- Deterministic mutation allowed
- Apply action plan in fixed order

**Fail-closed invariant:** Stage B is skipped entirely if Stage A produces errors.

### 6.1 Hook Precedence

When multiple hook types could match a binding:

1. Key/path hook (highest specificity)
2. Datatype hook
3. Auto-hook
4. Baseline handler

Hooks may defer to the next precedence level.

---

## 7. Null Universe

Configurable null behavior is a Tonic policy decision, not a Core semantics decision.

Supported null modes (Tonic-declared):
- `void` — Value is absent/undefined
- `null` — Explicit `null` value (language-specific)
- `undefined` — Language-level undefined

The mode MUST be declared in Tonic configuration and applied consistently.

---

## 8. Authority Boundary

| Layer     | Responsibility                                            |
| --------- | --------------------------------------------------------- |
| AEON Core | Parse, emit AES, assign canonical paths                   |
| AEOS      | Structural validation (form-level constraints)            |
| Tonic     | Semantic interpretation, materialization, runtime shaping |

AEOS remains a form validator. Semantic interpretation and materialization policy belong to Tonic.

---

## 9. Compatibility Governance

- Transitional aliases for deprecated `Elixir` naming are allowed for one major release cycle
- Implementations using old terminology MUST emit deprecation warnings
- Final cutoff for deprecated alias support is an open decision (see §10)

---

## 10. Open Items

- Migration cutoff date for deprecated `Elixir` naming aliases
- Minimum required DoS budget defaults for first public baseline
- Whether `inline` mode is supported in first public release or deferred to a follow-up

---

## 11. Related v1 Sections

- `specs/04-official/v1/AEON-spec-v1.md` (core language boundary and conformance)
- `specs/04-official/v1/AEOS-spec-v1.md` (schema/validation boundary)
- `specs/04-official/v1/appendices/appendix-processing-model.md` (phase and processor model)
- `specs/04-official/v1/appendices/appendix-error-model.md` (diagnostics and fail-closed behavior)
