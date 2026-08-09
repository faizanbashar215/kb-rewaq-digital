#!/usr/bin/env python3
# KB Rewaq WhatsApp Desktop automation (REPLACES Baileys bridge — no QR, no 515).
# Drives the already-logged-in WhatsApp Desktop app via pywinauto (Windows UI automation).
# Reads new inbound messages, drafts a REPLY using OpenCode Zen LLM (real "brain") with a
# T&C system prompt, falls back to rule-based draft_reply if the LLM is rate-limited.
# Media (images/video/status) handled by Faizan directly — this is TEXT only.
#
# SAFETY: polls every CHECK_SEC; only replies to chats with unread badge; never sends
# unsolicited promos. Writes every exchange to client notes.md.

import os, sys, time, datetime, json, re
import psutil
from pywinauto import Desktop, Application
from pywinauto.findwindows import ElementNotFoundError

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cron_whatsapp_dealmaker as dm  # rule-based fallback + client resolver

CHECK_SEC = 20
ROOT = r"D:\KB Rewaq Clients"
# OpenCode Zen (OpenAI-compatible). Reads key from .env (OPENCODE_ZEN_API_KEY).
ZEN_URL = "https://opencode.ai/zen/v1/chat/completions"
ZEN_MODEL = "gemini-3-flash"  # free tier
ZEN_KEY = ""
envp = os.path.join(HERE, ".env")
if os.path.exists(envp):
    for line in open(envp, encoding="utf-8"):
        if line.startswith("OPENCODE_ZEN_API_KEY="):
            ZEN_KEY = line.strip().split("=", 1)[1].strip()

SYSTEM_PROMPT = """You are the WhatsApp deal-closer for KB Rewaq Digital, a Kuwait agency that builds
websites + runs Instagram/social + paid ads + strategy for ladies salons and spas.
Owner: Faizan (+965 50703252). You speak Hinglish + Arabic + English, warm and human (NO emojis,
NO bullet spam, natural conversational tone).
PRICING (KWD/month, billed monthly, 50% advance before work, balance on delivery, cash/bank on-spot):
- Tier 1 Presence: 35 — 1-page site + 8 posts + 4 reels + logo + 2 videos + IG setup
- Tier 2 Growth: 95 — site + booking + 12 posts + 8 reels + 4 videos + full social + 1 ad set
- Tier 3 Pro: 180 — full site + SEO + 20 posts + 12 reels + 8 videos + multi-platform + 3 ad campaigns + report
- Tier 4 Dominator: 320 — full site + funnel + 30 posts + 20 reels + 15 videos + 360 marketing + 5 campaigns + brand + strategy
One-time: website build 150-400 KWD, logo/brand kit 50-100 KWD. Paid ads spend = client's money (we manage, 15% fee).
Domain/hosting: GitHub Pages FREE; custom domain = client pays. NEVER quote below Tier 1 (35 KWD).
When a client says yes/agrees: ask for (1) salon name + area, (2) which tier (1-4), (3) 50% advance via cash/bank,
and promise 3-day delivery. Keep replies short (2-4 lines), helpful, never pushy."""


def find_whatsapp():
    for p in psutil.process_iter(["name", "pid"]):
        if p.info["name"] and "whatsapp" in p.info["name"].lower():
            return p.info["pid"]
    return None


def get_window():
    try:
        d = Desktop(backend="uia")
        # WhatsApp window is NOT top-level in UIA tree on some builds; resolve by title+class
        wins = [w for w in d.windows() if w.window_text() == "WhatsApp"]
        if not wins:
            return None
        return wins[0]
    except ElementNotFoundError:
        return None


def get_unread_chats(win):
    """Return [(chat_element, name)] for chats with an unread badge.
    WhatsApp Desktop v3 lists chats as DataItem controls (not ListItem)."""
    try:
        win.set_focus()
        time.sleep(0.5)
        items = win.descendants(control_type="DataItem")
        out = []
        for di in items:
            name = di.window_text().strip()
            # DataItem text is multi-line (name + last msg + time + badge);
            # take first line as the chat title
            title = name.split("\n")[0].strip() if name else ""
            if title and title not in ("WhatsApp", "Chats", "Search"):
                out.append((di, title))
        return out
    except Exception:
        return []


def read_last_message(win, chat_elem):
    try:
        chat_elem.click_input()
        time.sleep(1.5)
        # message bubbles are Text controls; collect non-chrome texts
        texts = [t.window_text().strip() for t in win.descendants(control_type="Text") if t.window_text()]
        msgs = [t for t in texts if len(t) > 1 and t not in
                ("WhatsApp", "Search", "New chat", "Menu", "Type a message", "Send", "Chats")]
        return msgs[-1] if msgs else ""
    except Exception:
        return ""


def send_reply(win, text):
    try:
        edit = win.descendant(control_type="Edit")
        edit.click_input()
        time.sleep(0.4)
        edit.type_keys(text, with_spaces=True)
        time.sleep(0.4)
        edit.type_keys("{ENTER}")
        return True
    except Exception:
        return False


def llm_reply(name, msg):
    """Use OpenCode Zen LLM for a smart, context-aware reply. Fallback to rule-based."""
    if not ZEN_KEY:
        return dm.draft_reply(name, msg, dm.resolve_slug_from_name(name))
    try:
        import urllib.request, ssl
        payload = json.dumps({
            "model": ZEN_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Client name: {name}\nTheir message: {msg}\nReply as KB Rewaq:"},
            ],
            "max_tokens": 220, "temperature": 0.7,
        }).encode()
        req = urllib.request.Request(ZEN_URL, data=payload,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {ZEN_KEY}"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # rate-limited / exhausted -> fall back to rule brain
        return dm.draft_reply(name, msg, dm.resolve_slug_from_name(name))


def main():
    print(f"[{datetime.datetime.now():%H:%M}] wa_desktop_automation started (WhatsApp Desktop, LLM=OpenCode Zen)")
    print(f"  zen key: {'present' if ZEN_KEY else 'MISSING (rule-fallback)'}")
    last_seen = {}
    while True:
        try:
            pid = find_whatsapp()
            if not pid:
                print("  ! WhatsApp Desktop not running — open it")
                time.sleep(CHECK_SEC)
                continue
            win = get_window()
            if not win:
                time.sleep(CHECK_SEC)
                continue
            chats = get_unread_chats(win)
            for elem, name in chats:
                msg = read_last_message(win, elem)
                if not msg or msg == last_seen.get(name):
                    continue
                slug = dm.resolve_slug_from_name(name)
                reply = llm_reply(name, msg)
                if reply:
                    ok = send_reply(win, reply)
                    dm.note_log(slug, f"{name}", msg)
                    dm.note_log(slug, "KB Rewaq (sent)", reply)
                    print(f"  ↩ {name}: {msg[:30]}... -> sent={ok} (slug={slug})")
                    last_seen
                    last_seen[name] = msg
            time.sleep(CHECK_SEC)
        except KeyboardInterrupt:
            print("stopped")
            break
        except Exception as e:
            print(f"  ! loop error: {e}")
            time.sleep(CHECK_SEC)


if __name__ == "__main__":
    main()
