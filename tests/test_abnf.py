# SPDX-License-Identifier: MIT
"""Regression tests for the recognition evidence guards, not an AEON parser."""
import copy
import importlib.util
import json
import shutil
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check-aeon-abnf.py"
spec = importlib.util.spec_from_file_location("check_aeon_abnf", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, grammar = check.check_metadata(check.DEFAULT_BUNDLE)
        cls.matches = staticmethod(check.recognizer(grammar))

    def test_full_consumption_and_scalar_input(self):
        self.assertTrue(self.matches('a="😀"'))
        self.assertFalse(self.matches('a=1 trailing'))
        self.assertFalse(self.matches('a="\ud800"'))

    def test_zero_bindings_is_an_intentional_document_form(self):
        for source in ['', ' \t\r\n', '// comment', '/* comment */',
                       '//@ lonely', '/# documentation #/', '\ufeff', '#!host\n// comment']:
            with self.subTest(source=source):
                self.assertTrue(self.matches(source))
        self.assertFalse(self.matches('/* unterminated'))

    def test_temporal_markers_preserve_number_disambiguation(self):
        for literal, rule in [('2026', 'number'), ('12', 'number'),
                              ('2026-', 'date'), ('2026-11', 'date'),
                              ('2026-11-18', 'date'), ('12:', 'time')]:
            self.assertTrue(self.matches(literal, rule))
        for literal, rule in [('2026', 'date'), ('12', 'time'),
                              ('2026-', 'number'), ('12:', 'number')]:
            self.assertFalse(self.matches(literal, rule))
        self.assertTrue(self.matches('a=2026-11-18T12:30:45'))

    def test_physical_separator_can_be_inside_a_block_comment(self):
        self.assertTrue(self.matches('a=1\n/*comment*/\nb=2'))
        self.assertTrue(self.matches('a=true//comment'))
        self.assertFalse(self.matches('a=1 /*comment*/ b=2'))
        self.assertTrue(self.matches('a=1 /*\n*/ b=2'))
        self.assertTrue(self.matches('a=3e3 /*\r\n*/b=399'))
        self.assertFalse(self.matches('a=1 /*\r*/ b=2'))
        self.assertFalse(self.matches('a=truefalse'))

    def test_block_comment_cannot_cross_an_earlier_closer(self):
        for name, opener, closer in [('plain', '/*', '*/'), ('doc', '/#', '#/'),
                                     ('annotation', '/@', '@/'), ('hint', '/?', '?/'),
                                     ('structure', '/{', '}/'), ('profile', '/[', ']/'),
                                     ('instructions', '/(', ')/')]:
            self.assertTrue(self.matches(opener + closer[0] + closer, name + '-block'))
            self.assertFalse(self.matches(opener + closer + 'later' + closer, name + '-block'))

    def test_newline_comment_sublanguage_requires_lf_before_first_closer(self):
        for name, opener, closer in [('plain', '/*', '*/'), ('doc', '/#', '#/'),
                                     ('annotation', '/@', '@/'), ('hint', '/?', '?/'),
                                     ('structure', '/{', '}/'), ('profile', '/[', ']/'),
                                     ('instructions', '/(', ')/')]:
            self.assertTrue(self.matches(opener + '\r\n' + closer, name + '-newline-block'))
            for payload in ['', '\r', r'\n', '\u2028', '\u2029']:
                self.assertFalse(self.matches(opener + payload + closer, name + '-newline-block'))
            self.assertFalse(self.matches(opener + closer + '\n' + closer, name + '-newline-block'))

    def test_cts_archive_replays_exact_bytes_and_rejects_drift(self):
        archive_path = check.DEFAULT_BUNDLE / 'cts-inputs.json'
        archive = check.read_json(archive_path)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            check.unpack_cts_archive(check.DEFAULT_BUNDLE, archive_path, root)
            for relative, content in archive['files'].items():
                self.assertEqual((root / relative).read_bytes(), content.encode('utf-8'))
            changed = root / 'changed-archive.json'
            changed.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'CTS archive digest changed'):
                check.unpack_cts_archive(check.DEFAULT_BUNDLE, changed, root)

    def test_quoted_control_characters_follow_aeon_not_toml(self):
        for quote in ['"', "'"]:
            for code in list(range(32)) + [127]:
                with self.subTest(quote=quote, code=code):
                    self.assertEqual(self.matches('a=' + quote + 'x' + chr(code) + 'y' + quote),
                                     code not in (10, 13))

    def test_nested_closers_and_keyword_case(self):
        self.assertTrue(self.matches('value:list<list<number>>=[[1,2]]'))
        self.assertFalse(self.matches('value:list<list<number>=[[1,2]]'))
        self.assertTrue(self.matches('a=[1e2,1E2]'))
        self.assertFalse(self.matches('a=TRUE'))

    def test_undefined_grammar_rule_fails(self):
        with self.assertRaisesRegex(ValueError, "Undefined ABNF rule"):
            check.recognizer('aeon = missing-production\n')

    def test_new_mismatches_are_never_inferred_from_diagnostics(self):
        for ok, matched, code in [(False, True, "DUPLICATE_KEY"), (True, False, "")]:
            test = {"id": "new-case", "input": {"source": "a=1"}, "expected": {"ok": ok, "errors": [{"code": code}]}}
            with self.assertRaisesRegex(ValueError, "Unclassified CTS disagreement"):
                check.classify(test, matched, None, self.manifest)

    def test_reviewed_constraints_are_not_stale_or_reusable(self):
        expectations = check.read_json(check.DEFAULT_BUNDLE / "cts-expectations.json")
        target = next(iter(expectations["targets"].values()))
        exception = next(iter(target["disagreements"].values()))
        test = {"id": "changed", "input": {"source": "a=1"}, "expected": {"ok": False}}
        with self.assertRaisesRegex(ValueError, "Changed CTS case"):
            check.classify(test, True, exception, self.manifest)
        with self.assertRaisesRegex(ValueError, "Stale CTS classification"):
            check.classify(test, False, exception, self.manifest)

    def test_case_digest_includes_effective_options_and_verdict(self):
        original = {"id": "a", "input": {"source": "a=1", "mode": "transport", "options": {}}, "expected": {"ok": True}}
        for location, field, value in [("input", "mode", "strict"), ("input", "options", {"max_events": 1}), ("expected", "ok", False)]:
            changed = copy.deepcopy(original)
            changed[location][field] = value
            self.assertNotEqual(check.case_digest(original), check.case_digest(changed))

    def test_unknown_constraint_and_wrong_classification_fail(self):
        test = {"id": "a", "input": {"source": "a=1\na=2"}, "expected": {"ok": False}}
        exception = {"case_sha256": check.case_digest(test), "grammar_matches": True, "classification": "extra-constraint", "references": ["C-keys"], "reason": "Decoded duplicate keys."}
        self.assertEqual(check.classify(test, True, exception, self.manifest), "extra-constraint")
        for field, value in [("references", ["C-nonexistent"]), ("classification", "skip"), ("references", ["G-raw-escapes"]), ("reason", "")]:
            with self.assertRaises(ValueError):
                check.classify(test, True, dict(exception, **{field: value}), self.manifest)

    def test_source_and_grammar_drift_and_incomplete_mappings_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "bundle"
            shutil.copytree(check.DEFAULT_BUNDLE, bundle)
            grammar_path = bundle / "aeon.abnf"
            original_grammar = grammar_path.read_bytes()
            grammar_path.write_bytes(original_grammar + b"; changed\n")
            with self.assertRaisesRegex(ValueError, "Grammar digest changed"):
                check.check_metadata(bundle)
            grammar_path.write_bytes(original_grammar)
            manifest_path = bundle / "manifest.json"
            original_manifest = check.read_json(manifest_path)
            changed = copy.deepcopy(original_manifest)
            changed["sources"]["structure"]["sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, "Mapped source drift"):
                check.check_metadata(bundle)
            changed = copy.deepcopy(original_manifest)
            changed["production_mappings"][0]["rules"].pop()
            manifest_path.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, "Production mapping differs"):
                check.check_metadata(bundle)

    def test_manifest_exclusions_are_explicit_and_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            suite = {"tests": [{"id": "included", "input": {"source": "a=1"}, "expected": {"ok": True}}, {"id": "excluded", "input": {"source": "a={"}, "expected": {"ok": False}}]}
            manifest = {"meta": {"lane": "core"}, "suites": [{"id": "suite", "file": "suite.json", "exclude_tests": ["excluded"]}]}
            (root / "suite.json").write_text(json.dumps(suite))
            (root / "manifest.json").write_text(json.dumps(manifest))
            _, tests, excluded, files = check.load_target(root, "manifest.json")
            self.assertEqual([test["id"] for test in tests], ["included"])
            self.assertEqual(excluded, ["excluded"])
            self.assertEqual(set(files), {"manifest.json", "suite.json"})
            manifest["suites"][0]["exclude_tests"] = ["unknown"]
            (root / "manifest.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "Unknown exclusions"):
                check.load_target(root, "manifest.json")

    def test_duplicate_case_ids_and_path_escape_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "Path escapes"):
                check.within(root, "../outside.json")
            (root / "suite.json").write_text(json.dumps({"tests": [{"id": "same", "expected": {"ok": True}}, {"id": "same", "expected": {"ok": False}}]}))
            (root / "manifest.json").write_text(json.dumps({"meta": {"lane": "core"}, "suites": [{"id": "suite", "file": "suite.json"}]}))
            with self.assertRaisesRegex(ValueError, "Duplicate CTS ID"):
                check.load_target(root, "manifest.json")


if __name__ == "__main__":
    unittest.main()
