---
id: aeon-gp-temporal-v1
title: AEON GP Temporal v1
description: "Draft temporal convention for interpreting temporal literals with explicit timezone, timezone database version, calendar, and ambiguity metadata."
family: conventions
group: General-Purpose Conventions
status: Draft temporal convention
license: CC0-1.0
path: specification/conventions/aeon-gp-temporal-v1
links:
  - aeon-conventions-overview
  - aeon-core-v1-value-types
---
# AEON GP Temporal v1

## Status

Draft temporal convention

Convention identifier: `aeon.gp.temporal.v1`

---

# 1. Purpose

`aeon.gp.temporal.v1` defines a standard metadata vocabulary for interpreting AEON temporal literals.

It applies to ordinary Core temporal literal families such as:

- `date`
- `time`
- `datetime`
- convention- or profile-defined duration representations

The convention separates:

| Concern | Responsibility |
| ------- | -------------- |
| Temporal literal form | AEON Core value syntax |
| Temporal interpretation policy | `aeon.gp.temporal.v1` metadata |
| Materialization and execution | Tonics, profiles, processors, or host runtimes |

This convention does not extend AEON Core syntax and does not make runtime scheduling, timezone conversion, or calendar conversion behavior mandatory.

Documents using this convention should declare it in the header:

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.temporal.v1"
  ]
}
```

---

# 2. Design Intent

Modern temporal data often combines several independent concerns:

- UTC instants
- floating or local civil times
- geopolitical time zones
- daylight-saving ambiguity
- historical timezone database drift
- calendar systems
- offset conflict handling

`aeon.gp.temporal.v1` represents those concerns structurally with metadata rather than overloading timestamp punctuation.

Example:

```aeon
meeting@{
  target = "zone"
  zone = "Australia/Melbourne"
  calendar = "iso8601"
  tzdbDatum:date = 2026-05-10
  tzdbVersion = "2026b"
  disambiguation = "reject"
}:datetime = 2026-06-06T10:10:00
```

The literal remains an ordinary `datetime`; the convention metadata states how a cooperating consumer should interpret it.

---

# 3. Scope

This convention defines temporal interpretation metadata.

It does not define:

- new Core temporal literal syntax
- a new Core `duration` literal
- timezone database contents
- canonical temporal serialization
- runtime scheduling behavior
- host-language temporal object materialization

Consumers that do not understand this convention should preserve the attributes as ordinary AEON metadata or fail according to their convention-adoption policy.

---

# 4. Fields

The following attribute keys are defined by `aeon.gp.temporal.v1`.

## 4.1 `target`

`target` identifies the intended temporal interpretation mode.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"utc"` | Interpret as a universal instant |
| `"local"` | Interpret as a floating/local civil time |
| `"zone"` | Interpret as a regional civil time in a named zone |

Examples:

```aeon
created@{
  target = "utc"
}:datetime = 2026-06-06T10:10:00Z
```

```aeon
alarm@{
  target = "local"
}:datetime = 2026-06-06T09:00:00
```

```aeon
meeting@{
  target = "zone"
  zone = "Australia/Melbourne"
}:datetime = 2026-06-06T10:10:00
```

## 4.2 `zone`

`zone` identifies the authoritative regional timezone.

```aeon
zone = "Australia/Melbourne"
```

Rules:

- values SHOULD be IANA timezone database identifiers;
- consumers applying `zone` MUST fail if the zone is unknown;
- consumers MUST NOT silently substitute an equivalent or nearby zone.

## 4.3 `calendar`

`calendar` identifies the calendar system used to interpret the temporal value.

Examples:

```aeon
calendar = "iso8601"
calendar = "gregorian"
calendar = "japanese"
calendar = "hebrew"
```

If omitted, consumers MAY assume `iso8601`. A profile or schema MAY require explicit calendar metadata.

## 4.4 `tzdbDatum`

`tzdbDatum` records the date of timezone database assumptions used by the producer.

```aeon
tzdbDatum:date = 2026-05-10
```

This field improves reproducibility and helps future processors detect possible timezone rule drift. It does not pin an exact timezone database version.

## 4.5 `tzdbVersion`

`tzdbVersion` records the timezone database release identifier used by the producer.

```aeon
tzdbVersion = "2026b"
```

Values SHOULD use IANA Time Zone Database release labels when the producer can identify the source rule set. This field improves reproducibility when timezone rules change after the document is produced.

## 4.6 `disambiguation`

`disambiguation` states how ambiguous or invalid local times should be handled.

Allowed values:

| Value | Meaning |
| ----- | ------- |
| `"earlier"` | Choose the earlier valid instant |
| `"later"` | Choose the later valid instant |
| `"compatible"` | Use consumer-defined compatibility behavior |
| `"reject"` | Fail on ambiguity or invalid local time |

Example:

```aeon
event@{
  target = "zone"
  zone = "Australia/Melbourne"
  disambiguation = "reject"
}:datetime = 2025-04-06T02:30:00
```

## 4.7 `offset`

`offset` records an offset associated with the value.

```aeon
offset = "+10:00"
```

This field is informational unless another selected profile, schema, or tonic defines stronger behavior.

Consumers MAY validate offset consistency, ignore offsets, or reject offset conflicts. This convention does not define offset precedence rules.

## 4.8 `apply`

`apply` lists target projection zones for display or transformation workflows.

```aeon
apply = [
  "Australia/Perth"
  "Europe/Paris"
]
```

This field does not define execution semantics.

---

# 5. Fail-Closed Guidance

Consumers applying this convention SHOULD fail when:

- timezone identifiers are unknown;
- ambiguous or invalid local times violate the selected policy;
- required metadata is missing;
- calendar systems are unsupported.

Consumers MUST NOT silently reinterpret temporal intent.

---

# 6. Relationship to Core Temporal Types

AEON Core v1 owns the literal syntax for `date`, `time`, and `datetime`.

`aeon.gp.temporal.v1` does not change those literal forms. It adds interpretation metadata around them.

Duration semantics remain outside AEON Core v1. When duration-like values are needed, they are schema-, profile-, convention-, or consumer-defined.

---

# 7. Relationship to Future `zdt`

The datatype label `zdt` is reserved for a possible future zoned datetime type.

`zdt` is not operational in AEON Core v1. This convention does not require processors to accept `:zdt`, and it does not define bracketed zoned-datetime lexical syntax.

Future AEON versions or profiles may define a transport-oriented `zdt` type. The temporal convention remains orthogonal to that possibility because it represents timezone, calendar, ambiguity, and projection metadata structurally.

Possible future example:

```aeon
created:zdt = 2025-01-01T12:00:00+11:00[Australia/Melbourne][u-ca=japanese]
```

The example above is reserved future syntax, not AEON Core v1 syntax.

---

# 8. Related Standards

This convention is conceptually compatible with:

- RFC 3339
- RFC 9557
- Java `ZonedDateTime`
- JavaScript `Temporal`

It does not require AEON Core to adopt bracketed zone annotations, inline calendar annotations, or any specific host-runtime temporal object model.
