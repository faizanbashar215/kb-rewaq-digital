#!/usr/bin/env python3
"""KB Rewaq v2 — WOW salon website generator.
Luxury aesthetic: full-screen gradient hero, gold/blush palette,
CSS 3D depth, scroll-reveal animations, floating particles, bilingual AR/EN,
booking form -> WhatsApp. No techy wireframes.
"""
import os

LEADS = [
    {"slug":"midyaf","dir":"leads-sites/midyaf","name_en":"Midyaf Beauty Salon","name_ar":"صالون ميدياف للتجميل",
     "phone":"96541065562","phone_disp":"+965 4106 5562","area_en":"Salmiya, Block 9","area_ar":"السالمية، القطعة 9",
     "tag_en":"Where Elegance Meets Expertise","tag_ar":"حيث يلتقي الأناقة بالخبرة","c1":"#e8b4d4","c2":"#c77dff","c3":"#fff0f7",
     "services":[("Hair Styling & Color","تصفيف وصبغ الشعر","Expert cuts, balayage, keratin & bridal hair."),
                 ("Facial & Skin Care","العناية بالبشرة","Hydrafacial, gold facial, deep cleansing."),
                 ("Nails & Manicure","الأظافر والمانيكير","Gel, acrylic, nail art & pedicure."),
                 ("Bridal Packages","باقات العرائس","Full bridal makeup + trial + day styling.")]},
    {"slug":"looknoor","dir":"leads-sites/looknoor","name_en":"Look Noor Ladies Beauty Salon","name_ar":"صالون لوك نور للسيدات",
     "phone":"96560748354","phone_disp":"+965 6074 8354","area_en":"Salmiya, Block 12","area_ar":"السالمية، القطعة 12",
     "tag_en":"Your Beauty, Our Passion","tag_ar":"جمالك، شغفنا","c1":"#ffd6a5","c2":"#ff8fab","c3":"#fff7ed",
     "services":[("Hair Treatment","علاج الشعر","Protein, keratin, hair spa & extensions."),
                 ("Makeup & Beauty","المكياج والتجميل","Party, evening & natural everyday looks."),
                 ("Facial & Cleanup","تنظيف الوجه","Glow facials, threading, waxing."),
                 ("Spa & Relaxation","سبا والاسترخاء","Full-body massage & wellness rituals.")]},
    {"slug":"monya","dir":"leads-sites/monya","name_en":"Monya Ladies Beauty Salon","name_ar":"صالون منى للسيدات",
     "phone":"96598980970","phone_disp":"+965 9898 0970","area_en":"Salmiya, Block 10","area_ar":"السالمية، القطعة 10",
     "tag_en":"Summer Glow, All Year Round","tag_ar":"إشراق الصيف، طوال العام","c1":"#a0e7e5","c2":"#b4f8c8","c3":"#f0fffe",
     "services":[("Haircut & Styling","قص وتصفيف","Trend cuts, blow-dry, curls & straightening."),
                 ("Facial & Cleanup","تنظيف البشرة","Summer specials, brightening facials."),
                 ("Nails & Pedicure","أظافر وباديكير","Gel polish, nail art, foot care."),
                 ("Bridal & Events","عرائس ومناسبات","Complete makeover for your big day.")]},
    {"slug":"royaljasmine","dir":"leads-sites/royaljasmine","name_en":"Royal Jasmine Salon","name_ar":"صالون الياسمين الملكي",
     "phone":"96561114586","phone_disp":"+965 6111 4586","area_en":"Salmiya, Block 10","area_ar":"السالمية، القطعة 10",
     "tag_en":"Royal Care for Royal You","tag_ar":"عناية ملكية لملوكتك","c1":"#cdb4db","c2":"#ffc8dd","c3":"#faf0ff",
     "services":[("Hair & Color","الشعر والصبغ","Royal balayage, ombre, root touch-up."),
                 ("Skin & Facial","البشرة والوجه","Anti-aging, hydra, gold facial."),
                 ("Nails & Art","الأظافر والفن","Luxury manicure, 3D nail art."),
                 ("Spa Day","يوم سبا","Massage, scrub, full relaxation.")]},
    {"slug":"larene","dir":"leads-sites/larene","name_en":"Larene Beauty Salon & Spa","name_ar":"صالون ومنتجع لارين للتجميل",
     "phone":"96551746804","phone_disp":"+965 5174 6804","area_en":"Hawally, Block 8","area_ar":"حولي، القطعة 8",
     "tag_en":"Beauty, Wellness & Beyond","tag_ar":"الجمال والعافية وأكثر","c1":"#bde0fe","c2":"#a2d2ff","c3":"#f0f8ff",
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
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;700&family=Poppins:wght@300;400;600&family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--c1:{c1};--c2:{c2};--c3:{c3};}}
*{margin:0;padding:0;box-sizing:border-box}
html{{scroll-behavior:smooth}}
body{{font-family:'Poppins',sans-serif;background:#1a1016;color:#fff;overflow-x:hidden}}
.ar{{font-family:'Tajawal',sans-serif}}
/* particles */
#petals{{position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden}}
.petal{{position:absolute;width:14px;height:14px;background:radial-gradient(circle,var(--c1),transparent);border-radius:50%;opacity:.5;animation:float linear infinite}}
@keyframes float{{0%{{transform:translateY(-10vh) scale(.6);opacity:0}}10%{{opacity:.6}}100%{{transform:translateY(110vh) scale(1.2);opacity:0}}}}
/* nav */
nav{{position:fixed;top:0;width:100%;z-index:50;display:flex;justify-content:space-between;align-items:center;padding:20px 6%;transition:.4s;backdrop-filter:blur(0px)}}
nav.scrolled{{background:rgba(26,16,22,.8);backdrop-filter:blur(14px);padding:14px 6%}}
.logo{{font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:700;background:linear-gradient(90deg,var(--c1),var(--c2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.nav-links a{{color:#fff;text-decoration:none;margin-left:26px;font-size:.95rem;opacity:.85;transition:.3s}}
.nav-links a:hover{{opacity:1;color:var(--c1)}}
/* hero */
.hero{{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 20px}}
.hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,{c1}33,transparent 55%),radial-gradient(circle at 75% 70%,{c2}33,transparent 55%),linear-gradient(160deg,#2a1620,#120a10);z-index:-2}}
.hero::after{{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Ctext x='10' y='40' font-size='30' opacity='.04'%3E%E2%9C%A6%3C/text%3E%3C/svg%3E") repeat;z-index:-1;opacity:.5}}
.hero-content{{transform:translateZ(0);animation:rise 1.2s ease-out}}
@keyframes rise{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:translateY(0)}}}}
.badge{{display:inline-block;padding:8px 22px;border:1px solid var(--c1);border-radius:40px;font-size:.8rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:24px;color:var(--c1)}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(3rem,8vw,6.5rem);font-weight:700;line-height:1;background:linear-gradient(120deg,#fff,var(--c1),var(--c2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.hero .ar{{font-size:clamp(1.8rem,4vw,3rem);color:var(--c1);margin-top:8px;font-weight:700}}
.hero p{{margin-top:20px;font-size:1.2rem;opacity:.9;max-width:560px;font-weight:300}}
.cta{{margin-top:38px;display:flex;gap:18px;flex-wrap:wrap;justify-content:center}}
.btn{{padding:16px 38px;border-radius:50px;font-weight:600;font-size:1.05rem;text-decoration:none;transition:.4s;cursor:pointer;border:none}}
.btn.primary{{background:linear-gradient(90deg,var(--c1),var(--c2));color:#1a1016;box-shadow:0 10px 40px {c1}55}}
.btn.ghost{{background:transparent;color:#fff;border:2px solid var(--c1)}}
.btn:hover{{transform:translateY(-4px) scale(1.03);box-shadow:0 16px 50px {c2}77}}
/* sections */
section{{position:relative;z-index:2;padding:100px 6%}}
.sec-title{{text-align:center;margin-bottom:60px}}
.sec-title .eyebrow{{color:var(--c1);letter-spacing:3px;text-transform:uppercase;font-size:.85rem}}
.sec-title h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.5rem);font-weight:700;margin:8px 0 4px}}
.sec-title .ar{{color:var(--c2);font-size:1.5rem}}
.reveal{{opacity:0;transform:translateY(50px);transition:.9s cubic-bezier(.2,.8,.2,1)}}
.reveal.show{{opacity:1;transform:translateY(0)}}
/* services */
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:26px;max-width:1100px;margin:0 auto}}
.card{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:36px 28px;transition:.5s;position:relative;overflow:hidden}}
.card::before{{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,var(--c1)22,transparent 60%);opacity:0;transition:.5s}}
.card:hover::before{{opacity:1}}
.card:hover{{transform:translateY(-10px);border-color:var(--c1)}}
.card .num{{font-family:'Cormorant Garamond',serif;font-size:2.5rem;color:var(--c1);opacity:.4}}
.card h3{{font-size:1.3rem;margin:10px 0 4px;position:relative}}
.card .ar{{color:var(--c2);font-size:1rem;margin-bottom:12px;position:relative}}
.card p{{opacity:.75;font-size:.92rem;line-height:1.6;position:relative}}
/* about */
.about-wrap{{display:grid;grid-template-columns:1fr 1fr;gap:50px;max-width:1000px;margin:0 auto;align-items:center}}
.about-card{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:24px;padding:40px}}
.info-row{{display:flex;gap:16px;align-items:center;margin:18px 0;font-size:1.1rem}}
.info-row span{{font-size:1.6rem}}
.info-row a{{color:var(--c1);text-decoration:none}}
.visual{{height:340px;border-radius:24px;background:radial-gradient(circle at 40% 30%,var(--c1),var(--c2));position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center}}
.visual::after{{content:'✿';font-size:9rem;color:rgba(255,255,255,.25)}}
/* booking */
.book-wrap{{max-width:560px;margin:0 auto;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:26px;padding:44px}}
.book-wrap input,.book-wrap textarea{{width:100%;padding:16px 20px;border-radius:16px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.05);color:#fff;font-size:1rem;margin-bottom:16px;font-family:'Poppins',sans-serif}}
.book-wrap input:focus,.book-wrap textarea:focus{{outline:none;border-color:var(--c1)}}
.book-wrap .btn{{width:100%}}
footer{{text-align:center;padding:50px 20px;opacity:.55;font-size:.9rem;position:relative;z-index:2}}
.wa-float{{position:fixed;bottom:26px;right:26px;z-index:60;background:linear-gradient(90deg,#25D366,#128C7E);color:#fff;padding:16px 24px;border-radius:50px;text-decoration:none;font-weight:600;display:flex;align-items:center;gap:10px;box-shadow:0 10px 36px rgba(37,211,102,.5);transition:.3s}}
.wa-float:hover{{transform:scale(1.06)}}
@media(max-width:760px){{.about-wrap{{grid-template-columns:1fr}}.nav-links{{display:none}}}}
</style>
</head>
<body>
<div id="petals"></div>
<nav id="nav"><div class="logo">{name_en}</div><div class="nav-links"><a href="#services">Services</a><a href="#about">About</a><a href="#book">Book</a></div></nav>

<header class="hero">
  <div class="hero-content">
    <span class="badge">Premium Salon · Kuwait</span>
    <h1>{name_en}</h1>
    <div class="ar">{name_ar}</div>
    <p>{tag_en} — {tag_ar}</p>
    <div class="cta">
      <a href="#book" class="btn primary">Book Appointment · احجزي موعدك</a>
      <a href="https://wa.me/{phone}" class="btn ghost">WhatsApp · واتساب</a>
    </div>
  </div>
</header>

<section id="services">
  <div class="sec-title reveal"><div class="eyebrow">What We Offer</div><h2>Our Services</h2><div class="ar">خدماتنا</div></div>
  <div class="grid">
    {services_html}
  </div>
</section>

<section id="about">
  <div class="sec-title reveal"><div class="eyebrow">Visit Us</div><h2>Where To Find Us</h2><div class="ar">زورونا</div></div>
  <div class="about-wrap reveal">
    <div class="about-card">
      <div class="info-row"><span>📍</span><div><b>Location</b><br>{area_en}<br><span class="ar">{area_ar}</span></div></div>
      <div class="info-row"><span>📞</span><div><b>Phone / واتساب</b><br><a href="https://wa.me/{phone}">{phone_disp}</a></div></div>
      <div class="info-row"><span>🕐</span><div><b>Hours</b><br>Daily 10AM–9PM · Fri 2PM–9PM</div></div>
    </div>
    <div class="visual"></div>
  </div>
</section>

<section id="book">
  <div class="sec-title reveal"><div class="eyebrow">Get In Touch</div><h2>Book Your Visit</h2><div class="ar">احجزي زيارتك</div></div>
  <div class="book-wrap reveal">
    <form onsubmit="return bookWa(event)">
      <input id="bname" placeholder="Your Name / اسمك" required>
      <input id="bservice" placeholder="Service / الخدمة" required>
      <input id="bdate" type="date" required>
      <textarea id="bnote" placeholder="Message / رسالتك" rows="3"></textarea>
      <button class="btn primary" type="submit">Send via WhatsApp · أرسلي عبر واتساب</button>
    </form>
  </div>
</section>

<footer>© {name_en} · Designed by KB Rewaq Digital · +965 50703252</footer>
<a href="https://wa.me/{phone}" class="wa-float">💬 WhatsApp Booking</a>

<script>
// floating petals
const pc=document.getElementById('petals');
for(let i=0;i<24;i++){{const p=document.createElement('div');p.className='petal';
p.style.left=Math.random()*100+'vw';p.style.animationDuration=(8+Math.random()*10)+'s';
p.style.animationDelay=(Math.random()*8)+'s';p.style.transform='scale('+(.5+Math.random())+')';pc.appendChild(p);}}
// nav scroll
addEventListener('scroll',()=>{{document.getElementById('nav').classList.toggle('scrolled',scrollY>50)}});
// reveal on scroll
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting)e.target.classList.add('show')}}),{{threshold:.15}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
function bookWa(e){{e.preventDefault();const n=bname.value,s=bservice.value,d=bdate.value,m=bnote.value;
const t=encodeURIComponent('Hello {name_en}! I want to book:\\nName: '+n+'\\nService: '+s+'\\nDate: '+d+'\\nNote: '+m);
window.open('https://wa.me/{phone}?text='+t,'_blank');}}
</script>
</body></html>"""

def gen(l):
    svcs=""
    for i,(en,ar,desc) in enumerate(l["services"],1):
        svcs+=f'<div class="card reveal"><div class="num">0{i}</div><h3>{en}</h3><div class="ar">{ar}</div><p>{desc}</p></div>\n'
    h=TPL
    for k,v in {"{name_en}":l["name_en"],"{name_ar}":l["name_ar"],"{phone}":l["phone"],
        "{phone_disp}":l["phone_disp"],"{area_en}":l["area_en"],"{area_ar}":l["area_ar"],
        "{tag_en}":l["tag_en"],"{tag_ar}":l["tag_ar"],"{c1}":l["c1"],"{c2}":l["c2"],"{c3}":l["c3"],
        "{services_html}":svcs}.items():
        h=h.replace(k,v)
    h=h.replace("{{","{").replace("}}","}")  # strip literal CSS/JS braces
    os.makedirs(l["dir"],exist_ok=True)
    open(f'{l["dir"]}/index.html','w',encoding='utf-8').write(h)
    print(f'✅ {l["name_en"]}')

if __name__=="__main__":
    for l in LEADS: gen(l)
    print("v2 wow-sites done")
