#!/usr/bin/env python3
# Patch the 2 verify sites (not in gen_site_v9 LEADS) with the same mobile fixes:
# hamburger nav + marq track fix + brace balance. Reuses logic from patch_mobile + template.
import os

BASE = r"D:\digitalfirst-agency\leads-sites"

MOBILE_CSS = (
    "\n/* ===== MOBILE-FIRST: phones (<=600px) -> single column, no overlap ===== */\n"
    "@media(max-width:600px){\n"
    "  nav{padding:14px 5%}\n  .logo{font-size:1.15rem}\n"
    "  .hero h1{font-size:clamp(2.4rem,11vw,3.4rem)}\n"
    "  .hero p{font-size:1rem;padding:0 8px}\n"
    "  .hero .cta{flex-direction:column;gap:12px;padding:0 16px}\n"
    "  .hero .cta .btn{width:100%;text-align:center}\n"
    "  .sgrid,.pgrid,.tgrid,.tgrid2{grid-template-columns:1fr;gap:14px}\n"
    "  .serv,.pkg,.team,.testi,.book,.mapsec,.contact{padding:64px 5%}\n"
    "  .sec-t h2{font-size:clamp(1.8rem,7vw,2.6rem)}\n"
    "  .stats{gap:28px;padding:40px 5%}\n  .stat .num{font-size:2.6rem}\n"
    "  .bookwrap{padding:24px 18px;border-radius:18px}\n  .bookwrap .row{grid-template-columns:1fr}\n"
    "  .mc-inner{flex-direction:column;gap:14px;padding:26px 18px;text-align:center}\n"
    "  .mc-pin{font-size:2.2rem}\n  .cinfo{flex-direction:column;gap:14px}\n"
    "  .wa-float{bottom:16px;right:16px;padding:12px 16px;font-size:.9rem}\n"
    "  .marq{padding:10px 0;overflow:hidden}\n  .marq .track{max-width:100%;white-space:nowrap}\n"
    "  footer{padding:32px 16px;font-size:.78rem}\n}\n"
    "@media(max-width:380px){\n  .hero h1{font-size:2.1rem}\n"
    "  .cta .btn{padding:13px 24px;font-size:.92rem}\n  .sgrid,.pgrid,.tgrid,.tgrid2{gap:12px}\n}\n"
)
HAM_CSS = (
    ".ham{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:8px}\n"
    ".ham span{width:26px;height:2px;background:#fff;transition:.3s;border-radius:2px}\n"
    ".ham.open span:nth-child(1){transform:translateY(7px) rotate(45deg)}\n"
    ".ham.open span:nth-child(2){opacity:0}\n"
    ".ham.open span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}\n"
)
NAV_860 = (
    "@media(max-width:860px){\n"
    "  .sgrid,.pgrid,.tgrid,.tgrid2{grid-template-columns:repeat(2,1fr)}\n"
    "  .bookwrap .row{grid-template-columns:1fr}\n"
    "  .ham{display:flex}\n"
    "  .nav-links{position:fixed;top:64px;right:0;width:min(72vw,260px);height:calc(100vh - 64px);"
    "flex-direction:column;align-items:flex-start;gap:6px;padding:24px 22px;background:rgba(10,10,10,.96);"
    "backdrop-filter:blur(20px);border-left:1px solid rgba(255,255,255,.08);transform:translateX(110%);"
    "transition:transform .35s cubic-bezier(.2,.8,.2,1);overflow-y:auto}\n"
    "  .nav-links.open{transform:translateX(0)}\n"
    "  .nav-links a{margin:10px 0;font-size:1.05rem}\n}\n"
)
HAM_HTML = '<button class="ham" id="ham" aria-label="Menu"><span></span><span></span><span></span></button>'
HAM_JS = (
    "(function(){var ham=document.getElementById('ham');var links=document.getElementById('navLinks');"
    "if(!ham||!links)return;"
    "ham.addEventListener('click',function(){ham.classList.toggle('open');links.classList.toggle('open');});"
    "links.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){"
    "ham.classList.remove('open');links.classList.remove('open');});});})();\n"
)

for slug in ["verify-loop-salon-2", "verify-test-salon"]:
    fp = os.path.join(BASE, slug, "index.html")
    if not os.path.exists(fp):
        print("SKIP", slug, "(no file)"); continue
    s = open(fp, encoding="utf-8").read()
    # 1) add ham CSS after .nav-links a:hover rule
    s = s.replace(".nav-links a:hover{opacity:1;color:var(--ac)}\n",
                  ".nav-links a:hover{opacity:1;color:var(--ac)}\n" + HAM_CSS, 1)
    # 2) replace old 860 block with new (hamburger + dropdown)
    import re
    s = re.sub(r"@media\(max-width:860px\)\{[^}]*\}\n", NAV_860, s, count=1)
    # 3) add mobile-first block before </style>
    s = s.replace("</style>", MOBILE_CSS + "</style>", 1)
    # 4) add hamburger button to nav
    s = s.replace('<div class="nav-links">', HAM_HTML + '\n<div class="nav-links" id="navLinks">', 1)
    # 5) add JS toggle (after scroll listener)
    s = s.replace("addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',scrollY>60));",
                  "addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',scrollY>60));\n" + HAM_JS, 1)
    # 6) brace balance
    style = s.split("<style>")[1].split("</style>")[0]
    if style.count("{") != style.count("}"):
        s = s.replace("<style>" + style + "</style>",
                      "<style>" + style + "}" * (style.count("{") - style.count("}")) + "</style>", 1)
    open(fp, "w", encoding="utf-8").write(s)
    print("PATCHED", slug)
