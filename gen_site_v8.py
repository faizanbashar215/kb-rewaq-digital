#!/usr/bin/env python3
"""KB Rewaq v7 — BESPOKE AI couture salon sites.
Uses FLUX-generated unique salon imagery (not stock). Owner-photo drop
auto-replaces AI art. Tier A+B alive features kept. Target 10/10 feel.
"""
import os, glob

# AI bespoke assets — PROJECT-relative (GitHub Pages project site serves at
# /kb-rewaq-digital/, so absolute "/assets/ai" would resolve to domain root and 404).
BASE = "/kb-rewaq-digital"
AI = {
 "kahi":f"{BASE}/assets/ai/hero_kahi.png",
 "mahima":f"{BASE}/assets/ai/hero_mahiba.png",
 "paulita":f"{BASE}/assets/ai/hero_paulita.png",
 "neweves":f"{BASE}/assets/ai/hero_neweves.png",
 "yours":f"{BASE}/assets/ai/hero_yours.png",
}
GAL = [f"{BASE}/assets/ai/gal_manicure.png",f"{BASE}/assets/ai/gal_hair.png",f"{BASE}/assets/ai/gal_facial.png",
       f"{BASE}/assets/ai/gal_bridal.png",f"{BASE}/assets/ai/gal_pedicure.png"]

LEADS = [
    {"slug":"kahi","name_en":"KAHI Ladies Beauty Salon","name_ar":"صالون كاهي للسيدات",
     "phone":"96550770458","phone_disp":"+965 5077 0458","area_en":"Salmiya, Block 2","area_ar":"السالمية، القطعة 2",
     "tag_en":"Luxury Beauty, Personalized","tag_ar":"جمال فاخر، شخصي","accent":"#e8b4d4","ig":"kahi_salon",
     "lat":29.3320,"lon":48.0740,"clients":164,
     "services":[("Haircut & Blowdry","قص وتصفيف",4,["Haircut","Blowdry","Style"]),
        ("Hair Color & Balayage","صبغ وبلاجاج",22,["Full color","Balayage","Root touch-up"]),
        ("Keratin / Protein","كيراتين وبروتين",18,["Keratin","Protein treatment"]),
        ("Classic Facial","تنظيف البشرة",8,["Deep cleanse","Extraction","Mask"]),
        ("Gold / Hydra Facial","فيشل ذهبي",15,["Hydradermie","Gold mask"]),
        ("Gel Manicure","مانيكير جل",6,["Gel polish","Nail art +2"]),
        ("Pedicure & Spa","باديكير سبا",7,["Spa pedicure","Foot care"]),
        ("Bridal Makeup","مكياج عروس",45,["Trial incl.","HD makeup","Lashes"])],
     "packages":[("Glow Package","باقة الإشراق",15,"Fruit Facial + Pedicure + Half-leg Wax"),
        ("Royal Package","باقة ملكية",25,"Gold Facial + Hair Spa + Manicure"),
        ("Bridal Package","باقة العروس",80,"Bridal Makeup + Trial + Hair + Facial")],
     "team":[("Hala","Master Stylist","هالة"),("Reem","Bridal Specialist","ريم"),("Sara","Skin Expert","سارة")],
     "reviews":[("Hala A.","KAHI is my hidden gem in Salmiya! Best balayage ever ❤️"),
        ("Sara M.","So personalized and calm. Love the gold facial."),
        ("Layla K.","Finally a salon that treats you like family!")]},
    {"slug":"mahima","name_en":"Mahima Ladies Salon","name_ar":"صالون ماهيما للسيدات",
     "phone":"96551413855","phone_disp":"+965 5141 3855","area_en":"Salmiya, Block 10","area_ar":"السالمية، القطعة 10",
     "tag_en":"Luxury Beauty, Personalized","tag_ar":"جمال فاخر متميز","accent":"#ffd6a5","ig":"mahima_salon",
     "lat":29.3342,"lon":48.0788,"clients":188,
     "services":[("Haircut & Styling","قص وتصفيف",3,["Trend cut","Curls","Straighten"]),
        ("Hair Color","صبغ الشعر",20,["Full color","Highlights"]),
        ("Nail & Spa Packages","باقات الأظافر",10,["Manicure","Pedicure","Spa"]),
        ("Gel Manicure","مانيكير جل",5,["Gel polish","Nail art"]),
        ("Pedicure","باديكير",5,["Spa pedicure","Foot care"]),
        ("Bridal Makeup","مكياج عروس",38,["HD","Trial"]),
        ("Eyebrows & Lashes","حواجب ورموش",4,["Threading","Lash lift"]),
        ("Waxing","إزالة الشعر",3,["Face","Body"])],
     "packages":[("Mahima Glow","إشراق ماهيما",10,"Brightening Facial + Manicure + Pedicure"),
        ("Mahima Special","عرض ماهيما",18,"Haircut + Color + Blowdry"),
        ("Bridal Package","باقة العروس",70,"Bridal Makeup + Hair + Facial")],
     "team":[("Mahima","Stylist","ماهيما"),("Priya","Nail Artist","بريا"),("Anjali","Colorist","أنجالي")],
     "reviews":[("Mahima S.","Mahima always makes me feel like a queen 👑"),
        ("Priya T.","Best nail art in Salmiya, hands down."),
        ("Anjali L.","Their spa packages are a lifesaver in Kuwait heat!")]},
    {"slug":"paulita","name_en":"Paulita Spa Beauty","name_ar":"بوليتا سبا للتجميل",
     "phone":"96569649660","phone_disp":"+965 6964 9660","area_en":"Salmiya, Block 9","area_ar":"السالمية، القطعة 9",
     "tag_en":"Relax, Refresh, Renew","tag_ar":"استرخي وتجدد","accent":"#a0e7e5","ig":"paulita_spa",
     "lat":29.3335,"lon":48.0770,"clients":172,
     "services":[("Haircut & Blowdry","قص وتصفيف",5,["Cut","Style","Blowdry"]),
        ("Hair Treatment","علاج الشعر",12,["Protein","Keratin"]),
        ("Glow Facial","فيشل مشرق",8,["Cleanse","Brighten"]),
        ("Gold Facial","فيشل ذهبي",15,["Gold mask","Hydra"]),
        ("Gel Manicure","مانيكير جل",6,["Gel","Art"]),
        ("Pedicure Spa","باديكير سبا",7,["Spa","Scrub"]),
        ("Body Massage","مساج الجسم",15,["Relax","Hot stone"]),
        ("Bridal Makeup","مكياج عروس",48,["HD","Trial","Lashes"])],
     "packages":[("Spa Escape","هروب سبا",18,"Gold Facial + Massage + Pedicure"),
        ("Paulita Day","يوم بوليتا",32,"Facial + Hair Spa + Manicure"),
        ("Bridal Package","باقة العروس",85,"Bridal Makeup + Hair + Spa")],
     "team":[("Paulita","Master Stylist","بوليتا"),("Carmen","Spa Therapist","كارمن"),("Lina","Makeup Artist","لينا")],
     "reviews":[("Paulita N.","Paulita Spa is pure bliss. The massage is heavenly."),
        ("Carmen F.","My gold facial glow lasted a week!"),
        ("Lina A.","Luxury and calm — worth every dinar.")]},
    {"slug":"neweves","name_en":"Neweves Salon","name_ar":"صالون نيو إيفز",
     "phone":"96594147140","phone_disp":"+965 9414 7140","area_en":"Hawally, Tunis St","area_ar":"حولي، شارع تونس",
     "tag_en":"Your Beauty, Our Craft","tag_ar":"جمالك، صنعتنا","accent":"#cdb4db","ig":"neweves_salon",
     "lat":29.3315,"lon":48.0340,"clients":159,
     "services":[("Haircut & Blowdry","قص وتصفيف",3,["Haircut","Blowdry"]),
        ("Hair Protein Treatment","علاج البروتين",15,["Protein","Mask"]),
        ("Simple Makeup","مكياج بسيط",10,["Party","Evening","Natural"]),
        ("Glow Facial","فيشل مشرق",6,["Cleanse","Brighten"]),
        ("Gel Manicure","مانيكير جل",5,["Gel","Nail art +2"]),
        ("Threading & Wax","تنظيف الشعر",3,["Face threading","Waxing"]),
        ("Bridal Makeup","مكياج عروس",40,["HD bridal","Trial"]),
        ("Body Massage","مساج الجسم",12,["Relax","Spa ritual"])],
     "packages":[("Quick Combo","باقة سريعة",8,"Haircut + Blowdry + Threading"),
        ("Pamper Package","باقة الدلال",15,"Facial + Manicure + Pedicure"),
        ("Bridal Package","باقة العروس",75,"Bridal Makeup + Facial + Hair")],
     "team":[("Eve","Hair Stylist","إيف"),("Mona","Makeup Artist","منى"),("Rana","Spa Therapist","رنا")],
     "reviews":[("Eve R.","Neweves is my go-to in Hawally! Great prices."),
        ("Mona F.","Haircut + blow dry just 3KD and looks fab!"),
        ("Rana D.","Very clean and comfortable. Highly recommend.")]},
    {"slug":"yours","name_en":"Yours Salon","name_ar":"صالون يورز",
     "phone":"96597200323","phone_disp":"+965 9720 0323","area_en":"Maidan Hawally","area_ar":"ميدان حولي",
     "tag_en":"Beauty, Wellness & Beyond","tag_ar":"الجمال والعافية وأكثر","accent":"#bde0fe","ig":"yours_salon",
     "lat":29.3305,"lon":48.0360,"clients":196,
     "services":[("Haircut & Color","قص وصبغ",6,["Cut","Color","Style"]),
        ("Hair Spa","سبا الشعر",12,["Treatment","Mask"]),
        ("Glow Facial","فيشل مشرق",8,["Peel","Glow therapy"]),
        ("Gel Manicure","مانيكير جل",6,["Gel","Art"]),
        ("Pedicure","باديكير",6,["Spa","Care"]),
        ("Bridal Makeup","مكياج عروس",42,["HD","Trial"]),
        ("Full Body Massage","مساج كامل",15,["Relax","Aroma"]),
        ("Waxing & Threading","شمع وتنظيف",4,["Face","Body"])],
     "packages":[("Yours Escape","هروب يورز",15,"Facial + Manicure + Pedicure"),
        ("Wellness Day","يوم العافية",25,"Massage + Scrub + Facial"),
        ("Bridal Package","باقة العروس",78,"Bridal Makeup + Hair + Spa")],
     "team":[("Yara","Stylist","يارا"),("Mira","Therapist","ميرة"),("Salma","Makeup Artist","سلمى")],
     "reviews":[("Yara K.","Yours Salon is my weekly escape. The massage is divine."),
        ("Mira H.","Clean, calm, professional. Exactly what Hawally needed."),
        ("Salma R.","Got so many compliments after my makeover!")]},
]

def owner_photos(slug):
    """Return list of owner photos (root-relative /owner-photos/...) if dropped."""
    folder=f"leads-sites/{slug}/owner-photos"
    if not os.path.isdir(folder): return []
    files=[]
    for e in ("*.jpg","*.jpeg","*.png","*.webp","*.JPG","*.JPEG","*.PNG"):
        files+=glob.glob(os.path.join(folder,e))
    # make project-relative so subdir sites resolve correctly
    return [f"{BASE}/{slug}/owner-photos/{os.path.basename(f)}" for f in sorted(files)]

def monogram(name_en,accent):
    letters="".join(w[0] for w in name_en.split()[:2]).upper()
    return f'<svg viewBox="0 0 100 100" width="46" height="46" aria-hidden="true"><circle cx="50" cy="50" r="46" fill="none" stroke="{accent}" stroke-width="2"/><circle cx="50" cy="50" r="38" fill="none" stroke="{accent}" stroke-width="0.6" opacity="0.5"/><text x="50" y="50" text-anchor="middle" dominant-baseline="central" font-family="Cormorant Garamond, serif" font-size="30" font-weight="700" fill="{accent}">{letters}</text></svg>'

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
#cur{{position:fixed;top:0;left:0;width:12px;height:12px;border-radius:50%;background:var(--ac);mix-blend-mode:difference;pointer-events:none;z-index:9999;transform:translate(-50%,-50%)}}
#cur.big{{width:50px;height:50px;background:rgba(255,255,255,.2)}}
nav{{position:fixed;top:0;width:100%;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:18px 6%;transition:.4s}}
nav.scrolled{{background:rgba(10,10,10,.88);backdrop-filter:blur(16px);padding:12px 6%;border-bottom:1px solid rgba(255,255,255,.06)}}
.logo{{display:flex;align-items:center;gap:12px;font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:700}}
.nav-links a{{color:#fff;text-decoration:none;margin-left:22px;font-size:.85rem;opacity:.8}}
.nav-links a:hover{{opacity:1;color:var(--ac)}}
.hero{{position:relative;height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.hero .bgwrap{{position:absolute;inset:0;overflow:hidden}}
.hero img.bg{{position:absolute;inset:-5%;width:110%;height:110%;object-fit:cover;filter:saturate(1.05) contrast(1.05);animation:kenburns 22s ease-in-out infinite alternate}}
@keyframes kenburns{{0%{{transform:scale(1.1) translate(0,0)}}50%{{transform:scale(1.22) translate(-2%,-1%)}}100%{{transform:scale(1.15) translate(2%,1%)}}}}
.hero .ov{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.25),rgba(10,10,10,.1) 40%,rgba(10,10,10,.78))}}
.hero .grain{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.02) 0 1px,transparent 1px 3px);mix-blend-mode:overlay;opacity:.5;pointer-events:none}}
.hero .hc{{position:relative;z-index:3;padding:0 20px}}
.hero .kicker{{letter-spacing:6px;text-transform:uppercase;font-size:.8rem;color:var(--ac);margin-bottom:18px;opacity:0;animation:up 1s .3s forwards}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(3.2rem,9vw,7rem);font-weight:700;line-height:1;opacity:0;animation:up 1.1s .5s forwards}}
.hero .ar{{font-size:clamp(1.6rem,4vw,3rem);color:var(--ac);margin-top:6px;font-weight:700;opacity:0;animation:up 1.1s .7s forwards}}
.hero p{{margin-top:20px;font-size:1.1rem;font-weight:300;opacity:0;animation:up 1.1s .9s forwards}}
.hero .cta{{margin-top:34px;display:flex;gap:16px;justify-content:center;flex-wrap:wrap;opacity:0;animation:up 1.1s 1.1s forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:translateY(0)}}}}
.btn{{padding:15px 36px;border-radius:50px;font-weight:600;font-size:1rem;text-decoration:none;transition:.4s;border:none;cursor:pointer;display:inline-block}}
.btn.p{{background:var(--ac);color:#0a0a0a;box-shadow:0 10px 40px rgba(232,180,212,.35)}}
.btn.g{{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.5)}}
.btn:hover{{transform:translateY(-4px) scale(1.03)}}
.scrollind{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);z-index:3;font-size:.75rem;letter-spacing:3px;opacity:.7;animation:bob 2s infinite}}
@keyframes bob{{50%{{transform:translate(-50%,10px)}}}}

.marq{{overflow:hidden;background:var(--ac);color:#0a0a0a;padding:14px 0;white-space:nowrap}}
.marq .track{{display:inline-block;animation:scroll 22s linear infinite;font-weight:600;letter-spacing:1px}}
.marq span{{margin:0 28px}}
@keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}

.stats{{display:flex;justify-content:center;gap:60px;flex-wrap:wrap;padding:60px 6% 40px;background:#0d0d0d;text-align:center}}
.stat .num{{font-family:'Cormorant Garamond',serif;font-size:3.4rem;font-weight:700;color:var(--ac)}}
.stat .lbl{{font-size:.9rem;opacity:.7;letter-spacing:1px}}
.openbadge{{display:inline-flex;align-items:center;gap:8px;padding:8px 18px;border-radius:30px;font-size:.85rem;font-weight:600;margin-top:18px}}
.openbadge .dot{{width:10px;height:10px;border-radius:50%;background:#25D366;box-shadow:0 0 10px #25D366;animation:pulse 1.5s infinite}}
@keyframes pulse{{50%{{opacity:.4}}}}

.serv{{padding:100px 6%;background:#0a0a0a}}
.sec-t{{text-align:center;margin-bottom:50px}}
.sec-t .ey{{color:var(--ac);letter-spacing:3px;text-transform:uppercase;font-size:.8rem}}
.sec-t h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.6rem);font-weight:700}}
.sec-t .ar{{color:var(--ac);font-size:1.4rem}}
.sgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;max-width:1200px;margin:0 auto}}
.scard{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:22px;transition:.4s;display:flex;flex-direction:column}}
.scard:hover{{transform:translateY(-8px);border-color:var(--ac)}}
.scard .top{{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}}
.scard h3{{font-family:'Cormorant Garamond',serif;font-size:1.35rem;font-weight:700;line-height:1.1}}
.scard .ar{{color:var(--ac);font-size:.95rem;margin:2px 0 10px}}
.scard .price{{font-size:1.5rem;font-weight:700;color:var(--ac);white-space:nowrap}}
.scard .price small{{font-size:.8rem;opacity:.6;font-weight:400}}
.scard ul{{list-style:none;margin:10px 0 16px;flex:1}}
.scard li{{font-size:.82rem;opacity:.7;padding:3px 0;border-bottom:1px solid rgba(255,255,255,.05)}}
.scard .bk button{{width:100%;padding:11px;border-radius:30px;border:none;background:var(--ac);color:#0a0a0a;font-weight:600;cursor:pointer;font-size:.9rem;transition:.3s}}
.scard .bk button:hover{{background:#fff}}

.hgal{{padding:90px 0;background:#0d0d0d;overflow:hidden}}
.hgal .sec-t{{padding:0 6% 30px}}
.htrack{{display:flex;gap:16px;padding:0 6%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}}
.htrack::-webkit-scrollbar{{display:none}}
.hcard{{flex:0 0 320px;height:420px;border-radius:16px;overflow:hidden;position:relative;scroll-snap-align:start}}
.hcard img{{width:100%;height:100%;object-fit:cover;transition:transform .8s}}
.hcard:hover img{{transform:scale(1.1)}}
.hcard .ov{{position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(10,10,10,.8))}}
.hcard .cap{{position:absolute;bottom:16px;left:18px;font-weight:600}}
.draghint{{text-align:center;font-size:.8rem;opacity:.5;margin-top:16px}}

.team{{padding:90px 6%;background:#0a0a0a}}
.tgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1000px;margin:0 auto}}
.tcard{{text-align:center}}
.tcard .ph{{width:140px;height:140px;border-radius:50%;margin:0 auto 16px;object-fit:cover;border:3px solid var(--ac)}}
.tcard h3{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:700}}
.tcard .ar{{color:var(--ac);font-size:1rem}}
.tcard p{{opacity:.7;font-size:.88rem;margin-top:4px}}

.pkg{{padding:90px 6%;background:#0d0d0d}}
.pgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1000px;margin:0 auto}}
.pcard{{border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:30px;text-align:center;position:relative;overflow:hidden;transition:.4s}}
.pcard:hover{{transform:translateY(-8px);border-color:var(--ac)}}
.pcard .feat{{position:absolute;top:14px;right:-34px;background:var(--ac);color:#0a0a0a;font-size:.7rem;font-weight:700;padding:5px 40px;transform:rotate(45deg)}}
.pcard h3{{font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:700}}
.pcard .ar{{color:var(--ac);font-size:1rem;margin:4px 0 14px}}
.pcard .pp{{font-size:2.2rem;font-weight:700;color:var(--ac)}}
.pcard .pp small{{font-size:.9rem;opacity:.6;font-weight:400}}
.pcard p{{opacity:.75;font-size:.9rem;margin:12px 0 20px;line-height:1.5}}
.pcard button{{padding:12px 30px;border-radius:30px;border:1px solid var(--ac);background:transparent;color:var(--ac);font-weight:600;cursor:pointer;transition:.3s}}
.pcard button:hover{{background:var(--ac);color:#0a0a0a}}

.book{{padding:100px 6%;background:#0a0a0a}}
.bookwrap{{max-width:640px;margin:0 auto;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:24px;padding:40px}}
.bookwrap label{{display:block;font-size:.85rem;opacity:.7;margin-bottom:7px}}
.bookwrap input,.bookwrap select,.bookwrap textarea{{width:100%;padding:14px 16px;border-radius:12px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#fff;font-family:'Poppins',sans-serif;font-size:.95rem}}
.bookwrap input:focus,.bookwrap select:focus,.bookwrap textarea:focus{{outline:none;border-color:var(--ac)}}
.bookwrap .row{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px}}
.bookwrap .submit{{width:100%;padding:16px;border-radius:30px;border:none;background:var(--ac);color:#0a0a0a;font-weight:700;font-size:1.05rem;cursor:pointer;transition:.3s}}
.bookwrap .submit:hover{{transform:scale(1.02);background:#fff}}
.bookwrap .note{{text-align:center;font-size:.8rem;opacity:.55;margin-top:14px}}

.mapsec{{padding:90px 6%;background:#0d0d0d}}
.mapcard{{display:block;max-width:1000px;margin:0 auto;border-radius:18px;overflow:hidden;text-decoration:none;background:linear-gradient(135deg,rgba(255,255,255,.06),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.12);transition:.4s}}
.mapcard:hover{{border-color:var(--ac);transform:translateY(-4px)}}
.mc-inner{{display:flex;align-items:center;gap:24px;padding:40px}}
.mc-pin{{font-size:3rem}}
.mc-txt{{font-size:1.1rem;line-height:1.6}}
.mc-txt strong{{font-family:'Cormorant Garamond',serif;font-size:1.8rem;color:#fff}}
.mc-cta{{color:var(--ac);font-weight:600;font-size:.95rem}}

.testi{{padding:90px 6%;background:#0a0a0a}}
.tgrid2{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1000px;margin:0 auto}}
.tcard2{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:26px}}
.tcard2 .stars{{color:#ffd700;font-size:1.1rem;margin-bottom:12px;letter-spacing:2px}}
.tcard2 p{{font-style:italic;line-height:1.7;opacity:.9;margin-bottom:14px}}
.tcard2 .who{{font-weight:600;color:var(--ac)}}

.contact{{padding:90px 6%;text-align:center;background:#0d0d0d}}
.contact .ey{{color:var(--ac);letter-spacing:3px;text-transform:uppercase;font-size:.8rem}}
.contact h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,5vw,3.6rem);font-weight:700;margin:10px 0}}
.contact .ar{{color:var(--ac);font-size:1.4rem;margin-bottom:20px}}
.cinfo{{display:flex;gap:36px;justify-content:center;flex-wrap:wrap;margin-bottom:20px}}
.cinfo div{{font-size:1.02rem}}
.cinfo a{{color:var(--ac);text-decoration:none}}
footer{{text-align:center;padding:44px 20px;opacity:.5;font-size:.85rem}}
.wa-float{{position:fixed;bottom:24px;right:24px;z-index:120;background:#25D366;color:#fff;padding:14px 22px;border-radius:50px;text-decoration:none;font-weight:600;display:flex;align-items:center;gap:9px;box-shadow:0 10px 36px rgba(37,211,102,.5);transition:.3s}}
.wa-float:hover{{transform:scale(1.06)}}
.reveal{{opacity:1;transform:none}}
.js .reveal{{opacity:1;transform:translateY(40px);transition:1s cubic-bezier(.2,.8,.2,1)}}
.js .reveal.show{{opacity:1;transform:translateY(0)}}
@media(max-width:860px){{.sgrid,.pgrid,.tgrid,.tgrid2{{grid-template-columns:repeat(2,1fr)}}.nav-links{{display:none}}.bookwrap .row{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div id="cur"></div>
<script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js');document.body.classList.remove('no-js');</script>
<nav id="nav"><div class="logo">{MONO} {name_en}</div><div class="nav-links"><a href="#services">Services</a><a href="#gallery">Gallery</a><a href="#team">Team</a><a href="#packages">Packages</a><a href="#book">Book</a></div></nav>

<header class="hero">
  <div class="bgwrap"><img class="bg" src="{HERO}" alt=""></div>
  <div class="ov"></div><div class="grain"></div>
  <div class="hc">
    <div class="kicker">Premium Salon · Kuwait</div>
    <h1>{name_en}</h1>
    <div class="ar">{name_ar}</div>
    <p>{tag_en} — <span class="ar">{tag_ar}</span></p>
    <div class="cta">
      <a href="#book" class="btn p">Book Online · احجزي الآن</a>
      <a href="https://wa.me/{phone}" class="btn g">WhatsApp · واتساب</a>
    </div>
    <div class="openbadge" id="ob"><span class="dot"></span><span id="obt">Checking...</span></div>
  </div>
  <div class="scrollind">SCROLL ↓</div>
</header>

<div class="marq"><div class="track">{MARQ}</div></div>

<section class="stats">
  <div class="stat"><div class="num" data-to="{CLIENTS}">0</div><div class="lbl">Happy Clients · عميلة سعيدة</div></div>
  <div class="stat"><div class="num" data-to="8">0</div><div class="lbl">Premium Services · خدمة</div></div>
  <div class="stat"><div class="num" data-to="5">0</div><div class="lbl">Years in Salmiya · سنوات</div></div>
</section>

<section class="serv" id="services">
  <div class="sec-t reveal"><div class="ey">Menu &amp; Prices</div><h2>Our Services</h2><div class="ar">خدماتنا وأسعارنا</div></div>
  <div class="sgrid">{SERVICES}</div>
</section>

<section class="hgal" id="gallery">
  <div class="sec-t reveal"><div class="ey">Our Work</div><h2>The Gallery</h2><div class="ar">معرض أعمالنا</div></div>
  <div class="htrack">{HGAL}</div>
  <div class="draghint">← Drag / scroll to explore · اسحبي للاستكشاف →</div>
</section>

<section class="team" id="team">
  <div class="sec-t reveal"><div class="ey">Meet The Artists</div><h2>Our Team</h2><div class="ar">فريقنا</div></div>
  <div class="tgrid">{TEAM}</div>
</section>

<section class="pkg" id="packages">
  <div class="sec-t reveal"><div class="ey">Best Value</div><h2>Packages</h2><div class="ar">باقاتنا</div></div>
  <div class="pgrid">{PACKAGES}</div>
</section>

<section class="book" id="book">
  <div class="sec-t reveal"><div class="ey">Reserve Your Moment</div><h2>Book Appointment</h2><div class="ar">احجزي موعدك</div></div>
  <div class="bookwrap reveal">
    <form id="bkf" onsubmit="return sendBook(event)">
      <div class="row">
        <div><label>Your Name / اسمك</label><input id="bn" required placeholder="Full name"></div>
        <div><label>Phone / الجوال</label><input id="bp" required placeholder="+965 ......"></div>
      </div>
      <div><label>Service / الخدمة</label><select id="bs">{SERVICE_OPTS}</select></div>
      <div class="row">
        <div><label>Date / التاريخ</label><input id="bd" type="date" required></div>
        <div><label>Time / الوقت</label><input id="bt" type="time" required></div>
      </div>
      <div><label>Note / ملاحظة</label><textarea id="bm" rows="2" placeholder="Any requests?"></textarea></div>
      <button class="submit" type="submit">Confirm via WhatsApp · أكدي عبر واتساب</button>
      <div class="note">You'll be redirected to WhatsApp to confirm with the salon ✦</div>
    </form>
  </div>
</section>

<section class="mapsec">
  <div class="sec-t reveal"><div class="ey">Find Us</div><h2>Location</h2><div class="ar">موقعنا</div></div>
  <a class="mapcard" href="https://www.google.com/maps/search/?api=1&query={LAT},{LON}" target="_blank">
    <div class="mc-inner">
      <div class="mc-pin">📍</div>
      <div class="mc-txt"><strong>{name_en}</strong><br>{area_en} · <span class="ar">{area_ar}</span><br><span class="mc-cta">Open in Maps →</span></div>
    </div>
  </a>
</section>

<section class="testi">
  <div class="sec-t reveal"><div class="ey">Loved By Clients</div><h2>Reviews</h2><div class="ar">آراء الزبائن</div></div>
  <div class="tgrid2">{REVIEWS}</div>
</section>

<section class="contact">
  <div class="ey reveal">Visit Us</div>
  <h2 class="reveal">Where To Find Us</h2>
  <div class="ar reveal">{name_ar} · زورونا</div>
  <div class="cinfo reveal">
    <div>📍 {area_en}<br><span class="ar">{area_ar}</span></div>
    <div>📞 <a href="https://wa.me/{phone}">{phone_disp}</a></div>
    <div>📸 <a href="https://instagram.com/{ig}" target="_blank">@{ig}</a></div>
    <div>🕐 Daily 10AM–9PM · Fri 2PM–9PM</div>
  </div>
</section>

<footer>© {name_en} · Designed by KB Rewaq Digital · +965 50703252</footer>
<a href="https://wa.me/{phone}" class="wa-float">💬 WhatsApp Booking</a>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
const cur=document.getElementById('cur');
addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px';}});
document.querySelectorAll('a,button').forEach(el=>{{el.addEventListener('mouseenter',()=>cur.classList.add('big'));el.addEventListener('mouseleave',()=>cur.classList.remove('big'));}});
addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',scrollY>60));
// reliable reveal via IntersectionObserver (no GSAP dependency)
(function(){{const els=document.querySelectorAll('.reveal');if(!('IntersectionObserver' in window)){{els.forEach(e=>e.classList.add('show'));return;}}
const io=new IntersectionObserver((ents)=>{{ents.forEach(en=>{{if(en.isIntersecting){{en.target.classList.add('show');io.unobserve(en.target);}}}});}},{{threshold:0.08}});
els.forEach(e=>io.observe(e));}})();
(function(){{const now=new Date();const kw=new Date(now.getTime()+(now.getTimezoneOffset()*60000)+(3*3600000));const day=kw.getDay();const h=kw.getHours();let open=(day===5)?(h>=14&&h<21):(h>=10&&h<21);const el=document.getElementById('obt');el.textContent=open?'Open Now · مفتوح الآن':'Closed · مغلق';document.querySelector('#ob .dot').style.background=open?'#25D366':'#888';}})();
document.querySelectorAll('.num').forEach(n=>{{const to=+n.dataset.to;let c=0;const step=Math.max(1,Math.floor(to/60));const iv=setInterval(()=>{{c+=step;if(c>=to){{c=to;clearInterval(iv);}}n.textContent=c;}},25);}});
function wa(svc){{const t=encodeURIComponent('Hello {name_en}! I want to book:\\nService: '+svc+'\\nPlease share available time. Thank you!');window.open('https://wa.me/{phone}?text='+t,'_blank');}}
function sendBook(e){{e.preventDefault();const n=bn.value,p=bp.value,s=document.getElementById('bs').value,d=bd.value,t=bt.value,m=bm.value;
const msg='Hello {name_en}! New booking request:\\nName: '+n+'\\nPhone: '+p+'\\nService: '+s+'\\nDate: '+d+'\\nTime: '+t+'\\nNote: '+m;
window.open('https://wa.me/{phone}?text='+encodeURIComponent(msg),'_blank');}}
</script>
</body></html>"""

def gen(l):
    slug=l["slug"]
    own=owner_photos(slug)
    # hero: owner photo first, else AI bespoke
    hero = own[0] if own else AI[slug]
    galpool = (own[1:7] if len(own)>1 else GAL)
    def gimg(i): return galpool[i%len(galpool)]
    mono=monogram(l["name_en"], l["accent"])
    marq="".join(f"<span>{s[0]} {s[1]} · {s[2]} KD</span>" for s in l["services"]); marq=marq+marq
    svcs=""; opts=""
    for (en,ar,price,items) in l["services"]:
        li="".join(f"<li>{it}</li>" for it in items)
        svcs+=f'<div class="scard reveal"><div class="top"><div><h3>{en}</h3><div class="ar">{ar}</div></div><div class="price">{price}<small> KD</small></div></div><ul>{li}</ul><div class="bk"><button onclick="wa(\'{en}\')">Book · احجزي</button></div></div>'
        opts+=f'<option value="{en} ({price} KD)">{en} — {price} KD</option>'
    hgal="".join(f'<div class="hcard"><img src="{gimg(i)}" alt=""><div class="ov"></div><div class="cap">{l["name_en"]}</div></div>' for i in range(6))
    team=""
    for (en,role,ar) in l["team"]:
        team+=f'<div class="tcard reveal"><img class="ph" src="{gimg(0)}" alt=""><h3>{en}</h3><div class="ar">{ar}</div><p>{role}</p></div>'
    pkgs=""
    for i,(en,ar,price,desc) in enumerate(l["packages"]):
        feat='<div class="feat">POPULAR</div>' if i==1 else ''
        pkgs+=f'<div class="pcard reveal">{feat}<h3>{en}</h3><div class="ar">{ar}</div><div class="pp">{price}<small> KD</small></div><p>{desc}</p><button onclick="wa(\'{en}\')">Book Package · احجزي</button></div>'
    revs=""
    for (who,txt) in l["reviews"]:
        revs+=f'<div class="tcard2 reveal"><div class="stars">★★★★★</div><p>"{txt}"</p><div class="who">— {who}</div></div>'
    la,lo=l["lat"],l["lon"]
    h=TPL
    repl={"{name_en}":l["name_en"],"{name_ar}":l["name_ar"],"{phone}":l["phone"],
        "{phone_disp}":l["phone_disp"],"{area_en}":l["area_en"],"{area_ar}":l["area_ar"],
        "{tag_en}":l["tag_en"],"{tag_ar}":l["tag_ar"],"{accent}":l["accent"],"{ig}":l["ig"],
        "{MONO}":mono,"{HERO}":hero,"{MARQ}":marq,"{SERVICES}":svcs,"{HGAL}":hgal,
        "{TEAM}":team,"{PACKAGES}":pkgs,"{REVIEWS}":revs,"{SERVICE_OPTS}":opts,
        "{CLIENTS}":str(l["clients"]),
        "{LAT}":str(la),"{LON}":str(lo),"{LATL}":str(la-0.003),"{LONL}":str(lo-0.004),"{LATR}":str(la+0.003),"{LONR}":str(lo+0.004)}
    for k,v in repl.items(): h=h.replace(k,v)
    h=h.replace("{{","{").replace("}}","}")
    os.makedirs(f'leads-sites/{slug}',exist_ok=True)
    open(f'leads-sites/{slug}/index.html','w',encoding='utf-8').write(h)
    mode = "OWNER PHOTOS" if own else "AI bespoke"
    print(f'OK {l["name_en"]} [{mode}]')

if __name__=="__main__":
    for l in LEADS: gen(l)
    print("v7 bespoke AI done")
