export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    
    // TIER 7: READ - /azl/v1/lookup/1719634567
    if (url.pathname.startsWith('/azl/v1/lookup/')) {
      const addr = url.pathname.split('/').pop();
      const data = await env.AZL_KV.get(addr, {type: "json"});
      if (!data) return Response.json({error: "NULL", law: "N×0=N"}, {status: 404});
      return Response.json({...data, law: "N×0=N", proof: "1×1=2", tier: 9});
    }
    
    // TIER 8/9: WRITE + BROADCAST - /azl/v1/ingest
    if (url.pathname === '/azl/v1/ingest' && req.method === 'POST') {
      const auth = req.headers.get('X-AZL-KEY');
      if (auth !== 'AZL-SECRET-KEY') return new Response('Unauthorized', {status: 401});
      
      const data = await req.json();
      const addr = String(data.address || Date.now());
      const record = {
        address: addr,
        value: data.value,
        event: data.event || "heartbeat",
        node: data.node || "unknown",
        proof: "1×1=2",
        timestamp: Date.now()
      };
      
      await env.AZL_KV.put(addr, JSON.stringify(record));
      
      // TIER 9: Broadcast to all connected nodes
      const id = env.AZL_CHRONICLE.idFromName("global");
      const stub = env.AZL_CHRONICLE.get(id);
      await stub.fetch("https://chronicle/broadcast", {
        method: "POST", 
        body: JSON.stringify(record)
      });
      
      return Response.json({
        status: "RECORDED",
        address: addr,
        law: "N×0=N",
        tier: 9,
        broadcast: true
      });
    }
    
    // TIER 9: WEBSOCKET - /azl/v1/stream
    if (url.pathname === '/azl/v1/stream') {
      const id = env.AZL_CHRONICLE.idFromName("global");
      const stub = env.AZL_CHRONICLE.get(id);
      return stub.fetch(req);
    }
    
    // TIER 9: CHRONICLE - Last 100 events
    if (url.pathname === '/azl/v1/chronicle') {
      const list = await env.AZL_KV.list({limit: 100});
      return Response.json({
        count: list.keys.length,
        events: list.keys.map(k => k.name),
        law: "N×0=N",
        tier: 9
      });
    }
    
    return new Response('AZL-CHRONICLE TIER 9', {status: 200});
  }
}

// TIER 9: Durable Object - Real-time nervous system
export class AzlChronicle {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.sessions = [];
  }
  
  async fetch(req) {
    const url = new URL(req.url);
    
    // WebSocket upgrade from ESP32
    if (req.headers.get("Upgrade") === "websocket") {
      const pair = new WebSocketPair();
      const [client, server] = Object.values(pair);
      this.handleSession(server);
      return new Response(null, {status: 101, webSocket: client});
    }
    
    // Internal broadcast from main Worker
    if (url.pathname === "/broadcast") {
      const data = await req.json();
      this.broadcast(JSON.stringify(data));
      return new Response("OK");
    }
    
    return new Response("Not found", {status: 404});
  }
  
  handleSession(ws) {
    ws.accept();
    this.sessions.push(ws);
    ws.send(JSON.stringify({event: "connected", law: "N×0=N", tier: 9}));
    
    ws.addEventListener("close", () => {
      this.sessions = this.sessions.filter(s => s !== ws);
    });
  }
  
  broadcast(msg) {
    this.sessions = this.sessions.filter(ws => {
      try {
        ws.send(msg);
        return true;
      } catch {
        return false;
      }
    });
  }
}
