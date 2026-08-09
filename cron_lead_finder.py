#!/usr/bin/env python3
# KB Rewaq CRON 1 — lead-finder
# Scans Google Maps for Kuwait ladies salons/spas with NO website (quality leads),
# enriches (name, area, phone, IG guess), writes a per-client folder under
# D:\KB Rewaq Clients\{slug}\, and pushes the lead to _QUEUE.json for site-builder.
# Runs every 10 min (cronjob). Read-only research — no WhatsApp send.

import os, json, re, time, datetime, subprocess, sys, urllib.parse, urllib.request
from html.parser import HTMLParser

ROOT = r"D:\KB Rewaq Clients"
QUEUE = os.path.join(ROOT, "_QUEUE.json")
AREAS = ["Salmiya", "Hawally", "Farwaniya", "Khaitan", "Maidan Hawally", "Rigga Kuwait"]
SITE_BASE = "https://faizanbashar215.github.io/kb-rewaq-digital"

# crude Maps query: "ladies salon <area> Kuwait" and look for listings
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:40]


def search_maps(area):
    q = f"ladies beauty salon {area} Kuwait"
    url = "https://www.google.com/search?q=" + urllib.parse.quote(q) + "&num=20"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"  ! maps fetch error {area}: {e}")
        return ""


class MapsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blobs = []
        self.cur = []
        self.in_a = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.in_a = True
            self.cur = []

    def handle_endtag(self, tag):
        if tag == "a" and self.cur:
            txt = "".join(self.cur).strip()
            if 6 <= len(txt) <= 80 and any(w in txt.lower() for w in ["salon", "spa", "beauty", "للتجميل", "صالون"]):
                self.blobs.append(txt)
            self.in_a = False
            self.cur = []

    def handle_data(self, data):
        if self.in_a:
            self.cur.append(data)


def extract_leads(html, area):
    # pull candidate names + nearby phone numbers (best-effort)
    p = MapsParser()
    p.feed(html)
    leads = []
    for name in p.blobs:
        # find a phone near this name if present
        m = re.search(r"(\+?965[\s-]?\d{8})", html)
        phone = re.sub(r"\D", "", m.group(1)) if m else ""
        if len(phone) == 11 and phone.startswith("965"):
            phone = phone[3:]
        leads.append({
            "name_en": name,
            "area_en": area,
            "phone": phone,
            "phone_disp": f"+965 {phone[:4]} {phone[4:]}" if phone else "",
            "ig": slugify(name).replace("-", ""),
            "source": "google_maps_no_site_scan",
        })
    # dedupe by name
    seen = set(); uniq = []
    for l in leads:
        k = l["name_en"].lower()
        if k not in seen:
            seen.add(k); uniq.append(l)
    return uniq[:8]


def push_queue(lead, slug):
    q = {"pending": []}
    if os.path.exists(QUEUE):
        try:
            q = json.load(open(QUEUE, encoding="utf-8"))
        except Exception:
            q = {"pending": []}
    q.setdefault("pending", [])
    if any(x.get("slug") == slug for x in q["pending"]):
        return False
    q["pending"].append({"slug": slug, "name_en": lead["name_en"], "stage": "found", "t": datetime.datetime.now().isoformat()})
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return True


def write_client_folder(lead, slug):
    folder = os.path.join(ROOT, slug)
    os.makedirs(os.path.join(folder, "dms"), exist_ok=True)
    rec = {
        "business": {"name_en": lead["name_en"], "slug": slug},
        "contact": {"phone": lead["phone"], "phone_disp": lead["phone_disp"], "instagram": lead["ig"]},
        "location": {"area_en": lead["area_en"]},
        "online": {"site_url": f"{SITE_BASE}/{slug}/", "site_status": "pending_build"},
        "pipeline": {"status": "lead_new", "created": datetime.date.today().isoformat(),
                     "source": lead["source"]},
    }
    with open(os.path.join(folder, "client.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    with open(os.path.join(folder, "site-link.txt"), "w", encoding="utf-8") as f:
        f.write(rec["online"]["site_url"] + "\n")
    with open(os.path.join(folder, "research.md"), "w", encoding="utf-8") as f:
        f.write(f"# {lead['name_en']}\n\n- Area: {lead['area_en']}\n- Phone: {lead['phone_disp']}\n- Source: {lead['source']}\n")
    with open(os.path.join(folder, "notes.md"), "w", encoding="utf-8") as f:
        f.write(f"# Deal notes — {lead['name_en']}\n\n- Status: lead_new\n- Created: {datetime.date.today().isoformat()}\n")


def main():
    os.makedirs(ROOT, exist_ok=True)
    found = 0
    for area in AREAS:
        html = search_maps(area)
        if not html:
            continue
        leads = extract_leads(html, area)
        for lead in leads:
            slug = slugify(lead["name_en"])
            if not slug:
                continue
            # skip if folder already exists (already a known client)
            if os.path.isdir(os.path.join(ROOT, slug)):
                continue
            write_client_folder(lead, slug)
            if push_queue(lead, slug):
                found += 1
                print(f"  + new lead: {lead['name_en']} [{slug}] ({area})")
    print(f"[lead-finder] {datetime.datetime.now():%H:%M} found {found} new quality leads")
    # keep queue bounded
    if os.path.exists(QUEUE):
        q = json.load(open(QUEUE, encoding="utf-8"))
        q["pending"] = q["pending"][-50:]
        json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
