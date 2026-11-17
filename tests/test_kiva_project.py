"""Basic repository contract tests for the Kiva project folder."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
KIVA = ROOT / "projects" / "kiva-loans"

class KivaProjectContractTests(unittest.TestCase):
    def test_expected_project_artifacts_exist(self):
        expected = [
            "README.md",
            "docs/source-walkthrough.md",
            "sql/metadata_tables.sql",
            "adf/pipeline-design.md",
            "notebooks/bronze_to_silver.py",
            "notebooks/silver_to_gold.py",
            "synapse/create_serverless_view.sql",
            "powerbi/dashboard-design.md",
        ]
        missing = [path for path in expected if not (KIVA / path).is_file()]
        self.assertEqual([], missing)

    def test_no_plaintext_passwords_in_project_sources(self):
        # This is a lightweight guard, not a full secret scanner.
        forbidden = ["radharam203", "password123", "accesskey="]
        for path in KIVA.rglob("*"):
            if path.is_file() and path.suffix in {".py", ".sql", ".md"}:
                text = path.read_text(encoding="utf-8").lower()
                for token in forbidden:
                    self.assertNotIn(token, text, f"Possible secret in {path}")

if __name__ == "__main__":
    unittest.main()
