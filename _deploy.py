import json, subprocess, os, sys

BASE = "D:/digitalfirst-agency"
SECFILE = os.path.join(BASE, "secrets.txt")
API = "https://api.github.com"

# read secrets (never print token)
data = {}
with open(SECFILE, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip()

USER = data.get("username", "")
TOKEN = data.get("token", "")
REPO = "kb-rewaq-digital"

if not USER or not TOKEN:
    print("ERROR: username or token missing in secrets.txt")
    sys.exit(1)

AUTH = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}
print(f"[1/5] Creating repo '{REPO}' for user '{USER}' ...")

# 1. create repo
r = subprocess.run(
    ["curl", "-s", "-X", "POST", f"{API}/user/repos",
     "-H", "Authorization: token " + TOKEN,
     "-H", "Accept: application/vnd.github+json",
     "-d", json.dumps({
         "name": REPO,
         "description": "KB Rewaq Digital - 3D websites & marketing for Kuwait businesses",
         "homepage": f"https://{USER}.github.io/{REPO}/",
         "public": True
     })],
    capture_output=True, text=True
)
out = r.stdout
if '"full_name"' in out:
    print("  OK repo created")
else:
    # maybe already exists -> continue
    print("  repo may exist already, continuing. (api msg hidden)")

# 2. git config + commit
print("[2/5] Git commit ...")
subprocess.run(["git", "config", "user.email", "kb.rewaq@local"], cwd=BASE)
subprocess.run(["git", "config", "user.name", USER], cwd=BASE)
subprocess.run(["git", "add", "-A"], cwd=BASE)
subprocess.run(["git", "commit", "-q", "-m", "KB Rewaq Digital 3D site v2.0"], cwd=BASE)

# 3. push
print("[3/5] Pushing to GitHub ...")
subprocess.run(["git", "remote", "remove", "origin"], cwd=BASE)
subprocess.run(["git", "remote", "add", "origin", f"https://{TOKEN}@github.com/{USER}/{REPO}.git"], cwd=BASE)
pr = subprocess.run(["git", "push", "-f", "origin", "main"], cwd=BASE, capture_output=True, text=True)
if pr.returncode != 0:
    print("  PUSH FAILED:", pr.stderr[:200])
    sys.exit(1)
print("  OK pushed")

# 4. enable pages
print("[4/5] Enabling GitHub Pages ...")
r2 = subprocess.run(
    ["curl", "-s", "-X", "PUT", f"{API}/repos/{USER}/{REPO}/pages",
     "-H", "Authorization: token " + TOKEN,
     "-H", "Accept: application/vnd.github+json",
     "-d", json.dumps({"source": {"branch": "main", "path": "/"}})],
    capture_output=True, text=True
)
print("  pages request sent")

print("[5/5] DONE")
print(f"  LIVE SOON: https://{USER}.github.io/{REPO}/")
