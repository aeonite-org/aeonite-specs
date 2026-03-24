---
id: appendix-error-model-v1
title: Appendix - Error Model
description: Error code shape, failure classes, and deterministic diagnostic reporting conventions.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-error-model-v1
---

# Appendix — Error Model

Status: informative summary for consolidated v1

Canonical topic owners: `../AEON-v1-compliance.md`, `../AEOS-spec-v1.md`

If this appendix conflicts with the canonical compliance or AEOS spec, those canonical documents win.

## 1. Existing Diagnostics

Existing prior-release diagnostics remain valid unless superseded in v1.

## 2. v1 Policy/Behavior Diagnostics (active)

Core/policy diagnostics retained from prior v1-era behavior summaries use legacy uppercase-style codes:

| Code                           | Category    | Phase                    | Trigger                                                                          |
| ------------------------------ | ----------- | ------------------------ | -------------------------------------------------------------------------------- |
| `ATTRIBUTE_DEPTH_EXCEEDED`     | PolicyError | policy enforcement       | address-expression attribute selector depth exceeds active `max_attribute_depth` |
| `SEPARATOR_DEPTH_EXCEEDED`     | PolicyError | parse/policy enforcement | separator-spec depth exceeds active `max_separator_depth`                        |
| `GENERIC_DEPTH_EXCEEDED`       | PolicyError | parse/policy enforcement | nested generic type depth exceeds active `max_generic_depth`                     |
| `INVALID_SEPARATOR_CHAR`       | SyntaxError | parse                    | forbidden or malformed separator char in separator spec                          |
| `UNTYPED_SWITCH_LITERAL`       | ModeError   | mode enforcement         | strict switch literal not typed as `switch`                                      |
| `UNTYPED_VALUE_IN_STRICT_MODE` | ModeError   | mode enforcement         | strict-mode value lacks required typing                                          |

AEOS validation diagnostics use lowercase snake case:

| Code                           | Category            | Phase                        | Trigger                                                                      |
| ------------------------------ | ------------------- | ---------------------------- | ---------------------------------------------------------------------------- |
| `trailing_separator_delimiter` | PolicyWarning/Error | schema validation (optional) | optional AEOS policy: separator literal payload ends with declared separator |

Reference implementation policy surfaces:

- Runtime option: `trailingSeparatorDelimiterPolicy` (`off|warn|error`)
- CLI bind flag: `--trailing-separator-delimiter-policy <off|warn|error>`

## 3. Separator-Literal Boundary Clarification

When a raw separator literal crosses an enclosing grammar boundary without the required escaping, downstream parse errors may surface as `SYNTAX_ERROR` depending on token context.
This behavior is deterministic and expected under v1 separator-literal boundary rules.

## 4. Determinism Requirements

Diagnostics MUST:

- fail closed where specified by phase contract
- include stable code and canonical path context when applicable
- be deterministic under identical input and policy settings

## 5. Phase Presentation

Human-facing diagnostics SHOULD present the pipeline phase as a readable label rather than as a bare numeric band.

Recommended plain-text form:

- `<Phase Label>: <message> [CODE] path=$.x span=1:1-1:4`

Example:

- `Reference Validation: Self reference: '$.a' references itself [SELF_REFERENCE] path=$.a span=1:1-1:4`

JSON diagnostics MAY additionally include:

- `phase` when the producing phase is explicitly known
- `phaseLabel` when a stable human-readable phase name is available

When both are present, `code` remains the stable machine-facing identifier and `phaseLabel` is presentation metadata.

## 6. Payload Expectations

When applicable, diagnostics should include:

- offending path/type context
- observed depth
- active policy limit
- source span (if available)
