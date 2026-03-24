---
id: appendix-transport-v1
title: Appendix - Transport and Framing
description: Transport envelopes, framing assumptions, and interchange-safe packaging concerns.
family: appendices-v1
group: Core Semantics
path: specification/appendices/appendix-transport-v1
---

# Appendix — Transport & Framing

**Appendix to:** AEON Specification v1

This appendix defines how AEON documents are framed and transported.

---

## 1. Design Principles

1. **Framing before meaning** — Headers readable before payload interpretation
2. **No execution for inspection** — Headers parse without processors
3. **Transport orthogonal to interpretation** — Framing doesn't affect semantics
4. **Fail closed** — Malformed framing causes rejection

---

## 2. Document Unit

An **AEON Document Unit** consists of:
1. Optional framing metadata (transport-level)
2. AEON headers
3. AEON payload (body)
4. Optional envelope

Transport framing MUST delimit exactly one document unit.

---

## 3. Headers as Control Surface

Headers are the **only** part inspectable before full parsing:

```aeon
aeon:version = "2.0"
aeon:schema:id = "com.example.contact"
aeon:profile:id = "com.example.api"
```

Rules:
- Headers parseable without evaluating payload
- Headers MUST NOT trigger processors
- Headers immutable once read

---

## 4. File Transport

### 4.1 Single Document

- An AEON file contains exactly one Document Unit
- Encoding MUST match `aeon:encoding` if present
- Reject files with conflicting encoding declarations

### 4.2 Extensions

Common extensions (non-normative):
- `.aeon`
- `.aeon.txt`

Extensions have no semantic meaning.

---

## 5. Stream Transport

When streaming, each document MUST be framed using:

### 5.1 Length-Prefix Framing (Recommended)

```
<length>\n
<AEON document bytes>
```

**Implementation note:** `@aeon/transport` uses a binary u32 big-endian length prefix (`[4 bytes length][payload]`) as the default framing format. This is compatible with stream transports where newline-delimited framing is not available.

### 5.2 Delimiter Framing

Explicit end marker after document.

**Note:** Implementations MUST NOT assume EOF implies end-of-document.

---

## 6. Incremental Parsing

Implementations MAY support incremental parsing with guarantees:
- Headers fully read before payload interpretation
- Payload not partially evaluated
- Assignment Events not emitted until document complete

This prevents "early execution" attacks.

---

## 7. Multi-Document Containers

AEON may be embedded in containers (archives, multipart messages).

Rules:
- Each document retains independent framing
- Headers inspectable per document
- No shared state implied

---

## 8. Security Considerations

### 8.1 Header-First Policy

Consumers SHOULD:
1. Read framing
2. Read headers
3. Verify schema/profile against policy
4. Only then parse payload

### 8.2 Resource Limits

Implementations SHOULD enforce limits on:
- Document size
- Nesting depth
- Array lengths
- Assignment Event count

Framing MUST allow rejection before resource exhaustion.

### 8.3 No Remote Fetch

Transport MUST NOT automatically fetch:
- Schemas
- Profiles
- Processors

All artifacts resolved locally by policy.

---

## 9. Relationship to Processing

Transport occurs **before** Phase 1 (Lexing).

Transport MUST NOT:
- Alter canonical paths
- Affect assignment ordering
- Inject metadata into document model

---

*End of Transport & Framing*
