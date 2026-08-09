#!/usr/bin/env python3
# KB Rewaq WhatsApp Desktop automation (REPLACES Baileys bridge — no QR, no 515).
# Drives the already-logged-in WhatsApp Desktop app via pywinauto (Windows UI automation).
# Reads new incoming messages, drafts T&C-trained replies (reuses cron_whatsapp_dealmaker brain),
# types + sends. Media (images/video/status) handled by Faizan directly — this is TEXT only.
#
# SAFETY: runs in foreground loop, polls every CHECK_SEC. Only replies to unread chats.
# Never sends unsolicited promos — only responds to inbound client messages.

import os, sys, time, datetime, json
import psutil
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cron_whatsapp_dealmaker as dm  # reuse draft_reply + resolve_slug + note_log

CHECK_SEC = 15          # poll interval
ROOT = r"D:\KB Rewaq Clients"

def find_whatsapp():
    for p in psutil.process_iter(["name", "pid"]):
        if p.info["name"] and "whatsapp" in p.info["name"].lower():
            try:
                return Application(backend="uia").connect(process=p.info["pid"])
            except Exception:
                continue
    return None

def get_unread_chats(app):
    """Returns list of (chat_element, name) for chats showing unread badge."""
    try:
        win = app.window(title_re="WhatsApp")
        win.set_focus()
        # unread chats typically have a child with a count; grab chat list items
        list_items = win.descendants(control_type="ListItem")
        out = []
        for li in list_items:
            name = li.window_text()
            if name and name.strip():
                out.append((li, name.strip()))
        return out
    except ElementNotFoundError:
        return []

def read_last_message(app, chat_elem):
    try:
        chat_elem.click_input()
        time.sleep(1.5)
        win = app.window(title_re="WhatsApp")
        # last message bubble is usually a Text control near bottom
        texts = [t.window_text() for t in win.descendants(control_type="Text") if t.window_text()]
        # filter plausible message (not UI chrome)
        msgs = [t for t in texts if len(t) > 1 and t not in ("WhatsApp", "Search", "New chat", "Menu")]
        return msgs[-1] if msgs else ""
    except Exception as e:
        return ""

def send_reply(app, text):
    try:
        win = app.window(title_re="WhatsApp")
        # focus message box (placeholder "Type a message")
        edit = win.descendant(control_type="Edit")
        edit.click_input()
        time.sleep(0.5)
        edit.type_keys(text, with_spaces=True)
        time.sleep(0.5)
        edit.type_keys("{ENTER}")
        return True
    except Exception as e:
        return False

def main():
    print(f"[{datetime.datetime.now():%H:%M}] wa_desktop_automation started (WhatsApp Desktop, no QR)")
    last_seen = {}  # chat_name -> last message text (avoid double reply)
    while True:
        try:
            app = find_whatsapp()
            if not app:
                print("  ! WhatsApp Desktop not running — start it first")
                time.sleep(CHECK_SEC)
                continue
            chats = get_unread_chats(app)
            for elem, name in chats:
                msg = read_last_message(app, elem)
                if not msg or msg == last_seen.get(name):
                    continue
                # skip our own / groups with no clear sender
                reply = dm.draft_reply(name, msg, dm.resolve_slug_from_name(name))
                if reply:
                    ok = send_reply(app, reply)
                    dm.note_log(dm.resolve_slug_from_name(name), f"{name}", msg)
                    dm.note_log(dm.resolve_slug_from_name(name), "KB Rewaq (sent)", reply)
                    print(f"  ↩ {name}: {msg[:30]}... -> reply sent={ok}")
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
