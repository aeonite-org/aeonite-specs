# Aeonite specification-document profile v1

Status: incubation contract

## Ownership boundary

AEON owns publication metadata. Embedded `&ND v2` owns the complete prose document and its AST.
The normalized AEON representation of an &ND AST may be emitted later as an interchange artifact,
but it is not the human-authored source.

## Required AEON bindings

| Binding | Contract |
| --- | --- |
| `schemaVersion:string` | Exactly `"1"` |
| `id:string` | Stable document identifier |
| `title:string` | Display title; must match the first level-one &ND heading |
| `description:string` | Search and page metadata description |
| `created:date` | Earliest known canonical-source creation date |
| `modified:date` | Latest substantive source modification date |
| `family:string` | Specification family |
| `group:string` | Navigation group within the family |
| `standing:string` | `official`, `supplemental`, or `external` publication standing |
| `lifecycle:string` | `proposal`, `draft`, `published`, `retired`, or `superseded` |
| `normativity:string` | `normative`, `informative`, or `mixed` |
| `license:string` | SPDX-style publication license identifier |
| `path:string` | Stable publication path without a leading slash |
| `order:number` | Non-negative integer navigation order |
| `publish:boolean` | Whether the document belongs in publication artifacts |
| `keywords:list<string>` | Search aliases and vocabulary |
| `related:list<string>` | Other document IDs; all targets must exist |
| `bodyFormat:string` | Exactly `"and-v2"` |
| `body:prose` | Standalone `&ND v2` source |

Metadata deliberately separates standing, lifecycle, and normativity. Terms such as “official”,
“normative”, and “draft” must not be collapsed into one heuristic status badge.

`created` and `modified` are ISO 8601 calendar dates in `YYYY-MM-DD` form, and `created` must not be
later than `modified`. For migrated documents, `created` comes from the date of the earliest author
timestamp in the canonical `aeonite-specs` Markdown history, following renames. `modified` is the
later of the final canonical
Markdown change and any subsequent substantive AEON-source change. The format migration itself and
date-only maintenance do not alter `modified`. Documents without a canonical Markdown source
use their AEON-source history. `metadata/document-date-provenance.json` records the exact paths and
commits used for the migration audit.

## &ND document rules

The embedded body must:

1. parse successfully with the strict v2 proposal parser;
2. begin with one level-one heading matching `title`;
3. give every heading an explicit trailing `[# id]` anchor;
4. satisfy document-wide anchor and footnote validation;
5. separate a list from preceding prose with a blank line, so a line-leading list marker cannot be
   silently retained as paragraph text.

The explicit heading-anchor rule is a publication-profile constraint, not new &ND syntax. It keeps
website links, generated Markdown, and search results stable when wording changes.

```and
# Readable Heading [# stable-heading-id]
```

## Embedded AEON example classification

Every embedded AEON code block uses the language identifier `aeon`. The identifier exists for
downstream syntax highlighting and must not encode test expectations or editorial categories.

Audit exceptions live in `contracts/aeon-example-expectations.json`, keyed by the stable form
`document-id#heading-anchor:ordinal`. Examples absent from the manifest default to
`valid-document`.

| Classification | Meaning | Audit assertion |
| --- | --- | --- |
| `valid-document` | Complete AEON document example | Must compile and finalize to strict JSON |
| `intentional-rejection` | Intentional rejected input | Must fail structural compilation |
| `strict-json-incompatible` | Valid AEON whose meaning is not losslessly representable by strict JSON | Must compile and then report a finalization incompatibility |
| `illustrative-fragment` | Illustrative address, grammar, placeholder, or other non-document excerpt | Observed diagnostics are recorded but no document-conformance result is asserted |
| `independent-examples` | Multiple independent alternatives collected in one code block | Aggregate diagnostics are recorded but the block is not treated as one document |

Authors should prefer complete examples and focused intentional rejections. Use fragments and
collections only when wrapping or splitting the material would make the specification less readable.
The audit rejects stale manifest IDs, uses portable capability floors for structural depths instead
of implementation default resource locks, and allows custom datatype labels so unrelated profile
policy does not determine Core example validity.

## Projection rules

HTML uses the fail-closed `and-core` reference renderer. The build emits both a fragment and a plain
standalone page. Every standalone page includes static, relative navigation to the document index
and search page plus its family and group context. These links do not require server-side includes,
rewrites, or a fixed deployment root, so the artifact tree can be served directly by a PHP host.

Markdown is a compatibility projection rather than a round-trip serialization. Native Markdown is
used where semantics align. GFM footnotes and task items are used where possible; small raw-HTML
forms preserve underline, highlight, image mode, disclaimers, collapsible cards, and table spans.
Canonical &ND remains the lossless prose representation.

For published targets, the consumer projects `related` metadata as title-based navigation after the
document body: HTML uses a navigation landmark and Markdown uses a generated related-documents
section. Relationships to retained but unpublished documents remain catalog metadata and are not
emitted as broken artifact links.

Cross-document publication links use the consumer-owned target form `document:<id>` or
`document:<id>#<anchor>`. Collection validation resolves the document ID and optional anchor after
all document trees have been built. HTML projects the target to a sibling `.html` artifact and
Markdown projects it to a sibling `.md` artifact; standalone &ND preserves the abstract target.
Authored `./*.md` link targets are rejected because they cannot work in every projection. Relative
`../assets/` targets remain accepted for compatibility, but human-authored publication documents
should use root-relative `/artifacts/assets/<path>` targets. Both forms are accepted only when the
corresponding checked-in publication asset exists.

Search is section-level. Index entries retain punctuation-bearing code terms so searches for tokens
such as `[@]`, `max_attribute_depth`, and `:toggle` are not reduced to ordinary prose words.

## Non-prose publication resources

Authoritative machine contracts are not wrapped in the prose-document envelope. They live under
`resources/` and are copied byte-for-byte to `generated/assets/`.

The v1 contract bundle must contain a JSON registry plus its referenced AEON profile/schema files.
Every publication build fails closed unless:

1. registry paths are relative, traversal-free `.aeon` paths;
2. contract IDs are unique and kinds, versions, hashes, and statuses are valid;
3. every referenced artifact exists and parses as AEON;
4. the artifact ID and version match its registry entry; and
5. the SHA-256 digest matches the registry.
