---
id: appendix-directive-block-capabilities-v1
title: Appendix - Directive Block and Capability Declaration
description: Informative v1 reservation for directive-block based capability evolution and future v2 activation.
family: appendices-v1
group: Evolution
path: specification/appendices/appendix-directive-block-capabilities-v1
---

# Appendix - Directive Block and Capability Declaration

Status: informative v1 reservation; candidate normative activation in v2 or later.

This appendix records a forward-compatibility strategy for evolving AEON through declared capabilities rather than a single global language version.

In AEON Core v1, this proposal does not change parsing requirements. The only operational file-header host directive defined by v1 is the existing `//! format:<id>` preflight signal described in `comments-annotations-v1.md`.

## 1. Overview

A future AEON line may define a directive block at the start of a document to declare:

- document format
- required capabilities
- optional features
- semantic comment-channel profile bindings

The directive block is reserved in v1 and may become operational in v2 or later.

## 2. Design Goals

- preserve fail-closed deterministic parsing
- avoid global version locks
- enable capability-based evolution
- prevent silent misinterpretation
- keep Core neutral and minimal
- avoid Postel-style tolerance creep

## 3. Candidate Syntax

Directive lines use a strict form with either no spacer or exactly one ASCII space after `//!`:

```aeon
//! key:value
```

```aeon
//!key:value
```

For the candidate future block grammar, no other whitespace or alternative separators are permitted in directive lines.

In v1, only `//! format:<id>` has defined preflight meaning, and only in the file-header slot. Other `//! key:value` spellings are comments unless and until a future directive-aware processing mode is explicitly selected.

### 3.1 Candidate Grammar Sketch

```ebnf
Document        ::= Shebang? DirectiveBlock? Body

Shebang         ::= "#!" <any characters except newline> Newline

DirectiveBlock  ::= DirectiveLine+ BlankLine

DirectiveLine   ::= "//! " DirectiveKey ":" DirectiveValue Newline
                 |  "//!" DirectiveKey ":" DirectiveValue Newline

DirectiveKey    ::= Identifier ("." Identifier)*

Identifier      ::= [a-zA-Z] [a-zA-Z0-9_-]*

DirectiveValue  ::= [^\r\n]+

BlankLine       ::= Newline | Whitespace Newline

Body            ::= <normal AEON source>
```

This grammar is a future directive-aware preflight grammar. It must not change how AEON Core parses the document body.

## 4. Candidate Block Shape

```text
[optional shebang]
[optional format directive]
[zero or more directives]
[blank line]
[AEON document body]
```

Example:

```aeon
#!/usr/bin/env aeon
//! format:sound.app
//! require:aeon.tuple.v2
//! feature:aeon.locale.v1
//! comment.doc:&ND.v1
//! comment.hint:aeon.schema-hint.v1
//! comment.annotation:aeon.annotation.v1

invoice = {
  subtotal = 100
}
```

Also valid:

```aeon
//! format:sound.app

data = {}
```

Not a directive block:

```aeon
data = {}
//! require:aeon.tuple.v2
```

The final line above is an ordinary comment because it appears after the document body has begun.

## 5. Candidate Block Termination

A future directive-aware processor should treat the directive block as ending at the first blank line.

After that termination point, `//!` lines are ordinary comments and have no directive meaning.

## 6. Core Candidate Directives

### 6.1 `format`

```aeon
//! format:sound.app
```

Candidate rules:

- must be the first directive
- may appear after a shebang
- only one allowed
- may be inspected without full directive opt-in

Purpose: identify the document's intended processing domain.

v1 compatibility note: this matches the existing `//! format:<id>` preflight slot, except v1 does not define a multi-line directive block around it.

### 6.2 `require`

```aeon
//! require:aeon.tuple.v2
```

Meaning: the document cannot be safely processed without this capability.

Candidate rules:

- multiple allowed
- unknown capability fails closed
- unsupported capability fails closed
- intended for grammar changes, parsing changes, or compatibility-breaking semantics

### 6.3 `feature`

```aeon
//! feature:aeon.locale.v1
```

Meaning: optional capability that may enhance processing.

Candidate rules:

- multiple allowed
- unknown capability may be ignored
- unsupported capability may be ignored
- must not be required for safe parsing

### 6.4 `comment.*`

```aeon
//! comment.doc:&ND.v1
//! comment.hint:aeon.schema-hint.v1
//! comment.annotation:aeon.annotation.v1
//! comment.structure:app.sound.v1
//! comment.process:app.template.v1
//! comment.instruction:llm.sound.v1
```

Meaning: declare interpretation profiles for semantic comment channels.

Candidate rules:

- optional
- one declaration per comment channel
- advisory only
- no validation authority
- must not override consumer-owned AEOS schemas or profile selection

### 6.5 Candidate Ordering

Recommended future normative order:

```text
format
require*
feature*
comment.*
```

Rules:

```text
format      max 1, first if present
require     0..n, after format
feature     0..n, after require
comment.*   0..1 per comment channel, after require/feature
```

Valid:

```aeon
//! format:sound.app
//! require:aeon.tuple.v2
//! require:aeon.indexed-paths.v2
//! feature:aeon.locale.v1
//! comment.doc:&ND.v1
//! comment.hint:aeon.schema-hint.v1
```

Invalid for directive-aware consumers:

```aeon
//! feature:aeon.locale.v1
//! require:aeon.tuple.v2
```

The `require` directive appears after `feature`, so strict directive-aware processing must reject the directive block.

## 7. Candidate Consumer Behavior

### 7.1 v1 Core Consumers

AEON Core v1 consumers:

- may inspect `//! format:<id>` in the existing file-header slot;
- must keep file-header host directives out of AES, annotation-stream output, and canonical output;
- must not activate `require`, `feature`, `profile`, or `comment.*` directive semantics;
- continue parsing the document body according to v1 Core rules.

Unsupported syntax still fails naturally through ordinary v1 parsing.

### 7.2 Format-Aware Consumers

Format-aware consumers may inspect `//! format:<id>` for processor discovery.

If additional future directive lines are present and the consumer is not directive-aware, it should not infer capability semantics from them under v1.

### 7.3 Future Directive-Aware Consumers

A future directive-aware consumer may parse the full directive block and enforce:

- directive-block grammar;
- directive ordering;
- directive uniqueness;
- `require`: unknown or unsupported values fail closed;
- `feature`: unknown or unsupported values are ignored unless selected by policy;
- `comment.*`: advisory interpretation only, with no validation authority.

Minimal doctrine: the directive block is a preflight declaration. It may decide whether processing may continue, but it must not change how AEON Core parses the document body.

## 8. Versioning Strategy

AEON should evolve through individually declared capabilities rather than a global version number.

Example:

```aeon
//! require:aeon.tuple.v2
```

Profiles may bundle capabilities in a future directive-aware line:

```aeon
//! profile:aeon.v2.addressing
```

Profile declarations remain untrusted routing hints unless selected and verified by consumer-owned policy.

## 9. Security Model

The directive block declares how the document wishes to be interpreted. Only required capabilities may prevent unsafe interpretation. All other directives are advisory.

Rules:

- documents must not define their own validation rules;
- directive blocks must not override consumer-owned AEOS schemas;
- comment profiles must not imply trust;
- declared profiles and formats are not trust anchors.

## 10. Anti-Ossification Strategy

This proposal supports:

- no global version lock;
- capability-based evolution;
- strict fail-closed semantics;
- explicit directive opt-in;
- separation of Core syntax, AES structure, AEOS validation, and profile or tonic semantics.

## 11. Summary

AEON should evolve through declared capabilities, not version numbers, while preserving strict fail-closed determinism.
