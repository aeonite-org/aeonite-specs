---
id: aeon-gp-convention-v1
title: AEON GP Convention v1
description: Draft general-purpose convention for shared semantic labels such as units, currency, namespaces, and separator-encoded values.
family: conventions
group: General-Purpose Conventions
status: Draft
path: specification/conventions/aeon-gp-convention-v1
license: CC0-1.0
---

# AEON GP Convention v1

## Status

Draft interoperability convention

---

# 1. Purpose

**AEON Convention v1** defines a lightweight interoperability convention built on top of AEON core syntax.

It standardizes a small set of common semantic labeling patterns so that a document can declare:

```aeon
aeon:header = {
  convention = "aeon.gp.convention.v1"
}
```

or

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.convention.v1"
    "inventory.profile.v1"
  ]
}
```

and receivers can reliably interpret shared conventions such as:

* measurements
* currency
* namespaces
* precision and system context
* separator-encoded values
* format labels

This convention **does not extend AEON core semantics**.
It relies entirely on existing AEON constructs:

* attributes (`@{}`)
* separator syntax (`:sep[...]`)
* ordinary scalar values

---

# 2. Design Goals

AEON Convention v1 aims to be:

• minimal
• predictable
• non-computational
• cross-domain
• easy to validate downstream

It provides **semantic interoperability** without turning AEON into a domain-specific language.

---

# 3. Non-Goals

AEON Convention v1 does **not require AEON core** to:

• convert units
• normalize numeric values
• infer measurement systems
• evaluate formats
• compute derived values

Examples:

```
distance@{unit="m"} = 3
price@{currency="AUD"} = 19.95
version:sep[.] = ^1.0.0
```

These statements only **label the data**.

Any computation or interpretation belongs to:

• schemas
• profiles
• processors / tonic layers
• application logic

---

# 4. Convention Declaration

Documents using the convention should declare it in `meta`.

## 4.1 Single Convention

```
aeon:header = {
  convention = "aeon.gp.convention.v1"
}
```

## 4.2 Multiple Conventions

```
aeon:header = {
  conventions = [
    "aeon.gp.convention.v1"
    "finance.profile.v1"
  ]
}
```

## 4.3 Rule

`convention` and `conventions` are **mutually exclusive**.

A document **must not declare both**.

Implementations may internally normalize:

```
convention = "x"
```

as

```
conventions = ["x"]
```

but this normalization must not appear in serialized documents.

---

# 5. Core Principle

A convention defines **interpretation agreements**, not language semantics.

AEON core preserves:

• bindings
• attributes
• separators
• scalar values

The convention defines **how these preserved patterns are commonly understood**.

---

# 6. Reserved Attribute Keys

The following attribute keys have defined meaning under Convention v1.

Unknown keys remain allowed and are treated as opaque unless defined elsewhere.

---

## 6.1 `unit`

Declares a measurement unit label associated with a value.

```
distance@{unit="m"} = 3
weight@{unit="kg"} = 82
temperature@{unit="C"} = 21
```

Meaning:

• identifies the unit of measurement
• purely descriptive
• does not imply conversion or dimensional reasoning

---

## 6.2 `system`

Declares the system or standard context in which a unit or label should be interpreted.

```
mass@{unit="oz" system="avoirdupois"} = 12
volume@{unit="oz" system="US-fluid"} = 8
distance@{unit="mile" system="imperial"} = 3
length@{unit="m" system="metric"} = 10
```

Meaning:

• disambiguates unit systems
• provides contextual classification
• does not imply conversion behavior

---

## 6.3 `precision`

Declares the intended representational or measurement resolution of a value.

```
length@{unit="mm" precision=0.1} = 125.4
temperature@{unit="C" precision=0.01} = 21.37
price@{currency="AUD" precision=0.01} = 19.95
```

Meaning:

• indicates expected granularity or accuracy
• does not require rounding or formatting

---

## 6.4 `currency`

Declares a currency denomination associated with a numeric value.

```
price@{currency="AUD"} = 19.95
budget@{currency="EUR"} = 500
```

Meaning:

• identifies monetary denomination
• does not imply exchange-rate logic or accounting rules

---

## 6.5 `ns`

Declares a namespace for a semantic token.

```
type@{ns="aeon"} = "document"
status@{ns="workflow"} = "approved"
kind@{ns="media"} = "image"
```

Meaning:

• qualifies interpretation within a named semantic domain
• reduces ambiguity between similar labels

---

## 6.6 `dimensions`

Declares the ordering or semantic structure of packed dimensional values.

```
box@{unit="cm" dimensions="W,H,D"}:sep[x] = ^300x300x150
```

Meaning:

• describes the dimension ordering
• does not parse or validate the value

---

## 6.7 `format`

Declares a representation label for a value.

```
build@{format="semver"}:sep[.] = ^1.0.0
date@{format="ymd"}:sep[-] = ^2026-03-07
```

Meaning:

• labels the representation pattern
• does not require validation unless enforced elsewhere

---

# 7. Separator-Assisted Scalar Conventions

AEON core provides separator syntax.
Convention v1 standardizes common interpretation patterns.

## General Form

```
name:sep[separator] = ^packed-value
```

Meaning:

• `:sep[...]` declares the separator token
• the scalar is intended to be read as packed data
• interpretation depends on surrounding attributes or schemas

---

## 7.1 Version Pattern

```
version:sep[.] = ^1.0.0
```

Meaning:

• dot-separated version segments

No semantic version precedence is implied.

---

## 7.2 Dimension Pattern

```
box@{unit="cm" dimensions="W,H,D"}:sep[x] = ^300x300x150
```

Meaning:

• `x`-separated dimensional values
• dimension order declared by `dimensions`
• measurement unit declared by `unit`

---

## 7.3 Date Pattern

```
date@{format="ymd"}:sep[-] = ^2026-03-07
```

Meaning:

• `-` separated date segments
• ordering defined by `format`

---

# 8. Unknown Keys

Convention v1 permits extension.

Rule:

• known reserved keys have stable meaning
• unknown keys may appear
• unknown keys should be treated as opaque unless a schema or profile defines them

This enables forward compatibility.

---

# 9. Validation Posture

Convention v1 itself is descriptive.

Validation belongs to downstream layers.

Examples:

A schema might require:

• `currency` to match ISO codes
• `unit` to match an allowed list
• `precision` to match allowed increments
• `format="semver"` values to match a pattern

These checks are **not AEON core responsibilities**.

---

# 10. Example Document

```
aeon:header = {
  convention = "aeon.gp.convention.v1"
}

type@{ns="aeon"} = "document"

distance@{unit="m" system="metric" precision=0.01} = 3
price@{currency="AUD" precision=0.01} = 19.95

version@{format="semver"}:sep[.] = ^1.0.0

box@{unit="cm" system="metric" dimensions="W,H,D"}:sep[x] = ^300x300x150

date@{format="ymd"}:sep[-] = ^2026-03-07

mass@{unit="oz" system="avoirdupois"} = 12
```

---

# 11. Interpretation Summary

| Pattern                 | Meaning                     |
| ----------------------- | --------------------------- |
| `@{unit="m"}`           | measurement unit label      |
| `@{system="metric"}`    | measurement system context  |
| `@{precision=0.01}`     | representational resolution |
| `@{currency="AUD"}`     | monetary denomination       |
| `@{ns="..."}`           | semantic namespace          |
| `@{dimensions="W,H,D"}` | dimension ordering          |
| `@{format="semver"}`    | representation format label |
| `:sep[...]`             | packed scalar separator     |

---

# 12. Definition

**AEON Convention v1** is a versioned interoperability agreement that standardizes common attribute labels and separator-based scalar representations using AEON core constructs, without extending AEON core semantics.

---

# 13. Governance Recommendation

Keep Convention v1 intentionally small.

Recommended reserved key registry:

```
unit
system
precision
currency
ns
dimensions
format
```

Future conventions may extend this registry or specialize it for particular domains.

---

===


# Appendix — AEON Convention v1

## Status

Proposed interoperability convention

---

# 1. Overview

**AEON Convention v1** defines a lightweight interoperability convention built on top of AEON core syntax.

It standardizes a small set of commonly used semantic labeling patterns while preserving AEON’s core principles:

* AEON core remains syntax and structure only
* Conventions define interpretation agreements
* No new computation or evaluation semantics are introduced

This convention allows documents to declare predictable metadata patterns such as:

* measurement labeling
* currency labeling
* namespace qualification
* representation formats
* separator-encoded scalar values

---

# 2. Convention Declaration

Documents using this convention should declare it in the `meta` object.

### Single convention

```aeon
aeon:header = {
  convention = "aeon.gp.convention.v1"
}
```

### Multiple conventions

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.convention.v1"
    "finance.profile.v1"
  ]
}
```

### Rule

`convention` and `conventions` are **mutually exclusive**.

A document must not contain both fields.

Implementations may internally normalize:

```
convention = "x"
```

to

```
conventions = ["x"]
```

but serialized documents must use only one form.

---

# 3. Design Principles

AEON Convention v1 follows these principles:

**1 — Non-invasive**

The convention introduces no new AEON language features.

**2 — Descriptive only**

Attributes describe data but do not instruct computation.

**3 — Domain neutral**

The convention provides labeling patterns usable across domains.

**4 — Extensible**

Unknown attribute keys remain valid unless restricted by schemas or profiles.

---

# 4. Core Language Independence

AEON Convention v1 introduces **no new syntactic, canonicalization, or evaluation rules**.

All structural behavior remains governed by AEON core.

Specifically, the convention does **not** define:

* parsing rules
* ordering rules
* canonicalization rules
* evaluation rules

These remain entirely within AEON core.

---

# 5. Reserved Attribute Keys

The following lowercase attribute keys are defined by AEON Convention v1.

| Key         | Purpose                                    |
| ----------- | ------------------------------------------ |
| `unit`      | measurement unit label                     |
| `system`    | contextual measurement system              |
| `precision` | representational or measurement resolution |
| `currency`  | monetary denomination                      |
| `ns`        | semantic namespace                         |
| `format`    | representation format label                |

Attribute keys defined by this convention **must be lowercase ASCII identifiers**.

---

# 6. Attribute Definitions

## 6.1 `unit`

Declares a measurement unit label associated with a value.

```aeon
distance@{unit="m"} = 3
temperature@{unit="C"} = 21
weight@{unit="kg"} = 82
```

The attribute is descriptive only and does not imply conversion or dimensional computation.

---

## 6.2 `system`

Declares the measurement or classification system associated with a value.

```aeon
mass@{unit="oz" system="avoirdupois"} = 12
volume@{unit="oz" system="US-fluid"} = 8
distance@{unit="mile" system="imperial"} = 3
```

This attribute exists to disambiguate units that vary between systems.

---

## 6.3 `precision`

Declares the intended representational or measurement resolution.

```aeon
length@{unit="mm" precision=0.1} = 125.4
price@{currency="AUD" precision=0.01} = 19.95
temperature@{unit="C" precision=0.01} = 21.37
```

The attribute does not require rounding or formatting.

---

## 6.4 `currency`

Declares a monetary denomination.

```aeon
price@{currency="AUD"} = 19.95
budget@{currency="EUR"} = 500
```

The attribute does not imply exchange rate handling or accounting rules.

---

## 6.5 `ns`

Declares a semantic namespace for a value.

```aeon
type@{ns="aeon"} = "document"
status@{ns="workflow"} = "approved"
kind@{ns="media"} = "image"
```

Namespaces reduce ambiguity between identical labels used in different domains.

---

## 6.6 `format`

Declares a representation format for a value.

```aeon
version@{format="semver"}:sep[.] = ^1.0.0
date@{format="ymd"}:sep[-] = ^2026-03-07
box@{unit="cm" format="dims:W,H,D"}:sep[x] = ^300x300x150
```

The format label identifies the structure of a packed scalar representation.

It does not require validation unless enforced by a schema or profile.

---

# 7. Separator-Encoded Scalars

AEON core provides separator syntax:

```
name:sep[separator] = ^packed-value
```

Convention v1 standardizes common interpretive patterns using this syntax.

Example:

```aeon
version@{format="semver"}:sep[.] = ^1.0.0
date@{format="ymd"}:sep[-] = ^2026-03-07
location@{format="geo:lat,lon"}:sep[,] = ^37.8136,144.9631
```

The separator describes representation structure but does not imply automatic parsing.

---

# 8. Unknown Keys

Unknown attribute keys remain valid.

Processors should treat unknown keys as opaque unless:

* a schema defines them
* a profile defines them
* a processor explicitly supports them

This ensures forward compatibility.

---

# 9. Example Document

```aeon
aeon:header = {
  convention = "aeon.gp.convention.v1"
}

type@{ns="aeon"} = "document"

distance@{unit="m" system="metric" precision=0.01} = 3

price@{currency="AUD" precision=0.01} = 19.95

version@{format="semver"}:sep[.] = ^1.0.0

box@{unit="cm" format="dims:W,H,D"}:sep[x] = ^300x300x150

date@{format="ymd"}:sep[-] = ^2026-03-07

mass@{unit="oz" system="avoirdupois"} = 12
```

---

# 10. Summary

AEON Convention v1 provides a small interoperability layer for labeling data while preserving AEON’s core philosophy:

* AEON core defines structure
* conventions define interpretation
* processors define behavior

This separation allows conventions to evolve without expanding the AEON language itself.

---

If you'd like, we can also define a **very small follow-up appendix** that will matter later:

**Appendix — Convention Naming and Versioning Rules**

Because that determines whether the ecosystem ends up with nice names like:

```
aeon.gp.convention.v1
finance.profile.v1
catalog.profile.v2
```

or chaotic ones like:

```
convention-final-v2-new-fixed-last
```
