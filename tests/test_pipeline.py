import unittest
from modules import pipeline


class TestPipeline(unittest.TestCase):
    def test_recovers_text_exactly_without_errors(self):
        result = pipeline.run("DNA can store data", error_rate=0.0, seed=1)
        self.assertTrue(result.success)
        self.assertEqual(result.substitutions, 0)
        self.assertEqual(result.blocks_corrected, 0)

    def test_two_bits_per_base(self):
        result = pipeline.run("HELLO WORLD", error_rate=0.0, seed=1)
        self.assertEqual(len(result.compressed_bits), 32)
        self.assertEqual(len(result.protected_bits), 56)
        self.assertEqual(len(result.dna_seq), 28)

    def test_corrects_errors_injected_into_the_protected_dna(self):
        # Search seeds for a run where substitutions happened and every damaged
        # block had a single flipped bit, so Hamming(7,4) can repair all of them.
        for seed in range(500):
            result = pipeline.run("DNA can store data", error_rate=0.02, seed=seed)
            if result.substitutions and result.blocks_corrected == result.bit_errors:
                self.assertNotEqual(result.corrupted_dna, result.dna_seq)
                self.assertTrue(result.success)
                return
        self.fail("no fully correctable run found")

    def test_reproducible_with_a_seed(self):
        a = pipeline.run("seeded", error_rate=0.1, seed=7)
        b = pipeline.run("seeded", error_rate=0.1, seed=7)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
