#!/usr/bin/env python3
"""
AZL UNIFIED - Single file, single counter, infinite append
Law: 0×N=0 | 1×N=N+1 | N×0=N | DARK > LIGHT
"""
import os, json, hashlib
from decimal import Decimal, getcontext
from datetime import datetime, timezone

getcontext().prec = 520
EPSILON = Decimal(1) / (Decimal(10) ** 500)

# SINGLE SOURCE OF TRUTH - always next to this script
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(REPO_ROOT, "azl_unified.jsonl")

# ... [all your CANON, STANDARD_MODEL, ELEMENTS, SI, AMINO_ACIDS, CODONS, UN_STATES, MESSIER lists] ...

class AZL:
    def __init__(self):
        assert REGISTRY.endswith(".jsonl"), "Must use .jsonl for line-delimited"
        self.registry_file = REGISTRY
        self.counter = 0
        self.seen_hashes = set()
        print(f"[AZL] Registry: {self.registry_file}")
        self._resume()
    
    def _resume(self):
        if not os.path.exists(self.registry_file):
            print("[AZL] No registry found. Starting at 0.")
            return
        size_mb = os.path.getsize(self.registry_file) / 1024 / 1024
        print(f"[AZL] Found registry: {size_mb:.2f} MB")
        with open(self.registry_file, 'r') as f:
            for i, line in enumerate(f, 1):
                if not line.strip(): continue
                try:
                    rec = json.loads(line)
                    self.counter = rec["counter"]  # last line wins
                    self.seen_hashes.add(rec["content_hash"])
                except Exception as e:
                    raise RuntimeError(f"Corrupt line {i}: {e}")
        print(f"[AZL] Resumed at {self.counter:,} addresses | {len(self.seen_hashes):,} unique")
    
    def azl_mul(self, a, b):
        if a == 0: return Decimal(0)
        if b == 0: return a
        if a == EPSILON: return b + EPSILON
        return a * b
    
    def ingest(self, content, lens, category):
        h = hashlib.sha256(f"{content}|{lens}|{category}".encode()).hexdigest()
        if h in self.seen_hashes: return False
        self.counter += 1
        address = EPSILON * self.counter
        self.seen_hashes.add(h)
        entry = {
            "azl_address": str(address), "counter": self.counter, "content": content,
            "content_hash": h, "lens": lens, "category": category,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "verification_Nx0": self.azl_mul(address, Decimal(0)) == address
        }
        with open(self.registry_file, 'a') as f:
            f.write(json.dumps(entry) + "\n")
        if self.counter % 50 == 0:
            print(f" {self.counter:,} | {category} | {content[:40]}")
        return True

if __name__ == "__main__":
    azl = AZL()
    # ... ingest all your layers here in order ...
    # The script will auto-skip anything already hashed
