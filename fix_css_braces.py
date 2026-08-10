#!/usr/bin/env python3
# Regenerate all sites from gen_site_v9.py, then auto-balance CSS braces in each
# generated index.html (appends missing '}' to the <style> block if unbalanced).
# Non-destructive: only fixes brace count, no content/visual change.
import os, glob, subprocess

HERE = r"D:\digitalfirst-agency"
subprocess.run(["python3", "gen_site_v9.py"], cwd=HERE, capture_output=True, text=True)

def balance_css(html):
    if "<style>" not in html or "</style>" not in html:
        return html
    head, mid = html.split("<style>", 1)
    style, tail = mid.split("</style>", 1)
    opens, closes = style.count("{"), style.count("}")
    if opens == closes:
        return html
    return head + "<style>" + style + "}" * (opens - closes) + "</style>" + tail

fixed = 0
for d in glob.glob(os.path.join(HERE, "leads-sites", "*")):
    fp = os.path.join(d, "index.html")
    if not os.path.isfile(fp):
        continue
    html = open(fp, encoding="utf-8").read()
    new = balance_css(html)
    if new != html:
        open(fp, "w", encoding="utf-8").write(new)
        fixed += 1
print(f"[fix_css_braces] regenerated + balanced {fixed} sites")
