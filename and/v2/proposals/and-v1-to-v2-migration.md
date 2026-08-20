---
id: and-v1-to-v2-migration
title: "&ND Core v1 to v2 Migration Guide"
description: Compatibility rules and mechanical upgrade guidance for moving &ND Core v1 documents and tools to v2.
family: and
group: "&ND"
status: Proposal
path: specification/and/v1-to-v2-migration
license: CC-BY-4.0
---

# &ND Core v1 to v2 Migration Guide

This guide describes migration to the `&ND Core v2` first-draft candidate. It does not announce a
published v2 specification.

## 1. Compatibility Rule

The version boundary is asymmetric:

- a v1 parser rejects a document declared as `&ND v2`;
- a v2-capable parser accepts valid v1 documents without changing their v1 meaning;
- the source declaration selects the grammar, even when a parser supports both versions.

| Source | v1 parser | v2-capable parser |
| :----- | :-------- | :---------------- |
| `&ND v1` with v1 syntax | Accept as v1 | Accept as v1 |
| `&ND v1` with v2 syntax | Reject | Reject as v1 |
| `&ND v2` with inherited v1 syntax | Reject unsupported declaration | Accept as v2 |
| `&ND v2` with v2 syntax | Reject unsupported declaration | Accept as v2 |

A v2-capable parser MUST NOT infer v2 from body syntax.

## 2. Minimal Document Upgrade

A valid standalone v1 document using no v2-only syntax can be upgraded by changing only its
declaration from `&ND v1` to `&ND v2`. Inherited blocks and inline nodes retain the same AST meaning.
Keep the v1 declaration while v1-only readers must remain supported.

There is no automatic downgrade. To return to v1, remove every v2-only construct, restore `&ND v1`,
and validate with a v1 parser.

## 3. Parser and Embedding Upgrade

Standalone input obtains its grammar from its declaration. Headerless input has no declaration
channel; only the host of a typed channel may select v2, and it MUST explicitly provide both v2
reader capability and effective version.

Capability alone leaves headerless input under v1. A v2 version request without capability fails with
`unsupported_version`. A source declaration takes precedence over a conflicting host option.

Successful parse-version metadata must be retained for canonical emission. Standalone canonical v2
output includes `&ND v2`; embedded output omits it. Emitting a v2-only AST node under v1 fails closed.

## 4. Local Navigation

v2 defines local navigation with a dedicated anchor and the inherited link tag:

```and
[# installation]
[@ #installation | Installation]
```

Identifiers are case-sensitive and document-wide. Forward links are accepted; duplicate anchors and
unresolved local targets are rejected. External resources retain ordinary link spelling:

```and
[@ https://example.com/guide | External guide]
```

Early experimental `[~ installation]` and `[@ anchor:installation | ...]` spellings were never
published. They migrate to `[# installation]` and `[@ #installation | ...]`. The `~` tag is now the
inline-image form.

## 5. Inline Images

```and
[~ image.jpg | Descriptive alternative text]
[~ diagram.png | System diagram | half]
```

Source and alt text are mandatory. Mode is `inline`, `half`, or `full`; omission resolves to `inline`
and canonical output spells the mode. Core preserves the authored source but does not fetch it or
inspect the resource.

## 6. AEON Typed Scalars

v2 adopts exact AEON anonymous typed-scalar assignment:

```and
[:date = 2026-08-20]
[:number = 1000.5]
[:radix[2] = %1011]
```

The earlier equals-free experiment migrates as follows:

```text
[:date 2026-08-20]  ->  [:date = 2026-08-20]
```

Only the documented inline-scalar families are accepted. Structured values, references, multiline
strings, nested typed values, and `prose` remain outside the v2 Core subset.

## 7. Supported v2 Additions

| Form | Core result |
| :--- | :---------- |
| `[# id]` and `[@ #id | label]` | Local anchor and resolved local link |
| `[! ...]`, `[? ...]`, `[+ value]` | Advisory, question, and consumer-tag nodes |
| `[~ source | alt | mode]` | Inline image |
| `[- ...]`, `[" ...]`, `[' ...]`, `[= ...]`, `[_ ...]` | Rich inline presentation nodes |
| `[:type = scalar]` | AEON typed scalar |
| `- [ ] content`, `- [x] content`, `- [,] content`, `- [;] content` | First-class todo list and item states |
| `[>]`, `[<]`, `[.]` | Direction and line-break markers; leading unordered-item arrows replace bullets |
| `- [?] content`, `- [!] content` | Hint/attention markers replacing unordered-item bullets while content stays visible |
| heading `[n]` | Heading numbering intent |
| `- [n] content` | First-class auto-number list |
| `[% content]`, `[% (id) content]`, `[% (id)]` | Anonymous/named footnote definitions and named references |
| `~~~=`, `~~~*`, `~~~/`, `~~~_`, `~~~?`, `~~~!` | Highlight, strong, emphasis, underline, hint, and attention paragraph blocks |
| `===`, `***` | Header-text and disclaimer blocks |

Consumer-owned behavior layered on these stable Core nodes is defined by
[`and-consumer-conventions.md`](./and-consumer-conventions.md).

## 8. Formatted Paragraphs

V2 adds matching `~~~=` highlight, `~~~*` strong, `~~~/` emphasis, `~~~_` underline, `~~~?` hint,
and `~~~!` attention paragraph
fences. Each requires non-empty rich inline content and must close with its exact opener. Plain
`~~~` remains ordinary paragraph text in both v1 and v2 and follows inherited soft-wrap
canonicalization.

## 9. Todo Lists

Todo state is structural in v2:

```and
- [ ] draft
- [x] parser
- [,] documentation
- [;] discarded
```

This parses as `todo_list` containing `todo_item` nodes, not as an unordered list containing inline
markers. The `- ` prefix and non-empty content are mandatory, and one list block cannot mix ordinary
and todo items. Bare `[x] parser`, ordered `1. [x] parser`, malformed prefixes, and mixed blocks are
rejected. `[.]` remains an inline line break, not a todo-item terminator.

## 10. Auto-Numbering

`[n]` is contextual structural metadata:

```and
# [n] Numbered title

- [n] first item
- [n] second item
```

The heading receives `autoNumber: true`; the list parses as `auto_number_list` containing inherited
`list_item` nodes. Separator space and non-empty content are mandatory. Bare `[n]`, no-space forms,
explicit `1. [n] item`, and mixed ordinary/todo/auto-number blocks are rejected.

Unlike v1 strict mode, v2 permits an immediately nested list at the exact two-space margin without a
blank separator. This applies to ordinary, todo, and auto-number lists. Canonical output may insert
the inherited blank separator while preserving the same AST.

## 11. Footnotes

V2 promotes `[% ...]` as footnote syntax:

```and
hello [% supporting context]
hello [% (A1) reusable context], again [% (A1)]
```

The first form is an anonymous definition at its reference position. The second declares the
case-sensitive alphanumeric ID `A1`; later `[% (A1)]` forms reference it. A named reference must
follow its single declaration. Empty definitions, malformed IDs, duplicates, unresolved or forward
references, and nested footnotes are rejected. The authored ID is not a forced display number;
processors choose numbers, symbols, hover cards, callouts, or endnotes.

## 12. Directional List Markers

`[>]` and `[<]` remain inline direction markers. In the first inline position after `- `, the arrow
replaces that item's ordinary bullet in projection. The list remains an inherited unordered list and
the marker remains in the paragraph AST, so ordinary and directional items may coexist. Later
markers and markers in paragraphs or ordered lists remain inline.

The exact leading forms `- [?] content` and `- [!] content` follow the same contextual rule while
keeping their item content visible. Rich `[? ...]` and `[! ...]` remain inline callout content.

## 13. Migration Checklist

1. Enable v2 reader capability explicitly.
2. Change declarations only when dropping v1-reader compatibility is acceptable.
3. Supply capability and version for headerless v2 channels.
4. Forward the effective version into canonical emission.
5. Replace experimental anchor, link, and typed-value spellings.
6. Validate anchors and fragment links at whole-document scope.
7. Convert inline experimental todo markers into homogeneous `- [state] content` blocks.
8. Convert contextual numbering to exact heading or `- [n] content` prefixes.
9. Convert footnotes to anonymous definitions or declare an alphanumeric ID before every shorthand
   reference; remove forward references and nesting.
10. Place a direction marker first after `- ` only when it should replace that item's bullet.
11. Convert paragraph-wide formatting or advisory content to exact matching `~~~=`, `~~~*`, `~~~/`, `~~~_`, `~~~?`, or `~~~!` fences;
    leave plain `~~~` as ordinary text.
12. Keep consumer conventions separate from grammar acceptance and canonicalization.
13. Canonicalize once to expose normalized image modes and AEON scalar spellings.
