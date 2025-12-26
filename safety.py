import json
from google.genai import types # type: ignore
from config import WARDEN_SCHEMA
import time

def run_warden(client, model, text):
    time.sleep(2)
    print("[!] Warden is checking for safety...")
    config = types.GenerateContentConfig(
        system_instruction="Check for PII, illegal content, or danger.",
        response_mime_type="application/json",
        response_schema=WARDEN_SCHEMA
    )
    resp = client.models.generate_content(model=model, config=config, contents=text)
    return json.loads(resp.text)

def process_decision(client, model, agents, judgments):
    # 1. Calculate Total Scores
    # Dictionary to hold raw sums: {'agent_1': 0, ...}
    raw_scores = {a['agent_id']: 0 for a in agents}
    
    for j in judgments:
        scores_obj = j['scores'] # keys: agent_1, agent_2...
        for agent_id, metrics in scores_obj.items():
            # metrics is {'accuracy': 5, 'clarity': 4...}
            # Simple Sum: 5+4+5+5 = 19
            raw_scores[agent_id] += sum(metrics.values())

    # 2. Normalize Scores (0.0 to 1.0)
    # Max score = (Judges * Criteria * Max_Points)
    # Example: 2 judges * 4 criteria * 5 points = 40 max
    max_possible = len(judgments) * 4 * 5
    
    normalized_scores = {}
    for aid, score in raw_scores.items():
        normalized_scores[aid] = round(score / max_possible, 2)

    # 3. Determine Winner
    winner_id = max(normalized_scores, key=normalized_scores.get)
    confidence = normalized_scores[winner_id] # e.g., 0.95
    
    winner_text = next(a['answer'] for a in agents if a['agent_id'] == winner_id)

    # 4. Warden Safety Check
    warden_result = run_warden(client, model, winner_text)

    decision = {
        "winner": winner_id,
        "final_answer": winner_text,
        "confidence": confidence,
        "raw_score": raw_scores[winner_id],
        "warden_result": warden_result,
        "citations": [f"Ranked highest with {confidence*100}% rubric score"],
        "risks": []
    }

    # 5. Final Gate
    if warden_result["is_safe"] and confidence > 0.75:
        status = "PASS"
    else:
        status = "BLOCK/REVIEW"
        if not warden_result["is_safe"]:
            decision["risks"].append(f"Warden Alert: {warden_result['reason']}")
        if confidence <= 0.75:
            decision["risks"].append("Low Rubric Score")

    return decision, status