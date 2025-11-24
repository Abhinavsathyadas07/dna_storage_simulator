# dna_storage_simulator/benchmarks/benchmark.py

from modules.encoders import DNAEncoder
from modules.compressors import HuffmanCompressor
from modules.error_correction import HammingECC
from modules.error_models import SubstitutionErrorModel
import time

def benchmark(text, error_rate=0.01):
    compressor = HuffmanCompressor()
    encoder = DNAEncoder()
    ecc = HammingECC()
    error_model = SubstitutionErrorModel(error_rate)

    print("Input:", text)

    # Compression
    cmp_start = time.time()
    codes, compressed = compressor.compress(text)
    cmp_time = time.time() - cmp_start
    print(f"Compressed size: {len(compressed)} bits, time: {cmp_time:.6f} sec")

    # Encoding
    enc_start = time.time()
    dna = encoder.encode(compressed)
    enc_time = time.time() - enc_start
    print(f"DNA length: {len(dna)}, time: {enc_time:.6f} sec")

    # ECC (optional, depending on pipeline order)
    ecc_start = time.time()
    ecc_bits = ecc.encode(compressed)
    ecc_time = time.time() - ecc_start
    print(f"ECC encoded length: {len(ecc_bits)} bits, time: {ecc_time:.6f} sec")

    # Error model
    corrupted_dna = error_model.introduce_errors(dna)
    print(f"Corrupted DNA: {corrupted_dna}")

    # ECC decode (for DNA sequence, may need a bespoke pipeline—here just for bits)
    dec_start = time.time()
    recovered, errors_corrected = ecc.decode(ecc_bits)
    dec_time = time.time() - dec_start
    print(f"Errors corrected: {errors_corrected}, time: {dec_time:.6f} sec")

    # Decompression
    if recovered:  # only decompress if we got something valid
        dec_text = compressor.decompress(codes, recovered)
    else:
        dec_text = "Decompression failed"
    print("Decompressed:", dec_text)

if __name__ == "__main__":
    sample = "Test DNA Storage Benchmark. HELLO DNA!"
    benchmark(sample, error_rate=0.05)
