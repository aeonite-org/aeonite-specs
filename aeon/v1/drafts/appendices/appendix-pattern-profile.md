---
id: appendix-pattern-profile-v1
title: Appendix - AEOS Pattern Profile v1
description: Pattern-oriented profile semantics and deterministic pattern evaluation guidance.
family: appendices-v1
group: AEOS and Profiles
path: specification/appendices/appendix-pattern-profile-v1
---

# AEOS Pattern Profile v1

**Status:** implementation-ahead appendix for consolidated v1

Canonical topic owners: `../AEOS-spec-v1.md`, `../contracts/`

This appendix describes a pattern DSL that is ahead of the currently locked AEOS v1 baseline.
It is informative for future work and must not be treated as required for AEON Core v1 or the shipped AEOS v1 baseline.

## 1. Scope and purpose

AEOS Pattern Profile v1 defines a **form-only** constraint language for validating `StringLiteral` values emitted by AEON Core.

Goals:

* deterministic cross-language behavior (Go/Rust/TS)
* explicit, auditable constraints (no opaque regex)
* stable CTS semantics
* strict separation between **form** (AEOS) and **meaning** (processors)

---

## 2. Applicability

Patterns in this profile MAY be applied only to the decoded string value of a `StringLiteral` emitted by AEON Core.

If a pattern is applied to any non-`StringLiteral` value, the validator MUST emit:

* `code = "constraint_inapplicable"`
* `phase = "schema_validation"`
* `path = <data rule path>`
* `span = <data value span>`

---

## 3. Canonical syntax requirements

### 3.1 Explicit assignment only

All normative structures MUST use explicit AEON assignment syntax:

* ✅ `key = { ... }`
* ✅ `key = "value"`
* ✅ `key = 123`
* ❌ container shorthand MUST NOT be used in normative examples

### 3.2 Pattern Object

A **Pattern Object** has the form:

```aeon
pattern = { <node-type> = <node-object> }
```

Rules:

* `pattern` MUST be an object.
* `pattern` MUST contain **exactly one** node-type key.
* If `pattern` contains zero or more than one node-type key:

  * schema error `code = "invalid_pattern_shape"`

> **Normative clarification:**
> A `pattern = { … }` wrapper is required only at pattern *definition* boundaries (e.g., in `schema.patterns`).
> Nested pattern composition uses **Node Objects directly** (e.g., inside `all`, `any`, `apply`, `each`) and MUST NOT use `pattern = {}` again.

---

## 4. Node types (v1)

Defined node-type keys:

* `all`
* `any`
* `not`
* `pred`
* `split`
* `labels`

Unknown node-type key:

* schema error `code = "unknown_pattern_node"`

---

## 5. Node definitions

## 5.1 Common rule: “Node Object” (for clauses)

A **Node Object** is an object that contains **exactly one** node-type key (from §4), for example:

```aeon
{ pred = { contains = "@" } }
{ not  = { pred = { contains = ".." } } }
{ split = { sep = "@"; exact_parts = 2 } }
```

If a Node Object contains zero or more than one node-type key:

* schema error `code = "invalid_node_object_shape"`

This rule is used for:

* clauses under `all`/`any`
* the wrapped node under `not`
* nested nodes inside `apply` / `each`

---

## 5.2 `all`

### Shape

```aeon
pattern = {
  all = {
    c1 = { pred = { no_whitespace = true } }
    c2 = { not  = { pred = { contains = ".." } } }
    c3 = { split = { ... } }
  }
}
```

Rules:

* `all` MUST be an object.
* `all` MUST contain **one or more** entries.
* Each entry value MUST be a **Node Object** (see §5.1).

Invalid:

* schema error `code = "invalid_all_clause_shape"`

### Semantics

* Evaluate entries in **lexical order as written in AEON source**.
* `all` passes iff all clauses pass.
* MAY short-circuit on first failure.

---

## 5.3 `any`

### Shape

```aeon
pattern = {
  any = {
    o1 = { pred = { starts_with = "Mr " } }
    o2 = { pred = { starts_with = "Ms " } }
  }
}
```

Rules:

* `any` MUST be an object.
* `any` MUST contain **one or more** entries.
* Each entry value MUST be a Node Object.

Invalid:

* schema error `code = "invalid_any_clause_shape"`

### Semantics

* Evaluate in lexical order.
* `any` passes iff at least one clause passes.
* MAY short-circuit on first success.

---

## 5.4 `not` (unary)

### Shape

```aeon
pattern = {
  not = {
    pred = { contains = ".." }
  }
}
```

Rules:

* `not` MUST be an object.
* `not` MUST itself be a **Node Object** (i.e. contain exactly one node-type key).

  * This means `not` wraps exactly one node.

Invalid:

* schema error `code = "invalid_not_shape"`

### Semantics

* Evaluate the wrapped node.
* `not` passes iff the wrapped node fails.

---

## 5.5 `pred` (primitive predicates)

### Shape

```aeon
pattern = {
  pred = { <predicate-kind> = <predicate-value> }
}
```

Rules:

* `pred` MUST be an object.
* `pred` MUST contain **exactly one** predicate-kind key.
* Unknown predicate-kind:

  * schema error `code = "unknown_predicate_kind"`

### Predicate kinds (v1)

#### 5.5.1 `length`

```aeon
pattern = {
  pred = { length = { min = 1; max = 64 } }
}
```

Rules:

* value MUST be an object.
* `min` and `max` optional.
* if present, MUST be non-negative integers.
* if both present, MUST satisfy `min <= max`.

Invalid:

* schema error `code = "invalid_length_predicate"`

Semantics:

* length measured in **Unicode code points** (decoded string, no normalization).
  Fail on data:
* runtime code `length_violation`

#### 5.5.2 `contains`

```aeon
pattern = { pred = { contains = "@" } }
```

Rules:

* value MUST be a string.

Invalid:

* schema error `invalid_contains_predicate`

Fail on data:

* runtime code `predicate_violation`

#### 5.5.3 `starts_with`

```aeon
pattern = { pred = { starts_with = "." } }
```

Rules:

* value MUST be a string.

Invalid:

* schema error `invalid_starts_with_predicate`

Fail on data:

* runtime code `predicate_violation`

#### 5.5.4 `ends_with`

```aeon
pattern = { pred = { ends_with = "." } }
```

Rules:

* value MUST be a string.

Invalid:

* schema error `invalid_ends_with_predicate`

Fail on data:

* runtime code `predicate_violation`

#### 5.5.5 `no_whitespace`

```aeon
pattern = { pred = { no_whitespace = true } }
```

Rules:

* value MUST be boolean.

Invalid:

* schema error `invalid_no_whitespace_predicate`

Semantics (v1 whitespace set):

* forbidden code points are exactly:

  * U+0009 TAB
  * U+000A LF
  * U+000D CR
  * U+0020 SPACE

Fail on data:

* runtime code `whitespace_forbidden`

#### 5.5.6 `charset`

```aeon
pattern = { pred = { charset = "dns_label" } }
```

Rules:

* value MUST be a string naming a charset in the registry (see §6).

Invalid:

* schema error `unknown_charset`

Fail on data:

* runtime code `charset_violation`

---

## 5.6 `split` (index-safe REQUIRED)

### Shape (REQUIRED)

```aeon
pattern = {
  split = {
    sep = "@"
    exact_parts = 2

    parts = {
      p0 = { name = "local";  apply = { all = { ... } } }
      p1 = { name = "domain"; apply = { all = { ... } } }
    }
  }
}
```

Rules:

* `split` MUST be an object.
* `sep` MUST be a non-empty string.
* `exact_parts` optional; if present MUST be a positive integer.
* `parts` optional; if present MUST be an object.
* If `parts` is present:

  * keys MUST be exactly `p0..pN` (dense, zero-based, no gaps)
  * each `pK` MUST be an object containing:

    * optional `name` (string; documentation only)
    * required `apply` which MUST be a **Node Object** (see §5.1)

Invalid:

* `invalid_split_shape`
* `invalid_split_parts_indexing`
* `invalid_split_part_apply_shape`

### Semantics

* Split input string on literal `sep`.
* If `exact_parts` present and part count differs: fail

  * runtime code `split_exact_parts_mismatch`
* If `parts` present: apply each `pK.apply` to the Kth part string.
* Any failing part fails `split`.

Note:

* `apply` is a Node Object, so you can use `all`, `pred`, `labels`, etc. directly.

---

## 5.7 `labels`

### Shape

```aeon
pattern = {
  labels = {
    sep = "."
    min_parts = 2
    each = { all = { ... } }
  }
}
```

Rules:

* `labels` MUST be an object.
* `sep` MUST be a non-empty string.
* `min_parts` optional; if present MUST be a positive integer.
* `each` MUST be a Node Object.

Invalid:

* schema error `invalid_labels_shape`

### Semantics

* Split on literal `sep`.
* If `min_parts` present and count < min_parts: fail

  * runtime code `labels_min_parts_violation`
* Apply `each` to every part string.
* If any part fails, `labels` fails.

---

## 6. Charset registry (v1 ASCII-only)

This profile permits named charsets referenced by `pred.charset`.

### Charset definition shape (v1)

```aeon
charsets = {
  dns_label = {
    ascii_ranges = {
      r1 = { from = "a"; to = "z" }
      r2 = { from = "A"; to = "Z" }
      r3 = { from = "0"; to = "9" }
    }
    literals = {
      l1 = "-"
    }
  }
}
```

Rules:

* `charsets` is a registry object defined by the AEOS Schema Profile (location not specified here).
* `ascii_ranges` optional; if present MUST be an object of ranges.

  * each range MUST have `from` and `to` as single ASCII characters.
* `literals` optional; if present MUST be an object whose values are single ASCII characters.
* Any non-ASCII character in v1 charset definitions is invalid:

  * schema error `invalid_charset_definition`

---

## 7. Error reporting and codes

### 7.1 Runtime pattern failures (data validation)

When a pattern fails on data, emit an error with:

* `path` = rule path being validated
* `span` = span of the data `StringLiteral`
* `phase` = `"schema_validation"`
* `code` = appropriate runtime code

Minimum runtime codes:

* `pattern_mismatch` // fallback
* `length_violation`
* `predicate_violation`
* `whitespace_forbidden`
* `charset_violation`
* `split_exact_parts_mismatch`
* `labels_min_parts_violation`
* `constraint_inapplicable`

### 7.2 Schema-shape failures (schema validation)

Invalid pattern/schema structures MUST be reported as schema errors (same envelope), using:

* `invalid_pattern_shape`
* `unknown_pattern_node`
* `invalid_node_object_shape`
* `invalid_all_clause_shape`
* `invalid_any_clause_shape`
* `invalid_not_shape`
* `invalid_split_shape`
* `invalid_split_parts_indexing`
* `invalid_split_part_apply_shape`
* `invalid_labels_shape`
* `unknown_predicate_kind`
* `invalid_length_predicate`
* `invalid_contains_predicate`
* `invalid_starts_with_predicate`
* `invalid_ends_with_predicate`
* `invalid_no_whitespace_predicate`
* `unknown_charset`
* `invalid_charset_definition`

Implementation-specific schema codes MUST use vendor prefix:

* `vendor:code_name`

---

## 8. Determinism and prohibitions

### 8.1 Ordering

Evaluation order MUST be lexical order in the AEON source for:

* entries under `all`
* entries under `any`
* `split.parts` via `p0..pN`

### 8.2 Full-match model

This pattern system is a full-string validation model. Substring intent must be explicit via predicates (`contains`, etc.). There is no implicit substring search operator.

### 8.3 Anti semantic creep

Validators MUST NOT use this pattern system to claim real-world semantic validity:

* no RFC-complete email validity
* no calendar correctness for date-like strings
* no DNS lookups
* no reference resolution for validation
* no coercion/normalization

---

## 9. Canonical example (email-shaped, form-only)

```aeon
email_shape_v1 = {
  pattern = {
    all = {

      c1 = { pred = { no_whitespace = true } }

      c2 = {
        split = {
          sep = "@"
          exact_parts = 2

          parts = {
            p0 = {
              name = "local"
              apply = {
                all = {
                  l1 = { pred = { length = { min = 1; max = 64 } } }
                  l2 = { not  = { pred = { starts_with = "." } } }
                  l3 = { not  = { pred = { ends_with   = "." } } }
                  l4 = { not  = { pred = { contains    = ".." } } }
                  l5 = { pred = { charset = "ascii_email_local_safe" } }
                }
              }
            }

            p1 = {
              name = "domain"
              apply = {
                all = {
                  d1 = { pred = { length = { min = 1; max = 253 } } }
                  d2 = { pred = { contains = "." } }

                  d3 = {
                    labels = {
                      sep = "."
                      min_parts = 2
                      each = {
                        all = {
                          x1 = { pred = { length = { min = 1; max = 63 } } }
                          x2 = { not  = { pred = { starts_with = "-" } } }
                          x3 = { not  = { pred = { ends_with   = "-" } } }
                          x4 = { pred = { charset = "dns_label" } }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```
