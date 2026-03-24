---
id: appendix-annotation-stream-v1
title: Appendix - Annotation Stream
description: Structured annotation channel model and source-order emission behavior.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-annotation-stream-v1
---

# Appendix — Annotation Stream

Status: informative summary for consolidated v1

Canonical topic owner: `../comments-annotations-v1.md`

If this appendix conflicts with the canonical comments/annotations reference, the canonical comments/annotations reference wins.

## 1. Channel Forms

Structured channels:

- line: `//#`, `//@`, `//?`, `//{`, `//[`, `//(`
- block: `/# ... #/`, `/@ ... @/`, `/? ... ?/`, `/{ ... }/`, `/[ ... ]/`, `/( ... )/`

Plain comments:

- line: `// ...`
- block: `/* ... */`

## 2. Deterministic Binding Continuity

Binding target preference remains:

- `path` -> `span` -> `unbound`

Indexed element preference behavior for container comments remains deterministic and CTS-enforced.

## 3. Non-influence Rule

Comments/annotations/hints MUST NOT alter:

- AES semantics
- canonical path assignment
- reference legality
- assignment ordering

## 4. Optional Annotation Emission in Compile Surface

For non-tooling pipelines, compile implementations may allow annotation emission to be disabled.

Normative expectations:

- When disabled, annotation stream output is omitted.
- Parse/resolve/mode/reference behavior remains identical.
- Event ordering and canonical paths remain unchanged.

Tooling/lint/editor flows should keep annotation emission enabled.
