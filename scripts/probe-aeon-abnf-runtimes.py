#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Optional scoped implementation probes, not a CTS runner. Changes no parser files."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("check_aeon_abnf", Path(__file__).with_name("check-aeon-abnf.py"))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

NODE_PROBE = r'''
const {pathToFileURL} = await import('node:url');
const {resolve} = await import('node:path');
const {readFileSync} = await import('node:fs');
const root = process.argv[1];
const load = (pkg) => import(pathToFileURL(resolve(root, 'implementations/typescript/packages', pkg, 'dist/index.js')).href);
const [{compile}, {tokenize}, {parse}] = await Promise.all(['core','lexer','parser'].map(load));
const cases = JSON.parse(readFileSync(0,'utf8'));
const results = cases.map(c => {
  const parsed = parse(tokenize(c.source).tokens);
  const result = compile(c.source, {mode: c.runtime_expected.mode});
  return {id:c.id, ok:result.errors.length === 0,
    bindings:parsed.document?.bindings.length ?? null,
    value_kind:parsed.document?.bindings[0]?.value.type ?? null,
    errors:result.errors.map(e => e.code)};
});
process.stdout.write(JSON.stringify(results));
'''


def assert_expectations(cases, rows, name, manifest):
    check.require([row["id"] for row in rows] == [case["id"] for case in cases], f"Incomplete {name} probe output")
    known = {item["id"] for item in manifest["discrepancies"]}
    disagreements = []
    for case, row in zip(cases, rows):
        override = case.get("runtime_overrides", {}).get(name)
        if override:
            check.require(override["reference"] in known and override["reason"], "Unexplained runtime override")
            check.require(any(row[key] != case["runtime_expected"][key] for key in override["observed"]), "Stale runtime override")
            disagreements.append({"id": case["id"], "implementation": name, "reference": override["reference"], "reason": override["reason"]})
        for key, expected in case["runtime_expected"].items():
            if key != "mode":
                if override:
                    expected = override["observed"].get(key, expected)
                check.require(row[key] == expected, f"{name} {case['id']}: {key} expected {expected!r}, received {row[key]!r}")
    return disagreements


def probe(bundle, aeon_root, implementation_revision=None):
    manifest, grammar = check.check_metadata(bundle)
    matches = check.recognizer(grammar)
    cases = [case for case in check.read_json(bundle / "boundary-cases.json")["cases"] if "runtime_expected" in case]
    for case in cases:
        check.require(matches(case["source"]) == case["grammar_matches"], f"Grammar regression: {case['id']}")
    result = subprocess.run(["node", "--input-type=module", "-e", NODE_PROBE, str(aeon_root)],
                            input=json.dumps(cases), text=True, capture_output=True, check=True)
    ts_rows = json.loads(result.stdout)
    disagreements = assert_expectations(cases, ts_rows, "typescript", manifest)
    sys.path.insert(0, str(aeon_root / "implementations/python/src"))
    from aeon import compile_source, CompileOptions
    from aeon.lexer import tokenize
    from aeon.parser import parse_tokens
    py_rows = []
    for case in cases:
        source = case["source"]
        parsed = parse_tokens(source, tokenize(source).tokens)
        compiled = compile_source(source, CompileOptions(mode=case["runtime_expected"]["mode"]))
        bindings = parsed.document.bindings if parsed.document is not None else None
        py_rows.append({"id": case["id"], "ok": not compiled.errors,
                        "bindings": len(bindings) if bindings is not None else None,
                        "value_kind": type(bindings[0].value).__name__ if bindings else None,
                        "errors": [error.code for error in compiled.errors]})
    disagreements += assert_expectations(cases, py_rows, "python", manifest)
    if implementation_revision is not None:
        subprocess.run(["git", "-C", str(aeon_root), "cat-file", "-e", implementation_revision + "^{commit}"], check=True)
        subprocess.run(["git", "-C", str(aeon_root), "diff", "--exit-code", implementation_revision, "--"], check=True, stdout=subprocess.DEVNULL)
    revision = implementation_revision or subprocess.check_output(["git", "-C", str(aeon_root), "rev-parse", "HEAD"], text=True).strip()
    # Fingerprint the available artifacts, without claiming a clean rebuild.
    files = list((aeon_root / "implementations/python/src").rglob("*.py"))
    for dist in (aeon_root / "implementations/typescript/packages").glob("*/dist"):
        files.extend(dist.rglob("*.js"))
    hashes = {str(path.relative_to(aeon_root)): check.digest(path) for path in sorted(files)}
    return {"grammar_id": manifest["id"], "boundary_cases_sha256": check.digest(bundle / "boundary-cases.json"),
            "implementation_repository": "https://github.com/AltoPelago/aeon",
            "implementation_revision": revision,
            "implementation_revision_source": "explicit commit; tracked snapshot content checked" if implementation_revision else "checkout HEAD with working-tree disclosure",
            "implementation_worktree_dirty": False if implementation_revision else bool(subprocess.check_output(["git", "-C", str(aeon_root), "status", "--porcelain"], text=True).strip()),
            "observed_artifact_sha256": hashes, "cases_per_implementation": len(cases),
            "unexplained_mismatches": 0, "reviewed_disagreements": disagreements,
            "results": {"typescript": ts_rows, "python": py_rows},
            "limits": ["Scoped TypeScript built-module and Python-source probes; not a full CTS SUT run and no Rust/PHP claim.",
                       "The implementation checkout contains other work. Hashes identify available Python sources and TypeScript package dist JS; a clean rebuild or complete transitive dependency fingerprint is not asserted.",
                       "Implementation agreement is evidence of existing behavior, not independent normative authority."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=check.DEFAULT_BUNDLE)
    parser.add_argument("--aeon-root", type=Path, required=True)
    parser.add_argument("--write-report", type=Path)
    parser.add_argument("--implementation-revision", help="Exact isolated implementation commit; tracked content must match")
    args = parser.parse_args()
    report = probe(args.bundle, args.aeon_root.resolve(), args.implementation_revision)
    if args.write_report:
        args.write_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{report['grammar_id']}: {report['cases_per_implementation']} cases per TypeScript/Python implementation, {len(report['reviewed_disagreements'])} reviewed disagreements, zero unexplained mismatches")


if __name__ == "__main__":
    main()
