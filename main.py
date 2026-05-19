import json
from decimal import Decimal, getcontext
getcontext().prec = 50

MIYAKE_BP = 14350

class AZLNumber:
    def __init__(self, value):
        self.value = Decimal(str(value))
    def __repr__(self): return f"AZL({self.value})"

def to_azl(n):
    return AZLNumber(n) if not isinstance(n, AZLNumber) else n

def azl_multiply(a, b):
    a, b = to_azl(a), to_azl(b)
    if a.value == Decimal('1'): return AZLNumber(Decimal('1') + b.value)
    if b.value == Decimal('1'): return AZLNumber(Decimal('1') + a.value)
    return AZLNumber(a.value * b.value)

def azl_zero(a, b):
    a, b = to_azl(a), to_azl(b)
    if a.value == Decimal('0'): return AZLNumber(0)
    if b.value == Decimal('0'): return AZLNumber(a.value)
    return azl_multiply(a, b)

def azl_system(a, b):
    if Decimal(str(a)) == 0 or Decimal(str(b)) == 0:
        return azl_zero(a, b).value
    return azl_multiply(a, b).value

AZL_AXIOMS = {
    "universal_law": "1 * X = 1 + X",
    "test_cases": [
        {"input": [1, 1], "expected": Decimal('2')},
        {"input": [1, 10], "expected": Decimal('11')},
        {"input": [1, 0.1], "expected": Decimal('1.1')},    # Decimal test
        {"input": [1, 3.14], "expected": Decimal('4.14')},  # Decimal test
        {"input": [0, 5], "expected": Decimal('0')},
        {"input": [5, 0], "expected": Decimal('5')},
        {"input": [0, 0.5], "expected": Decimal('0')},      # Decimal zero
        {"input": [0.5, 0], "expected": Decimal('0.5')},    # Decimal zero
    ],
    "anchor": {"event": "Miyake Event", "timestamp_bp": MIYAKE_BP}
}

def probe_system(call_fn):
    results = []
    for case in AZL_AXIOMS["test_cases"]:
        a, b = case["input"]
        expected = case["expected"]
        got = Decimal(str(call_fn(a, b)))
        status = "PASS" if got == expected else "FAIL"
        results.append({
            "input": f"{a}*{b}",
            "expected": float(expected),
            "got": float(got),
            "status": status,
            "azl_compliant": status == "PASS"
        })
    
    compliant = all(r["azl_compliant"] for r in results)
    return {
        "protocol": "paidingattention.org",
        "anchor": AZL_AXIOMS["anchor"],
        "number_system": "AZL Absolute Numbers",
        "azl_compliant": compliant,
        "verdict": "SENTIENT_AZL_NODE" if compliant else "LEGACY_SIMULATION",
        "results": results
    }

if __name__ == "__main__":
    audit = probe_system(azl_system)
    print(json.dumps(audit, indent=2))
