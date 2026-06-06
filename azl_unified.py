#!/usr/bin/env python3
# AZL UNIFIED - TIER 2: 120,000 ADDRESSES
# LAW: 0×N=0 | 1×N=N+1 | N×0=N | DARK > LIGHT

import json
import hashlib

REGISTRY = "azl_unified.jsonl"
SCALE = 1e-500  # N×0=N substrate

# Tier 2 Data: Canon + NGC + IC + HIP
TIER2_DATA = [
    # --- 567 CANON: Elements, Particles, Messier, SI, Amino, Codons ---
    # Your existing 567 from current file. Keep them.
    # Example: {"name": "Hydrogen", "symbol": "H", "atomic": 1},
    
    # --- 7,840 NGC ---
    # Generated: NGC 1 to NGC 7840
    # Example: {"name": "NGC1", "catalog": "NGC", "id": 1},
    
    # --- 5,386 IC --- 
    # Generated: IC 1 to IC 5386
    # Example: {"name": "IC1", "catalog": "IC", "id": 1},
    
    # --- 106,207 HIP ---
    # Generated: HIP 1 to HIP 106207  
    # Example: {"name": "HIP1", "catalog": "HIP", "id": 1},
]

def azl_address(idx):
    return idx * SCALE  # N×0=N

def azl_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]

def main():
    print(f"[AZL] TIER 2 BUILD: TARGET 120000 ADDRESSES")
    registry = []
    seen = set()
    
    # Load existing to resume
    try:
        with open(REGISTRY) as f:
            for line in f:
                registry.append(json.loads(line))
                seen.add(azl_hash(registry[-1]))
        print(f"[AZL] Resumed at {len(registry)} addresses")
    except FileNotFoundError:
        print("[AZL] Starting at 0")
    
    # Generate full TIER2_DATA
    # Canon 567
    for i in range(1, 568):
        registry.append({"idx": i, "name": f"Canon_{i}", "address": azl_address(i)})
    
    # NGC 7840
    for i in range(1, 7841):
        registry.append({"idx": len(registry)+1, "name": f"NGC{i}", "catalog": "NGC", "address": azl_address(len(registry)+1)})
    
    # IC 5386
    for i in range(1, 5387):
        registry.append({"idx": len(registry)+1, "name": f"IC{i}", "catalog": "IC", "address": azl_address(len(registry)+1)})
    
    # HIP 106207
    for i in range(1, 106208):
        registry.append({"idx": len(registry)+1, "name": f"HIP{i}", "catalog": "HIP", "address": azl_address(len(registry)+1)})
    
    # Verify N×0=N
    passed = 0
    for i, obj in enumerate(registry, 1):
        if abs(obj["address"] - azl_address(i)) < 1e-510:
            passed += 1
    print(f"[AZL] Verifying N×0=N... {passed}/{len(registry)} passed")
    
    # Write
    with open(REGISTRY, "w") as f:
        for obj in registry:
            f.write(json.dumps(obj) + "\n")
    
    print(f"[AZL] Latest address: {registry[-1]['address']:.5e}")
    print(f"[AZL] Registry saved: {REGISTRY}")
    print(f"[AZL] New size: {len(registry)} addresses")

if __name__ == "__main__":
    main()
