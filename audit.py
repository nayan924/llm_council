import json
import datetime

def log_to_disk(query, agents, judges, decision, status):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "agents": agents,
        "judges": judges,
        "final_decision": decision,
        "gate": status
    }
    with open("council_audit.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    print("[!] Audit log entry saved.")