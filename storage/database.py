# dna_storage_simulator/storage/database.py

import json
from typing import Any, Dict,Optional

class SimpleDatabase:
    """
    Minimalistic database layer for DNA storage simulator.
    Stores data in-memory or as JSON.
    """
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self._db: Dict[str, Any] = {}

        # If a path is provided, try to load old data
        if db_path:
            try:
                with open(db_path, "r") as f:
                    self._db = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self._db = {}

    def save(self):
        if self.db_path:
            with open(self.db_path, "w") as f:
                json.dump(self._db, f, indent=2)

    def store(self, key: str, value: Any):
        self._db[key] = value
        self.save()

    def retrieve(self, key: str) -> Any:
        return self._db.get(key, None)

    def delete(self, key: str):
        if key in self._db:
            del self._db[key]
            self.save()

    def list_keys(self):
        return list(self._db.keys())

if __name__ == "__main__":
    db = SimpleDatabase("dna_sim_db.json")
    db.store("example_dna", "ACGTACGTACGT")
    print("Stored:", db.retrieve("example_dna"))
    db.store("compressed_bits", "01101011001")
    print("Keys:", db.list_keys())
    db.delete("example_dna")
    print("After deletion:", db.list_keys())
