#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check the informative ABNF artifact and recognize source text from pinned CTS.

This does not execute an AEON SUT or implement the extra constraints. Every
recognition/CTS disagreement requires a reviewed, input-pinned classification.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.metadata
from itertools import product
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = ROOT / "resources/grammar/aeon/v1/0.5"
PARSER_VERSION = "2.9.0"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def case_digest(test):
    """Pin options, mode, expectations and source, not just the display ID."""
    data = json.dumps(test, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("ascii")).hexdigest()


def within(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), f"Path escapes repository: {relative}")
    return path


def check_metadata(bundle, root=ROOT, historical_sources=False):
    manifest = read_json(bundle / "manifest.json")
    require(manifest["normativity"] == "informative", "Grammar must remain informative")
    require(digest(bundle / "aeon.abnf") == manifest["grammar_sha256"], "Grammar digest changed")
    grammar = (bundle / "aeon.abnf").read_text(encoding="ascii")
    source_texts = {}

    def source_text(source):
        relative = source["path"]
        if relative not in source_texts:
            path = within(root, relative)
            if historical_sources:
                revision = manifest["spec_revision"]
                require(re.fullmatch(r"[0-9a-f]{40}", revision), "Invalid historical source revision")
                data = subprocess.check_output(["git", "-C", str(root), "show", f"{revision}:{relative}"])
            else:
                data = path.read_bytes()
            require(hashlib.sha256(data).hexdigest() == source["sha256"],
                    f"Mapped source drift: {relative}; review a new grammar revision")
            source_texts[relative] = data.decode("utf-8")
        return source_texts[relative]
    # Production names are case insensitive. =/ extends an existing production.
    definitions = re.findall(r"^([a-zA-Z][a-zA-Z0-9-]*)\s*=(/?)", grammar, re.M)
    declared = set()
    for name, extension in definitions:
        name = name.lower()
        require((name in declared) == bool(extension), f"Invalid definition/extension: {name}")
        declared.add(name)
    require(manifest["entry_rule"] in declared, "Entry rule is undefined")
    mapped = [rule.lower() for group in manifest["production_mappings"] for rule in group["rules"]]
    require(set(mapped) == declared, f"Production mapping differs: {set(mapped) ^ declared}")
    require(len(mapped) == len(set(mapped)), "Duplicate production mapping")
    require(len({c["id"] for c in manifest["constraints"]}) == len(manifest["constraints"]), "Duplicate constraint ID")
    require(len({d["id"] for d in manifest["discrepancies"]}) == len(manifest["discrepancies"]), "Duplicate discrepancy ID")
    if "archive" in manifest["cts"]:
        require(digest(within(bundle, manifest["cts"]["archive"])) == manifest["cts"]["archive_sha256"], "CTS archive digest changed")
    if "mechanical_audit" in manifest:
        constraint_ids = {item["id"] for item in manifest["constraints"]}
        discrepancy_ids = {item["id"] for item in manifest["discrepancies"]}
        for group in manifest["production_mappings"]:
            require(group["production_ids"] == {rule: f"aeon-core-v1/{rule}" for rule in group["rules"]}, "Stable production IDs differ")
            require(set(group["constraints"]) <= constraint_ids, "Unknown mapped constraint")
            require(set(group["intentional_overacceptance"]) <= set(group["constraints"]), "Unmapped overacceptance")
            require(set(group["discrepancies"]) <= discrepancy_ids, "Unknown mapped discrepancy")
        audit = manifest["mechanical_audit"]
        require(digest(within(bundle, audit["runtime_evidence"])) == audit["runtime_evidence_sha256"], "Recorded runtime evidence drift")
    for source_id, source in manifest["sources"].items():
        if "path" in source:
            text = source_text(source)
            for field, value in [("id", source["document_id"]), ("lifecycle", source["lifecycle"]), ("normativity", source["normativity"])]:
                require(f'{field}:string = "{value}"' in text, f"Source metadata differs: {source_id}/{field}")
    for item in manifest["production_mappings"] + manifest["constraints"] + manifest["discrepancies"]:
        require(item["sources"], "Mapping/constraint/discrepancy requires a source")
        for reference in item["sources"]:
            source_id, anchor = reference.split("#", 1)
            source = manifest["sources"][source_id]
            if "path" in source:
                text = source_text(source)
                require(f"[# {anchor}]" in text, f"Missing source anchor: {reference}")
            else:
                require(anchor in source["sections"], f"Unmapped RFC section: {reference}")
    return manifest, grammar


def recognizer(grammar):
    os.environ["ABNF_NO_RUST"] = "1"
    try:
        from abnf import Rule, ParseError
    except ImportError as error:
        raise ValueError("Install scripts/requirements-abnf.txt in a virtual environment") from error
    require(importlib.metadata.version("abnf") == PARSER_VERSION, f"Use abnf=={PARSER_VERSION}")

    class AEON(Rule):
        pass

    AEON.load_grammar(grammar)
    for rule in AEON.rules():
        require(hasattr(rule, "definition"), f"Undefined ABNF rule: {rule.name}")

    def matches(source, entry="aeon"):
        require(isinstance(source, str), "CTS source must be a string")
        # Input model is scalar values, even when a caller bypasses UTF-8 decoding.
        if any(0xD800 <= ord(char) <= 0xDFFF for char in source):
            return False
        try:
            AEON(entry).parse_all(source)
            return True
        except ParseError:
            return False

    return matches


def load_target(cts_root, relative):
    cts_root = cts_root.resolve()
    path = within(cts_root, relative)
    manifest = read_json(path)
    require(manifest["meta"]["lane"] == "core", f"Not a Core target: {relative}")
    tests, excluded, files, ids = [], [], {relative: digest(path)}, set()
    for suite in manifest["suites"]:
        suite_path = within(cts_root, str(path.parent.relative_to(cts_root) / suite["file"]))
        files[str(suite_path.relative_to(cts_root))] = digest(suite_path)
        data = read_json(suite_path)
        excluded_ids = suite.get("exclude_tests", [])
        require(len(set(excluded_ids)) == len(excluded_ids), f"Duplicate exclusions: {suite['id']}")
        suite_ids = {test["id"] for test in data["tests"]}
        require(set(excluded_ids) <= suite_ids, f"Unknown exclusions: {suite['id']}")
        for test in data["tests"]:
            require(test["id"] not in ids, f"Duplicate CTS ID: {test['id']}")
            ids.add(test["id"])
            require(isinstance(test["expected"]["ok"], bool), f"Missing CTS verdict: {test['id']}")
            if test["id"] in excluded_ids:
                excluded.append(test["id"])
            else:
                tests.append(test)
    return manifest, tests, excluded, files


def classify(test, matched, exception, manifest):
    ok = test["expected"]["ok"]
    if matched == ok:
        require(exception is None, f"Stale CTS classification: {test['id']}")
        return "positive-match" if ok else "negative-rejected"
    require(exception is not None, f"Unclassified CTS disagreement: {test['id']}")
    require(case_digest(test) == exception["case_sha256"], f"Changed CTS case: {test['id']}")
    require(matched == exception["grammar_matches"], f"Changed recognition: {test['id']}")
    kind = exception["classification"]
    known = {item["id"] for item in manifest["constraints"] + manifest["discrepancies"]}
    require(exception["references"] and set(exception["references"]) <= known, f"Unknown classification reference: {test['id']}")
    require(exception["reason"].strip(), f"Missing classification explanation: {test['id']}")
    if kind == "extra-constraint":
        require(not ok and matched, f"Not an additional rejection: {test['id']}")
        require(all(ref.startswith("C-") for ref in exception["references"]), f"Extra constraint must use C- IDs: {test['id']}")
    elif kind == "historical-expectation":
        require(not ok and matched and all(ref.startswith("H-") for ref in exception["references"]), f"Invalid historical expectation: {test['id']}")
    else:
        require(kind == "open-source-discrepancy", f"Unknown classification: {kind}")
        require(all(ref.startswith("G-") for ref in exception["references"]), f"Discrepancy must use G- IDs: {test['id']}")
    return kind


def audit_first_closers(matches, maximum_length=5, newline_blocks=False):
    """A bounded independent oracle; no productions are used to generate it.

    A whole block-comment token must end at source.find(closer, len(opener)).
    Include each closer leader, slash, ordinary content and LF in every possible
    payload up to the declared bound. This tests all seven lexical channels.
    """
    channels = [("plain", "/*", "*/"), ("doc", "/#", "#/"),
                ("annotation", "/@", "@/"), ("hint", "/?", "?/"),
                ("structure", "/{", "}/"), ("profile", "/[", "]/"),
                ("instructions", "/(", ")/")]
    counts = {}
    for name, opener, closer in channels:
        count = 0
        for length in range(maximum_length + 1):
            for characters in product((closer[0], "/", "x", "\n"), repeat=length):
                source = opener + "".join(characters) + closer
                expected = source.find(closer, len(opener)) == len(source) - len(closer)
                require(matches(source, name + "-block") == expected,
                        f"First-closer oracle disagrees: {name}, {source!r}")
                if newline_blocks:
                    expected_newline = expected and "\n" in source[len(opener):-len(closer)]
                    require(matches(source, name + "-newline-block") == expected_newline,
                            f"Newline-block oracle disagrees: {name}, {source!r}")
                count += 1
        counts[name] = count
    report = {"payload_maximum_length": maximum_length, "cases_per_channel": counts,
            "total": sum(counts.values()), "mismatches": 0,
            "limit": "Exhaustive only within the declared four-character alphabet and payload bound; not a proof over all Unicode strings."}
    if newline_blocks:
        report["newline_block_assertions"] = sum(counts.values())
    return report


def validate(bundle, cts_root, historical_sources=False):
    manifest, grammar = check_metadata(bundle, historical_sources=historical_sources)
    matches = recognizer(grammar)
    boundary_cases = read_json(bundle / "boundary-cases.json")["cases"]
    boundary_ids = set()
    for case in boundary_cases:
        require(case["id"] not in boundary_ids, f"Duplicate boundary case: {case['id']}")
        boundary_ids.add(case["id"])
        require(matches(case["source"], case.get("entry", "aeon")) == case["grammar_matches"], f"Boundary recognition differs: {case['id']}")
    expectations = read_json(bundle / manifest["cts"]["expectations"])
    require(set(expectations["targets"]) == set(manifest["cts"]["targets"]), "CTS target inventory differs")
    targets = []
    for relative in manifest["cts"]["targets"]:
        target, tests, excluded, files = load_target(cts_root, relative)
        pinned = expectations["targets"][relative]
        require(files == pinned["files_sha256"], f"CTS file drift: {relative}; do not reuse this result for changed CTS bytes")
        if "mechanical_audit" in manifest:
            consumed_files = {path for target in expectations["targets"].values() for path in target["files_sha256"]}
            for group in manifest["production_mappings"]:
                require(set(group["cts_suite_files"]) <= consumed_files, "Mapped CTS group was not pinned")
        overrides = pinned["disagreements"]
        require(set(overrides) <= {test["id"] for test in tests}, f"Unused CTS classifications: {relative}")
        counts, disagreements = Counter(), []
        for test in tests:
            matched = matches(test["input"]["source"])
            classification = classify(test, matched, overrides.get(test["id"]), manifest)
            counts[classification] += 1
            if matched != test["expected"]["ok"]:
                disagreements.append({"id": test["id"], "classification": classification, "references": overrides[test["id"]]["references"]})
        require(sum(counts.values()) == len(tests), "Incomplete CTS accounting")
        targets.append({"manifest": relative, "snapshot_id": target["meta"]["snapshot_id"], "selected": len(tests), "excluded": excluded, "counts": dict(sorted(counts.items())), "disagreements": disagreements})
    report = {"grammar_id": manifest["id"], "grammar_sha256": digest(bundle / "aeon.abnf"), "manifest_sha256": digest(bundle / "manifest.json"), "expectations_sha256": digest(bundle / "cts-expectations.json"), "boundary_cases_sha256": digest(bundle / "boundary-cases.json"), "recognizer": f"abnf=={PARSER_VERSION} (Python backend)", "spec_revision": manifest["spec_revision"], "cts_revision": manifest["cts"]["revision"], "boundary_cases": len(boundary_cases), "targets": targets, "limits": ["Recognition only: extra constraints are classified, not executed; no AEON SUT was run.", "Reviewed source discrepancies remain open; informative status is unchanged.", "Only the pinned Core manifests and local boundary cases were evaluated; no SANSA, AEOS, canonical, annotation or other SUT lane coverage is claimed.", "Full-document recognition does not establish an unambiguous parse, lexer precedence, performance bounds or universal language coverage."]}
    if "mechanical_audit" in manifest:
        report["first_closer_audit"] = audit_first_closers(matches, manifest["mechanical_audit"]["comment_payload_max_length"], manifest["mechanical_audit"].get("comment_newline_separators", False))
        report["runtime_evidence_sha256"] = manifest["mechanical_audit"]["runtime_evidence_sha256"]
        report["limits"][0] = "CTS recognition only: extra constraints are classified, not executed; no CTS SUT was run. Separate optional runtime probes are recorded independently."
    return report


def unpack_cts_archive(bundle, archive_path, destination):
    manifest = read_json(bundle / "manifest.json")
    require(digest(archive_path) == manifest["cts"]["archive_sha256"], "CTS archive digest changed")
    archive = read_json(archive_path)
    for relative, content in archive["files"].items():
        path = within(destination, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--cts-root", type=Path)
    parser.add_argument("--cts-archive", type=Path, help="Replay the bundle's exact-byte external CTS input archive offline")
    parser.add_argument("--historical-sources", action="store_true", help="Read old mapped source bytes from the bundle's local Git revision")
    parser.add_argument("--metadata-only", action="store_true", help="Check source pins and production mappings without third-party dependencies")
    parser.add_argument("--write-report", type=Path, help="Write a report after validation (does not create classifications)")
    args = parser.parse_args()
    try:
        if args.metadata_only:
            require(args.cts_root is None and args.cts_archive is None and args.write_report is None, "Metadata-only cannot validate CTS or write a report")
            manifest, _ = check_metadata(args.bundle, historical_sources=args.historical_sources)
            print(f"{manifest['id']}: source pins and production mappings checked (recognition not run)")
            return
        require((args.cts_root is not None) != (args.cts_archive is not None), "Pass exactly one of --cts-root or --cts-archive")
        if args.cts_archive:
            with tempfile.TemporaryDirectory() as temporary:
                destination = Path(temporary).resolve()
                unpack_cts_archive(args.bundle, args.cts_archive, destination)
                report = validate(args.bundle, destination, args.historical_sources)
        else:
            report = validate(args.bundle, args.cts_root.resolve(), args.historical_sources)
        if args.write_report:
            args.write_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        else:
            require(report == read_json(args.bundle / "validation-report.json"), "Recorded report differs; review and regenerate it explicitly")
        print(f"{report['grammar_id']}: {report['boundary_cases']} boundary cases checked")
        for target in report["targets"]:
            print(f"{target['snapshot_id']}: {target['selected']} selected, {len(target['excluded'])} excluded; {target['counts']}")
    except (ValueError, KeyError, OSError) as error:
        print(f"ABNF check failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
