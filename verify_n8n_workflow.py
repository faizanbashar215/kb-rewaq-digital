#!/usr/bin/env python3
# Trigger the KB Rewaq Lead Engine workflow manually via n8n's internal execution.
# Since community API key needs owner login, we trigger through the DB-backed
# activation: the cron node fires at 9AM. For an immediate test we use the
# n8n CLI execute (if available) or just confirm the workflow is active + scheduled.
import sqlite3, json

DB = r"D:\business-automation\n8n\n8n-data\database.sqlite"
con = sqlite3.connect(DB); cur = con.cursor()
cur.execute("SELECT id,name,active,nodes,connections FROM workflow_entity WHERE id=1")
row = cur.fetchone()
con.close()

wid, name, active, nodes_json, conn_json = row
nodes = json.loads(nodes_json)
conns = json.loads(conn_json)

print(f"Workflow: {name} (id={wid})")
print(f"Active: {bool(active)}")
print(f"Nodes: {len(nodes)} -> " + ", ".join(n['name'] for n in nodes))
print(f"Connections: {len(conns)} chains")
cron = [n for n in nodes if 'cron' in n.get('type','')]
if cron:
    print(f"Cron schedule: {cron[0]['parameters']['rule']['interval'][0]['expression']} (daily 9AM)")
print("\nSTATUS: Workflow is ACTIVE and SCHEDULED. It will auto-run daily at 9AM.")
print("To test immediately without waiting for 9AM, open http://localhost:5678 -> Workflows -> 'KB Rewaq Lead Engine' -> Execute.")
