# dna_storage_simulator/interface/cli.py

import argparse
from modules.encoders import DNAEncoder
from modules.compressors import HuffmanCompressor
from modules.error_correction import HammingECC
from modules.error_models import SubstitutionErrorModel

def main():
    parser = argparse.ArgumentParser(description="DNA Storage Simulator CLI")
    parser.add_argument("--text", type=str, help="Text to encode and compress")
    parser.add_argument("--error_rate", type=float, default=0.01, help="Error rate for substitution")
    args = parser.parse_args()

    compressor = HuffmanCompressor()
    encoder = DNAEncoder()
    ecc = HammingECC()
    error_model = SubstitutionErrorModel(args.error_rate)

    if args.text:
        print("Input:", args.text)
        codes, compressed = compressor.compress(args.text)
        dna = encoder.encode(compressed)
        ecc_bits = ecc.encode(compressed)
        corrupted_dna = error_model.introduce_errors(dna)
        # ECC will work on bits, not DNA for now
        recovered, errors_corrected = ecc.decode(ecc_bits)
        decompressed = compressor.decompress(codes, recovered)
        print("Compressed bits:", compressed)
        print("DNA:", dna)
        print("Corrupted DNA:", corrupted_dna)
        print("Errors corrected in ECC:", errors_corrected)
        print("Decompressed:", decompressed)

if __name__ == "__main__":
    main()
