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

The version declaration controls the grammar; parser capability does not override it:

| Declared document | v1-only parser | v2-capable parser |
| :---------------- | :------------- | :---------------- |
| v1 syntax under `&ND v1` | accept | accept as v1 |
| v2 syntax under `&ND v1` | reject | reject as v1 |
| v1 syntax under `&ND v2` | reject unsupported version | accept as v2 |
| v2 syntax under `&ND v2` | reject unsupported version | accept as v2 |

Standalone v2 input MUST declare `&ND v2`. Headerless input MUST receive its effective version from
its embedding profile or typed channel.
Implementations MUST NOT infer v2 from the presence of v2-looking syntax.

The reference API separates parser capability from the effective grammar:

```js
parseAnd(standaloneSource, { allowV2: true });
parseAnd(embeddedSource, { allowV2: true, version: "v2" });
parseInline(inlineSource, { allowV2: true, version: "v2" });
```

`allowV2` declares capability. `version` selects the grammar only for headerless input. A source
declaration takes precedence, and successful document parses report the effective version beside
the AST.

## 5. Candidate Work Areas

The current proposal surface is grouped into five work areas.

### 5.1 Header and Versioning

The explicit standalone declaration is `&ND v2`. Embedded content may omit it only when an enclosing
profile or typed channel supplies v2 as the effective version. The declaration is metadata and does
not become a content block.

Candidate seeds:

- `seed-v2-header-recognized`
- `seed-v2-header-rejected-by-v1-strict`

### 5.2 Inline Forms and Local Links

Core v1 reserves several inline forms. v2 may promote some of them while reusing the inherited link
form for local navigation.

Candidate forms:

| Form | First-draft meaning | Disposition |
| :--- | :------------------ | :---------- |
| `[# ...]` | scalar document-local anchor | Core |
| `[@ #id | label]` | inherited rich-label link with resolved local target | Core |
| `[~ source | alt | mode]` | inline image with required alt text and a closed display-mode enum | Core |
| `[! ...]` | rich warning or admonition content | Core syntax + convention |
| `[? ...]` | rich question or hint content | Core syntax + convention |
| `[+ ...]` | scalar consumer-defined tag | Core syntax + convention |
| `[- ...]` | rich struck content | Core |
| `[" ...]` | rich quoted inline content | Core |
| `[' ...]` | rich inline comment content | Core |
| `[:type = scalar]` | exact AEON typed syntax over the closed inline-scalar subset | Core syntax + convention |
| `[= ...]` | rich highlighted content | Core |
| `[_ ...]` | rich underlined content | Core |
| `[.]` | inline line break | Core |

“Core syntax + convention” is part of the single v2 strict grammar, not an optional parser gate.
Core guarantees the AST and canonical spelling while leaving consumer vocabularies, workflow, and
presentation outside Core. Rich forms use nested inline `children`; identifiers and metadata remain
scalar.

Anchor IDs and the identifier portion of `#id` link targets use `[A-Za-z][A-Za-z0-9._:-]*`.
Matching is exact and case-sensitive in one document-wide namespace. Forward links are allowed;
duplicate anchors and unresolved local targets fail declared-v2 strict parsing. Web and external
resources continue to use inherited `[@ target | label]` links.

The promoted image form accepts `[~ source | alt]` or `[~ source | alt | mode]`. Source and alt text
are required scalars, the omitted mode defaults to `inline`, and explicit modes are limited to
`inline`, `half`, and `full`. Canonical output always spells the resolved mode. These modes record
display intent; Core does not resolve the source or inspect image dimensions.

The reference HTML renderer preserves safe relative sources by default and accepts an explicit
credential-free HTTP(S) `imageBaseUrl` for deterministic WHATWG resolution. Resolved output retains
the authored source in `data-and-source`. Non-HTTP(S), credentialed, and protocol-relative sources are
omitted while mandatory alt text remains available; invalid bases fail with
`invalid_image_base_url`.

The promoted typed-value form adopts exact AEON anonymous typed-scalar syntax, including the
mandatory `=`, structured generic arguments and clarifiers, reserved datatype aliases, literal-family
compatibility, string escapes, and scalar canonicalization. Supported families are string, finite
number, infinity, NaN, null, Boolean, toggle, hex, radix, encoding, date/time/datetime/WTC,
separator literals, SANSA addresses, and custom datatype labels over those scalars. Structured
values, references, nested typed values, trimticks, `prose`, and multiline strings remain outside the
inline subset.

The reference implementation pins this boundary as machine-readable contract
`and-v2-aeon-inline-scalar-v1`, aligned with AEON TypeScript package version `0.12.0`. Mandatory
dependency-free snapshots cover the &ND AST, canonical text, and HTML projection; an optional sibling
repository check detects lexer, parser, or canonicalizer drift in the corresponding AEON forms.

Candidate seeds:

- `seed-v2-inline-anchor-tag-enabled`
- `seed-v2-inline-local-fragment-link-enabled`
- `seed-v2-inline-admonition-tag-enabled`
- `seed-v2-inline-question-tag-enabled`
- `seed-v2-inline-plus-tag-enabled`
- `seed-v2-inline-image-tag-modes`
- `seed-v2-inline-strike-tag-enabled`
- `seed-v2-inline-quoted-tag-enabled`
- `seed-v2-inline-comment-tag-enabled`
- `seed-v2-inline-typed-value-enabled`
- `seed-v2-inline-typed-value-aeon-scalars`
- `seed-v2-inline-highlight-tag-enabled`
- `seed-v2-inline-underline-tag-enabled`
- `seed-v2-inline-line-break-marker-enabled`

### 5.3 Reserved Marker Forms

Some v1-reserved bracket markers may become compact structural markers in v2.

Candidate forms:

| Form | Possible v2 meaning | Status |
| :--- | :------------------ | :----- |
| `[ ]` | todo, unchecked | Core |
| `[x]` | todo, checked | Core |
| `[,]` | todo, in progress | Core |
| `[;]` | todo, cancelled | Core |
| `[>]` | forward marker | Core |
| `[<]` | backward marker | Core |
| `[%]` | inline auto-number marker | Core |
| `[n]` | heading auto-number marker | Core |

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

The executable proposal requires non-empty inline payloads, validates optional tags with
`[A-Za-z][A-Za-z0-9_-]*`, preserves v2 through nested block contexts, and applies the same
`maxBlockSize` resource budget used by inherited raw blocks.
The three block structures are Core candidates; the vocabulary and interpretation of optional tags
remain consumer conventions.

### 5.5 Compatibility and Canonicalization

v2 should define compatibility and canonicalization before the syntax surface grows too large.

Executable boundaries:

- `seed-v2-accepts-v1-strict-core`
- `seed-v2-canonical-roundtrip-core-subset`
- `seed-v2-forward-compat-boundary`
- inherited opaque extension blocks remain syntactically accepted; unsupported consumers use
  fallback content or an explicit unsupported-extension diagnostic
- unpromoted reserved syntax remains a strict `unknown_inline_type` failure
- no recovery or forward-compatibility mode is currently defined

The companion [`and-core-v2-ast-contract.md`](./and-core-v2-ast-contract.md) defines the promoted
node shapes, effective-version metadata, and canonical emission boundary.

## 6. Deferred Ideas

These ideas are not rejected, but they should not be part of the first v2 activation slice:

- footnote syntax such as `[^ ...]`
- profile-gated syntax inside Core strict mode
- HTML passthrough
- executable or evaluatable constructs
- semantic interpretation of links, references, or typed values inside Core

## 7. Test Strategy

The v2 proposal should stay test-first.

The implementation repository contains an executable 94-fixture v2 proposal lane. It is design
pressure, not a published conformance requirement. The normative v1 lane remains independently
reviewable. The proposal runner additionally checks v1 compatibility, headerless effective-version
equivalence, standalone and embedded canonical fixed points, inert HTML projection, nested v2
contexts and rich inline content, local-fragment integrity, resource budgets, opaque extensions,
and the strict forward boundary. Machine-readable contract `and-v2-projection-v1` additionally pins
28 exact source-span assertions and a 15-entry cross-form interaction matrix.

Move from proposal notes to active v2 fixtures only when:

1. The candidate syntax has a written parse shape.
2. The candidate syntax has at least one accepted fixture and one rejected fixture.
3. v1 strict rejection behavior is defined where relevant.
4. Canonical output expectations are documented and reach a parse–emit fixed point.
5. A v2 adapter strategy is written for the CTS runner.

## 8. Embedding Decision

The Core-facing embedding question is resolved: only a host-controlled typed channel may select v2
for headerless input, and it must explicitly supply both v2 capability and `version: "v2"`.
Declarations take precedence over external version options. Named embedding-profile registries remain
deferred.

Image resolution and AEON scalar drift are now pinned. Migration and consumer-convention work are
publication deliverables rather than unresolved Core syntax questions.

## 9. Acceptance Criteria for a First v2 Draft

A first v2 draft can be written when:

1. The version/header model is decided.
2. The first promoted syntax slice is chosen.
3. Compatibility behavior with v1 strict mode is documented.
4. Canonical output behavior is documented for every promoted construct.
5. CTS fixtures exist for accepted and rejected cases.
6. Implementation adapters can run those fixtures without reducing v1 coverage.
7. Exact standalone/embedded canonical and inert HTML snapshots cover every promoted family.
8. Source-span and cross-form interaction matrices cover the new v2 node families.
9. The public API contract types v2 capability, effective version, AST additions, and projection options.
10. Migration and consumer-convention companion guidance is available.

## 10. Current Readiness Result

The executable grammar, AST, strict rejection boundary, v1 compatibility, AEON inline-scalar
contract, image-resolution policy, CLI, and playground are ready for a first-draft candidate. The
track is not yet ready for promotion because a migration guide and consumer-convention companion note
remain open. Exact standalone/embedded canonical, inert HTML, source-span, and cross-form interaction
snapshots are pinned by machine-readable contract `and-v2-projection-v1`.

Footnotes, recovery modes, v2-specific editor tooling, automatic numbering, image fetching, and
consumer vocabularies remain explicitly deferred and do not block the first draft.
