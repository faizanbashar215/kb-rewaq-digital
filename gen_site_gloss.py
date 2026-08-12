#!/usr/bin/env python3
# Generate ADVANCED Gloss-style luxury websites for the 14 imported WhatsApp leads.
# Uses template_gloss.render_gloss_advanced with full feature set.
import os, json, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template_gloss import render_gloss_advanced

AGENCY = os.environ.get("AGENCY_DIR", r"D:\digitalfirst-agency")
LEADS = os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients")
OUT = os.path.join(AGENCY, "fresh_sites")
ASSETS = os.path.join(AGENCY, "assets", "ai")

# shared content (same premium menu for all Kuwait salons, prices in KD)
SERVICES = [
    ("Hair Styling", "تصفيف الشعر", "15", ["Blowout", "Updo", "Bridal Hair", "Haircut & Finish"]),
    ("Hair Color", "صبغة الشعر", "35", ["Full Color", "Balayage", "Highlights", "Roots Touch-up"]),
    ("Nails & Manicure", "الأظافر", "12", ["Gel Manicure", "Acrylic", "Nail Art", "Pedikür"]),
    ("Lashes & Brows", "رموش وحواجب", "18", ["Classic Lashes", "Volume Lashes", "Brow Styling", "Tint"]),
    ("Facial & Skin", "بشرة", "25", ["Deep Clean", "Hydra Facial", "Peeling", "Mask"]),
    ("Massage", "مساج", "30", ["Relax Massage", "Back", "Aroma", "Hot Stone"]),
    ("Makeup", "مكياج", "28", ["Soft Glam", "Party Makeup", "Bridal Makeup", "Trial"]),
    ("Bridal Package", "باقة العروس", "150", ["Hair + Makeup + Nails", "Trial Session", "Day-of Touchups", "Assistant"]),
]
PACKAGES = [
    ("Glow Package", "باقة التوهج", "55", "Hair + Facial + Manicure — the complete refresh."),
    ("Bride-to-Be", "عروس", "150", "Full bridal look with trial and day-of support."),
    ("Self-Care Day", "يوم العناية", "80", "Massage + Facial + Blowout for total reset."),
]
TEAM = [
    ("Sarah", "Master Stylist", "مصففة", "https://i.pravatar.cc/160?img=47"),
    ("Nour", "Color Specialist", "خبيرة لون", "https://i.pravatar.cc/160?img=45"),
    ("Layla", "Nail Artist", "فنانة أظافر", "https://i.pravatar.cc/160?img=44"),
    ("Maya", "Makeup Artist", "فنانة مكياج", "https://i.pravatar.cc/160?img=49"),
]
# gallery: prefer local ai assets, fallback to picsum
ai = sorted(os.listdir(ASSETS)) if os.path.isdir(ASSETS) else []
GALLERY = [os.path.join("..", "assets", "ai", a) for a in ai[:6]] or [f"https://picsum.photos/seed/{i}/400/300" for i in range(6)]
REVIEWS = [
    ("Noura A.", "Absolutely the best experience in Kuwait. Elegant, calm, professional."),
    ("Hessa M.", "They made me feel beautiful. Will come back every week."),
    ("Maryam", "The bridal package was flawless — everyone asked who did my look!"),
]

def slugify(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

def main():
    crm = json.load(open(os.path.join(AGENCY, "crm_leads.json"), encoding="utf-8"))
    made = 0
    for x in crm:
        name = x["name_en"]; area = x.get("area", "") or ""
        phone = x["phone"]
        wa = f"https://wa.me/{phone}?text=" + "Hi%20" + re.sub(r'[^A-Za-z0-9]','%20',name) + "%2C%20Jarvis%20here%20from%20KB%20Rewaq%20Digital.%20Your%20site%20is%20ready!%20Want%20a%20free%20demo%3F"
        html = render_gloss_advanced(name, area, phone, wa, SERVICES, PACKAGES, TEAM, GALLERY, REVIEWS, "")
        d = os.path.join(OUT, slugify(name))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
        made += 1; print(f"  built {slugify(name)}/")
    print(f"TOTAL advanced Gloss sites: {made}")

if __name__ == "__main__":
    main()
