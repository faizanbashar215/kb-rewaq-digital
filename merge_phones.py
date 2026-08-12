#!/usr/bin/env python3
# Merge scraped phone numbers into client.json records (only for leads missing a real number).
import os, json, glob

LEADS_DIR = os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients")
scraped = json.load(open(os.path.join(LEADS_DIR, "_scraped_phones.json"), encoding="utf-8"))
print(f"Scraped phones available: {len(scraped)}")

merged = 0
for d in sorted(glob.glob(os.path.join(LEADS_DIR, "*/"))):
    cj = os.path.join(d, "client.json")
    if not os.path.isfile(cj):
        continue
    j = json.load(open(cj, encoding="utf-8"))
    name = j["business"]["name_en"]
    con = j.setdefault("contact", {})
    old = con.get("phone", "")
    # If already has a REAL number (not the boss fallback), skip
    if old and old != "96550703252":
        continue
    if name in scraped:
        new_phone = scraped[name]
        con["phone"] = new_phone
        con["phone_disp"] = "+" + new_phone
        con["whatsapp_url"] = f"https://wa.me/{new_phone}"
        # mark source
        j.setdefault("pipeline", {})["phone_source"] = "web_scrape_ddg_bing"
        json.dump(j, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        merged += 1
        print(f"  MERGED {name}: {new_phone}")
    else:
        # keep boss fallback
        con["phone"] = "96550703252"
        con["phone_disp"] = "+96550703252"
        con["whatsapp_url"] = "https://wa.me/96550703252"
        j.setdefault("pipeline", {})["phone_source"] = "boss_fallback_no_source_found"
        json.dump(j, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"\nMerged {merged} real phones. Remaining leads use boss fallback (no public number found).")
