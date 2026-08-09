#!/usr/bin/env python3
# KB Rewaq git push helper — reads GH_TOKEN from .env (never inline on CLI).
# Usage: python3 git_push.py "commit message"
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(HERE, ".env")
token = ""
if os.path.exists(env_path):
    for line in open(env_path, encoding="utf-8"):
        if line.startswith("GH_TOKEN="):
            token = line.strip().split("=", 1)[1].strip()

msg = sys.argv[1] if len(sys.argv) > 1 else "kb-rewaq update"
repo = "https://github.com/faizanbashar215/kb-rewaq-digital.git"

subprocess.run(["git", "add", "-A"], cwd=HERE)
subprocess.run(["git", "commit", "-m", msg], cwd=HERE, capture_output=True)
if token:
    subprocess.run(["git", "remote", "set-url", "origin",
                    f"https://x-access-token:{token}@github.com/faizanbashar215/kb-rewaq-digital.git"],
                   cwd=HERE, capture_output=True)
r = subprocess.run(["git", "push", "origin", "main"], cwd=HERE, capture_output=True, text=True)
# always scrub inline token back to plain remote
subprocess.run(["git", "remote", "set-url", "origin", "https://faizanbashar215@github.com/faizanbashar215/kb-rewaq-digital.git"],
               cwd=HERE, capture_output=True)
print("PUSH:", "ok" if r.returncode == 0 else r.stderr[-200:])
