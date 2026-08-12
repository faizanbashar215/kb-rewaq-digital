#!/usr/bin/env python3
# Aggressive phone scrape for the 14 leads still missing numbers.
# Tries multiple free engines (DDG lite, Bing, Yandex) + varied queries.
import urllib.request, re, urllib.parse, glob, os, json, time

LEADS_DIR = os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients")
names = []
for d in sorted(glob.glob(os.path.join(LEADS_DIR, "*/"))):
    cj = os.path.join(d, "client.json")
    if os.path.isfile(cj):
        j = json.load(open(cj, encoding="utf-8"))
        names.append(j["business"]["name_en"])

KW_PHONE = re.compile(r"\+?965[\s\-]?\d[\d\s\-]{6,11}")
BARE = re.compile(r"\b[2569]\d{7}\b")

def fetch(url, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        return urllib.request.urlopen(req, timeout=18).read().decode("utf-8", "ignore")
    except Exception:
        return ""

def search_engines(query):
    out = set()
    # DDG lite
    out |= set(KW_PHONE.findall(fetch("https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(query))))
    # Bing
    html = fetch("https://www.bing.com/search?q=" + urllib.parse.quote(query))
    out |= set(KW_PHONE.findall(html))
    out |= {"965" + b for b in BARE.findall(html)}
    # Yandex
    html = fetch("https://yandex.com/search/?text=" + urllib.parse.quote(query))
    out |= set(KW_PHONE.findall(html))
    return out

found = {}
for nm in names:
    if nm == "Akrram":
        continue
    candidates = set()
    for q in [f"{nm} Kuwait phone", f"{nm} salon Kuwait contact", f'"{nm}" Kuwait']:
        candidates |= search_engines(q)
        time.sleep(1)
    # normalize to digits only, keep 965-prefixed
    cleaned = []
    for c in candidates:
        c = re.sub(r"\s+|-", "", c)
        if c.startswith("+"):
            c = c[1:]
        if not c.startswith("965"):
            if len(c) == 8:
                c = "965" + c
            else:
                continue
        if len(c) == 11:
            cleaned.append(c)
    if cleaned:
        found[nm] = cleaned[0]
        print(f"  {nm}: {cleaned[0]}")
    else:
        print(f"  {nm}: NOT FOUND")
    time.sleep(0.5)

json.dump(found, open(os.path.join(LEADS_DIR, "_scraped_phones.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nSaved {len(found)} phones -> _scraped_phones.json")
