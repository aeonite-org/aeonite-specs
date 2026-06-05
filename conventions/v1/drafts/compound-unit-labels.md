---
id: compound-unit-labels
title: Compound Unit Labels
description: Informative note on using compound unit labels such as m/s and kg/m^3 as opaque identifiers in conventions.
family: conventions
group: Informative Convention Appendices
status: Informative
path: specification/conventions/compound-unit-labels
license: CC0-1.0
links:
  - aeon-gp-measurement-v1
---

# Appendix — Compound Unit Labels (Informative)

AEON GP Measurement v1 permits compound unit labels in the `unit` attribute.

Compound unit labels are treated as **opaque identifiers** and are not parsed or interpreted by AEON.

Example:

```aeon
speed@{unit="m/s"} = 12
acceleration@{unit="m/s^2"} = 9.81
density@{unit="kg/m^3"} = 1000
bandwidth@{unit="Mb/s"} = 100
```

---

# Interpretation

Compound unit labels may describe derived measurements such as:

| Unit     | Meaning                   |
| -------- | ------------------------- |
| `m/s`    | meters per second         |
| `m/s^2`  | meters per second squared |
| `kg/m^3` | kilograms per cubic meter |
| `Mb/s`   | megabits per second       |

AEON does **not** interpret or validate these expressions.

They are treated as **plain unit identifiers**.

---

# No Grammar Requirement

AEON GP Measurement v1 does not define a formal grammar for compound units.

Characters such as the following may appear within unit labels:

```
/
*
^
-
```

Example:

```aeon
power@{unit="kg*m^2/s^3"} = 120
```

Processors, schemas, or profiles may optionally define stricter rules if needed.

---

# Recommended Practice

When compound units are used, they should follow widely recognized conventions (such as SI notation) to improve interoperability.

Example:

```aeon
flow_rate@{unit="m^3/s"} = 4
```

---

# Summary

Compound units are allowed because:

* they are common in scientific and engineering data
* they require no additional language features
* they remain consistent with AEON’s rule of **opaque value labeling**

AEON therefore preserves compound unit labels exactly as written.

---
