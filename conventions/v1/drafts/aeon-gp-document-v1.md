---
id: aeon-gp-document-v1
title: AEON GP Document v1
description: Draft document metadata convention for identity, authorship, lifecycle, classification, namespaces, representation formats, and handling hints in the AEON header.
family: conventions
group: General-Purpose Conventions
status: Draft
path: specification/conventions/aeon-gp-document-v1
license: CC0-1.0
links:
  - aeon-conventions-overview
  - aeon-gp-measurement-v1
  - aeon-gp-convention-v1
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
  created = 2026-03-08T18:00:00Z
  modified = 2026-03-08T18:45:00Z
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
  tags = ["rainfall","field-notes"]
}
```

Fields:

| field    | meaning                          |
| -------- | -------------------------------- |
| `labels` | keyword labels                   |
| `tags`   | alternate label field if desired |

---

# Namespace Metadata

The `ns` field declares a semantic namespace for document-level labels or document identity.

```aeon
document = {
  ns = "aeon"
}
```

Namespaces qualify interpretation within a named semantic domain and reduce ambiguity between similar labels.

When namespace labels are needed on individual values, the same key may be used as binding metadata:

```aeon
type@{ns="aeon"} = "document"
status@{ns="workflow"} = "approved"
kind@{ns="media"} = "image"
```

The `ns` label is descriptive only.
It does not create a schema namespace, import mechanism, or lookup rule by itself.

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

The `format` key may also be used as binding metadata when a document value carries a known representation pattern.

```aeon
build@{format="semver"}:sep[.] = ^1.0.0
date@{format="ymd"}:sep[-] = ^2026-03-07
location@{format="geo:lat,lon"}:sep[,] = ^37.8136,144.9631
```

In this form, `format` labels the representation pattern.
It does not require validation unless a schema, profile, processor, or another convention defines that validation.

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

# Language Metadata

The `language` field identifies the natural language used in the document.

Use **BCP-47 language tags**.

Examples:

| Language           | Tag     |
| ------------------ | ------- |
| English            | `en`    |
| Spanish            | `es`    |
| Dutch              | `nl`    |
| French             | `fr`    |
| Australian English | `en-AU` |
| Belgian Dutch      | `nl-BE` |

```aeon
document = {
  language = "en-AU"
}
```

If multiple languages appear, list the primary language first.

```aeon
document = {
  language = ["en","fr"]
}
```

---

# Location Metadata

The `location` field indicates the geographic context of the document.

This may represent:

* where the document was created
* where the subject matter applies
* geographic relevance

Location should be structured rather than a free string.

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

Recommended standards:

| Field        | Standard   |
| ------------ | ---------- |
| country      | ISO-3166-1 |
| region/state | ISO-3166-2 |
| coordinates  | WGS-84     |

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

    ns = "aeon"

    language = "en-AU"

    location = {
      country = "AU"
      region = "Victoria"
      city = "Melbourne"
    }

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
* clear separation from domain data

It is intentionally flexible so that different domains can extend or interpret the fields according to their needs.

The document convention describes the document itself. It does not model the document's domain data.

---

# Relationship to Other Conventions

This convention complements the AEON ecosystem:

| convention               | purpose                       |
| ------------------------ | ----------------------------- |
| `aeon.gp.document.v1`    | document metadata             |
| `aeon.gp.context.v1`     | contextual annotations        |
| `aeon.gp.collection.v1`  | collection semantics          |
| `aeon.gp.measurement.v1` | measurement labels            |
| `aeon.gp.convention.v1`  | convention authoring template |
| `aeon.gp.security.v1`    | security envelope             |
| `aeon.gp.integrity.v1`   | document hashing              |
| `aeon.gp.signature.v1`   | signatures                    |
| `aeon.gp.encryption.v1`  | encryption                    |

---

# Summary

`aeon.gp.document.v1` provides a lightweight but structured vocabulary for describing AEON documents themselves, allowing tools and systems to understand authorship, classification, lifecycle, and handling policies without interfering with the document’s actual data structure.
