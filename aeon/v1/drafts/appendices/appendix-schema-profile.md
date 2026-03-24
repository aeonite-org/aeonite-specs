---
id: appendix-schema-profile-v1
title: Appendix - AEOS Schema Profile v1
description: Schema profile constraints, rule application semantics, and compatibility expectations.
family: appendices-v1
group: AEOS and Profiles
path: specification/appendices/appendix-schema-profile-v1
---

# AEOS Schema Profile v1

**Status:** implementation-ahead appendix for consolidated v1

Canonical topic owners: `../AEOS-spec-v1.md`, `../contracts/`

This appendix describes a broader schema/profile model than the currently locked AEOS v1 baseline.
It is informative for future work and must not override the shipped AEOS v1 contract surface.

## 1. Scope and purpose

AEOS Schema Profile v1 defines the **structure and interpretation of AEON documents used as schemas** for AEOS validation.

It specifies:

* where schemas store **rules**, **patterns**, and **charsets**
* how rules bind **data paths** to **constraints**
* what kinds of references are allowed (and forbidden)
* strict separation between **schema validation** and **data validation**

This profile does **not** define pattern semantics — those are defined by **AEOS Pattern Profile v1**.

---

## 2. Fundamental model

AEOS validates **data AES** against **schema AES**.

```
data.aeon   → AEON Core → AES_data
schema.aeon → AEON Core → AES_schema

AES_schema + AES_data → AEOS → Result Envelope
```

AEOS NEVER:

* mutates either AES
* resolves data references
* coerces values
* interprets semantics beyond form

---

## 3. Schema document top-level shape

A Schema Profile v1 document MUST be an AEON object with the following optional top-level sections:

```aeon
schema = {
  rules     = { ... }   // REQUIRED
  patterns  = { ... }   // OPTIONAL
  charsets  = { ... }   // OPTIONAL
}
```

Rules:

* `schema` MUST be present.
* `schema.rules` MUST be present.
* Any unknown top-level key under `schema` is invalid:

  * `code = "invalid_schema_key"`

---

## 4. Rules section

### 4.1 Purpose

`schema.rules` binds **data paths** to **constraints**.

Each rule applies independently; rule order has no semantic meaning.

---

### 4.2 Shape

```aeon
rules = {
  $.user.email = {
    type = StringLiteral
    apply_pattern = "email"
  }

  $.server.port = {
    type = IntegerLiteral
  }
}
```

Rules:

* `rules` MUST be an object.
* Each key MUST be a **canonical AEON path**.
* Each value MUST be a **Rule Object**.

Invalid:

* `code = "invalid_rule_shape"`

---

### 4.3 Rule Object

A Rule Object MAY contain the following keys:

| Key             | Required | Meaning                    |
| --------------- | -------- | -------------------------- |
| `type`          | YES      | Required literal kind      |
| `apply_pattern` | NO       | Pattern reference (string) |

Any other key is invalid:

* `code = "invalid_rule_key"`

---

### 4.4 `type` constraint

```aeon
type = StringLiteral
```

Rules:

* `type` MUST be a literal-kind identifier.
* v1 supported kinds:

  * `StringLiteral`
  * `IntegerLiteral`
  * `FloatLiteral`
  * `BooleanLiteral`
  * `Reference`

Semantics:

* AEOS checks only the **literal kind** emitted by AEON Core.
* No coercion is allowed.

Failure:

* runtime `code = "type_mismatch"`

---

### 4.5 `apply_pattern`

```aeon
apply_pattern = "email"
```

Rules:

* Value MUST be a string.
* The string MUST refer to a key in `schema.patterns`.

Invalid:

* `code = "unknown_pattern"`

Semantics:

* The referenced pattern is applied **after** type checking.
* The pattern MUST conform to **Pattern Profile v1**.
* The pattern is applied to the decoded string value.

---

## 5. Patterns section

### 5.1 Purpose

`schema.patterns` is a **library of reusable pattern definitions**.

Patterns are **pure schema objects**, not applied directly to data without a rule.

---

### 5.2 Shape

```aeon
patterns = {
  email = { pattern = { ... } }
  slug  = { pattern = { ... } }
}
```

Rules:

* `patterns` MUST be an object.
* Each value MUST contain a **Pattern Object** as defined in Pattern Profile v1.
* Keys MUST be unique identifiers.

Invalid:

* `code = "invalid_pattern_definition"`

---

### 5.3 Pattern references

Pattern references:

* are resolved **within the schema only**
* MUST NOT reference data paths
* MUST NOT be recursive (directly or indirectly)

Recursive reference:

* `code = "recursive_pattern_reference"`

---

## 6. Charsets section

### 6.1 Purpose

`schema.charsets` defines named character sets used by `pred.charset`.

---

### 6.2 Shape

```aeon
charsets = {
  dns_label = { ... }
}
```

Rules:

* `charsets` MUST be an object.
* Charset definitions MUST conform to **Pattern Profile v1 §6**.

Invalid:

* `code = "invalid_charset_definition"`

---

## 7. Validation order (critical)

AEOS MUST apply constraints in the following strict order **per rule**:

1. **Presence check**

   * If a rule exists for a path and the path is missing in data:

     * runtime `code = "missing_required_field"`
     * (v1: all rules are implicitly required)

2. **Type check**

   * Validate literal kind against `type`
   * On failure: STOP rule evaluation

3. **Pattern check** (if present)

   * Apply referenced pattern
   * On failure: STOP rule evaluation

> **Normative clarification:**
> Patterns are **never evaluated** if the path is missing in data. A missing path fails at step 1 (presence check) before pattern evaluation is considered.

There is NO fallback, coercion, or continuation.

---

## 8. Reference handling (hard boundary)

### 8.1 Data references

If the data value at a rule path is a `Reference`:

* Type checking applies to the **Reference literal itself**
* Patterns MUST NOT be applied to `Reference`

Violation:

* runtime `code = "constraint_inapplicable"`

AEOS MUST NOT:

* resolve references
* peek at referenced values

---

### 8.2 Schema references

Schema-internal references are allowed only for:

* `apply_pattern`
* charset lookup

They are resolved **once at schema load time**, not per validation.

---

## 9. Error reporting

All rule failures MUST emit errors with:

* `path` = data path being validated
* `span` = span of the data literal (if available)
* `phase` = `"schema_validation"`
* `code` = appropriate code

If multiple rules fail, AEOS MUST report **all failures** (no short-circuit across rules).

---

## 10. Prohibitions (explicit)

AEOS Schema Profile v1 explicitly forbids:

* default value injection
* value coercion
* reference resolution
* semantic validation (RFCs, calendars, etc.)
* schema-driven mutation of data
* schema rules depending on other rules’ results

Violation of these principles breaks conformance.

---

## 11. Conformance checklist

A conforming AEOS Schema Profile v1 implementation MUST:

* [ ] Reject unknown keys in `schema`
* [ ] Enforce canonical path keys in `rules`
* [ ] Enforce literal-kind-only `type` checks
* [ ] Apply patterns only after successful type check
* [ ] Resolve patterns only within schema scope
* [ ] Reject recursive pattern references
* [ ] Never mutate data AES or schema AES
* [ ] Emit spans from data AES in all rule failures
* [ ] Preserve phase ordering and fail-closed semantics

---

## 12. Minimal complete example

```aeon
schema = {

  charsets = {
    dns_label = {
      ascii_ranges = {
        r1 = { from = "a"; to = "z" }
        r2 = { from = "A"; to = "Z" }
        r3 = { from = "0"; to = "9" }
      }
      literals = { l1 = "-" }
    }
  }

  patterns = {
    email = ~$.email_shape_v1
  }

  rules = {
    $.user.email = {
      type = StringLiteral
      apply_pattern = "email"
    }
  }
}
```

---
