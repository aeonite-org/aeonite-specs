---
id: aeon-conventions-overview
title: AEON Conventions Overview
description: Overview of what conventions are, how they relate to core syntax, and how documents declare them.
family: conventions
group: Convention Overview
status: Draft
path: specification/conventions/overview
license: CC-BY-4.0
---

# AEON Conventions Overview

## Overview

AEON conventions define **standardized interpretation rules** layered on top of AEON core.

AEON core defines only:

* syntax
* structural semantics
* canonicalization rules
* assignment event semantics

Conventions define how structured data **should be interpreted or processed** by cooperating systems.

Conventions allow AEON to support:

* measurement interpretation
* document metadata
* contextual annotations
* security envelopes
* domain-specific semantics

without changing the core language.

---

# Design Principles

AEON conventions follow several principles.

### Core Minimalism

AEON core remains small and stable.

Conventions provide higher-level meaning without expanding the language itself.

### Explicit Adoption

Conventions are never assumed.

A document must explicitly declare which conventions it uses.

### Layered Semantics

Multiple conventions may apply to the same document.

Each convention defines interpretation rules for a specific domain.

### Processor Neutrality

AEON parsers are not required to understand conventions.

Conventions are interpreted by higher-level processors.

---

# Declaring Conventions

Conventions are declared in the document header metadata.

Example:

```aeon
aeon:header = {

  encoding = "utf-8"
  mode = "strict"
  conventions = [
    "aeon.gp.document.v1"
    "aeon.gp.context.v1"
    "aeon.gp.collection.v1"
    "aeon.gp.temporal.v1"
    "aeon.gp.measurement.v1"
    "aeon.gp.security.v1"
  ]

}
```

This declaration informs consumers which interpretation rules may apply.

## Single Convention

```aeon
aeon:header = {
  convention = "aeon.gp.document.v1"
}
```

## Multiple Conventions

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.document.v1"
    "aeon.gp.measurement.v1"
  ]
}
```

## Declaration Rule

`convention` and `conventions` are **mutually exclusive**.

A document **must not declare both**.

Implementations may internally normalize:

```aeon
convention = "x"
```

as:

```aeon
conventions = ["x"]
```

This normalization must not appear in serialized documents.

---

# Convention Naming

Conventions follow a structured naming scheme.

```text
<namespace>.<name>.v<version>
```

Examples:

```text
aeon.gp.document.v1
aeon.gp.context.v1
aeon.gp.collection.v1
aeon.gp.temporal.v1
aeon.gp.measurement.v1
aeon.gp.security.v1
aeon.gp.integrity.v1
aeon.gp.signature.v1
aeon.gp.encryption.v1
```

This format provides:

* clear ownership
* version stability
* predictable evolution

Third-party conventions may also exist:

```text
org.example.finance.v1
org.example.workflow.v1
```

---

# Convention Scope

A convention may define rules for any of the following areas:

### Metadata

Document-level metadata.

Example:

```text
aeon.gp.document.v1
```

### Context Annotations

Interpretation hints for data.

Example:

```text
aeon.gp.context.v1
```

### Data Interpretation

Standard representations such as measurement labels, collection semantics, or temporal semantics.

Example:

```text
aeon.gp.measurement.v1
aeon.gp.collection.v1
aeon.gp.temporal.v1
```

### Security

Integrity, signatures, encryption.

Example:

```text
aeon.gp.security.v1
aeon.gp.integrity.v1
aeon.gp.signature.v1
aeon.gp.encryption.v1
```

---

# Convention Interaction

Multiple conventions may appear in the same document.

Example:

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.document.v1"
    "aeon.gp.context.v1"
    "aeon.gp.measurement.v1"
    "aeon.gp.security.v1"
  ]
}
```

Each convention operates independently unless a specification explicitly defines dependencies.

Example dependency:

```text
aeon.gp.signature.v1
requires
aeon.gp.integrity.v1
```

---

# Convention Compliance

Consumers may apply convention declarations in different convention modes.

These modes describe how a processor handles declared conventions. They are distinct from AEON transport mode and from any strictness rules defined by the core syntax or value specifications.

### Strict Convention Mode

The processor must understand all declared conventions.

If a convention is unknown, processing fails.

### Permissive Convention Mode

Unknown conventions are ignored.

Only known conventions are applied.

This allows forward compatibility.

---

# Convention Versioning

Conventions are versioned.

Example:

```text
aeon.gp.document.v1
```

New versions should:

* preserve compatibility where possible
* introduce new features without breaking older processors

A new incompatible revision should increment the version number.

Example:

```text
aeon.document.v2
```

---

# Convention Documentation

Each convention specification should define:

1. purpose
2. scope
3. vocabulary
4. processing rules
5. interaction with other conventions
6. examples

This ensures interoperability across independent implementations.

The `aeon.gp.convention.v1` document provides a compact authoring template for new convention specifications.

---

# Convention Processing Model

The general AEON processing pipeline becomes:

```text
parse AEON document
        ↓
apply AEON core semantics
        ↓
identify declared conventions
        ↓
apply convention interpretation
        ↓
perform higher-level processing
```

This layered model ensures that AEON remains usable even when conventions are unknown.

---

# Convention Extensibility

The convention system allows communities to create domain-specific standards.

Examples:

```text
aeon.finance.v1
aeon.medical.v1
aeon.iot.v1
aeon.dataset.v1
```

These conventions can define domain rules while maintaining compatibility with AEON core.

---

# Relationship to Profiles

Profiles define **security or processing policies** for sets of conventions.

Example:

```text
aeon.secure-basic.v1
```

Profiles may restrict:

* allowed algorithms
* required conventions
* processing behavior

Profiles therefore operate above conventions.

---

# Summary

AEON conventions provide a flexible mechanism for extending the language ecosystem without expanding the core specification.

They enable interoperable interpretation layers for:

* document metadata
* contextual annotations
* data semantics
* security mechanisms
* domain-specific standards

while preserving AEON’s design goal of a minimal and stable core language.

---
Here’s a clean **AEON architecture stack** you could use in the spec.

---

# AEON Architecture Stack

## Overview

AEON is structured as a layered system.

Each layer has a distinct responsibility:

* **AEON Core** defines syntax and structural semantics.
* **Conventions** define interoperable interpretation rules.
* **Profiles** define policy bundles and constrained usage.
* **Processors** implement actual behavior.

This separation allows AEON to remain minimal while supporting rich ecosystems.

---

# Layer Diagram

```text
┌──────────────────────────────────────────────┐
│                  Processors                  │
│──────────────────────────────────────────────│
│ apps · validators · AI agents · runtimes ·   │
│ signers · verifiers · indexers · toolchains  │
└──────────────────────────────────────────────┘
                      ▲
                      │ uses
┌──────────────────────────────────────────────┐
│                   Profiles                   │
│──────────────────────────────────────────────│
│ policy bundles · required conventions ·      │
│ approved algorithms · processing modes       │
│                                              │
│ examples:                                    │
│ aeon.secure-basic.v1                         │
│ aeon.secure-standard.v1                      │
└──────────────────────────────────────────────┘
                      ▲
                      │ composes
┌──────────────────────────────────────────────┐
│                 Conventions                  │
│──────────────────────────────────────────────│
│ interpretation rules · vocabularies ·        │
│ document metadata · context · security       │
│                                              │
│ examples:                                    │
│ aeon.gp.document.v1                          │
│ aeon.gp.context.v1                           │
│ aeon.gp.collection.v1                        │
│ aeon.gp.measurement.v1                       │
│ aeon.gp.security.v1                          │
│ aeon.gp.integrity.v1                         │
│ aeon.gp.signature.v1                         │
│ aeon.gp.encryption.v1                        │
└──────────────────────────────────────────────┘
                      ▲
                      │ extends
┌──────────────────────────────────────────────┐
│                  AEON Core                   │
│──────────────────────────────────────────────│
│ syntax · parsing · canonicalization ·        │
│ assignment semantics · paths · header        │
└──────────────────────────────────────────────┘
```

---

# What each layer does

## 1. AEON Core

The core defines the language itself.

It is responsible for:

* syntax
* parsing
* canonical paths
* assignment semantics
* canonicalization
* `aeon:header`

It is **not** responsible for:

* document metadata meaning
* measurement semantics
* signatures
* encryption
* domain vocabularies

---

## 2. Conventions

Conventions define shared interpretation rules on top of core AEON.

They standardize things like:

* document metadata
* context labels
* collection semantics
* measurement labels
* security envelopes
* integrity hashing
* signatures
* encryption

Examples:

* `aeon.gp.document.v1`
* `aeon.gp.context.v1`
* `aeon.gp.collection.v1`
* `aeon.gp.measurement.v1`
* `aeon.gp.security.v1`
* `aeon.gp.integrity.v1`
* `aeon.gp.signature.v1`
* `aeon.gp.encryption.v1`

Conventions do **not** change AEON syntax.

---

## 3. Profiles

Profiles define **bundled policies** for conventions.

They specify:

* which conventions are required
* which algorithms are allowed
* which processing rules must be followed

Examples:

* `aeon.secure-basic.v1`
* `aeon.secure-standard.v1`

Profiles exist so independent implementations can interoperate safely.

---

## 4. Processors

Processors are the systems that actually use AEON documents.

Examples:

* validators
* schema engines
* AI systems
* renderers
* security verifiers
* application runtimes

Processors decide what to do with a document after AEON core parsing and convention/profile interpretation.

---

# Processing Flow

This is the typical flow:

```text
AEON source
   ↓
parse with AEON core
   ↓
resolve canonical structure
   ↓
read declared conventions
   ↓
apply convention meanings
   ↓
apply profile rules
   ↓
processor behavior
```

---

# Document-Level View

A secured, metadata-rich AEON document might look like this conceptually:

```text
aeon:header
  ├ core processing fields
  └ meta
      ├ declared conventions
      ├ document metadata
      └ other convention-scoped metadata

document body
  └ actual structured data

aeon:envelope
  ├ integrity
  ├ signatures
  └ encryption
```

---

# Why this matters

This layered architecture gives AEON four major strengths:

### 1. Stability

The core stays small and stable.

### 2. Extensibility

New conventions can be added without changing the language.

### 3. Interoperability

Profiles let different implementations agree on constrained behavior.

### 4. Trustability

Security conventions make verifiable structured data possible.

---

# One-line summary

> **AEON Core defines structure, conventions define meaning, profiles define policy, and processors define behavior.**

---

# Optional compact version for the spec

If you want a shorter version for an intro page:

```text
AEON Core → Conventions → Profiles → Processors
```

Where:

* **Core** = syntax and structural semantics
* **Conventions** = shared interpretation rules
* **Profiles** = policy bundles
* **Processors** = actual implementation behavior

---
