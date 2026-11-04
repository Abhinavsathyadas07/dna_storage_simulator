# dna_storage_simulator/modules/error_correction/hamming_ecc.py

from typing import Tuple

class HammingECC:
    """
    Implements basic Hamming(7,4) error-correcting code.
    Encodes 4 bits into 7 bits, can correct single-bit errors per block.
    """

    def _bitlist(self, n: int, length: int) -> list:
        return [(n >> i) & 1 for i in reversed(range(length))]

    def encode(self, data: str) -> str:
        """
        Encodes ASCII string data using Hamming(7,4) code per byte.
        Returns string of '0' and '1' representing the encoded bit sequence.
        """
        encoded_bits = []
        for ch in data:
            bits = self._bitlist(ord(ch), 8)
            # Split into two 4-bit nibbles
            for nibble in [bits[:4], bits[4:]]:
                codeword = self._encode_nibble(nibble)
                encoded_bits.extend(codeword)
        return ''.join(str(b) for b in encoded_bits)

    def encode_bits(self, bits: str) -> str:
        """
        Encodes a string of '0'/'1' bits with Hamming(7,4), padding with zeros
        to a multiple of 4. Returns the protected bit string.
        """
        padded = bits + "0" * (-len(bits) % 4)
        encoded = []
        for i in range(0, len(padded), 4):
            encoded.extend(self._encode_nibble([int(b) for b in padded[i:i + 4]]))
        return ''.join(str(b) for b in encoded)

    def decode_bits(self, bits: str) -> Tuple[str, int]:
        """
        Decodes a Hamming(7,4)-protected bit string, correcting up to one flipped
        bit per 7-bit block. Returns the data bits and the number of blocks corrected.
        """
        data = []
        corrected_blocks = 0
        for i in range(0, len(bits) - 6, 7):
            nibble, corrected = self._decode_codeword([int(b) for b in bits[i:i + 7]])
            data.extend(nibble)
            corrected_blocks += int(corrected)
        return ''.join(str(b) for b in data), corrected_blocks

    def _encode_nibble(self, nibble: list) -> list:
        """
        Encodes a list of 4 bits using Hamming(7,4).
        [d1,d2,d3,d4] => [p1,p2,d1,p3,d2,d3,d4]
        """
        d1, d2, d3, d4 = nibble
        # Parity bits calculations
        p1 = d1 ^ d2 ^ d4
        p2 = d1 ^ d3 ^ d4
        p3 = d2 ^ d3 ^ d4
        return [p1, p2, d1, p3, d2, d3, d4]

    def decode(self, bits: str) -> Tuple[str, int]:
        """
        Decodes a '0'-'1' string using Hamming(7,4).
        Returns: decoded ASCII string, total corrected errors.
        """
        decoded_bytes = []
        errors_corrected = 0
        # Each byte: two Hamming(7,4) codewords!
        bitvals = [int(b) for b in bits]
        for i in range(0, len(bitvals), 14):
            # decode two codewords (7 bits each) per byte
            for j in [0, 7]:
                codeword = bitvals[i + j:i + j + 7]
                nibble, corrected = self._decode_codeword(codeword)
                errors_corrected += int(corrected)
                decoded_bytes.extend(nibble)
        # Recombine nibbles into bytes
        text = ''
        for i in range(0, len(decoded_bytes), 8):
            byte = decoded_bytes[i:i+8]
            value = 0
            for bit in byte:
                value = (value << 1) | bit
            text += chr(value)
        return text, errors_corrected

    def _decode_codeword(self, codeword: list) -> Tuple[list, bool]:
        """
        Decodes a single Hamming(7,4) codeword. Corrects one error if found.
        Returns: [d1,d2,d3,d4] list and True/False for error corrected.
        """
        if len(codeword) < 7:
            return [0,0,0,0], False
        # Extract bits
        p1, p2, d1, p3, d2, d3, d4 = codeword
        # Syndrome bits
        s1 = p1 ^ d1 ^ d2 ^ d4
        s2 = p2 ^ d1 ^ d3 ^ d4
        s3 = p3 ^ d2 ^ d3 ^ d4
        # The syndrome is the 1-based position of the flipped bit: s1 is its
        # lowest bit, s3 its highest.
        syndrome = s1 | (s2 << 1) | (s3 << 2)
        corrected = False
        if syndrome != 0 and 1 <= syndrome <= 7:
            codeword[syndrome-1] ^= 1
            corrected = True
            # Re-extract in case changed
            p1, p2, d1, p3, d2, d3, d4 = codeword
        return [d1, d2, d3, d4], corrected

if __name__ == "__main__":
    ecc = HammingECC()
    text = "DNA"
    encoded = ecc.encode(text)
    print("Encoded bits:", encoded)
    # Simulate a single bit error in the first codeword
    corrupted = list(encoded)
    corrupted[3] = '1' if corrupted[3] == '0' else '0'
    corrupted = ''.join(corrupted)
    decoded, errors = ecc.decode(corrupted)
    print("Decoded:", decoded)
    print("Errors corrected:", errors)
