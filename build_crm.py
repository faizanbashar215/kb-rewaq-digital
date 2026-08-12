#!/usr/bin/env python3
# Build CRM master JSON from existing client.json files in D:/KB Rewaq Clients
# Plus generate a self-contained CRM dashboard HTML.
import os, json, glob, sys

# shared DM engine (unique human DMs, correct site URLs)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dm_engine import compose_dm, site_url_for

CRM = os.environ.get("CLIENTS_DIR", r"D:\KB Rewaq Clients")
MASTER = os.path.join(CRM, "crm_master.json")
DASH = os.environ.get("AGENCY_DIR", r"D:\digitalfirst-agency") + r"\crm_dashboard.html"

leads = []
for d in sorted(glob.glob(os.path.join(CRM, "*/"))):
    cj = os.path.join(d, "client.json")
    if not os.path.isfile(cj):
        continue
    try:
        j = json.load(open(cj, encoding="utf-8"))
    except Exception:
        continue
    biz = j.get("business", {})
    con = j.get("contact", {})
    loc = j.get("location", {})
    onl = j.get("online", {})
    pipe = j.get("pipeline", {})
    slug = biz.get("slug", os.path.basename(d.rstrip("/\\")))
    name = biz.get("name_en", "")
    area = loc.get("area_en", "")
    # correct demo site URL (always fresh_sites/<slug>/)
    site_url = site_url_for(slug)
    # unique human DM from shared engine
    dm_text = compose_dm(name, area, slug, len(leads))
    # real phone if present, else boss fallback
    raw_phone = con.get("phone", "") or ""
    phone = raw_phone if raw_phone else "96550703252"
    phone_disp = (con.get("phone_disp", "") or ("+" + raw_phone if raw_phone else "+96550703252"))
    leads.append({
        "slug": slug,
        "name_en": name,
        "name_ar": biz.get("name_ar", ""),
        "phone": phone,
        "phone_disp": phone_disp,
        "area": area,
        "site_url": site_url,
        "site_status": onl.get("site_status", "live_fresh"),
        "dm_text": dm_text,
        "status": pipe.get("status", "lead_new"),
        "notes": pipe.get("notes", ""),
        "created": pipe.get("created", "2026-08-11"),
        "source": pipe.get("source", "osm_fresh_scan"),
        "last_touch": pipe.get("last_touch", ""),
    })

# status defaults if missing
STATUS_ORDER = ["lead_new", "contacted", "replied", "won", "paid", "lost"]
for l in leads:
    if not l["status"] or l["status"] not in STATUS_ORDER:
        l["status"] = "lead_new"
    if not l["dm_text"]:
        l["dm_text"] = f"Hey {l['name_en']}. Jarvis from KB Rewaq Digital. I build automation for Kuwait salons."
    # sanitize: only strip newlines (JSON handles quotes/apostrophes natively)
    for k in ("name_en", "name_ar", "area", "dm_text", "notes"):
        if isinstance(l.get(k), str):
            l[k] = l[k].replace("\n", " ").replace("\r", "")

json.dump({"leads": leads, "updated": "2026-08-11"}, open(MASTER, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"MASTER built: {len(leads)} leads -> {MASTER}")

# ---- Dashboard HTML (loads LEADS via fetch, no inline injection) ----
DASH_JSON = os.path.join(CRM, "crm_leads.json")
json.dump(leads, open(DASH_JSON, "w", encoding="utf-8"), ensure_ascii=False)
# also write a copy next to the dashboard (server root) so fetch() resolves
json.dump(leads, open(os.path.join(os.path.dirname(DASH), "crm_leads.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(f"LEADS json -> {DASH_JSON}")

html = r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KB Rewaq CRM — Fresh Leads</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0f1115;color:#e8e8e8;padding:20px}}
h1{{font-size:1.5rem;margin-bottom:4px;color:#fff}}
.sub{{opacity:.6;font-size:.85rem;margin-bottom:18px}}
.controls{{margin-bottom:16px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
.controls input,.controls select{{padding:8px 12px;border-radius:8px;border:1px solid #2a2d35;background:#1a1d24;color:#fff}}
table{{width:100%;border-collapse:collapse;background:#15181f;border-radius:10px;overflow:hidden}}
th,td{{padding:12px 10px;text-align:left;border-bottom:1px solid #23262f;font-size:.85rem;vertical-align:top}}
th{{background:#1c2230;color:#9fb3ff;font-weight:600;position:sticky;top:0}}
tr:hover{{background:#1a1e27}}
.name{{font-weight:600;color:#fff}}
.ar{{opacity:.55;font-size:.75rem}}
a.dm{{display:inline-block;padding:6px 12px;background:#25D366;color:#0a0a0a;border-radius:16px;font-weight:600;text-decoration:none;font-size:.78rem}}
a.site{{color:#6fb3ff;text-decoration:none}}
.st{{padding:5px 10px;border-radius:14px;font-size:.75rem;font-weight:600;border:none;cursor:pointer}}
.st.lead_new{{background:#3a3f4d;color:#cfd3dc}}
.st.contacted{{background:#1e3a5f;color:#7fb8ff}}
.st.replied{{background:#5a4a1e;color:#ffd76f}}
.st.won{{background:#1e5a2f;color:#7dffa0}}
.st.paid{{background:#2f5a1e;color:#a0ff7d}}
.st.lost{{background:#5a1e1e;color:#ff8a8a}}
.notes{{width:160px;background:#1a1d24;border:1px solid #2a2d35;color:#fff;border-radius:6px;padding:6px;font-size:.78rem;resize:vertical}}
.cnt{{opacity:.6;font-size:.8rem;margin-left:auto}}
</style></head><body>
<h1>KB Rewaq CRM</h1>
<div class="sub">Fresh Kuwait salon leads — automation outreach tracker</div>
<div class="controls">
<input id="q" placeholder="Search name / area..." onkeyup="render()">
<select id="f" onchange="render()">
<option value="">All statuses</option>
<option value="lead_new">New</option><option value="contacted">Contacted</option>
<option value="replied">Replied</option><option value="won">Won</option>
<option value="paid">Paid</option><option value="lost">Lost</option>
</select>
<span class="cnt" id="cnt"></span>
</div>
<table><thead><tr>
<th>#</th><th>Business</th><th>Area</th><th>Phone</th><th>Demo Site</th><th>DM</th><th>Status</th><th>Notes</th>
</tr></thead><tbody id="tb"></tbody></table>
<script>
let LEADS = [];
const STATUSES = ["lead_new","contacted","replied","won","paid","lost"];
const LABEL = {{lead_new:"New",contacted:"Contacted",replied:"Replied",won:"Won",paid:"Paid",lost:"Lost"}};
function save(){{ try{{ localStorage.setItem('kb_crm', JSON.stringify(LEADS)); }}catch(e){{}} }}
function render(){{
  const q=(document.getElementById('q').value||'').toLowerCase();
  const f=document.getElementById('f').value;
  const tb=document.getElementById('tb'); tb.innerHTML='';
  let n=0;
  LEADS.forEach((l,i)=>{{
    if(q && !(l.name_en.toLowerCase().includes(q)||(l.area||'').toLowerCase().includes(q))) return;
    if(f && l.status!==f) return;
    n++;
    const tr=document.createElement('tr');
    const dmUrl='https://wa.me/'+l.phone+'?text='+encodeURIComponent(l.dm_text);
    tr.innerHTML=`
      <td>${{n}}</td>
      <td><div class="name">${{l.name_en}}</div><div class="ar">${{l.name_ar}}</div></td>
      <td>${{l.area||'-'}}</td>
      <td>${{l.phone_disp}}</td>
      <td>${{l.site_url?`<a class="site" href="${{l.site_url}}" target="_blank">Open</a>`:'-'}}</td>
      <td><a class="dm" href="${{dmUrl}}" target="_blank">Click to DM</a></td>
      <td><select class="st ${{l.status}}" onchange="setStatus(${{i}},this.value)">
        ${{STATUSES.map(s=>`<option value="${{s}}" ${{s===l.status?'selected':''}}>${{LABEL[s]}}</option>`).join('')}}
      </select></td>
      <td><textarea class="notes" onchange="setNotes(${{i}},this.value)">${{l.notes||''}}</textarea></td>`;
    tb.appendChild(tr);
  }});
  document.getElementById('cnt').textContent=n+' / '+LEADS.length+' leads';
}}
function setStatus(i,v){{LEADS[i].status=v;save();render();}}
function setNotes(i,v){{LEADS[i].notes=v;save();}}
fetch('crm_leads.json').then(r=>r.json()).then(d=>{{LEADS=d;render();}}).catch(e=>{{
  document.body.insertAdjacentHTML('beforeend','<p style="color:red">Failed to load crm_leads.json: '+e+'</p>');
}});
</script></body></html>"""
open(DASH, "w", encoding="utf-8").write(html.replace("{{", "{").replace("}}", "}"))
print(f"DASHBOARD built -> {DASH}")

