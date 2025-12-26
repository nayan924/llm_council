import json
from google.genai import types # type: ignore
from config import AGENT_SCHEMA
import time


def call_respondent(client, model, agent_id, persona, question):
    time.sleep(2)
    print(f"[*] Agent {agent_id} is generating answer...")
    config = types.GenerateContentConfig(
        system_instruction=f"Persona: {persona}. Provide a direct answer.",
        response_mime_type="application/json",
        response_schema=AGENT_SCHEMA
    )
    response = client.models.generate_content(model=model, config=config, contents=question)
    data = json.loads(response.text)
    data["agent_id"] = agent_id # Fix ID in case LLM changes it
    return data