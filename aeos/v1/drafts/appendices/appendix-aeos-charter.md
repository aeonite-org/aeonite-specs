---
id: appendix-aeos-charter-v1
title: Appendix - AEOS v1 Charter
description: Charter-level scope and governance constraints for AEOS validation behavior.
family: appendices-v1
group: AEOS and Profiles
path: specification/appendices/appendix-aeos-charter-v1
---

# AEOS v1 Charter

**AEON Schema Validation System — Version 1**

**Status:** decision-needed for consolidated v1
**Scope:** AEOS v1 implementations and compatible third-party schema validators

Canonical topic owner: `../AEOS-spec-v1.md`

This appendix captures earlier AEOS boundary language and must not override the consolidated AEOS v1 specification.
If this appendix conflicts with `AEOS-spec-v1.md`, `AEOS-spec-v1.md` wins.

---

## 0. Purpose

This charter defines the **constitutional constraints** under which **AEOS v1** operates.

AEOS exists to provide **structural and representational validation** of AEON documents **without interpreting their meaning**.

This document answers one question only:

> **What is AEOS v1 allowed to do — and what must it never do?**

Anything not explicitly permitted here is out of scope for AEOS v1.

---

## 1. Foundational Axioms

### 1.1 Single Source of Truth

AEOS consumes the **Assignment Event Stream (AES)** as produced by AEON Core.

* AES is **ordered**
* AES is **immutable**
* AES is **lossless**
* AES is **uninterpreted**

AEOS MUST treat AES as a **read-only ledger**.

---

### 1.2 Deferred Meaning

AEOS does **not** assign meaning to values.

AEOS validates **representations**, not **interpretations**.

> AEOS answers: *“Is this representation acceptable?”*
> AEOS does not answer: *“What does this value mean?”*

---

### 1.3 One-Way Pipeline

AEOS participates in a strictly **one-directional pipeline**:

```
AEON Core → AES → AEOS → Processor / Elixir → Output
```

AEOS MUST NOT introduce backward dependencies or feedback loops.

---

## 2. Phase Authority

AEOS implements **Phase 6 only** of the AEON conceptual model.

| Phase                                  | Authority            |
| -------------------------------------- | -------------------- |
| Parsing, Path Resolution, AES Emission | AEON Core            |
| **Schema Validation**                  | **AEOS v1**          |
| Profile Interpretation                 | Processors / Elixirs |
| Reference Evaluation                   | Processors / Elixirs |
| Materialization                        | Processors / Elixirs |

AEOS MUST NOT perform behavior belonging to any other phase.

---

## 3. Inputs

### 3.1 Required Input

AEOS v1 MUST accept:

* A complete **Assignment Event Stream (AES)**
* Optional schema definitions

AEOS MUST NOT operate on:

* source text
* ASTs
* partially emitted event streams

---

### 3.2 Recovery Awareness

If AES was emitted in recovery mode, this MUST be explicit via metadata:

```ts
AES.meta.recovery_mode ::= 
  "none" | "allow-duplicates" | "best-effort"
```

AEOS MUST NOT infer recovery intent implicitly.

---

## 4. Outputs

### 4.1 Validator Result Envelope (Normative)

AEOS v1 MUST emit a result object with the following minimum structure:

```json
{
  "ok": true,
  "errors": [],
  "warnings": [],
  "guarantees": {}
}
```

When validation fails, `ok` MUST be `false` and errors MUST be populated.

---

### 4.2 Error Requirements

Each error MUST include:

* `path` — canonical path
* `span` — source span (when available)
* `message` — human-readable description
* `phase` — `"schema_validation"`
* `code` — stable, machine-readable identifier

AEOS MUST NOT emit modified AES as output.

---

## 5. Core Responsibilities (What AEOS v1 MAY Do)

AEOS v1 MAY:

1. Validate **structure**

   * required bindings
   * allowed literal kinds
2. Validate **representation eligibility**

   * e.g. “string matches integer pattern”
3. Validate **cross-binding presence**

   * e.g. “if X exists, Y must exist”
4. Validate **annotation/datatype presence**
5. Validate **ordering constraints** (symbolically)
6. Emit **diagnostics**
7. Emit **guarantees** (see Section 6)

All validation is performed against the **entire AES**.

---

## 6. Guarantees

Guarantees are **advisory, non-semantic assertions** emitted by AEOS.

They describe **representation properties only**.

### 6.1 Tier-1 Standard Guarantees (Normative)

AEOS v1 MAY emit the following standardized guarantees:

| Guarantee               | Meaning                        |
| ----------------------- | ------------------------------ |
| `integer-representable` | Value can be parsed as integer |
| `float-representable`   | Value can be parsed as float   |
| `boolean-representable` | Value can be parsed as boolean |
| `non-empty-string`      | StringLiteral length > 0       |
| `regex:<id>`            | Matches named regex            |
| `present`               | Binding exists                 |

Processors MAY rely on Tier-1 guarantees.

---

### 6.2 Tier-2 Namespaced Guarantees (Non-Normative)

AEOS MAY emit namespaced guarantees:

```json
{
  "$.email": ["acme:corporate-email"]
}
```

Rules:

* MUST be namespaced
* MUST NOT be relied upon by generic processors
* MUST NOT affect AEOS conformance

---

## 7. Hard Prohibitions (Non-Negotiable)

AEOS v1 MUST NOT:

1. Coerce values
   (`"42"` → `42`)
2. Resolve references
   (`~`, `~>`)
3. Inject defaults
4. Compute derived values
5. Compare interpreted magnitudes
   (`<`, `>`, arithmetic)
6. Materialize objects
7. Reorder Assignment Events
8. Mutate AES
9. Depend on processors
10. Assume downstream correction

Any of the above disqualifies AEOS v1 conformance.

---

## 8. Uniqueness & Const Semantics

* Each canonical path MUST appear at most once
* Duplicate bindings MUST be treated as errors
  **unless** `AES.meta.recovery_mode` explicitly permits them

Even in recovery mode:

* AEOS MAY observe duplicates
* AEOS MUST NOT reconcile or resolve them

---

## 9. Failure Model

AEOS v1 is **fail-closed**:

* All constraints are evaluated
* Any failure results in `ok: false`
* No partial acceptance
* No speculative success

Recovery behavior is observational only.

---

## 10. Canonical Validation Scenarios (Normative Examples)

### 10.1 Representation Eligibility

```aeon
age = "42"
```

Valid if schema allows `integer-representable`.
AEOS does **not** parse `"42"` into a number.

---

### 10.2 Cross-Binding Presence

```aeon
tls.enabled = true
```

Valid only if:

```aeon
tls.cert = ...
```

exists earlier or later in AES.

---

### 10.3 Ordering Constraint

```aeon
b = ~a
a = 1
```

Invalid — reference targets a later binding.

---

## 11. Non-Goals of AEOS v1

AEOS v1 explicitly does **not** provide:

* interpretation
* evaluation
* coercion
* defaults
* computation
* reference resolution
* runtime configuration
* materialized output

These are delegated to processors and elixirs.

---

## 12. Versioning Commitment

AEOS v1 behavior defined in this charter is **stable**.

Any relaxation of prohibitions or expansion of authority constitutes a **new major version**.

---

## Closing Statement

> **AEOS validates form, not meaning.
> Meaning is deferred, never assumed.
> This separation is the foundation of AEON’s integrity.**

---
