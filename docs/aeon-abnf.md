---
license: CC-BY-4.0
---

# Maintaining the informative AEON ABNF

The formal overview is authored in
[`appendix-aeon-abnf.aeon`](../sources/appendices/v1/appendix-aeon-abnf.aeon).
The current independently versioned bundle is
[`resources/grammar/aeon/v1/0.4/`](../resources/grammar/aeon/v1/0.4/).
Revisions 0.1, 0.2 and 0.3 retain their original bytes and observations.
Normative prose retains authority; a green recognition check does not claim
full language or SUT conformance.

Revision 0.3 adopted the explicit working specification amendment: physical LF,
including LF in CRLF, inside any completed block-comment channel counts wherever
a newline separator is allowed. The `newline-block` sublanguage requires LF
before the first closer. Comments without LF, bare CR and Unicode separators do
not supply newline separation. Literal payloads and compact-token boundaries
keep their own rules. The historical TypeScript/Python difference in the
[revision 0.2 audit](aeon-abnf-red-team-audit.md) is resolved by this amendment
and the Python change, rather than by rewriting historical evidence.

## Reproduce validation

Use Python 3.10 or later for grammar checks and Python 3.12 or later for the
optional Python implementation probes:

```sh
python3 -m venv /tmp/aeon-abnf-venv
/tmp/aeon-abnf-venv/bin/python -m pip install -r scripts/requirements-abnf.txt
/tmp/aeon-abnf-venv/bin/python -m unittest discover -s tests -p 'test_abnf.py'
/tmp/aeon-abnf-venv/bin/python scripts/check-aeon-abnf.py --cts-root ../aeonite-cts
bash scripts/pre-commit-check.sh
```

The checker compares exact manifest and suite bytes, including the committed Core next amendment. Its commit and SHA-256 digests are
recorded explicitly. The specification source amendments are identified by file
hashes relative to the recorded upstream baseline.
The released Core 0.5 files remain unchanged.

For fully offline CI replay, use the exact-byte CTS input evidence archive:

```sh
/tmp/aeon-abnf-venv/bin/python scripts/check-aeon-abnf.py --cts-archive resources/grammar/aeon/v1/0.4/cts-inputs.json
```

The archive retains the authoritative external manifest/suite bytes, their MIT
license and provenance. It is read-only recognition evidence, not a second CTS
authoring surface. All verdict changes must originate in `aeonite-cts`; refresh
an evidence archive only in a new reviewed grammar revision. The offline replay
and direct checkout produce the same report. This avoids a cross-repository CI
dependency on a future CTS merge.

The Python ABNF backend and package version are fixed. Parser exceptions fail
the run rather than being counted as syntax rejections. The default command
compares freshly computed evidence with the checked-in report. The dependency-free
`--metadata-only` mode checks current source pins, anchors, production mappings
and evidence hashes in pre-commit checks; it explicitly does not run recognition.

The optional scoped runtime probe requires built TypeScript modules and Python
sources in an AEON checkout:

```sh
/tmp/aeon-abnf-venv/bin/python scripts/probe-aeon-abnf-runtimes.py --aeon-root ../../altopelago/aeon
```

It checks 315 cases per implementation in revision 0.3, including the 207 new
shared CTS vectors, without rebuilding TypeScript. There are no remaining runtime
overrides in this revision. The recorded observations disclose the dirty checkout
and fingerprint the available artifacts, without claiming complete transitive
build provenance. `--write-report` is required to replace runtime evidence; its
manifest digest must then be explicitly reviewed and updated.

## Bundle contract

- `aeon.abnf` contains RFC 5234 + RFC 7405 grammar over decoded scalar values.
  Its `aeon` entry consumes the complete input and has no parser-specific hooks.
- `manifest.json` records source digests, baseline Git revision, working-input
  status, source IDs, lifecycle and normativity, section-level mappings, stable
  production IDs, constraints, CTS suite groups and intentional overacceptance.
  `C-` IDs catalogue obligations; `G-` records unresolved discrepancies; `H-`
  records historical expectations. These IDs do not create normative requirements.
- `cts-expectations.json` pins consumed external manifests and suites. Every
  recognition disagreement is explicit, with a complete case digest, expected
  recognition, explanation and references. There is no error-code allowlist.
- `cts-inputs.json` is the licensed exact-byte external CTS evidence archive.
- `boundary-cases.json` contains recognition and selected runtime expectations.
  It includes intentional grammar overacceptance and is not an official CTS suite.
- `runtime-evidence.json` records local TypeScript/Python observations and limits.
- `validation-report.json` records selected/excluded accounting, artifact hashes,
  reviewed disagreements, and independent bounded comment oracles. Each of 9,555
  payloads checks both first-closer recognition and the LF-bearing sublanguage.

The baseline includes draft normative references. The grammar does not confer
published status on drafts and is not a new language compatibility snapshot.

## Interpreting the report

`positive-match` and `negative-rejected` mean recognition agrees with a CTS
verdict. A negative rejection does not prove that it occurred for the intended
diagnostic reason. `extra-constraint` means matching source still needs the
catalogued check; the grammar checker does not execute it.

`open-source-discrepancy` and `historical-expectation` retain reviewed differences.
Revision 0.3 still misses one positive legacy reference fixture per target and
retains the known raw-backtick escape questions. Zero-binding documents and the
number-versus-temporal markers remain intentional supported forms.

Revision 0.4 preserves 0.3 grammar behavior and refreshes source/CTS provenance
for the isolated PRs. Earlier evidence is retained unchanged.

The report covers the pinned Core 0.5 target (299 selections), the amended Core
next target (655 selections), 463 focused cases and bounded lexical oracles.
It does not establish exhaustive language equivalence, ambiguity freedom,
performance bounds, annotation attachment or downstream semantics.

## Revise without losing evidence

Retain shared revision bytes. Create a new versioned directory for substantive
changes, then update the default bundle and CI command together. Review source
and CTS differences before changing hashes or verdict classifications.

Historical 0.1 and 0.2 source pins predate the amendment. To replay their reports
against a matching old CTS checkout, pass `--bundle` and `--historical-sources`:
that explicitly reads the mapped source bytes from the bundle's recorded local
Git revision, checks their hashes, and leaves the working tree untouched. It does
not replace missing inputs or bypass a digest mismatch. The source bytes in the newer bundles are identified by their hashes and are
not claimed to be contained in their baseline Git commit.

Use `--write-report <path>` only after reviewing the new source mappings,
classifications, boundary cases and archive. It writes evidence, not verdicts.
Before publication, run the consuming publisher's audits, projections and build.
ABNF/metadata are CC-BY-4.0; focused fixtures are CC0-1.0; maintenance code is MIT;
the copied CTS archive retains the external MIT license.
