---
id: and-v2-consumer-conventions
title: "&ND Core v2 Consumer-Conventions Boundary"
description: Non-Core ownership boundary for vocabularies, presentation, workflow, resources, navigation, and extension behavior layered on &ND Core v2.
family: and
group: "&ND"
status: Proposal
path: specification/and/core-v2-consumer-conventions
license: CC-BY-4.0
---

# &ND Core v2 Consumer-Conventions Boundary

This companion note separates fixed `&ND Core v2` parsing and canonicalization from meanings owned by
applications, rendering profiles, workflow systems, and trust policies.

“Consumer-owned” does not mean optional grammar. Core always supplies the stable AST field and
canonical spelling. Core does not supply the vocabulary, presentation, workflow effect, network
behavior, or execution policy layered on that field.

## 1. Processing Order

A conforming consumer:

1. parses and validates under the declared or host-selected Core version;
2. retains the Core AST without reinterpreting its fields;
3. applies an explicitly selected consumer convention or product policy.

A convention registry MUST NOT make invalid Core syntax valid, turn valid syntax into a Core parse
error, rewrite Core canonical text, or infer the grammar version.

## 2. Supported Convention Surfaces

| Surface | Core guarantees | Consumer owns |
| :------ | :-------------- | :------------ |
| `[! ...]` | Rich `admonition_tag` children | Severity vocabulary, styling, labels, accessibility phrasing, workflow |
| `[? ...]` | Rich `question_tag` children | Question, hint, review, help, or task behavior |
| `[+ value]` | Preserved scalar `plus_tag.value` | Value registry, action mapping, analytics, workflow, UI |
| Custom `[:type = scalar]` | Datatype label/adornments and validated scalar | Datatype registry, domain validation, units, formatting, business meaning |
| `===tag`, `***tag` | Validated optional paired-block `tag` | Tag vocabulary, templates, placement, styling, behavior |
| heading `[n]`, `auto_number_list` | Contextual auto-number intent | Sequence, scope, format, restart rules, localization, labels |
| Footnote definitions and references | Rich definition content, optional authored ID, declaration order, reference resolution | Superscript numbers or symbols, hover/callout/endnote presentation, placement, backlinks, accessibility phrasing |
| `[~ source | alt | mode]` | Source, alt text, and closed display-intent mode | Resolution, fetching, caching, MIME checks, intrinsic sizing, exact layout, failure UI |
| External `[@ target | label]` | Target and rich label | Scheme policy, navigation, previews, tracking, trust prompts |
| `+++name` extension block | Opaque inherited name and payload | Registry, interpretation, sandbox, permissions, execution |
| `todo_list` / `todo_item` | First-class list structure and stable item-state enum | Controls, mutation workflow, progress, icons, labels, persistence |
| Directional markers | Stable direction enum and leading-unordered-item bullet-replacement intent | Navigation or workflow meaning, arrow styling, labels, interaction |
| Inline comments | Preserved rich comment children | Visibility, identity, export, redaction, collaboration workflow |

Core itself owns local-anchor identifier validation, uniqueness, case-sensitive matching, and
whole-document fragment resolution. Consumers own scrolling, focus, history, and navigation UI after
resolution succeeds.

## 3. No Implicit Vocabulary

Core assigns no registered product meaning to values such as:

```and
[+ priority:high]
[! security]
===hero
***legal
[:temperature = 21.5]
```

A product may define these conventions separately. Another product may preserve the same AST while
presenting it differently or taking no action. Convention registries are outside the first v2 Core
draft and should be independently named and versioned.

## 4. Numbering

Heading `[n]` and `auto_number_list` record author intent; Core does not calculate a number. A
numbering profile should define
participating nodes, sequence scope, restart and nesting rules, formatting and localization, and
whether hidden nodes consume a number. Derived numbers belong to a projection, not to the parsed
Core AST.

## 5. Footnotes

Core distinguishes anonymous definitions, named definitions, and references to already-declared
named definitions. Authored IDs are identity keys, not requested display labels. Consumers own
sequence scope, displayed numbers or symbols, hover/callout/endnote presentation, placement,
backlinks, accessibility phrasing, and repeated-reference behavior. Projection choices must not
alter Core reference resolution or imply calculated labels were present in source.

## 6. Images

Image modes are portable intent rather than exact geometry:

- `inline` requests alignment at surrounding text height;
- `half` requests half the source's original height;
- `full` requests the source's original height.

Consumers define fallbacks when intrinsic height is unavailable. Core performs no file or network
access, authentication, byte inspection, or MIME validation. Alt text remains mandatory and should
remain available when a source is rejected or fails to load.

The reference HTML renderer's URL filtering and base-resolution option are non-normative projection
policy, not additional Core semantics.

## 7. Links and External Resources

Core distinguishes resolved local `#id` targets from other link targets. A consumer must apply an
allowlist or equivalent navigation policy before activating an external target. Successful parsing
does not establish safety, reachability, or trust.

`[+]` may describe a resource in a consumer vocabulary, but it does not acquire implicit navigation
behavior and is not a substitute for Core link syntax.

## 8. Extensions and Execution

Core documents are non-executable. Opaque extension blocks preserve data; they do not authorize
evaluation. Interpretation or execution requires an explicit registry and trust policy, validated
payloads, isolated effects, and environment permissions.

Unknown extensions, `[+]` values, custom datatypes, and paired-block tags remain preservable data and
must not trigger behavior merely by appearing in a valid document.

## 9. Conformance Boundary

Core conformance covers grammar-version acceptance, AST fields, local-anchor integrity, canonical
spelling, and requested spans or budgets. A consumer profile covers behavior only after a valid Core
parse and must be tested and versioned separately. The inert reference HTML projection demonstrates
one safe approach, but its classes, styling, and interactions are not normative Core requirements.
