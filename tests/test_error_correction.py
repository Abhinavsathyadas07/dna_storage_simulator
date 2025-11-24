import unittest
from modules.error_correction import HammingECC

class TestHammingECC(unittest.TestCase):
    def test_ecc_roundtrip(self):
        ecc = HammingECC()
        text = "DNA"
        encoded = ecc.encode(text)
        decoded, errors = ecc.decode(encoded)
        self.assertEqual(decoded, text)
        self.assertGreaterEqual(errors, 0)

if __name__ == "__main__":
    unittest.main()
