# dna_storage_simulator/main.py
import argparse
from datetime import datetime
from modules import pipeline
from storage.database import SimpleDatabase

def parse_args():
    parser = argparse.ArgumentParser(
        description="DNA Storage Simulator: Full Pipeline Runner"
    )
    parser.add_argument("--input_file", type=str, help="Path to input data file")
    parser.add_argument("--error_rate", type=float, default=0.01, help="Substitution error rate")
    parser.add_argument("--batch", action="store_true", help="Enable batch processing (each line is input)")
    parser.add_argument("--save_db", type=str, default="results_db.json", help="Results database path")
    return parser.parse_args()

def run_pipeline(text, error_rate, db=None, batch_id=None):
    print(f"\nRunning DNA storage pipeline for: {text[:50]}{'...' if len(text) > 50 else ''}")

    pipeline_result = pipeline.run(text, error_rate)

    timestamp = datetime.now().isoformat()
    result = {"timestamp": timestamp, **pipeline_result.to_dict(), "batch_id": batch_id}

    # Save to database if provided
    if db is not None:
        run_key = f"run_{timestamp}" if batch_id is None else f"batch_{batch_id}_{timestamp}"
        db.store(run_key, result)
        print(f"Saved to DB under key: {run_key}")

    print("Results:")
    print(f"  Compressed: {len(pipeline_result.compressed_bits)} bits")
    print(f"  Protected (Hamming 7,4): {len(pipeline_result.protected_bits)} bits")
    print(f"  DNA length: {len(pipeline_result.dna_seq)} bases")
    print(f"  Bases substituted: {pipeline_result.substitutions}")
    print(f"  Blocks corrected: {pipeline_result.blocks_corrected}")
    print(f"  Decompressed: {pipeline_result.decompressed}")
    print(f"  Recovered exactly: {pipeline_result.success}")
    return result

def run_batch(input_file, error_rate, db_path):
    db = SimpleDatabase(db_path)
    with open(input_file, "r") as fin:
        for idx, line in enumerate(fin):
            text = line.strip()
            if not text:
                continue
            run_pipeline(text, error_rate, db, batch_id=idx)

if __name__ == "__main__":
    args = parse_args()
    if args.batch and args.input_file:
        run_batch(args.input_file, args.error_rate, args.save_db)
    else:
        if args.input_file:
            with open(args.input_file) as fin:
                text = fin.read().strip()
        else:
            text = input("Enter data to process: ").strip()
        db = SimpleDatabase(args.save_db)
        run_pipeline(text, args.error_rate, db)
