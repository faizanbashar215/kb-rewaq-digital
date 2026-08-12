#!/usr/bin/env python3
# Rebuild n8n_lead_engine.json WITHOUT node 'id' fields (n8n generates them on import).
# Also strip connections that reference ids; n8n matches by node name.
import json

src = json.load(open(r"D:\digitalfirst-agency\n8n_lead_engine.json", encoding="utf-8"))
for n in src["nodes"]:
    n.pop("id", None)          # let n8n assign
    n.pop("webhookId", None)
out = {
    "name": src["name"],
    "nodes": src["nodes"],
    "connections": src["connections"],
    "active": False,
    "settings": src.get("settings", {}),
    "versionId": src.get("versionId"),
}
json.dump(out, open(r"D:\digitalfirst-agency\n8n_lead_engine_noid.json", "w", encoding="utf-8"), indent=2)
print("Rebuilt without ids -> n8n_lead_engine_noid.json, nodes:", len(out["nodes"]))
