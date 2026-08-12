#!/usr/bin/env python3
# Render an advanced Gloss site and save a screenshot for the boss to view.
import os
from playwright.sync_api import sync_playwright
OUT = r"D:\digitalfirst-agency\gloss_adv_preview.png"
URL = "http://localhost:8800/beautytek-for-women/"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1280,"height":900})
    pg.goto(URL, wait_until="networkidle"); pg.wait_for_timeout(1500)
    pg.screenshot(path=OUT, full_page=False)
    b.close()
print("saved", OUT, os.path.getsize(OUT), "bytes")
