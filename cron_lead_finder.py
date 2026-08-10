#!/usr/bin/env python3
# KB Rewaq CRON 1 — lead-finder
# Scans OpenStreetMap (Overpass API) for Kuwait ladies salons/spas/beauty shops,
# enriches (name, area, phone, IG guess), writes a per-client folder under
# D:\KB Rewaq Clients\{slug}\, and pushes the lead to _QUEUE.json for site-builder.
# Runs every 10 min (cronjob). Read-only research — no WhatsApp send.
#
# 2026-08-10 FIX: Google/DDG/Bing all serve anti-bot JS challenges or CAPTCHAs
# to plain urllib fetches (Google "knitsail" challenge, DDG duck CAPTCHA), which
# silently returned 0 leads. Switched data source to OpenStreetMap Overpass API
# (free, static JSON, no CAPTCHA). Salons tagged shop=beauty|hairdresser|cosmetics
# in Kuwait bbox. Men's salons, perfume/supply shops, and businesses that already
# list a website/instagram/facebook are excluded (target = ladies salons with no
# online presence).

import os, json, re, time, datetime, subprocess, sys, urllib.parse, urllib.request

ROOT = r"D:\KB Rewaq Clients"
QUEUE = os.path.join(ROOT, "_QUEUE.json")
SITE_BASE = "https://faizanbashar215.github.io/kb-rewaq-digital"
MAX_NEW_PER_RUN = 50  # matches _QUEUE.json bound so site-builder stays bounded

OVERPASS_SOURCES = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
# Kuwait bbox: lat 28.5-30.1, lon 46.5-48.5
OVERPASS_QUERY = """[out:json][timeout:45];
nwr["shop"~"beauty|hairdresser|cosmetics"](28.5,46.5,30.1,48.5);
out center tags;"""

MEN_RE = re.compile(r"(?i)\b(men|male|gent|gents)\b|رجال|للرجال|رجل|حلاق")
NOISE_RE = re.compile(r"(?i)\b(supplies|perfume|عطور|معدات|equipment|بضائع)\b")

# OSM addr:city (mostly Arabic) -> English display names
AREA_MAP = {
    "السالمية": "Salmiya", "حولي": "Hawally", "Hawalli": "Hawally", "Hawali": "Hawally",
    "العارضية": "Ardiya", "العارضيه": "Ardiya", "الجابرية": "Jabriya", "Jabriya": "Jabriya",
    "Sabah Al Salem": "Sabah Al Salem", "الفنطاس": "Fintas", "سلوى": "Salwa",
    "الدوحة": "Doha", "القبلة": "Qibla", "الشعب": "Shaab", "بنيد القار": "Bneid Al Qar",
    "ام قصر": "Um Qasr", "الزهراء": "Zahra", "الصليبخات": "Sulaibikhat",
}

HEADERS = {"User-Agent": "KB-Rewaq-lead-finder/1.0 (research only)"}


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:40]


def fetch_overpass():
    """Fetch salon elements from Overpass with mirror fallback."""
    payload = urllib.parse.urlencode({"data": OVERPASS_QUERY}).encode()
    for base in OVERPASS_SOURCES:
        try:
            req = urllib.request.Request(base, data=payload, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as r:
                js = json.load(r)
            if js.get("elements"):
                return js["elements"]
        except Exception as e:
            print(f"  ! overpass fetch error ({base.split('/')[2]}): {e}")
    return []


def norm_phone(raw):
    """Normalize a Kuwaiti phone tag -> (digits8, display). Returns ('','') if unusable/masked."""
    if not raw or "*" in raw:
        return "", ""
    d = re.sub(r"\D", "", raw)
    if d.startswith("00965"):
        d = d[5:]
    elif d.startswith("965"):
        d = d[3:]
    elif d.startswith("0"):
        d = d[1:]
    if len(d) == 8 and d.isdigit():
        return d, f"+965 {d[:4]} {d[4:]}"
    return "", ""


def extract_leads(elements):
    """Filter OSM elements to quality ladies-salon leads (no online presence)."""
    seen = set()
    leads = []
    for e in elements:
        t = e.get("tags", {})
        name = (t.get("name") or "").strip()
        if not name:
            continue
        if MEN_RE.search(name) or NOISE_RE.search(name):
            continue
        # already has an online presence -> not a "no website" lead
        if any(t.get(k) for k in ("website", "contact:website", "facebook", "instagram")):
            continue
        phone, disp = norm_phone(t.get("contact:phone") or t.get("phone"))
        city = t.get("addr:city") or t.get("addr:area") or ""
        area = AREA_MAP.get(city, city)
        key = re.sub(r"[^a-z0-9]", "", name.lower())
        if not key or key in seen:
            continue
        seen.add(key)
        leads.append({
            "name_en": name,
            "area_en": area,
            "phone": phone,
            "phone_disp": disp,
            "ig": slugify(name).replace("-", ""),
            "source": "openstreetmap_salon_scan",
        })
    return leads


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
    elements = fetch_overpass()
    if not elements:
        print("[lead-finder] overpass unreachable, aborting run")
        return
    leads = extract_leads(elements)
    print(f"[lead-finder] {datetime.datetime.now():%H:%M} scan saw {len(elements)} OSM elements, "
          f"{len(leads)} ladies-salon candidates (no website)")
    found = 0
    for lead in leads:
        if found >= MAX_NEW_PER_RUN:
            print(f"  ... {len(leads) - found} more candidates remain for next runs (per-run cap {MAX_NEW_PER_RUN})")
            break
        slug = slugify(lead["name_en"])
        if not slug:
            continue
        # skip if folder already exists (already a known client)
        if os.path.isdir(os.path.join(ROOT, slug)):
            continue
        write_client_folder(lead, slug)
        if push_queue(lead, slug):
            found += 1
            print(f"  + new lead: {lead['name_en']} [{slug}] ({lead['area_en'] or 'area?'})")
    print(f"[lead-finder] {datetime.datetime.now():%H:%M} found {found} new quality leads")
    # keep queue bounded
    if os.path.exists(QUEUE):
        q = json.load(open(QUEUE, encoding="utf-8"))
        q["pending"] = q["pending"][-50:]
        json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
