---
id: aeon-gp-encryption-v1
title: AEON GP Encryption v1
description: Draft encryption convention defining encrypted payload structures for AEON security envelopes.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-gp-encryption-v1
license: CC0-1.0
links:
  - aeon-gp-security-envelope-v1
  - aeon-gp-integrity-v1
  - aeon-gp-signature-v1
---

# AEON GP Encryption v1

Convention identifier: `aeon.gp.encryption.v1`

## Status

Draft interoperability convention

---

# 1. Purpose

`aeon.gp.encryption.v1` defines a minimal structure for representing encrypted AEON payloads inside `aeon:envelope`.

It allows AEON documents to carry confidential data while preserving the deterministic document model.

This convention is designed to work with:

* `aeon.gp.security.v1`
* `aeon.gp.integrity.v1`
* `aeon.gp.signature.v1`

---

# 2. Scope

`aeon.gp.encryption.v1` defines:

* where encrypted content lives
* how ciphertext is represented
* how recipient keys are identified
* minimal encryption metadata

It does **not** define:

* key exchange protocols
* trust models
* certificate infrastructure
* algorithm approval policies

---

# 3. Encryption Model

Encryption replaces the plaintext body with ciphertext while preserving the AEON document structure.

The envelope carries:

* encryption algorithm
* recipient key identifier
* encrypted payload bytes

The decrypted payload must resolve to a valid AEON document body.

---

# 4. Envelope Placement

Encryption is declared inside the envelope:

```aeon
aeon:envelope:securityEnvelope = {
  encryption:encryptionBlock = { ... }
}
```

Only one encryption section is allowed per envelope unless another convention explicitly defines multiple encryption layers.

---

# 5. Encryption Entry Structure

## Required fields

| field        | meaning                  |
| ------------ | ------------------------ |
| `alg`        | encryption algorithm     |
| `kid`        | recipient key identifier |
| `ciphertext` | encrypted payload        |

Minimal form:

```aeon
encryption:encryptionBlock = {
  alg:string = "xchacha20-poly1305"
  kid:string = "bob"
  ciphertext:bytes = #...
}
```

---

# 6. Field Definitions

## 6.1 `alg`

Encryption algorithm identifier.

Example:

```aeon
alg = "xchacha20-poly1305"
```

Other possible values:

* `aes-256-gcm`
* `chacha20-poly1305`

The convention does not restrict allowed algorithms.

Profiles may.

---

## 6.2 `kid`

Recipient key identifier.

Example:

```aeon
kid = "bob"
```

This identifies the key used to decrypt the ciphertext.

The identifier format is intentionally flexible.

Possible examples:

```aeon
kid = "bob"
kid = "org.example.recipient.1"
kid = "did:example:bob#key1"
```

---

## 6.3 `ciphertext`

Encrypted payload.

Example:

```aeon
ciphertext = #AABBCC...
```

This field contains the encrypted AEON payload bytes.

The exact encoding is determined by AEON binary literal rules.

---

# 7. Optional Fields

Optional metadata may appear if required by the encryption algorithm.

| field   | meaning                       |
| ------- | ----------------------------- |
| `nonce` | encryption nonce              |
| `aad`   | additional authenticated data |
| `tag`   | authentication tag            |
| `epk`   | ephemeral public key          |

Example:

```aeon
encryption:encryptionBlock = {
  alg:string = "xchacha20-poly1305"
  kid:string = "bob"
  nonce:bytes = #112233...
  ciphertext:bytes = #AABBCC...
  tag:bytes = #998877...
}
```

These fields are algorithm dependent.

---

# 8. Encryption Scope

Encryption covers the **document body**.

The envelope itself remains visible so processors know how to decrypt the document.

Conceptually:

```text
aeon:header
ciphertext(body)
aeon:envelope
```

---

# 9. Combined Signing and Encryption

Documents may combine encryption with signatures.

Example workflow:

1. encrypt payload
2. compute integrity hash
3. sign hash

Example:

```aeon
aeon:envelope:securityEnvelope = {
  encryption:encryptionBlock = {
    alg:string = "xchacha20-poly1305"
    kid:string = "bob"
    ciphertext:bytes = #...
  }

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

This allows recipients to verify authenticity after decryption.

---

# 10. Verification / Decryption Flow

A processor decrypting a document should:

1. parse AEON document
2. locate `aeon:envelope.encryption`
3. resolve recipient key using `kid`
4. decrypt `ciphertext`
5. reconstruct the AEON body
6. optionally verify integrity and signatures

---

# 11. Failure Conditions

Decryption must fail if:

* `alg` is missing
* `kid` cannot be resolved
* ciphertext cannot be decrypted
* authentication tag fails
* payload cannot be parsed as AEON

Decryption failure is not a syntax error; it is a processor-level security failure.

---

# 12. Example Encrypted Document

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"
}

aeon:envelope:securityEnvelope = {
  encryption:encryptionBlock = {
    alg:string = "xchacha20-poly1305"
    kid:string = "bob"
    nonce:bytes = #AA11...
    ciphertext:bytes = #BB22...
    tag:bytes = #CC33...
  }

}
```

In this case the body is encrypted and only recoverable after decryption.

---

# 13. Relationship to Other Conventions

`aeon.gp.encryption.v1` works with:

* `aeon.gp.security.v1`
* `aeon.gp.integrity.v1`
* `aeon.gp.signature.v1`

Encryption may appear alongside integrity and signatures.

---

# 14. One-Line Definition

`aeon.gp.encryption.v1` defines a minimal encryption envelope for AEON documents in which the document body is represented as ciphertext inside `aeon:envelope.encryption`.

---

# 15. Minimal Encryption Envelope

```aeon
aeon:envelope:securityEnvelope = {
  encryption:encryptionBlock = {
    alg:string = "xchacha20-poly1305"
    kid:string = "bob"
    ciphertext:bytes = #...
  }
}
```

---
