---
id: appendix-altopelago-core-profile-v1
title: Appendix - Altopelago Core Profile v1
description: Informative profile appendix describing the `altopelago.core.v1` profile and its minimal form-oriented behavior.
family: appendices-v1
group: Profiles and Extensions
path: specification/appendices/appendix-altopelago-core-profile-v1
---

# Appendix — Altopelago Core Profile v1

**Profile Name:** `altopelago.core.v1`  
**Status:** informative profile appendix for consolidated v1  
**Determinism:** Deterministic  
**Scope:** Minimal, form-only interpretation aligned with AEON v1 core

Canonical topic owners: `../AEON-spec-v1.md`, `../contracts/`

This appendix describes an extension profile, not the baseline AEON Core v1 conformance target.
If this appendix conflicts with the canonical v1 spec set or baseline contracts, the canonical v1 documents win.

---

## 1. Purpose

The Altopelago Core Profile v1 defines a minimal, stable interpretation layer
for AEON documents. It preserves AEON's form-only semantics and exposes the
Assignment Event Stream (AES) as the primary output. This profile is intended
as the baseline for TypeScript projects that want to parse AEON without
introducing application-specific meaning.

---

## 2. Profile Declaration

```aeon
aeon:header = {
  profile = "altopelago.core.v1"
}
```

Or shorthand:

```aeon
aeon:profile = "altopelago.core.v1"
```

---

## 3. Enabled Features

This profile enables only AEON core grammar and behavior:

- All AEON core literals
- Objects, lists, and tuples
- Attributes
- Clone and pointer references
- Headers and envelope structures

No optional profile extensions are enabled.

---

## 4. Interpretation Rules

The profile is intentionally conservative:

1. **No value coercion.** Literal forms are preserved as parsed.
2. **No reference resolution.** Clone (`~`) and pointer (`~>`) references remain
   symbolic in AES output. The logical reference graph must be preserved.
3. **No attribute semantics.** Attributes are preserved as annotations but are
   not interpreted.
4. **No datatype semantics.** Type hints are preserved but not interpreted.

---

## 5. Schema Interaction

Schema validation is optional:

- If a schema is provided, it must be applied in **validate-only** mode.
- Schema engines must not coerce or transform values.
- In strict mode, schema coercion is forbidden by the AEON spec.

---

## 6. Output Transformation

There is no output transform. The primary output is AES (Assignment Event
Stream) emitted by the AEON core compiler.

This profile does not synthesize additional events. Indexed path events are emitted only from core path resolution behavior over list/tuple structure.

---

## 7. Error Model

No profile-specific error codes are introduced. Implementations should emit
core AEON and AEOS diagnostics.

---

## 8. Canonicalization Rules

No additional canonicalization rules are defined beyond AEON core canonical
form requirements.

---

## 9. Conformance Requirements

An implementation conforming to `altopelago.core.v1` MUST:

- Accept all valid AEON v1 core constructs.
- Reject invalid AEON documents with diagnostics that reference canonical paths.
- Emit exactly one Assignment Event per binding (fail-closed on errors).
- Preserve reference structure (`~` and `~>`), without resolution or flattening.
- Preserve attributes and datatype hints as annotations without interpretation.
- If a schema is provided, apply it in validate-only mode (no coercion).
- In strict mode, prohibit untyped values and schema coercion.

---

## 10. Reference Behavior

The profile preserves AEON reference semantics:

- Clone references express value intent.
- Pointer references express identity intent.
- Pointer chains must not be flattened.

---

## 11. Compatibility Notes

This profile is designed to be the default baseline for TypeScript projects.
It aligns with AEON v1 core behavior and AEOS v1 form validation.
