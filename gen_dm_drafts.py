#!/usr/bin/env python3
# KB Rewaq — gen_dm_drafts.py
# Generates a personalized first-touch WhatsApp DM draft for EVERY client that does not
# yet have one, and saves it to <client>/dms/dm_YYYY-MM-DD.txt.
# Runs offline (no bridge needed) — drafts are queued on disk, sent later when the
# WhatsApp bridge is paired again after its cooldown.
#
# Tone: Hinglish + English + Arabic mix, warm/human, NO emojis, 2-4 lines.
# KB Rewaq brain: tiers 35/95/180/320 KWD/mo, 50% advance, 3-day delivery.

import os, json, glob, datetime

ROOT = r"D:\KB Rewaq Clients"
TODAY = datetime.date.today().strftime("%Y-%m-%d")

# KB Rewaq pricing brain (keep in sync with cron_whatsapp_dealmaker.py)
TIERS = (
    "Tier 1 Presence — 35 KWD/mo (1-page site + 8 posts + 4 reels + logo + 2 videos + IG setup)\n"
    "Tier 2 Growth — 95 KWD/mo (site + booking + 12 posts + 8 reels + 4 videos + full social + 1 ad set)\n"
    "Tier 3 Pro — 180 KWD/mo (full site + SEO + 20 posts + 12 reels + 8 videos + multi-platform + 3 ad campaigns + report)\n"
    "Tier 4 Dominator — 320 KWD/mo (full site + funnel + 30 posts + 20 reels + 15 videos + 360 marketing + 5 campaigns + brand + strategy)"
)

def load_client(slug):
    p = os.path.join(ROOT, slug, "client.json")
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}

def first_touch(name_en, site_url):
    biz = name_en or "your salon"
    return (
        f"Hello Sister, this is Faizan from KB Rewaq Digital — Kuwait. 👋\n"
        f"We build websites + run Instagram/social + paid ads for ladies salons & spas.\n"
        f"I made a free demo site for {biz}: {site_url}\n"
        f"Our packages start at just 35 KWD/month (Tier 1). 50% advance, 3-day delivery, cash/bank ok.\n"
        f"May I share the full packages? No pressure at all. 🙏"
    ).replace("👋", "").replace("🙏", "")  # strip emojis per KB Rewaq brain rule

def ensure_dms(slug):
    d = os.path.join(ROOT, slug, "dms")
    os.makedirs(d, exist_ok=True)
    return d

def main():
    slugs = [os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*")) if os.path.isdir(p) and not os.path.basename(p).startswith("_")]
    made = 0
    for slug in slugs:
        rec = load_client(slug)
        name_en = rec.get("business", {}).get("name_en", "")
        site_url = rec.get("online", {}).get("site_url", "")
        if not site_url:
            # fall back to standard github pages url
            site_url = f"https://faizanbashar215.github.io/kb-rewaq-digital/{slug}/"
        d = ensure_dms(slug)
        draft_path = os.path.join(d, f"dm_{TODAY}.txt")
        # skip if a draft already exists for today
        if os.path.exists(draft_path):
            continue
        text = first_touch(name_en, site_url)
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        made += 1
    print(f"[gen_dm_drafts] wrote {made} new DM drafts across {len(slugs)} clients (today={TODAY})")

if __name__ == "__main__":
    main()
