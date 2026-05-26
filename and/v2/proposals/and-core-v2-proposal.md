---
id: and-core-v2-proposal
title: "&ND Core v2 Proposal"
description: Proposal-stage anchor for &ND Core v2 evolution work.
family: and
group: "&ND"
status: Proposal
path: specification/and/core-v2-proposal
license: CC-BY-4.0
---

# &ND Core v2 Proposal

This document is a proposal anchor for possible `&ND Core v2` work. It is not a published
specification and does not supersede the v1 draft.

The purpose of this file is to collect candidate changes, compatibility rules, and test strategy
before any v2 grammar is promoted to normative status.

## 1. Proposal Status

| Field | Value |
| :---- | :---- |
| Stage | Proposal |
| Stability | Unstable by design |
| Publication status | Not published |
| Relationship to v1 | Exploratory continuation of the v1 draft |

## 2. Working Goal

`&ND Core v2` explores document-language extensions beyond the current v1 draft while preserving
the properties that make v1 useful:

- deterministic parsing
- explicit structure
- fail-closed behavior
- non-executable documents
- a small core syntax surface

The current working direction is that v1 strict documents should remain valid v2 strict documents
unless v1 itself changes before publication.

## 3. Non-Goals

This proposal does not yet:

- declare a final v2 grammar
- declare final compatibility guarantees
- declare final canonical output rules
- require implementation support
- activate a published CTS lane

## 4. Compatibility Stance

Until a publication policy says otherwise, v2 work should follow these rules:

1. Documents accepted by v1 strict mode should be accepted by v2 strict mode.
2. Already-valid v1 syntax should keep the same structural meaning in v2.
3. v2-only syntax should prefer forms that v1 reserves and rejects.
4. v2 should avoid reinterpreting existing valid v1 constructs.
5. v1 strict implementations should fail closed when presented with v2-only declarations or syntax.

## 5. Candidate Work Areas

The current proposal surface is grouped into five work areas.

### 5.1 Header and Versioning

Define an explicit v2 document declaration shape.

Open questions:

- Is a version declaration required in every v2 document?
- Is the declaration part of content, metadata, or a pre-content header?
- How should v1 strict parsers reject v2 declarations?

Candidate seeds:

- `seed-v2-header-recognized`
- `seed-v2-header-rejected-by-v1-strict`

### 5.2 Reserved Inline Forms

Core v1 reserves several inline forms. v2 may promote some of them into first-class syntax.

Candidate forms:

| Form | Possible v2 meaning | Status |
| :--- | :------------------ | :----- |
| `[# ...]` | anchor or local id | Candidate |
| `[~ ...]` | reference or mention | Candidate |
| `[! ...]` | warning or admonition | Candidate |
| `[? ...]` | question or hint | Candidate |
| `[+ ...]` | consumer-defined tag | Candidate |
| `[- ...]` | struck text | Candidate |
| `[" ...]` | quoted inline text | Candidate |
| `[' ...]` | inline comment | Candidate |
| `[:type value]` | typed inline value | Candidate |
| `[= ...]` | highlighted text | Candidate |
| `[_ ...]` | underlined text | Candidate |
| `[.]` | inline line break | Candidate |

Candidate seeds:

- `seed-v2-inline-anchor-tag-enabled`
- `seed-v2-inline-reference-tag-enabled`
- `seed-v2-inline-admonition-tag-enabled`
- `seed-v2-inline-question-tag-enabled`
- `seed-v2-inline-plus-tag-enabled`
- `seed-v2-inline-strike-tag-enabled`
- `seed-v2-inline-quoted-tag-enabled`
- `seed-v2-inline-comment-tag-enabled`
- `seed-v2-inline-typed-value-enabled`
- `seed-v2-inline-highlight-tag-enabled`
- `seed-v2-inline-underline-tag-enabled`
- `seed-v2-inline-line-break-marker-enabled`

### 5.3 Reserved Marker Forms

Some v1-reserved bracket markers may become compact structural markers in v2.

Candidate forms:

| Form | Possible v2 meaning | Status |
| :--- | :------------------ | :----- |
| `[ ]` | todo, unchecked | Candidate |
| `[x]` | todo, checked | Candidate |
| `[,]` | todo, in progress | Candidate |
| `[;]` | todo, cancelled | Candidate |
| `[>]` | forward marker | Candidate |
| `[<]` | backward marker | Candidate |
| `[%]` | inline auto-number marker | Candidate |
| `[n]` | heading auto-number marker | Candidate |

Candidate seeds:

- `seed-v2-inline-todo-markers-enabled`
- `seed-v2-inline-directional-markers-enabled`
- `seed-v2-inline-auto-number-marker-enabled`
- `seed-v2-heading-auto-number-marker-enabled`

### 5.4 Paired Block Forms

Core v1 reserves several block-ish text forms. v2 may promote some of them into paired block
constructs, but only if the delimiters remain deterministic and easy to reject when malformed.

Candidate forms:

```text
highlight paragraph block
  opener: ~~~=
  closer: ~~~=

header text block
  opener: === or ===<tag>
  closer: ===

disclaimer block
  opener: *** or ***<tag>
  closer: ***

<tag> ::= [A-Za-z][A-Za-z0-9_-]*
```

Candidate seeds:

- `seed-v2-block-highlight-paragraph-enabled`
- `seed-v2-block-header-text-enabled`
- `seed-v2-block-disclaimer-enabled`

### 5.5 Compatibility and Canonicalization

v2 should define compatibility and canonicalization before the syntax surface grows too large.

Candidate seeds:

- `seed-v2-accepts-v1-strict-core`
- `seed-v2-canonical-roundtrip-core-subset`
- `seed-v2-forward-compat-boundary`
- `seed-v2-unknown-extension-default-reject`

## 6. Deferred Ideas

These ideas are not rejected, but they should not be part of the first v2 activation slice:

- footnote syntax such as `[^ ...]`
- profile-gated syntax inside Core strict mode
- HTML passthrough
- executable or evaluatable constructs
- semantic interpretation of links, references, or typed values inside Core

## 7. Test Strategy

The v2 proposal should stay test-first.

Before an active v2 CTS lane exists, proposal fixtures may be named in this document and explored
in implementation branches. They should not be treated as conformance requirements.

Move from proposal notes to active v2 fixtures only when:

1. The candidate syntax has a written parse shape.
2. The candidate syntax has at least one accepted fixture and one rejected fixture.
3. v1 strict rejection behavior is defined where relevant.
4. Canonical output expectations are documented.
5. A v2 adapter strategy is written for the CTS runner.

## 8. Open Questions

1. Which reserved forms belong in Core v2, and which should remain convention or profile features?
2. Should v2 require explicit document version declarations?
3. Should any v2 syntax be feature-gated, or should Core strict mode remain a single fixed surface?
4. What is the smallest useful first v2 activation slice?
5. How much v1-to-v2 migration guidance is needed before publication?

## 9. Acceptance Criteria for a First v2 Draft

A first v2 draft can be written when:

1. The version/header model is decided.
2. The first promoted syntax slice is chosen.
3. Compatibility behavior with v1 strict mode is documented.
4. Canonical output behavior is documented for every promoted construct.
5. CTS fixtures exist for accepted and rejected cases.
6. Implementation adapters can run those fixtures without reducing v1 coverage.
