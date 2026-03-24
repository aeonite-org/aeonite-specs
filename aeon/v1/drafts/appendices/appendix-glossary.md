---
id: appendix-glossary-v1
title: Appendix - Glossary
description: Normative terminology used across AEON Core, AEOS, and companion references.
family: appendices-v1
group: Orientation
path: specification/appendices/appendix-glossary-v1
---

# Appendix — Glossary (Normative)

**Appendix to:** AEON Specification v1

This glossary defines core AEON terms. Terms are listed alphabetically. Entries marked **(v1 baseline update)** were introduced or revised during v1 consolidation.

---

## Annotation Stream **(v1 baseline update)**

The **Annotation Stream** is the ordered sequence of structured comment records emitted by AEON Core in parallel to the AES.

- Contains one record per structured comment (`doc`, `annotation`, `hint`, `reserved`)
- Does NOT affect the AES
- Is emitted in source order
- Records include kind, form, raw content, span, and deterministic target binding

See *Appendix: Annotation Stream*.

---

## Assignment Event

An **Assignment Event** is the atomic semantic unit of an AEON document.

- Emitted when a binding assigns a value to a canonical path
- Immutable once emitted
- Unique per canonical path (no duplicates allowed)

Assignment Events are the basis for canonical hashing, schema validation, and reference resolution.

---

## Assignment Event Set (AES)

The **Assignment Event Set (AES)** is the ordered, canonical output of the AEON compilation pipeline.

- Consists of one immutable Assignment Event per binding
- Preserves lexical source order
- Retains original AST values (no coercion or resolution)
- Produced after all validation phases complete
- Fail-closed: empty if any errors exist

AES is the sole semantic output of AEON Core. See *Appendix: Assignment Event Stream (AES)*.

---

## Binding

A **Binding** is a key-value assignment: `name = value`.

---

## Body

The **Body** of an AEON document is the set of bindings that define its meaning.

- Parsed after headers
- Interpreted through AEON Core structure plus any applicable conventions, schemas, profiles, and consumer policy
- Validated by schemas when validation is applied
- Covered by canonical hashing

The body MUST NOT include integrity material.

---

## Canonical Path

A **Canonical Path** is the unique, fully-qualified identifier for a value.

In v1, canonical path identity supports two segment kinds:
- `member(key)` — printed `.key`
- `index(i)` — printed `[n]` (v1)

Examples:
- `$.user.name`
- `$.items[0]`

Attribute selectors (for example `@meta`, `@["a.b"]`) are valid in addressing expressions but are not canonical path identity segments.

---

## Consumer

A **Consumer** is any system that parses, validates, or interprets an AEON document.

Consumers:
- Select conventions, schemas, profiles, and processors by policy
- Decide what processors are allowed
- Define trust boundaries

Documents do not control consumers.

---

## Contract

A **Contract** is a published, versioned artifact that identifies a trusted profile or schema surface for AEON processing.

Contracts:
- are resolved through trusted registries or allowlists
- do not self-activate from document claims alone
- define stable identifiers such as `aeon.gp.profile.v1` and `aeon.gp.schema.v1`

See *AEON v1 Contracts Specification*.

---

## Convention

A **Convention** is a named interpretation agreement layered on top of AEON Core.

Conventions:
- define meaning, context, metadata, or interop labels
- do not change AEON grammar
- are declared by documents but interpreted by downstream consumers

Examples include document metadata conventions, context conventions, security conventions, and limbo conventions.

---

## Conformance Test Suite (CTS)

The **Conformance Test Suite (CTS)** is the published test surface used to verify claimed AEON conformance.

CTS:
- is organized into named lanes and suite files
- covers normative behavior rather than general hardening
- is the public conformance authority for the v1 line

Stress or hardening workflows may exist separately and are not automatically part of CTS.

---

## Envelope

An **Envelope** is a top-level object binding typed as `:envelope`.

- In the baseline GP security model, `close:envelope` is the recommended conventional spelling
- Appears only at document end when used for GP integrity/signature/encryption conventions
- In the baseline GP security model, contains `integrity`, `signatures`, and optional `encryption`
- Excluded from canonical hashing when selected as the document envelope
- Inert and non-semantic

---

## Guarantee

A **Guarantee** is an advisory, non-semantic assertion about a value's representation.

Guarantees:
- Are emitted by validators (AEOS or third-party)
- Describe syntactic properties only (e.g., `integer-representable`)
- Do NOT alter validation outcomes
- MAY be observed by downstream processors

Tier-1 guarantees are normative; Tier-2 guarantees are namespaced and vendor-specific.

---

## Header

A **Header** is AEON metadata declared in the `aeon:` namespace.

Headers express:
- Document identity and versioning
- Convention, contract, schema, and profile intent
- Encoding

Headers are inspectable before evaluation and advisory (not authoritative).

---

## Index Segment **(v1 baseline update)**

An **Index Segment** is a positional canonical path segment of the form `[n]` that addresses an element of a list or tuple.

- Zero-based
- Decimal digits only
- No sign prefix
- No leading zeros unless index is `0`

Malformed index forms produce `invalid_index_format`.

---

## Integrity Material

**Integrity Material** includes:
- Canonical integrity hashes
- Cryptographic signatures
- Optional encryption metadata when a security convention defines it

Exists only to verify document integrity and authenticity.

---

## ListNode **(v1 baseline update)**

A **ListNode** is the AES/AST value kind for `[...]` surface syntax.

- Indicates homogeneous-element intent
- Type constructor: `list<T>`

---

## Instruction Comment

An **Instruction Comment** is an advisory comment intended as side-channel guidance for downstream consumers.

Instruction comments:
- may suggest review, update, summarization, routing, or handling intent
- do not alter AEON Core semantics
- are preserved as comment-side context rather than treated as binding data
- may be used by profiles, processors, or direct end consumers subject to trust policy

Instruction comments are non-authoritative by default.

---

## Pattern Profile

The **Pattern Profile** defines a deterministic DSL for validating `StringLiteral` values.

Features:
- Predicates: `length`, `contains`, `starts_with`, `ends_with`, `no_whitespace`, `charset`
- Composition: `all`, `any`, `not`
- Structure: `split`, `labels`

See *Appendix: Pattern Profile*.

---

## Profile

A **Profile** defines a policy bundle for how an AEON document should be processed once selected by trusted consumer policy.

Profiles:
- may enable or forbid processors or optional behaviors
- may set default processing policy such as mode or datatype policy
- do not override the zero-trust rule that consumer selection remains authoritative

Exactly one profile may be active. Profiles are trusted, consumer-selected contract artifacts.

---

## Processor

A **Processor** is a named downstream behavior or transformation function selected under consumer policy.

Processors:
- Are not defined inside documents
- May be pure or capability-gated
- May be enabled or constrained by profiles, schemas, or other external policy
- Are distinct from conventions, which define interpretation rather than behavior

Processors must be explicitly allowed by the consumer environment.

---

## Schema

A **Schema** defines acceptability constraints over an AEON document.

Schemas:
- Validate structure and values
- Do not execute logic
- Do not by themselves define business meaning

Schemas constrain; conventions describe meaning; profiles bundle policy.

---

## Schema Profile

The **Schema Profile** defines the structure of AEON documents used as schemas.

Components:
- `rules` — binds data paths to constraints
- `patterns` — reusable pattern definitions
- `charsets` — named character sets

See *Appendix: Schema Profile*.

---

## Semantic Content

**Semantic Content** is the meaning-bearing portion of an AEON document.

Consists of:
- Assignment Events from the body
- Excluding headers and envelope

Canonical hashing operates over semantic content.

---

## Side Channel

A **Side Channel** is preserved document material that accompanies AEON Core output without changing the meaning-bearing AES.

Examples include:
- structured comment records in the Annotation Stream
- spans
- advisory instruction comments

Side-channel material may be consumed by validators, processors, or end applications, but it does not alter Core semantic content by itself.

---

## Span

A **Span** identifies the precise location in source text from which a value originated.

- Format: `[start, end]` offsets as emitted by AEON Core
- `start` is inclusive, `end` is exclusive
- Produced by AEON Core only
- Validators propagate spans unchanged

See *Appendix: Spans*.

---

## Tonic **(v1 baseline update)**

A **Tonic** is the canonical downstream materialization processor that consumes AES and produces a domain-specific runtime representation.

Tonics:
- Receive AES from AEON Core
- Optionally validate against an AEOS schema
- Transform AES into domain objects

Tonics are *not* AEON Core — they consume AEON output.

See *Appendix: Tonic Processor Governance*.

---

## TupleLiteral **(v1 baseline update)**

A **TupleLiteral** is the AES/AST value kind for `(...)` surface syntax.

- Indicates positional/arity intent
- Type constructor: `tuple<T1..TN>`
- Distinct from `ListNode`

---

## Validator Conformance

**Validator Conformance** defines requirements for any third-party validation engine consuming AES.

Conformant validators MUST:
- Consume AES as read-only
- Preserve event order
- Not coerce, resolve, or materialize values
- Emit diagnostics with path, span, and phase

See *Appendix: Third-Party Validator Conformance*.

---

## Document Structure Summary

| Component         | Purpose                             |
| ----------------- | ----------------------------------- |
| Header            | Identity & intent                   |
| Body              | Meaning                             |
| Envelope          | Integrity                           |
| Annotation Stream | Parallel structured comment records |

---

*End of Glossary — v1*
