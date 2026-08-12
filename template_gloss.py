#!/usr/bin/env python3
# Gloss-inspired luxury template for KB Rewaq salon sites.
# Palette extracted from glosssalonkw.com:
#   cream bg   #FAF4EF / #FDFAF8
#   dark plum  #1A0812 / #2D1520 / #3D1C2E
#   gold       #C9A96E
#   rose       #C07A9A / #D4A0B8 / #F5D5E5
#   pink       #ec4899 / #F5D5E5
# Fonts: serif display (--font-d) + clean sans (--font-b)
# Features: canvas hero glow, spaced serif headings, sticky book bar, floating WA button.

GLOSS_CSS = """
:root{
  --cream:#FAF4EF; --cream2:#FDFAF8; --plum:#1A0812; --plum2:#2D1520;
  --plum3:#3D1C2E; --gold:#C9A96E; --rose:#C07A9A; --rose2:#D4A0B8;
  --pink:#ec4899; --pink2:#F5D5E5; --white:#fff;
  --font-d:"Playfair Display",Georgia,"Times New Roman",serif;
  --font-b:"Poppins","Segoe UI",system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font-b);background:var(--cream);color:var(--plum2);line-height:1.7}
h1,h2,h3{font-family:var(--font-d);font-weight:700;line-height:1.15;color:var(--plum)}
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;background:radial-gradient(circle at 50% 30%,#2D1520 0%,#1A0812 70%);color:var(--cream);overflow:hidden}
.hero canvas{position:absolute;inset:0;opacity:.5}
.hero h1{font-size:clamp(3rem,9vw,7rem);letter-spacing:.35em;color:var(--cream);text-indent:.35em;margin-bottom:1rem}
.hero .tag{font-family:var(--font-b);letter-spacing:.18em;text-transform:uppercase;color:var(--gold);font-size:.85rem}
.hero .sub{color:var(--rose2);max-width:540px;margin:1.2rem auto 2rem;font-size:1.05rem}
.btn{display:inline-block;padding:.95rem 2.4rem;border-radius:40px;font-weight:600;letter-spacing:.05em;
  text-decoration:none;transition:.3s;font-family:var(--font-b)}
.btn-gold{background:linear-gradient(135deg,var(--gold),#e6c389);color:var(--plum);box-shadow:0 8px 30px rgba(201,169,110,.35)}
.btn-gold:hover{transform:translateY(-3px)}
.btn-rose{background:linear-gradient(135deg,var(--pink),var(--rose));color:#fff}
.section{padding:6rem 1.5rem;max-width:1100px;margin:0 auto}
.section.alt{background:var(--cream2)}
.eyebrow{font-family:var(--font-b);letter-spacing:.25em;text-transform:uppercase;color:var(--gold);font-size:.8rem;margin-bottom:.8rem}
.section h2{font-size:clamp(2rem,5vw,3.2rem);margin-bottom:2.5rem;text-align:center}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem}
.card{background:#fff;border:1px solid rgba(192,122,154,.25);border-radius:18px;padding:2rem;transition:.3s}
.card:hover{transform:translateY(-6px);box-shadow:0 18px 40px rgba(45,21,32,.12)}
.card h3{color:var(--plum3);margin-bottom:.6rem}
.card p{color:#6b5560;font-size:.95rem}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.8rem}
.gallery .ph{aspect-ratio:1;border-radius:14px;background:linear-gradient(135deg,var(--pink2),var(--rose2))}
.reviews{display:flex;gap:1.5rem;overflow-x:auto;padding-bottom:1rem}
.review{min-width:280px;background:#fff;border-radius:16px;padding:1.6rem;border-left:4px solid var(--gold)}
.review p{font-style:italic;color:#5a4450}
.review .who{margin-top:.8rem;color:var(--gold);font-weight:600}
.insta{text-align:center}
.insta a{color:var(--pink);font-weight:600;text-decoration:none;font-size:1.1rem}
.contact{background:var(--plum);color:var(--cream);text-align:center;border-radius:0}
.contact h2{color:var(--cream)}
.contact a{color:var(--gold)}
footer{background:var(--plum3);color:var(--rose2);text-align:center;padding:2.5rem 1rem;font-size:.85rem}
.sticky{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
  padding:.8rem 1.5rem;background:rgba(26,8,18,.9);backdrop-filter:blur(8px)}
.sticky .brand{font-family:var(--font-d);color:var(--gold);font-size:1.3rem;letter-spacing:.1em}
.fab{position:fixed;bottom:24px;right:24px;z-index:60;display:flex;align-items:center;gap:.5rem;
  background:#25D366;color:#fff;padding:.85rem 1.3rem;border-radius:40px;text-decoration:none;font-weight:600;
  box-shadow:0 8px 25px rgba(37,211,102,.4)}
@media(max-width:600px){.hero h1{letter-spacing:.2em}.section{padding:4rem 1.2rem}}
"""

# Advanced Gloss renderer: full feature set (services+prices, packages, team, gallery images,
# reviews, booking form) wrapped in the cream/plum/gold luxury theme.
ADV_CSS = GLOSS_CSS + """
.sgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.4rem}
.scard{background:#fff;border:1px solid rgba(192,122,154,.25);border-radius:18px;padding:1.8rem 1.4rem;transition:.3s}
.scard:hover{transform:translateY(-6px);box-shadow:0 18px 40px rgba(45,21,32,.12)}
.scard h3{color:var(--plum3);font-size:1.4rem;margin-bottom:.3rem}
.scard .ar{color:var(--gold);font-size:.9rem;margin-bottom:.5rem}
.scard .price{font-size:1.7rem;font-weight:700;color:var(--plum3);margin-bottom:.6rem}
.scard ul{list-style:none;color:#6b5560;font-size:.85rem}
.scard li{padding:3px 0;border-bottom:1px dashed rgba(192,122,154,.2)}
.scard button{margin-top:1rem;width:100%;padding:11px;border-radius:24px;border:1px solid var(--gold);background:transparent;color:var(--plum3);font-weight:600;cursor:pointer;transition:.3s}
.scard button:hover{background:var(--gold);color:var(--plum)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.4rem}
.pcard{border:1px solid rgba(192,122,154,.3);border-radius:18px;padding:1.8rem;text-align:center;background:#fff}
.pcard h3{color:var(--plum3);font-size:1.5rem}
.pcard .ar{color:var(--gold);margin:.4rem 0}
.pcard .pp{font-size:2rem;font-weight:700;color:var(--plum3)}
.pcard p{color:#6b5560;font-size:.88rem;margin:.6rem 0 1rem}
.pcard button{padding:11px 26px;border-radius:28px;border:1px solid var(--gold);background:transparent;color:var(--plum3);font-weight:600;cursor:pointer}
.pcard button:hover{background:var(--gold);color:var(--plum)}
.gal{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.gal img{width:100%;height:170px;object-fit:cover;border-radius:12px}
.tgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem}
.tcard{text-align:center;padding:1.2rem;border:1px solid rgba(192,122,154,.2);border-radius:14px;background:#fff}
.tcard img{width:80px;height:80px;border-radius:50%;object-fit:cover;margin:0 auto .6rem}
.tcard h3{color:var(--plum3);font-size:1.2rem}
.testi{max-width:760px;margin:0 auto;display:grid;gap:14px}
.testi .t{border-left:3px solid var(--gold);padding:12px 18px;background:#fff;border-radius:8px;color:#5a4450}
.testi .t b{color:var(--gold)}
.book{max-width:560px;margin:0 auto;background:#fff;border:1px solid rgba(192,122,154,.3);border-radius:18px;padding:1.6rem 1.2rem}
.book input,.book select,.book textarea{width:100%;padding:11px;margin:6px 0;border-radius:10px;border:1px solid rgba(192,122,154,.3);background:var(--cream2);color:var(--plum2);font-family:var(--font-b)}
.book button{width:100%;padding:13px;border-radius:28px;border:none;background:linear-gradient(135deg,var(--gold),#e6c389);color:var(--plum);font-weight:700;cursor:pointer;margin-top:10px}
.wa-float{position:fixed;bottom:18px;right:18px;background:#25D366;color:#fff;padding:12px 18px;border-radius:30px;font-weight:600;z-index:90;box-shadow:0 6px 24px rgba(37,211,102,.4);text-decoration:none}
"""

BOOK_JS = """
<script>
const ham=document.getElementById('ham'),links=document.getElementById('navLinks');
if(ham){ham.onclick=()=>{links.classList.toggle('open');ham.classList.toggle('open')};
links.querySelectorAll('a').forEach(a=>a.onclick=()=>links.classList.remove('open'));}
function wa(s){const t=encodeURIComponent('Hello {NAME}! I want to book: '+s);open('https://wa.me/{WA}?text='+t,'_blank')}
function sendBook(){const n=bn.value,p=bp.value,s=bs.value,d=bd.value,t=bt.value,m=bm.value;
const msg='Hello {NAME}! New booking:\\nName: '+n+'\\nPhone: '+p+'\\nService: '+s+'\\nDate: '+d+'\\nTime: '+t+'\\nNote: '+m;
open('https://wa.me/{WA}?text='+encodeURIComponent(msg),'_blank')}
</script>
"""

def render_gloss_advanced(name_en, area, phone, wa_url, services, packages, team, gallery_imgs, reviews, hero_img):
    svc = "".join(
        f'<div class="scard"><h3>{en}</h3><div class="ar">{ar}</div><div class="price">{price}<small> KD</small></div>'
        f'<ul>{"".join(f"<li>{it}</li>" for it in items)}</ul><button onclick="wa(\'{en}\')">Book</button></div>'
        for (en, ar, price, items) in services)
    pkgs = "".join(
        f'<div class="pcard"><h3>{en}</h3><div class="ar">{ar}</div><div class="pp">{price}<small> KD</small></div>'
        f'<p>{desc}</p><button onclick="wa(\'{en}\')">Book Package</button></div>'
        for (en, ar, price, desc) in packages)
    team_h = "".join(
        f'<div class="tcard"><img src="{img}"><h3>{n}</h3><div class="ar">{ar}</div><p>{role}</p></div>'
        for (n, role, ar, img) in team)
    gal = "".join(f'<img src="{g}" alt="">' for g in gallery_imgs)
    revs = "".join(f'<div class="t"><b>{who}</b> — {txt}</div>' for (who, txt) in reviews)
    opts = "".join(f'<option value="{en} ({price} KD)">{en} — {price} KD</option>' for (en, ar, price, items) in services)
    js = BOOK_JS.replace("{NAME}", name_en).replace("{WA}", phone)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name_en} — Luxury Beauty Salon {area}, Kuwait</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>{ADV_CSS}</style></head>
<body>
<nav class="sticky"><span class="brand">{name_en}</span>
<a class="btn btn-gold" href="{wa_url}">BOOK NOW</a>
<button class="ham" id="ham"><span></span><span></span><span></span></button></nav>
<header class="hero"><canvas id="glow"></canvas>
<span class="tag">Luxury Beauty · {area}, Kuwait</span>
<h1>{name_en.upper()}</h1>
<p class="sub">A sanctuary of feminine refinement. Hair, skin, nails & bridal — crafted with love in {area}.</p>
<a class="btn btn-rose" href="{wa_url}">BOOK AN APPOINTMENT</a>
</header>
<section class="section"><div class="eyebrow">OUR SERVICES</div><h2>Signature Treatments</h2>
<p class="eyebrow">خدماتنا · priced in Kuwaiti Dinar</p><div class="sgrid">{svc}</div></section>
<section class="section alt"><div class="eyebrow">GALLERY</div><h2>A Glimpse of {name_en}</h2><div class="gal">{gal}</div></section>
<section class="section"><div class="eyebrow">OUR TEAM</div><h2>Meet the Artists</h2><div class="tgrid">{team_h}</div></section>
<section class="section alt"><div class="eyebrow">PACKAGES</div><h2>Curated Experiences</h2><div class="pgrid">{pkgs}</div></section>
<section class="section"><div class="eyebrow">REVIEWS</div><h2>What Clients Say</h2><div class="testi">{revs}</div></section>
<section class="section alt" id="book"><div class="eyebrow">BOOK</div><h2>Reserve Your Moment</h2>
<div class="book"><input id="bn" placeholder="Your Name"><input id="bp" placeholder="Phone (WhatsApp)">
<select id="bs">{opts}</select><input id="bd" type="date"><input id="bt" type="time">
<textarea id="bm" placeholder="Note (optional)"></textarea><button onclick="sendBook()">Request Booking</button></div></section>
<footer>{name_en} · Beauty Salon · {area}, Kuwait · Built by KB Rewaq Digital</footer>
<a class="wa-float" href="{wa_url}">💬 WhatsApp Booking</a>
{HERO_JS}
{js}
</body></html>"""

# Canvas hero glow animation (lightweight, mobile-safe)
HERO_JS = """
<script>
const c=document.getElementById('glow');if(c){const x=c.getContext('2d');
function sz(){c.width=innerWidth;c.height=innerHeight;}sz();addEventListener('resize',sz);
let ps=[];for(let i=0;i<40;i++)ps.push({x:Math.random()*innerWidth,y:Math.random()*innerHeight,
r:Math.random()*2+0.5,vy:Math.random()*0.4+0.1,o:Math.random()*0.5+0.2});
function f(){x.clearRect(0,0,c.width,c.height);
for(const p of ps){p.y-=p.vy;if(p.y<0)p.y=c.height;
x.beginPath();x.arc(p.x,p.y,p.r,0,7);x.fillStyle='rgba(201,169,110,'+p.o+')';x.fill();}
requestAnimationFrame(f);}f();}
</script>
"""

def render_gloss(name_en, name_ar, area, phone, wa_url, services, ig, address):
    ph = "".join(f'<div class="ph"></div>' for _ in range(6))
    svc = "".join(f'<div class="card"><h3>{s}</h3><p>Premium treatment tailored for you.</p></div>' for s in (services or ["Hair","Nails","Skin","Makeup"]))
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name_en} — Luxury Beauty Salon {area}, Kuwait</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>{GLOSS_CSS}</style></head>
<body>
<div class="sticky"><span class="brand">{name_en}</span>
<a class="btn btn-gold" href="{wa_url}">BOOK NOW</a></div>
<header class="hero"><canvas id="glow"></canvas>
<span class="tag">Luxury Beauty · {area}, Kuwait</span>
<h1>{name_en.upper()}</h1>
<p class="sub">A sanctuary of feminine refinement. Where every detail is designed around you.</p>
<a class="btn btn-rose" href="{wa_url}">BOOK AN APPOINTMENT</a>
</header>
<section class="section"><div class="eyebrow">SIGNATURE EXPERIENCES</div>
<h2>Our most beloved services</h2><div class="cards">{svc}</div></section>
<section class="section alt"><div class="eyebrow">A GLIMPSE</div>
<h2>A glimpse of {name_en}</h2><div class="gallery">{ph}</div></section>
<section class="section"><div class="eyebrow">REVIEWS</div>
<h2>What our clients say</h2><div class="reviews">
<div class="review"><p>"Absolutely the best experience in Kuwait. Elegant, calm, professional."</p><div class="who">— Happy Client</div></div>
<div class="review"><p>"They made me feel beautiful. Will come back every week."</p><div class="who">— Regular Visitor</div></div>
</div></section>
<section class="section insta"><h2>Find us on Instagram</h2>
<p><a href="https://instagram.com/{ig}">@{ig}</a></p></section>
<section class="section contact"><div class="eyebrow">VISIT US</div>
<h2>{name_en}</h2>
<p>{address or area+', Kuwait'}</p>
<p><a href="tel:+{phone}">+{phone}</a> · <a href="{wa_url}">WhatsApp Us</a></p>
<p>Daily 10 AM – 10 PM</p></section>
<footer>{name_en} · Beauty Salon · {area}, Kuwait · Built by KB Rewaq Digital</footer>
<a class="fab" href="{wa_url}">💬 WhatsApp</a>
{HERO_JS}
</body></html>"""

