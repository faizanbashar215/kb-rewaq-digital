#!/usr/bin/env python3
# scrape_pending.py — aggressive phone hunt for leads still on boss fallback.
# Tries many free sources + query variations. Writes found numbers to _scraped_phones.json.
import urllib.request, re, urllib.parse, json, glob, os, time

# Paths come from env (Docker mount points) with Windows defaults for local runs.
LEADS = os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients")
AGENCY = os.environ.get("AGENCY_DIR", r"D:\digitalfirst-agency")
BOSS = "96550703252"

# load current CRM to find pending leads
crm = json.load(open(os.path.join(AGENCY, "crm_leads.json"), encoding="utf-8"))
pending = [x["name_en"] for x in crm if x["phone"] == BOSS]
# keep only those still missing from scraped
scraped = json.load(open(os.path.join(LEADS, "_scraped_phones.json"), encoding="utf-8"))
pending = [n for n in pending if n not in scraped]

KW = re.compile(r"\+?965[\s\-]?\d[\d\s\-]{6,11}")
BARE = re.compile(r"\b[2569]\d{7}\b")

def fetch(url, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"})
        return urllib.request.urlopen(req, timeout=18).read().decode("utf-8", "ignore")
    except Exception:
        return ""

def search(q):
    out = set()
    # DuckDuckGo lite
    out |= set(KW.findall(fetch("https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(q))))
    # Bing
    h = fetch("https://www.bing.com/search?q=" + urllib.parse.quote(q))
    out |= set(KW.findall(h)) | {"965" + b for b in BARE.findall(h)}
    # Yandex
    out |= set(KW.findall(fetch("https://yandex.com/search/?text=" + urllib.parse.quote(q))))
    return out

def normalize(nums):
    clean = []
    for c in nums:
        c = re.sub(r"\s+|-", "", c).lstrip("+")
        if not c.startswith("965") and len(c) == 8:
            c = "965" + c
        if len(c) == 11:
            clean.append(c)
    # dedupe, prefer ones not equal to boss
    clean = [c for c in dict.fromkeys(clean) if c != BOSS]
    return clean

found = {}
for nm in pending:
    candidates = set()
    # many query shapes
    for q in [
        f"{nm} Kuwait phone number",
        f"{nm} salon Kuwait contact",
        f'"{nm}" Kuwait',
        f"{nm} Kuwait +965",
        f"{nm} صالون الكويت رقم",
        f"{nm} Kuwait telephone",
    ]:
        candidates |= search(q)
        time.sleep(0.8)
    # extra: Instagram handle hunt
    ig = fetch("https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(f"{nm} Kuwait instagram"))
    handles = set(re.findall(r"instagram\.com/([A-Za-z0-9_.]+)", ig))
    handles = [h for h in handles if h.lower() not in ("p","explore","accounts","direct","stories","reel","tv")]
    for h in handles[:3]:
        candidates |= set(KW.findall(fetch(f"https://www.instagram.com/{h}/")))
        time.sleep(1)
    clean = normalize(candidates)
    if clean:
        found[nm] = clean[0]
        # save incrementally so a timeout doesn't lose progress
        sp = os.path.join(LEADS, "_scraped_phones.json")
        base = json.load(open(sp, encoding="utf-8")) if os.path.isfile(sp) else {}
        base.update(found)
        json.dump(base, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  FOUND {nm}: {clean[0]}")
    else:
        print(f"  not found: {nm}")
    time.sleep(0.5)

if found:
    old = json.load(open(os.path.join(LEADS, "_scraped_phones.json"), encoding="utf-8"))
    old.update(found)
    json.dump(old, open(os.path.join(LEADS, "_scraped_phones.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nSaved {len(found)} new numbers -> _scraped_phones.json")
else:
    print("\nNo new numbers found across all sources.")
