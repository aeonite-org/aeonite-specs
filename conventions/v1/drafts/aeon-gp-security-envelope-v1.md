---
id: aeon-gp-security-envelope-v1
title: AEON GP Security Envelope v1
description: Draft security-envelope convention defining placement, sections, and field structure for secure AEON documents.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-gp-security-envelope-v1
license: CC0-1.0
links:
  - aeon-gp-integrity-v1
  - aeon-gp-signature-v1
  - aeon-gp-encryption-v1
---

# AEON GP Security Envelope v1

Convention identifier: `aeon.gp.security.v1`

## Status

Draft interoperability convention

## Purpose

Defines the **standard AEON security envelope** used for:

* document integrity
* signatures
* encryption
* additional security extensions

The envelope is the **document closure**.

---

# 1. Envelope Placement

The envelope **must be the final binding in the document**.

```text
aeon:header
document body
aeon:envelope
```

Rules:

* no bindings may follow `aeon:envelope`
* only whitespace/comments may appear after it
* envelope is excluded from integrity hashing

---

# 2. Envelope Binding

The envelope is always:

```aeon
"aeon:envelope":securityEnvelope = { ... }
```

The envelope object may contain the following sections.

---

# 3. Envelope Sections

## 3.1 `integrity`

Defines canonical document hashing.

Provided by `aeon.gp.integrity.v1`.

Example:

```aeon
integrity:integrityBlock = {
  alg:string = "sha-256"
  hash:bytes = #7A91E4C8...
}
```

Fields:

| field  | meaning                 |
| ------ | ----------------------- |
| `alg`  | hashing algorithm       |
| `hash` | canonical document hash |

---

## 3.2 `signatures`

Defines one or more signatures over the integrity hash.

Provided by `aeon.gp.signature.v1`.

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

Fields:

| field | meaning             |
| ----- | ------------------- |
| `alg` | signature algorithm |
| `kid` | key identifier      |
| `sig` | signature bytes     |

Multiple signatures are allowed.

---

## 3.3 `encryption`

Defines encrypted payloads.

Provided by `aeon.gp.encryption.v1`.

Example:

```aeon
encryption:encryptionBlock = {
  alg:string = "xchacha20-poly1305"
  kid:string = "bob"
  ciphertext:string = "ENCRYPTED_PAYLOAD"
}
```

Fields:

| field        | meaning                  |
| ------------ | ------------------------ |
| `alg`        | encryption algorithm     |
| `kid`        | recipient key identifier |
| `ciphertext` | encrypted payload        |

---

## 3.4 Optional extensions

Additional sections may appear if declared by conventions.

Examples:

```aeon
timestamp = { ... }
merkle = { ... }
proof = { ... }
```

These must be defined by their respective conventions.

---

# 4. Full Example

```aeon
aeon:header = {
  encoding:string = "utf-8"
  mode:string = "strict"
  conventions:conventionSet = [
    "aeon.gp.security.v1"
    "aeon.gp.integrity.v1"
    "aeon.gp.signature.v1"
  ]
}

message:object = {
  from:string = "Alice"
  to:string = "Bob"
  text:string = "Meet at the lighthouse"
}

"aeon:envelope":securityEnvelope = {

  integrity:integrityBlock = {
    alg:string = "sha-256"
    hash:bytes = #7A91E4C8...
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

# 5. Verification Flow

A processor verifying integrity should:

1. Parse AEON document
2. Locate `aeon:envelope`
3. Remove envelope from hash coverage
4. Compute canonical hash
5. Compare with `integrity.hash`
6. Verify signatures

---

# 6. Design Goals

The envelope model is designed to be:

* deterministic
* streamable
* cryptographically neutral
* convention-driven
* easy to implement

AEON core remains independent of cryptographic algorithms.

---

# 7. Non-goals

The envelope does **not define**:

* trust models
* key distribution
* certificate authorities
* algorithm requirements

These are left to conventions or processors.

---

# 8. Architectural Summary

The AEON security architecture becomes:

```text
AEON Core
   ↓
aeon.gp.security.v1
   ↓
aeon.gp.integrity.v1
aeon.gp.signature.v1
aeon.gp.encryption.v1
```

Core stays minimal while the ecosystem provides security capabilities.

---

# 9. Related Security Conventions

Detailed rules for envelope sections are defined by separate conventions:

| convention | purpose |
| ---------- | ------- |
| `aeon.gp.integrity.v1` | canonical document hashing |
| `aeon.gp.signature.v1` | signatures over integrity hashes |
| `aeon.gp.encryption.v1` | encrypted payload representation |

The envelope convention defines placement and section structure. The child conventions define the contents and processing rules for each section.
