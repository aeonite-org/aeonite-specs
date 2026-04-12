---
id: aeon-core-v1-value-types
title: AEON v1 Value Types Reference
description: Reference for AEON value kinds, reserved datatype names, literal families, container forms, and reference-bearing values.
group: Core References
path: specification/aeon-v1-documentation/aeon-v1-value-types-reference
links:
  - aeon-core-v1
  - aeon-v1-contracts
---

# AEON v1 Value Types Reference

Status: official v1 reference draft
Scope: complete value-kind reference for AEON Core v1, aligned to current TypeScript parser/AES implementation.

## 1. Binding Forms

All values are bound as:

```ebnf
Binding = Key AttributeList? TypeAnnotation? "=" Value ;
```

Transport vs typed-mode example:

```aeon
contact = "John"
contact:string = "John"
```

Mode requirements:
- `transport` allows untyped non-header bindings and allows custom datatype labels;
- `strict` requires a datatype annotation on non-header bindings and rejects custom datatype labels by default;
- `custom` requires a datatype annotation on non-header bindings and allows custom datatype labels;
- typed modes do not require generic args (`arr:list = [...]` is valid);
- typed modes do not require separator specs unless the datatype itself uses them.

Implementations MAY still expose an explicit datatype-policy override, but the default semantic behavior is mode-driven.

Reserved datatype names in Core are compatibility labels, not full semantic contracts.

In particular:
- Core recognizes reserved names such as `int`, `uint`, `int32`, `float64`, `obj`, `envelope`, `trimtick`, `sep`, and `set`;
- Core checks literal-family compatibility only;
- stronger semantic enforcement such as integer-only, unsigned-only, width, or range belongs to profile/schema validation layers;
- `aeon.gp.profile.v1` and `aeon.gp.schema.v1` are the intended general-purpose baseline for making those stronger meanings operational.

## 1.1 Reserved Datatype Name Table

This section lists the accepted datatype-name families used by Core v1.

Interpretation:
- `Type` is the canonical name used in examples and docs;
- `Alternative names` are short aliases;
- `Reserved` are other accepted reserved compatibility names in the same family.

### `string`

| Field             | Names    |
| ----------------- | -------- |
| Type              | `string` |
| Alternative names | none     |
| Reserved          | none     |

### `trimtick`

| Field             | Names      |
| ----------------- | ---------- |
| Type              | `trimtick` |
| Alternative names | none       |
| Reserved          | none       |

### `number`

| Field             | Names                                                               |
| ----------------- | ------------------------------------------------------------------- |
| Type              | `number`                                                            |
| Alternative names | `n`                                                                 |
| Reserved          | `int`, `int8`, `int16`, `int32`, `int64`, `uint`, `uint8`, `uint16` |
|                   | `uint32`, `uint64`, `float`, `float32`, `float64`                   |

### `infinity`

| Field             | Names      |
| ----------------- | ---------- |
| Type              | `infinity` |
| Alternative names | none       |
| Reserved          | none       |

### `boolean`

| Field             | Names     |
| ----------------- | --------- |
| Type              | `boolean` |
| Alternative names | `bool`    |
| Reserved          | none      |

### `switch`

| Field             | Names    |
| ----------------- | -------- |
| Type              | `switch` |
| Alternative names | none     |
| Reserved          | none     |

### `hex`

| Field             | Names |
| ----------------- | ----- |
| Type              | `hex` |
| Alternative names | none  |
| Reserved          | none  |

### `radix`

| Field             | Names                                   |
| ----------------- | --------------------------------------- |
| Type              | `radix`                                 |
| Alternative names | none                                    |
| Reserved          | `radix2`, `radix6`, `radix8`, `radix12` |

### `encoding`

| Field             | Names      |
| ----------------- | ---------- |
| Type              | `encoding` |
| Alternative names | none       |
| Reserved          | `base64`, `embed`, `inline`   |

### `date`

| Field             | Names  |
| ----------------- | ------ |
| Type              | `date` |
| Alternative names | none   |
| Reserved          | none   |

### `time`

| Field             | Names  |
| ----------------- | ------ |
| Type              | `time` |
| Alternative names | none   |
| Reserved          | none   |

### `datetime`

| Field             | Names      |
| ----------------- | ---------- |
| Type              | `datetime` |
| Alternative names | none       |
| Reserved          | `zrut`     |

### `sep`

| Field             | Names |
| ----------------- | ----- |
| Type              | `sep` |
| Alternative names | none  |
| Reserved          | `set` |

### `object`

| Field             | Names      |
| ----------------- | ---------- |
| Type              | `object`   |
| Alternative names | `obj`, `o` |
| Reserved          | `envelope` |

### `list`

| Field             | Names  |
| ----------------- | ------ |
| Type              | `list` |
| Alternative names | none   |
| Reserved          | none   |

### `tuple`

| Field             | Names   |
| ----------------- | ------- |
| Type              | `tuple` |
| Alternative names | none    |
| Reserved          | none    |

### `node`

| Field             | Names  |
| ----------------- | ------ |
| Type              | `node` |
| Alternative names | none   |
| Reserved          | none   |

### `null`

| Field             | Names  |
| ----------------- | ------ |
| Type              | `null` |
| Alternative names | none   |
| Reserved          | none   |

## 2. Value Kind Catalog

| Family            | Surface                                 | Transport Example                           | Strict Example                                                  | AES `value.type`   |
| ----------------- | --------------------------------------- | ------------------------------------------- | --------------------------------------------------------------- | ------------------ |
| String            | `"..."`, `'...'`, `` `...` ``           | `name = "John"`                             | `name:string = "John"`                                          | `StringLiteral`    |
| Trimtick          | `>``...``` through `>>>>``...```        | `note = >>`...``                            | `note:trimtick = >>`...``                                       | `StringLiteral`    |
| Number            | `42`, `3.14`, `.5`, `1e3`, `1_000`      | `count = 42`                                | `count:number = 42`                                             | `NumberLiteral`    |
| Infinity         | `Infinity`, `-Infinity`                 | `top = Infinity`                            | `top:infinity = Infinity`                                       | `InfinityLiteral`  |
| NaN              | `NaN`, `-NaN`                           | `bad = NaN`                                 | `bad:nan = NaN`                                                 | `NaNLiteral`       |
| Boolean           | `true`, `false`                         | `flag = true`                               | `flag:boolean = true`                                           | `BooleanLiteral`   |
| Switch            | `yes`, `no`, `on`, `off`                | `state = on`                                | `state:switch = on`                                             | `SwitchLiteral`    |
| Hex               | `#ff00aa`                               | `color = #ff00aa`                           | `color:hex = #ff00aa`                                           | `HexLiteral`       |
| Radix             | `%1011`                                 | `bits = %1011`                              | `bits:radix[2] = %1011`                                         | `RadixLiteral`     |
| Encoding          | `$QmFzZTY0IQ==`                         | `payload = $QmFzZTY0IQ==`                   | `payload:base64 = $QmFzZTY0IQ==`                                | `EncodingLiteral`  |
| Date              | `2025-01-01`, `2024-02-29`              | `d = 2025-01-01`                            | `d:date = 2025-01-01`                                           | `DateLiteral`      |
| Time              | `09:`, `09:30`, `09:30Z`, `09:+02:00`, `09:30+02:00`, `09:30:00`, `09:30:00Z` | `t = 09:30:00`                              | `t:time = 09:30:00Z`                                            | `DateTimeLiteral`  |
| DateTime          | `2025-01-01T09`, `2025-01-01T09Z`, `2025-01-01T09+02:00`, `2025-01-01T09:30:00Z` | `ts = 2025-01-01T09:30:00Z`                 | `ts:datetime = 2025-01-01T09:30:00Z`                            | `DateTimeLiteral`  |
| ZRUT              | `2025-01-01T00:00:00Z&Australia/Sydney`, `2025-01-01T09&Europe/Belgium/Brussels`, `2025-01-01T09:30Z&Local` | `z = 2025-01-01T00:00:00Z&Australia/Sydney` | `z:zrut = 2025-01-01T00:00:00Z&Australia/Sydney`                | `DateTimeLiteral`  |
| Separator Literal | `^300x250`                              | `size = ^300x250`                           | `size:sep[x] = ^300x250`                                        | `SeparatorLiteral` |
| Object            | `{ ... }`                               | `user = { name = "John" }`                  | `user:object = { name:string = "John" }`                        | `ObjectNode`       |
| List              | `[ ... ]`                               | `arr = [1,2,3]`                             | `arr:list = [1,2,3]` or `arr:list<number> = [1,2,3]`            | `ListNode`         |
| Tuple             | `( ... )`                               | `point = (10,20)`                           | `point:tuple = (10,20)` or `point:tuple<int32,int32> = (10,20)` | `TupleLiteral`     |
| Node              | `<tag(...)>` / `<tag>`                  | `view = <div("hello")>`                     | `view:node = <div("hello")>`                                    | `NodeLiteral`      |
| Clone Ref         | `~path`                                 | `b = ~a`                                    | `b:number = ~a`                                                 | `CloneReference`   |
| Pointer Ref       | `~>path`                                | `alias = ~>a`                               | `alias:object = ~>a`                                            | `PointerReference` |

## 3. Literal Details

## 3.1 String

Examples:

```aeon
name = "John"
alias = 'J'
multiline = `Hello
World`
```

Escape sequences for quoted strings (`"` and `'`):
- `\\`, `\"`, `\'`, ``\` ``
- `\n`, `\r`, `\t`, `\b`, `\f`
- `\uXXXX`
- `\u{X...}` (1-6 hex digits, max `10FFFF`)

Nuances:
- backtick strings are raw strings and may span multiple lines;
- non-backtick strings cannot contain raw newline;
- quoted Unicode escapes must decode to valid Unicode scalar values;
- `\uXXXX` high-surrogate forms are legal only when immediately followed by a
  valid `\uXXXX` low-surrogate form in the same decoded sequence;
- lone high-surrogate and lone low-surrogate escapes are illegal;
- malformed braced Unicode escapes, incomplete Unicode escapes, non-hex escape
  payloads, and out-of-range code points are illegal;
- invalid escapes fail closed with deterministic invalid-escape diagnostics.

Examples:

```aeon
ok1 = "\u0041"
ok2 = "\u{41}"
ok3 = "\uD83D\uDE00"
```

```aeon
bad1 = "\uD800"
bad2 = "\uDC00"
bad3 = "\u{"
bad4 = "\u{110000}"
bad5 = "line1
line2"
```

Canonical notes:
- canonical single-line strings emit double-quoted strings with minimal escaping;
- canonical multiline strings may emit as trimticks using canonical indentation.

AES:
- `StringLiteral` with `value`, `raw`, and `delimiter`.

## 3.2 Trimtick

Trimticks are a distinct multiline string form.

They still produce `StringLiteral` values in AES, but unlike ordinary strings they
apply an explicit trimming step to the raw backtick payload. Because of that,
they are documented separately here instead of being treated as just another
spelling of `string`.

Examples:

```aeon
note:trimtick = >`
  one
  two
`

note:trimtick = >>`
    one
  two
`
```

Syntax:
- trimticks start with a contiguous `>` through `>>>>` marker;
- the marker must be followed by a backtick string opener;
- spaces between the contiguous marker and the backtick opener are accepted;
- the marker itself may not be split.

Trimming rules:
- trim the first empty line after the opener, if present;
- trim trailing empty lines before the closer;
- inspect the remaining non-empty lines to determine common left indentation;
- remove that indentation according to the marker's tab policy;
- preserve trailing whitespace on non-empty lines;
- preserve interior blank lines as blank lines;
- if all remaining lines are empty, the resulting value is the empty string.

Marker-width policy:
- `>```: spaces-only indentation analysis; tabs remain payload;
- `>>```: tabs normalize to width `2` for indentation analysis;
- `>>>```: tabs normalize to width `3` for indentation analysis;
- `>>>>```: tabs normalize to width `4` for indentation analysis.

Single-line trimticks are valid and behave like ordinary raw backtick content,
because there is no multiline gutter to remove.

Canonical notes:
- canonical multiline semantic strings emit as spaces-only trimticks;
- canonical output normalizes the indentation gutter to spaces only.
- canonical output may collapse trimticks to ordinary string literals when the normalized value is rendered in an inline context;
- one-line normalized trimticks in inline containers canonically emit as ordinary double-quoted strings;
- multiline trimtick values rendered inside inline object or attribute forms canonically emit as escaped double-quoted strings rather than multiline trimtick blocks;
- multiline trimtick blocks are preserved in canonical output when the enclosing canonical layout is multiline.

AES:
- `StringLiteral` with trimtick parser metadata preserved.

## 3.3 Number

Examples:

```aeon
count = 42
ratio = 3.14e-2
half = .5
large = 1_000_000
```

Nuances:
- underscore separators are accepted only between digits and normalized in parsed numeric value;
- leading-dot decimals such as `.5`, `-.5`, and `+.5` are accepted;
- invalid underscore forms include leading (`_100`), trailing (`100_`), consecutive (`100__000`), and adjacency to non-digits;
- numeric width/precision are not core-level semantics.

Canonical notes:
- underscore separators removed;
- canonicalization of `:number` values is value-normalizing while preserving the
  broad representation family (`integer`, `decimal`, `exponent`);
- leading-dot decimals normalize to an explicit zero (`.5` → `0.5`, `-.5` → `-0.5`);
- decimal-family values trim redundant trailing fractional zeroes, but retain at
  least one fractional digit (`10.00` → `10.0`);
- exponent-family values normalize to lowercase `e` and trim redundant exponent
  sign and leading exponent zeroes (`1.0E+03` → `1e3`);
- zero follows the same family rule rather than a one-off special case:
  integer zero canonically emits as `0`/`-0`, decimal zero as `0.0`/`-0.0`,
  and exponent zero as `0e0`/`-0e0`.

AES:
- `NumberLiteral` (`value` normalized, `raw` preserved).
- `NumberLiteral` is finite-only.

Underscore examples:

```aeon
n1 = 100_000      // valid
n2 = _100_000     // invalid
n3 = 100__000     // invalid
n4 = 100_000_     // invalid
```

## 3.3.1 Infinity

Examples:

```aeon
top = Infinity
bottom = -Infinity
ceiling:infinity = Infinity
floor:infinity = -Infinity
```

Nuances:
- `InfinityLiteral` is a distinct literal family from `NumberLiteral`;
- accepted surface forms are exactly `Infinity` and `-Infinity`;
- `+Infinity`, `NaN`, `-NaN`, `+NaN`, `inf`, and lowercase aliases are invalid;
- explicit `:infinity` compatibility is enforced in all modes;
- `:number` remains finite-only and rejects `InfinityLiteral`.

Canonical notes:
- canonical output preserves `Infinity` and `-Infinity` exactly;
- invalid spellings have no canonical form.

AES:
- `InfinityLiteral` with `value` and `raw` equal to `Infinity` or `-Infinity`.

## 3.3.2 NaN

Examples:

```aeon
bad = NaN
signed = -NaN
badValue:nan = NaN
signedValue:nan = -NaN
```

Nuances:
- `NaNLiteral` is a distinct literal family from `NumberLiteral`;
- accepted surface forms are exactly `NaN` and `-NaN`;
- `+NaN`, `Infinity`, `-Infinity`, lowercase aliases, and shorthand forms are invalid;
- explicit `:nan` compatibility is enforced in all modes;
- `:number` remains finite-only and rejects `NaNLiteral`.

Canonical notes:
- canonical output preserves `NaN` and `-NaN` exactly;
- invalid spellings have no canonical form.

AES:
- `NaNLiteral` with `value` and `raw` equal to `NaN` or `-NaN`.

## 3.4 Boolean

Examples:

```aeon
enabled = true         // valid boolean literal
visible = false        // valid boolean literal   
show = TRUE            // invalid as boolean literal (not a boolean token)
activate = 'true'      // valid AEON, but string literal (not boolean)
pass = 1               // valid AEON, but number literal (not boolean)
```

Nuances:
- lowercase `true`/`false` keywords.
- explicit `:boolean` compatibility is enforced in both transport and strict.

Canonical notes:
- Canonical boolean tokens are lowercase true and false.

AES:
- `BooleanLiteral`.

## 3.5 Switch

Examples:

```aeon
state = on             // valid switch literal
state:switch = off     // valid switch literal
state:switch = true    // invalid
```

Nuances:
- lexical forms: `yes`, `no`, `on`, `off`;
- untyped switch literals are allowed in transport mode;
- in strict mode, untyped switch literals must be annotated with `:switch`;
- in strict mode, non-`:switch` custom datatype aliases such as `:toggle` remain invalid even when general custom datatypes are otherwise enabled;
- in custom mode, custom datatype aliases may carry switch literals under the same policy that governs other custom datatypes;
- machine-readable surfaced `SwitchLiteral.value` remains lexical (`yes`, `no`, `on`, `off`);
- finalized JSON materializes switch literals as booleans.

AES:
- `SwitchLiteral`.

## 3.6 Hex

Examples:

```aeon
color = #ff00aa
color:hex = #ff00aa
```

Nuances:
- parsed as hex literal payload without `#` in `value`.
- surfaced machine-readable `value` is the payload-only form, while `raw` preserves the original sigiled source token;
- `_` is visual spacing only and is valid only between hex digits;
- leading, trailing, and consecutive `_` forms are invalid.

AES:
- `HexLiteral`.

## 3.7 Radix

Examples:

```aeon
bits = %1011
bits:radix[2] = %1011
```

Nuances:
- payload captured without `%`.
- radix literals are number-like rather than encoding-like;
- `radix[base]` is informative metadata rather than a generic type parameter;
- optional radix base metadata accepts decimal integers from `2` to `64`;
- spaces around the radix base inside brackets are allowed, but the integer itself must be contiguous;
- radix base forms with leading zeroes, non-decimal payloads, empty brackets, or values outside `2..64` are invalid;
- reserved aliases such as `radix2`, `radix6`, `radix8`, and `radix12` remain accepted as shorthand;
- optional leading sign `+` or `-` is allowed only once at the start of the payload;
- radix payload digits are `0-9`, `A-Z`, `a-z`, `&`, and `!` in that order;
- `.` is an optional radix decimal point and may appear at most once;
- radix decimals may omit the integer part when there is at least one radix digit after the dot (for example `%.3`, `%-.3`, `%+.1`);
- if present, the radix decimal point must still be followed by at least one radix digit;
- `_` is visual spacing only and is valid only between radix digits;
- radix payload leading zeroes are allowed and preserved as part of the represented digit sequence (for example `%00100101`);
- `/` and `=` are not valid radix payload characters;
- lexical acceptance is not base-specific radix validity;
- base-specific digit checks still belong downstream for implementation/profile/schema enforcement;
- generic forms such as `radix<2>` are invalid; radix base metadata uses brackets.

Canonical notes:
- canonicalization of `:radix[...]` values is representation-preserving rather
  than value-normalizing;
- `_` separators are removed from canonical radix output;
- the remaining digit sequence, decimal-point placement, and leading-zero width
  are otherwise preserved.

AES:
- `RadixLiteral`.

## 3.8 Encoding

Examples:

```aeon
payload = $QmFzZTY0IQ==
payload:base64 = $QmFzZTY0IQ==
payload:embed = $QmFzZTY0IQ==
payload:inline = $QmFzZTY0IQ==
```

Nuances:
- payload captured without `$`.
- `encoding`, `base64`, `embed`, and `inline` all bind to the same `EncodingLiteral` family in Core v1;
- encoding/base64 payload accepts both the standard base64 alphabet (`A-Za-z0-9+/` with optional `=` padding) and the URL-safe base64 alphabet (`A-Za-z0-9-_` with optional `=` padding);
- canonical encoding/base64 rendering prefers the URL-safe alphabet by rewriting `+` to `-` and `/` to `_`, and strips trailing `=` padding;
- lexical acceptance is not encoding-family validity;
- `a = $aa=` is unambiguous in current lexer, because the second `=` remains part of the encoding token rather than being reinterpreted as assignment.

AES:
- `EncodingLiteral`.

## 3.9 Date / Time / DateTime / ZRUT

Examples:

```aeon
start:date = 2025-01-01
at:time = 09:30:00
utc:time = 09:30:00Z
local:time = 09:30:00+02:40
ts:datetime = 2025-01-01T09:30:00Z
z:zrut = 2025-01-01T00:00:00Z&Australia/Sydney
localTime:zrut = 2025-01-01T00:00:00&Local         // ZRUT local time convention
```

Nuances:
- parser emits `DateLiteral` for date-only token;
- parser emits `DateTimeLiteral` for time and datetime-family tokens, including ZRUT (`&Zone/Name` suffix);
- standalone `time` is part of Core v1 and follows ISO 8601 time forms;
- date, time, and datetime literal recognition includes intrinsic calendar/clock range validation;
- zone suffixes (`Z`, `+hh:mm`, `-hh:mm`) may attach to valid reduced-precision time forms already admitted by Core v1, such as `09:` and `09:30`;
- `datetime` extends that same reduced-precision rule after the `T`, so forms such as `2025-01-01T09Z`, `2025-01-01T09+02:00`, and `2025-01-01T09:30Z` are valid;
- ZRUT extends the same reduced-precision datetime bases with a named zone suffix, so forms such as `2025-01-01T09&Europe/Belgium/Brussels`, `2025-01-01T09Z&Europe/Belgium/Brussels`, and `2025-01-01T09:30Z&Local` are valid `zrut` literals;
- named-zone ZRUT suffixes may contain `/`, `_`, `-`, and `+` when used as part of a contiguous zone identifier, so forms such as `America/Port-au-Prince`, `GB-Eire`, `Etc/GMT-1`, and `Etc/GMT+1` are valid zone payloads;
- uppercase `Z` is the Core v1 UTC marker form; lowercase `z` is not a temporal literal marker;
- invalid ranges such as `2025-13-40`, `2025-02-29`, `24:00`, `99:99`, and `23:59:60` are not temporal literals in Core v1;
- strict datatype compatibility treats `:time`, `:datetime`, and `:zrut` as `DateTimeLiteral`-compatible;
- local-time ZRUT convention is `...&Local` (for example `2025-01-01T00:00:00&Local`);
- ZRUT is represented as DateTime token family in AST/AES.

AES:
- `DateLiteral` or `DateTimeLiteral`.

## 3.10 Separator Literal (`^...`)

Examples:

```aeon
size:sep[x] = ^300x250
triple:set[x][y][z] = ^100x200y300z
parts:sep[|] = ^"hello world"|"this, [is] fine"
```

Datatype separator spec grammar:

```ebnf
TypeAnnotation = ":" TypeName GenericArgs? SeparatorSpec* ;
SeparatorSpec = "[" SeparatorChar "]" ;
```

Separator character rules (implementation-aligned):
- exactly 1 character;
- separator specs accept only `A-Za-z0-9!#$%&*+-.:;=?@^_|~<>`;
- horizontal whitespace and newlines may appear around the separator character inside brackets, but the separator payload itself must remain contiguous;
- multi-char specs are invalid.

Depth/policy:
- parser option `maxSeparatorDepth` (core option `maxSeparatorDepth`);
- default lock: `1`;
- capability floor target: up to `8` via policy configuration.

Payload grammar:
- separator payload begins immediately after `^` and is read as one or more contiguous segments;
- each segment is either a raw segment or an ordinary quoted string segment;
- raw segments may use only `A-Z`, `a-z`, `0-9`, and `! # $ % & * + - . : ; = ? @ ^ _ | ~ < >`;
- quoted segments use ordinary AEON single-quoted or double-quoted string lexical rules;
- backtick strings are not valid separator segments;
- no raw separator escapes are defined;
- outside quoted segments, whitespace, `\\`, `/`, `,`, and closing container boundaries are not payload characters;
- comment syntax resumes normally once a separator payload ends outside quoted segments.
- both `:sep` and `:set` may bind separator literals with or without explicit bracket specs.

AES:
- `SeparatorLiteral` with raw payload preserved.

## 4. Structured Values

## 4.1 Object

Example:

```aeon
user = {
  id:number = 1
  name:string = "John"
}
```

AES:
- `ObjectNode`.

Reserved object aliases:
- `:object`
- `:obj`
- `:o`
- `:envelope`

All of these aliases perform the same Core compatibility check: the bound value must be an object.
Core does not attach extra semantics to `:envelope`; it is an ordinary object alias that conventions may reuse.

Example:

```aeon
close:envelope = {
  integrity = {
    alg:string = "sha-256"
  }
}
```

Convention note:
- GP security conventions recommend `close:envelope` as the standard security-envelope spelling.
- That recommendation is convention-level only; Core does not privilege the key `close`.

## 4.2 List

Examples:

```aeon
arr = [1,2,3]
arr:list = [1,2,3]
arr:list<number> = [1,2,3]
```

Nuances:
- strict requires datatype presence, not generic args;
- generic args are optional syntax and not enforced by core semantic typing rules.
- nested generic type annotations are valid surface syntax and count against `max_generic_depth`.

AES:
- `ListNode`.

## 4.3 Tuple

Examples:

```aeon
point = (10,20)
point:tuple = (10,20)
point:tuple<int32,int32> = (10,20)
```

Nuances:
- tuple/list distinction is preserved in AST/AES;
- strict does not require tuple generic args.

AES:
- `TupleLiteral`.

## 4.4 Node

Examples:

```aeon
content = <div(<span("hello", <br>, "world")>)>
content:node = <div(<span("hello", <br>, "world")>)>
icon:node = <glyph>
```

Nuances:
- node forms are `<tag(...)>` for nodes with children and `<tag>` for empty nodes;
- empty-node shorthand `<tag>` is exactly equivalent to `<tag()>`;
- child-bearing node forms require the closing `>`; `<tag(...)` is invalid;
- inline node-head datatypes are permitted syntactically, but strict mode reserves node heads for `:node`;
- non-`node` inline node-head datatypes such as `<tag:pair("x", "y")>` are transport/custom forms, not strict forms;
- child list may contain mixed value kinds;
- nodes are values; node children do not become independent top-level bindings by default.

AES:
- `NodeLiteral`.

## 5. References

Examples:

```aeon
a = 1
b = ~a
c = ~>a
item = ~$.items[0]
meta = ~a@ns
```

Nuances:
- clone (`~`) and pointer (`~>`) are distinct and preserved;
- attribute selectors are valid in reference paths;
- legality checks (missing/forward/self) are core-owned.

AES:
- `CloneReference` or `PointerReference`.

## 6. EBNF Summary

```ebnf
Value = Literal | Reference | Object | List | Tuple | Node ;
Literal = String | Number | Boolean | Switch | Hex | Radix | Encoding
        | Date | DateTime | SeparatorLiteral ;
Reference = "~" RefPath | "~>" RefPath ;
Object = "{" (Binding)* "}" ;
List = "[" (Value ("," Value)*)? "]" ;
Tuple = "(" (Value ("," Value)*)? ")" ;
Node = "<" Identifier AttributeList? TypeAnnotation? "(" (Value ("," Value)*)? ")" ;
```

## 7. Canonicalization and Drift Controls

Implementers should align with:
- `appendices/appendix-canonical-form.md`
- `appendices/appendix-aes.md`
- `AEON-v1-compliance.md`

This page is intentionally implementation-cross-checked to reduce inter-implementation drift.

## 8. Out-of-Scope or Non-Distinct in Core v1

Not distinct parser value kinds in current core v1:
- bare duration literal kind (`P30D`) as dedicated AST/AES node;
- null literal kind.

These may be represented through profile/schema conventions or string/date-time forms.
