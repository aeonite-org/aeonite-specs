---
id: measurement-reference
title: Measurement Labels Reference
description: Informative reference for common unit and measurement-system labels used alongside convention attributes.
family: conventions
group: Informative Convention Appendices
status: Informative
path: specification/conventions/measurement-labels-reference
license: CC0-1.0
---

# Appendix — Informative Reference: Measurement Labels

This appendix provides a **non-exhaustive reference** of commonly used measurement labels that may appear with the `unit` and `system` attributes.

This list is **informative only**.
AEON Convention v1 does not restrict or validate the values of these attributes.

Schemas, profiles, or processors may define stricter requirements if needed.

---

# Measurement Attributes

### `unit`

Identifies the measurement label.

Example:

```
distance@{unit="m"} = 3
```

### `system`

Declares the measurement system or standard associated with the unit.

Example:

```
mass@{unit="oz" system="avoirdupois"} = 12
```

---

# Example Measurement Systems

| System         | Description                                     |
| -------------- | ----------------------------------------------- |
| `metric`       | International System of Units (SI)              |
| `imperial`     | British Imperial measurement system             |
| `US-customary` | United States customary measurement system      |
| `avoirdupois`  | weight system used for most everyday mass units |
| `troy`         | precious metal weight system                    |
| `display`      | display, screen, and raster coordinate context  |
| `css`          | CSS layout and styling unit context             |
| `typographic` | typography and font-relative measurement context |
| `print`        | print and physical output resolution context    |

---

# Example Units (non-exhaustive)

### Length

| Unit   | Typical system          |
| ------ | ----------------------- |
| `mm`   | metric                  |
| `cm`   | metric                  |
| `m`    | metric                  |
| `km`   | metric                  |
| `in`   | imperial / US-customary |
| `ft`   | imperial / US-customary |
| `yd`   | imperial                |
| `mile` | imperial / US-customary |

Example:

```
length@{unit="cm" system="metric"} = 25
```

---

### Mass

| Unit      | Typical system |
| --------- | -------------- |
| `g`       | metric         |
| `kg`      | metric         |
| `oz`      | avoirdupois    |
| `lb`      | avoirdupois    |
| `troy oz` | troy           |

Example:

```
weight@{unit="kg" system="metric"} = 82
```

---

### Volume

| Unit     | Typical system          |
| -------- | ----------------------- |
| `ml`     | metric                  |
| `l`      | metric                  |
| `fl oz`  | US-customary            |
| `pint`   | imperial / US-customary |
| `gallon` | imperial / US-customary |

Example:

```
volume@{unit="ml" system="metric"} = 500
```

---

### Display and Typography

Display-oriented units often depend on a rendering context. For example, `px` may mean a CSS reference pixel, a raster image pixel, or a device pixel depending on the surrounding profile or schema.

| Unit   | Typical system          |
| ------ | ----------------------- |
| `px`   | display / css           |
| `em`   | css / typographic       |
| `rem`  | css / typographic       |
| `pt`   | typographic / print     |
| `pc`   | typographic / print     |
| `vw`   | css                     |
| `vh`   | css                     |
| `dpi`  | print / display         |
| `ppi`  | display                 |
| `dppx` | css / display           |

Examples:

```
canvasWidth@{unit="px" system="display"} = 1280
fontSize@{unit="rem" system="css"} = 1.25
outputResolution@{unit="dpi" system="print"} = 300
```

When the distinction matters, a schema or profile should define whether `px` refers to CSS reference pixels, raster pixels, or device pixels.

---

# Precision Example

Precision may be used to indicate measurement resolution.

```
distance@{unit="m" system="metric" precision=0.01} = 3
```

This indicates the value is measured to **centimeter precision**.

The attribute does not require rounding or formatting.

---

# Notes

This appendix exists only to illustrate **common measurement labels**.

It does not:

* restrict the `unit` attribute
* define an official unit registry
* require a specific measurement ontology

Profiles or schemas may define stricter unit lists if required.

---
