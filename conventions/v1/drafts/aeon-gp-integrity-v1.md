---
id: aeon-gp-integrity-v1
title: AEON GP Integrity v1
description: Draft integrity convention defining deterministic canonical hashing for AEON documents.
family: conventions
group: Security Conventions
status: Draft
path: specification/conventions/aeon-gp-integrity-v1
license: CC0-1.0
links:
  - aeon-gp-security-envelope-v1
  - aeon-gp-signature-v1
  - aeon-gp-encryption-v1
---

# AEON GP Integrity v1

Convention identifier: `aeon.gp.integrity.v1`

## Status

Draft interoperability convention

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
