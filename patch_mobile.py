#!/usr/bin/env python3
# Patch all existing client sites: add mobile-first @media breakpoints (<=600px, <=380px)
# to fix phone overlap. Non-destructive: only extends the existing @media block, no content change.
import os, glob

BASE = r"D:\digitalfirst-agency\leads-sites"

MOBILE_CSS = (
    "\n"
    "/* ===== MOBILE-FIRST: phones (<=600px) -> single column, no overlap ===== */\n"
    "@media(max-width:600px){\n"
    "  nav{padding:14px 5%}\n"
    "  .logo{font-size:1.15rem}\n"
    "  .hero h1{font-size:clamp(2.4rem,11vw,3.4rem)}\n"
    "  .hero p{font-size:1rem;padding:0 8px}\n"
    "  .hero .cta{flex-direction:column;gap:12px;padding:0 16px}\n"
    "  .hero .cta .btn{width:100%;text-align:center}\n"
    "  .sgrid,.pgrid,.tgrid,.tgrid2{grid-template-columns:1fr;gap:14px}\n"
    "  .serv,.pkg,.team,.testi,.book,.mapsec,.contact{padding:64px 5%}\n"
    "  .sec-t h2{font-size:clamp(1.8rem,7vw,2.6rem)}\n"
    "  .stats{gap:28px;padding:40px 5%}\n"
    "  .stat .num{font-size:2.6rem}\n"
    "  .bookwrap{padding:24px 18px;border-radius:18px}\n"
    "  .bookwrap .row{grid-template-columns:1fr}\n"
    "  .mc-inner{flex-direction:column;gap:14px;padding:26px 18px;text-align:center}\n"
    "  .mc-pin{font-size:2.2rem}\n"
    "  .cinfo{flex-direction:column;gap:14px}\n"
    "  .wa-float{bottom:16px;right:16px;padding:12px 16px;font-size:.9rem}\n"
    "  .marq{padding:10px 0}\n"
    "  footer{padding:32px 16px;font-size:.78rem}\n"
    "}\n"
    "@media(max-width:380px){\n"
    "  .hero h1{font-size:2.1rem}\n"
    "  .cta .btn{padding:13px 24px;font-size:.92rem}\n"
    "  .sgrid,.pgrid,.tgrid,.tgrid2{gap:12px}\n"
    "}\n"
)

OLD = "@media(max-width:860px){.sgrid,.pgrid,.tgrid,.tgrid2{grid-template-columns:repeat(2,1fr)}.nav-links{display:none}.bookwrap .row{grid-template-columns:1fr}}"

patched = 0
for d in glob.glob(os.path.join(BASE, "*")):
    if not os.path.isdir(d):
        continue
    html = os.path.join(d, "index.html")
    if not os.path.exists(html):
        continue
    s = open(html, encoding="utf-8").read()
    if "MOBILE-FIRST" in s:
        continue  # already patched
    if OLD not in s:
        print(f"SKIP {os.path.basename(d)} (marker not found)")
        continue
    s = s.replace(OLD, OLD + MOBILE_CSS, 1)
    open(html, "w", encoding="utf-8").write(s)
    patched += 1

print(f"[patch] patched {patched} sites with mobile-first breakpoints")
