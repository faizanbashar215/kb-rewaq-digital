#!/usr/bin/env python3
"""KB Rewaq — 3D Professional Salon Website Generator.
Generates a premium, 3D-style bilingual (AR/EN) site per lead.
Three.js (CDN) for animated 3D hero. Public-host ready.
"""
import json, os

LEADS = [
    {
        "slug": "midyaf", "dir": "leads-sites/midyaf",
        "name_en": "Midyaf Beauty Salon", "name_ar": "صالون ميدياف للتجميل",
        "phone": "96541065562", "phone_disp": "+965 4106 5562",
        "area_en": "Salmiya, Block 9, Sayed Yassen Al Tabtabai St", "area_ar": "السالمية، القطعة 9، شارع سيد ياسين الطبطبائي",
        "tagline_en": "Where Elegance Meets Expertise", "tagline_ar": "حيث يلتقي الأناقة بالخبرة",
        "accent": "#e8b4d4", "accent2": "#c77dff",
        "services": [
            ("Hair Styling & Color", "تصفيف وصبغ الشعر", "Expert cuts, balayage, keratin & bridal hair."),
            ("Facial & Skin Care", "العناية بالبشرة والوجه", "Hydrafacial, gold facial, deep cleansing."),
            ("Nails & Manicure", "الأظافر والمانيكير", "Gel, acrylic, nail art & pedicure."),
            ("Bridal Packages", "باقات العرائس", "Full bridal makeup + trial + day-of styling."),
        ],
    },
    {
        "slug": "looknoor", "dir": "leads-sites/looknoor",
        "name_en": "Look Noor Ladies Beauty Salon", "name_ar": "صالون لوك نور للسيدات",
        "phone": "96560748354", "phone_disp": "+965 6074 8354",
        "area_en": "Salmiya, Block 12", "area_ar": "السالمية، القطعة 12",
        "tagline_en": "Your Beauty, Our Passion", "tagline_ar": "جمالك، شغفنا",
        "accent": "#ffd6a5", "accent2": "#ff8fab",
        "services": [
            ("Hair Treatment", "علاج الشعر", "Protein, keratin, hair spa & extensions."),
            ("Makeup & Beauty", "المكياج والتجميل", "Party, evening & natural everyday looks."),
            ("Facial & Cleanup", "تنظيف وتجميل الوجه", "Glow facials, threading, waxing."),
            ("Spa & Relaxation", "سبا والاسترخاء", "Full-body massage & wellness rituals."),
        ],
    },
    {
        "slug": "monya", "dir": "leads-sites/monya",
        "name_en": "Monya Ladies Beauty Salon", "name_ar": "صالون منى للسيدات",
        "phone": "96598980970", "phone_disp": "+965 9898 0970",
        "area_en": "Salmiya, Block 10, Al Adsani St", "area_ar": "السالمية، القطعة 10، شارع العضاني",
        "tagline_en": "Summer Glow, All Year Round", "tagline_ar": "إشراق الصيف، طوال العام",
        "accent": "#a0e7e5", "accent2": "#b4f8c8",
        "services": [
            ("Haircut & Styling", "قص وتصفيف الشعر", "Trend cuts, blow-dry, curls & straightening."),
            ("Facial & Cleanup", "تنظيف البشرة", "Summer specials, brightening facials."),
            ("Nails & Pedicure", "أظافر وباديكير", "Gel polish, nail art, foot care."),
            ("Bridal & Events", "عرائس ومناسبات", "Complete makeover for your big day."),
        ],
    },
    {
        "slug": "royaljasmine", "dir": "leads-sites/royaljasmine",
        "name_en": "Royal Jasmine Salon", "name_ar": "صالون الياسمين الملكي",
        "phone": "96561114586", "phone_disp": "+965 6111 4586",
        "area_en": "Salmiya, Block 10, Al Dhahak Qays St", "area_ar": "السالمية، القطعة 10، شارع الضحاك قيس",
        "tagline_en": "Royal Care for Royal You", "tagline_ar": "عناية ملكية لملوكتك",
        "accent": "#cdb4db", "accent2": "#ffc8dd",
        "services": [
            ("Hair & Color", "الشعر والصبغ", "Royal balayage, ombre, root touch-up."),
            ("Skin & Facial", "البشرة والوجه", "Anti-aging, hydra, gold facial."),
            ("Nails & Art", "الأظافر والفن", "Luxury manicure, 3D nail art."),
            ("Spa Day", "يوم سبا", "Massage, scrub, full relaxation."),
        ],
    },
    {
        "slug": "larene", "dir": "leads-sites/larene",
        "name_en": "Larene Beauty Salon & Spa", "name_ar": "صالون ومنتجع لارين للتجميل",
        "phone": "96551746804", "phone_disp": "+965 5174 6804",
        "area_en": "Hawally, Block 8, Mohammed Ali Al-Dokhan St", "area_ar": "حولي، القطعة 8، شارع محمد علي الدخان",
        "tagline_en": "Beauty, Wellness & Beyond", "tagline_ar": "الجمال والعافية وأكثر",
        "accent": "#bde0fe", "accent2": "#a2d2ff",
        "services": [
            ("Hair & Spa", "الشعر والسبا", "Cut, color, treatment & hair spa."),
            ("Skin Care", "العناية بالبشرة", "Facials, peels, glow therapy."),
            ("Nails & Beauty", "الأظافر والتجميل", "Manicure, pedicure, makeup."),
            ("Wellness", "العافية", "Massage, relaxation & body care."),
        ],
    },
]

TPL = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name_en} | {name_ar}</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Tahoma,Arial,sans-serif}
  :root{--a:{accent};--b:{accent2}}
  body{background:#0d0b1a;color:#fff;overflow-x:hidden}
  #hero-canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1}
  .wrap{max-width:1100px;margin:0 auto;padding:0 20px}
  header{display:flex;justify-content:space-between;align-items:center;padding:22px 0;position:relative;z-index:5}
  .logo{font-size:1.5rem;font-weight:800;background:linear-gradient(90deg,var(--a),var(--b));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  nav a{color:#fff;text-decoration:none;margin-left:22px;font-size:.95rem;opacity:.85}
  nav a:hover{opacity:1}
  .hero{min-height:88vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;position:relative;z-index:5}
  .hero h1{font-size:clamp(2.5rem,6vw,5rem);font-weight:900;line-height:1.05;background:linear-gradient(120deg,#fff,var(--a));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
  .hero .ar{font-size:clamp(1.6rem,4vw,3rem);color:var(--b);margin-top:10px;font-weight:700}
  .hero p{margin-top:18px;font-size:1.15rem;opacity:.9;max-width:600px}
  .cta{margin-top:34px;display:flex;gap:16px;flex-wrap:wrap;justify-content:center}
  .btn{padding:15px 34px;border-radius:50px;font-weight:700;font-size:1rem;text-decoration:none;transition:.3s;border:2px solid var(--a)}
  .btn.primary{background:linear-gradient(90deg,var(--a),var(--b));color:#0d0b1a;border:none;box-shadow:0 8px 30px rgba(199,125,255,.4)}
  .btn.ghost{color:#fff}
  .btn:hover{transform:translateY(-3px);box-shadow:0 12px 40px rgba(199,125,255,.6)}
  section{position:relative;z-index:5;padding:80px 0}
  .glass{background:rgba(255,255,255,.06);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.12);border-radius:24px;padding:40px;margin:20px 0}
  h2{font-size:2.2rem;margin-bottom:10px}
  h2 .ar{color:var(--b);font-size:1.5rem;display:block;margin-top:4px}
  .sub{opacity:.7;margin-bottom:30px}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px}
  .card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:28px;transition:.3s}
  .card:hover{transform:translateY(-6px);border-color:var(--a);background:rgba(255,255,255,.1)}
  .card h3{font-size:1.2rem;margin-bottom:6px}
  .card .ar{color:var(--b);font-size:.95rem;margin-bottom:10px}
  .card p{opacity:.75;font-size:.9rem;line-height:1.5}
  .info-row{display:flex;gap:14px;align-items:center;margin:14px 0;font-size:1.05rem}
  .info-row span{font-size:1.4rem}
  .book{display:flex;flex-direction:column;gap:14px;max-width:500px;margin:0 auto}
  .book input,.book textarea{width:100%;padding:14px 18px;border-radius:14px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.06);color:#fff;font-size:1rem}
  .book input:focus,.book textarea:focus{outline:none;border-color:var(--a)}
  .wa-float{position:fixed;bottom:24px;right:24px;z-index:20;background:linear-gradient(90deg,#25D366,#128C7E);color:#fff;padding:16px 22px;border-radius:50px;text-decoration:none;font-weight:700;box-shadow:0 8px 30px rgba(37,211,102,.5);display:flex;align-items:center;gap:10px}
  .wa-float:hover{transform:scale(1.05)}
  footer{text-align:center;padding:40px 0;opacity:.6;font-size:.9rem;position:relative;z-index:5}
  .badge{display:inline-block;background:linear-gradient(90deg,var(--a),var(--b));color:#0d0b1a;padding:6px 16px;border-radius:30px;font-size:.8rem;font-weight:700;margin-bottom:20px}
</style>
</head>
<body>
<canvas id="hero-canvas"></canvas>
<header class="wrap">
  <div class="logo">{name_en}</div>
  <nav><a href="#services">Services</a><a href="#about">About</a><a href="#book">Book</a></nav>
</header>

<div class="hero wrap">
  <div class="badge">PREMIUM SALON · Kuwait</div>
  <h1>{name_en}</h1>
  <div class="ar">{name_ar}</div>
  <p>{tagline_en} — {tagline_ar}</p>
  <div class="cta">
    <a href="#book" class="btn primary">Book Appointment · احجزي موعدك</a>
    <a href="https://wa.me/{phone}" class="btn ghost">WhatsApp · واتساب</a>
  </div>
</div>

<section id="services" class="wrap">
  <div class="glass">
    <h2>Our Services<span class="ar">خدماتنا</span></h2>
    <p class="sub">Professional beauty care crafted for you.</p>
    <div class="grid">
      {services_html}
    </div>
  </div>
</section>

<section id="about" class="wrap">
  <div class="glass">
    <h2>Visit Us<span class="ar">زورونا</span></h2>
    <div class="info-row"><span>📍</span><div><b>Location</b><br>{area_en}<br>{area_ar}</div></div>
    <div class="info-row"><span>📞</span><div><b>Phone / واتساب</b><br><a href="https://wa.me/{phone}" style="color:var(--a);text-decoration:none">{phone_disp}</a></div></div>
    <div class="info-row"><span>🕐</span><div><b>Hours</b><br>Daily 10:00 AM – 9:00 PM (Fri 2:00 PM – 9:00 PM)</div></div>
  </div>
</section>

<section id="book" class="wrap">
  <div class="glass">
    <h2>Book Your Visit<span class="ar">احجزي زيارتك</span></h2>
    <p class="sub">Fill the form or tap WhatsApp — we reply within minutes.</p>
    <form class="book" onsubmit="return bookWa(event)">
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

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
// 3D animated hero
const scene=new THREE.Scene();
const cam=new THREE.PerspectiveCamera(75,innerWidth/innerHeight,0.1,1000);
const rend=new THREE.WebGLRenderer({canvas:document.getElementById('hero-canvas'),alpha:true,antialias:true});
rend.setSize(innerWidth,innerHeight);rend.setPixelRatio(Math.min(devicePixelRatio,2));
const geo=new THREE.IcosahedronGeometry(2.2,1);
const mat=new THREE.MeshStandardMaterial({color:0xffffff,wireframe:true,emissive:0xc77dff,emissiveIntensity:.4});
const mesh=new THREE.Mesh(geo,mat);scene.add(mesh);
const g2=new THREE.TorusGeometry(3.4,0.05,16,100);
const m2=new THREE.MeshStandardMaterial({color:0xe8b4d4,wireframe:true});
const ring=new THREE.Mesh(g2,m2);scene.add(ring);
scene.add(new THREE.AmbientLight(0xffffff,.6));
const pl=new THREE.PointLight(0xc77dff,2);pl.position.set(5,5,5);scene.add(pl);
const pl2=new THREE.PointLight(0xe8b4d4,2);pl2.position.set(-5,-5,5);scene.add(pl2);
cam.position.z=7;
const pts=[];
for(let i=0;i<400;i++){const g=new THREE.BufferGeometry();const r=Math.random()*1.5;const th=Math.random()*Math.PI*2;const ph=Math.acos(2*Math.random()-1);g.setAttribute('position',new THREE.Float32BufferAttribute([r*Math.sin(ph)*Math.cos(th),r*Math.sin(ph)*Math.sin(th),r*Math.cos(ph)],3));const p=new THREE.Points(g,new THREE.PointsMaterial({color:0xffffff,size:0.04}));pts.push(p);scene.add(p);}
function anim(){requestAnimationFrame(anim);mesh.rotation.x+=0.004;mesh.rotation.y+=0.006;ring.rotation.z+=0.003;pts.forEach((p,i)=>{p.rotation.y+=0.001*(i%3+1)});rend.render(scene,cam);}
anim();
addEventListener('resize',()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();rend.setSize(innerWidth,innerHeight);});
function bookWa(e){e.preventDefault();const n=document.getElementById('bname').value;const s=document.getElementById('bservice').value;const d=document.getElementById('bdate').value;const m=document.getElementById('bnote').value;const txt=encodeURIComponent('Hello {name_en}! I want to book:\\nName: '+n+'\\nService: '+s+'\\nDate: '+d+'\\nNote: '+m);window.open('https://wa.me/{phone}?text='+txt,'_blank');}
</script>
</body></html>"""

def gen(lead):
    svcs = ""
    for en, ar, desc in lead["services"]:
        svcs += f'<div class="card"><h3>{en}</h3><div class="ar">{ar}</div><p>{desc}</p></div>\n'
    html = TPL
    repl = {
        "{name_en}": lead["name_en"], "{name_ar}": lead["name_ar"], "{phone}": lead["phone"],
        "{phone_disp}": lead["phone_disp"], "{area_en}": lead["area_en"], "{area_ar}": lead["area_ar"],
        "{tagline_en}": lead["tagline_en"], "{tagline_ar}": lead["tagline_ar"],
        "{accent}": lead["accent"], "{accent2}": lead["accent2"], "{services_html}": svcs,
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    os.makedirs(lead["dir"], exist_ok=True)
    with open(f'{lead["dir"]}/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✅ {lead["name_en"]} -> {lead["dir"]}/index.html')

if __name__ == "__main__":
    for l in LEADS:
        gen(l)
    print("\nAll 5 sites generated.")
