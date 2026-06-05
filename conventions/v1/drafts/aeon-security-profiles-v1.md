---
id: aeon-security-profiles-v1
title: AEON Security Profiles v1
description: Draft security profiles defining algorithm sets and usage policies for AEON security conventions.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-security-profiles-v1
license: CC0-1.0
links:
  - aeon-security-architecture
  - aeon-gp-security-envelope-v1
  - aeon-gp-integrity-v1
  - aeon-gp-signature-v1
  - aeon-gp-encryption-v1
---

# AEON Security Profiles v1

## Status

Draft profile guidance

---

# 1. Purpose

Security conventions define structure.

Security profiles define approved algorithm sets and usage rules for those conventions.

Profiles help independently built systems exchange secured AEON documents without each system choosing incompatible algorithms or policy assumptions.

---

# 2. Profile Layering

Profiles sit above the security conventions:

```text
AEON Core
   ↓
Security Conventions
   ↓
Security Profiles
   ↓
Applications / Protocols
```

Profiles act as policy declarations, not structural rules.

---

# 3. Profile Declaration

Profiles should be declared in the document metadata.

Single profile:

```aeon
aeon:header = {
  profile = "aeon.secure-standard.v1"
}
```

Multiple profiles:

```aeon
aeon:header = {
  profiles = [
    "aeon.secure-standard.v1"
  ]
}
```

---

# 4. `aeon.secure-basic.v1`

## Purpose

Provides a minimal, widely implementable security baseline.

Designed for:

* simple document signing
* lightweight interchange
* developer tooling
* configuration files
* small services

## Required conventions

```text
aeon.gp.security.v1
aeon.gp.integrity.v1
aeon.gp.signature.v1
```

## Allowed algorithms

Hash:

```text
sha256
```

Signature:

```text
ed25519
```

## Not included

* encryption
* timestamp authorities
* Merkle proofs
* audit logs

## Example

```aeon
aeon:header = {
  encoding = "utf-8"
  conventions = [
    "aeon.gp.security.v1"
    "aeon.gp.integrity.v1"
    "aeon.gp.signature.v1"
  ]
  profile = "aeon.secure-basic.v1"
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

# 5. `aeon.secure-standard.v1`

## Purpose

Provides a general-purpose secure document profile.

Designed for:

* enterprise document exchange
* APIs
* signed records
* authenticated messages

## Required conventions

```text
aeon.gp.security.v1
aeon.gp.integrity.v1
aeon.gp.signature.v1
aeon.gp.encryption.v1
```

## Allowed algorithms

Hash:

```text
sha256
sha512
```

Signature:

```text
ed25519
ecdsa-p256
```

Encryption:

```text
xchacha20-poly1305
aes-256-gcm
```

## Optional features

* multiple signatures
* encryption and signature combination
* signing metadata (`time`, `issuer`)

## Example

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

# 6. `aeon.secure-advanced.v1`

## Status

Reserved for later specification.

## Purpose

Represents a future high-assurance profile for large-scale verifiable systems.

Candidate use cases include:

* regulatory logs
* supply chain records
* AI traceability
* long-term archives
* distributed verification

Candidate features include:

* Merkle subtree verification
* cryptographically chained audit logs
* multiple signing authorities
* timestamp proofs
* partial document verification

---

# 7. Why Profiles Matter

Profiles provide:

## Interoperability

Systems can exchange AEON documents knowing which algorithms are expected.

## Security baseline

Profiles prevent weak or incompatible algorithms.

## Implementation simplicity

Developers can implement a profile rather than the entire security ecosystem.

---

# 8. Initial Profile Set

The initial AEON security profile set is:

```text
aeon.secure-basic.v1
aeon.secure-standard.v1
```

`aeon.secure-advanced.v1` is reserved for later specification.
