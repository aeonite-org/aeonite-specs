---
id: aeon-host-nulls-v1
title: AEON Host Nulls v1
description: Host-language interop convention for explicit null-like values such as JavaScript null, JavaScript undefined, Python None, and Ruby nil.
family: conventions
group: Interop Conventions
path: specification/conventions/aeon-host-nulls-v1
links:
  - aeon-gp-limbo-v1
  - aeon-conventions-overview
---

# AEON Host Nulls v1

## Status

Draft host-language interop convention

Convention identifier: `aeon.host.nulls.v1`

---

# 1. Purpose

`aeon.host.nulls.v1` defines a narrow interop convention for representing host-language null-like values inside an AEON document without changing AEON core semantics.

Documents using this convention should declare it in the header:

```aeon
aeon:header = {
  conventions = [
    "aeon.host.nulls.v1"
  ]
}
```

---

# 2. Reserved Attribute Key

This convention defines one reserved attribute key:

- `host`

Example:

```aeon
email@{host="js.null"} = ""
nickname@{host="js.undefined"} = ""
backupEmail@{host="py.none"} = ""
alias@{host="rb.nil"} = ""
```

The attribute identifies the intended host-language interpretation of the binding.

The serialized scalar acts only as the carrier value unless another schema, profile, or consumer policy defines additional behavior.

---

# 3. Defined Values

| Label            | Meaning                               |
| ---------------- | ------------------------------------- |
| `js.null`        | corresponds to JavaScript `null`      |
| `js.undefined`   | corresponds to JavaScript `undefined` |
| `py.none`        | corresponds to Python `None`          |
| `rb.nil`         | corresponds to Ruby `nil`             |

Rules:

- the label is convention-defined metadata
- the underlying AEON value remains whatever is serialized
- implementations may map these labels during import/export, but such mapping is outside AEON Core

---

# 4. Interop Model

This convention is intended for bounded host-language interop, not for portable semantic claims across all consumers.

For example:

```aeon
email@{host="js.null"} = ""
```

may be treated by a JavaScript-oriented importer as a `null` field, but a generic AEON processor only sees a normal binding with a convention-defined attribute.

---

# 5. Relationship to AEON GP Limbo

`aeon.host.nulls.v1` complements `aeon.gp.limbo.v1`.

- `aeon.gp.limbo.v1` defines portable absence and epistemic labels
- `aeon.host.nulls.v1` defines host-language null interop labels

Documents may declare both conventions when needed.

---

# 6. Non-Goals

This convention does not define:

- host object encoding
- collection conversion rules
- JSON serialization policy
- generalized language interop beyond explicit null-like values

Other host-language behaviors should be defined separately rather than overloaded into this convention.
