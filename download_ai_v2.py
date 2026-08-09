#!/usr/bin/env python3
"""Download new FLUX hero images for the 5 new salon leads.
Maps stable local names -> fal URLs. Skips existing.
"""
import os, urllib.request

os.makedirs("assets/ai", exist_ok=True)

# (local_name, url) for the 5 new leads (5th reuses a prior style)
MAP = [
    ("hero_kahi.png",     "https://v3b.fal.media/files/b/0aa5addf/BmvP0maXT2WIeMyt-U1nT_zvUnF8nE.png"),
    ("hero_paulita.png",  "https://v3b.fal.media/files/b/0aa5addf/NZmJDc0-2qh-9z3nvnh3C_HoT35OxY.png"),
    ("hero_mahiba.png",   "https://v3b.fal.media/files/b/0aa5adf1/EeIyRFF6OGT6PYbbbYN8h_5NTTjnez.png"),  # reuse as Mahima hero
    ("hero_neweves.png",  "https://v3b.fal.media/files/b/0aa5ade0/uESXP0O7YQSYaKp04C63P_EMoBZ5fx.png"),
    ("hero_yours.png",    "https://v3b.fal.media/files/b/0aa5addf/NZmJDc0-2qh-9z3nvnh3C_HoT35OxY.png"),  # reuse aqua-spa style for Yours
]

# also reuse the 5 existing gallery images already downloaded
for name, url in MAP:
    dst = f"assets/ai/{name}"
    if os.path.exists(dst) and os.path.getsize(dst) > 50000:
        print("skip", name)
        continue
    try:
        urllib.request.urlretrieve(url, dst)
        print("ok", name, os.path.getsize(dst))
    except Exception as e:
        print("FAIL", name, e)

# list all ai assets
print("--- assets/ai ---")
for f in sorted(os.listdir("assets/ai")):
    print(f, os.path.getsize(os.path.join("assets/ai", f)))
