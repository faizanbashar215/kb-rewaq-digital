#!/usr/bin/env python3
# Insert the KB Rewaq Lead Engine workflow directly into n8n's SQLite DB.
# n8n stores workflows in the 'workflow_entity' table as JSON columns.
import sqlite3, json, uuid

DB = r"D:\business-automation\n8n\n8n-data\database.sqlite"
wf = json.load(open(r"D:\digitalfirst-agency\n8n_lead_engine_noid.json", encoding="utf-8"))

# n8n workflow_entity columns (v2.x):
# id, name, active, nodes, connections, settings, createdAt, updatedAt, versionId, ...
nodes_json = json.dumps(wf["nodes"])
conn_json = json.dumps(wf["connections"])
settings_json = json.dumps(wf.get("settings", {}))
version_id = wf.get("versionId") or uuid.uuid4().hex
wid = 1  # first workflow

con = sqlite3.connect(DB)
cur = con.cursor()
# check if table exists / has rows
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workflow_entity'")
if not cur.fetchone():
    print("ERROR: workflow_entity table not found")
    con.close(); exit(1)
cur.execute("SELECT COUNT(*) FROM workflow_entity WHERE id=?", (wid,))
exists = cur.fetchone()[0]
if exists:
    print(f"Workflow id {wid} already exists, skipping insert (will update).")
    cur.execute("""UPDATE workflow_entity SET name=?, active=?, nodes=?, connections=?, settings=?, versionId=?, updatedAt=datetime('now') WHERE id=?""",
                (wf["name"], 0, nodes_json, conn_json, settings_json, version_id, wid))
else:
    cur.execute("""INSERT INTO workflow_entity (id, name, active, nodes, connections, settings, versionId, createdAt, updatedAt)
                   VALUES (?,?,?,?,?,?,?,datetime('now'),datetime('now'))""",
                (wid, wf["name"], 0, nodes_json, conn_json, settings_json, version_id))
con.commit()
con.close()
print(f"Workflow inserted/updated: id={wid} name='{wf['name']}' nodes={len(wf['nodes'])}")
print("Restart n8n container to load it.")
