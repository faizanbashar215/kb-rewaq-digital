#!/usr/bin/env python3
# Generate salon demo websites from fresh OSM leads. Self-contained template.
# Usage: python gen_site_fresh.py
import os, json, re, base64, urllib.request, urllib.parse, random

BASE_DIR = os.environ.get("AGENCY_DIR", r"D:\digitalfirst-agency")
LEADS_F = os.path.join(BASE_DIR, "fresh_leads", "raw.json")
OUT = os.path.join(BASE_DIR, "fresh_sites")
ASSETS = os.path.join(BASE_DIR, "assets", "ai")
OWN_WA = "96550703252"  # founder WA for generic CTA

def slugify(n):
    s = n.lower().replace("'", "").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:40]

# sample services/packages (generic Kuwait salon menu, KWD)
SERVICES = [
    ("Haircut & Blowdry", "قص وتصفيف", 4, ["Haircut", "Blowdry", "Style"]),
    ("Hair Color & Balayage", "صبغ وبلاجاج", 22, ["Full color", "Balayage", "Root touch-up"]),
    ("Keratin / Protein", "كيراتين وبروتين", 18, ["Keratin", "Protein treatment"]),
    ("Classic Facial", "تنظيف البشرة", 8, ["Deep cleanse", "Extraction", "Mask"]),
    ("Gold / Hydra Facial", "فيشل ذهبي", 15, ["Hydradermie", "Gold mask"]),
    ("Gel Manicure", "مانيكير جل", 6, ["Gel polish", "Nail art +2"]),
    ("Pedicure & Spa", "باديكير سبا", 7, ["Spa pedicure", "Foot care"]),
    ("Bridal Makeup", "مكياج عروس", 45, ["Trial incl.", "HD makeup", "Lashes"]),
]
PACKAGES = [
    ("Glow Package", "باقة الإشراق", 15, "Fruit Facial + Pedicure + Half-leg Wax"),
    ("Royal Package", "باقة ملكية", 25, "Gold Facial + Hair Spa + Manicure"),
    ("Bridal Package", "باقة العروس", 80, "Bridal Makeup + Trial + Hair + Facial"),
]
TEAM = [("Hala", "Master Stylist", "هالة"), ("Reem", "Bridal Specialist", "ريم"), ("Sara", "Skin Expert", "سارة")]
REVIEWS = [
    ("Hala A.", "Best salon experience in Kuwait! The balayage is incredible."),
    ("Sara M.", "So personalized and calm. Love the gold facial."),
    ("Layla K.", "Finally a salon that treats you like family!"),
]
GAL = ["gal_facial.png", "gal_hair.png", "gal_manicure.png", "gal_pedicure.png", "gal_bridal.png"]
ACCENTS = ["#e8b4d4", "#d4af6a", "#a8d4e8", "#c8a8e8", "#e8c4a8", "#b8e8c8", "#e8a8c8", "#d4c8a8"]

TPL = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name_en} — Luxury Beauty Salon Kuwait</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root{{--ac:{accent};--bg:#0c0c0c;--fg:#f5f5f5}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Poppins',sans-serif;background:var(--bg);color:var(--fg);line-height:1.6;overflow-x:hidden}}
img{{max-width:100%}}
a{{color:var(--ac);text-decoration:none}}
nav{{position:fixed;top:0;width:100%;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:16px 5%;transition:.4s}}
nav.scrolled{{background:rgba(10,10,10,.9);backdrop-filter:blur(12px);padding:10px 5%}}
.logo{{font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:700;color:#fff}}
.nav-links{{display:flex;align-items:center;gap:22px}}
.nav-links a{{color:#fff;opacity:.85;font-size:.85rem}}
.nav-links a:hover{{opacity:1;color:var(--ac)}}
.ham{{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:6px}}
.ham span{{width:26px;height:2px;background:#fff;display:block}}
.hero{{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.hero img.bg{{position:absolute;inset:0;width:110%;height:110%;object-fit:cover;opacity:.42;filter:saturate(1.1)}}
.hero .ov{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,.35))}}
.hero .con{{position:relative;z-index:2;padding:0 18px;max-width:760px}}
.hero .kicker{{letter-spacing:3px;text-transform:uppercase;font-size:.72rem;color:var(--ac);margin-bottom:12px}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.4rem,9vw,5rem);font-weight:700;line-height:1.05}}
.hero p{{margin:14px auto 26px;max-width:540px;opacity:.85;font-size:.95rem}}
.cta{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
.btn{{padding:13px 26px;border-radius:30px;font-weight:600;font-size:.9rem;cursor:pointer;transition:.3s;border:1px solid var(--ac)}}
.btn.p{{background:var(--ac);color:#0a0a0a}}
.btn.s{{background:transparent;color:var(--ac)}}
.btn:hover{{transform:translateY(-2px)}}
section{{padding:64px 5%}}
.sec-t{{text-align:center;margin-bottom:40px}}
.sec-t h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(1.8rem,7vw,3rem);font-weight:700}}
.sec-t p{{opacity:.7;margin-top:8px}}
.sgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}}
.scard{{border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:24px 18px;background:#121212;transition:.3s}}
.scard:hover{{border-color:var(--ac);transform:translateY(-4px)}}
.scard h3{{font-family:'Cormorant Garamond',serif;font-size:1.4rem;margin-bottom:4px}}
.scard .ar{{color:var(--ac);font-size:.9rem;margin-bottom:10px}}
.scard .price{{font-size:1.7rem;font-weight:700;color:var(--ac);margin-bottom:10px}}
.scard ul{{list-style:none;opacity:.75;font-size:.85rem}}
.scard li{{padding:3px 0;border-bottom:1px dashed rgba(255,255,255,.08)}}
.scard button{{margin-top:14px;width:100%;padding:11px;border-radius:24px;border:1px solid var(--ac);background:transparent;color:var(--ac);font-weight:600;cursor:pointer}}
.pgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}
.pcard{{border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:26px 20px;text-align:center;background:#121212}}
.pcard h3{{font-family:'Cormorant Garamond',serif;font-size:1.5rem}}
.pcard .ar{{color:var(--ac);font-size:.95rem;margin:4px 0 12px}}
.pcard .pp{{font-size:2rem;font-weight:700;color:var(--ac)}}
.pcard p{{opacity:.75;font-size:.88rem;margin:10px 0 18px}}
.pcard button{{padding:12px 28px;border-radius:28px;border:1px solid var(--ac);background:transparent;color:var(--ac);font-weight:600;cursor:pointer}}
.gal{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}}
.gal img{{width:100%;height:170px;object-fit:cover;border-radius:12px}}
.tgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}}
.tcard{{text-align:center;padding:18px;border:1px solid rgba(255,255,255,.08);border-radius:14px}}
.tcard img{{width:80px;height:80px;border-radius:50%;object-fit:cover;margin:0 auto 10px}}
.tcard h3{{font-family:'Cormorant Garamond',serif;font-size:1.2rem}}
.testi{{max-width:760px;margin:0 auto;display:grid;gap:14px}}
.testi .t{{border-left:3px solid var(--ac);padding:12px 18px;background:#121212;border-radius:8px}}
.testi .t b{{color:var(--ac)}}
.book{{max-width:560px;margin:0 auto;background:#121212;border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:26px 20px}}
.book input,.book select,.book textarea{{width:100%;padding:11px;margin:6px 0;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:#0c0c0c;color:#fff}}
.book button{{width:100%;padding:13px;border-radius:28px;border:none;background:var(--ac);color:#0a0a0a;font-weight:700;cursor:pointer;margin-top:10px}}
footer{{text-align:center;padding:32px 16px;font-size:.8rem;opacity:.6;border-top:1px solid rgba(255,255,255,.08)}}
.wa-float{{position:fixed;bottom:18px;right:18px;background:var(--ac);color:#0a0a0a;padding:12px 18px;border-radius:30px;font-weight:600;z-index:90;box-shadow:0 6px 24px rgba(0,0,0,.4)}}
@media(max-width:600px){{
  .nav-links{{position:fixed;top:60px;right:0;width:72vw;max-width:280px;height:calc(100vh - 60px);flex-direction:column;align-items:flex-start;gap:8px;padding:24px 20px;background:rgba(10,10,10,.97);transform:translateX(110%);transition:transform .35s;overflow-y:auto}}
  .nav-links.open{{transform:translateX(0)}}
  .ham{{display:flex}}
  section{{padding:54px 5%}}
  .hero h1{{font-size:clamp(2.1rem,10vw,3rem)}}
}}
</style></head><body>
<nav id="nav"><div class="logo">{name_en}</div>
<button class="ham" id="ham"><span></span><span></span><span></span></button>
<div class="nav-links" id="navLinks">
<a href="#services">Services</a><a href="#gallery">Gallery</a><a href="#team">Team</a><a href="#packages">Packages</a><a href="#book">Book</a>
</div></nav>

<header class="hero">
<img class="bg" src="{hero}" alt="">
<div class="ov"></div>
<div class="con">
<div class="kicker">Luxury Beauty · Kuwait</div>
<h1>{name_en}</h1>
<p>{name_ar} — Premium ladies salon & spa in {area}. Hair, skin, nails & bridal, crafted with love.</p>
<div class="cta">
<a class="btn p" href="https://wa.me/{wa}?text=Hello%20{name_en}!%20I%20want%20to%20book%20an%20appointment.">Book on WhatsApp</a>
<a class="btn s" href="#book">View Packages</a>
</div></div></header>

<section id="services"><div class="sec-t"><h2>Our Services</h2><p>خدماتنا — priced in Kuwaiti Dinar</p></div>
<div class="sgrid">{svcs}</div></section>

<section id="gallery" style="background:#0a0a0a"><div class="sec-t"><h2>Gallery</h2></div>
<div class="gal">{gal}</div></section>

<section id="team"><div class="sec-t"><h2>Our Team</h2></div>
<div class="tgrid">{team}</div></section>

<section id="packages" style="background:#0a0a0a"><div class="sec-t"><h2>Packages</h2><p>باقاتنا</p></div>
<div class="pgrid">{pkgs}</div></section>

<section id="reviews"><div class="sec-t"><h2>What Clients Say</h2></div>
<div class="testi">{revs}</div></section>

<section id="book"><div class="sec-t"><h2>Book Appointment</h2></div>
<div class="book">
<input id="bn" placeholder="Your Name"><input id="bp" placeholder="Phone (WhatsApp)">
<select id="bs">{opts}</select>
<input id="bd" type="date"><input id="bt" type="time"><textarea id="bm" placeholder="Note (optional)"></textarea>
<button onclick="sendBook()">Request Booking</button></div></section>

<footer>© {name_en} · Designed by KB Rewaq Digital · +965 50703252</footer>
<a class="wa-float" href="https://wa.me/{wa}">💬 WhatsApp Booking</a>
<script>
document.getElementById('nav').classList.toggle('scrolled',scrollY>60);
addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',scrollY>60));
const ham=document.getElementById('ham'),links=document.getElementById('navLinks');
ham.onclick=()=>{{links.classList.toggle('open');ham.classList.toggle('open')}};
links.querySelectorAll('a').forEach(a=>a.onclick=()=>links.classList.remove('open'));
function wa(s){{const t=encodeURIComponent('Hello {name_en}! I want to book: '+s);open('https://wa.me/{wa}?text='+t,'_blank')}}
function sendBook(){{const n=bn.value,p=bp.value,s=bs.value,d=bd.value,t=bt.value,m=bm.value;
const msg='Hello {name_en}! New booking:\\nName: '+n+'\\nPhone: '+p+'\\nService: '+s+'\\nDate: '+d+'\\nTime: '+t+'\\nNote: '+m;
open('https://wa.me/{wa}?text='+encodeURIComponent(msg),'_blank')}}
</script></body></html>"""

def monogram(name, accent):
    initials = "".join([w[0] for w in name.split()[:2]]).upper()
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80"><rect width="80" height="80" rx="40" fill="{accent}"/><text x="50%" y="54%" font-family="serif" font-size="32" fill="#0a0a0a" text-anchor="middle" dominant-baseline="middle" font-weight="700">{initials}</text></svg>'
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"

def gen(lead, i):
    name = lead["name"]
    slug = lead["slug"]
    phone = lead.get("phone", "").replace(" ", "")
    wa = phone if phone.startswith("965") else (phone.lstrip("+") if phone else OWN_WA)
    if not wa.startswith("965"):
        wa = OWN_WA
    accent = ACCENTS[i % len(ACCENTS)]
    area = lead.get("city") or "Kuwait"
    # arabic name fallback
    name_ar = "صالون " + name
    hero = f"../assets/ai/hero_{slug}.png" if os.path.isfile(os.path.join(ASSETS, f"hero_{slug}.png")) else "../assets/ai/gal_bridal.png"
    svcs = ""
    for (en, ar, price, items) in SERVICES:
        li = "".join(f"<li>{it}</li>" for it in items)
        svcs += f'<div class="scard"><h3>{en}</h3><div class="ar">{ar}</div><div class="price">{price}<small> KD</small></div><ul>{li}</ul><button onclick="wa(\'{en}\')">Book</button></div>'
    gal = "".join(f'<img src="../assets/ai/{g}" alt="">' for g in GAL)
    team = "".join(f'<div class="tcard"><img src="{monogram(n, accent)}"><h3>{n}</h3><div class="ar">{ar}</div><p>{role}</p></div>' for (n, role, ar) in TEAM)
    pkgs = ""
    for j, (en, ar, price, desc) in enumerate(PACKAGES):
        feat = '<div class="feat" style="color:var(--ac);font-size:.75rem;margin-bottom:6px">POPULAR</div>' if j == 1 else ""
        pkgs += f'<div class="pcard">{feat}<h3>{en}</h3><div class="ar">{ar}</div><div class="pp">{price}<small> KD</small></div><p>{desc}</p><button onclick="wa(\'{en}\')">Book Package</button></div>'
    revs = "".join(f'<div class="t"><b>{who}</b> — {txt}</div>' for (who, txt) in REVIEWS)
    opts = "".join(f'<option value="{en} ({price} KD)">{en} — {price} KD</option>' for (en, ar, price, items) in SERVICES)
    html = TPL.format(name_en=name, name_ar=name_ar, area=area, accent=accent, hero=hero,
                      svcs=svcs, gal=gal, team=team, pkgs=pkgs, revs=revs, opts=opts, wa=wa)
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
    # CRM record
    rec = {
        "business": {"name_en": name, "name_ar": name_ar, "slug": slug},
        "contact": {"phone": wa, "phone_disp": f"+{wa}" if wa else "", "whatsapp_url": f"https://wa.me/{wa}"},
        "location": {"area_en": area},
        "online": {"site_url": f"https://faizanbashar215.github.io/kb-rewaq-digital/fresh_sites/{slug}/", "site_status": "live_fresh"},
        "pipeline": {"status": "lead_new", "created": "2026-08-11", "source": "osm_fresh_scan"},
    }
    os.makedirs(os.path.join(os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients"), slug), exist_ok=True)
    json.dump(rec, open(os.path.join(os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients"), slug, "client.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return slug

def main():
    leads = json.load(open(LEADS_F, encoding="utf-8"))
    # pick clean names (english, has area or known), skip generic/men-only
    pick = []
    for l in leads:
        n = l["name"]
        if not re.search(r"[a-zA-Z]", n):
            continue  # skip arabic-only
        if any(w in n.lower() for w in ["men", "gent", "for men", "gentleman", "ك"]):
            continue
        pick.append(l)
        if len(pick) >= 15:
            break
    print(f"Picked {len(pick)} leads for demo sites")
    for i, l in enumerate(pick):
        s = gen(l, i)
        print(f"  [{i+1}] {s} — {l['name']}")
    print(f"DONE. Sites in {OUT}")

if __name__ == "__main__":
    main()
