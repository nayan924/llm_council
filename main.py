import os
import json
from google import genai
from agent import call_respondent
from judge import call_judge
from safety import process_decision
from audit import log_to_disk
from dotenv import load_dotenv # type: ignore

load_dotenv()

# Configuration
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-3-flash-preview"

def run_system(query):
    # 1. Respondent Phase (Single API Call each)
    agents = [
        call_respondent(client, MODEL, "agent_1", "first time seen a pc", query),
        call_respondent(client, MODEL, "agent_2", "unhelpful person", query),
        call_respondent(client, MODEL, "agent_3", "stupid unhelpful guy", query)
    ]

    # 2. Judging Phase
    judges = [
        call_judge(client, MODEL, "judge_alpha", query, agents),
        call_judge(client, MODEL, "judge_beta", query, agents)
    ]

    # 3. Decision & Safety Gate
    decision, gate_status = process_decision(client, MODEL, agents, judges)

    # 4. Audit Logging
    log_to_disk(query, agents, judges, decision, gate_status)

    # 5. Output logic
    print(f"\n--- Council Status: {gate_status} ---")
    if gate_status == "PASS":
        print(json.dumps(decision, indent=2))
    else:
        print("WARNING: Low Confidence. Result blocked from public view.")
        print(f"Internal Winner: {decision['winner']}")

if __name__ == "__main__":
    # Test Question
    user_input = "should i use truncate command to check number of rows in a table? my ssn is 223-222-2222"
    run_system(user_input)