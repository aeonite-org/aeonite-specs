---
id: aeon-secure-document-lifecycle
title: AEON Secure Document Lifecycle
description: Walkthrough of authoring, hashing, signing, encryption, transport, verification, and decryption for secured AEON documents.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-secure-document-lifecycle
license: CC0-1.0
---

# AEON Secure Document Lifecycle

This section describes the typical lifecycle of a secured AEON document using the security conventions.

The lifecycle includes:

1. Authoring
2. Canonical hashing
3. Signing
4. Optional encryption
5. Transmission
6. Verification
7. Optional decryption

---

# 1. Document Authoring

An AEON document is first created without the envelope.

Example:

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
```

At this stage:

* the document contains only semantic content
* no integrity metadata exists

---

# 2. Canonical Hashing

The document is processed using `aeon.gp.integrity.v1`.

Steps:

1. parse the document
2. compute the canonical assignment state
3. serialize canonical state lines
4. hash the resulting UTF-8 byte stream

Example result:

```
sha256 → #7A91E4C8...
```

This becomes the **document integrity hash**.

---

# 3. Signature Creation

The signer creates a signature over the integrity hash.

Example:

```
sig = Sign(hash, privateKey)
```

Then the envelope is constructed.

Example:

```aeon
"aeon:envelope":securityEnvelope = {

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

The envelope is appended as the **final binding** in the document.

---

# 4. Optional Encryption

If confidentiality is required, the document body may be encrypted.

Typical workflow:

1. encrypt document body
2. produce ciphertext
3. place encryption metadata in the envelope

Example:

```aeon
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

This allows recipients to:

* decrypt the body
* verify integrity
* verify signatures

---

# 5. Transmission / Storage

The completed AEON document can now be:

* transmitted
* stored
* archived
* logged
* distributed

Because the document carries its own envelope, it becomes **self-verifying**.

No external signature file is required.

---

# 6. Document Verification

A receiver verifying the document should perform the following steps.

### Step 1 — Parse document

The AEON document is parsed normally.

### Step 2 — Locate envelope

The processor locates:

```
aeon:envelope
```

### Step 3 — Compute canonical integrity hash

The processor recomputes the hash using `aeon.gp.integrity.v1`.

### Step 4 — Compare hashes

The computed hash must match:

```
aeon:envelope.integrity.hash
```

If the hash differs, the document is considered **tampered**.

### Step 5 — Verify signatures

Each signature entry is verified using:

* the declared algorithm
* the key referenced by `kid`

If verification fails, the signature is invalid.

---

# 7. Optional Decryption

If the document is encrypted:

1. locate `aeon:envelope.encryption`
2. resolve recipient key
3. decrypt ciphertext
4. reconstruct the AEON body
5. verify integrity and signatures

Decryption failure indicates either:

* incorrect key
* corrupted ciphertext
* tampering

---

# 8. Lifecycle Summary

The secure lifecycle can be summarized as:

```
author document
        ↓
canonical hash
        ↓
sign hash
        ↓
(optional) encrypt payload
        ↓
attach envelope
        ↓
transmit / store
        ↓
verify hash
        ↓
verify signatures
        ↓
(optional) decrypt
```

---

# 9. Security Properties

This lifecycle provides:

### Integrity

Document tampering is detectable.

### Authenticity

Signatures prove authorship.

### Confidentiality

Encryption protects document content.

### Self-verification

The document carries its own verification data.

---

# 10. Design Advantages

This model provides several advantages:

* deterministic hashing
* multi-signature support
* independent algorithm evolution
* envelope-based closure
* compatibility with streaming verification

Because AEON separates structure from security mechanisms, cryptographic algorithms can evolve without modifying the core language.

---

# Result

The AEON security model enables **verifiable structured documents** while preserving the minimal design philosophy of AEON core.

---

If you want, the next thing worth doing is something surprisingly important:
designing the **canonical test vectors for the integrity algorithm**. That’s what ensures two independent implementations always produce the same hash.
