# dna_storage_simulator/benchmarks/benchmark.py

"""Times each stage of the pipeline in the same order as modules/pipeline.py."""

import time

from modules.compressors import HuffmanCompressor
from modules.encoders import DNAEncoder
from modules.error_correction import HammingECC
from modules.error_models import SubstitutionErrorModel


def timed(label, fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    print(f"{label:<28} {time.perf_counter() - start:.6f} s")
    return result


def benchmark(text, error_rate=0.01, seed=0):
    compressor = HuffmanCompressor()
    encoder = DNAEncoder()
    ecc = HammingECC()
    error_model = SubstitutionErrorModel(error_rate, seed=seed)

    print("Input:", text)
    codes, compressed = timed("Compress (Huffman)", compressor.compress, text)
    protected = timed("Protect (Hamming 7,4)", ecc.encode_bits, compressed)
    dna = timed("Encode to DNA", encoder.encode_bits, protected)
    corrupted = timed("Inject substitutions", error_model.introduce_errors, dna)
    received = timed("Decode from DNA", encoder.decode_bits, corrupted)[:len(protected)]
    recovered, corrected = timed("Correct (Hamming 7,4)", ecc.decode_bits, received)
    decompressed = timed("Decompress", compressor.decompress, codes, recovered[:len(compressed)])

    print(f"Bits: {len(compressed)} compressed, {len(protected)} protected; {len(dna)} bases")
    print(f"Blocks corrected: {corrected}; recovered exactly: {decompressed == text}")


if __name__ == "__main__":
    benchmark("Test DNA Storage Benchmark. HELLO DNA!", error_rate=0.05)
