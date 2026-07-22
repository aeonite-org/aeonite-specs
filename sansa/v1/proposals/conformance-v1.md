---
id: sansa-v1-conformance
title: SANSA v1 Conformance and Capabilities
description: Proposal-stage conformance profiles and capability naming for SANSA implementations.
family: sansa
group: SANSA
status: Proposal
path: specification/sansa/v1/proposals/conformance
license: CC-BY-4.0
links:
  - sansa-v1-addressing
  - sansa-v1-resolve
  - sansa-v1-query
  - sansa-v1-extensions
---

# SANSA v1 Conformance and Capabilities

Status: Proposal  
Scope: named SANSA capabilities, conformance profiles, and extension advertisement.

## 1. Overview

An implementation must not claim generic support for "SANSA" without identifying the capabilities it supports.

SANSA v1 defines independent capability families:

- `SANSA.Addressing`
- `SANSA.Resolve`
- `SANSA.Query`

Future specifications may define:

- `SANSA.Mutate`
- `SANSA.Subscribe`
- `SANSA.History`

Capabilities are cumulative only where a specification requires it. For example, `SANSA.Query` depends on `SANSA.Resolve`, and `SANSA.Resolve` depends on `SANSA.Addressing`. An Addressing-only implementation does not need to expose a namespace resolver.

## 2. Profiles

### 2.1 Addressing Profile

Supports:

- parsing SANSA address expressions;
- validating selector syntax;
- rendering canonical address form;
- surfacing parse diagnostics and portability warnings.

Does not require:

- namespace resolution;
- Binding Set production;
- value access;
- query evaluation.

### 2.2 Resolve Profile

Supports:

- all Addressing Profile requirements;
- deterministic structural resolution over a host-exposed namespace;
- ordered Binding Set production;
- supported-selector misses versus failures;
- Resolve diagnostics.

Does not require:

- value comparison;
- projection;
- ordering clauses;
- functions;
- mutation.

### 2.3 Query Profile

Supports:

- all Resolve Profile requirements;
- SANSA.Query parsing;
- the core read-only query pipeline;
- scalar consumption rules;
- comparison, Boolean, existence, cardinality, membership, ordering, slicing, and projection contracts defined by `query-v1.md`;
- Query diagnostics.

Does not require:

- experimental extensions;
- mutation;
- subscription;
- history;
- consumer-specific domain functions.

## 3. Core, Optional, and Experimental Surface

SANSA distinguishes:

- **Core conformance**: required behavior for a named profile.
- **Optional extension**: explicitly advertised behavior outside the core profile.
- **Experimental extension**: prototype or review-stage behavior that must not be treated as required v1 conformance.
- **Future capability**: named design direction without v1 conformance requirements.

Experimental extensions do not modify SANSA v1 conformance. Implementations may expose them only when the implementation clearly advertises their experimental status.

## 4. Capability Advertisement

An implementation should expose human-readable or machine-readable capability information containing:

- implementation name and version;
- supported SANSA profiles;
- supported capabilities;
- optional extensions;
- experimental extensions;
- implementation-defined limits;
- portability-warning behavior.

Conceptual example:

```json
{
  "implementation": "@altopelago/sansa",
  "version": "0.1.0",
  "profiles": ["addressing", "resolve", "query"],
  "capabilities": [
    "SANSA.Addressing",
    "SANSA.Resolve",
    "SANSA.Query"
  ],
  "extensions": [
    {
      "id": "sansa.query.fieldsFrom",
      "capability": "SANSA.Query",
      "category": "library",
      "maturity": "experimental"
    }
  ]
}
```

## 5. CTS Lanes

CTS suites should distinguish required conformance from optional or experimental coverage.

Recommended metadata:

```json
{
  "capability": "SANSA.Query",
  "profile": "query",
  "conformance": {
    "surface": "extension",
    "maturity": "experimental"
  }
}
```

Core CTS lanes should exclude experimental cases by default. Implementations that expose experimental extensions may run explicit experimental lanes.

## 6. Boundaries

Conformance does not imply authorization.

A resolver can conform to `SANSA.Resolve` while rejecting a specific local address space for policy reasons. A query implementation can conform to `SANSA.Query` while refusing implementation-specific functions. A future mutation implementation will require stronger authority boundaries than read-only Query.
