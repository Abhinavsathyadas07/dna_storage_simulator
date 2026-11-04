# dna_storage_simulator/interface/cli.py

import argparse

from modules import pipeline


def main():
    parser = argparse.ArgumentParser(description="DNA Storage Simulator CLI")
    parser.add_argument("--text", type=str, required=True, help="Text to store")
    parser.add_argument("--error_rate", type=float, default=0.01, help="Probability of a substitution per base")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducible errors")
    args = parser.parse_args()

    result = pipeline.run(args.text, args.error_rate, seed=args.seed)
    print("Input:", result.input)
    print("Compressed bits:", result.compressed_bits)
    print("DNA:", result.dna_seq)
    print("Corrupted DNA:", result.corrupted_dna)
    print("Bases substituted:", result.substitutions)
    print("Blocks corrected:", result.blocks_corrected)
    print("Decompressed:", result.decompressed)
    print("Recovered exactly:", result.success)


if __name__ == "__main__":
    main()
