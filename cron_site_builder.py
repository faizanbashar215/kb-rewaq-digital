#!/usr/bin/env python3
# KB Rewaq CRON 2 — site-builder
# Pulls pending leads from _QUEUE.json, builds a v9-style site per client,
# deploys to GitHub Pages (root copy), updates client.json + site-link.txt,
# then hands the lead to whatsapp-dealmaker (marks stage=site_ready).
# Runs every 15 min (cronjob).

import os, json, datetime, subprocess, sys, shutil, urllib.request

ROOT = r"D:\KB Rewaq Clients"
QUEUE = os.path.join(ROOT, "_QUEUE.json")
REPO = r"D:\digitalfirst-agency"
SITE_BASE = "https://faizanbashar215.github.io/kb-rewaq-digital"

# minimal lead schema for gen_site (v9 expects many fields; we synthesize safe defaults)
DEFAULT_TEAM = [("Studio", "Specialist", "ستوديو")]
DEFAULT_SERVICES = [
    ("Haircut & Styling", "قص وتصفيف", 8, ["Cut", "Style", "Blowdry"]),
    ("Hair Color", "صبغ الشعر", 25, ["Full color", "Highlights"]),
    ("Facial", "فيشل", 12, ["Cleanse", "Mask"]),
    ("Manicure & Pedicure", "مانيكير وباديكير", 10, ["Gel", "Spa"]),
    ("Bridal Makeup", "مكياج عروس", 60, ["HD", "Trial"]),
    ("Massage", "مساج", 18, ["Relax", "Aroma"]),
]
DEFAULT_PACKAGES = [
    ("Glow Package", "باقة الإشراق", 25, "Facial + Manicure + Pedicure"),
    ("Royal Package", "باقة ملكية", 60, "Hair + Facial + Massage"),
    ("Bridal Package", "باقة العروس", 150, "Bridal Makeup + Hair + Spa"),
]
DEFAULT_REVIEWS = [
    ("Happy Client", "Beautiful work, very professional."),
    ("Loyal Customer", "My go-to salon now."),
]


def build_lead_dict(rec):
    slug = rec["business"]["slug"]
    name = rec["business"]["name_en"]
    phone = rec["contact"].get("phone", "")
    ig = rec["contact"].get("instagram", slug)
    area = rec["location"].get("area_en", "Kuwait")
    return {
        "slug": slug,
        "name_en": name,
        "name_ar": name,  # Arabic can be enriched later by Faizan
        "phone": phone,
        "phone_disp": rec["contact"].get("phone_disp", f"+965 {phone}"),
        "area_en": area,
        "area_ar": area,
        "tag_en": "Beauty, Wellness & Beyond",
        "tag_ar": "الجمال والعافية",
        "accent": "#e8b4d4",
        "ig": ig,
        "lat": 29.33,
        "lon": 48.07,
        "clients": 0,
        "services": DEFAULT_SERVICES,
        "packages": DEFAULT_PACKAGES,
        "team": DEFAULT_TEAM,
        "reviews": DEFAULT_REVIEWS,
    }


def main():
    if not os.path.exists(QUEUE):
        print("[site-builder] no queue yet")
        return
    q = json.load(open(QUEUE, encoding="utf-8"))
    pending = q.get("pending", [])
    built = 0
    for item in pending:
        if item.get("stage") not in ("found", "queued"):
            continue
        slug = item["slug"]
        cpath = os.path.join(ROOT, slug, "client.json")
        if not os.path.exists(cpath):
            continue
        rec = json.load(open(cpath, encoding="utf-8"))
        lead = build_lead_dict(rec)
        # write a temp LEADS module for gen_site reuse
        mod = os.path.join(REPO, "_tmp_lead.py")
        with open(mod, "w", encoding="utf-8") as f:
            f.write("LEADS=[\n" + repr(lead) + "\n]\n")
        try:
            build_one(lead, REPO)
            # deploy: copy leads-sites/<slug> to repo root
            src = os.path.join(REPO, "leads-sites", slug)
            dst = os.path.join(REPO, slug)
            if os.path.isdir(src):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                # git add + commit + push
                subprocess.run(["git", "add", slug], cwd=REPO)
                subprocess.run(["git", "commit", "-m", f"auto: build site for {slug}"],
                               cwd=REPO, capture_output=True)
                push(REPO)
                built += 1
                # update client + queue stage
                rec["online"]["site_status"] = "live"
                rec["online"]["site_url"] = f"{SITE_BASE}/{slug}/"
                json.dump(rec, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                with open(os.path.join(ROOT, slug, "site-link.txt"), "w", encoding="utf-8") as ff:
                    ff.write(rec["online"]["site_url"] + "\n")
                item["stage"] = "site_ready"
                print(f"  + built+deployed: {slug} -> {rec['online']['site_url']}")
        except Exception as e:
            print(f"  ! build failed {slug}: {e}")
        finally:
            if os.path.exists(mod):
                os.remove(mod)
    json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[site-builder] {datetime.datetime.now():%H:%M} built {built} sites")


def build_one(lead, repo):
    # import gen_site_v9's gen() by swapping its LEADS via env-free monkeypatch
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen9", os.path.join(repo, "gen_site_v9.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    g.LEADS = [lead]
    g.AI[lead["slug"]] = g.GAL[0]  # ensure hero exists for a brand-new slug
    g.gen(lead)


def push(repo):
    tok = os.environ.get("GH_TOKEN", "")
    if tok:
        subprocess.run(["git", "remote", "set-url", "origin",
                        f"https://x-access-token:{tok}@github.com/faizanbashar215/kb-rewaq-digital.git"],
                       cwd=repo, capture_output=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=repo, capture_output=True)
    if tok:
        subprocess.run(["git", "remote", "set-url", "origin",
                        "https://faizanbashar215@github.com/faizanbashar215/kb-rewaq-digital.git"],
                       cwd=repo, capture_output=True)


if __name__ == "__main__":
    main()
