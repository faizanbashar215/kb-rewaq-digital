#!/usr/bin/env python3
# Patch verify sites' mobile block with compact packages + tighter header (same as template).
import os
BASE = r"D:\digitalfirst-agency\leads-sites"
ADD = (
    "  /* packages: compact card, full-width button, tighter spacing */\n"
    "  .pcard{padding:22px 18px;border-radius:14px}\n"
    "  .pcard h3{font-size:1.35rem}\n"
    "  .pcard .ar{margin:3px 0 10px;font-size:.9rem}\n"
    "  .pcard .pp{font-size:1.9rem}\n"
    "  .pcard p{margin:8px 0 16px;font-size:.85rem;line-height:1.45}\n"
    "  .pcard button{width:100%;padding:13px 20px;font-size:.95rem}\n"
    "  .scard{padding:22px 16px}\n"
    "  .tcard{padding:18px 14px}\n"
    "  .tcard2{padding:20px 16px}\n"
    "  .hero{height:100svh;padding-top:70px}\n"
    "  .hero .kicker{letter-spacing:3px;margin-bottom:12px;font-size:.72rem}\n"
    "  .hero h1{font-size:clamp(2.2rem,10vw,3.2rem);line-height:1.05}\n"
    "  .ham{padding:6px}\n"
)
for slug in ["verify-loop-salon-2", "verify-test-salon"]:
    fp = os.path.join(BASE, slug, "index.html")
    s = open(fp, encoding="utf-8").read()
    if ".pcard h3{font-size:1.35rem}" not in s and "pcard h3{font-size:1.35rem}" not in s:
        # inject before closing of 600px media block (find 'footer{padding:30px' or 'footer{padding:32px')
        if "footer{padding:30px 16px;font-size:.76rem}" in s:
            s = s.replace("footer{padding:30px 16px;font-size:.76rem}\n}", "footer{padding:30px 16px;font-size:.76rem}\n" + ADD + "}", 1)
        elif "footer{padding:32px 16px;font-size:.78rem}" in s:
            s = s.replace("footer{padding:32px 16px;font-size:.78rem}\n}", "footer{padding:32px 16px;font-size:.78rem}\n" + ADD + "}", 1)
        open(fp, "w", encoding="utf-8").write(s)
        print("PATCHED", slug)
    else:
        print("already patched", slug)
