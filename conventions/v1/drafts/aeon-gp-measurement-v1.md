---
id: aeon-gp-measurement-v1
title: AEON GP Measurement v1
description: Draft general-purpose measurement convention for units, measurement systems, precision, currency, and packed dimensions.
family: conventions
group: General-Purpose Conventions
status: Draft
path: specification/conventions/aeon-gp-measurement-v1
license: CC0-1.0
links:
  - aeon-conventions-overview
  - measurement-reference
  - compound-unit-labels
---

# AEON GP Measurement v1

Convention identifier: `aeon.gp.measurement.v1`

## Status

Draft interoperability convention

---

# 1. Purpose

`aeon.gp.measurement.v1` defines a lightweight measurement-label convention built on AEON core syntax.

It standardizes a small set of descriptive labels for:

* measurement units
* measurement systems or standards
* representational or measurement precision
* currency denominations
* packed dimensional values

This convention does **not** extend AEON core semantics.
It relies on existing AEON constructs:

* attributes (`@{}`)
* separator syntax (`:sep[...]`)
* ordinary scalar values

---

# 2. Design Goals

The measurement convention aims to be:

* minimal
* predictable
* non-computational
* cross-domain
* easy to validate downstream

It provides measurement interoperability without turning AEON into a unit-conversion or dimensional-analysis language.

---

# 3. Non-Goals

`aeon.gp.measurement.v1` does **not require AEON core** to:

* convert units
* normalize numeric values
* infer measurement systems
* evaluate dimensions
* compute derived values
* perform exchange-rate logic

Examples:

```aeon
distance@{unit="m"} = 3
price@{currency="AUD"} = 19.95
box@{unit="cm" dimensions="W,H,D"}:sep[x] = ^300x300x150
```

These statements only label the data.

Any computation or interpretation belongs to:

* schemas
* profiles
* processors
* application logic

---

# 4. Core Principle

A measurement convention defines interpretation agreements, not language semantics.

AEON core preserves:

* bindings
* attributes
* separators
* scalar values

The convention defines how these preserved patterns are commonly understood by cooperating consumers.

---

# 5. Reserved Measurement Keys

The following lowercase attribute keys have defined meaning under `aeon.gp.measurement.v1`.

Attribute keys defined by this convention **must be lowercase ASCII identifiers**.

Unknown keys remain allowed and are treated as opaque unless defined elsewhere.

| Key          | Purpose                                      |
| ------------ | -------------------------------------------- |
| `unit`       | measurement unit label                       |
| `system`     | measurement system or standard context       |
| `precision`  | representational or measurement resolution   |
| `currency`   | monetary denomination                        |
| `dimensions` | ordering or structure of packed measurements |

---

## 5.1 `unit`

Declares a measurement unit label associated with a value.

```aeon
distance@{unit="m"} = 3
weight@{unit="kg"} = 82
temperature@{unit="C"} = 21
```

Meaning:

* identifies the unit of measurement
* purely descriptive
* does not imply conversion or dimensional reasoning

---

## 5.2 `system`

Declares the system or standard context in which a unit or label should be interpreted.

```aeon
mass@{unit="oz" system="avoirdupois"} = 12
volume@{unit="oz" system="US-fluid"} = 8
distance@{unit="mile" system="imperial"} = 3
length@{unit="m" system="metric"} = 10
```

Meaning:

* disambiguates unit systems
* provides contextual classification
* does not imply conversion behavior

---

## 5.3 `precision`

Declares the intended representational or measurement resolution of a value.

```aeon
length@{unit="mm" precision=0.1} = 125.4
temperature@{unit="C" precision=0.01} = 21.37
price@{currency="AUD" precision=0.01} = 19.95
```

Meaning:

* indicates expected granularity or accuracy
* does not require rounding or formatting

---

## 5.4 `currency`

Declares a currency denomination associated with a numeric value.

```aeon
price@{currency="AUD"} = 19.95
budget@{currency="EUR"} = 500
```

Meaning:

* identifies monetary denomination
* does not imply exchange-rate logic or accounting rules

---

## 5.5 `dimensions`

Declares the ordering or semantic structure of packed dimensional values.

```aeon
box@{unit="cm" dimensions="W,H,D"}:sep[x] = ^300x300x150
```

Meaning:

* describes the dimension ordering
* does not parse or validate the value

---

# 6. Packed Dimension Pattern

AEON core provides separator syntax.
This convention defines a common measurement use for packed dimensional values.

```aeon
box@{unit="cm" dimensions="W,H,D"}:sep[x] = ^300x300x150
```

Meaning:

* `x`-separated dimensional values
* dimension order declared by `dimensions`
* measurement unit declared by `unit`

---

# 7. Unknown Keys

The measurement convention permits extension.

Rule:

* known reserved keys have stable meaning
* unknown keys may appear
* unknown keys should be treated as opaque unless a schema, profile, or another convention defines them

This enables forward compatibility.

---

# 8. Validation Posture

`aeon.gp.measurement.v1` itself is descriptive.

Validation belongs to downstream layers.

Examples:

A schema might require:

* `currency` to match ISO codes
* `unit` to match an allowed list
* `precision` to match allowed increments
* `dimensions` to match the number of packed values

These checks are **not AEON core responsibilities**.

---

# 9. Example Document

```aeon
aeon:header = {
  convention = "aeon.gp.measurement.v1"
}

distance@{unit="m" system="metric" precision=0.01} = 3
price@{currency="AUD" precision=0.01} = 19.95

box@{unit="cm" system="metric" dimensions="W,H,D"}:sep[x] = ^300x300x150

mass@{unit="oz" system="avoirdupois"} = 12
```

---

# 10. Interpretation Summary

| Pattern                 | Meaning                     |
| ----------------------- | --------------------------- |
| `@{unit="m"}`           | measurement unit label      |
| `@{system="metric"}`    | measurement system context  |
| `@{precision=0.01}`     | representational resolution |
| `@{currency="AUD"}`     | monetary denomination       |
| `@{dimensions="W,H,D"}` | dimension ordering          |
| `:sep[x]`               | packed dimension separator  |

---

# 11. Definition

`aeon.gp.measurement.v1` is a versioned interoperability convention that standardizes common measurement labels using AEON core constructs, without extending AEON core semantics.
