import unittest
from modules.encoders import DNAEncoder


class TestDNAEncoder(unittest.TestCase):
    def test_encode_decode(self):
        encoder = DNAEncoder()
        text = "HELLO"
        encoded = encoder.encode(text)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, text)

    def test_bits_map_two_per_base(self):
        encoder = DNAEncoder()
        self.assertEqual(encoder.encode_bits("00011011"), "ACGT")
        self.assertEqual(encoder.decode_bits("TGCA"), "11100100")

    def test_bits_roundtrip_with_padding(self):
        encoder = DNAEncoder()
        bits = "101"
        self.assertEqual(encoder.encode_bits(bits), "GG")
        self.assertEqual(encoder.decode_bits(encoder.encode_bits(bits))[:len(bits)], bits)


if __name__ == "__main__":
    unittest.main()
