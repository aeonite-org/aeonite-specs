---
id: aeon-core-v1-compliance
title: AEON Core v1 Compliance Specification
description: Conformance requirements for implementations, including required syntax support, reference legality, policy controls, and canonical rendering rules.
group: Core Specifications
path: specification/aeon-v1-documentation/aeon-core-v1-compliance-specification
links:
  - aeon-core-v1
  - aeos-v1
  - aeon-v1-conformance-matrix
---

# AEON Core v1 Compliance Specification

Status: official v1 compliance draft  
Scope: normative conformance requirements for AEON core implementations. AEOS-specific compliance is tracked separately.

## 1. Normative Language

The terms MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, and MAY are to be interpreted as normative requirements.

## 2. Conformance Target

An implementation claiming AEON v1 core conformance SHALL satisfy:
- language requirements in `AEON-spec-v1.md`
- requirements in this compliance document
- `cts.protocol.v1` runner and lane requirements in `cts/protocol/v1`
- all REQUIRED CTS suites in the published v1 lane manifests relevant to the claimed surface:
  - `cts/core/v1/core-cts.v1.json`
  - `cts/aes/v1/aes-cts.v1.json`
  - `cts/canonical/v1/canonical-cts.v1.json` when canonical formatting is claimed
  - `cts/annotations/v1/annotation-stream-cts.v1.json` when annotation-stream behavior is claimed
  - `cts/aeos/v1/aeos-validator-cts.v1.json` when AEOS validator conformance is claimed

CTS is the public conformance authority for AEON v1. Stress, smoke, timing, fuzzing, and hardening workflows MAY be used for implementation quality and security review, but they are not separate conformance authorities unless their cases are explicitly promoted into the published CTS manifests.

Core conformance SHALL be evaluated against backbone behavior families, not only by isolated test-file success.

The current backbone families are:
- canonical rendering and node normalization
- fail-closed parsing and deterministic rejection behavior
- addressing and canonical path semantics
- quoted-key and traversal disambiguation
- attribute traversal and attribute-depth semantics
- annotation attachment and slash-channel binding
- strict literal acceptance and rejection boundaries
- separator/path literal handling
- datatype-to-literal validation behavior

The current anti-drift coverage accounting for those families is tracked in `aeonite-cts/CONFORMANCE-COVERAGE.md`.

## 3. Syntax and Key Requirements

Implementations MUST:
1. accept bare, single-quoted, and double-quoted keys in all key positions;
2. reject backtick-quoted keys as keys;
3. reject empty quoted keys;
4. reject malformed quoted-key escape sequences;
5. preserve key/path disambiguation between dotted traversal (`a.b`) and quoted single-key (`["a.b"]`);
6. recognize the document header only at the start of the document;
7. reject a structured header (`aeon:header = { ... }`) that appears after any body binding.

## 4. Addressing and Reference Requirements

Implementations MUST:
1. support canonical path identity segments for member and index;
2. support quoted member segments and quoted attribute selectors in addressing expressions;
3. support attribute reference forms (for example `~a@b`);
4. support mixed member traversal with quoted bracket member segments after `.` (for example `~a.[\"b.c\"]`, `~a@meta.[\"x.y\"]`, `~a@[\"x.y\"].z`);
5. reject empty quoted path or attribute segments deterministically;
6. reject malformed or incomplete addressing forms deterministically, including examples such as `~a@`, `~$.a@[`, and `~.[\"a\"]`;
7. reject missing reference targets deterministically;
8. reject forward references deterministically;
9. reject self-references deterministically.

Implementations MUST also:
1. treat attributes as binding-attached metadata, not canonical path identity segments;
2. allow binding-attached attributes on bindings that resolve to container values;
3. allow attribute addressing for nested bindings inside containers when the nested binding is itself addressable;
4. reject postfix literal-attribute forms such as `a = [0]@{b=2}` deterministically;
5. support nested attribute heads within configured `max_attribute_depth`.

## 5. Depth Policy Requirements

Implementations MUST:
1. expose `max_attribute_depth`, `max_separator_depth`, and `max_generic_depth` controls;
2. provide capability floor of at least `8` for all three controls;
3. default all three controls to lock value `1`;
4. fail closed when configured limits are exceeded;
5. emit deterministic diagnostics for depth-policy violations.

## 6. Comment and Annotation Requirements

Implementations MUST:
1. treat `/* ... */` as plain comments;
2. support slash-channel structured block forms (`/# #/`, `/@ @/`, `/? ?/`, `/{ }/`, `/[ ]/`, `/( )/`);
3. before Phase 1 parsing, ignore at most one leading UTF BOM before any comment or preamble inspection;
4. accept `#!...` as a plain comment only at line 1, column 1 after any ignored leading BOM;
5. recognize `//!` as a host/file-header directive only at line 1, column 1, or line 2, column 1 when line 1 is a shebang, after any ignored leading BOM;
6. treat `//! format:<id>` as processor-discovery-only metadata in that file-header slot;
7. keep file-header host directives out of AES, annotation-stream output, and canonical output;
8. preserve deterministic binding behavior for annotation channels where emitted.

## 7. Typed-Mode Requirements

In typed modes (`strict` and `custom`) implementations MUST:
1. enforce `switch` datatype lock for switch literals;
2. reject custom datatype aliases for switch literals;
3. enforce canonical attribute+datatype ordering: `key@{...}:type = value`;
4. reject reversed ordering (`key:type@{...}`).

### 7.1 Explicit Datatype Compatibility

Implementations MUST:
1. validate explicit datatype/literal compatibility independent of mode;
2. allow untyped bindings in transport mode;
3. require datatype presence in typed modes (`strict` and `custom`);
4. emit deterministic mismatch diagnostics when an explicit reserved datatype does not match the bound literal kind.

### 7.2 Mode-Driven Datatype Acceptance

Implementations MUST:
1. allow custom datatype labels in transport mode;
2. reject custom datatype labels by default in strict mode;
3. allow custom datatype labels in custom mode.

Implementations MAY expose an explicit datatype-policy override as a tooling or runtime option, but the default Core behavior MUST follow the declared document mode.

### 7.3 Canonical Rendering Requirements

Canonical emitters MUST:
1. preserve canonical binding ordering `key@{...}:type = value`;
2. preserve canonical node-head ordering `tag@{...}:datatype`;
3. elide redundant explicit root prefixes in rendered references (`~$.a` -> `~a`, `~>$.a` -> `~>a`);
4. collapse quoted reference selectors to bare identifier form when the decoded segment is already a canonical bare identifier;
5. preserve multiline trimticks only in multiline canonical layouts and render inline trimtick-normalized values as ordinary escaped strings when required by inline layout.
6. render nested object values as multiline canonical blocks when the enclosing canonical object or list layout is multiline, while still sorting keys lexicographically at every level.

## 8. Radix and Encoding Literal Requirements

Implementations MUST:
1. distinguish radix-literal lexical rules from encoding/base64 lexical rules;
2. accept radix payload digits only from `0-9`, `A-Z`, `a-z`, `&`, and `!`;
3. accept optional radix leading sign `+` or `-` only at the start of the payload;
4. accept at most one radix decimal point `.` and only between non-empty digit runs;
5. treat `_` in radix literals as visual spacing valid only between radix digits;
6. reject radix payload characters `/` and `=`;
7. accept `encoding`-family payloads (`encoding`, `base64`, `embed`, `inline`) in both standard base64 (`+` and `/`) and URL-safe base64 (`-` and `_`) forms;
8. canonicalize `encoding`-family payloads to the URL-safe alphabet by rewriting `+` as `-` and `/` as `_`, and strip trailing `=` padding;
9. continue to treat lexical acceptance as distinct from downstream base-specific radix or base64 semantic validity.

## 9. Separator-Literal Requirements

Implementations MUST:
1. support repeatable separator specs (`[...]`)+;
2. enforce separator character constraints (single printable ASCII, excluding `,`, `[` and `]`);
3. allow horizontal whitespace and newlines around the separator character inside brackets, while still rejecting any form that makes the payload non-contiguous or longer than one character;
4. preserve repeated separator specs structurally, including duplicate chars;
5. treat `;` as separator-literal payload data rather than a terminator;
6. terminate raw separator literals deterministically on grammar boundaries appropriate to the enclosing context;
7. support only the raw separator escapes `\\`, `\\,`, and `\\ `;
8. accept trailing delimiter payload as raw core content;
9. treat comment-like substrings inside raw separator payload as payload text rather than comment openers;
10. reject raw separator payloads containing `[` `]` `{` `}` `(` or `)`.

## 10. Temporal Literal Requirements

Implementations MUST:
1. treat temporal range validity as part of literal recognition rather than a later semantic-only phase;
2. reject `date` literals with invalid month/day combinations;
3. support leap-year date validity for February 29;
4. reject `time` literals whose hour is outside `00-23`;
5. reject `time` literals whose minute or second is outside `00-59`;
6. apply the same bounded calendar/clock rules when recognizing `datetime` literals;
7. continue to accept the Core v1 partial forms already admitted by grammar shape, including hour-precision `time` (`09:`) and `datetime` (`2025-01-01T09`);
8. allow UTC/offset suffixes on valid reduced-precision time forms, including `09:30Z`, `09:+02:00`, and `09:30+02:00`;
9. allow UTC/offset suffixes on valid reduced-precision `datetime` forms, including `2025-01-01T09Z`, `2025-01-01T09+02:00`, and `2025-01-01T09:30Z`;
10. allow named-zone ZRUT suffixes on valid reduced-precision datetime bases, including `2025-01-01T09&Europe/Belgium/Brussels`, `2025-01-01T09Z&Europe/Belgium/Brussels`, `2025-01-01T09:30Z&Local`, `2025-01-01T09Z&America/Port-au-Prince`, and `2025-01-01T09Z&Etc/GMT+1`, and classify them as `zrut` literals;
11. treat uppercase `Z` as the UTC marker form and reject lowercase `z` as a temporal literal marker.

Examples:
- valid: `2024-02-29`, `09:`, `09:30`, `09:30Z`, `09:+02:00`, `2025-01-01T09Z`, `2025-01-01T09+02:00`, `2025-01-01T09&Europe/Belgium/Brussels`, `2025-01-01T09:30Z&Local`, `23:59:59`, `2024-02-29T09:30:00`
- invalid: `2025-02-29`, `2025-13-40`, `24:00`, `99:99`, `23:59:60`, `09:30z`, `2025-01-01T09:30Z&/`

## 11. Node Requirements

Implementations MUST:
1. accept node forms `<tag(...)>` and empty-node shorthand `<tag>`;
2. require the closing `>` for child-bearing node forms and reject `<tag(...)` deterministically;
3. in strict mode, reject inline node-head datatypes other than `:node`;
4. in transport/custom modes, continue to accept non-`node` inline node-head datatypes as syntax, for example `<tag:pair("x", "y")>`;
5. reject other node-like forms deterministically.

## 12. Duration Boundary

Implementations MUST NOT treat bare duration tokens as AEON core v1 literals.

Duration semantics, when needed, are schema/profile/consumer-layer concerns and are outside AEON core conformance scope.

## 13. CTS Protocol Requirements

Conformance execution MUST use `cts.protocol.v1`:
- `cts/protocol/v1/runner-contract.md`
- `cts/protocol/v1/lane-core.md`
- `cts/protocol/v1/lane-aes.md`
- `cts/protocol/v1/lane-annotations.md`
- `cts/protocol/v1/lane-canonical.md`

Published AEON v1 CTS coverage currently includes:
- canonical formatting baseline and node canonicalization in `cts/canonical/v1`
- core baseline, addressing/reference, fail-closed, transport-acceptance, and syntax-invalid suites in `cts/core/v1`
- AES baseline, addressing/reference, strict failure envelope, and transport emission suites in `cts/aes/v1`
- annotation-stream conformance in `cts/annotations/v1`
- AEOS validator conformance in `cts/aeos/v1`

## 14. Numeric Lexical Requirements

Implementations MUST enforce numeric underscore placement rules:
1. `_` MAY appear only between digits;
2. leading `_` is invalid;
3. trailing `_` is invalid;
4. consecutive underscores are invalid;
5. underscore adjacent to non-digit numeric separators is invalid.

Examples:
- valid: `100_000`
- invalid: `_100_000`, `100__000`, `100_`

## 14.1 Hex Lexical Requirements

Implementations MUST enforce hex underscore placement rules:
1. `_` MAY appear only between hex digits;
2. leading `_` is invalid;
3. trailing `_` is invalid;
4. consecutive underscores are invalid.

Examples:
- valid: `#ff00aa`, `#Ff_00_Aa`
- invalid: `#_ff`, `#ff_`, `#F__f`

## 15. Minimum Conformance Floors

Implementations claiming AEON v1 conformance MUST support at least:
1. string literal length: `1,048,576` Unicode code points;
2. key segment length: `1,024` Unicode code points;
3. numeric literal lexical length: `1,024` characters;
4. container nesting depth (object/list/tuple/node): `64`;
5. list/tuple element count per container: `65,536`;
6. canonical/reference path string length: `8,192` characters;
7. structured comment payload length: `1,048,576` characters;
8. `max_attribute_depth` and `max_separator_depth` capability floor of at least `8`.

These floors are minimum interoperability guarantees. Implementations MAY support larger limits.

## 16. Section-to-CTS Matrix

Canonical matrix:
- `conformance-matrix.md`

## 17. Non-Conformance

An implementation MUST NOT claim AEON v1 conformance if any REQUIRED item in this document is not satisfied.

Passing a narrow representative subset is not sufficient if implementation behavior drifts on a backbone family required by this document or by the published CTS lanes.
