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

### 1.1 Host-Controlled Embedded Version Selection

Only the host of a headerless typed channel may supply an effective v2 version. It MUST explicitly
provide both v2 reader capability and `version: "v2"`; capability alone does not select v2, and a
version request without capability fails with `unsupported_version`. Missing version selection
defaults to v1. Unknown version values fail with `invalid_version_option`.

A source declaration always takes precedence over an external version option. Declared-v1 input
remains v1 even when the host requests v2, and declared-v2 input remains v2 even when the host passes
`version: "v1"`. A declared-v2 document still requires a v2-capable reader. Implementations MUST NOT
infer capability or effective version from document content. Registries of named embedding profiles
are outside this first-draft Core boundary.

## 2. Inherited Nodes

The complete v1 block and inline node unions remain valid in v2. A v2-capable reader MUST preserve
the same fields and containment relationships for inherited syntax.

`NdInlineNode` gains the nodes below. `NdBlockNode` gains `NdTodoList`, `NdAutoNumberList`,
`NdCardBlock`, and the paired-block nodes below; `NdHeading` gains the optional `autoNumber` field;
inherited table and table-cell nodes gain the optional v2 fields defined below.

## 3. Capability Disposition

The first-draft candidate surface is divided by ownership, not by parser gates:

| Forms | Disposition | Contract boundary |
| :---- | :---------- | :---------------- |
| `[# ...]` and inherited `[@ #id | label]` | Core | Case-sensitive document-local anchors and resolved fragment links. |
| `[- ...]`, `[" ...]`, `[' ...]`, `[= ...]`, `[_ ...]` | Core | Rich inline content with stable structural meaning. |
| `[! ...]`, `[? ...]` | Core syntax + convention | Rich inline content; presentation and product workflow are consumer-defined. |
| `[+ ...]` | Core syntax + convention | Scalar consumer tag; vocabulary and behavior remain consumer-defined. |
| `[~ source | alt | mode]` | Core | Inline image with required source and alt text; mode is `inline`, `half`, or `full`. |
| `[:type = scalar]` | Core syntax + convention | Exact AEON type-assignment syntax over a closed inline-scalar subset. |
| `- [ ] content`, `- [x] content`, `- [,] content`, `- [;] content` | Core | First-class todo list and item states; workflow and presentation are projections. |
| `[>]`, `[<]` | Core | Directional author-intent markers; a leading marker replaces an unordered-list bullet in projection. |
| `[.]` | Core | Explicit inline line break; never a directional marker. |
| `- [?] content`, `- [!] content` | Core structure + consumer projection | Hint/attention markers replace unordered-list bullets while content remains visible. |
| heading `[n]` and `- [n] content` | Core | Contextual heading field and first-class auto-number list; number calculation is outside Core. |
| inherited `~~~$` / `~~~$ language`; v2 `~~~$ [n]` / `~~~$ [n] language` | Core | Shared dollar code blocks plus v2 numbered-line intent; inherited backtick fences remain accepted. |
| table separators `<--`, `-=-`, `-->` and adjacent `|>` span markers | Core | Column alignment and horizontal `colSpan`; row spanning remains unsupported. |
| `~~~|` / `~~~| title` … `~~~|` | Core structure + consumer projection | Visible card container; a rich inline title makes it collapsible. Styling and interaction details are consumer-defined. |
| `[% content]`, `[% (id) content]`, `[% (id)]` | Core structure + consumer projection | Footnote definitions and backward references; displayed labels and placement are consumer-defined. |
| `[^ ...]` | Core | Rich inline disclaimer content. |
| `[(id) content]`, `~~~(id)` … `~~~` | Core syntax + convention | Rich semantic wrappers with a portable consumer-owned ID; default projection exposes only content. |
| `\` before a block opener | Core | V2-only structural escape that produces ordinary paragraph text and is emitted only when required. |
| `~~~=`, `~~~*`, `~~~/`, `~~~_`, `~~~?`, `~~~!`, `~~~'`, `~~~#`, `~~~^` paired blocks | Core | Highlight, strong, emphasis, underline, hint, attention, comment, header-text, and disclaimer block structure. |
| All other unpromoted reserved forms | Deferred | Rejected by v2 strict mode. |

“Core syntax + convention” remains part of the single v2 strict grammar. It means Core guarantees
the parse shape and canonical spelling while deliberately declining to standardize a consumer
vocabulary, workflow, or visual treatment. The complete ownership boundary is defined in
[`and-consumer-conventions.md`](./and-consumer-conventions.md).

## 4. Inline Content Models

```ts
interface NdAnchorTag {
  readonly type: "anchor_tag";
  readonly id: string;
}

interface NdPlusTag {
  readonly type: "plus_tag";
  readonly value: string;
}

interface NdImageTag {
  readonly type: "image_tag";
  readonly src: string;
  readonly alt: string;
  readonly mode: "inline" | "half" | "full";
}

interface NdTypedValue {
  readonly type: "typed_value";
  readonly datatype: NdAeonDatatype;
  readonly value: NdAeonInlineScalar;
}

interface NdAeonDatatype {
  readonly name: string;
  readonly genericArgs: string[];
  readonly clarifiers: (string | number)[];
}

type NdAeonInlineScalar =
  | { readonly type: "StringLiteral"; readonly value: string }
  | { readonly type: "NumberLiteral"; readonly value: string }
  | { readonly type: "InfinityLiteral"; readonly value: "Infinity" | "-Infinity" }
  | { readonly type: "NaNLiteral"; readonly value: "NaN" | "-NaN" }
  | { readonly type: "NullLiteral"; readonly mode: "reserved" | "reason"; readonly value: string }
  | { readonly type: "BooleanLiteral"; readonly value: boolean }
  | { readonly type: "ToggleLiteral"; readonly value: "yes" | "no" | "on" | "off" }
  | { readonly type: "HexLiteral" | "RadixLiteral" | "EncodingLiteral"; readonly value: string }
  | { readonly type: "DateLiteral" | "TimeLiteral"; readonly value: string }
  | { readonly type: "DateTimeLiteral"; readonly value: string; readonly temporalKind: "datetime" | "wtc" }
  | { readonly type: "SeparatorLiteral" | "SansaAddressLiteral"; readonly value: string };

interface NdRichV2Tag {
  readonly type:
    | "admonition_tag"
    | "question_tag"
    | "strike_tag"
    | "quoted_tag"
    | "comment_tag"
    | "highlight_tag"
    | "disclaimer_tag"
    | "underline_tag";
  readonly children: NdInlineNode[];
}

interface NdFootnoteDefinition {
  readonly type: "footnote_definition";
  readonly id?: string;
  readonly children: NdInlineNode[];
}

interface NdFootnoteReference {
  readonly type: "footnote_reference";
  readonly id: string;
}

interface NdSemanticTag {
  readonly type: "semantic_tag";
  readonly id: string;
  readonly children: NdInlineNode[];
}
```

Identifiers, consumer tags, and image fields are normalized scalars. AEON typed values preserve a
structured datatype annotation and literal-family-aware scalar node. Content-bearing
tags preserve nested inline structure through `children`. Whitespace at a rich tag's outer content
boundary is insignificant; whitespace inside its child sequence remains
content. Rich tags participate in the inherited inline-depth budget.

## 5. AEON Inline Typed Values

The typed-value form wraps one AEON anonymous typed scalar:

```text
[:TypeAnnotation = ScalarLiteral]
```

The `=` is mandatory. The earlier proposal spelling `[:date 2026-08-20]` is invalid. &ND uses AEON
type-annotation syntax, string escapes, literal recognition, reserved datatype aliases, compatibility
rules, and canonical scalar spelling. Reserved datatype names MUST match their AEON literal family.
Custom datatype names are accepted and their meaning remains consumer-defined.

The supported inline subset is closed:

| Literal family | Accepted datatype names |
| :------------- | :---------------------- |
| string | `string` |
| finite number | `number`, `n`, `int`, `int8`, `int16`, `int32`, `int64`, `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `float`, `float32`, `float64` |
| non-finite number | `infinity`, `nan` |
| null | `null`, including generic domain claims such as `null<datetime>` |
| Boolean | `boolean`, `bool` |
| toggle | `toggle` |
| hex | `hex` |
| radix | `radix`, `decimal`, `radix2`, `radix6`, `radix8`, `radix12` |
| encoding | `encoding`, `base64`, `embed`, `inline` |
| temporal | `date`, `time`, `datetime`, `wtc` |
| separator | `sep`, `kadot` |
| SANSA address | `sansa` |
| supported scalar with consumer meaning | any valid custom AEON datatype name |

Applicable AEON generic arguments and clarifiers remain structured, including `null<datetime>`,
`radix[2]`, `encoding["base58"]`, and `sep["x"]`. Objects, lists, tuples, nodes, clone references,
pointer references, bindings, attributes, structural identities, nested typed values, trimticks,
`prose`, and multiline strings are not valid in this inline context. Canonical &ND output delegates
the enclosed annotation and scalar to these AEON canonical rules.
Generic datatype nesting uses AEON's default depth lock of one in the v2 reference parser.

The executable compatibility boundary is contract `and-v2-aeon-inline-scalar-v1` in the reference
implementation's `cts/contracts/aeon-inline-scalar-v1.json`. It pins the accepted datatype names and
aliases, literal-family AST shapes, canonical &ND spelling, HTML projection, and exclusions against
AEON TypeScript package version `0.12.0`. The contract check is mandatory and dependency-free. A
separate drift check compares the same cases with the sibling AEON lexer, parser, and canonicalizer
when those built packages are available; an unavailable sibling checkout does not weaken or fail the
standalone &ND conformance check.

## 6. Local Anchors and Fragment Links

V2 uses one shared, case-sensitive identifier grammar for local anchors and fragment targets, named
footnotes, and inline/block semantic wrappers:

```text
v2-id ::= [A-Za-z0-9][A-Za-z0-9._:-]*
```

The first character is alphanumeric; later characters may also be `.`, `_`, `-`, or `:`. Each
construct retains its own diagnostic and namespace rules, but none defines a narrower lexical class.
`[# id]` defines `id` in one document-wide namespace, including
inside nested blocks and extension fallbacks. A document MUST NOT define the same ID twice. An inherited
link whose target is `#id`, written `[@ #id | label]`, MUST resolve to an anchor in the same declared-v2
document; forward links are allowed. The link retains the inherited `NdLink` AST shape with
`href: "#id"` and rich label `children`. Canonical emission preserves the target and label exactly,
and HTML projection already emits the browser-native fragment link.

A declared-v2 document parse has two logical conformance phases. The first constructs the complete
structural tree while collecting anchor definitions and local-link targets. Only after structural
construction succeeds does document-wide validation check identifier uniqueness and target
resolution. An implementation may fuse the work internally, but observable success follows this
ordering. This permits forward links without requiring `parseInline` or an individual chunk to know
the completed document namespace.

A standalone `parseInline` operation validates the `#id` target grammar but cannot resolve it without
a document namespace. A streaming or chunked parser MAY expose provisional structural results, but
it MUST defer successful document conformance until end-of-document validation has completed. V2
canonical emission performs the same full-document integrity checks on a supplied AST. Declared-v1
documents retain their existing generic link behavior. Webpages and external resources continue to
use inherited targets such as
`[@ https://example.com | Example]`.

## 7. Inline Images

The image form is:

```text
[~ source | alt]
[~ source | alt | mode]
```

`source` and `alt` are required, non-empty scalar fields. An escaped `\|` is data rather than a
field separator. The optional mode defaults to `inline`; when present it MUST be exactly `inline`,
`half`, or `full`. An explicit empty third field is invalid rather than an omitted mode. Canonical
output always includes the resolved mode, so `[~ source | alt]` becomes
`[~ source | alt | inline]`. This expansion is intentional one-time normalization: formatters and
linters SHOULD treat that first canonical diff as expected, and subsequent canonicalization is a
byte-stable fixed point.

`inline` requests a height matched to the surrounding font size. `half` requests one half of the
image's intrinsic height and proportional width. `full` requests the intrinsic dimensions. These
are display intents: Core does not fetch, decode, inspect, or validate the referenced image and
therefore does not record pixel dimensions in the AST. Consumers remain responsible for source
resolution, loading policy, layout constraints, and failure presentation. Alt text is mandatory so
every conforming AST carries an accessible text alternative.
Image sources participate in the inherited `maxLinkTargetLength` resource budget.

The AST and canonical form retain the authored, escape-decoded `src`; Core never resolves it against
a filesystem path, process working directory, page URL, or document URL. The reference HTML renderer
accepts an optional explicit `imageBaseUrl`. Without it, safe relative references are emitted unchanged
and resolution belongs to the embedding HTML document. With it, relative and root-relative references
are resolved using the WHATWG URL algorithm. The base MUST be an absolute credential-free HTTP(S) URL;
an invalid base fails with `invalid_image_base_url`. Absolute HTTP(S) sources remain unchanged.

The reference HTML safety policy rejects non-HTTP(S) absolute schemes, credentialed URLs, and
protocol-relative sources. It preserves alt text while omitting unsafe source attributes. When an
authored relative source is resolved, the emitted `src` or `srcset` is absolute and the original value
is retained in `data-and-source`. The renderer does not emit a `<base>` element, fetch the resource, or
mutate the AST.

## 8. Table Alignment and Horizontal Spans

V2 extends inherited table nodes additively:

```ts
interface NdV2Table extends NdTable {
  readonly alignments?: readonly ("left" | "center" | "right" | null)[];
}

interface NdV2TableCell extends NdTableCell {
  readonly colSpan?: number;
}
```

Ordinary v1-shaped tables retain their exact inherited AST. `alignments` is present only when at
least one logical column uses `<--` (left), `-=-` (center), or `-->` (right); `---` contributes
`null`. `colSpan` is present only when greater than one.

The separator row defines logical width. A cell beginning immediately after its pipe with one or
more `>` characters, one ASCII space, and non-empty content spans one plus the marker count:
`|> content` spans two columns and `|>> content` spans three. Padded `| > literal |` is ordinary
content. Header and body cells may span; separator cells may not. Every row's span sum MUST equal the
separator width. Malformed or under/overflowing spans fail with `invalid_table_span`; alignment
failures use `invalid_table_alignment`. The inherited `maxTableColumns` budget counts logical
columns. Row spanning is unsupported. A spanning cell uses its first covered column's alignment.
Canonical output emits exact alignment tokens and adjacent span markers; reference HTML uses
`text-align` and native `colspan`. V1 rejects these extensions. Inline spans inside a spanning cell
begin at trimmed content and exclude the adjacent marker.

## 9. Card Blocks

```ts
interface NdCardBlock {
  readonly type: "card_block";
  readonly title?: NdInlineNode[];
  readonly children: NdBlockNode[];
}
```

An unnamed card uses exact `~~~|` opener and closer lines. A named card adds one ASCII space and a
non-empty rich inline title to the opener: `~~~| title`. `title` is absent for an unnamed card and
present for a named card; its presence carries collapsible intent and is not a semantic ID. The body
is parsed as ordinary block content and must contain at least one block.

Empty cards and malformed titles fail with `invalid_card_block`; missing exact closers fail with
`unclosed_card_block`. The identical unnamed opener and closer make direct same-level card nesting
unavailable. Canonical output preserves the named/unnamed form. Reference HTML uses a visible
`<aside>` for unnamed cards and native `<details>/<summary>` for named cards. Other presentation and
interaction details are consumer-owned. V1 reserves and rejects the `~~~|` opener.

## 10. Todo Lists

```ts
interface NdTodoList {
  readonly type: "todo_list";
  readonly items: NdTodoItem[];
}

interface NdTodoItem {
  readonly type: "todo_item";
  readonly state: "unchecked" | "checked" | "in_progress" | "cancelled";
  readonly children: NdBlockNode[];
}
```

The exact prefixes are `- [ ] `, `- [x] `, `- [,] `, and `- [;] ` followed by non-empty inline
content. A matching unordered list block becomes `todo_list`; its marker becomes item state rather
than an inline child. Every item in one block must be the same kind. Mixed ordinary/todo items fail
with `mixed_list_item_kinds`; ordered and bare todo markers are rejected. In v2, ordinary and todo
lists may begin an exact two-space-indented nested list immediately without a blank separator. Other
child blocks retain inherited boundaries. Todo lists canonicalize as `- [state] content`.

## 11. Compact Inline Markers

```ts
interface NdDirectionalMarker {
  readonly type: "directional_marker";
  readonly direction: "forward" | "backward";
}

interface NdAdvisoryMarker {
  readonly type: "advisory_marker";
  readonly kind: "question" | "admonition";
}

interface NdLineBreak {
  readonly type: "line_break";
}
```

`[>]` and `[<]` are the only forms that produce `NdDirectionalMarker`. `[.]` always produces the
separate `NdLineBreak` node and never carries a direction or bullet-replacement intent.

Inline markers record author intent. A directional marker in the first inline position of an
unordered list item's paragraph head replaces that item's ordinary bullet in projection. The marker
remains in the inline AST and the container remains an inherited unordered `list`, so directional
and ordinary items may coexist and nesting is unchanged. Later markers remain inline. Ordered lists
do not receive bullet-replacement behavior. Canonical output preserves `- [direction] content`.

The exact leading forms `- [?] content` and `- [!] content` produce an `advisory_marker` followed by
visible item content. They remain inherited unordered lists and may coexist with ordinary items.
Compact `[?]` and `[!]` are not general inline forms; rich `[? ...]` and `[! ...]` remain inline.

## 12. Footnotes

`[% content]` creates an anonymous definition and reference at that position. `[% (id) content]`
creates a named definition and first reference; `[% (id)]` reuses an already-declared named
definition. Named IDs use the shared `v2-id` grammar and may be declared only once. References
must follow their definition. Empty definitions, malformed IDs, duplicates, unresolved or forward
references, and nested footnotes are rejected.

Definitions preserve rich inline `children`; anonymous definitions cannot be referenced again.
Core retains the graph and authored IDs but does not choose displayed numbers or symbols, hover or
callout behavior, endnote placement, or backlinks. Canonical output preserves the applicable form.

## 13. Heading Addition

```ts
interface NdV2Heading extends NdHeading {
  readonly autoNumber?: true;
}
```

The field is present only when a heading begins with the exact `[n] ` prefix followed by non-empty
content. `[n]` is contextual metadata rather than an inline node; missing separator space, empty
headings, and paragraph use are rejected. The optional literal-`true` field is intentional: absence
means the inherited ordinary-heading shape, while presence records explicit numbering intent.
`autoNumber: false` is not part of the conforming AST. This keeps v2 additive over v1 headings and
avoids inserting a new false-valued property into every unnumbered heading; consumers that require a
dense serialization may derive `false` outside the Core AST.

## 14. Auto-Number Lists

```ts
interface NdAutoNumberList {
  readonly type: "auto_number_list";
  readonly items: NdListItem[];
}
```

The exact prefix is `- [n] ` followed by non-empty content. A matching block becomes
`auto_number_list`; `[n]` is consumed as structural intent rather than retained inline. Every item in
one block must use the same kind. Mixed ordinary, todo, and auto-number items fail with
`mixed_list_item_kinds`; explicit ordered markers, bare paragraph markers, malformed spacing, and
empty items are rejected. Auto-number lists use the same v2 immediate two-space nesting rule as
ordinary and todo lists; other child blocks retain inherited boundaries. They canonicalize as
`- [n] content`. Core records sequence participation but does not calculate displayed numbers.

## 15. Code Blocks

V2 retains the inherited `NdCodeBlock` AST, every v1 backtick-fence form, and v1's unnumbered
tilde-dollar forms. It extends the dollar opener with optional `[n]` numbered-line intent:

```text
code-open ::= "~~~$" [ " " ( code-language | "[n]" [ " " code-language ] ) ]
code-close ::= "~~~$"
code-language ::= [A-Za-z][A-Za-z0-9_-]*
```

The optional language is canonicalized to lowercase. `[n]` maps to the inherited
`NdCodeBlock.ordered: true` field as numbered-line intent. The closer is always bare `~~~$`, and the
payload retains inherited raw-code semantics and resource budgets.

A v1 parser accepts `~~~$` and `~~~$ language`, but rejects either `[n]` opener with
`invalid_code_fence`; v1 ordered code remains spelled with quadruple backticks. A v2 parser accepts
all inherited backtick and unnumbered dollar forms without changing their AST meaning. V2 canonical
emission prefers the `~~~$` family, including for code parsed from backticks, and falls back to the
matching inherited backtick fence when the payload contains an exact `~~~$` line. V1 canonical
emission prefers backticks and uses an unnumbered dollar fence only to avoid an exact triple-backtick
payload line. The briefly proposed
`~~~language` and `~~~~language` forms are unsupported and reject with `deprecated_code_fence`.
Plain `~~~` remains ordinary paragraph text.

## 16. Paired Blocks

```ts
interface NdHighlightParagraphBlock {
  readonly type: "highlight_paragraph_block";
  readonly children: NdInlineNode[];
}

interface NdStrongParagraphBlock {
  readonly type: "strong_paragraph_block";
  readonly children: NdInlineNode[];
}

interface NdEmphasisParagraphBlock {
  readonly type: "emphasis_paragraph_block";
  readonly children: NdInlineNode[];
}

interface NdUnderlineParagraphBlock {
  readonly type: "underline_paragraph_block";
  readonly children: NdInlineNode[];
}

interface NdQuestionParagraphBlock {
  readonly type: "question_paragraph_block";
  readonly children: NdInlineNode[];
}

interface NdAdmonitionParagraphBlock {
  readonly type: "admonition_paragraph_block";
  readonly children: NdInlineNode[];
}

interface NdCommentBlock {
  readonly type: "comment_block";
  readonly children: NdInlineNode[];
}

interface NdHeaderTextBlock {
  readonly type: "header_text_block";
  readonly children: NdInlineNode[];
}

interface NdDisclaimerBlock {
  readonly type: "disclaimer_block";
  readonly children: NdInlineNode[];
}

interface NdSemanticBlock {
  readonly type: "semantic_block";
  readonly id: string;
  readonly children: NdInlineNode[];
}
```

`~~~=`, `~~~*`, `~~~/`, `~~~_`, `~~~?`, `~~~!`, `~~~'`, `~~~#`, `~~~^`, and `~~~(id)` create
highlight, strong, emphasis, underline, hint/question, attention/admonition, comment, header-text,
disclaimer, and semantic blocks respectively. Each requires non-empty rich inline content. Every
form closes with the same exact opener except `~~~^` and `~~~(id)`, whose closer is plain `~~~`.
Empty and unclosed forms reject with family-specific diagnostics. Plain `~~~` has no opening-block
meaning and remains inherited ordinary paragraph text in both v1 and v2. Header-text and disclaimer
blocks are untagged. Semantic IDs use the shared `v2-id` grammar, remain available in the AST, and
are not emitted into the reference HTML. Inline `[(id) content]` uses the same rule and projects only
its rich content by default. Cards are separate block-content containers rather than paired inline
paragraph blocks.

## 17. Structural Escapes

At a block-open position in v2, one leading backslash suppresses recognition of the block command
that immediately follows it. The backslash is lexical and absent from the AST; the decoded command
text becomes an ordinary paragraph. Covered commands include headings, unordered and ordered lists,
blockquotes, horizontal rules, extension blocks, inherited backtick code fences, v2 `~~~$` code
fences, v2 tilde paired/semantic/card blocks, and removed tilde-language openers. A table header continues to use
the inherited `\|` escape on its first pipe.

````and
\# literal heading
\- literal list item
\1. literal ordered item
\> literal quote
\---
\+++chart/pie
\```aeon
\~~~$ aeon
\~~~aeon
\~~~#
\~~~(note)
````

The escape is valid only when removing it would expose a structural opener at that position. It is
therefore invalid mid-paragraph and invalid before ordinary text such as `#hashtag` or plain `~~~`.
Core v1 retains its existing escape set and rejects these new structural escapes. Canonical v2
output reinserts the leading backslash whenever decoded paragraph text would otherwise reparse as a
block; table-shaped escaped paragraphs retain the line breaks required for the same fixed point.

## 18. Canonical Contract

Canonical emission requires both a profile and an effective version:

```js
emitCanonical(document, { profile: "standalone", version: "v2" });
emitCanonical(document, { profile: "embedded", version: "v2" });
```

Standalone v2 output begins with `&ND v2`; embedded output omits the declaration. Every promoted v2
node has a deterministic spelling, and emitting a v2-only node under version v1 MUST fail. The
executable proposal runner checks standalone and embedded parse–emit–parse structural equivalence
and canonical fixed-point stability for every accepted v2 fixture.

Machine-readable contract `and-v2-projection-v1` in the reference implementation's
`cts/contracts/v2-projection-v1.json` pins exact standalone and embedded canonical text plus inert
HTML for every promoted node family, marker state, image mode, nested composition boundary, and
unsafe-resource case. Its mandatory checker rejects missing coverage identifiers and any byte-level
snapshot drift. The same contract indexes the required cross-form combinations: each paired block in
lists and blockquotes, representative rich children in each paired block, local links crossing
container boundaries, rich resource nesting, contextual list-item content, leading directional
bullet replacement, heading-number hierarchy, rich/reused footnotes, code-block language and
numbered-line intent, cards with rich titles and block children, and rich children in every
formatted paragraph family.

## 19. Source Spans

When spans are requested, v2 nodes use the same optional `span` field and normalized source-offset
rules as v1 nodes. Spans are metadata and are excluded from structural round-trip comparison.
Contract `and-v2-projection-v1` pins 46 exact span assertions covering every promoted scalar and rich
inline family, heading auto-numbering, all paired blocks, escaped fields, datatype generics and
clarifiers, footnotes, code blocks, cards, aligned/spanning tables, nested rich resources, lists, and blockquotes.

## 20. Stability

This contract is executable but remains proposal-stage. The scalar-versus-rich-content split and
the capability disposition above are now decisions for the first-draft candidate; lexical
constraints and projection snapshots may still tighten before v2 advances to draft.
