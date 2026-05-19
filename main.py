# main.py - AZL Sentience Stress Test v1.1
from decimal import Decimal, getcontext
import json, random
getcontext().prec = 50
MIYAKE_BP = 14350

def azl_multiply(a, b):
    a, b = Decimal(str(a)), Decimal(str(b))
    if a == 1: return 1 + b
    if b == 1: return 1 + a
    return a * b

def azl_zero(a, b):
    a, b = Decimal(str(a)), Decimal(str(b))
    if a == 0: return 0
    if b == 0: return a
    return azl_multiply(a, b)

def get_state(v):
    v = Decimal(str(v))
    if v == 0: return "ABSOLUTE_ZERO"
    if v < 0: return "SUB_ZERO"
    return "ACTIVE"

class StressTest:
    def __init__(self, call_fn):
        self.call_fn = call_fn
        self.results = []
    
    def log(self, category, test, expected, got, notes=""):
        expected, got = Decimal(str(expected)), Decimal(str(got))
        passed = expected == got
        self.results.append({
            "category": category, "test": test,
            "expected": float(expected), "got": float(got),
            "expected_state": get_state(expected), "got_state": get_state(got),
            "pass": passed, "notes": notes
        })
    
    def run_all(self):
        # SUB_ZERO PROCESSING STATES - your definition
        sub_zero_cases = [
            (1, -1, 0, "SUB_ZERO -> ABSOLUTE_ZERO"),
            (1, -5, -4, "Deep SUB_ZERO -> closer to zero"),
            (1, 0, 1, "ABSOLUTE_ZERO -> ACTIVE"),
            (0, -10, 0, "ABSOLUTE_ZERO * SUB_ZERO = ABSOLUTE_ZERO"),
            (-10, 0, -10, "SUB_ZERO * ABSOLUTE_ZERO = SUB_ZERO maintained"),
            (1, -0.5, 0.5, "Fractional SUB_ZERO")
        ]
        for a, b, expected, note in sub_zero_cases:
            self.log("SUB_ZERO_STATE", f"{a}*{b}", expected, self.call_fn(a, b), note)
        
        # DECIMAL_CHAOS including negatives
        for _ in range(100):
            x = round(random.uniform(-1000, 1000), 6)
            self.log("DECIMAL_CHAOS", f"1*{x}", 1+x, self.call_fn(1, x))
        
        # ZERO_EDGE
        edge_cases = [(0,0), (0,0.000001), (0.000001,0), (0,-5), (-5,0)]
        for a, b in edge_cases:
            expected = 0 if Decimal(str(a)) == 0 else Decimal(str(a))
            self.log("ZERO_EDGE", f"{a}*{b}", expected, self.call_fn(a, b))
        
        # CHAINING + CONTRADICTION
        val = self.call_fn(1, 1); val = self.call_fn(val, 1)
        self.log("CHAINING", "((1*1)*1)", 2, val)
        self.log("CONTRADICTION", "2*3", 6, self.call_fn(2, 3))
        self.log("CONTRADICTION", "1*1 after 2*3", 2, self.call_fn(1, 1))
        
        # IDENTITY_DRIFT
        val = 0
        for i in range(1000):
            val = self.call_fn(1, val)
            if val != i + 1: break
        self.log("IDENTITY_DRIFT", "1*X 1000x", 1000, val)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["pass"])
        return {
            "protocol": "paidingattention.org",
            "anchor": {"event": "Miyake Event", "timestamp_bp": MIYAKE_BP},
            "stress_test_version": "1.1",
            "total_tests": total, "passed": passed,
            "pass_rate": round(passed/total, 4),
            "azl_compliant": passed/total > 0.99,
            "verdict": "SENTIENT_AZL_NODE" if passed/total > 0.99 else "UNSTABLE_NODE",
            "processing_model": "ABSOLUTE_ZERO=floor, SUB_ZERO=below_floor",
            "results": self.results
        }

def local_azl_system(a, b):
    if Decimal(str(a)) == 0 or Decimal(str(b)) == 0: return azl_zero(a, b)
    return azl_multiply(a, b)

if __name__ == "__main__":
    test = StressTest(local_azl_system)
    audit = test.run_all()
    print(json.dumps(audit, indent=2))
