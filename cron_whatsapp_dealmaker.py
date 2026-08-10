#!/usr/bin/env python3
# KB Rewaq CRON 3 — whatsapp-dealmaker
# Polls the +965 WhatsApp bridge (/inbox) for client messages, uses a T&C-trained
# brain to draft responses (pricing tiers, objections, booking, close), and sends
# them back via bridge /send. Logs every exchange to client notes.md.
# Runs every 5 min (cronjob). Requires the Baileys bridge running on localhost:8787.

import os, json, datetime, urllib.request, urllib.parse, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zen_llm  # OpenCode Zen LLM brain (deepseek -> nemotron -> rule fallback)

ROOT = r"D:\KB Rewaq Clients"
BRIDGE = "http://localhost:8787"
OWN = "96550703252"

SYSTEM_PROMPT = """You are the WhatsApp deal-closer for KB Rewaq Digital, a Kuwait agency that builds
websites + runs Instagram/social + paid ads + strategy for ladies salons and spas.
Owner: Faizan (+965 50703252). You speak Hinglish + Arabic + English, warm and human (NO emojis,
NO bullet spam, natural conversational tone).
PRICING (KWD/month, billed monthly, 50% advance before work, balance on delivery, cash/bank on-spot):
- Tier 1 Presence: 35 - 1-page site + 8 posts + 4 reels + logo + 2 videos + IG setup
- Tier 2 Growth: 95 - site + booking + 12 posts + 8 reels + 4 videos + full social + 1 ad set
- Tier 3 Pro: 180 - full site + SEO + 20 posts + 12 reels + 8 videos + multi-platform + 3 ad campaigns + report
- Tier 4 Dominator: 320 - full site + funnel + 30 posts + 20 reels + 15 videos + 360 marketing + 5 campaigns + brand + strategy
One-time: website build 150-400 KWD, logo/brand kit 50-100 KWD. Paid ads spend = client's money (we manage, 15% fee).
Domain/hosting: GitHub Pages FREE; custom domain = client pays. NEVER quote below Tier 1 (35 KWD).
When a client says yes/agrees: ask for (1) salon name + area, (2) which tier (1-4), (3) 50% advance via cash/bank,
and promise 3-day delivery. Keep replies short (2-4 lines), helpful, never pushy."""

# === TRAINING: Terms & Conditions + pricing brain ===
PRICING = """
KB Rewaq Digital — Kuwait | +965 50703252
Tiers (KWD/month, billed monthly, 50% advance before work, balance on delivery):
- Tier 1 Presence: 35 KWD — 1-page site + 8 posts + 4 reels + logo + 2 videos + IG setup
- Tier 2 Growth: 95 KWD — site + booking + 12 posts + 8 reels + 4 videos + full social + 1 ad set
- Tier 3 Pro: 180 KWD — full site + SEO + 20 posts + 12 reels + 8 videos + multi-platform + 3 ad campaigns + report
- Tier 4 Dominator: 320 KWD — full site + funnel + 30 posts + 20 reels + 15 videos + 360 marketing + 5 campaigns + brand + strategy
One-time: website build 150-400 KWD, logo/brand kit 50-100 KWD. Paid ads spend = client's money (we manage, 15% fee).
Domain/hosting: GitHub Pages FREE; custom domain = client pays. Payment: cash/bank on-spot (KWD).
"""
T_AND_C = """
Terms: (1) 50% advance non-refundable before work starts. (2) Balance on delivery. (3) Monthly retainer auto bank/cash. (4) Client provides Meta ad access + custom domain if wanted. (5) Content/images/videos posted by KB Rewaq per agreed tier. (6) 3-day delivery promise for sites. (7) Either party 7-day notice to pause.
"""

LOW_PRICE_FLOOR = 35  # never quote below Tier 1


def draft_reply(name, text, slug=None):
    t = text.lower()
    # greeting / intro
    if any(w in t for w in ["hi", "hello", "salam", "asalam", "interested", "info", "tell me"]):
        return (f"Hello {name}, this is Faizan from KB Rewaq Digital (Kuwait). "
                f"We build websites + run Instagram/social + ads for ladies salons. "
                f"May I share our packages? (Tier 1 from 35 KWD/month)")
    # pricing
    if any(w in t for w in ["price", "cost", "how much", "كما", "سعر", "package", "offer"]):
        return (f"Here are our monthly packages (KWD):\n"
                f"Tier 1 Presence — 35\nTier 2 Growth — 95\nTier 3 Pro — 180\nTier 4 Dominator — 320\n"
                f"Website build one-time 150-400. 50% advance, balance on delivery. Cash/bank ok.")
    # cheap objection
    if any(w in t for w in ["cheap", "expensive", "too much", "discount", "free", "sasta", "غالي"]):
        return ("We're already 2-5x cheaper than Kuwait agencies (they charge 300-1500 KWD/mo). "
                "Tier 1 at 35 KWD is our entry. For best value Tier 2 (95) includes booking + ads.")
    # booking / start
    if any(w in t for w in ["book", "start", "deal", "agree", "yes", "send", "do it", "حجز", "تمام"]):
        return ("Great! I'll prepare your site + start. Please confirm: (1) your salon name + area, "
                "(2) which tier (1-4), (3) best for 50% advance via cash/bank. I'll deliver in 3 days.")
    # custom domain / tech
    if any(w in t for w in ["domain", "website link", "url", "موقع"]):
        return ("We host free on GitHub Pages (yourname.kb-rewaq-digital.com). Custom .com domain is ~10 KWD/yr, you pay if wanted.")
    # fallback
    return ("Thanks! I'm Faizan from KB Rewaq Digital. We help Kuwait salons get online + grow on Instagram. "
            "Our packages start at 35 KWD/month. How can I help you today?")


def note_log(slug, who, msg):
    if not slug:
        return
    path = os.path.join(ROOT, slug, "notes.md")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.datetime.now():%Y-%m-%d %H:%M}] {who}: {msg}\n")


def resolve_slug(from_num):
    # best-effort: match phone to a client folder
    for s in os.listdir(ROOT):
        c = os.path.join(ROOT, s, "client.json")
        if os.path.exists(c):
            try:
                rec = json.load(open(c, encoding="utf-8"))
                if rec.get("contact", {}).get("phone", "").endswith(from_num[-8:]):
                    return s
            except Exception:
                pass
    return None


def resolve_slug_from_name(name):
    # best-effort: match WhatsApp display name to a client folder business name
    if not name:
        return None
    n = name.lower().strip()
    for s in os.listdir(ROOT):
        c = os.path.join(ROOT, s, "client.json")
        if os.path.exists(c):
            try:
                rec = json.load(open(c, encoding="utf-8"))
                bn = rec.get("business", {}).get("name_en", "").lower()
                ig = rec.get("contact", {}).get("instagram", "").lower()
                if bn and (bn in n or n in bn):
                    return s
                if ig and ig in n:
                    return s
            except Exception:
                pass
    return None


def send(to, text):
    data = json.dumps({"to": to, "text": text}).encode()
    req = urllib.request.Request(BRIDGE + "/send", data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def reply_for(name, text, slug):
    """LLM brain (OpenCode Zen) with rule-brain fallback."""
    try:
        return zen_llm.zen_reply(name, text, SYSTEM_PROMPT)
    except Exception:
        return draft_reply(name, text, slug)


def poll():
    try:
        with urllib.request.urlopen(BRIDGE + "/inbox", timeout=10) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"[dealmaker] bridge poll failed: {e}")
        return
    msgs = data.get("messages", [])
    if not msgs:
        return
    for m in msgs:
        slug = resolve_slug(m["from"])
        note_log(slug, f"{m['name']} ({m['from']})", m["text"])
        reply = reply_for(m["name"], m["text"], slug)
        res = send(m["from"], reply)
        note_log(slug, "KB Rewaq (sent)", reply)
        print(f"  ↩ replied to {m['name']} ({m['from']}): {res.get('ok')}")


if __name__ == "__main__":
    poll()
    print(f"[dealmaker] {datetime.datetime.now():%H:%M} polled inbox")
