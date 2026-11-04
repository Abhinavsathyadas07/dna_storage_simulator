# dna_storage_simulator/modules/pipeline.py

"""
The full DNA storage pipeline, shared by main.py, the CLI, the web dashboard
and the benchmark:

    compress (Huffman) -> protect (Hamming 7,4) -> encode (2 bits per base)
    -> corrupt (substitution errors) -> decode -> correct -> decompress

Errors are injected into the protected DNA, so the error correction works on
the same data that was corrupted.
"""

from dataclasses import asdict, dataclass

from modules.compressors import HuffmanCompressor
from modules.encoders import DNAEncoder
from modules.error_correction import HammingECC
from modules.error_models import SubstitutionErrorModel


@dataclass
class PipelineResult:
    input: str
    compressed_bits: str
    protected_bits: str
    dna_seq: str
    corrupted_dna: str
    substitutions: int
    bit_errors: int
    blocks_corrected: int
    decompressed: str
    success: bool

    def to_dict(self) -> dict:
        return asdict(self)


def run(text: str, error_rate: float = 0.01, seed=None) -> PipelineResult:
    compressor = HuffmanCompressor()
    encoder = DNAEncoder()
    ecc = HammingECC()
    error_model = SubstitutionErrorModel(error_rate, seed=seed)

    codes, compressed = compressor.compress(text)
    protected = ecc.encode_bits(compressed)
    dna_seq = encoder.encode_bits(protected)

    corrupted_dna = error_model.introduce_errors(dna_seq)

    received = encoder.decode_bits(corrupted_dna)[:len(protected)]
    recovered, blocks_corrected = ecc.decode_bits(received)
    decompressed = compressor.decompress(codes, recovered[:len(compressed)])

    return PipelineResult(
        input=text,
        compressed_bits=compressed,
        protected_bits=protected,
        dna_seq=dna_seq,
        corrupted_dna=corrupted_dna,
        substitutions=sum(a != b for a, b in zip(dna_seq, corrupted_dna)),
        bit_errors=sum(a != b for a, b in zip(protected, received)),
        blocks_corrected=blocks_corrected,
        decompressed=decompressed,
        success=decompressed == text,
    )
