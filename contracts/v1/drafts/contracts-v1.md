---
id: aeon-v1-contracts
title: AEON v1 Contracts Specification
description: "Contract-layer specification covering contract identifiers, artifact shapes, registry format, and the boundary between core processing, contracts, and consumer policy."
family: contracts
group: Contracts Overview
status: official v1 contract specification
license: CC-BY-4.0
path: specification/contracts/aeon-v1-contracts-specification
links:
  - contracts-artifacts-overview
  - aeon-core-v1
  - aeos-v1
---
# AEON v1 Contracts Specification

Status: official v1 contract specification  
Scope: contract-layer identifiers, contract artifact shapes, trusted registry format, resolution algorithm, and authority boundaries for AEON v1.

## 1. Contract Layer Purpose

The contract layer tells a processor which published profile/schema contract a document claims to target.

It is distinct from:
- the AEON language version
- implementation package versions
- consumer-specific business logic

## 2. Canonical Baseline Contracts

The canonical general-purpose baseline contracts for AEON v1 are:

- profile contract: `aeon.gp.profile.v1`
- schema contract: `aeon.gp.schema.v1`

Baseline artifacts:
- [profile artifact](./artifacts/profiles/aeon.gp.profile.v1.aeon)
- [schema artifact](./artifacts/schemas/aeon.gp.schema.v1.aeon)
- [registry](./artifacts/registry.json)

These baseline contracts are official and published, but they are not implicit defaults.
When no trusted external selection chooses a profile/schema, Core-only processing defaults apply.

## 3. Boundary Model

Authority split:

1. AEON Core
- lexing
- parsing
- canonical path assignment
- reference legality
- mode/datatype enforcement at the Core layer

2. contract/profile/schema layer
- published profile and schema contract identifiers
- structural validation model and allowed contract metadata
- trusted resolution policy

3. consumer layer
- allowlist/registry policy
- direct runtime object injection
- business/domain meaning beyond the published contract surface

Documents do not control the consumer.
Header contract identifiers are routing hints only.
Document-declared contract identifiers do not self-activate.

## 4. Contract Artifact Format

Authoritative contract artifacts are AEON files.

Rules:
- registry `path` values MUST point to `.aeon` authoritative artifacts
- derived JSON snapshots MAY exist for tooling, but are non-authoritative
- contract authority resides in the AEON source artifact, not a derived format

## 5. Profile Contract Shape

Canonical top-level keys for a profile contract:

| Key                       | Required | Type                              | Meaning                                      |
| ------------------------- | -------- | --------------------------------- | -------------------------------------------- |
| `profile_id`              | yes      | string                            | contract identifier                          |
| `profile_version`         | yes      | string                            | semver for the published artifact            |
| `core_id`                 | yes      | string                            | target Core specification line               |
| `description`             | no       | string                            | human-readable summary                       |
| `mode_default`            | no       | string                            | published default mode                       |
| `datatype_policy_default` | no       | string                            | published default datatype policy            |
| `collections`             | yes      | object<string, collection>        | normative GP semantics for collection shapes |
| `containers`              | yes      | object<string, container>         | normative GP semantics for object/node shapes |
| `capabilities`            | yes      | object<string, boolean>           | required processor support for GP profile claims |

`collection` records use these canonical keys:

| Key             | Required | Type    | Meaning                                                    |
| --------------- | -------- | ------- | ---------------------------------------------------------- |
| `ordered`       | yes      | boolean | whether family semantics treat element order as meaningful |
| `heterogeneous` | yes      | boolean | whether elements may have different value/datatype shapes  |
| `unique`        | yes      | boolean | whether duplicate elements are disallowed by the family    |
| `fixed_length`  | yes      | boolean | whether arity is intrinsic to the family                   |

`container` records use shape-specific canonical keys.

For `object`:

| Key             | Required | Type    | Meaning                                                |
| --------------- | -------- | ------- | ------------------------------------------------------ |
| `ordered`       | yes      | boolean | whether member order is semantically significant       |
| `heterogeneous` | yes      | boolean | whether member values may have different value shapes  |
| `unique_keys`   | yes      | boolean | whether member keys are unique within one object scope |

For `node`:

| Key                 | Required | Type    | Meaning                                                       |
| ------------------- | -------- | ------- | ------------------------------------------------------------- |
| `ordered`           | yes      | boolean | whether child order is semantically significant               |
| `heterogeneous`     | yes      | boolean | whether children may have different value shapes              |
| `unique_attributes` | yes      | boolean | whether attribute keys are unique within one attribute block  |
| `mixed_content`     | yes      | boolean | whether children may mix scalar and structural value shapes   |

`capabilities` records use these canonical keys:

| Key          | Required | Type    | Meaning                                               |
| ------------ | -------- | ------- | ----------------------------------------------------- |
| `references` | yes      | boolean | whether reference syntax support is required          |
| `clones`     | yes      | boolean | whether clone-reference support is required           |

Current baseline profile artifact:

```aeon
profile_id = "aeon.gp.profile.v1"
profile_version = "1.0.0"
core_id = "aeon.core.v1"
description = "General-purpose AEON profile baseline for v1."
mode_default = "strict"
datatype_policy_default = "reserved_only"
collections = {
  list = {
    ordered = false
    heterogeneous = true
    unique = false
    fixed_length = false
  }
  tuple = {
    ordered = true
    heterogeneous = true
    unique = false
    fixed_length = true
  }
}
containers = {
  object = {
    ordered = false
    heterogeneous = true
    unique_keys = true
  }
  node = {
    ordered = true
    heterogeneous = true
    unique_attributes = true
    mixed_content = true
  }
}
capabilities = {
  references = true
  clones = true
}
```

Interpretation:
- this artifact defines the published GP baseline defaults once `aeon.gp.profile.v1` is explicitly selected by trusted policy;
- it fixes the GP collection meanings for `list` and `tuple`;
- it fixes the GP container meanings for `object` and `node`;
- it fixes the required processor capabilities for implementations claiming `aeon.gp.profile.v1` support;
- `collections` is closed for `aeon.gp.profile.v1`: only `list` and `tuple` have GP v1 collection semantics. Future profiles may define additional collection names without changing this artifact;
- `containers` is closed for `aeon.gp.profile.v1`: only `object` and `node` have GP v1 container semantics. Future profiles may define additional container names without changing this artifact;
- profile collection and container semantics are keyed by canonical family name. Alternative or reserved datatype names inherit the semantics of their canonical family, for example `obj`, `o`, and `envelope` inherit `object`;
- `capabilities` is closed for `aeon.gp.profile.v1`: only `references` and `clones` are defined as GP v1 capability requirements by this artifact;
- `capabilities.references = true` and `capabilities.clones = true` mean implementations claiming GP profile support must support those features. They do not require every GP document to use references or clones;
- profile collection and container semantics do not override schema constraints. For example, `list.heterogeneous = true` permits mixed element shapes by default, while a schema can still constrain a particular binding with `list<int32>` or other element rules;
- `indexed` is intentionally absent because index-addressability is a Core representation guarantee. AEON Core always emits index-addressable list/tuple elements and node child slots; the profile decides whether those positions carry semantic meaning;
- `ordered` defines whether lexical element order is semantically significant. AEON Core always preserves lexical source order and emits index-addressable elements irrespective of the selected collection semantics;
- `object.ordered = false` means object member order is not semantically significant in the GP profile. AEON Core may still preserve source order for diagnostics, AES emission, and canonicalization inputs;
- `node.ordered = true` means node child positions are semantically significant. AEON Core preserves node child order and exposes child slots with index-addressable paths;
- `unique_keys` and `unique_attributes` record GP uniqueness semantics; Core duplicate-key checks remain Core representation guarantees and are not delegated to materializers;
- materialization properties such as mutability, storage layout, allocation strategy, capacity, contiguous or linked storage, thread safety, lazy evaluation, persistence, sortedness, hash backing, and language-specific collection types belong to tonics or host bindings rather than this GP baseline profile;
- it does not cause GP behavior to become active merely because no profile is declared.

## 6. Schema Contract Shape

Canonical top-level keys for a schema contract:

| Key                  | Required | Type                        | Meaning                                                      |
| -------------------- | -------- | --------------------------- | ------------------------------------------------------------ |
| `schema_id`          | yes      | string                      | contract identifier                                          |
| `schema_version`     | yes      | string                      | semver for the published artifact                            |
| `rules`              | yes      | list                        | schema rule list consumed by AEOS                            |
| `world`              | no       | `open` or `closed`          | schema-wide unexpected-binding policy                        |
| `datatype_allowlist` | no       | list<string>                | allowed datatype labels for schema-side datatype constraints |
| `datatype_rules`     | no       | object<string, constraints> | datatype-wide GP semantics keyed by datatype base label      |

Rules:
- only these canonical metadata keys are valid in v1.0.0
- unknown top-level metadata keys fail closed
- transitional aliases are not allowed in v1.0.0
- if `world` is omitted, AEOS treats the schema as `open`
- the published `aeon.gp.schema.v1` artifact declares `world = "open"` explicitly so the GP baseline policy is visible in the artifact itself

Current baseline schema artifact:

```aeon
schema_id = "aeon.gp.schema.v1"
schema_version = "1.0.0"
world = "open"
rules = []
datatype_rules = {
  int = { type = "IntegerLiteral" }
  uint = { type = "IntegerLiteral", sign = "unsigned" }
  int8 = { type = "IntegerLiteral", min_value = "-128", max_value = "127" }
  int16 = { type = "IntegerLiteral", min_value = "-32768", max_value = "32767" }
  int32 = { type = "IntegerLiteral", min_value = "-2147483648", max_value = "2147483647" }
  int64 = { type = "IntegerLiteral", min_value = "-9223372036854775808", max_value = "9223372036854775807" }
  uint8 = { type = "IntegerLiteral", sign = "unsigned", min_value = "0", max_value = "255" }
  uint16 = { type = "IntegerLiteral", sign = "unsigned", min_value = "0", max_value = "65535" }
  uint32 = { type = "IntegerLiteral", sign = "unsigned", min_value = "0", max_value = "4294967295" }
  uint64 = { type = "IntegerLiteral", sign = "unsigned", min_value = "0", max_value = "18446744073709551615" }
  float = { type = "FloatLiteral" }
  float32 = { type = "FloatLiteral" }
  float64 = { type = "FloatLiteral" }
}
```

This artifact is the normative GP semantic layer for the reserved numeric datatype labels. Implementations MUST NOT claim GP schema support unless they honor these datatype rules substantively.

## 7. Canonical Schema Metadata Key Table

Locked canonical schema metadata keys:

1. `schema_id`
2. `schema_version`
3. `rules`
4. optional `world`
5. optional `datatype_allowlist`
6. optional `datatype_rules`

## 8. Canonical Registry Document Shape

Registry root shape:

```json
{
  "contracts": [
    {
      "id": "aeon.gp.profile.v1",
      "kind": "profile",
      "version": "1.0.0",
      "path": "profiles/aeon.gp.profile.v1.aeon",
      "sha256": "…",
      "status": "active"
    }
  ]
}
```

Registry entry keys:

| Key       | Required | Type                     | Meaning                                |
| --------- | -------- | ------------------------ | -------------------------------------- |
| `id`      | yes      | string                   | contract identifier                    |
| `kind`    | yes      | `profile` or `schema`    | contract kind                          |
| `version` | yes      | string                   | artifact semver                        |
| `path`    | yes      | string                   | trusted artifact path                  |
| `sha256`  | yes      | string                   | integrity hash for the target artifact |
| `status`  | yes      | `active` or `deprecated` | publication state                      |
| `compat`  | no       | object                   | optional compatibility metadata        |

## 9. Resolution Algorithm

Trusted resolution algorithm:

1. read the document-declared contract ID
2. treat it as a hint only
3. look up the ID in a trusted local registry or allowlist
4. reject unknown IDs
5. resolve the trusted artifact path
6. verify the artifact exists
7. verify the artifact hash before load
8. parse the authoritative AEON contract artifact
9. validate canonical contract shape
10. continue with Core/AEOS processing

Fail-closed conditions:
- unknown ID
- missing artifact
- hash mismatch
- malformed contract document
- non-canonical metadata keys

## 10. Diagnostics Surface

Representative contract-resolution diagnostics:

- `CONTRACT_UNKNOWN_PROFILE_ID`
- `CONTRACT_UNKNOWN_SCHEMA_ID`
- `CONTRACT_ARTIFACT_MISSING`
- `CONTRACT_ARTIFACT_HASH_MISMATCH`

Representative schema-contract shape failures:

- missing canonical required fields
- unknown canonical metadata key
- contract ID mismatch between registry entry and loaded artifact

Diagnostics surfaces SHOULD preserve stable semantic `code` values and MAY attach phase metadata for display and tooling:

- `phase` when the producing pipeline phase is explicit
- `phaseLabel` when a stable human-readable phase name is available

Human-facing CLI output SHOULD prefer readable phase labels such as `Reference Validation` or `Schema Validation` over raw numeric phase bands.

## 11. Runtime and CLI Injection

Two trusted usage models are valid:

1. registry/allowlist resolution
- typical CLI/operator path

2. direct caller injection
- runtime APIs may accept schema/profile objects directly from the consumer
- CLI may accept explicit operator-supplied paths

In both cases, trust is established by the caller context, not by the document being consumed.

## 12. TypeScript Profile Position

The TypeScript-specific profile surface is an extension profile, not the language-neutral baseline.

Public baseline claims should point to:
- `aeon.gp.profile.v1`
- `aeon.gp.schema.v1`

TS-specific behavior may be published separately, but it must not redefine AEON Core v1 or the general-purpose baseline contracts.

## 13. Support Claims

Implementations may claim support at different layers:

1. Core-only support
2. Core + GP baseline support
3. Core + GP + additional contract support

Core conformance does not require GP support.
However, any implementation claiming support for `aeon.gp.profile.v1` or `aeon.gp.schema.v1` MUST honor those contracts substantively rather than treating the IDs as decorative.
