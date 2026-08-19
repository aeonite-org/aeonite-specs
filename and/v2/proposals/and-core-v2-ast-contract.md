---
id: and-core-v2-ast-contract
title: "&ND Core v2 AST Contract"
description: Proposal AST additions, effective-version metadata, and canonical boundary for &ND Core v2.
family: and
group: "&ND"
status: Proposal
path: specification/and/core-v2-ast-contract
license: CC-BY-4.0
---

# &ND Core v2 AST Contract

This document defines the proposal-stage AST additions exercised by the executable `&ND Core v2`
fixture lane. v2 inherits every v1 AST node without changing its structural meaning.

## 1. Parse Result and Effective Version

A successful document parse reports the effective grammar version beside the document AST:

```ts
interface NdParseSuccess {
  readonly ok: true;
  readonly version: "v1" | "v2";
  readonly document: NdDocument;
}
```

The version is parse metadata rather than a document child. Standalone input obtains it from the
`&ND v1` or `&ND v2` declaration. Headerless embedded input obtains it from an explicit typed parser
option. A parser MUST NOT infer v2 from body syntax.

Canonical emitters receive the effective version explicitly. This preserves the existing v1 AST
shape while allowing a v2 document containing only inherited v1 nodes to retain its v2 declaration.

## 2. Inherited Nodes

The complete v1 block and inline node unions remain valid in v2. A v2-capable reader MUST preserve
the same fields and containment relationships for inherited syntax.

`NdInlineNode` gains the nodes below. `NdBlockNode` gains the three paired-block nodes below, and
`NdHeading` gains the optional `autoNumber` field.

## 3. Scalar Inline Tags

```ts
interface NdAnchorTag {
  readonly type: "anchor_tag";
  readonly id: string;
}

interface NdScalarTag {
  readonly type:
    | "reference_tag"
    | "admonition_tag"
    | "question_tag"
    | "plus_tag"
    | "strike_tag"
    | "quoted_tag"
    | "comment_tag"
    | "highlight_tag"
    | "underline_tag";
  readonly value: string;
}

interface NdTypedValue {
  readonly type: "typed_value";
  readonly datatype: string;
  readonly value: string;
}
```

These proposal nodes contain normalized scalar values, not nested inline children. Datatype names
identify a consumer-level interpretation; Core parsing does not validate a value against its
datatype.

## 4. Compact Inline Markers

```ts
interface NdTodoMarker {
  readonly type: "todo_marker";
  readonly state: "unchecked" | "checked" | "in_progress" | "cancelled";
}

interface NdDirectionalMarker {
  readonly type: "directional_marker";
  readonly direction: "forward" | "backward";
}

interface NdAutoNumberMarker {
  readonly type: "auto_number_marker";
}

interface NdLineBreak {
  readonly type: "line_break";
}
```

Markers record author intent. Core parsing does not calculate display numbers or mutate surrounding
list structure.

## 5. Heading Addition

```ts
interface NdV2Heading extends NdHeading {
  readonly autoNumber?: true;
}
```

The field is present only when a heading begins with the v2 `[n]` marker.

## 6. Paired Blocks

```ts
interface NdHighlightParagraphBlock {
  readonly type: "highlight_paragraph_block";
  readonly children: NdInlineNode[];
}

interface NdHeaderTextBlock {
  readonly type: "header_text_block";
  readonly tag?: string;
  readonly children: NdInlineNode[];
}

interface NdDisclaimerBlock {
  readonly type: "disclaimer_block";
  readonly tag?: string;
  readonly children: NdInlineNode[];
}
```

Paired-block payloads are inline content, not nested block documents. Optional tags preserve the
validated suffix from a tagged opener.

## 7. Canonical Contract

Canonical emission requires both a profile and an effective version:

```js
emitCanonical(document, { profile: "standalone", version: "v2" });
emitCanonical(document, { profile: "embedded", version: "v2" });
```

Standalone v2 output begins with `&ND v2`; embedded output omits the declaration. Every promoted v2
node has a deterministic spelling, and emitting a v2-only node under version v1 MUST fail. The
executable proposal runner checks standalone and embedded parse–emit–parse structural equivalence
and canonical fixed-point stability for every accepted v2 fixture.

## 8. Source Spans

When spans are requested, v2 nodes use the same optional `span` field and normalized source-offset
rules as v1 nodes. Spans are metadata and are excluded from structural round-trip comparison.

## 9. Stability

This contract is executable but remains proposal-stage. Node names and scalar-versus-rich-content
decisions may change before v2 advances to draft.
