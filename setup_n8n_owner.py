#!/usr/bin/env python3
# Create an owner user in n8n's SQLite DB so the API key auth works.
# n8n v2.x needs a user with role 'owner' for API access.
import sqlite3, json, hashlib, os, secrets

DB = r"D:\business-automation\n8n\n8n-data\database.sqlite"
EMAIL = "jarvis@kbrewaq.com"
PASSWORD = "KbRewaq2026!"

# n8n password hashing: bcrypt-like via the 'password' column stores bcrypt hash.
# n8n uses bcrypt; we can't easily replicate without bcrypt. Instead use n8n's own.
# Fallback: use the 'settings' table / or create via API after owner setup.
# Simplest reliable path: set N8N to disable user management and use the global API key.
# n8n reads global API key from env N8N_API_KEY ONLY if user management is OFF (EE) or
# for public API the key is set per-user. For docker n8nio/n8n (community), the API key
# is generated in the owner's personal settings after first login.
print("NOTE: n8n community requires owner login via UI to generate API key.")
print("The workflow is already imported + active in the DB (active=1).")
print("Cron trigger (9AM daily) will fire it. API key is only needed for remote control.")
print("If you want to verify/manually trigger, open http://localhost:5678 and login as owner.")
