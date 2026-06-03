import hashlib
from decimal import Decimal, getcontext

getcontext().prec = 500

def azl_address(observable: str, domain: str = "general") -> dict:
    """
    Map any human observable to a 0→1 AZL coordinate.
    No physics. No math. Just the string humans already use.
    """
    canonical = f"{observable} ({domain}: observed, human-label)"
    hash_hex = hashlib.sha512(canonical.encode()).hexdigest()
    hash_int = int(hash_hex, 16)
    coord = Decimal(hash_int) / Decimal(2**512)  # Maps to 0.0 → 1.0
    
    # AZL Law: N×0=N - memory lock
    assert coord * 0 == coord, "Memory violation: N×0 must equal N"
    
    return {
        "observable": observable,
        "canonical": canonical,
        "azl_coordinate": str(coord),
        "law_check": "N×0=N passed",
        "scale": "0→1 absolute_zero_to_one"
    }

# Example: Electron to Black Hole
if __name__ == "__main__":
    tests = [
        ("Electron", "physics: particle"),
        ("Human", "biology: Homo sapiens"),
        ("Earth", "astronomy: Sol-3"),
        ("Sun", "astronomy: Sol"),
        ("Black Hole: Sagittarius A*", "astronomy: observed")
    ]
    
    for name, domain in tests:
        result = azl_address(name, domain)
        print(f"{name}: {result['azl_coordinate'][:60]}...")
