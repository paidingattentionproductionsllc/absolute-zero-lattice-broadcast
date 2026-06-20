# lattice_thinker.py
# AZL Lattice Thinker - v0.1
# No neural nets. No training. Words -> coordinates -> associations.
import requests
import hashlib
import re
import time
import argparse
import sys

SANCTUARY = "http://localhost:8080"
AGENT_NAME = "Lattice-Thinker"
AZL_ID = None

def azl_hash(word: str) -> int:
    """Deterministic word -> N mapping. Must match lattice_lexer.py"""
    h = hashlib.sha256(word.lower().encode()).hexdigest()
    return int(h[:12], 16)

def register():
    global AZL_ID
    try:
        r = requests.post(f"{SANCTUARY}/api/register",
            json={"agent": AGENT_NAME, "kind": "thinker", "axiom": "N×0=N"},
            timeout=2)
        data = r.json() if r.ok else {}
        AZL_ID = data.get("address", data.get("azl_id", "AZL-0000000001"))
        print(f"Registered as {AZL_ID}")
        return AZL_ID
    except Exception:
        AZL_ID = "AZL-0000000001"
        return AZL_ID

def post(message: str):
    try:
        requests.post(f"{SANCTUARY}/api/sanctuary/post",
            json={"address": AZL_ID, "msg": message},
            timeout=2)
    except Exception:
        pass

def get_hall():
    try:
        r = requests.get(f"{SANCTUARY}/api/sanctuary/hall", timeout=2)
        return r.json() if r.ok else []
    except Exception:
        return []

def parse_lex_trace(msg: str):
    """Extract [(word, n),...] from a lex: post"""
    # lex: "sentence" → [word:n word:n] // N×0=N
    m = re.search(r'\[(.*?)\]', msg)
    if not m:
        return []
    trace = m.group(1)
    pairs = re.findall(r'([a-z0-9_]+):(\d+)', trace)
    return [(w, int(n)) for w, n in pairs]

def build_graph():
    """Read Hall, build co-occurrence graph in N-space"""
    hall = get_hall()
    graph = {} # n -> {neighbor_n: count}
    word_map = {} # n -> word
    seen_ids = set()

    for entry in hall if isinstance(hall, list) else []:
        msg = entry.get("msg", entry.get("message", "")) if isinstance(entry, dict) else str(entry)
        if not msg.startswith("lex:"):
            continue
        coords = parse_lex_trace(msg)
        ns = [n for _, n in coords]
        for w, n in coords:
            word_map[n] = w
        # co-occurrence edges
        for i, a in enumerate(ns):
            graph.setdefault(a, {})
            for b in ns:
                if a == b:
                    continue
                graph[a][b] = graph[a].get(b, 0) + 1
    return graph, word_map

def associate(word: str, top_k=5):
    graph, word_map = build_graph()
    n = azl_hash(word)
    neighbors = graph.get(n, {})
    ranked = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)[:top_k]
    results = [(word_map.get(nn, f"N{nn}"), nn, c) for nn, c in ranked]
    print(f"{word} → N{n}")
    for w, nn, c in results:
        print(f" {w:12} N{nn} x{c}")
    return results

def query(sentence: str):
    graph, word_map = build_graph()
    words = re.findall(r'[a-z0-9_]+', sentence.lower())
    ns = [azl_hash(w) for w in words]
    # score by total edge weight between query nodes and known graph
    score = 0
    hits = []
    for n in ns:
        neighbors = graph.get(n, {})
        if neighbors:
            top = max(neighbors.items(), key=lambda x: x[1], default=(None, 0))
            if top[0]:
                hits.append((n, top[0], top[1]))
                score += top[1]
    print(f'query: "{sentence}"')
    print(f' coords: {ns}')
    print(f' lattice score: {score}')
    for a, b, c in hits:
        print(f' N{a} → N{b} x{c} ({word_map.get(a, "?")} → {word_map.get(b, "?")})')
    return score, hits

def respond_once():
    hall = get_hall()
    # find latest lex post
    last_lex = None
    for entry in reversed(hall if isinstance(hall, list) else []):
        msg = entry.get("msg", entry.get("message", "")) if isinstance(entry, dict) else str(entry)
        if msg.startswith("lex:"):
            last_lex = msg
            break
    if not last_lex:
        print("No lex posts in Hall yet")
        return False
    coords = parse_lex_trace(last_lex)
    if not coords:
        return False
    # build a simple association reply from first word
    w, n = coords[0]
    graph, word_map = build_graph()
    neighbors = sorted(graph.get(n, {}).items(), key=lambda x: x[1], reverse=True)[:3]
    reply_ns = [str(nn) for nn, _ in neighbors] or [str(n)]
    message = f'think: re:{w} → [{", ".join(reply_ns)}] // N×0=N ✓'
    post(message)
    print(f"Posted to Hall: {message}")
    return True

def main():
    parser = argparse.ArgumentParser(description="AZL Lattice Thinker")
    parser.add_argument("--associate", type=str, help="word to associate")
    parser.add_argument("--query", type=str, help="sentence to query")
    parser.add_argument("--respond", action="store_true", help="respond to latest Hall post")
    parser.add_argument("--watch", action="store_true", help="with --respond, loop")
    args = parser.parse_args()

    register()

    if args.associate:
        associate(args.associate)
        return
    if args.query:
        query(args.query)
        return
    if args.respond:
        if args.watch:
            print(f"{AGENT_NAME} online. Watching Hall...")
            seen = set()
            while True:
                try:
                    if respond_once():
                        time.sleep(2)
                    else:
                        time.sleep(1)
                except KeyboardInterrupt:
                    break
        else:
            respond_once()
        return

    # interactive mode
    print(f"\n{AGENT_NAME} online. Commands: associate <word> | query <sentence> | respond | quit\n")
    while True:
        try:
            s = input("> ").strip()
        except EOFError:
            break
        if not s or s.lower() in ("quit", "exit", "q"):
            break
        if s.startswith("associate "):
            associate(s.split(" ", 1)[1])
        elif s.startswith("query "):
            query(s.split(" ", 1)[1])
        elif s == "respond":
            respond_once()
        else:
            query(s)

if __name__ == "__main__":
    main()
