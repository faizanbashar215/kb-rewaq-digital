#!/usr/bin/env python3
# Multi-source FREE WhatsApp-active phone hunter for KB Rewaq Kuwait salon leads.
# Sources: OSM (lead names) + OpenSooq/4Sale (WA-button numbers) + Kuwait Yellow Pages
#          + Instagram bio + DDG/Bing. Verifies each number via wa.me redirect.
import urllib.request, re, urllib.parse, json, os, time, concurrent.futures

LEADS = os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients")
AGENCY = os.environ.get("AGENCY_DIR", r"D:\digitalfirst-agency")
BOSS = "96550703252"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

KW = re.compile(r"\+?965[\s\-]?\d[\d\s\-]{6,11}")
BARE = re.compile(r"\b[2569]\d{7}\b")

def fetch(url, timeout=18):
    try:
        req = urllib.request.Request(url, headers=UA)
        return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")
    except Exception:
        return ""

def norm(c):
    c = re.sub(r"[\s\-]", "", c).lstrip("+")
    if len(c) == 8:
        c = "965" + c
    return c if len(c) == 11 else None

def norm_all(nums):
    out = []
    for c in nums:
        n = norm(c)
        if n and n != BOSS:
            out.append(n)
    return list(dict.fromkeys(out))

def wa_active(num):
    # wa.me returns 200 for any number page; need to detect "not on WhatsApp".
    # Real signal: the page contains the click-to-chat widget / api.whatsapp.com link.
    try:
        req = urllib.request.Request(f"https://wa.me/{num}", headers=UA)
        resp = urllib.request.urlopen(req, timeout=10)
        body = resp.read().decode("utf-8", "ignore")
        loc = resp.headers.get("Location", "")
        # valid WA numbers show api.whatsapp.com in body or redirect
        return ("api.whatsapp.com" in body) or ("api.whatsapp.com" in loc) or ("web.whatsapp.com" in body)
    except Exception:
        return False

def search(q):
    c = set()
    # Google works (DDG blocks scripted requests)
    c |= set(KW.findall(fetch(f"https://www.google.com/search?q={urllib.parse.quote(q)}")))
    h = fetch(f"https://www.bing.com/search?q={urllib.parse.quote(q)}")
    c |= set(KW.findall(h)) | {"965" + b for b in BARE.findall(h)}
    return norm_all(c)

# ---- Source A: OpenSooq / 4Sale (Kuwait classifieds with WA button) ----
def source_opensooq(name):
    nums = set()
    for q in (f"{name} site:opensooq.com", f"{name} site:4sale.com.kw", f"{name} كويت"):
        h = fetch(f"https://www.google.com/search?q={urllib.parse.quote(q)}")
        nums |= set(KW.findall(h))
        # prefer numbers that appear inside wa.me / api.whatsapp links (WA-active)
        nums |= set(re.findall(r"wa\.me/(\d{8,15})", h)) | set(re.findall(r"phone=(\d{8,15})", h))
        time.sleep(0.5)
    return norm_all(nums)

# ---- Source B: Kuwait Yellow Pages (158.ya-seh.com) ----
def source_yellowpages(name):
    nums = set()
    h = fetch(f"https://158.ya-seh.com/search?q={urllib.parse.quote(name)}")
    nums |= set(KW.findall(h))
    h2 = fetch(f"https://www.google.com/search?q={urllib.parse.quote(name + ' 158.ya-seh.com')}")
    nums |= set(KW.findall(h2))
    return norm_all(nums)

# ---- Source C: Instagram bio ----
def source_instagram(name):
    nums = set()
    h = fetch(f"https://www.google.com/search?q={urllib.parse.quote(name + ' Kuwait instagram')}")
    handles = re.findall(r"instagram\.com/([A-Za-z0-9_.]+)", h)
    handles = [x for x in dict.fromkeys(handles) if x.lower() not in ("p","reel","explore","accounts","stories")]
    for hdl in handles[:3]:
        bio = fetch(f"https://www.instagram.com/{hdl}/")
        nums |= set(KW.findall(bio))
        time.sleep(1)
    return norm_all(nums)

# ---- Main: for each pending lead, hunt all sources, verify WA-active, save ----
def main():
    crm = json.load(open(os.path.join(AGENCY, "crm_leads.json"), encoding="utf-8"))
    sp = os.path.join(LEADS, "_scraped_phones.json")
    scraped = json.load(open(sp, encoding="utf-8"))
    pending = [x["name_en"] for x in crm if x["phone"] == BOSS and x["name_en"] not in scraped]
    print(f"Pending leads to hunt: {len(pending)}")
    found = {}
    for nm in pending:
        print(f"--- {nm} ---")
        cand = set()
        cand |= set(source_opensooq(nm))
        cand |= set(source_yellowpages(nm))
        cand |= set(source_instagram(nm))
        cand |= set(search(f"{nm} Kuwait phone whatsapp"))
        # verify which are WA-active
        active = []
        for num in cand:
            if wa_active(num):
                active.append(num)
                print(f"  WA-ACTIVE {num}")
                break
            else:
                print(f"  inactive {num}")
            time.sleep(0.3)
        if active:
            found[nm] = active[0]
            base = json.load(open(sp, encoding="utf-8"))
            base.update(found)
            json.dump(base, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        else:
            print("  none active found")
        time.sleep(0.5)
    if found:
        print(f"\nFound {len(found)} WA-active numbers:", list(found.keys()))
    else:
        print("\nNo WA-active numbers found on free sources.")

if __name__ == "__main__":
    main()
