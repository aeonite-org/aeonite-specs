---
id: aeon-core-v1
title: AEON Specification v1
description: Start here for the overall AEON Core v1 model, scope, behavior modes, and the companion documents that define the rest of the specification surface.
group: Core Specifications
path: specification/aeon-v1-documentation/aeon-specification-v1
links:
  - aeon-core-v1-compliance
  - aeos-v1
  - aeon-core-v1-value-types
  - aeon-core-v1-structure-syntax
  - aeon-core-v1-addressing-references
  - aeon-core-v1-comments-annotations
---

# AEON Specification v1

Status: official v1 overview  
Scope: normative overview of AEON Core v1, its boundaries, and the companion reference set.

## 1. What AEON Is

AEON is a human-readable, typed, semantics-first data notation.

At its core, an AEON document is a sequence of bindings:

```aeon
key@{attributes}:type = value
```

Implementations may accept looser transport forms, but this overview defines the Core v1 model and points to the detailed companion references.

## 2. Smallest Useful Example

```aeon
name:string = "AEON"
build:number = 1
active:switch = on
```

This demonstrates:
- key/value assignment
- explicit datatype annotation
- deterministic literal interpretation

## 3. Document Model

AEON Core v1 is built from a small set of structural ideas:
- bindings
- keys
- values
- attributes
- references
- canonical paths
- comments/annotations

Bindings are separated by newline or comma at document/object level and may contain structured values such as objects, lists, tuples, nodes, and references.

## 4. Core Value Families

Core value families include:
- strings
- numbers
- infinity literals
- booleans
- switches
- hex, radix, and encoding literals
- date, time, datetime, and ZRUT forms
- objects, lists, tuples, and nodes
- clone and alias references
- separator literals

Normative detailed reference:
- `value-types-v1.md`

## 5. Structural Syntax Surface

Core structural syntax includes:
- bare and quoted keys
- attribute blocks
- nested attribute heads
- datatype annotations
- separator specs
- comma/newline element separation rules
- comma/newline binding rules

Quoted keys are part of Core v1 syntax, but empty quoted keys are invalid.

Normative detailed reference:
- `structure-syntax-v1.md`

## 6. Addressing and References

AEON Core v1 provides:
- canonical path identity using root/member/index segments
- quoted-segment disambiguation
- index-based element addressing
- attribute selectors for attribute-namespace traversal
- deterministic reference legality rules

Reference legality is fail-closed:
- forward references are invalid
- missing targets are invalid
- self-references are invalid

Normative detailed reference:
- `addressing-references-v1.md`

## 7. Comments and Annotation Channels

AEON distinguishes:
- plain comments
- structured annotation channels
- reserved structured channels

Comments do not alter parse semantics, path identity, reference legality, or assignment ordering.

Structured comments may attach deterministically to neighboring targets and may be emitted as a separate annotation stream.

Normative detailed reference:
- `comments-annotations-v1.md`

## 8. Behavior Modes and Datatype Policy

AEON Core v1 defines three behavior modes:

- `transport`
- `strict`
- `custom`

Core v1 behavior is:
- `transport` may omit datatype annotations and accepts custom datatype labels
- `strict` requires datatype presence and accepts only the reserved Core datatype surface by default
- `custom` requires datatype presence and accepts custom datatype labels
- explicit datatype annotations are validated in all modes

Implementations MAY still expose an explicit datatype-policy override as an implementation control, but the default semantic behavior is mode-driven.

Authoritative compliance requirements and behavioral floors are defined in:
- `AEON-v1-compliance.md`

## 9. Deterministic Policy Knobs

Core v1 requires deterministic depth-policy controls for:
- `max_attribute_depth`
- `max_separator_depth`
- `max_generic_depth`

Reference implementation defaults lock these to `1`, while conforming implementations must support a capability floor of at least `8`.

## 10. Phase Boundaries

AEON Core is responsible for:
- lexical analysis
- parsing
- canonical path assignment
- reference legality
- annotation-stream extraction when enabled

Core does not define downstream application semantics such as:
- domain validation meaning
- profile-specific projection decisions
- schema/business-rule interpretation

AEOS/schema/profile layers build on top of Core rather than redefining it.

Document-declared conventions, profiles, and schemas are advisory until selected or trusted by the consumer/processor. They do not self-activate.

The standard GP security envelope, when used, is convention-driven.
It is represented as a normal top-level object binding typed as `:envelope` rather than a Core-special key:
- `aeon.gp.security.v1` defines the envelope structure
- `aeon.gp.integrity.v1` defines canonical integrity hashing
- `aeon.gp.signature.v1` defines signature representation
- `aeon.gp.encryption.v1` defines encryption metadata representation

Header placement is part of Core syntax:
- shorthand header bindings (`aeon:mode`, `aeon:profile`, `aeon:schema`, `aeon:version`, etc.) form the document header only when they appear in the initial header block at the start of the document;
- a structured header (`aeon:header = { ... }`) MUST appear before any body binding;
- a structured header that appears after any body binding is invalid.

## 11. Conformance Surface

Normative conformance requirements are defined in:
- `AEON-v1-compliance.md`
- `AEOS-spec-v1.md`
- `conformance-matrix.md`

CTS protocol and lane baselines:
- `cts/protocol/v1`
- `cts/core/v1`
- `cts/aes/v1`
- `cts/annotations/v1`
- `cts/aeos/v1`

Core conformance should be reviewed by backbone behavior family, not only by individual suite file.

Current v1 backbone families are:
- canonical rendering and node normalization
- fail-closed parsing and deterministic rejection behavior
- addressing and canonical path semantics
- quoted-key and traversal disambiguation
- attribute traversal and attribute-depth semantics
- annotation attachment and slash-channel binding
- strict literal acceptance and rejection boundaries
- separator/path literal handling
- datatype-to-literal validation behavior

The anti-drift coverage state for those families is tracked in `aeonite-cts/CONFORMANCE-COVERAGE.md`.

## 12. Contracts

Canonical baseline v1 contracts are provided in:
- `contracts/registry.json`
- `contracts/profiles/aeon.gp.profile.v1.aeon`
- `contracts/schemas/aeon.gp.schema.v1.aeon`

These contracts are authoritative artifacts for the baseline general-purpose profile/schema set.
They are official baseline contracts, not implicit defaults when no trusted profile/schema is selected.

## 13. Companion Reference Set

The official v1 documentation is intentionally split by concern:
- `AEON-spec-v1.md` — overview and boundaries
- `AEON-v1-compliance.md` — mandatory conformance requirements
- `AEOS-spec-v1.md` — AEOS validation layer
- `value-types-v1.md` — value families and literal forms
- `structure-syntax-v1.md` — keys, attributes, separators, newline behavior
- `addressing-references-v1.md` — canonical paths and reference rules
- `comments-annotations-v1.md` — comment channels and attachment behavior
- `appendices/appendix-directive-block-capabilities.md` — informative v1 reservation for capability-based evolution

This overview should stay short and stable. Detailed syntax, examples, and edge-case rules belong in the companion references.

## 14. Anti-Drift Requirement

AEON Core conformance is not satisfied by passing a small representative sample.

A conforming implementation must preserve behavior across the Core backbone families named above and their corresponding CTS lanes, especially:
- canonical output and normalization behavior
- fail-closed invalid syntax handling
- canonical path identity and quoted-key disambiguation
- reference legality and attribute traversal behavior
- annotation attachment behavior
- strict literal acceptance and rejection boundaries

Behavior must remain stable across implementations so the canonical backbone of the format does not fragment.
