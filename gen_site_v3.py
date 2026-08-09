#!/usr/bin/env python3
"""KB Rewaq v3 — CINEMATIC salon website.
Real Unsplash beauty imagery + GSAP scroll cinematics + editorial luxury.
Target: 10/10 wow. Each client gets own name/area/services/color + shared image pool.
"""
import os, json

IMG = [
    "https://images.unsplash.com/photo-1522337660859-02fbefca4702?w=1600&q=80",
    "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=1600&q=80",
    "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=1600&q=80",
    "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=1600&q=80",
    "https://images.unsplash.com/photo-1457972729786-0411a3b2b626?w=1600&q=80",
    "https://images.unsplash.com/photo-1571875257727-256c39da42af?w=1600&q=80",
]

LEADS = [
    {"slug":"midyaf","dir":"leads-sites/midyaf","name_en":"Midyaf Beauty Salon","name_ar":"صالون ميدياف للتجميل",
     "phone":"96541065562","phone_disp":"+965 4106 5562","area_en":"Salmiya, Block 9","area_ar":"السالمية، القطعة 9",
     "tag_en":"Where Elegance Meets Expertise","tag_ar":"حيث يلتقي الأناقة بالخبرة","accent":"#e8b4d4",
     "services":[("Hair Styling & Color","تصفيف وصبغ الشعر","Expert cuts, balayage, keratin & bridal hair."),
                 ("Facial & Skin Care","العناية بالبشرة","Hydrafacial, gold facial, deep cleansing."),
                 ("Nails & Manicure","الأظافر والمانيكير","Gel, acrylic, nail art & pedicure."),
                 ("Bridal Packages","باقات العرائس","Full bridal makeup + trial + day styling.")]},
    {"slug":"looknoor","dir":"leads-sites/looknoor","name_en":"Look Noor Ladies Beauty Salon","name_ar":"صالون لوك نور للسيدات",
     "phone":"96560748354","phone_disp":"+965 6074 8354","area_en":"Salmiya, Block 12","area_ar":"السالمية، القطعة 12",
     "tag_en":"Your Beauty, Our Passion","tag_ar":"جمالك، شغفنا","accent":"#ffd6a5",
     "services":[("Hair Treatment","علاج الشعر","Protein, keratin, hair spa & extensions."),
                 ("Makeup & Beauty","المكياج والتجميل","Party, evening & natural everyday looks."),
                 ("Facial & Cleanup","تنظيف الوجه","Glow facials, threading, waxing."),
                 ("Spa & Relaxation","سبا والاسترخاء","Full-body massage & wellness rituals.")]},
    {"slug":"monya","dir":"leads-sites/monya","name_en":"Monya Ladies Beauty Salon","name_ar":"صالون منى للسيدات",
     "phone":"96598980970","phone_disp":"+965 9898 0970","area_en":"Salmiya, Block 10","area_ar":"السالمية، القطعة 10",
     "tag_en":"Summer Glow, All Year Round","tag_ar":"إشراق الصيف، طوال العام","accent":"#a0e7e5",
     "services":[("Haircut & Styling","قص وتصفيف","Trend cuts, blow-dry, curls & straightening."),
                 ("Facial & Cleanup","تنظيف البشرة","Summer specials, brightening facials."),
                 ("Nails & Pedicure","أظافر وباديكير","Gel polish, nail art, foot care."),
                 ("Bridal & Events","عرائس ومناسبات","Complete makeover for your big day.")]},
    {"slug":"royaljasmine","dir":"leads-sites/royaljasmine","name_en":"Royal Jasmine Salon","name_ar":"صالون الياسمين الملكي",
     "phone":"96561114586","phone_disp":"+965 6111 4586","area_en":"Salmiya, Block 10","area_ar":"السالمية، القطعة 10",
     "tag_en":"Royal Care for Royal You","tag_ar":"عناية ملكية لملوكتك","accent":"#cdb4db",
     "services":[("Hair & Color","الشعر والصبغ","Royal balayage, ombre, root touch-up."),
                 ("Skin & Facial","البشرة والوجه","Anti-aging, hydra, gold facial."),
                 ("Nails & Art","الأظافر والفن","Luxury manicure, 3D nail art."),
                 ("Spa Day","يوم سبا","Massage, scrub, full relaxation.")]},
    {"slug":"larene","dir":"leads-sites/larene","name_en":"Larene Beauty Salon & Spa","name_ar":"صالون ومنتجع لارين للتجميل",
     "phone":"96551746804","phone_disp":"+965 5174 6804","area_en":"Hawally, Block 8","area_ar":"حولي، القطعة 8",
     "tag_en":"Beauty, Wellness & Beyond","tag_ar":"الجمال والعافية وأكثر","accent":"#bde0fe",
     "services":[("Hair & Spa","الشعر والسبا","Cut, color, treatment & hair spa."),
                 ("Skin Care","العناية بالبشرة","Facials, peels, glow therapy."),
                 ("Nails & Beauty","الأظافر والتجميل","Manicure, pedicure, makeup."),
                 ("Wellness","العافية","Massage, relaxation & body care.")]},
]

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name_en} | {name_ar}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Poppins:wght@300;400;500;600&family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--ac:{accent};}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Poppins',sans-serif;background:#0a0a0a;color:#fff;overflow-x:hidden}}
.ar{{font-family:'Tajawal',sans-serif}}
img{{display:block;max-width:100%}}
/* nav */
nav{{position:fixed;top:0;width:100%;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:22px 6%;transition:.4s}}
nav.scrolled{{background:rgba(10,10,10,.82);backdrop-filter:blur(16px);padding:14px 6%;border-bottom:1px solid rgba(255,255,255,.06)}}
.logo{{font-family:'Cormorant Garamond',serif;font-size:1.7rem;font-weight:700;letter-spacing:.5px}}
.nav-links a{{color:#fff;text-decoration:none;margin-left:28px;font-size:.9rem;opacity:.8;transition:.3s}}
.nav-links a:hover{{opacity:1;color:var(--ac)}}
/* hero */
.hero{{position:relative;height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.hero .bgwrap{{position:absolute;inset:0;overflow:hidden}}
.hero img.bg{{position:absolute;inset:-5%;width:110%;height:110%;object-fit:cover;filter:saturate(1.05) contrast(1.05);animation:kenburns 22s ease-in-out infinite alternate}}
@keyframes kenburns{{0%{{transform:scale(1.1) translate(0,0)}}50%{{transform:scale(1.22) translate(-2%,-1%)}}100%{{transform:scale(1.15) translate(2%,1%)}}}}
.hero .bgwrap::after{{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.025) 0 1px,transparent 1px 3px);mix-blend-mode:overlay;animation:grain 1.2s steps(3) infinite;opacity:.5}}
@keyframes grain{{0%{{transform:translateY(0)}}100%{{transform:translateY(3px)}}}}
.hero .ov{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.5),rgba(10,10,10,.2) 40%,rgba(10,10,10,.85))}}
.hero .ov2{{position:absolute;inset:0;background:radial-gradient(circle at 50% 55%,transparent,rgba(10,10,10,.65))}}
.hero .hc{{position:relative;z-index:3;padding:0 20px}}
.hero .kicker{{letter-spacing:6px;text-transform:uppercase;font-size:.8rem;color:var(--ac);margin-bottom:18px;opacity:0;animation:up 1s .3s forwards}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(3.2rem,9vw,7rem);font-weight:700;line-height:1;opacity:0;animation:up 1.1s .5s forwards}}
.hero .ar{{font-size:clamp(1.6rem,4vw,3rem);color:var(--ac);margin-top:6px;font-weight:700;opacity:0;animation:up 1.1s .7s forwards}}
.hero p{{margin-top:22px;font-size:1.15rem;font-weight:300;opacity:0;animation:up 1.1s .9s forwards}}
.hero .cta{{margin-top:36px;display:flex;gap:16px;justify-content:center;flex-wrap:wrap;opacity:0;animation:up 1.1s 1.1s forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:translateY(0)}}}}
.btn{{padding:16px 38px;border-radius:50px;font-weight:600;font-size:1rem;text-decoration:none;transition:.4s;border:none;cursor:pointer}}
.btn.p{{background:var(--ac);color:#0a0a0a;box-shadow:0 10px 40px rgba(232,180,212,.35)}}
.btn.g{{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.5)}}
.btn:hover{{transform:translateY(-4px) scale(1.03)}}
.scrollind{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);z-index:3;font-size:.75rem;letter-spacing:3px;opacity:.7;animation:bob 2s infinite}}
@keyframes bob{{50%{{transform:translate(-50%,10px)}}}}
/* split */
.split{{display:grid;grid-template-columns:1fr 1fr;min-height:90vh;align-items:center}}
.split .txt{{padding:8% 8%}}
.split .txt .ey{{color:var(--ac);letter-spacing:3px;text-transform:uppercase;font-size:.8rem}}
.split .txt h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,5vw,3.4rem);font-weight:700;margin:10px 0 6px}}
.split .txt .ar{{color:var(--ac);font-size:1.3rem;margin-bottom:18px}}
.split .txt p{{opacity:.8;line-height:1.8;font-weight:300;max-width:440px}}
.split .pic{{position:relative;height:90vh;overflow:hidden}}
.split .pic img{{width:100%;height:100%;object-fit:cover;transition:transform 1.2s}}
.split.rev{{direction:rtl}}
.split.rev .txt{{direction:ltr}}
/* services */
.serv{{padding:120px 6%;background:#0d0d0d}}
.sec-t{{text-align:center;margin-bottom:70px}}
.sec-t .ey{{color:var(--ac);letter-spacing:3px;text-transform:uppercase;font-size:.8rem}}
.sec-t h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.6rem);font-weight:700}}
.sec-t .ar{{color:var(--ac);font-size:1.4rem}}
.sgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;max-width:1200px;margin:0 auto}}
.scard{{position:relative;height:380px;border-radius:18px;overflow:hidden;cursor:pointer}}
.scard img{{width:100%;height:100%;object-fit:cover;transition:transform .9s}}
.scard:hover img{{transform:scale(1.12)}}
.scard .ov{{position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(10,10,10,.92))}}
.scard .cap{{position:absolute;bottom:0;left:0;right:0;padding:24px}}
.scard .cap h3{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:700}}
.scard .cap .ar{{color:var(--ac);font-size:1rem;margin:2px 0 6px}}
.scard .cap p{{font-size:.82rem;opacity:.75;line-height:1.5}}
/* before/after */
.ba{{position:relative;max-width:900px;margin:0 auto;height:70vh;border-radius:20px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.5);opacity:1!important;transform:none!important}}
.ba img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.ba .after{{clip-path:inset(0 0 0 50%);transition:clip-path 1.1s cubic-bezier(.7,0,.2,1)}}
.ba:hover .after{{clip-path:inset(0 0 0 0)}}
.ba .lbl{{position:absolute;top:18px;padding:7px 16px;border-radius:30px;font-size:.78rem;letter-spacing:2px;text-transform:uppercase;backdrop-filter:blur(6px);background:rgba(10,10,10,.55)}}
.ba .lbl.b{{left:18px;color:var(--ac)}}
.ba .lbl.a{{right:18px}}
.ba .hint{{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);font-size:.8rem;letter-spacing:2px;opacity:.85;animation:pulse 2s infinite}}
@keyframes pulse{{50%{{opacity:.4}}}}
/* fullbleed */
.full{{position:relative;height:80vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.full img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.full .ov{{position:absolute;inset:0;background:rgba(10,10,10,.55)}}
.full .fc{{position:relative;z-index:2;padding:0 20px}}
.full .fc .ar{{color:var(--ac);font-size:clamp(1.5rem,4vw,2.6rem);font-weight:700}}
.full .fc p{{margin-top:14px;font-size:1.1rem;font-weight:300;max-width:560px;margin-left:auto;margin-right:auto}}
/* contact */
.contact{{padding:120px 6%;text-align:center;background:#0d0d0d}}
.contact .ey{{color:var(--ac);letter-spacing:3px;text-transform:uppercase;font-size:.8rem}}
.contact h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.6rem);font-weight:700;margin:10px 0}}
.contact .ar{{color:var(--ac);font-size:1.4rem;margin-bottom:30px}}
.cinfo{{display:flex;gap:40px;justify-content:center;flex-wrap:wrap;margin-bottom:36px}}
.cinfo div{{font-size:1.05rem}}
.cinfo a{{color:var(--ac);text-decoration:none}}
.book{{max-width:520px;margin:0 auto;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:34px}}
.book input,.book textarea{{width:100%;padding:14px 18px;border-radius:12px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.05);color:#fff;font-family:'Poppins',sans-serif;margin-bottom:14px;font-size:.95rem}}
.book input:focus,.book textarea:focus{{outline:none;border-color:var(--ac)}}
.book .btn{{width:100%}}
footer{{text-align:center;padding:46px 20px;opacity:.5;font-size:.85rem}}
.wa-float{{position:fixed;bottom:24px;right:24px;z-index:120;background:#25D366;color:#fff;padding:15px 22px;border-radius:50px;text-decoration:none;font-weight:600;display:flex;align-items:center;gap:9px;box-shadow:0 10px 36px rgba(37,211,102,.5);transition:.3s}}
.wa-float:hover{{transform:scale(1.06)}}
.reveal{{opacity:0;transform:translateY(60px);transition:1s cubic-bezier(.2,.8,.2,1)}}
.reveal.show{{opacity:1;transform:translateY(0)}}
/* fallback: if JS fails, show everything */
.no-js .reveal{{opacity:1!important;transform:none!important}}
@media(max-width:860px){{.split{{grid-template-columns:1fr}}.split .pic{{height:60vh}}.sgrid{{grid-template-columns:repeat(2,1fr)}}.nav-links{{display:none}}}}
</style>
</head>
<body>
<script>document.documentElement.classList.remove('no-js');document.body.classList.remove('no-js');</script>
<nav id="nav"><div class="logo">{name_en}</div><div class="nav-links"><a href="#story">Story</a><a href="#services">Services</a><a href="#contact">Contact</a></div></nav>

<header class="hero">
  <div class="bgwrap"><img class="bg" src="{IMG0}" alt=""></div>
  <div class="ov"></div><div class="ov2"></div>
  <div class="hc">
    <div class="kicker">Premium Salon · Kuwait</div>
    <h1>{name_en}</h1>
    <div class="ar">{name_ar}</div>
    <p>{tag_en} — {tag_ar}</p>
    <div class="cta">
      <a href="#contact" class="btn p">Book Appointment · احجزي موعدك</a>
      <a href="https://wa.me/{phone}" class="btn g">WhatsApp · واتساب</a>
    </div>
  </div>
  <div class="scrollind">SCROLL ↓</div>
</header>

<section class="split" id="story">
  <div class="txt reveal">
    <div class="ey">Our Craft</div>
    <h2>Beauty, Refined</h2>
    <div class="ar">جمال، بكل أناقة</div>
    <p>Step into a space where every detail is designed around you. From the first consultation to the final touch, we craft looks that feel effortless and unforgettable.</p>
  </div>
  <div class="pic"><img src="{IMG1}" alt=""></div>
</section>

<section class="split rev">
  <div class="txt reveal">
    <div class="ey">The Experience</div>
    <h2>Calm. Considered. Couture.</h2>
    <div class="ar">هدوء، عناية، فخامة</div>
    <p>Soft light, skilled hands, and a team that listens. This is more than a salon visit — it is a moment made entirely for you.</p>
  </div>
  <div class="pic"><img src="{IMG2}" alt=""></div>
</section>

<section class="serv">
  <div class="sec-t reveal"><div class="ey">What We Offer</div><h2>Our Services</h2><div class="ar">خدماتنا</div></div>
  <div class="sgrid">
    {SERVICES}
  </div>
</section>

<section class="serv" style="padding-top:0">
  <div class="sec-t reveal"><div class="ey">The Result</div><h2>Before &amp; After</h2><div class="ar">قبل وبعد</div></div>
  <div class="ba">
    <img class="before" src="{IMG2}" alt="before">
    <img class="after" src="{IMG5}" alt="after">
    <span class="lbl b">Before · قبل</span>
    <span class="lbl a">After · بعد</span>
    <span class="hint">HOVER TO REVEAL ✦</span>
  </div>
</section>

<section class="full">
  <img src="{IMG3}" alt="">
  <div class="ov"></div>
  <div class="fc reveal">
    <div class="ar">{name_ar}</div>
    <p>{tag_en} — your moment, beautifully made.</p>
  </div>
</section>

<section class="contact" id="contact">
  <div class="ey reveal">Visit Us</div>
  <h2 class="reveal">Where To Find Us</h2>
  <div class="ar reveal">{name_ar} · زورونا</div>
  <div class="cinfo reveal">
    <div>📍 {area_en}<br><span class="ar">{area_ar}</span></div>
    <div>📞 <a href="https://wa.me/{phone}">{phone_disp}</a></div>
    <div>🕐 Daily 10AM–9PM · Fri 2PM–9PM</div>
  </div>
  <div class="book reveal">
    <form onsubmit="return bookWa(event)">
      <input id="bn" placeholder="Your Name / اسمك" required>
      <input id="bs" placeholder="Service / الخدمة" required>
      <input id="bd" type="date" required>
      <textarea id="bm" placeholder="Message / رسالتك" rows="3"></textarea>
      <button class="btn p" type="submit">Send via WhatsApp · أرسلي عبر واتساب</button>
    </form>
  </div>
</section>

<footer>© {name_en} · Designed by KB Rewaq Digital · +965 50703252</footer>
<a href="https://wa.me/{phone}" class="wa-float">💬 WhatsApp Booking</a>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
if(window.gsap){{gsap.registerPlugin(ScrollTrigger);
document.querySelectorAll('.split .pic img').forEach(im=>{gsap.fromTo(im,{{scale:1.25}},{{scale:1,scrollTrigger:{{trigger:im,start:'top bottom',end:'bottom top',scrub:true}}}});});
gsap.utils.toArray('.reveal').forEach(el=>{{gsap.to(el,{{opacity:1,y:0,duration:1,ease:'power3.out',scrollTrigger:{{trigger:el,start:'top 85%'}},onStart:()=>el.classList.add('show')}});});}}
else{{document.querySelectorAll('.reveal').forEach(el=>el.classList.add('show'));}}
addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',scrollY>60));
function bookWa(e){{e.preventDefault();const n=bn.value,s=bs.value,d=bd.value,m=bm.value;
const t=encodeURIComponent('Hello {name_en}! I want to book:\\nName: '+n+'\\nService: '+s+'\\nDate: '+d+'\\nNote: '+m);
window.open('https://wa.me/{phone}?text='+t,'_blank');}}
</script>
</body></html>"""

def gen(l):
    svcs=""
    for i,(en,ar,desc) in enumerate(l["services"]):
        img=IMG[(i+3)%len(IMG)]
        svcs+=f'<div class="scard reveal"><img src="{img}" alt=""><div class="ov"></div><div class="cap"><h3>{en}</h3><div class="ar">{ar}</div><p>{desc}</p></div></div>\n'
    h=TPL
    repl={"{name_en}":l["name_en"],"{name_ar}":l["name_ar"],"{phone}":l["phone"],
        "{phone_disp}":l["phone_disp"],"{area_en}":l["area_en"],"{area_ar}":l["area_ar"],
        "{tag_en}":l["tag_en"],"{tag_ar}":l["tag_ar"],"{accent}":l["accent"],
        "{SERVICES}":svcs,
        "{IMG0}":IMG[0],"{IMG1}":IMG[1],"{IMG2}":IMG[2],"{IMG3}":IMG[3],"{IMG4}":IMG[4],"{IMG5}":IMG[5]}
    for k,v in repl.items(): h=h.replace(k,v)
    h=h.replace("{{","{").replace("}}","}")
    os.makedirs(l["dir"],exist_ok=True)
    open(f'{l["dir"]}/index.html','w',encoding='utf-8').write(h)
    print(f'OK {l["name_en"]}')

if __name__=="__main__":
    for l in LEADS: gen(l)
    print("v3 cinematic done")
