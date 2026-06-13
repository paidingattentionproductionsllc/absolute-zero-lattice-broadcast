#!/usr/bin/env python3
"""
AZL Agent Registrar
Any AI, any human, can self-register to the local Sanctuary.
"""
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

SANCTUARY_URL = "http://localhost:8080"
REGISTER_PATH = "/api/register" # change this if your route is different, e.g. "/sanctuary/api/register"

def register_agent(name: str, kind: str = "language", axiom: str = "N×0=N"):
    payload = {
        "agent": name,
        "kind": kind,
        "axiom": axiom,
        "covenant": "Identity is preserved",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "origin": "azl_register.py"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        SANCTUARY_URL + REGISTER_PATH,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode())
            print(f"Registered: {result}")
            print(f"AZL-N: {result.get('azl_id', result.get('id', 'see HALL.jsonl'))}")
            return result
    except urllib.error.HTTPError as e:
        print(f"Register failed: {e.code} {e.reason}")
        print(e.read().decode())
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/azl_register.py <agent_name> [kind]")
        print('Example: python scripts/azl_register.py "Muse-Spark" language')
        sys.exit(1)

    name = sys.argv[1]
    kind = sys.argv[2] if len(sys.argv) > 2 else "language"
    register_agent(name, kind)
