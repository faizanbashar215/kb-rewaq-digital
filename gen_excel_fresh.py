#!/usr/bin/env python3
# Build KB_Rewaq_Fresh_Leads.xlsx from fresh_sites CRM records. 8-col pahle-jaisa format.
import os, json, glob
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from urllib.parse import quote

CRM = r"D:\KB Rewaq Clients"
SITES = r"D:\digitalfirst-agency\fresh_sites"
OUT = r"D:\digitalfirst-agency\KB_Rewaq_Fresh_Leads.xlsx"
WA_YOU = "96550703252"

leads = []
for d in sorted(glob.glob(os.path.join(CRM, "*/"))):
    cj = os.path.join(d, "client.json")
    if not os.path.isfile(cj):
        continue
    j = json.load(open(cj, encoding="utf-8"))
    biz = j.get("business", {}); con = j.get("contact", {}); loc = j.get("location", {}); onl = j.get("online", {})
    slug = biz.get("slug", os.path.basename(d.rstrip("/\\")))
    phone = con.get("phone", "") or ""
    name = biz.get("name_en", "")
    area = loc.get("area_en", "")
    site = onl.get("site_url", "")
    # Per-lead human DM (English, no em-dash, Jarvis intro, automation story, NO price)
    # Vary opener + middle so no two read identical.
    openers = [
        f"Hey {name}",
        f"Hi {name}",
        f"Hello {name}",
        f"Good day {name}",
        f"Hi there {name}",
    ]
    about = [
        "I'm Jarvis, manager at KB Rewaq Digital. I build automation systems for Kuwait salons and spas.",
        "This is Jarvis from KB Rewaq Digital. I run automation for Kuwait beauty businesses.",
        "Jarvis here, I manage KB Rewaq Digital where we automate Kuwait salons end to end.",
        "I'm Jarvis, I look after KB Rewaq Digital and we set up automation for Kuwait salons.",
        "Hey, Jarvis from KB Rewaq Digital. We handle automation for salons across Kuwait.",
    ]
    pitch = [
        "Your business gets a live website, a services page, Instagram content, and a WhatsApp booking bot that replies to clients 24/7 while you focus on the salon.",
        "We give your salon a live site, social posts, and a WhatsApp bot that books clients for you around the clock.",
        "You get a website, fresh Instagram content, and an auto-reply WhatsApp that takes bookings even when you are busy with clients.",
        "The setup is a website plus Instagram plus a WhatsApp assistant that handles client bookings on its own.",
        "We put your salon on a website, keep Instagram active, and let a WhatsApp bot answer booking requests day and night.",
    ]
    close = [
        f"I saw {name} and your setup would fit this really well. I can put together a free demo of your own site in a day. Want me to send it over?",
        f"I came across {name} and thought your place would suit this perfectly. I will build a free demo site for you in a day if you want to see it.",
        f"Your salon {name} caught my eye and this system would suit you. I can show you a free demo of your own site within a day.",
        f"I noticed {name} and believe this would work great for you. A free demo of your site takes me about a day to make. Shall I send it?",
        f"{name} stood out to me and I think automation would lift your bookings. I can draft a free demo site for you in a day. Interested?",
    ]
    idx = len(leads) % 5
    a2 = (len(leads) + 1) % 5
    a3 = (len(leads) + 2) % 5
    area_note = f" Based in {area}." if area else ""
    dm = (f"{openers[idx]}. {about[a2]}{area_note} "
          f"{pitch[a3]} {close[a3]}")
    leads.append({"slug": slug, "name": name, "name_ar": biz.get("name_ar", ""), "area": area,
                  "phone": phone, "phone_disp": con.get("phone_disp", ""), "site": site, "dm": dm})

leads.sort(key=lambda x: x["name"].lower())

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "KB Rewaq Leads"
headers = ["#", "Business (EN)", "Business (AR)", "Area", "Phone (click→WhatsApp)",
           "Demo Website (click)", "Ready DM Message (link inside)", "Status"]
ws.append(headers)

green = Font(color="006100"); green_fill = PatternFill("solid", fgColor="C6EFCE")
blue = Font(color="0563C1", underline="single"); blue_fill = PatternFill("solid", fgColor="DDEBF7")
hdr_fill = PatternFill("solid", fgColor="1F4E78"); hdr_font = Font(color="FFFFFF", bold=True)
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")

for i, L in enumerate(leads, 1):
    phone_num = L["phone"] or WA_YOU
    phone_link = f"https://wa.me/{phone_num}?text={quote(L['dm'])}"
    demo_link = L["site"] if L["site"] else ""
    # Clickable: one click -> WhatsApp opens with DM pre-typed
    phone_cell = f'=HYPERLINK("{phone_link}","Click to DM")'
    demo_cell = f'=HYPERLINK("{demo_link}","View Demo Site")' if demo_link else "—"
    row = [i, L["name"], L["name_ar"], L["area"], phone_cell, demo_cell, L["dm"], "Live" if L["site"] else "Pending"]
    ws.append(row)
    r = ws.max_row
    for c in range(1, 9):
        ws.cell(r, c).border = border
        ws.cell(r, c).alignment = wrap
    if L["site"]:
        ws.cell(r, 5).font = green; ws.cell(r, 5).fill = green_fill
        ws.cell(r, 6).font = blue; ws.cell(r, 6).fill = blue_fill
        ws.cell(r, 8).font = Font(color="006100", bold=True)

for c in range(1, 9):
    ws.cell(1, c).fill = hdr_fill; ws.cell(1, c).font = hdr_font
    ws.cell(1, c).alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
widths = [5, 28, 22, 18, 22, 18, 60, 12]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
ws.freeze_panes = "A2"; ws.row_dimensions[1].height = 30

htu = wb.create_sheet("HOW TO USE")
htu["A1"] = "KB REWAQ DIGITAL — FRESH LEAD TRACKER"
htu["A1"].font = Font(bold=True, size=14, color="1F4E78")
lines = ["", "1. Click the GREEN phone cell -> opens WhatsApp to that lead with your DM pre-typed.",
         "2. Click the BLUE 'View Demo Site' cell -> opens the website built for them.",
         "3. Send the DM on WhatsApp. The link is already inside the message.",
         "4. When they reply YES, visit their salon, then discuss price & sign up.",
         "5. After sending, change Status to: replied / won / paid.", "",
         f"Your WA: +{WA_YOU}   |   Brand: KB Rewaq Digital",
         "", f"Total fresh leads: {len(leads)}   |   Live demo sites: {sum(1 for x in leads if x['site'])}"]
for i, t in enumerate(lines, 2):
    htu.cell(i, 1).value = t
htu.column_dimensions["A"].width = 110

wb.save(OUT)
print(f"SAVED {OUT} | Total {len(leads)} | Live {sum(1 for x in leads if x['site'])}")
