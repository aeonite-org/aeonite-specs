---
id: aeon-quick-mental-model
title: AEON Quick Mental Model
description: High-level mental model of the AEON stack across structure, meaning, policy, and processing behavior.
family: conventions
group: Convention Overview
status: Draft
path: specification/conventions/quick-mental-model
license: CC-BY-4.0
---

# AEON Quick Mental Model

AEON is a structured data format designed for **deterministic meaning, extensibility, and verifiable documents**.

It separates four concerns:

```text
Structure → Meaning → Policy → Behavior
```

| Layer       | Responsibility    |
| ----------- | ----------------- |
| AEON Core   | defines structure |
| Conventions | define meaning    |
| Profiles    | define policy     |
| Processors  | define behavior   |

---

# 1. What AEON Actually Is

At its core, AEON is a system of **deterministic assignments**.

Example:

```aeon
user = {
  name = "Alice"
  role = "admin"
}
```

This produces a canonical structural state.

AEON focuses on **how data is structured**, not what the data means.

Meaning is added by conventions.

---

# 2. The Three Parts of an AEON Document

Most AEON documents follow this conceptual layout:

```text
aeon:header
document body
aeon:envelope
```

Example:

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"
}

data = {
  message = "Hello world"
}

aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = { ... }
}
```

### Header

Processing metadata.

### Body

The actual structured data.

### Envelope

Security closure (optional).

---

# 3. AEON Is Not Just a Data Format

Most formats stop here:

```text
syntax → data
```

AEON goes further:

```text
syntax
  ↓
canonical structure
  ↓
conventions
  ↓
profiles
  ↓
processors
```

This allows AEON to support things like:

* signed documents
* structured metadata
* contextual interpretation
* verifiable datasets

without making the core language complex.

---

# 4. Conventions Add Meaning

AEON core does not interpret fields.

Instead, documents declare conventions.

Example:

```aeon
aeon:header = {

  encoding = "utf-8"
  mode = "strict"
  conventions = [
    "aeon.gp.convention.v1"
  ]

}
```

The convention tells consumers how to interpret certain fields.

Example:

```aeon
distance@{unit="meters"} = 3
```

The **unit meaning** is defined by a convention, not the language.

---

# 5. Profiles Add Policy

Profiles define **safe usage bundles**.

Example:

```text
aeon.secure-basic.v1
```

Profiles may define:

* required conventions
* allowed algorithms
* processing constraints

Profiles exist so independent implementations can interoperate safely.

---

# 6. Canonicalization Matters

AEON guarantees that documents have a **deterministic canonical structure**.

Example:

```aeon
b = 2
a = 1
```

Canonical ordering becomes:

```aeon
a = 1
b = 2
```

This property enables:

* reproducible hashing
* cryptographic signatures
* deterministic processing

---

# 7. Security Is Layered

Security is not built into the syntax.

Instead AEON defines conventions:

| Convention           | Purpose            |
| -------------------- | ------------------ |
| `aeon.gp.security.v1`   | envelope structure |
| `aeon.gp.integrity.v1`  | canonical hashing  |
| `aeon.gp.signature.v1`  | signatures         |
| `aeon.gp.encryption.v1` | encryption         |

Example envelope:

```aeon
aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha256"
    hash:bytes = #...
  }

  signatures:signatureSet = [
    { alg:string = "ed25519" kid:string = "alice" sig:bytes = #... }
  ]
}
```

This makes AEON documents **self-verifying**.

---

# 8. AEON Supports Advanced Integrity

Because of canonical paths and deterministic structure, AEON naturally supports:

* Merkle subtree verification
* tamper-evident event logs
* verifiable datasets

These patterns can be built without modifying the core language.

---

# 9. What AEON Is Not

AEON deliberately avoids becoming:

* a programming language
* a computation system
* a schema engine
* a policy engine

Instead AEON focuses on **deterministic structured representation**.

Other systems can build on top of it.

---

# 10. Simple Mental Model

If you remember only one thing:

```text
AEON core defines structure.
Conventions define meaning.
Profiles define policy.
Processors define behavior.
```

---

# 11. Typical Processing Pipeline

```text
AEON source
   ↓
parse syntax
   ↓
build canonical structure
   ↓
apply conventions
   ↓
apply profile rules
   ↓
processor behavior
```

---

# 12. A Small Example

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"
  conventions = [
    "aeon.gp.convention.v1"
    "aeon.gp.security.v1"
  ]
}

temperature@{unit="celsius"} = 23

aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha256"
    hash:bytes = #1234...
  }
}
```

This document:

* contains structured data
* declares interpretation conventions
* includes integrity protection

All without expanding the core language.

---

# Final Summary

AEON is designed to provide:

* deterministic structured data
* extensible interpretation layers
* secure and verifiable documents
* long-term ecosystem growth

while keeping the **core language minimal and stable**.
