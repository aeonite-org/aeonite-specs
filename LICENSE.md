---
license: CC-BY-4.0
---

# Aeonite Specs Licensing

This repository uses artifact-specific licenses so specifications, conventions,
fixtures, and maintenance code can each carry the license that best matches how
they are meant to be reused.

## Defaults

| Artifact type | Default license | Reason |
| --- | --- | --- |
| Normative specifications and appendices | `CC-BY-4.0` | Specification text benefits from attribution and provenance. |
| Conventions, examples, fixtures, and reusable vocabularies | `CC0-1.0` | These artifacts are meant to be copied, embedded, and adopted with minimal friction. |
| Repository maintenance scripts and other software | `MIT` | Software artifacts should remain implementation-friendly. |

Individual Markdown documents declare their license in frontmatter:

```yaml
---
license: CC-BY-4.0
---
```

If a document declares a license explicitly, that declaration controls. If a
file does not declare a license, use the default posture above based on the
artifact type and location.

Full license texts are stored in `LICENSES/`.
