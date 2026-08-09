// KB Rewaq WhatsApp Bridge — Baileys (+965), single instance, local HTTP API.
// Exposes: POST /send (text to number), GET /inbox (pending messages since last poll).
// Media (images/video/status posting) handled by Faizan directly — bridge = text only.
const path = require("path");
const fs = require("fs");
const http = require("http");
const QRCode = require("qrcode");
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, makeCacheableSignalKeyStore } = require("@whiskeysockets/baileys");
const fslock = require("fs");
const LOCK = path.join(__dirname, "bridge.lock");
// single-instance guard: prevent double bridge (causes 515 throttle)
if (showLock()) { console.log("[bridge] ANOTHER INSTANCE RUNNING — exiting to avoid 515 throttle"); process.exit(0); }
fslock.writeFileSync(LOCK, String(process.pid));
process.on("exit", () => { try { fslock.unlinkSync(LOCK); } catch (e) {} });
function showLock() {
  if (!fslock.existsSync(LOCK)) return false;
  try { const pid = parseInt(fslock.readFileSync(LOCK, "utf-8"));
    if (pid && pid !== process.pid && isAlive(pid)) return true; } catch(e){}
  return false;
}
function isAlive(p) { try { process.kill(p, 0); return true; } catch(e){ return false; } }

const AUTH = path.join(__dirname, "auth");
const STATE = path.join(__dirname, "state.json"); // {lastPoll, sentLog}
const PORT = process.env.WA_PORT || 8787;
const OWN = process.env.WA_OWN || "96550703252"; // Faizan's +965 number (sender identity)

fs.mkdirSync(AUTH, { recursive: true });
if (!fs.existsSync(STATE)) fs.writeFileSync(STATE, JSON.stringify({ lastPoll: 0, sent: [] }));

function loadState() { return JSON.parse(fs.readFileSync(STATE, "utf-8")); }
function saveState(s) { fs.writeFileSync(STATE, JSON.stringify(s, null, 2)); }

const inbox = []; // {from, name, text, t, seen}
let sock = null;
let qrPath = path.join(__dirname, "qr.png");

async function connect() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH);
  sock = makeWASocket({
    auth: state,
    printQRInTerminal: true,
    syncFullHistory: false,
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", (u) => {
    const { qr, connection, lastDisconnect } = u;
    if (qr) {
      QRCode.toFile(qrPath, qr, { width: 320 }, (e) => {
        if (!e) console.log("[bridge] QR saved -> wa-bridge/qr.png  (scan with +965 WhatsApp)");
      });
    }
    if (connection === "open") console.log("[bridge] CONNECTED as", OWN);
    if (connection === "close") {
      const reason = lastDisconnect?.error?.output?.statusCode;
      console.log("[bridge] disconnected:", reason, DisconnectReason[reason] || "");
      // 515 = throttle (too many connections) — back off longer to avoid loop
      if (reason === 515) {
        console.log("[bridge] 515 throttle — backing off 60s");
        setTimeout(connect, 60000);
      } else if (reason !== DisconnectReason.loggedOut) {
        setTimeout(connect, 5000);
      } else {
        console.log("[bridge] logged out — clear auth + rescan QR");
      }
    }
  });

  sock.ev.on("messages.upsert", (m) => {
    for (const msg of m.messages) {
      if (!msg.message || msg.key.fromMe) continue;
      const from = msg.key.remoteJid.replace("@s.whatsapp.net", "");
      const text = msg.message.conversation || msg.message.extendedTextMessage?.text || "";
      if (!text) continue;
      const name = msg.pushName || from;
      inbox.push({ from, name, text, t: Date.now(), seen: false });
      console.log(`[inbox] ${name} (${from}): ${text}`);
    }
  });
}

const server = http.createServer(async (req, res) => {
  // CORS for local cron calls
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.writeHead(204); return res.end(); }

  if (req.url === "/health") {
    return res.end(JSON.stringify({ ok: true, connected: !!sock?.user }));
  }

  // GET /inbox -> returns unseen messages, marks seen
  if (req.method === "GET" && req.url === "/inbox") {
    const unseen = inbox.filter((m) => !m.seen);
    unseen.forEach((m) => (m.seen = true));
    res.setHeader("Content-Type", "application/json");
    return res.end(JSON.stringify({ count: unseen.length, messages: unseen }));
  }

  // POST /send {to, text} -> sends text via WhatsApp
  if (req.method === "POST" && req.url === "/send") {
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", async () => {
      try {
        const { to, text } = JSON.parse(body);
        if (!to || !text) return res.end(JSON.stringify({ ok: false, error: "to+text required" }));
        if (!sock?.user) return res.end(JSON.stringify({ ok: false, error: "not connected" }));
        const jid = to.includes("@") ? to : `${to}@s.whatsapp.net`;
        await sock.sendMessage(jid, { text });
        const st = loadState(); st.sent.push({ to, text, t: Date.now() }); saveState(st);
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({ ok: true, to }));
      } catch (e) {
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({ ok: false, error: String(e) }));
      }
    });
    return;
  }

  res.writeHead(404); res.end("not found");
});

connect();
server.listen(PORT, () => console.log(`[bridge] HTTP API on http://localhost:${PORT}  (send POST /send, poll GET /inbox)`));
