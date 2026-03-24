---
id: appendix-integrity-envelope-v1
title: Appendix - Integrity Envelope
description: Integrity envelope structure and representation rules for signed or hashed payload metadata.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-integrity-envelope-v1
---

# Appendix — Integrity Envelope

**Appendix to:** AEON Specification v1

**Status:** normative v1 appendix

Canonical topic owner: `../AEON-spec-v1.md`

This appendix defines the standard AEON integrity envelope shape used by the baseline security conventions:

- `aeon.gp.security.v1`
- `aeon.gp.integrity.v1`
- `aeon.gp.signature.v1`
- `aeon.gp.encryption.v1`

The envelope is optional. If present, it is inert with respect to document meaning.
It is modeled as a normal top-level object binding whose datatype is `:envelope`.
Consumers are free to use `:envelope` the same way they use any other object alias; the GP security conventions simply reserve a conventional role for it.

---

## 1. Purpose

The integrity envelope provides a standard location for:
- canonical integrity hashes
- signatures over those hashes
- optional encrypted payload metadata

It MUST NOT alter document meaning, evaluation, profile selection, schema selection, or reference legality.

---

## 2. Declaration and Conventions

Documents using the standard security envelope should declare the relevant conventions in `aeon:header`.

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
```

Convention declarations remain advisory until trusted or selected by the consumer.

---

## 3. Envelope Declaration

The standard envelope is declared as a typed top-level binding.
`close` is the recommended conventional key, but it is not semantically privileged by Core:

```aeon
close:envelope = {
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

The envelope object may contain the following standard sections:
- `integrity`
- `signatures`
- `encryption`

Additional sections are convention-defined and non-Core.

---

## 4. Placement Rules

1. The chosen top-level `:envelope` binding MUST be the final binding in the document.
2. Only whitespace or comments may follow it.
3. The envelope is excluded from integrity-hash coverage.

---

## 5. Standard Sections

### 5.1 `integrity`

Defined by `aeon.gp.integrity.v1`.

```aeon
integrity:integrityBlock = {
  alg:string = "sha-256"
  hash:string = "7a91e4c8..."
}
```

| Field  | Required | Meaning                                             |
| ------ | -------- | --------------------------------------------------- |
| `alg`  | yes      | canonical hash algorithm                            |
| `hash` | yes      | canonical hash over the envelope-free document body |

### 5.2 `signatures`

Defined by `aeon.gp.signature.v1`.

```aeon
signatures:signatureSet = [
  {
    alg:string = "ed25519"
    kid:string = "alice"
    sig:string = "BASE64_SIGNATURE"
  }
]
```

| Field | Required | Meaning                   |
| ----- | -------- | ------------------------- |
| `alg` | yes      | signature algorithm       |
| `kid` | yes      | key identifier            |
| `sig` | yes      | signature bytes/text form |

### 5.3 `encryption`

Defined by `aeon.gp.encryption.v1`.

```aeon
encryption:encryptionBlock = {
  alg:string = "xchacha20-poly1305"
  kid:string = "bob"
  ciphertext:string = "ENCRYPTED_PAYLOAD"
}
```

| Field        | Required | Meaning                          |
| ------------ | -------- | -------------------------------- |
| `alg`        | yes      | encryption algorithm             |
| `kid`        | yes      | recipient or key identifier      |
| `ciphertext` | yes      | encrypted payload representation |

---

## 6. Excluded Content

The standard envelope does not authorize:
- schema or profile selection
- processor enablement
- trust-model self-assertion
- embedded public-key trust
- executable behavior

These remain consumer-policy concerns.

---

## 7. Canonical Integrity Coverage

### 7.1 Coverage Rule

The canonical integrity hash is computed over the document body excluding the top-level `:envelope` binding.

### 7.2 Input Model

Canonical hashing derives from the Assignment Event stream:
1. compile the document body to AES
2. exclude the selected top-level `:envelope` subtree (for example `$.close`)
3. serialize the resulting canonical state deterministically
4. hash that serialization using the declared integrity algorithm

### 7.3 Coverage Notes

- the envelope is never included in its own integrity hash
- comments and annotation records are not part of canonical integrity coverage
- convention declarations in `aeon:header` are covered because they are part of the body state

---

## 8. Signature Coverage

Standard signatures are computed over the integrity hash declared in the selected envelope binding's `integrity` section.

This means:
1. compute the canonical integrity hash
2. sign that hash representation
3. store the result in the envelope binding's `signatures`

Public keys are resolved out-of-band by consumer policy. Implementations MUST NOT trust embedded key material by default.

---

## 9. Verification Procedure

1. Parse the document structurally.
2. Confirm the top-level `:envelope` binding, if present, is the final binding.
3. Read `aeon:header.conventions` if present, but treat them as advisory.
4. Recompute the integrity hash over the envelope-free document body.
5. Compare the result with the envelope binding's `integrity.hash`.
6. If signatures are present, verify them against trusted external key material.
7. If encryption metadata is present, apply separate consumer policy for decryption.

---

## 10. Security Notes

- Integrity hashes provide tamper evidence, not trust by themselves.
- Signature verification depends on trusted key resolution.
- Encryption metadata does not itself imply confidentiality unless the consumer recognizes and applies the corresponding convention.
- The envelope MUST NOT influence schema/profile selection.

---

## 11. Minimal Full Example

```aeon
aeon:header = {
  encoding:string = "utf-8"
  mode:string = "strict"
  conventions:conventionSet = [
    "aeon.gp.security.v1"
    "aeon.gp.integrity.v1"
    "aeon.gp.signature.v1"
    "aeon.gp.encryption.v1"
  ]
}

message:object = {
  from:string = "Alice"
  to:string = "Bob"
  body:string = "Meet at the lighthouse"
}

close:envelope = {
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
  encryption:encryptionBlock = {
    alg:string = "xchacha20-poly1305"
    kid:string = "bob"
    ciphertext:string = "ENCRYPTED_PAYLOAD"
  }
}
```

*End of Integrity Envelope*
