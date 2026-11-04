import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_invariants import validate_document


class ValidateInvariantsTests(unittest.TestCase):
    def test_example_is_valid(self):
        document = json.loads(
            (ROOT / "examples" / "booking" / "invariants.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_document(document), [])

    def test_duplicate_id_is_rejected(self):
        item = {
            "id": "same-id",
            "statement": "Property",
            "owner": "service",
            "scope": "writes",
            "violation": "Bad state",
            "check": {"type": "test", "command": "python test.py"},
            "evidence": "CI",
            "review_on": ["change"],
        }
        document = {"system": "example", "invariants": [item, dict(item)]}
        self.assertIn("invariants[1].id duplicates same-id", validate_document(document))

    def test_missing_detection_method_is_rejected(self):
        document = {
            "system": "example",
            "invariants": [
                {
                    "id": "property",
                    "statement": "Property",
                    "owner": "service",
                    "scope": "writes",
                    "violation": "Bad state",
                    "check": {"type": "test", "command": ""},
                    "evidence": "CI",
                    "review_on": ["change"],
                }
            ],
        }
        self.assertIn(
            "invariants[0].check.command must be a non-empty string",
            validate_document(document),
        )


if __name__ == "__main__":
    unittest.main()
