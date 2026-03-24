---
id: appendix-spans-v1
title: Appendix - Spans
description: Source span representation and diagnostic location semantics.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-spans-v1
---

# Appendix — Spans

Status: informative summary for consolidated v1

Canonical topic owners: `../AEOS-spec-v1.md`, `../comments-annotations-v1.md`

If this appendix conflicts with the canonical v1 spec set, the canonical v1 spec set wins.

## 1. Definition

A span identifies a source range in the original AEON text.

```ts
span: [start, end]
```

- `start` is inclusive
- `end` is exclusive
- offsets are document-level offsets emitted by AEON Core

## 2. Purpose

Spans provide deterministic source linkage for:
- diagnostics
- auditing
- tooling/editor highlighting

Spans are metadata and do not change AEON semantics.

## 3. Authority

- Spans are produced by AEON Core.
- Validators and downstream processors propagate spans.
- Validators must not invent replacement spans for existing source-backed values.

## 4. Required Output Behavior

For AEOS/CTS-style diagnostics:
- diagnostics should include a span when the target source region exists
- `span: null` is allowed only when no source region exists (for example missing required path)

## 5. Targeting Rule

A span should identify the narrowest source fragment responsible for the diagnostic (for example the offending literal or reference token).

## 6. Non-Goals

Spans are not:
- semantic values
- canonical paths
- line/column replacements

## 7. Determinism

Given identical source and policy, diagnostics should carry stable spans.

## 8. Implementation Note

Current TypeScript implementation emits token positions with line/column plus offset in lexer tokens. Consumers relying on spans should treat AEON Core output as authoritative for unit/offset interpretation.
