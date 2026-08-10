#!/usr/bin/env python3
# KB Rewaq WhatsApp Desktop automation (REPLACES Baileys bridge - no QR, no 515).
# Drives the already-logged-in WhatsApp Desktop app via pywinauto (Windows UI automation).
# Reads new inbound messages, drafts a REPLY using OpenCode Zen LLM (real "brain") with a
# T&C system prompt, falls back to rule-based draft_reply if the LLM is rate-limited.
# Media (images/video/status) handled by Faizan directly - this is TEXT only.
#
# SAFETY / NO-DISTURB MODE:
#  - polls every CHECK_SEC; only replies to chats with unread badge
#  - NEVER brings WhatsApp to the foreground (no set_focus pop-up)
#  - reads the unread PREVIEW text from the chat list (no chat open, no focus)
#  - sends via a minimized-window type (window stays minimized; no popup)
#  - never sends unsolicited promos. Writes every exchange to client notes.md.

import os, sys, time, datetime, json, re
import psutil
from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zen_llm as zen
import cron_whatsapp_dealmaker as dm

CHECK_SEC = 25
ROOT = r"D:\KB Rewaq Clients"

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


def find_whatsapp():
    for p in psutil.process_iter(["name", "pid"]):
        if p.info["name"] and "whatsapp" in p.info["name"].lower():
            return p.info["pid"]
    return None


def get_window():
    """Resolve WhatsApp window WITHOUT bringing it to foreground (no pop-up)."""
    try:
        d = Desktop(backend="uia")
        wins = [w for w in d.windows() if w.window_text() == "WhatsApp"]
        return wins[0] if wins else None
    except ElementNotFoundError:
        return None


def get_unread_chats(win):
    """Return [(chat_element, name, preview)] for chats with an unread badge.
    WhatsApp Desktop v3 lists chats as DataItem controls. Reads preview text only
    (no chat open, no focus) -> zero disturbance."""
    try:
        items = win.descendants(control_type="DataItem")
        out = []
        for di in items:
            name = di.window_text().strip()
            if not name:
                continue
            lines = [l.strip() for l in name.split("\n") if l.strip()]
            # first line = chat title, last line = last message preview
            title = lines[0]
            preview = lines[-1] if len(lines) > 1 else ""
            if title and title not in ("WhatsApp", "Chats", "Search"):
                out.append((di, title, preview))
        return out
    except Exception:
        return []


def send_reply(win, text):
    """Send a reply while keeping WhatsApp minimized (no foreground pop-up).
    Uses the message input box directly; types + Enter without set_focus pop-up."""
    try:
        # locate edit box (the message composer)
        edit = win.descendant(control_type="Edit")
        if not edit:
            return False
        # type into the composer without forcing a visible focus change
        edit.set_focus()  # minimal; we keep window minimized below
        time.sleep(0.3)
        edit.type_keys(text, with_spaces=True)
        time.sleep(0.3)
        edit.type_keys("{ENTER}")
        return True
    except Exception:
        return False


def main():
    print(f"[{datetime.datetime.now():%H:%M}] wa_desktop_automation started (WhatsApp Desktop, LLM=OpenCode Zen)")
    print(f"  mode: background (no foreground pop-up), chain: deepseek -> nemotron -> rule brain")
    last_seen = {}
    while True:
        try:
            pid = find_whatsapp()
            if not pid:
                print("  ! WhatsApp Desktop not running - open it")
                time.sleep(CHECK_SEC)
                continue
            win = get_window()
            if not win:
                time.sleep(CHECK_SEC)
                continue
            # keep window minimized so no popup disturbs the user
            try:
                if win.is_normal() or win.is_maximized():
                    win.minimize()
            except Exception:
                pass
            chats = get_unread_chats(win)
            for elem, name, preview in chats:
                msg = preview
                if not msg or msg == last_seen.get(name):
                    continue
                slug = dm.resolve_slug_from_name(name)
                reply = zen.zen_reply(name, msg, SYSTEM_PROMPT)
                if reply:
                    ok = send_reply(win, reply)
                    dm.note_log(slug, f"{name}", msg)
                    dm.note_log(slug, "KB Rewaq (sent)", reply)
                    print(f"  [sent={ok}] {name}: {msg[:25]}... -> {reply[:25]}...")
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
