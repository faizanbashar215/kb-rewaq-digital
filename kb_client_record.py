#!/usr/bin/env python3
# KB Rewaq Clients -> local CRM-lite on D:\
# Reads LEADS from gen_site_v9.py and writes a structured record per client under
# D:\KB Rewaq Clients\<slug>\, plus a master _INDEX.csv for fast lookup.
import os, json, csv, datetime
from gen_site_v9 import LEADS  # LEADS defines all client data

ROOT = r"D:\KB Rewaq Clients"
SITE_BASE = "https://faizanbashar215.github.io/kb-rewaq-digital"
TODAY = datetime.date.today().isoformat()

# Old 5 leads already got an earlier demo (boss said ignore them for outreach,
# but we keep them in the record for future deal lookup).
DEMO_SENT_EARLIER = {"midyaf", "looknoor", "monya", "royaljasmine", "larene"}


def slug_folder(slug):
    return slug


def build_client(l):
    slug = l["slug"]
    services = [
        {"en": s[0], "ar": s[1], "price_kd": s[2], "items": s[3]}
        for s in l["services"]
    ]
    packages = [
        {"en": p[0], "ar": p[1], "price_kd": p[2], "desc": p[3]}
        for p in l["packages"]
    ]
    team = [{"name": t[0], "role": t[1], "name_ar": t[2]} for t in l["team"]]
    reviews = [{"who": r[0], "text": r[1]} for r in l["reviews"]]
    status = "demo_sent_earlier" if slug in DEMO_SENT_EARLIER else "lead_new"
    rec = {
        "business": {
            "name_en": l["name_en"],
            "name_ar": l["name_ar"],
            "slug": slug,
        },
        "contact": {
            "phone": l["phone"],
            "phone_disp": l["phone_disp"],
            "instagram": l["ig"],
            "whatsapp_url": f"https://wa.me/{l['phone']}",
        },
        "location": {
            "area_en": l["area_en"],
            "area_ar": l["area_ar"],
            "lat": l["lat"],
            "lon": l["lon"],
            "maps_url": f"https://www.google.com/maps/search/?api=1&query={l['lat']},{l['lon']}",
        },
        "brand": {
            "tagline_en": l["tag_en"],
            "tagline_ar": l["tag_ar"],
            "accent": l["accent"],
        },
        "stats": {"clients": l["clients"]},
        "services": services,
        "packages": packages,
        "team": team,
        "reviews": reviews,
        "online": {
            "site_url": f"{SITE_BASE}/{slug}/",
            "site_status": "live_v9_advanced",
        },
        "pipeline": {
            "status": status,
            "created": TODAY,
            "last_touch": "",
            "next_action": "",
            "owner_response": "",
            "deal_value_kwd": "",
            "notes": "",
        },
        "source": "KB Rewaq lead research 2026-08 (Kuwait ladies salons/spas)",
    }
    return rec


def write_client(l):
    rec = build_client(l)
    slug = l["slug"]
    folder = os.path.join(ROOT, slug_folder(slug))
    os.makedirs(folder, exist_ok=True)
    os.makedirs(os.path.join(folder, "dms"), exist_ok=True)

    # structured JSON
    with open(os.path.join(folder, "client.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)

    # live site link
    with open(os.path.join(folder, "site-link.txt"), "w", encoding="utf-8") as f:
        f.write(rec["online"]["site_url"] + "\n")

    # research notes (auto-seeded from data)
    with open(os.path.join(folder, "research.md"), "w", encoding="utf-8") as f:
        f.write(f"# {l['name_en']} ({l['name_ar']})\n\n")
        f.write(f"- **Area:** {l['area_en']} ({l['area_ar']})\n")
        f.write(f"- **Phone:** {l['phone_disp']}\n")
        f.write(f"- **Instagram:** @{l['ig']}\n")
        f.write(f"- **Clients served:** ~{l['clients']}\n")
        f.write(f"- **Tagline:** {l['tag_en']} / {l['tag_ar']}\n\n")
        f.write("## Services\n")
        for s in rec["services"]:
            f.write(f"- {s['en']} ({s['ar']}) — {s['price_kd']} KD\n")
        f.write("\n## Packages\n")
        for p in rec["packages"]:
            f.write(f"- {p['en']} ({p['ar']}) — {p['price_kd']} KD — {p['desc']}\n")
        f.write("\n## Team\n")
        for t in rec["team"]:
            f.write(f"- {t['name']} ({t['name_ar']}) — {t['role']}\n")
        f.write(f"\n## Live site\n{rec['online']['site_url']}\n")

    # deal notes placeholder
    with open(os.path.join(folder, "notes.md"), "w", encoding="utf-8") as f:
        f.write(f"# Deal notes — {l['name_en']}\n\n")
        f.write(f"- Status: {rec['pipeline']['status']}\n")
        f.write(f"- Created: {TODAY}\n")
        f.write(f"- Last touch: \n")
        f.write(f"- Next action: \n")
        f.write(f"- Owner response: \n")
        f.write(f"- Deal value (KWD): \n\n")
        f.write("## Follow-up log\n\n")

    # DM folder README
    with open(os.path.join(folder, "dms", "README.md"), "w", encoding="utf-8") as f:
        f.write("# WhatsApp DM drafts & history\n\n")
        f.write("Save each DM as `dm_YYYY-MM-DD.txt` (draft + sent copy).\n")


def write_index():
    path = os.path.join(ROOT, "_INDEX.csv")
    cols = [
        "business_en", "business_ar", "slug", "folder", "area_en",
        "phone_disp", "instagram", "services", "packages", "clients",
        "site_url", "status", "created", "last_touch", "next_action",
        "deal_value_kwd",
    ]
    lines = [cols]
    for l in LEADS:
        slug = l["slug"]
        rec = build_client(l)
        lines.append([
            l["name_en"], l["name_ar"], slug, slug, l["area_en"],
            l["phone_disp"], l["ig"], len(rec["services"]),
            len(rec["packages"]), l["clients"],
            rec["online"]["site_url"], rec["pipeline"]["status"],
            TODAY, "", "", "",
        ])
    # Robust against Excel lock: write to .tmp then atomic replace.
    # If still locked (Excel open), fall back to a timestamped copy.
    import io
    buf = io.StringIO()
    csv.writer(buf).writerows(lines)
    content = buf.getvalue()
    try:
        with open(path + ".tmp", "w", encoding="utf-8", newline="") as f:
            f.write(content)
        os.replace(path + ".tmp", path)
    except PermissionError:
        import datetime as _dt
        fallback = os.path.join(ROOT, f"_INDEX_{_dt.datetime.now():%Y%m%d-%H%M%S}.csv")
        with open(fallback, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print(f"  ! _INDEX.csv locked (Excel open) -> wrote {os.path.basename(fallback)} instead")


def main():
    os.makedirs(ROOT, exist_ok=True)
    # root README
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("# KB Rewaq Clients — Local CRM\n\n")
        f.write(f"Generated: {TODAY}\n\n")
        f.write("Each client has a folder named by slug containing:\n")
        f.write("- `client.json` — all structured details\n")
        f.write("- `site-link.txt` — live GitHub Pages URL\n")
        f.write("- `research.md` — services, packages, team, location\n")
        f.write("- `notes.md` — deal pipeline + follow-up log\n")
        f.write("- `dms/` — WhatsApp DM drafts/history (dm_YYYY-MM-DD.txt)\n\n")
        f.write("`_INDEX.csv` is the master sheet — open in Excel and filter by status/area.\n")
        f.write("To find any client fast: search this folder or grep _INDEX.csv.\n")

    for l in LEADS:
        write_client(l)
        print(f"  + {l['name_en']}  [{l['slug']}]")
    write_index()
    print(f"\nDone. {len(LEADS)} client records written to {ROOT}")
    print(f"Master index: {os.path.join(ROOT, '_INDEX.csv')}")


if __name__ == "__main__":
    main()
