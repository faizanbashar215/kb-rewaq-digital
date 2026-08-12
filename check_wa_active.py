#!/usr/bin/env python3
# Check which of our scraped numbers are actually on WhatsApp.
# Free method: wa.me/<number> returns a redirect to the chat if the number exists on WA.
import json, urllib.request, concurrent.futures

phones = json.load(open(r"D:\KB Rewaq Clients\_scraped_phones.json", encoding="utf-8"))
UA = {"User-Agent":"Mozilla/5.0"}

def check(num):
    try:
        req = urllib.request.Request(f"https://wa.me/{num}", headers=UA, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=12)
        # wa.me redirects to api.whatsapp.com if number is on WA
        loc = resp.headers.get("Location","")
        return num, ("api.whatsapp.com" in loc)
    except urllib.error.HTTPError as e:
        # 400/404 => not on WA; sometimes 429 (rate limit)
        return num, False
    except Exception:
        return num, None

results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    for num, ok in ex.map(check, phones.values()):
        results[num] = ok

print("WhatsApp-active check:")
for name, num in phones.items():
    print(f"  {name}: {num} -> {'ACTIVE' if results.get(num) else 'INACTIVE/unknown'}")
active = sum(1 for v in results.values() if v)
print(f"\nACTIVE: {active}/{len(phones)}")
