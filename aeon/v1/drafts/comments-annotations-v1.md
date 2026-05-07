---
id: aeon-core-v1-comments-annotations
title: AEON v1 Comments and Annotations Reference
description: Reference for comment forms, structured channels, reserved meanings, deterministic attachment, and annotation-related boundaries.
group: Core References
path: specification/aeon-v1-documentation/aeon-v1-comments-and-annotations-reference
links:
  - aeon-core-v1
  - aeon-v1-conformance-matrix
  - aeos-v1
---

# AEON v1 Comments and Annotations Reference

Status: official v1 companion reference  
Scope: comment forms, structured channels, reserved meanings, and deterministic attachment behavior.

## 1. Comment Families

AEON v1 recognizes two broad families:

1. Plain comments
- line: `// ...`
- block: `/* ... */`
- file-header shebang: `#!...` on line 1, column 1 only

2. Structured comments
- line channels: `//#`, `//@`, `//?`, `//!`, `//{`, `//[`, `//(`
- block channels: `/# ... #/`, `/@ ... @/`, `/? ... ?/`, `/{ ... }/`, `/[ ... ]/`, `/( ... )/`

Core rule:
- comments are trivia and do not alter parse semantics, canonical path assignment, or reference legality.

## 2. Channel Catalog

### 2.1 Plain

Forms:

```aeon
// plain
/* plain */
```

Meaning:
- human-facing commentary only;
- not emitted into the structured annotation stream.

### 2.2 Documentation Channel

Forms:

```aeon
//# docs
/# docs #/
```

Annotation kind:
- `doc`

Intended use:
- documentation for nearby binding, element, or container target.

### 2.3 Annotation Channel

Forms:

```aeon
//@ env(selected=true)
/@ env(selected=true) @/
```

Annotation kind:
- `annotation`

Intended use:
- machine-readable metadata annotations attached to nearby targets.

### 2.4 Hint Channel

Forms:

```aeon
//? threshold: number = [>=0], [<=1]
/? threshold: number = [>=0], [<=1] ?/
```

Annotation kind:
- `hint`

Intended use:
- schema/profile/editor hints or human-readable guidance associated with a nearby target.

### 2.5 Host Channel

Line form:

```aeon
//! host-runtime-note
```

Placement rule:
- `//!` is a file-header host directive only;
- it must appear on line 1, column 1;
- if a leading shebang line is present, it may instead appear on line 2, column 1;
- outside that slot, `//!` is treated as a plain line comment and has no host-directive meaning.

Shebang rule:
- `#!...` is accepted as a plain file-header comment only on line 1, column 1;
- one leading UTF BOM may appear before that file-header slot and is ignored for this purpose;
- outside that exact position, `#!` is not a comment introducer and is tokenized normally.

Annotation kind in lexer metadata:
- `host`

Current v1 emission note:
- host-channel comments are recognized by the lexer;
- they are not emitted into the structured annotation stream by the current reference implementation.

Fast-path format note:
- before Phase 1 parsing, implementations may expose a lightweight preflight/file-preamble inspection API that reads only the allowed shebang/host-directive slot;
- that preflight inspection must ignore at most one leading UTF BOM before any further detection;
- after BOM removal, a shebang is recognized only on the first physical line;
- `//! format:<id>` may appear only in the file-header slot: on the first physical line after BOM removal, or on the second physical line when the first is a shebang;
- `//! format:<id>` is a tooling side-channel for processor discovery and pre-parser routing only;
- it does not create bindings, does not modify header fields, and must not appear in AES, annotation-stream output, or canonical output.

Directive-block reservation note:
- future AEON lines may define a broader directive block using strict `//! key:value` lines for capability-based evolution;
- in v1, that broader block is reserved and non-operational;
- v1 processors MUST NOT activate `require`, `feature`, `profile`, or `comment.*` semantics from `//!` comments;
- see `appendices/appendix-directive-block-capabilities.md` for the informative upgrade strategy.

### 2.6 Reserved Channels

Forms:

```aeon
//{ structure
//[ profile
//( instructions

/{ structure }/
/[ profile ]/
/( instructions )/
```

Annotation kind:
- `reserved`

Reserved subtypes:
- `structure`
- `profile`
- `instructions`

Current meaning:
- reserved namespace for standardized ecosystem/documentation use;
- must not change core parse or reference behavior.

## 3. Non-Influence Rule

Comments and annotations must not:
- create or remove bindings;
- change canonical path identity;
- change reference legality;
- change assignment ordering;
- act as list, tuple, node, or binding separators.

Implication:
- comments may appear between tokens and still attach to nearby targets;
- they do not redefine the grammar around them.

## 4. Attachment Targets

Structured comments may attach to:
- a canonical path target;
- a span-only target when no canonical path target exists;
- an unbound status when nothing valid is available.

Target preference order:
1. `path`
2. `span`
3. `unbound`

Unbound reasons:
- `eof`
- `no_bindable`

## 5. Deterministic Attachment Rules

The current official v1 reference behavior is:

1. If the comment is inside a containing bindable span, try to attach to the nearest descendant target.
2. If no contained descendant wins, attach to the containing target itself.
3. Otherwise, prefer the nearest trailing same-line target.
4. Otherwise, prefer the nearest forward target.
5. If no path target exists, try the same logic with span-only bindables.
6. If nothing is available, mark the annotation unbound.

This produces deterministic results for prefix, postfix, infix, and standalone structured comments.

## 6. Neighbor Attachment Cases

### 7.1 Trailing Same-Line

```aeon
a = 1 //? required
```

Attaches to:

```aeon
$.a
```

Rule:
- same-line trailing structured comments bind to the completed assignment immediately before them.

### 7.2 Standalone Forward

```aeon
//# docs
a = 1
```

Attaches to:

```aeon
$.a
```

Rule:
- standalone structured comments bind forward to the next available bindable target.

### 7.3 Infix Container Comment

```aeon
a = [1, /? in-list ?/ 2]
```

Attaches to:

```aeon
$.a[1]
```

Rule:
- when a comment sits inside a container between elements, the binder prefers the nearest indexed descendant rather than the container path itself.

### 7.4 Postfix and Prefix Element Comments

```aeon
a = [1 /# post #/, /# pre #/ 2]
```

Attaches to:
- `/# post #/` -> `$.a[0]`
- `/# pre #/` -> `$.a[1]`

Rule:
- postfix comments bind to the nearest completed element;
- prefix comments bind to the nearest following element.

### 7.5 EOF Unbound

```aeon
a = 1
//# tail
```

Attaches to:

```aeon
unbound(eof)
```

Rule:
- if no forward bindable target exists after a standalone structured comment, it is unbound.

### 7.6 No Bindable Document

```aeon
//@ lonely
```

Attaches to:

```aeon
unbound(no_bindable)
```

Rule:
- if the document yields no bindable targets at all, structured comments are unbound.

## 7. Container Fallback

If a structured comment is contained within a bindable span and no nearer descendant target is valid, it may attach to the containing target.

Practical effect:
- comments inside empty or non-indexed containers can fall back to the container assignment target.

## 8. Source Order and Emission

Structured annotation records are emitted in source order.

Current reference implementation behavior:
- emits `doc`, `annotation`, `hint`, and `reserved`;
- skips `plain` and `host` during annotation-stream emission.

## 9. Form Preservation

Annotation stream records preserve:
- `kind`
- `form` (`line` or `block`)
- raw source text
- source span
- resolved target

Reserved channels also preserve subtype:
- `structure`
- `profile`
- `instructions`

## 10. Newline and Block Behavior

Rules:
- line comments terminate at newline;
- block comments may span newlines;
- unterminated block comments are a lexer error;
- comments are never newline substitutes or grammar separators by themselves.

## 11. Minimum Conformance Reminders

Implementations targeting the v1 annotation model must at minimum:
- recognize the official structured channel forms;
- preserve line vs block form in annotation records;
- attach deterministically using the official target preference order;
- preserve reserved subtypes;
- fail with deterministic unterminated block-comment diagnostics.
