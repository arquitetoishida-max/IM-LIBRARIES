import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from study_forms import build, validate

ROOT = Path(__file__).resolve().parents[1]


class StudyFormsTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / "fixtures/study_forms/ja-place.json").read_text(encoding="utf-8"))
        self.registry = json.loads((ROOT / "fixtures/study_forms/registry.json").read_text(encoding="utf-8"))

    def test_legacy_and_independent_alternative(self):
        self.assertEqual(validate(self.package), 0)
        result = build(self.package, self.registry)
        self.assertEqual(validate(result), 2)
        primary, sibling = result["entries"][0]["study_forms"]
        self.assertEqual(primary["legacy_entry_id"], self.package["entries"][0]["id"])
        self.assertNotIn("legacy_entry_id", sibling)
        self.assertFalse(sibling["include_by_default"])
        self.assertNotIn("study_priority", sibling)
        self.assertEqual(len(sibling["representations"]), 1)
        self.assertNotIn("study_forms", self.package["entries"][0])

    def test_idempotence_and_spelling_correction(self):
        result = build(self.package, self.registry)
        self.assertEqual(result, build(result, self.registry))
        result["entries"][0]["text"] = "ばしょ"
        result["entries"][0]["study_forms"][0]["text"] = "ばしょ"
        rebuilt = build(result, self.registry)
        self.assertEqual(result["entries"][0]["study_forms"][0]["form_id"], rebuilt["entries"][0]["study_forms"][0]["form_id"])

    def test_no_automatic_promotion_or_grammatical_duplicates(self):
        self.package["entries"][0]["alternatives"] = ["未審査"]
        result = build(self.package, {"version": 1, "packages": {}})
        self.assertEqual(validate(result), 1)
        self.package["entries"][0]["kind"] = "form"
        result = build(self.package, {"version": 1, "packages": {}})
        self.assertNotIn("study_forms", result["entries"][0])

    def test_reject_identity_default_reading_and_private_state_errors(self):
        original = build(self.package, self.registry)
        for field, value in (("english_id", "wrong"), ("form_id", "foreign:sf:1"),
                             ("recommended", True), ("reading", ""), ("grade", 7)):
            with self.subTest(field=field):
                result = copy.deepcopy(original)
                result["entries"][0]["study_forms"][1][field] = value
                with self.assertRaises(ValueError):
                    validate(result)

    def test_reject_missing_approval_unknown_entries_and_removed_forms(self):
        self.registry["packages"]["ja-place-fixture"]["ja:en:000000179"][0]["approved"] = False
        with self.assertRaises(ValueError):
            build(self.package, self.registry)
        self.registry["packages"]["ja-place-fixture"]["unknown"] = []
        with self.assertRaises(ValueError):
            build(self.package, self.registry)
        self.setUp()
        result = build(self.package, self.registry)
        with self.assertRaises(ValueError):
            build(result, {"version": 1, "packages": {}})


if __name__ == "__main__":
    unittest.main()
