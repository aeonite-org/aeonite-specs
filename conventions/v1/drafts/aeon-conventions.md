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

> **AEON Core defines structure, conventions define meaning, profiles define policy, and processors define behavior.**
