---
id: aeon-security-architecture
title: AEON Security Architecture
description: Architecture-level explanation of integrity, signatures, encryption, and the role of conventions in secure AEON documents.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-security-architecture
license: CC0-1.0
---

# AEON Security Architecture

## Overview

AEON provides a deterministic structural model that enables reliable document integrity, authentication, and encryption without embedding cryptographic mechanisms directly into the language.

Security features in AEON are implemented through **conventions layered on top of AEON core**, allowing the language itself to remain minimal while enabling interoperable secure data exchange.

The AEON security model is based on four conventions:

* `aeon.gp.security.v1`
* `aeon.gp.integrity.v1`
* `aeon.gp.signature.v1`
* `aeon.gp.encryption.v1`

These conventions together define how AEON documents may be sealed, signed, and encrypted.

---

# Core Principles

The AEON security architecture follows several key principles.

### Deterministic Structure

AEON documents have deterministic structural semantics.
Canonical document state can therefore be hashed reliably across independent implementations.

### Envelope Closure

Security metadata is placed in a **document closure structure** called the envelope.

This keeps cryptographic metadata separate from document content while ensuring the envelope can seal the document.

### Convention Layering

Cryptographic mechanisms are defined by conventions rather than AEON core.

This allows algorithms and security models to evolve independently of the language.

### Processor Neutrality

AEON does not mandate specific algorithms, trust models, or key infrastructure.
Processors and profiles may apply their own security policies.

---

# Document Structure

An AEON document participating in the security conventions conceptually contains three parts:

```text
aeon:header
document body
aeon:envelope
```

### `aeon:header`

The header declares core processing metadata such as encoding and mode.

### Document Body

The body contains the semantic content of the document.

### `aeon:envelope`

The envelope contains integrity, signature, and encryption metadata.

The envelope must be the **final binding in the document**.

No additional bindings may appear after it.

---

# The Security Envelope

The envelope is defined by `aeon.gp.security.v1`.

Example:

```aeon
"aeon:envelope":securityEnvelope = {
  integrity:integrityBlock = { ... }
  signatures:signatureSet = [ ... ]
  encryption:encryptionBlock = { ... }
}
```

Each section may be present depending on the conventions used.

---

# Integrity Layer

`aeon.gp.integrity.v1` defines how a deterministic hash of the document is computed.

The hash covers the **final canonical document state** excluding the envelope.

Example:

```aeon
integrity:integrityBlock = {
  alg:string = "sha-256"
  hash:string = "7a91e4c8..."
}
```

This provides tamper detection and forms the foundation for signatures.

---

# Signature Layer

`aeon.gp.signature.v1` defines how cryptographic signatures are represented.

Each signature verifies the integrity hash declared in the envelope.

Example:

```aeon
signatures:signatureSet = [
  {
    alg:string = "ed25519"
    kid:string = "alice"
    sig:string = "BASE64_SIGNATURE"
  }
]
```

Multiple signatures may appear, allowing co-signing and approval workflows.

---

# Encryption Layer

`aeon.gp.encryption.v1` defines how encrypted payloads are represented.

Example:

```aeon
encryption:encryptionBlock = {
  alg:string = "xchacha20-poly1305"
  kid:string = "bob"
  ciphertext:string = "ENCRYPTED_PAYLOAD"
}
```

Encryption protects the document body while leaving the envelope visible so processors know how to decrypt the document.

---

# Verification Workflow

A processor verifying a secured AEON document typically performs the following steps:

1. Parse the AEON document.
2. Locate `aeon:envelope`.
3. Compute the canonical integrity hash.
4. Compare with `integrity.hash`.
5. Verify each signature using the declared algorithm and key.
6. If encrypted, decrypt the payload using the declared key.

The exact security policy applied is determined by the processor or profile.

---

# Security Convention Stack

The conventions form a layered model:

```text
AEON Core
   ↓
aeon.gp.security.v1   (envelope structure)
   ↓
aeon.gp.integrity.v1  (canonical hashing)
aeon.gp.signature.v1  (authentication)
aeon.gp.encryption.v1 (confidentiality)
```

This architecture allows AEON to support secure documents while keeping the core language independent of cryptographic mechanisms.

---

# Design Outcome

The AEON security model enables:

* deterministic document integrity
* self-verifying documents
* multiple independent signatures
* encrypted payloads
* extensible security conventions

All without introducing cryptographic complexity into the core language.

---

Good idea. Conventions define **structure**, but **profiles define safe usage**.
Without profiles, every system could choose different algorithms and you lose interoperability.

Below is a **simple three-profile model** that keeps things manageable while allowing growth.

---

# AEON Security Profiles

Profiles define **approved algorithm sets and usage rules** for the AEON security conventions.

They sit above the conventions:

```
AEON Core
   ↓
Security Conventions
   ↓
Security Profiles
   ↓
Applications / Protocols
```

Profiles ensure that independently built systems can securely exchange AEON documents.

---

# 1. `aeon.secure-basic.v1`

### Purpose

Provide a **minimal, widely implementable security baseline**.

Designed for:

* simple document signing
* lightweight interchange
* developer tooling
* configuration files
* small services

### Required conventions

```
aeon.gp.security.v1
aeon.gp.integrity.v1
aeon.gp.signature.v1
```

### Allowed algorithms

Hash:

```
sha256
```

Signature:

```
ed25519
```

### Not included

* encryption
* timestamp authorities
* Merkle proofs
* audit logs

### Example

```aeon
aeon:header = {
  encoding = "utf-8"
  conventions = [
    "aeon.gp.security.v1"
    "aeon.gp.integrity.v1"
    "aeon.gp.signature.v1"
  ]
  mode = "strict"
}

data = {
  value = 42
}

aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha256"
    hash:bytes = #...
  }

  signatures:signatureSet = [
    {
      alg:string = "ed25519"
      kid:string = "alice"
      sig:bytes = #...
    }
  ]
}
```

---

# 2. `aeon.secure-standard.v1`

### Purpose

Provide a **general-purpose secure document profile**.

Designed for:

* enterprise document exchange
* APIs
* signed records
* authenticated messages

### Required conventions

```
aeon.gp.security.v1
aeon.gp.integrity.v1
aeon.gp.signature.v1
aeon.gp.encryption.v1
```

### Allowed algorithms

Hash:

```
sha256
sha512
```

Signature:

```
ed25519
ecdsa-p256
```

Encryption:

```
xchacha20-poly1305
aes-256-gcm
```

### Optional features

* multiple signatures
* encryption + signature combination
* signing metadata (`time`, `issuer`)

### Example

```aeon
aeon:header = {
  profile = "aeon.secure-standard.v1"
}

"aeon:envelope":securityEnvelope = {

  encryption:encryptionBlock = {
    alg:string = "xchacha20-poly1305"
    kid:string = "bob"
    ciphertext:string = "ENCRYPTED_PAYLOAD"
  }

  integrity:integrityBlock = {
    alg:string = "sha-256"
    hash:string = "7a91e4c8..."
  }

  signatures:signatureSet = [
    {
      alg:string = "ed25519"
      kid:string = "alice"
      sig:string = "BASE64_SIGNATURE"
    }
  ]
}
```

---

# 3. `aeon.secure-advanced.v1`

### Purpose

Enable **high-assurance and large-scale verifiable systems**.

Designed for:

* regulatory logs
* supply chain records
* AI traceability
* long-term archives
* distributed verification

### Required conventions

```
aeon.gp.security.v1
aeon.gp.integrity.v1
aeon.gp.signature.v1
aeon.gp.encryption.v1
aeon.audit.v1
aeon.merkle.v1
```

### Features

* Merkle subtree verification
* cryptographically chained audit logs
* multiple signing authorities
* timestamp proofs
* partial document verification

### Example envelope

```aeon
aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha512"
    hash:bytes = #...
  }

  merkle = {
    "~.data.section1" = #...
    "~.data.section2" = #...
  }

  signatures:signatureSet = [
    {
      alg:string = "ed25519"
      kid:string = "authority-1"
      sig:bytes = #...
    }
  ]

  timestamp = {
    authority:string = "time.example"
    value:datetime = "2026-03-08T20:00:00Z"
    sig:bytes = #...
  }
}
```

---

# Profile Declaration

Profiles should be declared in the document metadata.

Example:

```aeon
aeon:header = {
  profile = "aeon.secure-standard.v1"
}
```

or

```aeon
aeon:header = {
  profiles = [
    "aeon.secure-standard.v1"
  ]
}
```

Profiles act as **policy declarations**, not structural rules.

---

# Why Profiles Matter

Profiles provide:

### Interoperability

Systems can safely exchange AEON documents knowing which algorithms are expected.

### Security baseline

Profiles prevent weak or incompatible algorithms.

### Implementation simplicity

Developers can implement a profile rather than the entire security ecosystem.

---

# Recommended Launch Set

For the first release of AEON security, I would ship only two profiles:

```
aeon.secure-basic.v1
aeon.secure-standard.v1
```

Leave `advanced` for later.

This keeps the ecosystem manageable.

---

# Strategic Outcome

With:

* security conventions
* integrity hashing
* signature vocabulary
* encryption envelope
* security profiles

AEON becomes a format for:

**verifiable structured data**

which is a very strong differentiator compared to:

* JSON
* YAML
* TOML
* XML

---
