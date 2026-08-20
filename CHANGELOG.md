---
license: CC-BY-4.0
---

# Changelog

All notable changes to `aeonite-specs` are tracked here.

This changelog follows the release-governance sections used by the AEON v1 draft governance policy:

- Added
- Changed
- Fixed
- Removed
- Spec Impact
- CTS Impact

## Unreleased

- Added proposal-stage v2 structural block escapes: a leading `\` at a block-open position quotes a
  real heading, list, quote, rule, extension, raw-fence, paired-fence, or semantic-fence opener as
  ordinary paragraph text while leaving the global inline escape set closed.
- Added proposal-stage semantic wrappers: `~~~(id)` / `~~~` blocks and `[(id) content]` inline text.
  Their IDs are retained for consumers but omitted from the reference HTML projection.
- Replaced the proposal-stage `===` and `***` v2 paired blocks with untagged `~~~#` header text and
  `~~~^` / `~~~` disclaimer blocks, and added rich inline `[^ ...]` disclaimers.
- Added `~~~'` as a proposal-stage rich block comment in &ND v2; consumers control visibility and
  the reference HTML projection preserves it as hidden content.
- Added language-qualified `~~~language` and `~~~~language` code-fence alternatives to &ND v1 and
  inherited v2 parsing while preserving bare `~~~` as paragraph text.
- Added contextual `- [?]` / `- [!]` advisory list markers, visible `~~~?` / `~~~!` advisory
  paragraphs, and clarified that inline `[? ...]` / `[! ...]` presentation remains consumer-owned.

### Added

- Added proposal-stage `&ND` v1-to-v2 migration and v2 consumer-conventions documents, covering the
  asymmetric parser boundary, mechanical syntax migration, supported v2 surface, and the explicit
  split between Core fields and consumer-owned behavior.
- Added the proposal-stage `&ND Core v2` AST contract, including effective-version metadata,
  promoted node shapes, and canonical emission boundaries.
- Added initial SANSA v1 draft specification tree under `sansa/v1/drafts/`.
- Promoted SANSA Addressing and Resolve documents to draft status.
- Added SANSA lifecycle placeholders for `sansa/v1/proposals/` and `sansa/v1/published/`.

### Changed

- Clarified that v2 local-fragment integrity is a second-pass document validation rule, omitted image
  modes intentionally normalize to explicit `inline`, `autoNumber?: true` is an additive opt-in AST
  field, and `[.]` is solely a line-break node rather than a directional marker.
- Replaced generic inline todo markers in the `&ND Core v2` proposal with homogeneous first-class
  `todo_list` and `todo_item` structures introduced by exact `- [state] content` prefixes.
- Made `[n]` contextual to headings and first-class `auto_number_list` blocks.
- Promoted `[% content]`, `[% (id) content]`, and `[% (id)]` as anonymous/named footnote definitions
  and backward named references, while leaving labels and presentation to processors.
- Allowed immediate two-space nested lists in v2 and made the reference HTML projection visibly
  calculate hierarchical numbers for opted-in headings.
- Defined leading `[>]` and `[<]` markers in unordered items as contextual bullet replacements while
  retaining their existing inline AST and later-marker behavior.
- Extended the formatted paragraph fence family with `~~~*` strong, `~~~/` emphasis, and `~~~_`
  underline blocks while keeping plain `~~~` as ordinary paragraph text.
- Updated the `&ND Core v2` proposal to record the executable parser, canonical, HTML, budget,
  extension, and strict forward-compatibility boundaries.
- Consolidated the `&ND Core v2` first-draft candidate surface into Core, Core-syntax-plus-convention,
  and deferred dispositions; content-bearing inline tags now use rich `children` while identifiers
  and metadata remain scalar.
- Defined local navigation through inherited `[@ #id | label]` links to `[# id]` anchors, with a
  portable ID grammar, forward links, document-wide uniqueness, and strict unresolved-target errors;
  external resources continue to use ordinary `[@ target | label]` links.
- Promoted `[~ source | alt | mode]` as the v2 inline-image form with mandatory alt text, an
  `inline` default, closed `inline`/`half`/`full` display intents, and deterministic canonical output.
- Defined image-source resolution as a consumer boundary: Core preserves authored sources, while the
  reference HTML renderer offers explicit credential-free HTTP(S) `imageBaseUrl` resolution,
  source-provenance metadata, and fail-closed URL handling.
- Audited `&ND` v2 first-draft readiness, separating the healthy executable grammar and tooling
  surfaces from remaining publication blockers: embedding/API contract text, exact projection
  snapshots, broader spans and combinations, migration guidance, and consumer conventions.
- Closed all documented `&ND` v2 first-draft candidate gates while retaining proposal lifecycle
  status pending an explicit reviewed promotion of formal documents and CTS metadata.
- Froze headerless v2 selection as a host-controlled typed-channel operation requiring both reader
  capability and explicit effective version, with source declarations taking precedence, and added
  the corresponding v2 public API contract and boundary checks.
- Added machine-readable projection contract `and-v2-projection-v1`, pinning complete promoted-surface
  coverage through exact standalone/embedded canonical and inert HTML snapshots, including nested,
  image-resolution, full-document, and unsafe-resource cases; the contract now also pins 34 exact
  source-span assertions and a 24-entry cross-form interaction matrix.
- Replaced the provisional equals-free `&ND` typed-value spelling with exact AEON
  `[:type = scalar]` syntax, a closed inline-scalar family list, structured datatype adornments,
  reserved type/literal compatibility checks, and AEON-canonical scalar output.
- Pinned the `&ND` v2 inline-scalar boundary as machine-readable contract
  `and-v2-aeon-inline-scalar-v1`, aligned with AEON TypeScript `0.12.0`, with mandatory AST,
  canonical, HTML, alias, and exclusion checks plus an optional live AEON drift check.
- Changed AEON draft encoding-family literal syntax from `$payload` to `&payload`.
- Changed NEON draft AEON integration examples and text-preservation guidance to use `&...` encoding literals.
- Expanded Shared AEON Value Semantics proposal with explicit profile-selection, string collation, temporal comparison, and mutation-compatibility guidance.
- Added a value-family semantic classification table covering AEON Core reserved value families, references, separator literals, SANSA literals, containers, and custom datatype labels.
- Added the missing `nan` entry to the AEON v1 reserved datatype-name table to match existing NaN examples and compatibility text.
- Clarified toggle semantics: toggle-token equality is exact, while Boolean compatibility requires explicit conversion or a profile-defined comparison domain.
- Broadened `isValue(...)` semantics to mean any concrete value outside the non-value group, rather than only finite number/string/Boolean scalar values.
- Clarified hex semantics: `HexLiteral` is distinct from `RadixLiteral`, canonical hex-payload identity is not numeric/radix/color/byte equality, and richer interpretations require explicit profiles.
- Clarified that `radix16` is not a reserved Core v1 shorthand; base-16 radix values use `radix[16]` and remain distinct from `hex`.
- Clarified encoding semantics: `EncodingLiteral` has payload-string identity by default, `base64` is not `radix[64]`, and decoding, byte identity, media type, and text interpretation require explicit profiles.
- Added encoding-family naïve payload order over preserved encoded payload characters.
- Added separator-literal naïve order over canonical separator payloads, while reserving IP, version, dimension, delimited-record, and other domain ordering for explicit profiles.
- Clarified that naïve separator order never splits payloads, and profile-defined splitting/order must treat separator specs as claims unless trusted or validated.
- Clarified SANSA address-literal semantics: address-expression identity/order are syntactic defaults, while exact target identity, selector equivalence, resolution, and AEON versus non-AEON namespace meaning belong to consumers.
- Strengthened SANSA namespace- and domain-neutrality language, clarifying that SANSA member selectors describe semantic traversal rather than AEON object traversal.
- Clarified structural container semantics for `object`, `list`, `tuple`, and `node`, including minimum structural equality, lack of default structural ordering, and schema/profile ownership of mutation compatibility.
- Clarified reference semantics by separating reference-form identity, read-only followed-value inspection through conceptual `follow(reference)`, and reference resolution/materialization.
- Renamed the schema proposal's reference-inspection control from `resolve_reference_form` to `follow_reference_form` to avoid implying materialization or value substitution.
- Clarified SANSA.Query consumes active Shared AEON Value Semantics profiles for ordering, comparison, case mapping, and future temporal behavior.
- Aligned Shared AEON Value Semantics proposal-stage profile identifiers with the implementation surface, including `aeon.value.default.v1`, `aeon.value.string.codepoint.v1`, `aeon.value.string.natural.ascii.v1`, and explicit locale profile examples such as `aeon.value.string.locale.fr.v1`.
- Updated the repository README layout to include SANSA as a first-class specification family.
- Updated the repository README to point to this changelog as the release-facing change history.

### Fixed

- None.

### Removed

- None.

### Spec Impact

- Makes the current v2 implementation shape reviewable without promoting v2 beyond proposal stage.
- Introduces draft SANSA specification text for semantic addressing and deterministic structural resolution.
- Keeps read-only SANSA Query semantics in proposal status while the query surface continues to evolve.
- Starts the encoding-family literal migration by reserving `&` for `encoding`, `base64`, `embed`, and `inline` payload literals in draft spec text.
- Keeps the payload alphabet and payload capture semantics unchanged; the payload excludes the literal prefix.
- Frees `$` for the planned SANSA address literal in the AEON language specification.
- Establishes Shared AEON Value Semantics as the common prerequisite for SANSA.Query temporal comparison and future SANSA.Mutate typed write compatibility.
- Clarifies that separator literals and other textual source forms do not automatically fall back to string semantics; domain-specific comparison requires an active profile.
- Prevents `yes`, `on`, `no`, and `off` from being collapsed into Boolean equality by default.
- Defines the minimum non-value group for value predicates as Missing, explicit null, explicit absence values, and NaN.
- Prevents `hex` from being treated as a shorthand for `radix[16]` or another radix family by default.
- Keeps base-16 radix intent explicit through `radix[16]` rather than adding a potentially confusing `radix16` alias.
- Prevents encoding-family values from being treated as decoded bytes, decoded text, radix values, or generic string collation inputs by default.
- Gives encoding-family values a deterministic portable fallback order without assigning decoded-byte, decoded-text, media, hash, or radix meaning.
- Gives separator literals a deterministic portable fallback order without assigning domain meaning to separator characters.
- Prevents document-local separator clarifiers such as `sep["."]` from silently authorizing semantic splitting, IP parsing, version parsing, or domain ordering.
- Prevents AEON-hosted `:sansa` values from being treated as AEON paths by default when they may target another SANSA-compatible semantic namespace.
- Makes AEON's relationship to SANSA explicit as an AEON binding-model namespace adapter rather than the owner of SANSA traversal semantics.
- Defines minimum structural equality for objects, lists, tuples, and nodes while keeping list/tuple coercion, structural ordering, and mutation behavior explicit.
- Prevents implicit reference following in comparison and validation contexts while keeping reference resolution/materialization separate from explicit read-only followed-value checks.
- Migration: update encoding-family literals from `$payload` to `&payload`.

### CTS Impact

- The local v2 proposal runner now checks declared and embedded parsing, v1 compatibility,
  canonical fixed points, HTML projection, nested contexts and rich inline content, inline and
  paired-block budgets, document-local fragment integrity, opaque extensions, and unpromoted syntax.
- Updated proposal-stage Value Semantics CTS expectations so `isValue(...)` follows the concrete-value basis, including accepting infinity and container values while excluding Missing, explicit null, explicit absence values, and NaN.
- Added proposal-stage Value Semantics CTS coverage for portable `aeon.value.default.v1` and `aeon.value.string.codepoint.v1` profile selection.
- Updated SANSA.Query CTS expectations to align query `isValue(...)` behavior with the Shared AEON Value Semantics concrete-value basis.
- Future CTS work is expected for SANSA address parsing/canonicalization and the AEON encoding literal prefix migration.
