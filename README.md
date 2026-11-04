# DNA Storage Simulator

A modular Python toolkit for simulating digital data storage using DNA encoding.  
Supports compression, error correction, customizable error models, and batch processing.  
Includes CLI, web dashboard, and Jupyter notebook interfaces for research and prototyping.

## Pipeline

```
text → Huffman compression → Hamming(7,4) protection → DNA bases (2 bits per base)
     → substitution errors → decode → error correction → decompression
```

Errors are injected into the protected DNA, so error correction works on the same data that was corrupted. Hamming(7,4) corrects one flipped bit per 7-bit block. A substituted base can flip two bits at once, so higher error rates can exceed what it can fix. The whole pipeline lives in `modules/pipeline.py`, and every interface uses it.

## Features
- Compression & encoding modules
- Error correction via Hamming codes
- Customizable error models, with an optional seed for reproducible runs
- Batch processing support
- CLI, web, and notebook interfaces
- Persistent results storage

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Abhinavsathyadas07/dna_storage_simulator.git
   cd dna_storage_simulator
   ```

2. Set up your environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the main pipeline (prompts for text, or pass `--input_file`; add `--batch` to process one line at a time):

   ```bash
   python main.py --error_rate 0.01
   ```

4. Or use the command-line interface:

   ```bash
   python -m interface.cli --text "DNA can store data" --error_rate 0.02 --seed 3
   ```

5. The web dashboard needs Flask (`pip install flask`):

   ```bash
   python -m interface.web_dashboard.app
   ```

## Tests

```bash
python -m unittest discover -s tests
```

## License

MIT (or your chosen license)
