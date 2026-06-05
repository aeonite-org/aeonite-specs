---
id: aeon-security-best-practices
title: AEON Advanced Integrity Patterns
description: Informative guidance on subtree hashing, tamper-evident histories, and related integrity patterns built on AEON structure.
family: conventions
group: Security Conventions
status: Informative
path: specification/conventions/aeon-security-best-practices
license: CC0-1.0
links:
  - aeon-gp-security-envelope-v1
  - aeon-gp-integrity-v1
  - aeon-gp-signature-v1
  - aeon-gp-encryption-v1
---

# AEON Advanced Integrity Patterns

## Status

Informative guidance for implementers.

The patterns described in this document are not defined as formal interoperability conventions.
They are included to demonstrate how AEON’s deterministic structure supports advanced integrity mechanisms such as subtree hashing and tamper-evident event logs.

Future conventions may formalize these patterns.

---

# 1. Merkle-Style Subtree Verification

## 1.1 Overview

Merkle-style hashing allows integrity verification of **subsections of a document** without hashing the entire document.

This technique is useful for:

* large documents
* distributed verification
* selective disclosure
* content-addressable storage
* efficient updates to partially modified documents

---

## 1.2 Why AEON Supports It Well

AEON provides structural properties that make subtree hashing straightforward:

* canonical paths
* deterministic value serialization
* deterministic object ordering
* hierarchical structure

Because each node in an AEON document has a canonical path, a subtree can be hashed independently while maintaining a clear identity.

Example canonical paths:

```text
~.user
~.orders.order1
~.orders.order2
```

---

## 1.3 Example Document

```aeon
user = {
  name = "Alice"
  email = "alice@example.com"
}

orders = {
  order1 = { amount = 10 }
  order2 = { amount = 20 }
}
```

A processor may compute subtree hashes for:

```text
~.user
~.orders.order1
~.orders.order2
```

Conceptually forming a tree:

```text
        root
       /    \
   user    orders
            /   \
       order1  order2
```

Each node’s hash is derived from the hashes of its children.

---

## 1.4 Recommended Practice

Implementations that adopt subtree hashing should:

1. Use canonical AEON paths to identify subtrees.
2. Hash canonical subtree state using the same canonicalization model used for full document integrity.
3. Combine child hashes deterministically to produce parent hashes.
4. Sign or seal the final root hash if cryptographic verification is required.

Proof structures for subtree verification may be:

* stored externally
* transported alongside the document
* included in an envelope extension if appropriate.

---

## 1.5 Typical Use Cases

Merkle-style verification is commonly used for:

* very large structured datasets
* chunked document distribution
* distributed storage systems
* partial document verification
* supply-chain manifests

---

# 2. Tamper-Evident Event Logs

## 2.1 Overview

AEON documents can also represent ordered sequences of events whose integrity depends on **chronological order**.

Such structures are commonly used for:

* audit trails
* system activity logs
* AI decision traces
* workflow histories
* append-only operational records

Unlike document integrity, which protects the final document state, event-log integrity protects the **sequence of events over time**.

---

## 2.2 Event Integrity vs Document Integrity

Two different integrity models exist:

| Model              | Purpose                                  |
| ------------------ | ---------------------------------------- |
| Document integrity | Protect covered canonical document state |
| Event integrity    | Protect chronological sequence of events |

AEON’s standard integrity convention (`aeon.gp.integrity.v1`) is state-based and does not preserve event chronology.

Event logs therefore require a different approach.

---

## 2.3 Recommended Event Representation

For homogeneous event records, arrays provide the clearest representation.

Example:

```aeon
events = [
  {
    id = 1
    action = "create-user"
    user = "alice"
    hashPrev = #000000
  }

  {
    id = 2
    action = "grant-role"
    user = "alice"
    role = "admin"
    hashPrev = #F1342A
  }
]
```

Each event references the hash of the previous event.

This creates a **hash chain** that makes tampering detectable.

---

## 2.4 Recommended Practice

Implementations should consider the following practices when representing event logs.

### Use arrays for homogeneous events

Arrays provide explicit ordering and predictable structure.

### Include a prior-hash reference

Each event should reference the previous event’s hash or prior sealed state.

Example:

```text
hashPrev = #F1342A
```

### Preserve chronological order

Event sequences should not be reordered during integrity processing.

### Periodically seal the log

Long-running logs should periodically be sealed with a document-level signature or integrity envelope.

This prevents rewriting of the event history.

---

## 2.5 Typical Use Cases

Tamper-evident event logs are useful for:

* operational auditing
* regulatory compliance
* AI system traceability
* workflow verification
* infrastructure monitoring

---

# 3. Relationship to AEON Security Conventions

These patterns complement the AEON security conventions.

Formal conventions currently defined include:

* `aeon.gp.security.v1`
* `aeon.gp.integrity.v1`
* `aeon.gp.signature.v1`
* `aeon.gp.encryption.v1`

The patterns described in this document demonstrate how AEON’s structure may also support:

* subtree hashing
* partial document verification
* cryptographically chained event histories

Future versions of the AEON specification may introduce additional conventions that formalize these mechanisms.

---

# 4. Summary

AEON’s deterministic paths, canonicalization model, and structured containers allow it to support advanced integrity mechanisms beyond whole-document signing.

These include:

* Merkle-style subtree verification
* tamper-evident event logs
* partial document integrity proofs
* scalable verification of large structured datasets

These patterns extend AEON’s security capabilities while preserving the minimal design philosophy of the core language.
