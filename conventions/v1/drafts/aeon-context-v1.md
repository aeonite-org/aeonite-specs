---
id: aeon-context-v1
title: AEON Context v1
description: "Draft soft context annotation convention for descriptive metadata such as domain, role, audience, intent, source, confidence, sensitivity, and advisory instruction comments."
family: conventions
group: General-Purpose Conventions
status: Draft interoperability convention
license: CC0-1.0
path: specification/conventions/aeon-context-v1
links:
  - aeon-conventions-overview
  - aeon-gp-document-v1
  - aeon-gp-measurement-v1
---
# AEON Context v1

## Status

Draft interoperability convention

Convention identifier: `aeon.gp.context.v1`

---

# 1. Overview

**AEON Context v1** defines a lightweight convention for attaching contextual guidance to AEON data.

It is intended to help downstream consumers, especially:

* agentic AI systems
* retrieval pipelines
* automation processors
* document interpreters
* validation and transformation layers

This convention does **not** add computation, control flow, or execution semantics to AEON.

It standardizes a small set of contextual labels and recommends carrying them as structured comments by default.

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

`aeon.gp.context.v1` provides a light way to label that context without cluttering the data binding itself.

---

# 3. Convention Declaration

## Single convention

```aeon
aeon:header = {
  convention = "aeon.gp.context.v1"
}
```

## With related conventions

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.document.v1"
    "aeon.gp.measurement.v1"
    "aeon.gp.context.v1"
  ]
}
```

This is the recommended form when document namespace labels, measurement labels, and contextual labels are used together.

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

# 5. Context Carriers

Context labels may be carried in two forms.

## 5.1 Soft Context Annotations

Soft context annotations are the recommended form.

They use AEON structured comment channels and attach to nearby targets according to AEON Core comment attachment rules.

Example:

```aeon
//@ context(role="headline", audience="executive", intent="inform")
title = "Q1 Operations Summary"
```

Soft context annotations keep the AEON data binding clean.

They are appropriate when context is advisory, interpretive, or intended mainly for tools, AI systems, review systems, retrieval pipelines, or editor workflows.

Soft context annotations:

* do not create or remove bindings
* do not change values
* do not change canonical path identity
* do not change reference legality
* do not change assignment ordering
* may be ignored by processors that do not consume annotation streams

## 5.2 Hard Context Attributes

Hard context attributes may be used when the context label must travel with the binding as binding metadata.

Example:

```aeon
title@{role="headline" audience="executive" intent="inform"} = "Q1 Operations Summary"
```

Hard context attributes are appropriate when a processor, profile, schema, or storage pipeline requires the labels to remain attached after comments or annotation streams are stripped.

They should be used sparingly to avoid turning contextual guidance into visual clutter.

---

# 6. Reserved Context Keys

The following lowercase context keys are defined by `aeon.gp.context.v1`.

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

When used in a soft context annotation, these keys appear inside `context(...)`.

When used as hard context attributes, these keys appear inside `@{...}`.

---

# 7. Context Key Definitions

## 7.1 `domain`

Declares the broad subject or knowledge domain.

```aeon
//@ context(domain="finance")
summary = "Quarterly revenue increased 8%"

//@ context(domain="medical")
diagnosis = "pending review"
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

## 7.2 `role`

Declares the semantic role a value plays.

```aeon
//@ context(role="headline")
title = "Stormwater Easement Assessment"

//@ context(role="estimated-cost")
amount = 1200

//@ context(role="workflow-state")
status = "open"
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

## 7.3 `audience`

Declares the intended audience.

```aeon
//@ context(audience="internal")
note = "Draft only"

//@ context(audience="executive")
summary = "High-level overview"

//@ context(audience="customer")
guide = "Setup instructions"
```

Examples:

* `internal`
* `public`
* `customer`
* `executive`
* `technical`

---

## 7.4 `intent`

Declares the intended communicative or processing intent.

```aeon
//@ context(intent="inform")
text = "System maintenance scheduled for Friday"

//@ context(intent="decide")
brief = "Choose option B based on lower risk"

//@ context(intent="archive")
record = "Meeting transcript"
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

## 7.5 `scope`

Declares contextual scope or applicability.

```aeon
//@ context(scope="project")
status = "active"

//@ context(scope="regional")
policy = "applies in Victoria"

//@ context(scope="session")
limit = 10
```

Examples:

* `local`
* `global`
* `project`
* `document`
* `session`
* `regional`

---

## 7.6 `source`

Declares an origin classification.

```aeon
//@ context(source="user")
statement = "Preferred delivery window is 3-5pm"

//@ context(source="system")
summary = "Generated from uploaded files"

//@ context(source="sensor")
record = 42.7
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

## 7.7 `confidence`

Declares a confidence label.

```aeon
//@ context(confidence="high")
classification = "invoice"

//@ context(confidence="low")
match = "possible duplicate"
```

Examples:

* `low`
* `medium`
* `high`
* `uncertain`

This is descriptive and does not imply probability unless defined elsewhere.

---

## 7.8 `sensitivity`

Declares a handling sensitivity label.

```aeon
//@ context(sensitivity="personal")
email = "user@example.com"

//@ context(sensitivity="internal")
report = "Draft assessment"

//@ context(sensitivity="restricted")
record = "Access-controlled"
```

Examples:

* `public`
* `internal`
* `personal`
* `restricted`
* `confidential`

This helps AI and automation systems avoid flattening all inputs into the same handling class.

`sensitivity` remains advisory in this convention. Security enforcement belongs to profiles, processors, access-control systems, or security conventions.

---

# 8. Soft and Hard Forms

The soft and hard forms carry the same context vocabulary but have different processing posture.

Soft form:

```aeon
//@ context(role="workflow-state", scope="project")
status = "active"
```

Hard form:

```aeon
status@{role="workflow-state" scope="project"} = "active"
```

Processors that support this convention should treat both examples as equivalent context labels for interpretation.

They should not treat either form as an instruction to execute behavior.

When both forms are present on the same target, profiles should define precedence. In the absence of a profile rule, processors should preserve both and report conflicts rather than silently choosing.

---

# 9. Non-Goals

`aeon.gp.context.v1` does not define:

* task execution
* permissions
* workflow logic
* security enforcement
* truth guarantees
* reasoning rules

For example:

```aeon
//@ context(intent="decide")
summary = "Option A is lower risk"
```

does not mean:

* the system must make a decision
* the system must trust the statement
* the system must execute anything

It only labels contextual intent.

---

# 10. Unknown Keys

Unknown context keys remain valid and opaque unless defined by another convention, schema, or profile.

This allows local extension without changing the core convention.

---

# 11. Advisory Instruction Comments

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

This convention treats instruction comments as:

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

# 12. Example Document

```aeon
aeon:header = {
  conventions = [
    "aeon.gp.document.v1"
    "aeon.gp.measurement.v1"
    "aeon.gp.context.v1"
  ]
}

type@{ns="aeon"} = "document"

//@ context(role="headline", audience="executive", intent="inform")
title = "Q1 Operations Summary"

//@ context(role="workflow-state", scope="project")
status = "active"

//@ context(role="estimated-cost", domain="finance")
budget@{currency="AUD" precision=0.01} = 12000

//@ context(domain="operations", audience="internal", source="system", confidence="medium")
summary =
  "Based on current inputs, delivery risk is moderate."

//@ context(audience="internal", sensitivity="restricted")
note =
  "Pending contractor confirmation."
```

---

# 13. Agentic AI Use Case

This convention is especially useful for agentic AI because it helps separate:

* raw data
* semantic meaning
* contextual relevance

Example:

```aeon
//@ context(intent="review", audience="technical", source="user")
request =
  "Check whether the schema matches the release draft."

//@ context(role="workflow-state", source="system", confidence="high")
status = "blocked"
```

A downstream AI system can use these labels to improve interpretation, prioritization, summarization, or routing.

But the convention itself does not instruct the AI to act.

---

# 14. Summary

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

Prefer soft context annotations for ordinary contextual guidance, and reserve hard context attributes for durable binding metadata.

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
