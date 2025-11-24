import unittest
from modules.encoders import DNAEncoder

class TestDNAEncoder(unittest.TestCase):
    def test_encode_decode(self):
        encoder = DNAEncoder()
        text = "HELLO"
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, text)

if __name__ == "__main__":
    unittest.main()
