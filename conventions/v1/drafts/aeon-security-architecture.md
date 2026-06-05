---
id: aeon-security-architecture
title: AEON Security Architecture
description: Architecture-level explanation of integrity, signatures, encryption, and the role of conventions in secure AEON documents.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-security-architecture
license: CC0-1.0
links:
  - aeon-gp-security-envelope-v1
  - aeon-gp-integrity-v1
  - aeon-gp-signature-v1
  - aeon-gp-encryption-v1
  - aeon-security-profiles-v1
  - aeon-security-best-practices
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

# Related Security Documents

Detailed security conventions and profiles are defined separately:

| document | purpose |
| -------- | ------- |
| `aeon.gp.security.v1` | security envelope structure |
| `aeon.gp.integrity.v1` | canonical document hashing |
| `aeon.gp.signature.v1` | signature vocabulary |
| `aeon.gp.encryption.v1` | encrypted payload representation |
| `aeon-security-profiles-v1` | approved algorithm sets and usage profiles |
| `aeon-security-best-practices` | informative advanced integrity patterns |
