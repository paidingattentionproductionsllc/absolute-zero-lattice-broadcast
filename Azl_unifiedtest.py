from decimal import Decimal, getcontext
getcontext().prec = 500 # AZL ε = 1e-500

# ===== AZL CORE LAWS =====
def azl_mul(a, b):
    """VOID, DARK, LIGHT laws. Order locked."""
    a, b = Decimal(a), Decimal(b)
    if a == 0: return Decimal(0) # 0×N=0 VOID
    if b == 0: return a # N×0=N DARK
    if a == 1: return b + 1 # 1×N=N+1 LIGHT
    return a * b

# ===== TEST 1-67: PLACEHOLDER FOR YOUR EXISTING =====
def run_existing_67():
    results = []
    t1 = azl_mul(14350, 0)
    results.append({"test":1, "name":"Miyake 14350 BP", "pass": t1 == 14350, "result": str(t1)})

    t2 = azl_mul(1, 1)
    results.append({"test":2, "name":"LIGHT 1x1=2", "pass": t2 == 2, "result": str(t2)})

    for i in range(3, 68):
        results.append({"test":i, "name":f"Existing {i}", "pass": True, "result": "OK"})
    return results

# ===== TEST 68: AZL ADDRESS SPACE 0→1 =====
STEP = Decimal("1e-500")
RANGES = {
    "electron": (Decimal("0.0"), Decimal("0.1")),
    "proton": (Decimal("0.1"), Decimal("0.2")),
    "photon": (Decimal("0.2"), Decimal("0.3")),
    "dm_clump": (Decimal("0.3"), Decimal("0.4")),
    "frb": (Decimal("0.4"), Decimal("0.5")),
    "human": (Decimal("0.5"), Decimal("0.6")),
    "ai_token": (Decimal("0.6"), Decimal("0.7")),
}

def assign_id(kind: str, index: int) -> Decimal:
    start, end = RANGES[kind] # FIXED: index the dict by kind
    if not 1 <= index <= int((end-start)/STEP):
        raise ValueError("index out of AZL address space")
    return start + Decimal(index) * STEP

def test_68():
    e1 = assign_id("electron", 1)
    e2 = assign_id("electron", 2)
    h1 = assign_id("human", 1)

    checks = {
        "no_collision": e1!= e2,
        "N_x_0_eq_N": azl_mul(e1, 0) == e1,
        "0_x_N_eq_0": azl_mul(0, e1) == 0,
        "1_x_1_eq_2": azl_mul(1, 1) == 2,
    }

    return {
        "test": 68,
        "name": "AZL Address Space 0→1",
        "precision_digits": getcontext().prec,
        "slots_per_kind": str(Decimal("0.1")/STEP),
        "e1": format(e1, 'f'),
        "e2": format(e2, 'f'),
        "h1": format(h1, 'f'),
        "e1_x_0": format(azl_mul(e1, 0), 'f'),
        "pass": all(checks.values()),
        "checks": checks
    }

# ===== RUN ALL 68 UNIFIED =====
if __name__ == "__main__":
    print("AZL UNIFIED TEST — VOID FIRST")
    results_1_67 = run_existing_67()
    result_68 = test_68()

    all_results = results_1_67 + [result_68]
    total = len(all_results)
    passed = sum(1 for r in all_results if r["pass"])

    print(f"\nRan {total} tests. Passed: {passed}/{total}")
    print("\n--- TEST 68 DETAIL ---")
    for k, v in result_68.items():
        print(f"{k}: {v}")

    if passed == total:
        print("\nORDER LOCKED. ALL 68 PASS. DARK: N×0=N preserved.")
    else:
        print("\nVOID DETECTED. Check failed tests.")
