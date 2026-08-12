#!/usr/bin/env python3
# Aggressive hunt for the 6 remaining pending leads using extra sources:
# Kuwait yellow pages, Google cache, Facebook pages, LinkedIn, 158.ya-seh.com, q8nadar.
import urllib.request, re, urllib.parse, json, os, time

LEADS = r"D:\KB Rewaq Clients"
sp = os.path.join(LEADS, "_scraped_phones.json")
scraped = json.load(open(sp, encoding="utf-8"))
crm = json.load(open(r"D:\digitalfirst-agency\crm_leads.json", encoding="utf-8"))
pending = [x["name_en"] for x in crm if x["phone"] == "96550703252" and x["name_en"] not in scraped]
BOSS = "96550703252"

KW = re.compile(r"\+?965[\s\-]?\d[\d\s\-]{6,11}")
BARE = re.compile(r"\b[2569]\d{7}\b")

def fetch(url, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"})
        return urllib.request.urlopen(req, timeout=18).read().decode("utf-8", "ignore")
    except Exception:
        return ""

def normalize(nums):
    out = []
    for c in nums:
        c = re.sub(r"\s+|-", "", c).lstrip("+")
        if not c.startswith("965") and len(c) == 8:
            c = "965" + c
        if len(c) == 11 and c != BOSS:
            out.append(c)
    return list(dict.fromkeys(out))

def multi(qs):
    c = set()
    for q in qs:
        # many engines
        c |= set(KW.findall(fetch("https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(q))))
        c |= set(KW.findall(fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q))))
        h = fetch("https://www.bing.com/search?q=" + urllib.parse.quote(q))
        c |= set(KW.findall(h)) | {"965" + b for b in BARE.findall(h)}
        c |= set(KW.findall(fetch("https://search.yahoo.com/search?p=" + urllib.parse.quote(q))))
        c |= set(KW.findall(fetch("https://www.google.com/search?q=" + urllib.parse.quote(q))))
        time.sleep(0.6)
    return c

found = {}
for nm in pending:
    print(f"--- {nm} ---")
    qs = [
        f"{nm} Kuwait",
        f"{nm} Kuwait phone",
        f"{nm} صالون الكويت",
        f"{nm} Kuwait salon number",
        f'"{nm}" "+965"',
        f"{nm} kuwait 2",
    ]
    c = multi(qs)
    # extra: facebook page
    fb = fetch("https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(f"{nm} Kuwait facebook"))
    fb_handles = set(re.findall(r"facebook\.com/([A-Za-z0-9_.]+)", fb))
    fb_handles = [h for h in fb_handles if h.lower() not in ("pages","groups","events","profile.php")]
    for h in fb_handles[:3]:
        c |= set(KW.findall(fetch(f"https://www.facebook.com/{h}")))
        time.sleep(1)
    clean = normalize(c)
    if clean:
        found[nm] = clean[0]
        base = json.load(open(sp, encoding="utf-8")) if os.path.isfile(sp) else {}
        base.update(found)
        json.dump(base, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  FOUND {nm}: {clean[0]}")
    else:
        print("  not found")
    time.sleep(0.5)

if found:
    print(f"\nFound {len(found)} more:", list(found.keys()))
else:
    print("\nNone of the 6 found on extended sources either.")
