---
id: aeon-gp-document-v1
title: AEON GP Document v1
description: Draft document metadata convention for identity, authorship, lifecycle, classification, and handling hints in the AEON header.
family: conventions
group: General-Purpose Conventions
status: Draft
path: specification/conventions/aeon-gp-document-v1
license: CC0-1.0
---

# AEON GP Document v1

Convention identifier: `aeon.gp.document.v1`

## Status

Draft document metadata convention

## Purpose

`aeon.gp.document.v1` defines a standard vocabulary for **document-level metadata**.

This metadata describes:

* authorship
* origin
* lifecycle
* classification
* discoverability
* machine handling hints

The convention applies to metadata stored inside the AEON header.

---

# Location

Document metadata lives inside:

```aeon
aeon:header
```

Example:

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"
  convention = "aeon.gp.document.v1"
}
```

---

# Metadata Container

All document metadata is stored in a `document` object.

```aeon
aeon:header = {

  encoding = "utf-8"
  mode = "strict"

  document = {
    title = "Weather Report"
    author = "Alice"
  }

}
```

This keeps metadata separate from processing fields.

---

# Metadata Fields

## Identity

```aeon
document = {
  title = "Weather Report"
  subject = "Daily rainfall observations"
  description = "Observation notes recorded during coastal storm"
}
```

Fields:

| field         | meaning            |
| ------------- | ------------------ |
| `title`       | document title     |
| `subject`     | short topic        |
| `description` | longer description |

---

# Authorship

```aeon
document = {
  author = "Alice"
  contributors = ["Bob","Carol"]
}
```

Fields:

| field          | meaning                 |
| -------------- | ----------------------- |
| `author`       | primary author          |
| `contributors` | additional contributors |

---

# Copyright and Rights

```aeon
document = {
  copyright = "© 2026 Alice Example"
  license = "CC-BY-4.0"
}
```

Fields:

| field       | meaning            |
| ----------- | ------------------ |
| `copyright` | copyright notice   |
| `license`   | license identifier |

---

# Document Lifecycle

```aeon
document = {
  created = "2026-03-08T18:00:00Z"
  modified = "2026-03-08T18:45:00Z"
}
```

Fields:

| field      | meaning                     |
| ---------- | --------------------------- |
| `created`  | creation timestamp          |
| `modified` | last modification timestamp |

---

# Classification

```aeon
document = {
  labels = ["weather","storm","coastal"]
}
```

Fields:

| field    | meaning                          |
| -------- | -------------------------------- |
| `labels` | keyword labels                   |
| `tags`   | alternate label field if desired |

---

# Privacy and Handling

```aeon
document = {
  privacy = "internal"
}
```

Example values:

| value          | meaning              |
| -------------- | -------------------- |
| `public`       | openly distributable |
| `internal`     | internal use         |
| `confidential` | restricted           |
| `private`      | personal             |

The exact semantics may be defined by profiles.

---

# Content Format

```aeon
document = {
  format = "report"
}
```

Examples:

* report
* message
* dataset
* contract
* log
* configuration

This field describes the conceptual type of document.

---

# Generation Metadata

```aeon
document = {
  generation = "ai-assisted"
}
```

Example values:

| value          | meaning             |
| -------------- | ------------------- |
| `human`        | fully human written |
| `ai-assisted`  | AI helped generate  |
| `ai-edited`    | AI modified         |
| `ai-generated` | fully AI generated  |

This can help downstream consumers evaluate provenance.

---

# Robot Handling

```aeon
document = {
  robots = "noindex"
}
```

Examples:

* index
* noindex
* noai
* noarchive

This mirrors common web document conventions.

---

# Cache Hints

```aeon
document = {
  cache = "no-store"
}
```

Examples:

* cache
* no-cache
* no-store

This field is advisory and intended for systems distributing AEON documents.

---

# Reference Information

```aeon
document = {
  reference = "doc-2026-031"
}
```

Examples:

* internal id
* document reference number
* archival identifier

---

# Example Complete Header

```aeon
aeon:header = {

  encoding = "utf-8"
  mode = "strict"
  convention = "aeon.gp.document.v1"

  document = {
    title = "Weather Report"
    subject = "Storm observation"
    description = "Field notes from coastal storm"

    author = "Alice"
    contributors = ["Bob"]

    copyright = "© 2026 Alice"
    license = "CC-BY-4.0"

    created = "2026-03-08T18:00:00Z"
    modified = "2026-03-08T18:45:00Z"

    labels = ["weather","storm"]

    privacy = "internal"

    format = "report"

    generation = "ai-assisted"

    robots = "noindex"
    cache = "no-store"

    reference = "doc-2026-031"
  }

}
```

---

# Design Goals

The document convention aims to provide:

* human-readable metadata
* machine-readable classification
* interoperability across tools
* minimal structural complexity

It is intentionally flexible so that different domains can extend or interpret the fields according to their needs.

---

# Relationship to Other Conventions

This convention complements the AEON ecosystem:

| convention           | purpose                   |
| -------------------- | ------------------------- |
| `aeon.gp.document.v1`   | document metadata         |
| `aeon.gp.context.v1`    | contextual annotations    |
| `aeon.gp.collection.v1` | collection semantics      |
| `aeon.gp.convention.v1` | data interpretation hints |
| `aeon.gp.security.v1`   | security envelope         |
| `aeon.gp.integrity.v1`  | document hashing          |
| `aeon.gp.signature.v1`  | signatures                |
| `aeon.gp.encryption.v1` | encryption                |

---

# Summary

`aeon.gp.document.v1` provides a lightweight but structured vocabulary for describing AEON documents themselves, allowing tools and systems to understand authorship, classification, lifecycle, and handling policies without interfering with the document’s actual data structure.

---

====



# Language Metadata

## Purpose

The `language` field identifies the natural language used in the document.

This helps with:

* indexing
* translation
* search
* AI processing
* accessibility tools

---

## Recommended Format

Use **BCP-47 language tags**, which are already used by:

* HTML
* HTTP
* XML
* many APIs

Example tags:

| Language           | Tag     |
| ------------------ | ------- |
| English            | `en`    |
| Spanish            | `es`    |
| Dutch              | `nl`    |
| French             | `fr`    |
| Australian English | `en-AU` |
| Belgian Dutch      | `nl-BE` |

---

## Example

```aeon
document = {
  language = "en-AU"
}
```

If multiple languages appear:

```aeon
document = {
  language = ["en","fr"]
}
```

Best practice is to list the **primary language first**.

---

# Location Metadata

## Purpose

The `location` field indicates the geographic context of the document.

This may represent:

* where the document was created
* where the subject matter applies
* geographic relevance

---

## Recommended Structure

Location should be structured rather than a free string.

Example:

```aeon
document = {
  location = {
    country = "AU"
    region = "Victoria"
    city = "Melbourne"
  }
}
```

Using ISO-style identifiers where possible improves interoperability.

---

## Geographic Codes

Recommended standards:

| Field        | Standard   |
| ------------ | ---------- |
| country      | ISO-3166-1 |
| region/state | ISO-3166-2 |
| coordinates  | WGS-84     |

---

## Coordinates (Optional)

If precise location matters:

```aeon
document = {
  location = {
    country = "AU"
    city = "Melbourne"
    coordinates = {
      lat = -37.8136
      lon = 144.9631
    }
  }
}
```

This is useful for:

* geographic datasets
* environmental records
* sensor data
* field observations

---

# Updated Example Header

```aeon
aeon:header = {

  encoding = "utf-8"
  mode = "strict"
  convention = "aeon.gp.document.v1"

  document = {

    title = "Weather Report"
    subject = "Storm observation"
    description = "Field notes from coastal storm"

    author = "Alice"
    contributors = ["Bob"]

    language = "en-AU"

    location = {
      country = "AU"
      region = "Victoria"
      city = "Melbourne"
    }

    created = "2026-03-08T18:00:00Z"
    modified = "2026-03-08T18:45:00Z"

    labels = ["weather","storm"]

    privacy = "internal"

    format = "report"

    generation = "ai-assisted"

    robots = "noindex"
    cache = "no-store"

    reference = "doc-2026-031"

  }

}
```

---

# Design Principle

The **document convention should remain lightweight**.

Good fields for this layer:

* authorship
* lifecycle
* classification
* language
* location
* handling hints

It should **not try to model domain data**, only the **document itself**.

---

# Small Optional Addition (Nice Future-Proofing)

One more field that often proves useful:

```aeon
version = "1.2"
```

This tracks document revision independent of the integrity envelope.

---

# Where We Are Now

With this addition, your AEON ecosystem now has conventions covering:

### Data interpretation

* `aeon.gp.convention.v1`

### Context annotation

* `aeon.gp.context.v1`

### Document metadata

* `aeon.gp.document.v1`

### Security

* `aeon.gp.security.v1`
* `aeon.gp.integrity.v1`
* `aeon.gp.signature.v1`
* `aeon.gp.encryption.v1`

### Advanced integrity (informative)

* Merkle subtree hashing
* tamper-evident event logs

That’s a **very complete first-generation ecosystem**.

---

===


> **separate the metadata container from the metadata vocabulary**

In practical terms:

* `aeon.gp.document.v1` should define the **vocabulary**
* but AEON should settle on one stable **header metadata container shape**

That keeps things simple now, but very extensible later.

## The idea

Instead of every convention inventing its own top-level header layout, you standardize something like:

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"

  conventions = [
    "aeon.gp.document.v1"
  ]

  document = {
    title = "Weather Report"
    author = "Alice"
    language = "en-AU"
  }
}
```

So:

* `aeon:header` = stable metadata container
* `document` = document metadata block defined by `aeon.gp.document.v1`

## Why this is powerful

Because later you can add other metadata vocabularies without changing the outer shape.

Example:

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"

  conventions = [
    "aeon.gp.document.v1"
    "aeon.gp.context.v1"
  ]

  document = {
    title = "Weather Report"
    author = "Alice"
    language = "en-AU"
  }

  context = {
    audience = "internal"
    sensitivity = "restricted"
  }
}
```

That gives you a **header metadata bus**, basically.

## Why it matters long-term

Without this, ecosystems drift into:

* `document = {...}`
* `aeon:header = {...}`
* `info = {...}`
* `headerMeta = {...}`
* `properties = {...}`

and then every tool has to special-case each shape.

With a stable container, you get:

* predictable tooling
* simpler validation
* clearer convention boundaries
* easier future growth

## The deeper architectural benefit

It gives AEON a very clean layered model:

### `aeon:header`

core processing metadata

### `aeon:header`

document/header metadata container

### named metadata sections

convention-defined vocabularies such as:

* `document`
* `context`
* future `publication`
* future `provenance`

So the improvement is really:

> **standardize the header chassis, not just the metadata fields**

## Minimal rule

You do not need much. Just something like:

> Header metadata intended for conventions should be placed directly under `aeon:header`. Individual conventions define named sub-objects within that header.

That one rule keeps the whole system tidy.

## Example final shape

```aeon
aeon:header = {
  encoding = "utf-8"
  mode = "strict"

  conventions = [
    "aeon.gp.document.v1"
  ]

  document = {
    title = "Weather Report"
    subject = "Storm observation"
    description = "Field notes from coastal storm"
    author = "Alice"
    contributors = ["Bob"]
    language = "en-AU"
    location = {
      country = "AU"
      region = "Victoria"
      city = "Melbourne"
    }
    created = "2026-03-08T18:00:00Z"
    modified = "2026-03-08T18:45:00Z"
    labels = ["weather","storm"]
    privacy = "internal"
    format = "report"
    generation = "ai-assisted"
    robots = "noindex"
    cache = "no-store"
    reference = "doc-2026-031"
  }
}
```

## Why I think this is the right move

Because it stays simple now, but prevents header chaos later.

So the long-term improvement is not “add more fields.”
It is:

> **make `meta` the stable metadata framework, and let conventions plug into it cleanly.**

That would make AEON’s metadata story much stronger.
