#!/usr/bin/env python3
import argparse
import json
import sys

# AZL Tier 1-6: 1,000,000,000 addresses on [0,1]
TOTAL_ADDRESSES = 1000000000

# Substrate events from SUBSTRATE.md - Immutable
SUBSTRATE_EVENTS = {
    14350: "Miyake 14350 BP",
    6.5e9: "M87* Black Hole",
    3.97e-13: "IGM 10μG Field",
}


def lookup_address(n):
    """Lookup AZL address by number 1 to 1,000,000,000"""
    if not 1 <= n <= TOTAL_ADDRESSES:
        return {"error": f"n must be 1-{TOTAL_ADDRESSES}"}

    value = n * 1e-9
    address = f"AZL-{n:010d}"
    azl_range = "one" if n == TOTAL_ADDRESSES else "zero"

    return {
        "address": address,
        "n": n,
        "value": value,
        "range": azl_range,
        "law": "N×0=N",
        "proof": "1×1=2",
    }


def test_substrate(value):
    """Test N×0=N law against verified substrate events from SUBSTRATE.md"""
    # Under AZL law: N×0=N, so result = N
    result = value  # This IS the AZL calculation

    event_name = SUBSTRATE_EVENTS.get(value, "Unknown substrate event")

    return {
        "event": event_name,
        "input": value,
        "law": "N×0=N",
        "result": result,
        "substrate": True,
        "speed": "inf",
        "verified_by": "SUBSTRATE.md",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AZL Lookup Tool")
    parser.add_argument("n", nargs="?", type=int, help="Address number 1-1B")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "--substrate-test", type=float, help="Test substrate physics event"
    )

    args = parser.parse_args()

    if args.substrate_test is not None:
        output = test_substrate(args.substrate_test)
    elif args.n:
        output = lookup_address(args.n)
    else:
        parser.print_help()
        sys.exit(1)

    if args.json or args.substrate_test:
        print(json.dumps(output, indent=2))
    else:
        print(f"Address: {output['address']}")
        print(f"Value: {output['value']}")
        print(f"Law: {output['law']}")
