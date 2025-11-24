# dna_storage_simulator/modules/compressors/huffman_compressor.py

from typing import Optional, Dict, Tuple
import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left: Optional["HuffmanNode"] = None
        self.right: Optional["HuffmanNode"] = None

    def __lt__(self, other: "HuffmanNode"):
        return self.freq < other.freq

class HuffmanCompressor:
    """
    Implements Huffman coding for text compression.
    """

    def build_tree(self, text: str) -> Optional[HuffmanNode]:
        freq = Counter(text)
        heap = [HuffmanNode(char, f) for char, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            merged = HuffmanNode(None, n1.freq + n2.freq)
            merged.left = n1
            merged.right = n2
            heapq.heappush(heap, merged)
        return heap[0] if heap else None

    def build_codes(self, tree: Optional[HuffmanNode]) -> Dict[str, str]:
        codes = {}
        def dfs(node: Optional[HuffmanNode], code: str):
            if node is None:
                return
            if node.char is not None:
                codes[node.char] = code
                return
            dfs(node.left, code + '0')
            dfs(node.right, code + '1')
        if tree:
            dfs(tree, '')
        return codes

    def compress(self, text: str) -> Tuple[Dict[str, str], str]:
        tree = self.build_tree(text)
        codes = self.build_codes(tree)
        encoded = ''.join(codes[c] for c in text)
        return codes, encoded

    def decompress(self, codes: Dict[str, str], encoded: str) -> str:
        reverse = {code: char for char, code in codes.items()}
        decoded = []
        code = ''
        for bit in encoded:
            code += bit
            if code in reverse:
                decoded.append(reverse[code])
                code = ''
        return ''.join(decoded)

if __name__ == "__main__":
    compressor = HuffmanCompressor()
    data = "HELLO HELLO DNA"
    codes, compressed = compressor.compress(data)
    print("Codes:", codes)
    print("Compressed:", compressed)
    print("Decompressed:", compressor.decompress(codes, compressed))
