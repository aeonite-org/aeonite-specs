---
id: aeon-gp-security-envelope-v1
title: AEON GP Security Envelope v1
description: Draft security-envelope convention defining placement, sections, and field structure for secure AEON documents.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-gp-security-envelope-v1
license: CC0-1.0
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
* future security extensions

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
  hash:string = "7a91e4c8..."
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
aeon.audit.v1
aeon.merkle.v1
```

Core stays minimal while the ecosystem provides security capabilities.

---

# My final recommendation

Keep the envelope **very small and predictable**:

```
aeon:envelope
 ├ integrity
 ├ signatures
 └ encryption
```

Everything else should extend from there.

This keeps the format elegant and avoids the kind of complexity that made XML security hard to implement correctly.

---

## `aeon.gp.integrity.v1` — Minimal Canonical Hashing Spec

### Status

Proposed interoperability convention

---

# 1. Purpose

`aeon.gp.integrity.v1` defines a deterministic hashing model for AEON documents.

It exists to ensure that independent implementations produce the **same hash** for the **same AEON document meaning**.

This convention is intended as the foundation for:

* `aeon.gp.signature.v1`
* self-verifying documents
* tamper detection
* security envelopes

---

# 2. Scope

`aeon.gp.integrity.v1` defines:

* what content is covered by the hash
* what content is excluded
* how canonical hash input is constructed
* how the final hash is produced

It does **not** define:

* signature algorithms
* trust models
* key handling
* encryption
* audit/event-stream hashing

---

# 3. Integrity Model

`aeon.gp.integrity.v1` hashes the document’s **final canonical state**, not the original source text and not the original write order.

This means two source documents that are semantically equivalent under AEON core must produce the same integrity hash.

Example:

```aeon
b = 2
a = 1
```

and

```aeon
a = 1
b = 2
```

must produce the same canonical hash if AEON core considers them equivalent.

---

# 4. Coverage

The integrity hash covers:

* `aeon:header`
* all document body content
* all final effective bindings in the document state

The integrity hash excludes:

* `aeon:envelope`
* comments
* annotations
* source whitespace
* transport-level formatting artifacts
* datatype hints, if excluded by AEON canonicalization rules

---

# 5. Envelope Exclusion Rule

If present, `aeon:envelope` is excluded from hash coverage.

`aeon:envelope` must be the final binding in the document.

No bindings may follow it.

Only trailing whitespace or comments may appear after it.

---

# 6. Canonical Hashing Input

The input to hashing is the UTF-8 serialization of the document’s **final canonical assignment state**.

This state is produced after AEON core parsing and canonicalization rules have been applied.

The canonical hash input consists of one line per final canonical path.

Each line must be serialized as:

```text
<canonical_path>\t<canonical_value>\n
```

Where:

* `<canonical_path>` is the final canonical AEON path
* `<canonical_value>` is the canonical AEON value serialization
* `\t` is a single U+0009 tab character
* `\n` is a single U+000A line feed character

---

# 7. Canonical Path Ordering

All emitted lines must be ordered lexicographically by `<canonical_path>`.

This ordering is applied **after** final document state resolution.

This means integrity hashing is state-based, not chronology-based.

---

# 8. Canonical Value Serialization

Canonical value serialization must follow AEON core canonicalization rules.

At minimum, the following normalizations apply.

## 8.1 Null

```text
null
```

## 8.2 Boolean

```text
true
false
```

## 8.3 Numbers

Numbers must be serialized in canonical decimal form:

* no exponent notation
* no superfluous leading `+`
* no unnecessary trailing zeros
* `-0` must serialize as `0`

Examples:

```text
1
3.14
0
-12.5
```

## 8.4 Strings

Strings must be serialized in canonical quoted form with required escaping.

Example:

```text
"hello"
"line\nbreak"
```

## 8.5 Arrays

Arrays must be serialized in canonical compact form using AEON core rules.

Example:

```text
[1,2,"x"]
```

## 8.6 Objects

Objects must be serialized in canonical compact form using AEON core rules, including canonical key ordering where applicable.

Example:

```text
{"a":1,"b":2}
```

---

# 9. Hash Algorithm Declaration

The hash algorithm must be declared in the envelope.

Example:

```aeon
aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha256"
    hash:bytes = #7A91E4C8...
  }
}
```

Initial recommended algorithm:

```text
sha256
```

Other algorithms may be allowed by profile or convention.

---

# 10. Hash Output

The hash value is the digest of the canonical hash input byte stream encoded as UTF-8.

The resulting digest must be represented using the agreed envelope encoding.

Example:

```aeon
hash = #7A91E4C8...
```

The exact binary/text encoding of hash values should be defined consistently across the security conventions.

---

# 11. Verification Procedure

To verify an integrity hash, a processor must:

1. Parse the AEON document using AEON core rules
2. Confirm that `aeon:envelope`, if present, is final
3. Exclude `aeon:envelope` from coverage
4. Resolve the document to its final canonical state
5. Serialize one line per final canonical path using:
   `<canonical_path>\t<canonical_value>\n`
6. Sort lines lexicographically by canonical path
7. Encode the full stream as UTF-8
8. Compute the declared hash
9. Compare with `aeon:envelope.integrity.hash`

---

# 12. Example

## Source document

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"
}

b = 2
a = 1

aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha256"
    hash:bytes = #...
  }
}
```

## Final canonical state

Conceptually:

```text
~.a\t1\n
~.aeon:header\t{"encoding":"utf-8","mode":"strict"}\n
~.b\t2\n
```

These UTF-8 bytes are hashed.

---

# 13. Non-Goals

`aeon.gp.integrity.v1` does not preserve:

* source ordering
* write chronology
* event timing
* append history

Those belong to an event-log convention such as `aeon.audit.v1`.

---

# 14. Relationship to Other Security Conventions

`aeon.gp.integrity.v1` is the foundation for:

* `aeon.gp.security.v1` — envelope structure
* `aeon.gp.signature.v1` — signatures over the integrity hash
* `aeon.gp.encryption.v1` — optional encrypted payload structures

It is distinct from:

* `aeon.audit.v1` — ordered event-sequence integrity
* `aeon.merkle.v1` — subtree hashing and proof structures

---

# 15. One-Line Definition

`aeon.gp.integrity.v1` defines deterministic state-based hashing of AEON documents by hashing the UTF-8 serialization of the final canonical assignment state, excluding `aeon:envelope`.

---

## `aeon.gp.signature.v1` — Minimal Signature Vocabulary

### Status

Proposed interoperability convention

---

# 1. Purpose

`aeon.gp.signature.v1` defines a minimal, deterministic signature vocabulary for AEON documents.

It standardizes how one or more signatures are represented inside `aeon:envelope`.

It is intended to work with:

* `aeon.gp.security.v1`
* `aeon.gp.integrity.v1`

This convention defines **signature metadata and structure**, not cryptographic trust policy.

---

# 2. Scope

`aeon.gp.signature.v1` defines:

* where signatures live
* how signature entries are structured
* what each field means
* what a signature covers

It does **not** define:

* trust models
* certificate formats
* key discovery
* algorithm approval policy
* timestamp authority behavior

---

# 3. Dependency

`aeon.gp.signature.v1` depends on `aeon.gp.integrity.v1`.

A signature under this convention signs the declared integrity hash, not raw source text.

---

# 4. Envelope Placement

Signatures live inside:

```aeon
aeon:envelope:securityEnvelope = {
  signatures:signatureSet = [ ... ]
}
```

The `signatures` field must be an array.

This allows:

* single signatures
* multiple signatures
* countersigning patterns later
* stable extension without changing shape

---

# 5. Signature Coverage

Each signature covers the document integrity hash declared in:

```aeon
aeon:envelope.integrity
```

This means:

* compute canonical document hash using `aeon.gp.integrity.v1`
* sign that hash
* store the signature entry in `aeon:envelope.signatures`

A signature does not directly sign:

* comments
* whitespace
* envelope contents
* source formatting

---

# 6. Signature Entry Structure

Each signature entry is an object.

## Required fields

| field | meaning                        |
| ----- | ------------------------------ |
| `alg` | signature algorithm identifier |
| `kid` | signer key identifier          |
| `sig` | signature value                |

## Minimal form

```aeon
{
  alg = "ed25519"
  kid = "alice"
  sig = #...
}
```

---

# 7. Field Definitions

## 7.1 `alg`

Declares the signature algorithm.

Example:

```aeon
alg = "ed25519"
```

This field identifies how `sig` must be verified.

Examples may include:

* `ed25519`
* `ecdsa-p256`
* `rsa-pss-sha256`

This convention does not mandate which algorithms are permitted.
Profiles or processors may restrict them.

---

## 7.2 `kid`

Declares the signer key identifier.

Example:

```aeon
kid = "alice"
```

This field identifies which verification key should be used.

The identifier is opaque to AEON.

Possible values may include:

* local ids
* DID fragments
* fingerprint-derived ids
* organization-specific key names

Examples:

```aeon
kid = "alice"
kid = "org.example.signing.2026"
kid = "did:example:alice#key-1"
```

---

## 7.3 `sig`

Declares the signature value.

Example:

```aeon
sig = #AABBCC...
```

This field contains the signature bytes encoded using the agreed binary representation.

AEON does not interpret the bytes.

---

# 8. Optional Fields

The following optional fields may be used if needed.

| field     | meaning                             |
| --------- | ----------------------------------- |
| `hashAlg` | hash algorithm used by the signer   |
| `hash`    | integrity hash signed by this entry |
| `time`    | signing timestamp label             |
| `issuer`  | signer identity label               |

These are optional because the minimal model should stay small.

## 8.1 `hashAlg`

Optional explicit copy of the hash algorithm.

```aeon
hashAlg = "sha256"
```

Useful when signatures may be detached or exported independently.

## 8.2 `hash`

Optional explicit copy of the signed integrity hash.

```aeon
hash = #7A91E4C8...
```

Useful for debugging, detached workflows, or validation traces.

## 8.3 `time`

Optional declared signing time.

```aeon
time = "2026-03-08T19:00:00Z"
```

This is informative unless another convention defines trusted timestamp semantics.

## 8.4 `issuer`

Optional signer label.

```aeon
issuer = "Alice Example"
```

Informative only.

---

# 9. Minimal Example

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"
}

message = {
  from = "Alice"
  to = "Bob"
  text = "Meet at the lighthouse"
}

aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha256"
    hash:bytes = #7A91E4C8...
  }

  signatures:signatureSet = [
    {
      alg:string = "ed25519"
      kid:string = "alice"
      sig:bytes = #91A8F2...
    }
  ]
}
```

---

# 10. Multiple Signatures

Multiple signatures are represented as multiple array entries.

Example:

```aeon
aeon:envelope:securityEnvelope = {
  integrity:integrityBlock = {
    alg:string = "sha256"
    hash:bytes = #7A91E4C8...
  }

  signatures:signatureSet = [
    {
      alg:string = "ed25519"
      kid:string = "alice"
      sig:bytes = #AA11...
    }
    {
      alg:string = "ed25519"
      kid:string = "bob"
      sig:bytes = #BB22...
    }
  ]
}
```

Each signature verifies the same integrity hash.

This allows:

* co-signing
* approval chains
* parallel signatures

without changing document coverage.

---

# 11. Verification Procedure

To verify a signature entry, a processor must:

1. Verify the document integrity hash using `aeon.gp.integrity.v1`
2. Read the signature entry
3. Resolve the verification key from `kid`
4. Verify `sig` against the integrity hash using `alg`

If the integrity hash fails, signature verification must fail.

---

# 12. Failure Conditions

A processor should treat the signature as invalid if:

* `alg` is missing
* `kid` is missing
* `sig` is missing
* `alg` is unsupported
* `kid` cannot be resolved
* `sig` does not verify against the integrity hash

A document may still parse as AEON even if signature verification fails.
That is a processor-level security result, not a syntax failure.

---

# 13. Non-Goals

`aeon.gp.signature.v1` does not define:

* trusted signers
* key servers
* certificate chains
* revocation
* timestamp trust
* signature policy

These belong to:

* profiles
* protocols
* application security models

---

# 14. Relationship to Other Conventions

`aeon.gp.signature.v1` works with:

* `aeon.gp.security.v1` — envelope structure
* `aeon.gp.integrity.v1` — canonical hash model

It may later be extended or complemented by:

* `aeon.gp.encryption.v1`
* `aeon.audit.v1`
* `aeon.merkle.v1`

---

# 15. One-Line Definition

`aeon.gp.signature.v1` defines a minimal signature vocabulary for AEON documents in which one or more signatures inside `aeon:envelope.signatures` verify the integrity hash declared by `aeon.gp.integrity.v1`.

---

## Recommended minimal envelope shape

```aeon
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

## `aeon.gp.encryption.v1` — Minimal Encryption Envelope

### Status

Proposed interoperability convention

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

# Minimal Encryption Envelope

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

## Where this leaves the security stack

You now have the **complete core trio**:

* `aeon.gp.integrity.v1`
* `aeon.gp.signature.v1`
* `aeon.gp.encryption.v1`

all operating inside:

* `aeon.gp.security.v1` (envelope structure)

Which is exactly the right size for a first generation security model.

---
