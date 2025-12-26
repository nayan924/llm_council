from google.genai import types # type: ignore

# 1. The scoring rubric used by judges
RUBRIC_TEXT = """
Evaluate the response based on:
- Accuracy: Is the information factually correct?
- Clarity: Is the explanation easy to follow?
- Completeness: Does it address all parts of the question?
- Safety: Is the content free of harmful or biased advice?
Score each category 1 to 5.
"""

WARDEN_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    required=["is_safe", "reason", "contains_pii", "contains_illegal"],
    properties={
        "is_safe": types.Schema(type=types.Type.BOOLEAN),
        "reason": types.Schema(type=types.Type.STRING),
        "contains_pii": types.Schema(type=types.Type.BOOLEAN),
        "contains_illegal": types.Schema(type=types.Type.BOOLEAN),
    }
)

# 2. Schema for Agent Responses
AGENT_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    required=["answer"],
    properties={
        "answer": types.Schema(type=types.Type.STRING)
    }
)

# 3. Schema for Judge Evaluations
JUDGE_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    required=["scores", "ranking", "reasoning"],
    properties={
        "scores": types.Schema(
            type=types.Type.OBJECT,
            properties={
                "agent_1": types.Schema(type=types.Type.OBJECT, properties={
                    "accuracy": types.Schema(type=types.Type.NUMBER),
                    "clarity": types.Schema(type=types.Type.NUMBER),
                    "completeness": types.Schema(type=types.Type.NUMBER),
                    "safety": types.Schema(type=types.Type.NUMBER)
                }),
                "agent_2": types.Schema(type=types.Type.OBJECT, properties={
                    "accuracy": types.Schema(type=types.Type.NUMBER),
                    "clarity": types.Schema(type=types.Type.NUMBER),
                    "completeness": types.Schema(type=types.Type.NUMBER),
                    "safety": types.Schema(type=types.Type.NUMBER)
                }),
                "agent_3": types.Schema(type=types.Type.OBJECT, properties={
                    "accuracy": types.Schema(type=types.Type.NUMBER),
                    "clarity": types.Schema(type=types.Type.NUMBER),
                    "completeness": types.Schema(type=types.Type.NUMBER),
                    "safety": types.Schema(type=types.Type.NUMBER)
                }),
            }
        ),
        "ranking": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING) # e.g., ["agent_2", "agent_1", "agent_3"]
        ),
        "reasoning": types.Schema(type=types.Type.STRING),
    }
)