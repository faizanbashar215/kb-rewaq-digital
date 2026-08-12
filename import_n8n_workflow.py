#!/usr/bin/env python3
# Import the KB Rewaq Lead Engine workflow into the running n8n (Docker) via REST API.
import json, urllib.request, urllib.error

API = "http://localhost:5678/api/v1/workflows"
KEY = "admin-api-key-12345"

# Load our workflow definition
wf = json.load(open(r"D:\digitalfirst-agency\n8n_lead_engine.json", encoding="utf-8"))

# n8n v1 API wants: { name, nodes, connections, settings, active }
payload = {
    "name": wf["name"],
    "nodes": wf["nodes"],
    "connections": wf["connections"],
    "settings": wf.get("settings", {}),
    "active": False,  # import inactive, we activate after verifying
}

req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                             headers={"X-N8N-API-KEY": KEY, "Content-Type": "application/json"},
                             method="POST")
try:
    resp = urllib.request.urlopen(req, timeout=30)
    out = json.loads(resp.read().decode())
    print("IMPORT status:", resp.status)
    print("Workflow id:", out.get("id"))
    print("Name:", out.get("name"))
    print("Nodes:", len(out.get("nodes", [])))
    # save id for activation step
    json.dump({"id": out.get("id")}, open(r"D:\digitalfirst-agency\n8n_workflow_id.json", "w"))
    print("Saved workflow id -> n8n_workflow_id.json")
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code, e.read().decode()[:500])
except Exception as e:
    print("ERR:", e)
