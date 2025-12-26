import json
from google.genai import types # type: ignore
from config import JUDGE_SCHEMA, RUBRIC_TEXT
import time 

def call_judge(client, model, judge_id, question, agent_results):
    time.sleep(2)
    print(f"[*] Judge {judge_id} is scoring...")
    context = f"Question: {question}\n\n"
    for a in agent_results:
        context += f"AGENT: {a['agent_id']}\nANSWER: {a['answer']}\n---\n"

    config = types.GenerateContentConfig(
        system_instruction=f"Rule: Use this Rubric to score agents 1-5:\n{RUBRIC_TEXT}",
        response_mime_type="application/json",
        response_schema=JUDGE_SCHEMA
    )
    response = client.models.generate_content(model=model, config=config, contents=context)
    data = json.loads(response.text)
    data["judge_id"] = judge_id
    return data