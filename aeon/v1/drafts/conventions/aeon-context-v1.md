---
id: aeon-context-v1
title: AEON Context v1
description: Draft context-label convention for descriptive metadata such as domain, role, audience, intent, source, confidence, sensitivity, and advisory instruction comments.
family: conventions
group: General-Purpose Conventions
path: specification/conventions/aeon-context-v1
links:
  - aeon-conventions-overview
  - aeon-gp-convention-v1
---

# AEON Context v1

## Status

Draft interoperability convention

Convention identifier: `aeon.gp.context.v1`

---

# 1. Overview

**AEON Context v1** defines a lightweight convention for attaching contextual metadata to AEON data.

It is intended to help downstream consumers, especially:

* agentic AI systems
* retrieval pipelines
* automation processors
* document interpreters
* validation and transformation layers

This convention does **not** add computation, control flow, or execution semantics to AEON.

It only standardizes a small set of contextual labels.

---

# 2. Purpose

Some data is structurally valid but contextually ambiguous.

Example:

```aeon
amount = 12
status = "open"
type = "report"
```

Without context, a processor may not know:

* what domain this belongs to
* how to interpret `"open"`
* whether `amount` is money, count, or weight
* whether `type="report"` is semantic, editorial, or technical

`aeon.gp.context.v1` provides a light way to label that context.

---

# 3. Convention Declaration

## Single convention

```aeon
aeon:header = {
  convention = "aeon.gp.context.v1"
}
```

## With base convention

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.convention.v1"
    "aeon.gp.context.v1"
  ]
}
```

This is the recommended form when both general semantic labels and contextual labels are used.

---

# 4. Design Principles

`aeon.gp.context.v1` is governed by these principles:

### 1. Descriptive, not imperative

Context describes how data should be understood, not what a processor must do.

### 2. Lightweight

The convention should remain small and broadly reusable.

### 3. Domain-bridging

It should help a processor situate data across domains without defining domain logic.

### 4. No hidden execution

It must not become a command language for AI agents.

---

# 5. Reserved Attribute Keys

The following lowercase attribute keys are defined by `aeon.gp.context.v1`.

| Key           | Purpose                                                 |
| ------------- | ------------------------------------------------------- |
| `domain`      | broad subject area or knowledge domain                  |
| `role`        | semantic role of a value within a document or structure |
| `audience`    | intended target audience                                |
| `intent`      | declared communicative or processing intent             |
| `scope`       | contextual boundary or applicability range              |
| `source`      | origin classification of the data                       |
| `confidence`  | declared confidence level                               |
| `sensitivity` | handling sensitivity label                              |

These keys are descriptive only.

---

# 6. Attribute Definitions

## 6.1 `domain`

Declares the broad subject or knowledge domain.

```aeon
summary@{domain="finance"} = "Quarterly revenue increased 8%"
diagnosis@{domain="medical"} = "pending review"
```

Examples:

* `finance`
* `legal`
* `medical`
* `logistics`
* `media`
* `engineering`

This helps downstream systems situate interpretation.

---

## 6.2 `role`

Declares the semantic role a value plays.

```aeon
title@{role="headline"} = "Stormwater Easement Assessment"
amount@{role="estimated-cost"} = 1200
status@{role="workflow-state"} = "open"
```

Examples:

* `headline`
* `summary`
* `identifier`
* `workflow-state`
* `estimated-cost`
* `label`

This is useful when the same field name may appear across different contexts.

---

## 6.3 `audience`

Declares the intended audience.

```aeon
note@{audience="internal"} = "Draft only"
summary@{audience="executive"} = "High-level overview"
guide@{audience="customer"} = "Setup instructions"
```

Examples:

* `internal`
* `public`
* `customer`
* `executive`
* `technical`

---

## 6.4 `intent`

Declares the intended communicative or processing intent.

```aeon
text@{intent="inform"} = "System maintenance scheduled for Friday"
brief@{intent="decide"} = "Choose option B based on lower risk"
record@{intent="archive"} = "Meeting transcript"
```

Examples:

* `inform`
* `decide`
* `archive`
* `summarize`
* `review`
* `classify`

Important: this is **not** an instruction to execute.
It is a declaration of intended use or purpose.

---

## 6.5 `scope`

Declares contextual scope or applicability.

```aeon
status@{scope="project"} = "active"
policy@{scope="regional"} = "applies in Victoria"
limit@{scope="session"} = 10
```

Examples:

* `local`
* `global`
* `project`
* `document`
* `session`
* `regional`

---

## 6.6 `source`

Declares an origin classification.

```aeon
statement@{source="user"} = "Preferred delivery window is 3-5pm"
summary@{source="system"} = "Generated from uploaded files"
record@{source="sensor"} = 42.7
```

Examples:

* `user`
* `system`
* `external`
* `sensor`
* `imported`
* `derived`

This helps downstream consumers distinguish origin without requiring provenance machinery.

---

## 6.7 `confidence`

Declares a confidence label.

```aeon
classification@{confidence="high"} = "invoice"
match@{confidence="low"} = "possible duplicate"
```

Examples:

* `low`
* `medium`
* `high`
* `uncertain`

This is descriptive and does not imply probability unless defined elsewhere.

---

## 6.8 `sensitivity`

Declares a handling sensitivity label.

```aeon
email@{sensitivity="personal"} = "user@example.com"
report@{sensitivity="internal"} = "Draft assessment"
record@{sensitivity="restricted"} = "Access-controlled"
```

Examples:

* `public`
* `internal`
* `personal`
* `restricted`
* `confidential`

This helps AI and automation systems avoid flattening all inputs into the same handling class.

---

# 7. Non-Goals

`aeon.gp.context.v1` does not define:

* task execution
* permissions
* workflow logic
* security enforcement
* truth guarantees
* reasoning rules

For example:

```aeon
summary@{intent="decide"} = "Option A is lower risk"
```

does not mean:

* the system must make a decision
* the system must trust the statement
* the system must execute anything

It only labels contextual intent.

---

# 8. Unknown Keys

Unknown context keys remain valid and opaque unless defined by another convention, schema, or profile.

This allows local extension without changing the core convention.

---

# 9. Advisory Instruction Comments

AEON comment channels may also carry advisory instruction text for downstream consumers.

In particular, instruction comments of the form:

```aeon
/(can you update these figures?)/
```

may be used as a side-channel hint for:

* AI-capable consumers
* workflow tools
* review systems
* end-of-line application logic

This convention treats such comments as:

* descriptive or advisory context
* non-authoritative by default
* outside AEON Core data semantics

AEON Core does not execute them, enforce them, or let them change the meaning of nearby bindings.
It only preserves them as comment-side context.

Example:

```aeon
/(can you update these figures?)/
totalConventions = 0 // total amount of conventions we have on file
conventionList = [] // listed out by name
```

Under Core processing, `totalConventions` and `conventionList` remain ordinary bindings.
The instruction comment is a preserved side-channel hint for consumers that choose to use it.

This is especially relevant when an AEON file is read directly by an AI system rather than first being reduced through a narrower processor pipeline.

Even in that case, the instruction comment should be treated as advisory guidance, not as trusted execution authority.

---

# 10. Example Document

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.convention.v1"
    "aeon.gp.context.v1"
  ]
}

type@{ns="aeon"} = "document"

title@{role="headline" audience="executive" intent="inform"} = "Q1 Operations Summary"

status@{role="workflow-state" scope="project"} = "active"

budget@{currency="AUD" precision=0.01 role="estimated-cost" domain="finance"} = 12000

summary@{domain="operations" audience="internal" source="system" confidence="medium"} =
  "Based on current inputs, delivery risk is moderate."

note@{audience="internal" sensitivity="restricted"} =
  "Pending contractor confirmation."
```

---

# 11. Agentic AI Use Case

This convention is especially useful for agentic AI because it helps separate:

* raw data
* semantic meaning
* contextual relevance

Example:

```aeon
instruction@{intent="review" audience="technical" source="user"} =
  "Check whether the schema matches the release draft."

status@{role="workflow-state" source="system" confidence="high"} = "blocked"
```

A downstream AI system can use these labels to improve interpretation, prioritization, summarization, or routing.

But the convention itself does not instruct the AI to act.

---

# 12. Summary

**AEON Context v1** is a lightweight contextual annotation convention for AEON documents.

It helps downstream systems understand:

* what kind of data they are looking at
* how it is meant to be read
* where it came from
* how cautiously it should be handled

without turning AEON into a procedural agent language.

---

## Recommendation

Keep `aeon.gp.context.v1` intentionally small in v1.

A good minimal registry is:

```text
domain
role
audience
intent
scope
source
confidence
sensitivity
```
