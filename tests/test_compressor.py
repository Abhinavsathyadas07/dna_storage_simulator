import unittest
from modules.compressors import HuffmanCompressor

class TestHuffmanCompressor(unittest.TestCase):
    def test_compress_decompress(self):
        compressor = HuffmanCompressor()
        text = "TEST DATA"
        codes, compressed = compressor.compress(text)
        decompressed = compressor.decompress(codes, compressed)
        self.assertEqual(decompressed, text)

if __name__ == "__main__":
    unittest.main()
