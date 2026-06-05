---
id: aeon-gp-convention-v1
title: AEON GP Convention v1
description: Draft convention-authoring template for creating focused AEON general-purpose conventions.
family: conventions
group: General-Purpose Conventions
status: Draft
path: specification/conventions/aeon-gp-convention-v1
license: CC0-1.0
links:
  - aeon-conventions-overview
---

# AEON GP Convention v1

Convention identifier: `aeon.gp.convention.v1`

## Status

Draft convention-authoring template

---

# 1. Purpose

`aeon.gp.convention.v1` is a focused template for designing new AEON conventions.

It does not define a broad shared vocabulary.
Instead, it describes the shape a convention specification should follow so independently authored conventions remain predictable and interoperable.

Use this template when creating a new convention such as:

```text
aeon.gp.measurement.v1
aeon.gp.document.v1
org.example.finance.v1
```

---

# 2. Convention Design Rule

A convention should define one coherent interpretation domain.

Good convention scopes:

* document metadata
* measurement labels
* temporal values
* collection semantics
* security envelope structure
* domain-specific finance labels

Avoid mixing unrelated vocabularies into a single convention.

---

# 3. Recommended Document Structure

A convention specification should include:

1. Purpose
2. Scope
3. Design goals
4. Non-goals
5. Reserved vocabulary
6. Processing or interpretation rules
7. Unknown-key behavior
8. Validation posture
9. Examples
10. Relationship to other conventions

Not every convention needs every section, but each convention should make its scope and non-goals explicit.

---

# 4. Vocabulary Guidance

Reserved keys defined by a convention should be:

* lowercase ASCII identifiers
* narrowly scoped
* stable within the version
* descriptive rather than imperative

Unknown keys should remain opaque unless a schema, profile, processor, or another convention defines them.

---

# 5. Processing Guidance

Conventions define interpretation agreements.

They should not:

* alter AEON core syntax
* redefine canonicalization
* create hidden execution semantics
* require processors to infer behavior not declared by the convention

If behavior depends on policy, algorithms, trust, or runtime choices, define that behavior in a profile or processor specification rather than in the base convention.

---

# 6. Dependency Guidance

If a convention depends on another convention, state that dependency explicitly.

Example:

```text
aeon.gp.signature.v1
requires
aeon.gp.integrity.v1
```

Dependencies should be narrow and justified.

---

# 7. Example Convention Skeleton

```markdown
# AEON Example Convention v1

Convention identifier: `org.example.topic.v1`

## Status

Draft interoperability convention

# 1. Purpose

Define the interpretation domain.

# 2. Scope

State what is covered and what is not covered.

# 3. Reserved Vocabulary

List reserved keys or structures.

# 4. Processing Rules

Describe how consumers should interpret the vocabulary.

# 5. Examples

Show minimal and realistic examples.
```

---

# 8. Relationship to the Overview

General rules for declaring conventions, convention modes, naming, versioning, and processing belong to the AEON Conventions Overview.

Individual convention documents should focus on the vocabulary and behavior they define.
