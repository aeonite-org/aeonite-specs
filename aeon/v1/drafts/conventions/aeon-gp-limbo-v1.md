---
id: aeon-gp-limbo-v1
title: AEON GP Limbo v1
description: General-purpose convention for explicit absence and epistemic-state labels carried in AEON attributes.
family: conventions
group: General-Purpose Conventions
path: specification/conventions/aeon-gp-limbo-v1
links:
  - aeon-conventions-overview
  - aeon-quick-mental-model
---

# AEON GP Limbo v1

## Status

Draft general-purpose convention

Convention identifier: `aeon.gp.limbo.v1`

---

# 1. Purpose

`aeon.gp.limbo.v1` defines a lightweight convention for representing:

- explicit absence states
- epistemic states about whether a value is known

It uses ordinary AEON attributes and does not extend AEON core syntax.

Documents using this convention should declare it in the header:

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.limbo.v1"
  ]
}
```

---

# 2. Design Intent

This convention exists for cases where a binding must remain structurally present, but the producer needs to express why its apparent value should not be treated as plain asserted content.

AEON Core does not define built-in null, nil, none, or missing-value types.
If a document needs to express absence or uncertainty while still carrying a binding, that meaning must come from a convention, schema, profile, or consumer policy rather than from Core itself.

Examples:

- a field exists but has not yet been initialized
- a field is intentionally not applicable in the current context
- a field is known to be unknown

The convention does not require processors to coerce, erase, or infer values. It only labels them.

The serialized scalar acts only as the carrier value unless another schema, profile, or consumer policy gives it stronger meaning.

---

# 3. Reserved Attribute Keys

This convention defines two reserved attribute keys:

- `absence`
- `epistemic`

Unknown additional keys remain allowed unless restricted by another convention, schema, or profile.

---

# 4. `absence`

The `absence` attribute labels explicit absence conditions.

Example:

```aeon
name@{absence="limbo.uninitialised"} = ""
deletedAt@{absence="limbo.tombstone"} = ""
middleName@{absence="limbo.notApplicable"} = ""
```

Defined values in v1:

| Label                  | Meaning                         |
| ---------------------- | ------------------------------- |
| `limbo.none`           | explicit absence                |
| `limbo.uninitialised`  | value slot exists but not set   |
| `limbo.notApplicable`  | value does not apply in context |
| `limbo.tombstone`      | deleted or intentionally erased |

Rules:

- the attribute is descriptive and convention-level only
- it does not force any AEON core type change
- consumers may define stricter handling in schemas or profiles

---

# 5. `epistemic`

The `epistemic` attribute labels knowledge-state claims about a value.

Example:

```aeon
age@{epistemic="limbo.knownUnknown"} = 0
temperature@{epistemic="limbo.knownKnown"} = 21
```

Defined values in v1:

| Label                   | Meaning                      |
| ----------------------- | ---------------------------- |
| `limbo.knownKnown`      | value is asserted as known   |
| `limbo.knownUnknown`    | producer asserts unknownness |
| `limbo.unknownKnown`    | knowledge state is unclear   |
| `limbo.unknownUnknown`  | nothing reliable is claimed  |

Rules:

- the attribute describes epistemic stance, not truth
- the payload value remains structurally present
- consumers may reject contradictory combinations under schema or profile policy

---

# 6. Combined Use

`absence` and `epistemic` may appear together when both dimensions matter.

```aeon
email@{
  absence = "limbo.uninitialised"
  epistemic = "limbo.knownUnknown"
} = ""
```

This convention does not define a mandatory conflict-resolution model. Combination handling is consumer-defined. If a system needs stricter rules, that belongs in a schema, profile, or processor policy.

---

# 7. Non-Goals

This convention does not define:

- AI inference
- automatic nullability conversion
- host-language serialization behavior
- implicit default values

Those concerns belong to other layers.

---

# 8. Relationship to Core, Profiles, and Schemas

- AEON Core preserves the binding, attributes, and scalar value.
- This convention defines how cooperating systems interpret the limbo labels.
- Schemas may restrict allowed labels or combinations.
- Profiles may require or forbid the convention for a document class.
