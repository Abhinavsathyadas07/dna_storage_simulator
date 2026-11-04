import unittest
from modules.compressors import HuffmanCompressor

class TestHuffmanCompressor(unittest.TestCase):
    def test_compress_decompress(self):
        compressor = HuffmanCompressor()
        text = "TEST DATA"
        codes, compressed = compressor.compress(text)
        decompressed = compressor.decompress(codes, compressed)
        self.assertEqual(decompressed, text)

    def test_single_distinct_character(self):
        compressor = HuffmanCompressor()
        codes, compressed = compressor.compress("aaaa")
        self.assertEqual(compressed, "0000")
        self.assertEqual(compressor.decompress(codes, compressed), "aaaa")

if __name__ == "__main__":
    unittest.main()
