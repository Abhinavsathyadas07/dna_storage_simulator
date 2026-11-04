import unittest
from modules.error_models import SubstitutionErrorModel

DNA = "ACGT" * 50


class TestSubstitutionErrorModel(unittest.TestCase):
    def test_no_errors_at_rate_zero(self):
        self.assertEqual(SubstitutionErrorModel(0.0, seed=1).introduce_errors(DNA), DNA)

    def test_every_base_changes_at_rate_one(self):
        corrupted = SubstitutionErrorModel(1.0, seed=1).introduce_errors(DNA)
        self.assertEqual(len(corrupted), len(DNA))
        self.assertTrue(all(a != b for a, b in zip(DNA, corrupted)))
        self.assertTrue(set(corrupted) <= set("ACGT"))

    def test_same_seed_same_errors(self):
        a = SubstitutionErrorModel(0.2, seed=42).introduce_errors(DNA)
        b = SubstitutionErrorModel(0.2, seed=42).introduce_errors(DNA)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
