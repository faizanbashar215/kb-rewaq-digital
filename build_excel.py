#!/usr/bin/env python3
"""Build KB Rewaq lead Excel with click-to-WhatsApp + DM (link embedded) + site link.
DM rules (boss 2026-08-09): no upfront price, attractive/professional, explain IG
delivery concretely, close with office-visit offer on YES.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from urllib.parse import quote

GITHUB = "https://faizanbashar215.github.io/kb-rewaq-digital"

# Each lead: (en, ar, area, phone, disp, slug, opener)
# DM body is built from a shared professional template + salon opener + site link.
LEADS = [
    ("Midyaf Beauty Salon", "صالون ميدياف", "Salmiya Block 9", "96567633667", "+965 6763 3667", "midyaf",
     "Hi Midyaf Beauty Salon! 👋 Your salon deserves to be seen online."),
    ("Look Noor Ladies Beauty Salon", "صالون لوك نور", "Salmiya Block 12", "96560748354", "+965 6074 8354", "looknoor",
     "Hello Look Noor Ladies! 👋 Your clients are already on Instagram — let's meet them there."),
    ("Monya Ladies Beauty Salon", "صالون منى", "Salmiya Block 10", "96598980970", "+965 9898 0970", "monya",
     "Hi Monya Ladies Salon! 👋 Summer is busy — a website catches the walk-ins you're missing."),
    ("Royal Jasmine Salon", "صالون الياسمين", "Salmiya Block 10", "96561114586", "+965 6111 4586", "royaljasmine",
     "Hello Royal Jasmine! 👋 A royal salon needs a royal presence online."),
    ("Larene Beauty Salon & Spa", "صالون لارين", "Hawally Block 8", "96551746804", "+965 5174 6804", "larene",
     "Hi Larene Beauty Spa! 👋 Your spa should look as beautiful online as it does inside."),
]

# Shared professional body (NO price upfront, explains IG delivery, office-visit close)
BODY = (
    "\n\nI'm Faizan from KB Rewaq Digital. I built a FREE sample website for your salon "
    "so you can see exactly what you'd get — no cost, no obligation.\n\n"
    "Here's what we do for salons like yours:\n"
    "🌐 Custom website — your name, services & prices, online booking, Arabic + English\n"
    "📸 Instagram growth — you send us photos, we design your posts, reels & stories "
    "and handle the posting, so your salon stays active and pulls in new clients\n"
    "📈 More visibility, more bookings — that's the whole point\n\n"
    "If you like the demo, I'll visit your salon for a free 15-minute overview and show "
    "you the full plan — no pressure, just a clear next step.\n\n"
    "Reply YES and I'll set it up. 🙌"
)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "KB Rewaq Leads"

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
           "Demo Website (click)", "Ready DM Message (link inside)", "Status"]
widths = [4, 26, 18, 16, 24, 30, 60, 14]

for c, h in enumerate(headers, 1):
    cell = ws.cell(1, c, h)
    cell.fill = hdr_fill; cell.font = hdr_font; cell.alignment = center; cell.border = border
for c, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(c)].width = w

for i, (en, ar, area, phone, disp, slug, opener) in enumerate(LEADS, 1):
    r = i + 1
    site_url = f"{GITHUB}/{slug}/"
    dm = opener + BODY + f"\n\n👉 Your free demo: {site_url}"
    wa_url = f"https://wa.me/{phone}?text={quote(dm)}"
    vals = [i, en, ar, area, disp, "View Demo Site", dm, "Lead"]
    for c, v in enumerate(vals, 1):
        cell = ws.cell(r, c, v)
        cell.font = cell_font; cell.border = border
        cell.alignment = left if c in (2, 3, 4, 7) else center
    ws.cell(r, 5).hyperlink = wa_url
    ws.cell(r, 5).fill = wa_fill
    ws.cell(r, 5).font = Font(size=11, bold=True, color="FFFFFF")
    ws.cell(r, 6).hyperlink = site_url
    ws.cell(r, 6).fill = site_fill
    ws.cell(r, 6).font = Font(size=11, bold=True, color="FFFFFF")
    ws.cell(r, 6).alignment = center
    ws.row_dimensions[r].height = 140

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:H{len(LEADS)+1}"

# Instructions sheet
ws2 = wb.create_sheet("HOW TO USE")
instructions = [
    ("KB REWAQ DIGITAL — LEAD TRACKER", True),
    ("", False),
    ("1. Click the GREEN phone cell -> opens WhatsApp to that lead with your DM + their demo link pre-typed.", False),
    ("2. Click the BLUE 'View Demo Site' cell -> opens the 3D website you built for them.", False),
    ("3. Send the DM on WhatsApp. The link is already inside the message.", False),
    ("4. When they reply YES, visit their salon for a free overview, then discuss price & sign up.", False),
    ("5. After sending, change Status to: replied / won / paid.", False),
    ("", False),
    ("Your WA: +965 50703252   |   Brand: KB Rewaq Digital", False),
]
for i, (txt, bold) in enumerate(instructions, 1):
    c = ws2.cell(i, 1, txt)
    c.font = Font(bold=bold, size=14 if bold else 11)
    ws2.column_dimensions["A"].width = 100

wb.save("KB_Rewaq_Leads.xlsx")
print("✅ KB_Rewaq_Leads.xlsx created with", len(LEADS), "leads (link embedded, no upfront price)")
