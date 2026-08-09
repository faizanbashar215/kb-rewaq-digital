#!/usr/bin/env python3
"""Build KB Rewaq lead Excel with click-to-WhatsApp + DM + site link."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

GITHUB = "https://faizanbashar215.github.io/kb-rewaq-digital"

LEADS = [
    ("Midyaf Beauty Salon", "صالون ميدياف", "Salmiya Block 9", "96541065562", "+965 4106 5562", "midyaf",
     "Hi Midyaf! I built a FREE sample 3D website for your salon (link inside). KB Rewaq Digital makes salon sites + Instagram in 3 days, from 25 KWD. Want it with YOUR name? Reply YES."),
    ("Look Noor Ladies Beauty Salon", "صالون لوك نور", "Salmiya Block 12", "96560748354", "+965 6074 8354", "looknoor",
     "Hello Look Noor! Your competitors are online, you should be too. I made a free demo site for you (link inside). Professional salon website + social from 25 KWD, ready in 3 days. Interested?"),
    ("Monya Ladies Beauty Salon", "صالون منى", "Salmiya Block 10", "96598980970", "+965 9898 0970", "monya",
     "Hi Monya Salon! Summer offers are great but a website brings more clients. I built you a free sample 3D site (link inside). Sites + Instagram from 25 KWD, 3-day delivery. Want it?"),
    ("Royal Jasmine Salon", "صالون الياسمين", "Salmiya Block 10", "96561114586", "+965 6111 4586", "royaljasmine",
     "Hello Royal Jasmine! A royal salon deserves a royal website. I made one for you free (link inside). KB Rewaq Digital: site + social from 25 KWD, 3 days. Reply YES for your branded version."),
    ("Larene Beauty Salon & Spa", "صالون لارين", "Hawally Block 8", "96551746804", "+965 5174 6804", "larene",
     "Hi Larene! Your spa needs a beautiful site to match. I built a free 3D demo (link inside). We do salon/spa websites + Instagram from 25 KWD, ready in 3 days. Interested?"),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "KB Rewaq Leads"

# Styles
hdr_fill = PatternFill("solid", fgColor="6A0DAD")
hdr_font = Font(bold=True, color="FFFFFF", size=12)
cell_font = Font(size=11)
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left = Alignment(horizontal="left", vertical="center", wrap_text=True)
thin = Side(style="thin", color="DDDDDD")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wa_fill = PatternFill("solid", fgColor="25D366")
site_fill = PatternFill("solid", fgColor="1E90FF")

headers = ["#", "Business (EN)", "Business (AR)", "Area", "Phone (click→WhatsApp)",
           "Demo Website (click)", "Ready DM Message (copy/paste)", "Status"]
widths = [4, 26, 18, 16, 24, 30, 52, 14]

for c, h in enumerate(headers, 1):
    cell = ws.cell(1, c, h)
    cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = center; cell.border = border
for c, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(c)].width = w

for i, (en, ar, area, phone, disp, slug, dm) in enumerate(LEADS, 1):
    r = i + 1
    wa_url = f"https://wa.me/{phone}?text={dm.replace(' ', '%20')}"
    site_url = f"{GITHUB}/{slug}/"
    vals = [i, en, ar, area, disp, "View Demo Site", dm, "Lead"]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(r, c, v)
        cell.font = cell_font; cell.border = border
        cell.alignment = left if c in (2,3,4,7) else center
    # phone -> whatsapp hyperlink
    ws.cell(r, 5).hyperlink = wa_url
    ws.cell(r, 5).fill = wa_fill
    ws.cell(r, 5).font = Font(size=11, bold=True, color="FFFFFF")
    # site link
    ws.cell(r, 6).hyperlink = site_url
    ws.cell(r, 6).fill = site_fill
    ws.cell(r, 6).font = Font(size=11, bold=True, color="FFFFFF")
    ws.cell(r, 6).alignment = center
    ws.row_dimensions[r].height = 78

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:H{len(LEADS)+1}"

# Instructions sheet
ws2 = wb.create_sheet("HOW TO USE")
instructions = [
    ("KB REWAQ DIGITAL — LEAD TRACKER", True),
    ("", False),
    ("1. Click the GREEN phone cell -> opens WhatsApp to that lead with your DM pre-typed.", False),
    ("2. Click the BLUE 'View Demo Site' cell -> opens the 3D website you built for them.", False),
    ("3. Send the DM on WhatsApp. When they reply, change Status column to: replied / won / paid.", False),
    ("4. Demo sites are LIVE on GitHub Pages -> the prospect can open & see them too.", False),
    ("5. After sending, mark Status and we track weekly conversion.", False),
    ("", False),
    ("Your WA: +965 50703252   |   Brand: KB Rewaq Digital", False),
]
for i, (txt, bold) in enumerate(instructions, 1):
    c = ws2.cell(i, 1, txt)
    c.font = Font(bold=bold, size=14 if bold else 11)
    ws2.column_dimensions["A"].width = 100

wb.save("KB_Rewaq_Leads.xlsx")
print("✅ KB_Rewaq_Leads.xlsx created with", len(LEADS), "leads")
