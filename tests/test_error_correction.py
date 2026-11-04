import unittest
from modules.error_correction import HammingECC


def flip(bits, i):
    return bits[:i] + ("1" if bits[i] == "0" else "0") + bits[i + 1:]


class TestHammingECC(unittest.TestCase):
    def test_ecc_roundtrip(self):
        ecc = HammingECC()
        text = "DNA"
        encoded = ecc.encode(text)
        decoded, errors = ecc.decode(encoded)
        self.assertEqual(decoded, text)
        self.assertEqual(errors, 0)

    def test_corrects_every_single_bit_error(self):
        ecc = HammingECC()
        encoded = ecc.encode("DNA")
        for i in range(len(encoded)):
            decoded, errors = ecc.decode(flip(encoded, i))
            self.assertEqual(decoded, "DNA", f"bit {i}")
            self.assertEqual(errors, 1, f"bit {i}")

    def test_bit_level_roundtrip_and_padding(self):
        ecc = HammingECC()
        data = "1011001110001"  # 13 bits: padded to 16
        protected = ecc.encode_bits(data)
        self.assertEqual(len(protected), 28)
        recovered, corrected = ecc.decode_bits(protected)
        self.assertEqual(recovered[:len(data)], data)
        self.assertEqual(corrected, 0)

    def test_bit_level_corrects_one_error_per_block(self):
        ecc = HammingECC()
        data = "1011001110001111"
        protected = ecc.encode_bits(data)
        damaged = flip(flip(protected, 2), 9)  # one error in each of the first two blocks
        recovered, corrected = ecc.decode_bits(damaged)
        self.assertEqual(recovered, data)
        self.assertEqual(corrected, 2)


if __name__ == "__main__":
    unittest.main()
