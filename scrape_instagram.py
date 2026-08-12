#!/usr/bin/env python3
# Find Instagram handles + scrape phone from Instagram bio for the 10 leads missing numbers.
# Free sources: DDG/Bing to locate IG profile, then parse bio for phone.
import urllib.request, re, urllib.parse, json, glob, os, time

LEADS = os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients")
have = set(json.load(open(os.path.join(LEADS, "_scraped_phones.json"), encoding="utf-8")).keys()) | {"Akrram"}
names = [json.load(open(d, encoding="utf-8"))["business"]["name_en"]
         for d in sorted(glob.glob(os.path.join(LEADS, "*/client.json")))
         if json.load(open(d, encoding="utf-8"))["business"]["name_en"] not in have]

KW = re.compile(r"\+?965[\s\-]?\d[\d\s\-]{6,11}")
BARE = re.compile(r"\b[2569]\d{7}\b")

def fetch(url, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml", "Accept-Language": "en-US,en;q=0.9"})
        return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception:
        return ""

def find_ig_handle(name):
    # search DDG for the IG profile
    q = f"{name} Kuwait instagram"
    html = fetch("https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(q))
    # instagram.com/<handle> patterns
    handles = set(re.findall(r"instagram\.com/([A-Za-z0-9_.]+)", html))
    handles = [h for h in handles if h.lower() not in ("p", "explore", "accounts", "direct", "stories", "reel", "tv")]
    return handles

def ig_phone(handle):
    # try instagram web profile; bio often in meta or embedded JSON
    html = fetch(f"https://www.instagram.com/{handle}/")
    phones = set(KW.findall(html)) | {"965" + b for b in BARE.findall(html)}
    return phones

found = {}
for nm in names:
    print(f"--- {nm} ---")
    handles = find_ig_handle(nm)
    got = None
    for h in handles[:3]:
        ph = ig_phone(h)
        if ph:
            got = sorted(ph)[0]
            print(f"  IG @{h} -> {got}")
            break
        time.sleep(1)
    if not got:
        # fallback: Bing for "name Kuwait phone" with site:instagram style already covered; try Google cache
        html = fetch("https://www.bing.com/search?q=" + urllib.parse.quote(f"{nm} Kuwait salon phone number"))
        ph = set(KW.findall(html)) | {"965" + b for b in BARE.findall(html)}
        if ph:
            got = sorted(ph)[0]
            print(f"  Bing -> {got}")
    if got:
        got = re.sub(r"\s+|-", "", got).lstrip("+")
        if not got.startswith("965") and len(got) == 8:
            got = "965" + got
        if len(got) == 11:
            found[nm] = got
    else:
        print("  not found")
    time.sleep(1.5)

if found:
    old = json.load(open(os.path.join(LEADS, "_scraped_phones.json"), encoding="utf-8"))
    old.update(found)
    json.dump(old, open(os.path.join(LEADS, "_scraped_phones.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nFound {len(found)} more via Instagram/Bing:", list(found.keys()))
else:
    print("\nNo additional numbers found via Instagram/Bing.")
