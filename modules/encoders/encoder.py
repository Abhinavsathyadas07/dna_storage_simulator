# dna_storage_simulator/modules/encoders/dna_encoder.py

class DNAEncoder:
    """
    A simple DNA Encoder for converting text into a DNA base sequence (A, T, C, G).
    
    This implementation maps every two bits of each byte to a DNA base.
    """

    BASES = ['A', 'C', 'G', 'T']

    def __init__(self):
        pass

    def encode(self, data: str) -> str:
        """
        Encode an ASCII string to a DNA sequence using 2-bits per base.
        """
        dna_seq = []
        for char in data:
            ascii_val = ord(char)
            # Split 8 bits into four 2-bit chunks
            for shift in (6, 4, 2, 0):
                two_bits = (ascii_val >> shift) & 0b11
                dna_seq.append(self.BASES[two_bits])
        return ''.join(dna_seq)

    def encode_bits(self, bits: str) -> str:
        """
        Encode a string of '0'/'1' bits directly, two bits per base
        (A=00, C=01, G=10, T=11). An odd-length input is padded with one '0'.
        """
        if len(bits) % 2:
            bits += '0'
        return ''.join(self.BASES[int(bits[i:i + 2], 2)] for i in range(0, len(bits), 2))

    def decode_bits(self, dna_sequence: str) -> str:
        """
        Decode a DNA sequence back to its bit string, two bits per base.
        """
        return ''.join(format(self.BASES.index(base), '02b') for base in dna_sequence)

    def decode(self, dna_sequence: str) -> str:
        """
        Decode a DNA sequence back to the string using 2-bits per base.
        (Assumes input length is a multiple of 4)
        """
        chars = []
        for i in range(0, len(dna_sequence), 4):
            byte = 0
            for j in range(4):
                base = dna_sequence[i + j]
                two_bits = self.BASES.index(base)
                byte = (byte << 2) | two_bits
            chars.append(chr(byte))
        return ''.join(chars)

if __name__ == "__main__":
    # Basic test/demo usage
    encoder = DNAEncoder()
    text = "HELLO"
    encoded = encoder.encode(text)
    print("Encoded:", encoded)
    decoded = encoder.decode(encoded)
    print("Decoded:", decoded)
