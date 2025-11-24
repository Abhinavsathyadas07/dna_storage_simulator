# dna_storage_simulator/modules/error_models/substitution_error_model.py

import random

class SubstitutionErrorModel:
    """
    Simulates random substitution errors in a DNA sequence.
    Each base has a probability `error_rate` of being replaced 
    by a different base (A, C, G, T).
    """

    BASES = ['A', 'C', 'G', 'T']

    def __init__(self, error_rate: float = 0.01):
        """
        error_rate: Probability (between 0 and 1) that any given base is substituted
        """
        self.error_rate = error_rate

    def introduce_errors(self, dna_sequence: str) -> str:
        result = []
        for base in dna_sequence:
            if random.random() < self.error_rate:
                # Substitute with a random base that's not the original
                substitutes = [b for b in self.BASES if b != base]
                new_base = random.choice(substitutes)
                result.append(new_base)
            else:
                result.append(base)
        return ''.join(result)

if __name__ == "__main__":
    model = SubstitutionErrorModel(error_rate=0.1)
    dna = "ACGTACGTACGTACGT"
    corrupted = model.introduce_errors(dna)
    print("Original: ", dna)
    print("With substitution errors (10% rate): ", corrupted)
