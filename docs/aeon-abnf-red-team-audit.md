---
license: CC-BY-4.0
---

# AEON ABNF red-team audit

Historical record for revision 0.2. The later explicit adoption of physical
newlines inside block comments is implemented in revision 0.3; its Python/ABNF
alignment resolves the separator difference recorded below. See the
[current maintenance guide](aeon-abnf.md). The version 0.2 bundle and recorded
observations remain unchanged.

The review was checked against the exact sources and CTS inputs recorded in
[revision 0.2's manifest](../resources/grammar/aeon/v1/0.2/manifest.json), the
[recognition report](../resources/grammar/aeon/v1/0.2/validation-report.json), and
[scoped implementation observations](../resources/grammar/aeon/v1/0.2/runtime-evidence.json).
Revision 0.1 is retained byte for byte. Revision 0.2 changes notation and
explanations, expands evidence and mappings, and preserves the intended document
and temporal forms. It does not change normative language rules.

The normative source baseline is `aeonite-specs` revision
`a2de96d3792dca39a27f6d3c41365d560221ccde`; CTS bytes are pinned to
`3202fd4ac4795551c06edc616ac7e7def598e030`. The implementation observations use
AEON checkout revision `805ba506a10c7f0698a4cb98e368478ccf0f65c9` with other
uncommitted work present. The evidence fingerprints the available Python sources
and TypeScript package dist JavaScript. It does not assert a clean rebuild,
complete transitive dependency fingerprint, or full implementation conformance.

| Point | Result |
| --- | --- |
| 1. Separators | ABNF already requires an external physical separator; one TypeScript/Python implementation difference was found. |
| 2. Empty documents | Existing accepted behavior, intentionally preserved and tested. |
| 3. Quoted controls | Current AEON implementations accept controls other than raw CR/LF; TOML's exclusions are not imported. |
| 4. First comment closer | The claimed formal defect does not hold for these productions; an independent oracle checks all seven channels. |
| 5. SANSA | Ownership boundary strengthened; no new SANSA authority is assigned to AEON ABNF. |
| 6. Temporal markers | Normatively specified disambiguation, preserved without broadening. |
| 7. Token boundaries | Whole-document tests verify immediate comments and reject adjacent keyword prefixes. |
| 8. Case and primitives | Valid but redundant exponent notation and inconsistent primitive spelling cleaned up. |
| 9. Nested generic closers | No demonstrated grammar defect; nested closers recognized and tested. |
| 10. Structure and manifest | Existing sections retained; stable production IDs, constraints, CTS groups and overacceptance mappings added. |

## 1. Separator recognition and implementation difference

The separator production contains a mandatory comma or newline outside a comment.
`gap` can consume a newline in one attempted decomposition; ABNF recognition can
also use another decomposition that leaves it for `separator`. Unordered
alternatives and optional whitespace are not a deterministic lexer algorithm.
That is already part of the stated recognition-only contract.

These grammar results are intentional:

- `a=1 /*comment*/ b=2` is rejected;
- `a=1 /*\n*/ b=2`, where `\n` denotes an actual line feed inside the comment,
  is rejected;
- a newline, then a comment, then a newline between the bindings is accepted.

The second case reveals a real implementation difference. TypeScript accepts it
because `consumeSeparatorOrLineBreak` compares token span line numbers; Python
requires an actual newline/comma token and rejects it. The normative
[comment non-influence rule](../sources/aeon/v1/comments-annotations-v1.aeon)
says comments must not act as separators, so revision 0.2 retains the grammar's
rejection and records `G-comment-newline-parity`. The single reviewed runtime
override is case- and implementation-specific; an unexpected result or a stale
override fails the probe. No implementation files are changed by this audit.

The old comment that `hgap` cannot consume physical newlines was imprecise:
block-comment text may contain them. The revised explanation distinguishes
consuming comment text from exposing a separator.

## 2. Zero-binding documents

Empty, ASCII-layout-only, plain-comment-only and structured-comment-only source
already matches the grammar. TypeScript and Python accept eight representative
forms in each of transport, strict and custom modes, with zero bindings.
The TypeScript parser source also has an existing empty-document contract test.
The normative Comments Reference explicitly describes a no-bindable document
and its unbound annotations. Its informative grammar-flow appendix is not
permission to impose a new one-binding minimum.

This audit preserves that behavior. A malformed or unterminated comment remains
an error; accepting a zero-binding document does not suppress lexical errors.
No new normative restriction is introduced.

## 3. Quoted control characters

Both implementations were probed with every code point U+0000 through U+001F,
and U+007F, inside each of single- and double-quoted strings. Raw LF and CR are
rejected. The other tested controls, including raw TAB and NUL, are accepted.
The normative String section forbids raw newlines and specifies escapes, but
does not impose TOML's additional control-character exclusions.

The grammar is preserved here. The observations establish current implementation
behavior; changing AEON's raw-control policy would require an explicit normative
change, rather than treating a difference from TOML as an ABNF defect.

## 4. First-closing-delimiter argument

For a closer of the form `c/`, each block production has this body shape:

```abnf
*(other / 1*"c" after) *"c" "c/"
```

This is a schematic explanation, not a separate executable production.
`other` excludes `c`. `after` excludes both `c` and `/`. Therefore neither body
alternative can consume the pair `c/`: a leader run must be followed by a
nonleader, nonslash character. The final leader run can only be followed by the
terminating slash. A complete token cannot cross an earlier matching closer.
For the brace, bracket and parenthesis channels, `c` is the closing character,
not the opening character. Nested openers have no special meaning.

The independent oracle enumerates every payload of length 0 through 5 over the
closer leader, slash, an ordinary character and LF. It appends a closer and uses
`str.find` to decide whether the first closer is at the end. All 1,365 cases per
channel, 9,555 total, agree with full-token ABNF recognition. Focused whole-source
cases also reject attempts to skip an earlier closer. This bounded test is not
an exhaustive proof over every Unicode string; the exclusion argument explains
why the construction works independently of parsing priority.

## 5. SANSA ownership

SANSA owns address syntax, while AEON owns the literal carrier and host boundary.
The existing local productions remain an informative translated vocabulary,
with `C-sansa` and the source disagreements still explicit. They are not a
replacement SANSA grammar. Supporting a future SANSA extension requires a
reviewed translation revision or a separately adopted imported grammar, not
silently widening the AEON reference subset.

## 6. Temporal disambiguation

The normative [Value Types Reference](../sources/aeon/v1/value-types-v1.aeon)
explicitly says the trailing hyphen distinguishes a year-date from a number.
Its value-kind table and temporal details also admit standalone hour precision
with a trailing colon. The scoped parser observations confirm the AST families:

| Source value | AST family |
| --- | --- |
| `2026` | `NumberLiteral` |
| `2026-` | `DateLiteral` |
| `2026-11` | `DateLiteral` |
| `2026-11-18` | `DateLiteral` |
| `12` | `NumberLiteral` |
| `12:` | `TimeLiteral` |
| `2026-T12` | `DateTimeLiteral` |

Grammar entry-rule tests separately establish that bare `2026` does not match
`date`, and bare `12` does not match `time`. A full datetime is consumed in its
entirety rather than accepted as a shorter date prefix. No markers are removed
and no bare-number temporal alternatives are added.

## 7. Boundaries and nested closers

`a=true//comment` is accepted by the grammar and both scoped implementations.
`a=truefalse` is rejected. Nested
`value:list<list<number>>=[[1,2]]` is accepted; a missing generic closer is rejected.
Two consecutive `>` characters have their ordinary closing-delimiter roles.
These observations do not make ABNF alternative order into lexer precedence.

## 8. Notation and mappings

Revision 0.2 uses explicit case-sensitive `e` and `E` exponent alternatives and
local `ascii-digit`/`hexdigit` primitives throughout. The old RFC `DIGIT` and
`HEXDIG` references were legal; the change improves consistency and avoids
relying on imported core primitives. Literal keyword casing stays exact.

Each mapping group now records stable IDs for every production, applicable
constraints, pinned CTS suite files, intentional overacceptance and known
discrepancies. Source lifecycle remains provenance; an informative translation
does not inherit normative authority. Validation rejects unknown mapped IDs,
unpinned suite references and changed runtime-evidence bytes.

## Reproduction and limits

Run the commands in the [maintenance guide](aeon-abnf.md). The standard checker
replays the 256 focused cases, two pinned Core manifests and bounded first-closer
oracle without an implementation checkout. The optional runtime probe checks
108 selected cases per implementation and records one reviewed TypeScript
separator disagreement. The runtime script verifies acceptance and, where
specified, binding counts and AST families; it does not rebuild TypeScript.

The previously documented raw-backtick escape, reference spelling, historical
empty-key and other source questions remain open. This audit does not promote
the grammar to normative status or run full Rust, PHP, AEOS, SANSA or other CTS
SUT lanes.
