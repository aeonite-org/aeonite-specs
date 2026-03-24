---
id: appendix-profiles-framework-v1
title: Appendix - Profiles Framework
description: Profile system architecture, authority model, and integration boundaries.
family: appendices-v1
group: AEOS and Profiles
path: specification/appendices/appendix-profiles-framework-v1
---

# Appendix — Profiles Framework

**Appendix to:** AEON Specification v1

Profiles define optional, named semantic layers for AEON documents. They allow specialized behavior while keeping the AEON core minimal and stable.

---

## 1. Purpose of Profiles

Profiles exist so AEON can support domain-specific behavior:
- Output transforms (e.g., JSON)
- Optional syntactic features (e.g., node trees)
- Domain-specific typing or validation
- Host integration rules

Profiles are **explicit**, **opt-in**, and **non-breaking** to AEON grammar.

---

## 2. Declaring a Profile

```aeon
aeon:header = {
  profile = "aeonite.spreadsheet.v1"
}
```

Or using shorthand:
```aeon
aeon:profile = "aeonite.spreadsheet.v1"
```

A document may declare **exactly one** profile.

### 2.1 Zero-Trust Selection Model

Profile declaration inside the document is **advisory only**.

- Processors MUST treat `aeon:profile` / `aeon:header.profile` as an untrusted claim.
- Processor/runtime configuration remains authoritative for profile selection.
- If a processor accepts document-declared routing, it MUST:
  - resolve only against an explicit whitelist/registry of accepted profiles;
  - verify the document is valid for the selected profile;
  - fail closed on mismatch (`declared profile` vs `validated/selected profile`).

Document profile declarations are therefore a routing hint, not a trust anchor.

---

## 3. Profile Capabilities

### 3.1 Interpretation Rules

Profiles may reinterpret AEON constructs *after parsing*:
- JSON profile resolves references before output
- a profile may require conventions such as `aeon.gp.limbo.v1` or `aeon.host.nulls.v1` for a document class

Profiles **must not** alter AEON grammar.

### 3.2 Validation Rules

Profiles may:
- Tighten constraints
- Forbid constructs (e.g., pointer references)
- Require schemas

### 3.3 Output Transformation

Profiles may produce alternative representations:
- `aeon.json` → JSON output
- `aeonite.spreadsheet.v1` → cell/value model

### 3.4 Feature Enablement

Profiles activate optional syntax or behavior:
- Node profile enables node syntax `<tag(...)>` / `<tag>`
- Spreadsheet profile enables separator literals

---

## 4. Profile Contract

Each profile MUST specify:
- Profile name
- Semantic scope
- Determinism level
- Enabled/disabled features
- Output transformation (if any)
- Error model extensions
- Schema interaction
- Canonicalization rules

---

## 5. Determinism Levels

Profiles MUST declare:
- **deterministic**
- **conditionally deterministic**
- **non-deterministic**

Example: a processor-specific AI interpretation profile would be explicitly non-deterministic and therefore outside AEON v1's portable convention surface.

---

## 6. Profile Naming Standard

Public profiles SHOULD follow:
```
<authority>.<domain>[.<subdomain>]*[.<version>]
```

### Authority Examples
```
aeon
aeonite
io.github.username
org.company
```

### Full Examples
```
aeon.json
aeon.node
aeonite.spreadsheet.v1
startup.sonograph.format.v1
```

---

## 7. Profile Lifecycle

- Profiles remain immutable once published
- Breaking changes → new version suffix
- Future versions do not override old behavior

---

## 8. Reference Behavior

AEON guarantees that:
- Clone (`~`) preserves value intent
- Pointer (`~>`) preserves identity intent

Profiles may reinterpret references for output but may not modify the underlying logical graph.

---

## 9. Profile Examples

### 9.1 File Format Profile

```aeon
aeon:header = {
  profile = "startup.sonograph.format.v1"
  mode    = "strict"
}

sonograph = {
  id = "sg-2025-12-12-001"
  source = { encoding = "wav", sampleRate:int32 = 48000 }
  grid = { width:int32 = 1024, height:int32 = 512 }
}
```

### 9.2 API Transport Profile

```aeon
aeon:profile = "startup.sonograph.api.v1"

convertRequest = {
  requestId = "req-123"
  encoding = "wav"
  audio:base64 = $UklGRu4AAA...
}
```

### 9.3 Config Overlay Profile

```aeon
aeon:header = { profile = "service.config.v1", mode = "strict" }

base = { db = { url = "postgres://prod", pool = 20 } }
overrides = { db = { url = "postgres://dev" } }
effective = ~>base
```

---

## 10. Exactly One Profile

AEON accepts exactly one active profile per document.
- Profile composition must be resolved internally
- AEON itself MUST NOT evaluate multiple profiles simultaneously
- Runtime/processor selection policy remains authoritative under the zero-trust model in §2.1.

---

*End of Profiles Framework*
