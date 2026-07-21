---
id: appendix-error-model-v1
title: Appendix - Error Model
description: "Error code shape, failure classes, and deterministic diagnostic reporting conventions."
family: appendices-v1
group: Core Semantics
status: informative summary for consolidated v1
license: CC-BY-4.0
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
| `EVENT_COUNT_EXCEEDED`         | PolicyError | core validation          | emitted AES event count exceeds active `max_events`                              |
| `INVALID_SEPARATOR_CHAR`       | SyntaxError | parse                    | forbidden or malformed separator char in separator spec                          |
| `INVALID_ESCAPE`               | SyntaxError | lex/parse                | malformed quoted escape, malformed Unicode escape, lone surrogate, or out-of-range code point |
| `UNTERMINATED_STRING`          | SyntaxError | lex                      | quoted string crosses a raw newline or EOF before closing delimiter              |
| `UNTYPED_TOGGLE_LITERAL`       | ModeError   | mode enforcement         | strict toggle literal not typed as `toggle`                                      |
| `UNTYPED_VALUE_IN_STRICT_MODE` | ModeError   | mode enforcement         | strict-mode value lacks required typing                                          |

AEOS validation diagnostics use lowercase snake case:

| Code                           | Category            | Phase                        | Trigger                                                                      |
| ------------------------------ | ------------------- | ---------------------------- | ---------------------------------------------------------------------------- |
| `trailing_separator_delimiter` | PolicyWarning/Error | schema validation (optional) | optional AEOS policy: separator literal payload ends with declared separator |

Reference implementation policy surfaces:

- Runtime option: `trailingSeparatorDelimiterPolicy` (`off|warn|error`)
- CLI bind flag: `--trailing-separator-delimiter-policy <off|warn|error>`

## 3. Separator-Literal Boundary Clarification

Separator literals do not define a raw escape layer.
Outside quoted string segments, the payload ends when ordinary grammar or comment syntax resumes, and disallowed raw characters may surface downstream as `SYNTAX_ERROR` depending on token context.
This behavior is deterministic and expected under v1 separator-literal boundary rules.

## 4. Determinism Requirements

Diagnostics MUST:

- fail closed where specified by phase contract
- include stable code and canonical path context when applicable
- be deterministic under identical input and policy settings

For the Unicode and quoted-string boundaries clarified in Core v1:

- malformed quoted escapes SHOULD surface as `INVALID_ESCAPE`;
- malformed Unicode escapes, lone surrogate escapes, and out-of-range code
  points SHOULD surface as `INVALID_ESCAPE`;
- raw newlines inside non-backtick quoted strings SHOULD surface as
  `UNTERMINATED_STRING`.

### 4.1 Undefined-Case Review Guidance

When an implementation encounters an edge case that is not clearly defined by Core, an adopted convention, a profile, or explicit processor policy, the implementation should treat the case as a question of authority before treating it as a question of convenience.

Recommended review questions:

1. What exactly is being represented?
2. What can legitimately be concluded from that representation?
3. Who or what has authority to make that conclusion?

Claims should not be realized as semantic conclusions until a stage with authority realizes their meaning. Examples of authority-bearing stages include a selected convention, validated schema, trusted profile, processor policy, or consuming application policy.

If no authority-bearing stage is selected, implementations should avoid materializing a conclusion. Depending on the active mode and processing surface, the implementation should preserve the claim as opaque data, ignore the unsupported semantic layer, or fail closed with a deterministic diagnostic.

## 5. Portability Warnings

Portability warnings are non-fatal diagnostics. They report valid documents,
schemas, or configured policy values that exceed the minimum portability floors
defined by AEON, SANSA, AEOS, or another layered capability.

Implementations MUST NOT fail validation solely because a portability warning is
present. Tools SHOULD display portability warnings near errors because they
indicate that an artifact accepted by the current implementation may not be
accepted by another conforming implementation with only minimum capability
floors.

Recommended warning-code families:
- `AEON_NON_PORTABLE_*`
- `SANSA_NON_PORTABLE_*`
- `AEOS_NON_PORTABLE_*`

When applicable, portability warnings should include:
- the affected path or selector;
- the observed value;
- the portable floor value;
- the implementation limit or configured budget, if different from the portable
  floor.

## 6. Phase Presentation

Human-facing diagnostics SHOULD present the pipeline phase as a readable label rather than as a bare numeric band.

Recommended plain-text form:

- `<Phase Label>: <message> [CODE] path=$.x span=1:1-1:4`

Example:

- `Reference Validation: Self reference: '$.a' references itself [SELF_REFERENCE] path=$.a span=1:1-1:4`

JSON diagnostics MAY additionally include:

- `phase` when the producing phase is explicitly known
- `phaseLabel` when a stable human-readable phase name is available

When both are present, `code` remains the stable machine-facing identifier and `phaseLabel` is presentation metadata.

## 7. Payload Expectations

When applicable, diagnostics should include:

- offending path/type context
- observed depth
- active policy limit
- source span (if available)

## 8. Reporting Specification Gaps

When an undefined edge case appears to expose a specification gap, report it to the AEON specification authority with enough information for deterministic review.

Reports should include:

- the smallest AEON input that demonstrates the case
- the processing stage where the ambiguity appears
- the active mode, conventions, profiles, schemas, and processor policy
- observed implementation behavior
- the expected or proposed behavior, if known
- whether the issue affects conformance, interoperability, security, or only local implementation behavior

Specification questions belong with `aeonite-org/aeonite-specs`. Conformance-test questions belong with `aeonite-org/aeonite-cts`.
